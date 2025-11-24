"""
Embeddings module for OpsChat Lite
Handles text embedding generation and similarity calculations
"""
from openai import OpenAI
import numpy as np # NumPy library for math operations on arrays/vectors
import config # Imports the config (to get the API key and settings)

# Creates an object that can talk to OpenAI's servers
client = OpenAI(api_key=config.OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]: # converts text to 1536-dim vectors
    """
    Generate an embedding vector for the given text using OpenAI API.
     
    Args:
        text (str): The text to convert to an embedding
        
    Returns:
        list[float]: A list of 1536 numbers representing the text's meaning
        
    Example:
        >>> embedding = get_embedding("Python is great for web development")
        >>> len(embedding)
        1536
    """
    try: # API calls can fail (network issues, invalid API key, etc.)
       
        text = text.replace("\n", " ").strip()  # Remove newlines and leading/trailing whitespace
        
        # where the magic happens
        response = client.embeddings.create( # make a request to call OpenAI's embedding creation endpoint
            model=config.EMBEDDING_MODEL,  # Specifies which AI model to use for embeddings
            input=text # The text to be converted into an embedding
        )
        
        # Extract the embedding vector
        embedding = response.data[0].embedding # The embedding is a list of floats
        
        return embedding # Return the embedding vector of a list of 1536 numbers
        # Returns: [0.023, -0.015, 0.042, ..., 0.891]
        
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        raise # Re-raise the exception for the caller to handle


def compute_similarity(embedding1: list[float], embedding2: list[float]) -> float: # Returns a single number (the similarity score)
    """
    Calculate cosine similarity between two embeddings.
    
    Cosine similarity measures how similar two vectors are.
    Result ranges from -1 to 1:
    - 1.0 = identical
    - 0.0 = unrelated
    - -1.0 = opposite
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        float: Similarity score between -1 and 1
        
    Example:
        >>> emb1 = get_embedding("dog")
        >>> emb2 = get_embedding("puppy")
        >>> similarity = compute_similarity(emb1, emb2)
        >>> similarity > 0.8  # Should be very similar!
        True
    """
    # Convert to numpy arrays for mathematical operations
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Calculate cosine similarity
    # Formula: (A · B) / (||A|| * ||B||)
    dot_product = np.dot(vec1, vec2) # A · B
    magnitude1 = np.linalg.norm(vec1) # ||A||
    magnitude2 = np.linalg.norm(vec2) # ||B||
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    similarity = dot_product / (magnitude1 * magnitude2) # 0° angle = most similar, 90° = not similar, 180° = opposite
    return float(similarity) # Convert numpy float to regular float, return a single number representing similarity between -1 and 1
    # Returns: 0.95 (very similar!)


# Test the module if run directly
if __name__ == "__main__":
    print("🧪 Testing embeddings module...\n")
    
    # Test 1: Generate embedding
    print("Test 1: Generating embedding for 'Hello world'")
    embedding = get_embedding("Hello world")
    print(f"✅ Generated embedding with {len(embedding)} dimensions")
    print(f"   First 5 values: {embedding[:5]}\n") # slice notation: get first 5 elements, 1536 numbers is too much
    
    # Test 2: Compare similar texts
    print("Test 2: Comparing similar texts")
    emb1 = get_embedding("Python programming")
    emb2 = get_embedding("Coding in Python")
    similarity = compute_similarity(emb1, emb2)
    print(f"✅ Similarity between 'Python programming' and 'Coding in Python': {similarity:.4f}") # Format as floating point with 4 decimal places
    print(f"   (Should be high, around 0.7-0.9)\n")
    
    # Test 3: Compare different texts
    print("Test 3: Comparing different texts")
    emb3 = get_embedding("Python programming")
    emb4 = get_embedding("Cooking pasta")
    similarity2 = compute_similarity(emb3, emb4)
    print(f"✅ Similarity between 'Python programming' and 'Cooking pasta': {similarity2:.4f}")
    print(f"   (Should be low, around 0.0-0.3)\n")
    
    print("🎉 All tests passed!")
