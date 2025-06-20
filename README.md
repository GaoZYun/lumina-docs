# Lumina Docs

**中文** | [English](README.en.md)

一个使用MCP协议的智能结构化文档管理系统，专为解决大型需求文档的token超长问题和保证内容一致性而设计。

## 核心特性

🚀 **解决核心问题**
我是一个PM，最近尝试用 Claude Code 去写Markdown 格式的需求文档，它的工作完成得还可以，但当文档规模越来越大的时候，会导致 Tokens 超出限制的问题，也会导致文档结构极度混乱。
好在需求文档是一种结构化的文档，在编写的时候往往只需要关注当前正在编辑的部分，无需每次都阅读全文，正是在这个思路之下，我使用 Claude Code 做了这样一个 MCP Server 它能够解决的问题是：
- ✅ 解决大文档token超长问题
- ✅ 通过结构化查询保证内容一致性  
- ✅ 支持模块化文档管理
- ✅ 智能的内容参考和模式匹配
**这是一个专门为大语言模型定制的方案！！！！**
🔧
 **技术特性**
- 基于SQLite的轻量级数据库设计
- MCP协议标准化接口
- 父子层级关系管理
- 灵活的元数据支持
- 强大的结构化查询能力
- 纯 Claude Code 编写

## 快速开始

### 1. 安装依赖
```bash
# 克隆或下载项目
git clone <repository-url>
cd lumina-docs

# 安装依赖
pip install -e .
```

### 2. 配置环境变量（可选）
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件（可选，使用默认配置可直接跳过）
nano .env
```

### 3. 创建示例数据
```bash
cd examples
python sample_data.py
```

### 4. 启动MCP服务器
```bash
python -m doc_manager
```

### 5. 配置Claude Desktop
#### 方式1: 自动安装（推荐）
```bash
# 自动配置到Claude Desktop
./install_to_claude_desktop.sh
```

#### 方式2: 手动配置
如果自动安装遇到问题，可以手动配置。首先确定你的 Python 路径：
```bash
# 查找 Python 路径
which python3
# 或者如果使用 conda
which python
```

然后编辑 Claude Desktop 配置文件 `~/Library/Application Support/Claude/claude_desktop_config.json`，添加或更新 lumina-docs 配置。

### 6. 使用命令行工具
```bash
# 查看文档树结构
python -m doc_manager.cli tree

# 搜索特定类型的节点
python -m doc_manager.cli by-type business_flow

# 导出为Markdown
python -m doc_manager.cli export --output requirements.md
```

## 配置说明

### 环境变量配置

Lumina Docs 支持通过环境变量进行配置，使项目更灵活、更适合不同的部署环境。

#### 核心配置项

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `DOC_MANAGER_DB_PATH` | `<data_dir>/database/documents.db` | SQLite数据库文件路径 |
| `DOC_MANAGER_EXPORT_DIR` | `~/Desktop` | 导出文件保存目录 |
| `DOC_MANAGER_DATA_DIR` | `~/.lumina-docs` | 数据文件根目录 |
| `LUMINA_DOCS_SERVER_NAME` | `lumina-docs` | MCP服务器名称 |
| `DOC_MANAGER_DEBUG` | `false` | 调试模式开关 |
| `DOC_MANAGER_LOG_LEVEL` | `INFO` | 日志级别 |

#### 配置方式

**方式1: 使用.env文件**
```bash
# 复制模板文件
cp .env.example .env

# 编辑配置
DOC_MANAGER_DB_PATH=/path/to/your/database.db
DOC_MANAGER_EXPORT_DIR=/path/to/exports
DOC_MANAGER_DEBUG=true
```

**方式2: 系统环境变量**
```bash
export DOC_MANAGER_DB_PATH="/var/lib/doc-manager/documents.db"
export DOC_MANAGER_EXPORT_DIR="/home/user/Documents/exports"
```

**方式3: Claude Desktop配置**
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

> **注意**: 请使用系统中实际的 Python 路径，如 `/usr/bin/python3`、`/usr/local/bin/python3` 或 conda 环境的完整路径。

### 部署配置示例

#### 开发环境
```bash
DOC_MANAGER_DEBUG=true
DOC_MANAGER_LOG_LEVEL=DEBUG
DOC_MANAGER_DB_PATH=./dev-database.db
```

#### 生产环境
```bash
DOC_MANAGER_DATA_DIR=/var/lib/doc-manager
DOC_MANAGER_DB_PATH=/var/lib/doc-manager/database/documents.db
DOC_MANAGER_EXPORT_DIR=/var/lib/doc-manager/exports
DOC_MANAGER_LOG_LEVEL=WARNING
```

#### Docker部署
```yaml
# docker-compose.yml
services:
  document-manager:
    image: doc-manager:latest
    environment:
      DOC_MANAGER_DB_PATH: "/app/data/documents.db"
      DOC_MANAGER_EXPORT_DIR: "/app/data/exports"
      DOC_MANAGER_DATA_DIR: "/app/data"
    volumes:
      - ./data:/app/data
```

#### 多用户环境
```bash
DOC_MANAGER_DATA_DIR=/home/$USER/.local/share/doc-manager
DOC_MANAGER_EXPORT_DIR=/home/$USER/Documents/doc-manager-exports
```

## Claude Desktop MCP Server 配置示例

### 完整配置示例

以下是完整的 Claude Desktop 配置文件示例，展示如何将 document-manager 与其他 MCP 服务器一起配置：

```json
{
  "mcpServers": {
    "document-manager": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/doc-manager",
      "env": {
        "PYTHONPATH": "/path/to/doc-manager/src",
        "DOC_MANAGER_DB_PATH": "/path/to/doc-manager/database/documents.db",
        "DOC_MANAGER_EXPORT_DIR": "/Users/username/Desktop",
        "DOC_MANAGER_DATA_DIR": "/path/to/doc-manager",
        "DOC_MANAGER_SERVER_NAME": "document-manager",
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

### 常见 Python 路径配置

根据你的 Python 安装方式，选择合适的配置：

#### 系统 Python (macOS)
```json
{
  "command": "/usr/bin/python3",
  "args": ["-m", "doc_manager"]
}
```

#### 系统 Python (Linux)
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

#### Conda 环境
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

### 不同场景的配置

#### 开发环境配置
```json
{
  "mcpServers": {
    "document-manager-dev": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/doc-manager",
      "env": {
        "PYTHONPATH": "/path/to/doc-manager/src",
        "DOC_MANAGER_DEBUG": "true",
        "DOC_MANAGER_LOG_LEVEL": "DEBUG",
        "DOC_MANAGER_DB_PATH": "/path/to/doc-manager/dev-database.db",
        "DOC_MANAGER_EXPORT_DIR": "/path/to/dev-exports"
      }
    }
  }
}
```

#### 生产环境配置
```json
{
  "mcpServers": {
    "document-manager": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/opt/doc-manager",
      "env": {
        "PYTHONPATH": "/opt/doc-manager/src",
        "DOC_MANAGER_DATA_DIR": "/var/lib/doc-manager",
        "DOC_MANAGER_DB_PATH": "/var/lib/doc-manager/database/documents.db",
        "DOC_MANAGER_EXPORT_DIR": "/var/lib/doc-manager/exports",
        "DOC_MANAGER_LOG_LEVEL": "WARNING"
      }
    }
  }
}
```

#### 多用户环境配置
```json
{
  "mcpServers": {
    "document-manager": {
      "command": "/usr/bin/python3",
      "args": ["-m", "doc_manager"],
      "cwd": "/opt/doc-manager",
      "env": {
        "PYTHONPATH": "/opt/doc-manager/src",
        "DOC_MANAGER_DATA_DIR": "/home/$USER/.local/share/doc-manager",
        "DOC_MANAGER_EXPORT_DIR": "/home/$USER/Documents/doc-manager-exports"
      }
    }
  }
}
```

### 故障排除

#### 查找正确的 Python 路径
```bash
# 查找 Python 3 路径
which python3

# 查找 Python 路径 (如果使用 conda)
which python

# 查看 Python 版本
python3 --version
```

#### 测试配置
```bash
# 切换到项目目录
cd /path/to/doc-manager

# 测试模块导入
PYTHONPATH=/path/to/doc-manager/src python3 -c "import doc_manager; print('导入成功')"

# 测试服务器启动
PYTHONPATH=/path/to/doc-manager/src python3 -m doc_manager --help
```

#### 查看日志
Claude Desktop 的 MCP 服务器日志位置：
- **macOS**: `~/Library/Logs/Claude/mcp-server-document-manager.log`
- **Linux**: `~/.local/share/Claude/logs/mcp-server-document-manager.log`

#### 常见错误及解决方案

1. **`spawn python ENOENT`**
   - 原因：找不到 python 命令
   - 解决：使用完整的 Python 路径，如 `/usr/bin/python3`

2. **`No module named doc_manager`**
   - 原因：PYTHONPATH 配置错误
   - 解决：确保 PYTHONPATH 指向正确的 src 目录

3. **权限错误**
   - 原因：数据库或导出目录权限不足
   - 解决：检查目录权限，确保 Claude Desktop 可以读写

### 配置验证

配置完成后，可以通过以下方式验证：

1. **重启 Claude Desktop**
2. **查看日志文件**，确认没有错误
3. **在 Claude Desktop 中测试**：
   ```
   请获取当前所有文档列表
   ```
4. **检查可用工具**：
   ```
   document-manager 有哪些可用的工具？
   ```

### 配置文件模板

项目提供了多个配置文件模板，可以根据你的环境选择：

- `claude_desktop_config.example.json` - 通用模板
- `claude_desktop_config.macos.json` - macOS 系统 Python 配置
- `claude_desktop_config.conda.json` - Conda 环境配置
- `claude_desktop_config.multi.json` - 多 MCP 服务器配置示例

使用方法：
```bash
# 复制合适的模板
cp claude_desktop_config.macos.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 编辑路径
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## 核心概念

### 文档节点类型
- **document_root**: 文档根节点
- **section**: 章节（如项目概述、需求说明）
- **module**: 功能模块（如总览模块、系统监控模块）
- **feature**: 具体功能（如系统状态统计功能）
- **business_flow**: 业务流程说明
- **data_display_rules**: 数据展示规则
- **permission_rules**: 权限控制规则
- **architecture_design**: 架构设计

### 层级关系
```
智能运维系统需求文档 (document_root)
├── 项目概述 (section)
├── 功能模块 (section)
│   ├── 总览模块 (module)
│   │   ├── 系统状态统计功能 (feature)
│   │   │   ├── 业务流程说明 (business_flow)
│   │   │   └── 数据展示规则 (data_display_rules)
│   │   └── 我关注的系统功能 (feature)
│   └── 系统监控模块 (module)
└── 权限设计 (section)
```

## 使用场景

### 1. 快速导入现有文档
```python
# 通过Claude直接使用MCP工具导入单个文档
import_markdown_file("项目需求.md", "project_requirements")

# 批量导入文档目录
import_markdown_batch(["docs/*.md", "guides/**/*.md"])
```

### 2. 结构化查询保证一致性
```python
# 查询所有【业务流程说明】作为新内容的参考
nodes = db.get_nodes_by_type("business_flow")

# 查询特定模块的所有【数据展示规则】
results = db.search_nodes(
    node_type="data_display_rules",
    metadata_filter={"module": "overview"}
)
```

### 2. 编写新内容时的一致性检查
```bash
# 使用一致性检查工具
cd examples
python consistency_checker.py
```

### 3. 按需导出文档
```bash
# 导出完整文档
python -m doc_manager.cli export --output complete.md

# 只导出功能模块部分
python -m doc_manager.cli export --parent-id 3 --output modules.md
```

## MCP工具列表

### 文档管理工具
| 工具名称 | 功能说明 |
|---------|---------|
| `create_document` | 创建新文档（独立表） |
| `get_documents_list` | 获取所有文档列表 |
| `delete_document` | 删除文档及其数据表 |

### Markdown导入工具
| 工具名称 | 功能说明 |
|---------|---------|
| `import_markdown_file` | 导入单个Markdown文件，自动解析层次结构 |
| `import_markdown_batch` | 批量导入Markdown文件，支持通配符匹配 |

### 节点管理工具
| 工具名称 | 功能说明 |
|---------|---------|
| `create_node` | 创建新的文档节点 |
| `get_node` | 获取指定节点详情 |
| `update_node` | 更新现有节点 |
| `delete_node` | 删除节点及其子节点 |
| `move_node` | 移动节点到新位置 |

### 查询和导出工具
| 工具名称 | 功能说明 |
|---------|---------|
| `get_children` | 获取子节点列表 |
| `search_nodes` | 多条件搜索节点 |
| `get_nodes_by_type` | 按类型获取节点（一致性分析） |
| `get_node_path` | 获取节点完整路径 |
| `get_tree_structure` | 获取树形结构 |
| `export_to_markdown` | 导出为Markdown格式 |

## 命令行工具

### 基本操作
```bash
# 创建节点
python -m doc_manager.cli create "新功能" "feature" --parent-id 5 --content "功能描述"

# 查看节点
python -m doc_manager.cli get 1

# 更新节点
python -m doc_manager.cli update 1 --title "新标题" --content "新内容"

# 删除节点
python -m doc_manager.cli delete 1
```

### 查询操作
```bash
# 列出子节点
python -m doc_manager.cli list --parent-id 1

# 搜索节点
python -m doc_manager.cli search --query "业务流程" --type "business_flow"

# 查看树结构
python -m doc_manager.cli tree

# 按类型查找
python -m doc_manager.cli by-type data_display_rules
```

### 导出操作
```bash
# 导出完整文档
python -m doc_manager.cli export --output requirements.md

# 导出指定部分
python -m doc_manager.cli export --parent-id 3 --output modules.md
```

## 项目结构

```
doc-manager/
├── src/
│   └── doc_manager/
│       ├── __init__.py           # 模块初始化
│       ├── database.py           # SQLite数据库操作
│       ├── simple_server.py      # MCP服务器实现
│       ├── markdown_parser.py    # Markdown解析和导入模块
│       ├── cli.py                # 命令行工具
│       └── __main__.py           # 服务器启动入口
├── examples/
│   ├── sample_data.py            # 示例数据创建
│   └── consistency_checker.py    # 一致性检查工具
├── database/
│   └── documents.db              # SQLite数据库文件
├── docs/
│   └── (文档目录)
├── pyproject.toml                # 项目配置
└── README.md                     # 项目说明
```

## 高级用法

### 1. 一致性保证工作流

在编写新的【业务流程说明】时：
```python
# 1. 查询现有的业务流程说明
existing_flows = db.get_nodes_by_type("business_flow")

# 2. 分析现有模式
for flow in existing_flows:
    print(f"参考: {flow['title']}")
    print(f"格式: {flow['content'][:100]}...")

# 3. 创建新节点时遵循现有模式
new_id = db.create_node(
    title="新业务流程说明",
    node_type="business_flow", 
    content="1. 步骤一\n2. 步骤二\n3. 步骤三",  # 保持格式一致
    parent_id=parent_id
)
```

### 2. 元数据驱动的管理
```python
# 使用元数据进行精确查询
frontend_modules = db.search_nodes(
    node_type="module",
    metadata_filter={"module_type": "frontend"}
)

high_priority_features = db.search_nodes(
    metadata_filter={"priority": "high"}
)
```

### 3. 批量操作
```python
# 批量更新相同类型节点的元数据
business_flows = db.get_nodes_by_type("business_flow")
for flow in business_flows:
    db.update_node(
        flow['id'],
        metadata={**flow['metadata'], "reviewed": True}
    )
```

## 最佳实践

1. **命名规范**: 使用一致的节点标题格式
2. **类型管理**: 为不同内容类型定义清晰的node_type
3. **元数据使用**: 充分利用metadata字段存储额外信息
4. **层级设计**: 合理设计父子关系，避免过深的嵌套
5. **一致性检查**: 定期运行一致性检查工具

## 与传统方式对比

| 传统方式 | 结构化方式 |
|---------|-----------|
| 单一大文件 | 模块化节点 |
| Token容易超长 | 按需加载内容 |
| 难以保证一致性 | 结构化查询参考 |
| 修改影响全文 | 精确修改特定节点 |
| 手工维护格式 | 自动化导出合并 |

## 开发和扩展

### 添加新的节点类型
1. 在数据库中添加新的node_type
2. 更新MCP工具的schema定义
3. 在一致性检查器中添加相应检查逻辑

### 自定义导出格式
1. 继承DocumentDatabase类
2. 重写export_tree_to_markdown方法
3. 实现自定义的格式化逻辑

## 问题反馈

如有问题或建议，请联系开发团队。