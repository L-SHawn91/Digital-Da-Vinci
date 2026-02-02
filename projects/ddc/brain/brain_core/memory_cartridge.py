"""
🧠 Memory Cartridge System
- 핵심 필수 카트리지: 사용자 인식 및 기억 관리
- 카트리지 교체 = 사용자 전환
- 백엔드 스토리지 추상화 (Provider 패턴)

Author: Dr. SHawn (Digital Da Vinci Project)
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ============================================================
# 1. Memory Provider Interface (백엔드 스토리지 추상화)
# ============================================================

class MemoryProvider(ABC):
    """
    메모리 저장소 추상 인터페이스
    - Pinecone, Obsidian, OneDrive, LocalJSON 등 교체 가능
    - 모든 Provider는 이 인터페이스를 구현해야 함
    """
    
    @abstractmethod
    async def save(self, key: str, value: Dict[str, Any], metadata: dict = None) -> bool:
        """데이터 저장"""
        pass
    
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """유사도 검색"""
        pass
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """키로 직접 조회"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """삭제"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[str]:
        """모든 키 목록 반환"""
        pass


# ============================================================
# 2. User Profile DataClass
# ============================================================

@dataclass
class UserProfile:
    """사용자 프로필 정보"""
    user_id: str
    user_name: str
    is_admin: bool
    preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "is_admin": self.is_admin,
            "preferences": self.preferences,
            "created_at": self.created_at
        }


# ============================================================
# 3. Memory Cartridge Interface (사용자 인식 + 기억)
# ============================================================

class MemoryCartridge(ABC):
    """
    메모리 카트리지 추상 클래스 - 사용자별 기억 공간
    
    핵심 개념:
    - 카트리지 교체 = 사용자 전환
    - 각 카트리지는 독립된 기억 공간 보유
    - Provider를 통해 백엔드 스토리지에 저장
    """
    
    def __init__(self, provider: MemoryProvider):
        self.provider = provider
        self._profile: Optional[UserProfile] = None
        self._intent_history: List[dict] = []
        self._conversation_buffer: List[dict] = []
        self._max_buffer_size = 20  # 최근 대화 버퍼 크기
    
    @property
    @abstractmethod
    def profile(self) -> UserProfile:
        """사용자 프로필 반환 (서브클래스에서 구현)"""
        pass
    
    # =========================================================
    # 대화 컨텍스트 관리
    # =========================================================
    
    def add_message(self, role: str, content: str, importance: float = 0.5):
        """
        대화 기록 추가
        
        Args:
            role: 발화자 ("user" 또는 "assistant")
            content: 메시지 내용
            importance: 중요도 (0.0 ~ 1.0)
        """
        self._conversation_buffer.append({
            "role": role,
            "content": content,
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        })
        
        # 버퍼 크기 제한
        if len(self._conversation_buffer) > self._max_buffer_size:
            self._conversation_buffer = self._conversation_buffer[-self._max_buffer_size:]
        
        logger.debug(f"💬 Message added: [{role}] {content[:50]}...")
    
    def get_conversation_context(self, n: int = 5) -> str:
        """
        최근 n개 대화 컨텍스트 반환
        
        Args:
            n: 가져올 대화 수
            
        Returns:
            포맷된 대화 컨텍스트 문자열
        """
        recent = self._conversation_buffer[-n:] if self._conversation_buffer else []
        if not recent:
            return ""
        
        lines = ["[Recent Conversation]"]
        for m in recent:
            role_label = "User" if m["role"] == "user" else "Assistant"
            lines.append(f"- {role_label}: {m['content'][:100]}...")
        
        return "\n".join(lines)
    
    def get_last_assistant_response(self) -> Optional[str]:
        """마지막 어시스턴트 응답 반환 (맥락 참조용)"""
        for m in reversed(self._conversation_buffer):
            if m["role"] == "assistant":
                return m["content"]
        return None
    
    # =========================================================
    # 의도 히스토리 관리 (숫자 선택 추적)
    # =========================================================
    
    def record_intent(self, intent_type: str, options: List[str] = None):
        """
        선택지 제시 시 기록
        
        Args:
            intent_type: 의도 유형 (예: "menu_selection", "clarification")
            options: 제시된 선택지 리스트
        """
        self._intent_history.append({
            "type": intent_type,
            "options": options or [],
            "timestamp": datetime.now().isoformat()
        })
        
        # 히스토리 크기 제한 (최근 10개)
        if len(self._intent_history) > 10:
            self._intent_history = self._intent_history[-10:]
        
        logger.debug(f"📝 Intent recorded: {intent_type} with {len(options or [])} options")
    
    def resolve_numeric_choice(self, number: int) -> Optional[str]:
        """
        숫자 입력 시 이전 선택지 참조
        
        Args:
            number: 선택된 번호 (1-indexed)
            
        Returns:
            해당 선택지 텍스트 또는 None
        """
        if not self._intent_history:
            return None
        
        last_intent = self._intent_history[-1]
        options = last_intent.get("options", [])
        
        if options and 0 < number <= len(options):
            selected = options[number - 1]
            logger.info(f"✅ Numeric choice resolved: {number} → '{selected}'")
            return selected
        
        return None
    
    def get_last_options(self) -> List[str]:
        """마지막으로 제시된 선택지 리스트 반환"""
        if not self._intent_history:
            return []
        return self._intent_history[-1].get("options", [])
    
    # =========================================================
    # 장기 기억 (Provider 위임)
    # =========================================================
    
    async def store_memory(self, key: str, content: str, metadata: dict = None):
        """
        장기 기억 저장
        
        Args:
            key: 저장 키
            content: 저장할 내용
            metadata: 메타데이터
        """
        await self.provider.save(
            key, 
            {"content": content, "user_id": self.profile.user_id}, 
            metadata
        )
        logger.info(f"💾 Memory stored: {key}")
    
    async def recall(self, query: str, top_k: int = 5) -> List[str]:
        """
        기억 검색
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 최대 결과 수
            
        Returns:
            검색된 내용 리스트
        """
        results = await self.provider.search(query, top_k)
        return [r.get("content", "") for r in results if r.get("content")]
    
    # =========================================================
    # 세션 컨텍스트 생성 (프롬프트 주입용)
    # =========================================================
    
    def get_session_context(self) -> str:
        """
        세션 컨텍스트 문자열 생성 (프롬프트 주입용)
        
        Returns:
            시스템 프롬프트에 주입할 세션 정보
        """
        p = self.profile
        
        # 최근 선택지가 있으면 포함
        last_options = self.get_last_options()
        options_context = ""
        if last_options:
            options_str = "\n".join([f"  {i+1}. {opt}" for i, opt in enumerate(last_options)])
            options_context = f"\n[Last Offered Options]\n{options_str}"
        
        return f"""[Session Info]
- 사용자: {p.user_name}
- 권한: {'관리자 (Admin)' if p.is_admin else '일반 사용자'}
- 세션 ID: {p.user_id}{options_context}
"""
    
    def clear_session(self):
        """세션 데이터 초기화"""
        self._conversation_buffer.clear()
        self._intent_history.clear()
        logger.info(f"🧹 Session cleared for {self.profile.user_id}")
    
    async def save(self):
        """대화 버퍼를 Provider에 저장 (영속화)"""
        if not self._conversation_buffer:
            return
        
        key = f"session_{self.profile.user_id}"
        value = {
            "user_id": self.profile.user_id,
            "conversation_buffer": self._conversation_buffer,
            "intent_history": self._intent_history,
            "last_updated": datetime.now().isoformat()
        }
        
        success = await self.provider.save(key, value)
        if success:
            logger.debug(f"💾 Session saved for {self.profile.user_id}")
        return success


# ============================================================
# 4. Concrete Implementations
# ============================================================

class SHawnMemoryCartridge(MemoryCartridge):
    """
    Dr. SHawn 전용 메모리 카트리지 (관리자 모드)
    
    특징:
    - 관리자 권한
    - 연구 도메인 선호도 설정
    - What-Why-How 응답 스타일
    """
    
    @property
    def profile(self) -> UserProfile:
        if not self._profile:
            self._profile = UserProfile(
                user_id="dr_shawn",
                user_name="Dr. SHawn (이수형 박사)",
                is_admin=True,
                preferences={
                    "response_style": "what-why-how",
                    "domain_focus": ["bio", "organoid", "stem_cell", "endometrium"],
                    "language": "ko",
                    "detail_level": "high"
                },
                created_at="2026-01-01T00:00:00"
            )
        return self._profile


class GuestMemoryCartridge(MemoryCartridge):
    """
    일반 사용자 메모리 카트리지
    
    특징:
    - 제한된 권한
    - 세션 기반 임시 기억
    """
    
    def __init__(self, provider: MemoryProvider, guest_id: str, guest_name: str = "Guest"):
        super().__init__(provider)
        self._guest_id = guest_id
        self._guest_name = guest_name
    
    @property
    def profile(self) -> UserProfile:
        if not self._profile:
            self._profile = UserProfile(
                user_id=self._guest_id,
                user_name=self._guest_name,
                is_admin=False,
                preferences={
                    "response_style": "concise",
                    "language": "ko"
                }
            )
        return self._profile


# ============================================================
# 5. Cartridge Factory (편의 함수)
# ============================================================

class MemoryCartridgeFactory:
    """메모리 카트리지 팩토리"""
    
    _cartridges: Dict[str, MemoryCartridge] = {}
    
    @classmethod
    def get_or_create(
        cls, 
        user_id: str, 
        provider: MemoryProvider,
        is_admin: bool = False,
        user_name: str = None
    ) -> MemoryCartridge:
        """
        카트리지 조회 또는 생성
        
        Args:
            user_id: 사용자 ID
            provider: 메모리 프로바이더
            is_admin: 관리자 여부
            user_name: 사용자 이름 (Guest용)
            
        Returns:
            해당 사용자의 MemoryCartridge
        """
        cache_key = f"{user_id}_{id(provider)}"
        
        if cache_key not in cls._cartridges:
            if is_admin:
                cls._cartridges[cache_key] = SHawnMemoryCartridge(provider)
            else:
                cls._cartridges[cache_key] = GuestMemoryCartridge(
                    provider, 
                    user_id, 
                    user_name or f"User_{user_id[-4:]}"
                )
            logger.info(f"🎰 New cartridge created: {cache_key}")
        
        return cls._cartridges[cache_key]
    
    @classmethod
    def clear_cache(cls):
        """캐시 초기화"""
        cls._cartridges.clear()
        logger.info("🧹 Cartridge cache cleared")
