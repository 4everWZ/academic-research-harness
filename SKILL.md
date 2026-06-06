---
name: academic-research-harness
description: Use when explicitly requested for paper-writing or literature-grounded work: paper search/indexing, BibTeX/reading notes, idea refinement, repo-to-paper Markdown drafting, claim/citation audits, writing-style revision, or paper handoff.
---

# Academic Research Harness

## Purpose

Use this skill as an on-demand paper-writing and evidence-management layer for a research project.

It routes paper-facing work: literature evidence, paper indexes, claim tracking, Markdown paper sections, citation audits, and paper handoff. Keep code, training, debugging, validation, and experiment execution in the main implementation harness unless the user explicitly connects them to paper writing.

## Activation Boundary

Use only for explicit paper-writing or literature-grounded work. Normal coding, debugging, training, log analysis, and general research stay outside this skill unless the user asks to connect them to papers, claims, citations, or sections.

## Progressive Disclosure Rule

Start with this file, choose the route, then load only the reference files and templates needed for the task.

Create workspaces progressively. Use `full` only when the user asks for complete scaffolding; otherwise create the route's minimal files and add section templates only when they are being drafted.

## Task Router

| User intent | Load | Workspace mode | Template loading |
|---|---|---|---|
| Initialize or validate a paper workspace | `references/workspace.md` | requested mode, default `minimal` | only files being created or checked |
| Search, collect, index, download, classify, or summarize papers | `references/literature.md` | `literature` | `paper_index.md`, `references.bib`, `notes/<citation_key>.md`, and `papers/*.pdf` only when writing/downloading them |
| Refine an idea using papers | `references/literature.md` | `idea` | `idea_log.md` only when writing it |
| Convert repo/code/config/logged setup into paper sections | `references/repo-to-paper.md` | `repo-to-paper` | only the requested section template plus `claims.md` when adding claims |
| Create result tables or placeholders | `references/repo-to-paper.md` | `repo-to-paper` | `results_tables.md` |
| Draft or revise writing style, contribution framing, limitation placement, or over-defensive prose | `references/writing-style.md` | existing mode | target section plus `claims.md` when claim handling changes |
| Audit citations, claims, novelty, related work, or SOTA language | `references/citation-audit.md` | `citation-audit` | `claims.md`, audited section, and only the needed evidence files (`paper_index.md`, `references.bib`, relevant notes/sources) |
| Prepare paper-state handoff | `references/handoff.md` | `handoff` | `handoff.md` only |
| Check shared evidence, results, or confirmation constraints | `references/evidence-policy.md` | existing mode | only files needed to support the decision |

## Shared Rules

- For workspace creation, validation, mode selection, and scripts, load `references/workspace.md`.
- For novelty, SOTA, superiority, results, contribution framing, claim support, or user-confirmation boundaries, load `references/evidence-policy.md`.
- For writing style, contribution framing, limitation placement, or over-defensive prose, load `references/writing-style.md`.
- If a task spans routes, load the relevant references but keep template loading minimal.
- Use available browsing/search tools with `site:` filters when supported for literature. Use available fetch/open tools for abstracts and full text. Use local search and file-reading tools for repo evidence. Do not invent tool names.
- For cross-file consistency, inspect only the necessary workspace files, normally `venue_profile.md`, `paper_index.md`, `claims.md`, and the target section.
- Record nontrivial paper claims in `claims.md`.
- Report results only from user-provided numbers or verified logs.

## Route Boundaries

- Literature collection must not automatically draft `intro.md`, `related_work.md`, or `method.md`.
- Idea refinement writes candidates to `idea_log.md`; it must not modify code or convert suggestions into final claims without evidence and user decision.
- Repo-to-paper writes only the requested section and marks unknown implementation details as `TODO` or unverified.
- Citation audit checks exact claim support, not topical similarity.
- Handoff updates `handoff.md` only for explicit handoff or material Tier A/B paper-state changes.
