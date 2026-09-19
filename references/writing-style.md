# Direct Academic Prose

## Remove defensive writing

Resolve method ambiguities through the document-led lookup in [repo-to-paper.md](repo-to-paper.md). If required inputs remain missing or conflicting, pause that passage and ask for the specific result, method detail or source. Do not fill the manuscript with unavailable-material reports, unverified results or invented nonperformance. If a missing input is irrelevant to the passage, leave it out and write. A limitation explicitly established by the author or source remains a research fact and may belong in the paper.

State the strongest supported proposition at its actual scope. Do not weaken an observed result to make it harder to challenge. For style-only edits, preserve its epistemic strength.

Put necessary scope inside the claim. Remove disclaimers about claims the paper never makes, hypothetical confounder lists, and repeated qualifications. Retain a boundary wherever omitting it would change the interpretation, including in an independently read abstract or conclusion.

Preserve real uncertainty and tradeoffs. When a defensive sentence also contains a relevant interpretive consequence, express that consequence directly rather than deleting the whole sentence. Remove a contrast only when it denies an unmade claim; do not mechanically ban contrast words or erase a measured disadvantage. A proposed explanation may remain an explicitly identified interpretation, without being promoted to a demonstrated mechanism.

- Defensive: `The method outperforms the baseline on both evaluated datasets. However, this does not imply superiority on every possible dataset.`
- Direct: `The method outperforms the baseline on both evaluated datasets.`
- Material boundary: `The estimated reduction was positive, but its confidence interval included zero.`

## Make the evidence carry the paragraph

Lead a results paragraph with the finding that matters to the argument. Select the values and comparisons that establish it, then explain the consequence when it adds information. Do not append a paraphrase of the finding as a substitute for interpretation or force this into a fixed sentence template.

Use figure and table references where they support that reasoning. Combine visuals answering the same question; remove body text that merely repeats a caption. Keep a visual-led sentence when it introduces organization needed to read the analysis.

Explain method choices through the research need and the operation that addresses it. Avoid retrospective justifications invented to make every implementation choice sound like a contribution.

Do not put source-code intermediate variables, internal module aliases, configuration keys, CLI flags, paths, run/job IDs, branches, or workflow metadata into manuscript prose, even as quoted tokens or generic phrases such as "the recorded run." Express scientific objects, operations, settings and values directly. Mathematical notation defined for the paper and established method names are distinct from implementation identifiers. Translate an internal label only when its scientific meaning is established by the documents or focused lookup; otherwise ask rather than guessing.
