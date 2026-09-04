import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "trufflehog_report.py"
TOOLCHAIN = ROOT / ".gitlab" / "security-toolchain.yml"


def load_target():
    spec = importlib.util.spec_from_file_location("trufflehog_report", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(MODULE)
    target = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(target)
    return target


class TruffleHogTests(unittest.TestCase):
    def test_pipeline_scans_git_history_and_immutable_snapshot(self):
        pipeline = TOOLCHAIN.read_text(encoding="utf-8")
        self.assertIn("trufflehog-source:", pipeline)
        self.assertIn("trufflehog-snapshot:", pipeline)
        self.assertIn("--no-verification", pipeline)
        self.assertIn("--no-update", pipeline)
        self.assertIn("scripts/trufflehog_report.py", pipeline)
        self.assertIn("artifacts/trufflehog-source.json", pipeline)
        self.assertIn("artifacts/trufflehog-snapshot.json", pipeline)
        self.assertNotIn("allow_failure: true", pipeline)
        self.assertNotIn("raw.json", pipeline)

    def test_report_excludes_candidate_secret_material(self):
        target = load_target()
        with tempfile.TemporaryDirectory() as value:
            raw = Path(value) / "raw.jsonl"
            raw.write_text(json.dumps({
                "DetectorName": "Example",
                "DetectorType": 1,
                "Verified": False,
                "Raw": "candidate-value",
                "RawV2": "candidate-value-v2",
                "SecretParts": {"token": "candidate-part"},
                "ExtraData": {"unsafe": "candidate-extra"},
                "SourceMetadata": {"Data": {"Git": {
                    "file": "config/example.env",
                    "line": 7,
                    "commit": "a" * 40,
                    "email": "author@example.invalid",
                }}},
            }) + "\n", encoding="utf-8")
            report = target.build_report(
                raw,
                scope="git-history",
                scanner_exit_code=183,
                scanner_version="operator-pinned",
                source_commit="b" * 40,
            )
        serialized = json.dumps(report, sort_keys=True)
        self.assertEqual(report["status"], "findings")
        self.assertEqual(report["finding_count"], 1)
        self.assertNotIn("candidate-value", serialized)
        self.assertNotIn("author@example.invalid", serialized)
        self.assertEqual(report["findings"][0]["file"], "config/example.env")


if __name__ == "__main__":
    unittest.main()
