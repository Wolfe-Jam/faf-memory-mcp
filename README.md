# faf-memory-mcp

**MCP server for `.fafm` — the Permanent Memory Layer (PML) for Claude Code, Cursor, Grok, and any MCP host.**

Cross-vendor persistent memory in a file you can read. Offline-first. Your soul, your bytes.

Wraps [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/) via [`fastmcp`](https://pypi.org/project/fastmcp/). Receipt: **400+× faster type-filter queries vs `grep`** on a real 492-file AI memory corpus — falsifiable methodology at [`Wolfe-Jam/faf-memory-proof`](https://github.com/Wolfe-Jam/faf-memory-proof).

[![PyPI](https://img.shields.io/pypi/v/faf-memory-mcp)](https://pypi.org/project/faf-memory-mcp/)
[![CI](https://github.com/Wolfe-Jam/faf-memory-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Wolfe-Jam/faf-memory-mcp/actions/workflows/ci.yml)
[![IANA](https://img.shields.io/badge/IANA-application%2Fvnd.fafm%2Byaml-FF6B35)](https://www.iana.org/assignments/media-types/application/vnd.fafm+yaml)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20348942-00D4D4)](https://doi.org/10.5281/zenodo.20348942)
[![DOI: Agents paper](https://img.shields.io/badge/DOI-Agents%20paper-FF6B35)](https://doi.org/10.5281/zenodo.21951641)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Why

Every AI session, your agent starts blank — no memory of what you decided yesterday, what worked, what was tried. The fix isn't another hosted memory service; it's a **file** the AI reads at session start and writes back to as it learns. That file is `.fafm` — IANA-registered, cross-vendor, and 996 KB / 49 ms cold-load for a 492-fact corpus (full numbers: [the receipt](https://github.com/Wolfe-Jam/faf-memory-proof)).

## Install

```bash
uvx faf-memory-mcp
```

## Use in Claude Code (recommended)

Via the [`faf-memory`](https://github.com/Wolfe-Jam/faf-memory) plugin (coming to `claude-plugins-community`):

```bash
/plugin install faf-memory
```

Or wire `.mcp.json` directly:

```json
{
  "faf-memory": {
    "command": "uvx",
    "args": ["faf-memory-mcp"]
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `etch(text, id?, type?, priority?, tags?)` | Write a durable fact. O(1) dedup by `id`. |
| `recall(query?, type?, tags?, min_priority?, limit?)` | Filter (substring + type + tags + priority floor) → rank by priority then recency. |
| `list_facts()` | List ALL facts — no filter, no rank. |
| `save_soul(path?)` | Persist the soul to a `.fafm` file. |
| `load_soul(path?)` | Load a `.fafm` from disk, replacing the in-memory soul. |

## Configuration

| Env var | Default | What |
|---|---|---|
| `FAF_SOUL_NAMEPOINT` | `@local` | Initial soul identifier |
| `FAF_SOUL_PROFILE` | `knowledge` | `.fafm` profile (`knowledge` or `voice`) |
| `FAF_SOUL_PATH` | `soul.fafm` | Default save/load path |

## Format

`.fafm` is **IANA-registered** as `application/vnd.fafm+yaml` (registered 2026-05-13). Sibling of `.faf` (`application/vnd.faf+yaml`, 2025-10-30).

- Spec: [`Wolfe-Jam/faf` · MEMORY-FORMAT.md](https://github.com/Wolfe-Jam/faf/blob/main/MEMORY-FORMAT.md)
- Paper: [Zenodo DOI 10.5281/zenodo.20348942](https://doi.org/10.5281/zenodo.20348942)
- Reference impls: [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/) (Python) · [`grok-faf-voice`](https://pypi.org/project/grok-faf-voice/) (voice profile, Python)
- Cross-vendor proof: a `.fafm` written by `claude-fafm-sdk` reads cleanly via `grok-faf-voice`, both directions tested.

## How to know it's working

- Your agent doesn't ask *"what is this project?"* twice in the same week.
- `recall("X")` surfaces what you etched last session, not just this one.
- The `.fafm` file grows readably — it's plain YAML, diff it like code.
- Open the same `.fafm` in [`grok-faf-voice`](https://pypi.org/project/grok-faf-voice/) — same facts. Cross-vendor proven.

## Tradeoff note

Biases toward **deterministic recall** (substring + type + tags + priority + recency) over **semantic recall**. For semantic/ranked recall + LLM smart-merge, see hosted namepoints in [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/). Offline-first ≠ offline-only.

## The FAF Memory cluster

- This repo — **`faf-memory-mcp`** — the MCP server (wraps the SDK)
- [`Wolfe-Jam/faf-memory`](https://github.com/Wolfe-Jam/faf-memory) — the Claude Code plugin that installs this MCP
- [`Wolfe-Jam/faf-memory-proof`](https://github.com/Wolfe-Jam/faf-memory-proof) — the falsifiable receipt (412× methodology + scripts)
- [`claude-fafm-sdk`](https://pypi.org/project/claude-fafm-sdk/) — the open Python SDK this server wraps
- [`Wolfe-Jam/faf`](https://github.com/Wolfe-Jam/faf) — the format spec + IANA registration

## Citation

> Wolfe, J. (2026). *Permanent Memory and Instant Recall: The .fafm Standard for Multi-Profile AI Agent Memory*. Zenodo. https://doi.org/10.5281/zenodo.20348942

> Wolfe, J. (2026). *Why Agents Need a Passport: .fafa — Portable Identity for the Agentic Era*. Zenodo. https://doi.org/10.5281/zenodo.21951641

## License

MIT.
