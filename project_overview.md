DOpsChat-lite-AI — Project Overview

🎯 Elevator Pitch

OpsChat-lite-AI is a full-stack web application that lets users upload documents, search through them semantically, and ask natural language questions to receive AI-grounded answers with citations. It demonstrates practical skills across backend API development, database design, AI/ML integration, and modern frontend development—ideal for software developer co-op roles.

🎓 Why This Project?

Skills Demonstrated

RESTful API development with Python FastAPI
Database design and SQL integration (SQLite)
AI/ML integration using OpenAI embeddings and chat models
Frontend development with vanilla JavaScript
Full-stack architecture and API communication
RAG (Retrieval Augmented Generation) implementation
Clean code practices and professional documentation
Job Alignment

This project maps directly to co-op job requirements:

Delta Python Developer ✅

Python with FastAPI (specifically mentioned as bonus)
OpenAI API integration experience
Linux environment deployment ready
SAP Software Developer ✅

JavaScript frontend
Backend development experience
Full-stack project demonstration
Aquatic Informatics ✅

Full-stack development
JavaScript + modern practices
Problem-solving and technical skills
📋 Project Scope (MVP)

Core Features

✅ Upload documents (.txt, .md; PDFs optional later)
✅ Text chunking and indexing to database
✅ Semantic search using embeddings
✅ AI-powered Q&A with citations
✅ Clean web interface for all operations
Non-Goals (Keeping it Simple)

❌ Multi-user authentication (JWT optional in stretch)
❌ Vector databases (pgvector optional in stretch)
❌ Real-time streaming responses
❌ Microservices architecture
❌ Complex PDF OCR (plain text extraction only)
🛠️ Tech Stack

Backend

Python 3.10+ - Core language
FastAPI - Async web framework
Uvicorn - ASGI server
SQLite - Database (Postgres + pgvector optional later)
OpenAI API - Embeddings and chat completions
Frontend

HTML5 + CSS3 - Structure and styling
Vanilla JavaScript (ES6+) - Interactivity
Fetch API - HTTP requests to backend
Development Tools

pytest - Testing framework
Docker - Containerization (optional)
GitHub Actions - CI/CD (optional)
🏗️ Architecture

┌─────────────────────────────────────┐
│         Browser (Frontend)          │
│     HTML + CSS + JavaScript         │
│  - Upload form                      │
│  - Search interface                 │
│  - Chat interface                   │
└─────────────┬───────────────────────┘
              │
              │ HTTP/REST (fetch)
              │
┌─────────────▼───────────────────────┐
│      FastAPI Backend (Python)       │
│                                     │
│  POST /upload    - Save documents   │
│  POST /index     - Chunk & embed    │
│  GET  /search    - Find chunks      │
│  POST /chat      - AI Q&A           │
│                                     │
└─────────────┬───────────────────────┘
              │
              │ SQL queries
              │
┌─────────────▼───────────────────────┐
│         SQLite Database             │
│                                     │
│  documents  - File metadata         │
│  chunks     - Text segments         │
│  embeddings - Vector representations│
│                                     │
└─────────────────────────────────────┘
              │
              │ API calls
              │
┌─────────────▼───────────────────────┐
│          OpenAI API                 │
│  - text-embedding-3-small           │
│  - gpt-4 or gpt-3.5-turbo           │
└─────────────────────────────────────┘
📅 10-Week Development Timeline

Total Duration: October 1 - December 15, 2025
Pace: 8-12 hours/week (medium pace)

Phase 1: Foundation (Weeks 1-2)

Goal: Python basics + FastAPI setup

Deliverables:

Development environment configured
Basic FastAPI application running
GET /ping endpoint for health check
Virtual environment and dependencies
Acceptance Criteria:

Server starts without errors
Can make HTTP requests to /ping
Basic understanding of Python web development
Phase 2: Backend Core (Weeks 3-4)

Goal: File handling + Database setup

Deliverables:

POST /upload endpoint - accepts file uploads
SQLite database with documents table
File storage on disk
Basic error handling and validation
Acceptance Criteria:

Files upload successfully via API
Metadata stored in database
Files saved to /uploads directory
Proper error responses for invalid inputs
Phase 3: Search Foundation (Weeks 5-6)

Goal: Text chunking + Basic search

Deliverables:

Text chunking logic (split documents into segments)
chunks table in database
POST /index endpoint - process documents
GET /search?q=keyword&k=5 - keyword search
Acceptance Criteria:

Documents split into meaningful chunks
Chunks stored with document references
Search returns relevant snippets
Top-k results ranked by relevance
Phase 4: AI Integration (Weeks 7-8)

Goal: Embeddings + AI Q&A

Deliverables:

OpenAI API integration
Embedding generation and storage
Semantic search using cosine similarity
POST /chat endpoint - AI answers with citations
Acceptance Criteria:

Embeddings computed for all chunks
Search uses semantic similarity (better than keyword)
AI returns contextual answers
Responses include chunk citations
Phase 5: Frontend (Weeks 9-10)

Goal: User interface

Deliverables:

index.html - main page structure
styles.css - responsive design
app.js - API interactions
Upload, search, and chat interfaces
Acceptance Criteria:

Users can upload files through UI
Search displays results dynamically
Chat interface shows questions and answers
Error messages displayed appropriately
Phase 6: Polish & Deploy (Week 11 - Buffer)

Goal: Documentation + Optional deployment

Deliverables:

Comprehensive README with examples
Code comments and docstrings
Screenshots and demo video (optional)
Docker setup (optional)
Deploy to cloud VM (optional)
Acceptance Criteria:

README covers setup and usage
Code is clean and documented
Project is portfolio-ready
🎯 Success Metrics

Technical Demonstrations

✅ RESTful API with multiple endpoints
✅ Database design with relationships
✅ AI/ML API integration
✅ Frontend-backend communication
✅ Error handling and validation
Resume-Ready Accomplishments

"Built full-stack document Q&A system with Python/FastAPI backend and JavaScript frontend"
"Implemented semantic search using OpenAI embeddings and cosine similarity for document retrieval"
"Designed RESTful API with SQLite database for document storage and chunk indexing"
"Created AI-powered chat interface providing contextual answers with source citations"
Portfolio Assets

Live demo application (or video)
Clean GitHub repository
Professional documentation
Technical architecture diagrams
📂 Repository Structure

doc-chat-ai/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── rag.py              # RAG logic (embeddings, retrieval, chat)
│   ├── chunking.py         # Text splitting utilities
│   ├── db.py               # Database helpers
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # Uploaded documents (gitignored)
│   └── data/               # SQLite database (gitignored)
│
├── frontend/
│   ├── index.html          # Main page
│   ├── styles.css          # Styling
│   └── app.js              # JavaScript logic
│
├── docs/
│   ├── PROJECT_OVERVIEW.md # This file
│   ├── ARCHITECTURE.md     # Detailed architecture
│   └── API_DOCS.md         # Endpoint documentation
│
├── tests/
│   ├── test_chunking.py
│   ├── test_search.py
│   └── test_chat.py
│
├── .gitignore
├── README.md
├── LICENSE
└── Dockerfile              # Optional: containerization
🧪 Testing Strategy

Unit Tests

Text chunking logic
Embedding generation
Search ranking algorithms
Integration Tests

API endpoint functionality
Database operations
OpenAI API interactions (with mocks)
Manual Testing

Upload various file types
Search queries with different keywords
Ask diverse questions and verify citations
⚠️ Risks & Mitigations

Risk	Mitigation
OpenAI API rate limits	Cache embeddings in database
Large file processing	Set file size limits, chunk incrementally
Slow embedding generation	Process in background, show progress
Poor PDF text extraction	Start with TXT/MD, add PDFs later
Scope creep	Each phase is independently shippable
🔮 Future Enhancements (Post-MVP)

Security & Auth

JWT authentication for uploads
Rate limiting per user
Input sanitization improvements
Database Upgrades

PostgreSQL + pgvector for production
Full-text search optimization
Caching layer (Redis)
Advanced Features

Multi-document conversations
Document comparison queries
Export conversation history
Support for more file types (DOCX, PPTX)
DevOps

Automated testing in CI/CD
Docker Compose for easy deployment
Monitoring and logging (Prometheus/Grafana)
Security scanning (OWASP ZAP, Trivy)
📚 Learning Resources

Python & FastAPI

FastAPI official tutorial
Python virtual environments
Async/await concepts
AI/RAG

OpenAI API documentation
Embedding models overview
RAG architecture patterns
Frontend

MDN Web Docs (JavaScript, Fetch API)
CSS Grid and Flexbox
Responsive design principles
🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to:

Open issues for bugs or suggestions
Fork and experiment
Share learning resources
This document will be updated as the project progresses.