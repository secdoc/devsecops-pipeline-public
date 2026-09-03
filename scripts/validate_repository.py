#!/usr/bin/env python3
"""Fail-closed validation for a public-only repository."""
from __future__ import annotations
import argparse, ipaddress, json, os, re, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

FORBIDDEN_EXTENSIONS={'.7z','.bak','.cer','.crt','.csr','.db','.der','.gz','.jks','.key','.kubeconfig','.log','.p12','.pcap','.pem','.pfx','.png','.pdf','.sqlite','.tar','.tgz','.zip'}
FORBIDDEN_DIRS={'evidence','exports','logs','reports','backups','snapshots'}
TEXT_EXTENSIONS={'.css','.gitignore','.html','.ini','.json','.md','.py','.service','.sh','.svg','.timer','.toml','.txt','.yaml','.yml',''}
REQUIRED={'README.md','LICENSE','LICENSE-docs','LICENSING.md','NOTICE','docs/SANITIZATION.md','.gitlab-ci.yml','.github/workflows/validate.yml'}
PATTERNS=[
 ('PRIVATE_KEY',re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE' + r' KEY-----')),
 ('CERTIFICATE',re.compile(r'-----BEGIN CERTI' + r'FICATE-----')),
 ('INTERNAL_DOMAIN',re.compile(r'(?i)(?:[a-z0-9-]+\.)+(?:home|internal|lan|local)\b')),
 ('TOKEN_ASSIGNMENT',re.compile(r'(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)\s*[:=]\s*["\']?[A-Za-z0-9_./+=-]{12,}')),
 ('GITHUB_TOKEN',re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b')),
 ('GITLAB_TOKEN',re.compile(r'\bglpat-[A-Za-z0-9_-]{20,}\b')),
 ('AWS_KEY',re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
 ('MAC_ADDRESS',re.compile(r'(?i)\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b')),
 ('LIVE_VM_ID',re.compile(r'(?i)\bvm(?:id)?[-_ ]?[0-9]{2,}\b')),
 ('EM_DASH',re.compile('\u2014')),
]
URL_RE=re.compile(r'https?://[^\s)\]>"\']+')
IPV4_RE=re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?![\w.])')
EMAIL_RE=re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
ALLOWED_EMAILS={'55542561+secdoc@users.noreply.github.com','operator@example.com','git@github.com'}
ALLOWED_DOC_NETS=[ipaddress.ip_network(x) for x in ('192.0.2.0/24','198.51.100.0/24','203.0.113.0/24')]


def tracked(root:Path):
 p=subprocess.run(['git','ls-files','-z'],cwd=root,capture_output=True,check=True)
 return [root/Path(x.decode()) for x in p.stdout.split(b'\0') if x]

def scan_text(label:str,text:str,issues:list[str]):
 for name,rx in PATTERNS:
  for m in rx.finditer(text): issues.append(f'{label}: {name} at character {m.start()}')
 for m in IPV4_RE.finditer(text):
  raw=m.group().split('/')[0]
  try: ip=ipaddress.ip_address(raw)
  except ValueError: continue
  if not any(ip in n for n in ALLOWED_DOC_NETS): issues.append(f'{label}: NON_DOCUMENTATION_IPV4 {m.group()}')
 for email in EMAIL_RE.findall(text):
  if email.lower() not in ALLOWED_EMAILS and not email.lower().endswith(('@example.com','@example.invalid')):
   issues.append(f'{label}: NONPUBLIC_EMAIL {email}')
 for url in URL_RE.findall(text):
  host=(urlparse(url.rstrip('.,;')).hostname or '').lower()
  if host and (host.endswith(('.home','.internal','.lan','.local')) or host in {'localhost'}):
   issues.append(f'{label}: NONPUBLIC_URL_HOST {host}')

def validate(root:Path,history:bool=False)->list[str]:
 issues=[]
 files=tracked(root)
 names={str(p.relative_to(root)) for p in files}
 for required in sorted(REQUIRED-names): issues.append(f'missing required file: {required}')
 for p in files:
  rel=str(p.relative_to(root)); parts=set(p.relative_to(root).parts)
  if p.is_symlink(): issues.append(f'{rel}: symlink is prohibited'); continue
  if parts & FORBIDDEN_DIRS: issues.append(f'{rel}: prohibited directory class')
  if p.suffix.lower() in FORBIDDEN_EXTENSIONS: issues.append(f'{rel}: prohibited extension')
  if p.name=='.env' or p.name.startswith('.env.') and p.name!='.env.example': issues.append(f'{rel}: environment file is prohibited')
  try: size=p.stat().st_size
  except OSError as e: issues.append(f'{rel}: unreadable: {e}'); continue
  if size>1_000_000: issues.append(f'{rel}: file exceeds 1 MB')
  try: data=p.read_bytes()
  except OSError as e: issues.append(f'{rel}: unreadable: {e}'); continue
  if b'\0' in data: issues.append(f'{rel}: opaque binary content is prohibited'); continue
  if p.suffix.lower() in TEXT_EXTENSIONS or p.name in {'LICENSE','NOTICE'}:
   try: text=data.decode('utf-8')
   except UnicodeDecodeError: issues.append(f'{rel}: text is not UTF-8'); continue
   scan_text(rel,text,issues)
   if p.suffix=='.json':
    try: obj=json.loads(text)
    except json.JSONDecodeError as e: issues.append(f'{rel}: malformed JSON: {e}')
    else:
     if rel.startswith('examples/') and isinstance(obj,dict):
      if obj.get('synthetic') is not True or obj.get('source')!='generated': issues.append(f'{rel}: JSON fixture lacks synthetic provenance')
   if p.suffix=='.svg':
    try: svg=ET.fromstring(text)
    except ET.ParseError as e: issues.append(f'{rel}: malformed SVG: {e}')
    else:
     tag=lambda n:f'{{http://www.w3.org/2000/svg}}{n}'
     for attr in ('width','height','viewBox'):
      if not svg.get(attr): issues.append(f'{rel}: SVG missing {attr}')
     if svg.find(tag('title')) is None or svg.find(tag('desc')) is None: issues.append(f'{rel}: SVG missing title or desc')
     for attr in ('href','{http://www.w3.org/1999/xlink}href'):
      for node in svg.iter():
       if node.get(attr,'').startswith(('http:','https:','file:')): issues.append(f'{rel}: external SVG reference')
   if p.suffix=='.md':
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
     if target.startswith(('#','http://','https://','mailto:')): continue
     local=(p.parent/target.split('#',1)[0]).resolve()
     if target and not local.exists(): issues.append(f'{rel}: broken relative link {target}')
 if history:
  proc=subprocess.run(['git','log','--all','--format=commit:%H%n%B','-p','--no-ext-diff','--binary'],cwd=root,capture_output=True)
  if proc.returncode: issues.append('unable to scan Git history')
  else:
   text=proc.stdout.decode('utf-8','replace')
   scan_text('GIT_HISTORY',text,issues)
   if ('GIT binary' + ' patch') in text: issues.append('GIT_HISTORY: binary content is prohibited')
 return sorted(set(issues))

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); ap.add_argument('--history',action='store_true'); args=ap.parse_args()
 issues=validate(Path(args.root).resolve(),args.history)
 if issues:
  print('\n'.join(f'FAIL {x}' for x in issues)); return 2
 print('PASS public repository validation'); return 0
if __name__=='__main__': raise SystemExit(main())
