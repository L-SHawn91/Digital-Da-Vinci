#!/usr/bin/env python3
"""
emotion_analyzer.py - L2 변연계: 감정 분석 모듈 (Week 4, Step 1)

사용자 메시지에서 감정을 인식하고 분석합니다.
기본 감정 6가지 + 혼합 감정 지원
강도 측정 (0-1 신뢰도) + 맥락 분석 + 감정 이력 추적
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib


@dataclass
class Emotion:
    """감정 데이터 클래스"""
    primary: str  # 주 감정 (happy, sad, angry, neutral, fear, surprise)
    secondary: Optional[str] = None  # 부 감정
    intensity: float = 0.5  # 강도 (0-1)
    confidence: float = 0.7  # 신뢰도 (0-1)
    keywords: List[str] = None  # 감정 키워드
    timestamp: str = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class EmotionDetector:
    """감정 인식 엔진"""
    
    # 기본 감정 6가지와 키워드
    EMOTION_KEYWORDS = {
        'happy': [
            '행복', '좋아', '최고', '완벽', '멋진', '아름다워', '즐거워',
            '신나', '신나다', '기뻐', '기쁜', '운이좋게', '좋다', '좋네',
            'great', 'happy', 'awesome', 'love', 'wonderful', 'amazing',
            'excellent', 'fantastic', 'beautiful', 'perfect', 'brilliant',
            '😊', '😄', '😍', '🎉', '✨'
        ],
        'sad': [
            '슬픔', '슬프', '우울', '우울해', '힘들어', '괴로워', '외로워',
            '혼자', '절망', '절망적', '형편없어', '나빠', '안된다', '안돼',
            'sad', 'depressed', 'lonely', 'hopeless', 'terrible', 'awful',
            'crying', 'upset', 'miserable', 'heartbroken', '😢', '😭', '💔'
        ],
        'angry': [
            '화나', '화났어', '짜증', '짜증나', '분노', '분개', '성남',
            '열받아', '열받다', '욕먹어', '욕했어', '싫어', '싫다',
            'angry', 'furious', 'rage', 'irritated', 'annoyed', 'upset',
            'frustrated', 'furious', '😠', '😡', '🤬'
        ],
        'fear': [
            '두려워', '두렵', '무서워', '무섭', '불안해', '불안', '걱정',
            '공포', '공포감', '놀래', '놀랬어', '깜짝', '깜짝놀라',
            'afraid', 'scared', 'fearful', 'anxious', 'worried', 'terrified',
            'panic', 'nervous', '😨', '😰', '😱'
        ],
        'surprise': [
            '놀라', '놀랐어', '깜짝', '어?', '어!!', '와!!', '오!!',
            '예상', '예상밖', '뜻밖', '정말?', '진짜?', '설마?',
            'surprised', 'amazed', 'shocked', 'wow', 'unexpected',
            '😲', '😮', '🤯'
        ],
        'neutral': [
            '그래', '알겠어', '네', '예', '맞아', '맞는데', '그렇지',
            '음...', '흠...', '일반적으로', '보통', '보편적', '일상적',
            'okay', 'fine', 'alright', 'neutral', 'normal',
            '😐', '😑', '🤷'
        ]
    }
    
    # 강도 수정자 (텍스트에서 감정 강도 높이는 표현들)
    INTENSITY_MODIFIERS = {
        'very': 0.15,      # "매우", "정말"
        'really': 0.15,    # "진짜"
        'so': 0.15,        # "너무"
        'extremely': 0.2,  # "극도로"
        'absolutely': 0.2, # "완전히"
        'totally': 0.15,   # "완전"
        '!!!': 0.1,        # 느낌표 3개
        '!!': 0.05,        # 느낌표 2개
        '매우': 0.15,
        '정말': 0.15,
        '진짜': 0.15,
        '너무': 0.15,
        '극도로': 0.2,
        '완전히': 0.15,
        '완전': 0.1,
        '반복': 0.1,  # 글자 반복 (예: "싫싫싫")
    }
    
    def __init__(self):
        """감정 감지기 초기화"""
        self.emotion_scores = defaultdict(float)
        self.total_detections = 0
        
    def detect(self, text: str) -> Emotion:
        """
        메시지에서 감정을 감지합니다.
        
        Args:
            text: 사용자 메시지
            
        Returns:
            Emotion: 감지된 감정 데이터
        """
        text_lower = text.lower()
        
        # 각 감정별 점수 계산
        emotion_scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = self._calculate_emotion_score(text_lower, emotion, keywords)
            emotion_scores[emotion] = score
        
        # 주 감정 선택
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        primary_score = emotion_scores[primary_emotion]
        
        # 부 감정 선택 (2번째로 높은 점수)
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        secondary_emotion = sorted_emotions[1][0] if len(sorted_emotions) > 1 else None
        secondary_score = sorted_emotions[1][1] if len(sorted_emotions) > 1 else 0
        
        # 신뢰도 계산
        max_score = max(emotion_scores.values())
        confidence = min(1.0, max(0.5, max_score / 100))
        
        # 강도 계산
        intensity = self._calculate_intensity(text, primary_emotion)
        
        # 키워드 추출
        keywords = self._extract_keywords(text_lower, primary_emotion)
        
        # 부 감정이 너무 약하면 None 처리
        if secondary_score < primary_score * 0.3:
            secondary_emotion = None
        
        emotion = Emotion(
            primary=primary_emotion,
            secondary=secondary_emotion,
            intensity=intensity,
            confidence=confidence,
            keywords=keywords
        )
        
        self.emotion_scores[primary_emotion] += 1
        self.total_detections += 1
        
        return emotion
    
    def _calculate_emotion_score(self, text: str, emotion: str, keywords: List[str]) -> float:
        """감정별 점수 계산"""
        score = 0.0
        
        for keyword in keywords:
            # 정확한 단어 매칭
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = len(re.findall(pattern, text))
            
            if matches > 0:
                # 기본 점수
                base_score = 20.0 * matches
                
                # 강도 수정자 적용
                intensity_boost = self._get_intensity_boost(text)
                score += base_score * (1 + intensity_boost)
        
        return score
    
    def _get_intensity_boost(self, text: str) -> float:
        """강도 부스트 계산"""
        boost = 0.0
        
        # 강도 수정자 확인
        for modifier, value in self.INTENSITY_MODIFIERS.items():
            if modifier in text:
                boost += value
        
        # 대문자 비율 확인 (ALL CAPS는 감정이 강함)
        if len(text) > 3:
            uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
            if uppercase_ratio > 0.5:
                boost += 0.2
        
        # 느낌표 개수 확인
        exclamation_count = text.count('!')
        boost += min(0.2, exclamation_count * 0.05)
        
        return min(1.0, boost)  # 최대 100% 부스트
    
    def _calculate_intensity(self, text: str, emotion: str) -> float:
        """감정 강도 (0-1) 계산"""
        base_intensity = 0.5
        
        # 강도 수정자에 따른 조정
        intensity_boost = self._get_intensity_boost(text)
        
        final_intensity = min(1.0, base_intensity + intensity_boost)
        return round(final_intensity, 2)
    
    def _extract_keywords(self, text: str, emotion: str) -> List[str]:
        """감정 관련 키워드 추출"""
        keywords = []
        emotion_keywords = self.EMOTION_KEYWORDS[emotion]
        
        for keyword in emotion_keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text):
                keywords.append(keyword)
        
        return keywords[:5]  # 최대 5개


class IntensityScorer:
    """감정 강도 측정 엔진"""
    
    def __init__(self):
        """강도 스코어러 초기화"""
        self.intensity_history = []
    
    def score(self, emotion: Emotion, context: str = None) -> Dict:
        """
        감정의 강도를 점수화합니다.
        
        Args:
            emotion: Emotion 객체
            context: 맥락 정보 (선택사항)
            
        Returns:
            Dict: 강도 점수 정보
        """
        result = {
            'intensity': emotion.intensity,
            'confidence': emotion.confidence,
            'combined_score': emotion.intensity * emotion.confidence,
            'level': self._get_intensity_level(emotion.intensity),
            'context': context
        }
        
        self.intensity_history.append(result)
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
    
    def get_average_intensity(self) -> float:
        """평균 강도 계산"""
        if not self.intensity_history:
            return 0.5
        
        total = sum(h['combined_score'] for h in self.intensity_history)
        return total / len(self.intensity_history)


class ContextAnalyzer:
    """맥락 분석 엔진"""
    
    def __init__(self):
        """맥락 분석기 초기화"""
        self.context_history = []
        self.user_profile = {}
    
    def analyze(self, text: str, emotion: Emotion, user_id: str = None) -> Dict:
        """
        메시지의 맥락을 분석합니다.
        
        Args:
            text: 원본 메시지
            emotion: 감지된 감정
            user_id: 사용자 ID
            
        Returns:
            Dict: 맥락 분석 결과
        """
        context = {
            'user_id': user_id or 'anonymous',
            'text_length': len(text),
            'sentence_count': len(text.split('.')),
            'question_count': text.count('?'),
            'exclamation_count': text.count('!'),
            'mention_count': text.count('@'),
            'emotion': emotion.primary,
            'is_question': text.strip().endswith('?'),
            'is_urgent': text.count('!') > 2 or text.count('?') > 2,
            'emoji_count': self._count_emojis(text),
            'sentiment_category': self._categorize_sentiment(text, emotion),
        }
        
        self.context_history.append(context)
        return context
    
    def _count_emojis(self, text: str) -> int:
        """이모지 개수 세기"""
        emoji_pattern = r'[\U0001F300-\U0001F9FF]'
        return len(re.findall(emoji_pattern, text))
    
    def _categorize_sentiment(self, text: str, emotion: Emotion) -> str:
        """감정 카테고리화"""
        if emotion.primary in ['happy', 'surprise']:
            return 'positive'
        elif emotion.primary in ['sad', 'fear', 'angry']:
            return 'negative'
        else:
            return 'neutral'
    
    def get_user_profile(self, user_id: str) -> Dict:
        """사용자 프로필 조회"""
        user_contexts = [c for c in self.context_history if c['user_id'] == user_id]
        
        if not user_contexts:
            return {'user_id': user_id, 'message_count': 0}
        
        emotions = [c['emotion'] for c in user_contexts]
        primary_emotion = max(set(emotions), key=emotions.count)
        
        profile = {
            'user_id': user_id,
            'message_count': len(user_contexts),
            'primary_emotion': primary_emotion,
            'emotion_distribution': dict([(e, emotions.count(e)) for e in set(emotions)]),
            'avg_text_length': sum(c['text_length'] for c in user_contexts) / len(user_contexts),
            'question_tendency': sum(1 for c in user_contexts if c['is_question']) / len(user_contexts),
        }
        
        return profile


class EmotionTracker:
    """감정 이력 추적 엔진"""
    
    def __init__(self, max_history: int = 1000):
        """감정 추적기 초기화"""
        self.history = []
        self.max_history = max_history
        self.emotion_timeline = defaultdict(list)
    
    def track(self, emotion: Emotion, user_id: str, message_hash: str = None) -> None:
        """
        감정을 이력에 추가합니다.
        
        Args:
            emotion: Emotion 객체
            user_id: 사용자 ID
            message_hash: 메시지 해시 (중복 방지용)
        """
        if message_hash is None:
            message_hash = 'unknown'
        
        record = {
            'user_id': user_id,
            'emotion': emotion.primary,
            'secondary_emotion': emotion.secondary,
            'intensity': emotion.intensity,
            'confidence': emotion.confidence,
            'keywords': emotion.keywords,
            'timestamp': emotion.timestamp,
            'message_hash': message_hash,
        }
        
        self.history.append(record)
        self.emotion_timeline[user_id].append(record)
        
        # 최대 이력 크기 유지
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_emotion_trend(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        사용자의 감정 추세를 조회합니다.
        
        Args:
            user_id: 사용자 ID
            limit: 조회 제한 개수
            
        Returns:
            List[Dict]: 감정 이력
        """
        user_history = self.emotion_timeline.get(user_id, [])
        return user_history[-limit:]
    
    def get_emotion_stats(self, user_id: str) -> Dict:
        """
        사용자의 감정 통계를 조회합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            Dict: 감정 통계
        """
        user_history = self.emotion_timeline.get(user_id, [])
        
        if not user_history:
            return {'user_id': user_id, 'total_messages': 0}
        
        emotions = [record['emotion'] for record in user_history]
        intensities = [record['intensity'] for record in user_history]
        confidences = [record['confidence'] for record in user_history]
        
        stats = {
            'user_id': user_id,
            'total_messages': len(user_history),
            'primary_emotion': max(set(emotions), key=emotions.count),
            'emotion_distribution': dict([(e, emotions.count(e)) for e in set(emotions)]),
            'avg_intensity': round(sum(intensities) / len(intensities), 2),
            'avg_confidence': round(sum(confidences) / len(confidences), 2),
            'most_intense_emotion': max(emotions, key=lambda e: intensities[emotions.index(e)]),
        }
        
        return stats
    
    def export_history(self, user_id: str = None) -> str:
        """
        감정 이력을 JSON으로 내보냅니다.
        
        Args:
            user_id: 사용자 ID (None이면 전체)
            
        Returns:
            str: JSON 문자열
        """
        if user_id:
            data = self.emotion_timeline.get(user_id, [])
        else:
            data = self.history
        
        return json.dumps(data, indent=2, ensure_ascii=False)


class EmotionAnalyzerSystem:
    """통합 감정 분석 시스템"""
    
    def __init__(self):
        """시스템 초기화"""
        self.detector = EmotionDetector()
        self.intensity_scorer = IntensityScorer()
        self.context_analyzer = ContextAnalyzer()
        self.tracker = EmotionTracker()
    
    def analyze_message(self, text: str, user_id: str = 'default') -> Dict:
        """
        메시지를 종합적으로 분석합니다.
        
        Args:
            text: 사용자 메시지
            user_id: 사용자 ID
            
        Returns:
            Dict: 종합 분석 결과
        """
        # 1. 감정 감지
        emotion = self.detector.detect(text)
        
        # 2. 강도 측정
        intensity_score = self.intensity_scorer.score(emotion)
        
        # 3. 맥락 분석
        context = self.context_analyzer.analyze(text, emotion, user_id)
        
        # 4. 이력 추적
        message_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        self.tracker.track(emotion, user_id, message_hash)
        
        # 5. 종합 결과
        result = {
            'message': text[:100] + ('...' if len(text) > 100 else ''),
            'user_id': user_id,
            'emotion': {
                'primary': emotion.primary,
                'secondary': emotion.secondary,
                'intensity': emotion.intensity,
                'confidence': emotion.confidence,
                'keywords': emotion.keywords,
            },
            'intensity_score': intensity_score,
            'context': context,
            'timestamp': emotion.timestamp,
            'message_hash': message_hash,
        }
        
        return result
    
    def get_user_emotion_report(self, user_id: str) -> Dict:
        """사용자 감정 리포트 생성"""
        profile = self.context_analyzer.get_user_profile(user_id)
        stats = self.tracker.get_emotion_stats(user_id)
        trend = self.tracker.get_emotion_trend(user_id)
        
        report = {
            'user_id': user_id,
            'profile': profile,
            'statistics': stats,
            'recent_trend': trend[-5:],  # 최근 5개
            'generated_at': datetime.now().isoformat(),
        }
        
        return report


# ============================================================================
# 테스트 코드
# ============================================================================

if __name__ == '__main__':
    print('=' * 80)
    print('🧠 L2 변연계: 감정 분석 모듈 테스트')
    print('=' * 80)
    
    system = EmotionAnalyzerSystem()
    
    # 테스트 메시지들
    test_messages = [
        ('오늘 정말 행복해! 모든 게 완벽해!!', 'user1'),
        ('요즘 정말 힘들어... 너무 우울해', 'user1'),
        ('화났어!!! 정말 짜증난다!!!', 'user2'),
        ('정말 두렵고 불안해', 'user2'),
        ('오, 정말 예상 밖이네! 깜짝 놀랐어', 'user3'),
        ('네, 알겠습니다. 진행하겠습니다.', 'user3'),
    ]
    
    print('\n📊 감정 분석 결과:\n')
    
    for message, user_id in test_messages:
        result = system.analyze_message(message, user_id)
        
        print(f'메시지: "{message}"')
        print(f'사용자: {user_id}')
        print(f'감정: {result["emotion"]["primary"]} (부감정: {result["emotion"]["secondary"]})')
        print(f'강도: {result["emotion"]["intensity"]:.2f} / 신뢰도: {result["emotion"]["confidence"]:.2f}')
        print(f'키워드: {", ".join(result["emotion"]["keywords"])}')
        print(f'맥락: {result["context"]["sentiment_category"]} | 긴급: {result["context"]["is_urgent"]}')
        print('-' * 80)
    
    # 사용자별 리포트
    print('\n📈 사용자 감정 리포트:\n')
    for user_id in ['user1', 'user2', 'user3']:
        report = system.get_user_emotion_report(user_id)
        print(f'사용자: {user_id}')
        print(f'메시지 수: {report["statistics"]["total_messages"]}')
        print(f'주 감정: {report["statistics"]["primary_emotion"]}')
        print(f'감정 분포: {report["statistics"]["emotion_distribution"]}')
        print(f'평균 강도: {report["statistics"]["avg_intensity"]}')
        print('-' * 80)
    
    print('\n✅ 감정 분석 모듈 테스트 완료!')
    print('=' * 80)
