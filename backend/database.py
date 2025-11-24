import sqlite3
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
import json #Any time you need to store complex data (lists, dicts) in SQLite as text

# Database file path - this is where the SQLite database will be stored
DATABASE_PATH = "opschat.db" #This constant defines where the database file lives 
UPLOAD_FOLDER = "uploads" # Folder to store uploaded files


def ensure_upload_folder():
    """Create uploads folder if it doesn't exist"""
    if not os.path.exists(UPLOAD_FOLDER): # Check if the upload folder exists
        os.makedirs(UPLOAD_FOLDER) # Create the folder if it doesn't exist, use makedirs to create any necessary parent directories as well instead of mkdir to create a single folder
        print(f"Created upload folder at {UPLOAD_FOLDER}")


def get_db_connection(): #function logic to connect to the database
    """
    Creates and returns a connection to the SQLite database.
    The row_factory setting makes query results return as dictionaries
    instead of tuples, which is much more convenient to work with.
    """
    conn = sqlite3.connect(DATABASE_PATH) # Create actual path connection to the database
    conn.row_factory = sqlite3.Row  # This lets us access columns by name, basically lets us treat rows like dictionaries 
    return conn # Return the connection object, not cursor

def init_database(): #function to start up the database
    """
    Initializes the database by creating the necessary tables.
    This function is safe to call multiple times - it only creates
    tables if they don't already exist.
    """
    ensure_upload_folder()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create documents table
    # This stores metadata about each uploaded document
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create chunks table
    # This stores the individual text chunks from each document
    # Each chunk links back to its parent document via document_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit() # makes changes permanent
    conn.close()
    
    print("Database initialized successfully")
    
    
def get_document_by_id(document_id: int):
    """Get a document from the database by its ID"""
    conn = get_db_connection() # Open database connection
    cursor = conn.cursor()
    
    cursor.execute( # Execute SQL query to get document by ID
        "SELECT id, filename, file_path, upload_date FROM documents WHERE id = ?",
        (document_id,)
        # Python does this: "WHERE id = ?"  +  (1,)  →  "WHERE id = 1"
    )
    
    row = cursor.fetchone() # fetches one single row (horizontal line) that contains MULTIPLE COLUMNS
    conn.close()
    
    if row is None:
        return None
    
    return {
        "id": row[0], # Access first column (id)
        "filename": row[1], # Access second column (filename)
        "file_path": row[2], # Access third column (file_path)
        "upload_date": row[3] # Access fourth column (upload_date)
    }



def insert_chunk(document_id: int, chunk_text: str, chunk_index: int):
    """Insert a single chunk into the database"""
    conn = get_db_connection() # Open database connection
    cursor = conn.cursor()
    
    cursor.execute( # Execute SQL query to insert a new chunk
        "INSERT INTO chunks (document_id, chunk_text, chunk_index) VALUES (?, ?, ?)",
        (document_id, chunk_text, chunk_index)
    )
    
    conn.commit() # makes changes permanent, from memory to disk
    conn.close() 



def delete_existing_chunks(document_id: int):
    """Delete all existing chunks for a document (for re-indexing)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
    # Deletes all chunks associated with the given document_id
    
    conn.commit()
    conn.close()




def search_chunks(query: str, limit: int = 5):
    """
    Search for chunks containing a keyword
    
    Args:
        query: The keyword to search for
        limit: Maximum number of results to return
        
    Returns:
        List of dictionaries with chunk and document info
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL query with JOIN to get both chunk and document info
    sql = """
        SELECT 
            chunks.id as chunk_id,
            chunks.chunk_text,
            chunks.chunk_index,
            chunks.document_id,
            documents.filename
        FROM chunks JOIN documents ON chunks.document_id = documents.id
        WHERE chunks.chunk_text LIKE ? 
        LIMIT ? 
    """
    
    # Add wildcards for LIKE search (% means "anything before or after")
    search_pattern = f"%{query}%" 
    
    cursor.execute(sql, (search_pattern, limit)) # provide values in a tuple
    rows = cursor.fetchall() # Fetch all matching rows and Returns a list of tuples
    conn.close()
    
    """
    rows looks like:
    
    rows = [
    (1, "Python is great...", 0, 5, "notes.txt"),
    (3, "Learning python...", 2, 5, "notes.txt"),
    (7, "Python projects...", 1, 6, "project.md")
    ]
    """
    
    # Convert to list of dictionaries
    results = []
    for row in rows:
        results.append({
            "chunk_id": row[0],  # "chunk_id": 1,
            "chunk_text": row[1],  # "chunk_text": "Python is great for web development...",
            "chunk_index": row[2], # "chunk_index": 0,
            "document_id": row[3],  # "document_id": 5,
            "filename": row[4]  # "filename": "notes.txt"
        })
     
    return results # Return the list of result dictionaries




def count_chunks_for_document(document_id: int) -> int:
    """Count how many chunks exist for a document"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM chunks WHERE document_id = ?",
        (document_id,)
        # SELECT COUNT(*) - Count the number of rows where id = document_id   
    )
    
    # Returns a tuple: (3,), even though it's just one number, it's in a tuple!
    count = cursor.fetchone()[0] # Gets the first element and store in the count variable
    conn.close()
    
    return count



def update_chunk_embedding(chunk_id: int, embedding: list[float]):
    """
    Store an embedding for a specific chunk.
    
    Args:
        chunk_id: The ID of the chunk to update
        embedding: List of 1536 floats representing the embedding
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert embedding Python list to JSON string for storage
    embedding_json = json.dumps(embedding) #json.dumps converts Python objects into JSON strings
                                           # json.loads converts JSON strings back into Python objects
    
    cursor.execute(
        "UPDATE chunks SET embedding = ? WHERE id = ?", # update the embedding column for a specific chunk
        (embedding_json, chunk_id) 
    )
    
    conn.commit() 
    conn.close()


def get_all_chunks_with_embeddings(document_id: int = None):
    """
    Get all chunks that have embeddings.
    
    Args:
        document_id: Optional - filter by specific document
        
    Returns:
        List of dictionaries with chunk data including embeddings
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if document_id:
        cursor.execute("""
            SELECT c.id, c.document_id, c.chunk_text, c.chunk_index, c.embedding, d.filename
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.embedding IS NOT NULL AND c.document_id = ?
            ORDER BY c.chunk_index
        """, (document_id,))
    else:
        cursor.execute("""
            SELECT c.id, c.document_id, c.chunk_text, c.chunk_index, c.embedding, d.filename
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.embedding IS NOT NULL
            ORDER BY c.document_id, c.chunk_index
        """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries and parse embeddings
    chunks = []
    for row in rows:
        chunk = {
            "id": row[0],
            "document_id": row[1],
            "chunk_text": row[2],  # Changed from "content" to "chunk_text"
            "chunk_index": row[3],
            "embedding": json.loads(row[4]) if row[4] else None,
            "filename": row[5]
        }
        chunks.append(chunk)
    
    return chunks # rows contains tuples, chunks contains dictionaries


def get_chunks_by_document(document_id: int):
    """
    Get all chunks for a specific document (with or without embeddings).
    
    Args:
        document_id: The document ID
        
    Returns:
        List of chunk dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, document_id, chunk_text, chunk_index, embedding
        FROM chunks
        WHERE document_id = ?
        ORDER BY chunk_index
    """, (document_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    chunks = []
    for row in rows:
        chunk = {
            "id": row[0],
            "document_id": row[1],
            "chunk_text": row[2],  # Changed from "content" to "chunk_text"
            "chunk_index": row[3],
            "embedding": json.loads(row[4]) if row[4] else None # might be None or have embedding
        }
        chunks.append(chunk) 
    
    return chunks



# Test function to verify database is working
if __name__ == "__main__":
    init_database()
    print(f"Database created at {DATABASE_PATH}")