# Worked example

Optional. Read it only when unsure how a multi-item plan should look.

**Input:** "PO in planning: 'we want to recommend relevant help articles inside the support ticket form, before the customer submits. the KB team will call our service from their frontend. let's target end of quarter. check with Linh in DS whether our ticket data is even usable for this'"

**Interview:** the user says the results go to the PO, there is no existing recommendation code, and they have never built a recommender.

**Plan (abridged):**

## Summary
Three to four items, ending in a recommendation service that the KB team calls from their frontend, by end of quarter. It starts with a check that the ticket data can support it.
Confidence: medium - the PO named the outcome and one check, but not the intermediate deliverables.

## Work plan
| # | Item | Deliverable | For | Skill | Depends on | Stated / inferred | Size | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Data usability check | Notebook plus findings summary | PO, Linh | `ds-ml-research` | — | stated | 3-5 days | TODO |
| 2 | Recommendation approach and service design | Design doc | Team, KB team | `design-doc` | 1 | inferred | 3 days | UNCONFIRMED |
| 3 | API contract for the KB team | OpenAPI spec plus usage guide | KB team | `api-docs` | 2 | inferred | 2 days | UNCONFIRMED |
| 4 | Recommendation quality evaluation | Eval set plus results report | PO | no skill yet (ranking quality) | 1 | inferred | 3 days | UNCONFIRMED |

Order: 1 → {2, 4} → 3, then implementation (not planned yet; depends on 2 and 3)
Checkpoints: item 1. If the data is not usable, items 2-4 are cancelled and the question goes back to the PO.
Start now: item 1 - everything else depends on whether the data is usable.

## Ask before you start
| # | Question | If no answer, assume |
|---|---|---|
| 1 | Do you want a design doc and API contract before building, or a prototype first? | Design doc and contract, because another team integrates |
| 2 | How will we judge "relevant": click-through on the suggestions, fewer tickets submitted, or a labelled test set? | A labelled test set built with Linh |

## Hand-offs
### Item 1: Data usability check
Skill: `ds-ml-research`
Uses: nothing
Task statement:
> Determine whether historical support tickets and the help-article catalogue are usable for recommending relevant articles at ticket-creation time. Deliver an analysis notebook and a short findings summary for the PO, with a usable / not usable / usable-if verdict. Coordinate with Linh in DS on data access and quality. Due within the first two weeks of the quarter, since the service design depends on it.
Problem Card draft:
  task_type:                   descriptive (inferred: this checks data, it does not build a model)
  research_deliverable:        UNKNOWN - ask PO [wording suggests: analysis_report]
  decision_or_action:          whether to proceed with the article recommender
  success_criteria:            UNKNOWN - ask PO and Linh
