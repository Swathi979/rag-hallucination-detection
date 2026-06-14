"""Database module"""
from app.database.base import Base, engine, SessionLocal
from app.database.models import Document, Query, EvaluationResult, TrustScore

def init_db():
    Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine", "SessionLocal", "Document", "Query", "EvaluationResult", "TrustScore", "init_db"]
