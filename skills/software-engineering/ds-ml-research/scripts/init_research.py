#!/usr/bin/env python3
"""Create a deterministic DS/ML research topic from the skill assets."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from research_lang import LANGUAGES, NARRATIVE_PLACEHOLDER, text


SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
NOTEBOOKS = (
    ("00_data_inventory.ipynb", "00", "Data inventory", "G1"),
    ("01_data_quality.ipynb", "01", "Data quality", "G1"),
    ("02_eda.ipynb", "02", "Exploratory data analysis", "G2"),
    ("03_build_dataset.ipynb", "03", "Build dataset", "G2"),
    ("04_baselines.ipynb", "04", "Baselines", "G3"),
    ("05_candidates.ipynb", "05", "Candidate experiments", "G4"),
    ("06_evaluation.ipynb", "06", "Locked-test evaluation", "G5"),
)


def safe_name(value: str, flag: str) -> str:
    if not SAFE_NAME.fullmatch(value):
        raise ValueError(
            f"{flag} must match {SAFE_NAME.pattern!r}; received {value!r}"
        )
    return value


def render(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", result)))
    if unresolved:
        raise ValueError(f"unresolved template variables: {', '.join(unresolved)}")
    return result


def markdown_cell(cell_id: str, content: str) -> dict[str, object]:
    source = [line + "\n" for line in content.rstrip("\n").splitlines()]
    if source:
        source[-1] = source[-1].rstrip("\n")
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}


def section_cells(language: str) -> list[dict[str, object]]:
    """Skeleton of standard section 13.2 with one example question block."""
    todo = NARRATIVE_PLACEHOLDER
    titles = text(language, "section_titles")

    def label(key: str) -> str:
        return str(text(language, key))

    divider = "|" + "---|" * (label("findings_header").count("|") - 1)
    contents = [
        f"## 1. {titles[0]}\n\n{todo}\n\n1. {todo}",
        f"## 2. {titles[1]}",
        f"## 3. {titles[2]}",
        f"### 3.1. {todo}\n\n{label('look_for')} {todo}",
        f"{label('answer')} {todo}\n\n{label('trace')} {todo}",
        f"## 4. {titles[3]}",
        "\n\n".join(
            [
                f"## 5. {titles[4]}",
                f"{label('findings_header')}\n{divider}\n| 1 | {todo} | {todo} | {todo} | {todo} |",
                f"{label('not_proven')} {todo}",
                f"{label('limitations')} {todo}",
                f"{label('next_decision')} {todo}",
            ]
        ),
    ]
    return [markdown_cell(f"section-{index}", content) for index, content in enumerate(contents)]


def notebook_document(header: str, language: str) -> dict[str, object]:
    return {
        "cells": [markdown_cell("research-header", header), *section_cells(language)],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def current_umask() -> int:
    mask = os.umask(0)
    os.umask(mask)
    return mask


def is_git_ignored(project_root: Path, path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(project_root), "check-ignore", "-q", str(path)],
        check=False,
    )
    return result.returncode == 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument(
        "--language",
        required=True,
        choices=LANGUAGES,
        help="prose language of the research artifacts; technical terms stay in English",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        slug = safe_name(args.slug, "--slug")
        environment = safe_name(args.environment, "--environment")
        domain = safe_name(args.domain, "--domain")
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    language = args.language

    project_root = args.project_root.expanduser().resolve()
    if not (project_root / ".git").exists():
        print(f"ERROR: not a Git repository root: {project_root}", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets" / language
    topic_dir = project_root / "notebooks" / slug
    if topic_dir.exists():
        print(f"ERROR: topic already exists: {topic_dir}", file=sys.stderr)
        return 1

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    common = {
        "RESEARCH_SLUG": slug,
        "ENVIRONMENT": environment,
        "DOMAIN": domain,
        "CREATED_AT_UTC": created_at,
    }

    header_template = (assets / "notebook-header.md").read_text()
    questions = text(language, "notebooks")
    try:
        plan = render((assets / "research-plan.md").read_text(), common)
        log = render((assets / "research-log.md").read_text(), common)
        notebooks = {
            filename: render(
                header_template,
                common
                | {
                    "NUMBER": number,
                    "TITLE": title,
                    "GATE": gate,
                    "QUESTION": questions[filename][0],
                    "OUTPUT": questions[filename][1],
                },
            )
            for filename, number, title, gate in NOTEBOOKS
        }
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    topic_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{slug}-", dir=topic_dir.parent))
    try:
        staging.chmod(0o777 & ~current_umask())
        (staging / "research-plan.md").write_text(plan)
        (staging / "research-log.md").write_text(log)
        for filename, header in notebooks.items():
            (staging / filename).write_text(
                json.dumps(notebook_document(header, language), ensure_ascii=False, indent=1)
                + "\n"
            )
        staging.rename(topic_dir)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    data_root = project_root / "data" / environment / domain
    for layer in ("bronze", "silver", "gold", "manifests"):
        (data_root / layer).mkdir(parents=True, exist_ok=True)
    if not is_git_ignored(project_root, data_root / "bronze" / ".probe"):
        (data_root / ".gitignore").write_text("*\n!.gitignore\n")
        print(f"Added {data_root / '.gitignore'} so local data is not committed")

    print(f"Created research topic: {topic_dir} (language: {language})")
    print(f"Created data layers: {data_root}")
    print("Current state: G0 NOT_STARTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
