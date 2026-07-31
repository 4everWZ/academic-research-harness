# Repository to Paper

Use this reference to convert engineering evidence into paper-facing
propositions before drafting or style revision.

## Establish the evidence boundary

Distinguish implementation evidence, literature, verified results, user intent,
assumptions, and unresolved inference. Do not invent modules, equations, tensor
shapes, training settings, datasets, metrics, losses, or results.

Use author intent for framing or decisions, never as evidence for factual,
novelty, causal, or empirical claims.

Every raw engineering, workflow, or provenance token is an evidence anchor,
not reader-visible manuscript content. This includes source-level variables,
function or module names, config keys, CLI flags, environment variables, paths,
revisions, run or job IDs and names, branches, scratch labels, and internal
codenames. Quoting or replacing a token with generic provenance language does
not override this boundary. Retain an exact name already public in an
authoritative source only when needed for attribution, disambiguation, or
reproducibility. Express material settings through paper-facing names and values.

Complete this filtering before passing propositions to `writing-style.md`. Do
not launder evidence anchors into generic phrases such as "the recorded run."

For material implementation claims, classify behavior as present, enabled, or
executed. Keep the revision, entrypoint, overrides, and reachability in working
context; persist them in `claims.md` only when a ledger is needed. Verify these
facts before saying a method was used or evaluated; code presence establishes
only availability, and an enabled setting does not establish execution in any
experiment.

Transform verified implementation behavior into mechanisms and material
settings; do not mirror the module tree or narrate source files. Keep unsupported
novelty, rationale, causality, and performance outside manuscript source and
output. Route empirical results, citations, novelty, and comparisons through
`evidence-and-citations.md`; route prose through `writing-style.md`.
