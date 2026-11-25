"""CLI for agent-memory-sync."""

from __future__ import annotations

import argparse
from pathlib import Path

from .core import safe_sqlite_backup, to_portable_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-sync", description="Normalize agent memory files for multi-PC sync.")
    sub = parser.add_subparsers(dest="command", required=True)

    norm = sub.add_parser("normalize", help="Replace OS-specific home paths with portable $HOME paths.")
    norm.add_argument("file", help="Target Markdown/JSON file.")
    norm.add_argument("--in-place", action="store_true", help="Write normalized text back to file.")

    bak = sub.add_parser("backup-db", help="Safely snapshot a SQLite DB through local temp storage.")
    bak.add_argument("src_db")
    bak.add_argument("dst_db")

    args = parser.parse_args(argv)
    if args.command == "normalize":
        p = Path(args.file)
        cleaned = to_portable_paths(p.read_text(encoding="utf-8"))
        if args.in_place:
            p.write_text(cleaned, encoding="utf-8", newline="\n")
        else:
            print(cleaned, end="")
        return 0

    out = safe_sqlite_backup(args.src_db, args.dst_db)
    print(f"Backed up SQLite DB to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
