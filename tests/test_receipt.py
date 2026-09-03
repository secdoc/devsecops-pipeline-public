import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from create_receipt import create
class ReceiptTests(unittest.TestCase):
 def test_hash_binding(self):
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'a';s=Path(d)/'s.json';a.write_text('x');s.write_text(json.dumps({'bomFormat':'CycloneDX'}));r=create(a,s,'abc');self.assertEqual(r['artifact_sha256'],hashlib.sha256(b'x').hexdigest());self.assertEqual(r['source_revision'],'abc')
 def test_reject_non_cyclonedx(self):
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'a';s=Path(d)/'s.json';a.write_text('x');s.write_text('{}');
   with self.assertRaises(ValueError): create(a,s)
if __name__=='__main__': unittest.main()
