from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import shutil
import embeddings
import time
from datetime import datetime
from chunking import chunk_document
import database

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
# Users upload a file → Saved to disk + record in database    
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


# Index document endpoint
@app.post("/index/{document_id}")
def index_document(document_id: int):
    """
    Chunk a document and store chunks in the database
    
    Args:
        document_id: The ID of the document to index
        
    Returns:
        JSON response with success status and chunk count
    """
    
    # 1. Get document from database
    document = database.get_document_by_id(document_id)
    
    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID {document_id} not found"
        )
    
    # 2. Check if file exists on disk
    file_path = document["file_path"]
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=500,
            detail=f"File not found on disk: {file_path}"
        )
    
    # 3. Check if document already has chunks and delete them for re-indexing
    existing_chunk_count = database.count_chunks_for_document(document_id)
    
    if existing_chunk_count > 0:
        database.delete_existing_chunks(document_id)  # Delete existing chunks before inserting to database, avoid duplicates and clean slate
        print(f"Deleted {existing_chunk_count} existing chunks for document {document_id}")
    
    # 4. Chunk the document
    try:
        chunks_list = chunk_document(
            file_path=file_path,
            chunk_size=500,
            overlap=50
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error chunking document: {str(e)}"
        )
    
    # 5. Loops through all chunks and Insert into database
    try:
        for index, chunk_text in enumerate(chunks_list):
            database.insert_chunk(
                document_id=document_id,
                chunk_text=chunk_text,
                chunk_index=index
            )
    except Exception as e:
        database.delete_existing_chunks(document_id) # Delete all related chunks if inserting goes wrong in the middle of inserting, to ensure data clean slate and return an error message
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting chunks into database: {str(e)}"
        )
    
    # Return success response
    return {
        "success": True,
        "document_id": document_id,
        "filename": document["filename"],
        "chunks_created": len(chunks_list),
        "message": "Document successfully indexed"
    }
    
    
    
    
@app.get("/search") # It's GET (not POST) because we're reading/searching data, not creating anything
def search_documents(q: str, k: int = 5):
    """
    Search for a keyword in all indexed document chunks
    
    Args:
        q: Search query (keyword or phrase)
        k: Number of results to return (default 5, max 20)
        
    Returns:
        JSON with search results
    """
    # Validate query parameter
    if not q or len(q.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'q' cannot be empty"
        )
    
    # Validate k parameter
    if k < 1 or k > 20:
        raise HTTPException(
            status_code=400,
            detail="Parameter 'k' must be between 1 and 20"
        )
    
    # Search the database
    results = database.search_chunks(q, k)
    
    # Return formatted response
    return {
        "query": q,
        "limit": k,
        "results_found": len(results),
        "results": results
    }


# generate embeddings endpoint
@app.post("/generate-embeddings/{document_id}")
def generate_embeddings_for_document(document_id: int) -> dict:
    """
    Generate embeddings for all chunks of a document.
    
    Args:
        document_id: ID of the document to process
        
    Returns:
        Dictionary with summary statistics
    """
    try:
        start_time: float = time.time()
        
        # Step 1: Check if document exists
        document: dict = database.get_document_by_id(document_id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Step 2: Get all chunks for this document
        chunks: list[dict] = database.get_chunks_by_document(document_id)
        
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail=f"No chunks found for document {document_id}. Did you index it first?"
            )
        
        # Step 3: Generate embeddings for each chunk
        embeddings_generated: int = 0
        embeddings_skipped: int = 0
        
        for chunk in chunks:
            # Skip if already has embedding
            if chunk["embedding"] is not None:
                embeddings_skipped += 1 # Why skip? Don't waste API calls and money re-generating embeddings that already exist!
                continue
            
            # Generate embedding using OpenAI 
            embedding: list[float] = embeddings.get_embedding(chunk["chunk_text"])
            
            # Store in database
            database.update_chunk_embedding(chunk["id"], embedding)
            
            embeddings_generated += 1
            print(f"✅ Generated embedding for chunk {chunk['id']}")
        
        # Step 4: Calculate statistics
        end_time: float = time.time()
        duration: float = round(end_time - start_time, 2)
        
        result: dict = {
            "message": "Embeddings generated successfully",
            "document_id": document_id,
            "document_name": document["filename"],
            "total_chunks": len(chunks),
            "embeddings_generated": embeddings_generated,
            "embeddings_skipped": embeddings_skipped,
            "duration_seconds": duration,
            "average_time_per_chunk": round(duration / len(chunks), 2) if len(chunks) > 0 else 0
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embeddings: {str(e)}"
        )
        
# Semantic search endpoint     
@app.get("/semantic-search")
def semantic_search(q: str, k: int = 5):
    """
    Search for chunks using semantic similarity (meaning-based search).
    
    Args:
        q: Query string to search for
        k: Number of top results to return (default: 5)
        
    Returns:
        JSON with query, results ranked by similarity, and metadata
    """
    # Validation
    if not q or q.strip() == "":
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required and cannot be empty")
    
    if k < 1 or k > 20:
        raise HTTPException(status_code=400, detail="Parameter 'k' must be between 1 and 20")
    
    try:
        # Step 1: Generate embedding for the query
        print(f"🔍 Generating embedding for query: '{q}'")
        vector1 = embeddings.get_embedding(q) # converts text to 1536-dim vectors
        
        # Step 2: Fetches all chunks from database that have embeddings
        print(f"📚 Fetching all chunks with embeddings...")
        all_chunks = database.get_all_chunks_with_embeddings() # each chunk inside is a second vector
        
        if len(all_chunks) == 0:
            return {
                "query": q,
                "results": [],
                "total_chunks_searched": 0,
                "message": "No chunks with embeddings found. Please generate embeddings first."
            }
        
        print(f"✅ Found {len(all_chunks)} chunks with embeddings")
        
        # Step 3: Calculate similarity for each chunk
        results = []
        for chunk in all_chunks:
            similarity = embeddings.compute_similarity(vector1, chunk["embedding"]) # The actual calculation of the similarity between the query and the chunk
            
            results.append({
                "chunk_id": chunk["id"],
                "chunk_text": chunk["chunk_text"],
                "chunk_index": chunk["chunk_index"],
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "similarity": round(similarity, 4)  # Round to 4 decimal places
            })
        
        # Step 4: Sort by similarity (highest first)
        results.sort(key=lambda x: x["similarity"], reverse=True) # Sorts the results by similarity value in descending order
        
        # Step 5: Return top K results
        top_results = results[:k] 
        
        print(f"🎯 Returning top {len(top_results)} results")
        
        return {
            "query": q,
            "results": top_results,
            "total_chunks_searched": len(all_chunks),
            "results_returned": len(top_results)
        }
        
    except Exception as e:
        print(f"❌ Error during semantic search: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    
    

# Ping endpoint
@app.get("/ping")
def ping():
    return {"message": "pong"}