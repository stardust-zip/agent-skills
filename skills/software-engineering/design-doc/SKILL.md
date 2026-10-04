---
name: design-doc
description: Writes a design doc (RFC) for a feature or system change, grounded in the existing code, tracks it through gates from problem agreement to approval, and prepares the user to defend it in review. Use when the user asks for a design doc, RFC, technical proposal or "how would we build X", brings a task-decoder hand-off item routed to design-doc, or returns with review comments or an approval for an existing design doc. It writes the document only; it does not implement the design.
---

# Design Doc

The user is a fullstack engineer at a large tech company, fairly new in the role, often working on projects that lean into ML, data science and AI applications. At a company like theirs a design doc is how a change gets agreed before anyone builds it: reviewers read it, argue with specific choices, and approve or object.

You have two jobs. Write a doc that reviewers can approve or object to in specifics, and make sure the user can defend it, because their name is on it and they did not make every choice in it themselves.

## Conventions

- `{skill-root}` is this skill's directory.
- The doc template is `{skill-root}/assets/<language>/design-doc.md`, where `<language>` is `en` or `vi`. Copy its structure; do not restate it from memory.
- Reply to the user in the language they write in. The doc's language is chosen separately (see the interview) and recorded in its header.
- In a `vi` doc, write prose in Vietnamese and keep technical terms, gate IDs, statuses and code identifiers in English.

## Work machine: no Markdown in the repository

Check whether `~/work-docs/` exists. If it does, this is a work machine, and company policy forbids pushing Markdown files to the work Git host. Then the design doc goes to `~/work-docs/<repo-name>/` plus the path it would have had in the repository, for example `~/work-docs/<repo-name>/docs/design/2026-10-04-order-sync.md`. Never write a `.md` file inside the repository on a work machine. Diagrams stay as Mermaid blocks inside the doc, so nothing else needs to move.

## Input

One of:
- A task-decoder hand-off item (skill, what it uses from earlier items, task statement), often from a plan in `notes/items/`.
- The user's own description of what needs designing.
- A PRD, a ticket, or notes from a discussion.
- An existing design doc plus review comments, an owner's confirmation, or an approval. Then skip to the gate the doc is at.

## Gates

A doc moves through four gates. Their status lives in the doc's "Gate status" table, so the state survives between sessions.

| Gate | Meaning | Required before it can PASS |
|---|---|---|
| D0 Problem agreed | Everyone agrees on what is being solved | Summary of the problem, goals, non-goals, success measure with target, constraints, reviewers and approver are filled with no `__REQUIRED__` or TBD, and the owner has confirmed them (who and when recorded in the gate table) |
| D1 Design drafted | A reviewable proposal exists | D0 is PASS. Every section of the template filled; at least two real alternatives; diagrams; every assumption marked; nothing from the no-invent list made up; open questions each have someone who can answer them |
| D2 Reviewed | Reviewers have weighed in | D1 is PASS. The doc went to the named reviewers, and every comment the user reports is in the review log as accepted or rejected, with a reason; accepted ones are applied to the doc |
| D3 Approved | Cleared to build | D2 is PASS. The approver's name and date are recorded; every open question is closed or deferred to a named owner |

Gate statuses: `NOT_STARTED`, `PROVISIONAL` (D0 only), `PASS`.

Rules:
- **D0 can be provisional.** If the owner has not confirmed the D0 fields yet, mark D0 `PROVISIONAL`, list the unconfirmed items in the Evidence column, and carry on drafting. D1 can never be marked `PASS` while D0 is `PROVISIONAL`; mark the drafted doc's D1 `NOT_STARTED` with "drafted, waiting on D0" in Evidence.
- **Only the user can report D2 and D3 events.** You may never mark a review as done, a comment as received, or the doc as approved on your own inference. Record them only when the user tells you, with the names and dates they give.
- Never skip a gate or mark one `PASS` without its requirements. If a later change undoes a requirement (for example a review comment changes the goals), drop the affected gates back and say so.
- The document's Status field follows the gates: `Draft` until D1 passes, `In review` during D2, `Approved` after D3, `Superseded` when the user says a newer doc replaces it.

## Must not invent

Never make up any of these. Take them from the code, the input or the user, or leave them unresolved:

- Numbers: traffic, latency, throughput, data volume, cost, SLAs and SLOs, budgets.
- Targets and thresholds: the success measure, its target, acceptance criteria.
- People and authority: owners, reviewers, approvers, which team owns what.
- Internal systems, team names, policies and compliance requirements you cannot see.
- Events: that someone confirmed, reviewed, commented on or approved anything.
- Decisions that belong to someone else: product scope, priorities, a choice the owner is entitled to make.

What to do when one is missing:
- **A measurable fact** (latency, volume, cost): write "to be measured" and how to measure it. Carry on.
- **A D0 field**: mark D0 `PROVISIONAL` and list it. Carry on.
- **A decision that determines the design**, where the reasonable answers lead to different designs and no default is safe (for example "must this survive a region outage?" or "may this data leave the EU?"): stop. End the run with `OWNER_DECISION_REQUIRED`, naming the decision, the options, how each changes the design, and who should decide. Give the user a short message they can send to that person.

## Workflow

### 1. Find the starting point

If the user brought an existing doc, read its gate table and continue from the first gate that is not `PASS`. For D2, go to step 7; for D3, record the approval and check the D3 requirements.

For a new doc, check that a design doc is the right size of answer. It is for a change with real choices: more than one reasonable approach, more than one team affected, or something expensive to undo. If the change is small and obvious, say so, suggest a PR description or a half-page note, and end with `NOT_NEEDED` unless the user still wants the doc.

Scale the doc to the change:
- **Mini** (about one page): one component, a few days of work. Keep every template heading, a few lines each; drop cross-cutting items that do not apply.
- **Standard** (two to five pages): the full template.
- **Large**: past roughly six pages, propose an overview doc plus one doc per component, and write the overview.

### 2. Ground it in what exists

If you are running inside a repository, read before you ask or write.

- **House style.** Look for existing design docs, RFCs or ADRs (commonly `docs/design/`, `docs/rfcs/`, `docs/architecture/`, `docs/adr/`, `rfcs/`) and for a template file, both in the repository and, on a work machine, in `~/work-docs/<repo-name>/`. If the team has its own template, use its sections in place of the skill's template, but keep the header, the Gate status table and the Review log appendix from the skill's template.
- **The relevant code.** Find the components the change touches: entry points, data models, the interfaces between them, and how similar features were built before. Note file paths; the doc cites them.
- **Gaps.** Anything about the current system you could not verify from the code is an assumption and is marked as one.

If there is no repository, work from what the user gives you and say in the context section that the description of the current system is from the user's account.

### 3. Interview the user

One round, two to five questions in a single message, after grounding, so you only ask what the code and input did not answer. Use a structured question tool if the environment has one; otherwise a numbered list. Always allow "I don't know"; those become open questions or provisional D0 items.

Always ask, unless the request already says:
- **Which language should the doc be in, English or Vietnamese?** Do not infer it from the language of the chat.
- **Is there a team template or an example doc to follow?** Skip if you already found one.

Then pick from:
- **Who will review it, and who approves it?** (roles or names)
- **What is fixed already?** Constraints, a deadline, technologies that must or must not be used, a direction the boss already favours.
- **What is explicitly out of scope?**
- **How will anyone know it worked?** A metric and target, or an acceptance check.
- **Has the owner already agreed the problem and goals?** Decides whether D0 can pass now.

Do not ask the user to make design choices in the interview. Propose them in the doc, where the alternatives sit side by side.

### 4. Design it

Work out at least two approaches a competent engineer might actually choose, and pick one. An alternative nobody would choose is padding; if there is truly only one sensible approach, say so and explain why the obvious other option fails.

For each approach, state what it costs: complexity, time to build, operational burden, what it makes harder later. Reviewers trust a doc that states the downsides of its own proposal.

If a decision on the no-invent list blocks the choice between approaches, stop here with `OWNER_DECISION_REQUIRED`.

### 5. Write the doc

Copy `{skill-root}/assets/<language>/design-doc.md` and fill it. Replace every `__REQUIRED__` and `{{...}}` placeholder; anything you cannot fill goes in Open questions, not left as a placeholder.

Writing rules:
- A design doc argues for choices; it is not an implementation manual. Show interfaces, schemas and contracts; leave function bodies out.
- Diagrams are Mermaid blocks: one for the system, one sequence diagram for the main flow, more only if they earn their place.
- When the design involves ML or an LLM, cross-cutting concerns cover evaluation (test set, metric, baseline, bar for shipping), data (source, owner, personal data), model choice (which, why, cost per request, latency) and failure behaviour (what the user sees when the model is wrong, slow or down). If the work is really a research question rather than a build, say so and suggest the `ds-ml-research` skill.
- Non-goals are the most skipped and most useful section. Each one prevents a review argument.
- Write for a reviewer who knows the company's systems but was not in the conversations. Define terms new to the codebase.
- Plain sentences. If a cross-cutting item has nothing real under it, drop it.

Where it goes: follow the repository's convention if there is one; otherwise `docs/design/YYYY-MM-DD-short-title.md`. On a work machine, put that path under `~/work-docs/<repo-name>/` (see above). Write the file; do not commit it.

Then update the gate table per the gate rules.

### 6. Review prep

After writing, give the user this in the chat, in the language they write to you in. It does not go in the doc.

```
## Decisions I made for you
[Each significant choice the user did not make themselves, one line each, with the reason. Read these first; change any you disagree with.]

## Questions reviewers will likely ask
[Three to six, hardest first. Each with a two-line answer, or "no good answer yet" plus what would settle it.]

## Weakest points
[Where the design is thinnest or rests on an unverified assumption. Be candid.]

## Before you send it
[What the user must check or fill in: provisional D0 items to confirm, assumptions to verify, numbers to measure, people to ask.]

## Terms to know
[Concepts from outside fullstack engineering, one plain line each. Omit if none.]
```

Do not soften the weakest points. The user is better off hearing them from you than from a reviewer.

### 7. Handle review comments (D2)

When the user brings comments:
- Add each to the review log: date, reviewer, a one-line summary, `Accepted` or `Rejected`, and the reason.
- Apply accepted comments to the doc. Propose a reason for each rejection, and let the user confirm or overrule it before it goes in the log.
- If a comment changes the problem, goals or non-goals, drop D0 back to `PROVISIONAL` and D1 to `NOT_STARTED`, and say why.
- Mark D2 `PASS` only when the user says review is finished and every reported comment is logged.

## End of every run

Stop there. Do not implement the design or create tickets. End with exactly one state and the gate summary:

- `DRAFTED`: a new doc was written. Example: `DRAFTED — D0: PROVISIONAL (owner has not confirmed the success target); D1: waiting on D0`.
- `REVISED`: an existing doc was updated. Say what changed, and which comments were not acted on and why.
- `OWNER_DECISION_REQUIRED`: name the decision, the options, who decides, and give the message to send.
- `NOT_NEEDED`: a design doc is the wrong size of answer; say what to write instead.
