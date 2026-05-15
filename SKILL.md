---
name: academic-research-harness
description: Use only when the user explicitly requests this skill or explicitly asks to search/curate academic literature, update paper_index/references/claims, refine an idea using papers, convert repo/code into Markdown paper sections, audit citations, or prepare paper handoff. Do not use for normal coding/debugging/training/log analysis/general research chat without an explicit paper-writing or literature-grounding request.
---

# Academic Research Harness

## Purpose

Use this skill as an on-demand paper-writing and evidence-management layer for an existing or evolving deep learning research project.

It is not an autonomous research system. It must not run as a default research layer. It should activate only when the user explicitly requests literature search, citation management, idea refinement from papers, repo-to-paper writing, citation audit, or paper handoff.

The main implementation harness owns code, training, debugging, validation, experiment execution, and code handoff. This skill owns literature evidence, paper index maintenance, claim tracking, Markdown paper sections, citation audit, and paper-writing handoff.

## Non-Goals

Do not use this skill to:

- autonomously conduct research;
- automatically run experiments;
- automatically write paper prose after literature search;
- invent results, ablations, metrics, captions, or conclusions;
- claim novelty, superiority, or SOTA without explicit evidence;
- change datasets, splits, metrics, protocols, baselines, or contribution framing without user confirmation;
- optimize for novelty over evidence quality, reproducibility, and real effect.

## Required Flat Workspace

For each paper-like project, use one flat workspace under `docs/`:

```text
docs/<paper_slug>/
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

After the target venue/outlet is confirmed, the workspace folder may be renamed with a double-underscore suffix, for example:

```text
docs/<paper_slug>__<venue_slug>/
```

Use `venue_profile.md` to record venue/outlet assumptions and the explicit writing mode: `conference`, `journal`, or another stated outlet type. Do not create many venue-specific writing templates.

When a workspace uses the suffix form `docs/<paper_slug>__<venue_slug>/`, treat the suffix as an explicit outlet signal. Before drafting paper prose, read `venue_profile.md` and state which outlet-aware mode is being used. Use the mode to guide content emphasis only; do not apply a concrete venue-specific writing template.

## Core Files

Treat these files as the central state:

- `paper_index.md`: indexed literature and evidence quality;
- `claims.md`: claim ledger linking draft claims to literature, code, experiments, user decisions, or explicit assumptions;
- `idea_log.md`: literature-driven idea refinement and rejected options;
- `venue_profile.md`: confirmed or provisional target venue/outlet and writing tendencies.

Do not write unsupported academic claims into paper sections without recording them in `claims.md`.

## Progressive Loading Policy

Load the smallest useful reference file. Do not read every reference by default.

### Load 0: Router only

Use only this `SKILL.md` when deciding whether the skill should apply, selecting a task route, or initializing a workspace.

### Load 1: Single task reference

Use one reference file when the task is narrow:

- Literature collection or idea refinement: load `references/literature.md`.
- Repo/code/config to paper section: load `references/repo-to-paper.md`.
- Citation/claim checking: load `references/citation-audit.md`.
- Paper handoff: load `references/handoff.md`.

### Load 2: Task reference plus templates

Load the relevant template from `assets/templates/` only when writing or validating that file.

Examples:

- `paper_index.md` work: load `references/literature.md` plus `assets/templates/paper_index.md`.
- Method section work: load `references/repo-to-paper.md` plus `assets/templates/method.md`.
- Claim audit: load `references/citation-audit.md` plus `assets/templates/claims.md`.

### Load 3: Cross-file consistency

Use Load 3 when the user asks for consistency across literature, claims, and sections. Inspect only the necessary workspace files, normally `paper_index.md`, `claims.md`, the target section, and `venue_profile.md`.

### Load 4: Major paper-state update

Use Load 4 only for Tier A/B changes or explicit paper handoff. Inspect the relevant workspace state and update `handoff.md` if required.

## Task Routing

### Literature collection

Use `references/literature.md` when the user asks to search, collect, index, classify, download, or summarize academic papers, build/update `paper_index.md`, add BibTeX, or create reading notes.

Do not write introduction, related work, or method prose after literature collection unless the user explicitly asks for section writing.

### Idea refinement from literature

Use `references/literature.md` when the user asks to refine an idea using papers.

Write candidate refinements to `idea_log.md`. Do not modify code. Do not convert suggestions into paper claims without evidence and user decision.

### Repo-to-paper writing

Use `references/repo-to-paper.md` when the user asks to convert implemented code, configs, architecture notes, or experiment setup into Markdown paper sections.

Write only the requested section. Update `claims.md` for nontrivial claims introduced by the section.

### Citation audit

Use `references/citation-audit.md` when the user asks whether citations support claims, whether related work is distorted, whether novelty is overclaimed, or whether claims are unsupported.

### Handoff

Use `references/handoff.md` when the user asks for paper handoff or when a Tier A/B change has occurred.

## Source Hierarchy Summary

Use the full policy in `references/literature.md`. The short version is:

1. Prefer recent formal peer-reviewed papers from the last 1-3 years in top venues and top journals recognized by the relevant subfield.
2. Include older foundational work, strong baselines, community-standard methods, datasets, metrics, and protocols when still relevant.
3. Use recent arXiv only as frontier supplement, not as sole theoretical support or sole evidence for key conclusions.
4. Strictly downgrade or exclude MDPI, Hindawi, Frontiers, isolated low-quality preprints, marketing-like sources, weakly reproducible works, and sources with unclear academic consensus.
5. Venue rank is not evidence. Final evidence strength depends on relevance, method clarity, baseline strength, evaluation fairness, dataset/metric/split transparency, code/reproducibility support, and claim-evidence alignment.

## Confirmation Checkpoints

Ask the user before:

- changing contribution framing;
- declaring novelty or SOTA;
- choosing the final method direction;
- removing or replacing strong baselines;
- changing dataset, split, metric, or evaluation protocol;
- converting speculative refinements into final paper claims;
- downgrading or excluding a source if that decision materially affects the paper narrative.

## Results Policy

Do not write experimental results unless the user provides the numbers.

For results, you may only:

- create table structures;
- define metric columns;
- prepare neutral captions;
- mark missing cells as `TODO`;
- list required experiments.

## Handoff Policy

Do not update `handoff.md` for every small edit.

Update `handoff.md` for:

- Tier A: paper direction, contribution framing, method direction, baseline strategy, or evaluation protocol changes;
- Tier B: completed literature collection, major section draft, important idea refinement, strong similar-work discovery, or major evidence gap discovery.

Do not update `handoff.md` for Tier C local edits such as wording, formatting, single BibTeX fixes, or one citation addition.

## Scripts

Use scripts only for explicit workspace initialization or local validation.

```bash
# Writes files. Run only when the user asks to create or refresh a paper workspace.
python scripts/init_paper_workspace.py docs/<paper_slug>

# Read-only validation.
python scripts/validate_workspace.py docs/<paper_slug>
python scripts/validate_paper_index.py docs/<paper_slug>/paper_index.md
python scripts/quick_validate_skill.py .
```

Do not add or rely on scripts that scrape Google Scholar, automatically summarize PDFs, or automatically write related work.
