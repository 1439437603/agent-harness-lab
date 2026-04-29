# Agent Harness Lab

[中文说明](README.zh-CN.md)

A project-ready, TDD-first Agent Harness for scanning local codebases, producing reproducible agent workflow reports, and validating outputs with lightweight evaluation checks.

Agent Harness Lab is a small, runnable Python harness that can be used against real local projects. It provides task input, workspace scanning, material classification, runtime-contract reporting, observability events, Markdown/JSON/JSONL artifacts, and lightweight evaluation checks.

It is designed as truthful GitHub-ready evidence for an AI agent token grant application. It does not claim production users, commercial impact, or external model integration in v1.

## Why This Exists

Many agent demos look impressive but are hard to reproduce. This project starts from the opposite direction: a deterministic harness that can be run, tested, inspected, evaluated, and extended.

The guiding ideas are:

- Build the smallest useful runtime first.
- Add evaluation before expanding behavior.
- Keep tool and output contracts explicit.
- Record risks and verification evidence.
- Spend future token budget on long-context analysis, tool execution, and multi-step review loops.

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
max_evidence_files: 12
check_timeout_seconds: 60
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

## What The Harness Demonstrates

- Reads a Markdown task brief.
- Scans any local project path using only the Python standard library.
- Classifies files as documentation, code/page assets, media evidence, or other material.
- Prints a clear runtime contract for engine, tools, storage, types, and evaluation.
- Lists observability events that mark decision points in the workflow.
- Generates reviewable Markdown plus machine-readable JSON and JSONL artifacts.
- Runs configured project checks such as tests, lint, or build commands.
- Includes a small evaluation mode with pass/fail checks.
- Keeps claims bounded to what the repository can prove.

## TDD / Agent Harness Shape

The current prototype maps to a practical Agent Harness structure:

- `engine`: task reading, workspace scan, step decomposition, report generation.
- `tools`: deterministic filesystem inspection through standard-library functions.
- `storage`: Markdown files under `examples/` and `output/`.
- `types`: dataclasses for file summaries and evaluation cases.
- `evaluation`: built-in checks run with `--eval`.

Future versions can add a real tool registry, LLM provider abstraction, session checkpoints, cancellation, and richer observability.

The design details are documented in [`docs/runtime-contract.md`](docs/runtime-contract.md) and [`docs/evaluation-strategy.md`](docs/evaluation-strategy.md).

## Grant Application Copy

For form item 04, use the stronger copy in [`application-answer.md`](application-answer.md).

For form item 05, use this repository link first:

```text
https://github.com/1439437603/agent-harness-lab
```

If uploads are supported, also attach:

- Terminal screenshot of `python .\agent_workflow.py`.
- Generated report screenshot from `output/run-report.md`.
- Evaluation screenshot of `python .\agent_workflow.py --eval`.

## Professional Scope Boundaries

- v1 is local and deterministic.
- v1 does not call external LLM APIs.
- v1 is not a deployed commercial agent.
- v1 is a credible foundation for a larger token-intensive agent runtime.
