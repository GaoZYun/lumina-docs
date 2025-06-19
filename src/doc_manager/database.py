"""
Database schema and operations for document management system.
"""
import sqlite3
import json
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime
from .config import config


class DocumentDatabase:
    """SQLite database manager for structured document management."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection and create tables if not exist."""
        # Use config path if not provided
        if db_path is None:
            db_path = config.get_database_path()
        
        # Ensure database directory exists
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.init_database()
        self.init_documents_metadata_table()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self) -> None:
        """Initialize database schema."""
        with self.get_connection() as conn:
            # Create main document nodes table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    node_type TEXT NOT NULL,
                    level INTEGER NOT NULL DEFAULT 1,
                    sort_order INTEGER NOT NULL DEFAULT 0,
                    metadata TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES document_nodes(id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for better query performance
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_parent_id 
                ON document_nodes(parent_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_node_type 
                ON document_nodes(node_type)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_level_sort 
                ON document_nodes(level, sort_order)
            """)
            
            # Create trigger to update updated_at timestamp
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS update_timestamp 
                AFTER UPDATE ON document_nodes
                BEGIN
                    UPDATE document_nodes 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
    
    def init_documents_metadata_table(self) -> None:
        """Initialize documents metadata table to track all documents."""
        with self.get_connection() as conn:
            # Create documents metadata table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_name TEXT UNIQUE NOT NULL,
                    table_name TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create trigger to update updated_at timestamp for documents
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS update_documents_timestamp 
                AFTER UPDATE ON documents_metadata
                BEGIN
                    UPDATE documents_metadata 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
    
    def create_document(self, document_name: str, title: str, description: Optional[str] = None) -> str:
        """Create a new document with its own table."""
        # Sanitize document name for use as table name
        table_name = f"doc_{document_name.lower().replace(' ', '_').replace('-', '_')}"
        
        # Remove any non-alphanumeric characters except underscore
        import re
        table_name = re.sub(r'[^a-zA-Z0-9_]', '', table_name)
        
        with self.get_connection() as conn:
            try:
                # Insert document metadata
                cursor = conn.execute("""
                    INSERT INTO documents_metadata (document_name, table_name, title, description)
                    VALUES (?, ?, ?, ?)
                """, (document_name, table_name, title, description))
                
                # Create document-specific table
                conn.execute(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        parent_id INTEGER,
                        title TEXT NOT NULL,
                        content TEXT,
                        node_type TEXT NOT NULL,
                        level INTEGER NOT NULL DEFAULT 1,
                        sort_order INTEGER NOT NULL DEFAULT 0,
                        metadata TEXT DEFAULT '{{}}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (parent_id) REFERENCES {table_name}(id) ON DELETE CASCADE
                    )
                """)
                
                # Create indexes for the new table
                conn.execute(f"""
                    CREATE INDEX idx_{table_name}_parent_id 
                    ON {table_name}(parent_id)
                """)
                
                conn.execute(f"""
                    CREATE INDEX idx_{table_name}_node_type 
                    ON {table_name}(node_type)
                """)
                
                conn.execute(f"""
                    CREATE INDEX idx_{table_name}_level_sort 
                    ON {table_name}(level, sort_order)
                """)
                
                # Create trigger for the new table
                conn.execute(f"""
                    CREATE TRIGGER update_{table_name}_timestamp 
                    AFTER UPDATE ON {table_name}
                    BEGIN
                        UPDATE {table_name} 
                        SET updated_at = CURRENT_TIMESTAMP 
                        WHERE id = NEW.id;
                    END
                """)
                
                conn.commit()
                return table_name
                
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    raise ValueError(f"Document '{document_name}' already exists")
                else:
                    raise e
    
    def get_documents_list(self) -> List[Dict[str, Any]]:
        """Get list of all documents."""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM documents_metadata 
                ORDER BY created_at DESC
            """).fetchall()
            
            return [dict(row) for row in rows]
    
    def get_document_table_name(self, document_name: str) -> Optional[str]:
        """Get table name for a document."""
        with self.get_connection() as conn:
            row = conn.execute("""
                SELECT table_name FROM documents_metadata 
                WHERE document_name = ?
            """, (document_name,)).fetchone()
            
            return row['table_name'] if row else None
    
    def delete_document(self, document_name: str) -> bool:
        """Delete a document and its table."""
        table_name = self.get_document_table_name(document_name)
        if not table_name:
            return False
            
        with self.get_connection() as conn:
            try:
                # Drop the document table
                conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                
                # Remove from metadata
                cursor = conn.execute("""
                    DELETE FROM documents_metadata 
                    WHERE document_name = ?
                """, (document_name,))
                
                conn.commit()
                return cursor.rowcount > 0
                
            except Exception:
                return False

    def create_node(self, 
                   title: str, 
                   node_type: str,
                   content: Optional[str] = None,
                   parent_id: Optional[int] = None,
                   metadata: Optional[Dict[str, Any]] = None,
                   sort_order: Optional[int] = None,
                   document_name: Optional[str] = None) -> int:
        """Create a new document node."""
        # Determine table name
        if document_name:
            table_name = self.get_document_table_name(document_name)
            if not table_name:
                raise ValueError(f"Document '{document_name}' does not exist")
        else:
            table_name = "document_nodes"  # Use default table
        
        with self.get_connection() as conn:
            # Calculate level based on parent
            if parent_id is None:
                level = 1
            else:
                parent_level = conn.execute(
                    f"SELECT level FROM {table_name} WHERE id = ?", 
                    (parent_id,)
                ).fetchone()
                level = (parent_level['level'] + 1) if parent_level else 1
            
            # Calculate sort_order if not provided
            if sort_order is None:
                max_order = conn.execute(
                    f"SELECT MAX(sort_order) as max_order FROM {table_name} WHERE parent_id = ?",
                    (parent_id,)
                ).fetchone()
                sort_order = (max_order['max_order'] or 0) + 1
            
            # Insert new node
            cursor = conn.execute(f"""
                INSERT INTO {table_name} 
                (parent_id, title, content, node_type, level, sort_order, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                parent_id, 
                title, 
                content, 
                node_type, 
                level, 
                sort_order,
                json.dumps(metadata or {})
            ))
            
            return cursor.lastrowid
    
    def get_node(self, node_id: int, document_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a single node by ID."""
        # Determine table name
        if document_name:
            table_name = self.get_document_table_name(document_name)
            if not table_name:
                raise ValueError(f"Document '{document_name}' does not exist")
        else:
            table_name = "document_nodes"  # Use default table
        
        with self.get_connection() as conn:
            row = conn.execute(
                f"SELECT * FROM {table_name} WHERE id = ?", 
                (node_id,)
            ).fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def update_node(self, 
                   node_id: int,
                   title: Optional[str] = None,
                   content: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing node."""
        with self.get_connection() as conn:
            # Build update query dynamically
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            
            if content is not None:
                updates.append("content = ?")
                params.append(content)
            
            if metadata is not None:
                updates.append("metadata = ?")
                params.append(json.dumps(metadata))
            
            if not updates:
                return False
            
            params.append(node_id)
            
            cursor = conn.execute(f"""
                UPDATE document_nodes 
                SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            
            return cursor.rowcount > 0
    
    def delete_node(self, node_id: int) -> bool:
        """Delete a node and all its children."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM document_nodes WHERE id = ?", 
                (node_id,)
            )
            return cursor.rowcount > 0
    
    def get_children(self, parent_id: Optional[int] = None, document_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get direct children of a node."""
        # Determine table name
        if document_name:
            table_name = self.get_document_table_name(document_name)
            if not table_name:
                raise ValueError(f"Document '{document_name}' does not exist")
        else:
            table_name = "document_nodes"  # Use default table
        
        with self.get_connection() as conn:
            if parent_id is None:
                # Get root nodes
                rows = conn.execute(f"""
                    SELECT * FROM {table_name} 
                    WHERE parent_id IS NULL 
                    ORDER BY sort_order
                """).fetchall()
            else:
                rows = conn.execute(f"""
                    SELECT * FROM {table_name} 
                    WHERE parent_id = ? 
                    ORDER BY sort_order
                """, (parent_id,)).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def get_node_path(self, node_id: int) -> List[Dict[str, Any]]:
        """Get the full path from root to the specified node."""
        with self.get_connection() as conn:
            # Use recursive CTE to get path
            rows = conn.execute("""
                WITH RECURSIVE node_path AS (
                    SELECT id, parent_id, title, node_type, level, 0 as depth
                    FROM document_nodes 
                    WHERE id = ?
                    
                    UNION ALL
                    
                    SELECT n.id, n.parent_id, n.title, n.node_type, n.level, np.depth + 1
                    FROM document_nodes n
                    JOIN node_path np ON n.id = np.parent_id
                )
                SELECT * FROM node_path ORDER BY depth DESC
            """, (node_id,)).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def search_nodes(self, 
                    query: str = "",
                    node_type: Optional[str] = None,
                    metadata_filter: Optional[Dict[str, Any]] = None,
                    document_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search nodes based on various criteria."""
        # Determine table name
        if document_name:
            table_name = self.get_document_table_name(document_name)
            if not table_name:
                raise ValueError(f"Document '{document_name}' does not exist")
        else:
            table_name = "document_nodes"  # Use default table
        
        with self.get_connection() as conn:
            sql = f"SELECT * FROM {table_name} WHERE 1=1"
            params = []
            
            # Text search in title and content
            if query:
                sql += " AND (title LIKE ? OR content LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            # Filter by node type
            if node_type:
                sql += " AND node_type = ?"
                params.append(node_type)
            
            # Filter by metadata (simple key-value matching)
            if metadata_filter:
                for key, value in metadata_filter.items():
                    sql += " AND JSON_EXTRACT(metadata, ?) = ?"
                    params.extend([f"$.{key}", value])
            
            sql += " ORDER BY level, sort_order"
            
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_nodes_by_type(self, node_type: str, document_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all nodes of a specific type."""
        return self.search_nodes(node_type=node_type, document_name=document_name)
    
    def move_node(self, node_id: int, new_parent_id: Optional[int]) -> bool:
        """Move a node to a new parent."""
        with self.get_connection() as conn:
            # Calculate new level
            if new_parent_id is None:
                new_level = 1
            else:
                parent = conn.execute(
                    "SELECT level FROM document_nodes WHERE id = ?", 
                    (new_parent_id,)
                ).fetchone()
                if not parent:
                    return False
                new_level = parent['level'] + 1
            
            # Update node and all its descendants
            cursor = conn.execute("""
                UPDATE document_nodes 
                SET parent_id = ?, level = ?
                WHERE id = ?
            """, (new_parent_id, new_level, node_id))
            
            # Update levels of all descendants
            self._update_descendant_levels(conn, node_id)
            
            return cursor.rowcount > 0
    
    def _update_descendant_levels(self, conn: sqlite3.Connection, node_id: int) -> None:
        """Recursively update levels of all descendant nodes."""
        # Get current node level
        current_node = conn.execute(
            "SELECT level FROM document_nodes WHERE id = ?", 
            (node_id,)
        ).fetchone()
        
        if not current_node:
            return
        
        # Update direct children
        conn.execute("""
            UPDATE document_nodes 
            SET level = ? 
            WHERE parent_id = ?
        """, (current_node['level'] + 1, node_id))
        
        # Recursively update grandchildren
        children = conn.execute(
            "SELECT id FROM document_nodes WHERE parent_id = ?", 
            (node_id,)
        ).fetchall()
        
        for child in children:
            self._update_descendant_levels(conn, child['id'])
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary."""
        result = dict(row)
        # Parse JSON metadata
        if result.get('metadata'):
            try:
                result['metadata'] = json.loads(result['metadata'])
            except json.JSONDecodeError:
                result['metadata'] = {}
        else:
            result['metadata'] = {}
        
        return result
    
    def get_tree_structure(self, parent_id: Optional[int] = None, document_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get complete tree structure starting from parent_id."""
        children = self.get_children(parent_id, document_name)
        
        for child in children:
            child['children'] = self.get_tree_structure(child['id'], document_name)
        
        return children
    
    def export_tree_to_markdown(self, parent_id: Optional[int] = None, level: int = 1, document_name: Optional[str] = None) -> str:
        """Export tree structure to Markdown format."""
        children = self.get_children(parent_id, document_name)
        markdown = ""
        
        for child in children:
            # Add title with appropriate heading level
            markdown += "#" * level + " " + child['title'] + "\n\n"
            
            # Add content if exists
            if child.get('content'):
                markdown += child['content'] + "\n\n"
            
            # Recursively add children
            markdown += self.export_tree_to_markdown(child['id'], level + 1, document_name)
        
        return markdown
    
    def clear_all_data(self) -> None:
        """Clear all data from the database (for testing)."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM document_nodes")
            conn.commit()