# Changelog

All notable changes to `agent-memory-sync` are documented in this file.

## [1.0.0] - 2026-11-25

### Added
- Portable `$HOME` path normalizer converting Windows and POSIX user home paths cleanly.
- Transient cache filter excluding `.venv`, `__pycache__`, `scratch`, `browser_sandbox`, and `.system_generated`.
- Cloud-drive-safe SQLite snapshot helper (`safe_sqlite_backup`), CLI (`agent-sync`), and GitHub Actions CI matrix.
