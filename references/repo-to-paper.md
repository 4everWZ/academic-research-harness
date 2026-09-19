# From a Method Spec to Paper Text

For drafting, use documents first. If the spec supports the passage, write without checking code.

## Read the spec

For the `managing-project-docs` spec format, use the sections by their purpose:

| Section | Use in writing |
|---|---|
| Intent | Research aim and scope; an intended outcome is not an observed finding. |
| Contract; Technical semantics, when present | Method inputs, outputs, operations, order, parameter meanings and constraints. These support Methods and formal algorithms. |
| Governing decisions; Open decisions, when present | Read relevant rationale or unresolved choices only when they affect the requested passage. A proposal does not establish which method was evaluated. |
| Acceptance | Requirements, evaluation definitions and verification methods. Use actual findings from supplied evidence for empirical claims; criteria or planned checks alone do not establish results. |

Use equivalent sections in other layouts; missing headings do not imply missing information. Leave the source spec unchanged unless its maintenance is part of the task. Reading it for writing needs no separate algorithm document, contract acceptance or implementation audit. If a relevant method choice remains unresolved, ask the author; unrelated open items need not delay writing.

## Resolve a method question

When algorithm details, operation order or parameter meaning are unclear, follow the spec's implementation link or named entry point without asking for separate permission. Such pointers may appear in any relevant section; the format does not require them. An explicit request to extract or check a method from code also uses this guide.

Read the referenced operation and only the directly relevant helper, caller or definition needed to answer the method question. Stop when it is resolved. If there is no usable implementation pointer, or the narrow lookup leaves the meaning unclear, ask the author rather than expanding into a repository survey. If spec and code disagree about the method, ask which applies instead of silently choosing one.

Code can explain what an operation or parameter means; it cannot establish which settings were actually run, which results were observed, or whether uncertainty was measured. A default value is not an experimental setting. If the requested passage needs missing results, actual run settings or uncertainty estimates, ask the author for those facts or relevant records. Do not reconstruct execution from source or run experiments to fill the gap. Missing estimates do not mean they were never measured.

Express the resolved method as scientific objects, operations, equations or an algorithm block. Keep variable aliases, paths, debugging steps and other implementation metadata out of the manuscript, following [writing-style.md](writing-style.md). A source lookup should end in usable paper text or a specific author question, not a code report.
