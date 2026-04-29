from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_harness_lab.engine import HarnessResult, RuntimeEvent


def build_markdown_report(result: "HarnessResult") -> str:
    lines = [
        "# Agent Harness Lab Run Report",
        "",
        f"- Run time: {result.generated_at}",
        f"- Status: {result.status}",
        f"- Status message: {result.status_message}",
        f"- Project: {result.project_name}",
        f"- Project root: `{result.project_root}`",
        "",
        "## Input Task",
        "",
        result.task,
        "",
        "## Workspace Scan",
        "",
    ]

    for category in sorted(result.category_counts):
        lines.append(f"- {category}: {result.category_counts[category]} files")

    lines.extend(["", "## Project Artifacts", ""])
    for item in result.artifact_files:
        lines.append(f"- `{item.path}` ({item.category}, {item.size} bytes)")

    lines.extend(["", "## Runtime Contract", ""])
    for name, description in result.runtime_modules.items():
        lines.append(f"- `{name}`: {description}")

    lines.extend(["", "## Observability Events", ""])
    for event in result.observability_events:
        lines.append(f"- `{event}`")

    lines.extend(["", "## Project Checks", ""])
    if result.check_results:
        for check in result.check_results:
            status = "PASS" if check.passed else "FAIL"
            lines.append(f"- {status} `{check.name}`: `{check.command}` (exit {check.exit_code})")
            if check.stdout.strip():
                lines.append(f"  - stdout: {check.stdout.strip().splitlines()[0]}")
            if check.stderr.strip():
                lines.append(f"  - stderr: {check.stderr.strip().splitlines()[0]}")
    else:
        lines.append("- No project checks configured.")

    lines.extend(["", "## Harness Steps", ""])
    for index, step in enumerate(result.steps, start=1):
        lines.append(f"{index}. {step}")

    lines.extend(["", "## Result Summary", "", result.summary, "", "## Risks", ""])
    lines.extend(f"- {risk}" for risk in result.risks)
    lines.extend(["", "## Highest-ROI Next Step", "", result.next_step, ""])
    return "\n".join(lines)


def result_to_json(result: "HarnessResult") -> dict[str, object]:
    return {
        "generated_at": result.generated_at,
        "status": result.status,
        "status_message": result.status_message,
        "project_name": result.project_name,
        "project_root": str(result.project_root),
        "task_file": str(result.task_file),
        "category_counts": result.category_counts,
        "artifact_files": [
            {"path": str(item.path), "size": item.size, "category": item.category}
            for item in result.artifact_files
        ],
        "runtime_modules": result.runtime_modules,
        "observability_events": list(result.observability_events),
        "checks": [
            {
                "name": check.name,
                "command": check.command,
                "exit_code": check.exit_code,
                "passed": check.passed,
                "stdout": check.stdout,
                "stderr": check.stderr,
            }
            for check in result.check_results
        ],
        "steps": result.steps,
        "risks": result.risks,
        "next_step": result.next_step,
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_events_jsonl(path: Path, events: list["RuntimeEvent"]) -> None:
    rows = []
    for event in events:
        row = asdict(event)
        row["timestamp"] = event.timestamp or datetime.now().isoformat(timespec="seconds")
        rows.append(json.dumps(row, ensure_ascii=False))
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
