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

When a candidate is first found through arXiv, search by exact title and authors for a formal conference, journal, DOI, or publisher page before writing BibTeX.

## Source Quality Route

For source freshness, priority labels, arXiv credibility, venue risk, or downgrade/exclusion decisions, load `references/source-quality.md`.

Use `venue_profile.md` to record subfield and outlet assumptions. If the subfield is unclear, keep assumptions provisional.

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

Formal-version precedence is a hard check. Before adding an arXiv-only BibTeX entry, check whether the paper already has a formal conference or journal version.

If a formal version exists, use the formal proceedings or journal BibTeX as the primary entry. Keep arXiv only as `eprint`, `note`, or a `paper_index.md` link when useful.

Use arXiv as the primary BibTeX source only when no formal version is found, the cited object is specifically the preprint, or the user explicitly requests the preprint version. Record that status in `paper_index.md` or the reading note.

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
