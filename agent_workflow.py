from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

from agent_harness_lab.cli import main as cli_main
from agent_harness_lab.config import HarnessConfig, load_config
from agent_harness_lab.engine import (
    HarnessResult,
    OBSERVABILITY_EVENTS,
    RUNTIME_MODULES,
    build_execution_steps,
    evaluate_report_text,
    read_task,
    run_harness,
    summarize_categories,
)
from agent_harness_lab.reporting import build_markdown_report
from agent_harness_lab.scanner import FileSummary, classify_file, scan_workspace as _scan_workspace


ROOT = Path(__file__).resolve().parent
DEFAULT_TASK_FILE = ROOT / "examples" / "task.md"
DEFAULT_REPORT_FILE = ROOT / "output" / "run-report.md"


def scan_workspace(root: Path = ROOT) -> list[FileSummary]:
    return _scan_workspace(root, load_config(root).ignore_dirs)


def build_report(task: str, files: list[FileSummary]) -> str:
    config = load_config(ROOT)
    result = HarnessResult(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        project_name=config.project_name,
        project_root=ROOT,
        task_file=DEFAULT_TASK_FILE,
        task=task,
        files=files,
        artifact_files=[
            item for item in files if item.category in {"documentation", "code-or-page", "config-or-data"}
        ][: config.max_artifact_files],
        category_counts=summarize_categories(files),
        runtime_modules=RUNTIME_MODULES,
        observability_events=OBSERVABILITY_EVENTS,
        check_results=[],
        steps=build_execution_steps(files),
        summary=(
            "Agent Harness Lab is a project-ready, TDD-first harness for scanning local codebases, "
            "producing reproducible agent workflow reports, and validating outputs with lightweight evaluation checks."
        ),
        risks=[
            "The harness is deterministic and local; external LLM tool execution is not enabled in v0.2.",
            "Generated reports are operational summaries and should be reviewed before use in release workflows.",
        ],
        next_step="Run the harness against a target project and add project-specific evaluation cases.",
        output_dir=ROOT / config.output_dir,
    )
    return build_markdown_report(result)


def write_report(task_file: Path, report_file: Path) -> Path:
    base_config = load_config(ROOT)
    config = HarnessConfig(
        project_name=base_config.project_name,
        output_dir=base_config.output_dir,
        ignore_dirs=base_config.ignore_dirs,
        max_artifact_files=base_config.max_artifact_files,
        check_timeout_seconds=base_config.check_timeout_seconds,
        checks=(),
    )
    result = run_harness(ROOT, task_file, report_file.parent, config=config)
    generated_report = result.output_dir / "run-report.md"
    if generated_report != report_file:
        report_file.write_text(generated_report.read_text(encoding="utf-8"), encoding="utf-8")
    return report_file


def run_eval() -> int:
    result = run_harness(ROOT, DEFAULT_TASK_FILE, ROOT / "output")
    report_text = (result.output_dir / "run-report.md").read_text(encoding="utf-8")
    missing = evaluate_report_text(report_text)
    if missing:
        print("Evaluation failed:")
        for phrase in missing:
            print(f"- missing {phrase}")
        return 1
    print("Evaluation passed: project-ready report checks")
    return 0


def _legacy_main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in {"run", "eval"}:
        return cli_main(sys.argv[1:])

    parser = argparse.ArgumentParser(description="Compatibility wrapper for Agent Harness Lab.")
    parser.add_argument("--task", type=Path, default=DEFAULT_TASK_FILE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_FILE)
    parser.add_argument("--project", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--eval", action="store_true")
    args = parser.parse_args()

    if args.eval:
        return cli_main(["eval", "--project", str(args.project), "--task", str(args.task), *(
            ["--output-dir", str(args.output_dir)] if args.output_dir else []
        )])

    output_dir = args.output_dir or args.report.parent
    return cli_main(["run", "--project", str(args.project), "--task", str(args.task), "--output-dir", str(output_dir)])


if __name__ == "__main__":
    raise SystemExit(_legacy_main())
