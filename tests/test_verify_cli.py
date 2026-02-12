import subprocess
import sys
from pathlib import Path
import unittest


class TestVerifyCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.python = sys.executable
        cls.verify = cls.root / "sie_verify.py"
        cls.env_file = cls.root / "SKILL.md.sie.json"
        cls.skill_file = cls.root / "SKILL.md"
        cls.keyring = cls.root / "trusted_issuers.json"

    def run_cmd(self, *args):
        return subprocess.run(
            [self.python, str(self.verify), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def test_verify_ok_with_trusted_issuers(self):
        r = self.run_cmd(
            "--file", str(self.env_file),
            "--trusted-issuers", str(self.keyring),
        )
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    def test_verify_ok_with_check_file(self):
        r = self.run_cmd(
            "--file", str(self.env_file),
            "--trusted-issuers", str(self.keyring),
            "--check-file", str(self.skill_file),
        )
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    def test_untrusted_issuer_fails(self):
        bad_keyring = self.root / "tests" / "tmp_bad_issuers.json"
        bad_keyring.write_text("{}", encoding="utf-8")
        try:
            r = self.run_cmd(
                "--file", str(self.env_file),
                "--trusted-issuers", str(bad_keyring),
            )
            self.assertNotEqual(r.returncode, 0)
        finally:
            bad_keyring.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
