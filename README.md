# Agent Harness Lab

A TDD-first Agent Harness prototype for building, evaluating, and showcasing reproducible AI agent workflows.

Agent Harness Lab is a small, runnable Python prototype that demonstrates the foundation of an agent runtime: task input, workspace scanning, material classification, step decomposition, bounded risk reporting, evaluation cases, and Markdown report generation.

It is designed as a truthful GitHub-ready proof package for an AI agent token grant application. It does not claim production users, commercial impact, or external model integration in v1.

## Why This Exists

Many agent demos look impressive but are hard to reproduce. This project starts from the opposite direction: a deterministic harness that can be run, tested, inspected, and extended.

The guiding ideas are:

- Build the smallest useful runtime first.
- Add evaluation before expanding behavior.
- Keep tool and output contracts explicit.
- Record risks and verification evidence.
- Spend future token budget on long-context analysis, tool execution, and multi-step review loops.

## Run

```powershell
python .\agent_workflow.py
```

This generates:

```text
output/run-report.md
```

Run the built-in evaluation cases:

```powershell
python .\agent_workflow.py --eval
```

Use a custom task file:

```powershell
python .\agent_workflow.py --task .\examples\task.md --report .\output\run-report.md
```

## What The Harness Demonstrates

- Reads a Markdown task brief.
- Scans the repository using only the Python standard library.
- Classifies files as documentation, code/page assets, media evidence, or other material.
- Generates a reviewable Markdown report.
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

## Scope Boundaries

- v1 is local and deterministic.
- v1 does not call external LLM APIs.
- v1 is not a deployed commercial agent.
- v1 is a credible foundation for a larger token-intensive agent runtime.
