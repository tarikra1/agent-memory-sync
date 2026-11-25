# agent-memory-sync

[![CI](https://github.com/tarikra1/agent-memory-sync/actions/workflows/ci.yml/badge.svg)](https://github.com/tarikra1/agent-memory-sync/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/release-v1.0.0-0EA5E9.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Cross-PC `CLAUDE.md` / `AGENTS.md` path normalizer and cloud-drive-safe SQLite snapshot utility for developers working across multiple workstations.**

## Quickstart

```bash
pip install -e .
agent-sync normalize AGENTS.md --in-place
agent-sync backup-db ./state.db ./synced/state.db
```

## License

MIT License — see [LICENSE](LICENSE).
