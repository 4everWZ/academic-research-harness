# Usage Examples

## Initialize only

```text
Use academic-research-harness.
Create docs/<paper_slug> as a flat paper workspace.
Do not search literature.
Do not write paper content.
```

## Initialize with confirmed outlet mode

```text
Use academic-research-harness.
Create docs/<paper_slug>__<venue_slug> as a flat paper workspace.
Set venue_profile.md outlet mode to conference or journal.
Do not add concrete venue-specific writing templates.
```

## Literature search only

```text
Use academic-research-harness literature mode.
Search high-quality deep learning papers related to [topic].
Update only paper_index.md, references.bib, and reading notes.
Do not write introduction or related work.
Rank sources by evidence quality, not venue alone.
```

## Idea refinement

```text
Use academic-research-harness idea refinement mode.
Current idea: [paste idea].
Use indexed papers to suggest refinements.
Do not modify code.
Do not optimize for novelty alone.
Write only to idea_log.md.
```

## Repo to method section

```text
Use academic-research-harness repo-to-paper mode.
Convert the implemented module into method.md.
Inspect code/config first.
Read venue_profile.md and state whether conference, journal, or neutral mode is being used.
Do not invent tensor shapes.
Do not write results.
Do not claim novelty.
Update claims.md for nontrivial claims.
```

## Results placeholders only

```text
Use academic-research-harness.
Create results_tables.md placeholders for my main comparison and ablation study.
Do not fill values.
Use TODO for all missing metrics.
```

## Citation audit

```text
Use academic-research-harness citation-audit mode.
Check whether related_work.md citations support the claims.
Update claims.md with unsupported or partially supported claims.
Do not rewrite the whole section unless necessary.
```

## Paper handoff

```text
Use academic-research-harness.
Prepare paper handoff because the method direction changed.
Classify this as Tier A/B/C and update handoff.md only if needed.
```
