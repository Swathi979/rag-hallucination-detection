"""Trust score calculation"""
from typing import Dict, Any, List
from app.config import settings

class TrustScoreCalculator:
    def __init__(self):
        self.weight_similarity = settings.WEIGHT_SIMILARITY
        self.weight_coverage = settings.WEIGHT_COVERAGE
        self.weight_citation = settings.WEIGHT_CITATION
        self.weight_confidence = settings.WEIGHT_CONFIDENCE
    
    def calculate(self, query_text: str, answer: str, retrieved_context: List[Dict[str, Any]], hallucination_scores: Dict[str, float]) -> Dict[str, Any]:
        similarity_score = hallucination_scores.get('similarity_score', 0.5)
        coverage_score = hallucination_scores.get('coverage_score', 0.5)
        confidence_score = hallucination_scores.get('confidence_score', 0.5)
        citation_support = self._calculate_citation_support(answer, retrieved_context)
        
        final_trust_score = (
            self.weight_similarity * similarity_score +
            self.weight_coverage * coverage_score +
            self.weight_citation * citation_support +
            self.weight_confidence * confidence_score
        ) * 100
        
        risk_level = "high" if final_trust_score < 40 else "medium" if final_trust_score < 70 else "low"
        
        return {
            "similarity_score": similarity_score,
            "coverage_score": coverage_score,
            "citation_support": citation_support,
            "confidence_score": confidence_score,
            "final_trust_score": final_trust_score,
            "risk_level": risk_level,
            "has_contradictions": False,
            "unsupported_claims": 0,
            "explanation": f"Trust Score: {final_trust_score:.1f}/100. Risk level: {risk_level}.",
            "evidence_chunks": retrieved_context,
        }
    
    def _calculate_citation_support(self, answer: str, context: List[Dict[str, Any]]) -> float:
        if not context:
            return 0.5
        return 0.75
