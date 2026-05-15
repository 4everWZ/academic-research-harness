# Repo-to-Paper Writing

## Scope

Use this reference when converting existing code, configs, architecture notes, experiment setup, or implementation details into Markdown paper sections.

For workspace creation or validation, load `references/workspace.md`.

For novelty, SOTA, superiority, result interpretation, or contribution-framing decisions, load `references/evidence-policy.md`.

Supported target files:

- `intro.md` only when the user explicitly asks for introduction writing;
- `related_work.md` only when the user explicitly asks for related work;
- `method.md`;
- `experiments.md`;
- `results_tables.md` only as placeholders;
- `limitations.md`;
- `figures.md`.

## Evidence Sources

Before writing, distinguish:

- confirmed from code;
- confirmed from config;
- confirmed from logs or user-provided results;
- supported by literature;
- user-stated intent;
- assumption;
- unverified.

Do not invent tensor shapes, modules, equations, training settings, datasets, metrics, losses, or results.

## Code to Logic to Writing

Prioritize this order:

1. Identify what the code actually implements.
2. Explain the logical mechanism.
3. Connect the mechanism to the problem or design goal.
4. Add literature support only when directly relevant.
5. Write clear Markdown prose.

Do not start from a venue template. The human decides final paper composition.

## Outlet-Aware Writing

Before drafting any paper section, inspect the active workspace path and `venue_profile.md`.

If the workspace uses `docs/<paper_slug>__<venue_slug>/`, treat the suffix as an explicit target-outlet signal. Use it to report the target outlet, but use `venue_profile.md` to determine the writing mode. If the mode is missing or undecided, state that and write in neutral academic Markdown without assuming a concrete venue style.

Use only broad outlet modes, not concrete venue-specific prose templates.

### Conference Mode

When `venue_profile.md` indicates `conference`, write with:

- sharper motivation;
- early contribution framing;
- compact related work;
- concise method explanation;
- focused experiment setup and key ablation placeholders;
- neutral, compact limitation statements.

### Journal Mode

When `venue_profile.md` indicates `journal`, allow:

- fuller background and problem context;
- deeper related-work taxonomy;
- more detailed method explanation;
- richer experiment setup and ablation planning;
- more explicit limitations, failure cases, and reproducibility notes.

The mode changes emphasis and depth only. It must not change evidence standards, invent results, or alter the user's scientific claims.

## Method Section Rules

For `method.md`, include only implementation-confirmed or explicitly intended content.

A useful method draft may include:

- module overview;
- input/output assumptions;
- operation sequence;
- architecture integration point;
- design rationale;
- computational considerations;
- relation to prior mechanisms;
- limitations or open implementation questions.

Add claim entries to `claims.md` for nontrivial statements, especially:

- performance expectation;
- efficiency expectation;
- novelty or difference from prior work;
- mechanism benefit;
- generalization or robustness statement.

## Experiment Section Rules

For `experiments.md`, describe setup only when provided or confirmed:

- datasets;
- splits;
- metrics;
- baselines;
- implementation details;
- training schedule;
- hardware;
- inference settings.

Mark unknown fields as `TODO`, not guesses.

Do not change metric, split, protocol, or baseline framing without user confirmation.

## Results Policy

Do not write results unless the user gives numbers.

For `results_tables.md`, only:

- build table structure;
- define columns;
- prepare neutral captions;
- mark values as `TODO`;
- list missing experiments.

Avoid interpretive wording such as "outperforms", "achieves SOTA", or "significantly improves" unless the user provides validated evidence.

## Introduction and Related Work Rules

Only write `intro.md` or `related_work.md` when explicitly requested.

Use `paper_index.md` and `claims.md`.

Do not use source collection as permission to write prose.

Related work should be organized by method families, problem settings, or evaluation assumptions, not as a paper-by-paper list.

## Output Format

When reporting repo-to-paper work, include:

1. Section updated;
2. Implementation facts used;
3. Literature evidence used;
4. Assumptions or TODOs;
5. Claims added or updated;
6. Files changed.
