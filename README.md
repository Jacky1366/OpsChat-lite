# OpsChat-lite

**AI-Powered Document Q&A System with Retrieval-Augmented Generation (RAG)**

A full-stack application that enables intelligent document search and question-answering using semantic retrieval and OpenAI's language models. Built as a portfolio project demonstrating practical RAG implementation, backend API development, and AI integration skills.

---

## 🎯 Project Status: **Phase 2 Complete** ✅

**Working Features:**
- ✅ Document upload and storage
- ✅ Intelligent text chunking with overlap
- ✅ OpenAI embeddings generation and storage
- ✅ Semantic search using cosine similarity
- ✅ RAG-based question answering with source citations
- ✅ FastAPI backend with RESTful endpoints
- ✅ SQLite database with document and chunk management

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   Client/User   │
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────────────────────────┐
│      FastAPI Backend                │
│  ┌─────────────────────────────┐    │
│  │ Endpoints:                  │    │
│  │ • POST /upload              │    │
│  │ • POST /index/{doc_id}      │    │
│  │ • GET  /search              │    │
│  │ • POST /chat                │    │
│  └─────────────────────────────┘    │
└────────┬───────────────┬────────────┘
         │               │
         ▼               ▼
┌─────────────────┐  ┌──────────────┐
│  SQLite Database│  │  OpenAI API  │
│  • documents    │  │  • Embeddings│
│  • chunks       │  │  • Chat      │
└─────────────────┘  └──────────────┘
```

## 🔄 RAG Pipeline

1. **Document Upload** → Store document metadata and content
2. **Chunking** → Split text into overlapping segments (500 chars, 100 char overlap)
3. **Embedding** → Generate vector embeddings using OpenAI's text-embedding-3-small
4. **Indexing** → Store chunks and embeddings in SQLite
5. **Retrieval** → When user asks question:
   - Generate query embedding
   - Find top-k similar chunks using cosine similarity
   - Retrieve relevant context
6. **Generation** → Send context + question to GPT-4o-mini for answer with citations

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.10+
- FastAPI (async web framework)
- SQLite (document and chunk storage)
- OpenAI API (text-embedding-3-small, gpt-4o-mini)

**Key Libraries:**
- `fastapi` - Web framework
- `openai` - OpenAI API client
- `sqlite3` - Database operations
- `uvicorn` - ASGI server

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Jacky1366/OpsChat-lite.git
cd OpsChat-lite
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create a .env file or set environment variable
export OPENAI_API_KEY='your-api-key-here'
```

4. **Initialize database**
```bash
cd backend
python database.py  # Creates opschat.db with required tables
```

5. **Run the server**
```bash
python main.py
# Server starts at http://localhost:8000
```

---

## 📡 API Endpoints

### Health Check
```bash
GET /ping
# Returns: {"status": "healthy"}
```

### Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

# Upload a text file
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.txt"

# Returns: {"document_id": 1, "filename": "sample.txt"}
```

### Index Document (Generate Embeddings)
```bash
POST /index/{doc_id}

# Process and generate embeddings for document
curl -X POST http://localhost:8000/index/1

# Returns: {
#   "document_id": 1,
#   "chunks_created": 15,
#   "embeddings_generated": 15
# }
```

### Semantic Search
```bash
GET /search?q={query}&k={num_results}

# Search for relevant chunks
curl "http://localhost:8000/search?q=machine%20learning&k=3"

# Returns: {
#   "query": "machine learning",
#   "results": [
#     {
#       "chunk_id": 5,
#       "document_id": 1,
#       "text": "...",
#       "similarity": 0.87
#     },
#     ...
#   ]
# }
```

### AI Question Answering (RAG)
```bash
POST /chat
Content-Type: application/json

# Ask a question about uploaded documents
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main benefits of machine learning?",
    "top_k": 5
  }'

# Returns: {
#   "query": "What are the main benefits of machine learning?",
#   "answer": "Based on the documents, the main benefits include...",
#   "sources": [
#     {"chunk_id": 5, "document_id": 1, "similarity": 0.87},
#     {"chunk_id": 12, "document_id": 1, "similarity": 0.82}
#   ]
# }
```

---

## 🧪 Example Usage

```bash
# 1. Start the server
python backend/main.py

# 2. Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@research_paper.txt"
# Response: {"document_id": 1, "filename": "research_paper.txt"}

# 3. Index the document (generate embeddings)
curl -X POST http://localhost:8000/index/1
# Response: {"document_id": 1, "chunks_created": 42, "embeddings_generated": 42}

# 4. Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What methodology was used in the study?", "top_k": 3}'
# Response: AI-generated answer with source citations
```

---

## 📂 Project Structure

```
OpsChat-lite/
├── backend/
│   ├── main.py              # FastAPI application and endpoints
│   ├── database.py          # SQLite schema and operations
│   ├── chunking.py          # Text chunking logic
│   ├── embeddings.py        # OpenAI embeddings integration
│   ├── config.py            # Configuration management
│   ├── test_chunking.py     # Unit tests for chunking
│   ├── uploads/             # Uploaded document storage
│   └── requirements.txt     # Python dependencies
├── README.md                # This file
├── project_overview.md      # Detailed project plan
└── .gitignore              # Git ignore rules
```

---

## 🔑 Key Implementation Details

### Text Chunking Strategy
- **Chunk size:** 500 characters
- **Overlap:** 100 characters (20%)
- **Purpose:** Balance between context preservation and retrieval granularity

### Embedding Model
- **Model:** text-embedding-3-small (OpenAI)
- **Dimensions:** 1536
- **Storage:** SQLite BLOB field with JSON serialization

### Retrieval Strategy
- **Method:** Cosine similarity between query and chunk embeddings
- **Ranking:** Top-k most similar chunks (default k=5)
- **Context Window:** Multiple chunks combined for richer context

### Answer Generation
- **Model:** gpt-4o-mini (OpenAI)
- **Prompt Engineering:** System prompt instructs model to use only provided context
- **Citation:** Returns source chunk IDs and similarity scores

---

## 🎓 Learning Outcomes

This project demonstrates practical skills in:
- **Backend Development:** RESTful API design with FastAPI
- **Database Design:** SQLite schema for documents, chunks, and embeddings
- **AI Integration:** OpenAI API usage for embeddings and chat completion
- **RAG Architecture:** Implementing retrieval-augmented generation pipeline
- **Vector Search:** Semantic similarity using embeddings and cosine distance
- **Async Programming:** Python async/await patterns
- **API Documentation:** Clear endpoint documentation and examples

---

## 🚧 Future Enhancements (Phase 3)

- [ ] Frontend interface (vanilla JavaScript or React)
- [ ] Support for PDF documents
- [ ] PostgreSQL with pgvector for production-scale vector search
- [ ] User authentication and document permissions
- [ ] Docker containerization
- [ ] Unit and integration tests
- [ ] CI/CD pipeline with GitHub Actions

---

## 🤝 Why This Project?

Built as a portfolio project to demonstrate modern software development skills relevant to co-op positions:
- Full-stack application architecture
- Modern Python web frameworks (FastAPI)
- AI/ML integration and practical RAG implementation
- Database design and query optimization
- RESTful API best practices
- Clear documentation and code organization

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Jacky Huang**  
Third-year Bachelor of Technology in Information Technology  
Kwantlen Polytechnic University

**Contact:**
- GitHub: [@Jacky1366](https://github.com/Jacky1366)
- Email: yichi.huang@student.kpu.ca
- LinkedIn: [linkedin.com/in/jacky-huang-a43420197](https://www.linkedin.com/in/jacky-huang-a43420197)

---

**Note:** This project represents Phase 2 completion of a 3-phase development plan. The backend RAG system is fully functional and demonstrates practical AI/ML application development. Frontend interface (Phase 3) is planned for future implementation.