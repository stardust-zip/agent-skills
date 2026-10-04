"""Where a research topic's Markdown files live.

Notebooks always live in {project-root}/notebooks/<slug>/. The Markdown files
(research-plan.md, research-log.md) live there too, except on a work machine,
marked by the ~/work-docs directory existing: there, company policy forbids
pushing Markdown to the work Git host, so they go to
~/work-docs/<repo-name>/notebooks/<slug>/ instead, outside the repository.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def work_docs_root() -> Path | None:
    root = Path.home() / "work-docs"
    return root if root.is_dir() else None


def markdown_dir(project_root: Path, slug: str) -> Path:
    root = work_docs_root()
    if root is None:
        return project_root / "notebooks" / slug
    return root / project_root.name / "notebooks" / slug


def markdown_dir_for_topic(topic_dir: Path) -> Path:
    toplevel = subprocess.run(
        ["git", "-C", str(topic_dir), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if toplevel.returncode != 0:
        return topic_dir
    return markdown_dir(Path(toplevel.stdout.strip()), topic_dir.name)
