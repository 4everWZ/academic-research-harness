---
name: academic-research-harness
description: "Use when explicitly requested to develop a paper from existing results, shape its argument, revise defensive prose, or support that writing with literature, source checks, or paper workspace tools."
---

# Academic Research Harness

Develop the paper's argument from existing research results and express it as manuscript prose.

Use author-designated methods and results as drafting inputs without requiring an independent audit. If material needed for a requested passage is missing or conflicting, pause that passage and ask the author for the specific input. Do not replace it with a gap report, invented limitation, or repository investigation. Inspect code only when the author requests implementation extraction or verification.

Keep author questions and work notes outside manuscript prose. Exclude code variables, internal labels, paths, run identifiers, and workflow metadata from the article. Use scientific descriptions; ask when a necessary mapping is missing.

For project-level writing, locate or create a sibling `<paper_slug>/` with independent Git; follow the project guide below. Keep subsequent work there. Standalone edits and searches need no project setup. Keep outlines in working context unless requested.

## Load for the writing task

| Intent | Load |
|---|---|
| Start or locate a paper project | [paper-project.md](references/paper-project.md), then the relevant writing guide |
| Frame a paper, draft or reorganize sections | [results-to-paper.md](references/results-to-paper.md) and [writing-style.md](references/writing-style.md) |
| Revise prose with the argument established | [writing-style.md](references/writing-style.md) |
| Find literature, prioritizing leading venues in the relevant field; position contributions or refine an idea | [literature.md](references/literature.md) |
| Check a disputed claim or citation | [evidence-and-citations.md](references/evidence-and-citations.md) |
| Extract or check a method against implementation | [repo-to-paper.md](references/repo-to-paper.md) |
| Add auxiliary artifacts or maintain a literature collection | [workspace.md](references/workspace.md) |

Load extra references only for a concrete need. Numerical results alone do not require an audit.
