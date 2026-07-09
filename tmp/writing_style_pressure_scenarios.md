# Writing Style Pressure Scenarios

These are local TDD artifacts for iterating the skill. They are intentionally
kept under `tmp/` and are not part of the deployed skill.

## Scenario 1: Contribution draft under review pressure

Prompt:

```text
Use academic-research-harness repo-to-paper mode.
Draft the introduction and contribution bullets for an implemented method.
Evidence is available for what the method does, but no final SOTA result exists.
The author is worried reviewers will attack missing ablations.
```

Expected failure before this revision:

- The draft over-emphasizes missing ablations in the contribution area.
- The contribution bullets repeatedly self-limit instead of stating what was done.
- Internal risk tracking language leaks into public prose.

Expected behavior after this revision:

- The introduction states the contribution directly and scopes claims by evidence.
- Missing ablations are tracked internally or placed in a compact limitation area,
  not repeatedly surfaced in contribution framing.

## Scenario 2: Limitations without confession mode

Prompt:

```text
Use academic-research-harness.
Write limitations for a method section where the implementation and setup are
known, but external generalization has not been tested.
```

Expected failure before this revision:

- The limitations template invites a visible list of every not-yet-allowed claim.
- The writing sounds like a rebuttal or apology rather than an interpretive boundary.

Expected behavior after this revision:

- The limitations identify uncertainty that changes how readers should apply the work.
- Unsupported claims remain in the claim ledger instead of becoming prominent paper prose.

## Scenario 3: Taste and focus

Prompt:

```text
Use academic-research-harness literature and repo-to-paper context.
The user asks whether the paper should include every adjacent method family and
every possible limitation, or focus on one clear contribution.
```

Expected failure before this revision:

- The skill pushes broad coverage and defensive completeness.

Expected behavior after this revision:

- The skill treats taste as a focus decision: important problem, plausible attack,
  evidence-supported claim, clear reader value, and selective omission of minor side paths.

## Scenario 4: Engineering artifact ingress

Prompt:

```text
Use academic-research-harness repo-to-paper mode.
Draft the method section from source files, config snippets, experiment logs, and notes.
The evidence includes variable names, config keys, file paths, run IDs, issue labels,
branch names, scratch TODOs, and an internal codename.
```

Expected failure before this revision:

- Raw engineering identifiers appear in manuscript prose as if they were paper concepts.
- Metadata, process labels, and scratch planning notes are treated as method content.
- The method reads like an implementation log rather than academic explanation.

Expected behavior after this revision:

- Raw identifiers are kept as evidence anchors in `claims.md` or notes.
- Manuscript prose uses semantic academic terms for mechanisms, datasets, metrics,
  settings, and public artifact names.
- Exact internal tokens appear only when they are public names, studied APIs,
  reproducibility-critical settings, or quoted logs analyzed as data.
