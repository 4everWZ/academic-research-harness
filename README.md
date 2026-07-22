# academic-research-harness

A Codex skill for explicitly requested literature-grounded paper work. It keeps
source and result claims evidence-bound while leaving academic structure,
framing, and prose flexible.

## Capabilities

- create paper artifacts only when needed;
- search and index literature with verified formal-source metadata;
- maintain BibTeX, reading notes, and literature-grounded idea candidates;
- translate repository evidence into requested paper sections;
- audit material claims and citations;
- revise academic framing without drifting into overly defensive prose.

The skill does not run experiments or treat code structure as a manuscript
outline. It does not own project handoffs.

## Runtime layout

```text
SKILL.md
agents/openai.yaml
references/
assets/templates/
scripts/
```

The fallback workspace is `docs/<paper_slug>/`. Files are added on demand; a
workspace does not require a README, venue profile, claim ledger, or empty paper
sections.

```bash
python scripts/init_paper_workspace.py docs/example-paper --include literature
python scripts/init_paper_workspace.py docs/example-paper --include literature,ideas,claims
python scripts/validate_paper_index.py docs/example-paper/paper_index.md
```

Use the official `skill-creator` validator for the skill folder. Runtime scripts
validate paper artifacts, not the prose or scientific validity of a manuscript.
