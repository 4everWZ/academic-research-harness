# Evidence and Citations

Use this reference for source quality, claims, results, citation audits,
novelty, comparisons, contribution boundaries, and SOTA language.

## Evaluate source quality for the claim

No venue, publisher, citation count, or publication date proves a claim. Judge a
source by the role it plays and the evidence needed for that claim. Check:

- exact claim support rather than topical similarity;
- formal publication, revision, correction, or retraction status;
- method and protocol clarity;
- dataset, split, metric, and baseline comparability;
- reproducibility signals such as code, data, and sufficient implementation detail;
- conflicts, limitations, and fit to the target subfield.

Peer review and venue standing can raise confidence but do not replace these
checks. Treat early or weakly documented work as a frontier signal, not sole
support for a central novelty, superiority, or final-conclusion claim unless the
paper explicitly frames that limitation and corroborating evidence is unavailable.

## Track only claims that need a ledger

Use `claims.md` for material claims or unresolved evidence risks, especially:

- novelty, SOTA, superiority, or comparative claims;
- numerical results;
- causal or mechanism explanations;
- contribution claims;
- limitations that change interpretation;
- claims reused across sections whose evidence is incomplete or easy to overstate.

Ordinary background statements with direct, adequate citations do not require a
ledger entry. Unsupported or speculative claims stay out of final conclusions.

## Validate results

Use user-provided results or evidence traceable to the relevant code or revision,
configuration, dataset and split, metric, baseline, and evaluation protocol. A
timestamp, run identifier, or file under `logs/`, `runs/`, or `results/` does not
by itself establish that match.

When provenance is incomplete, preserve the table structure or neutral prose,
mark the value or interpretation `TODO` or unverified, and state what must be
matched. Do not use stronger comparative language than the evidence supports.

## Preserve research authority

Ask before a material change to research meaning that is not already authorized
by the user's request, including a new contribution claim, final method choice,
dataset or split, metric, evaluation protocol, or baseline strategy. Routine
editing within an explicitly authorized direction does not require renewed
confirmation.

## Audit citations

For the target text:

1. identify material claims;
2. inspect the cited source at the level needed for each claim;
3. check publication status, source role, and protocol comparability;
4. classify support as supported, partial, unsupported, or speculative;
5. revise the claim, replace the citation, or record the evidence gap.

A related paper is not evidence for a broader statement merely because it shares
the topic.
