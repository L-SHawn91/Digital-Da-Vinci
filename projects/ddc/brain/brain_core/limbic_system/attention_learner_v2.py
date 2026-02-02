#!/usr/bin/env python3
"""
attention_learner.py - L2 변연계: 우선순위 & 학습 시스템 (Week 5-6, Step 3)

감정에 따른 중요도 판단 & 감정 기반 Q-Learning
상황별 최적 전략 학습 + 신경 신호 라우팅
"""

import json
import random
import statistics
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib


@dataclass
class PriorityLevel:
    """우선순위 레벨"""
    score: float  # 0-1
    level: str  # critical, high, medium, low
    reasoning: str
    action_required: bool


class PriorityCalculator:
    """우선순위 계산 엔진"""
    
    # 감정별 기본 우선순위
    EMOTION_PRIORITY = {
        'happy': 0.3,      # 낮음 (유지만 하면 됨)
        'sad': 0.8,        # 높음 (지원 필요)
        'angry': 0.9,      # 매우 높음 (즉시 대응)
        'fear': 0.85,      # 높음 (지원 필요)
        'surprise': 0.4,   # 중간 (대응 필요)
        'neutral': 0.2,    # 낮음 (정보 전달만)
    }
    
    # 강도에 따른 우선순위 배수
    INTENSITY_MULTIPLIER = {
        'weak': 0.5,       # <0.3
        'moderate': 1.0,   # 0.3-0.6
        'strong': 1.5,     # 0.6-0.8
        'intense': 2.0,    # >=0.8
    }
    
    def __init__(self):
        """우선순위 계산기 초기화"""
        self.priority_history = []
        self.user_patterns = defaultdict(dict)
    
    def calculate(self, emotion: str, intensity: float, context: Dict = None) -> PriorityLevel:
        """
        우선순위를 계산합니다.
        
        Args:
            emotion: 감정
            intensity: 강도 (0-1)
            context: 맥락 정보
            
        Returns:
            PriorityLevel: 우선순위 레벨
        """
        # 1. 감정 기본 우선순위
        base_priority = self.EMOTION_PRIORITY.get(emotion, 0.5)
        
        # 2. 강도 배수 적용
        intensity_level = self._get_intensity_level(intensity)
        multiplier = self.INTENSITY_MULTIPLIER.get(intensity_level, 1.0)
        
        # 3. 맥락 요소 적용
        context_boost = 0.0
        reasoning = []
        
        if context:
            # 긴급 여부 확인
            if context.get('is_urgent', False):
                context_boost += 0.2
                reasoning.append('긴급 상황')
            
            # 질문이 많으면 응답 필요
            if context.get('question_count', 0) > 1:
                context_boost += 0.15
                reasoning.append('여러 질문 감지')
            
            # 메시지 길이 (길면 중요할 가능성)
            if context.get('text_length', 0) > 100:
                context_boost += 0.1
                reasoning.append('긴 메시지')
        
        # 4. 최종 우선순위 계산
        final_priority = min(1.0, base_priority * multiplier + context_boost)
        
        # 5. 우선순위 레벨 결정
        if final_priority >= 0.8:
            level = 'critical'
            action_required = True
        elif final_priority >= 0.6:
            level = 'high'
            action_required = True
        elif final_priority >= 0.4:
            level = 'medium'
            action_required = True
        else:
            level = 'low'
            action_required = False
        
        reasoning_text = ' + '.join(reasoning) if reasoning else '감정 기반 판단'
        
        result = PriorityLevel(
            score=round(final_priority, 2),
            level=level,
            reasoning=reasoning_text,
            action_required=action_required
        )
        
        self.priority_history.append({
            'emotion': emotion,
            'priority': result.score,
            'level': level,
            'timestamp': datetime.now().isoformat(),
        })
        
        return result
    
    def _get_intensity_level(self, intensity: float) -> str:
        """강도 레벨 결정"""
        if intensity < 0.3:
            return 'weak'
        elif intensity < 0.6:
            return 'moderate'
        elif intensity < 0.8:
            return 'strong'
        else:
            return 'intense'


class EmotionalQLearner:
    """감정 기반 Q-Learning 엔진"""
    
    def __init__(self, learning_rate: float = 0.15, discount_factor: float = 0.85, exploration_rate: float = 0.20):
        """
        감정 Q-Learning 초기화
        
        Args:
            learning_rate: 학습률 (α) - 0.15로 빠른 학습
            discount_factor: 할인율 (γ) - 0.85로 현재 만족도 중시
            exploration_rate: 탐험률 (ε) - 0.20으로 20% 탐험
        """
        self.alpha = learning_rate  # 0.15
        self.gamma = discount_factor  # 0.85
        self.epsilon = exploration_rate  # 0.20
        
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.emotion_weights = {
            'happy': 1.2,      # 행복은 약간 가중치
            'sad': 1.8,        # 슬픔은 높은 가중치
            'angry': 2.0,      # 분노는 최고 가중치
            'fear': 1.8,       # 두려움은 높은 가중치
            'surprise': 1.0,   # 놀람은 기본
            'neutral': 0.8,    # 중립은 낮은 가중치
        }
        
        self.learning_history = []
        self.convergence_history = []
    
    def select_action(self, state: str, available_actions: List[str]) -> str:
        """
        ε-그리디 정책으로 행동을 선택합니다.
        
        Args:
            state: 현재 상태
            available_actions: 가능한 행동 목록
            
        Returns:
            str: 선택된 행동
        """
        # 20% 탐험, 80% 활용
        if random.random() < self.epsilon:
            # 탐험: 무작위 선택
            return random.choice(available_actions)
        else:
            # 활용: 최고 Q값 선택
            best_actions = []
            best_q = -float('inf')
            
            for action in available_actions:
                q_value = self.q_table[state][action]
                
                if q_value > best_q:
                    best_q = q_value
                    best_actions = [action]
                elif q_value == best_q:
                    best_actions.append(action)
            
            return random.choice(best_actions)
    
    def update_q_value(self, emotion: str, state: str, action: str, 
                      satisfaction: float, next_state: str, 
                      available_next_actions: List[str]) -> float:
        """
        감정 가중 Q-Learning으로 Q값을 업데이트합니다.
        
        수식: Q(s,a) = Q(s,a) + α[r·w_emotion + γ·max(Q(s',a')) - Q(s,a)]
        
        Args:
            emotion: 감정
            state: 현재 상태
            action: 선택된 행동
            satisfaction: 만족도 (0-10)
            next_state: 다음 상태
            available_next_actions: 다음 가능 행동
            
        Returns:
            float: 업데이트된 Q값
        """
        # 현재 Q값
        current_q = self.q_table[state][action]
        
        # 감정 가중치 적용
        emotion_weight = self.emotion_weights.get(emotion, 1.0)
        weighted_reward = satisfaction * emotion_weight
        
        # 다음 상태의 최고 Q값
        max_future_q = 0.0
        if available_next_actions:
            max_future_q = max(self.q_table[next_state][a] for a in available_next_actions)
        
        # Bellman 방정식
        new_q = current_q + self.alpha * (weighted_reward + self.gamma * max_future_q - current_q)
        
        # Q-table 업데이트
        self.q_table[state][action] = new_q
        
        # 학습 이력 저장
        self.learning_history.append({
            'emotion': emotion,
            'state': state,
            'action': action,
            'satisfaction': satisfaction,
            'old_q': round(current_q, 2),
            'new_q': round(new_q, 2),
            'delta': round(new_q - current_q, 2),
            'timestamp': datetime.now().isoformat(),
        })
        
        return new_q
    
    def get_convergence_status(self) -> Dict:
        """
        학습 수렴 상태를 분석합니다.
        
        Returns:
            Dict: 수렴 상태 정보
        """
        if len(self.learning_history) < 10:
            return {'status': 'insufficient_data', 'convergence_rate': 0.0}
        
        # 최근 100개 학습 이력
        recent = self.learning_history[-100:]
        
        # Q값 변화량 분석
        deltas = [abs(entry['delta']) for entry in recent]
        avg_delta = sum(deltas) / len(deltas)
        
        # 표준편차 계산
        variance = sum((d - avg_delta) ** 2 for d in deltas) / len(deltas)
        std_delta = variance ** 0.5
        
        # 수렴도 계산 (변화가 적을수록 수렴)
        # 0에 가까울수록 수렴, 1에 가까울수록 발산
        convergence_rate = min(1.0, avg_delta / (std_delta + 0.1)) if std_delta > 0 else 0.0
        
        status = 'converging' if convergence_rate < 0.3 else 'exploring'
        
        return {
            'status': status,
            'convergence_rate': round(convergence_rate, 2),
            'avg_delta': round(avg_delta, 2),
            'total_updates': len(self.learning_history),
        }
    
    def get_q_stats(self) -> Dict:
        """Q-table 통계를 조회합니다."""
        if not self.q_table:
            return {}
        
        all_q_values = []
        for state_dict in self.q_table.values():
            all_q_values.extend(state_dict.values())
        
        if not all_q_values:
            return {}
        
        avg_q = sum(all_q_values) / len(all_q_values)
        variance = sum((q - avg_q) ** 2 for q in all_q_values) / len(all_q_values)
        std_q = variance ** 0.5
        
        return {
            'q_range': (round(min(all_q_values), 2), round(max(all_q_values), 2)),
            'avg_q': round(avg_q, 2),
            'std_q': round(std_q, 2),
            'total_states': len(self.q_table),
        }


class StrategyOptimizer:
    """전략 최적화 엔진"""
    
    # 전략 카테고리
    STRATEGIES = {
        'support': {
            'description': '감정적 지원',
            'for_emotions': ['sad', 'fear'],
            'actions': ['empathize', 'listen', 'guide'],
        },
        'management': {
            'description': '감정 관리',
            'for_emotions': ['angry', 'fear'],
            'actions': ['calm', 'explain', 'redirect'],
        },
        'celebration': {
            'description': '축하/공유',
            'for_emotions': ['happy', 'surprise'],
            'actions': ['celebrate', 'encourage', 'share'],
        },
        'information': {
            'description': '정보 제공',
            'for_emotions': ['neutral'],
            'actions': ['inform', 'explain', 'guide'],
        },
    }
    
    def __init__(self):
        """전략 최적화기 초기화"""
        self.strategy_performance = defaultdict(lambda: {'success': 0, 'total': 0})
        self.strategy_history = []
    
    def recommend_strategy(self, emotion: str, priority_level: str) -> Dict:
        """
        감정과 우선순위에 따라 최적 전략을 추천합니다.
        
        Args:
            emotion: 감정
            priority_level: 우선순위 레벨
            
        Returns:
            Dict: 추천 전략
        """
        # 감정에 맞는 전략 찾기
        matching_strategies = []
        
        for strategy_name, strategy_info in self.STRATEGIES.items():
            if emotion in strategy_info['for_emotions']:
                matching_strategies.append((strategy_name, strategy_info))
        
        if not matching_strategies:
            matching_strategies = [('information', self.STRATEGIES['information'])]
        
        # 우선순위에 따라 전략 선택
        if priority_level == 'critical':
            # 가장 효과적인 전략
            best_strategy = max(matching_strategies,
                              key=lambda x: self.strategy_performance[x[0]]['success'] / max(1, self.strategy_performance[x[0]]['total']))
        else:
            best_strategy = matching_strategies[0]
        
        return {
            'strategy': best_strategy[0],
            'description': best_strategy[1]['description'],
            'actions': best_strategy[1]['actions'],
            'emotion': emotion,
            'priority': priority_level,
        }
    
    def record_strategy_outcome(self, strategy: str, success: bool) -> None:
        """전략의 성공 여부를 기록합니다."""
        self.strategy_performance[strategy]['total'] += 1
        if success:
            self.strategy_performance[strategy]['success'] += 1
        
        self.strategy_history.append({
            'strategy': strategy,
            'success': success,
            'timestamp': datetime.now().isoformat(),
        })
    
    def get_strategy_stats(self) -> Dict:
        """전략별 성공률을 조회합니다."""
        stats = {}
        for strategy, perf in self.strategy_performance.items():
            if perf['total'] > 0:
                success_rate = perf['success'] / perf['total']
                stats[strategy] = {
                    'success_rate': round(success_rate, 2),
                    'total_uses': perf['total'],
                    'successes': perf['success'],
                }
        
        return stats


class NeuroSignalRouter:
    """신경 신호 라우팅 (L4로 전달)"""
    
    def __init__(self):
        """신경 신호 라우터 초기화"""
        self.routing_table = []
        self.signal_queue = []
    
    def route_signal(self, emotion: str, priority: float, strategy: str, 
                    satisfaction: float) -> Dict:
        """
        신경 신호를 다음 계층(L3/L4)으로 라우팅합니다.
        
        Args:
            emotion: 감정
            priority: 우선순위
            strategy: 전략
            satisfaction: 만족도
            
        Returns:
            Dict: 라우팅된 신호
        """
        signal = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'priority': priority,
            'strategy': strategy,
            'satisfaction': satisfaction,
            'destination': self._determine_destination(priority, strategy),
            'urgency': 'immediate' if priority >= 0.8 else 'normal',
        }
        
        self.signal_queue.append(signal)
        return signal
    
    def _determine_destination(self, priority: float, strategy: str) -> str:
        """라우팅 목적지를 결정합니다."""
        if priority >= 0.9 and strategy in ['management', 'support']:
            return 'L3_executive_center'  # 긴급: 전두엽으로
        elif priority >= 0.7:
            return 'L3_limbic_processing'  # 높음: 측두엽으로
        else:
            return 'L3_standard_processing'  # 낮음: 기본 처리


class AttentionLearnerSystem:
    """통합 우선순위 & 학습 시스템"""
    
    def __init__(self):
        """시스템 초기화"""
        self.priority_calc = PriorityCalculator()
        self.q_learner = EmotionalQLearner()
        self.strategy_opt = StrategyOptimizer()
        self.signal_router = NeuroSignalRouter()
    
    def process_emotion(self, emotion: str, intensity: float, 
                       satisfaction: float, context: Dict = None, 
                       user_id: str = None) -> Dict:
        """
        감정을 처리하고 학습합니다.
        
        Args:
            emotion: 감정
            intensity: 강도
            satisfaction: 만족도 (0-10)
            context: 맥락
            user_id: 사용자 ID
            
        Returns:
            Dict: 처리 결과
        """
        # 1. 우선순위 계산
        priority = self.priority_calc.calculate(emotion, intensity, context)
        
        # 2. 전략 추천
        strategy_rec = self.strategy_opt.recommend_strategy(emotion, priority.level)
        
        # 3. Q-Learning 업데이트
        state = f"{emotion}_{priority.level}"
        next_state = f"{emotion}_processed"
        action = strategy_rec['strategy']
        
        q_value = self.q_learner.update_q_value(
            emotion=emotion,
            state=state,
            action=action,
            satisfaction=satisfaction,
            next_state=next_state,
            available_next_actions=['support', 'management', 'celebration']
        )
        
        # 4. 신경 신호 라우팅
        signal = self.signal_router.route_signal(
            emotion=emotion,
            priority=priority.score,
            strategy=action,
            satisfaction=satisfaction
        )
        
        # 5. 결과 종합
        result = {
            'emotion': emotion,
            'priority': {
                'score': priority.score,
                'level': priority.level,
                'reasoning': priority.reasoning,
                'action_required': priority.action_required,
            },
            'strategy': strategy_rec,
            'q_learning': {
                'state': state,
                'action': action,
                'q_value': round(q_value, 2),
            },
            'signal': signal,
            'convergence': self.q_learner.get_convergence_status(),
        }
        
        return result
    
    def get_system_report(self) -> Dict:
        """시스템 전체 리포트"""
        return {
            'q_learning_stats': self.q_learner.get_q_stats(),
            'convergence': self.q_learner.get_convergence_status(),
            'strategy_performance': self.strategy_opt.get_strategy_stats(),
            'total_signals': len(self.signal_router.signal_queue),
        }


# ============================================================================
# 테스트 코드
# ============================================================================

if __name__ == '__main__':
    print('=' * 80)
    print('🧠 L2 변연계: 우선순위 & 학습 시스템 테스트')
    print('=' * 80)
    
    system = AttentionLearnerSystem()
    
    # 테스트 케이스
    test_cases = [
        ('happy', 0.85, 8.0),
        ('sad', 0.80, 6.0),
        ('angry', 1.00, 5.0),
        ('fear', 0.65, 4.0),
        ('surprise', 0.70, 7.0),
        ('neutral', 0.50, 5.0),
    ]
    
    print('\n📊 감정 처리 & 학습:\n')
    
    for emotion, intensity, satisfaction in test_cases:
        context = {
            'is_urgent': intensity > 0.8,
            'question_count': int(intensity * 3),
            'text_length': int(intensity * 200),
        }
        
        result = system.process_emotion(emotion, intensity, satisfaction, context)
        
        print(f'감정: {result["emotion"]} (강도: {intensity})')
        print(f'우선순위: {result["priority"]["level"]} ({result["priority"]["score"]})')
        print(f'전략: {result["strategy"]["strategy"]} - {result["strategy"]["description"]}')
        print(f'Q값: {result["q_learning"]["q_value"]}')
        print(f'신경신호: {result["signal"]["destination"]} (긴급도: {result["signal"]["urgency"]})')
        print(f'수렴도: {result["convergence"]["convergence_rate"]}')
        print('-' * 80)
    
    # 시스템 리포트
    print('\n📈 시스템 전체 리포트:\n')
    report = system.get_system_report()
    print(f'Q-Learning 통계: {report["q_learning_stats"]}')
    print(f'수렴 상태: {report["convergence"]}')
    print(f'전략 성능: {report["strategy_performance"]}')
    print(f'총 신경신호: {report["total_signals"]}')
    
    print('\n✅ 우선순위 & 학습 시스템 테스트 완료!')
    print('=' * 80)
