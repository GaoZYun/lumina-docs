"""
Consistency checker for document structure.
This script demonstrates the structured query capabilities for maintaining document consistency.
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from doc_manager.database import DocumentDatabase
from typing import List, Dict, Any


class ConsistencyChecker:
    """Check and maintain consistency across document sections."""
    
    def __init__(self, db_path: str = "../database/documents.db"):
        """Initialize consistency checker."""
        self.db = DocumentDatabase(db_path)
    
    def check_business_flow_consistency(self) -> Dict[str, Any]:
        """Check consistency of all business flow descriptions."""
        print("=== 检查业务流程说明的一致性 ===")
        
        # Get all business flow nodes
        business_flows = self.db.get_nodes_by_type("business_flow")
        
        analysis = {
            "total_count": len(business_flows),
            "nodes": [],
            "patterns": {},
            "recommendations": []
        }
        
        print(f"找到 {len(business_flows)} 个业务流程说明：")
        
        for flow in business_flows:
            print(f"\n节点ID: {flow['id']}")
            print(f"标题: {flow['title']}")
            
            # Get parent context
            parent = self.db.get_node(flow['parent_id']) if flow['parent_id'] else None
            if parent:
                print(f"所属功能: {parent['title']}")
            
            # Analyze content structure
            content = flow.get('content', '')
            steps = content.count('\n')
            has_numbers = any(char.isdigit() for char in content[:50])
            
            flow_info = {
                "id": flow['id'],
                "title": flow['title'],
                "parent": parent['title'] if parent else None,
                "step_count": steps,
                "has_numbering": has_numbers,
                "content_length": len(content)
            }
            
            analysis['nodes'].append(flow_info)
            
            print(f"步骤数量: {steps}")
            print(f"是否有编号: {'是' if has_numbers else '否'}")
            print(f"内容长度: {len(content)} 字符")
        
        # Generate recommendations
        if analysis['nodes']:
            avg_steps = sum(node['step_count'] for node in analysis['nodes']) / len(analysis['nodes'])
            analysis['recommendations'].append(f"平均步骤数: {avg_steps:.1f}")
            
            numbered_count = sum(1 for node in analysis['nodes'] if node['has_numbering'])
            if numbered_count != len(analysis['nodes']) and numbered_count > 0:
                analysis['recommendations'].append("建议统一编号格式：所有业务流程都使用数字编号")
        
        return analysis
    
    def check_data_display_rules_consistency(self) -> Dict[str, Any]:
        """Check consistency of data display rules."""
        print("\n=== 检查数据展示规则的一致性 ===")
        
        display_rules = self.db.get_nodes_by_type("data_display_rules")
        
        analysis = {
            "total_count": len(display_rules),
            "nodes": [],
            "common_patterns": [],
            "recommendations": []
        }
        
        print(f"找到 {len(display_rules)} 个数据展示规则：")
        
        # Common keywords to look for
        keywords = ["颜色", "分页", "排序", "筛选", "悬停", "点击"]
        keyword_counts = {keyword: 0 for keyword in keywords}
        
        for rule in display_rules:
            print(f"\n节点ID: {rule['id']}")
            print(f"标题: {rule['title']}")
            
            parent = self.db.get_node(rule['parent_id']) if rule['parent_id'] else None
            if parent:
                print(f"所属功能: {parent['title']}")
            
            content = rule.get('content', '')
            
            # Count keywords
            rule_keywords = []
            for keyword in keywords:
                if keyword in content:
                    keyword_counts[keyword] += 1
                    rule_keywords.append(keyword)
            
            rule_info = {
                "id": rule['id'],
                "title": rule['title'],
                "parent": parent['title'] if parent else None,
                "keywords": rule_keywords,
                "content_length": len(content)
            }
            
            analysis['nodes'].append(rule_info)
            print(f"包含关键词: {', '.join(rule_keywords)}")
        
        # Analyze patterns
        for keyword, count in keyword_counts.items():
            if count > 0:
                percentage = (count / len(display_rules)) * 100
                analysis['common_patterns'].append(f"{keyword}: {count}/{len(display_rules)} ({percentage:.1f}%)")
        
        # Generate recommendations
        if len(display_rules) > 1:
            if keyword_counts["颜色"] != len(display_rules):
                analysis['recommendations'].append("建议所有模块都明确定义颜色标识规则")
            if keyword_counts["分页"] < len(display_rules) // 2:
                analysis['recommendations'].append("考虑为更多列表功能添加分页支持")
        
        return analysis
    
    def check_permission_rules_consistency(self) -> Dict[str, Any]:
        """Check consistency of permission rules."""
        print("\n=== 检查权限控制规则的一致性 ===")
        
        permission_rules = self.db.get_nodes_by_type("permission_rules")
        
        analysis = {
            "total_count": len(permission_rules),
            "nodes": [],
            "common_phrases": [],
            "recommendations": []
        }
        
        print(f"找到 {len(permission_rules)} 个权限控制规则：")
        
        # Common permission-related phrases
        phrases = ["用户权限", "管理员权限", "操作权限", "访问权限", "数据权限"]
        phrase_counts = {phrase: 0 for phrase in phrases}
        
        for rule in permission_rules:
            print(f"\n节点ID: {rule['id']}")
            print(f"标题: {rule['title']}")
            
            parent = self.db.get_node(rule['parent_id']) if rule['parent_id'] else None
            if parent:
                print(f"所属类别: {parent['title']}")
            
            content = rule.get('content', '')
            
            # Count phrases
            rule_phrases = []
            for phrase in phrases:
                if phrase in content:
                    phrase_counts[phrase] += 1
                    rule_phrases.append(phrase)
            
            rule_info = {
                "id": rule['id'],
                "title": rule['title'],
                "parent": parent['title'] if parent else None,
                "phrases": rule_phrases,
                "content_length": len(content)
            }
            
            analysis['nodes'].append(rule_info)
            print(f"包含权限短语: {', '.join(rule_phrases)}")
        
        return analysis
    
    def generate_consistency_report(self) -> str:
        """Generate a comprehensive consistency report."""
        print("\n" + "="*60)
        print("生成一致性检查报告")
        print("="*60)
        
        # Check all types
        business_flow_analysis = self.check_business_flow_consistency()
        display_rules_analysis = self.check_data_display_rules_consistency()
        permission_analysis = self.check_permission_rules_consistency()
        
        # Generate report
        report = f"""
# 文档一致性检查报告

## 业务流程说明一致性
- 总数量: {business_flow_analysis['total_count']}
- 建议: {'; '.join(business_flow_analysis['recommendations'])}

## 数据展示规则一致性
- 总数量: {display_rules_analysis['total_count']}
- 常见模式: {'; '.join(display_rules_analysis['common_patterns'])}
- 建议: {'; '.join(display_rules_analysis['recommendations'])}

## 权限控制规则一致性
- 总数量: {permission_analysis['total_count']}

## 总体建议
1. 统一所有【业务流程说明】的编号格式
2. 保持【数据展示规则】的结构一致性
3. 确保【权限控制规则】覆盖所有功能模块
"""
        
        return report
    
    def find_similar_content_for_new_node(self, node_type: str, parent_context: str = "") -> List[Dict[str, Any]]:
        """Find similar content to help maintain consistency when creating new nodes."""
        print(f"\n=== 为新的 {node_type} 节点查找参考内容 ===")
        
        # Get all existing nodes of the same type
        existing_nodes = self.db.get_nodes_by_type(node_type)
        
        print(f"找到 {len(existing_nodes)} 个相同类型的现有节点：")
        
        references = []
        for node in existing_nodes:
            parent = self.db.get_node(node['parent_id']) if node['parent_id'] else None
            
            reference = {
                "id": node['id'],
                "title": node['title'],
                "parent_title": parent['title'] if parent else None,
                "content": node.get('content', ''),
                "content_preview": node.get('content', '')[:200] + "..." if len(node.get('content', '')) > 200 else node.get('content', '')
            }
            
            references.append(reference)
            
            print(f"\n参考节点 {node['id']}: {node['title']}")
            if parent:
                print(f"  所属: {parent['title']}")
            print(f"  内容预览: {reference['content_preview']}")
        
        if references:
            print(f"\n建议: 新的 {node_type} 节点应该参考以上内容的格式和深度，保持一致性。")
        
        return references


def main():
    """Main function to demonstrate consistency checking."""
    checker = ConsistencyChecker()
    
    # Generate full consistency report
    report = checker.generate_consistency_report()
    print(report)
    
    # Demonstrate finding references for new content
    print("\n" + "="*60)
    print("演示：为新节点查找参考内容")
    print("="*60)
    
    # Example: Finding references for a new business flow
    checker.find_similar_content_for_new_node("business_flow", "新功能模块")
    
    # Example: Finding references for new data display rules
    checker.find_similar_content_for_new_node("data_display_rules", "新功能模块")


if __name__ == "__main__":
    main()