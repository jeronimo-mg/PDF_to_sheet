"""Unit tests for Desktop Commander and Ollama MCP configuration templates."""

import json
import os


def test_mcp_config_file_validity() -> None:
    config_file = "mcp_config.json"
    assert os.path.exists(config_file)

    with open(config_file, encoding="utf-8") as f:
        data = json.load(f)

    assert "mcpServers" in data
    assert "pdf-to-sheet" in data["mcpServers"]
    assert data["mcpServers"]["pdf-to-sheet"]["env"]["OLLAMA_HOST"] == "http://localhost:11434"


def test_claude_desktop_config_file_validity() -> None:
    config_file = "claude_desktop_config.json"
    assert os.path.exists(config_file)

    with open(config_file, encoding="utf-8") as f:
        data = json.load(f)

    assert "mcpServers" in data
    assert "pdf-to-sheet" in data["mcpServers"]
