---
name: ds-ml-research
description: Use when initializing, executing, auditing, or reviewing data-science or machine-learning research, including datasets, EDA, baselines, experiments, evaluation protocols, model comparisons, anomaly detection, forecasting, or production handoff.
---

# DS/ML Research

## Overview

Run DS/ML research through a reproducible, evidence-backed gate system. The canonical standard is [`references/standard.md`](references/standard.md); this file routes the work and does not duplicate that standard.

**Core principle:** a claim is valid only when it traces to a versioned dataset snapshot, code revision, experiment run, evaluation protocol, and persisted artifact.

## Conventions

- `{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.
- `{project-root}` is the Git root of the service repository or submodule that owns the data and model (for example `~/projects/example-ml-service`). It is never the umbrella repository that only aggregates submodules; if the current directory is an umbrella root, ask which service repository to use.
- `{topic-dir}` is `{project-root}/notebooks/<research-slug>`.
- `{topic-md-dir}` is where the topic's Markdown files (`research-plan.md`, `research-log.md`) live. Normally it is `{topic-dir}`. On a work machine, marked by `~/work-docs/` existing, company policy forbids pushing Markdown to the work Git host, so it is `~/work-docs/<repo-name>/notebooks/<research-slug>` instead. The scripts resolve this themselves (`scripts/topic_paths.py`). This is the one approved exception to the fixed layout in standard section 3: notebooks, code and data stay where the standard puts them. Never write a `.md` file inside the repository on a work machine.
- Local `AGENTS.md`, `CLAUDE.md`, security rules, and service constraints take precedence for tool and storage choices. They do not waive the research gates, evidence contract, or leakage controls.

## On Activation

1. Resolve `{project-root}` and read applicable repository instructions.
2. Determine the mode: **initialize**, **execute**, **audit**, or **review**. Infer it from the request; ask only when the requested outcome cannot be inferred.
3. Read sections 1–5 of `references/standard.md`, the section mapped to the current gate below, and `references/writing.md` before writing any prose artifact.
4. For a new topic, interview the user once, in a single message, asking only what the request does not already say. Use a structured question tool if available. Always allow "I don't know"; an unknown that only the owner can settle becomes `OWNER_DECISION_REQUIRED`.
   - **Language**: is the research in English (`en`) or Vietnamese (`vi`)? Do not infer it from the language of the chat.
   - **Where the data may be processed**: may it be copied to this machine, or must it stay on a company platform (a hosted notebook service, a data warehouse), and may extracts leave that platform? This becomes `processing_environment` in the Data Contract. If the data must stay on a platform, the notebooks run there and nothing is copied locally. Never download data first and ask afterwards.
   - **Target gate**: the last gate the research is planned to reach. Propose one from the expected deliverable (an analysis report usually stops at G2, a feasibility check at G3 or G4, a model selection at G5, anything going to production at G6) and let the user confirm. It can be raised later with `scripts/raise_target_gate.py`. This is a planning choice, not `research_deliverable`, which stays the owner's decision.
   - **Familiarity**: how familiar is the user with this kind of analysis? It sets how much the briefing explains (see "Briefing the user").

   Then run:

   ```bash
   python -B {skill-root}/scripts/init_research.py \
     --project-root {project-root} \
     --slug <research-slug> \
     --environment <environment> \
     --domain <domain> \
     --language <en|vi> \
     --target-gate <G2|G3|G4|G5|G6>
   ```

   **From a task-decoder hand-off.** If the request includes a task-decoder hand-off with a Problem Card draft, copy every known value into the Problem Card after initialization. A value marked `UNKNOWN - ask <role>` stays `__REQUIRED__` and is listed as `OWNER_DECISION_REQUIRED` naming that role. A value marked as inferred (usually `task_type`) is written in, but G0 cannot `PASS` until the user or owner confirms it. Never treat the draft's "wording suggests" note on `research_deliverable` as the owner's choice.
5. For an existing topic, read `{topic-md-dir}/research-plan.md`, take the topic language from `language:` and the target from `target_gate:` in section 1, determine the first gate not marked `PASS`, and run the structural validator before changing research artifacts:

   ```bash
   python -B {skill-root}/scripts/validate_research.py {topic-dir}
   ```

6. Execute only the current gate, in the order of `references/writing.md` section 3.4: write the questions and each block's **What to look for** criterion, implement one module function per question, execute the notebook with placeholder answers (see "Running notebooks"), then write each **Answer** and the findings table from the executed outputs, checking every number against them. Persist the required artifact and append the experiment or decision to `research-log.md`. When rewriting a notebook whose results are already known, follow section 3.5.
7. Run the validator again. Report the terminal state and the exact failed rule or required owner decision, then brief the user (see "Briefing the user").

## Running notebooks

A notebook counts as executed only when it ran top to bottom in a fresh kernel. Never assemble outputs from interactive runs.

- Use the project's own environment: its virtualenv, uv, Poetry or conda environment, or the company platform when `processing_environment` requires it.
- Check that headless execution is available in that environment first: `jupyter nbconvert --version`.
- Execute in place:

  ```bash
  jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=-1 {topic-dir}/<notebook>.ipynb
  ```

  Add `--ExecutePreprocessor.kernel_name=<kernel>` if the project uses a named kernel. If the project already runs notebooks another way (papermill, a Make target, a platform job), use that instead.
- If Jupyter or the kernel is missing, do not install anything globally or add dependencies on your own. Tell the user what is missing and propose adding `nbconvert` and `ipykernel` to the project's development dependencies.
- On a company platform, run the notebook with the platform's own runner and bring back only the executed notebook, never the data.

## Briefing the user

The user is a fullstack engineer rather than a DS specialist, and has to defend this research to DS colleagues and the owner. After the terminal state, give this in the chat, in the language the user writes in:

```
## What this gate settled
[Two to four plain sentences: what was checked or built, and what it means for the decision.]

## Choices made, and why
[Each methodological choice made in this run (split, baseline, metric, threshold, exclusion, feature), one line each with its reason.]

## Questions you will likely get
[Three to five, hardest first, each with a two-line answer.]

## Needs a decision
[Each OWNER_DECISION_REQUIRED item: who decides, the options, and a short message the user can send. Omit if none.]

## Terms
[Concepts used in this gate, one plain line each, scaled to the user's familiarity. Omit if none.]
```

The briefing only restates what the notebook and `research-log.md` already record. If explaining a choice needs a reason that is not written down, write it into the notebook or log first (or mark it `OWNER_DECISION_REQUIRED`); never give the user reasoning that exists only in the chat. Keep the briefing to a two-minute read.

## Gate Routing

| Current work | Read from `references/standard.md` | Primary artifact |
|---|---|---|
| G0 Problem framing | sections 4–6, including the owner-chosen `research_deliverable` and which fields may be `not_applicable` for the task type | Problem Card |
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
- MUST NOT process or copy data outside its `processing_environment` (standard section 7.4).
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

The validator checks file shape, the notebooks required up to `target_gate`, required headings, Problem Card keys and `not_applicable` fields allowed for the task type, gate table values, `__REQUIRED_BEFORE_Gn__` placeholders of passed gates, notebook JSON, notebook headers and status, the question-driven notebook layout (every question has a `3.k` block with **What to look for** before its code and **Answer** after it, plus a findings row with an allowed verdict), one table or figure per code cell and only inside question blocks, no rule or gate codes in reader-facing prose, prose layout (no line breaks inside paragraphs or bullets), and that `data/<environment>/<domain>/` is Git-ignored. It does not prove scientific validity or that the narrative is good. The agent MUST still review data leakage, split choice, metrics, uncertainty, evidence quality, and claims against the corresponding standard rules.
