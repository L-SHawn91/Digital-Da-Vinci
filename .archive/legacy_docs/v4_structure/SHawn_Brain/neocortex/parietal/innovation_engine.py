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
        """도메인 간 개념 교배"""
        
        # 유사성 계산 (간단한 휴리스틱)
        similarity = self._calculate_conceptual_similarity(
            concept1, domain1, concept2, domain2
        )
        
        # 새 아이디어 생성
        idea_name = f"{concept1}_{concept2}_hybrid"
        
        # 신규도 계산
        novelty = similarity * 0.5 + 0.4  # 0.4 ~ 0.9
        
        idea = Idea(
            name=idea_name,
            source_domains=[domain1, domain2],
            components=[concept1, concept2],
            novelty_score=novelty,
            feasibility_score=0.6,
            impact_score=0.7,
            rationale=f"Combining {concept1} from {domain1} with {concept2} from {domain2}"
        )
        
        self.ideas.append(idea)
        
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'concept1': concept1,
            'domain1': domain1,
            'concept2': concept2,
            'domain2': domain2,
            'resulting_idea': idea_name,
            'similarity': similarity
        }
        self.synthesis_history.append(synthesis)
        
        return idea
    
    def _calculate_conceptual_similarity(
        self,
        concept1: str,
        domain1: str,
        concept2: str,
        domain2: str
    ) -> float:
        """개념적 유사성 계산"""
        # 단순 구현: 이름 유사성 + 도메인 거리
        name_similarity = 0.3  # 기본값
        domain_distance = 0.0 if domain1 == domain2 else 0.5
        
        return min(1.0, (name_similarity + (1.0 - domain_distance)) / 2.0)
    
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
