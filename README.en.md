# Lumina Docs

[中文](README.md) | **English**

An intelligent structured document management system using the MCP protocol, designed to solve token overflow issues in large requirement documents and ensure content consistency.

## Core Features

🚀 **Solving Core Problems**
As a PM, I recently tried using Claude Code to write Markdown requirement documents. It worked well, but when the document scale grew larger, it would cause token overflow issues and make the document structure extremely chaotic.
Fortunately, requirement documents are structured documents. When writing, you often only need to focus on the part currently being edited, without needing to read the entire document every time. Based on this idea, I used Claude Code to create this MCP Server, which can solve the following problems:
- ✅ Solve large document token overflow issues
- ✅ Ensure content consistency through structured queries  
- ✅ Support modular document management
- ✅ Intelligent content reference and pattern matching

"This is a solution specifically customized for large language models!!!!"

🔧 **Technical Features**
- Lightweight database design based on SQLite
- Standardized interface using MCP protocol
- Parent-child hierarchical relationship management
- Flexible metadata support
- Powerful structured query capabilities
- Written entirely with Claude Code

## Quick Start

### 1. Install Dependencies
```bash
# Clone or download the project
git clone <repository-url>
cd lumina-docs

# Install dependencies
pip install -e .
```

### 2. Configure Environment Variables (Optional)
```bash
# Copy environment variable template
cp .env.example .env

# Edit configuration file (optional, you can skip this to use default configuration)
nano .env
```

### 3. Create Sample Data
```bash
cd examples
python sample_data.py
```

### 4. Start MCP Server
```bash
python -m doc_manager
```

### 5. Configure Claude Desktop
#### Method 1: Automatic Installation (Recommended)
```bash
# Automatically configure to Claude Desktop
./install_to_claude_desktop.sh
```

#### Method 2: Manual Configuration
If automatic installation encounters issues, you can configure manually. First determine your Python path:
```bash
# Find Python path
which python3
# Or if using conda
which python
```

Then edit the Claude Desktop configuration file `~/Library/Application Support/Claude/claude_desktop_config.json`, add or update the lumina-docs configuration.

### 6. Use Command Line Tools
```bash
# View document tree structure
python -m doc_manager.cli tree

# Search for specific types of nodes
python -m doc_manager.cli by-type business_flow

# Export to Markdown
python -m doc_manager.cli export --output requirements.md
```

## Configuration Guide

### Environment Variable Configuration

Lumina Docs supports configuration through environment variables, making the project more flexible and suitable for different deployment environments.

#### Core Configuration Items

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `DOC_MANAGER_DB_PATH` | `<data_dir>/database/documents.db` | SQLite database file path |
| `DOC_MANAGER_EXPORT_DIR` | `~/Desktop` | Export file save directory |
| `DOC_MANAGER_DATA_DIR` | `~/.lumina-docs` | Data file root directory |
| `LUMINA_DOCS_SERVER_NAME` | `lumina-docs` | MCP server name |
| `DOC_MANAGER_DEBUG` | `false` | Debug mode switch |
| `DOC_MANAGER_LOG_LEVEL` | `INFO` | Log level |

#### Configuration Methods

**Method 1: Using .env file**
```bash
# Copy template file
cp .env.example .env

# Edit configuration
DOC_MANAGER_DB_PATH=/path/to/your/database.db
DOC_MANAGER_EXPORT_DIR=/path/to/exports
DOC_MANAGER_DEBUG=true
```

**Method 2: System environment variables**
```bash
export DOC_MANAGER_DB_PATH="/var/lib/lumina-docs/documents.db"
export DOC_MANAGER_EXPORT_DIR="/home/user/Documents/exports"
```

**Method 3: Claude Desktop configuration**
```json
{
  "mcpServers": {
    "lumina-docs": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/lumina-docs",
      "env": {
        "PYTHONPATH": "/path/to/lumina-docs/src",
        "DOC_MANAGER_DB_PATH": "/path/to/database.db",
        "DOC_MANAGER_EXPORT_DIR": "/path/to/exports",
        "DOC_MANAGER_DATA_DIR": "/path/to/lumina-docs",
        "LUMINA_DOCS_SERVER_NAME": "lumina-docs",
        "DOC_MANAGER_DEBUG": "false",
        "DOC_MANAGER_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

> **Note**: Please use the actual Python path in your system, such as `/usr/bin/python3`, `/usr/local/bin/python3`, or the full path of conda environment.

### Deployment Configuration Examples

#### Development Environment
```bash
DOC_MANAGER_DEBUG=true
DOC_MANAGER_LOG_LEVEL=DEBUG
DOC_MANAGER_DB_PATH=./dev-database.db
```

#### Production Environment
```bash
DOC_MANAGER_DATA_DIR=/var/lib/lumina-docs
DOC_MANAGER_DB_PATH=/var/lib/lumina-docs/database/documents.db
DOC_MANAGER_EXPORT_DIR=/var/lib/lumina-docs/exports
DOC_MANAGER_LOG_LEVEL=WARNING
```

#### Docker Deployment
```yaml
# docker-compose.yml
services:
  lumina-docs:
    image: lumina-docs:latest
    environment:
      DOC_MANAGER_DB_PATH: "/app/data/documents.db"
      DOC_MANAGER_EXPORT_DIR: "/app/data/exports"
      DOC_MANAGER_DATA_DIR: "/app/data"
    volumes:
      - ./data:/app/data
```

#### Multi-user Environment
```bash
DOC_MANAGER_DATA_DIR=/home/$USER/.local/share/lumina-docs
DOC_MANAGER_EXPORT_DIR=/home/$USER/Documents/lumina-docs-exports
```

## Claude Desktop MCP Server Configuration Examples

### Complete Configuration Example

The following is a complete Claude Desktop configuration file example, showing how to configure lumina-docs with other MCP servers:

```json
{
  "mcpServers": {
    "lumina-docs": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/lumina-docs",
      "env": {
        "PYTHONPATH": "/path/to/lumina-docs/src",
        "DOC_MANAGER_DB_PATH": "/path/to/lumina-docs/database/documents.db",
        "DOC_MANAGER_EXPORT_DIR": "/Users/username/Desktop",
        "DOC_MANAGER_DATA_DIR": "/path/to/lumina-docs",
        "LUMINA_DOCS_SERVER_NAME": "lumina-docs",
        "DOC_MANAGER_DEBUG": "false",
        "DOC_MANAGER_LOG_LEVEL": "INFO"
      }
    },
    "other-mcp-server": {
      "command": "node",
      "args": ["/path/to/other-server/index.js"]
    }
  }
}
```

### Common Python Path Configurations

Choose appropriate configuration based on your Python installation:

#### System Python (macOS)
```json
{
  "command": "/usr/bin/python3",
  "args": ["-m", "doc_manager"]
}
```

#### System Python (Linux)
```json
{
  "command": "/usr/bin/python3",
  "args": ["-m", "doc_manager"]
}
```

#### Homebrew Python (macOS)
```json
{
  "command": "/opt/homebrew/bin/python3",
  "args": ["-m", "doc_manager"]
}
```

#### Conda Environment
```json
{
  "command": "/Users/username/miniconda/bin/python",
  "args": ["-m", "doc_manager"]
}
```

#### pyenv Python
```json
{
  "command": "/Users/username/.pyenv/versions/3.11.0/bin/python",
  "args": ["-m", "doc_manager"]
}
```

### Troubleshooting

#### Find Correct Python Path
```bash
# Find Python 3 path
which python3

# Find Python path (if using conda)
which python

# Check Python version
python3 --version
```

#### Test Configuration
```bash
# Change to project directory
cd /path/to/lumina-docs

# Test module import
PYTHONPATH=/path/to/lumina-docs/src python3 -c "import doc_manager; print('Import successful')"

# Test server startup
PYTHONPATH=/path/to/lumina-docs/src python3 -m doc_manager --help
```

#### View Logs
Claude Desktop MCP server log locations:
- **macOS**: `~/Library/Logs/Claude/mcp-server-lumina-docs.log`
- **Linux**: `~/.local/share/Claude/logs/mcp-server-lumina-docs.log`

#### Common Errors and Solutions

1. **`spawn python ENOENT`**
   - Cause: Cannot find python command
   - Solution: Use full Python path, like `/usr/bin/python3`

2. **`No module named doc_manager`**
   - Cause: PYTHONPATH configuration error
   - Solution: Ensure PYTHONPATH points to correct src directory

3. **Permission Error**
   - Cause: Insufficient permissions for database or export directory
   - Solution: Check directory permissions, ensure Claude Desktop can read/write

### Configuration Templates

The project provides multiple configuration file templates, choose based on your environment:

- `claude_desktop_config.example.json` - General template
- `claude_desktop_config.macos.json` - macOS system Python configuration
- `claude_desktop_config.conda.json` - Conda environment configuration
- `claude_desktop_config.multi.json` - Multi MCP server configuration example

Usage:
```bash
# Copy appropriate template
cp claude_desktop_config.macos.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Edit paths
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## Core Concepts

### Document Node Types
- **document_root**: Document root node
- **section**: Chapters (like project overview, requirement specification)
- **module**: Function modules (like overview module, system monitoring module)
- **feature**: Specific features (like system status statistics feature)
- **business_flow**: Business process description
- **data_display_rules**: Data display rules
- **permission_rules**: Permission control rules
- **architecture_design**: Architecture design

### Hierarchical Structure
```
Intelligent Operation System Requirements Document (document_root)
├── Project Overview (section)
├── Function Modules (section)
│   ├── Overview Module (module)
│   │   ├── System Status Statistics Feature (feature)
│   │   │   ├── Business Process Description (business_flow)
│   │   │   └── Data Display Rules (data_display_rules)
│   │   └── My Focused Systems Feature (feature)
│   └── System Monitoring Module (module)
└── Permission Design (section)
```

## Use Cases

### 1. Structured Queries to Ensure Consistency
```python
# Query all [Business Process Descriptions] as reference for new content
nodes = db.get_nodes_by_type("business_flow")

# Query all [Data Display Rules] for specific module
results = db.search_nodes(
    node_type="data_display_rules",
    metadata_filter={"module": "overview"}
)
```

### 2. Consistency Check When Writing New Content
```bash
# Use consistency check tool
cd examples
python consistency_checker.py
```

### 3. Export Documents on Demand
```bash
# Export complete document
python -m doc_manager.cli export --output complete.md

# Export only function modules part
python -m doc_manager.cli export --parent-id 3 --output modules.md
```

## MCP Tools List

### Document Management Tools
| Tool Name | Function Description |
|-----------|---------------------|
| `create_document` | Create new document (independent table) |
| `get_documents_list` | Get all documents list |
| `delete_document` | Delete document and its data table |

### Node Management Tools
| Tool Name | Function Description |
|-----------|---------------------|
| `create_node` | Create new document node |
| `get_node` | Get specified node details |
| `update_node` | Update existing node |
| `delete_node` | Delete node and its child nodes |
| `move_node` | Move node to new position |

### Query and Export Tools
| Tool Name | Function Description |
|-----------|---------------------|
| `get_children` | Get child nodes list |
| `search_nodes` | Multi-condition search nodes |
| `get_nodes_by_type` | Get nodes by type (consistency analysis) |
| `get_node_path` | Get node complete path |
| `get_tree_structure` | Get tree structure |
| `export_to_markdown` | Export to Markdown format |

## Command Line Tools

### Basic Operations
```bash
# Create node
python -m doc_manager.cli create "New Feature" "feature" --parent-id 5 --content "Feature description"

# View node
python -m doc_manager.cli get 1

# Update node
python -m doc_manager.cli update 1 --title "New Title" --content "New content"

# Delete node
python -m doc_manager.cli delete 1
```

### Query Operations
```bash
# List child nodes
python -m doc_manager.cli list --parent-id 1

# Search nodes
python -m doc_manager.cli search --query "business process" --type "business_flow"

# View tree structure
python -m doc_manager.cli tree

# Find by type
python -m doc_manager.cli by-type data_display_rules
```

### Export Operations
```bash
# Export complete document
python -m doc_manager.cli export --output requirements.md

# Export specified part
python -m doc_manager.cli export --parent-id 3 --output modules.md
```

## Project Structure

```
lumina-docs/
├── src/
│   └── doc_manager/
│       ├── __init__.py           # Module initialization
│       ├── database.py           # SQLite database operations
│       ├── simple_server.py      # MCP server implementation
│       ├── cli.py                # Command line tools
│       ├── config.py             # Configuration management
│       └── __main__.py           # Server startup entry
├── examples/
│   ├── sample_data.py            # Sample data creation
│   └── consistency_checker.py    # Consistency check tool
├── database/
│   └── documents.db              # SQLite database file
├── docs/
│   └── (documentation directory)
├── .env.example                  # Environment variable template
├── claude_desktop_config.*.json # Configuration templates
├── pyproject.toml                # Project configuration
├── README.md                     # Chinese documentation
├── README.en.md                  # English documentation
└── docker-compose.example.yml   # Docker deployment example
```

## Advanced Usage

### 1. Consistency Assurance Workflow

When writing new [Business Process Description]:
```python
# 1. Query existing business process descriptions
existing_flows = db.get_nodes_by_type("business_flow")

# 2. Analyze existing patterns
for flow in existing_flows:
    print(f"Reference: {flow['title']}")
    print(f"Format: {flow['content'][:100]}...")

# 3. Follow existing patterns when creating new nodes
new_id = db.create_node(
    title="New Business Process Description",
    node_type="business_flow", 
    content="1. Step one\n2. Step two\n3. Step three",  # Keep format consistent
    parent_id=parent_id
)
```

### 2. Metadata-Driven Management
```python
# Use metadata for precise queries
frontend_modules = db.search_nodes(
    node_type="module",
    metadata_filter={"module_type": "frontend"}
)

high_priority_features = db.search_nodes(
    metadata_filter={"priority": "high"}
)
```

### 3. Batch Operations
```python
# Batch update metadata for same type nodes
business_flows = db.get_nodes_by_type("business_flow")
for flow in business_flows:
    db.update_node(
        flow['id'],
        metadata={**flow['metadata'], "reviewed": True}
    )
```

## Best Practices

1. **Naming Conventions**: Use consistent node title formats
2. **Type Management**: Define clear node_type for different content types
3. **Metadata Usage**: Make full use of metadata field to store additional information
4. **Hierarchy Design**: Design reasonable parent-child relationships, avoid overly deep nesting
5. **Consistency Checks**: Regularly run consistency check tools

## Comparison with Traditional Methods

| Traditional Method | Structured Method |
|-------------------|------------------|
| Single large file | Modular nodes |
| Easy token overflow | Load content on demand |
| Hard to ensure consistency | Structured query reference |
| Modifications affect entire document | Precise modification of specific nodes |
| Manual format maintenance | Automated export and merge |

## Development and Extension

### Adding New Node Types
1. Add new node_type in database
2. Update MCP tools schema definition
3. Add corresponding check logic in consistency checker

### Custom Export Formats
1. Inherit DocumentDatabase class
2. Override export_tree_to_markdown method
3. Implement custom formatting logic

## Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback

If you have any questions or suggestions, please feel free to open an issue or contact the development team.