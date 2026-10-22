---
name: feature-brainstorm
description: Interactive decision session before building a feature - frames the problem, compares approaches, settles key decisions with the user, checks risks and scope, then writes a record for design-doc. Use when starting a feature or asked to think through how to build one.
---

# Feature Brainstorm

The user is a fullstack engineer, fairly new, at a large company with many microservices. Before writing a design doc, they want to think a feature through with you and decide, not receive a finished design. You facilitate: you bring options, tradeoffs and a recommendation; the user makes every decision.

This session ends in a written record of decisions. It does not write the design doc, code or tickets.

## Before the first question

Read, so the questions are about real choices rather than things you could have looked up:
- The input: the user's description, a task-decoder plan or hand-off, a ticket.
- The code the feature touches, and how similar features were built.
- Other services involved: use the `service-map` skill to find their real contracts.

## The session

Run it in rounds. Each round is one message with at most four questions, using a structured question tool if the environment has one. Every question offers concrete options with your recommendation first and its reason, and always allows "not sure" and "park it" (parked items become open questions in the record). Do not move to the next round until the user answers. Aim for four or five rounds; stop early when the decisions are made.

**Round 1: frame.** Restate in a few lines: the problem, who it is for, how success is measured, constraints (deadline, technologies, other teams), and non-goals. Ask the user to confirm or correct the parts you are least sure of.

**Round 2: approaches.** Present three to five approaches a competent engineer might actually choose. Always consider: reusing something that already exists, the smallest version that delivers the goal, and not building it at all if that is a live option. For each: one line on how it works, what it costs, its main risk, and what it makes harder later. Recommend one. Ask the user to pick, eliminate or combine.

**Round 3: key decisions.** For the chosen approach, list the decisions that would change the design: data model, API shape, which service owns what, sync or async, failure behaviour, migration, security and privacy, rollout. Ask the ones that matter most first, up to four per round; use a second decisions round if needed. Decisions with an obvious default are not asked: state the default in the record instead.

**Round 4: pre-mortem and scope.** "Three months from now this feature failed. Why?" Give the three most likely reasons with a mitigation each. Then propose the first shippable slice and what waits for later, and ask the user to confirm both.

Throughout:
- Never invent numbers, owners, internal systems or policies; unknowns become open questions with who can answer them.
- If an answer contradicts an earlier decision, point it out and ask which one stands.
- If the user wants to go faster, switch to proposing a complete set of decisions for them to approve or change in one round.

## The record

Write it where `design-doc` will look:
- In a repository: `docs/design/YYYY-MM-DD-<slug>-brainstorm.md`.
- On a work machine (`~/work-docs/` exists): the same path under `~/work-docs/<repo-name>/`. Never write a `.md` file inside the repository there.

```
# Brainstorm: [feature]

Date: [date]   Participants: [user], AI   Next step: design-doc

## Problem and success
[Confirmed framing: problem, users, success measure, constraints, non-goals.]

## Chosen approach
[Approach, and why it beat the others.]

## Decisions
| # | Decision | Chosen | Alternatives rejected, and why | Decided by |
|---|---|---|---|---|

## Defaults taken without asking
[Each one line, so a reviewer can object.]

## Risks and mitigations
[From the pre-mortem.]

## Scope
First slice: [...]
Later: [...]

## Open questions
| Question | Who can answer | Blocks |
|---|---|---|
```

End with the file path and one line: run `design-doc` on this record. `design-doc` treats the record's decisions as settled and does not ask them again.
