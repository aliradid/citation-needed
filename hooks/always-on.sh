#!/usr/bin/env sh
# SessionStart hook: injects the full citation-needed ruleset when the user has
# opted in by creating $CLAUDE_CONFIG_DIR/.citation-needed-always (default ~/.claude).
# POSIX fallback for environments without Node. Never blocks session start.

claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
flag_path="$claude_dir/.citation-needed-always"

[ -f "$flag_path" ] || exit 0

script_dir=$(dirname -- "$0")
skill_path="$script_dir/../skills/citation-needed/SKILL.md"
[ -f "$skill_path" ] || exit 0

# Strip a leading YAML frontmatter block only if it is properly closed.
body=$(awk '
  NR == FNR {
    if (NR == 1 && $0 ~ /^---[[:space:]]*$/) { in_fm = 1; next }
    if (in_fm && $0 ~ /^---[[:space:]]*$/)   { in_fm = 0; closed = 1 }
    next
  }
  FNR == 1 { strip = closed }
  strip && FNR == 1 && $0 ~ /^---[[:space:]]*$/ { skipping = 1; next }
  skipping && $0 ~ /^---[[:space:]]*$/          { skipping = 0; next }
  !skipping { print }
' "$skill_path" "$skill_path") || exit 0

printf 'CITATION-NEEDED GUARD ACTIVE (always-on). The rules below apply to every response. "stop citation-needed" turns it off for this session; delete %s to turn always-on off for good.\n\n%s\n' \
  "$flag_path" "$body"
