AI-powered document Q&A system for intelligent information retrieval

🎯 Project Overview

OpsChat-lite is a full-stack web application that allows users to upload documents, search through them, and ask natural language questions to receive AI-generated answers with citations. Built as a portfolio project to demonstrate modern web development and AI integration skills.

✨ Key Features (Planned)

📤 Document Upload - Support for TXT, MD, and PDF files
🔍 Semantic Search - Find relevant content using AI embeddings
💬 AI-Powered Q&A - Ask questions and get contextual answers with citations
🎨 Clean Interface - Simple, responsive vanilla JavaScript frontend
🚀 RESTful API - Well-documented FastAPI backend
🛠️ Tech Stack

Backend:

Python 3.10+
FastAPI (async web framework)
SQLite (document & chunk storage)
OpenAI API (embeddings & chat)
Frontend:

HTML5 + CSS3
Vanilla JavaScript (ES6+)
Fetch API for backend communication
Tools & Deployment:

Docker (containerization)
pytest (testing)
GitHub Actions (CI/CD)
OpsChat Lite

A document question-answering system with AI-powered search and retrieval. Built with Python and FastAPI as a learning project to demonstrate backend development, database integration, and AI API usage.

Project Status

🚧 Phase 1 Complete - Foundation with document storage and basic search functionality

This project is actively being developed as part of a structured learning plan. Currently implemented features represent Phase 1 of a 3-phase roadmap.

What It Does

OpsChat Lite allows users to upload documents and ask questions about their content. The system breaks documents into searchable chunks and will eventually use AI to provide intelligent, cited answers.

Currently Implemented (Phase 1):

FastAPI backend with RESTful endpoints
SQLite database for document and chunk storage
Health check and ping endpoints
Database initialization and management
Project structure ready for file upload and indexing features
Planned Features (Phase 2-3):

Document upload and text extraction
Intelligent text chunking
Embedding-based semantic search
AI-powered question answering with citations
React frontend interface
Technology Stack

Backend Framework: FastAPI (Python 3.10+)
Database: SQLite with plans to migrate to PostgreSQL with pgvector
API Server: Uvicorn
Future Integrations: OpenAI API for embeddings and chat
Why This Project?

This project demonstrates practical full-stack development skills needed for software developer co-op positions:

RESTful API design and implementation
Database schema design and SQL operations
Modern Python web development with FastAPI
AI/ML API integration
Full-stack application architecture
📝 Architecture (High-Level)

┌─────────────┐
│   Browser   │
│  (HTML/JS)  │
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼──────────┐
│  FastAPI Backend│
│  - /upload      │
│  - /search      │
│  - /chat        │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  SQLite DB      │
│  - documents    │
│  - chunks       │
│  - embeddings   │
└─────────────────┘
🚀 Getting Started

Setup instructions will be added as development progresses.

Prerequisites

Python 3.10 or higher
pip (Python package manager)
OpenAI API key
Installation

# Coming soon
📖 API Documentation

API endpoints will be documented here as they're implemented.

🧪 Testing

Test suite information will be added during development.

📦 Project Structure

doc-chat-ai/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── rag.py           # AI/RAG logic
│   ├── chunking.py      # Text processing
│   ├── db.py            # Database helpers
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   └── ARCHITECTURE.md
├── tests/
├── .gitignore
├── README.md
└── LICENSE
🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

🙏 Acknowledgments

FastAPI documentation and community
OpenAI API documentation
Inspiration from modern RAG implementations
Note: This project is under active development as part of a 10-week learning journey (Oct-Dec 2025). Check back for updates!