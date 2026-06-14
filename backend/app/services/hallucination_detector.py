"""Hallucination detection service"""
from typing import Dict, Any, List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

class HallucinationDetector:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def detect(self, query: str, answer: str, context: List[Dict[str, Any]]) -> Dict[str, float]:
        similarity_score = self._calculate_similarity(answer, str(context))
        coverage_score = self._calculate_coverage(answer, str(context))
        confidence_score = self._estimate_confidence(answer, str(context))
        return {
            "similarity_score": similarity_score,
            "coverage_score": coverage_score,
            "confidence_score": confidence_score,
            "has_contradictions": False,
        }
    
    def _calculate_similarity(self, answer: str, context: str) -> float:
        try:
            answer_embedding = self.model.encode([answer])
            context_embedding = self.model.encode([context[:512]])
            similarity = cosine_similarity(answer_embedding, context_embedding)[0][0]
            return min(1.0, max(0.0, similarity))
        except:
            return 0.5
    
    def _calculate_coverage(self, answer: str, context: str) -> float:
        sentences = answer.split('.')
        covered = 0
        for sentence in sentences:
            if len(sentence.strip()) > 5 and sentence.lower() in context.lower():
                covered += 1
        return covered / len(sentences) if sentences else 0.5
    
    def _estimate_confidence(self, answer: str, context: str) -> float:
        return 0.7
