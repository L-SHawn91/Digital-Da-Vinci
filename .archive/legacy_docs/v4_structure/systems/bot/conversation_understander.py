#!/usr/bin/env python3
"""
conversation_understander.py - L3 신피질: 일반 대화 이해 모듈

현재 문제: 키워드만 인식 → 자연스러운 대화 이해 못함
해결: NLP 기반 의도 분석 + 맥락 인식 + 개체명 추출
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ConversationIntent:
    """대화 의도"""
    intent_type: str  # greeting, question, statement, request, sentiment
    confidence: float  # 0-1
    entities: Dict  # 개체명 (person, place, time, object)
    keywords: List[str]
    context_score: float  # 맥락 연관도


class IntentClassifier:
    """의도 분류 엔진"""
    
    # 의도별 패턴
    INTENT_PATTERNS = {
        'greeting': {
            'keywords': ['안녕', '반가워', '만나서', '인사', 'hello', 'hi', '오랜만'],
            'patterns': [
                r'(안녕|안녕하|반가워|만나|인사)',
                r'(hello|hi|hey|greetings)',
            ],
            'priority': 1,
        },
        'farewell': {
            'keywords': ['안녕', '바이', '나중에', '헤어져', '종료', 'bye', 'goodbye'],
            'patterns': [
                r'(안녕|바이|나중에|헤어져|종료)',
                r'(bye|goodbye|see you)',
            ],
            'priority': 1,
        },
        'question': {
            'keywords': ['뭐', '어떻게', '왜', '언제', '어디', '누가', '무엇', '?'],
            'patterns': [
                r'[?？]',  # 물음표
                r'\b(뭐|어떻게|왜|언제|어디|누가|무엇|뭔가)\b',
                r'(what|how|why|when|where|who|which)',
            ],
            'priority': 5,
        },
        'request': {
            'keywords': ['해줘', '해주세요', '부탁', '도와줘', '필요', 'help', 'please'],
            'patterns': [
                r'(해줘|해주세요|부탁|도와줘|필요)',
                r'(help|please|can you|could you)',
            ],
            'priority': 4,
        },
        'statement': {
            'keywords': ['생각', '느낌', '말이야', '그래', '맞아', '사실', 'think', 'feel'],
            'patterns': [
                r'(생각|느낌|말이야|그래|맞아|사실)',
                r'(think|feel|believe|mean)',
            ],
            'priority': 3,
        },
        'problem': {
            'keywords': ['문제', '에러', '버그', '안됨', '깨짐', 'error', 'bug', 'issue'],
            'patterns': [
                r'(문제|에러|버그|안됨|깨짐|고장)',
                r'(error|bug|issue|problem|not working)',
            ],
            'priority': 7,
        },
        'thanks': {
            'keywords': ['감사', '고마워', '고맙', 'thanks', 'thank', 'appreciate'],
            'patterns': [
                r'(감사|고마워|고맙)',
                r'(thanks|thank|appreciate)',
            ],
            'priority': 1,
        },
        'agreement': {
            'keywords': ['네', '맞아', '그래', '알겠어', '좋아', 'yes', 'sure', 'ok'],
            'patterns': [
                r'(네|맞아|그래|알겠어|좋아|예)',
                r'(yes|sure|ok|okay|alright)',
            ],
            'priority': 2,
        },
        'disagreement': {
            'keywords': ['아니', '싫어', '안돼', '거부', 'no', 'nope', 'refuse'],
            'patterns': [
                r'(아니|싫어|안돼|거부)',
                r'(no|nope|refuse|disagree)',
            ],
            'priority': 2,
        },
    }
    
    def __init__(self):
        """의도 분류기 초기화"""
        self.classification_history = []
        self.user_intent_profile = defaultdict(lambda: defaultdict(int))
    
    def classify(self, text: str, user_id: str = None) -> ConversationIntent:
        """
        메시지의 의도를 분류합니다.
        
        Args:
            text: 사용자 메시지
            user_id: 사용자 ID
            
        Returns:
            ConversationIntent: 분류된 의도
        """
        text_lower = text.lower()
        
        # 각 의도별 점수 계산
        intent_scores = {}
        
        for intent_type, intent_info in self.INTENT_PATTERNS.items():
            score = 0.0
            matched_keywords = []
            
            # 패턴 매칭
            for pattern in intent_info['patterns']:
                matches = re.findall(pattern, text_lower)
                if matches:
                    score += len(matches) * 0.3
                    matched_keywords.extend(matches)
            
            # 키워드 매칭
            for keyword in intent_info['keywords']:
                if keyword in text_lower:
                    score += 0.2
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
            
            # 우선순위 적용
            score *= (1 + intent_info['priority'] * 0.1)
            
            intent_scores[intent_type] = {
                'score': score,
                'keywords': matched_keywords[:5],
            }
        
        # 최고 점수 의도 선택
        best_intent = max(intent_scores, key=lambda x: intent_scores[x]['score'])
        best_score_info = intent_scores[best_intent]
        
        # 신뢰도 계산 (0.5-1.0 범위)
        max_possible_score = max(s['score'] for s in intent_scores.values()) + 1
        confidence = min(1.0, max(0.5, best_score_info['score'] / max_possible_score))
        
        # 개체명 추출
        entities = self._extract_entities(text)
        
        # 맥락 점수 (사용자 이전 의도와의 관련도)
        context_score = self._calculate_context_score(best_intent, user_id)
        
        intent = ConversationIntent(
            intent_type=best_intent,
            confidence=round(confidence, 2),
            entities=entities,
            keywords=best_score_info['keywords'],
            context_score=context_score,
        )
        
        self.classification_history.append({
            'intent': best_intent,
            'confidence': confidence,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
        })
        
        if user_id:
            self.user_intent_profile[user_id][best_intent] += 1
        
        return intent
    
    def _extract_entities(self, text: str) -> Dict:
        """개체명을 추출합니다."""
        entities = {
            'time': [],
            'person': [],
            'place': [],
            'object': [],
        }
        
        # 시간 표현
        time_patterns = [
            r'(오늘|내일|어제|지금|곧)',
            r'(\d+시간?|\d+분|오전|오후)',
            r'(월요|화요|수요|목요|금요|토요|일요)',
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, text)
            if matches:
                entities['time'].extend(matches)
        
        # 대문자로 시작하는 단어 (인명, 지명 가능성)
        caps_words = re.findall(r'\b[A-Z][a-z]+', text)
        if caps_words:
            # 간단한 휴리스틱: 첫 글자 대문자는 인명/지명 가능성
            entities['person'].extend(caps_words[:2])
        
        return entities
    
    def _calculate_context_score(self, current_intent: str, user_id: str = None) -> float:
        """맥락 점수를 계산합니다."""
        if not user_id or user_id not in self.user_intent_profile:
            return 0.5
        
        user_profile = self.user_intent_profile[user_id]
        total_intents = sum(user_profile.values())
        
        if total_intents == 0:
            return 0.5
        
        # 사용자가 자주 사용하는 의도와의 관련도
        intent_frequency = user_profile.get(current_intent, 0) / total_intents
        
        return round(0.5 + (intent_frequency * 0.5), 2)


class ContextMemory:
    """대화 맥락 메모리"""
    
    def __init__(self, max_history: int = 50):
        """맥락 메모리 초기화"""
        self.conversation_history = []
        self.max_history = max_history
        self.user_contexts = defaultdict(list)
    
    def add_turn(self, user_id: str, user_message: str, intent: ConversationIntent, 
                 bot_response: str = None) -> None:
        """
        대화 턴을 메모리에 추가합니다.
        
        Args:
            user_id: 사용자 ID
            user_message: 사용자 메시지
            intent: 의도
            bot_response: 봇 응답 (선택사항)
        """
        turn = {
            'user_id': user_id,
            'user_message': user_message[:100],  # 처음 100자만
            'intent': intent.intent_type,
            'confidence': intent.confidence,
            'entities': intent.entities,
            'bot_response': bot_response[:100] if bot_response else None,
            'timestamp': datetime.now().isoformat(),
        }
        
        self.conversation_history.append(turn)
        self.user_contexts[user_id].append(turn)
        
        # 크기 관리
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_user_context(self, user_id: str, limit: int = 5) -> List[Dict]:
        """사용자의 최근 대화 맥락을 조회합니다."""
        return self.user_contexts[user_id][-limit:]
    
    def get_conversation_flow(self, user_id: str) -> str:
        """사용자의 대화 흐름을 텍스트로 반환합니다."""
        user_turns = self.user_contexts[user_id][-5:]
        
        flow = []
        for turn in user_turns:
            flow.append(f"사용자 [{turn['intent']}]: {turn['user_message']}")
            if turn['bot_response']:
                flow.append(f"봇: {turn['bot_response']}")
        
        return '\n'.join(flow)


class SemanticSimilarity:
    """의미론적 유사도 계산"""
    
    def __init__(self):
        """의미론적 유사도 계산기 초기화"""
        # 유사 단어 그룹
        self.semantic_groups = {
            'greeting': ['안녕', '반가워', '만나서', '인사', '처음', 'hello', 'hi'],
            'help': ['도와줘', '해줘', '부탁', '필요', '도움', 'help', 'assist'],
            'problem': ['문제', '에러', '버그', '안됨', '고장', 'error', 'bug'],
            'positive': ['좋아', '최고', '멋진', '좋은', 'great', 'good', 'awesome'],
            'negative': ['싫어', '안좋아', '형편없어', 'bad', 'terrible', 'awful'],
        }
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        두 텍스트 간의 의미론적 유사도를 계산합니다.
        
        Args:
            text1: 첫 번째 텍스트
            text2: 두 번째 텍스트
            
        Returns:
            float: 유사도 (0-1)
        """
        # 간단한 구현: 공통 단어 비율
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_similar_intent(self, text: str, intent_type: str) -> float:
        """
        텍스트가 특정 의도와 얼마나 유사한지 계산합니다.
        
        Args:
            text: 텍스트
            intent_type: 의도 타입
            
        Returns:
            float: 유사도 (0-1)
        """
        if intent_type not in self.semantic_groups:
            return 0.0
        
        group_words = self.semantic_groups[intent_type]
        text_lower = text.lower()
        
        matched = sum(1 for word in group_words if word in text_lower)
        
        return min(1.0, matched / len(group_words))


class ConversationUnderstander:
    """통합 대화 이해 시스템"""
    
    def __init__(self):
        """시스템 초기화"""
        self.intent_classifier = IntentClassifier()
        self.context_memory = ContextMemory()
        self.semantic_similarity = SemanticSimilarity()
        self.response_map = self._init_response_map()
    
    def _init_response_map(self) -> Dict[str, str]:
        """의도별 응답 맵 초기화"""
        return {
            'greeting': '안녕하세요! 만나서 반갑습니다.',
            'farewell': '안녕히 가세요! 나중에 또 만나요.',
            'question': '좋은 질문이네요. 더 자세히 설명해주실 수 있을까요?',
            'request': '그렇게 해드리겠습니다!',
            'statement': '그렇군요. 더 알고 싶으신 게 있으신가요?',
            'problem': '문제가 생기셨군요. 어떻게 해결해드릴까요?',
            'thanks': '감사합니다! 도움이 되었으면 좋겠습니다.',
            'agreement': '네, 알겠습니다. 계속 진행하겠습니다.',
            'disagreement': '이해합니다. 다른 방법이 있을까요?',
        }
    
    def understand_message(self, text: str, user_id: str = None) -> Dict:
        """
        메시지를 종합적으로 이해합니다.
        
        Args:
            text: 사용자 메시지
            user_id: 사용자 ID
            
        Returns:
            Dict: 이해 결과
        """
        # 1. 의도 분류
        intent = self.intent_classifier.classify(text, user_id)
        
        # 2. 맥락 조회
        recent_context = self.context_memory.get_user_context(user_id, limit=3) if user_id else []
        
        # 3. 의미론적 유사도 계산
        semantic_score = self.semantic_similarity.find_similar_intent(text, intent.intent_type)
        
        # 4. 응답 선택
        base_response = self.response_map.get(intent.intent_type, '네, 이해했습니다.')
        
        # 5. 맥락 메모리에 추가
        self.context_memory.add_turn(user_id or 'anonymous', text, intent, base_response)
        
        result = {
            'message': text[:80] + ('...' if len(text) > 80 else ''),
            'intent': {
                'type': intent.intent_type,
                'confidence': intent.confidence,
                'keywords': intent.keywords,
            },
            'entities': intent.entities,
            'semantic_score': round(semantic_score, 2),
            'context_score': intent.context_score,
            'recent_context': len(recent_context),
            'response': base_response,
            'timestamp': datetime.now().isoformat(),
        }
        
        return result
    
    def get_user_profile(self, user_id: str) -> Dict:
        """사용자 대화 프로필을 조회합니다."""
        user_intents = self.intent_classifier.user_intent_profile.get(user_id, {})
        total = sum(user_intents.values())
        
        if total == 0:
            return {'user_id': user_id, 'message_count': 0}
        
        profile = {
            'user_id': user_id,
            'message_count': total,
            'intent_distribution': dict(user_intents),
            'primary_intent': max(user_intents, key=user_intents.get) if user_intents else None,
            'conversation_flow': self.context_memory.get_conversation_flow(user_id),
        }
        
        return profile


# ============================================================================
# 테스트 코드
# ============================================================================

if __name__ == '__main__':
    print('=' * 80)
    print('🧠 L3 신피질: 일반 대화 이해 모듈 테스트')
    print('=' * 80)
    
    understander = ConversationUnderstander()
    
    # 테스트 메시지들
    test_messages = [
        ('안녕하세요! 반갑습니다.', 'user1'),
        ('요즘 숀봇이 일반 대화를 잘 못 이해하는 것 같아요.', 'user1'),
        ('이 문제를 어떻게 해결할 수 있을까요?', 'user1'),
        ('좋은 솔루션 감사합니다!', 'user1'),
        ('네, 그대로 진행해주세요.', 'user1'),
        ('안녕하세요', 'user2'),
        ('심각한 버그가 발생했습니다!', 'user2'),
        ('도와주실 수 있나요?', 'user2'),
    ]
    
    print('\n📝 대화 이해 분석:\n')
    
    for message, user_id in test_messages:
        result = understander.understand_message(message, user_id)
        
        print(f'메시지: "{message}"')
        print(f'사용자: {user_id}')
        print(f'의도: {result["intent"]["type"]} (신뢰도: {result["intent"]["confidence"]})')
        print(f'키워드: {", ".join(result["intent"]["keywords"])}')
        print(f'개체: {result["entities"]}')
        print(f'의미론적 점수: {result["semantic_score"]}')
        print(f'응답: "{result["response"]}"')
        print('-' * 80)
    
    # 사용자별 프로필
    print('\n👤 사용자 대화 프로필:\n')
    for user_id in ['user1', 'user2']:
        profile = understander.get_user_profile(user_id)
        print(f'사용자: {user_id}')
        print(f'메시지 수: {profile["message_count"]}')
        print(f'주 의도: {profile.get("primary_intent", "N/A")}')
        print(f'의도 분포: {profile.get("intent_distribution", {})}')
        print('-' * 80)
    
    print('\n✅ 일반 대화 이해 모듈 테스트 완료!')
    print('=' * 80)
