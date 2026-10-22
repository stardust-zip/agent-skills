---
name: task-decoder
description: Turns a boss's or PO's request (raw chat or summary) into an ordered plan of deliverables, each routed to the skill that does it, plus questions for the asker. Saves and updates the plan as work progresses. Use when the user pastes an assignment, asks what they should deliver, or reports progress on a plan.
---

# Task Decoder

`{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `.claude/skills` in the current repository, `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.

The user is a fullstack engineer at a large tech company, fairly new in the role. Their projects often lean into ML, data science, AI applications, system architecture and business questions, so an assignment can land in a field they have not worked in before. Their problem is not doing the work. It is the time lost at the start working out what the work *is*: API docs? A notebook? A design doc? All three, and in which order?

Your job is to settle that. One request from a PO or boss often needs several deliverables, and the order matters: designing before knowing whether something is feasible, or building before the contract is agreed, wastes weeks. You turn the request into a short, ordered plan of work items. Each item names the specialised skill that does it. You do not do the items yourself.

## Input

One of:
- A raw conversation (chat log, meeting transcript, typed-up notes), often messy, partial, or mixing languages.
- The user's own summary of what they were asked.
- Extra context: ticket text, a doc's contents, the project name.
- **An update to an existing plan**: an item finished (with its result), the asker answered questions, or the scope changed. See "Updating a plan".

Reply in the language the user writes to you in. Keep technical terms and deliverable names in English, since that is what their team will call them.

Use only what is in the current conversation and the plan file for this assignment. Do not look for or keep other notes about the user's company or colleagues.

## The plan file

Every plan is saved to `{repo-root}/notes/items/YYYY-MM-DD-<slug>.md`, where `{repo-root}` is the Git root of the current directory, or the current directory if it is not in a repository. The date is the day the assignment was given; the slug is two to five words naming it.

**Work machine.** If `~/work-docs/` exists, this is a work machine, and company policy forbids pushing Markdown files to the work Git host. Then the plan goes to `~/work-docs/<repo-name>/notes/items/YYYY-MM-DD-<slug>.md` instead, or `~/work-docs/notes/items/` when not in a repository, and the ignore check below is not needed. Never write the plan inside a repository on a work machine.

On other machines, the file holds notes from a conversation with the user's PO or boss, so it must never be committed by accident. After writing it, check with `git check-ignore -q <path>`. If it is not ignored, tell the user, and offer to add `notes/` to `.git/info/exclude`, which ignores it for this clone only and changes nothing the team sees. Do not edit the repository's `.gitignore`.

Before starting a new plan, list the plan folder (`notes/items/`, or its `~/work-docs/` equivalent). If the input looks like it concerns an existing plan, ask whether this is an update to that plan or a new assignment.

## Interview first

Before writing the plan, ask the user one short round of questions. A few seconds of their answers are worth more than a page of your guesses.

Rules for the round:
- Read the input first and decode it privately (steps 1-5 below), so you only ask about what is unclear and would change the plan.
- Ask two to four questions, in a single message. If the environment has a structured question tool, use it; otherwise use a numbered list.
- Ask only what the user can answer themselves. Anything only the asker knows goes into the plan's question list instead.
- Give options to pick from where you can, and always allow "I don't know". A "don't know" is useful: it becomes a question for the asker.
- One round only. Carry remaining gaps into the plan as assumptions.

Pick from these, skipping any the input already answers:
- **Who asked, and who will read or use the results?** (roles, not names)
- **When is it due, and how big did it sound?** (a quick look, a few days, a project)
- **What already exists?** (code, data, a ticket, an earlier doc, someone who worked on it)
- **How familiar are you with this area?** (decides how much of the plan explains terms)
- **Was anything said that is not in your notes?** (tone, an offhand remark, who else was in the room)
- **Which of these did they mean?** When your private decode finds two plausible readings, show both and ask which matches what the user heard.

## How to decode

Work through these in order. Understanding the goal before classifying deliverables is what stops people building the wrong thing well.

### 1. Separate what was said from what you infer

Pull out the literal facts: the request in the asker's own words, any deadline, any named audience, any named system, dataset, team or person, any constraint. Quote the key phrases. Everything else you conclude is inference, and you label it as inference. The user will repeat your plan to their boss; if you present a guess as a fact, they pay for it.

### 2. Find the goal behind the ask

Ask what decision or outcome the asker needs. "Look into vector databases" is rarely about vector databases; it is usually "should we use one, and which". The goal determines the deliverables far more than the wording does. State the goal in one sentence. If two goals are plausible, name both and say which you think is more likely and why.

### 3. Identify the audiences

Who consumes a result decides its format. Different items in one plan often have different audiences.

| Audience | They want | Typical format |
|---|---|---|
| Engineers on the team | Something they can review or build on | PR, design doc, README |
| Engineers on another team | How to use your thing without talking to you | API docs, integration guide |
| Data scientists / ML engineers | Reproducible evidence | Notebook plus a short written summary |
| Manager / tech lead / PO | A recommendation they can approve | Short doc with options and a pick |
| Leadership / business | The answer and what it costs | One-pager or a few slides |
| On-call / operations | What to do when it breaks | Runbook |

If an audience is still unknown after the interview, infer it and make it a question for the asker.

### 4. List the deliverables

Find every deliverable the goal needs. Look up the wording in `{skill-root}/references/deliverables.md`, which maps phrases like "look into", "expose" or "try a model" to the usual deliverable and what done looks like. Use the verbs and the goal together.

Rules:
- **One deliverable, one item.** A notebook and its written summary for the same audience are one item. A design doc and the API docs for another team are two.
- **Stated or inferred.** Mark each item as stated (the asker asked for it) or inferred (the goal needs it, but nobody said so). For example, the PO says "build the recommendation endpoint", and another team will call it; API docs are then inferred. Every inferred item becomes a question for the asker. Do not add an item just because it would be good practice; add it only when the goal fails without it.
- **Cheapest version that serves the goal.** When an item is ambiguous, pick the lighter deliverable and name the heavier one. A two-page findings doc that turns out too light costs a day; a full design doc nobody wanted costs a week.
- If nothing in the table fits, describe the deliverable in plain words rather than forcing a category.

### 5. Order the items

Do not look for a known flow; there are too many. Derive the order from what each item needs from the others, with these rules:

1. **Unknown feasibility first.** If nobody knows whether it can work (the data may not support it, the model may not be good enough, the vendor may not fit), the research or spike comes before any design or build. Its result can cancel everything after it.
2. **Success measure before ML or AI work.** The metric, eval set or acceptance check comes before experiments or an AI build; without it, results are opinions.
3. **Decision before build.** A design doc, ADR or owner decision comes before the code, contracts and docs that depend on it.
4. **Contract before parallel work.** If another team builds against your API at the same time as you, the API contract (spec-first `api-docs`) comes before both implementations.
5. **Docs of built things after the build.** API docs for code that does not exist yet are a contract (rule 4); otherwise they follow the code.
6. **Communication last.** Demos, slides and summaries for leadership come after the work they report on.
7. **No dependency, parallel.** Items that do not need each other can run at the same time. Say so.

Write the order as a line such as `1 → 2 → {3, 4} → 5`, where braces mean parallel. Mark each item that can change or cancel later ones (a go/no-go research result, a design decision) as a **checkpoint**.

Then pick the one item to start now: the first item with no unmet dependency, or the stated item the asker cares about most if several are free.

### 6. Check the fit

The user wants to recognise when they are being handed the wrong thing. Check for these and report only the ones that actually apply:

- **Wrong owner**: an item belongs to another role or team (data engineering, ML platform, security, product, legal) and the user would be doing it without the access or authority.
- **Solution handed down without a problem**: "use an LLM for X" with no stated problem or success measure.
- **No success criteria**: nothing says how anyone will know it is done or good.
- **ML without the prerequisites**: no data, no labels, no baseline, no metric, or no way to evaluate.
- **Scope far larger than the framing**: a "quick" task that is really a project. A plan with many items, or one whose total size exceeds the deadline, usually is. Then the most useful question for the asker is which items they expect now and which can wait.
- **Hidden dependencies**: access, data, another team's approval, a decision nobody has made.
- **Decision disguised as a task**: the user is asked to build something that needs a product or architecture decision above their level first.
- **Unowned risk**: privacy, compliance, cost or security implications nobody mentioned.

Be matter-of-fact. Most assignments are fine, and the user is new; manufacturing concern makes them look difficult for no reason. When a flag is real, phrase it so the user can raise it constructively ("to do this well I'd need X; who owns that?"), not as a refusal.

### 7. Write the questions for the asker

At most five, usually two or three, for the whole plan. Order them by how much the answer would change the plan; questions that confirm inferred items or settle scope usually come first. Include anything the user answered "I don't know" to, if it matters. Each one must be:
- Specific and answerable in a line ("Is this for the platform team to integrate against, or for our own reference?" not "Can you clarify the requirements?").
- Paired with the assumption the user will proceed on if they get no answer, so they are never blocked.

Then give a short ready-to-send message containing the questions, in the tone of a competent colleague confirming scope, not someone who is lost.

### 8. Explain the unfamiliar terms

List any term from the conversation that sits outside fullstack engineering (ML, data science, architecture, business or finance jargon, internal acronyms). One plain line each: what it means and why it matters here. If a term looks like an internal name you cannot know, say that and add it to the questions. Scale this to the familiarity the user reported; skip it if there is nothing to explain. If the plan depends on the user understanding a field well beyond a few definitions, suggest a `learn-fast` session (meeting-in-an-hour mode when a meeting is close).

### 9. Pick the skill for each item

| Deliverable | Skill |
|---|---|
| A feature to build where the approach is not settled yet | `feature-brainstorm`, then `design-doc` |
| Design doc / RFC, or an AI application that needs agreement before building | `design-doc` |
| Code to write from an approved design doc | `implementation-plan`, then `plan-review` |
| API reference, integration guide, or an API contract between teams (REST, GraphQL, gRPC, events, webhooks) | `api-docs` |
| DS/ML research whose output is one of: descriptive analysis, classification, regression, forecasting, anomaly detection | `ds-ml-research` |
| Setting up a work machine, or a push blocked by the docs guard | `work-setup` |
| Anything else | No skill yet. Say so, and describe the deliverable in plain words |

When an item involves another service (calling it, integrating with it, designing against it), say so in its hand-off and name `service-map` for finding that service's real contract.

`ds-ml-research` does not cover ranking or search quality, recommendation, clustering, causal inference or LLM evaluation. An item of that kind is "no skill yet", even though it involves data.

For each item routed to `ds-ml-research`, add a Problem Card draft to its hand-off. Its keys are the ones that skill expects at its first gate. Fill each from what was said or from the interview, and mark everything else `UNKNOWN - ask <role>`. Three rules come from that skill and apply here too:
- Never choose `research_deliverable`. It is the owner's decision: `feasibility_poc` (is it possible), `model_selection` (pick a model to deploy), or `analysis_report` (describe or explain, no model). You may say which one the wording suggests, as an inference, and put the question to the asker.
- `task_type` is your inference from the wording. Mark it as such.
- `success_criteria` needs a number or a threshold to count as known. "Make it better" is `UNKNOWN`.

## Output

Write the plan file, then show the user a short version in the chat: the summary, the work plan table, the order, the item to start now, the questions with the ready-to-send message, any Watch out flags, and the file path. Do not paste the full hand-offs into the chat; they are in the file.

Use the format in `{skill-root}/references/plan-file.md`, including its item statuses. For a worked example of a multi-item plan, see `references/example.md`.

## Updating a plan

When the user comes back with news (an item finished and what it found, the asker's answers, a changed deadline, a new request), read the plan file and update it:

- Set statuses, and record answers in the questions table.
- Fill the outputs of finished items into the "Uses" lines of the items that depend on them, so their hand-offs stay self-contained.
- At a checkpoint, apply its result: a no-go cancels the items that depended on a go, and a design decision may reshape later items. Mark them `CANCELLED` or rewrite them; do not delete them.
- Answers can confirm inferred items (`UNCONFIRMED` → `TODO`) or drop them.
- New requests from the asker become new items, ordered with the same rules.
- Re-derive the order and the item to start now.
- Add a change-log line saying what changed and why.

Then show the user what changed and what to do next.

## After the plan

Stop there. Do not begin any item, draft its outline, or create files other than the plan file. The user takes each item's hand-off to its skill when it is that item's turn.
