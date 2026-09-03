import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_linkage import validate
class LinkageTests(unittest.TestCase):
 def test_manifest(self): self.assertEqual(validate(json.loads(Path('integrations/soc-pipeline-public.json').read_text())),[])
 def test_wrong_repo(self):
  d=json.loads(Path('integrations/soc-pipeline-public.json').read_text());d['repository']='https://github.com/example/wrong';self.assertIn('unexpected repository',validate(d))
if __name__=='__main__': unittest.main()
