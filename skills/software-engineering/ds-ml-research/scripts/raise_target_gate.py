#!/usr/bin/env python3
"""Raise a research topic's target gate and add the notebooks it now needs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from init_research import NOTEBOOKS, notebook_document, render
from research_lang import LANGUAGES, text
from topic_paths import TARGET_GATES, gate_number, markdown_dir_for_topic, required_by


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic_dir", type=Path)
    parser.add_argument("target_gate", choices=TARGET_GATES)
    args = parser.parse_args()

    topic_dir = args.topic_dir.expanduser().resolve()
    plan_path = markdown_dir_for_topic(topic_dir) / "research-plan.md"
    if not plan_path.is_file():
        print(f"ERROR: research plan not found: {plan_path}", file=sys.stderr)
        return 2
    plan = plan_path.read_text()

    language = re.search(r"(?m)^language:\s*(\S+)\s*$", plan)
    current = re.search(r"(?m)^target_gate:\s*(G[0-6])\s*$", plan)
    slug = re.search(r"(?m)^research_slug:\s*(\S+)\s*$", plan)
    if not language or language.group(1) not in LANGUAGES or not current or not slug:
        print("ERROR: research-plan.md section 1 needs language, target_gate and research_slug", file=sys.stderr)
        return 2
    if gate_number(args.target_gate) <= gate_number(current.group(1)):
        print(f"ERROR: target gate is already {current.group(1)}", file=sys.stderr)
        return 1

    assets = Path(__file__).resolve().parents[1] / "assets" / language.group(1)
    header_template = (assets / "notebook-header.md").read_text()
    questions = text(language.group(1), "notebooks")
    added = []
    for filename, number, title, gate in NOTEBOOKS:
        path = topic_dir / filename
        if path.exists() or not required_by(args.target_gate, gate):
            continue
        header = render(
            header_template,
            {
                "NUMBER": number,
                "TITLE": title,
                "GATE": gate,
                "QUESTION": questions[filename][0],
                "OUTPUT": questions[filename][1],
            },
        )
        path.write_text(
            json.dumps(notebook_document(header, language.group(1)), ensure_ascii=False, indent=1) + "\n"
        )
        added.append(filename)

    plan_path.write_text(
        plan.replace(current.group(0), f"target_gate: {args.target_gate}", 1)
    )
    print(f"Target gate: {current.group(1)} -> {args.target_gate}")
    print(f"Added notebooks: {', '.join(added) or 'none'}")
    print("Record the change and its reason in research-log.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
