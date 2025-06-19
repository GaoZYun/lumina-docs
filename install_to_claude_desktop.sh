#!/bin/bash

# 安装Lumina Docs到Claude Desktop的脚本

echo "正在配置Lumina Docs MCP服务器到Claude Desktop..."

# Claude Desktop配置文件路径
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# 创建配置目录（如果不存在）
mkdir -p "$CLAUDE_CONFIG_DIR"

# 备份现有配置
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "备份现有配置到: $CLAUDE_CONFIG_FILE.backup"
    cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup"
fi

# 获取当前项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "项目路径: $PROJECT_DIR"

# 检查是否已有配置文件
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "检测到现有配置，将合并lumina-docs服务..."
    # 使用Python来合并JSON配置
    python3 - << EOF
import json
import os

config_file = "$CLAUDE_CONFIG_FILE"
project_dir = "$PROJECT_DIR"

# 读取现有配置
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {"mcpServers": {}}

# 确保mcpServers存在
if "mcpServers" not in config:
    config["mcpServers"] = {}

# 添加lumina-docs配置
config["mcpServers"]["lumina-docs"] = {
    "command": "python",
    "args": ["-m", "doc_manager"],
    "cwd": project_dir,
    "env": {
        "PYTHONPATH": f"{project_dir}/src",
        "DOC_MANAGER_DB_PATH": f"{project_dir}/database/documents.db",
        "DOC_MANAGER_EXPORT_DIR": f"{os.path.expanduser('~/Desktop')}",
        "DOC_MANAGER_DATA_DIR": project_dir,
        "LUMINA_DOCS_SERVER_NAME": "lumina-docs",
        "DOC_MANAGER_DEBUG": "false",
        "DOC_MANAGER_LOG_LEVEL": "INFO"
    }
}

# 写回配置文件
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("配置已合并")
EOF
else
    # 创建新的配置文件
    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "lumina-docs": {
      "command": "python",
      "args": [
        "-m",
        "doc_manager"
      ],
      "cwd": "$PROJECT_DIR",
      "env": {
        "PYTHONPATH": "$PROJECT_DIR/src",
        "DOC_MANAGER_DB_PATH": "$PROJECT_DIR/database/documents.db",
        "DOC_MANAGER_EXPORT_DIR": "$HOME/Desktop",
        "DOC_MANAGER_DATA_DIR": "$PROJECT_DIR",
        "LUMINA_DOCS_SERVER_NAME": "lumina-docs",
        "DOC_MANAGER_DEBUG": "false",
        "DOC_MANAGER_LOG_LEVEL": "INFO"
      }
    }
  }
}
EOF
fi

echo "配置文件已创建: $CLAUDE_CONFIG_FILE"

# 检查是否需要安装依赖
if [ ! -f "$PROJECT_DIR/src/doc_manager/__init__.py" ]; then
    echo "错误: 项目文件不完整，请确保在正确的目录运行此脚本"
    exit 1
fi

# 创建示例数据（如果数据库不存在）
if [ ! -f "$PROJECT_DIR/database/documents.db" ]; then
    echo "创建示例数据..."
    cd "$PROJECT_DIR/examples"
    python sample_data.py
    cd "$PROJECT_DIR"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步操作："
echo "1. 重启Claude Desktop应用"
echo "2. 在Claude Desktop中，你将看到lumina-docs服务可用"
echo "3. 你可以使用以下工具："
echo ""
echo "   文档管理工具："
echo "   - create_document: 创建新文档"
echo "   - get_documents_list: 获取文档列表" 
echo "   - delete_document: 删除文档"
echo ""
echo "   节点管理工具："
echo "   - create_node: 创建新节点"
echo "   - get_node: 获取节点信息"
echo "   - update_node: 更新节点"
echo "   - delete_node: 删除节点"
echo "   - move_node: 移动节点"
echo ""
echo "   查询和导出工具："
echo "   - search_nodes: 搜索节点"
echo "   - get_nodes_by_type: 按类型获取节点"
echo "   - get_children: 获取子节点"
echo "   - get_tree_structure: 获取树结构"
echo "   - get_node_path: 获取节点路径"
echo "   - export_to_markdown: 导出为Markdown"
echo ""
echo "示例对话:"
echo "\"创建一个新文档，名称为'api-docs'，标题为'API文档'\""
echo "\"查看当前有哪些文档\""
echo "\"在api-docs文档中创建一个标题为'用户管理'的章节\""
echo "\"搜索包含'API'的所有节点\""
echo "\"导出api-docs文档为Markdown格式\""
echo ""
echo "配置文件位置: $CLAUDE_CONFIG_FILE"