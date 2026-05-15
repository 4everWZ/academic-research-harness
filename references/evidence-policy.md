# Evidence Policy

## Scope

Use this reference when a task involves novelty, SOTA, superiority, claim support, result wording, contribution framing, evidence gaps, or user-confirmation boundaries.

Do not load this file for simple workspace initialization or purely mechanical formatting.

## Non-Goals

Do not:

- autonomously conduct research;
- automatically run experiments;
- automatically write paper prose after literature search;
- invent results, ablations, metrics, captions, or conclusions;
- claim novelty, superiority, or SOTA without explicit evidence;
- change datasets, splits, metrics, protocols, baselines, or contribution framing without user confirmation;
- optimize for novelty over evidence quality, reproducibility, and real effect.

## Confirmation Checkpoints

Ask the user before:

- changing contribution framing;
- declaring novelty or SOTA;
- choosing the final method direction;
- removing or replacing strong baselines;
- changing dataset, split, metric, or evaluation protocol;
- converting speculative refinements into final paper claims;
- downgrading or excluding a source if that decision materially affects the paper narrative.

## Claims

Do not write unsupported academic claims into paper sections without recording them in `claims.md`.

For every nontrivial claim, distinguish whether support comes from:

- literature;
- code;
- config;
- verified logs;
- user-provided result;
- user-stated intent;
- assumption;
- unverified inference.

Claims marked unsupported or speculative must not appear as final conclusions.

## Results

Do not write experimental results unless the user provides numbers or verified logs.

**Verified Log Detection:**
Search for files that provide direct, timestamped, or serial evidence of execution. Look for:
- Standard log folders: `logs/`, `runs/`, `checkpoints/`, `results/`.
- File formats: `.log`, `.jsonl` (e.g., from `training_log.jsonl`), `.yaml` (config/summary), `.csv` (metric dumps).
- Tool-specific outputs: `wandb/`, `tensorboard/`, or Hydra output directories.

For results, you may only:

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
