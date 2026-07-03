# Citation Audit and Claim Ledger

## Scope

Use this reference to check whether citations support the exact claims made in a paper section.

For workspace creation or validation, load `references/workspace.md`.

For novelty, SOTA, result wording, or source-quality policy, load only the needed evidence files and the relevant shared reference. Use `references/source-quality.md` for source freshness, priority, and downgrade checks.

## Core Principle

A citation is valid only if it supports the claim as written. Related work is not support for a stronger or broader claim.

## Claim Ledger

Record nontrivial academic claims in `claims.md`.

Claim types:

- `background`;
- `method`;
- `experiment`;
- `comparison`;
- `limitation`;
- `speculation`.

Evidence status:

- `supported`;
- `partially_supported`;
- `unsupported`;
- `speculative`.

Unsupported or speculative claims stay out of final conclusions.

## Audit Procedure

1. Inspect the target section.
2. Extract nontrivial claims.
3. Match each claim to `claims.md` when possible.
4. Check direct citation support, source role, and arXiv/formal-version status.
5. Mark unsupported, overbroad, or missing-evidence claims.
6. Suggest precise revisions.

## Common Failure Modes

Flag material mismatches:

- citation supports the general topic but not the exact claim;
- citation is based only on the abstract;
- novelty claim ignores recent strong work;
- SOTA claim does not match dataset, split, metric, or protocol;
- method superiority is claimed without user-provided results or verified logs;
- weak sources are used as key evidence;
- arXiv-only BibTeX entry when a formal version exists;
- venue prestige is used as evidence quality.

## Strong Revision Pattern

Instead of:

```text
Existing methods fail to solve this problem effectively.
```

Use a scoped version:

```text
Several prior methods address related aspects of this problem, but they differ in assumptions, evaluation settings, and supported use cases.
```

Then cite only papers that actually support the scoped statement.

## Output Format

When reporting an audit, use:

1. Supported claims;
2. Partially supported claims;
3. Unsupported or speculative claims;
4. Citation mismatches;
5. Required revisions;
6. Files updated.
