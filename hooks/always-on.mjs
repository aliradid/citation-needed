// SessionStart hook: injects the full citation-needed ruleset when the user has
// opted in by creating $CLAUDE_CONFIG_DIR/.citation-needed-always (default ~/.claude).
// Never blocks session start: any failure exits 0.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

try {
  const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const flagPath = path.join(claudeDir, ".citation-needed-always");

  if (!fs.existsSync(flagPath)) process.exit(0);

  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const skillPath = path.join(scriptDir, "..", "skills", "citation-needed", "SKILL.md");
  if (!fs.existsSync(skillPath)) process.exit(0);

  const body = fs
    .readFileSync(skillPath, "utf8")
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, "")
    .replace(/(?:\r?\n)+$/, "");

  process.stdout.write(
    "CITATION-NEEDED GUARD ACTIVE (always-on). The rules below apply to every response. " +
      '"stop citation-needed" turns it off for this session; ' +
      `delete ${flagPath} to turn always-on off for good.\n\n${body}\n`,
  );
} catch {
  process.exit(0);
}
