"""
Command-line interface for document management.
"""
import argparse
import json
import sys
from typing import Optional, Dict, Any

from .database import DocumentDatabase


class DocumentManagerCLI:
    """Command-line interface for document management."""
    
    def __init__(self, db_path: str = "database/documents.db"):
        """Initialize CLI with database path."""
        self.db = DocumentDatabase(db_path)
    
    def create_node(self, title: str, node_type: str, 
                   content: Optional[str] = None,
                   parent_id: Optional[int] = None,
                   metadata: Optional[str] = None) -> None:
        """Create a new document node."""
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON metadata: {metadata}")
                return
        
        node_id = self.db.create_node(
            title=title,
            node_type=node_type,
            content=content,
            parent_id=parent_id,
            metadata=metadata_dict
        )
        
        print(f"Created node with ID: {node_id}")
        print(f"Title: {title}")
        print(f"Type: {node_type}")
        if parent_id:
            print(f"Parent ID: {parent_id}")
    
    def get_node(self, node_id: int) -> None:
        """Get and display a document node."""
        node = self.db.get_node(node_id)
        if node:
            print(json.dumps(node, indent=2, default=str))
        else:
            print(f"Node with ID {node_id} not found.")
    
    def update_node(self, node_id: int, 
                   title: Optional[str] = None,
                   content: Optional[str] = None,
                   metadata: Optional[str] = None) -> None:
        """Update an existing document node."""
        metadata_dict = None
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON metadata: {metadata}")
                return
        
        success = self.db.update_node(
            node_id=node_id,
            title=title,
            content=content,
            metadata=metadata_dict
        )
        
        if success:
            print(f"Successfully updated node {node_id}")
        else:
            print(f"Failed to update node {node_id} - node may not exist")
    
    def delete_node(self, node_id: int) -> None:
        """Delete a document node."""
        success = self.db.delete_node(node_id)
        if success:
            print(f"Successfully deleted node {node_id} and all its children")
        else:
            print(f"Failed to delete node {node_id} - node may not exist")
    
    def list_children(self, parent_id: Optional[int] = None) -> None:
        """List direct children of a node."""
        children = self.db.get_children(parent_id)
        if children:
            print(f"Children of node {parent_id if parent_id else 'root'}:")
            for child in children:
                print(f"  ID: {child['id']}, Title: {child['title']}, Type: {child['node_type']}")
        else:
            print(f"No children found for node {parent_id if parent_id else 'root'}")
    
    def search_nodes(self, query: str = "", node_type: Optional[str] = None) -> None:
        """Search document nodes."""
        results = self.db.search_nodes(query=query, node_type=node_type)
        if results:
            print(f"Found {len(results)} matching nodes:")
            for node in results:
                print(f"  ID: {node['id']}, Title: {node['title']}, Type: {node['node_type']}")
        else:
            print("No matching nodes found.")
    
    def show_tree(self, parent_id: Optional[int] = None) -> None:
        """Display tree structure."""
        tree = self.db.get_tree_structure(parent_id)
        self._print_tree(tree, 0)
    
    def _print_tree(self, nodes: list, indent: int) -> None:
        """Recursively print tree structure."""
        for node in nodes:
            print("  " * indent + f"├─ {node['title']} (ID: {node['id']}, Type: {node['node_type']})")
            if 'children' in node and node['children']:
                self._print_tree(node['children'], indent + 1)
    
    def export_markdown(self, parent_id: Optional[int] = None, output_file: Optional[str] = None) -> None:
        """Export document tree to Markdown."""
        markdown = self.db.export_tree_to_markdown(parent_id)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Exported to {output_file}")
        else:
            print(markdown)
    
    def get_nodes_by_type(self, node_type: str) -> None:
        """Get all nodes of a specific type."""
        nodes = self.db.get_nodes_by_type(node_type)
        if nodes:
            print(f"Found {len(nodes)} nodes of type '{node_type}':")
            for node in nodes:
                print(f"  ID: {node['id']}, Title: {node['title']}")
                if node.get('content'):
                    # Show first 100 characters of content
                    content_preview = node['content'][:100]
                    if len(node['content']) > 100:
                        content_preview += "..."
                    print(f"    Content: {content_preview}")
        else:
            print(f"No nodes found of type '{node_type}'")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Document Manager CLI")
    parser.add_argument("--db", default="database/documents.db", help="Database file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create node command
    create_parser = subparsers.add_parser("create", help="Create a new document node")
    create_parser.add_argument("title", help="Node title")
    create_parser.add_argument("node_type", help="Node type")
    create_parser.add_argument("--content", help="Node content")
    create_parser.add_argument("--parent-id", type=int, help="Parent node ID")
    create_parser.add_argument("--metadata", help="Metadata as JSON string")
    
    # Get node command
    get_parser = subparsers.add_parser("get", help="Get a document node")
    get_parser.add_argument("node_id", type=int, help="Node ID")
    
    # Update node command
    update_parser = subparsers.add_parser("update", help="Update a document node")
    update_parser.add_argument("node_id", type=int, help="Node ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--content", help="New content")
    update_parser.add_argument("--metadata", help="New metadata as JSON string")
    
    # Delete node command
    delete_parser = subparsers.add_parser("delete", help="Delete a document node")
    delete_parser.add_argument("node_id", type=int, help="Node ID")
    
    # List children command
    list_parser = subparsers.add_parser("list", help="List children of a node")
    list_parser.add_argument("--parent-id", type=int, help="Parent node ID (omit for root nodes)")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search document nodes")
    search_parser.add_argument("--query", help="Search query")
    search_parser.add_argument("--type", help="Node type filter")
    
    # Tree command
    tree_parser = subparsers.add_parser("tree", help="Show tree structure")
    tree_parser.add_argument("--parent-id", type=int, help="Root node ID (omit for complete tree)")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export to Markdown")
    export_parser.add_argument("--parent-id", type=int, help="Root node ID for export")
    export_parser.add_argument("--output", help="Output file path")
    
    # Get by type command
    type_parser = subparsers.add_parser("by-type", help="Get nodes by type")
    type_parser.add_argument("node_type", help="Node type to search for")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = DocumentManagerCLI(args.db)
    
    try:
        if args.command == "create":
            cli.create_node(
                title=args.title,
                node_type=args.node_type,
                content=args.content,
                parent_id=args.parent_id,
                metadata=args.metadata
            )
        elif args.command == "get":
            cli.get_node(args.node_id)
        elif args.command == "update":
            cli.update_node(
                node_id=args.node_id,
                title=args.title,
                content=args.content,
                metadata=args.metadata
            )
        elif args.command == "delete":
            cli.delete_node(args.node_id)
        elif args.command == "list":
            cli.list_children(args.parent_id)
        elif args.command == "search":
            cli.search_nodes(query=args.query or "", node_type=args.type)
        elif args.command == "tree":
            cli.show_tree(args.parent_id)
        elif args.command == "export":
            cli.export_markdown(args.parent_id, args.output)
        elif args.command == "by-type":
            cli.get_nodes_by_type(args.node_type)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()