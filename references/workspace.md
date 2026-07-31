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
Treat venue name and status as user-owned decisions. Never infer `confirmed` or
change an existing target or status without explicit user direction.
Run the initializer only with exclusive control of the workspace path; concurrent
renames or link replacement are outside its containment guarantee.

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

Resolve `<skill-root>` as the directory containing this skill's `SKILL.md`.
Run it from the target repository root; use `--workspace-root` only to authorize
a different explicit root.

```bash
python "<skill-root>/scripts/init_paper_workspace.py" docs/<paper_slug> --include literature
python "<skill-root>/scripts/init_paper_workspace.py" docs/<paper_slug> --include literature,ideas,claims
python "<skill-root>/scripts/init_paper_workspace.py" docs/<paper_slug> --include venue --venue "Target Venue" --venue-status confirmed --venue-authority "user confirmation, YYYY-MM-DD" --outlet-mode conference
python "<skill-root>/scripts/init_paper_workspace.py" docs/<new_paper_slug> --include venue --venue "Target Venue" --venue-status confirmed --venue-authority "user confirmation, YYYY-MM-DD" --suffix-venue
```

Available includes are `literature`, `papers`, `claims`, `ideas`, and `venue`.
Existing files are preserved except when explicit venue arguments update
`venue_profile.md`. Use `--suffix-venue` only when the unsuffixed workspace does
not exist; rename an existing workspace separately after approval. Supply
`--venue-slug` with `--suffix-venue` when the venue name has no usable ASCII slug.

Validate the workspace after every index edit:

```bash
python "<skill-root>/scripts/validate_paper_index.py" docs/<paper_slug>
```
