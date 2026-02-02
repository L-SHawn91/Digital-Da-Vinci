"""
🎯 Intent Classifier - 사용자 의도 분류기

핵심 기능:
- 이모지 → 카트리지 매핑
- 숫자 선택 → 이전 선택지 해석
- 맥락 참조 질문 감지 ("근거는?", "왜?")

Author: Dr. SHawn (Digital Da Vinci Project)
Version: 1.0.0
"""

import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class IntentType(Enum):
    """의도 유형"""
    CARTRIDGE_SWITCH = "cartridge_switch"    # 카트리지 전환
    NUMERIC_CHOICE = "numeric_choice"         # 숫자 선택
    CONTEXT_FOLLOW_UP = "context_follow_up"   # 맥락 참조 질문
    GREETING = "greeting"                     # 인사
    IDENTITY_QUERY = "identity_query"         # "나는 누구야" 등
    SYSTEM_QUERY = "system_query"             # 시스템 관련 질문
    GENERAL = "general"                       # 일반 질문


@dataclass
class IntentResult:
    """의도 분류 결과"""
    intent_type: IntentType
    target: Optional[str]           # 타겟 (카트리지명, 선택번호 등)
    confidence: float               # 신뢰도 (0.0 ~ 1.0)
    raw_input: str                  # 원본 입력
    metadata: Dict[str, Any] = None # 추가 메타데이터
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class IntentClassifier:
    """
    사용자 입력 의도 분류기
    
    사용법:
        classifier = IntentClassifier()
        result = classifier.classify("🧬 바이오 분석")
        # result.intent_type == IntentType.CARTRIDGE_SWITCH
        # result.target == "bio"
    """
    
    # =========================================================
    # 이모지 → 카트리지 매핑
    # =========================================================
    EMOJI_CARTRIDGE_MAP = {
        "🧬": "bio",
        "🔬": "bio",
        "📈": "inv",
        "💹": "inv",
        "📊": "quant",
        "📚": "lit",
        "📖": "lit",
        "🌌": "astro",
        "🔭": "astro",
        "⚙️": "system",
        "🛠️": "system",
        "🧠": "dcns",
    }
    
    # =========================================================
    # 패턴 정의
    # =========================================================
    
    # 숫자 패턴 (1, 2번, 3. 등)
    NUMERIC_PATTERNS = [
        re.compile(r'^(\d+)$'),              # 순수 숫자
        re.compile(r'^(\d+)번$'),            # X번
        re.compile(r'^(\d+)\.$'),            # X.
        re.compile(r'^(\d+)\)$'),            # X)
    ]
    
    # 맥락 참조 패턴
    CONTEXT_REF_PATTERNS = [
        (re.compile(r'근거.*[?？]?', re.IGNORECASE), "evidence"),      # "근거는?"
        (re.compile(r'왜[요\s]*[?？]?', re.IGNORECASE), "why"),        # "왜?", "왜요?"
        (re.compile(r'어떻게.*[?？]?', re.IGNORECASE), "how"),         # "어떻게?"
        (re.compile(r'더\s*자세히', re.IGNORECASE), "detail"),         # "더 자세히"
        (re.compile(r'계속', re.IGNORECASE), "continue"),              # "계속"
        (re.compile(r'예시|예를\s*들', re.IGNORECASE), "example"),     # "예시", "예를 들어"
    ]
    
    # 인사 패턴
    GREETING_PATTERNS = [
        re.compile(r'^(안녕|하이|헬로|hi|hello|hey)[\s!]*$', re.IGNORECASE),
        re.compile(r'^(반가워|반갑습니다)[\s!]*$', re.IGNORECASE),
    ]
    
    # 정체성 질문 패턴
    IDENTITY_PATTERNS = [
        re.compile(r'(나|내가|저|제가)\s*(는|은)?\s*누구', re.IGNORECASE),   # "나는 누구야"
        re.compile(r'(너|네가|당신)\s*(는|은)?\s*누구', re.IGNORECASE),      # "너는 누구야"
        re.compile(r'(나|저)\s*를?\s*알아', re.IGNORECASE),                 # "나를 알아?"
        re.compile(r'Dr\.?\s*SHawn', re.IGNORECASE),                       # Dr.SHawn 언급
    ]
    
    # 시스템 관련 패턴
    SYSTEM_PATTERNS = [
        re.compile(r'(리소스|메모리|CPU|상태|버전)', re.IGNORECASE),
        re.compile(r'(업데이트|업그레이드)', re.IGNORECASE),
        re.compile(r'(설정|config)', re.IGNORECASE),
    ]
    
    def __init__(self):
        logger.info("🎯 IntentClassifier initialized")
    
    def classify(
        self, 
        text: str, 
        intent_history: List[dict] = None,
        user_profile: dict = None
    ) -> IntentResult:
        """
        입력 텍스트 의도 분류
        
        Args:
            text: 사용자 입력
            intent_history: 이전 의도 히스토리 (숫자 선택 해석용)
            user_profile: 사용자 프로필 (관리자 여부 등)
            
        Returns:
            IntentResult
        """
        text = text.strip()
        
        if not text:
            return IntentResult(
                intent_type=IntentType.GENERAL,
                target=None,
                confidence=0.0,
                raw_input=text
            )
        
        # 1. 이모지 카트리지 전환 확인
        result = self._check_cartridge_switch(text)
        if result:
            return result
        
        # 2. 숫자 선택 확인
        result = self._check_numeric_choice(text, intent_history)
        if result:
            return result
        
        # 3. 인사 확인
        result = self._check_greeting(text)
        if result:
            return result
        
        # 4. 정체성 질문 확인
        result = self._check_identity_query(text, user_profile)
        if result:
            return result
        
        # 5. 맥락 참조 질문 확인
        result = self._check_context_follow_up(text)
        if result:
            return result
        
        # 6. 시스템 관련 질문 확인
        result = self._check_system_query(text)
        if result:
            return result
        
        # 7. 일반 질문
        return IntentResult(
            intent_type=IntentType.GENERAL,
            target=None,
            confidence=0.5,
            raw_input=text
        )
    
    def _check_cartridge_switch(self, text: str) -> Optional[IntentResult]:
        """이모지 카트리지 전환 확인"""
        for emoji, cartridge in self.EMOJI_CARTRIDGE_MAP.items():
            if text.startswith(emoji):
                # 이모지 뒤의 텍스트 추출
                remaining_text = text[len(emoji):].strip()
                
                return IntentResult(
                    intent_type=IntentType.CARTRIDGE_SWITCH,
                    target=cartridge,
                    confidence=0.95,
                    raw_input=text,
                    metadata={"remaining_text": remaining_text}
                )
        return None
    
    def _check_numeric_choice(
        self, 
        text: str, 
        intent_history: List[dict] = None
    ) -> Optional[IntentResult]:
        """숫자 선택 확인"""
        for pattern in self.NUMERIC_PATTERNS:
            match = pattern.match(text)
            if match:
                number = int(match.group(1))
                
                # 이전 선택지에서 해당 번호 해석 시도
                resolved = None
                if intent_history:
                    resolved = self._resolve_from_history(number, intent_history)
                
                return IntentResult(
                    intent_type=IntentType.NUMERIC_CHOICE,
                    target=resolved or str(number),
                    confidence=0.9 if resolved else 0.7,
                    raw_input=text,
                    metadata={
                        "number": number,
                        "resolved": resolved is not None
                    }
                )
        return None
    
    def _check_greeting(self, text: str) -> Optional[IntentResult]:
        """인사 확인"""
        for pattern in self.GREETING_PATTERNS:
            if pattern.match(text):
                return IntentResult(
                    intent_type=IntentType.GREETING,
                    target=None,
                    confidence=0.9,
                    raw_input=text
                )
        return None
    
    def _check_identity_query(
        self, 
        text: str, 
        user_profile: dict = None
    ) -> Optional[IntentResult]:
        """정체성 질문 확인"""
        for pattern in self.IDENTITY_PATTERNS:
            if pattern.search(text):
                query_type = "user_identity" if "나" in text or "저" in text else "bot_identity"
                
                return IntentResult(
                    intent_type=IntentType.IDENTITY_QUERY,
                    target=query_type,
                    confidence=0.9,
                    raw_input=text,
                    metadata={"user_profile": user_profile}
                )
        return None
    
    def _check_context_follow_up(self, text: str) -> Optional[IntentResult]:
        """맥락 참조 질문 확인"""
        for pattern, follow_up_type in self.CONTEXT_REF_PATTERNS:
            if pattern.search(text):
                return IntentResult(
                    intent_type=IntentType.CONTEXT_FOLLOW_UP,
                    target=follow_up_type,
                    confidence=0.85,
                    raw_input=text
                )
        return None
    
    def _check_system_query(self, text: str) -> Optional[IntentResult]:
        """시스템 관련 질문 확인"""
        for pattern in self.SYSTEM_PATTERNS:
            if pattern.search(text):
                return IntentResult(
                    intent_type=IntentType.SYSTEM_QUERY,
                    target="system",
                    confidence=0.8,
                    raw_input=text
                )
        return None
    
    def _resolve_from_history(
        self, 
        number: int, 
        history: List[dict]
    ) -> Optional[str]:
        """이전 선택지에서 번호 해석"""
        if not history:
            return None
        
        # 가장 최근 의도에서 options 찾기
        for intent in reversed(history):
            options = intent.get("options", [])
            if options and 0 < number <= len(options):
                return options[number - 1]
        
        return None


# =========================================================
# Singleton Instance
# =========================================================

_classifier_instance = None

def get_intent_classifier() -> IntentClassifier:
    """IntentClassifier 싱글톤 인스턴스 반환"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier()
    return _classifier_instance
