# Agent Harness Lab

[中文说明](README.zh-CN.md)

A project-ready, TDD-first Agent Harness for scanning local codebases, producing reproducible agent workflow reports, and validating outputs with lightweight evaluation checks.

Agent Harness Lab is a small, runnable Python harness that can be used against real local projects. It provides task input, workspace scanning, material classification, runtime-contract reporting, observability events, Markdown/JSON/JSONL artifacts, configured project checks, and lightweight evaluation checks.

It is designed as a practical project harness for development teams that want agent workflows to be inspectable, testable, and repeatable before connecting more advanced automation.

## Why This Exists

Many agent demos look impressive but are hard to reproduce. This project starts from the opposite direction: a deterministic harness that can be run, tested, inspected, evaluated, and extended.

The guiding ideas are:

- Build the smallest useful runtime first.
- Add evaluation before expanding behavior.
- Keep tool and output contracts explicit.
- Record risks, check results, and operational artifacts.
- Keep agent workflow runs reproducible before adding deeper automation.

## Run In This Repository

```powershell
python .\agent_workflow.py
```

This generates:

```text
output/run-report.md
output/run-result.json
output/events.jsonl
```

Run the built-in evaluation cases:

```powershell
python .\agent_workflow.py --eval
```

Use a custom task file:

```powershell
python .\agent_workflow.py --task .\examples\task.md --report .\output\run-report.md
```

## Run Against Another Project

Use the module CLI directly:

```powershell
python -m agent_harness_lab.cli run --project D:\path\to\project --task D:\path\to\task.md
```

Evaluate the generated report:

```powershell
python -m agent_harness_lab.cli eval --project D:\path\to\project --task D:\path\to\task.md
```

The compatibility wrapper also accepts the same subcommands:

```powershell
python .\agent_workflow.py run --project . --task .\examples\task.md
```

## Configure A Project

Add `harness.yaml` to the project root:

```yaml
project_name: My Service
output_dir: harness-results
max_artifact_files: 12
check_timeout_seconds: 60
state_dir: .agent-harness
cancel_file: cancel
ignore_dirs:
  - node_modules
  - dist
  - tmp
checks:
  - name: unit-tests
    command: python -m unittest discover -s tests -v
```

The harness reads this file before scanning and writes artifacts to `output_dir`.
Configured checks run from the target project root. Results are included in `run-report.md`, `run-result.json`, and `events.jsonl`.

## Runtime State And Cancellation

Every run writes a checkpoint:

```text
.agent-harness/checkpoint.json
```

To request cancellation before the check phase, create the configured cancel file:

```powershell
New-Item .\.agent-harness\cancel -ItemType File
```

When the cancel file exists, the harness marks the run as `cancelled`, skips configured checks, writes the final artifacts, and records `cancellation.detected` in `events.jsonl`.

## What The Harness Demonstrates

- Reads a Markdown task brief.
- Scans any local project path using only the Python standard library.
- Classifies files as documentation, code/page assets, media, config/data, or other material.
- Prints a clear runtime contract for engine, tools, storage, types, and evaluation.
- Lists observability events that mark decision points in the workflow.
- Generates reviewable Markdown plus machine-readable JSON and JSONL artifacts.
- Runs configured project checks such as tests, lint, or build commands.
- Writes checkpoint state and respects a cancel signal before running checks.
- Includes a small evaluation mode with pass/fail checks.
- Keeps claims bounded to what the repository can prove.

## TDD / Agent Harness Shape

The current prototype maps to a practical Agent Harness structure:

- `engine`: task reading, workspace scan, step decomposition, report generation.
- `tools`: deterministic filesystem inspection through standard-library functions.
- `storage`: Markdown files under `examples/` and `output/`.
- `types`: dataclasses for file summaries and evaluation cases.
- `evaluation`: built-in checks run with `--eval`.

Future versions can add a real tool registry, LLM provider abstraction, richer checkpoint resume semantics, and deeper observability.

The design details are documented in [`docs/runtime-contract.md`](docs/runtime-contract.md) and [`docs/evaluation-strategy.md`](docs/evaluation-strategy.md).

## Professional Scope Boundaries

- v1 is local and deterministic.
- v1 does not call external LLM APIs.
- v1 does not modify project source code.
- v1 focuses on scanning, configured checks, reporting, event logs, and lightweight evaluation.
- v1 is a foundation for a larger agent runtime with tool execution, checkpoints, cancellation, and LLM-backed analysis.
