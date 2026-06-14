"""Document management routes"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from pathlib import Path
from app.database import Document, SessionLocal
from app.services.document_processor import DocumentProcessor
from app.config import settings

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), doc_name: str = None, db: Session = Depends(get_db)):
    allowed_extensions = settings.ALLOWED_EXTENSIONS.split(",")
    file_ext = Path(file.filename).suffix.lower().lstrip(".")
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File type .{file_ext} not allowed")
    
    try:
        doc_id = str(uuid.uuid4())
        filename = f"{doc_id}_{file.filename}"
        file_path = Path(f"./documents/{filename}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        file_path.write_bytes(content)
        
        processor = DocumentProcessor()
        text_content = processor.extract_text(str(file_path), file_ext)
        chunks = processor.chunk_text(text_content)
        
        doc = Document(
            id=doc_id,
            filename=filename,
            doc_name=doc_name or file.filename,
            file_path=str(file_path),
            file_type=file_ext,
            content=text_content,
            num_chunks=len(chunks),
        )
        
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        return {"id": doc.id, "filename": doc.filename, "doc_name": doc.doc_name, "chunks": len(chunks)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [{"id": d.id, "filename": d.filename, "doc_name": d.doc_name, "created_at": d.created_at} for d in documents]

@router.get("/documents/{doc_id}")
async def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": doc.id, "filename": doc.filename, "doc_name": doc.doc_name, "chunks": doc.num_chunks}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    Path(doc.file_path).unlink(missing_ok=True)
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted"}
