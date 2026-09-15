"""The Node and POSIX sh always-on hooks must behave identically."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks"
SKILL = ROOT / "skills" / "citation-needed" / "SKILL.md"


def run_hook(kind: str, config_dir: str) -> str:
    env = dict(os.environ, CLAUDE_CONFIG_DIR=config_dir)
    if kind == "node":
        cmd = ["node", str(HOOKS / "always-on.mjs")]
    else:
        cmd = ["sh", str(HOOKS / "always-on.sh")]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def expected_body() -> str:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.index("\n---\n", 4)
    return text[end + 5 :].rstrip("\n")


class AlwaysOnHookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="cn-hook-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def kinds(self):
        kinds = []
        if shutil.which("node"):
            kinds.append("node")
        if shutil.which("sh") and sys.platform != "win32":
            kinds.append("sh")
        if not kinds:
            self.skipTest("neither node nor sh available")
        return kinds

    def test_silent_without_flag(self):
        for kind in self.kinds():
            self.assertEqual(run_hook(kind, self.tmp), "", kind)

    def test_injects_body_without_frontmatter_when_flagged(self):
        Path(self.tmp, ".citation-needed-always").touch()
        outputs = {}
        for kind in self.kinds():
            out = run_hook(kind, self.tmp)
            outputs[kind] = out
            self.assertTrue(out.startswith("CITATION-NEEDED GUARD ACTIVE (always-on)."), kind)
            self.assertNotIn("\nname: citation-needed\n", out, kind)
            self.assertIn(expected_body(), out, kind)
            self.assertIn(os.path.join(self.tmp, ".citation-needed-always"), out, kind)
        if len(outputs) == 2:
            self.assertEqual(outputs["node"], outputs["sh"], "node and sh hooks diverge")


if __name__ == "__main__":
    unittest.main()
