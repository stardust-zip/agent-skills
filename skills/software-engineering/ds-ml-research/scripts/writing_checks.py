"""Mechanical checks for research prose: Markdown layout and notebook narrative."""

from __future__ import annotations

import re

from research_lang import (
    ANALYSIS_SECTION,
    ANSWER_MIN_WORDS,
    AUDIT_CODE,
    FINDINGS_PROSE_MIN_WORDS,
    FINDINGS_SECTION,
    LOOK_FOR_MIN_WORDS,
    NARRATIVE_PLACEHOLDER,
    QUESTION_MIN_WORDS,
    QUESTIONS_SECTION,
    SECTION_COUNT,
    text,
)

FENCE = re.compile(r"^\s*(```|~~~)")
STRUCTURAL = re.compile(r"^\s*([-*+] |\d+[.)] |#|\||>|<|!\[|\$\$|---\s*$)")
LABEL_LINE = re.compile(r"^\*\*[^*]+:\*\*")
SECTION_HEADING = re.compile(r"^## (\d+)\. ")
BLOCK_HEADING = re.compile(rf"^### {ANALYSIS_SECTION}\.(\d+)\. ")
QUESTION_ITEM = re.compile(r"(?m)^(\d+)\. (.+)$")
RICH_OUTPUTS = ("image/png", "image/jpeg", "image/svg+xml", "text/html")


def _prose_lines(markdown: str) -> list[tuple[int, str]]:
    """Return (line number, line) pairs outside code fences, HTML comments and front matter."""
    result = []
    in_fence = in_comment = False
    lines = markdown.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if closing is not None:
            start = closing + 1
    for number, line in enumerate(lines[start:], start=start + 1):
        if FENCE.match(line):
            in_fence = not in_fence
            result.append((number, ""))
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
        if in_fence or in_comment:
            result.append((number, ""))
            if "-->" in line:
                in_comment = False
            continue
        result.append((number, line))
    return result


def soft_break_lines(markdown: str) -> list[int]:
    """Line numbers where a paragraph or bullet continues on the next source line.

    Markdown renders such lines as one paragraph, so they either break a sentence
    mid-way or cluster separate ideas (for example consecutive **Label:** lines).
    """
    found = []
    previous = ""
    for number, line in _prose_lines(markdown):
        continues = (
            line.strip()
            and previous.strip()
            and not STRUCTURAL.match(line)
            and not previous.lstrip().startswith(("#", "|", ">", "<"))
            and not previous.rstrip().endswith(("  ", "\\"))
        )
        clustered_labels = LABEL_LINE.match(line) and LABEL_LINE.match(previous)
        if continues or clustered_labels:
            found.append(number)
        previous = line
    return found


def word_count(markdown: str) -> int:
    cleaned = re.sub(r"\*\*[^*]+:\*\*", " ", markdown)
    cleaned = cleaned.replace(NARRATIVE_PLACEHOLDER, " ")
    return sum(1 for token in cleaned.split() if re.search(r"\w", token))


def cell_text(cell: dict[str, object]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(item) for item in source)
    return str(source)


def _rich_output_count(cell: dict[str, object]) -> int:
    count = 0
    for output in cell.get("outputs", []) or []:
        data = output.get("data", {}) if isinstance(output, dict) else {}
        html = data.get("text/html", "")
        html = "".join(html) if isinstance(html, list) else str(html)
        if (not any(kind in data for kind in RICH_OUTPUTS if kind != "text/html")
                and re.fullmatch(r"(?:\s*<style\b[^>]*>[\s\S]*?</style>\s*)+", html, re.IGNORECASE)):
            continue  # CSS-only notebook styling does not show a table or figure.
        if any(kind in data for kind in RICH_OUTPUTS):
            count += 1
    return count


def _label_text(markdown: str, label: str, stop_labels: list[str]) -> str:
    """Text after `label`, up to the next stop label or the end of the cell."""
    start = markdown.find(label)
    if start < 0:
        return ""
    body = markdown[start + len(label):]
    cut = min((body.find(stop) for stop in stop_labels if stop in body), default=len(body))
    return body[:cut].strip()


def _audit_codes(prose: str) -> list[str]:
    return sorted(set(re.findall(AUDIT_CODE, prose)))


class _Layout:
    """Cells grouped into `## N.` sections and `### 3.k.` analysis blocks."""

    def __init__(self, cells: list[dict[str, object]]) -> None:
        self.section_order: list[int] = []
        self.sections: dict[int, list[tuple[int, dict[str, object]]]] = {}
        self.block_order: list[int] = []
        self.blocks: dict[int, list[tuple[int, dict[str, object]]]] = {}
        section = block = 0
        for index, cell in enumerate(cells):
            if index == 0:
                continue
            if cell.get("cell_type") == "markdown":
                first_line = cell_text(cell).lstrip().split("\n", 1)[0]
                heading = SECTION_HEADING.match(first_line)
                if heading:
                    section = int(heading.group(1))
                    self.section_order.append(section)
                    block = 0
                sub = BLOCK_HEADING.match(first_line)
                if sub and section == ANALYSIS_SECTION:
                    block = int(sub.group(1))
                    self.block_order.append(block)
            self.sections.setdefault(section, []).append((index, cell))
            if block:
                self.blocks.setdefault(block, []).append((index, cell))

    def markdown(self, section: int) -> str:
        return "\n\n".join(
            cell_text(cell)
            for _, cell in self.sections.get(section, [])
            if cell.get("cell_type") == "markdown"
        )


def _question_issues(layout: _Layout, language: str) -> tuple[list[int], list[str]]:
    issues = []
    items = QUESTION_ITEM.findall(layout.markdown(QUESTIONS_SECTION))
    numbers = [int(number) for number, _ in items]
    if not numbers:
        issues.append(f"section {QUESTIONS_SECTION} must list the questions as '1. ...', '2. ...'")
    elif numbers != list(range(1, len(numbers) + 1)):
        issues.append(f"section {QUESTIONS_SECTION} questions must be numbered 1..n (found {numbers})")
    for number, question in items:
        if word_count(question) < QUESTION_MIN_WORDS:
            issues.append(
                f"question {number} needs at least {QUESTION_MIN_WORDS} words: "
                "the question and why it matters for the decision"
            )
        codes = _audit_codes(question)
        if codes:
            issues.append(f"question {number} uses audit codes {', '.join(codes)}; move them to {text(language, 'trace')}")
    return numbers, issues


def _block_issues(number: int, cells: list[tuple[int, dict[str, object]]], language: str) -> list[str]:
    look_for, answer, trace = (str(text(language, key)) for key in ("look_for", "answer", "trace"))
    stops = [look_for, answer, trace]
    where = f"block {ANALYSIS_SECTION}.{number}"
    code_positions = [pos for pos, (_, cell) in enumerate(cells) if cell.get("cell_type") == "code"]
    if not code_positions:
        return [f"{where} has no code cell"]

    issues = []
    before = "\n\n".join(
        cell_text(cell) for _, cell in cells[: code_positions[0]] if cell.get("cell_type") == "markdown"
    )
    after = "\n\n".join(
        cell_text(cell) for _, cell in cells[code_positions[-1] + 1 :] if cell.get("cell_type") == "markdown"
    )
    for label, source, minimum, position in (
        (look_for, before, LOOK_FOR_MIN_WORDS, "before its first code cell"),
        (answer, after, ANSWER_MIN_WORDS, "after its last code cell"),
    ):
        prose = _label_text(source, label, stops)
        if label not in source:
            issues.append(f"{where} needs {label} {position}")
        elif word_count(prose) < minimum:
            issues.append(f"{where} {label} has {word_count(prose)} words; at least {minimum} required")
        codes = _audit_codes(prose)
        if codes:
            issues.append(f"{where} {label} uses audit codes {', '.join(codes)}; move them to {trace}")
    return issues


def _output_issues(cells: list[dict[str, object]], layout: _Layout) -> list[str]:
    issues = []
    in_blocks = {index for block in layout.blocks.values() for index, _ in block}
    for index, cell in enumerate(cells):
        rich = _rich_output_count(cell) if cell.get("cell_type") == "code" else 0
        if not rich:
            continue
        if index not in in_blocks:
            issues.append(f"code cell {index} shows a table/figure outside a {ANALYSIS_SECTION}.k question block")
        if rich > 1:
            issues.append(f"code cell {index} shows {rich} tables/figures; show one per cell")
        following = cells[index + 1] if index + 1 < len(cells) else None
        if following is None or following.get("cell_type") != "markdown":
            issues.append(f"code cell {index} shows a table/figure that is not followed by markdown")
    return issues


def _findings_issues(layout: _Layout, numbers: list[int], language: str) -> list[str]:
    issues = []
    body = layout.markdown(FINDINGS_SECTION)
    verdicts = text(language, "verdicts")
    rows = {}
    for line in body.splitlines():
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and cells and cells[0].rstrip(".").isdigit():
            rows[int(cells[0].rstrip("."))] = cells
    if sorted(rows) != numbers:
        issues.append(
            f"findings table must have one row per question {numbers}; found rows {sorted(rows)}"
        )
    for number, cells in sorted(rows.items()):
        if len(cells) < 5 or cells[3] not in verdicts:
            issues.append(f"findings row {number}: verdict must be one of {', '.join(verdicts)}")
    for key in ("not_proven", "limitations", "next_decision"):
        if str(text(language, key)) not in body:
            issues.append(f"section {FINDINGS_SECTION} needs {text(language, key)}")
    prose = "\n".join(line for line in body.splitlines() if not line.lstrip().startswith("|"))
    if word_count(prose) < FINDINGS_PROSE_MIN_WORDS:
        issues.append(
            f"section {FINDINGS_SECTION} has {word_count(prose)} words outside the table; "
            f"at least {FINDINGS_PROSE_MIN_WORDS} required"
        )
    return issues


def narrative_issues(cells: list[dict[str, object]], language: str) -> list[str]:
    """Check the question-driven layout of a started notebook (standard section 13.5)."""
    layout = _Layout(cells)
    issues = []
    expected = list(range(1, SECTION_COUNT + 1))
    if layout.section_order != expected:
        issues.append(
            f"sections must be '## 1.' to '## {SECTION_COUNT}.' exactly once and in order "
            f"(found {layout.section_order or 'none'})"
        )
    numbers, question_issues = _question_issues(layout, language)
    issues += question_issues
    if layout.block_order != numbers:
        issues.append(
            f"section {ANALYSIS_SECTION} must have one '### {ANALYSIS_SECTION}.k.' block per question, "
            f"in order: expected {numbers}, found {layout.block_order}"
        )
    for number in layout.block_order:
        issues += _block_issues(number, layout.blocks[number], language)
    issues += _output_issues(cells, layout)
    issues += _findings_issues(layout, numbers, language)
    if any(NARRATIVE_PLACEHOLDER in cell_text(cell) for cell in cells):
        issues.append(f"{NARRATIVE_PLACEHOLDER} placeholder remains")
    return issues
