# Repo-to-Paper Writing

## Scope

Use this reference when converting code, configs, architecture notes, experiment setup, or implementation details into Markdown paper sections.

For workspace creation or validation, load `references/workspace.md`.

For novelty, SOTA, superiority, result interpretation, or contribution-framing decisions, load `references/evidence-policy.md`.

For tone, contribution framing, limitation placement, or over-defensive prose, load `references/writing-style.md`.

Target files: `method.md`, `experiments.md`, `limitations.md`, `figures.md`; `results_tables.md` placeholders; `intro.md` and `related_work.md` only on explicit request.

Initialize only the needed section:

```bash
python scripts/init_paper_workspace.py docs/<paper_slug> --mode repo-to-paper --section method
```

Use `full` only when the user explicitly wants complete paper scaffolding.

## Evidence Sources

Before writing, distinguish support: code, config, logs/user results, literature, user intent, assumption, or unverified.

## Artifact Firewall

Repo evidence enters prose only after translation into paper concepts. Treat variables, config keys, filenames, paths, metadata, branches, run IDs, scratch labels, and internal codenames as evidence anchors, not manuscript terms.

Preserve exact tokens only for public artifact names, studied APIs, critical settings, or quoted logs; otherwise keep them in `claims.md` or notes.

**Log Probing:** Use available local tools to inspect common experiment folders (`logs/`, `runs/`, `results/`). Verify that logs match the current code/config. Do not invent tool names.

Do not invent tensor shapes, modules, equations, training settings, datasets, metrics, losses, or results.

## Code to Logic to Writing

Order:

1. Identify what the code implements.
2. Explain the mechanism.
3. Connect it to the problem or design goal.
4. Add literature only when directly relevant.
5. Draft clear Markdown prose.

Do not start from a venue template. The human decides final paper composition.

## Paper-Prose Mode

When drafting manuscript text, use paper-prose mode rather than rebuttal mode.

In paper-prose mode:

- state what the implementation does;
- connect the mechanism to the paper's problem;
- scope claims to available evidence;
- keep internal reviewer-risk notes in `claims.md`.

Use reviewer-response style only for rebuttals, response letters, or point-by-point revision text.

## Outlet-Aware Writing

Before drafting, inspect the workspace path and `venue_profile.md`.

If the workspace uses `docs/<paper_slug>__<venue_slug>/`, report the suffix as the target-outlet signal, but use `venue_profile.md` to determine mode. If missing, write neutral academic Markdown.

Use broad outlet modes, not venue-specific prose templates.

### Conference Mode

When `venue_profile.md` indicates `conference`, emphasize:

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
- more space for interpretive boundaries.

### Other Outlet Modes

For workshop, thesis, technical report, undecided, or other modes, use `venue_profile.md` audience/style notes. If missing, write neutral academic Markdown and state the outlet style is unresolved.

Mode changes emphasis only; evidence standards stay fixed.

## Method Section Rules

For `method.md`, include only implementation-confirmed or intended content.

A useful method draft may include:

- module overview;
- input/output assumptions;
- operation sequence;
- architecture integration point;
- design rationale;
- computational considerations;
- relation to prior mechanisms;
- limitations or open implementation questions.

Add `claims.md` entries for nontrivial statements about:

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

Do not write results unless the user provides numbers or you verify matching logs.

For `results_tables.md`, only:

- build table structure;
- define columns;
- prepare neutral captions;
- mark values as `TODO`;
- list missing experiments.

Avoid "outperforms", "achieves SOTA", or "significantly improves" unless user-provided results or verified logs support that exact claim under the same dataset, split, metric, and protocol.

## Introduction and Related Work Rules

Only write `intro.md` or `related_work.md` when explicitly requested.

Use `paper_index.md` and `claims.md`.

Do not use source collection as permission to write prose.

Related work should be organized by method families, problem settings, or evaluation assumptions, not as a paper-by-paper list.

## Output Format

Report:

1. Section updated;
2. Implementation facts used;
3. Literature evidence used;
4. Assumptions or TODOs;
5. Claims added or updated;
6. Files changed.
