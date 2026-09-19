# Optional Paper Workspace Tools

Use only for requested workspace or collection maintenance. These utilities are not prerequisites for drafting, revising, searching, or discussing an idea. Use existing manuscript and bibliography conventions where available; the bundled index format is needed only when using this package's index validator.

## Create only the requested artifacts

Use the paper directory already selected through [paper-project.md](paper-project.md), normally a sibling `<paper_slug>/` with independent Git. These optional tools do not choose or initialize its Git repository. Preserve an explicitly requested legacy location.

| Requested artifact | Template or directory |
|---|---|
| Indexed literature collection | [paper_index.md](../assets/templates/paper_index.md), [references.bib](../assets/templates/references.bib), and `notes/` |
| Durable analysis of a source | [reading_note.md](../assets/templates/reading_note.md) |
| Local paper copies | `papers/` |
| Recurring claim or evidence gaps | [claims.md](../assets/templates/claims.md) |
| Idea development record | [idea_log.md](../assets/templates/idea_log.md) |
| Target outlet constraints | [venue_profile.md](../assets/templates/venue_profile.md) |

Resolve `<skill-root>` to this package's directory. From the selected paper directory:

```bash
python "<skill-root>/scripts/init_paper_workspace.py" . --include literature
```

Available includes: `literature,papers,claims,ideas,venue`. Existing files are preserved except for explicit venue updates. Use `--workspace-root` for a different intended root. Run the initializer with exclusive control of the destination path; concurrent renames or link replacement are outside its containment guarantee.

## Maintain the bundled collection

Selected index entries require matching BibTeX keys; excluded entries need not have bibliography entries or notes. Keys use `[A-Za-z][A-Za-z0-9_-]*`; note filenames use the same key. Verification fields use `YYYY-MM-DD / <checked version or status>`, with a nonfuture date and a resolved suffix. Templates define the remaining fields.

The validator accepts a constrained plain-metadata BibTeX format. Reconstruct imported entries from checked metadata rather than copying directives or TeX commands. A percent prefix does not hide an entry from validation. Structural validation does not establish source support or compilation safety.

After completing a batch of collection edits, run:

```bash
python "<skill-root>/scripts/validate_paper_index.py" .
```

## Optional outlet profile

The initializer's `provisional` status is a tool default. To record a confirmed target, use the author's chosen venue with `--venue`, `--venue-status confirmed`, `--venue-authority`, and `--outlet-mode`. These fields belong to the tool's profile schema; ordinary writing does not require a decision record.

Changing confirmed to provisional clears authority/date; reconfirmation needs a new authority value. Repair a legacy provisional profile with stale authority by rebinding its venue as provisional. The `--suffix-venue` option applies only to a new workspace; it does not rename an existing one. Supply `--venue-slug` if the name has no usable ASCII slug.
