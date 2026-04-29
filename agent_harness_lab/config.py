from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from agent_harness_lab.checks import CheckSpec


DEFAULT_IGNORE_DIRS = (
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
)


@dataclass(frozen=True)
class HarnessConfig:
    project_name: str
    output_dir: str = "output"
    ignore_dirs: tuple[str, ...] = field(default_factory=lambda: DEFAULT_IGNORE_DIRS)
    max_artifact_files: int = 12
    check_timeout_seconds: int = 60
    checks: tuple[CheckSpec, ...] = ()


def _coerce_value(value: str) -> str | int:
    stripped = value.strip().strip("\"'")
    if stripped.isdigit():
        return int(stripped)
    return stripped


def _read_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    current_mapping: dict[str, object] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        if stripped.startswith("- ") and current_list_key:
            values = data.setdefault(current_list_key, [])
            if isinstance(values, list):
                item = stripped[2:].strip()
                if ":" in item:
                    key, value = item.split(":", 1)
                    current_mapping = {key.strip(): _coerce_value(value)}
                    values.append(current_mapping)
                else:
                    values.append(str(_coerce_value(item)))
                    current_mapping = None
            continue

        if current_mapping is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current_mapping[key.strip()] = _coerce_value(value)
            continue

        current_list_key = None
        current_mapping = None
        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = _coerce_value(value)
        else:
            data[key] = []
            current_list_key = key

    return data


def load_config(project_root: Path) -> HarnessConfig:
    project_root = project_root.resolve()
    config_path = project_root / "harness.yaml"
    raw = _read_simple_yaml(config_path) if config_path.exists() else {}

    ignore_dirs = raw.get("ignore_dirs", DEFAULT_IGNORE_DIRS)
    if isinstance(ignore_dirs, list):
        merged_ignore_dirs = tuple(dict.fromkeys([*DEFAULT_IGNORE_DIRS, *map(str, ignore_dirs)]))
    else:
        merged_ignore_dirs = DEFAULT_IGNORE_DIRS

    project_name = raw.get("project_name", project_root.name)
    output_dir = raw.get("output_dir", "output")
    max_artifact_files = raw.get("max_artifact_files", 12)
    check_timeout_seconds = raw.get("check_timeout_seconds", 60)
    checks = []
    raw_checks = raw.get("checks", [])
    if isinstance(raw_checks, list):
        for item in raw_checks:
            if isinstance(item, dict) and item.get("name") and item.get("command"):
                checks.append(CheckSpec(name=str(item["name"]), command=str(item["command"])))

    return HarnessConfig(
        project_name=str(project_name),
        output_dir=str(output_dir),
        ignore_dirs=merged_ignore_dirs,
        max_artifact_files=int(max_artifact_files),
        check_timeout_seconds=int(check_timeout_seconds),
        checks=tuple(checks),
    )
