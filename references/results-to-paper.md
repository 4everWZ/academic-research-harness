# From Results to a Paper

## Build the argument from the completed work

Start with the supplied findings and the author's research question. Identify the central answer those findings support, then arrange the evidence around the questions a reader must resolve to accept it. When an early project slogan no longer fits the experiments, propose a framing grounded in the completed work; do not quietly redefine the method or evaluation to preserve the slogan.

For a full paper, settle that argument before polishing section prose. For a requested paragraph or section, work locally within the established argument. An outline is a working aid, not a mandatory intermediate deliverable.

Keep research findings separate from the state of the handoff. Missing tables, logs, or definitions may require an author question; they are not findings to narrate in Results or Discussion. Pause the dependent passage rather than substituting a status report about files, verification, or unfinished workflow.

Separate evidence that establishes the main finding, evidence that explains a design choice, and evidence that locates a boundary or cost. Order them by their role in the argument, rather than by experiment chronology or table number. If results are mixed, use the pattern of differences to shape the thesis rather than hiding exceptions in a final limitations paragraph.

## Use each result for the question it answers

| Writing situation | Useful move |
|---|---|
| Main benchmark table | Select the comparisons that decide the research question. Distinguish consistent gains from gains concentrated in a condition; do not let an average obscure a reversal that changes the thesis. |
| Component ablation | State what changes under the tested removal or replacement. Its performance cost supports the component's role under that intervention; it does not by itself establish the proposed internal mechanism. |
| Robustness or transfer | Organize by the shift or condition where behavior changes. Make adaptation inputs, such as labeled target examples, part of the interpretation when they determine what kind of robustness was evaluated. |
| Efficiency comparison | Connect the observed quality gain to its measured cost. Equal parameter count does not cancel higher latency; a measured latency difference should not be converted into an untested deployment verdict. |
| Sensitivity analysis | Explain where the conclusion holds, weakens, or reverses. Use this to locate an operating range rather than describing every curve point. |
| Null or uncertain result | State what remains unresolved and how that affects the paper's central answer. Do not turn lack of established improvement into equivalence or add generic future-work prose. |

## Carry the same argument across sections

Write contribution statements as research advances established by the work. A list of implemented modules or completed experiments does not explain the advance. Keep a proposed framing distinct from an author-approved change in research meaning.

Build Methods around the objects and operations needed to understand the result. Introduce a component's rationale where its role becomes clear; supply material settings where they affect interpretation or reproduction, without reconstructing the source tree.

Use Discussion to explain what the combined findings change about the motivating problem. Separate observed patterns from candidate explanations; plausible explanations can be discussed as interpretations without claiming they were experimentally established.

Derive the abstract and conclusion from the resulting argument. Keep any resource requirement, exception, or uncertainty that changes the central claim, even if it is already explained in Results. Apply outlet-specific structure and reporting rules when a target outlet is supplied; do not import another field's conventions by default.
