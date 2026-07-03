# Source Quality and Freshness

## Scope

Use this reference when selecting, filtering, or auditing sources by freshness, venue fit, arXiv credibility, source priority, or evidence grade.

Load it from `references/literature.md` during paper collection, and from `references/citation-audit.md` when a claim depends on source quality.

## Freshness

Default search weight favors recent work.

For core sources, prefer:

- formally peer-reviewed papers;
- last 1-3 years;
- top conferences or journals recognized by the target subfield.

For fast-moving areas, use the last 1 year as the frontier scan window.

Older sources need a role:

- foundational work;
- strong baseline;
- community-standard method;
- dataset, metric, or protocol reference;
- survey context;
- direct support for a specific claim.

Reduce old papers that are only topically related.

## Priority 1: Core Sources

Use `P1_core` for:

- recent peer-reviewed top-venue or top-journal work matched to the subfield;
- older foundational, strong-baseline, or community-standard work.

Match the venue profile to the actual subfield instead of mechanically restricting all fields to a few generic venues.

## Priority 2: Frontier Supplement

Use `P2_frontier` for last 1 year arXiv or similarly early sources that identify emerging trends or unsettled directions.

Prefer teams with sustained high-quality work in the area.

Then check paper-level evidence:

- public code;
- implementation detail;
- experiment transparency;
- baseline strength;
- dataset, metric, and split clarity;
- community attention;
- later top-venue acceptance signals.

Do not use an arXiv preprint as the only theoretical basis or only support for key novelty, superiority, or final conclusions.

If the same work has a formal conference or journal version, use that version for citation and priority decisions unless the preprint itself is the cited object.

## Priority 3: Background

Use `P3_background` for useful surveys, dataset or metric references, implementation context, or non-central background.

## Strict Downgrade

Default to `downgraded`, `excluded`, `weak`, `low_confidence`, or `reject` for:

- MDPI;
- Hindawi;
- Frontiers;
- low-quality isolated preprints;
- sources lacking reproducibility or citation support;
- marketing-like sources;
- unclear-consensus sources;
- work with weak baselines or unverifiable claims.

These sources are not key evidence, not a primary theoretical basis, and not core support for method superiority or novelty. If mentioned, label the low confidence and use them only as auxiliary context.

## Final Check

Freshness and venue rank help search. Evidence grade still depends on exact claim support, protocol clarity, baseline strength, reproducibility, and fit to the current paper.
