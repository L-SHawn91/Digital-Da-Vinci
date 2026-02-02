"""
AwarenessMonitor - Brainstem의 자각
도메인별 신뢰도, 지식 간격 식별, 불확실성 명시적 표현
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class DomainKnowledge:
    """도메인별 지식 상태"""
    domain: str
    confidence_level: float  # 0.0 ~ 1.0
    known_areas: List[str] = field(default_factory=list)
    knowledge_gaps: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def knowledge_completeness(self) -> float:
        """지식 완성도"""
        total_areas = len(self.known_areas) + len(self.knowledge_gaps)
        if total_areas == 0:
            return 0.0
        return len(self.known_areas) / total_areas


class AwarenessMonitor:
    """
    자각 모니터
    - 도메인별 신뢰도 관리
    - 지식 간격 식별
    - 불확실성 명시적 표현
    - "나는 뭘 모르는가" 항상 인식
    """
    
    def __init__(self):
        """자각 모니터 초기화"""
        self.domain_knowledge: Dict[str, DomainKnowledge] = {
            "biology": DomainKnowledge(
                domain="biology",
                confidence_level=0.80,
                known_areas=[
                    "uterine organoids basic structure",
                    "stemcell differentiation",
                    "organogenesis principles"
                ],
                knowledge_gaps=[
                    "complex disease modeling",
                    "inter-individual variability",
                    "long-term stability"
                ]
            ),
            "finance": DomainKnowledge(
                domain="finance",
                confidence_level=0.60,
                known_areas=[
                    "basic portfolio theory",
                    "market mechanics"
                ],
                knowledge_gaps=[
                    "derivative pricing models",
                    "behavioral finance nuances",
                    "emerging market risks"
                ]
            ),
            "astronomy": DomainKnowledge(
                domain="astronomy",
                confidence_level=0.50,
                known_areas=[
                    "basic stellar classification",
                    "orbital mechanics"
                ],
                knowledge_gaps=[
                    "advanced cosmology",
                    "exoplanet detection methods",
                    "dark matter/dark energy"
                ]
            ),
            "literature": DomainKnowledge(
                domain="literature",
                confidence_level=0.70,
                known_areas=[
                    "major literary movements",
                    "classic texts"
                ],
                knowledge_gaps=[
                    "contemporary avant-garde works",
                    "linguistic poetry analysis",
                    "postcolonial theory nuances"
                ]
            )
        }
        
        self.uncertainty_statements: Dict[str, str] = {
            "very_low": "I have very limited knowledge here. Expert review recommended.",
            "low": "I have some knowledge but significant gaps remain.",
            "moderate": "I have reasonable knowledge but acknowledge limitations.",
            "high": "I have good knowledge in this area, though always open to correction.",
            "very_high": "I have strong knowledge, but remain open to new evidence."
        }
        
        self.awareness_log: List[Dict] = []
    
    def assess_domain(self, domain: str) -> Dict:
        """도메인 평가"""
        if domain not in self.domain_knowledge:
            return {
                "domain": domain,
                "status": "unknown",
                "message": f"I have no prior knowledge of domain: {domain}",
                "recommendation": "This domain would require new learning."
            }
        
        knowledge = self.domain_knowledge[domain]
        return {
            "domain": domain,
            "confidence": knowledge.confidence_level,
            "confidence_level": self._interpret_confidence(knowledge.confidence_level),
            "known_areas": knowledge.known_areas,
            "knowledge_gaps": knowledge.knowledge_gaps,
            "completeness": knowledge.knowledge_completeness(),
            "uncertainty_statement": self._generate_uncertainty_statement(knowledge),
            "last_updated": knowledge.last_updated.isoformat()
        }
    
    def identify_knowledge_gaps(self, domain: str) -> List[str]:
        """지식 간격 식별"""
        if domain not in self.domain_knowledge:
            return ["Unknown domain - no prior knowledge"]
        
        return self.domain_knowledge[domain].knowledge_gaps
    
    def express_uncertainty(self, domain: str, claim: str, confidence: float) -> str:
        """불확실성 명시적 표현"""
        knowledge = self.domain_knowledge.get(domain)
        
        if not knowledge:
            return f"⚠️ DISCLAIMER: I lack domain knowledge in '{domain}'. This claim should be verified by an expert."
        
        # 확신도별 표현
        if confidence < 0.4:
            uncertainty = "I am NOT confident about this claim."
        elif confidence < 0.6:
            uncertainty = "I have MODERATE confidence in this, with significant caveats."
        elif confidence < 0.8:
            uncertainty = "I am fairly confident, but acknowledge potential gaps."
        else:
            uncertainty = "I am confident, though always open to correction."
        
        # 도메인 신뢰도 포함
        disclaimer = f"\n[DOMAIN CONFIDENCE: {knowledge.confidence_level:.0%}] "
        disclaimer += f"In '{domain}', known gaps include: {', '.join(knowledge.knowledge_gaps[:2])}"
        
        return f"{uncertainty}{disclaimer}"
    
    def update_domain_knowledge(
        self,
        domain: str,
        new_known_areas: List[str] = None,
        new_gaps: List[str] = None,
        confidence_adjustment: float = 0.0
    ) -> Dict:
        """도메인 지식 업데이트 (학습)"""
        if domain not in self.domain_knowledge:
            self.domain_knowledge[domain] = DomainKnowledge(
                domain=domain,
                confidence_level=0.5
            )
        
        knowledge = self.domain_knowledge[domain]
        
        if new_known_areas:
            knowledge.known_areas.extend(new_known_areas)
            knowledge.known_areas = list(set(knowledge.known_areas))  # 중복 제거
        
        if new_gaps:
            knowledge.knowledge_gaps.extend(new_gaps)
            knowledge.knowledge_gaps = list(set(knowledge.knowledge_gaps))
        
        # 신뢰도 조정
        new_confidence = max(0.0, min(1.0, knowledge.confidence_level + confidence_adjustment))
        knowledge.confidence_level = new_confidence
        knowledge.last_updated = datetime.now()
        
        # 로그
        self.awareness_log.append({
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "action": "knowledge_update",
            "new_confidence": new_confidence,
            "areas_added": new_known_areas or [],
            "gaps_identified": new_gaps or []
        })
        
        return self.assess_domain(domain)
    
    def _interpret_confidence(self, confidence: float) -> str:
        """신뢰도 레벨 해석"""
        if confidence >= 0.85:
            return "Very High"
        elif confidence >= 0.70:
            return "High"
        elif confidence >= 0.55:
            return "Moderate"
        elif confidence >= 0.40:
            return "Low"
        else:
            return "Very Low"
    
    def _generate_uncertainty_statement(self, knowledge: DomainKnowledge) -> str:
        """불확실성 표현 생성"""
        confidence_level = knowledge.confidence_level
        
        if confidence_level >= 0.85:
            return self.uncertainty_statements["very_high"]
        elif confidence_level >= 0.70:
            return self.uncertainty_statements["high"]
        elif confidence_level >= 0.55:
            return self.uncertainty_statements["moderate"]
        elif confidence_level >= 0.40:
            return self.uncertainty_statements["low"]
        else:
            return self.uncertainty_statements["very_low"]
    
    def self_awareness_report(self) -> str:
        """전체 자각 보고서"""
        report = """
        🧠 SELF-AWARENESS REPORT
        ════════════════════════════════════════════
        
        MY KNOWLEDGE LANDSCAPE:
        """
        
        for domain, knowledge in self.domain_knowledge.items():
            report += f"\n\n  {domain.upper()}: {knowledge.confidence_level:.0%} confidence"
            report += f"\n    ✅ Known: {', '.join(knowledge.known_areas[:2])}"
            report += f"\n    ❌ Unknown: {', '.join(knowledge.knowledge_gaps[:2])}"
        
        report += """
        
        KEY PRINCIPLE:
        I am more useful when I explicitly acknowledge what I don't know.
        Every claim comes with: confidence level, domain expertise, and known gaps.
        
        WHAT I KNOW ABOUT WHAT I DON'T KNOW:
        - I lack expertise in emerging fields
        - I may miss recent developments
        - I can be fooled by plausible misinformation
        - I have blind spots I'm not aware of
        
        ════════════════════════════════════════════
        """
        
        return report
    
    def get_awareness_log(self) -> List[Dict]:
        """자각 로그 반환"""
        return self.awareness_log[-10:]  # 최근 10개


# 테스트
if __name__ == "__main__":
    monitor = AwarenessMonitor()
    
    # 도메인 평가
    print(json.dumps(monitor.assess_domain("biology"), indent=2, default=str))
    print("\n")
    
    # 지식 간격
    print("📚 Biology Knowledge Gaps:")
    for gap in monitor.identify_knowledge_gaps("biology"):
        print(f"  - {gap}")
    print("\n")
    
    # 불확실성 표현
    print("⚠️ Uncertainty Statement:")
    print(monitor.express_uncertainty("biology", "Organoids can model disease", 0.75))
    print("\n")
    
    # 전체 보고서
    print(monitor.self_awareness_report())
