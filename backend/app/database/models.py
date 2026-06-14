"""SQLAlchemy database models"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    doc_name = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    content = Column(Text)
    num_chunks = Column(Integer, default=0)
    num_embeddings = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    queries = relationship("Query", back_populates="document")

class Query(Base):
    __tablename__ = "queries"
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, index=True)
    query_text = Column(Text)
    answer = Column(Text)
    retrieved_context = Column(Text)
    top_k = Column(Integer, default=5)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    trust_scores = relationship("TrustScore", uselist=False, back_populates="query")
    document = relationship("Document", back_populates="queries")

class TrustScore(Base):
    __tablename__ = "trust_scores"
    id = Column(String, primary_key=True, index=True)
    query_id = Column(String, index=True)
    similarity_score = Column(Float)
    coverage_score = Column(Float)
    citation_support = Column(Float)
    confidence_score = Column(Float)
    final_trust_score = Column(Float)
    risk_level = Column(String)
    has_contradictions = Column(Boolean, default=False)
    contradiction_details = Column(Text)
    unsupported_claims = Column(Integer, default=0)
    explanation = Column(Text)
    evidence_chunks = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    query = relationship("Query", back_populates="trust_scores")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id = Column(String, primary_key=True, index=True)
    evaluation_type = Column(String)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    accuracy = Column(Float)
    metrics = Column(JSON)
    config = Column(JSON)
    results_summary = Column(Text)
    detailed_results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
