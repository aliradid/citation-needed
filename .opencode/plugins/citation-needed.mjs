// citation-needed — OpenCode plugin.
//
// The skill in `skills/citation-needed/SKILL.md` is the single source of truth.
//
//   • On demand   — registers the skills directory and a `/citation-needed`
//                   command so the rules apply for the rest of the session.
//   • Always-on   — when the opt-in flag file exists, the full ruleset is
//                   appended to the system prompt every turn (the OpenCode
//                   equivalent of the SessionStart hook in hooks/).
//
// Opt in to always-on:   touch ~/.config/opencode/.citation-needed-always
// Opt back out:          rm ~/.config/opencode/.citation-needed-always
//
// Install — add to opencode.json:
//   { "plugin": ["./.opencode/plugins/citation-needed.mjs"] }

import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '../../skills');
const skillPath = path.join(skillsDir, 'citation-needed', 'SKILL.md');
const commandPath = path.join(__dirname, '..', 'command', 'citation-needed.md');

// JSON is valid YAML frontmatter; share command metadata without a YAML dependency.
async function commandDefinition() {
  const raw = await fs.promises.readFile(commandPath, 'utf8');
  const match = raw.match(/^---[^\S\r\n]*\r?\n([\s\S]*?)\r?\n---[^\S\r\n]*(?:\r?\n|$)([\s\S]*)$/);
  if (!match) throw new Error('Missing command frontmatter');
  return { ...JSON.parse(match[1]), template: match[2].trim() };
}

const flagPath = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'opencode',
  '.citation-needed-always',
);

// Read SKILL.md and strip a leading YAML frontmatter block. Same regex as
// hooks/always-on.mjs so injections are identical across harnesses.
function rulesetBody() {
  return fs
    .readFileSync(skillPath, 'utf8')
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
    .replace(/(?:\r?\n)+$/, '');
}

export default async () => {
  return {
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir);
      try {
        config.command = config.command || {};
        if (!config.command['citation-needed']) {
          config.command['citation-needed'] = await commandDefinition();
        }
      } catch (e) {
        // A missing or malformed command file must not break skill discovery.
      }
    },

    'experimental.chat.system.transform': async (_input, output) => {
      let on = false;
      try { on = fs.existsSync(flagPath); } catch (e) {}
      if (!on) return;

      let body;
      try { body = rulesetBody(); } catch (e) { return; }

      const header =
        'CITATION-NEEDED GUARD ACTIVE (always-on). The rules below apply to every ' +
        'response. "stop citation-needed" turns it off for this session; delete ' +
        flagPath + ' to turn always-on off for good.';
      const injected = header + '\n\n' + body;

      if (output.system.length > 0) {
        output.system[output.system.length - 1] += '\n\n' + injected;
      } else {
        output.system.push(injected);
      }
    },
  };
};
