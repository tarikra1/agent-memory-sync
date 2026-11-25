# Contributing to agent-memory-sync

1. Fork and clone the repository.
2. Ensure SQLite connections are closed explicitly via `contextlib.closing(...)` so temporary directories clean up cleanly on Windows.
3. Run `python -m unittest discover -s tests -v` before submitting a pull request.
