from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import HTTPException
from database import get_db_connection


# Import the database module
from database import init_database

# Lifespan context manager - runs code when the app starts and stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    print("Starting up: Initializing database...")
    init_database()
    yield
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, filename, upload_date FROM documents")
    documents = cursor.fetchall()
    
    conn.close()
    
    # Convert Row objects to dictionaries for JSON serialization
    return {"documents": [dict(row) for row in documents]}

# Ping endpoint
@app.get("/ping")
def ping():
    return {"message": "pong"}