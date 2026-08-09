# Evidence and Citations

Use this reference for source quality, claims, results, citation audits, novelty, comparisons, contribution boundaries, and SOTA language.

## Evaluate source quality for the claim

No venue, publisher, citation count, or publication date proves a claim. Judge a source by the role it plays and the evidence needed for that claim. Check:

- exact claim support rather than topical similarity;
- formal publication, revision, correction, or retraction status;
- method and protocol clarity;
- dataset, split, metric, and baseline comparability;
- reproducibility signals such as code, data, and sufficient implementation detail;
- conflicts, limitations, and fit to the target subfield.

Peer review and venue standing can raise confidence but do not replace these checks. Treat early or weakly documented work only as attributed, scoped frontier evidence. Never use it as sole support for central novelty, superiority, or final-conclusion claims.

## Track only claims that need a ledger

When persistent tracking is requested, create `claims.md` from the [bundled template](../assets/templates/claims.md) for material claims or unresolved evidence risks, especially:

- novelty, SOTA, superiority, or comparative claims;
- numerical results;
- causal or mechanism explanations;
- contribution claims;
- limitations that change interpretation;
- claims reused across sections whose evidence is incomplete or easy to overstate.

Ordinary background statements with direct, adequate citations do not require a ledger entry. Unsupported or speculative claims stay out of final conclusions. Before relying on a ledger status, manually verify citation keys against the index and BibTeX, and verify implementation or result provenance against source artifacts. Workspace validation does not establish claim semantics. Never infer an approval or verified audit from an unprovenanced ledger value. Direct public handling requires supported status and a verified audit; accepted research decisions require recorded explicit user authorization.

## Validate results

Use a result in manuscript claims only when its provenance is appropriate to the result and method. For computational experiments, verify the applicable code or revision, configuration, dataset and split, metric, baseline, and evaluation protocol. Treat user-provided values as unverified until the needed match is available. A timestamp, run identifier, or result file alone does not establish provenance.

When provenance is incomplete, keep unresolved values and control states in the response or a separate author-facing artifact. Omit the unsupported manuscript sentence; never place the gap anywhere in manuscript source or output. Preserve citation keys only in the manuscript's established citation syntax; ask which syntax to use when none is established. Do not use stronger comparative language than the evidence supports.

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
