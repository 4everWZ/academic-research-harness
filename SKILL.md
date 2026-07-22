---
name: academic-research-harness
description: "Use when explicitly requested for paper-writing or literature-grounded work: paper workspace setup, literature search and indexing, BibTeX or reading notes, literature-grounded idea refinement, repo-to-paper drafting, claim or citation audits, and academic writing-style revision."
---

# Academic Research Harness

Use this skill as the evidence and writing layer for academic papers. Evidence
rules constrain what the paper may claim; writing rules leave room to synthesize
implementation, literature, and research intent into effective academic prose.

Keep coding, training, debugging, and experiment execution outside this skill
unless the user explicitly connects them to a paper artifact or claim.

## Route the task

| Intent | Load | Typical artifacts |
|---|---|---|
| Create or extend a paper workspace | [workspace.md](references/workspace.md) | only the artifacts needed now |
| Search, select, index, or summarize literature; maintain BibTeX or reading notes; refine an idea from literature | [literature.md](references/literature.md) | `paper_index.md`, `references.bib`, selected notes, optional `idea_log.md` |
| Judge source quality, support a claim, validate results, or audit citations, novelty, comparison, or SOTA language | [evidence-and-citations.md](references/evidence-and-citations.md) | target section, relevant sources, optional `claims.md` |
| Convert a repository, configuration, or experiment setup into a requested paper section | [repo-to-paper.md](references/repo-to-paper.md) | requested section and only the supporting artifacts it needs |
| Draft or revise contribution framing, tone, limitations, hedging, or overly defensive prose | [writing-style.md](references/writing-style.md) | target section; `claims.md` only when evidence handling changes |

Load all applicable references when a task crosses routes, but do not scaffold
unrequested sections. Literature collection does not authorize manuscript
drafting, and idea refinement does not authorize code changes or final research
decisions.
