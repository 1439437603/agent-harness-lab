from __future__ import annotations

import argparse
from pathlib import Path

from agent_harness_lab.engine import evaluate_report_text, run_harness


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-harness", description="Run Agent Harness Lab.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run the harness on a project.")
    run_parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root to scan.")
    run_parser.add_argument("--task", type=Path, required=True, help="Markdown task file.")
    run_parser.add_argument("--output-dir", type=Path, default=None, help="Override output directory.")

    eval_parser = subparsers.add_parser("eval", help="Run the harness and evaluate the generated report.")
    eval_parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root to scan.")
    eval_parser.add_argument("--task", type=Path, required=True, help="Markdown task file.")
    eval_parser.add_argument("--output-dir", type=Path, default=None, help="Override output directory.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"run", "eval"}:
        result = run_harness(args.project, args.task, args.output_dir)
        report_path = result.output_dir / "run-report.md"
        print(f"Generated report: {report_path}")
        print(f"Generated JSON: {result.output_dir / 'run-result.json'}")
        print(f"Generated events: {result.output_dir / 'events.jsonl'}")
        print(f"Scanned files: {len(result.files)}")

        if args.command == "eval":
            missing = evaluate_report_text(report_path.read_text(encoding="utf-8"))
            if missing:
                print("Evaluation failed:")
                for phrase in missing:
                    print(f"- missing {phrase}")
                return 1
            print("Evaluation passed: project-ready report checks")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
