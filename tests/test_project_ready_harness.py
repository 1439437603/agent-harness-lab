from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from agent_harness_lab.config import load_config
from agent_harness_lab.engine import run_harness


class ProjectReadyHarnessTests(unittest.TestCase):
    def test_load_config_reads_project_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harness.yaml").write_text(
                "\n".join(
                    [
                        "project_name: Example Service",
                        "output_dir: .harness-output",
                        "max_evidence_files: 3",
                        "ignore_dirs:",
                        "  - node_modules",
                        "  - tmp",
                        "checks:",
                        "  - name: unit",
                        "    command: python check_ok.py",
                    ]
                ),
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(config.project_name, "Example Service")
            self.assertEqual(config.output_dir, ".harness-output")
            self.assertEqual(config.max_evidence_files, 3)
            self.assertIn("node_modules", config.ignore_dirs)
            self.assertIn("tmp", config.ignore_dirs)
            self.assertEqual(config.checks[0].name, "unit")
            self.assertEqual(config.checks[0].command, "python check_ok.py")

    def test_run_harness_writes_markdown_json_and_events_for_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harness.yaml").write_text(
                "project_name: Checkout API\noutput_dir: harness-results\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text("# Checkout API\n", encoding="utf-8")
            (root / "service.py").write_text("print('checkout')\n", encoding="utf-8")
            task_file = root / "task.md"
            task_file.write_text("Assess this project for agent readiness.", encoding="utf-8")

            result = run_harness(project_root=root, task_file=task_file)

            output_dir = root / "harness-results"
            self.assertTrue((output_dir / "run-report.md").exists())
            self.assertTrue((output_dir / "run-result.json").exists())
            self.assertTrue((output_dir / "events.jsonl").exists())
            self.assertEqual(result.project_name, "Checkout API")

            payload = json.loads((output_dir / "run-result.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["project_name"], "Checkout API")
            self.assertEqual(payload["project_root"], str(root.resolve()))
            self.assertIn("category_counts", payload)
            self.assertGreaterEqual(payload["category_counts"]["documentation"], 1)

            events = [
                json.loads(line)
                for line in (output_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(events[0]["event"], "task.loaded")
            self.assertEqual(events[-1]["event"], "evaluation.checked")

    def test_run_harness_executes_configured_project_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harness.yaml").write_text(
                "\n".join(
                    [
                        "project_name: Checked Project",
                        "output_dir: harness-results",
                        "checks:",
                        "  - name: smoke",
                        "    command: python check_ok.py",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "check_ok.py").write_text("print('smoke-ok')\n", encoding="utf-8")
            task_file = root / "task.md"
            task_file.write_text("Run configured checks.", encoding="utf-8")

            result = run_harness(project_root=root, task_file=task_file)

            self.assertEqual(len(result.check_results), 1)
            self.assertTrue(result.check_results[0].passed)
            self.assertIn("smoke-ok", result.check_results[0].stdout)

            output_dir = root / "harness-results"
            report = (output_dir / "run-report.md").read_text(encoding="utf-8")
            self.assertIn("## Project Checks", report)
            self.assertIn("smoke", report)

            payload = json.loads((output_dir / "run-result.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["checks"][0]["name"], "smoke")
            self.assertEqual(payload["checks"][0]["exit_code"], 0)

            events = [
                json.loads(line)
                for line in (output_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertIn("checks.completed", [event["event"] for event in events])
