# Evaluation Strategy

Agent Harness Lab follows a TDD-first path: add evaluation cases before expanding runtime behavior.

## Current Checks

The built-in evaluation command is:

```powershell
python .\agent_workflow.py --eval
```

For another project:

```powershell
python -m agent_harness_lab.cli eval --project D:\path\to\project --task D:\path\to\task.md
```

It verifies that generated report content includes:

- Workspace scan structure.
- Harness execution steps.
- Bounded claim language.
- Reproducible project artifact references.
- Runtime and observability contracts.
- Machine-readable artifacts for CI or follow-up automation.
- Configured project check results and their exit codes.

## Why This Matters

The project is intended as a practical development harness. Evaluation prevents the repository from drifting into vague claims or static documentation that cannot be verified.

## Next Cases To Add

- Tool description contract checks.
- Cancellation and checkpoint behavior checks.
- Long-context summarization fixtures.
- Multi-agent review flow fixtures.
- JSONL observability output checks.
