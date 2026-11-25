"""Portable $HOME path normalizer and cloud-safe SQLite backup helper for multi-PC agent configs."""

from __future__ import annotations

import contextlib
import re
import shutil
import sqlite3
import tempfile
from pathlib import Path

EXCLUDED_DIRS = frozenset(
    {
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "scratch",
        "browser_sandbox",
        ".system_generated",
        ".user_uploaded",
    }
)

WIN_USER_RE = re.compile(r'[A-Za-z]:[\\/]Users[\\/][^\\/\s"`]+')
POSIX_USER_RE = re.compile(r'/(?:Users|home)/[^/\s"`]+')


def to_portable_paths(text: str) -> str:
    """Normalize OS-specific user home prefixes to portable `$HOME/...` forward-slash paths."""
    step1 = WIN_USER_RE.sub("$HOME", text)
    step2 = POSIX_USER_RE.sub("$HOME", step1)
    return re.sub(r'\$HOME(?:\\[^\s"`]+)+', lambda m: m.group(0).replace("\\", "/"), step2)


def should_sync_path(rel_path: Path) -> bool:
    return not any(part in EXCLUDED_DIRS for part in rel_path.parts)


def safe_sqlite_backup(src_db: str | Path, dst_db: str | Path) -> Path:
    """Copy a SQLite database via local temp directory first so cloud-mounted drives never raise disk I/O locks."""
    src = Path(src_db)
    dst = Path(dst_db)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        local_src = Path(tmp) / "src.db"
        local_bak = Path(tmp) / "bak.db"
        shutil.copy2(src, local_src)
        with contextlib.closing(sqlite3.connect(local_src)) as conn_in, contextlib.closing(sqlite3.connect(local_bak)) as conn_out:
            conn_in.backup(conn_out)
        shutil.copy2(local_bak, dst)
    return dst
