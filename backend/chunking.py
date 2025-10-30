"""
Document Chunking Module for OpsChat Lite

This module handles reading documents and splitting them into chunks
for storage and search.
"""

import os
from typing import List


def read_text_file(file_path: str) -> str:
    """
    Read content from a .txt or .md file
    
    Args:
        file_path: Path to the text file
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file encoding is not UTF-8
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content


def read_pdf_file(file_path: str) -> str:
    """
    Read content from a .pdf file
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ImportError: If PyPDF2 is not installed
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        import PyPDF2
    except ImportError:
        raise ImportError(
            "PyPDF2 is required for PDF processing. "
            "Install it with: pip install PyPDF2"
        )
    
    content = ""
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            content += page.extract_text()
    
    return content


def read_document(file_path: str) -> str:
    """
    Read content from any supported document type
    
    Automatically detects file type and uses appropriate reader
    
    Args:
        file_path: Path to the document
        
    Returns:
        Document content as string
        
    Raises:
        ValueError: If file type is not supported
        FileNotFoundError: If file doesn't exist
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext in ['.txt', '.md']:
        return read_text_file(file_path)
    elif file_ext == '.pdf':
        return read_pdf_file(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: {file_ext}. "
            f"Supported types: .txt, .md, .pdf"
        )


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: The text to chunk
        chunk_size: Maximum characters per chunk (default: 500)
        overlap: Number of overlapping characters between chunks (default: 50)
        
    Returns:
        List of text chunks
        
    Example:
        >>> text = "This is a test. " * 100  # 1600 characters
        >>> chunks = chunk_text(text, chunk_size=500, overlap=50)
        >>> len(chunks)  # Will be 4 chunks
        4
    """
    if not text or not text.strip():
        return []
    
    # Clean up text: remove excessive whitespace
    text = ' '.join(text.split())
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # Calculate end position
        end = start + chunk_size
        
        # If this is not the last chunk and we're in the middle of a word,
        # try to break at a space
        if end < text_length:
            # Look for the last space within the chunk
            space_pos = text.rfind(' ', start, end)
            if space_pos > start:  # Found a space
                end = space_pos
        
        # Extract chunk
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        # Move start position (with overlap)
        start = end - overlap
        
        # Prevent infinite loop if overlap >= chunk_size
        if start <= chunks[-1] if chunks else 0:
            start = end
    
    return chunks


def chunk_document(file_path: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Read a document and split it into chunks
    
    This is the main function you'll use to process documents.
    It combines reading and chunking in one step.
    
    Args:
        file_path: Path to the document
        chunk_size: Maximum characters per chunk (default: 500)
        overlap: Number of overlapping characters between chunks (default: 50)
        
    Returns:
        List of text chunks
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file type is not supported
        
    Example:
        >>> chunks = chunk_document("uploads/20251029_154747_test.txt")
        >>> print(f"Created {len(chunks)} chunks")
        Created 5 chunks
    """
    # Step 1: Read the document
    content = read_document(file_path)
    
    # Step 2: Chunk the content
    chunks = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
    
    return chunks


# Optional: Helper function to get chunk statistics
def get_chunk_stats(chunks: List[str]) -> dict:
    """
    Get statistics about a list of chunks
    
    Args:
        chunks: List of text chunks
        
    Returns:
        Dictionary with statistics (count, avg_length, min_length, max_length)
    """
    if not chunks:
        return {
            "count": 0,
            "avg_length": 0,
            "min_length": 0,
            "max_length": 0
        }
    
    lengths = [len(chunk) for chunk in chunks]
    
    return {
        "count": len(chunks),
        "avg_length": sum(lengths) // len(lengths),
        "min_length": min(lengths),
        "max_length": max(lengths)
    }