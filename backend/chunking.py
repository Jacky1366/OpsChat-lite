"""
Document Chunking Module for OpsChat Lite

This module handles reading documents and splitting them into chunks
for storage and search.
"""

import os # Imports Python's operating system module for file operations
from typing import List # Imports the List type hint


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
    if not os.path.exists(file_path): # Check if file exists
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f: # encoding='utf-8' specifies how to decode bytes into text
        content = f.read() # Read entire file into a string variable
    
    return content # Return the file content


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
    
    try: # always validate before trying to open!
        import PyPDF2
    except ImportError: # Try to import the PyPDF2 library
        raise ImportError(  # If import fails, catch that specific error
            "PyPDF2 is required for PDF processing. "  
            "Install it with: pip install PyPDF2"
        )
    
    content = ""
    with open(file_path, 'rb') as f: # 'rb' means read in binary mode, PDFs aren't plain text - they're binary files with special encoding
        pdf_reader = PyPDF2.PdfReader(f) # Create a PDF reader object that can parse the PDF structure, the PyPDF2 library handles all the complexity of PDF format
        for page in pdf_reader.pages:
            content += page.extract_text() # page.extract_text() gets text from one page

    
    return content # Return the full extracted text


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
    file_ext = os.path.splitext(file_path)[1].lower() # Splits filename and extension and get the extension in lowercase
    
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
    text = ' '.join(text.split()) # split by whitespace and join them back together with single space
    
    chunks = []
    start: int = 0
    text_length = len(text)
    
    while start < text_length:
        # Calculate end position
        end: int = start + chunk_size
        
        # If this is not the last chunk and we're in the middle of a word,
        # try to adjust the end to the last space
        if end < text_length:
            # Look for the last space within the chunk
            last_space = text.rfind(' ', start, end) # rfind means "reverse find" (searches backwards)
            if last_space > start:  # confirms it's a valid position
                end = last_space
        
        # Extract each chunk
        chunk: str = text[start:end].strip() # slice characters from position start to end, not including end and Remove leading/trailing whitespace 
        if chunk:  # if chunk isn't empty
            chunks.append(chunk) # Add chunk to the list
        
        old_start: int = start # Store old position before updating
        
        start = end - overlap # Move start forward, minus overlap to create overlap
        
        # Safety check, Ensure we don't move backwards
        if start <= old_start: # only happens when overlap is BIGGER than chunk_size!
            start = old_start
    
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
    chunks_list = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
    
    return chunks_list


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
    
    list = [len(chunk) for chunk in chunks] # store length of each chunk text in a list
    # eg. chunks = ["Hello world", "This is a test", "im good"] => list = [11, 14, 7]
    
    return {
        "count": len(chunks), #eg. return: 3
        "avg_length": sum(list) // len(list), # eg. return: (11 + 14 + 7) // 3 = 32 // 3 = 10, Double slash // = integer division (no decimal)
        "min_length": min(list), # finds the shortest chunk eg. return: 7
        "max_length": max(list) # finds the longest chunk eg. return: 14
    }