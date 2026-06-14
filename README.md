# RAG-Based Hallucination Detection & Trust Scoring Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-white.svg)](https://fastapi.tiangolo.com/)
[![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Objective

Production-ready AI research framework that detects hallucinations in Large Language Models using Retrieval-Augmented Generation (RAG), generates trust scores, and provides explainable evidence.

## Quick Start

### Docker Setup
```bash
git clone https://github.com/Swathi979/rag-hallucination-detection.git
cd rag-hallucination-detection
cp backend/.env.example backend/.env
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## Key Features

- Hallucination Detection with semantic analysis
- Trust Scoring Engine (0-100 scale)
- Document Processing (PDF, TXT, DOCX)
- RAG Pipeline with FAISS vector store
- Interactive Dashboard
- PDF/CSV Export
- Comprehensive Analytics

## API Endpoints

- POST /api/upload - Upload document
- POST /api/query - Process query
- GET /api/documents - List documents
- GET /api/analytics - Dashboard metrics
- GET /api/health - Health check

## Tech Stack

- Frontend: React 18, TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.9+
- AI: LangChain, FAISS, Sentence Transformers
- Database: SQLite
- Infrastructure: Docker, Docker Compose

## License

MIT License
