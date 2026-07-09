# Paper Writing Style and Research Taste

## Scope

Use this reference when drafting or revising paper prose involving tone, framing, limitations, hedging, or focus.

Do not load this file for workspace creation, citation-format checking, or result-table placeholders.

## Core Principle

Paper prose is not rebuttal.

Default to claim-first prose: say what the work does, scope it to evidence, and keep internal risks out unless they change interpretation.

## Paper-Prose Defaults

- State implementation-confirmed facts directly.
- Hedge only when uncertainty is real and relevant.
- Avoid stacked hedges such as "may possibly suggest" or repeated "although" clauses.
- Surface only boundaries that matter for interpretation.
- Admit only paper-facing facts: concepts, mechanisms, datasets, metrics, public artifact names.
- Keep variable names, config keys, paths, filenames, branch names, run IDs, metadata fields, scratch labels, and internal codenames in evidence notes.
- Translate raw implementation labels into semantic academic terms.
- Preserve exact internal tokens only for public artifact names, studied APIs, critical parameters, or logs quoted as data.
- Keep paper sections organized around reader value.

## Contribution framing

A contribution identifies the paper's main useful move.

Use this shape when possible:

```text
We introduce / develop / analyze [artifact or mechanism] to address [specific problem] under [evidence-supported scope].
```

Good contribution prose:

- names the artifact, mechanism, dataset, analysis, or empirical finding;
- explains reader value;
- scopes only material boundaries;
- avoids repeating limitations already handled elsewhere.

Avoid contribution prose that:

- opens with apologies, missing experiments, or edge-case qualifications;
- says the work is "only", "merely", or "preliminary" unless that is the intended publication category;
- converts every untested variant into a visible qualification;
- hides the main contribution behind caveats.

## Public prose vs internal ledger

Use `claims.md` as the internal ledger for risks, unsupported claims, required evidence, and notes that do not belong in the manuscript.

Manuscripts contain only the selected public-facing handling:

- `state_directly`: evidence supports a direct statement;
- `scope_briefly`: add a compact boundary near the claim;
- `move_to_limitations`: mention only where it changes interpretation or use;
- `omit_from_public_prose`: keep as internal risk or future work planning;
- `needs_user_decision`: ask before changing framing.

Do not omit material limitations affecting validity, reproducibility, comparison fairness, safety, or interpretation. `omit_from_public_prose` is for non-material, speculative, or planning-only reviewer-risk notes.

Risk tracking is not prose drafting. A real concern can be true and still not belong in a contribution paragraph.

If a revision changes contribution framing, load `references/evidence-policy.md` and follow its user-confirmation checkpoints.

## Limitations and Scope

Limitations explain how readers should interpret or apply the work.

Include limitations that affect:

- claim strength;
- evaluation meaning;
- reproducibility;
- domain transfer;
- comparison fairness;
- deployment or safety interpretation.

Limitations are for interpretation, not apology. Explain uncertainty and reader impact.

For paper sections, prefer compact interpretive boundaries:

```text
Because [source of uncertainty], the results support [scoped interpretation] rather than [broader interpretation].
```

## Research taste

Good research writing selects what matters.

Use taste as a focus filter:

- important problem: bottleneck, confusion, or useful gap;
- tractable move: concrete progress path;
- evidence fit: central claim supported by code, data, experiments, or literature;
- reader value: reusable method, result, explanation, or framing;
- selective context: related work and limitations serve the main claim.

Ask before broadening the paper into a larger claim, survey, benchmark suite, or general theory.

## Source Anchors

Nature summaries: https://www.nature.com/nature/for-authors/formatting-guide
Oxford on hedging: https://lifelong-learning.ox.ac.uk/about/hedging
Lingard on limitations: https://link.springer.com/article/10.1007/s40037-015-0181-0
Alon on taste: https://doi.org/10.1016/j.molcel.2009.09.013
Colah on taste: https://colah.github.io/notes/taste/
