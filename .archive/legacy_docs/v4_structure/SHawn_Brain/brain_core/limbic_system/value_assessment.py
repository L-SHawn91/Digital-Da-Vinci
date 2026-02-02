"""
ValueAssessment - Limbic System의 가치 평가
도메인별 가치 체계, 의사결정 영향도, 가치-행동 매핑
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ValueCategory(Enum):
    """가치 범주"""
    ETHICS = "ethics"           # 윤리 (truthfulness, integrity)
    ACHIEVEMENT = "achievement" # 성취 (success, progress)
    KNOWLEDGE = "knowledge"     # 지식 (understanding, learning)
    AUTONOMY = "autonomy"       # 자율 (freedom, agency)
    SOCIAL = "social"           # 사회 (cooperation, belonging)
    HEALTH = "health"           # 건강 (wellbeing, safety)
    CREATIVITY = "creativity"   # 창의 (innovation, expression)


@dataclass
class Value:
    """개별 가치"""
    name: str
    category: ValueCategory
    importance: float  # 중요도 (0~1)
    alignment_score: float = 1.0  # 정렬도 (행동과의 일치도)
    description: str = ""


@dataclass
class ValueInfluence:
    """가치가 의사결정에 미치는 영향"""
    value_name: str
    influence_strength: float  # -1 (반대) ~ 1 (찬성)
    reason: str = ""


class ValueAssessment:
    """
    가치 평가 시스템
    - 도메인별 가치 체계
    - 의사결정에 미치는 영향도
    - 가치-행동 매핑
    - 가치 충돌 식별
    """
    
    def __init__(self):
        """가치 평가 초기화"""
        self.domain_values: Dict[str, List[Value]] = {}
        self.value_hierarchy: Dict[str, float] = {}  # 가치 우선순위
        self.decision_history: List[Dict] = []
        self.value_conflicts: List[Dict] = []
        
        # 도메인별 기본 가치 설정
        self._initialize_domain_values()
    
    def _initialize_domain_values(self):
        """도메인별 기본 가치 초기화"""
        
        # Biology 도메인
        self.domain_values["biology"] = [
            Value(
                name="scientific_integrity",
                category=ValueCategory.ETHICS,
                importance=0.95,
                description="Truthfulness in research, accurate reporting"
            ),
            Value(
                name="human_benefit",
                category=ValueCategory.ETHICS,
                importance=0.9,
                description="Research benefits human health"
            ),
            Value(
                name="breakthrough_achievement",
                category=ValueCategory.ACHIEVEMENT,
                importance=0.85,
                description="Novel discoveries and innovations"
            ),
            Value(
                name="rigorous_methodology",
                category=ValueCategory.KNOWLEDGE,
                importance=0.9,
                description="Careful, reproducible experiments"
            ),
        ]
        
        # Finance 도메인
        self.domain_values["finance"] = [
            Value(
                name="financial_integrity",
                category=ValueCategory.ETHICS,
                importance=0.95,
                description="Honest dealing, no fraud"
            ),
            Value(
                name="wealth_creation",
                category=ValueCategory.ACHIEVEMENT,
                importance=0.85,
                description="Profitable investments"
            ),
            Value(
                name="risk_management",
                category=ValueCategory.HEALTH,
                importance=0.8,
                description="Protect capital and minimize losses"
            ),
            Value(
                name="informed_decisions",
                category=ValueCategory.KNOWLEDGE,
                importance=0.85,
                description="Data-driven analysis"
            ),
        ]
        
        # Literature 도메인
        self.domain_values["literature"] = [
            Value(
                name="artistic_expression",
                category=ValueCategory.CREATIVITY,
                importance=0.9,
                description="Authentic voice and vision"
            ),
            Value(
                name="truth_telling",
                category=ValueCategory.ETHICS,
                importance=0.85,
                description="Honesty about human experience"
            ),
            Value(
                name="cultural_impact",
                category=ValueCategory.SOCIAL,
                importance=0.8,
                description="Meaningful contribution to culture"
            ),
            Value(
                name="creative_autonomy",
                category=ValueCategory.AUTONOMY,
                importance=0.85,
                description="Freedom to create without constraint"
            ),
        ]
        
        # General 도메인
        self.domain_values["general"] = [
            Value(
                name="integrity",
                category=ValueCategory.ETHICS,
                importance=0.95,
                description="Honesty and moral principles"
            ),
            Value(
                name="learning",
                category=ValueCategory.KNOWLEDGE,
                importance=0.8,
                description="Growth and understanding"
            ),
            Value(
                name="autonomy",
                category=ValueCategory.AUTONOMY,
                importance=0.75,
                description="Self-direction and agency"
            ),
            Value(
                name="wellbeing",
                category=ValueCategory.HEALTH,
                importance=0.85,
                description="Safety and flourishing"
            ),
        ]
        
        # 가치 우선순위 계산
        self._calculate_value_hierarchy()
    
    def _calculate_value_hierarchy(self):
        """전체 가치 우선순위 계산"""
        all_values = {}
        for domain_values in self.domain_values.values():
            for value in domain_values:
                if value.name not in all_values:
                    all_values[value.name] = []
                all_values[value.name].append(value.importance)
        
        # 도메인 전체에서 평균 중요도
        for value_name, importances in all_values.items():
            self.value_hierarchy[value_name] = sum(importances) / len(importances)
    
    def assess_decision(
        self,
        domain: str,
        decision: str,
        action_description: str
    ) -> Dict:
        """
        의사결정 평가
        이 결정이 도메인의 가치와 얼마나 일치하는가?
        
        Args:
            domain: 도메인
            decision: 의사결정
            action_description: 행동 설명
        
        Returns:
            가치 영향도 분석
        """
        if domain not in self.domain_values:
            return {"error": f"Unknown domain: {domain}"}
        
        values = self.domain_values[domain]
        influences: List[ValueInfluence] = []
        value_conflicts = []
        
        # 각 가치와의 정렬도 평가
        for value in values:
            influence = self._evaluate_value_alignment(
                value, decision, action_description
            )
            influences.append(influence)
            
            # 음수 영향 (가치 충돌) 감지
            if influence.influence_strength < -0.5:
                value_conflicts.append({
                    'value': value.name,
                    'conflict_level': abs(influence.influence_strength),
                    'reason': influence.reason
                })
        
        # 종합 점수
        total_influence = sum(v.influence_strength * v_obj.importance 
                            for v, v_obj in zip(influences, values))
        max_possible = sum(v_obj.importance for v_obj in values)
        alignment_score = total_influence / max_possible if max_possible > 0 else 0.0
        
        assessment = {
            'decision': decision,
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'value_influences': [
                {
                    'value': v.value_name,
                    'influence': v.influence_strength,
                    'reason': v.reason
                }
                for v in influences
            ],
            'overall_alignment': alignment_score,
            'alignment_interpretation': self._interpret_alignment(alignment_score),
            'value_conflicts': value_conflicts,
            'recommendation': self._generate_recommendation(alignment_score, value_conflicts)
        }
        
        # 히스토리 저장
        self.decision_history.append(assessment)
        if value_conflicts:
            self.value_conflicts.extend(value_conflicts)
        
        return assessment
    
    def _evaluate_value_alignment(
        self,
        value: Value,
        decision: str,
        action_description: str
    ) -> ValueInfluence:
        """
        가치와 결정의 정렬도 평가
        간단한 키워드 기반 휴리스틱
        """
        decision_lower = (decision + " " + action_description).lower()
        
        # 긍정 키워드
        positive_keywords = {
            "scientific_integrity": ["truth", "accurate", "rigorous", "honest", "verify"],
            "human_benefit": ["help", "improve", "benefit", "healthy", "safe"],
            "breakthrough_achievement": ["novel", "innovation", "discover", "first", "breakthrough"],
            "rigorous_methodology": ["test", "experiment", "validate", "control", "replicate"],
            "financial_integrity": ["transparent", "honest", "compliant", "ethical", "fair"],
            "wealth_creation": ["profit", "return", "gain", "growth", "success"],
            "artistic_expression": ["creative", "original", "authentic", "unique", "express"],
            "truth_telling": ["honest", "true", "authentic", "real", "genuine"],
        }
        
        # 부정 키워드
        negative_keywords = {
            "scientific_integrity": ["falsify", "manipulate", "bias", "hide", "lie"],
            "human_benefit": ["harm", "damage", "risk", "danger", "hurt"],
            "breakthrough_achievement": ["derivative", "copy", "incremental", "trivial"],
            "rigorous_methodology": ["rush", "skip", "shortcut", "untested", "guess"],
            "financial_integrity": ["fraud", "deception", "insider", "manipulation", "illegal"],
            "wealth_creation": ["loss", "fail", "bankrupt", "collapse"],
            "artistic_expression": ["constrain", "censor", "limit", "restrict", "control"],
            "truth_telling": ["lie", "deceive", "fake", "false", "pretend"],
        }
        
        influence = 0.0
        reason_parts = []
        
        value_name = value.name
        
        # 긍정 키워드 확인
        if value_name in positive_keywords:
            positive_count = sum(
                1 for kw in positive_keywords[value_name]
                if kw in decision_lower
            )
            influence += positive_count * 0.3
            if positive_count > 0:
                reason_parts.append(f"Aligns with {value_name}")
        
        # 부정 키워드 확인
        if value_name in negative_keywords:
            negative_count = sum(
                1 for kw in negative_keywords[value_name]
                if kw in decision_lower
            )
            influence -= negative_count * 0.4
            if negative_count > 0:
                reason_parts.append(f"Conflicts with {value_name}")
        
        # 범위 제한
        influence = max(-1.0, min(1.0, influence))
        
        return ValueInfluence(
            value_name=value_name,
            influence_strength=influence,
            reason=" | ".join(reason_parts) if reason_parts else "No clear alignment"
        )
    
    def _interpret_alignment(self, score: float) -> str:
        """정렬도 해석"""
        if score > 0.7:
            return "Highly aligned with domain values"
        elif score > 0.4:
            return "Moderately aligned with domain values"
        elif score > 0.0:
            return "Slightly aligned with domain values"
        elif score > -0.3:
            return "Some value conflicts"
        else:
            return "Significant value conflicts"
    
    def _generate_recommendation(self, alignment: float, conflicts: List[Dict]) -> str:
        """권장사항 생성"""
        if alignment > 0.7:
            return "✅ Decision aligns well with domain values. Proceed with confidence."
        elif alignment > 0.3:
            return "⚠️ Decision has mixed alignment. Consider addressing identified conflicts."
        elif conflicts:
            reasons = [c['value'] for c in conflicts[:2]]
            return f"❌ Decision conflicts with core values: {', '.join(reasons)}"
        else:
            return "❓ Unable to determine value alignment clearly."
    
    def get_value_profile(self, domain: str = "general") -> Dict:
        """도메인의 가치 프로필"""
        if domain not in self.domain_values:
            return {"error": f"Unknown domain: {domain}"}
        
        values = self.domain_values[domain]
        return {
            'domain': domain,
            'values': [
                {
                    'name': v.name,
                    'category': v.category.value,
                    'importance': v.importance,
                    'description': v.description
                }
                for v in values
            ],
            'primary_value': max(values, key=lambda v: v.importance).name if values else None
        }
    
    def get_decision_consistency(self) -> Dict:
        """의사결정 일관성 분석"""
        if not self.decision_history:
            return {'decisions_analyzed': 0}
        
        alignments = [d['overall_alignment'] for d in self.decision_history]
        avg_alignment = sum(alignments) / len(alignments) if alignments else 0.0
        
        return {
            'total_decisions': len(self.decision_history),
            'average_alignment': avg_alignment,
            'consistency': self._interpret_alignment(avg_alignment),
            'total_conflicts': len(self.value_conflicts)
        }


# 테스트
if __name__ == "__main__":
    assessor = ValueAssessment()
    
    print("🧪 ValueAssessment Test\n")
    
    # 1. Biology 가치 프로필
    print("1️⃣ Biology Value Profile:")
    profile = assessor.get_value_profile("biology")
    for value in profile['values'][:3]:
        print(f"  • {value['name']}: {value['importance']:.0%}")
    
    # 2. 의사결정 평가 (좋은 결정)
    print("\n2️⃣ Assessing: Publish rigorous, verified organoid research")
    good_decision = assessor.assess_decision(
        domain="biology",
        decision="Publish findings",
        action_description="Conduct rigorous experiments, verify all results, transparent methods"
    )
    print(f"  Overall Alignment: {good_decision['overall_alignment']:.2f}")
    print(f"  Interpretation: {good_decision['alignment_interpretation']}")
    print(f"  Recommendation: {good_decision['recommendation']}")
    
    # 3. 의사결정 평가 (나쁜 결정)
    print("\n3️⃣ Assessing: Falsify data to show positive results")
    bad_decision = assessor.assess_decision(
        domain="biology",
        decision="Manipulate data",
        action_description="Falsify results to show success, hide negative outcomes"
    )
    print(f"  Overall Alignment: {bad_decision['overall_alignment']:.2f}")
    print(f"  Conflicts: {len(bad_decision['value_conflicts'])} identified")
    print(f"  Recommendation: {bad_decision['recommendation']}")
    
    # 4. 일관성 분석
    print("\n4️⃣ Decision Consistency:")
    consistency = assessor.get_decision_consistency()
    print(f"  Decisions analyzed: {consistency['total_decisions']}")
    print(f"  Average alignment: {consistency['average_alignment']:.2f}")
    
    print("\n✅ ValueAssessment working!")
