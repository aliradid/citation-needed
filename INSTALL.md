# Install

One skill, many harnesses. Pick yours. Every route loads the same
`skills/citation-needed/SKILL.md`.

After installing, type `/citation-needed` (or `$citation-needed` in Codex) and paste or
point at a draft. Say "stop citation-needed" to turn it off.

## Claude Code

```bash
claude plugin marketplace add aliradid/citation-needed
claude plugin install citation-needed@citation-needed
```

Then `/citation-needed` inside a session. Claude also invokes the skill on its own when
you ask it to fact-check something, and in guard mode when it writes publishable text.

**Always-on guard** (rules injected into every session):

```bash
touch ~/.claude/.citation-needed-always
```

Remove the file to turn it off. Respects `CLAUDE_CONFIG_DIR`.

**Manual fallback** (no plugin system):

```bash
git clone https://github.com/aliradid/citation-needed ~/.claude/skills/citation-needed-src
ln -s ~/.claude/skills/citation-needed-src/skills/citation-needed ~/.claude/skills/citation-needed
```

## Codex

```bash
codex plugin marketplace add aliradid/citation-needed --ref main
codex plugin add citation-needed@citation-needed
```

Then `$citation-needed` in a prompt.

**Always-on:** add this to `~/.codex/AGENTS.md`:

```markdown
Before delivering any article, script, post, report, or other publishable text that
states facts, apply the citation-needed skill: verify every check-worthy claim with web
search, cite only URLs returned by a tool, and mark anything unverified in place.
```

## Cursor (and other harnesses that read `~/.cursor/skills` or `.agents/skills`)

```bash
npx skills add aliradid/citation-needed -a cursor -y
```

Or copy `skills/citation-needed/` into `~/.cursor/skills/`. Type `/citation-needed`.

**Always-on:** add a rule in `.cursor/rules/` with `alwaysApply: true` that imports
the skill file.

## Gemini CLI

Command (on demand):

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/aliradid/citation-needed/main/skills/citation-needed/agents/gemini.toml \
  -o ~/.gemini/commands/citation-needed.toml
```

Then `/citation-needed`.

Extension (always-on, full ruleset via `GEMINI.md`):

```bash
gemini extensions install https://github.com/aliradid/citation-needed
```

## OpenCode

```bash
git clone https://github.com/aliradid/citation-needed ~/.config/opencode/vendor/citation-needed
```

Add to your `opencode.json`:

```json
{ "plugin": ["~/.config/opencode/vendor/citation-needed/.opencode/plugins/citation-needed.mjs"] }
```

Then `/citation-needed`. Always-on: `touch ~/.config/opencode/.citation-needed-always`.

## Kimi Code CLI

1. Run `/plugins` in a session.
2. Choose **Custom** and paste `https://github.com/aliradid/citation-needed`.
3. Choose **Trust and install**. Then `/skill:citation-needed`.

## Qwen Code

```bash
qwen extensions install aliradid/citation-needed
```

Then `/citation-needed`.

## Grok

```bash
grok plugin install aliradid/citation-needed --trust
grok plugin enable citation-needed
```

## GitHub Copilot (VS Code)

```bash
npx skills add aliradid/citation-needed -a github-copilot
```

Lands in `~/.copilot/skills/` or the project's `.github/skills/`. Type `/` and pick
`citation-needed`.

## Zed

Agent Panel → Skills → **Create skill from URL** → paste
`https://github.com/aliradid/citation-needed/blob/main/skills/citation-needed/SKILL.md`.
Or copy `skills/citation-needed/` into `~/.agents/skills/`.

## Anything else

Any harness that accepts a system prompt works: paste the body of
`skills/citation-needed/SKILL.md` (everything after the frontmatter) into it.

## Uninstall

Remove the plugin with your harness's plugin command, delete the always-on flag file
if you created one, and delete any copied skill directory.
