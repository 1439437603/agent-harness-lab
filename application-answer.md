# Grant Application Copy

## 04 - Work Built With Agents Or AI-Driven Workflows

I am building Agent Harness Lab, a project-ready TDD-first Agent Harness for turning local project material into reproducible agent workflow evidence. The current version can run against a target project path, read `harness.yaml`, scan project files, classify documentation/code/config evidence, emit a runtime contract, list observability events, and generate Markdown, JSON, and JSONL artifacts with risks, verification points, and the highest-ROI next action.

The project is intentionally small but usable. It demonstrates the foundation of an agent harness rather than claiming production traffic: task input, project configuration, workspace scan, material classification, runtime boundaries, report generation, machine-readable run output, JSONL observability events, and built-in evaluation cases. I currently use Codex and GPT-series models for requirement breakdown, code understanding, documentation cleanup, and verification planning.

If I receive a higher Token Plan or credit grant, I will extend this reference implementation into a stronger personal research and development agent harness: longer-context codebase analysis, richer tool registry behavior, automated test execution, session checkpoints, cancellation-safe runs, multi-agent review flows, PR and documentation generation, and more evaluation cases. Those use cases are token-intensive because they require repeated long-context reads, tool-result summarization, verification loops, and multi-step planning.

## 05 - Proof Of Usage And Impact

Recommended proof materials:

1. GitHub repository link for `agent-harness-lab`.
2. Terminal screenshot showing `python .\agent_workflow.py`.
3. Generated report screenshot from `output/run-report.md`.
4. Evaluation screenshot showing `python .\agent_workflow.py --eval`.
5. README screenshot showing the project goal, command, and scope boundaries.

If the form accepts only one proof field, use the GitHub repository link first.
