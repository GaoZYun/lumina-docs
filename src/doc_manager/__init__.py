"""
Document Manager MCP Server
A structured document management system using MCP protocol.
"""

__version__ = "0.1.0"
__author__ = "Jacques LaGaoi"
__email__ = "gaodie1@outlook.com"

from .database import DocumentDatabase

__all__ = ["DocumentDatabase"]