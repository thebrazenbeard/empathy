"""Editor startup safety checks. Do not execute workspace tasks or font assets."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkspaceStartupSafetyTests(unittest.TestCase):
    def test_no_hidden_folder_open_execution(self):
        tasks = (ROOT / ".vscode/tasks.json").read_text(encoding="utf-8")
        self.assertNotRegex(tasks, r'"runOn"\s*:\s*"folderOpen"')
        self.assertNotRegex(tasks, r"\bnode\s+[^\n]*public/fonts/")

    def test_no_ineffective_workspace_automatic_task_setting(self):
        settings = json.loads((ROOT / ".vscode/settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("task.allowAutomaticTasks", settings)
        self.assertNotIn("tasks", settings)

    def test_disguised_asset_is_not_tracked_as_font(self):
        self.assertFalse((ROOT / "public/fonts/fa-solid.lkf").exists())

    def test_editor_tasks_file_is_valid_json(self):
        tasks = json.loads((ROOT / ".vscode/tasks.json").read_text(encoding="utf-8"))
        self.assertEqual(tasks.get("tasks"), [])


if __name__ == "__main__":
    unittest.main()
