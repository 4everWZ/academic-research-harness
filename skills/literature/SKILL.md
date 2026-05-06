# Literature Curation Skill

## Purpose

Collect, filter, index, and summarize literature for a deep learning paper workspace without automatically generating paper prose.

Use this skill when the user explicitly asks to search papers, collect references, download/index PDFs, build `paper_index.md`, build `references.bib`, write reading notes, compare methods from literature, or refine an idea using papers.

## Boundary

Literature curation is not paper writing.

After literature collection, do not write introduction, related work, method, or contribution claims unless the user explicitly asks for section drafting.

## Required outputs

For a literature collection task, update or create:

- `docs/<paper_slug>/paper_index.md`
- `docs/<paper_slug>/references.bib`
- `docs/<paper_slug>/notes/<citation_key>.md` for important papers
- `docs/<paper_slug>/idea_log.md` only when the user asks for idea refinement

## Paper source policy

Do not rank papers by venue alone.

Assess each paper by:

1. relevance to the user's exact project;
2. clarity of method;
3. strength and fairness of baselines;
4. dataset/metric/split transparency;
5. code availability;
6. reproducibility risk;
7. logical rigor;
8. whether it supports the intended claim;
9. whether it provides real effect, efficiency, robustness, simplicity, or deployment fit;
10. whether it is mostly novelty packaging.

Conferences are not automatically reliable. Journals are not automatically inferior. arXiv is not automatically unusable. Evidence quality decides usage.

## Preferred sources

Prefer:

- strong conference or journal papers with clear method and evaluation;
- official code or sufficient implementation details;
- strong baselines;
- transparent dataset/metric/split;
- papers that directly support the project mechanism, baseline, dataset, or evaluation.

Use older foundational papers for core mechanisms and definitions.
Use recent papers for novelty comparison and current baselines.

## Weak-source handling

Mark a paper as `weak_signal` or Tier C if:

- it has no code and vague implementation;
- baselines are weak or unfair;
- dataset/metric/split are unclear;
- claim is much stronger than evidence;
- it is mostly module stacking or naming novelty;
- it is only loosely related to the current project.

Weak-signal papers may be useful for awareness but must not support central claims.

## Paper roles

Assign exactly one primary role and optional secondary roles:

- `baseline`
- `competing_method`
- `supporting_mechanism`
- `background`
- `dataset_metric_reference`
- `implementation_reference`
- `weak_signal`

## Evidence strength

Use:

- `strong`
- `medium`
- `weak`
- `reject`

Evidence strength is not equivalent to venue rank.

## Required paper_index.md schema

Use this table:

```markdown
# Paper Index

| Key | Title | Venue/Type | Year | Code | Task | Dataset/Metric | Role | Evidence Strength | Risk | PDF | URL/DOI |
|---|---|---:|---:|---|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | yes/no/unknown | TODO | TODO | baseline/competing_method/supporting_mechanism/background/dataset_metric_reference/implementation_reference/weak_signal | strong/medium/weak/reject | TODO | papers/TODO.pdf | TODO |
```

## Required reading note schema

Use one file per important paper:

```markdown
# <Citation Key>

## Bibliographic info
- Title:
- Authors:
- Venue/Type:
- Year:
- URL/DOI/arXiv:
- Code:
- Local PDF:

## Role in current project
baseline / competing_method / supporting_mechanism / background / dataset_metric_reference / implementation_reference / weak_signal

## Core method
...

## Datasets and metrics
...

## Main claimed result
...

## Evidence quality
strong / medium / weak / reject

## Reproducibility risk
- code availability:
- implementation clarity:
- baseline fairness:
- dataset/metric/split clarity:

## Useful citation claims
| Possible claim | Supported? | Notes |
|---|---|---|
| TODO | yes/partial/no | TODO |

## What it does not support
...

## Relevance to current idea
...

## Caveats
...
```

## Idea refinement mode

Use this mode only when the user explicitly asks to refine an idea using literature.

Output to `idea_log.md`.

Do not:

- auto-change code;
- choose the final method direction;
- optimize for novelty alone;
- present speculative design as proven;
- write paper claims.

Use this schema:

```markdown
# Idea Log

## Current idea
...

## Literature signals
| Paper | Mechanism | Evidence strength | Code | Relevance | Risk |
|---|---|---|---|---|---|
| TODO | TODO | strong/medium/weak | yes/no | TODO | TODO |

## Candidate refinements

### Option A: <name>
- Change:
- Expected benefit:
- Expected cost:
- Evidence:
- Risk:
- Required experiment:
- Human confirmation required: yes/no

### Option B: <name>
...

## Recommendation
State a bounded recommendation. Do not treat it as final decision.

## Rejected or deprioritized directions
| Direction | Reason | Evidence |
|---|---|---|
| TODO | TODO | TODO |

## Human decision points
- TODO
```

## Literature collection checklist

Before finishing, verify:

- [ ] every indexed paper has a role;
- [ ] every central paper has evidence strength;
- [ ] code availability is recorded as yes/no/unknown;
- [ ] dataset/metric/split information is recorded when relevant;
- [ ] weak papers are not used as central evidence;
- [ ] `references.bib` contains all indexed references that will be cited;
- [ ] no paper section prose was written unless explicitly requested.
