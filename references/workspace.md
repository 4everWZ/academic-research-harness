# Paper Workspace

## Location

Prefer an established repository convention. Otherwise use one flat workspace:

```text
docs/<paper_slug>/
```

After a target outlet is confirmed, the optional form is:

```text
docs/<paper_slug>__<venue_slug>/
```

Ask before renaming an existing workspace. Repair internal links and subsequent
paths after a rename.

## Create artifacts on demand

| Need | Create |
|---|---|
| literature collection | `paper_index.md`, `references.bib`, and `notes/` |
| local source copies explicitly requested | `papers/` |
| material or unresolved claim tracking | `claims.md` |
| literature-grounded idea refinement | `idea_log.md` |
| outlet-specific emphasis or constraints | `venue_profile.md` |
| manuscript drafting | only the requested section, using the repository or user-selected name |

Do not create a workspace README, empty section files, or a complete paper
scaffold merely because a workspace exists.

## Initialize

Use the initializer only when the user asks to create or extend a workspace:

```bash
python scripts/init_paper_workspace.py docs/<paper_slug> --include literature
python scripts/init_paper_workspace.py docs/<paper_slug> --include literature,ideas,claims
python scripts/init_paper_workspace.py docs/<paper_slug> --include venue --venue "Target Venue" --outlet-mode conference
```

Available includes are `literature`, `papers`, `claims`, `ideas`, and `venue`.
Existing files are preserved except when explicit venue arguments update
`venue_profile.md`.

Validate an index after structural edits:

```bash
python scripts/validate_paper_index.py docs/<paper_slug>/paper_index.md
```
