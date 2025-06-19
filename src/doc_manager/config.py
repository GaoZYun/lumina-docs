#!/usr/bin/env python3
"""
Configuration management for Document Manager MCP Server.
"""
import os
from typing import Optional
from pathlib import Path


class Config:
    """Configuration manager using environment variables."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables with defaults."""
        # Database configuration
        self.database_path = os.getenv(
            'DOC_MANAGER_DB_PATH', 
            self._get_default_db_path()
        )
        
        # Export configuration
        self.export_directory = os.getenv(
            'DOC_MANAGER_EXPORT_DIR',
            os.path.expanduser('~/Desktop')
        )
        
        # Server configuration
        self.server_name = os.getenv('LUMINA_DOCS_SERVER_NAME', 'lumina-docs')
        
        # Debug and logging
        self.debug_mode = os.getenv('DOC_MANAGER_DEBUG', 'false').lower() == 'true'
        self.log_level = os.getenv('DOC_MANAGER_LOG_LEVEL', 'INFO').upper()
        
        # Data directory (for relative paths)
        self.data_directory = os.getenv(
            'DOC_MANAGER_DATA_DIR',
            self._get_default_data_dir()
        )
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _get_default_db_path(self) -> str:
        """Get default database path relative to package or data directory."""
        data_dir = self._get_default_data_dir()
        return os.path.join(data_dir, 'database', 'documents.db')
    
    def _get_default_data_dir(self) -> str:
        """Get default data directory."""
        # If running from source, use project directory
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        
        # Check if we're in a source directory structure
        if (project_root / 'pyproject.toml').exists():
            return str(project_root)
        
        # Otherwise use user's home directory
        return os.path.expanduser('~/.lumina-docs')
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        # Ensure database directory exists
        db_dir = os.path.dirname(self.database_path)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        
        # Ensure export directory exists
        Path(self.export_directory).mkdir(parents=True, exist_ok=True)
        
        # Ensure data directory exists
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)
    
    def get_database_path(self) -> str:
        """Get the database file path."""
        return self.database_path
    
    def get_export_directory(self) -> str:
        """Get the export directory path."""
        return self.export_directory
    
    def get_server_name(self) -> str:
        """Get the MCP server name."""
        return self.server_name
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug_mode
    
    def get_log_level(self) -> str:
        """Get the log level."""
        return self.log_level
    
    def to_dict(self) -> dict:
        """Export configuration as dictionary."""
        return {
            'database_path': self.database_path,
            'export_directory': self.export_directory,
            'server_name': self.server_name,
            'debug_mode': self.debug_mode,
            'log_level': self.log_level,
            'data_directory': self.data_directory,
        }
    
    def print_config(self):
        """Print current configuration (for debugging)."""
        print("Lumina Docs Configuration:")
        print(f"  Database Path: {self.database_path}")
        print(f"  Export Directory: {self.export_directory}")
        print(f"  Server Name: {self.server_name}")
        print(f"  Debug Mode: {self.debug_mode}")
        print(f"  Log Level: {self.log_level}")
        print(f"  Data Directory: {self.data_directory}")


# Global configuration instance
config = Config()