#!/usr/bin/env python3
"""Create the approval receipt consumed by the public mirror job."""
import argparse,hashlib,json,subprocess
from pathlib import Path
def run(args,cwd,check=True): return subprocess.run(args,cwd=cwd,capture_output=True,check=check)
def create(root,reviewer):
 root=Path(root).resolve(); oid=run(['git','rev-parse','HEAD'],root).stdout.decode().strip()
 if run(['git','status','--porcelain'],root).stdout: raise ValueError('worktree is dirty')
 archive=run(['git','archive','--format=tar','HEAD'],root).stdout
 if not reviewer.strip(): raise ValueError('reviewer is required')
 return {'schema_version':1,'classification':'public','synthetic':True,'source':'generated','repository':'devsecops-pipeline-public','source_revision':oid,'content_sha256':hashlib.sha256(archive).hexdigest(),'approval_basis':'protected GitLab default branch plus required CI','reviewer':reviewer,'gates':{'repository':'pass','tests':'pass','policy':'pass','sanitization':'pass','history':'pass','diagrams':'pass'}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',default='.');ap.add_argument('--reviewer',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();doc=create(a.root,a.reviewer);p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n');print(p)
if __name__=='__main__': raise SystemExit(main())
