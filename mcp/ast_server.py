"""Optional MCP server wrapper for AST tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp.ast_tools import get_function, get_imports, list_symbols, parse_file


mcp = FastMCP("repomind-ast")


@mcp.tool()
def parse_file_tool(file_path: str, language: str) -> list[dict]:
    """Parse a file and return functions and classes."""
    return parse_file(file_path, language)


@mcp.tool()
def get_function_tool(file_path: str, function_name: str) -> dict:
    """Return one function or method definition."""
    return get_function(file_path, function_name)


@mcp.tool()
def list_symbols_tool(file_path: str) -> dict:
    """List symbols in a file."""
    return list_symbols(file_path)


@mcp.tool()
def get_imports_tool(file_path: str) -> list[str]:
    """List import-like lines in a file."""
    return get_imports(file_path)


if __name__ == "__main__":
    mcp.run()
