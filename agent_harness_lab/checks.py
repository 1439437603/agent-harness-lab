from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex
import subprocess


@dataclass(frozen=True)
class CheckSpec:
    name: str
    command: str


@dataclass(frozen=True)
class CheckResult:
    name: str
    command: str
    exit_code: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


def _limit_output(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]"


def run_check(project_root: Path, spec: CheckSpec, timeout_seconds: int) -> CheckResult:
    try:
        args = shlex.split(spec.command)
        completed = subprocess.run(
            args,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return CheckResult(
            name=spec.name,
            command=spec.command,
            exit_code=completed.returncode,
            stdout=_limit_output(completed.stdout),
            stderr=_limit_output(completed.stderr),
        )
    except subprocess.TimeoutExpired as error:
        return CheckResult(
            name=spec.name,
            command=spec.command,
            exit_code=124,
            stdout=_limit_output(error.stdout or ""),
            stderr=f"Timed out after {timeout_seconds} seconds.",
        )
    except OSError as error:
        return CheckResult(
            name=spec.name,
            command=spec.command,
            exit_code=127,
            stdout="",
            stderr=str(error),
        )


def run_checks(project_root: Path, specs: tuple[CheckSpec, ...], timeout_seconds: int) -> list[CheckResult]:
    return [run_check(project_root, spec, timeout_seconds) for spec in specs]
