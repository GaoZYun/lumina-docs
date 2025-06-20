#!/usr/bin/env python3
"""
Lumina Docs - Intelligent Document Management MCP Server using FastMCP.
"""
import json
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from .database import DocumentDatabase
from .config import config
from .markdown_parser import MarkdownImporter

# Initialize the database
db = DocumentDatabase()

# Initialize Markdown importer
markdown_importer = MarkdownImporter(db)

# Create MCP server
mcp = FastMCP(config.get_server_name())

@mcp.tool()
def create_document(
    document_name: str,
    title: str,
    description: Optional[str] = None
) -> str:
    """创建一个新文档，每个文档会有独立的数据表存储其内容节点。
    
    参数：
    - document_name: 文档的唯一标识名称，会用于生成表名（只能包含字母数字和下划线）
    - title: 文档的显示标题
    - description: 可选的文档描述信息
    
    用途：当你需要开始一个新的文档项目时使用，比如创建技术文档、产品手册、会议记录等。
    每个文档都有独立的存储空间，互不干扰。"""
    try:
        table_name = db.create_document(
            document_name=document_name,
            title=title,
            description=description
        )
        return f"Successfully created document '{document_name}'\nTitle: {title}\nTable: {table_name}\nDescription: {description or 'None'}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to create document: {str(e)}"

@mcp.tool()
def get_documents_list() -> str:
    """获取系统中所有文档的列表和基本信息。
    
    返回信息包括：
    - 文档ID和名称
    - 文档标题和描述
    - 创建和更新时间
    - 对应的数据表名
    
    用途：查看当前系统中有哪些文档，选择要操作的文档，或者了解文档的基本信息。"""
    try:
        documents = db.get_documents_list()
        if not documents:
            return "No documents found."
        return json.dumps(documents, indent=2, default=str)
    except Exception as e:
        return f"Failed to get documents list: {str(e)}"

@mcp.tool()
def create_node(
    title: str, 
    node_type: str, 
    content: Optional[str] = None,
    parent_id: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
    sort_order: Optional[int] = None,
    document_name: Optional[str] = None
) -> str:
    """在指定文档中创建新的内容节点（章节、段落、列表项等）。
    
    参数：
    - title: 节点标题（必需）
    - node_type: 节点类型，如 'chapter'、'section'、'paragraph'、'list_item' 等
    - content: 节点的具体内容（可选）
    - parent_id: 父节点ID，用于建立层级关系（可选，不填则为根节点）
    - metadata: 附加元数据，JSON格式（可选）
    - sort_order: 在同级节点中的排序位置（可选，自动计算）
    - document_name: 目标文档名称（可选，不填则使用默认表）
    
    用途：构建文档的层级结构，添加章节、段落等内容单元。"""
    try:
        node_id = db.create_node(
            title=title,
            node_type=node_type,
            content=content,
            parent_id=parent_id,
            metadata=metadata,
            sort_order=sort_order,
            document_name=document_name
        )
        doc_info = f" in document '{document_name}'" if document_name else " in default table"
        return f"Successfully created node with ID: {node_id}{doc_info}\nTitle: {title}\nType: {node_type}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to create node: {str(e)}"

@mcp.tool()
def get_node(node_id: int, document_name: Optional[str] = None) -> str:
    """根据节点ID获取指定节点的完整信息。
    
    参数：
    - node_id: 要获取的节点ID
    - document_name: 文档名称（可选，不填则从默认表查找）
    
    返回信息包括：
    - 节点的标题、内容、类型
    - 层级关系（父节点ID、层级深度）
    - 排序位置和元数据
    - 创建和更新时间
    
    用途：查看特定节点的详细信息，检查节点属性。"""
    try:
        node = db.get_node(node_id, document_name)
        if not node:
            doc_info = f" in document '{document_name}'" if document_name else " in default table"
            return f"Node with ID {node_id} not found{doc_info}."
        return json.dumps(node, indent=2, default=str)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to get node: {str(e)}"

@mcp.tool()
def update_node(
    node_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """更新现有节点的内容信息。
    
    参数：
    - node_id: 要更新的节点ID（必需）
    - title: 新的标题（可选，不填则不更新）
    - content: 新的内容（可选，不填则不更新）
    - metadata: 新的元数据（可选，不填则不更新）
    
    用途：修改节点的标题、内容或元数据信息。更新时间会自动更新。
    注意：不能通过此方法更改节点的层级关系或类型。"""
    success = db.update_node(
        node_id=node_id,
        title=title,
        content=content,
        metadata=metadata
    )
    if success:
        return f"Successfully updated node {node_id}"
    else:
        return f"Failed to update node {node_id} - node may not exist"

@mcp.tool()
def delete_node(node_id: int) -> str:
    """删除指定的节点及其所有子节点。
    
    参数：
    - node_id: 要删除的节点ID
    
    注意：此操作会级联删除该节点下的所有子节点，不可恢复！
    
    用途：移除不需要的文档章节或段落。删除父节点时，其下所有子节点也会被删除。"""
    success = db.delete_node(node_id)
    if success:
        return f"Successfully deleted node {node_id} and all its children"
    else:
        return f"Failed to delete node {node_id} - node may not exist"

@mcp.tool()
def get_children(parent_id: Optional[int] = None, document_name: Optional[str] = None) -> str:
    """获取指定节点的直接子节点列表。
    
    参数：
    - parent_id: 父节点ID（可选，不填则获取根节点）
    - document_name: 文档名称（可选，不填则从默认表查找）
    
    返回信息：
    - 按排序顺序返回所有直接子节点
    - 每个子节点的基本信息（ID、标题、类型等）
    
    用途：查看文档的层级结构，浏览某个章节下的所有小节。"""
    try:
        children = db.get_children(parent_id, document_name)
        return json.dumps(children, indent=2, default=str)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to get children: {str(e)}"

@mcp.tool()
def search_nodes(
    query: str = "",
    node_type: Optional[str] = None,
    metadata_filter: Optional[Dict[str, Any]] = None,
    document_name: Optional[str] = None
) -> str:
    """在指定文档或所有文档中搜索节点内容。
    
    参数：
    - query: 搜索关键词，会在节点标题和内容中进行模糊匹配（可选）
    - node_type: 按节点类型过滤，如 'chapter'、'section'、'paragraph' 等（可选）
    - metadata_filter: 按元数据键值对过滤，如 {'author': 'John', 'status': 'draft'}（可选）
    - document_name: 指定搜索的文档名称（可选，不填则搜索默认表）
    
    用途：快速找到包含特定内容的节点，支持全文搜索、类型筛选和元数据过滤。
    搜索结果按层级和排序顺序返回。"""
    try:
        results = db.search_nodes(
            query=query,
            node_type=node_type,
            metadata_filter=metadata_filter,
            document_name=document_name
        )
        return json.dumps(results, indent=2, default=str)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to search nodes: {str(e)}"

@mcp.tool()
def get_nodes_by_type(node_type: str, document_name: Optional[str] = None) -> str:
    """获取指定类型的所有节点，用于一致性分析和批量操作。
    
    参数：
    - node_type: 节点类型，如 'chapter'、'section'、'paragraph'、'image'、'table' 等
    - document_name: 文档名称（可选，不填则从默认表查找）
    
    返回信息：
    - 所有匹配类型的节点列表
    - 按层级和排序顺序排列
    
    用途：分析文档结构，检查特定类型节点的一致性，或对同类型节点进行批量处理。
    例如：查看所有章节标题的命名规范，或找出所有图片节点。"""
    try:
        nodes = db.get_nodes_by_type(node_type, document_name)
        return json.dumps(nodes, indent=2, default=str)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to get nodes by type: {str(e)}"

@mcp.tool()
def get_node_path(node_id: int) -> str:
    """获取从根节点到指定节点的完整路径。
    
    参数：
    - node_id: 目标节点的ID
    
    返回信息：
    - 从根节点到目标节点的完整路径链
    - 每个路径节点的标题、类型和层级信息
    
    用途：了解节点在文档中的位置，生成面包屑导航，或分析节点的层级关系。
    对于深层嵌套的节点特别有用。"""
    path = db.get_node_path(node_id)
    return json.dumps(path, indent=2, default=str)

@mcp.tool()
def get_tree_structure(parent_id: Optional[int] = None, document_name: Optional[str] = None) -> str:
    """获取完整的文档树状结构，包含所有层级关系。
    
    参数：
    - parent_id: 起始节点ID（可选，不填则从根节点开始）
    - document_name: 文档名称（可选，不填则从默认表获取）
    
    返回信息：
    - 嵌套的树状结构，包含所有子节点
    - 每个节点包含其完整信息和子节点列表
    
    用途：查看文档的完整结构，生成目录，或导出整个文档层级。
    适合需要了解文档全貌的场景。"""
    try:
        tree = db.get_tree_structure(parent_id, document_name)
        return json.dumps(tree, indent=2, default=str)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Failed to get tree structure: {str(e)}"

@mcp.tool()
def export_to_markdown(filename: Optional[str] = None, parent_id: Optional[int] = None, start_level: int = 1, document_name: Optional[str] = None) -> str:
    """将文档树导出为Markdown格式并保存到指定目录。
    
    参数：
    - filename: 输出文件名（可选，不填则自动生成带时间戳的文件名）
    - parent_id: 导出的起始节点ID（可选，不填则从根节点开始）
    - start_level: Markdown标题的起始级别，1表示#，2表示##（默认为1）
    - document_name: 源文档名称（可选，不填则从默认表导出）
    
    输出：
    - 在配置的导出目录创建.md文件
    - 节点层级转换为Markdown标题层级
    - 节点内容保持原格式
    
    用途：将结构化文档导出为标准Markdown格式，便于分享、发布或进一步编辑。"""
    import os
    from datetime import datetime
    
    try:
        # 生成 markdown 内容
        markdown = db.export_tree_to_markdown(parent_id, start_level, document_name)
        
        # 确定文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_suffix = f"_{document_name}" if document_name else ""
            filename = f"document_export{doc_suffix}_{timestamp}.md"
        
        # 确保文件名以 .md 结尾
        if not filename.endswith('.md'):
            filename += '.md'
        
        # 获取导出目录路径
        export_path = config.get_export_directory()
        file_path = os.path.join(export_path, filename)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        doc_info = f" from document '{document_name}'" if document_name else " from default table"
        return f"文档已成功导出{doc_info}：{filename}\n路径：{file_path}\n\n内容预览：\n{markdown[:200]}..."
    
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"导出失败：{str(e)}"

@mcp.tool()
def move_node(node_id: int, new_parent_id: Optional[int] = None) -> str:
    """将节点移动到新的父节点下，重新组织文档结构。
    
    参数：
    - node_id: 要移动的节点ID
    - new_parent_id: 新的父节点ID（可选，不填则移动到根级别）
    
    操作：
    - 自动调整节点的层级深度
    - 递归更新所有子节点的层级
    - 保持节点内容不变
    
    用途：重新组织文档结构，调整章节顺序，或将内容移动到不同的章节下。
    注意：移动操作会影响节点及其所有子节点的层级关系。"""
    success = db.move_node(node_id, new_parent_id)
    if success:
        return f"Successfully moved node {node_id} to new parent {new_parent_id}"
    else:
        return f"Failed to move node {node_id} - node or parent may not exist"

@mcp.tool()
def delete_document(document_name: str) -> str:
    """删除整个文档及其对应的数据表。
    
    参数：
    - document_name: 要删除的文档名称
    
    警告：此操作将永久删除文档及其包含的所有节点数据，不可恢复！
    
    操作内容：
    - 删除文档的数据表
    - 从文档元数据表中移除记录
    - 清理相关的索引和触发器
    
    用途：清理不再需要的文档，释放存储空间。请在执行前确认文档确实不再需要。"""
    try:
        success = db.delete_document(document_name)
        if success:
            return f"Successfully deleted document '{document_name}'"
        else:
            return f"Document '{document_name}' not found"
    except Exception as e:
        return f"Failed to delete document: {str(e)}"

@mcp.tool()
def import_markdown_file(
    file_path: str,
    document_name: Optional[str] = None
) -> str:
    """将Markdown文件解析并导入到文档管理系统中。
    
    参数：
    - file_path: Markdown文件路径（必需）
    - document_name: 目标文档名称（可选，默认使用文件名）
    
    功能：
    - 自动解析标题层次结构（#、##、###等）
    - 提取文档标题和描述
    - 保持内容的层级关系
    - 创建对应的节点结构
    
    用途：导入单个Markdown文档，保持原有结构和层次关系。"""
    try:
        result = markdown_importer.import_file(file_path, document_name)
        
        return f"✓ 成功导入文档: {result['document_name']}\n" \
               f"表名: {result['table_name']}\n" \
               f"创建节点数: {result['nodes_created']}\n" \
               f"文件路径: {result['file_path']}"
               
    except FileNotFoundError as e:
        return f"错误：文件不存在 - {str(e)}"
    except ValueError as e:
        return f"错误：{str(e)}"
    except Exception as e:
        return f"导入失败：{str(e)}"

@mcp.tool()
def import_markdown_batch(
    file_patterns: List[str],
    skip_errors: bool = True
) -> str:
    """批量导入多个Markdown文件到文档管理系统中。
    
    参数：
    - file_patterns: 文件路径模式列表，支持通配符如["docs/*.md"]（必需）
    - skip_errors: 遇到错误时是否继续处理其他文件（默认True）
    
    功能：
    - 支持通配符模式匹配文件
    - 每个文件创建独立文档
    - 自动跳过非Markdown文件
    - 提供处理结果摘要
    
    用途：批量导入文档目录或多个相关文档到系统中。"""
    try:
        result = markdown_importer.import_batch(file_patterns, skip_errors)
        
        # 构建结果摘要
        summary = f"=== 批量导入完成 ===\n"
        summary += f"总文件数: {result['total_files']}\n"
        summary += f"成功导入: {result['success_count']}\n"
        summary += f"失败数量: {result['total_files'] - result['success_count']}\n\n"
        
        # 显示每个文件的结果
        for file_result in result['results']:
            if file_result['success']:
                summary += f"✓ {file_result['file_path']} -> {file_result['document_name']} ({file_result['nodes_created']} 节点)\n"
            else:
                summary += f"✗ {file_result['file_path']}: {file_result['error']}\n"
        
        return summary
        
    except Exception as e:
        return f"批量导入失败：{str(e)}"

if __name__ == "__main__":
    mcp.run()