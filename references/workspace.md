# Progressive Workspace

## Scope

Use this reference for workspace creation, validation, mode selection, venue/outlet suffix handling, and script usage.

Do not load task-specific references unless the user asks for the corresponding task.

## Flat Workspace Rule

Use one flat workspace under `docs/` for each paper-like project:

```text
docs/<paper_slug>/
```

Create files progressively by task route. Do not create full paper-section scaffolding for literature search, idea refinement, citation audit, or handoff-only work.

## Workspace Modes

| Mode | Create When | Files / Dirs |
|---|---|---|
| `minimal` | workspace anchor only | `README.md`, `venue_profile.md` |
| `literature` | literature search, paper indexing, BibTeX, reading notes | `README.md`, `venue_profile.md`, `paper_index.md`, `references.bib`, `papers/`, `notes/` |
| `idea` | literature-grounded idea refinement | literature files plus `idea_log.md` |
| `citation-audit` | claim/citation checking without section drafting | `README.md`, `venue_profile.md`, `claims.md` |
| `repo-to-paper` | converting repo/code/config into paper sections | full paper workspace |
| `handoff` | paper-state handoff only | `README.md`, `venue_profile.md`, `handoff.md` |
| `full` | user explicitly requests complete paper workspace | full paper workspace |

**Note:** "Workspace Mode" (above) defines the current task's scope and file structure. "Outlet Mode" (defined in `venue_profile.md`) defines the target writing style (e.g., `conference`, `journal`). Do not confuse the two.

## Venue / Outlet Handling

After the target venue or outlet is confirmed, the workspace folder may use a double-underscore suffix:

```text
docs/<paper_slug>__<venue_slug>/
```

**Safety Rule:** You MUST ask the user before renaming a workspace folder. After renaming, immediately update all internal references and subsequent tool call paths to use the new directory name.

Use `venue_profile.md` to record venue/outlet assumptions and the explicit writing mode: `conference`, `journal`, or another stated outlet type.

When the suffix form is present, treat the suffix as an explicit outlet signal. Before drafting paper prose, read `venue_profile.md` and state which outlet-aware mode is being used. Use the mode to guide content emphasis only; do not apply concrete venue-specific prose templates.

## Central Files

- `venue_profile.md`: confirmed or provisional target venue/outlet and writing tendencies.
- `paper_index.md` when present: indexed literature and evidence quality.
- `claims.md` when present: claim ledger linking draft claims to literature, code, experiments, user decisions, or explicit assumptions.
- `idea_log.md` when present: literature-driven idea refinement and rejected options.

## Scripts

Use scripts only for explicit workspace initialization or local validation.

Writes files:

```bash
python scripts/init_paper_workspace.py docs/<paper_slug> --mode literature
python scripts/init_paper_workspace.py docs/<paper_slug> --mode repo-to-paper
python scripts/init_paper_workspace.py docs/<paper_slug> --mode full
```

Read-only validation:

```bash
python scripts/validate_workspace.py docs/<paper_slug> --mode literature
python scripts/validate_paper_index.py docs/<paper_slug>/paper_index.md
python scripts/quick_validate_skill.py .
```

Do not add or rely on scripts that scrape Google Scholar, automatically summarize PDFs, or automatically write related work.
