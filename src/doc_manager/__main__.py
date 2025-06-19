"""
Main entry point for the document manager MCP server.
"""
from .simple_server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")