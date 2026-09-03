import json,subprocess,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
class DiagramTests(unittest.TestCase):
 def test_specs_and_outputs(self):
  subprocess.run([sys.executable,'scripts/render_architecture.py'],check=True,capture_output=True)
  specs=sorted(Path('docs/architecture/specs').glob('*.json'));self.assertEqual(len(specs),4)
  for spec in specs:
   doc=json.loads(spec.read_text());self.assertTrue(doc['synthetic']);svg=spec.parent.parent/(spec.stem+'.svg');self.assertTrue(svg.exists());self.assertLess(svg.stat().st_size,30000);root=ET.parse(svg).getroot();self.assertEqual(root.get('viewBox'),'0 0 1600 900')
 def test_nonadjacent_same_column_flow_routes_around_nodes(self):
  subprocess.run([sys.executable,'scripts/render_architecture.py'],check=True,capture_output=True)
  svg=Path('docs/architecture/trust-boundaries.svg').read_text()
  self.assertIn('M 773.0 586.0 H 783.0 V 256.0 H 773.0',svg)
  self.assertNotIn('M 608.5 530.0 V 312.0',svg)
if __name__=='__main__': unittest.main()
