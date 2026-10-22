# Implementation plan: {{FEATURE}}

| Design doc | Design status | Implementer | Delivery | Created |
|---|---|---|---|---|
| {{DESIGN_DOC_PATH}} | {{D3 Approved / D1 only, user agreed}} | {{weaker / strong model}} | {{all at once / one task per session}} | {{DATE}} |

## Instructions for the implementer

Read this section before every task.

1. Do the tasks in order. Do not start a task before the previous one is checked off.
2. For each task: read the "Read first" files, write the tests, implement, run the verify commands, then tick the task's checkbox and fill its "Result" line.
3. Do only what the task says. No refactoring, renaming, reformatting or "improvements" outside it. No new dependencies unless the task lists them.
4. If anything differs from this plan (a file or function is missing, a signature is different, a command fails, a test fails and you do not know why), stop. Write what you found in the "Deviations" table and ask. Do not work around it.
5. Never touch environments other than local. Never commit secrets. {{Work machine: never commit .md files.}}
6. Commit after each task with the message given in the task.

## Project facts

- Build: `{{command}}`
- Test (all): `{{command}}`
- Test (one file): `{{command}}`
- Lint / format: `{{command}}`
- Conventions to follow: {{naming, error handling, logging, with a path to an example of each}}

## Tasks

### [ ] Task 1: {{name}}

Goal: {{one sentence}}
Design reference: {{section of the design doc}}
Read first: {{path:line-range, ...}}
Change: {{files to create or modify}}
Interface: {{signatures, schemas, endpoints, with a skeleton for anything non-obvious}}
Pattern to copy: {{path:line-range}}
Tests first: {{test file; cases with inputs and expected results}}
Verify: `{{command}}` → {{what passing looks like}}
Do not: {{explicit exclusions for this task}}
Commit message: {{message}}
Result: {{filled in by the implementer}}

## Coverage

| Design element | Task(s) |
|---|---|

## Deviations

| Task | What differed | What the implementer did | Resolution |
|---|---|---|---|

## Open questions

| Question | Who can answer | Blocks task |
|---|---|---|
