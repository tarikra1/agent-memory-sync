import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import contextlib
import sqlite3
import tempfile
import unittest

from agent_memory_sync.core import safe_sqlite_backup, should_sync_path, to_portable_paths


class TestAgentMemorySync(unittest.TestCase):
    def test_portable_path_normalization(self) -> None:
        raw = "Read skills from D:\\Users\\alice\\.claude\\skills\\demo and /home/bob/.config/rules.md"
        norm = to_portable_paths(raw)
        self.assertIn("$HOME/.claude/skills/demo", norm)
        self.assertIn("$HOME/.config/rules.md", norm)
        self.assertNotIn("alice", norm)
        self.assertNotIn("bob", norm)

    def test_should_sync_path_excludes_transient_dirs(self) -> None:
        self.assertTrue(should_sync_path(Path("rules/AGENTS.md")))
        self.assertFalse(should_sync_path(Path("brain/abc/scratch/temp.py")))
        self.assertFalse(should_sync_path(Path("project/.venv/pyvenv.cfg")))

    def test_safe_sqlite_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "state.db"
            dst = Path(tmp) / "out" / "state_backup.db"
            with contextlib.closing(sqlite3.connect(src)) as conn:
                conn.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, body TEXT)")
                conn.execute("INSERT INTO notes (body) VALUES ('synced')")
                conn.commit()
            safe_sqlite_backup(src, dst)
            with contextlib.closing(sqlite3.connect(dst)) as conn2:
                rows = conn2.execute("SELECT body FROM notes").fetchall()
                self.assertEqual(rows, [("synced",)])


if __name__ == "__main__":
    unittest.main()
