"""Query processing routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import time
from app.database import Query, SessionLocal, TrustScore
from app.services.rag_pipeline import RAGPipeline
from app.services.hallucination_detector import HallucinationDetector
from app.trust_scoring.calculator import TrustScoreCalculator
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    query_text: str
    document_id: str = None
    top_k: int = 5

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/query")
async def process_query(query_data: QueryRequest, db: Session = Depends(get_db)):
    try:
        query_id = str(uuid.uuid4())
        start_time = time.time()
        
        rag_pipeline = RAGPipeline()
        retrieved_context = rag_pipeline.retrieve(query_data.query_text, top_k=query_data.top_k)
        answer = rag_pipeline.generate(query_data.query_text, retrieved_context)
        
        detector = HallucinationDetector()
        hallucination_scores = detector.detect(query_data.query_text, answer, retrieved_context)
        
        calculator = TrustScoreCalculator()
        trust_score_data = calculator.calculate(
            query_text=query_data.query_text,
            answer=answer,
            retrieved_context=retrieved_context,
            hallucination_scores=hallucination_scores
        )
        
        query = Query(
            id=query_id,
            query_text=query_data.query_text,
            answer=answer,
            retrieved_context=str(retrieved_context),
            top_k=query_data.top_k,
            processing_time=time.time() - start_time,
        )
        
        db.add(query)
        db.flush()
        
        trust_score = TrustScore(
            id=str(uuid.uuid4()),
            query_id=query_id,
            **trust_score_data
        )
        
        db.add(trust_score)
        db.commit()
        
        return {
            "id": query_id,
            "query": query_data.query_text,
            "answer": answer,
            "trust_score": trust_score_data["final_trust_score"],
            "risk_level": trust_score_data["risk_level"],
            "processing_time": query.processing_time
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/query/{query_id}")
async def get_query(query_id: str, db: Session = Depends(get_db)):
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    trust_score = query.trust_scores
    return {
        "id": query.id,
        "query": query.query_text,
        "answer": query.answer,
        "trust_score": trust_score.final_trust_score if trust_score else None,
        "risk_level": trust_score.risk_level if trust_score else None
    }
