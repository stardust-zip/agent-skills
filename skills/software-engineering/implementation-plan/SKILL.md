---
name: implementation-plan
description: Turns an approved design doc into small ordered coding tasks an implementer AI, often a weaker model, can follow without the conversation - exact files, tests first, verify commands, stop conditions. Use when asked for an implementation plan or a plan to hand to another model.
---

# Implementation Plan

The plan is the only thing the implementer will see. Assume it is a capable but literal model with a small context window, no memory of the design discussion, and a tendency to improvise when something is unclear. Every ambiguity you leave becomes a guess, and every guess becomes a bug or an unrequested feature.

## Input

- A design doc, ideally with D3 Approved in its gate table. If it is only at D1, say so and continue only if the user agrees; record "based on an unapproved design" in the plan header.
- The repository the plan targets. Read it: the files the design touches, existing patterns to copy, the test layout, the build and test commands.

## Interview

One round, in a single message, only what the design and code do not answer:
- **Who implements?** A weaker model needs step-level instructions and skeletons for the tricky parts; a strong model needs goals, constraints and checks. Default to weaker.
- **How are tasks delivered?** All at once, or one task per session (then each task must stand alone).
- **Anything off limits?** Files, modules, dependencies, commands, environments.

## Writing the plan

Copy `{skill-root}/assets/plan-template.md` and fill it.

Rules for tasks:
- **Small.** One task changes one concern, roughly under an hour of work or a few hundred lines. Split anything bigger.
- **Ordered so the build stays green.** After every task, the project builds and all existing tests pass.
- **Self-contained.** Each task lists exactly what to read first (`path:line-range`), the files to create or change, the signatures or schemas to implement, and the existing code to copy the pattern from. Never write "similar to the other handler" without the path.
- **Tests first.** For each task with logic, the test to write before the implementation: file, cases, expected results.
- **Verifiable.** Exact commands to run, and what passing looks like. Use the project's real commands, read from its build files.
- **Bounded.** What not to do in this task (no refactors beyond scope, no new dependencies unless listed, no formatting changes to untouched code).
- **Stop conditions.** When reality differs from the plan (a file is missing, a signature differs, a test fails for an unexplained reason), the implementer stops and reports instead of improvising.

For a weaker implementer, add code skeletons for anything non-obvious: function signatures with docstrings, data structures, the shape of a migration. Do not write the full implementation; if a task is so subtle that only full code would do, say the task needs a strong model.

Map every element of the design to at least one task, and every task back to the design. Anything the plan needs that the design does not cover is a question for the user, not a silent addition.

Where it goes: next to the design doc, `docs/design/YYYY-MM-DD-<slug>-plan.md`; on a work machine (`~/work-docs/` exists), the same path under `~/work-docs/<repo-name>/`. Write the file; do not commit it.

## After writing

Tell the user: the number of tasks, the riskiest one, any task that needs a strong model, open questions, and the suggestion to run `plan-review` (ideally with a different model) before handing the plan over.
