# Research Plan — {{RESEARCH_SLUG}}

File này là trạng thái hiện hành của research topic. Lịch sử thay đổi và lý do nằm trong `research-log.md`.

Mục lục:

1. [Research status and target gate](#1-research-status-and-target-gate)
2. [Problem Card](#2-problem-card)
3. [Data Contracts](#3-data-contracts)
4. [Dataset snapshots and manifests](#4-dataset-snapshots-and-manifests)
5. [Data Readiness Thresholds](#5-data-readiness-thresholds)
6. [Evaluation Protocol hoặc Analysis Protocol](#6-evaluation-protocol-hoặc-analysis-protocol)
7. [Gate Status](#7-gate-status)
8. [Open Decisions](#8-open-decisions)
9. [Approved Exceptions](#9-approved-exceptions)

## 1. Research status and target gate

```yaml
research_slug: {{RESEARCH_SLUG}}
language: vi
status: NOT_STARTED
current_gate: G0
target_gate: G0
created_at_utc: {{CREATED_AT_UTC}}
```

## 2. Problem Card

```yaml
problem_id: __REQUIRED__
title: __REQUIRED__
task_type: __REQUIRED__
research_deliverable: __REQUIRED__
business_owner: __REQUIRED__
technical_owner: __REQUIRED__
decision_user: __REQUIRED__
decision_or_action: __REQUIRED__
prediction_or_analysis_unit: __REQUIRED__
scoring_time: __REQUIRED__
feature_cutoff_time: __REQUIRED__
target_definition: __REQUIRED__
label_available_time: __REQUIRED__
prediction_horizon: __REQUIRED__
false_positive_cost: __REQUIRED__
false_negative_cost: __REQUIRED__
current_process_or_baseline: __REQUIRED__
primary_business_metric: __REQUIRED__
primary_model_metric: __REQUIRED__
guardrail_metrics: __REQUIRED__
operational_constraints: __REQUIRED__
supported_population: __REQUIRED__
excluded_population: __REQUIRED__
success_criteria: __REQUIRED__
stop_criteria: __REQUIRED__
approval: __REQUIRED__
```

## 3. Data Contracts

`__REQUIRED_BEFORE_G1__`

## 4. Dataset snapshots and manifests

```yaml
environment: {{ENVIRONMENT}}
domain: {{DOMAIN}}
manifest_paths: []
```

## 5. Data Readiness Thresholds

`__REQUIRED_BEFORE_G1__`

## 6. Evaluation Protocol hoặc Analysis Protocol

`__REQUIRED_BEFORE_G2__`

## 7. Gate Status

| Gate | Status | Evidence/Artifact | Reviewer | Reviewed at UTC |
|---|---|---|---|---|
| G0 | NOT_STARTED | — | — | — |
| G1 | NOT_STARTED | — | — | — |
| G2 | NOT_STARTED | — | — | — |
| G3 | NOT_STARTED | — | — | — |
| G4 | NOT_STARTED | — | — | — |
| G5 | NOT_STARTED | — | — | — |
| G6 | NOT_STARTED | — | — | — |

## 8. Open Decisions

- Hoàn thiện Problem Card và lấy approval của owner.

## 9. Approved Exceptions

Không có.

