# Literature Collection and Idea Refinement

Use this reference for literature search, selection, indexing, BibTeX, reading
notes, baseline identification, and literature-grounded idea refinement. Load
`evidence-and-citations.md` when judging source quality or claim support.
Load `workspace.md` when locating, creating, or structurally changing artifacts.

## Collect sources

Use secondary sources for discovery, then cite the primary paper, formal record,
official project page, or official repository that supports the claim.

Choose a search window appropriate to the subfield, claim, and pace of change.
Cover recent work as well as older foundational, standard, dataset, metric, or
baseline sources when they remain relevant. Record material coverage limits
rather than treating a fixed year window as universal.

When a candidate is found as a preprint, search its exact title and authors for
a formal version, correction, retraction, or materially newer revision before
using it.

## Maintain the literature artifacts

Add sources that may be cited with disposition `selected`; add material
exclusions with disposition `excluded`. Use a portable key matching
`[A-Za-z][A-Za-z0-9_-]*`, such as `firstauthorYYYYshorttopic`, and record the
concrete quality basis rather than a grade.

Add selected sources to `references.bib` with the same key. Prefer verified
formal proceedings or journal metadata when a formal version exists. Use arXiv
as the primary entry only when no formal version is found, the preprint itself
is the cited object, or the user requests it. Never fabricate BibTeX fields.
Treat imported BibTeX as untrusted data: reconstruct entries from verified plain
metadata and exclude directives or TeX control commands. The validator checks
structure only and does not sanitize content for compilation. Never compile
bibliography content under this skill.

Create `notes/<citation_key>.md` only for papers whose claims, evidence,
limitations, method, or citation boundaries need durable analysis. Download a
local paper copy only when explicitly requested and legally appropriate.
When creating a durable note, start from the skill's
`assets/templates/reading_note.md` template.

After every `paper_index.md` edit, run the workspace-level validator described
in `workspace.md`. Every BibTeX key and note filename must match an index key;
indexed exclusions need not have BibTeX entries or notes.
Record verification as `YYYY-MM-DD / <checked version or status>` with a
nonfuture date and resolved suffix. Refresh it before using status-sensitive
claims when the source may have changed.

## Refine ideas

When asked to refine an idea:

1. state the current idea and its unresolved assumptions;
2. identify directly relevant mechanisms and evidence;
3. compare them with the current idea;
4. if persistence is requested, record candidate changes, expected value and
   cost, evidence gaps, risks, and required experiments in `idea_log.md` using
   the [bundled template](../assets/templates/idea_log.md);
5. keep candidates distinct from accepted research decisions.
