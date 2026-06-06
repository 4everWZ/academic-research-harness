# academic-research-harness

A Codex/OpenAI-style global skill for on-demand literature-grounded paper writing and evidence management.

This skill is not an autonomous research system. It is a router-only paper-writing evidence layer for existing or evolving research projects.

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

## Capabilities

- Route each task to the smallest needed reference file.
- Search and index literature, BibTeX, and reading notes.
- Track paper claims in `claims.md`.
- Convert code/config/design into Markdown paper sections.
- Audit claims, citations, writing style, and handoff state.

## Progressive Disclosure

`SKILL.md` only decides whether the skill applies and which reference to load. Task details live under `references/`:

- `workspace.md`: workspace modes, scripts, validation, venue suffixes.
- `literature.md`: paper search, indexing, reading notes, idea refinement.
- `repo-to-paper.md`: code/config to paper sections.
- `citation-audit.md`: claim and citation checking.
- `handoff.md`: paper-state handoff.
- `evidence-policy.md`: novelty, SOTA, results, claim support, and confirmation boundaries.

Load only the reference needed for the current task.

## Boundaries

- Activate only for explicit paper-writing or literature-grounded work.
- Draft paper sections only when requested.
- Report results only from user-provided numbers or verified logs.
- Treat venue rank as context, not evidence quality.

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

`repo-to-paper` creates the paper-section scaffold:

```text
docs/example_paper__target-venue/
  README.md
  venue_profile.md
  paper_index.md
  references.bib
  claims.md
  intro.md
  related_work.md
  method.md
  experiments.md
  results_tables.md
  limitations.md
  figures.md
  papers/
  notes/
```

`full` also includes route-state files such as `idea_log.md` and `handoff.md`.

## Outlet-Aware Drafting

Use `venue_profile.md` to record whether the target is `conference`, `journal`, or another outlet mode. The workspace suffix `docs/<paper_slug>__<venue_slug>/` records a confirmed target outlet, while the mode controls writing emphasis. Do not create concrete venue-specific prose templates.

## Validate

```bash
python tmp/quick_validate_skill.py .
python scripts/validate_workspace.py docs/example_paper --mode literature
python scripts/validate_paper_index.py docs/example_paper/paper_index.md
```

`tmp/quick_validate_skill.py` is a package-maintainer check for this skill folder. Runtime workspace commands stay under `scripts/`.
