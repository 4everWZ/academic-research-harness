# Literature Collection and Idea Refinement

## Scope

Use this reference for literature-facing work:

- academic literature search;
- paper collection and indexing;
- BibTeX/reference maintenance;
- reading notes;
- literature-grounded idea refinement;
- paper source filtering;
- method comparison and baseline identification.

For section drafting, workspace creation, or novelty/SOTA decisions, load the corresponding reference instead of stretching this one.

## Workspace Readiness

If output files are missing, load `references/workspace.md` and create only the minimal `literature` or `idea` workspace needed.

## Workflow Boundary

Literature collection indexes evidence; it does not draft paper sections unless the user asks. Default outputs:

- `paper_index.md`;
- `references.bib`;
- `notes/*.md`;
- `papers/*.pdf` only when download/archive is explicitly requested;
- `idea_log.md` when idea refinement is requested.

## Search and Extraction Policy

Use available search/fetch tools with domain filters where supported. Do not invent tool names.

Prefer primary sources: proceedings pages, OpenReview, arXiv, DOI/publisher pages, official project pages, and official repositories. Use secondary summaries only as search leads.

## Freshness Weighting

Default search weight favors the last 3-5 years, and the last 1-2 years for fast-moving areas such as LLMs, multimodal models, and active benchmarks.

Older sources need a role: foundational method, standard baseline, dataset/metric/protocol reference, survey context, or direct support for a specific claim. Do not include old papers merely because they are topically related.

## Source Hierarchy and Filtering Policy

Search and filter by role in the current paper, not by venue prestige alone.

### Source Priority vs. Evidence Grade

- **Source Priority**: venue/timing role (`P1_core`, `P2_frontier`, `P3_background`, `downgraded`, `excluded`).
- **Evidence Grade**: how directly the source supports the current claim (`strong`, `medium`, `weak`, `low_confidence`, `reject`).

### Priority 1: Core Sources

Prefer recent peer-reviewed work from venues recognized by the subfield, plus older foundational or community-standard work when it directly supports the claim.

Use `venue_profile.md` to record subfield and outlet assumptions. If the subfield is unclear, keep assumptions provisional.

### Non-Exhaustive Venue and Journal Examples

Use these only as search-orientation hints, not as an allowlist or ranking rule.

- machine learning: NeurIPS, ICML, ICLR, JMLR, TMLR;
- computer vision: CVPR, ICCV, ECCV, TPAMI, IJCV, TIP, WACV, BMVC when relevant;
- NLP / LLM: ACL, EMNLP, NAACL, TACL, COLING when relevant;
- multimodal / multimedia: ACM MM and relevant ML/CV/NLP venues;
- robotics / embodied AI: RSS, CoRL, ICRA, IROS, RA-L, IJRR;
- signal processing / remote sensing / imaging: TIP, TGRS, JSTARS, TNNLS, TMM, PR and field-recognized outlets;
- data mining / information retrieval: KDD, WWW, SIGIR, WSDM, TKDE when relevant;
- systems / AI infrastructure: SOSP, OSDI, NSDI, MLSys, EuroSys, ASPLOS when relevant.

Judge conference and journal sources by relevance, protocol clarity, baseline strength, reproducibility support, and claim-evidence alignment.

Include older papers when they are:

- foundational work;
- strong baselines;
- community-standard methods;
- widely used datasets, metrics, or evaluation protocols;
- still directly relevant to the current method or writing claim.

### Priority 2: Frontier Supplement

Use recent arXiv preprints mainly as frontier signals. They help identify:

- emerging trends;
- newly forming research directions;
- recent method families not yet stabilized by peer review;
- active benchmark or implementation trends.

For arXiv papers, make paper-level transparency the primary criterion:

- public code availability;
- implementation detail;
- experiment transparency;
- strength of baselines;
- dataset / metric / split clarity;
- time-normalized community attention or later acceptance/adoption;
- author or team track record as a secondary signal.

Recent preprints may support factual existence, method-context, dataset, benchmark, protocol, or implementation-trend claims. Do not use one as the sole support for key novelty, superiority, or final conclusions.

### Downgrade / Exclusion Risk Signals

Downgrade sources when paper-level evidence is weak: unclear protocol, weak baselines, unverifiable claims, no reproducibility support, marketing-like framing, isolated low-quality preprints, or disputed venue/publisher fit in the target subfield.

Publisher identity is a signal, not a verdict. Reject or downgrade because the paper cannot support the claim, and mark any retained weak source as low-confidence or auxiliary.

### Evidence Quality Overrides Venue Rank

Venue rank alone is not evidence. A top-venue paper can still be weak evidence if:

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

For each candidate, record the role it can actually play: baseline, competing method, mechanism support, dataset/metric reference, implementation reference, background, or weak signal. Grade by relevance, protocol clarity, baseline strength, reproducibility support, and claim-evidence alignment.

## Paper Index Rules

Update `paper_index.md` for every selected source and for downgraded/excluded sources that materially affected the search or paper narrative.

Use stable citation keys. Prefer:

```text
firstauthorYYYYshorttopic
```

Example:

```text
smith2024shorttopic
```

Classify `Source Priority` as:

- `P1_core`: recent core peer-reviewed work or older foundational/standard work;
- `P2_frontier`: recent frontier signal, usually arXiv or newly emerging work;
- `P3_background`: useful context, dataset, metric, survey, or non-central reference;
- `downgraded`: weak evidence, mention only with explicit caveat if needed;
- `excluded`: not used as evidence.

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

## BibTeX Rules

Update `references.bib` for selected sources that may be cited, using the same citation key as `paper_index.md`.

Prefer BibTeX from official proceedings pages, OpenReview, arXiv, DOI/publisher pages, or the paper's official repository.

Do not fabricate BibTeX fields. If metadata is unavailable, include only verified fields and mark missing information in `paper_index.md` or the relevant reading note.

Keep `references.bib` and `paper_index.md` synchronized when renaming citation keys.

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

When refining an idea with literature:

1. Summarize the current idea as understood.
2. Identify directly relevant mechanisms from indexed or newly found papers.
3. Compare against the current idea.
4. Suggest candidate refinements.
5. Record expected benefit, expected cost, evidence, risk, and required experiments.
6. Mark every suggestion as a candidate, not a decision.

Update `idea_log.md`.

Keep suggestions as candidates. Do not modify code, choose the final method direction, or turn speculative refinements into final contributions.

## Literature Search Output Format

When reporting to the user, structure the response as:

1. What was searched;
2. What was selected;
3. What was rejected or downgraded;
4. Why the selected papers matter;
5. Caveats;
6. Files updated or read-only status.
