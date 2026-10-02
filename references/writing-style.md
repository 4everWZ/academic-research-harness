# Direct Academic Prose

## Remove defensive writing

Actively remove defensive writing in drafting and revision. Delete disclaimers about claims the paper never makes, hypothetical objections, redundant hedging and repeated qualifications. Their presence in an existing draft does not justify keeping them. Routine removal needs no author confirmation when scientific meaning is clear.

State the strongest supported proposition at its actual scope. Do not weaken an observed result to make it harder to challenge. Preserve scientific content and epistemic strength while removing defensive phrasing.

Put necessary scope inside the claim. Retain a boundary wherever omitting it would change the interpretation, including in an independently read abstract or conclusion.

Preserve real uncertainty and tradeoffs. When a defensive sentence also contains a relevant interpretive consequence, express that consequence directly rather than deleting the whole sentence. Remove a contrast only when it denies an unmade claim; do not mechanically ban contrast words or erase a measured disadvantage. A proposed explanation may remain an explicitly identified interpretation, without being promoted to a demonstrated mechanism.

- Defensive: `The method outperforms the baseline on both evaluated datasets. However, this does not imply superiority on every possible dataset.`
- Direct: `The method outperforms the baseline on both evaluated datasets.`
- Material boundary: `The estimated reduction was positive, but its confidence interval included zero.`

Ask only when a concrete unresolved fact or intended claim would change the scientific interpretation, pausing only that part. Continue removing clear defensive prose elsewhere. For an ambiguous evidence statement, ask about its specific meaning; do not treat every caveat as protected or reopen clear author decisions. A style edit needs no provenance audit. Missing handoff materials are not research findings or proof of nonperformance. Use the [method guide](repo-to-paper.md) only when relevant source clarification is needed.

## Make the evidence carry the paragraph

Organize manuscript prose around the research question, method, findings and interpretation. Never substitute a chronological experiment log, implementation audit or account of locating and checking materials. Put necessary author questions and work notes in the conversation, not the paper.

Lead a results paragraph with the finding that matters to the argument. Select the values and comparisons that establish it, then explain the consequence when it adds information. Do not append a paraphrase of the finding as a substitute for interpretation or force this into a fixed sentence template.

Use figure and table references where they support that reasoning. Combine visuals answering the same question; remove body text that merely repeats a caption. Keep a visual-led sentence when it introduces organization needed to read the analysis.

Explain method choices through the research need and the operation that addresses it. Avoid retrospective justifications invented to make every implementation choice sound like a contribution.

Do not put source-code intermediate variables, internal module aliases, configuration keys, CLI flags, paths, run/job IDs, branches, or workflow metadata into manuscript prose, even as quoted tokens or generic phrases such as "the recorded run." Express scientific objects, operations, settings and values directly. Mathematical notation defined for the paper and established method names are distinct from implementation identifiers. Translate an internal label only when its scientific meaning is established by the documents or focused lookup; otherwise ask rather than guessing.
