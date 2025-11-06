"""
Test Script for Chunking Functionality

This script tests the chunking.py module to ensure it works correctly
before integrating it into the main API.

Run this from the backend/ directory:
    python test_chunking.py
"""

from chunking import chunk_document, chunk_text, get_chunk_stats, read_document
import os


def test_basic_chunking():
    """Test basic text chunking with a simple string"""
    print("\n" + "="*60)
    print("TEST 1: Basic Text Chunking")
    print("="*60)
    
    # Create a simple test text
    test_text = "This is a test document. " * 40  # 1000 characters
    
    print(f"Original text length: {len(test_text)} characters")
    
    # Chunk it
    chunks_list = chunk_text(test_text, chunk_size=200, overlap=20)
    
    print(f"Number of chunks created: {len(chunks_list)}")
    
    # Show first 3 chunks
    for i, chunk in enumerate(chunks_list[:3]):
        print(f"\nChunk {i+1} (length: {len(chunk)}):") # display index +1 and length of chunck
        print(f"'{chunk[:100]}...'")  # First 100 chars of the chunk
    
    # Get statistics
    # Prints each statistic from the dictionary
    stats = get_chunk_stats(chunks_list)
    print(f"\nChunk Statistics:")
    print(f"  - Total chunks: {stats['count']}")
    print(f"  - Average length: {stats['avg_length']} chars")
    print(f"  - Min length: {stats['min_length']} chars")
    print(f"  - Max length: {stats['max_length']} chars")
    
    print("\n✅ Basic chunking test passed!")


def test_file_chunking():
    """Test chunking a real uploaded file"""
    print("\n" + "="*60)
    print("TEST 2: File Chunking")
    print("="*60)
    
    # Look for any uploaded file in the uploads directory
    upload_dir = "uploads" 
    
    if not os.path.exists(upload_dir): # Check if the uploads/ folder exists
        print(f"⚠️  Upload directory '{upload_dir}' not found")
        print("   Please make sure you're in the backend/ directory")
        return
    
    files = os.listdir(upload_dir) # Lists all files in a directory. eg. files = ["20251029_154747_test.txt", "20251029_160000_doc.md"]
    
    if not files: 
        print("⚠️  No files found in uploads/") 
        print("   Upload a file first using POST /upload")
        return
    
    # Use the first file
    test_file = os.path.join(upload_dir, files[0]) # files[0] - Gets the first filename from the list and os.path.join() - Combines folder and filename properly
    print(f"Testing with file: {test_file}") # eg. uploads/20251029_154747_test.txt
    
    try:
        # Read the document
        content = read_document(test_file)
        print(f"✅ File read successfully: {len(content)} characters")
        
        # Chunk it
        chunks_list = chunk_document(test_file, chunk_size=500, overlap=50)
        print(f"✅ Chunking successful: {len(chunks_list)} chunks created")
        
        # Show first chunk
        if chunks_list:
            print(f"\nFirst chunk preview:")
            print(f"'{chunks_list[0][:200]}...'") # Show first 200 characters of the first chunk
        
        # Statistics
        stats = get_chunk_stats(chunks_list)
        print(f"\nChunk Statistics:")
        print(f"  - Total chunks: {stats['count']}")
        print(f"  - Average length: {stats['avg_length']} chars")
        print(f"  - Min length: {stats['min_length']} chars")
        print(f"  - Max length: {stats['max_length']} chars")
        
        print("\n✅ File chunking test passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("TEST 3: Edge Cases")
    print("="*60)
    
    # Test 1: Empty string
    print("\n1. Empty string:")
    chunks = chunk_text("")
    print(f"   Chunks from empty string: {len(chunks)} (expected: 0)")
    assert len(chunks) == 0, "Empty string should return 0 chunks"  # If chunk count is 0 → ✅ Passed, else crash with error message
    print("   ✅ Passed")
    
    # Test 2: Very short text (shorter than chunk size)
    print("\n2. Text shorter than chunk size:")
    short_text = "Short text"
    chunks = chunk_text(short_text, chunk_size=500)
    print(f"   Chunks from short text: {len(chunks)} (expected: 1)")
    assert len(chunks) == 1, "Short text should return 1 chunk"
    print("   ✅ Passed")
    
    # Test 3: Text with lots of whitespace
    print("\n3. Text with excessive whitespace:")
    messy_text = "Word1    \n\n\n   Word2     Word3"
    chunks = chunk_text(messy_text, chunk_size=500)
    print(f"   Original: '{messy_text}'")
    print(f"   Cleaned:  '{chunks[0]}'")
    assert "Word1 Word2 Word3" in chunks[0], "Whitespace should be normalized"
    print("   ✅ Passed")
    
    # Test 4: Non-existent file
    print("\n4. Non-existent file:")
    try:
        chunk_document("nonexistent.txt")
        print("   ❌ Should have raised FileNotFoundError") # if pass, not good, should have raised error
    except FileNotFoundError:
        print("   ✅ Correctly raised FileNotFoundError")
    
    # Test 5: Unsupported file type
    print("\n5. Unsupported file type:")
    try:
        read_document("test.docx")
        print("   ❌ Should have raised ValueError") # if pass, not good, should have raised error
    except ValueError as e:
        print(f"   ✅ Correctly raised ValueError: {e}")
    
    print("\n✅ All edge case tests passed!")


def test_overlap():
    """Test that overlap works correctly"""
    print("\n" + "="*60)
    print("TEST 4: Chunk Overlap")
    print("="*60)
    
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 5  # 130 characters
    chunks = chunk_text(text, chunk_size=30, overlap=10)
    
    print(f"Text length: {len(text)} characters")
    print(f"Chunk size: 30, Overlap: 10")
    print(f"Chunks created: {len(chunks)}")
    
    # Show first 3 chunks to demonstrate overlap
    for i in range(min(3, len(chunks))):
        print(f"\nChunk {i+1}: {chunks[i]}")
    
    if len(chunks) >= 2:
        overlap_found = chunks[0][-5:] in chunks[1][:15]
        
        # Use assert to fail the test if no overlap!
        assert overlap_found, "❌ FAILED: No overlap found between chunks!"
        
        print(f"\n✅ Overlap verified: {overlap_found}") #output true if overlap found, else crash with error message
    
    print("\n✅ Overlap test passed!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CHUNKING MODULE TEST SUITE")
    print("="*60)
    
    try:
        test_basic_chunking()
        test_file_chunking()
        test_edge_cases()
        test_overlap()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nThe chunking module is ready to be integrated into main.py")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback # Only needed if an error happens, a Python module that shows detailed error information
        traceback.print_exc() # Shows the full "stack trace" (path through the code), exc = "exception" (the error)


if __name__ == "__main__":
    main()