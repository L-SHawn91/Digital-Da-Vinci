"""
EmotionProcessor - Limbic System의 감정 처리
감정 상태, 감정 전파, 감정-기억 연결
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class BasicEmotion(Enum):
    """기본 감정 (Ekman's Big Six)"""
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"


class ArousalLevel(Enum):
    """각성 수준"""
    CALM = 0.2
    ALERT = 0.5
    EXCITED = 0.8
    OVERWHELMED = 1.0


@dataclass
class EmotionalState:
    """감정 상태"""
    emotions: Dict[str, float] = field(default_factory=dict)  # emotion -> intensity (0~1)
    valence: float = 0.0  # -1 (negative) ~ 1 (positive)
    arousal: float = 0.5  # 0 (calm) ~ 1 (intense)
    timestamp: datetime = field(default_factory=datetime.now)
    intensity: float = 0.0  # 전체 감정 강도
    dominant_emotion: Optional[str] = None


@dataclass
class EmotionalMemoryLink:
    """감정-기억 연결"""
    memory_id: str
    emotion: str
    strength: float  # 연결 강도 (0~1)
    timestamp: datetime = field(default_factory=datetime.now)


class EmotionProcessor:
    """
    감정 처리 시스템
    - 감정 상태 관리
    - 감정 전파 (다른 상태에 영향)
    - 감정-기억 연결
    - 감정 동역학 (dynamics)
    """
    
    def __init__(self):
        """감정 프로세서 초기화"""
        self.current_state = EmotionalState()
        self.emotional_history: List[EmotionalState] = []
        self.emotion_memory_links: List[EmotionalMemoryLink] = []
        
        # 기본 감정 초기값
        self.reset_emotions()
    
    def reset_emotions(self):
        """감정 초기화 (neutral state)"""
        self.current_state.emotions = {
            BasicEmotion.HAPPINESS.value: 0.0,
            BasicEmotion.SADNESS.value: 0.0,
            BasicEmotion.ANGER.value: 0.0,
            BasicEmotion.FEAR.value: 0.0,
            BasicEmotion.DISGUST.value: 0.0,
            BasicEmotion.SURPRISE.value: 0.0
        }
        self.current_state.valence = 0.0
        self.current_state.arousal = 0.5
        self.current_state.intensity = 0.0
        self.current_state.dominant_emotion = None
    
    def set_emotion(
        self,
        emotion: str,
        intensity: float,
        trigger: Optional[str] = None
    ):
        """
        감정 설정
        
        Args:
            emotion: 감정 종류 (happiness, sadness, anger, fear, disgust, surprise)
            intensity: 강도 (0~1)
            trigger: 감정 유발 원인
        """
        intensity = max(0.0, min(1.0, intensity))
        
        if emotion in self.current_state.emotions:
            self.current_state.emotions[emotion] = intensity
        
        # 가치감 계산
        self._update_valence()
        
        # 각성 수준 업데이트
        self._update_arousal()
        
        # 지배적 감정 결정
        self._determine_dominant_emotion()
        
        # 감정 전파
        self._propagate_emotion(emotion, intensity)
        
        # 히스토리 저장
        self._save_state()
    
    def _update_valence(self):
        """감정들로부터 가치감 계산"""
        positive = self.current_state.emotions.get(BasicEmotion.HAPPINESS.value, 0.0)
        positive += self.current_state.emotions.get(BasicEmotion.SURPRISE.value, 0.0) * 0.5
        
        negative = self.current_state.emotions.get(BasicEmotion.SADNESS.value, 0.0)
        negative += self.current_state.emotions.get(BasicEmotion.ANGER.value, 0.0) * 0.8
        negative += self.current_state.emotions.get(BasicEmotion.FEAR.value, 0.0) * 0.9
        negative += self.current_state.emotions.get(BasicEmotion.DISGUST.value, 0.0)
        
        self.current_state.valence = (positive - negative) / 2.0
    
    def _update_arousal(self):
        """각성 수준 업데이트"""
        # 높은 감정 강도 = 높은 각성
        high_arousal_emotions = [
            BasicEmotion.ANGER.value,
            BasicEmotion.FEAR.value,
            BasicEmotion.SURPRISE.value,
            BasicEmotion.HAPPINESS.value
        ]
        
        high_arousal_level = max(
            [self.current_state.emotions.get(e, 0.0) for e in high_arousal_emotions]
        )
        
        low_arousal_emotions = [
            BasicEmotion.SADNESS.value,
            BasicEmotion.DISGUST.value
        ]
        
        low_arousal_level = max(
            [self.current_state.emotions.get(e, 0.0) for e in low_arousal_emotions]
        )
        
        # 가중 평균
        self.current_state.arousal = (high_arousal_level * 0.7 + low_arousal_level * 0.3)
    
    def _determine_dominant_emotion(self):
        """지배적 감정 결정"""
        if not self.current_state.emotions:
            self.current_state.dominant_emotion = None
            return
        
        max_emotion = max(self.current_state.emotions.items(), key=lambda x: x[1])
        if max_emotion[1] > 0.1:  # 최소 임계값
            self.current_state.dominant_emotion = max_emotion[0]
            self.current_state.intensity = max_emotion[1]
        else:
            self.current_state.dominant_emotion = None
            self.current_state.intensity = 0.0
    
    def _propagate_emotion(self, emotion: str, intensity: float):
        """
        감정 전파 (고도화 v2.0)
        한 감정이 다른 감정들에 영향을 미침
        - 더 정교한 상호작용 모델
        - 강도 기반 감정 전파 계수
        - 양극성 감정 쌍 고려
        """
        # 감정 간 상호작용 매트릭스 (고도화)
        propagation_rules = {
            BasicEmotion.HAPPINESS.value: {
                BasicEmotion.SURPRISE.value: 0.4,  # 행복은 놀람을 강하게 증가
                BasicEmotion.SADNESS.value: -0.5,  # 행복은 슬픔을 강하게 억제
                BasicEmotion.ANGER.value: -0.3,    # 행복은 화를 약하게 억제
            },
            BasicEmotion.SADNESS.value: {
                BasicEmotion.FEAR.value: 0.4,      # 슬픔은 두려움을 강하게 증가
                BasicEmotion.HAPPINESS.value: -0.6, # 슬픔은 행복을 강하게 억제
                BasicEmotion.SURPRISE.value: -0.2,  # 슬픔은 놀람을 약하게 억제
            },
            BasicEmotion.ANGER.value: {
                BasicEmotion.DISGUST.value: 0.5,    # 화는 혐오를 강하게 증가
                BasicEmotion.FEAR.value: 0.3,       # 화는 두려움을 증가
                BasicEmotion.HAPPINESS.value: -0.7, # 화는 행복을 강하게 억제
                BasicEmotion.SADNESS.value: 0.2,    # 화는 슬픔을 약하게 증가
            },
            BasicEmotion.FEAR.value: {
                BasicEmotion.SURPRISE.value: 0.4,   # 두려움은 놀람을 증가
                BasicEmotion.ANGER.value: 0.3,      # 두려움은 화로 전환될 수 있음
                BasicEmotion.SADNESS.value: 0.3,    # 두려움은 슬픔을 증가
                BasicEmotion.DISGUST.value: 0.2,    # 두려움은 혐오를 약하게 증가
            },
            BasicEmotion.DISGUST.value: {
                BasicEmotion.ANGER.value: 0.4,      # 혐오는 화를 증가
                BasicEmotion.HAPPINESS.value: -0.6, # 혐오는 행복을 강하게 억제
                BasicEmotion.SADNESS.value: 0.2,    # 혐오는 슬픔을 약하게 증가
            },
            BasicEmotion.SURPRISE.value: {
                BasicEmotion.FEAR.value: 0.3,       # 놀람은 두려움으로 변할 수 있음
                BasicEmotion.HAPPINESS.value: 0.3,  # 놀람은 행복으로도 변할 수 있음
                BasicEmotion.SADNESS.value: -0.2,   # 놀람은 슬픔을 약하게 억제
            }
        }

        if emotion in propagation_rules:
            # 감정 강도에 따른 동적 전파
            propagation_strength = min(1.0, intensity * 0.5 + 0.3)  # 0.3 ~ 0.8

            for target_emotion, factor in propagation_rules[emotion].items():
                if target_emotion in self.current_state.emotions:
                    # 강도 기반 적응 전파
                    change = intensity * factor * propagation_strength
                    current = self.current_state.emotions[target_emotion]
                    self.current_state.emotions[target_emotion] = max(
                        0.0, min(1.0, current + change)
                    )
    
    def _save_state(self):
        """현재 감정 상태 저장"""
        self.emotional_history.append(
            EmotionalState(
                emotions=self.current_state.emotions.copy(),
                valence=self.current_state.valence,
                arousal=self.current_state.arousal,
                intensity=self.current_state.intensity,
                dominant_emotion=self.current_state.dominant_emotion
            )
        )
        
        # 최대 1000개 유지
        if len(self.emotional_history) > 1000:
            self.emotional_history = self.emotional_history[-1000:]
    
    def link_emotion_to_memory(
        self,
        memory_id: str,
        emotion: str,
        strength: float = 0.5
    ):
        """감정과 기억 연결"""
        link = EmotionalMemoryLink(
            memory_id=memory_id,
            emotion=emotion,
            strength=min(1.0, max(0.0, strength))
        )
        self.emotion_memory_links.append(link)
    
    def get_emotional_context(self, memory_id: str) -> Dict:
        """기억의 감정적 맥락 조회"""
        links = [
            link for link in self.emotion_memory_links
            if link.memory_id == memory_id
        ]
        
        return {
            'memory_id': memory_id,
            'emotional_associations': [
                {
                    'emotion': link.emotion,
                    'strength': link.strength,
                    'timestamp': link.timestamp.isoformat()
                }
                for link in links
            ],
            'total_associations': len(links)
        }
    
    def get_emotional_state_report(self) -> Dict:
        """감정 상태 보고서 (고도화)"""
        # 감정 안정성 지수 계산
        stability_index = self._calculate_emotional_stability()

        # 감정 다양성 지수 (다양한 감정이 섞여있는 정도)
        diversity_index = self._calculate_emotional_diversity()

        return {
            'current_state': {
                'dominant_emotion': self.current_state.dominant_emotion,
                'intensity': self.current_state.intensity,
                'valence': self.current_state.valence,
                'arousal': self.current_state.arousal,
                'timestamp': self.current_state.timestamp.isoformat()
            },
            'all_emotions': self.current_state.emotions,
            'stability_index': stability_index,  # 0~1: 높을수록 안정적
            'diversity_index': diversity_index,   # 0~1: 높을수록 다양한 감정
            'emotional_complexity': stability_index * diversity_index,  # 복잡도
            'history_length': len(self.emotional_history),
            'memory_links': len(self.emotion_memory_links)
        }

    def _calculate_emotional_stability(self) -> float:
        """감정 안정성 지수 계산"""
        if len(self.emotional_history) < 2:
            return 0.5

        # 최근 3개 상태의 변화도로 안정성 계산
        recent = self.emotional_history[-3:] if len(self.emotional_history) >= 3 else self.emotional_history

        total_change = 0.0
        for i in range(1, len(recent)):
            prev_emotions = recent[i-1].emotions
            curr_emotions = recent[i].emotions

            change = sum(abs(curr_emotions.get(e, 0.0) - prev_emotions.get(e, 0.0))
                        for e in prev_emotions.keys())
            total_change += change / len(prev_emotions) if prev_emotions else 0.0

        avg_change = total_change / max(1, len(recent) - 1)
        # 변화가 적을수록 안정적 (1.0 - 변화도)
        return max(0.0, 1.0 - min(1.0, avg_change))

    def _calculate_emotional_diversity(self) -> float:
        """감정 다양성 지수 계산"""
        emotions = self.current_state.emotions
        if not emotions:
            return 0.0

        # 0이 아닌 감정의 개수로 다양성 측정
        active_emotions = sum(1 for intensity in emotions.values() if intensity > 0.1)
        total_emotions = len(emotions)

        return active_emotions / total_emotions if total_emotions > 0 else 0.0
    
    def simulate_emotional_recovery(self, time_minutes: int = 30) -> Dict:
        """
        감정 회복 시뮬레이션
        시간이 지나면서 감정이 중립으로 돌아감
        """
        recovery_rate = 0.02 * time_minutes  # 분당 2% 회복
        
        for emotion in self.current_state.emotions:
            current = self.current_state.emotions[emotion]
            # 중립(0.0)으로 향함
            self.current_state.emotions[emotion] = current * (1.0 - recovery_rate)
        
        self._update_valence()
        self._update_arousal()
        self._determine_dominant_emotion()
        self._save_state()
        
        return self.get_emotional_state_report()


# 테스트
if __name__ == "__main__":
    processor = EmotionProcessor()
    
    print("🧪 EmotionProcessor Test\n")
    
    # 1. 행복 설정
    print("1️⃣ Setting HAPPINESS (intensity 0.8)")
    processor.set_emotion("happiness", 0.8, trigger="successful organoid differentiation")
    report = processor.get_emotional_state_report()
    print(f"  Valence: {report['current_state']['valence']:.2f}")
    print(f"  Arousal: {report['current_state']['arousal']:.2f}")
    print(f"  Dominant: {report['current_state']['dominant_emotion']}")
    
    # 2. 기억과 연결
    print("\n2️⃣ Linking emotion to memory")
    processor.link_emotion_to_memory("memory_001", "happiness", 0.8)
    context = processor.get_emotional_context("memory_001")
    print(f"  Associations: {context['total_associations']}")
    
    # 3. 감정 전파 확인
    print("\n3️⃣ Checking emotion propagation")
    emotions = processor.get_emotional_state_report()['all_emotions']
    print(f"  Happiness: {emotions['happiness']:.2f}")
    print(f"  Surprise: {emotions['surprise']:.2f} (propagated)")
    print(f"  Sadness: {emotions['sadness']:.2f} (suppressed)")
    
    # 4. 감정 회복
    print("\n4️⃣ Emotional recovery after 30 minutes")
    recovery = processor.simulate_emotional_recovery(30)
    print(f"  Valence: {recovery['current_state']['valence']:.2f}")
    print(f"  Dominant: {recovery['current_state']['dominant_emotion']}")
    
    print("\n✅ EmotionProcessor working!")
