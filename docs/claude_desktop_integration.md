# Claude Desktop 集成指南

本文档说明如何将Document Manager MCP服务器集成到Claude Desktop中。

## 快速安装

### 方法一：自动安装（推荐）
```bash
cd /Users/gaozhaoyun/MCP_test/doc-manager
./install_to_claude_desktop.sh
```

### 方法二：手动配置
1. 打开Claude Desktop配置文件：
   ```bash
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. 添加以下配置：
   ```json
   {
     "mcpServers": {
       "document-manager": {
         "command": "python",
         "args": ["-m", "doc_manager"],
         "cwd": "/Users/gaozhaoyun/MCP_test/doc-manager",
         "env": {
           "PYTHONPATH": "/Users/gaozhaoyun/MCP_test/doc-manager/src"
         }
       }
     }
   }
   ```

3. 重启Claude Desktop

## 验证安装

重启Claude Desktop后，你可以通过以下方式验证服务是否正常：

1. 在聊天中询问："有哪些MCP工具可用？"
2. 应该能看到document-manager相关的工具列表

## 在Claude Desktop中的使用方式

### 1. 查看文档结构
```
帮我查看当前文档的完整树形结构
```

### 2. 查询特定类型的内容
```
查找所有的业务流程说明节点，我想参考它们的格式来写新的业务流程
```

### 3. 创建新节点
```
帮我创建一个新的功能模块：
- 标题：数据分析模块
- 类型：module  
- 父节点ID：3
- 元数据：{"priority": "medium", "complexity": "high"}
```

### 4. 搜索和查询
```
搜索包含"权限"关键词的所有节点
```

### 5. 导出文档
```
将完整的文档导出为Markdown格式
```

### 6. 一致性检查
```
查找所有"数据展示规则"类型的节点，帮我分析它们的格式是否一致
```

## 实际使用场景

### 场景1：保证内容一致性
当你要写新的【业务流程说明】时：
```
我要为新功能写业务流程说明，请先帮我查看现有的所有业务流程说明，分析它们的格式和结构，然后给我一个模板
```

Claude会：
1. 使用`get_nodes_by_type`查询所有业务流程说明
2. 分析现有格式和结构
3. 提供一致的模板供你参考

### 场景2：模块化文档管理
```
帮我查看"总览模块"下的所有子功能，然后为其中的"系统状态统计"功能添加一个新的"性能优化建议"子节点
```

Claude会：
1. 查询特定模块的子节点
2. 创建新的子节点并保持层级关系

### 场景3：按需导出
```
我只需要"功能模块"部分的文档，请帮我导出这部分内容为Markdown格式
```

## 可用的MCP工具

| 工具名称 | 功能说明 | 典型用法 |
|---------|---------|----------|
| `create_node` | 创建新节点 | "创建一个标题为XXX的功能模块" |
| `get_node` | 获取节点详情 | "查看节点ID为5的详细信息" |
| `update_node` | 更新节点 | "更新节点3的内容为XXX" |
| `delete_node` | 删除节点 | "删除节点ID为10的节点" |
| `get_children` | 获取子节点 | "查看节点2的所有子节点" |
| `search_nodes` | 搜索节点 | "搜索包含'权限'的所有节点" |
| `get_nodes_by_type` | 按类型获取 | "获取所有业务流程说明节点" |
| `get_node_path` | 获取节点路径 | "显示节点8的完整路径" |
| `get_tree_structure` | 获取树结构 | "显示完整的文档树结构" |
| `export_to_markdown` | 导出Markdown | "导出完整文档为Markdown" |
| `move_node` | 移动节点 | "将节点5移动到节点3下面" |

## 对话示例

### 示例1：一致性检查
**用户**：我要写一个新的数据展示规则，帮我先查看现有的数据展示规则都是什么格式

**Claude**：我来帮你查看现有的数据展示规则格式。让我先获取所有相关节点。

*[使用get_nodes_by_type工具]*

基于现有的数据展示规则，我发现以下格式模式：
1. 都使用项目符号列表
2. 包含颜色标识说明
3. 提及分页和排序规则
4. 说明交互行为（悬停、点击等）

建议你的新规则也遵循这个格式...

### 示例2：结构化创建
**用户**：帮我在"系统监控模块"下创建一个"告警管理功能"

**Claude**：我来帮你创建这个功能节点。首先让我找到"系统监控模块"的ID。

*[使用search_nodes查找父节点]*
*[使用create_node创建新节点]*

已成功创建"告警管理功能"节点！节点ID为15，位于"系统监控模块"下。

## 故障排除

### 1. 服务无法启动
- 检查Python路径是否正确
- 确保所有依赖已安装
- 查看Claude Desktop的日志

### 2. 工具不可用
- 重启Claude Desktop
- 检查配置文件语法是否正确
- 确认MCP服务器正在运行

### 3. 数据库问题
- 确保database目录存在
- 运行示例数据创建脚本
- 检查文件权限

## 高级配置

### 自定义数据库路径
修改配置文件中的环境变量：
```json
{
  "mcpServers": {
    "document-manager": {
      "env": {
        "PYTHONPATH": "/path/to/src",
        "DOC_DB_PATH": "/custom/path/to/database.db"
      }
    }
  }
}
```

### 多项目支持
可以配置多个document-manager实例：
```json
{
  "mcpServers": {
    "doc-manager-project1": {
      "command": "python",
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/project1"
    },
    "doc-manager-project2": {
      "command": "python", 
      "args": ["-m", "doc_manager"],
      "cwd": "/path/to/project2"
    }
  }
}
```

通过这种方式，你可以在Claude Desktop中直接使用自然语言来管理结构化文档，真正实现了你想要的一致性保证和模块化管理！