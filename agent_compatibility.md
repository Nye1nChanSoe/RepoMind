# /agent_compatibility.md

# Agent Compatibility Map

Canonical rule file:
- `agent_rules.md`

Mirrors added for common agent ecosystems:
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

Guidance:
- Update `agent_rules.md` first.
- Keep mirror files short and stable.
- If a tool supports only one repo instruction file, keep the mirror and point it to `agent_rules.md`.
- If a tool ignores references and needs inline rules, duplicate the contents of `agent_rules.md` into that tool-specific file.
