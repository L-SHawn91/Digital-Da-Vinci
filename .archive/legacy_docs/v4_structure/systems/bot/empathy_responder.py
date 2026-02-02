#!/usr/bin/env python3
"""
empathy_responder.py - L2 변연계: 공감 응답 생성 모듈 (Week 4-5, Step 2)

감정에 맞는 자연스러운 응답을 생성합니다.
톤 조정 (따뜻함, 진지함, 가벼움) + 감정 맞춤 표현
응답 다양화 (반복 방지) + 개인화 학습
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import hashlib


@dataclass
class ResponseTemplate:
    """응답 템플릿"""
    emotion: str
    tone: str  # warm, serious, light
    template: str
    intensity_range: Tuple[float, float]  # (min, max)
    keywords: List[str]
    priority: int  # 1-5, 5가 가장 높음


class ToneAdjuster:
    """톤 조정 엔진"""
    
    # 감정별 톤 기본값
    EMOTION_TONE_MAP = {
        'happy': 'warm',      # 따뜻함
        'sad': 'warm',        # 따뜻함
        'angry': 'serious',   # 진지함
        'fear': 'warm',       # 따뜻함
        'surprise': 'light',  # 가벼움
        'neutral': 'serious', # 진지함
    }
    
    # 톤별 특징
    TONE_CHARACTERISTICS = {
        'warm': {
            'emojis': ['😊', '💙', '🤗', '✨', '💝'],
            'expressions': ['정말 그렇군요', '충분히 이해합니다', '공감합니다'],
            'connectors': ['정말', '확실히', '분명히'],
        },
        'serious': {
            'emojis': [],
            'expressions': ['이해하겠습니다', '그러하군요', '분석해보면'],
            'connectors': ['실제로', '객관적으로', '냉철하게'],
        },
        'light': {
            'emojis': ['😄', '😎', '🎉', '⚡', '🌟'],
            'expressions': ['재미있네요', '신기하네요', '좋은데요'],
            'connectors': ['아무튼', '어쨌든', '결국'],
        },
    }
    
    def __init__(self):
        """톤 조정기 초기화"""
        self.tone_history = []
        self.user_tone_preferences = defaultdict(str)
    
    def adjust_tone(self, emotion: str, base_intensity: float, user_id: str = None) -> str:
        """
        감정에 맞게 톤을 조정합니다.
        
        Args:
            emotion: 감정 (happy, sad 등)
            base_intensity: 기본 강도 (0-1)
            user_id: 사용자 ID (선택사항)
            
        Returns:
            str: 조정된 톤
        """
        # 기본 톤 선택
        base_tone = self.EMOTION_TONE_MAP.get(emotion, 'serious')
        
        # 강도에 따른 톤 조정
        if base_intensity > 0.8:
            # 강렬한 감정: 더 따뜻하거나 진지하게
            if emotion in ['sad', 'fear']:
                adjusted_tone = 'warm'
            else:
                adjusted_tone = base_tone
        elif base_intensity < 0.3:
            # 약한 감정: 가볍게
            adjusted_tone = 'light'
        else:
            adjusted_tone = base_tone
        
        # 사용자 선호도 반영
        if user_id and user_id in self.user_tone_preferences:
            preferred = self.user_tone_preferences[user_id]
            # 80% 확률로 선호 톤, 20% 확률로 다양성
            if random.random() < 0.8:
                adjusted_tone = preferred
        
        self.tone_history.append({
            'emotion': emotion,
            'base_tone': base_tone,
            'adjusted_tone': adjusted_tone,
            'intensity': base_intensity,
            'timestamp': datetime.now().isoformat(),
        })
        
        return adjusted_tone
    
    def set_user_preference(self, user_id: str, tone: str) -> None:
        """사용자의 톤 선호도를 설정합니다."""
        if tone in self.TONE_CHARACTERISTICS:
            self.user_tone_preferences[user_id] = tone
    
    def get_tone_characteristics(self, tone: str) -> Dict:
        """톤의 특징을 조회합니다."""
        return self.TONE_CHARACTERISTICS.get(tone, self.TONE_CHARACTERISTICS['serious'])


class ExpressionGenerator:
    """표현 생성 엔진"""
    
    # 감정별 공감 표현
    EMPATHY_EXPRESSIONS = {
        'happy': [
            '정말 좋은 일이 생기셨네요!',
            '당신의 행복이 느껴져요.',
            '그런 순간이 정말 소중하죠.',
            '축하합니다!',
            '정말 멋진데요!',
        ],
        'sad': [
            '정말 힘드신 상황이군요.',
            '그럴 때는 누구나 지쳐있기 마련이에요.',
            '충분히 그럴 수 있습니다.',
            '당신의 감정이 충분히 타당합니다.',
            '혼자가 아니에요.',
        ],
        'angry': [
            '정말 화날 만하네요.',
            '그런 상황이면 분노하는 게 당연합니다.',
            '당신의 감정이 정당합니다.',
            '상황을 이해합니다.',
            '정말 불공평한 상황이네요.',
        ],
        'fear': [
            '그런 불안감은 충분히 이해합니다.',
            '누구나 두려움을 느낄 수 있습니다.',
            '당신은 혼자가 아닙니다.',
            '이 감정은 자연스러운 거예요.',
            '함께라면 괜찮을 거예요.',
        ],
        'surprise': [
            '정말 예상 밖의 일이네요!',
            '뜻밖의 경험을 하셨군요.',
            '흥미로운데요!',
            '정말 신기하네요.',
            '이건 정말 특별한 순간이에요.',
        ],
        'neutral': [
            '그렇군요.',
            '이해하겠습니다.',
            '알겠습니다.',
            '정보 감사합니다.',
            '진행하시면 됩니다.',
        ],
    }
    
    # 감정별 후속 질문
    FOLLOW_UP_QUESTIONS = {
        'happy': [
            '그런 순간이 더 많이 생기길 바라요.',
            '좀 더 이야기해 주시겠어요?',
            '어떤 부분이 가장 좋으셨어요?',
            '당신의 행복을 함께하고 싶어요.',
        ],
        'sad': [
            '어떻게 도와드릴 수 있을까요?',
            '누군가와 이야기 나누면 좀 나을까요?',
            '혼자라고 생각하지 마세요.',
            '지금 필요한 게 뭔지 말씀해 주세요.',
        ],
        'angry': [
            '이 감정을 어떻게 처리하고 싶으세요?',
            '상황이 개선될 수 있는 방법이 있을까요?',
            '지금 필요한 건 뭘까요?',
            '이 감정에서 벗어나는 방법을 함께 생각해 볼까요?',
        ],
        'fear': [
            '당신이 걱정하는 것에 대해 이야기해 줄래요?',
            '어떤 도움이 필요하세요?',
            '작은 것부터 시작해 보는 건 어떨까요?',
            '함께라면 이겨낼 수 있어요.',
        ],
        'surprise': [
            '좀 더 자세히 말씀해 주실래요?',
            '이 경험에서 뭘 배웠어요?',
            '앞으로 어떻게 하실 거예요?',
            '정말 흥미로운데요!',
        ],
        'neutral': [
            '추가로 필요한 게 있으세요?',
            '다른 도움을 드릴 수 있을까요?',
            '궁금한 점이 있으신가요?',
            '언제든 물어봐 주세요.',
        ],
    }
    
    def __init__(self):
        """표현 생성기 초기화"""
        self.generated_history = []
        self.user_preferences = defaultdict(dict)
    
    def generate_main_response(self, emotion: str, intensity: float) -> str:
        """
        주 응답 생성
        
        Args:
            emotion: 감정
            intensity: 강도
            
        Returns:
            str: 생성된 응답
        """
        expressions = self.EMPATHY_EXPRESSIONS.get(emotion, self.EMPATHY_EXPRESSIONS['neutral'])
        
        # 강도에 따라 표현 선택
        if intensity > 0.8:
            # 강렬한 표현
            response = expressions[0]
        elif intensity < 0.3:
            # 약한 표현
            response = expressions[-1]
        else:
            # 무작위 선택
            response = random.choice(expressions)
        
        return response
    
    def generate_follow_up(self, emotion: str) -> str:
        """
        후속 질문 생성
        
        Args:
            emotion: 감정
            
        Returns:
            str: 생성된 후속 질문
        """
        questions = self.FOLLOW_UP_QUESTIONS.get(emotion, self.FOLLOW_UP_QUESTIONS['neutral'])
        return random.choice(questions)
    
    def generate_complete_response(self, emotion: str, intensity: float, include_question: bool = True) -> str:
        """
        완전한 응답 생성 (주 응답 + 선택적 후속 질문)
        
        Args:
            emotion: 감정
            intensity: 강도
            include_question: 후속 질문 포함 여부
            
        Returns:
            str: 완전한 응답
        """
        main = self.generate_main_response(emotion, intensity)
        
        if include_question:
            follow_up = self.generate_follow_up(emotion)
            response = f"{main} {follow_up}"
        else:
            response = main
        
        self.generated_history.append({
            'emotion': emotion,
            'intensity': intensity,
            'response': response,
            'timestamp': datetime.now().isoformat(),
        })
        
        return response


class DiversificationEngine:
    """응답 다양화 엔진 (반복 방지)"""
    
    def __init__(self, history_size: int = 100):
        """다양화 엔진 초기화"""
        self.response_pool = []
        self.history_size = history_size
        self.user_history = defaultdict(list)
    
    def diversify(self, response: str, user_id: str = None) -> str:
        """
        응답을 다양화합니다 (반복 방지).
        
        Args:
            response: 원본 응답
            user_id: 사용자 ID
            
        Returns:
            str: 다양화된 응답
        """
        # 사용자 이력이 있으면 확인
        if user_id and user_id in self.user_history:
            recent = self.user_history[user_id][-10:]  # 최근 10개
            
            # 최근 응답과 같으면 변형
            if any(r['response'] == response for r in recent):
                response = self._transform_response(response)
        
        # 전체 응답 풀에 추가
        self.response_pool.append({
            'response': response,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
        })
        
        # 풀 크기 관리
        if len(self.response_pool) > self.history_size:
            self.response_pool = self.response_pool[-self.history_size:]
        
        if user_id:
            self.user_history[user_id].append({
                'response': response,
                'timestamp': datetime.now().isoformat(),
            })
        
        return response
    
    def _transform_response(self, response: str) -> str:
        """응답을 변형합니다."""
        # 단순 변형 (추후 고급 NLP로 개선)
        transformations = [
            lambda r: r.replace('정말', '진짜'),
            lambda r: r.replace('충분히', '당연히'),
            lambda r: r.replace('당신', '이분'),
            lambda r: r.replace('.', '...'),
            lambda r: r.replace('군요', '네요'),
        ]
        
        transform = random.choice(transformations)
        return transform(response)
    
    def get_response_frequency(self, user_id: str = None) -> Dict:
        """응답 빈도를 조회합니다."""
        if user_id:
            responses = [r['response'] for r in self.user_history[user_id]]
        else:
            responses = [r['response'] for r in self.response_pool]
        
        frequency = {}
        for response in responses:
            frequency[response] = frequency.get(response, 0) + 1
        
        # 내림차순 정렬
        return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))


class UserPreferenceTracker:
    """사용자 선호도 추적 엔진"""
    
    def __init__(self):
        """선호도 추적기 초기화"""
        self.user_preferences = defaultdict(dict)
        self.feedback_history = []
    
    def record_feedback(self, user_id: str, response: str, feedback: int) -> None:
        """
        사용자 피드백을 기록합니다.
        
        Args:
            user_id: 사용자 ID
            response: 제시된 응답
            feedback: 만족도 (1-5, 5가 최고)
        """
        record = {
            'user_id': user_id,
            'response': response,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat(),
        }
        
        self.feedback_history.append(record)
        
        # 사용자 선호도 업데이트
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'total_feedback': 0,
                'avg_satisfaction': 0.0,
                'preferred_expressions': [],
            }
        
        pref = self.user_preferences[user_id]
        pref['total_feedback'] += 1
        
        # 평균 만족도 계산
        all_feedback = [f['feedback'] for f in self.feedback_history if f['user_id'] == user_id]
        pref['avg_satisfaction'] = sum(all_feedback) / len(all_feedback)
        
        # 좋은 응답 추적 (만족도 4 이상)
        if feedback >= 4:
            pref['preferred_expressions'].append(response)
    
    def get_user_preference(self, user_id: str) -> Dict:
        """사용자 선호도를 조회합니다."""
        return self.user_preferences.get(user_id, {
            'total_feedback': 0,
            'avg_satisfaction': 0.0,
            'preferred_expressions': [],
        })
    
    def recommend_response_style(self, user_id: str) -> str:
        """
        사용자에게 맞는 응답 스타일을 추천합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            str: 추천 스타일 설명
        """
        pref = self.get_user_preference(user_id)
        
        if pref['avg_satisfaction'] > 4.5:
            return 'warm'  # 따뜻한 톤 선호
        elif pref['avg_satisfaction'] > 3.5:
            return 'balanced'  # 균형잡힌 톤
        else:
            return 'serious'  # 진지한 톤


class EmpathyResponderSystem:
    """통합 공감 응답 시스템"""
    
    def __init__(self):
        """시스템 초기화"""
        self.tone_adjuster = ToneAdjuster()
        self.expression_generator = ExpressionGenerator()
        self.diversification = DiversificationEngine()
        self.preference_tracker = UserPreferenceTracker()
    
    def generate_response(self, emotion: str, intensity: float, user_id: str = None) -> Dict:
        """
        사용자 감정에 맞는 공감 응답을 생성합니다.
        
        Args:
            emotion: 감정
            intensity: 강도
            user_id: 사용자 ID
            
        Returns:
            Dict: 생성된 응답 정보
        """
        # 1. 톤 조정
        tone = self.tone_adjuster.adjust_tone(emotion, intensity, user_id)
        
        # 2. 표현 생성
        main_response = self.expression_generator.generate_main_response(emotion, intensity)
        follow_up = self.expression_generator.generate_follow_up(emotion)
        complete_response = f"{main_response} {follow_up}"
        
        # 3. 다양화
        final_response = self.diversification.diversify(complete_response, user_id)
        
        # 4. 톤 특징 적용
        tone_chars = self.tone_adjuster.get_tone_characteristics(tone)
        
        # 선택적 이모지 추가
        if tone_chars['emojis'] and random.random() < 0.6:
            emoji = random.choice(tone_chars['emojis'])
            final_response = f"{final_response} {emoji}"
        
        result = {
            'emotion': emotion,
            'intensity': intensity,
            'tone': tone,
            'main_response': main_response,
            'follow_up': follow_up,
            'complete_response': complete_response,
            'final_response': final_response,
            'user_id': user_id or 'anonymous',
            'timestamp': datetime.now().isoformat(),
        }
        
        return result
    
    def get_user_report(self, user_id: str) -> Dict:
        """사용자 선호도 리포트 생성"""
        pref = self.preference_tracker.get_user_preference(user_id)
        style = self.preference_tracker.recommend_response_style(user_id)
        tone_pref = self.tone_adjuster.user_tone_preferences.get(user_id, 'default')
        
        report = {
            'user_id': user_id,
            'preference': pref,
            'recommended_style': style,
            'tone_preference': tone_pref,
            'response_frequency': self.diversification.get_response_frequency(user_id),
        }
        
        return report


# ============================================================================
# 테스트 코드
# ============================================================================

if __name__ == '__main__':
    print('=' * 80)
    print('🧠 L2 변연계: 공감 응답 생성 모듈 테스트')
    print('=' * 80)
    
    system = EmpathyResponderSystem()
    
    # 테스트 케이스
    test_cases = [
        ('happy', 0.85, 'user1'),
        ('sad', 0.80, 'user1'),
        ('angry', 1.00, 'user2'),
        ('fear', 0.65, 'user2'),
        ('surprise', 0.70, 'user3'),
        ('neutral', 0.50, 'user3'),
    ]
    
    print('\n📝 공감 응답 생성:\n')
    
    for emotion, intensity, user_id in test_cases:
        result = system.generate_response(emotion, intensity, user_id)
        
        print(f'감정: {result["emotion"]} (강도: {result["intensity"]})')
        print(f'톤: {result["tone"]}')
        print(f'응답: {result["final_response"]}')
        print('-' * 80)
    
    # 피드백 기록
    print('\n📊 사용자 피드백 기록:\n')
    
    # user1 피드백
    system.preference_tracker.record_feedback('user1', '당신의 감정이 충분히 타당합니다. 어떻게 도와드릴 수 있을까요?', 5)
    system.preference_tracker.record_feedback('user1', '정말 좋은 일이 생기셨네요! 좀 더 이야기해 주시겠어요?', 4)
    
    # user2 피드백
    system.preference_tracker.record_feedback('user2', '상황을 이해합니다. 어떻게 도와드릴 수 있을까요?', 4)
    system.preference_tracker.record_feedback('user2', '그런 불안감은 충분히 이해합니다. 당신이 걱정하는 것에 대해 이야기해 줄래요?', 5)
    
    # 사용자별 리포트
    print('\n📈 사용자 선호도 리포트:\n')
    for user_id in ['user1', 'user2', 'user3']:
        report = system.get_user_report(user_id)
        print(f'사용자: {user_id}')
        print(f'평균 만족도: {report["preference"].get("avg_satisfaction", 0):.2f}/5')
        print(f'추천 스타일: {report["recommended_style"]}')
        print(f'총 피드백: {report["preference"].get("total_feedback", 0)}건')
        print('-' * 80)
    
    print('\n✅ 공감 응답 생성 모듈 테스트 완료!')
    print('=' * 80)
