# Evaluation Strategy

Agent Harness Lab follows a TDD-first path: add evaluation cases before expanding runtime behavior.

## Current Checks

The built-in evaluation command is:

```powershell
python .\agent_workflow.py --eval
```

It verifies that generated report content includes:

- Workspace scan evidence.
- Harness execution steps.
- Bounded claim language.
- Reproducible evidence references.
- Runtime and observability contracts.

## Why This Matters

The project is intended as credible grant evidence. Evaluation prevents the repository from drifting into vague claims or static documentation that cannot be verified.

## Next Cases To Add

- Tool description contract checks.
- Cancellation and checkpoint behavior checks.
- Long-context summarization fixtures.
- Multi-agent review flow fixtures.
- JSONL observability output checks.
