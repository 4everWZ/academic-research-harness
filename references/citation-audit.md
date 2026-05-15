# Citation Audit and Claim Ledger

## Scope

Use this reference when checking whether citations support claims, whether novelty is overclaimed, whether related work is distorted, or whether paper sections contain unsupported statements.

For workspace creation or validation, load `references/workspace.md`.

For global result, novelty, SOTA, and confirmation boundaries, load `references/evidence-policy.md` when the audit needs the shared policy.

## Core Principle

A citation is valid only if it supports the exact claim being made.

Do not treat a related paper as support for a stronger, broader, or different claim.

## Claim Ledger

Every nontrivial academic claim should be recorded in `claims.md`.

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

Claims marked `unsupported` or `speculative` must not appear as final conclusions.

## Audit Procedure

1. Read the target section.
2. Extract nontrivial claims.
3. Match each claim to `claims.md` when possible.
4. Check whether cited sources directly support the claim.
5. Downgrade overbroad claims.
6. Mark missing evidence.
7. Suggest precise revisions.

## Common Failure Modes

Flag these cases:

- citation supports the general topic but not the exact claim;
- citation is based only on the abstract;
- novelty claim ignores recent strong work;
- SOTA claim does not match dataset, split, metric, or protocol;
- method superiority is claimed without user-provided results;
- weak or downgraded sources are used as key evidence;
- arXiv is used as the only support for a central theoretical claim;
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
