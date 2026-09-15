"""Manifests, mirrors and docs must agree with the canonical skill."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "citation-needed" / "SKILL.md"
NAME = "citation-needed"

JSON_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "gemini-extension.json",
    "qwen-extension.json",
    "kimi.plugin.json",
    "plugin.json",
    "opencode.json",
    "hooks/hooks.json",
]
VERSIONED = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "gemini-extension.json",
    "qwen-extension.json",
    "kimi.plugin.json",
    "plugin.json",
]


def skill_version() -> str:
    text = SKILL.read_text(encoding="utf-8")
    m = re.search(r'^\s*version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', text, re.MULTILINE)
    assert m, "SKILL.md frontmatter needs metadata.version"
    return m.group(1)


class ManifestTests(unittest.TestCase):
    def test_all_json_manifests_parse(self):
        for rel in JSON_MANIFESTS:
            with self.subTest(rel):
                json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_names_match(self):
        for rel in JSON_MANIFESTS:
            data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            if "name" in data:
                self.assertEqual(data["name"], NAME, rel)
            for p in data.get("plugins", []):
                self.assertEqual(p["name"], NAME, rel)

    def test_versions_aligned_with_skill(self):
        v = skill_version()
        for rel in VERSIONED:
            data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            self.assertEqual(data.get("version"), v, rel)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## [{v}]", changelog, "CHANGELOG.md needs an entry for the current version")

    def test_cursor_mirror_in_sync(self):
        mirror = ROOT / ".cursor" / "skills" / NAME / "SKILL.md"
        self.assertEqual(mirror.read_text(encoding="utf-8"), SKILL.read_text(encoding="utf-8"))

    def test_skill_frontmatter(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIsNotNone(re.search(r"^name: citation-needed$", text, re.MULTILINE))
        self.assertIn("description:", text)
        self.assertNotIn("disable-model-invocation: true", text, "guard mode needs model invocation")

    def test_skill_references_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        for ref in re.findall(r"`references/([a-z\-]+\.md)`", text):
            self.assertTrue((SKILL.parent / "references" / ref).exists(), ref)

    def test_statuses_agree_between_skill_and_validator(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_report import STATUSES
        text = SKILL.read_text(encoding="utf-8")
        table = text[text.index("| Status | Meaning |"):]
        listed = set(re.findall(r"^\| ([A-Z]+) \|", table, re.MULTILINE))
        self.assertEqual(listed, STATUSES)

    def test_gemini_context_file_exists(self):
        data = json.loads((ROOT / "gemini-extension.json").read_text(encoding="utf-8"))
        ctx = ROOT / data["contextFileName"]
        self.assertTrue(ctx.exists())
        self.assertIn("@./skills/citation-needed/SKILL.md", ctx.read_text(encoding="utf-8"))

    def test_opencode_plugin_path_exists(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        for p in data["plugin"]:
            self.assertTrue((ROOT / p).exists(), p)

    def test_install_docs_mention_every_platform(self):
        install = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
        for platform in ["Claude Code", "Codex", "Cursor", "Gemini CLI", "OpenCode", "Kimi", "Qwen", "Copilot", "Zed"]:
            self.assertIn(platform, install, platform)


if __name__ == "__main__":
    unittest.main()
