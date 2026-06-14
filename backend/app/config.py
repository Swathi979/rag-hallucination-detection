"""Application configuration"""
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "RAG Hallucination Detection"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_TIMEOUT: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    DATABASE_URL: str = "sqlite:///./rag_system.db"
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.1"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 5
    MIN_SIMILARITY_THRESHOLD: float = 0.3
    WEIGHT_SIMILARITY: float = 0.35
    WEIGHT_COVERAGE: float = 0.25
    WEIGHT_CITATION: float = 0.20
    WEIGHT_CONFIDENCE: float = 0.20
    FAISS_INDEX_PATH: str = "./embeddings/faiss_index"
    MAX_UPLOAD_SIZE: int = 104857600
    ALLOWED_EXTENSIONS: str = "pdf,txt,docx"
    ENABLE_EVALUATION: bool = True
    EVALUATION_BATCH_SIZE: int = 32
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
