# Paper Projects and Materials

## Find the paper

Use the author's path or known project first, then sibling directories and explicit manuscript links. From a subdirectory, use Git to locate the repository root. Read only the project descriptions needed to identify the paper; do not search code or experiments.

Create and migrate papers beside the code repository at `<code-root>/../<paper_slug>/`, with independent Git, unless the author explicitly chose another location. Keep the established slug; ask if unknown. Reuse the matching paper directory; ask about ambiguous candidates or ownership.

## Move an old manuscript

Move an identified manuscript out of the code repository directly; do not offer to keep the old layout. Move its text, bibliography, formal figures and required build files, preserving edits. Leave research source documents and unrelated files in code.

Before moving, resolve source and destination paths, identify the paper files in mixed directories, and check collisions. Ask only about unresolved ownership, file selection or conflicts; do not overwrite either copy. Preserve a paper repository's own Git history, but never move the code repository's Git metadata or a shared worktree/submodule Git pointer. Resolve linked Git registrations before completing the move.

Rebase README material links to their original targets, repair paper asset/build paths, and update explicit links to the moved manuscript. Leave no duplicate, redirect stub or compatibility symlink. Initialize missing starter files after moving; on failure, report the actual remaining locations.

## Use the README's materials

When starting or resuming paper work, read `Research materials` in the paper-root `README.md`, or its existing equivalent. Reuse the mapping if it is already in context and unchanged. Resolve links from the README's directory, including when working in a paper subdirectory.

The code-project link locates the code. Named document links are continuing author inputs: read relevant files across directories without asking again. For algorithms, use the existing method spec's `Contract` and `Technical semantics`, or equivalent descriptions; for Results, use reported findings, not acceptance targets. Read current content for each new edit request, reusing reads within that task. The [method guide](repo-to-paper.md) explains the spec sections and focused implementation lookup for unresolved method details. Do not load all materials or expand into a code or experiment audit.

Add new project materials and update explicitly replaced entries in place. Resolve supplied paths from their stated context, then write README-relative links. Preserve other entries and README content. One-time inputs apply only to the current task and never replace persistent entries. Use names, links and necessary purposes only; add no status, date, version or approval fields. Do not invent file locations. The [English section template](../assets/templates/paper_readme.md) is an example, not a list of actual project inputs; fenced/commented examples and unrelated README links do not register materials.

If a needed path is broken or inaccessible, ask for an accessible location. For source conflicts, unresolved method details or missing experimental facts, pause that passage and ask specifically. An explicit author correction takes precedence; filenames and modification times do not settle scientific conflicts. Missing files do not mean unperformed research.

## Initialize and write

For a new project, or missing starter files after migration, run:

```bash
python "<skill-root>/scripts/init_paper_project.py" "<paper_slug>" --code-root "<code-root>"
```

Relative destinations use the actual code root's parent, even when `--code-root` names a subdirectory. Use an absolute path elsewhere only for an author's explicit location choice. The helper creates independent Git, an English README with only the real code link, and `.gitignore`, preserving existing files. It does not migrate, register documents, commit or configure remotes. Use ordinary file tools for reading, README edits and migration; no parser or sync service.

Continue in the paper repository without repeating setup. Preserve its manuscript and build conventions. Turn supplied materials into scientific prose, formal algorithms and figures, preserving meaning when translating engineering labels. Keep formal reading/build inputs inside the paper repository; the README's external sources support authoring, not the build. Use [workspace.md](workspace.md) only for requested auxiliary artifacts. Pasted-text edits or searches without a paper project need no repository.
