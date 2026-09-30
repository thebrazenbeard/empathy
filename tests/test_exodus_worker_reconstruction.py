from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TestEmpathyExodus(unittest.TestCase):
    def test_worker_contract(self):
        text = (ROOT / "docs" / "WORKER_RECONSTRUCTION_V1.md").read_text(encoding="utf-8")
        self.assertIn("NO_PERMANENT_CHAT_DEPENDENCY", text)
        self.assertIn("bus/yin-v2", text)
        self.assertIn("bus/yang-v2", text)
        self.assertNotIn("chatgpt.com", text.lower())

    def test_checkpoint(self):
        text = (ROOT / "docs" / "EXODUS_CHECKPOINT_20260919.md").read_text(encoding="utf-8")
        self.assertIn("STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT", text)
        self.assertIn("sequence 4168", text)
        self.assertIn("not a current assignment", text.lower())

if __name__ == "__main__":
    unittest.main()
