# research-writing-harness

A demand-triggered, evidence-first paper-writing layer for deep learning research projects.

This harness is not a research automation system. It does not run experiments, change code, claim novelty, or generate a paper end-to-end. It only activates when the user explicitly requests literature search, citation management, idea refinement from papers, repo-to-paper writing, venue/outlet profiling, or claim/citation auditing.

## Positioning

Use this harness with an implementation harness such as apex-harness or repo-level coding agents.

- Implementation harness: code, debugging, training, validation, experiment execution, implementation handoff.
- research-writing-harness: paper workspace, literature index, citation evidence, venue profile, claim ledger, section drafts, writing handoff.
- Human researcher: research direction, contribution framing, experiment selection, final numbers, final conclusions.

## Core definition

A demand-triggered, flat-document, `paper_index.md` + `claims.md` centered academic writing evidence layer.

## Non-goals

The harness must not:

- autonomously conduct research;
- run as an always-on research layer;
- start writing after literature collection unless explicitly requested;
- fabricate citations, metrics, ablations, or results;
- claim novelty, superiority, or SOTA without explicit evidence and human confirmation;
- silently change datasets, metrics, splits, baselines, or evaluation protocol;
- rank papers by venue alone;
- optimize for novelty over reproducibility, logical rigor, and real effect;
- create venue-specific prose templates that replace human writing judgment.

## Recommended paper workspace

Keep the workspace flat.

```text
docs/
  <paper_slug>/
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
      .gitignore
      README.md

    notes/
      2024_xxx.md
      2025_xxx.md
```

`paper_index.md` records literature metadata and evidence quality. `claims.md` records academic claims and their support status. These two files are the core of the harness. `venue_profile.md` records writing tendencies and format assumptions after the target outlet is known; it is not a full writing template.

## Skills

```text
skills/
  router/SKILL.md
  literature/SKILL.md
  repo-to-paper/SKILL.md
  citation-audit/SKILL.md
```

- `router`: activation, progressive loading, load tiers, task routing, human confirmation points.
- `literature`: paper search, filtering, indexing, BibTeX, reading notes, idea refinement.
- `repo-to-paper`: convert existing repo/code/config/design into requested paper sections.
- `citation-audit`: audit claims, citations, support status, unsupported statements.

## Progressive loading

The router uses load tiers to keep context small and avoid applying unrelated instructions.

- Load 0: router only, for activation and task classification.
- Load 1: router + one task skill, for literature-only, idea-only, repo-to-paper-only, or audit-only tasks.
- Load 2: router + one task skill + templates, for creating/updating workspace files.
- Load 3: router + selected skills + workspace files, for mixed tasks such as method writing plus claims update.
- Load 4: full paper-writing review, only for Tier A changes, major handoff, contribution reframing, or full evidence audit.

Do not use Load 4 for ordinary paper search, local drafting, citation cleanup, or table formatting.

## Quick usage prompts

Initialize a workspace:

```text
Use research-writing-harness router.
Create docs/<paper_slug>/ as a flat paper workspace.
Do not search literature yet. Do not write paper content yet.
```

Search literature only:

```text
Use research-writing-harness literature mode.
Search high-quality deep learning papers related to <topic>.
Output paper_index.md, references.bib, and notes only.
Do not write introduction or related work.
Rank papers by evidence quality, not venue alone.
```

Refine an idea using literature:

```text
Use research-writing-harness literature + idea refinement mode.
Current idea: <idea>.
Use indexed papers to propose refinements.
Do not auto-change code. Do not optimize for novelty alone.
Write only to idea_log.md and mark decisions that require human confirmation.
```

Record venue/outlet profile:

```text
Use research-writing-harness router.
Update venue_profile.md for target <venue/outlet>.
Record writing tendencies and format assumptions only.
Do not rewrite paper content.
```

Convert repo to paper section:

```text
Use research-writing-harness repo-to-paper mode.
Convert the implemented module into method.md.
Inspect code/config first. Do not invent tensor shapes, equations, or results.
Update claims.md for nontrivial claims.
```

Audit citations:

```text
Use research-writing-harness citation-audit mode.
Check whether claims in <section>.md are supported by citations and repo evidence.
Update claims.md and list unsupported or partially supported claims.
```

## Handoff policy

Do not update `handoff.md` for every local edit. Update it only for Tier A/B changes.

- Tier A: paper direction, contribution framing, method direction, baseline strategy, dataset/metric/protocol changes.
- Tier B: completed literature collection, completed major draft, target venue/outlet confirmed or changed, important idea refinement, strong similar work found, major evidence gap found.
- Tier C: local wording, one citation, table formatting, BibTeX cleanup. No handoff update required.

## Scripts

```text
scripts/init_paper_workspace.py
scripts/validate_workspace.py
scripts/validate_paper_index.py
```

These scripts only initialize and validate the flat workspace. They do not scrape papers, summarize PDFs, run experiments, or write paper content automatically.
