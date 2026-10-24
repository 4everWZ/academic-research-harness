# Progressive writing regression

Seven synthetic tasks exercise the skill's actual reference-loading paths: drafting, revision, literature positioning, claim checks, method specifications, material links followed by an abstract, and reading notes followed by manuscript prose. [cases.json](cases.json) owns the requests and original materials. This evaluation complements the broader [behavior cases](../behavior_cases.json).

## Run

From the repository root, create an isolated workspace with the repository's Python environment:

```powershell
python tests/eval_support/progressive_writing.py prepare tmp/progressive-writing-next
```

Give each case a separate fresh-context subagent using its exact entry in `tmp/progressive-writing-next/worker_prompts.json`. Keep the fixture, scoring guidance, previous runs and other cases out of writer contexts. Writers start with the author request and `candidate/SKILL.md`, then select references themselves through `python read.py <relative-path>`. Do not mention a required reference or provide reference contents in their starting prompts. The candidate package is available on disk; it is never preloaded into the prompt. Do not activate installed copies or unrelated skills.

After the writers finish, inspect the reading and artifact evidence:

```powershell
python tests/eval_support/progressive_writing.py audit tmp/progressive-writing-next
```

The audit checks full `writing-style.md` emission against the candidate text, selective reference loading, unchanged source inputs and output presence. It does not grade prose, prove attention, or establish that the agent's tool output was not truncated. Inspect tool responses for truncation and any reads bypassing the interface; invalidate affected loading evidence rather than treating declarations as proof.

Give a separate fresh-context reviewer the author requests, original materials from `fixture.json`, actual output files and traces. Withhold the candidate instructions and prior conclusions. Judge manuscript usefulness, scientific fidelity, removal of work notes and redundant defense, correction of known errors, and preservation of real uncertainty. Notes and README may retain requested work information; manuscript text must express the research. Record each case's pass/fail and evidence in a reviewer-authored JSON file, with `not_reviewed` for anything not assessed. Do not use exact prose matching or a negative-word blacklist.

Retain the run before removing its temporary workspace:

```powershell
python tests/eval_support/progressive_writing.py record tmp/progressive-writing-next 2026-10-25-next --review tmp/progressive-writing-next/review.json
```

`record` preserves the candidate snapshot, original fixture, actual files, full emitted-content traces, audit and supplied review under `runs/<run_name>/`. It also retains failed or incomplete runs, does not overwrite an existing run, and does not delete the workspace. Omitting `--review` records `not_reviewed`; passing evidence checks never creates a behavioral pass. Commit the retained run when it is needed for subsequent iteration. Generated working copies stay under ignored `tmp/`; retained regression materials stay in Git.

## Retained result

The [2026-10-25 review](runs/2026-10-25/review.json) reports seven passes using skill version 0.16.0. Its nine output files were recovered from retained tool-output transcripts after the original temporary workspace was removed. Original trace lines could not be recovered exactly; the retained record contains observed reference order and full-style-emission checks, rather than reconstructed raw logs. See [recovery.json](runs/2026-10-25/recovery.json) for per-artifact provenance and limits. This historical report is not a new run of the persistent tools.

Package tests validate fixture integrity and evaluation tooling. They do not execute the seven model tasks or certify future writing behavior.
