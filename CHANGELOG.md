# Changelog

All notable changes to `faf-memory-mcp` are documented here.

## Unreleased

- `etch` now writes `$FAF_SOUL_PATH` immediately so facts survive process exit.
- README plugin install matches live `faf-memory@claude-community`.

## [0.1.0] — 2026-05-26 — Initial release

- Wraps [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/) `>= 0.3.0` via `fastmcp >= 2.0`.
- **5 MCP tools** — `etch`, `recall`, `list_facts`, `save_soul`, `load_soul`.
- Soul namepoint / profile / path configurable via env vars (`FAF_SOUL_NAMEPOINT`, `FAF_SOUL_PROFILE`, `FAF_SOUL_PATH`).
- Lazy-load — if the configured path exists, the server boots into that soul; otherwise a fresh one.
- `.fafm` v1.1 round-trip — cross-vendor compatible with [`grok-faf-voice`](https://pypi.org/project/grok-faf-voice/) (both directions tested upstream).
