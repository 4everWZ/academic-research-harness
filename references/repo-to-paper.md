# Clarify a Method from Implementation

For drafting, use documents first. If the spec supports the passage, write without checking code. When algorithm details, operation order or parameter meaning are unclear, follow the spec's implementation link or named entry point without asking for separate permission. An explicit request to extract or check a method from code also uses this guide.

Read the referenced operation and only the directly relevant helper, caller or definition needed to answer the method question. Stop when it is resolved. If there is no usable implementation pointer, or the narrow lookup leaves the meaning unclear, ask the author rather than expanding into a repository survey. If spec and code disagree about the method, ask which applies instead of silently choosing one.

Code can explain what an operation or parameter means; it cannot establish which settings were actually run, which results were observed, or whether uncertainty was measured. A default value is not an experimental setting. If the requested passage needs missing results, actual run settings or uncertainty estimates, ask the author for those facts or relevant records. Do not reconstruct execution from source or run experiments to fill the gap. Missing estimates do not mean they were never measured.

Express the resolved method as scientific objects, operations, equations or an algorithm block. Keep variable aliases, paths, debugging steps and other implementation metadata out of the manuscript, following [writing-style.md](writing-style.md). A source lookup should end in usable paper text or a specific author question, not a code report.
