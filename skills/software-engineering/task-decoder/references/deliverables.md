# Deliverables by wording

Used by task-decoder step 4. Match the verbs and the goal together; the goal wins when they disagree.

| What they said | Usually means | Deliverable | Done looks like |
|---|---|---|---|
| "look into", "explore", "investigate", "research" | Spike: reduce uncertainty | Short findings doc (1-2 pages), sometimes a throwaway prototype | A recommendation with evidence, time-boxed |
| "can we...?", "is it possible to...?" | Feasibility check | Findings doc or small proof of concept | Yes / no / yes-if, with the blocker named |
| "compare", "evaluate options", "which should we use" | Decision support | Comparison table plus recommendation; benchmark if performance matters | Criteria, options scored, one pick |
| "design", "propose", "how would we build" | Agreement before building | Design doc / RFC with diagram | Reviewers can approve or object to specifics |
| "decide", "we chose X, write it down" | Record a decision | ADR (architecture decision record) | Context, decision, consequences in one page |
| "build", "implement", "add", "fix" | Working code | PR with tests | Merged, or ready for review |
| "expose", "integrate with", "other teams will call this" | A contract between teams | API spec plus usage docs | Another engineer can call it from the doc alone |
| "document" | Depends entirely on audience | API docs, README, runbook, or onboarding guide | The named reader can do their job from it |
| "analyze the data", "what does the data say", "why did X drop" | Evidence for a question | Notebook plus a written summary of findings | The question is answered in plain words, with the charts behind it |
| "try a model", "train", "fine-tune", "see if ML can do X" | Experiment | Notebook or script, plus an evaluation report against a baseline | A metric, a baseline, and a verdict |
| "how good is it", "measure quality", "is the model/prompt working" | Evaluation | Eval set plus results report | Numbers on a defined test set, with failure examples |
| "build a chatbot / assistant / RAG / agent" | AI application | Eval set, prototype, design doc | A demo on real examples and a way to measure it |
| "demo", "show", "present" | Convince an audience | Working demo and/or slides | Rehearsed, with one clear message |
| "estimate", "how long", "break it down" | Planning | Task breakdown with estimates and risks | Tickets someone could pick up |
| "monitor", "track", "report on" | Ongoing visibility | Dashboard or scheduled report | Metrics defined, owner named |
| "it broke", "what happened" | Explain an incident | Root-cause analysis / postmortem | Timeline, cause, fix, prevention |
| "make the business case", "is it worth it" | Justify spend | One-pager: problem, cost, benefit, risk | A decision-maker can say yes or no |
