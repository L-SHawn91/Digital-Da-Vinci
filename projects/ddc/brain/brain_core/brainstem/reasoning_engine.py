"""
ReasoningEngine - Brainstem의 논리 추론
증거 기반 추론, 신뢰도 계산, 인과관계 추적
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class ConfidenceLevel(Enum):
    """신뢰도 레벨"""
    VERY_LOW = 0.2
    LOW = 0.4
    MODERATE = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.95


@dataclass
class Evidence:
    """증거"""
    claim: str
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    source_confidence: float = 0.7
    
    def strength(self) -> float:
        """증거의 강도 (0~1)"""
        support_score = len(self.supporting_evidence) * 0.15
        contra_score = len(self.contradicting_evidence) * 0.1
        base_score = self.source_confidence
        return min(0.95, max(0.1, base_score + support_score - contra_score))


@dataclass
class Reasoning:
    """추론 결과"""
    hypothesis: str
    confidence: float
    evidence: List[Evidence]
    logical_chain: List[str]  # 추론 과정 단계별 기록
    potential_biases: List[str] = field(default_factory=list)
    alternative_explanations: List[str] = field(default_factory=list)


class ReasoningEngine:
    """
    논리 추론 엔진
    - 증거 기반 추론
    - 신뢰도 정량 계산
    - 인과관계 추적
    - 한계 인식
    """
    
    def __init__(self):
        """추론 엔진 초기화"""
        self.reasoning_history: List[Reasoning] = []
        self.domain_expertise: Dict[str, float] = {
            "biology": 0.80,
            "finance": 0.60,
            "astronomy": 0.50,
            "literature": 0.70,
            "general": 0.65
        }
    
    def reason(
        self,
        hypothesis: str,
        evidence_list: List[Evidence],
        domain: str = "general",
        check_biases: bool = True
    ) -> Reasoning:
        """
        가설을 검증하는 추론 수행
        
        Args:
            hypothesis: 검증할 가설
            evidence_list: 증거 목록
            domain: 도메인 (신뢰도에 영향)
            check_biases: 편향 검토 여부
        
        Returns:
            Reasoning: 추론 결과
        """
        logical_chain = []
        total_confidence = 0.0
        
        # Step 1: 증거 평가
        logical_chain.append(f"Step 1: Evaluating {len(evidence_list)} pieces of evidence")
        evidence_scores = [e.strength() for e in evidence_list]
        average_evidence_strength = sum(evidence_scores) / max(1, len(evidence_scores))
        
        # Step 2: 도메인 신뢰도 적용
        logical_chain.append(f"Step 2: Domain expertise adjustment ({domain}: {self.domain_expertise[domain]})")
        domain_factor = self.domain_expertise.get(domain, 0.65)
        
        # Step 3: 종합 신뢰도 계산
        logical_chain.append("Step 3: Synthesizing confidence score")
        total_confidence = (average_evidence_strength * 0.6) + (domain_factor * 0.4)
        
        # Step 4: 모순 검토
        logical_chain.append("Step 4: Checking for contradictions")
        contradictions = self._check_contradictions(evidence_list)
        if contradictions:
            total_confidence *= 0.85  # 신뢰도 감소
            logical_chain.append(f"   ⚠️ Found {len(contradictions)} contradictions")
        
        # Step 5: 편향 검토
        potential_biases = []
        alternative_explanations = []
        if check_biases:
            logical_chain.append("Step 5: Checking for biases")
            potential_biases = self._identify_biases(hypothesis, evidence_list)
            alternative_explanations = self._generate_alternatives(hypothesis, evidence_list)
        
        # 최종 결과
        reasoning = Reasoning(
            hypothesis=hypothesis,
            confidence=min(0.98, max(0.15, total_confidence)),
            evidence=evidence_list,
            logical_chain=logical_chain,
            potential_biases=potential_biases,
            alternative_explanations=alternative_explanations
        )
        
        self.reasoning_history.append(reasoning)
        return reasoning
    
    def _check_contradictions(self, evidence_list: List[Evidence]) -> List[Tuple[str, str]]:
        """증거 간 모순 찾기"""
        contradictions = []
        for i, e1 in enumerate(evidence_list):
            for e2 in evidence_list[i+1:]:
                # 간단한 모순 검사: 정반대 주장
                if e1.claim.lower() in str(e2.contradicting_evidence).lower():
                    contradictions.append((e1.claim, e2.claim))
        return contradictions
    
    def _identify_biases(self, hypothesis: str, evidence_list: List[Evidence]) -> List[str]:
        """가능한 편향 식별"""
        biases = []
        
        # 선택 편향 검사
        if len(evidence_list) < 3:
            biases.append("selection_bias: Limited evidence sample")
        
        # 확증 편향 검사
        supporting_count = sum(len(e.supporting_evidence) for e in evidence_list)
        contradicting_count = sum(len(e.contradicting_evidence) for e in evidence_list)
        if supporting_count > contradicting_count * 2:
            biases.append("confirmation_bias: Weighted towards supporting evidence")
        
        # 출처 신뢰도 검사
        low_confidence_sources = [e for e in evidence_list if e.source_confidence < 0.5]
        if low_confidence_sources:
            biases.append(f"source_reliability: {len(low_confidence_sources)} low-confidence sources")
        
        return biases
    
    def _generate_alternatives(self, hypothesis: str, evidence_list: List[Evidence]) -> List[str]:
        """대안적 설명 생성"""
        alternatives = []
        
        # 증거로부터 다른 결론 도출 가능성
        if len(evidence_list) > 0:
            alternatives.append("Alternative: Evidence could support multiple interpretations")
            alternatives.append("Alternative: Missing confounding variables not accounted for")
            alternatives.append("Alternative: Temporal relationship unclear")
        
        return alternatives[:3]  # 상위 3개만
    
    def assess_confidence(self, domain: str = "general") -> Dict:
        """도메인별 신뢰도 평가"""
        return {
            "domain": domain,
            "expertise_level": self.domain_expertise.get(domain, 0.0),
            "interpretation": self._interpret_confidence(self.domain_expertise.get(domain, 0.0))
        }
    
    def _interpret_confidence(self, confidence: float) -> str:
        """신뢰도를 인간 언어로 변환"""
        if confidence >= 0.85:
            return "Very confident"
        elif confidence >= 0.70:
            return "Confident"
        elif confidence >= 0.55:
            return "Moderately confident"
        elif confidence >= 0.40:
            return "Low confidence"
        else:
            return "Very low confidence - requires expert review"
    
    def get_reasoning_summary(self, reasoning: Reasoning) -> str:
        """추론 과정 요약"""
        summary = f"""
        🧠 REASONING SUMMARY
        ═══════════════════════════════════════════
        
        Hypothesis: {reasoning.hypothesis}
        Confidence: {reasoning.confidence:.1%}
        
        Evidence Evaluated: {len(reasoning.evidence)}
        
        Reasoning Chain:
        {chr(10).join('  ' + step for step in reasoning.logical_chain)}
        
        Potential Biases:
        {chr(10).join('  - ' + bias for bias in reasoning.potential_biases) if reasoning.potential_biases else '  None identified'}
        
        Alternative Explanations:
        {chr(10).join('  - ' + alt for alt in reasoning.alternative_explanations) if reasoning.alternative_explanations else '  None'}
        
        ═══════════════════════════════════════════
        """
        return summary


# 테스트
if __name__ == "__main__":
    engine = ReasoningEngine()
    
    # 증거 준비
    evidence1 = Evidence(
        claim="Organoids can model organ development",
        supporting_evidence=["Nature paper 2023", "Cell Reports 2022"],
        contradicting_evidence=["Some limitations exist"],
        source_confidence=0.85
    )
    
    evidence2 = Evidence(
        claim="Uterine organoids show endometrial features",
        supporting_evidence=["EMBO 2023", "Dev Cell 2023"],
        source_confidence=0.80
    )
    
    # 추론 수행
    result = engine.reason(
        hypothesis="Organoids can accurately model uterine pathology",
        evidence_list=[evidence1, evidence2],
        domain="biology",
        check_biases=True
    )
    
    print(engine.get_reasoning_summary(result))
