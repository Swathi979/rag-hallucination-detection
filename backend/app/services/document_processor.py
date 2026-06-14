"""Document processing service"""
import PyPDF2
from pathlib import Path
from typing import List
from docx import Document as DocxDocument
from app.config import settings

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        if file_type == "pdf":
            return self._extract_pdf(file_path)
        elif file_type == "txt":
            return self._extract_txt(file_path)
        elif file_type == "docx":
            return self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
        except:
            text = "Error extracting PDF"
        return text
    
    def _extract_txt(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "Error extracting TXT"
    
    def _extract_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = DocxDocument(file_path)
            for para in doc.paragraphs:
                text += para.text + "\\n"
        except:
            text = "Error extracting DOCX"
        return text
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        if chunk_size is None:
            chunk_size = self.chunk_size
        if overlap is None:
            overlap = self.chunk_overlap
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return [chunk.strip() for chunk in chunks if chunk.strip()]
