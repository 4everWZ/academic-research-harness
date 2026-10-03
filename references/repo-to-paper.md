# From a Method Spec to Paper Text

Use this guide only when a supplied spec or author-designated implementation is relevant. A manuscript need not have either. If the manuscript or supplied description supports the passage, write directly.

## Read the spec

For the `managing-project-docs` spec format, use the sections by their purpose:

| Section | Use in writing |
|---|---|
| Intent | Research aim and scope; an intended outcome is not an observed finding. |
| Contract; Technical semantics, when present | Method inputs, outputs, operations, order, parameter meanings and constraints. These support Methods and formal algorithms. |
| Governing decisions; Open decisions, when present | Read relevant rationale or unresolved choices only when they affect the requested passage. A proposal does not establish which method was evaluated. |
| Acceptance | Requirements, evaluation definitions and verification methods. Use actual findings from supplied evidence for empirical claims; criteria or planned checks alone do not establish results. |

Use equivalent sections in other layouts; missing headings do not imply missing information. Leave the spec unchanged unless maintenance is requested. No separate algorithm document, contract acceptance or implementation audit is needed. Use a spec for the study it describes; ask about concrete mismatches with reported results or unresolved method choices, without routine version audits. Unrelated open items need not delay writing.

## Resolve a method question

When a necessary method detail is unclear, ask the author for its meaning or the material to use. Inspect code when the author requests it, designates an implementation as the source for that question, or has already authorized this use. That instruction remains valid; do not ask again. An incidental implementation link in a document does not itself trigger inspection. Code held by a collaborator is not a prerequisite: a sufficient explanation can resolve the question.

Read the referenced operation and only helpers, callers or definitions needed to resolve the question; then stop. If the entry point is unknown or the meaning remains unclear, ask instead of surveying the repository. If spec and code disagree, ask which method applies.

Code explains operations and parameters, not observed results, actual run settings or whether uncertainty was measured. Defaults are not execution evidence. Ask for necessary missing facts or records; do not reconstruct execution from source or run experiments to fill gaps. Missing estimates do not mean they were never measured.

Express the method through its scientific objects, operations and material assumptions, following [writing-style.md](writing-style.md). Define an abstraction by what it represents and how it is used; do not turn source exclusions into manuscript disclaimers. End with usable paper text and any necessary author question separately, never a code report.
