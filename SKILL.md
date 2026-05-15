---
name: academic-research-harness
description: Use only when the user explicitly requests this skill or explicitly asks to search/curate academic literature, update paper_index/references/claims, refine an idea using papers, convert repo/code into Markdown paper sections, audit citations, or prepare paper handoff. Do not use for normal coding/debugging/training/log analysis/general research chat without an explicit paper-writing or literature-grounding request.
---

# Academic Research Harness

## Purpose

Use this skill as an on-demand paper-writing and evidence-management layer for an existing or evolving research project.

It is a router, not an autonomous research system. The main implementation harness owns code, training, debugging, validation, experiment execution, and code handoff. This skill owns literature evidence, paper index maintenance, claim tracking, Markdown paper sections, citation audit, and paper-writing handoff.

## Activation Boundary

Use only when the user explicitly requests this skill or asks for paper-writing / literature-grounded work.

Do not use for normal coding, debugging, training, log analysis, experiment execution, or general research chat unless the user explicitly asks to connect that work to papers, claims, citations, or paper sections.

## Progressive Disclosure Rule

Start with only this file. Pick one route, then load only the reference files and templates needed for that route.

Do not read all references by default. Do not create a full paper workspace unless the route is `repo-to-paper`, `full`, or the user explicitly asks for complete paper scaffolding.

## Task Router

| User intent | Load | Workspace mode | Template loading |
|---|---|---|---|
| Initialize or validate a paper workspace | `references/workspace.md` | requested mode, default `minimal` | only files being created or checked |
| Search, collect, index, download, classify, or summarize papers | `references/literature.md` | `literature` | `paper_index.md`, `references.bib`, `reading_note.md` only when writing them |
| Refine an idea using papers | `references/literature.md` | `idea` | `idea_log.md` only when writing it |
| Convert repo/code/config/logged setup into paper sections | `references/repo-to-paper.md` | `repo-to-paper` | only the requested section template plus `claims.md` when adding claims |
| Create result tables or placeholders | `references/repo-to-paper.md` | `repo-to-paper` | `results_tables.md` |
| Audit citations, claims, novelty, related work, or SOTA language | `references/citation-audit.md` | `citation-audit` | `claims.md` and the audited section only |
| Prepare paper-state handoff | `references/handoff.md` | `handoff` | `handoff.md` only |
| Check shared evidence, results, or confirmation constraints | `references/evidence-policy.md` | existing mode | only files needed to support the decision |

## Shared Rules

- For workspace creation, validation, mode selection, and scripts, load `references/workspace.md`.
- For novelty, SOTA, superiority, results, claim support, or user-confirmation boundaries, load `references/evidence-policy.md`.
- **Cross-Route Tasks:** If a task spans multiple intents (e.g., search + related work draft), you may load multiple reference files but must still follow progressive disclosure for templates.
- **Tool Usage:** Use `google_web_search` with `site:` filters (e.g., `site:arxiv.org`, `site:openreview.net`) for literature. Use `web_fetch` for abstracts/full-text. Use `grep_search` and `read_file` to probe the repo for logs and configs.
- For cross-file consistency, inspect only the necessary workspace files, normally `venue_profile.md`, `paper_index.md`, `claims.md`, and the target section.
- Do not write unsupported academic claims into paper sections without recording them in `claims.md`.
- Do not write experimental results unless the user provides numbers or verified logs.

## Route Boundaries

- Literature collection must not automatically draft `intro.md`, `related_work.md`, or `method.md`.
- Idea refinement writes candidates to `idea_log.md`; it must not modify code or convert suggestions into final claims without evidence and user decision.
- Repo-to-paper writes only the requested section and marks unknown implementation details as `TODO` or unverified.
- Citation audit checks exact claim support, not topical similarity.
- Handoff updates `handoff.md` only for explicit handoff or material Tier A/B paper-state changes.
