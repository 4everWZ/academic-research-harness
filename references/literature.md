# Literature Collection and Idea Refinement

Use this reference for literature search, selection, indexing, BibTeX, reading
notes, baseline identification, and literature-grounded idea refinement. Load
`evidence-and-citations.md` when judging source quality or claim support.

## Collect sources

Prefer primary sources such as proceedings, journals, OpenReview, arXiv, DOI or
publisher pages, official project pages, and official repositories. Secondary
sources may lead the search but should not replace the cited primary source.

Choose a search window appropriate to the subfield, claim, and pace of change.
Cover recent work as well as older foundational, standard, dataset, metric, or
baseline sources when they remain relevant. Record material coverage limits
rather than treating a fixed year window as universal.

When a candidate is found as a preprint, search its exact title and authors for
a formal version, correction, retraction, or materially newer revision before
using it. Do not downgrade a source solely by publisher label; judge the paper,
venue, evidence, and role in the current claim.

## Maintain the literature artifacts

Add to `paper_index.md` sources that may be cited and exclusions that materially
change a claim, baseline set, or paper narrative. Use a stable citation key such
as `firstauthorYYYYshorttopic` and record the concrete quality basis rather than
only a grade.

Add selected sources to `references.bib` with the same key. Prefer verified
formal proceedings or journal metadata when a formal version exists. Use arXiv
as the primary entry only when no formal version is found, the preprint itself
is the cited object, or the user requests it. Never fabricate BibTeX fields.

Create `notes/<citation_key>.md` only for papers whose claims, evidence,
limitations, method, or citation boundaries need durable analysis. Download a
local paper copy only when explicitly requested and legally appropriate.

## Refine ideas

When asked to refine an idea:

1. state the current idea and its unresolved assumptions;
2. identify directly relevant mechanisms and evidence;
3. compare them with the current idea;
4. record candidate changes, expected value and cost, evidence gaps, risks, and
   required experiments in `idea_log.md`;
5. keep candidates distinct from accepted research decisions.

Do not modify code or turn a candidate into a final contribution without the
user's decision and the required evidence.
