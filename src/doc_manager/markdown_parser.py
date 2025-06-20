#!/usr/bin/env python3
"""
Markdown文档解析和数据库导入模块

该模块提供Markdown文档解析和导入到文档管理系统的功能。
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from glob import glob

from .database import DocumentDatabase


class MarkdownParser:
    """Markdown文档解析器"""
    
    def __init__(self):
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.code_block_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
        self.inline_code_pattern = re.compile(r'`[^`]+`')
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """解析Markdown文件并返回结构化数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件名（不含扩展名）作为文档标题
        filename = Path(file_path).stem
        
        # 解析文档结构
        nodes = self._parse_content(content)
        
        return {
            'filename': filename,
            'title': self._extract_title(content, filename),
            'description': self._extract_description(content),
            'nodes': nodes
        }
    
    def _extract_title(self, content: str, fallback: str) -> str:
        """提取文档标题（第一个一级标题或文件名）"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return fallback
    
    def _extract_description(self, content: str) -> str:
        """提取文档描述（第一个段落或前100个字符）"""
        lines = content.split('\n')
        description_lines = []
        
        in_content = False
        for line in lines:
            line = line.strip()
            
            # 跳过标题行
            if line.startswith('#'):
                in_content = True
                continue
            
            # 如果遇到第二个标题，停止
            if in_content and line.startswith('#'):
                break
            
            # 收集内容行
            if in_content and line:
                description_lines.append(line)
                # 限制描述长度
                if len(' '.join(description_lines)) > 200:
                    break
        
        description = ' '.join(description_lines)
        return description[:200] + '...' if len(description) > 200 else description
    
    def _parse_content(self, content: str) -> List[Dict[str, Any]]:
        """解析文档内容，提取层次结构"""
        lines = content.split('\n')
        nodes = []
        current_sections = {}  # 用于跟踪各级标题的当前节点
        
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # 检查是否是标题行
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line_stripped)
            if heading_match:
                # 如果有积累的内容，添加到上一个节点
                if current_content:
                    self._add_content_to_last_node(nodes, current_sections, current_content)
                    current_content = []
                
                # 解析标题
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                # 创建节点
                node = {
                    'title': title,
                    'content': '',
                    'node_type': f'heading_{level}',
                    'level': level,
                    'parent_id': None,
                    'children': []
                }
                
                # 设置父级关系
                if level > 1:
                    parent_level = level - 1
                    while parent_level >= 1:
                        if parent_level in current_sections:
                            node['parent_id'] = current_sections[parent_level]['id']
                            break
                        parent_level -= 1
                
                # 清理更深层的节点引用
                levels_to_remove = [l for l in current_sections.keys() if l >= level]
                for l in levels_to_remove:
                    del current_sections[l]
                
                # 添加节点到列表
                nodes.append(node)
                
                # 设置临时ID（稍后会被数据库ID替换）
                node['id'] = len(nodes) - 1
                current_sections[level] = node
                
            else:
                # 收集内容行
                if line_stripped:
                    current_content.append(line)
        
        # 处理剩余内容
        if current_content:
            self._add_content_to_last_node(nodes, current_sections, current_content)
        
        return nodes
    
    def _add_content_to_last_node(self, nodes: List[Dict], current_sections: Dict, content_lines: List[str]):
        """将内容添加到最后一个节点"""
        if not nodes:
            return
        
        content = '\n'.join(content_lines).strip()
        if content:
            nodes[-1]['content'] = content


class MarkdownImporter:
    """Markdown文档导入器"""
    
    def __init__(self, db: DocumentDatabase):
        self.db = db
        self.parser = MarkdownParser()
    
    def import_file(self, file_path: str, document_name: Optional[str] = None) -> Dict[str, Any]:
        """导入单个Markdown文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not file_path.lower().endswith('.md'):
            raise ValueError(f"不是Markdown文件: {file_path}")
        
        # 解析文件
        markdown_data = self.parser.parse_file(file_path)
        
        # 使用指定的文档名或文件名
        if document_name:
            markdown_data['filename'] = document_name
        
        # 导入到数据库
        result = self._import_to_database(markdown_data)
        
        return {
            'file_path': file_path,
            'document_name': markdown_data['filename'],
            'table_name': result['table_name'],
            'nodes_created': result['nodes_created'],
            'success': True
        }
    
    def import_batch(self, file_patterns: List[str], skip_errors: bool = True) -> Dict[str, Any]:
        """批量导入Markdown文件"""
        results = []
        total_files = 0
        success_count = 0
        
        # 收集所有匹配的文件
        all_files = []
        for pattern in file_patterns:
            if '*' in pattern:
                matched_files = glob(pattern)
                all_files.extend(matched_files)
            else:
                all_files.append(pattern)
        
        # 去重并过滤
        unique_files = list(set(all_files))
        
        for file_path in unique_files:
            total_files += 1
            
            try:
                result = self.import_file(file_path)
                results.append(result)
                success_count += 1
                
            except Exception as e:
                error_result = {
                    'file_path': file_path,
                    'success': False,
                    'error': str(e)
                }
                results.append(error_result)
                
                if not skip_errors:
                    break
        
        return {
            'total_files': total_files,
            'success_count': success_count,
            'results': results
        }
    
    def _import_to_database(self, markdown_data: Dict[str, Any]) -> Dict[str, Any]:
        """将解析后的数据导入数据库"""
        filename = markdown_data['filename']
        title = markdown_data['title']
        description = markdown_data['description']
        nodes = markdown_data['nodes']
        
        # 创建文档表
        try:
            table_name = self.db.create_document(filename, title, description)
        except ValueError as e:
            if "already exists" in str(e):
                # 如果文档已存在，获取表名
                table_name = self.db.get_document_table_name(filename)
            else:
                raise e
        
        # 导入节点
        node_id_mapping = {}  # 临时ID到真实数据库ID的映射
        nodes_created = 0
        
        for node in nodes:
            # 获取父级ID
            parent_id = None
            if node['parent_id'] is not None:
                parent_id = node_id_mapping.get(node['parent_id'])
            
            # 创建节点
            db_id = self.db.create_node(
                title=node['title'],
                content=node['content'],
                node_type=node['node_type'],
                parent_id=parent_id,
                document_name=filename
            )
            
            # 记录ID映射
            node_id_mapping[node['id']] = db_id
            nodes_created += 1
        
        return {
            'table_name': table_name,
            'nodes_created': nodes_created
        }