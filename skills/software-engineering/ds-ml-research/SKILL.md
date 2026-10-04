---
name: ds-ml-research
description: Use when initializing, executing, auditing, or reviewing data-science or machine-learning research, including datasets, EDA, baselines, experiments, evaluation protocols, model comparisons, anomaly detection, forecasting, or production handoff.
---

# DS/ML Research

## Overview

Run DS/ML research through a reproducible, evidence-backed gate system. The canonical standard is [`references/standard.md`](references/standard.md); this file routes the work and does not duplicate that standard.

**Core principle:** a claim is valid only when it traces to a versioned dataset snapshot, code revision, experiment run, evaluation protocol, and persisted artifact.

## Conventions

- `{skill-root}` is this skill directory.
- `{project-root}` is the Git root of the service repository or submodule that owns the data and model (for example `~/projects/example-ml-service`). It is never the umbrella repository that only aggregates submodules; if the current directory is an umbrella root, ask which service repository to use.
- `{topic-dir}` is `{project-root}/notebooks/<research-slug>`.
- Local `AGENTS.md`, `CLAUDE.md`, security rules, and service constraints take precedence for tool and storage choices. They do not waive the research gates, evidence contract, or leakage controls.

## On Activation

1. Resolve `{project-root}` and read applicable repository instructions.
2. Determine the mode: **initialize**, **execute**, **audit**, or **review**. Infer it from the request; ask only when the requested outcome cannot be inferred.
3. Read sections 1–5 of `references/standard.md`, the section mapped to the current gate below, and `references/writing.md` before writing any prose artifact.
4. For a new topic, ask the user whether the research is in English (`en`) or Vietnamese (`vi`) unless the request already says so. Do not infer it from the language of the chat. Then run:

   ```bash
   python -B {skill-root}/scripts/init_research.py \
     --project-root {project-root} \
     --slug <research-slug> \
     --environment <environment> \
     --domain <domain> \
     --language <en|vi>
   ```

5. For an existing topic, read `research-plan.md`, take the topic language from `language:` in section 1, determine the first gate not marked `PASS`, and run the structural validator before changing research artifacts:

   ```bash
   python -B {skill-root}/scripts/validate_research.py {topic-dir}
   ```

6. Execute only the current gate, in the order of `references/writing.md` section 3.4: write the questions and each block's **What to look for** criterion, implement one module function per question, execute the notebook with placeholder answers, then write each **Answer** and the findings table from the executed outputs, checking every number against them. Persist the required artifact and append the experiment or decision to `research-log.md`. When rewriting a notebook whose results are already known, follow section 3.5.
7. Run the validator again. Report the terminal state and the exact failed rule or required owner decision.

## Gate Routing

| Current work | Read from `references/standard.md` | Primary artifact |
|---|---|---|
| G0 Problem framing | sections 4–6, including the owner-chosen `research_deliverable` | Problem Card |
| G1 Data readiness | section 7 | Data Contract, manifest, quality report |
| G2 Evaluation design | sections 3 (G2 order) and 8, including the feature contract in 8.5 | frozen Evaluation/Analysis Protocol and feature contract |
| G3 Baselines | section 9 | baseline runs and comparison |
| G4 Candidates | section 10, including the approach-space record in 10.2 | hypothesis runs or no-change decision |
| G5 Locked test | sections 11–12 | locked-test and stress-test report |
| Notebook/log work | sections 13–14 and `references/writing.md` | reproducible, self-explaining notebook and log entry |
| G6 Handoff | sections 15–17 | model card, monitoring and rollback |

Read `references/evidence.md` only when auditing evidence coverage, changing the standard, or answering a request for the basis of a rule.

## Hard Gates

- MUST NOT skip a gate or mark it `PASS` without its required artifact.
- MUST NOT invent target definitions, labels, business thresholds, costs, approvals, ground truth, the reason a feature was chosen, or the research deliverable (feasibility, model selection or analysis report). Separate inference from a feature's definition from a recorded selection decision (section 8.5). Return `OWNER_DECISION_REQUIRED` with the missing field.
- MUST NOT inspect locked-test labels or metrics before G5.
- MUST NOT report Precision, Recall, accuracy, or real detection quality without ground-truth labels.
- MUST NOT force MLflow where project rules prohibit it. Select an allowed experiment tracker at G2 and preserve the run contract in section 10.
- MUST NOT introduce a complex candidate merely to complete the workflow. The strongest baseline may be the selected run.
- MUST NOT leave reasoning only in the conversation. Every reason, rejected alternative, expectation and interpretation the agent states about a step MUST also be written into the notebook or `research-log.md`, in the topic language.
- MUST NOT claim completion from prose review alone; run the validator and the gate-specific checks required by the standard.

## Terminal States

Every invocation ends with exactly one research state:

- `PASS` — current gate meets every applicable rule.
- `FAIL` — evidence shows one or more rules are violated; list rule IDs and artifacts.
- `STOPPED` — the approved stop criterion was reached and logged.
- `OWNER_DECISION_REQUIRED` — progress depends on a named business or technical owner decision that the agent must not invent.

Do not use `PASS` to mean that the full research is complete. Report both the gate and state, for example `G1: PASS; next gate: G2`. At G4 also report the outcome from standard section 10.3, for example `G4: PASS (outcome: NO_CHANGE)`; a G4 `PASS` never means a better model was found.

## Mechanical Checks and Judgment

The validator checks file shape, required headings, Problem Card keys, gate table values, `__REQUIRED_BEFORE_Gn__` placeholders of passed gates, notebook JSON, notebook headers and status, the question-driven notebook layout (every question has a `3.k` block with **What to look for** before its code and **Answer** after it, plus a findings row with an allowed verdict), one table or figure per code cell and only inside question blocks, no rule or gate codes in reader-facing prose, prose layout (no line breaks inside paragraphs or bullets), and that `data/<environment>/<domain>/` is Git-ignored. It does not prove scientific validity or that the narrative is good. The agent MUST still review data leakage, split choice, metrics, uncertainty, evidence quality, and claims against the corresponding standard rules.
