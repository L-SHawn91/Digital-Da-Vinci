"""
DecisionFramework - Prefrontal Cortex의 의사결정 엔진
목표-수단 계층 구조, 의사결정 로직, 우선순위 결정
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DecisionStrategy(Enum):
    """의사결정 전략"""
    RATIONAL = "rational"              # 합리적 선택
    SATISFICING = "satisficing"        # 만족스러운 선택
    INTUITIVE = "intuitive"            # 직관적 선택
    RISK_AVERSE = "risk_averse"       # 위험 회피
    RISK_SEEKING = "risk_seeking"      # 위험 추구


@dataclass
class Goal:
    """목표"""
    name: str
    category: str
    priority: float  # 0 ~ 1
    deadline: Optional[str] = None
    metrics: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, active, completed, failed


@dataclass
class Alternative:
    """선택지"""
    name: str
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    expected_value: float = 0.0
    risk_level: float = 0.5
    timeline: str = "medium-term"


@dataclass
class Decision:
    """의사결정"""
    goal: str
    alternatives: List[Alternative]
    chosen_alternative: Optional[str] = None
    confidence: float = 0.0
    strategy_used: DecisionStrategy = DecisionStrategy.RATIONAL
    timestamp: datetime = field(default_factory=datetime.now)
    rationale: str = ""


class DecisionFramework:
    """
    의사결정 프레임워크
    - 목표-수단 계층 구조
    - 의사결정 로직
    - 우선순위 결정
    - 불확실성 처리
    """
    
    def __init__(self, strategy: DecisionStrategy = DecisionStrategy.RATIONAL):
        """의사결정 프레임워크 초기화"""
        self.strategy = strategy
        self.goals: List[Goal] = []
        self.decisions: List[Decision] = []
        self.constraints: Set[str] = set()
    
    def add_goal(
        self,
        name: str,
        category: str,
        priority: float,
        deadline: Optional[str] = None
    ) -> Goal:
        """목표 추가"""
        goal = Goal(
            name=name,
            category=category,
            priority=min(1.0, max(0.0, priority)),
            deadline=deadline
        )
        self.goals.append(goal)
        return goal
    
    def add_constraint(self, constraint: str):
        """제약 조건 추가"""
        self.constraints.add(constraint)
    
    def evaluate_alternative(
        self,
        alternative: Alternative,
        goal: Goal
    ) -> float:
        """선택지 평가"""
        # 간단한 평가: pros - cons의 가중치
        pro_score = len(alternative.pros) * 0.3
        con_score = len(alternative.cons) * 0.2
        
        # 위험도 조정
        if self.strategy == DecisionStrategy.RISK_AVERSE:
            con_score *= 1.5  # 위험에 더 무게
        elif self.strategy == DecisionStrategy.RISK_SEEKING:
            pro_score *= 1.5  # 기회에 더 무게
        
        score = (pro_score - con_score) * goal.priority
        alternative.expected_value = max(0.0, min(1.0, score))
        return alternative.expected_value
    
    def make_decision(
        self,
        goal_name: str,
        alternatives: List[Alternative]
    ) -> Decision:
        """의사결정 수행"""
        # 해당 목표 찾기
        goal = next((g for g in self.goals if g.name == goal_name), None)
        if not goal:
            return Decision(goal=goal_name, alternatives=alternatives)
        
        # 각 선택지 평가
        for alt in alternatives:
            self.evaluate_alternative(alt, goal)
        
        # 최선의 선택지 선택
        if alternatives:
            best_alternative = max(
                alternatives,
                key=lambda a: a.expected_value
            )
            
            # 신뢰도 계산
            if len(alternatives) > 1:
                second_best = sorted(
                    alternatives,
                    key=lambda a: a.expected_value
                )[-2]
                confidence = 1.0 - (second_best.expected_value / (best_alternative.expected_value + 0.001))
            else:
                confidence = 0.7
            
            decision = Decision(
                goal=goal_name,
                alternatives=alternatives,
                chosen_alternative=best_alternative.name,
                confidence=min(0.95, max(0.1, confidence)),
                strategy_used=self.strategy,
                rationale=f"Selected based on {self.strategy.value} strategy with {len(best_alternative.pros)} pros"
            )
        else:
            decision = Decision(goal=goal_name, alternatives=alternatives)
        
        self.decisions.append(decision)
        return decision
    
    def prioritize_goals(self) -> List[Goal]:
        """목표 우선순위 정렬"""
        return sorted(self.goals, key=lambda g: g.priority, reverse=True)
    
    def handle_uncertainty(
        self,
        best_case: float,
        worst_case: float,
        probability: float = 0.5
    ) -> float:
        """불확실성 처리"""
        # 기댓값 = 최악 + (최선-최악) * 확률
        expected_value = worst_case + (best_case - worst_case) * probability
        return max(0.0, min(1.0, expected_value))
    
    def get_decision_report(self) -> Dict:
        """의사결정 보고서"""
        if not self.decisions:
            return {'decisions': 0, 'status': 'no_decisions_made'}
        
        successful = len([d for d in self.decisions if d.chosen_alternative])
        avg_confidence = sum(d.confidence for d in self.decisions) / len(self.decisions)
        
        return {
            'total_decisions': len(self.decisions),
            'successful_decisions': successful,
            'average_confidence': avg_confidence,
            'strategy_used': self.strategy.value,
            'recent_decision': {
                'goal': self.decisions[-1].goal,
                'choice': self.decisions[-1].chosen_alternative,
                'confidence': self.decisions[-1].confidence
            }
        }


# 테스트
if __name__ == "__main__":
    framework = DecisionFramework(strategy=DecisionStrategy.RATIONAL)
    
    print("🧪 DecisionFramework Test\n")
    
    # 목표 설정
    print("1️⃣ Setting goals:")
    goal1 = framework.add_goal(
        name="Complete organoid research",
        category="research",
        priority=0.95
    )
    print(f"  ✅ Goal: {goal1.name} (priority: {goal1.priority})")
    
    # 선택지 생성
    print("\n2️⃣ Evaluating alternatives:")
    alt1 = Alternative(
        name="Intensive daily work",
        pros=["Fast completion", "High quality control"],
        cons=["High burnout risk", "Expensive"],
        risk_level=0.4
    )
    
    alt2 = Alternative(
        name="Steady pace over time",
        pros=["Sustainable", "Better long-term results"],
        cons=["Slower completion"],
        risk_level=0.2
    )
    
    # 의사결정
    decision = framework.make_decision(
        goal_name="Complete organoid research",
        alternatives=[alt1, alt2]
    )
    
    print(f"  Choice: {decision.chosen_alternative}")
    print(f"  Confidence: {decision.confidence:.0%}")
    print(f"  Rationale: {decision.rationale}")
    
    # 보고서
    print("\n3️⃣ Decision Report:")
    report = framework.get_decision_report()
    print(f"  Total decisions: {report['total_decisions']}")
    print(f"  Average confidence: {report['average_confidence']:.0%}")
    
    print("\n✅ DecisionFramework working!")
