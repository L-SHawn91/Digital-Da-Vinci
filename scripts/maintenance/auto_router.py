"""
AutoRouter: 신경계 기반 자동 라우팅 시스템
일반 메시지도 신경계가 자동으로 분류 + 모델 선택 + 응답 생성
"""

import asyncio
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AutoRouteConfig:
    """자동 라우팅 설정"""
    task_type: str  # Coding, Research, Speed, Analysis, Creative, General
    model_key: str  # 선택된 모델
    score: float    # 평가 점수
    reason: str     # 선택 이유
    confidence: float  # 확신도 (0-1)


class MessageClassifier:
    """신경계 기반 메시지 분류기"""
    
    # 각 작업별 키워드
    KEYWORDS = {
        "Coding": [
            "코드", "함수", "python", "javascript", "작성", "구현",
            "버그", "debug", "에러", "알고리즘", "헙", "클래스",
            "메서드", "라이브러리", "프레임워크", "react", "django"
        ],
        "Research": [
            "분석", "논문", "연구", "최신", "오가노이드", "세포",
            "실험", "데이터", "통계", "메커니즘", "심화", "학술",
            "이론", "개념", "원리", "구조", "프로세스"
        ],
        "Speed": [
            "빨리", "지금", "급", "즉시", "바로", "빨리빨리",
            "간단히", "요약", "핵심만", "짧게", "한줄로", "빠르게"
        ],
        "Analysis": [
            "뭐야", "뭔지", "설명", "정의", "의미", "개념",
            "차이", "비교", "vs", "어떻게", "왜", "뭐가",
            "설명해", "알려줘", "말해줘"
        ],
        "Creative": [
            "창의", "아이디어", "상상", "새로운", "생각", "아이디어",
            "제안", "어떻게하면", "가능할까", "방법", "전략", "계획",
            "디자인", "컨셉", "비즈니스"
        ],
    }
    
    # 특수 분류 (높은 우선순위)
    SPECIAL_KEYWORDS = {
        "Research/Specialized": ["자궁", "오가노이드", "줄기세포", "분화", "내막"],
        "Coding/Debug": ["버그", "에러", "오류", "fix", "문제"],
        "Speed/Urgent": ["급해", "빨리빨리", "지금당장"],
    }
    
    def classify(self, message: str) -> Tuple[str, float]:
        """
        메시지를 분류하고 확신도 반환
        
        Returns:
            (task_type, confidence)
        """
        message_lower = message.lower()
        
        # 특수 분류 먼저 확인 (높은 우선순위)
        for special_type, keywords in self.SPECIAL_KEYWORDS.items():
            if any(kw in message_lower for kw in keywords):
                return special_type, 0.95
        
        # 일반 분류
        scores = {}
        for task_type, keywords in self.KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in message_lower)
            if matches > 0:
                scores[task_type] = matches / len(keywords)
        
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = min(scores[best_type], 1.0)
            return best_type, confidence
        
        # 기본값
        return "General", 0.5


class ModelSelector:
    """작업별 최적 모델 선택기"""
    
    # 작업별 최적 모델 매핑
    TASK_MODELS = {
        "Coding": ("DeepSeek-Coder", 0.95, "최고 코딩 능력"),
        "Research": ("Claude Opus", 0.98, "심화 분석"),
        "Speed": ("Groq Mixtral", 0.98, "초고속"),
        "Analysis": ("Gemini Pro", 0.94, "포괄적 설명"),
        "Creative": ("Gemini Pro", 0.92, "창의성"),
        "General": ("Copilot Sonnet", 0.90, "균형"),
        
        # 특수 모델
        "Research/Specialized": ("Claude Opus", 0.99, "생물학 전문"),
        "Coding/Debug": ("DeepSeek-Coder", 0.97, "디버깅 최적화"),
        "Speed/Urgent": ("Groq Mixtral", 0.99, "초고속 응답"),
    }
    
    def select(self, task_type: str) -> Tuple[str, float, str]:
        """
        작업 유형에 따른 최적 모델 선택
        
        Returns:
            (model_key, score, reason)
        """
        if task_type in self.TASK_MODELS:
            return self.TASK_MODELS[task_type]
        
        # 기본값
        return self.TASK_MODELS["General"]


class AutoRouter:
    """완전 자동 라우팅 시스템"""
    
    def __init__(self):
        self.classifier = MessageClassifier()
        self.selector = ModelSelector()
        self.user_settings: Dict[str, str] = {}  # 사용자별 설정
    
    def get_user_setting(self, user_id: str) -> str:
        """사용자 설정 조회"""
        return self.user_settings.get(user_id, "auto")
    
    def set_user_setting(self, user_id: str, setting: str) -> bool:
        """사용자 설정 저장"""
        valid_settings = ["auto", "speed", "quality", "balance", "model"]
        if setting in valid_settings:
            self.user_settings[user_id] = setting
            return True
        return False
    
    def route(self, message: str, user_id: str = None) -> AutoRouteConfig:
        """
        메시지를 자동으로 라우팅
        
        Process:
        1. 신경계 분류
        2. 사용자 설정 적용
        3. 모델 선택
        4. 라우팅 결과 반환
        """
        
        # Step 1: 신경계 분류
        task_type, confidence = self.classifier.classify(message)
        
        # Step 2: 사용자 설정 적용 (optional)
        if user_id:
            setting = self.get_user_setting(user_id)
            if setting == "speed":
                task_type = "Speed"
            elif setting == "quality":
                task_type = "Research"
            # "auto"는 기본값 유지
            # "model"은 고정 모델 사용
        
        # Step 3: 모델 선택
        model_key, score, reason = self.selector.select(task_type)
        
        # Step 4: 결과 반환
        return AutoRouteConfig(
            task_type=task_type,
            model_key=model_key,
            score=score,
            reason=reason,
            confidence=confidence
        )
    
    def get_buttons(self, task_type: str) -> List[str]:
        """작업 유형별 스마트 버튼"""
        buttons_map = {
            "Coding": ["[다른 모델로 보기]", "[더 자세히]", "[설명만]"],
            "Research": ["[요약본]", "[더 깊이]", "[논문 링크]"],
            "Speed": ["[자세한 버전]", "[더 많이]", "[설명]"],
            "Analysis": ["[예시 추가]", "[더 깊이]", "[비교]"],
            "Creative": ["[다른 아이디어]", "[더 구체적]", "[실행계획]"],
            "General": ["[/brain 상세]", "[/ensemble 비교]", "[/debate]"],
        }
        return buttons_map.get(task_type, buttons_map["General"])


# ============================================================================
# 테스트 코드
# ============================================================================

if __name__ == "__main__":
    router = AutoRouter()
    
    print("=" * 70)
    print("🟢 AutoRouter: 완전 자동 라우팅 시스템")
    print("=" * 70)
    
    # 테스트 메시지
    test_messages = [
        "파이썬 함수 만들어",
        "양자컴퓨터 논문 분석",
        "지금 바로 답변 줘",
        "이게 뭔지 설명해",
        "창의적인 아이디어 줘",
        "자궁오가노이드 최신 연구",
        "코드 버그 찾아",
        "일반적인 질문입니다",
    ]
    
    print("\n【자동 라우팅 결과】\n")
    
    for message in test_messages:
        config = router.route(message, user_id="user_123")
        
        print(f"📝 질문: {message}")
        print(f"   🧠 분류: {config.task_type} (확신도: {config.confidence:.0%})")
        print(f"   🎯 모델: {config.model_key} (점수: {config.score:.2f})")
        print(f"   💡 이유: {config.reason}")
        print(f"   🔘 버튼: {', '.join(router.get_buttons(config.task_type))}")
        print()
    
    # 사용자 설정 테스트
    print("\n" + "=" * 70)
    print("⚙️ 사용자 설정 테스트")
    print("=" * 70)
    
    router.set_user_setting("user_123", "speed")
    config = router.route("복잡한 분석 질문", user_id="user_123")
    
    print(f"\n사용자 설정: speed")
    print(f"질문: 복잡한 분석 질문")
    print(f"✅ 자동 선택됨: {config.model_key} (대신 Speed 모델 선택)")
    
    print("\n" + "=" * 70)
    print("✅ AutoRouter 구현 완료!")
    print("=" * 70)
