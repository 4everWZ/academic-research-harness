# Evidence Policy

## Scope

Use this reference for novelty, SOTA, superiority, claim support, result wording, contribution framing, evidence gaps, or user-confirmation boundaries.

## Evidence Boundaries

Keep evidence decisions separate from paper ambition. Do not invent results, claim novelty/SOTA/superiority without explicit evidence, or change datasets, splits, metrics, protocols, baselines, or contribution framing without user confirmation.

## Confirmation Checkpoints

Ask the user before decisions that change research meaning:

- changing contribution framing;
- declaring novelty or SOTA;
- choosing the final method direction;
- removing or replacing strong baselines;
- changing dataset, split, metric, or evaluation protocol;
- converting speculative refinements into final paper claims;
- downgrading or excluding a source if that decision materially affects the paper narrative.

## Claims

Record unsupported or nontrivial academic claims in `claims.md` before using them in paper sections.

For every nontrivial claim, distinguish whether support comes from:

- literature;
- code;
- config;
- verified logs;
- user-provided result;
- user-stated intent;
- assumption;
- unverified inference.

Unsupported or speculative claims stay out of final conclusions.

## Evidence vs Prose Tone

Evidence control is not rebuttal prose. Use `claims.md` to track risks and missing evidence; expose only boundaries that help readers interpret the work.

## Results

Report experimental results only from user-provided numbers or verified logs.

**Verified Log Detection:**
Search for files that provide direct, timestamped, or serial evidence of execution. Look for:
- Standard log folders: `logs/`, `runs/`, `checkpoints/`, `results/`.
- File formats: `.log`, `.jsonl` (e.g., from `training_log.jsonl`), `.yaml` (config/summary), `.csv` (metric dumps).
- Experiment-tracking output directories from the current project.

Without verified numbers, limit results work to:

- create table structures;
- define metric columns;
- prepare neutral captions;
- mark missing cells as `TODO`;
- list required experiments.

Avoid interpretive wording such as "outperforms", "achieves SOTA", or "significantly improves" unless validated evidence supports that exact claim under the same dataset, split, metric, and protocol.

## Evidence Strength

Venue rank is not evidence. Final evidence strength depends on:

- relevance;
- method clarity;
- baseline strength;
- evaluation fairness;
- dataset, metric, and split transparency;
- code or reproducibility support;
- claim-evidence alignment.
