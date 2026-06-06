# Paper Writing Style and Research Taste

## Scope

Use this reference when drafting or revising paper prose where tone, contribution framing, limitation placement, hedging, or research focus is involved.

Do not load this file for mechanical workspace creation, citation-format checking, or result-table placeholders.

## Core Principle

Paper prose is not rebuttal.

Default to claim-first, evidence-calibrated writing: say what the work does, scope the claim to the evidence, and keep internal risk notes out of prominent paper prose unless they change interpretation.

## Paper-Prose Defaults

- State implementation-confirmed facts directly.
- Use hedging only when uncertainty is real and relevant to the claim.
- Avoid stacked hedges such as "may possibly suggest" or repeated "although" clauses.
- Surface only boundaries that matter for interpretation.
- Keep paper sections organized around reader value.

## Contribution framing

A contribution should identify the paper's main useful move.

Use this shape when possible:

```text
We introduce / develop / analyze [artifact or mechanism] to address [specific problem] under [evidence-supported scope].
```

Good contribution prose:

- names the artifact, mechanism, dataset, analysis, or empirical finding;
- explains why it matters for the reader's problem;
- scopes only the boundary that materially affects the claim;
- avoids repeating limitations already handled elsewhere.

Avoid contribution prose that:

- opens with apologies, missing experiments, or edge-case qualifications;
- says the work is "only", "merely", or "preliminary" unless that is the intended publication category;
- converts every untested variant into a visible qualification;
- hides the main contribution behind caveats.

## Public prose vs internal ledger

Use `claims.md` as the internal ledger. It may contain risks, unsupported claims, required evidence, and notes that do not belong in the manuscript.

The manuscript should contain only the public-facing handling selected for each claim:

- `state_directly`: evidence supports a direct statement;
- `scope_briefly`: add a compact boundary near the claim;
- `move_to_limitations`: mention only where it changes interpretation or use;
- `omit_from_public_prose`: keep as internal risk or future work planning;
- `needs_user_decision`: ask before changing framing.

Do not omit material limitations that affect validity, reproducibility, comparison fairness, safety, or interpretation. `omit_from_public_prose` is for non-material, speculative, or planning-only reviewer-risk notes.

Risk tracking is not prose drafting. A real concern can be true and still not belong in a contribution paragraph.

If a revision changes contribution framing, load `references/evidence-policy.md` and follow its user-confirmation checkpoints.

## Limitations and Scope

Limitations should explain how readers should interpret or apply the work.

Include limitations that affect:

- claim strength;
- evaluation meaning;
- reproducibility;
- domain transfer;
- comparison fairness;
- deployment or safety interpretation.

Limitations are for interpretation, not apology. Explain the source of uncertainty and its reader impact.

For paper sections, prefer compact interpretive boundaries:

```text
Because [source of uncertainty], the results support [scoped interpretation] rather than [broader interpretation].
```

## Research taste

No paper is complete. Good research writing selects what matters.

Use taste as a focus filter:

- important problem: the paper addresses a bottleneck, confusion, or useful gap;
- tractable move: the authors have a concrete way to make progress;
- evidence fit: the central claim is supported by code, data, experiments, or literature;
- reader value: the paper gives readers a reusable method, result, explanation, or framing;
- selective context: related work and limitations serve the main claim instead of expanding into a survey.

Ask before broadening the paper into a larger claim, survey, benchmark suite, or general theory.

## Source Anchors

- Nature article summaries foreground background, rationale, main conclusions, and field context: https://www.nature.com/nature/for-authors/formatting-guide
- Oxford writing guidance treats hedging as strategic and warns against over-hedging: https://lifelong-learning.ox.ac.uk/about/hedging
- Lingard distinguishes reflective limitations from confessional or dismissive limitation writing: https://link.springer.com/article/10.1007/s40037-015-0181-0
- Uri Alon frames good problem choice around feasibility and interest: https://doi.org/10.1016/j.molcel.2009.09.013
- Colah's research taste notes emphasize focus, community taste, and whether a proposed paper would be exciting to read: https://colah.github.io/notes/taste/
