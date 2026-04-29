from __future__ import annotations

import json
from pathlib import Path


def state_dir(project_root: Path, configured_state_dir: str) -> Path:
    path = Path(configured_state_dir)
    if path.is_absolute():
        return path
    return project_root / path


def checkpoint_path(project_root: Path, configured_state_dir: str) -> Path:
    return state_dir(project_root, configured_state_dir) / "checkpoint.json"


def cancel_path(project_root: Path, configured_state_dir: str, cancel_file: str) -> Path:
    return state_dir(project_root, configured_state_dir) / cancel_file


def is_cancelled(project_root: Path, configured_state_dir: str, cancel_file: str) -> bool:
    return cancel_path(project_root, configured_state_dir, cancel_file).exists()


def write_checkpoint(
    project_root: Path,
    configured_state_dir: str,
    *,
    status: str,
    phase: str,
    message: str,
    generated_at: str,
) -> Path:
    path = checkpoint_path(project_root, configured_state_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": status,
        "phase": phase,
        "message": message,
        "generated_at": generated_at,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
