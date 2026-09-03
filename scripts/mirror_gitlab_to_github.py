#!/usr/bin/env python3
"""Publish one approved GitLab commit to one GitHub main branch."""
import argparse,json,subprocess,sys
from pathlib import Path
def run(args,cwd,check=True): return subprocess.run(args,cwd=cwd,text=True,capture_output=True,check=check)
def mirror(source,destination,oid=None):
 root=Path(source).resolve(); oid=oid or run(['git','rev-parse','HEAD'],root).stdout.strip()
 if run(['git','status','--porcelain'],root).stdout: raise ValueError('source worktree is dirty')
 remote=run(['git','ls-remote','--heads',destination],root,False)
 if remote.returncode: raise ValueError('destination readback failed')
 heads={line.split()[1]:line.split()[0] for line in remote.stdout.splitlines() if line.split()}
 if set(heads)-{'refs/heads/main'}: raise ValueError('destination has unexpected branches')
 prior=heads.get('refs/heads/main')
 if prior and run(['git','merge-base','--is-ancestor',prior,oid],root,False).returncode: raise ValueError('destination diverged from GitLab')
 push=run(['git','push','--atomic',destination,f'{oid}:refs/heads/main'],root,False)
 if push.returncode: raise ValueError('mirror push rejected')
 verify=run(['git','ls-remote','--heads',destination,'refs/heads/main'],root,False)
 got=verify.stdout.split()[0] if verify.returncode==0 and verify.stdout.split() else ''
 if got!=oid: raise ValueError('GitHub OID readback mismatch')
 return {'status':'verified','source_oid':oid,'destination_oid':got,'prior_oid':prior}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--source',default='.'); ap.add_argument('--destination',required=True); ap.add_argument('--receipt',required=True); ap.add_argument('--expected-oid',required=True); a=ap.parse_args()
 root=Path(a.source).resolve(); receipt=json.loads(Path(a.receipt).read_text()); oid=run(['git','rev-parse','HEAD'],root).stdout.strip()
 if oid!=a.expected_oid or receipt.get('source_revision')!=oid: print('FAIL source OID or receipt mismatch'); return 2
 if receipt.get('classification')!='public' or any(v!='pass' for v in receipt.get('gates',{}).values()): print('FAIL release receipt is not approved public state'); return 2
 if run(['git','status','--porcelain'],root).stdout: print('FAIL source worktree is dirty'); return 2
 try: result=mirror(root,a.destination,oid)
 except ValueError as e: print('FAIL '+str(e)); return 2
 print('PASS mirrored approved main OID '+result['destination_oid']); return 0
if __name__=='__main__': raise SystemExit(main())
