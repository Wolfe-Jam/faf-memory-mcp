"""Functional round-trip tests for faf-memory-mcp.

Covers the five MCP tools (etch / recall / list_facts / save_soul / load_soul)
end-to-end against a fresh in-memory + on-disk soul per test.
"""

from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def soul_env(tmp_path, monkeypatch):
    """Reset server state with a fresh temp soul before each test."""
    from faf_memory_mcp import server

    path = tmp_path / "test.fafm"
    monkeypatch.setattr(server, "DEFAULT_PATH", path)
    monkeypatch.setattr(server, "DEFAULT_NAMEPOINT", "@test")
    server._soul = None  # force lazy re-init under the patched defaults
    yield server, path


def _call(tool: Any, **kwargs: Any) -> Any:
    """Invoke a fastmcp-decorated tool — handles both 2.x and 3.x decorator forms.

    fastmcp 3.x wraps tools in a FunctionTool with `.fn` pointing to the original;
    fastmcp 2.x leaves them as plain callables.
    """
    f = getattr(tool, "fn", None) or getattr(tool, "__wrapped__", None) or tool
    return f(**kwargs)


def test_etch_returns_fact_dict(soul_env):
    server, _ = soul_env
    fact = _call(server.etch, text="hello", id="h1", type="note")
    assert fact["id"] == "h1"
    assert fact["text"] == "hello"
    assert fact["type"] == "note"


def test_list_facts_counts(soul_env):
    server, _ = soul_env
    _call(server.etch, text="alpha", id="a")
    _call(server.etch, text="beta", id="b")
    facts = _call(server.list_facts)
    assert len(facts) == 2


def test_recall_filters_by_type(soul_env):
    server, _ = soul_env
    _call(server.etch, text="A feedback note", id="a", type="feedback")
    _call(server.etch, text="B reference doc", id="b", type="reference")
    matches = _call(server.recall, type="feedback")
    assert len(matches) == 1
    assert "feedback" in matches[0]["text"].lower()


def test_recall_priority_floor_excludes_ephemeral(soul_env):
    server, _ = soul_env
    _call(server.etch, text="durable", id="d", priority="critical")
    _call(server.etch, text="scratch", id="e", priority="ephemeral")
    standard_plus = _call(server.recall, min_priority="standard")
    assert len(standard_plus) == 1
    assert standard_plus[0]["text"] == "durable"


def test_recall_substring_query(soul_env):
    server, _ = soul_env
    _call(server.etch, text="The quick brown fox", id="q1")
    _call(server.etch, text="A lazy dog", id="q2")
    matches = _call(server.recall, query="quick")
    assert len(matches) == 1
    assert matches[0]["id"] == "q1"


def test_etch_persists_without_save_soul(soul_env):
    """etch must write the file so memory survives process exit."""
    server, path = soul_env
    _call(server.etch, text="survives restart", id="persist-1")
    assert path.exists(), "etch did not write $FAF_SOUL_PATH"

    server._soul = None
    loaded = _call(server.load_soul)
    assert loaded["fact_count"] == 1
    facts = _call(server.list_facts)
    assert facts[0]["text"] == "survives restart"


def test_save_then_load_round_trip(soul_env):
    server, path = soul_env
    _call(server.etch, text="persistent", id="p", priority="high")
    saved = _call(server.save_soul)
    assert saved["fact_count"] == 1
    assert path.exists()

    # Reset and reload — facts must come back
    server._soul = None
    loaded = _call(server.load_soul)
    assert loaded["fact_count"] == 1

    facts = _call(server.list_facts)
    assert len(facts) == 1
    assert facts[0]["text"] == "persistent"


def test_load_missing_path_returns_error(soul_env):
    server, _ = soul_env
    result = _call(server.load_soul, path="/tmp/does-not-exist-faf-memory-mcp.fafm")
    assert "error" in result
