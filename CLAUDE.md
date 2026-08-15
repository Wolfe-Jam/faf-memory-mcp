<!-- faf:start -->
<!-- faf: faf-memory-mcp | Python | mcp-server | MCP door for the .fafm file — etch persists to disk so any MCP host gets offline-first Permanent Memory without a hosted store -->
<!-- faf: claim=project.faf | family=FAF -->

# CLAUDE.md — faf-memory-mcp

## What This Is

MCP door for the .fafm file — etch persists to disk so any MCP host gets offline-first Permanent Memory without a hosted store

## Stack

- **Language:** Python
- **Backend:** FastMCP
- **API:** MCP (stdio)
- **Runtime:** Python 3.11+
- **Connection:** stdio
- **Hosting:** PyPI
- **Build:** hatchling
- **CI/CD:** GitHub Actions
- **Package Manager:** uv
- **Storage:** .fafm file on disk

## Context

- **Who:** MCP hosts (Claude Code via faf-memory plugin, Cursor, Grok, any stdio host) that need local .fafm
- **What:** Five-tool MCP adapter over claude-fafm-sdk — etch, recall, list_facts, save_soul, load_soul
- **Why:** Agents forget across sessions; the store should be a file you can diff, not a hosted lock-in
- **Where:** PyPI faf-memory-mcp · GitHub Wolfe-Jam/faf-memory-mcp · memory.faf.one
- **When:** v0.1.1 — 2026-08-15 — etch persists to $FAF_SOUL_PATH
- **How:** uvx faf-memory-mcp

---

*STATUS: BI-SYNC ACTIVE — 2026-08-15T20:03:24.597Z*
<!-- faf:end -->
