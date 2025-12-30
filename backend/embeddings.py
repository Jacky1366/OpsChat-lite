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




# Combines your chunks + question into a properly formatted prompt for OpenAI
def build_rag_prompt(question: str, chunks: list) -> list:
    """
    Build a prompt for RAG by combining the question with relevant chunks.
    
    Args:
        question: The user's question
        chunks: List of relevant chunk dictionaries with 'chunk_text' and 'filename'
        
    Returns:
        list: Messages formatted for OpenAI Chat API
    """
    # Build the context from chunks
    context = ""
    for i, chunk in enumerate(chunks, 1):
        context += f"\n--- Chunk {i} (from {chunk['filename']}) ---\n"
        context += chunk['chunk_text']
        context += "\n"
    
    # System message: Instructions that guide HOW the AI should behave
    system_message = """You are a helpful assistant that answers questions based ONLY on the provided document context.

Rules:
- Answer using ONLY the information in the provided chunks
- If the answer is not in the chunks, say "I don't have enough information to answer that question based on the available documents."
- Be concise and accurate
- When you use information from a chunk, mention which chunk number(s) you used
- Do not make up information or use external knowledge"""

    # User message: The actual content + question
    user_message = f"""Here are relevant document chunks:
    {context}

    Based ONLY on the above chunks, please answer this question:
    {question}"""

    # Formated RAG prompt for OpenAI API 
    messages = [
        {"role": "system", "content": system_message}, # return the first list of dictionaries
        {"role": "user", "content": user_message} # return the second list of dictionaries
    ]
    
    return messages




# Calls OpenAI's Chat Completions API to generate an answer
def get_rag_answer(question: str, chunks: list) -> dict:
    """
    Generate an AI answer to a question using RAG (Retrieval Augmented Generation).
    
    Args:
        question: The user's question
        chunks: List of relevant chunks retrieved by semantic search
        
    Returns:
        dict: Contains 'answer' and 'model' used
    """
    try:
        # Build the prompt
        messages = build_rag_prompt(question, chunks)
        
        # Call OpenAI Chat Completions API
        response = client.chat.completions.create(  # client is the OpenAI API key
            model=config.CHAT_MODEL,  # gpt-4o-mini
            messages=messages,
            temperature=0.3,  # Lower = more focused, higher = more creative
            max_tokens=500    # Limit response length
        )
        
        # Extract the answer
        answer = response.choices[0].message.content # answer is a regular Python string
        """
        response (big box)
            └─ choices (list of smaller boxes)
                └─ [0] (first small box)
                    └─ message (tiny box)
                        └─ content (the actual text you want)
        """

        
        return {
            "answer": answer,
            "model": config.CHAT_MODEL
        }
        
    except Exception as e:
        print(f"❌ Error generating RAG answer: {e}")
        raise





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
