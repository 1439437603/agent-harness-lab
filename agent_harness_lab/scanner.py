from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileSummary:
    path: Path
    size: int
    category: str


def classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".rst"}:
        return "documentation"
    if suffix in {".html", ".css", ".js", ".ts", ".tsx", ".py", ".go", ".rs", ".java"}:
        return "code-or-page"
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov"}:
        return "media-evidence"
    if suffix in {".json", ".jsonl", ".yaml", ".yml", ".toml"}:
        return "config-or-data"
    return "other"


def scan_workspace(project_root: Path, ignore_dirs: tuple[str, ...]) -> list[FileSummary]:
    project_root = project_root.resolve()
    ignored = set(ignore_dirs)
    summaries: list[FileSummary] = []

    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(project_root)
        if any(part in ignored for part in relative.parts):
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        summaries.append(
            FileSummary(
                path=relative,
                size=size,
                category=classify_file(path),
            )
        )

    return sorted(summaries, key=lambda item: (item.category, str(item.path)))
