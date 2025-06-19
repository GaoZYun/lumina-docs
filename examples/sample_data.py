"""
Sample data for testing the document management system.
This script creates a sample document structure representing an intelligent O&M system requirements document.
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from doc_manager.database import DocumentDatabase


def create_sample_data(db_path: str = "../database/documents.db"):
    """Create sample document structure."""
    db = DocumentDatabase(db_path)
    
    # Clear existing data
    db.clear_all_data()
    
    # Create root document
    root_id = db.create_node(
        title="智能运维系统需求文档",
        node_type="document_root",
        content="基于MCP协议的智能运维系统，通过大语言模型作为核心智能引擎，实现对被监控系统的主动指标采集、状态判断、日志分析、故障诊断及知识沉淀。"
    )
    
    # Create main sections
    overview_id = db.create_node(
        title="项目概述",
        node_type="section",
        parent_id=root_id,
        content="系统背景、架构概述和核心特性介绍"
    )
    
    requirements_id = db.create_node(
        title="需求说明",
        node_type="section", 
        parent_id=root_id,
        content="详细的功能需求和非功能需求说明"
    )
    
    modules_id = db.create_node(
        title="功能模块",
        node_type="section",
        parent_id=root_id
    )
    
    permissions_id = db.create_node(
        title="权限设计",
        node_type="section",
        parent_id=root_id
    )
    
    architecture_id = db.create_node(
        title="技术架构",
        node_type="section",
        parent_id=root_id
    )
    
    # Create functional modules
    overview_module_id = db.create_node(
        title="总览模块",
        node_type="module",
        parent_id=modules_id,
        metadata={"module_type": "frontend", "priority": "high"}
    )
    
    monitoring_module_id = db.create_node(
        title="系统监控模块", 
        node_type="module",
        parent_id=modules_id,
        metadata={"module_type": "frontend", "priority": "high"}
    )
    
    mcp_center_id = db.create_node(
        title="MCP中心模块",
        node_type="module", 
        parent_id=modules_id,
        metadata={"module_type": "backend", "priority": "medium"}
    )
    
    # Add detailed content for overview module
    system_stats_id = db.create_node(
        title="系统状态统计功能",
        node_type="feature",
        parent_id=overview_module_id,
        content="以卡片形式展示全部业务系统整体运行状态的核心统计数据。"
    )
    
    # Add business flow description
    db.create_node(
        title="业务流程说明",
        node_type="business_flow",
        parent_id=system_stats_id,
        content="""
1. 从i6000系统获取系统清单及系统告警信息
2. 通过MCP中心调度Prometheus MCP服务器采集系统指标
3. 计算总系统数量、异常系统数量、故障系统数量
4. 生成状态分布饼图展示正常/告警/故障系统比例
"""
    )
    
    # Add data display rules
    db.create_node(
        title="数据展示规则",
        node_type="data_display_rules",
        parent_id=system_stats_id,
        content="""
- 状态分布饼图支持点击查看详情
- 支持hover显示具体百分比
- 实时统计，数据随页面刷新
- 不同状态使用不同颜色标识（绿色正常、黄色异常、红色故障）
"""
    )
    
    # Add similar structure for monitoring module
    system_list_id = db.create_node(
        title="系统列表功能",
        node_type="feature",
        parent_id=monitoring_module_id,
        content="以卡片网格形式展示所有纳入监控的系统，支持筛选、搜索、状态查看和智能分析操作。"
    )
    
    db.create_node(
        title="业务流程说明", 
        node_type="business_flow",
        parent_id=system_list_id,
        content="""
1. 从i6000系统获取完整的系统清单
2. MCP中心调度Prometheus MCP服务器采集CPU、内存、磁盘数据
3. 从i6000系统获取各系统的当前告警信息
4. 查询最近的巡检执行记录
5. 将多源数据聚合后在卡片中展示
"""
    )
    
    db.create_node(
        title="数据展示规则",
        node_type="data_display_rules", 
        parent_id=system_list_id,
        content="""
- 系统按注册时间倒序排列
- 不同状态使用不同颜色标识
- 支持分页显示，默认每页显示10条记录
- 卡片悬停时高亮显示
- 根据屏幕尺寸自动调整卡片网格布局
"""
    )
    
    # Add permission designs
    user_permissions_id = db.create_node(
        title="用户权限",
        node_type="permission_rule",
        parent_id=permissions_id,
        metadata={"scope": "user"}
    )
    
    db.create_node(
        title="权限控制规则",
        node_type="permission_rules",
        parent_id=user_permissions_id,
        content="""
- 用户只能查看有权限的系统信息
- 操作权限根据用户角色进行控制
- 敏感系统信息需要特殊权限
- 巡检执行和周期配置需要相应操作权限
"""
    )
    
    data_permissions_id = db.create_node(
        title="数据权限",
        node_type="permission_rule",
        parent_id=permissions_id,
        metadata={"scope": "data"}
    )
    
    db.create_node(
        title="权限控制规则",
        node_type="permission_rules", 
        parent_id=data_permissions_id,
        content="""
- 报告下载需要数据导出权限
- AI生成的建议和评分对所有有权限用户可见
- 配置变更需要管理员权限
- 服务删除需要超级管理员权限
"""
    )
    
    # Add technical architecture
    db.create_node(
        title="系统架构设计",
        node_type="architecture_design",
        parent_id=architecture_id,
        content="""
系统基于MCP协议的数据采集架构：
用户 → 大语言模型 → MCP中心 → MCP服务器 → Prometheus/Elasticsearch/MySQL

核心组件：
1. 大语言模型：系统的智能核心
2. MCP中心：协调数据采集和处理任务  
3. MCP服务器：负责具体的数据采集
4. 数据源网关：统一的数据接入点
5. 知识库：存储运维知识和经验
"""
    )
    
    print(f"Sample data created successfully!")
    print(f"Root document ID: {root_id}")
    print(f"Database location: {db_path}")
    
    # Display the tree structure
    print("\nDocument Structure:")
    tree = db.get_tree_structure()
    print_tree(tree, 0)


def print_tree(nodes: list, indent: int) -> None:
    """Print tree structure."""
    for node in nodes:
        print("  " * indent + f"├─ {node['title']} (ID: {node['id']}, Type: {node['node_type']})")
        if 'children' in node and node['children']:
            print_tree(node['children'], indent + 1)


if __name__ == "__main__":
    create_sample_data()