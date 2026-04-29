# Runtime Contract

Agent Harness Lab uses a deliberately small runtime contract so the repository stays easy to inspect and extend.

## Modules

- `engine`: Loads the task, scans the workspace, builds harness steps, and writes artifacts.
- `tools`: Provides deterministic filesystem inspection and file classification.
- `storage`: Uses Markdown task briefs plus Markdown, JSON, and JSONL run artifacts.
- `types`: Defines small dataclasses for file summaries and evaluation cases.
- `evaluation`: Runs repeatable pass/fail checks against generated report content.

## Protocol Guarantees

- Inputs are explicit Markdown task files.
- Outputs are Markdown reports, JSON run summaries, and JSONL event streams.
- The harness does not mutate source files during normal report generation.
- Claims in generated reports are bounded to what this repository can prove.
- Future LLM or tool integrations should keep this contract visible in generated artifacts.

## Planned Extensions

- Tool registry with explicit field contracts.
- Session checkpoints and cancellation state.
- Provider abstraction for LLM calls.
- Structured observability events persisted as JSONL.
- Evaluation fixtures with expected tool sequences and final-state checks.
