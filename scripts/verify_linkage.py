#!/usr/bin/env python3
"""Verify the declared SOC pipeline relationship, optionally against GitHub."""
import argparse,json,urllib.error,urllib.request
from pathlib import Path
def validate(doc):
 issues=[]
 for k in ('name','repository','git_url','default_ref','relationship','required_files'):
  if not doc.get(k): issues.append('missing '+k)
 if doc.get('repository')!='https://github.com/secdoc/soc-pipeline-public': issues.append('unexpected repository')
 if not isinstance(doc.get('required_files'),list): issues.append('required_files is not a list')
 return issues
def validate_manifest(path):
 doc=json.loads(Path(path).read_text()); issues=validate(doc)
 if issues: raise ValueError('; '.join(issues))
 return doc
def live(doc):
 headers={'Accept':'application/vnd.github+json','User-Agent':'devsecops-pipeline-public'}
 req=urllib.request.Request('https://api.github.com/repos/secdoc/soc-pipeline-public',headers=headers)
 with urllib.request.urlopen(req,timeout=20) as r: meta=json.load(r)
 issues=[]
 if meta.get('visibility')!='public': issues.append('linked repository is not public')
 if meta.get('default_branch')!=doc['default_ref']: issues.append('default branch mismatch')
 for f in doc['required_files']:
  url='https://api.github.com/repos/secdoc/soc-pipeline-public/contents/'+f+'?ref='+doc['default_ref']
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as r:
    if r.status!=200: issues.append('missing live file '+f)
  except urllib.error.HTTPError as e: issues.append(f'live file {f} returned {e.code}')
 return issues
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--manifest',default='integrations/soc-pipeline-public.json'); ap.add_argument('--live',action='store_true'); a=ap.parse_args(); doc=json.loads(Path(a.manifest).read_text()); issues=validate(doc)+(live(doc) if a.live else [])
 if issues: print('\n'.join('FAIL '+x for x in issues)); raise SystemExit(2)
 print('PASS SOC pipeline linkage'+(' live' if a.live else ' manifest'))
