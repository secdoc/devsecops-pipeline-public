#!/usr/bin/env python3
"""Normalize release findings and apply a fail-closed policy."""
import argparse,datetime as dt,json
from pathlib import Path
REQ=('scanner','vulnerability','component','severity','known_exploited','fix_available')
def load(p): return json.loads(Path(p).read_text())
def evaluate(policy_doc, findings_doc, exceptions_doc, now=None):
 now=now or dt.datetime.now(dt.timezone.utc); reasons=[]
 artifact=findings_doc.get('artifact_sha256','')
 if len(artifact)!=64: reasons.append('MISSING_OR_INVALID_ARTIFACT_HASH')
 findings=findings_doc.get('findings'); scanners=findings_doc.get('scanners')
 if not isinstance(findings,list) or not isinstance(scanners,dict) or not scanners: reasons.append('MISSING_OR_MALFORMED_EVIDENCE'); findings=[]
 exceptions=exceptions_doc.get('exceptions',[])
 if not isinstance(exceptions,list): reasons.append('MALFORMED_EXCEPTION_INVENTORY'); exceptions=[]
 valid=[]
 required=policy_doc.get('required_match_fields',[])
 for i,e in enumerate(exceptions):
  if not isinstance(e,dict) or any(not e.get(k) for k in required+['owner','approver','expires_at','id']): reasons.append(f'INVALID_EXCEPTION:{i}'); continue
  if e['owner']==e['approver']: reasons.append(f'SELF_APPROVED_EXCEPTION:{e["id"]}'); continue
  try: expiry=dt.datetime.fromisoformat(e['expires_at'].replace('Z','+00:00'))
  except Exception: reasons.append(f'INVALID_EXCEPTION_EXPIRY:{e["id"]}'); continue
  if expiry<=now: reasons.append(f'EXPIRED_EXCEPTION:{e["id"]}'); continue
  if (expiry-now).days>policy_doc.get('exception_max_days',30): reasons.append(f'EXCEPTION_TOO_LONG:{e["id"]}'); continue
  valid.append(e)
 def excepted(f): return any(all(e.get(k)==(artifact if k=='artifact_sha256' else f.get(k)) for k in required) for e in valid)
 blocked=[]
 for i,f in enumerate(findings):
  if any(k not in f for k in REQ): reasons.append(f'MALFORMED_FINDING:{i}'); continue
  sev=str(f['severity']).lower()
  should=(sev in policy_doc['block']['severities'] or (policy_doc['block']['known_exploited'] and f['known_exploited']) or (sev in policy_doc['block']['fixable_severities'] and f['fix_available']))
  if should and not excepted(f): blocked.append(f'{f["vulnerability"]}:{f["component"]}')
 if blocked: reasons.extend('BLOCKING_FINDING:'+x for x in blocked)
 return {'decision':'deny' if reasons else 'allow','artifact_sha256':artifact,'reason_codes':sorted(reasons),'blocking_findings':blocked,'valid_exception_ids':sorted(e['id'] for e in valid)}
def main():
 ap=argparse.ArgumentParser(); [ap.add_argument(x,required=True) for x in ('--policy','--findings','--exceptions')]; a=ap.parse_args()
 r=evaluate(load(a.policy),load(a.findings),load(a.exceptions)); print(json.dumps(r,indent=2,sort_keys=True)); return 0 if r['decision']=='allow' else 2
if __name__=='__main__': raise SystemExit(main())
