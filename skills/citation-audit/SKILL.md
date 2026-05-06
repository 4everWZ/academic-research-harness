# Citation Audit Skill

## Purpose

Check whether draft claims are properly supported by citations, repo evidence, user-provided results, or explicitly marked assumptions.

Use this skill when the user asks to audit citations, related work, claim strength, novelty wording, unsupported statements, or citation-claim alignment.

## Required inputs

Use available files from the paper workspace:

- `paper_index.md`
- `references.bib`
- `claims.md`
- target section file, such as `intro.md`, `related_work.md`, `method.md`, `experiments.md`, or `limitations.md`
- relevant repo/config/log evidence if provided by the user or implementation harness

## Audit targets

Audit:

- broad background claims;
- claims about limitations of existing methods;
- claims about novelty;
- claims about superiority or SOTA;
- claims about efficiency, robustness, deployment, or complexity;
- method mechanism claims;
- experiment setup claims;
- dataset/metric/protocol claims;
- citation placement and relevance.

## Claim status labels

Use exactly one:

- `supported`: evidence directly supports the claim;
- `partially_supported`: evidence supports part of the claim or requires narrowing;
- `unsupported`: evidence is missing or citation does not support the claim;
- `speculative`: claim may be plausible but is not established by evidence.

## Citation support test

For each claim, check:

1. Is there a citation or repo/user evidence?
2. Does the cited source actually support the sentence?
3. Is the claim broader than the source?
4. Does the source use the same task, dataset, metric, split, or setting?
5. Is the source strong enough for this claim?
6. Is a caveat needed?
7. Should the sentence be narrowed or removed?

## Novelty and superiority audit

Novelty and superiority claims are Tier A.

Require human confirmation before accepting wording such as:

- first;
- novel;
- state-of-the-art;
- outperforms;
- significantly improves;
- superior;
- robust across;
- generalizes to;
- solves;
- overcomes existing limitations.

Suggested downgrade patterns:

- `is the first to` -> `explores`
- `outperforms` -> `is evaluated against`
- `solves` -> `addresses`
- `robustly improves` -> `aims to improve`
- `existing methods fail to` -> `some prior methods may be limited by`, only if supported

## Required output: claims.md update

Use this schema:

```markdown
# Claim Ledger

## Claim 001

**Claim text:**
...

**Location:**
intro.md / related_work.md / method.md / experiments.md / results_tables.md / limitations.md

**Claim type:**
background / method / experiment_setup / result / comparison / novelty / limitation / speculation

**Support:**
- code/config:
- literature:
- user-provided result:
- user decision:

**Evidence status:**
supported / partially_supported / unsupported / speculative

**Citation key:**
...

**Audit note:**
...

**Risk:**
...

**Required fix:**
keep / narrow / add citation / move to limitation / mark as speculative / remove / require human confirmation

**Allowed in final paper?**
yes / no / only_with_caveat
```

## Required output: audit summary

Provide:

```markdown
# Citation Audit Summary

## Supported claims
- ...

## Partially supported claims
- claim:
- issue:
- suggested fix:

## Unsupported claims
- claim:
- issue:
- suggested fix:

## Speculative claims
- claim:
- keep only as future work / limitation / hypothesis:

## Tier A confirmation required
- ...
```

## Common failure modes

Watch for:

- citation only supports a narrower claim;
- abstract-level reading used as full evidence;
- conference venue treated as proof;
- weak-signal paper used for central claim;
- dataset mismatch;
- metric mismatch;
- split/protocol mismatch;
- method name similarity mistaken for conceptual equivalence;
- result from one task generalized to another;
- repo intent written as implemented behavior;
- planned experiment written as completed result.

## Completion checklist

Before finishing:

- [ ] all nontrivial claims are classified;
- [ ] unsupported claims have fixes;
- [ ] novelty/SOTA claims are flagged Tier A;
- [ ] citations are not used as decoration;
- [ ] weak sources are not used as central evidence;
- [ ] `claims.md` is updated or a patch is provided.
