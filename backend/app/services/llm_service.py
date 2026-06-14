"""LLM service for generation"""
from app.config import settings
from typing import Optional

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        return "Generated response based on the context and query provided."
