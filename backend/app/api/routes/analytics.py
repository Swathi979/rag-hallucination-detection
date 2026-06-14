"""Analytics routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import Query, TrustScore, Document, SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    total_queries = db.query(func.count(Query.id)).scalar() or 0
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    
    trust_scores = db.query(TrustScore.final_trust_score).all()
    avg_trust_score = sum([ts[0] for ts in trust_scores]) / len(trust_scores) if trust_scores else 0
    
    hallucinations = db.query(func.count(TrustScore.id)).filter(
        TrustScore.risk_level.in_(["high", "medium"])
    ).scalar() or 0
    hallucination_rate = (hallucinations / total_queries * 100) if total_queries > 0 else 0
    
    avg_processing_time = db.query(func.avg(Query.processing_time)).scalar() or 0
    
    trust_dist = {
        "high_risk": db.query(func.count(TrustScore.id)).filter(TrustScore.final_trust_score < 40).scalar() or 0,
        "medium_risk": db.query(func.count(TrustScore.id)).filter(TrustScore.final_trust_score.between(40, 70)).scalar() or 0,
        "reliable": db.query(func.count(TrustScore.id)).filter(TrustScore.final_trust_score > 70).scalar() or 0,
    }
    
    risk_dist = {
        "high": db.query(func.count(TrustScore.id)).filter(TrustScore.risk_level == "high").scalar() or 0,
        "medium": db.query(func.count(TrustScore.id)).filter(TrustScore.risk_level == "medium").scalar() or 0,
        "low": db.query(func.count(TrustScore.id)).filter(TrustScore.risk_level == "low").scalar() or 0,
    }
    
    recent = db.query(Query).order_by(Query.created_at.desc()).limit(10).all()
    recent_queries = [{"id": q.id, "query": q.query_text[:50], "time": q.processing_time} for q in recent]
    
    return {
        "total_queries": total_queries,
        "total_documents": total_documents,
        "average_trust_score": avg_trust_score,
        "hallucination_rate": hallucination_rate,
        "avg_processing_time": avg_processing_time,
        "trust_distribution": trust_dist,
        "risk_distribution": risk_dist,
        "recent_queries": recent_queries
    }
