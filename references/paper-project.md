# Paper Projects and Materials

## Start from the paper

Use the selected manuscript or workspace in place, including downloaded LaTeX with no code, README or Git. Read the target passage and necessary definitions, surrounding text, figures or citations. Follow relevant includes; do not enumerate every file or seek a code checkout. Expand reading when the requested argument or structure needs it.

When first taking on a whole paper with unclear material scope, ask once whether to use only its manuscript, figures and references or also specified external materials. Follow the answer on resume. Local revisions and already stated scopes need no mapping question. No external materials does not mean incomplete research. Ask again only for a concrete gap affecting the passage.

## Optional material links

Read relevant author-designated materials as needed, using current content for a new edit and reusing reads within it. Consult the README's `Research materials` section or equivalent when their locations are needed. Resolve links from that document, even from a paper subdirectory. Do not reread the entry point on every edit or load every linked material.

Document links are continuing author inputs and need no repeated permission to read. A code-directory link identifies a location, not a search scope. Follow the [method guide](repo-to-paper.md) when a spec or explicitly designated implementation is relevant; do not infer authority to inspect code from incidental implementation links.

Keep links for confirmed materials intended for continued use. Update the existing material entry point locally; create a short README section only if persistent links are needed and none exists. Preserve other content, use document-relative paths, and omit one-time inputs. Record only names, links and necessary purposes. The [English template](../assets/templates/paper_readme.md) is illustrative: invent no paths or code association. Without external materials, no mapping file is needed.

Ask for a needed broken link's replacement, or the specific fact resolving a gap or conflict. Pause only the dependent passage. Author corrections take precedence; filename recency does not settle scientific meaning. Reading inputs does not authorize edits or remove established maintenance responsibilities.

## Create or organize a project

Directory discovery, migration and Git initialization belong to requested project setup or organization, not ordinary manuscript edits. When starting a paper from a code project, use the supplied or explicitly linked method descriptions and results; ask for necessary missing materials instead of surveying code. Locate an existing paper from the author's path or known links first; inspect only limited project descriptions if its location remains unclear. Ask about ambiguous candidates or source/destination conflicts.

For a new independent paper, use the author's location. With an explicitly associated code repository and no chosen paper location, use its sibling `<paper_slug>/`; resolve the code Git root when starting in a subdirectory. Keep the established slug, asking if unknown. Reuse an identified existing paper without relocation unless organization or migration is requested. Without a code project, ask for the intended location if none is known.

For requested setup, initialize independent Git and missing starter files:

```bash
python "<skill-root>/scripts/init_paper_project.py" "<paper-dir>"
python "<skill-root>/scripts/init_paper_project.py" "<paper_slug>" --code-root "<code-root>"
```

Without `--code-root`, relative paths use the current directory; with it, they use the actual code root's parent. The helper preserves existing files and creates independent Git, a short English README and `.gitignore`. It does not discover materials, migrate, commit or configure remotes. Use ordinary file tools for material links and migration.

For an authorized move out of a code repository, move the identified manuscript, bibliography, formal figures and required build files to the selected independent paper directory, preserving edits and the paper's own Git history. Leave research source documents in place. Check real paths, file selection and collisions; ask about unresolved ownership or conflicts. Never move code Git metadata or a shared worktree/submodule pointer; resolve linked registrations first. Repair material links, build paths and manuscript backlinks, leaving no duplicate, redirect stub or compatibility symlink. On failure, report actual remaining locations.

Preserve the manuscript's format. Formal text, bibliography and assets should travel with the paper; external material links support authoring, not its build. Use [workspace.md](workspace.md) only for requested auxiliary artifacts. Continue writing without repeating setup.
