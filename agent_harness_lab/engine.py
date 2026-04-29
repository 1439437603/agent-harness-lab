from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from agent_harness_lab.config import HarnessConfig, load_config
from agent_harness_lab.reporting import build_markdown_report, result_to_json, write_events_jsonl, write_json
from agent_harness_lab.scanner import FileSummary, scan_workspace


RUNTIME_MODULES = {
    "engine": "Task ingestion, workspace scan, step planning, report assembly.",
    "tools": "Deterministic filesystem inspection with explicit file classification.",
    "storage": "Markdown task briefs, JSON results, JSONL events, and generated reports.",
    "types": "Dataclasses that make file summaries, runtime events, and run results inspectable.",
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
class RuntimeEvent:
    event: str
    message: str
    timestamp: str


@dataclass(frozen=True)
class HarnessResult:
    generated_at: str
    project_name: str
    project_root: Path
    task_file: Path
    task: str
    files: list[FileSummary]
    evidence_files: list[FileSummary]
    category_counts: dict[str, int]
    runtime_modules: dict[str, str]
    observability_events: tuple[str, ...]
    steps: list[str]
    summary: str
    risks: list[str]
    next_step: str
    output_dir: Path


def read_task(task_file: Path) -> str:
    return task_file.read_text(encoding="utf-8").strip()


def summarize_categories(files: list[FileSummary]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in files:
        counts[item.category] = counts.get(item.category, 0) + 1
    return counts


def build_execution_steps(files: list[FileSummary]) -> list[str]:
    has_docs = any(item.category == "documentation" for item in files)
    has_code = any(item.category == "code-or-page" for item in files)
    has_config = any(item.category == "config-or-data" for item in files)

    steps = [
        "Read the task brief and lock the goal, expected output, and constraints.",
        "Load harness configuration so project name, ignored directories, and output location are explicit.",
        "Scan the target project and classify available files into documentation, code/page assets, config/data, media evidence, and other materials.",
    ]
    if has_docs:
        steps.append("Use project documentation as the primary source for claims, evidence notes, and review-ready copy.")
    if has_code:
        steps.append("Use source files as inspectable evidence that the harness is analyzing a real project tree.")
    if has_config:
        steps.append("Preserve config/data files as machine-readable evidence for CI or downstream automation.")

    steps.extend(
        [
            "Generate Markdown, JSON, and JSONL artifacts so humans, scripts, and CI can consume the same run.",
            "Run lightweight evaluation checks that guard against vague or unsupported claims.",
            "Keep claims bounded to what the target project and generated artifacts prove.",
        ]
    )
    return steps


def build_result(
    project_root: Path,
    task_file: Path,
    config: HarnessConfig,
    output_dir: Path,
) -> tuple[HarnessResult, list[RuntimeEvent]]:
    generated_at = datetime.now().isoformat(timespec="seconds")
    events: list[RuntimeEvent] = []

    task = read_task(task_file)
    events.append(RuntimeEvent("task.loaded", f"Loaded task from {task_file}", generated_at))

    scan_ignore_dirs = tuple(dict.fromkeys([*config.ignore_dirs, config.output_dir]))
    files = scan_workspace(project_root, scan_ignore_dirs)
    events.append(RuntimeEvent("workspace.scanned", f"Scanned {len(files)} files", generated_at))

    category_counts = summarize_categories(files)
    events.append(RuntimeEvent("materials.classified", f"Found {len(category_counts)} categories", generated_at))

    evidence_files = [
        item for item in files if item.category in {"documentation", "code-or-page", "config-or-data"}
    ][: config.max_evidence_files]

    summary = (
        "Agent Harness Lab is a project-ready, TDD-first harness for scanning local codebases, "
        "producing reproducible agent workflow reports, and validating outputs with lightweight evaluation checks."
    )
    risks = [
        "The harness is deterministic and local; external LLM tool execution is not enabled in v0.2.",
        "Generated reports should be treated as evidence summaries, not as proof of production usage.",
        "Large repositories may need narrower ignore rules before report output is concise.",
    ]
    next_step = (
        "Integrate this command into a real project workflow with `agent-harness run --project <path> --task <file>`, "
        "then add project-specific evaluation cases."
    )

    result = HarnessResult(
        generated_at=generated_at,
        project_name=config.project_name,
        project_root=project_root,
        task_file=task_file,
        task=task,
        files=files,
        evidence_files=evidence_files,
        category_counts=category_counts,
        runtime_modules=RUNTIME_MODULES,
        observability_events=OBSERVABILITY_EVENTS,
        steps=build_execution_steps(files),
        summary=summary,
        risks=risks,
        next_step=next_step,
        output_dir=output_dir,
    )
    return result, events


def run_harness(
    project_root: Path,
    task_file: Path,
    output_dir: Path | None = None,
    config: HarnessConfig | None = None,
) -> HarnessResult:
    project_root = project_root.resolve()
    task_file = task_file.resolve()
    config = config or load_config(project_root)
    output_dir = output_dir or project_root / config.output_dir
    if not output_dir.is_absolute():
        output_dir = project_root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    result, events = build_result(project_root, task_file, config, output_dir)

    (output_dir / "run-report.md").write_text(build_markdown_report(result), encoding="utf-8")
    write_json(output_dir / "run-result.json", result_to_json(result))
    events.append(RuntimeEvent("report.generated", f"Wrote artifacts to {output_dir}", result.generated_at))
    events.append(RuntimeEvent("evaluation.checked", "Prepared run artifacts for evaluation", result.generated_at))
    write_events_jsonl(output_dir / "events.jsonl", events)
    return result


def evaluate_report_text(report_text: str) -> list[str]:
    required = (
        "Workspace Scan",
        "Runtime Contract",
        "Observability Events",
        "Highest-ROI Next Step",
        "project-ready",
    )
    return [phrase for phrase in required if phrase not in report_text]
