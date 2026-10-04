# Data Science and Machine Learning Research Standard (SSOT)

**Version:** 2.9

**Status:** Normative

**Scope:** descriptive research, classification, regression, forecasting and time-series anomaly detection

**Goal:** two people or two AIs reading this document must produce the same artifact structure, pass through the same stage gates and apply the same selection protocol

## 1. Conventions and usage

This document is the **single source of truth**. Do not create another style guide in the same repository.

Only three keywords are used:

- **MUST:** mandatory. Missing evidence of completion fails the stage gate.
- **MUST NOT:** prohibited.
- **CONDITIONAL:** mandatory when the trigger stated in the decision table occurs.

Do not use "SHOULD", "MAY", "appropriate", "when needed" or "when feasible" as rules. Every exception MUST have a Decision Record in `research-log.md` containing: the rule ID, the reason, the approver, the expiry date and the accepted risk.

Every rule has an `Sxx` code. Every external basis has an `Exx` code. Syntax:

```text
[S<rule-id> | E<evidence-id>,...]
```

File names, folder names and artifact schemas are **project conventions**. They are not scientific results from external sources; they are how the repository enforces the traceability and reproducibility requirements of the sources cited next to them.

## 2. Evidence policy

The evidence registry and traceability matrix are maintained in [`evidence.md`](evidence.md). The agent MUST NOT read that file in the normal execution flow. It MUST read it when auditing sources, changing or adding to the standard, or when the user asks for the evidence behind a rule.

## 3. Required repository structure

[S01 | E02,E12,E13,E19]

Every research topic MUST have the following logical structure. Additional files are allowed; the names and locations of required artifacts MUST NOT change.

```text
notebooks/<research-slug>/
├── research-plan.md
├── research-log.md
├── 00_data_inventory.ipynb
├── 01_data_quality.ipynb
├── 02_eda.ipynb
├── 03_build_dataset.ipynb
├── 04_baselines.ipynb
├── 05_candidates.ipynb
└── 06_evaluation.ipynb

data/<environment>/<domain>/
├── bronze/
├── silver/
├── gold/
└── manifests/
```

Rules:

1. `research-plan.md` holds the current state: Problem Card, Data Contract, Evaluation Protocol and open decisions.
2. `research-log.md` is append-only; every experiment or decision is one dated entry.
3. Notebooks only orchestrate, inspect and narrate. Logic used by two or more notebooks MUST move into a Python module of the repository.
4. Raw data, model binaries and large outputs MUST NOT be committed to Git.
5. Every notebook MUST write its artifacts to `data/...`, the experiment tracker, or the artifact store declared in the Evaluation Protocol; notebook output is not the canonical artifact.
6. The topic's `target_gate` (section 1 of `research-plan.md`) is the last gate the research is planned to reach. Only the notebooks whose gate is at or before `target_gate` are required; they MUST all be created at initialization. Raising `target_gate` later MUST add the missing notebooks with `scripts/raise_target_gate.py` and be recorded in `research-log.md`. A notebook whose stage has not run MUST contain only the standard header, status `NOT_STARTED` and the section skeleton of section 13.2 with the placeholder `__NARRATIVE_REQUIRED__`; the output requirements of a notebook apply once its stage moves to `IN_PROGRESS`. A notebook header whose `**Status:**` is not `NOT_STARTED` MUST NOT still contain `__REQUIRED__`. When the notebook's gate (per the Stage/Gate column of the table below) is `PASS`, its `**Status:**` MUST be `PASS`, `FAIL` or `STOPPED`.
7. The topic's prose language (`en` or `vi`) MUST be chosen at initialization and recorded as `language:` in section 1 of `research-plan.md`. Every prose artifact of the topic uses that language; technical terms and identifiers stay in English per [`writing.md`](writing.md).
8. On a work machine, marked by `~/work-docs/` existing, company policy forbids pushing Markdown to the work Git host. `research-plan.md` and `research-log.md` then live in `~/work-docs/<repo-name>/notebooks/<research-slug>/` instead of next to the notebooks. This is the only approved change to the layout above; the scripts resolve it.

The purpose of each notebook is fixed:

| Notebook | Stage/Gate | Single question | Required output |
|---|---|---|---|
| `00_data_inventory.ipynb` | G1 | Which sources, fields, entities, time ranges and volumes exist? | inventory table and draft Data Contract |
| `01_data_quality.ipynb` | G1 | Does the data meet the approved readiness thresholds? | data-quality report, manifest of the checked snapshot and the G1 decision |
| `02_eda.ipynb` | G2 | How are the population, target and candidate signals distributed on train? | feature contract per section 8.5, then an EDA report on train only, using the split definition recorded in the Evaluation Protocol; never read validation or locked test |
| `03_build_dataset.ipynb` | G2 | How are reproducible Silver/Gold snapshots built? | dataset, manifest, a split assignment that implements the split definition, and assertions |
| `04_baselines.ipynb` | G3 | What do the required baselines achieve under the Evaluation Protocol? | baseline runs, comparison table and `strongest_baseline_id` |
| `05_candidates.ipynb` | G4 | Which hypothesis beats the strongest baseline on validation? | candidate runs, ablation and the selected candidate |
| `06_evaluation.ipynb` | G5 | Does the selected run PASS the locked test and stress tests? | locked-test report and the G5 decision |

Order within G2: (1) record the split definition (timestamps, entities and filters of train, validation and locked test) in the Evaluation Protocol per S09; (2) `02_eda.ipynb` filters train using that definition; (3) `03_build_dataset.ipynb` implements the split assignment and manifest; (4) freeze the rest of the Evaluation Protocol. EDA MUST NOT be used to choose or move the locked-test boundary.

`research-plan.md` MUST use exactly this section order:

```text
1. Research status and target gate
2. Problem Card
3. Data Contracts
4. Dataset snapshots and manifests
5. Data Readiness Thresholds
6. Evaluation Protocol or Analysis Protocol
7. Gate Status
8. Open Decisions
9. Approved Exceptions
```

`Gate Status` MUST be a table with the columns `Gate`, `Status`, `Evidence/Artifact`, `Reviewer`, `Reviewed at UTC`. `Status` values may only be `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL` or `STOPPED`.

## 4. Choosing the research type

[S02 | E01,E03,E05,E08,E14]

The first stage MUST choose exactly one `task_type` from the table. If the problem is not in the table, the research stops at Gate 0 until the SSOT is extended with a protocol and evidence.

| `task_type` | Output question |
|---|---|
| `descriptive` | How did the data behave? |
| `classification` | Which class does an entity or event belong to? |
| `regression` | What is the continuous value of an entity or event? |
| `forecasting` | What is the value of a time series over a future horizon? |
| `anomaly_detection` | Which entity or time range deviates from normal behaviour? |

Choose `task_type` by the first matching rule below:

1. The output only describes a population or past data, and produces no prediction or score per unit → `descriptive`.
2. The target is defined as a category, class or event label → `classification`, including when the label is predicted for a future time.
3. The target is a continuous numeric value at a future horizon of a time-ordered series → `forecasting`.
4. The target is a continuous numeric value but not as in rule 3 → `regression`.
5. There is no target label and the output is a deviation from normal behaviour → `anomaly_detection`.

If several rules match because the problem statement is unclear, G0 MUST FAIL; the owner MUST settle the output and the target before continuing.

Clustering, ranking/recommendation, causal inference, reinforcement learning, computer-vision foundation models and LLM evaluation have no protocol in this version. They MUST NOT fall back on the classification protocol; the SSOT must be extended before starting.

## 5. Required stage gates

[S03 | E01,E02,E03,E10,E15]

No stage may be skipped. When the research stops before its target gate, the state MUST be `STOPPED` and the reason MUST be recorded in the research log.

| Gate | Input | Required artifact | PASS condition |
|---|---|---|---|
| G0 Problem | business request | Problem Card in `research-plan.md` | every field has a value; the owner approved target, action and metric |
| G1 Data | G0 PASS | Data Contract, manifest, data-quality report | every required field of S05–S07 has a value; checksums match files; every readiness threshold is met or an exception is approved |
| G2 Protocol | G1 PASS | Evaluation Protocol, feature contract | split, baselines, metrics, slices, uncertainty, acceptance criteria, feature contract and locked test are frozen |
| G3 Baseline | G2 PASS | baseline runs and report | every required baseline ran on the same snapshot and split; failure analysis exists |
| G4 Candidate | G3 PASS | approach-space record, candidate runs and comparison or a no-change decision | every registered hypothesis has a result; the selected run is compared with the strongest baseline; the outcome is stated per section 10.3; the locked test was not used for tuning |
| G5 Locked test | G4 PASS; selected run chosen | locked-test report | run exactly once; meets every primary, guardrail and operational criterion |
| G6 Handoff | G5 PASS | model card, run/model URI, monitoring and rollback plan | the technical reviewer and the business owner signed off |

`Discovery-only` research MUST complete G0–G2; at G2, the Evaluation Protocol is replaced by an Analysis Protocol stating population, sampling, estimand/statistic, uncertainty and the limits of claims.

## 6. G0 — Problem Card

[S04 | E01,E03]

`research-plan.md` MUST contain exactly these fields:

```yaml
problem_id:
title:
task_type:
research_deliverable:
business_owner:
technical_owner:
decision_user:
decision_or_action:
prediction_or_analysis_unit:
scoring_time:
feature_cutoff_time:
target_definition:
label_available_time:
prediction_horizon:
false_positive_cost:
false_negative_cost:
current_process_or_baseline:
primary_business_metric:
primary_model_metric:
guardrail_metrics:
operational_constraints:
supported_population:
excluded_population:
success_criteria:
stop_criteria:
approval:
```

PASS rules:

1. Every field MUST have a value; `TBD` is not allowed.
2. A field that has no meaning for the chosen `task_type` MUST be written `not_applicable (<reason>)`, and only for the fields this table allows. Any other field written that way fails G0.

   | `task_type` | Fields that may be `not_applicable` |
   |---|---|
   | `descriptive` | `scoring_time`, `feature_cutoff_time`, `target_definition`, `label_available_time`, `prediction_horizon`, `false_positive_cost`, `false_negative_cost`, `primary_model_metric` |
   | `classification`, `regression` | `prediction_horizon`, when the target is not predicted for a future time |
   | `anomaly_detection` | `label_available_time`, when there are no labels |
   | `forecasting` | none |

3. `success_criteria` MUST be an inequality with a number, or the state `discovery_only`.
4. `target_definition` MUST describe the unit, the positive or value condition, and the timestamp.
5. `feature_cutoff_time` MUST be less than or equal to `scoring_time`.
6. `label_available_time` MUST be used to detect features that would not exist at scoring time.
7. The owner MUST record a name and approval date in `approval`.
8. `research_deliverable` MUST start with exactly one of three values, followed by one sentence naming the concrete output:
   - `feasibility_poc`: a conclusion on whether the research is feasible; no model is chosen for deployment.
   - `model_selection`: choose one model and configuration, or decide to keep the existing reference, to register in the system that consumes the model.
   - `analysis_report`: a descriptive or analytical report; no model is built for deployment.
9. The agent MUST NOT choose `research_deliverable`. It is the owner's decision; if it is missing, return `OWNER_DECISION_REQUIRED`.
10. When `research_deliverable` is `model_selection`: `operational_constraints` MUST name the consuming system with the artifact format and features it requires; `success_criteria` MUST quote that system's acceptance criteria, or record `OWNER_DECISION_REQUIRED` for the part that is missing. Research-only criteria without the consuming system's criteria are not enough to conclude that a model is usable.
11. When the owner changes `research_deliverable` after G0 PASS, G0 MUST reopen and every later gate MUST be re-evaluated for whether its existing artifacts still hold.

## 7. G1 — Data Contract, manifest and readiness

### 7.1. Data Contract

[S05 | E04,E10,E16]

Every source MUST have:

```yaml
source_name:
owner:
source_of_truth:
access_method:
processing_environment:
schema:
field_semantics:
units:
entity_key:
event_key:
event_time:
processing_time:
timezone:
expected_cadence:
null_semantics:
zero_semantics:
duplicate_definition:
retention:
expected_arrival_lag:
late_data_policy:
sensitive_fields:
access_policy:
label_source:
known_limitations:
```

`processing_environment` is where the data may be processed and stored under the data owner's or the company's policy: for example local machine allowed, or company platform only (a hosted notebook service or data warehouse), with whether extracts may leave it.

### 7.2. Dataset manifest

[S06 | E02,E04,E13]

Every Bronze/Silver/Gold snapshot MUST have a manifest:

```yaml
dataset_name:
snapshot_id:
layer: bronze|silver|gold
source_snapshot_ids:
created_at_utc:
created_by_code_commit:
extraction_query_or_job:
event_time_start:
event_time_end:
schema_version:
row_count:
entity_count:
label_count_by_class:
files:
checksums:
known_gaps:
filters:
transformations:
label_definition_version:
owner:
```

Bronze MUST be immutable. A Silver/Gold snapshot referenced by an experiment run MUST NOT be overwritten; create a new `snapshot_id`.

### 7.3. Data-quality report

[S07 | E04,E10]

`01_data_quality.ipynb` MUST output one table for the whole dataset and for each slice declared at G0:

| Check | Required output |
|---|---|
| Coverage | min/max time, duration, row count, entity count per period |
| Completeness | null/missing rate per field, entity and period |
| Uniqueness | duplicate count per `duplicate_definition` |
| Validity | count/rate outside range or enum |
| Cadence | median, p05, p95 of inter-arrival time |
| Freshness | `processing_time - event_time` p50/p95/p99/max |
| Population stability | entities added/removed per period |
| Label quality | class count, prevalence, ambiguous/unlabeled rate |
| Leakage inventory | availability time of every candidate feature |

Readiness thresholds MUST be declared in the Problem Card before any candidate model is looked at. There is no universal threshold. PASS means every metric meets its approved threshold; otherwise G1 FAILs or has an exception per section 1.

### 7.4. Large data, formats and security

[S08 | E02,E04,E16,E19]

1. If the estimated in-memory size exceeds 50% of available RAM, the data MUST be scanned by column, filter or batch and aggregated before pandas. The 50% mark is a project safety convention that leaves memory for the runtime.
2. A type-preserving format such as Parquet MUST be kept when the source is already Parquet; data MUST NOT be converted to CSV just for EDA.
3. Row counts MUST be recorded before and after every transformation.
4. Tokens, passwords, PII and URLs containing credentials MUST NOT appear in Git, notebook output, logs or screenshots.
5. Data MUST be processed and stored only where its `processing_environment` allows. If the data may not leave a company platform, the notebooks run on that platform and the `data/` layers there; nothing is extracted to a local machine.
6. Local data MUST live in a path protected by `.gitignore`. `data/<environment>/<domain>/` MUST be Git-ignored before any data is written.

## 8. G2 — Evaluation Protocol

### 8.1. Choosing the split with a decision table

[S09 | E05,E06]

Apply from the top; the first matching row is the required protocol.

| Production trigger | Required split |
|---|---|
| Predicting or evaluating the future by event time | chronological train → validation → locked test; forecasting uses rolling-origin evaluation |
| Production meets entities never seen before | group holdout by entity; entities MUST NOT overlap between splits |
| Both predicting the future and generalising to new entities | two separate tests: a temporal test on known entities and a temporal-group test on new entities |
| i.i.d. classification data, no group or time dependency | stratified random split |
| i.i.d. regression data, no group or time dependency | random split |
| `descriptive` | no train/test split; lock the population, sampling frame and analysis period |

Rules:

1. The test set MUST be defined by concrete timestamps, entities or filters in the manifest.
2. After G2, test labels MUST NOT be used for feature, threshold, model or hyperparameter selection.
3. The locked test runs only after a candidate is chosen. If test results are used to change the system, the test loses its locked status; the research MUST create a new test period or snapshot and record the invalidation.
4. Scalers, imputers, encoders, feature selectors, resampling parameters and learned thresholds MUST be fitted on train only, then applied to validation and test.

### 8.2. Baseline protocol by task

[S10 | E07,E08,E09]

Every baseline marked `MUST` has to run. `N/A` is valid only with a Decision Record.

| Task | Baseline 0 | Baseline 1 | Baseline 2 |
|---|---|---|---|
| Classification | majority class and class-prior probability — MUST | current rule — MUST if production has a rule | Logistic Regression — MUST |
| Regression | train mean and train median — MUST | current formula or rule — MUST if one exists | Linear or Ridge Regression — MUST |
| Forecasting | last-value naive — MUST | seasonal naive — MUST if train contains at least 2 defined cycles | ETS or ARIMA — MUST |
| Anomaly detection | all-normal and fixed alert-rate — MUST | current rule or threshold — MUST | rolling median + MAD — MUST |
| Descriptive | the current statistic or previous report — MUST if one exists | no model applies | no model applies |

Isolation Forest is a **candidate**, not a statistical baseline. A rule-based baseline is deterministic logic. A statistical baseline estimates a level, distribution or time pattern, such as median, MAD, EWMA, ETS or ARIMA; it is not the same as a probability.

### 8.3. Metric protocol by task

[S11 | E03,E08,E14,E17,E18]

| Task/trigger | Required primary report |
|---|---|
| Binary classification | confusion matrix at the operating threshold; precision, recall, F1; PR curve/AP; prevalence |
| Binary probability used as a risk score | everything above + Brier score + calibration curve |
| Multiclass | confusion matrix; per-class precision/recall/F1; macro average; support |
| Regression | MAE; RMSE; residual quantiles p50/p90/p95; error per slice |
| Forecasting | MAE or MASE; error per horizon; comparison with naive/seasonal naive |
| Time-series anomaly with labels | event precision/recall/F1; detection delay; false alerts per entity per day; event coverage |
| Time-series anomaly without labels | alert rate; score stability; coverage; runtime; injected-anomaly sensitivity; MUST state "real detection quality is not measured" |
| Descriptive | estimand/statistic, sample size, sampling frame and uncertainty interval |

The primary metric MUST be chosen in the Problem Card according to the cost of the decision:

- false positives are constrained → primary is precision at a recall floor, or false alerts per entity per day;
- false negatives are constrained → primary is recall at a precision floor;
- the probability is used directly → primary includes a proper scoring rule (Brier/log loss) and calibration;
- regression where large errors cost quadratically → RMSE; otherwise → MAE;
- anomalies that last over time → an event-level metric; MUST NOT use point-wise accuracy alone.

Accuracy MUST NOT be the primary metric for binary classification if the majority-class baseline accuracy already meets the success criterion or the positive class is a rare actionable class; use PR-based and operational metrics instead.

### 8.4. Slices, uncertainty and acceptance criteria

[S12 | E03,E11,E15]

The Evaluation Protocol MUST record:

```yaml
primary_metric:
primary_acceptance_threshold:
guardrail_metrics_and_thresholds:
operational_metrics_and_thresholds:
slices:
uncertainty_method:
confidence_level: 0.95
stochastic_repetitions:
locked_test_snapshot:
experiment_tracker:
tracking_location:
artifact_location:
```

Rules:

1. Slices MUST include every population listed at G0 and every group with different semantics or source.
2. Every metric MUST come with its sample size or support.
3. Stochastic models MUST run at least 5 seeds; report the mean, standard deviation and each seed. `5` is a project convention that enforces the error-bar requirement of E15.
4. Deterministic models run once; MUST record `stochastic_repetitions: 1` and why the model is deterministic.
5. Candidate-baseline comparisons MUST report a 95% interval of the delta over independent evaluation units. Time series MUST use block, entity or event resampling instead of row bootstrap when rows are autocorrelated.
6. A candidate may be declared "better" only if the interval of the delta excludes the no-improvement value and every guardrail meets its threshold.

### 8.5. Feature contract

This section extends S12: features are part of the Evaluation Protocol and MUST be frozen with it at G2. Deferred to handoff, nobody remembers why a feature was chosen.

Every feature MUST have one entry:

```yaml
feature:
definition:            # formula over a window, matching the code that builds the feature
unit:
definition_source:     # protocol section and implementing code; not a substitute for the reason it was chosen
targets_behaviour:     # the behaviour or failure the feature is meant to measure; or "data sufficiency" if it is only a quality control
behaviour_basis:       # recorded decision, or inference from definition; never treat inference as the history of the choice
used_by:               # model used for scoring, eligibility, or diagnostic only; state each role
decision_source:       # where the reason for choosing it is recorded, with owner and date if known; if missing, OWNER_DECISION_REQUIRED
```

Rules:

1. `definition` MUST match the code that builds the feature; a mismatch FAILs G2.
2. `decision_source` MUST point to where the reason for the choice is recorded. An approved definition does not prove the reason was recorded. If there is none, write `OWNER_DECISION_REQUIRED`; the agent MUST NOT supply a reason itself. The agent may explain the behaviour inferred from the formula, but MUST record `behaviour_basis` as inference and not treat it as evidence of detection effectiveness.
3. Every candidate feature ever considered (in an old plan, an old notebook or earlier research) but not in the protocol MUST be listed with the reason it was dropped, or `OWNER_DECISION_REQUIRED`. Distinguish dropped, renamed, redefined and metadata features; do not call an alias a dropped feature. Alternative window lengths are recorded separately.
4. A feature computed but used by no model for scoring MUST be stated in `used_by`, with its eligibility or diagnostic role if any and why it is kept. A model that uses only a subset MUST list a subset that matches the code and the source of the reason for that subset, or `OWNER_DECISION_REQUIRED`.
5. `02_eda.ipynb` MUST present the feature contract before describing feature distributions, and save it as an artifact.
6. When explanations are added to a frozen protocol, keep the old artifact and hash; use a versioned sidecar that references the protocol hash and records the unresolved decisions. Approval to update the documentation is not approval of a selection reason that was never provided. G2 is not re-affirmed as PASS while a required reason is missing.

## 9. G3 — Baseline implementation

[S13 | E01,E07,E08,E09]

`04_baselines.ipynb` MUST:

1. Load exactly the Gold snapshot and split manifest locked at G2.
2. Run every required baseline in S10.
3. Log each baseline as a separate experiment run in the tracker chosen at G2.
4. Use the same feature availability, metric implementation and evaluation unit as the candidates.
5. Output a comparison table with metrics, intervals, runtime, artifact size and failure examples.
6. Choose `strongest_baseline_id` by the primary metric among the baselines that PASS every guardrail threshold of S12.

If a rule-based or statistical baseline meets the success criteria, candidate experiments are still allowed and MUST use that baseline as the comparison standard. If no candidate hypothesis is registered, G4 MUST record a `no-change decision` and select the strongest baseline as the selected run. If no candidate beats the baseline per S12.6, the decision MUST be to keep the baseline, unless an approved Decision Record says otherwise.

## 10. G4 — Candidate experiments

[S14 | E02,E13,E15]

### 10.1. What a candidate is

A candidate is a registered hypothesis: a controlled change relative to the reference run. The change can be the model family, the feature set, how the score is computed, the threshold policy or the preprocessing.

A candidate is not necessarily an ML model. A rule or a statistical method that differs from the reference is also a candidate when it is registered as a hypothesis. An ML model is not required at G4; see section 10.3 for the valid outcomes when no candidate beats the reference.

### 10.2. Approach-space record

Before registering hypotheses, the researcher MUST record a Decision Record in `research-log.md` listing the approach families considered. Each family has exactly one status:

| Approach family | Status |
|---|---|
| Rule-based | `tried: <hypothesis_id>`, `not_tried: <reason>` or `OWNER_DECISION_REQUIRED` |
| Statistical | as above |
| Unsupervised ML | as above |
| Supervised ML | as above; `not_tried: no labels` is a valid reason when there are no labels |
| Other family suited to the task | as above |

Rules:

1. The agent MUST NOT supply a `not_tried` reason itself. The reason must be a verifiable fact (for example, no labels) or one the owner recorded; otherwise record `OWNER_DECISION_REQUIRED`.
2. Approach families supported by the system that consumes the model (per `operational_constraints` in the Problem Card) MUST be listed, even if not tried.
3. A family in state `OWNER_DECISION_REQUIRED` does not block G4 PASS, but MUST appear in the G4 report as an open item. When `research_deliverable` is `model_selection`, every family MUST have a status other than `OWNER_DECISION_REQUIRED` before G5 starts.

### 10.3. G4 outcome

The G4 report MUST state exactly one outcome next to the gate state:

| Outcome | Meaning |
|---|---|
| `IMPROVEMENT_FOUND` | A candidate beats the reference per S12.6 and meets every guardrail; the selected run is that candidate |
| `NO_CHANGE` | Every registered hypothesis has a result and no candidate beats the reference per S12.6; the selected run is the reference or the strongest baseline |
| `NO_CANDIDATE_REGISTERED` | No hypothesis was registered; a Decision Record states why, and the selected run is the strongest baseline |

`G4: PASS` only means every registered hypothesis has a result. It does not mean a better model was found. `NO_CHANGE` is a valid result, not a failure, but MUST be reported as "tried, and no candidate beat the baseline", never phrased as an improvement.

### 10.4. Registering a hypothesis

Every experiment MUST have a `hypothesis_id` and change only one group of factors:

```yaml
hypothesis_id:
question:
expected_mechanism:
change_from_reference_run:
fixed_components:
dataset_snapshot:
split_version:
primary_expected_effect:
falsification_condition:
```

Every experiment run used in a report MUST log:

```text
problem_id, hypothesis_id, research_stage
git_commit, branch
dataset_snapshot_id, manifest_hash
schema_version, feature_version, split_version
model_class, all hyperparameters, seed
package/environment reference
train/validation metrics
slice metrics and support
threshold
runtime and principal compute resource
model, preprocessing pipeline, plots, eval table
run status and conclusion
```

`experiment_tracker` MUST be a backend the project allows that can store every field and artifact above. If MLflow is used, the experiment name MUST be `<domain>-<task>-<environment>`. For every backend, the run ID MUST be stable and the run name MUST be `<stage>-<model>-<feature_version>-<yyyymmdd-hhmm>`.

The researcher MUST NOT look at locked-test metrics at G4.

## 11. G5 — Locked-test evaluation

[S15 | E03,E10,E11,E15]

`06_evaluation.ipynb` MUST run the selected run and the strongest baseline on the same locked test exactly once.

PASS only when all of these hold:

1. the primary metric meets `primary_acceptance_threshold`;
2. every guardrail meets its threshold;
3. every operational metric meets its threshold;
4. metrics and support are reported for every slice;
5. the uncertainty report contains `uncertainty_method`, `confidence_level`, the evaluation unit, the interval of every required metric and the candidate-baseline delta per S12;
6. the candidate-baseline claim follows S12.6;
7. failure analysis has at least false-positive and false-negative examples if labels exist;
8. limitations and the unsupported population are recorded.

Without ground truth, the G5 conclusion MUST be limited to technical readiness or score stability. It MUST NOT use the words precision, recall, real accuracy or "good model" for an unlabeled test.

## 12. Robustness and stress-test matrix

[S16 | E03,E10,E16]

Apply every row whose trigger holds; there is no optional list.

| Trigger | Required test |
|---|---|
| Event time or streaming | missing window, delayed/late data, out-of-order event, duplicate event |
| Categorical ID or category | unseen category and missing category |
| External dependency | timeout, error response, stale response and fallback |
| Real-time SLA | p50/p95/p99 latency, throughput and load at the declared capacity |
| Class imbalance | prevalence shift and threshold sensitivity |
| Entity, site or profile slices | metric and coverage per slice |
| Rolling or lag features | boundary test proving no future data is read |
| Retraining | schema drift, feature drift, label delay and empty training window |
| Stochastic model | seed variability per S12 |

Stress results MUST be logged as artifacts and linked from the locked-test report.

## 13. Notebook specification

[S17 | E02,E12,E19]

### 13.1. Standard header

The first cell of every notebook MUST contain exactly these items, each its own paragraph (separated by blank lines). Labels follow the topic language; the block below is the `en` version, and the `vi` version is in `assets/vi/notebook-header.md`.

```markdown
# <Number> — <Notebook name>

**Problem ID:**

**Stage/Gate:**

**Single question:**

**Out of scope:**

**Input snapshot/manifest:**

**Output artifact:**

**Config:**

**Git commit:**

**How to run:**

**Run date UTC:**

**Status:** NOT_STARTED|IN_PROGRESS|PASS|FAIL|STOPPED
```

### 13.2. Section order

A notebook is organised by questions, not by execution steps. Section names follow the topic language (`en` / `vi`):

```text
1. Questions / Câu hỏi
2. Setup
3. Analysis / Phân tích
   3.1. <question 1>
   3.2. <question 2>
   ...
4. Output checks and artifacts / Output assertions và artifacts
5. Findings / Kết luận
```

1. **Questions** lists the questions numbered `1.`..`n.`, each with why it matters for the gate decision. The single question in the header is broken down into these questions.
2. **Setup** contains configuration, imports, environment capture, input loading and input assertions. Setup MUST NOT display a table or figure.
3. **Analysis** has exactly one `### 3.k.` block for each question k, in the same order. Every table and figure MUST be inside a block.
4. **Output checks and artifacts** checks the outputs and saves the artifacts.
5. **Findings** has a findings table with exactly one row per question, followed by not proven, limitations and next decision.

### 13.3. Execution rules

1. The notebook MUST run successfully with `Restart Kernel and Run All`, or the equivalent headless execution described in the skill.
2. Seeds, paths and parameters MUST be at the top of Setup; later cells MUST NOT reassign them.
3. Input loading MUST use a snapshot/manifest, never "the latest file".
4. Input assertions MUST check the schema, time range, row count against the thresholds in S07, and the duplicate rule.
5. The notebook MUST NOT contain credentials or modify Bronze data.
6. Failing cells, dead code and debug output MUST be removed before review.
7. Shared or production logic MUST live in a tested module; the notebook only calls the module. The module MUST expose one function per analysis question, so each block 3.k calls exactly its own computation; the whole analysis MUST NOT be bundled into one call.
8. Every table or figure used in a claim MUST be saved under a stable name and logged to the run or artifact store.

### 13.4. Figure and table rules

Every figure MUST have a title, axis names, units, timezone/time range, sample size/support, a legend and a filter/aggregation note. Colour MUST NOT be the only channel distinguishing series or classes.

Every metric table MUST have the dataset/split, metric definition/version, threshold if any, support and uncertainty.

### 13.5. Narrative

A notebook MUST be understandable without the conversation that produced it. The reader is a colleague who knows the domain but not this standard: they must know which question the notebook answers, how each question is answered and how the answer changes the decision. Reasoning that exists only in the conversation is treated as not existing.

When `**Status:**` is not `NOT_STARTED`:

1. Every `### 3.k.` block MUST have three parts in order: **What to look for** before the first code cell, the code cell, and **Answer** after the last code cell.
2. **What to look for** MUST name the table or figure about to appear, the column or region to look at, and which result means fine and which means a problem. It is a criterion; it MUST be written before the code runs. When a notebook is rewritten after its results are known from an earlier run, the criterion MUST come from the protocol, thresholds or approved Data Contract, and `research-log.md` MUST record that the criterion was not pre-registered.
3. **Answer** MUST answer the question in its first sentence (with numbers), say whether the criterion in **What to look for** was met, and state the consequence for the next step.
4. Each code cell displays at most one table or figure and MUST be followed by markdown.
5. Rule IDs, evidence IDs and gate codes (`S05`, `E12`, `G1`) MUST NOT appear in a question, **What to look for** or **Answer**. They go in a **Trace** line at the end of the block.
6. Every issue mentioned in prose MUST either be a question with its own block or be recorded under **Not proven**. No issue is raised and then left hanging.
7. The findings table MUST have one row per question with a verdict of `Met` / `Not met` / `Partly met` / `Undetermined` (`vi`: `Đạt` / `Không đạt` / `Đạt một phần` / `Chưa xác định`). **Not proven** MUST NOT be empty.
8. The notebook describes the data and the results, not the history of its own creation (reruns, replays, rewritten narrative). That history belongs in `research-log.md`.
9. Every `__NARRATIVE_REQUIRED__` placeholder MUST be replaced with content.

Labels per topic language, minimum word counts and examples are in [`writing.md`](writing.md) section 3. The validator checks the structure; whether an answer actually answers its question is checked in review.

### 13.6. Prose layout

Markdown cells, `research-plan.md`, `research-log.md` and gate reports MUST follow [`writing.md`](writing.md) section 2: no line breaks inside a sentence, one idea per paragraph, `**Label:**` lines separated by blank lines, one idea per bullet.

## 14. Research plan and research log

[S18 | E02,E15]

`research-plan.md` is the current state and may be updated. `research-log.md` is append-only and MUST NOT delete negative results.

Every log entry MUST use the template below (the `en` version; the `vi` version is in `assets/vi/research-log.md`). Each label is its own paragraph, separated by blank lines.

```markdown
## YYYY-MM-DD — <Experiment/Decision ID> — <Name>

**Stage/Gate:**

**Question:**

**Hypothesis:**

**Data/snapshot:**

**Method/config:**

**Run/artifact:**

**Quantitative result:**

**Uncertainty/support:**

**Limitations:**

**Conclusion:**

**Decision:**

**Next step:**
```

A claim MUST state the population, period/split, baseline, metric delta, uncertainty and limitation. A compliant example:

```text
On the locked test of 01–07/09, covering 412 events from 2130 devices, the candidate reduces false alerts per device per day from 0.42 to 0.31 compared with the baseline (delta -0.11; 95% CI [-0.14; -0.08]) while event recall drops from 0.78 to 0.77.

Not yet evaluated on other sites.
```

## 15. G6 — Handoff

[S19 | E03,E10,E11,E13,E16]

Before production there MUST be:

```text
model card
dataset/manifest card
feature contract (from G2, section 8.5, updated if changed)
locked-test report
experiment/run/model URI or catalog identifier
inference interface and example
training-serving parity test
monitoring metric and threshold
data/model drift response
fallback and rollback procedure
owner and review date
```

The Model Card MUST record intended use, unsupported use, supported/excluded population, train/eval snapshots, metrics per slice, operational constraints, failure modes, ethical/privacy concerns and the expiry/review condition.

## 16. Definition of Done

[S20 | E02,E03,E10,E11,E15]

Research has the state `COMPLETE` only when:

1. The target gate has PASSed and the artifacts of every earlier gate exist.
2. Every claim traces to a snapshot, code commit, run and artifact.
3. Baseline and candidates use the same Evaluation Protocol.
4. The locked test was not used for tuning.
5. Metrics meet S11; uncertainty and support meet S12; every slice in the Evaluation Protocol has results; failure analysis meets S15.7.
6. Notebooks rerun from a clean kernel.
7. The conclusion states what was proven, what was not proven and the supported population.
8. If the goal is production, G6 has PASSed.

A complex model is not a completion condition. Valid concluding states include "rule/statistical baseline meets the success criteria", "data does not meet the readiness thresholds", "no predictive signal found under the Evaluation Protocol" or "candidate passes the gate".

## 17. Anti-patterns — automatic gate FAIL

[S21 | E01,E02,E06,E10,E15,E16]

- Missing Problem Card or a field still `TBD`.
- A field marked `not_applicable` that section 6 does not allow for the task type.
- Choosing an algorithm before G0 PASS.
- No manifest or snapshot ID.
- Modifying Bronze or overwriting a snapshot that was already used.
- Fitting preprocessing or thresholds on validation+test or on all data.
- Random split when there is a time or group dependency.
- Using the test set to choose features, model or threshold and still calling it a locked test.
- Candidate and baseline using different dataset, split or metric code.
- Dropping a required baseline without a Decision Record.
- Using accuracy alone for a rare positive class.
- Reporting only a point-wise metric for range anomalies.
- Calling weak, proxy or synthetic labels ground truth.
- Reporting precision or recall without labels.
- Not reporting support, slices or uncertainty per the protocol.
- Choosing a champion by sorting one metric while ignoring the guardrail and operational gates.
- Production logic that exists only in a notebook.
- A notebook that has run but lacks the narrative of section 13.5, or reasoning that exists only in the conversation.
- Deleting failed runs or negative results.
- Credentials or sensitive data in Git, notebooks or logs.
- Processing data outside its `processing_environment`.

## 18. Evidence traceability

The canonical registry and the `Sxx → Exx` matrix are in [`evidence.md`](evidence.md). Every change to a rule ID or evidence ID MUST update that file in the same change.
