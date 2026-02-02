"""
Reinforcement Learner - Q-Learning 기반 신경계 자동 최적화

시간이 지날수록 신경계가 최적의 모델을 자동으로 선택하도록 학습합니다.
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class NeuralLevel(Enum):
    """신경계 레벨"""
    L1 = "L1"  # 뇌간
    L2 = "L2"  # 변린계
    L3 = "L3"  # 신피질
    L4 = "L4"  # 신경망


@dataclass
class QTableEntry:
    """Q-테이블 항목"""
    state: str
    action: str
    q_value: float
    visits: int
    last_reward: float


@dataclass
class LearningEpisode:
    """학습 에피소드"""
    episode: int
    state: str
    action: str
    reward: float
    q_value: float
    epsilon: float
    timestamp: float


class ReinforcementLearner:
    """Q-Learning 기반 강화학습기"""
    
    def __init__(self, neural_levels: List[str] = None, models: List[str] = None):
        """
        초기화
        
        Args:
            neural_levels: 신경계 레벨 (L1-L4)
            models: 사용 가능 모델
        """
        self.neural_levels = neural_levels or ['L1', 'L2', 'L3', 'L4']
        self.models = models or [
            'Gemini', 'Claude', 'Groq', 'DeepSeek',
            'OpenAI', 'Mistral', 'SambaNova', 'Cerebras'
        ]
        
        # 상태: 신경계 레벨 × 시간대 (아침/오후/저녁/밤)
        self.time_slots = ['morning', 'afternoon', 'evening', 'night']
        self.states = [f"{level}_{slot}" 
                      for level in self.neural_levels 
                      for slot in self.time_slots]
        
        # Q-테이블: Dict[state][action] = Q값
        self.q_table: Dict[str, Dict[str, float]] = {}
        self.visit_counts: Dict[str, Dict[str, int]] = {}
        
        # 하이퍼파라미터
        self.alpha = 0.1        # 학습률
        self.gamma = 0.95       # 할인율
        self.epsilon = 0.1      # 탐색률 (ε-Greedy)
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        # 학습 기록
        self.episodes: List[LearningEpisode] = []
        self.episode_count = 0
        
        self._initialize_q_table()
    
    def _initialize_q_table(self) -> None:
        """Q-테이블 초기화"""
        for state in self.states:
            self.q_table[state] = {}
            self.visit_counts[state] = {}
            
            for action in self.models:
                self.q_table[state][action] = 0.0
                self.visit_counts[state][action] = 0
    
    def get_state(self, neural_level: str, hour: int) -> str:
        """
        현재 상태 반환
        
        Args:
            neural_level: 신경계 레벨
            hour: 시간 (0-23)
            
        Returns:
            상태 문자열
        """
        if hour < 6:
            time_slot = 'night'
        elif hour < 12:
            time_slot = 'morning'
        elif hour < 18:
            time_slot = 'afternoon'
        else:
            time_slot = 'evening'
        
        return f"{neural_level}_{time_slot}"
    
    def select_action_epsilon_greedy(self, state: str) -> str:
        """
        ε-Greedy 정책으로 액션 선택
        
        Args:
            state: 현재 상태
            
        Returns:
            선택된 모델
        """
        if np.random.random() < self.epsilon:
            # 탐색: 랜덤 모델 선택
            return np.random.choice(self.models)
        else:
            # 활용: 최고 Q값 모델 선택
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            best_actions = [model for model, q in q_values.items() 
                          if q == max_q]
            return np.random.choice(best_actions)
    
    def select_best_action(self, state: str) -> str:
        """
        최고 Q값 액션 선택 (활용만)
        
        Args:
            state: 현재 상태
            
        Returns:
            최고 Q값 모델
        """
        q_values = self.q_table[state]
        max_q = max(q_values.values())
        best_actions = [model for model, q in q_values.items() 
                       if q == max_q]
        return np.random.choice(best_actions)
    
    def update_q_value(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str
    ) -> float:
        """
        Q값 업데이트 (Q-Learning)
        
        Args:
            state: 현재 상태
            action: 선택한 액션
            reward: 받은 보상
            next_state: 다음 상태
            
        Returns:
            업데이트된 Q값
        """
        # 현재 Q값
        current_q = self.q_table[state][action]
        
        # 다음 상태의 최고 Q값
        max_next_q = max(self.q_table[next_state].values())
        
        # Q-Learning 업데이트
        new_q = current_q + self.alpha * (
            reward + self.gamma * max_next_q - current_q
        )
        
        self.q_table[state][action] = new_q
        self.visit_counts[state][action] += 1
        
        return new_q
    
    def train_episode(
        self,
        neural_level: str,
        hour: int,
        model_performance: Dict[str, float]
    ) -> Tuple[str, float]:
        """
        한 에피소드 학습
        
        Args:
            neural_level: 신경계 레벨
            hour: 시간
            model_performance: 각 모델의 성능 (0-1)
            
        Returns:
            (선택된 모델, 보상)
        """
        self.episode_count += 1
        
        # 현재 상태
        state = self.get_state(neural_level, hour)
        
        # 액션 선택 (ε-Greedy)
        action = self.select_action_epsilon_greedy(state)
        
        # 보상 계산
        performance = model_performance.get(action, 0.5)
        reward = self._calculate_reward(performance)
        
        # 다음 상태 (간단하게 현재와 동일)
        next_state = state
        
        # Q값 업데이트
        new_q = self.update_q_value(state, action, reward, next_state)
        
        # 에피소드 기록
        episode = LearningEpisode(
            episode=self.episode_count,
            state=state,
            action=action,
            reward=reward,
            q_value=new_q,
            epsilon=self.epsilon,
            timestamp=datetime.now().timestamp()
        )
        self.episodes.append(episode)
        
        # ε 감소
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        return action, reward
    
    def _calculate_reward(self, performance: float) -> float:
        """
        성능에 따른 보상 계산
        
        Args:
            performance: 모델 성능 (0-1)
            
        Returns:
            보상 (-1.0 ~ 1.0)
        """
        if performance > 0.95:
            return 1.0      # 성공
        elif performance > 0.85:
            return 0.5      # 부분 성공
        elif performance > 0.5:
            return 0.0      # 중간
        else:
            return -0.5     # 실패
    
    def check_convergence(self, window_size: int = 50) -> Tuple[bool, float]:
        """
        수렴 여부 확인 (Q값 변화 < 0.01)
        
        Args:
            window_size: 확인할 윈도우 크기
            
        Returns:
            (수렴 여부, 평균 Q값 변화)
        """
        if len(self.episodes) < window_size:
            return False, 0.0
        
        recent_episodes = self.episodes[-window_size:]
        q_changes = []
        
        for i in range(1, len(recent_episodes)):
            q_change = abs(
                recent_episodes[i].q_value - recent_episodes[i-1].q_value
            )
            q_changes.append(q_change)
        
        avg_change = np.mean(q_changes) if q_changes else 0.0
        converged = avg_change < 0.01
        
        return converged, avg_change
    
    def get_q_statistics(self) -> Dict:
        """Q값 통계"""
        all_q_values = []
        
        for state_q in self.q_table.values():
            all_q_values.extend(state_q.values())
        
        if not all_q_values:
            return {}
        
        return {
            'mean_q': float(np.mean(all_q_values)),
            'std_q': float(np.std(all_q_values)),
            'min_q': float(np.min(all_q_values)),
            'max_q': float(np.max(all_q_values)),
            'total_q_values': len(all_q_values)
        }
    
    def get_model_rankings(self) -> Dict[str, float]:
        """모델별 평균 Q값 순위"""
        model_q_values = {model: [] for model in self.models}
        
        for state_q in self.q_table.values():
            for model, q in state_q.items():
                if q > 0:
                    model_q_values[model].append(q)
        
        rankings = {}
        for model, q_vals in model_q_values.items():
            if q_vals:
                rankings[model] = float(np.mean(q_vals))
            else:
                rankings[model] = 0.0
        
        return dict(sorted(rankings.items(), key=lambda x: x[1], reverse=True))
    
    def export_q_table(self, filename: str) -> None:
        """Q-테이블 내보내기"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'episodes': len(self.episodes),
            'convergence': self.check_convergence(),
            'q_statistics': self.get_q_statistics(),
            'model_rankings': self.get_model_rankings(),
            'q_table': self.q_table,
            'visit_counts': self.visit_counts,
            'recent_episodes': [asdict(e) for e in self.episodes[-20:]]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def get_best_policy(self) -> Dict[str, str]:
        """최적 정책: 상태→최고 모델"""
        policy = {}
        
        for state in self.states:
            policy[state] = self.select_best_action(state)
        
        return policy


# 테스트 코드
if __name__ == "__main__":
    learner = ReinforcementLearner()
    
    # 100 에피소드 학습 시뮬레이션
    np.random.seed(42)
    
    for episode in range(100):
        neural_level = np.random.choice(['L1', 'L2', 'L3', 'L4'])
        hour = np.random.randint(0, 24)
        
        # 모델 성능 시뮬레이션
        model_performance = {
            model: np.random.random() * 0.9 + 0.1
            for model in learner.models
        }
        
        model, reward = learner.train_episode(
            neural_level, hour, model_performance
        )
    
    # 결과 출력
    print("=== 학습 완료 ===")
    print(f"에피소드: {learner.episode_count}")
    print(f"현재 ε: {learner.epsilon:.4f}")
    
    converged, avg_change = learner.check_convergence()
    print(f"수렴: {converged}, 평균 변화: {avg_change:.6f}")
    
    print("\n=== 모델 순위 ===")
    for i, (model, score) in enumerate(learner.get_model_rankings().items(), 1):
        print(f"{i}. {model}: {score:.4f}")
    
    print("\n=== 최적 정책 (샘플) ===")
    policy = learner.get_best_policy()
    for state in sorted(list(policy.keys())[:8]):
        print(f"{state}: {policy[state]}")
