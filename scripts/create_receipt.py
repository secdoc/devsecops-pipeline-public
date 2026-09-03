#!/usr/bin/env python3
"""Create a digest-bound synthetic release receipt."""
import argparse,datetime as dt,hashlib,json,subprocess
from pathlib import Path
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def sha256(path): return digest(path)
def create_receipt(artifact,sbom,source_revision='UNCOMMITTED',created_at=None):
 return {'schema_version':1,'classification':'public','synthetic':True,'source':'generated','source_revision':source_revision,'created_at':created_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),'artifact':{'sha256':digest(artifact)},'sbom':{'sha256':digest(sbom)},'gates':{'repository':'pass','tests':'pass','policy':'pass','sanitization':'pass'}}
def create(artifact,sbom,source_revision='UNCOMMITTED'):
 doc=json.loads(Path(sbom).read_text())
 if doc.get('bomFormat')!='CycloneDX': raise ValueError('SBOM is not CycloneDX')
 r=create_receipt(artifact,sbom,source_revision)
 r['artifact_sha256']=r['artifact']['sha256']; r['sbom_sha256']=r['sbom']['sha256']
 return r
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--artifact',required=True); ap.add_argument('--sbom',required=True); ap.add_argument('--output',required=True); ap.add_argument('--source-revision'); a=ap.parse_args()
 rev=a.source_revision
 if not rev:
  p=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True); rev=p.stdout.strip() if p.returncode==0 else 'UNCOMMITTED'
 out=create(a.artifact,a.sbom,rev); Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(a.output)
if __name__=='__main__': raise SystemExit(main())
