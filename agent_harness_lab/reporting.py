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

    lines.extend(["", "## Evidence Files", ""])
    for item in result.evidence_files:
        lines.append(f"- `{item.path}` ({item.category}, {item.size} bytes)")

    lines.extend(["", "## Runtime Contract", ""])
    for name, description in result.runtime_modules.items():
        lines.append(f"- `{name}`: {description}")

    lines.extend(["", "## Observability Events", ""])
    for event in result.observability_events:
        lines.append(f"- `{event}`")

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
        "project_name": result.project_name,
        "project_root": str(result.project_root),
        "task_file": str(result.task_file),
        "category_counts": result.category_counts,
        "evidence_files": [
            {"path": str(item.path), "size": item.size, "category": item.category}
            for item in result.evidence_files
        ],
        "runtime_modules": result.runtime_modules,
        "observability_events": list(result.observability_events),
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
