# Direct Academic Prose

## Remove defensive writing

Remove defensive writing throughout drafting and revision. A whole-paper task includes abstract, contributions, body, conclusion, captions, tables and supplementary prose; a local edit stays local. Existing wording has no exemption. Routine removal needs no author confirmation.

Delete rebuttals to unmade claims, imagined objections, apologetic self-diminishment, redundant hedging and repeated qualifications. Do not move them to Limitations or polish them into disclaimers. Rebuild useful scope around what the study models, measures or establishes. An overclaiming guard constrains the claim; it does not require appending its negation once the claim is correctly scoped.

## Replace rebuttal with a precise research model

State the strongest supported proposition at its actual scope. In machine learning and computer science, use relevant task distributions, supervision, model assumptions, comparison protocols or resource budgets. Select details that explain the argument, not a modeling checklist. Other fields use their own research objects and study conditions.

| Defensive pattern | Substantive replacement |
|---|---|
| Lists of what a dataset or system is not | Task, inputs, outputs, data construction and system role. |
| Dismissing an ablation as "only" a test | Measured effect, e.g., accuracy loss after removing attention, under its comparison protocol. |
| Denials of universal superiority | Evaluated distribution and supervision inside the finding. |
| Apologies for simplifications | Material assumptions and their interpretive consequences. |
| Generic deployment warnings | Observed operating constraints or measured tradeoffs. |

Match optimality, causal, independence, invariance and generalization claims to the proof, design or evaluation. Distinct inputs or modules do not establish independence; an observed best score is not an upper bound. Meaning-preserving edits need no approval or audit; propose central claim changes separately. Preserve input provenance and metric definitions.

Preserve real uncertainty, negative findings and tradeoffs with their consequences. Negative syntax is not inherently defensive: `Improvement was not established` can be the result. Keep explanations identifiable as interpretations. State an unevaluated recommendation's status once within its purpose: `We propose an untested retrieval extension to reduce unsupported answers.` Do not append a second nonvalidation warning. Include necessary scope in independently read abstracts, conclusions and captions without generic warnings.

Ask about necessary missing facts or scientific ambiguity; pause that part and revise the rest. Do not reopen resolved decisions. Missing material is not a negative finding or proof of nonperformance; even "untested" requires author evidence. Use the [method guide](repo-to-paper.md) for source clarification.

Check every included surface for residual or new defensive framing. Keep author questions separate; no removal ledger.

## Make the evidence carry the paragraph

Organize prose around the research question, method, findings and interpretation, never an experiment log, implementation audit or material-gap report.

Lead with the finding, support it with decisive comparisons and explain useful consequences. Avoid repetition and fixed sentence templates.

Use figure and table references for reasoning and navigation; combine related visuals and remove caption repetition.

Explain method choices through research needs and operations, without inventing retrospective rationales.

Exclude internal variables, module aliases, configuration keys, CLI flags, paths, run/job IDs, branches and workflow metadata, including substitutes such as "the recorded run." Express scientific objects, operations and settings directly. Preserve paper-defined notation and established method names. Translate internal labels only when their meaning is known; otherwise ask. Author-requested reproduction commands belong in separate reproduction files, not narrative prose.
