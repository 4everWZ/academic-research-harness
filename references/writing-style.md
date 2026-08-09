# Academic Writing Style

Use this reference for defensive-writing correction and method continuity.

## Resolve competing instructions

When writing goals compete, preserve claim truth and evidence-calibrated claim strength first, necessary scope second, argumentative continuity third, and concision fourth. This ordering does not override evidence constraints or an exact-claim request. Never gain concision by broadening a claim, increasing its certainty, or removing a boundary that changes interpretation.

## State the strongest supported proposition

State the strongest paper-facing proposition supported by the evidence available to the task and established claim meaning. Do not weaken a supported result merely to make it harder to challenge. In style-only revision, improve directness without changing epistemic strength.

Paper-facing content helps readers understand the research question, method, results, or conclusions. Apply `repo-to-paper.md` before revising engineering or provenance identifiers.

Encode necessary scope in the proposition itself, such as the evaluated datasets, population, conditions, metrics, or comparison set. Prefer a narrower precise proposition to a broader proposition surrounded by hedge language. Add a qualification only when removing it would make the proposition false, materially broader, or misleading.

Place each material boundary at the narrowest point where it changes interpretation. Do not repeat it within the same argumentative context, disclaim claims the paper does not make, or enumerate hypothetical confounders merely because they are possible. Preserve uncertainty required by the evidence, study design, validity, safety, ethics, or an exact-claim revision request.

Repeat a material boundary in a later section only when the later claim would otherwise become broader or misleading; do not repeat it merely for local completeness.

## Advance the argument directly

Keep a sentence only when it adds a premise, evidence, inference, mechanism, consequence, necessary scope, or logical relation. Delete repetitions, hypothetical-objection handling, denials of unmade claims, and explanations that only prevent unlikely misunderstandings.

Give each paragraph one primary argumentative purpose. Combine claims, evidence, mechanisms, and scope when they jointly serve that purpose. Delete repetition and unrelated defensive explanation.

## Integrate figures and tables into the argument

Treat figure and table references as pointers to supporting evidence, not as a running inventory. Lead with the supported finding, comparison, mechanism, or interpretive boundary, and place the reference where it identifies the evidence. When several visuals address the same question, synthesize their relationship instead of assigning one descriptive sentence to each.

Avoid consecutive sentences led by `Figure X shows`, `Table Y reports`, or equivalent frames. Retain a figure- or table-led sentence when the visual's organization, construction, or location must be introduced for navigation or interpretation. Preserve the manuscript's established cross-reference syntax and labels.

Do not use the main text merely to repeat information already available in a caption. Explain the material pattern, comparison, consequence, supported mechanism, or scope boundary. As a diagnostic, remove the figure or table reference: if no meaningful paper-facing proposition remains and navigation is not needed, rewrite or delete the sentence.

## Use logical connections naturally

Use contrast and connective words only when they express a real logical relationship. Remove contrast that merely denies an unmade claim, but preserve distinctions the argument needs. Do not manufacture contrast, inference, causality, escalation, or temporal relations for rhetorical effect, and do not mechanically avoid particular words or constructions.

Do not add background, caveats, transitions, or paraphrases merely to make a revision appear balanced. Add words only when accuracy or a necessary logical relation requires them. Preserve qualifications that change meaning, scope, evidence strength, validity, safety, or ethics.

## Explain method choices naturally

Explain why a method choice matters when the rationale is supported. Connect the research need to the choice naturally; do not force a fixed sentence sequence, invent rationale, or list alternatives the paper does not actually compare.

Revise only paper-facing propositions. If evidence or mapping blocks only part of the requested text, omit only the smallest dependent part, return the rest, and briefly state what is missing outside the manuscript. Do not report unrelated gaps or identifiers that do not affect the requested revision, and do not disclose protected identifiers; use `repo-to-paper.md` for filtering.

## Apply the rules together

Given verified evidence from three benchmark datasets:

- Avoid: `Figure 4 shows that our method consistently outperforms the baselines. However, this does not mean that the method is universally superior across all possible datasets.`
- Prefer: `Our method outperforms all evaluated baselines on the three benchmark datasets (Figure 4).`
