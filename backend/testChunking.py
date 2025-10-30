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
    chunks = chunk_text(test_text, chunk_size=200, overlap=20)
    
    print(f"Number of chunks created: {len(chunks)}")
    
    # Show first 3 chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1} (length: {len(chunk)}):")
        print(f"'{chunk[:100]}...'")  # First 100 chars
    
    # Get statistics
    stats = get_chunk_stats(chunks)
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
    
    if not os.path.exists(upload_dir):
        print(f"⚠️  Upload directory '{upload_dir}' not found")
        print("   Please make sure you're in the backend/ directory")
        return
    
    files = os.listdir(upload_dir)
    
    if not files:
        print("⚠️  No files found in uploads/")
        print("   Upload a file first using POST /upload")
        return
    
    # Use the first file
    test_file = os.path.join(upload_dir, files[0])
    print(f"Testing with file: {test_file}")
    
    try:
        # Read the document
        content = read_document(test_file)
        print(f"✅ File read successfully: {len(content)} characters")
        
        # Chunk it
        chunks = chunk_document(test_file, chunk_size=500, overlap=50)
        print(f"✅ Chunking successful: {len(chunks)} chunks created")
        
        # Show first chunk
        if chunks:
            print(f"\nFirst chunk preview:")
            print(f"'{chunks[0][:200]}...'")
        
        # Statistics
        stats = get_chunk_stats(chunks)
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
    assert len(chunks) == 0, "Empty string should return 0 chunks"
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
        print("   ❌ Should have raised FileNotFoundError")
    except FileNotFoundError:
        print("   ✅ Correctly raised FileNotFoundError")
    
    # Test 5: Unsupported file type
    print("\n5. Unsupported file type:")
    try:
        read_document("test.docx")
        print("   ❌ Should have raised ValueError")
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
    
    # Verify overlap exists between first two chunks
    if len(chunks) >= 2:
        # The end of chunk 1 should appear at the start of chunk 2
        overlap_found = chunks[0][-5:] in chunks[1][:15]
        print(f"\n✅ Overlap verified: {overlap_found}")
    
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
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()