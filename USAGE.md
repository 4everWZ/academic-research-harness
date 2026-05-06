# Usage

## Install in a repo

Copy `research-writing-harness/` into your project, or keep it in a shared skills directory and reference it from your implementation harness.

The harness is OpenAI-style and generic:

```text
skills/<skill_name>/SKILL.md
```

It is intentionally not tied to Claude Code, Codex, Gemini, or any single agent runtime. Agents that can read Markdown instructions should be able to load the router first and then progressively load only the needed task skill.

## Initialize a workspace

From the harness root:

```bash
python scripts/init_paper_workspace.py --slug my_paper --root docs
```

This creates:

```text
docs/my_paper/
  README.md
  venue_profile.md
  paper_index.md
  references.bib
  claims.md
  idea_log.md
  intro.md
  related_work.md
  method.md
  experiments.md
  results_tables.md
  limitations.md
  figures.md
  handoff.md
  papers/
  notes/
```

## Validate a workspace

```bash
python scripts/validate_workspace.py docs/my_paper
python scripts/validate_paper_index.py docs/my_paper/paper_index.md
```

The validators only check structure and obvious table issues. They do not judge research quality.

## Recommended invocation style

Always load the router first:

```text
Use research-writing-harness router.
Task: <specific writing/evidence task>.
```

Then specify the mode:

- literature-only;
- idea refinement;
- venue profile;
- repo-to-paper;
- citation audit;
- handoff.

## Important separation rule

Literature collection does not imply writing.

For example, this should only update paper metadata:

```text
Use research-writing-harness literature mode.
Search papers for <topic> and update paper_index.md and references.bib.
Do not write paper prose.
```

Writing is a separate request:

```text
Use research-writing-harness repo-to-paper mode.
Use the indexed papers and current repo to draft method.md only.
```

## Results rule

Do not ask the harness to invent results. It may create tables and TODO placeholders only unless actual numbers are provided.
