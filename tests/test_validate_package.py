"""Observable malformed-package checks for the read-only validator."""

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_package", ROOT / "scripts" / "validate_package.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "reflect-and-apply"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"),
        )

    def errors(self):
        return VALIDATOR.validate(self.root)

    def test_distribution_is_valid_and_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(self.errors(), [])
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_missing_reference_is_rejected(self):
        (self.root / "references" / "decision-guide.md").unlink()
        self.assertTrue(any("broken link" in e for e in self.errors()))

    def test_malformed_frontmatter_is_rejected(self):
        (self.root / "SKILL.md").write_text("# Missing YAML\n", encoding="utf-8")
        self.assertTrue(any("frontmatter" in e for e in self.errors()))

    def test_wrong_skill_name_is_rejected(self):
        path = self.root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "name: reflect-and-apply", "name: wrong-name", 1), encoding="utf-8")
        self.assertTrue(any("skill name" in e for e in self.errors()))

    def test_invalid_ui_policy_is_rejected(self):
        path = self.root / "agents" / "openai.yaml"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "allow_implicit_invocation: true", 'allow_implicit_invocation: "true"'),
            encoding="utf-8")
        self.assertTrue(any("boolean" in e for e in self.errors()))

    def test_unclosed_fence_is_rejected(self):
        path = self.root / "README.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\n```text\nnever closed\n")
        self.assertTrue(any("unclosed fence" in e for e in self.errors()))

    def test_local_link_outside_package_is_rejected(self):
        path = self.root / "README.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\n[escape](../outside.md)\n")
        self.assertTrue(any("outside package" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
