import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/mirror_gitlab_to_github.py"

def git(cwd,*args):
    return subprocess.run(["git",*args],cwd=cwd,text=True,capture_output=True,check=True)

class MirrorTests(unittest.TestCase):
    def test_initial_and_fast_forward_mirror(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/"src"; dst=td/"dst.git"; src.mkdir()
            git(src,"init","-b","main"); git(src,"config","user.name","test"); git(src,"config","user.email","operator@example.com")
            (src/"README.md").write_text("one\n"); git(src,"add","."); git(src,"commit","-m","one")
            git(td,"init","--bare",str(dst))
            for value in ("one\n","two\n"):
                if (src/"README.md").read_text()!=value:
                    (src/"README.md").write_text(value); git(src,"add","."); git(src,"commit","-m","advance")
                oid=git(src,"rev-parse","HEAD").stdout.strip()
                receipt=td/"receipt.json"
                receipt.write_text(json.dumps({"classification":"public","source_revision":oid,"gates":{"repository":"pass","tests":"pass","policy":"pass","sanitization":"pass"}}))
                proc=subprocess.run(["python3",str(SCRIPT),"--source",str(src),"--destination",str(dst),"--receipt",str(receipt),"--expected-oid",oid],text=True,capture_output=True)
                self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
                self.assertEqual(oid,git(td,"--git-dir",str(dst),"rev-parse","main").stdout.strip())

if __name__=="__main__": unittest.main()
