"""Language-specific labels shared by init_research.py and validate_research.py.

Keys, gate IDs, statuses, Problem Card fields and technical terms stay in English
in every language; only the prose labels below change.
"""

from __future__ import annotations

LANGUAGES = ("en", "vi")
LEGACY_LANGUAGE = "vi"
NARRATIVE_PLACEHOLDER = "__NARRATIVE_REQUIRED__"


TEXT: dict[str, dict[str, object]] = {
    "en": {
        "plan_headings": (
            "## 1. Research status and target gate",
            "## 2. Problem Card",
            "## 3. Data Contracts",
            "## 4. Dataset snapshots and manifests",
            "## 5. Data Readiness Thresholds",
            "## 6. Evaluation Protocol or Analysis Protocol",
            "## 7. Gate Status",
            "## 8. Open Decisions",
            "## 9. Approved Exceptions",
        ),
        "notebook_labels": (
            "**Problem ID:**",
            "**Stage/Gate:**",
            "**Single question:**",
            "**Out of scope:**",
            "**Input snapshot/manifest:**",
            "**Output artifact:**",
            "**Config:**",
            "**Git commit:**",
            "**How to run:**",
            "**Run date UTC:**",
        ),
        "section_titles": (
            "Questions",
            "Setup",
            "Analysis",
            "Output checks and artifacts",
            "Findings",
        ),
        "look_for": "**What to look for:**",
        "answer": "**Answer:**",
        "trace": "**Trace:**",
        "not_proven": "**Not proven:**",
        "limitations": "**Limitations:**",
        "next_decision": "**Next decision:**",
        "findings_header": "| # | Question | Answer | Verdict | Consequence |",
        "verdicts": ("Met", "Not met", "Partly met", "Undetermined"),
        "notebooks": {
            "00_data_inventory.ipynb": (
                "Which sources, fields, entities, time range and volume exist?",
                "inventory table and draft Data Contract",
            ),
            "01_data_quality.ipynb": (
                "Does the data meet the approved readiness thresholds?",
                "data-quality report, manifest of the checked snapshot and G1 decision",
            ),
            "02_eda.ipynb": (
                "How are population, target and candidate signals distributed on train?",
                "feature contract (standard section 8.5), then EDA report on train only, using the split definition in the Evaluation Protocol; no validation/locked-test reads",
            ),
            "03_build_dataset.ipynb": (
                "How is a reproducible Silver/Gold snapshot built?",
                "dataset, manifest, split assignment that implements the split definition, and assertions",
            ),
            "04_baselines.ipynb": (
                "What do the required baselines achieve under the Evaluation Protocol?",
                "baseline runs, comparison table and strongest_baseline_id",
            ),
            "05_candidates.ipynb": (
                "Which hypothesis beats the strongest baseline on validation?",
                "candidate runs, ablation and selected run",
            ),
            "06_evaluation.ipynb": (
                "Does the selected run PASS the locked test and stress tests?",
                "locked-test report and G5 decision",
            ),
        },
    },
    "vi": {
        "plan_headings": (
            "## 1. Research status and target gate",
            "## 2. Problem Card",
            "## 3. Data Contracts",
            "## 4. Dataset snapshots and manifests",
            "## 5. Data Readiness Thresholds",
            "## 6. Evaluation Protocol hoặc Analysis Protocol",
            "## 7. Gate Status",
            "## 8. Open Decisions",
            "## 9. Approved Exceptions",
        ),
        "notebook_labels": (
            "**Problem ID:**",
            "**Stage/Gate:**",
            "**Câu hỏi duy nhất:**",
            "**Ngoài phạm vi:**",
            "**Input snapshot/manifest:**",
            "**Output artifact:**",
            "**Config:**",
            "**Git commit:**",
            "**Cách chạy:**",
            "**Ngày chạy UTC:**",
        ),
        "section_titles": (
            "Câu hỏi",
            "Setup",
            "Phân tích",
            "Output assertions và artifacts",
            "Kết luận",
        ),
        "look_for": "**Cần nhìn gì:**",
        "answer": "**Trả lời:**",
        "trace": "**Trace:**",
        "not_proven": "**Chưa chứng minh:**",
        "limitations": "**Giới hạn:**",
        "next_decision": "**Quyết định tiếp theo:**",
        "findings_header": "| # | Câu hỏi | Trả lời | Đánh giá | Hệ quả |",
        "verdicts": ("Đạt", "Không đạt", "Đạt một phần", "Chưa xác định"),
        "notebooks": {
            "00_data_inventory.ipynb": (
                "Có source, field, entity, time range và volume nào?",
                "inventory table và draft Data Contract",
            ),
            "01_data_quality.ipynb": (
                "Dữ liệu có đạt readiness threshold đã duyệt không?",
                "data-quality report, manifest của snapshot đã kiểm tra và quyết định G1",
            ),
            "02_eda.ipynb": (
                "Population, target và candidate signal phân bố như thế nào trên train?",
                "feature contract (standard mục 8.5), rồi EDA report chỉ trên train theo split definition trong Evaluation Protocol; không đọc validation/locked test",
            ),
            "03_build_dataset.ipynb": (
                "Làm thế nào tạo Silver/Gold snapshot tái lập được?",
                "dataset, manifest, split assignment theo split definition và assertions",
            ),
            "04_baselines.ipynb": (
                "Baseline bắt buộc đạt kết quả nào theo Evaluation Protocol?",
                "baseline runs, comparison table và strongest_baseline_id",
            ),
            "05_candidates.ipynb": (
                "Hypothesis nào vượt strongest baseline trên validation?",
                "candidate runs, ablation và selected run",
            ),
            "06_evaluation.ipynb": (
                "Selected run có PASS locked test và stress tests không?",
                "locked-test report và quyết định G5",
            ),
        },
    },
}

# Notebook layout (standard section 13.2): questions first, one analysis block per question.
QUESTIONS_SECTION = 1
ANALYSIS_SECTION = 3
FINDINGS_SECTION = 5
SECTION_COUNT = 5

QUESTION_MIN_WORDS = 10
LOOK_FOR_MIN_WORDS = 15
ANSWER_MIN_WORDS = 25
FINDINGS_PROSE_MIN_WORDS = 30

# Rule IDs, evidence IDs and gate codes belong in the **Trace:** line, not in reader-facing prose.
AUDIT_CODE = r"\b(?:S\d{2}|E\d{2}|G[0-6])\b"


def text(language: str, key: str) -> object:
    return TEXT[language][key]
