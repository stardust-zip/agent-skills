---
name: plan-review
description: Reviews an implementation plan before handover - checks it against the design doc, verifies every cited file, symbol and command exists, and flags ambiguity a weaker model would guess at, ending in a verdict. Use when asked to review or harden an implementation plan.
---

# Plan Review

A plan fails in the hands of a weaker model in predictable ways: it references code that is not there, it leaves a choice open, it bundles too much into one task, or it quietly drifts from the design. Your job is to find those before the implementer does. Review as a different model from the one that wrote the plan when possible; the user picks.

## Input

The plan file, the design doc it cites, and the repository. If the design doc is missing, review against the plan's own goals and say that coverage could not be checked.

## Checks

Work through all of them. Verify against the repository; do not trust the plan's claims.

1. **Coverage.** Every design element maps to a task, and every task maps back to the design. Flag missing pieces and additions the design does not ask for.
2. **References exist.** Every path, line range, function, class, endpoint and config key the plan cites exists (grep or read it). Every command exists in the project (package scripts, Makefile, build files) and is spelled as the project spells it.
3. **Order and green builds.** Each task depends only on earlier tasks, and the build and existing tests can pass after each one. Migrations, schema changes and API changes come in a safe order (expand, migrate, contract).
4. **Task size.** Flag tasks that change more than one concern or would clearly exceed about an hour or a few hundred lines.
5. **Ambiguity.** Flag wording that forces a guess: "handle errors appropriately", "etc.", "similar to", "as needed", "clean up", an interface without types, a test without expected results, "update the docs" without saying which.
6. **Tests.** Each task with logic has tests written first, with concrete cases including an error case. Verification commands show what passing looks like.
7. **Risk.** Data loss, irreversible migrations, security and auth changes, cross-service contract changes, and rollout without a flag or rollback path are called out in the plan, with the safe sequence.
8. **Implementer fit.** For the implementer named in the plan's header, flag tasks that need judgment the plan does not supply, and tasks so subtle they need a strong model.
9. **Rules.** The plan's instructions include stop conditions, scope limits, no new dependencies unless listed, local environment only, and on a work machine no `.md` files committed.

## Output

Findings, most severe first:

```
[BLOCKER | MAJOR | MINOR] Task <n> (or "Plan"): <problem>
  Evidence: <what you checked, path:line or command output>
  Fix: <the exact change to the plan>
```

A BLOCKER means the implementer will fail or build the wrong thing. MAJOR means a likely guess or rework. MINOR means clarity.

Then one verdict:
- `READY`: no blockers or majors.
- `READY_AFTER_FIXES`: only fixes that are mechanical and listed.
- `NOT_READY`: blockers, or a question only the user or the design owner can answer.

Do not edit the plan unless the user asks. When they do, apply the fixes, then rerun the checks that the fixes touched and report the new verdict.
