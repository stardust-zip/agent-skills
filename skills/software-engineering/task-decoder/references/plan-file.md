# Plan file format

Used by task-decoder when writing or updating a plan.

```
# [Assignment title]

Asked by: [role]   Asked on: [date]   Due: [date or "not stated"]   Plan updated: [date]

## Summary
[One or two sentences: what the user has to deliver overall, for whom, by when.]
Confidence: high / medium / low - [one line on why]

## What they actually want
[The goal behind the ask.]

## What was said vs. what I'm assuming
Said: [quoted or closely paraphrased facts, including interview answers]
Assuming: [inferences, each one line]

## Work plan
| # | Item | Deliverable | For | Skill | Depends on | Stated / inferred | Size | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | `ds-ml-research` | — | stated | 3 days | TODO |

Order: [e.g. 1 → 2 → {3, 4}]
Checkpoints: [items whose result can change later items, and how]
Start now: item [n] - [why this one]

## Ask before you start
| # | Question | If no answer, assume | Answer |
|---|---|---|---|
Message you can send:
> [short draft]

## Watch out
[Only real flags. Omit if none.]

## Terms
[term - one-line meaning. Omit if none.]

## Hand-offs

### Item [n]: [name]
Skill: [exact name, or "no skill yet"]
Uses: [outputs of earlier items this one needs, or "nothing"]
Done looks like: [2-4 checks]
Task statement:
> [Three to five sentences that state this item on its own: goal, deliverable, audience, deadline, done criteria, known constraints. Pasteable into a fresh session or the named skill without this conversation.]
[Problem Card draft, only for ds-ml-research items:]
  task_type:                   [descriptive | classification | regression | forecasting | anomaly_detection] (inferred)
  research_deliverable:        UNKNOWN - ask <role> [wording suggests: ...]
  business_owner:
  technical_owner:
  decision_user:
  decision_or_action:
  target_definition:
  current_process_or_baseline:
  primary_business_metric:
  primary_model_metric:
  success_criteria:
  stop_criteria:
  operational_constraints:

## Change log
- [date] - Plan created.
```

Item statuses: `TODO`, `IN_PROGRESS`, `DONE`, `BLOCKED` (say on what), `CANCELLED` (say why), `UNCONFIRMED` (an inferred item the asker has not confirmed yet).

Keep it proportionate. A single-item assignment gets a one-row table and one hand-off, and the whole file stays short.
