#!/bin/bash

# Lumina Docs MCP Server startup script

echo "启动Lumina Docs - 智能结构化文档管理服务器..."

# 加载环境变量（如果 .env 文件存在）
if [ -f ".env" ]; then
    echo "加载环境变量配置文件 .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "安装依赖..."
pip install -e .

# Create sample data if database doesn't exist
if [ ! -f "database/documents.db" ]; then
    echo "创建示例数据..."
    cd examples
    python sample_data.py
    cd ..
fi

echo "启动MCP服务器..."
echo "服务器将通过stdio协议运行"
echo "按 Ctrl+C 停止服务器"

# Start the MCP server
python -m doc_manager