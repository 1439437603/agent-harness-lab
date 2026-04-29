from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_TASK_FILE = ROOT / "examples" / "task.md"
DEFAULT_REPORT_FILE = ROOT / "output" / "run-report.md"

RUNTIME_MODULES = {
    "engine": "Task ingestion, workspace scan, step planning, report assembly.",
    "tools": "Deterministic filesystem inspection with explicit file classification.",
    "storage": "Markdown task briefs, generated reports, and evaluation artifacts.",
    "types": "Dataclasses that make file summaries and evaluation cases inspectable.",
    "evaluation": "Built-in checks that keep the harness output bounded and reproducible.",
}

OBSERVABILITY_EVENTS = (
    "task.loaded",
    "workspace.scanned",
    "materials.classified",
    "report.generated",
    "evaluation.checked",
)


@dataclass(frozen=True)
class FileSummary:
    path: Path
    size: int
    category: str


@dataclass(frozen=True)
class EvalCase:
    name: str
    task_file: Path
    required_phrases: tuple[str, ...]


def read_task(task_file: Path) -> str:
    return task_file.read_text(encoding="utf-8").strip()


def classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return "documentation"
    if suffix in {".html", ".css", ".js", ".ts", ".tsx", ".py"}:
        return "code-or-page"
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov"}:
        return "media-evidence"
    return "other"


def scan_workspace(root: Path = ROOT) -> list[FileSummary]:
    ignored_parts = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
    summaries: list[FileSummary] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.relative_to(root).parts):
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        summaries.append(
            FileSummary(
                path=path.relative_to(root),
                size=size,
                category=classify_file(path),
            )
        )

    return sorted(summaries, key=lambda item: (item.category, str(item.path)))


def build_execution_steps(files: list[FileSummary]) -> list[str]:
    has_docs = any(item.category == "documentation" for item in files)
    has_code = any(item.category == "code-or-page" for item in files)

    steps = [
        "Read the task brief and lock the goal, expected output, and constraints.",
        "Scan the workspace and classify available files into documentation, code/page assets, media evidence, and other materials.",
    ]

    if has_docs:
        steps.append("Use Markdown documents as the primary source for project claims, evidence notes, and review-ready copy.")
    if has_code:
        steps.append("Use Python and page files as runnable or inspectable proof that the harness is more than a static write-up.")

    steps.extend(
        [
            "Generate a compact action plan with risks, verification points, and the highest-ROI next step.",
            "Write a Markdown report that can be attached to a grant application or reviewed in GitHub.",
            "Keep claims bounded to what the repository proves; do not invent production usage, users, or token spend.",
        ]
    )
    return steps


def summarize_categories(files: list[FileSummary]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in files:
        counts[item.category] = counts.get(item.category, 0) + 1
    return counts


def build_report(task: str, files: list[FileSummary]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    steps = build_execution_steps(files)
    category_counts = summarize_categories(files)
    evidence_files = [
        item for item in files if item.category in {"documentation", "code-or-page"}
    ][:12]

    lines = [
        "# Agent Harness Lab Run Report",
        "",
        f"- Run time: {now}",
        f"- Workspace: `{ROOT}`",
        "",
        "## Input Task",
        "",
        task,
        "",
        "## Workspace Scan",
        "",
    ]

    for category in sorted(category_counts):
        lines.append(f"- {category}: {category_counts[category]} files")

    lines.extend(["", "## Evidence Files", ""])
    for item in evidence_files:
        lines.append(f"- `{item.path}` ({item.category}, {item.size} bytes)")

    lines.extend(["", "## Runtime Contract", ""])
    for name, description in RUNTIME_MODULES.items():
        lines.append(f"- `{name}`: {description}")

    lines.extend(["", "## Observability Events", ""])
    for event in OBSERVABILITY_EVENTS:
        lines.append(f"- `{event}`")

    lines.extend(["", "## Harness Steps", ""])
    for index, step in enumerate(steps, start=1):
        lines.append(f"{index}. {step}")

    lines.extend(
        [
            "",
            "## Result Summary",
            "",
            "Agent Harness Lab is a TDD-first reference implementation for building reproducible AI agent workflows. "
            "This run demonstrates a minimal but reviewable loop: task input, workspace scan, material classification, "
            "runtime-contract reporting, observability event listing, step decomposition, risk recording, and Markdown report generation.",
            "",
            "The current version intentionally stays local and deterministic. It does not claim production traffic, "
            "commercial impact, or external model integration. The value is that the workflow can be run, inspected, "
            "tested, evaluated, and extended into a stronger agent runtime.",
            "",
            "## Risks",
            "",
            "- This is a local reference implementation, not a deployed commercial agent.",
            "- It does not call external LLM APIs yet, so model-driven tool execution remains future work.",
            "- Usage evidence should be limited to repository code, terminal runs, generated reports, and screenshots.",
            "",
            "## Highest-ROI Next Step",
            "",
            "Publish this repository, attach a terminal run screenshot and the generated report, then extend the harness "
            "with a small tool registry and more evaluation cases.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(task_file: Path, report_file: Path) -> Path:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    task = read_task(task_file)
    files = scan_workspace()
    report = build_report(task, files)
    report_file.write_text(report, encoding="utf-8")
    return report_file


def run_eval() -> int:
    cases = [
        EvalCase(
            name="default task produces harness report",
            task_file=DEFAULT_TASK_FILE,
            required_phrases=("Workspace Scan", "Harness Steps", "Highest-ROI Next Step"),
        ),
        EvalCase(
            name="report keeps claims bounded",
            task_file=DEFAULT_TASK_FILE,
            required_phrases=("local reference implementation", "does not claim production traffic"),
        ),
        EvalCase(
            name="report includes reproducible evidence",
            task_file=DEFAULT_TASK_FILE,
            required_phrases=("Evidence Files", "Markdown report generation"),
        ),
        EvalCase(
            name="report exposes runtime and observability contracts",
            task_file=DEFAULT_TASK_FILE,
            required_phrases=("Runtime Contract", "Observability Events", "task.loaded"),
        ),
    ]

    failures: list[str] = []
    files = scan_workspace()
    task = read_task(DEFAULT_TASK_FILE)
    report = build_report(task, files)

    for case in cases:
        missing = [phrase for phrase in case.required_phrases if phrase not in report]
        if missing:
            failures.append(f"{case.name}: missing {', '.join(missing)}")

    if failures:
        print("Evaluation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Evaluation passed: {len(cases)}/{len(cases)} cases")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Agent Harness Lab.")
    parser.add_argument("--task", type=Path, default=DEFAULT_TASK_FILE, help="Markdown task file.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_FILE, help="Output report path.")
    parser.add_argument("--eval", action="store_true", help="Run the built-in evaluation cases.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.eval:
        return run_eval()

    report_file = write_report(args.task, args.report)
    print(f"Generated report: {report_file}")
    print(f"Scanned files: {len(scan_workspace())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
