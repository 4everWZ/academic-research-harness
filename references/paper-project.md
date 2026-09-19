# Independent Paper Projects

Use this guide when starting or locating a paper project. Once its location is established, write there without repeating discovery or initialization. A standalone revision, discussion, or literature search does not require a repository.

## Locate before creating

Check the author's explicit path first, then the known paper project, then sibling candidates and explicit manuscript links in project descriptions. From a code subdirectory, use `git rev-parse --show-toplevel` to find the code root. Inspect only directory names, Git ownership, and the minimum project description needed to establish correspondence; do not recursively search code or experiment files. A directory name alone does not establish that an occupied directory belongs to this paper.

The default new location is `<code-root>/../<paper_slug>/`, with its own Git repository. Preserve the author's specified or already established slug. If none is known, ask for it; do not derive a `<code-name>-paper` name. Multiple candidates, an unrelated occupant, or uncertain Git ownership require an author choice before writes. If a known or discovered manuscript is still inside the code repository, ask whether to continue there or move it into an independent project; do not create a duplicate or move files while waiting.

Reuse a clearly corresponding existing paper directory and its conventions. If it has independent Git, do not reinitialize it. If it has no Git and is outside other repositories, initialize it in place without overwriting its files. A code subdirectory, linked worktree, or submodule does not provide the intended independent project; ask how to handle it. An explicit choice to continue a legacy layout overrides the default, without converting its Git arrangement.

## Initialize the minimum

After resolving the destination, run the helper without reading its implementation. Relative destinations are resolved against the actual code root's parent, even when `--code-root` names a code subdirectory. An explicit absolute destination can reuse a project elsewhere outside other repositories.

```bash
python "<skill-root>/scripts/init_paper_project.py" "<paper_slug>" --code-root "<code-root>"
```

The helper creates independent Git, a short `README.md`, and `.gitignore`; existing files are preserved. It does not choose a slug, discover the matching project, commit, configure a remote, or push. It checks paths and Git ownership before writing. Run it with exclusive control of the destination; if initialization fails, use the reported state to resolve the problem rather than blindly retrying or deleting contents.

Do not precreate manuscript sections, a venue template, evidence ledgers, or reading collections. Add the actual manuscript, bibliography, and final figures or tables as writing needs them. Use [workspace.md](workspace.md) only for requested auxiliary artifacts.

## Write and share from the paper repository

Resolve subsequent edits and Git operations against the paper root, even if the conversation started in the code repository. Keep manuscript format and build conventions already in use; choose a new format when needed for the deliverable. A README's relative code link is informational: the files needed to read or build the paper must live in the paper repository, without absolute local paths or symlinks into code. Formal figure PDFs and images must remain trackable. Copy only author-designated materials needed by the paper; do not mirror the code repository or experiment archives.

Creating a project supplies no research evidence. When a requested passage needs missing material, ask the author and pause that passage. Do not inspect code, validate experiments, or perform new research to avoid asking. Keep these questions outside manuscript prose and retain the writing and literature rules for the actual task.
