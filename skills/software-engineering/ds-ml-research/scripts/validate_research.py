#!/usr/bin/env python3
"""Validate the mechanical structure of a DS/ML research topic."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from research_lang import LANGUAGES, LEGACY_LANGUAGE, text
from topic_paths import markdown_dir_for_topic
from writing_checks import cell_text, narrative_issues, soft_break_lines


REQUIRED_FILES = (
    "research-plan.md",
    "research-log.md",
    "00_data_inventory.ipynb",
    "01_data_quality.ipynb",
    "02_eda.ipynb",
    "03_build_dataset.ipynb",
    "04_baselines.ipynb",
    "05_candidates.ipynb",
    "06_evaluation.ipynb",
)
NOTEBOOK_GATES = {
    "00_data_inventory.ipynb": 1,
    "01_data_quality.ipynb": 1,
    "02_eda.ipynb": 2,
    "03_build_dataset.ipynb": 2,
    "04_baselines.ipynb": 3,
    "05_candidates.ipynb": 4,
    "06_evaluation.ipynb": 5,
}
PROBLEM_FIELDS = (
    "problem_id",
    "title",
    "task_type",
    "business_owner",
    "technical_owner",
    "decision_user",
    "decision_or_action",
    "prediction_or_analysis_unit",
    "scoring_time",
    "feature_cutoff_time",
    "target_definition",
    "label_available_time",
    "prediction_horizon",
    "false_positive_cost",
    "false_negative_cost",
    "current_process_or_baseline",
    "primary_business_metric",
    "primary_model_metric",
    "guardrail_metrics",
    "operational_constraints",
    "supported_population",
    "excluded_population",
    "success_criteria",
    "stop_criteria",
    "approval",
)
DELIVERABLES = ("feasibility_poc", "model_selection", "analysis_report")
ALLOWED_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "STOPPED"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_language(plan: Path, report: Report) -> str:
    match = re.search(r"(?m)^language:\s*(\S+)\s*$", plan.read_text())
    if not match:
        report.warn(
            f"research-plan.md: no 'language:' in section 1; assuming {LEGACY_LANGUAGE!r}"
        )
        return LEGACY_LANGUAGE
    if match.group(1) not in LANGUAGES:
        report.error(
            f"research-plan.md: language must be one of {', '.join(LANGUAGES)}; "
            f"found {match.group(1)!r}"
        )
        return LEGACY_LANGUAGE
    return match.group(1)


def validate_markdown_layout(name: str, markdown: str, report: Report) -> None:
    lines = soft_break_lines(markdown)
    if lines:
        shown = ", ".join(str(line) for line in lines[:10])
        more = f" (+{len(lines) - 10} more)" if len(lines) > 10 else ""
        report.error(
            f"{name}: line break inside a paragraph or bullet at line(s) {shown}{more}; "
            "separate paragraphs and **Label:** lines with a blank line"
        )


def validate_plan(path: Path, language: str, report: Report) -> set[int]:
    plan_text = path.read_text()
    positions: list[int] = []
    for heading in text(language, "plan_headings"):
        position = plan_text.find(heading)
        if position < 0:
            report.error(f"research-plan.md: missing heading {heading!r}")
        positions.append(position)
    if all(position >= 0 for position in positions) and positions != sorted(positions):
        report.error("research-plan.md: required headings are out of order")

    values: dict[str, str] = {}
    for field in PROBLEM_FIELDS:
        match = re.search(rf"(?m)^{re.escape(field)}:\s*(.*)$", plan_text)
        if not match:
            report.error(f"research-plan.md: missing Problem Card field {field!r}")
        else:
            values[field] = match.group(1).strip()

    deliverable = re.search(r"(?m)^research_deliverable:\s*(.*)$", plan_text)
    if not deliverable:
        report.warn(
            "research-plan.md: no 'research_deliverable' in the Problem Card; add one of "
            + ", ".join(DELIVERABLES)
        )
    else:
        values["research_deliverable"] = deliverable.group(1).strip()
        keyword = re.match(r"[A-Za-z_]+", values["research_deliverable"].strip("\"' "))
        chosen = [keyword.group(0)] if keyword else []
        if chosen and chosen[0] != "__REQUIRED__" and chosen[0] not in DELIVERABLES:
            report.error(
                f"research-plan.md: research_deliverable must start with one of "
                f"{', '.join(DELIVERABLES)}; found {values['research_deliverable']!r}"
            )

    if re.search(r"(?i)\bTBD\b", plan_text):
        report.error("research-plan.md: TBD is prohibited")

    gate_rows: dict[int, tuple[str, str, str, str]] = {}
    for match in re.finditer(
        r"(?m)^\| G([0-6]) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
        plan_text,
    ):
        gate = int(match.group(1))
        gate_rows[gate] = tuple(part.strip() for part in match.groups()[1:])

    for gate in range(7):
        if gate not in gate_rows:
            report.error(f"research-plan.md: missing Gate Status row G{gate}")
            continue
        status, evidence, reviewer, reviewed_at = gate_rows[gate]
        if status not in ALLOWED_STATUSES:
            report.error(f"research-plan.md: invalid G{gate} status {status!r}")
        if status == "PASS" and any(
            value in {"", "—", "-", "__REQUIRED__"}
            for value in (evidence, reviewer, reviewed_at)
        ):
            report.error(f"research-plan.md: G{gate} PASS requires evidence, reviewer, and UTC review time")

    passed = {gate for gate, row in gate_rows.items() if row[0] == "PASS"}
    for gate in passed:
        missing = [f"G{previous}" for previous in range(gate) if previous not in passed]
        if missing:
            report.error(f"research-plan.md: G{gate} PASS before {', '.join(missing)}")

    active = [gate for gate, row in gate_rows.items() if row[0] == "IN_PROGRESS"]
    if len(active) > 1:
        report.error("research-plan.md: only one gate may be IN_PROGRESS")

    if gate_rows.get(0, (None,))[0] == "PASS":
        incomplete = [field for field, value in values.items() if not value or "__REQUIRED__" in value]
        if incomplete:
            report.error("research-plan.md: G0 PASS with incomplete Problem Card fields: " + ", ".join(incomplete))

    for gate in sorted({int(g) for g in re.findall(r"__REQUIRED_BEFORE_G([0-6])__", plan_text)}):
        if gate in passed:
            report.error(f"research-plan.md: G{gate} PASS but __REQUIRED_BEFORE_G{gate}__ placeholder remains")
    return passed


def validate_data_ignored(topic_dir: Path, plan: Path, report: Report) -> None:
    plan_text = plan.read_text()
    environment = re.search(r"(?m)^environment:\s*(\S+)\s*$", plan_text)
    domain = re.search(r"(?m)^domain:\s*(\S+)\s*$", plan_text)
    if not environment or not domain:
        report.error("research-plan.md: section 4 must declare environment and domain")
        return
    toplevel = subprocess.run(
        ["git", "-C", str(topic_dir), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if toplevel.returncode != 0:
        report.warn("topic is not inside a Git repository; skipped data ignore check")
        return
    project_root = Path(toplevel.stdout.strip())
    probe = project_root / "data" / environment.group(1) / domain.group(1) / "bronze" / ".probe"
    ignored = subprocess.run(
        ["git", "-C", str(project_root), "check-ignore", "-q", str(probe)],
        check=False,
    )
    if ignored.returncode != 0:
        report.error(f"data path is not Git-ignored: {probe.parent.parent} (S08.5)")


def validate_notebook(
    path: Path, passed_gates: set[int], language: str, report: Report
) -> None:
    try:
        document = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as error:
        report.error(f"{path.name}: invalid notebook JSON: {error}")
        return

    if document.get("nbformat") != 4:
        report.error(f"{path.name}: nbformat must be 4")
    cells = document.get("cells")
    if not isinstance(cells, list) or not cells:
        report.error(f"{path.name}: missing cells")
        return
    first = cells[0]
    if not isinstance(first, dict) or first.get("cell_type") != "markdown":
        report.error(f"{path.name}: first cell must be markdown")
        return
    header = cell_text(first)
    for label in text(language, "notebook_labels"):
        if label not in header:
            report.error(f"{path.name}: missing header label {label!r}")

    status = re.search(r"(?m)^\*\*Status:\*\*\s*(\S*)", header)
    if not status:
        report.error(f"{path.name}: missing header label '**Status:**'")
    elif status.group(1) not in ALLOWED_STATUSES:
        report.error(f"{path.name}: invalid notebook status {status.group(1)!r}")
    elif status.group(1) != "NOT_STARTED" and "__REQUIRED__" in header:
        report.error(f"{path.name}: status {status.group(1)} with __REQUIRED__ header placeholders")
    elif NOTEBOOK_GATES[path.name] in passed_gates and status.group(1) in {"NOT_STARTED", "IN_PROGRESS"}:
        report.error(
            f"{path.name}: G{NOTEBOOK_GATES[path.name]} is PASS but notebook status is {status.group(1)}"
        )

    for index, cell in enumerate(cells):
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown":
            validate_markdown_layout(f"{path.name} cell {index}", cell_text(cell), report)
    if status and status.group(1) != "NOT_STARTED":
        for issue in narrative_issues(cells, language):
            report.error(f"{path.name}: {issue}")


def validate_standard(standard_path: Path, evidence_path: Path, report: Report) -> None:
    standard_text = standard_path.read_text()
    evidence_text = evidence_path.read_text()
    definitions = re.findall(r"^\[(S\d{2}) \|", standard_text, re.MULTILINE)
    expected_standards = {f"S{index:02d}" for index in range(1, 22)}
    expected_evidence = {f"E{index:02d}" for index in range(1, 20)}
    defined_evidence = set(
        re.findall(r"^\| (E\d{2}) \|", evidence_text, re.MULTILINE)
    )
    if set(definitions) != expected_standards or any(
        count != 1 for count in Counter(definitions).values()
    ):
        report.error("standard.md: standards must define S01 through S21 exactly once")
    if defined_evidence != expected_evidence:
        report.error("evidence.md: registry must define E01 through E19")
    used_evidence = set(re.findall(r"\bE\d{2}\b", standard_text + evidence_text))
    if not used_evidence <= defined_evidence:
        report.error(
            "undefined evidence IDs: "
            + ", ".join(sorted(used_evidence - defined_evidence))
        )
    try:
        trace = evidence_text.split("## Traceability matrix", 1)[1]
    except IndexError:
        report.error("evidence.md: missing traceability matrix")
    else:
        traced = set(re.findall(r"\bS\d{2}\b", trace))
        if not expected_standards <= traced:
            report.error(
                "evidence.md: untraced standards: "
                + ", ".join(sorted(expected_standards - traced))
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic_dir", type=Path)
    parser.add_argument(
        "--standard",
        type=Path,
        help="standard file to validate; defaults to the copy bundled with this skill",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="evidence registry to validate; defaults to the copy bundled with this skill",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    topic_dir = args.topic_dir.expanduser().resolve()
    report = Report()

    if not topic_dir.is_dir():
        report.error(f"topic directory does not exist: {topic_dir}")
    else:
        md_dir = markdown_dir_for_topic(topic_dir)

        def location(filename: str) -> Path:
            return (md_dir if filename.endswith(".md") else topic_dir) / filename

        for filename in REQUIRED_FILES:
            if not location(filename).is_file():
                report.error(f"missing required file: {location(filename)}")

        plan = md_dir / "research-plan.md"
        passed_gates: set[int] = set()
        language = LEGACY_LANGUAGE
        if plan.is_file():
            language = read_language(plan, report)
            passed_gates = validate_plan(plan, language, report)
            validate_data_ignored(topic_dir, plan, report)
        for name in ("research-plan.md", "research-log.md"):
            if (md_dir / name).is_file():
                validate_markdown_layout(name, (md_dir / name).read_text(), report)
        for filename in REQUIRED_FILES:
            if filename.endswith(".ipynb") and (topic_dir / filename).is_file():
                validate_notebook(topic_dir / filename, passed_gates, language, report)

    references = Path(__file__).resolve().parents[1] / "references"
    standard = args.standard or references / "standard.md"
    evidence = args.evidence or references / "evidence.md"
    if not standard.is_file():
        report.error(f"standard file does not exist: {standard}")
    elif not evidence.is_file():
        report.error(f"evidence file does not exist: {evidence}")
    else:
        validate_standard(standard, evidence, report)

    for warning in report.warnings:
        print(f"WARN: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    if report.errors:
        print(f"FAIL: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    print(f"PASS: structure valid ({len(report.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
