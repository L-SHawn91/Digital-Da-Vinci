"""
InnovationEngine - Parietal Cortex의 혁신 엔진
도메인 간 개념 교배, 새로운 아이디어 생성, 창의적 문제 해결
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class Idea:
    """아이디어"""
    name: str
    source_domains: List[str]
    components: List[str]
    novelty_score: float  # 0 ~ 1 (새로움)
    feasibility_score: float  # 0 ~ 1 (실행 가능성)
    impact_score: float  # 0 ~ 1 (영향도)
    timestamp: datetime = field(default_factory=datetime.now)
    rationale: str = ""


@dataclass
class ConceptPair:
    """개념 쌍 (교배용)"""
    concept1: str
    domain1: str
    concept2: str
    domain2: str
    similarity: float  # 0 ~ 1


class InnovationEngine:
    """
    혁신 엔진
    - 도메인 간 개념 교배 (Cross-Domain Synthesis)
    - 새로운 아이디어 생성
    - 창의적 문제 해결
    - 메타인지
    """
    
    def __init__(self):
        """혁신 엔진 초기화"""
        self.concept_library: Dict[str, List[str]] = {
            "biology": [
                "adaptation", "evolution", "symbiosis", "mutation",
                "regeneration", "self-organization", "emergence"
            ],
            "finance": [
                "portfolio", "diversification", "hedging", "arbitrage",
                "valuation", "risk management", "optimization"
            ],
            "technology": [
                "scalability", "modularity", "distribution", "encryption",
                "automation", "integration", "optimization"
            ],
            "literature": [
                "narrative", "metaphor", "symbolism", "perspective",
                "tension", "resolution", "meaning-making"
            ]
        }
        
        self.ideas: List[Idea] = []
        self.synthesis_history: List[Dict] = []
        self.problem_solutions: Dict[str, List[str]] = defaultdict(list)
    
    def cross_domain_synthesis(
        self,
        concept1: str,
        domain1: str,
        concept2: str,
        domain2: str
    ) -> Idea:
        """도메인 간 개념 교배 (고도화 v2.0)"""

        # 유사성 계산 (고도화)
        similarity = self._calculate_conceptual_similarity(
            concept1, domain1, concept2, domain2
        )

        # 새 아이디어 생성
        idea_name = f"{concept1}_{concept2}_hybrid"

        # 신규도 계산 (고도화)
        # 다른 도메인일수록, 유사성이 중간 정도일 때 높은 신규도
        domain_distance = 1.0 if domain1 != domain2 else 0.5
        novelty = self._calculate_novelty(similarity, domain_distance)

        # 실행 가능성 계산 (고도화)
        # 유사성이 너무 높거나 낮으면 실행 가능성 감소
        feasibility = self._calculate_feasibility(similarity, domain1, domain2)

        # 영향도 계산 (고도화)
        # 도메인 거리와 신규도가 높을수록 영향도 증가
        impact = self._calculate_impact(novelty, domain_distance)

        idea = Idea(
            name=idea_name,
            source_domains=[domain1, domain2],
            components=[concept1, concept2],
            novelty_score=novelty,
            feasibility_score=feasibility,
            impact_score=impact,
            rationale=f"Synthesizing {concept1} ({domain1}) + {concept2} ({domain2}): "
                     f"Similarity={similarity:.2f}, Novelty={novelty:.2f}, "
                     f"Feasibility={feasibility:.2f}, Impact={impact:.2f}"
        )

        self.ideas.append(idea)

        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'concept1': concept1,
            'domain1': domain1,
            'concept2': concept2,
            'domain2': domain2,
            'resulting_idea': idea_name,
            'similarity': similarity,
            'novelty': novelty,
            'feasibility': feasibility,
            'impact': impact
        }
        self.synthesis_history.append(synthesis)

        return idea

    def _calculate_novelty(self, similarity: float, domain_distance: float) -> float:
        """신규도 계산"""
        # 유사성이 중간 정도(0.3~0.7)이고 도메인이 다를 때 신규도 높음
        optimal_similarity = 0.5
        similarity_novelty = 1.0 - abs(similarity - optimal_similarity) * 2.0

        # 도메인이 다를수록 신규도 높음
        domain_novelty = domain_distance

        # 종합
        novelty = similarity_novelty * 0.6 + domain_novelty * 0.4
        return max(0.3, min(1.0, novelty))

    def _calculate_feasibility(self, similarity: float, domain1: str, domain2: str) -> float:
        """실행 가능성 계산"""
        # 유사성이 너무 높으면(복잡함 없음) 또는 너무 낮으면(이질적) 실행 가능성 낮음
        similarity_feasibility = 1.0 - (similarity - 0.5) ** 2 * 2.0

        # 같은 도메인이면 실행 가능성 높음
        domain_feasibility = 0.8 if domain1 == domain2 else 0.6

        # 종합
        feasibility = similarity_feasibility * 0.5 + domain_feasibility * 0.5
        return max(0.3, min(1.0, feasibility))

    def _calculate_impact(self, novelty: float, domain_distance: float) -> float:
        """영향도 계산"""
        # 신규도와 도메인 거리가 높을수록 영향도 높음
        impact = novelty * 0.5 + domain_distance * 0.5

        # 기본값 상향
        return max(0.4, min(1.0, impact + 0.1))
    
    def _calculate_conceptual_similarity(
        self,
        concept1: str,
        domain1: str,
        concept2: str,
        domain2: str
    ) -> float:
        """개념적 유사성 계산 (고도화 v2.0)"""
        # 1. 문자열 레벤슈타인 거리 기반 유사성
        name_similarity = self._string_similarity(concept1, concept2)

        # 2. 도메인 거리
        domain_similarity = 1.0 if domain1 == domain2 else 0.5

        # 3. 의미론적 특성 유사성
        semantic_similarity = self._semantic_similarity(
            concept1, domain1, concept2, domain2
        )

        # 4. 교배 잠재성 (크로스 도메인 개념은 더 높은 점수)
        breeding_potential = 0.3 if domain1 != domain2 else 0.15

        # 종합 점수 (가중 평균)
        total_similarity = (
            name_similarity * 0.2 +      # 이름 유사성 20%
            domain_similarity * 0.2 +     # 도메인 유사성 20%
            semantic_similarity * 0.4 +   # 의미론적 유사성 40%
            breeding_potential * 0.2      # 교배 잠재성 20%
        )

        return min(1.0, max(0.0, total_similarity))

    def _string_similarity(self, s1: str, s2: str) -> float:
        """편집거리(Levenshtein) 기반 문자열 유사성"""
        s1_lower = s1.lower()
        s2_lower = s2.lower()

        if s1_lower == s2_lower:
            return 1.0

        # 최대 길이
        max_len = max(len(s1_lower), len(s2_lower))
        if max_len == 0:
            return 0.0

        # 간단한 Levenshtein 거리 계산
        distance = self._levenshtein_distance(s1_lower, s2_lower)
        similarity = 1.0 - (distance / max_len)

        return max(0.0, min(1.0, similarity))

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """편집거리(Levenshtein distance) 계산"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        # 동적 계획법
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _semantic_similarity(
        self,
        concept1: str,
        domain1: str,
        concept2: str,
        domain2: str
    ) -> float:
        """의미론적 유사성 계산"""
        # 개념의 특성(features) 매핑
        concept_features = {
            "adaptation": ["change", "environment", "dynamic", "responsive"],
            "evolution": ["change", "improvement", "gradual", "natural"],
            "symbiosis": ["cooperation", "mutual", "benefit", "integration"],
            "mutation": ["change", "random", "variation", "difference"],
            "regeneration": ["recovery", "restoration", "renewal", "growth"],
            "self-organization": ["autonomous", "order", "emergence", "complex"],
            "emergence": ["new", "property", "system", "complex"],
            "portfolio": ["collection", "diversity", "balance", "risk"],
            "diversification": ["variety", "spread", "balance", "risk"],
            "hedging": ["protection", "risk", "offset", "insurance"],
            "arbitrage": ["profit", "difference", "opportunity", "pricing"],
            "valuation": ["assessment", "worth", "value", "analysis"],
            "risk management": ["control", "mitigation", "planning", "safety"],
            "optimization": ["improvement", "efficiency", "best", "maximal"],
            "scalability": ["growth", "size", "capability", "expansion"],
            "modularity": ["component", "structure", "reuse", "flexibility"],
            "distribution": ["spread", "disperse", "allocation", "sharing"],
            "encryption": ["security", "protection", "hidden", "code"],
            "automation": ["self-operating", "efficiency", "reduction", "process"],
            "integration": ["combination", "unity", "connection", "synthesis"],
            "narrative": ["story", "sequence", "meaning", "communication"],
            "metaphor": ["analogy", "comparison", "symbolic", "meaning"],
            "symbolism": ["representation", "meaning", "abstract", "cultural"],
            "perspective": ["viewpoint", "angle", "frame", "understanding"],
            "tension": ["conflict", "opposition", "force", "dynamic"],
            "resolution": ["solution", "ending", "harmony", "closure"],
            "meaning-making": ["interpretation", "understanding", "sense", "cognitive"],
        }

        # 특성 추출
        features1 = concept_features.get(concept1.lower(), [])
        features2 = concept_features.get(concept2.lower(), [])

        if not features1 or not features2:
            return 0.3  # 기본값

        # 교집합/합집합 (Jaccard 유사도)
        intersection = len(set(features1) & set(features2))
        union = len(set(features1) | set(features2))

        jaccard = intersection / union if union > 0 else 0.0

        return min(1.0, jaccard)
    
    def generate_ideas(
        self,
        num_ideas: int = 5,
        domains: List[str] = None
    ) -> List[Idea]:
        """여러 아이디어 생성"""
        if not domains:
            domains = list(self.concept_library.keys())
        
        generated_ideas = []
        
        # 도메인 간 랜덤 조합
        for i in range(num_ideas):
            if len(domains) >= 2:
                d1, d2 = domains[i % len(domains)], domains[(i + 1) % len(domains)]
                
                concepts1 = self.concept_library.get(d1, [])
                concepts2 = self.concept_library.get(d2, [])
                
                if concepts1 and concepts2:
                    c1 = concepts1[i % len(concepts1)]
                    c2 = concepts2[i % len(concepts2)]
                    
                    idea = self.cross_domain_synthesis(c1, d1, c2, d2)
                    generated_ideas.append(idea)
        
        return generated_ideas
    
    def solve_problem_creatively(
        self,
        problem: str,
        target_domain: str
    ) -> List[str]:
        """창의적 문제 해결"""
        solutions = []
        
        # 현재 도메인의 개념 사용
        current_concepts = self.concept_library.get(target_domain, [])
        
        # 다른 도메인의 개념으로 새로운 해결책 제시
        for other_domain in self.concept_library.keys():
            if other_domain != target_domain:
                other_concepts = self.concept_library[other_domain]
                
                # 교배하여 해결책 생성
                for concept in other_concepts[:2]:  # 상위 2개만
                    solution = f"Apply {concept} concept from {other_domain} to solve: {problem}"
                    solutions.append(solution)
        
        self.problem_solutions[problem] = solutions
        return solutions[:3]  # 상위 3개 반환
    
    def evaluate_idea(self, idea: Idea) -> Dict:
        """아이디어 평가"""
        # 종합 점수
        overall_score = (
            idea.novelty_score * 0.3 +
            idea.feasibility_score * 0.4 +
            idea.impact_score * 0.3
        )
        
        viability = "viable" if overall_score > 0.6 else "interesting" if overall_score > 0.4 else "exploratory"
        
        return {
            'idea': idea.name,
            'novelty': idea.novelty_score,
            'feasibility': idea.feasibility_score,
            'impact': idea.impact_score,
            'overall_score': overall_score,
            'viability': viability,
            'domains': idea.source_domains
        }
    
    def get_innovation_metrics(self) -> Dict:
        """혁신 메트릭"""
        if not self.ideas:
            return {'total_ideas': 0}
        
        avg_novelty = sum(i.novelty_score for i in self.ideas) / len(self.ideas)
        avg_feasibility = sum(i.feasibility_score for i in self.ideas) / len(self.ideas)
        avg_impact = sum(i.impact_score for i in self.ideas) / len(self.ideas)
        
        return {
            'total_ideas_generated': len(self.ideas),
            'avg_novelty': avg_novelty,
            'avg_feasibility': avg_feasibility,
            'avg_impact': avg_impact,
            'synthesis_events': len(self.synthesis_history)
        }


# 테스트
if __name__ == "__main__":
    engine = InnovationEngine()
    
    print("🧪 InnovationEngine Test\n")
    
    # 1. 도메인 간 개념 교배
    print("1️⃣ Cross-Domain Synthesis:")
    idea1 = engine.cross_domain_synthesis(
        concept1="regeneration",
        domain1="biology",
        concept2="portfolio",
        domain2="finance"
    )
    print(f"  Idea: {idea1.name}")
    print(f"  Novelty: {idea1.novelty_score:.2f}")
    print(f"  Rationale: {idea1.rationale}")
    
    # 2. 여러 아이디어 생성
    print("\n2️⃣ Generating multiple ideas:")
    ideas = engine.generate_ideas(num_ideas=3)
    print(f"  Generated: {len(ideas)} ideas")
    for idea in ideas:
        print(f"    • {idea.name}")
    
    # 3. 창의적 문제 해결
    print("\n3️⃣ Creative problem solving:")
    problem = "How to scale organoid production?"
    solutions = engine.solve_problem_creatively(problem, "biology")
    for solution in solutions:
        print(f"    • {solution}")
    
    # 4. 아이디어 평가
    print("\n4️⃣ Idea evaluation:")
    evaluation = engine.evaluate_idea(idea1)
    print(f"  Overall score: {evaluation['overall_score']:.2f}")
    print(f"  Viability: {evaluation['viability']}")
    
    # 5. 메트릭
    print("\n5️⃣ Innovation metrics:")
    metrics = engine.get_innovation_metrics()
    print(f"  Total ideas: {metrics['total_ideas_generated']}")
    print(f"  Avg novelty: {metrics['avg_novelty']:.2f}")
    
    print("\n✅ InnovationEngine working!")
