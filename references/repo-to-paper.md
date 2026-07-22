# Repository to Paper

Use this reference to turn code, configuration, architecture, experiment setup,
or verified results into the paper section the user requested. Load
`evidence-and-citations.md` for claims or results and `writing-style.md` for
manuscript prose.

## Establish the evidence boundary

Distinguish implementation evidence, literature, verified results, user intent,
assumptions, and unresolved inference. Do not invent modules, equations, tensor
shapes, training settings, datasets, metrics, losses, or results.

Raw variables, config keys, paths, run IDs, branch names, scratch labels, and
internal codenames are evidence anchors rather than manuscript terminology.
Preserve exact tokens only when they are public artifact names, studied APIs,
reproducibility-critical settings, or data being quoted.

## Synthesize rather than transcribe

Code constrains factual implementation claims; it does not dictate the paper's
section structure, terminology, motivation, or explanatory level. The draft may:

- abstract implementation details into a coherent mechanism;
- connect that mechanism to the research problem and relevant literature;
- choose academically useful organization and terminology;
- explain rationale and expected behavior when clearly separated from measured results;
- foreground the contribution supported by the combined evidence.

Do not mirror the module tree or turn source files into a prose walkthrough.
Academic packaging may clarify and synthesize the work, but it must not create
unsupported novelty, theory, causality, or empirical performance.

## Draft the requested section

Inspect the evidence relevant to that section, then write at the level expected
by the target audience. If `venue_profile.md` exists, use its outlet and audience
constraints as emphasis guidance rather than a rigid prose template.

For methods, explain the mechanism, assumptions, integration point, rationale,
and material computational considerations. For experiments, use only confirmed
datasets, splits, metrics, baselines, protocols, hardware, and implementation
details. For results, follow the provenance rules in
`evidence-and-citations.md`. Mark unresolved factual details explicitly instead
of guessing.

Write only the requested section. Literature collection, repository inspection,
or creation of a result-table structure does not authorize drafting adjacent
sections.
