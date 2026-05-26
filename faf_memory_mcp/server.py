"""FAF Memory MCP server — exposes claude-fafm-sdk's Soul over MCP via fastmcp.

PML — the Permanent Memory Layer. Reads/writes ``.fafm``
(``application/vnd.fafm+yaml`` v1.1) — the IANA-registered cross-vendor AI
memory format. Format-compatible with ``grok-faf-voice`` (cross-vendor
proven, both directions tested).

Falsifiable receipt — 412× faster type-filter queries vs grep on a 492-file
Claude memory corpus. Methodology + scripts + sanitized pilot:
https://github.com/Wolfe-Jam/faf-memory-proof
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from claude_fafm_sdk import Soul

# Configuration (env, read once at startup)
DEFAULT_NAMEPOINT = os.environ.get("FAF_SOUL_NAMEPOINT", "@local")
DEFAULT_PROFILE = os.environ.get("FAF_SOUL_PROFILE", "knowledge")
DEFAULT_PATH = Path(os.environ.get("FAF_SOUL_PATH", "soul.fafm"))

# Single in-memory soul for the MCP session
_soul: Soul | None = None


def _get_soul() -> Soul:
    """Lazy-init the soul. Loads from FAF_SOUL_PATH if it exists; else fresh."""
    global _soul
    if _soul is None:
        if DEFAULT_PATH.exists():
            _soul = Soul.load(DEFAULT_PATH)
        else:
            _soul = Soul(namepoint=DEFAULT_NAMEPOINT, profile=DEFAULT_PROFILE)
    return _soul


def _fact_dict(fact: Any) -> dict[str, Any]:
    """Normalize Fact.to_obj() — it returns a bare string OR a mapping per the spec."""
    obj = fact.to_obj()
    return {"text": obj} if isinstance(obj, str) else obj


mcp = FastMCP("faf-memory")


@mcp.tool()
def etch(
    text: str,
    id: str | None = None,
    type: str | None = None,
    priority: str = "standard",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Write a durable fact to .fafm memory. If ``id`` matches an existing fact,
    it's updated in place (O(1) dedup); otherwise appended.

    Args:
        text:     The fact text (required).
        id:       Optional stable id for dedup/updates.
        type:     Optional type tag (e.g. "feedback", "reference", "decision").
        priority: One of "ephemeral", "standard", "high", "critical". Default "standard".
        tags:     Optional list of tag strings.
    """
    soul = _get_soul()
    fact = soul.etch(text=text, id=id, type=type, priority=priority, tags=tags)
    return _fact_dict(fact)


@mcp.tool()
def recall(
    query: str | None = None,
    type: str | None = None,
    tags: list[str] | None = None,
    min_priority: str = "ephemeral",
    limit: int | None = 20,
) -> list[dict[str, Any]]:
    """Recall facts — deterministic filter (substring on text, type equality,
    tag intersection, priority floor) ranked by priority then recency.

    Args:
        query:        Optional case-insensitive substring filter on fact text.
        type:         Optional type equality filter.
        tags:         Optional tag-intersection filter.
        min_priority: Priority floor — "ephemeral" | "standard" | "high" | "critical".
        limit:        Max facts to return. Default 20; pass null for all.
    """
    soul = _get_soul()
    results = soul.recall(
        query=query,
        type=type,
        tags=tags,
        min_priority=min_priority,
        limit=limit,
    )
    return [_fact_dict(f) for f in results]


@mcp.tool()
def list_facts() -> list[dict[str, Any]]:
    """List ALL facts in the current soul (no filter, no rank)."""
    soul = _get_soul()
    return [_fact_dict(f) for f in soul.facts]


@mcp.tool()
def save_soul(path: str | None = None) -> dict[str, Any]:
    """Persist the current soul to a .fafm file.

    Args:
        path: Optional override; default is $FAF_SOUL_PATH or ./soul.fafm.
    """
    soul = _get_soul()
    target = Path(path) if path else DEFAULT_PATH
    written = soul.save(target)
    return {"path": str(written), "fact_count": len(soul.facts)}


@mcp.tool()
def load_soul(path: str | None = None) -> dict[str, Any]:
    """Load a .fafm soul from disk, replacing the current in-memory soul.

    Args:
        path: Optional override; default is $FAF_SOUL_PATH or ./soul.fafm.
    """
    global _soul
    target = Path(path) if path else DEFAULT_PATH
    if not target.exists():
        return {"error": f"file not found: {target}"}
    _soul = Soul.load(target)
    return {"path": str(target), "fact_count": len(_soul.facts)}


def main() -> None:
    """Entry point — run the MCP server over stdio (default fastmcp transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
