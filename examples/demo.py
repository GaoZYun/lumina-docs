"""
Demo script showing how to use the document management system.
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from doc_manager.database import DocumentDatabase


def demo_basic_operations():
    """Demonstrate basic CRUD operations."""
    print("=== 基本操作演示 ===")
    
    # Initialize database
    db = DocumentDatabase("../database/demo.db")
    
    # Clear existing data for clean demo
    db.clear_all_data()
    
    # 1. Create root document
    print("\n1. 创建根文档")
    root_id = db.create_node(
        title="产品需求文档",
        node_type="document_root",
        content="这是一个产品需求文档的根节点"
    )
    print(f"创建根文档，ID: {root_id}")
    
    # 2. Create sections
    print("\n2. 创建章节")
    overview_id = db.create_node(
        title="产品概述",
        node_type="section",
        parent_id=root_id,
        content="产品的基本介绍和定位"
    )
    
    features_id = db.create_node(
        title="功能需求", 
        node_type="section",
        parent_id=root_id
    )
    
    print(f"创建概述章节，ID: {overview_id}")
    print(f"创建功能需求章节，ID: {features_id}")
    
    # 3. Create features
    print("\n3. 创建具体功能")
    user_mgmt_id = db.create_node(
        title="用户管理功能",
        node_type="feature",
        parent_id=features_id,
        content="用户注册、登录、权限管理等功能",
        metadata={"priority": "high", "complexity": "medium"}
    )
    
    # 4. Add business flow
    print("\n4. 添加业务流程")
    flow_id = db.create_node(
        title="业务流程说明",
        node_type="business_flow", 
        parent_id=user_mgmt_id,
        content="""
1. 用户访问注册页面
2. 填写基本信息并验证
3. 系统创建用户账户
4. 发送确认邮件
5. 用户激活账户
"""
    )
    
    print(f"创建业务流程，ID: {flow_id}")
    
    # 5. Show tree structure
    print("\n5. 显示文档树结构")
    tree = db.get_tree_structure()
    print_tree(tree, 0)
    
    return db


def demo_structured_queries():
    """Demonstrate structured query capabilities."""
    print("\n=== 结构化查询演示 ===")
    
    # Use the database from basic demo
    db = DocumentDatabase("../database/demo.db")
    
    # 1. Search by type
    print("\n1. 按类型查询")
    features = db.get_nodes_by_type("feature")
    print(f"找到 {len(features)} 个功能节点:")
    for feature in features:
        print(f"  - {feature['title']} (ID: {feature['id']})")
    
    # 2. Search by content
    print("\n2. 按内容搜索")
    results = db.search_nodes(query="用户")
    print(f"包含'用户'的节点:")
    for result in results:
        print(f"  - {result['title']} (类型: {result['node_type']})")
    
    # 3. Search by metadata
    print("\n3. 按元数据搜索")
    high_priority = db.search_nodes(metadata_filter={"priority": "high"})
    print(f"高优先级节点:")
    for node in high_priority:
        print(f"  - {node['title']}")
    
    # 4. Get node path
    print("\n4. 获取节点路径")
    flow_nodes = db.get_nodes_by_type("business_flow")
    if flow_nodes:
        path = db.get_node_path(flow_nodes[0]['id'])
        print("业务流程节点的完整路径:")
        for i, node in enumerate(path):
            indent = "  " * i
            print(f"{indent}- {node['title']} ({node['node_type']})")


def demo_consistency_checking():
    """Demonstrate consistency checking for content creation."""
    print("\n=== 一致性检查演示 ===")
    
    db = DocumentDatabase("../database/demo.db")
    
    # Add more business flows to demonstrate consistency
    features = db.get_nodes_by_type("feature")
    if features:
        feature_id = features[0]['id']
        
        # Add another business flow with similar structure
        db.create_node(
            title="业务流程说明",
            node_type="business_flow",
            parent_id=feature_id,
            content="""
1. 管理员登录系统
2. 进入用户管理界面
3. 查看用户列表
4. 执行用户管理操作
"""
        )
    
    # Now check consistency
    print("\n检查业务流程的一致性:")
    business_flows = db.get_nodes_by_type("business_flow")
    
    print(f"找到 {len(business_flows)} 个业务流程:")
    
    for flow in business_flows:
        parent = db.get_node(flow['parent_id'])
        content = flow.get('content', '')
        step_count = content.count('\n')
        
        print(f"\n流程: {flow['title']}")
        print(f"所属功能: {parent['title'] if parent else '无'}")
        print(f"步骤数量: {step_count}")
        print(f"内容预览: {content.strip()[:50]}...")
    
    print("\n一致性建议:")
    print("- 所有业务流程都使用了数字编号格式 ✓")
    print("- 步骤描述保持简洁明确 ✓")
    print("- 建议统一步骤数量在3-7步之间")


def demo_markdown_export():
    """Demonstrate Markdown export functionality."""
    print("\n=== Markdown导出演示 ===")
    
    db = DocumentDatabase("../database/demo.db")
    
    # Export complete document
    print("\n导出完整文档:")
    markdown = db.export_tree_to_markdown()
    
    # Save to file
    output_file = "demo_export.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"文档已导出到: {output_file}")
    
    # Show preview
    print("\n文档预览:")
    lines = markdown.split('\n')
    for i, line in enumerate(lines[:20]):  # Show first 20 lines
        print(line)
    
    if len(lines) > 20:
        print(f"\n... (共 {len(lines)} 行，已省略)")


def print_tree(nodes: list, indent: int) -> None:
    """Print tree structure with indentation."""
    for node in nodes:
        print("  " * indent + f"├─ {node['title']} (ID: {node['id']}, 类型: {node['node_type']})")
        if 'children' in node and node['children']:
            print_tree(node['children'], indent + 1)


def main():
    """Run all demos."""
    print("基于MCP的结构化需求文档管理系统 - 功能演示")
    print("=" * 60)
    
    # Run demos
    db = demo_basic_operations()
    demo_structured_queries()
    demo_consistency_checking()
    demo_markdown_export()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n下一步:")
    print("1. 查看生成的 demo_export.md 文件")
    print("2. 运行 'python consistency_checker.py' 进行一致性检查")
    print("3. 尝试使用命令行工具: 'python -m doc_manager.cli tree --db ../database/demo.db'")


if __name__ == "__main__":
    main()