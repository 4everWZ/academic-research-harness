# Literature Collection and Idea Refinement

## Scope

Use this reference for:

- academic literature search;
- paper collection and indexing;
- BibTeX/reference maintenance;
- reading notes;
- literature-grounded idea refinement;
- paper source filtering;
- method comparison and baseline identification.

Do not use this reference to write paper prose unless the user explicitly asks for a section draft.

## Workflow Boundary

Literature collection must not automatically produce `intro.md`, `related_work.md`, or `method.md`.

Default outputs are limited to:

- `paper_index.md`;
- `references.bib`;
- `notes/*.md`;
- `idea_log.md` when idea refinement is requested.

## Source Hierarchy and Filtering Policy

Search, filter, and summarize literature according to this hierarchy. The goal is to avoid low-quality literature, novelty noise, and unsupported claims.

### Priority 1: Core Sources

Prefer formal peer-reviewed papers from the last 1-3 years in top venues and top journals recognized by the specific subfield.

Match venues to the target subfield instead of mechanically restricting all work to a few generic conferences or journals.

Use `venue_profile.md` to record the relevant venue/outlet assumptions for the current paper workspace. When the target subfield is unclear, keep the search broad and explicitly mark venue assumptions as provisional.

### Non-Exhaustive Venue and Journal Examples

Use these examples only as search-orientation hints. They are not an allowlist, not a ranking rule, and not a substitute for evidence-quality judgment. Match the source to the subfield and current claim.

- machine learning: NeurIPS, ICML, ICLR, JMLR, TMLR;
- computer vision: CVPR, ICCV, ECCV, TPAMI, IJCV, TIP, WACV, BMVC when relevant;
- NLP / LLM: ACL, EMNLP, NAACL, TACL, COLING when relevant;
- multimodal / multimedia: ACM MM and relevant ML/CV/NLP venues;
- robotics / embodied AI: RSS, CoRL, ICRA, IROS, RA-L, IJRR;
- signal processing / remote sensing / imaging: TIP, TGRS, JSTARS, TNNLS, TMM, PR and field-recognized outlets;
- data mining / information retrieval: KDD, WWW, SIGIR, WSDM, TKDE when relevant;
- systems / AI infrastructure: SOSP, OSDI, NSDI, MLSys, EuroSys, ASPLOS when relevant.

Do not mechanically prefer conference papers over journal papers. Conference and journal sources should both be judged by relevance, protocol clarity, baseline strength, reproducibility support, and claim-evidence alignment.

Include older papers when they are:

- foundational work;
- strong baselines;
- community-standard methods;
- widely used datasets, metrics, or evaluation protocols;
- still directly relevant to the current method or writing claim.

### Priority 2: Frontier Supplement

Use recent arXiv preprints from the last year only as frontier signals.

They may help identify:

- emerging trends;
- newly forming research directions;
- recent method families not yet stabilized by peer review;
- active benchmark or implementation trends.

For arXiv papers, prefer work from teams with a sustained record of high-quality research in the area. Assess credibility using:

- public code availability;
- implementation detail;
- experiment transparency;
- strength of baselines;
- dataset / metric / split clarity;
- community attention;
- signs of later acceptance or adoption.

Do not use an arXiv preprint as the sole theoretical basis or sole support for a key conclusion.

### Strict Downgrade / Exclusion

Presumptively downgrade or exclude these sources unless the user explicitly asks to audit a specific source and strong, directly relevant evidence exists:

- MDPI;
- Hindawi;
- Frontiers;
- low-quality isolated preprints;
- papers without reproducibility support;
- papers without meaningful citation or community uptake;
- marketing-like sources;
- sources with unclear academic consensus;
- works with weak baselines, unclear metrics, or unverifiable claims.

These sources must not be used as:

- key evidence;
- primary theoretical basis;
- core support for method superiority;
- main support for novelty claims.

If such a source is mentioned for completeness, explicitly mark it as low-confidence or weak evidence, with limitations stated.

### Evidence Quality Overrides Venue Rank

Venue rank alone is not evidence.

A top-venue paper can still be weak evidence if:

- the comparison is unfair;
- the metric or split is unclear;
- the baseline is weak;
- the code is unavailable and implementation details are insufficient;
- the claim is stronger than the experiments support.

A journal paper, older paper, or non-top-venue paper can still be useful if:

- the method is clear;
- the logic is rigorous;
- the evaluation is transparent;
- the baseline is strong;
- the work is a community-standard reference;
- the claim directly supports the current paper.

### Final Judgment Criteria

Judge every candidate source by:

1. relevance to the current project;
2. venue/subfield fit;
3. method clarity;
4. baseline strength;
5. dataset, metric, and split transparency;
6. code or reproducibility support;
7. claim-evidence alignment;
8. role in the current writing task;
9. risk of novelty noise;
10. whether it can support a specific claim in `claims.md`.

## Paper Index Rules

Update `paper_index.md` for every selected source.

Use stable citation keys. Prefer:

```text
firstauthorYYYYshorttopic
```

Example:

```text
smith2024shorttopic
```

Classify `Source Priority` as:

- `P1_core`;
- `P2_frontier`;
- `P3_background`;
- `downgraded`;
- `excluded`.

Classify `Evidence Grade` as:

- `strong`;
- `medium`;
- `weak`;
- `low_confidence`;
- `reject`.

Classify `Role` as:

- `baseline`;
- `competing_method`;
- `supporting_mechanism`;
- `background`;
- `dataset_metric_reference`;
- `implementation_reference`;
- `weak_signal`.

## Reading Notes

Create a note under `notes/` only for important papers.

Use `assets/templates/reading_note.md`.

Each note should record:

- what the paper actually claims;
- what evidence supports the claim;
- whether code exists;
- whether baselines are strong;
- whether the method is directly useful;
- how the paper should and should not be cited.

## Idea Refinement Rules

When asked to refine an idea using literature:

1. Summarize the current idea as understood.
2. Identify directly relevant mechanisms from indexed or newly found papers.
3. Compare against the current idea.
4. Suggest candidate refinements.
5. Record expected benefit, expected cost, evidence, risk, and required experiments.
6. Mark every suggestion as a candidate, not a decision.

Write to `idea_log.md`.

Do not:

- modify code;
- choose the final method direction;
- frame speculative refinements as final contributions;
- optimize for novelty alone;
- ignore efficiency, reproducibility, baseline strength, or deployment constraints.

## Literature Search Output Format

When reporting to the user, structure the response as:

1. What was searched;
2. What was selected;
3. What was rejected or downgraded;
4. Why the selected papers matter;
5. Caveats;
6. Files updated.
