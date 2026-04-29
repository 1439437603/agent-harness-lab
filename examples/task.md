# Example Task

I want an agent harness that can turn a local workspace into a repeatable project readiness report for agent-assisted development.

## Expected Output

- Summarize the current project material.
- Scan the workspace and identify useful project artifacts.
- Break the work into concrete agent runtime steps.
- Generate a bounded, truthful result summary.
- List risks and the highest-ROI next step.

## Constraints

- Do not call external LLM APIs in v1.
- Keep the workflow runnable with the Python standard library.
