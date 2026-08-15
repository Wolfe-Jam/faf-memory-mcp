# Changelog

All notable changes to `faf-memory-mcp` are documented here.

## [Unreleased]

- Hosts-pull: Cursor · Grok · any host share one `mcpServers` JSON. Claude plugin unchanged.

## [0.1.1] — 2026-08-15

etch writes the file so memory survives the process. Plugin install matches live `faf-memory@claude-community`.

- `etch` writes `$FAF_SOUL_PATH` immediately so facts survive process exit.
- README plugin install is `faf-memory@claude-community` (no longer “coming soon”).
- This server is the local `.fafm` file. FAFA `etch_memory` / `recall_memory` is the hosted namepoint path.

## [0.1.0] — 2026-05-26 — Initial release

- Wraps [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/) `>= 0.3.0` via `fastmcp >= 2.0`.
- **5 MCP tools** — `etch`, `recall`, `list_facts`, `save_soul`, `load_soul`.
- Soul namepoint / profile / path configurable via env vars (`FAF_SOUL_NAMEPOINT`, `FAF_SOUL_PROFILE`, `FAF_SOUL_PATH`).
- Lazy-load — if the configured path exists, the server boots into that soul; otherwise a fresh one.
- `.fafm` v1.1 round-trip — cross-vendor compatible with [`grok-faf-voice`](https://pypi.org/project/grok-faf-voice/) (both directions tested upstream).
