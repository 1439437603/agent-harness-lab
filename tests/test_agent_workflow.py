from pathlib import Path
import tempfile
import unittest

import agent_workflow


class AgentWorkflowTests(unittest.TestCase):
    def test_classify_file(self) -> None:
        self.assertEqual(agent_workflow.classify_file(Path("README.md")), "documentation")
        self.assertEqual(agent_workflow.classify_file(Path("agent_workflow.py")), "code-or-page")
        self.assertEqual(agent_workflow.classify_file(Path("screen.png")), "media-evidence")
        self.assertEqual(agent_workflow.classify_file(Path("archive.zip")), "other")

    def test_build_report_contains_required_sections(self) -> None:
        files = [
            agent_workflow.FileSummary(Path("README.md"), 100, "documentation"),
            agent_workflow.FileSummary(Path("agent_workflow.py"), 200, "code-or-page"),
        ]
        report = agent_workflow.build_report("Build a harness.", files)

        self.assertIn("# Agent Harness Lab Run Report", report)
        self.assertIn("## Workspace Scan", report)
        self.assertIn("## Runtime Contract", report)
        self.assertIn("## Observability Events", report)
        self.assertIn("## Harness Steps", report)
        self.assertIn("## Risks", report)
        self.assertIn("Highest-ROI Next Step", report)

    def test_write_report_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_file = Path(tmp) / "task.md"
            report_file = Path(tmp) / "report.md"
            task_file.write_text("Build a reproducible agent harness.", encoding="utf-8")

            result = agent_workflow.write_report(task_file, report_file)

            self.assertEqual(result, report_file)
            self.assertTrue(report_file.exists())
            self.assertIn("Build a reproducible agent harness.", report_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
