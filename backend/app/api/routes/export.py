"""Export routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import io
import csv
from app.database import Query, SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/export/csv")
async def export_csv(db: Session = Depends(get_db)):
    try:
        queries = db.query(Query).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Query ID", "Query Text", "Answer", "Processing Time", "Created At"])
        for query in queries:
            writer.writerow([query.id, query.query_text[:50], query.answer[:50], query.processing_time, query.created_at])
        return {"data": output.getvalue()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
