# OpsChat Lite — Project Overview & 3‑Week Plan

## Elevator Pitch
**OpsChat Lite** is a small full‑stack app that lets users upload documents, search them, and ask questions with AI‑grounded answers and citations. It demonstrates practical skills across backend APIs, simple frontend, databases, and basic AI/RAG—ideal for software developer co‑op roles.

## Why This Project
- **Maps to many JDs:** REST APIs (FastAPI), data modeling (SQLite → Postgres), frontend basics (HTML/JS → React later), security hygiene, Docker/CI (Week 3 polish), plus AI retrieval for “wow”.  
- **Modular:** Start tiny and add features as separate, resume‑ready commits.

## Scope (MVP)
- Upload docs (`.txt`, `.md`; PDFs optional later).  
- Index: chunk + store in DB.  
- Search: return top‑k relevant chunks.  
- **AI Answer:** retrieve chunks → call chat model → answer with citations.  
- Single‑page frontend that calls the API.

## Non‑Goals (to keep it simple)
- No multi‑user auth or roles (JWT optional in stretch).  
- No fancy vector DB, no streaming, no microservices.  
- No large PDF OCR—plain text extraction only in MVP.

## Tech Stack
- **Backend:** Python 3.10+, FastAPI, Uvicorn, sqlite3 (pgvector/Postgres optional Week 3+).  
- **Frontend:** Single HTML/JS page (React + TS optional Week 3+).  
- **AI:** OpenAI‑compatible embeddings + chat model.  
- **Tooling (Week 3):** pytest (a few tests), Docker, GitHub Actions (build/test), basic security headers/rate limit.

---

## Architecture (MVP)
```
[Browser] --fetch()--> [FastAPI]
   |                         |
   | POST /upload            |  reads/saves files
   | POST /index             |  chunk_text() -> DB
   | GET  /search            |  naive/embedding retrieval
   | POST /chat              |  retrieve->prompt->LLM
                             v
                          [SQLite]
```

---

## Phases & Milestones

### Phase 1 — Foundation (Week 1)
**Goal:** Minimal API + DB + chunking + keyword search (no AI).  
**Deliverables:**
- `GET /ping`, `POST /upload`, `POST /index?doc_id=...`, `GET /search?q=&k=`
- SQLite schema: `documents`, `chunks`
- Basic CORS and validation
- Short README and sample docs
> See detailed Week 1 plan in **OPSCHAT_WEEK1_PLAN.md**

**Acceptance Criteria:**
- File uploads save to disk and DB.
- `/index` creates multiple chunks per document.
- `/search` returns plausible top‑k snippets.

---

### Phase 2 — Retrieval + AI Answers (Week 2)
**Goal:** Real RAG retrieval with embeddings + AI chat.  
**What to add:**
- Embedding pipeline: compute & store vectors per chunk.  
- Retrieval: cosine similarity top‑k.  
- `POST /chat` → retrieve → build prompt → call chat model → return `{answer, citations}`.  
- Update README with examples and screenshots.

**Acceptance Criteria:**
- `/search` ranks by embeddings (better than keyword).  
- `/chat` returns a grounded answer with 2–3 citations.  
- Handles empty/no‑index cases gracefully (helpful error).

---

### Phase 3 — Polish & Packaging (Week 3)
**Goal:** Make it “portfolio‑ready.”  
**What to add:**
- **Frontend polish:** simple single‑page HTML/JS UI (upload, search, ask).  
- **Robustness:** input validation, error messages, basic logging, config via env vars.  
- **Quality:** 3–6 pytest tests (chunking, search, chat happy path w/ stubs).  
- **Ops:** Dockerfile(s) + docker‑compose; one‑command run; CI (lint/test).  
- **Docs:** Final README (setup, API, architecture diagram) + demo script.

**Acceptance Criteria:**
- One‑command local start (compose or simple script).  
- Green CI for tests/build.  
- README and screenshots included.

---

## Stretch Roadmap (post‑Week 3)
- **Auth/JWT** (email/password) for uploads & chat.  
- **Postgres + pgvector** for scalable vector search.  
- **React + TypeScript** chat UI (or tiny Angular admin page to match certain JDs).  
- **Security gates:** OWASP ZAP baseline + Trivy in CI; security headers & rate limiting.  
- **Deployment:** Linux VM with systemd or Docker Compose.  
- **Caching/metrics:** Redis cache; Prometheus/Grafana.

---

## Repository Layout (suggested)
```
opschat-lite/
  backend/
    main.py
    rag.py            # embeddings, retrieval, AI answer
    chunking.py       # text splitting helper
    db.py             # SQLite helpers
    requirements.txt
    uploads/
    data/
  frontend/
    index.html
  README.md
  OPSCHAT_WEEK1_PLAN.md
  PROJECT_OVERVIEW.md
```

---

## Risks & Mitigations
- **LLM/API limits:** cache embeddings to DB; keep batch sizes small.  
- **Weak PDF text extraction:** start with .txt/.md; add PDFs after MVP.  
- **Time creep:** each phase is shippable; cut stretch items if needed.

---

## Demo Script (2 minutes)
1) Upload a doc → index it.  
2) Search for a keyword → show relevant snippets.  
3) Ask a question → show AI answer + citations.  
4) Show README and one‑command run.

---

## Resume Bullets (templates)
- Built a full‑stack RAG chatbot (FastAPI + HTML/JS + SQLite) enabling document upload, chunking, and semantic retrieval; added AI‑grounded answers with citations.  
- Implemented embeddings and cosine retrieval; documented architecture and shipped a one‑command local environment with basic tests and CI.

---

## Tailoring Notes (by JD)
- **Aquatic Informatics/SAP Dev:** emphasize REST, DB schema, frontend UI, tests, Docker.  
- **Delta (Python):** FastAPI focus, Linux‑ready, pytest; note clean code and typing.  
- **SAP Security:** basic hardening (headers, rate limit), optional CI ZAP/Trivy.  
- **Clio:** CRUD/search, pagination, README clarity; optional Rails/Angular page later.
