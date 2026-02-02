"""
🧠 WorkingMemory: 전두엽 (Prefrontal Cortex) 기반 작업 기억 모듈
- 학술 근거: Baddeley & Hitch (1974) 작업 기억 모델
- 기능: George Miller (1956) 'Magic Number 7±2' 준수 (7개 청크 제한)
- 관리: 사용자별 독립 데이터 격리
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import deque
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class MemoryTrace:
    """단일 기억 흔적 (Memory Trace)"""
    role: str  # user / assistant
    content: str
    timestamp: str
    emotional_weight: float = 0.5  # Amygdala 가중치 (기본값)
    importance: float = 0.5
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

class WorkingMemory:
    """
    전두엽 (Prefrontal Cortex) 기반 작업 기억
    실시간 대화의 맥락을 짧은 시간 동안 유지
    """
    
    def __init__(self, user_id: str, capacity: int = 7):
        """
        Args:
            user_id: 사용자 고유 식별자
            capacity: 유지할 대화 쌍(Turn)의 수 (Miller's Law)
        """
        self.user_id = user_id
        self.capacity = capacity
        # 저장 경로: ~/.openclaw/memory/{user_id}/working_memory.json
        self.storage_dir = os.path.expanduser(f"~/.openclaw/memory/{user_id}")
        self.storage_path = os.path.join(self.storage_dir, "working_memory.json")
        
        # deque를 사용하여 자동 용량 관리 (user+assistant 쌍이므로 capacity * 2)
        self.traces: deque = deque(maxlen=self.capacity * 2)
        
        self._load_memory()
        logger.info(f"🧠 WorkingMemory initialized for User {user_id} (Capacity: {capacity})")

    def _load_memory(self):
        """저장된 작업 기억 로드"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for trace_dict in data:
                        self.traces.append(MemoryTrace.from_dict(trace_dict))
                logger.debug(f"💾 Loaded {len(self.traces)} memory traces for User {self.user_id}")
            except Exception as e:
                logger.error(f"❌ Failed to load working memory: {e}")

    def _save_memory(self):
        """작업 기억 영구 저장"""
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            data = [asdict(t) for t in self.traces]
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ Failed to save working memory: {e}")

    def add_trace(self, role: str, content: str, emotional_weight: float = 0.5):
        """기억 흔적 추가"""
        trace = MemoryTrace(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            emotional_weight=emotional_weight
        )
        self.traces.append(trace)
        self._save_memory()
        logger.debug(f"➕ Trace added to WorkingMemory: {role}")

    def get_context(self) -> str:
        """프롬프트 주입용 텍스트 컨텍스트 생성"""
        if not self.traces:
            return ""
        
        context_lines = []
        for trace in self.traces:
            role_map = {"user": "User", "assistant": "Assistant"}
            context_lines.append(f"{role_map.get(trace.role, trace.role)}: {trace.content}")
        
        return "\n".join(context_lines)

    def clear(self):
        """메모리 초기화"""
        self.traces.clear()
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
        logger.info(f"🧹 WorkingMemory cleared for User {self.user_id}")

if __name__ == "__main__":
    # 간단한 테스트
    logging.basicConfig(level=logging.INFO)
    wm = WorkingMemory("test_user_123")
    wm.add_trace("user", "안녕하세요, 숀브레인!")
    wm.add_trace("assistant", "반갑습니다! 무엇을 도와드릴까요?")
    print(f"Current Context:\n{wm.get_context()}")
