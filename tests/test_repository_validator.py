import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_repository import scan_text
class ValidatorTests(unittest.TestCase):
 def test_private_address_rejected(self):
  issues=[];scan_text('x','connect to '+'10.20.'+'30.40',issues);self.assertTrue(any('NON_DOCUMENTATION_IPV4' in x for x in issues))
 def test_documentation_address_allowed(self):
  issues=[];scan_text('x','use 192.0.2.10',issues);self.assertFalse(any('NON_DOCUMENTATION_IPV4' in x for x in issues))
 def test_private_key_rejected(self):
  issues=[];scan_text('x','-----BEGIN PRIVATE'+' KEY-----',issues);self.assertTrue(any('PRIVATE_KEY' in x for x in issues))
if __name__=='__main__': unittest.main()
