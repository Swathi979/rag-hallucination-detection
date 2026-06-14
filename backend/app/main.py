"""FastAPI main application"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.api.routes import documents, queries, analytics, health, evaluation, export

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG Hallucination Detection System")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down RAG system")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready RAG-based hallucination detection framework",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZIPMiddleware, minimum_size=1000)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(queries.router, prefix="/api", tags=["Queries"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(evaluation.router, prefix="/api", tags=["Evaluation"])
app.include_router(export.router, prefix="/api", tags=["Export"])

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Error: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "type": type(exc).__name__})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL.lower())
