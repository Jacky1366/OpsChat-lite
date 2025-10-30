from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import shutil
from datetime import datetime

# Import the database module
from database import init_database, get_db_connection, UPLOAD_FOLDER

# Lifespan context manager - runs code when the app starts and stops (preparation process))
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    print("Starting up: Initializing database...")
    init_database()
    yield # Yield control back to FastAPI to start handling requests
    # Shutdown: Clean up resources (nothing needed for now)
    print("Shutting down...")

# Create the FastAPI application instance with lifespan management
app = FastAPI(
    title="OpsChat Lite API",
    description="A document Q&A system with AI-powered search",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow requests from any origin
    allow_credentials=True, # allows requests to include credentials like cookies or authorization headers.
    allow_methods=["*"], # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # allow all headers
)

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "OpsChat Lite API is running",
        "version": "0.1.0",
        "database": "initialized"
    }
    
# Get all documents endpoint
@app.get("/documents")
def list_documents():
    """
    Returns a list of all uploaded documents.
    This is a simple read-only query to demonstrate database interaction.
    """
    conn = get_db_connection() # Get connection from database.py
    cursor = conn.cursor() # Create cursor in main.py to execute SQL queries, for seperation of purposes, conneciton doesn't need cursor to execute queries
    
    cursor.execute("SELECT id, filename, upload_date FROM documents") # Query to get all documents
    documents = cursor.fetchall() # grab all rows into a Python list
    
    conn.close()
    
    # Convert Row objects to regular dictionaries for JSON serialization
    return {"documents": [dict(row) for row in documents]} #cant return "documents" : documents, because it's SQL lite format, fast API only accept JSON format
    """
    return Example Response:
    {
        "documents": [
            {"id": 1, "filename": "resume.pdf", "upload_date": "2025-10-22 10:30:00"},
            {"id": 2, "filename": "handbook.txt", "upload_date": "2025-10-22 11:15:00"},
            {"id": 3, "filename": "report.md", "upload_date": "2025-10-22 14:20:00"}
        ]
    }

    """
    
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)): #basiclly saying User MUST upload a file, or they get an error
    """
    Upload a document and store its metadata
    
    Accepts: .txt, .md, .pdf files
    Returns: Document ID and metadata
    """
    
    # 1. Validate file type
    allowed_extensions = ['.txt', '.md', '.pdf']
    file_ext = os.path.splitext(file.filename)[1].lower() # Get file extension in lowercase
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # 2. Generate full file path, combine upload time to ensure unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # e.g., "20251027_143052" (October 27, 2025, 2:30:52 PM)
    safe_filename = f"{timestamp}_{file.filename}" #combines the timestamp with the original filename: "20251027_143052_notes.txt"
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename) #combines folder and filename into a full path: "uploads/20251027_143052_notes.txt"
    #os.path.join()? It handles slashes correctly for different operating systems, (Mac uses /, Windows uses \)
    
    try:
        # 3. Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) #copies the uploaded file and paste it to the destination path, buffer will write the file into the disk for us!
            # file.file is the binary content of the uploaded file
        
        # 4. Insert metadata into database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO documents (filename, file_path, upload_date)
            VALUES (?, ?, ?)
            """,
            (file.filename, file_path, datetime.now())
        )
        
        conn.commit()
        document_id = cursor.lastrowid  # Get the auto-generated ID
        conn.close()
        
        # 5. Return success response
        return {
            "success": True,
            "message": "File uploaded successfully",
            "document": {
                "id": document_id,
                "filename": file.filename,
                "file_path": file_path,
                "upload_date": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        # Clean up file if database insertion fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# Ping endpoint
@app.get("/ping")
def ping():
    return {"message": "pong"}