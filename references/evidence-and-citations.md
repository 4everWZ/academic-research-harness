# Evidence and Citations

Use this reference for source quality, claims, results, citation audits, novelty, comparisons, contribution boundaries, and SOTA language.

## Evaluate source quality for the claim

No venue, publisher, citation count, or publication date proves a claim. Assess source fitness for the claim, not paper quality in the abstract. A source may establish who introduced a method, dataset, or hypothesis without establishing effectiveness, superiority, mechanism, or generality. Match scrutiny to the claim's consequence and inspect only material factors, such as:

- exact claim support rather than topical similarity;
- formal publication, revision, correction, or retraction status;
- method and protocol clarity;
- dataset, split, metric, and baseline comparability;
- reproducibility signals such as code, data, and sufficient implementation detail;
- conflicts, limitations, and fit to the target subfield.

Cite direct support: original studies for study-specific results and reviews or meta-analyses for synthesis claims. Do not cite a later source for a repeated result when the direct source is identifiable.

Peer review and venue standing can raise confidence but do not replace claim-relative assessment. Publication status alone does not determine fitness; apply review or documentation limits only when they change support, and do not reject or globally downgrade a preprint. A source's own claim of novelty, superiority, mechanism, or generality does not establish it.

Account for material dependence among corroborating sources. Reused results, overlapping samples, shared outputs, or derivative analyses are not independent support. A shared public benchmark alone does not establish dependence.

## Track only claims that need a ledger

When persistent tracking in `claims.md` is requested, create it from the [bundled template](../assets/templates/claims.md) for material claims or unresolved evidence risks, especially:

- novelty, SOTA, superiority, or comparative claims;
- numerical results;
- causal or mechanism explanations;
- contribution claims;
- limitations that change interpretation;
- claims reused across sections whose evidence is incomplete or easy to overstate.

Ordinary background statements with direct, adequate citations do not require a ledger entry. A ledger is bookkeeping, not evidence, verification, or authorization; derive its status from the cited support rather than from the entry itself. Unsupported or speculative claims stay out of final conclusions. Before relying on a ledger status in an audit, verify citation keys against the index and BibTeX and verify implementation or result provenance against source artifacts. Workspace validation does not establish claim semantics. Existing ledgers need not be migrated; treat legacy fields as bookkeeping.

## Draft and verify results

For drafting, treat author-supplied results and result artifacts the author designates as drafting inputs. Verify provenance when verification or claim auditing is requested, when sources conflict, or when a claim depends on repository or run provenance. When verification is required for computational results, inspect only the sources and provenance links needed to resolve the claim. State only the conflict or missing link that blocks the requested claim; do not enumerate a standard provenance checklist unless the user requests a full audit. A timestamp, run identifier, or result file alone does not establish provenance.

Never invent missing results or describe drafting inputs as independently verified. When verification or a source conflict blocks only part of a requested claim, keep the unresolved value outside manuscript prose, return unaffected requested text, and briefly state the conflict or missing evidence. Persist unresolved information only when the user requests a named artifact. Preserve citation keys only in the manuscript's established citation syntax; ask which syntax to use when none is established. Do not use stronger comparative language than the evidence supports.

## Preserve research authority

Ask before a material change to research meaning that is not already authorized by the user's request, including a new contribution claim, final method choice, dataset or split, metric, evaluation protocol, or baseline strategy. Routine editing within an explicitly authorized direction does not require renewed confirmation.

## Audit citations

For the target text:

1. identify material claims;
2. inspect the cited source at the level needed for each claim;
3. check publication status, source role, and protocol comparability;
4. classify support as supported, partial, unsupported, or speculative;
5. report the needed revision, replacement, or evidence gap; apply it only when editing or persistence is requested.

A related paper is not evidence for a broader statement merely because it shares the topic.
