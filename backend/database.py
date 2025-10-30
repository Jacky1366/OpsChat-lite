import sqlite3
from typing import Optional, List, Dict, Any
import os
from datetime import datetime

# Database file path - this is where the SQLite database will be stored
DATABASE_PATH = "opschat.db" #This constant defines where your database file lives 
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

# Test function to verify database is working
if __name__ == "__main__":
    init_database()
    print(f"Database created at {DATABASE_PATH}")