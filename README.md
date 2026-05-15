# academic-research-harness

A Codex/OpenAI-style global skill for on-demand literature-grounded paper writing and evidence management.

This skill is not an autonomous research system. It is a paper-writing evidence layer for existing or evolving research projects.

## Install

Place the `academic-research-harness/` folder in your Codex skills directory, for example:

```text
$CODEX_HOME/skills/academic-research-harness/
```

On a local Codex setup this may be:

```text
~/.agents/skills/academic-research-harness/
```

Restart Codex after installing or updating the skill.

## Standard Skill Shape

```text
academic-research-harness/
  SKILL.md
  agents/openai.yaml
  references/
  assets/templates/
  scripts/
```

`SKILL.md` is at the skill folder root and has YAML frontmatter with only `name` and `description`.

## What It Does

- Search and curate literature.
- Maintain `paper_index.md`.
- Maintain `references.bib`.
- Maintain `claims.md`.
- Refine ideas using literature without changing code automatically.
- Convert implemented code/config/design into Markdown paper sections.
- Audit claims and citations.
- Prepare Tier A/B paper handoff.

## What It Does Not Do

- Does not auto-run research.
- Does not always activate.
- Does not write paper sections after literature search unless explicitly requested.
- Does not invent results.
- Does not claim novelty/SOTA without evidence.
- Does not use venue rank alone as evidence quality.

## Initialize a Workspace

```bash
python scripts/init_paper_workspace.py docs/example_paper --mode literature
```

Workspace creation is progressive:

```bash
python scripts/init_paper_workspace.py docs/example_paper --mode minimal
python scripts/init_paper_workspace.py docs/example_paper --mode literature
python scripts/init_paper_workspace.py docs/example_paper --mode idea
python scripts/init_paper_workspace.py docs/example_paper --mode citation-audit
python scripts/init_paper_workspace.py docs/example_paper --mode repo-to-paper
python scripts/init_paper_workspace.py docs/example_paper --mode handoff
python scripts/init_paper_workspace.py docs/example_paper --mode full
```

Use `repo-to-paper` or `full` only when full paper-section scaffolding is needed.

After target venue/outlet is confirmed:

```bash
python scripts/init_paper_workspace.py docs/example_paper --mode repo-to-paper --venue "Target Venue" --outlet-mode conference --suffix-venue
```

`repo-to-paper` and `full` create:

```text
docs/example_paper__target-venue/
  README.md
  venue_profile.md
  paper_index.md
  references.bib
  claims.md
  idea_log.md
  intro.md
  related_work.md
  method.md
  experiments.md
  results_tables.md
  limitations.md
  figures.md
  handoff.md
  papers/
  notes/
```

## Outlet-Aware Drafting

Use `venue_profile.md` to record whether the target is `conference`, `journal`, or another outlet mode. The workspace suffix `docs/<paper_slug>__<venue_slug>/` records a confirmed target outlet, while the mode controls writing emphasis. Do not create concrete venue-specific prose templates.

## Validate

```bash
python scripts/quick_validate_skill.py .
python scripts/validate_workspace.py docs/example_paper --mode literature
python scripts/validate_paper_index.py docs/example_paper/paper_index.md
```
