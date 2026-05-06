# Repo-to-Paper Skill

## Purpose

Convert existing repo content, implemented modules, configs, experiment setup, architecture notes, or user-provided design into paper-ready section drafts without inventing results or unsupported claims.

Use this skill only when the user explicitly asks to write or revise a paper section, or to convert code/config/design into academic text.

## Allowed outputs

Write only the requested files, commonly:

- `intro.md`
- `related_work.md`
- `method.md`
- `experiments.md`
- `results_tables.md`
- `limitations.md`
- `figures.md`

Update `claims.md` for nontrivial academic claims introduced in the draft.

## Non-goals

Do not:

- run experiments;
- modify implementation;
- invent tensor shapes, hyperparameters, datasets, metrics, or results;
- infer missing numbers;
- claim novelty or SOTA without human confirmation;
- write final conclusions from unverified assumptions;
- convert literature collection into paper prose unless section drafting was requested.

## Evidence sources

A section may use only:

1. confirmed repo/code/config details;
2. user-provided design notes;
3. user-provided experimental numbers;
4. indexed literature from `paper_index.md` and `references.bib`;
5. claims recorded in `claims.md`;
6. explicit assumptions marked as speculative.

If a detail is not confirmed, mark it as `TODO`, `TBD`, or `UNVERIFIED`, not as fact.

## Section-specific rules

### Introduction

Allowed:

- background motivation;
- problem setting;
- limitations of existing work, if supported;
- high-level project objective;
- conservative contribution placeholders.

Require confirmation before:

- novelty claims;
- superiority claims;
- final contribution list;
- claims that existing work fails in a broad way.

### Related Work

Organize by method families or problem dimensions, not by a paper-by-paper list.

Use only indexed papers unless the user asks for additional search.

For each paragraph, ensure citations directly support the claim.

Avoid:

- dismissing prior work without evidence;
- venue-based authority claims;
- overemphasizing novelty;
- citing weak-signal papers as central evidence.

### Method

Inspect implementation/config/design before writing.

Separate:

- confirmed implementation details;
- intended design rationale;
- literature-supported mechanism;
- unverified assumptions.

Do not invent:

- tensor shapes;
- complexity values;
- equations;
- module interactions;
- training behavior.

If equations are derived from code or design, mark the source.

### Experiments

Write setup only.

Allowed:

- dataset names if confirmed;
- metrics if confirmed;
- baseline list if confirmed;
- training protocol if confirmed;
- implementation environment if confirmed.

Require confirmation before:

- changing baseline strategy;
- changing metric/dataset/split/protocol;
- removing strong baselines.

### Results tables

Do not write results unless the user provides numbers.

Allowed:

- table templates;
- columns;
- captions;
- TODO cells;
- required experiment list.

Required table convention:

```markdown
| Method | Backbone | Params | FLOPs | Metric 1 | Metric 2 | Notes |
|---|---|---:|---:|---:|---:|---|
| Baseline | TODO | TODO | TODO | TODO | TODO | TODO |
| Proposed | TODO | TODO | TODO | TODO | TODO | TODO |
```

### Limitations

Allowed:

- unverified claims;
- dataset/task scope limitations;
- reproducibility risks;
- method cost/complexity risks;
- baseline and evaluation caveats;
- implementation constraints.

Do not use limitations as a place to hide protocol changes or missing results.

### Figures

Allowed:

- figure plan;
- architecture diagram description;
- caption draft;
- labels and notation.

Do not claim visualized components exist unless confirmed by code/design.

## Claim ledger update

For every nontrivial academic claim, add or update an entry in `claims.md`:

```markdown
## Claim <id>

**Claim text:**
...

**Claim type:**
background / method / experiment_setup / comparison / limitation / speculation

**Support:**
- code/config:
- literature:
- user-provided result:
- user decision:

**Evidence status:**
supported / partially_supported / unsupported / speculative

**Citation key:**
...

**Risk:**
...

**Allowed in final paper?**
yes / no / only_with_caveat
```

## Human confirmation triggers

Ask before:

- writing novelty or SOTA claims;
- finalizing contributions;
- stating that the proposed method is better than a baseline;
- changing experimental setup;
- interpreting missing or unstable results;
- using weak evidence for a central claim.

## Completion checklist

Before finishing:

- [ ] only requested section(s) were written;
- [ ] no experimental results were invented;
- [ ] unverified details are marked;
- [ ] claims are reflected in `claims.md`;
- [ ] citations directly support claims;
- [ ] human confirmation points are listed.
