import datetime as dt,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_release import evaluate
class PolicyTests(unittest.TestCase):
 def setUp(self):
  self.p=json.loads(Path('policies/release-policy.json').read_text());self.base={'artifact_sha256':'a'*64,'scanners':{'s':'1'},'findings':[]}
 def test_medium_visible_but_allowed(self):
  d=self.base|{'findings':[{'scanner':'s','vulnerability':'CVE-X','component':'c','severity':'medium','known_exploited':False,'fix_available':False}]};self.assertEqual(evaluate(self.p,d,{'exceptions':[]})['decision'],'allow')
 def test_critical_blocks(self):
  d=self.base|{'findings':[{'scanner':'s','vulnerability':'CVE-X','component':'c','severity':'critical','known_exploited':False,'fix_available':False}]};self.assertEqual(evaluate(self.p,d,{'exceptions':[]})['decision'],'deny')
 def test_self_approval_blocks_even_unused(self):
  e={'id':'EX-1','scanner':'s','vulnerability':'CVE-X','component':'c','artifact_sha256':'a'*64,'owner':'same','approver':'same','expires_at':'2099-01-01T00:00:00Z'};self.assertIn('SELF_APPROVED_EXCEPTION:EX-1',evaluate(self.p,self.base,{'exceptions':[e]},dt.datetime(2026,1,1,tzinfo=dt.timezone.utc))['reason_codes'])
if __name__=='__main__': unittest.main()
