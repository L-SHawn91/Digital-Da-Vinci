"""
강화학습 & 의사결정 최적화 - AI 기반 선택

역할:
- 상황별 최적 선택
- 보상 기반 학습
- 정책 최적화
- 적응형 의사결정
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import random


@dataclass
class State:
    """상태"""
    id: str
    features: Dict[str, float]
    reward: float = 0.0


@dataclass
class Action:
    """행동"""
    id: str
    name: str
    estimated_reward: float = 0.0
    times_taken: int = 0
    success_count: int = 0


class MultiArmedBandit:
    """다중 팔 슬롯 머신 (기본 강화학습)"""
    
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon  # 탐험률
        self.actions: Dict[str, Action] = {}
        self.history = []
    
    def add_action(self, action: Action):
        """행동 추가"""
        self.actions[action.id] = action
    
    def select_action(self) -> Action:
        """행동 선택 (ε-그리디)"""
        
        if random.random() < self.epsilon:
            # 탐험: 무작위 선택
            return random.choice(list(self.actions.values()))
        else:
            # 활용: 최고 보상 선택
            return max(self.actions.values(), key=lambda a: a.estimated_reward)
    
    def update_action(self, action_id: str, reward: float):
        """행동 결과 업데이트"""
        
        if action_id not in self.actions:
            return
        
        action = self.actions[action_id]
        action.times_taken += 1
        
        if reward > 0:
            action.success_count += 1
        
        # 평균 보상 업데이트
        action.estimated_reward = action.success_count / action.times_taken
        
        self.history.append({
            'action_id': action_id,
            'reward': reward,
            'cumulative_reward': sum(a.estimated_reward * a.times_taken 
                                    for a in self.actions.values())
        })


class QLearning:
    """Q-러닝 알고리즘"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table: Dict[Tuple[str, str], float] = {}  # (state, action) -> Q-value
    
    def get_q_value(self, state_id: str, action_id: str) -> float:
        """Q-값 조회"""
        return self.q_table.get((state_id, action_id), 0.0)
    
    def update_q_value(
        self,
        state_id: str,
        action_id: str,
        reward: float,
        next_state_id: str,
        next_actions: List[str]
    ):
        """Q-값 업데이트"""
        
        current_q = self.get_q_value(state_id, action_id)
        
        # 다음 상태에서 최고 Q-값 조회
        max_next_q = max(
            [self.get_q_value(next_state_id, a) for a in next_actions],
            default=0.0
        )
        
        # Q-값 업데이트
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[(state_id, action_id)] = new_q
    
    def select_best_action(self, state_id: str, actions: List[str]) -> str:
        """최고 행동 선택"""
        
        q_values = [self.get_q_value(state_id, a) for a in actions]
        best_action_idx = q_values.index(max(q_values))
        return actions[best_action_idx]


class PolicyOptimizer:
    """정책 최적화"""
    
    def __init__(self):
        self.q_learning = QLearning()
        self.multi_armed_bandit = MultiArmedBandit(epsilon=0.15)
        self.policy_history = []
    
    async def optimize_decision(
        self,
        current_state: State,
        available_actions: List[Action],
        context: Dict[str, Any] = None
    ) -> Tuple[Action, Dict[str, Any]]:
        """의사결정 최적화"""
        
        decision_data = {
            'state_id': current_state.id,
            'state_features': current_state.features,
            'available_actions': [a.name for a in available_actions],
            'context': context or {}
        }
        
        # Q-러닝 기반 선택
        if available_actions:
            action_ids = [a.id for a in available_actions]
            best_action_id = self.q_learning.select_best_action(
                current_state.id,
                action_ids
            )
            selected_action = next(a for a in available_actions if a.id == best_action_id)
        else:
            selected_action = available_actions[0] if available_actions else None
        
        decision_data['selected_action'] = selected_action.name if selected_action else None
        decision_data['q_value'] = self.q_learning.get_q_value(
            current_state.id,
            selected_action.id
        ) if selected_action else 0.0
        
        self.policy_history.append(decision_data)
        
        return selected_action, decision_data
    
    def learn_from_feedback(
        self,
        state_id: str,
        action_id: str,
        reward: float,
        next_state_id: str,
        next_actions: List[str]
    ):
        """피드백으로부터 학습"""
        
        self.q_learning.update_q_value(
            state_id,
            action_id,
            reward,
            next_state_id,
            next_actions
        )
        
        self.multi_armed_bandit.update_action(action_id, reward)
    
    def get_policy_report(self) -> Dict[str, Any]:
        """정책 리포트"""
        
        return {
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'total_decisions': len(self.policy_history),
            'q_table_size': len(self.q_learning.q_table),
            'bandit_actions': len(self.multi_armed_bandit.actions),
            'recent_decisions': self.policy_history[-10:] if self.policy_history else [],
            'bandit_performance': {
                a.id: {
                    'times_taken': a.times_taken,
                    'success_count': a.success_count,
                    'success_rate': a.success_count / a.times_taken if a.times_taken > 0 else 0
                }
                for a in self.multi_armed_bandit.actions.values()
            }
        }


if __name__ == "__main__":
    print("🤖 강화학습 & 의사결정 테스트\n")
    
    optimizer = PolicyOptimizer()
    
    # 행동 설정
    actions = [
        Action("action_1", "aggressive_strategy", 0.5),
        Action("action_2", "conservative_strategy", 0.3),
        Action("action_3", "balanced_strategy", 0.6),
    ]
    
    for action in actions:
        optimizer.multi_armed_bandit.add_action(action)
    
    # 시뮬레이션
    state = State("market_state", {"volatility": 0.8, "trend": 0.6})
    
    import asyncio
    
    async def test():
        # 10번 반복
        for i in range(10):
            action, decision = await optimizer.optimize_decision(state, actions)
            
            # 보상 시뮬레이션
            reward = 1.0 if i % 2 == 0 else 0.5
            
            # 학습
            optimizer.learn_from_feedback(
                state.id,
                action.id,
                reward,
                "next_state",
                [a.id for a in actions]
            )
            
            print(f"Step {i+1}: {action.name} -> Reward: {reward}")
        
        # 리포트
        report = optimizer.get_policy_report()
        print(f"\n✅ 정책 학습 완료!")
        print(f"총 의사결정: {report['total_decisions']}")
        print(f"Q-테이블 크기: {report['q_table_size']}")
    
    asyncio.run(test())
