"""
Configuration file for OpsChat Lite
Loads environment variables and defines constants
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model names (using OpenAI's latest)
EMBEDDING_MODEL = "text-embedding-3-small"  # For generating embeddings
CHAT_MODEL = "gpt-4o-mini"  # For Q&A (cheaper, good quality)

# Embedding settings
EMBEDDING_DIMENSIONS = 1536  # Dimensions of the embedding vector

# Chunking settings (from Phase 1)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Search settings
DEFAULT_TOP_K = 5  # Number of results to return by default

# Validate API key exists
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. "
        "Please check your .env file."
    )

print("✅ Configuration loaded successfully!")