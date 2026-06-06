# Usage Examples

All examples assume `academic-research-harness` is explicitly requested. Load the listed reference, initialize the matching workspace mode only if needed, and keep outputs to the named files.

## Initialize only

```text
Load references/workspace.md.
Create docs/<paper_slug> as a minimal flat paper workspace.
```

## Initialize with confirmed outlet mode

```text
Load only references/workspace.md unless writing starts.
Create docs/<paper_slug>__<venue_slug> as a repo-to-paper or full flat paper workspace.
Set venue_profile.md outlet mode to conference or journal.
```

## Literature search only

```text
Load references/literature.md.
Search high-quality deep learning papers related to [topic].
Update only paper_index.md, references.bib, and reading notes.
Rank sources by evidence quality, not venue alone.
```

## Idea refinement

```text
Load references/literature.md.
Current idea: [paste idea].
Use indexed papers to suggest refinements.
Update only idea_log.md.
```

## Repo to method section

```text
Load references/repo-to-paper.md, plus references/evidence-policy.md only if claim/result/confirmation boundaries arise.
Convert the implemented module into method.md.
Inspect code/config first.
Inspect venue_profile.md and state whether conference, journal, or neutral mode is being used.
Update claims.md for nontrivial claims.
```

## Results placeholders only

```text
Load references/repo-to-paper.md.
Initialize or evolve the workspace with --mode repo-to-paper only if results_tables.md is missing.
Create results_tables.md placeholders for my main comparison and ablation study.
Use TODO for all missing metrics.
```

## Citation audit

```text
Load references/citation-audit.md.
Check whether related_work.md citations support the claims.
Update claims.md with unsupported or partially supported claims.
```

## Paper handoff

```text
Load references/handoff.md.
Prepare paper handoff because the method direction changed.
Classify this as Tier A/B/C and update handoff.md only if needed.
```
