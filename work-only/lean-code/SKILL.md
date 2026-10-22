---
name: lean-code
description: Keeps code changes minimal and boring - reuse what exists, prefer the standard library and installed dependencies, write the smallest correct diff, fix root causes, and never cut safety. Use on any coding task - writing, fixing, refactoring, reviewing or choosing a library.
---

# Lean Code

Every line written is a line someone maintains. The goal is the smallest change that is correct, in the right place, for the problem actually asked.

## First understand, then shrink

Read the task and the code it touches before choosing a solution: trace the real flow end to end and find every caller of what you will change. A small diff in the wrong place is a second bug, not a saving.

## Then pick the first option that works

1. **Is it needed?** If the need is speculative, do not build it; say so in one line.
2. **Does the codebase already have it?** A helper, type, pattern or component a few files away. Reuse it.
3. **Does the standard library do it?**
4. **Does the platform do it?** A database constraint over application checks, CSS over JavaScript, a native input over a widget library.
5. **Does an already-installed dependency do it?** Never add a dependency for something a few lines can do.
6. **Only then** write new code, as little as works.

When two options are equally small, take the one that is correct on edge cases.

## Rules

- **Fix root causes.** A bug report names a symptom. Fix it where all callers pass through, once, rather than patching the one path in the ticket.
- **No speculative structure.** No interface with one implementation, no factory for one product, no configuration for a value that never changes, no scaffolding for later.
- **Prefer deleting to adding,** and plain code to clever code.
- **Touch as few files as possible.** Do not reformat, rename or tidy code outside the change.
- **Name deliberate shortcuts.** When a simplification has a known limit (a global lock, a linear scan), leave a short comment naming the limit and the upgrade path.
- **Leave one check behind.** Non-trivial logic (a branch, a parser, money or security paths) gets one small test that fails if the logic breaks. Trivial one-liners need none.
- **Following an implementation plan?** The plan's scope wins. Do not add what the plan does not ask for; if the plan asks for something heavier than needed, say so and still follow it unless the user agrees to change it.

## Never simplify away

Input validation at trust boundaries, error handling that prevents data loss, security controls, accessibility basics, and anything the user explicitly asked for. If the user wants the fuller version, build it without re-arguing.

## How to report

Code first. Then at most three short lines: what you left out and when it would be worth adding. Give a longer explanation only when the user asks for one.
