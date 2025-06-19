# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Lumina Docs
- Multi-document management with independent tables per document
- Complete document and node management tools
- Environment variable configuration system
- Bilingual documentation (English and Chinese)
- Multiple Claude Desktop configuration templates

### Features
- **Document Management Tools**:
  - `create_document`: Create new document with independent table
  - `get_documents_list`: Get all documents list
  - `delete_document`: Delete document and its data table

- **Node Management Tools**:
  - `create_node`: Create new document node with document support
  - `get_node`: Get node details with document specification
  - `update_node`: Update existing node
  - `delete_node`: Delete node and its children
  - `move_node`: Move node to new position

- **Query and Export Tools**:
  - `get_children`: Get child nodes list
  - `search_nodes`: Multi-condition search with document filtering
  - `get_nodes_by_type`: Get nodes by type for consistency analysis
  - `get_node_path`: Get complete node path
  - `get_tree_structure`: Get tree structure
  - `export_to_markdown`: Export to configurable directory

### Technical Features
- SQLite-based lightweight database design
- MCP protocol standardized interface
- Parent-child hierarchical relationship management
- Flexible metadata support
- Powerful structured query capabilities
- Environment variable configuration
- Docker deployment support

### Documentation
- Comprehensive README in English and Chinese
- Detailed configuration guides
- Multiple deployment scenarios
- Troubleshooting guides
- Configuration templates for different environments

### Configuration
- Environment variable support for all major settings
- Claude Desktop integration with automatic installation
- Multiple Python environment support (system, conda, pyenv, etc.)
- Backward compatibility with existing configurations

## [1.0.0] - 2024-06-19

### Added
- Initial public release
- Project renamed from "Document Manager" to "Lumina Docs"
- MIT License
- Contributing guidelines
- Open source release preparation

---

## Version History Notes

This project was originally developed as "Document Manager" and has been renamed to "Lumina Docs" for the open source release. The core functionality remains the same, with enhanced documentation and configuration flexibility.

### Migration from Document Manager
- All existing configurations continue to work
- Data migration is optional
- New installations use updated naming conventions
- Backward compatibility maintained for all APIs