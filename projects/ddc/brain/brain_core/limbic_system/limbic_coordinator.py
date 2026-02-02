"""
🧠 LimbicCoordinator: 변연계 조정자
- 역할: WorkingMemory, Amygdala, Hippocampus, NeocorticalStore 통합 조정
- 특징: 비동기 병렬 처리를 통한 속도 최적화
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from projects.ddc.brain.brain_core.limbic_system.working_memory import WorkingMemory
from projects.ddc.brain.brain_core.limbic_system.hippocampus import Hippocampus
from projects.ddc.brain.brain_core.limbic_system.amygdala import Amygdala

logger = logging.getLogger(__name__)

class LimbicCoordinator:
    """
    변연계의 기억과 감정 신호를 통합하여 자아(ChatEngine)에게 전달하는 코디네이터
    """
    
    def __init__(self, user_id: str, is_admin: bool = False):
        self.user_id = user_id
        self.is_admin = is_admin
        
        # 1. 작업 기억 (전두엽)
        self.working_memory = WorkingMemory(user_id)
        
        # 2. 감정/중요도 (편도체)
        self.amygdala = Amygdala() 
        
        # 3. 해마 (색인 및 공고화)
        self.hippocampus = Hippocampus()
        self.neocortical_store = None # Pinecone Wrapper (Future)

    async def build_integrated_context(self, query: str, level: str = "L3") -> str:
        """
        3계층 기억을 병렬로 조회하여 통합 프롬프트 컨텍스트 생성
        """
        tasks = []
        sections = []
        
        # 1. 단기 기억 (항상 필수)
        # WorkingMemory는 이미 로컬 로딩되어 있음
        short_term_ctx = self.working_memory.get_context()
        
        # 2. 중/장기 기억 (L3 이상이거나 분석 질문일 때만)
        if level in ["L3", "L4"] and self.is_admin:
            tasks.append(self.hippocampus.search(query))
            # tasks.append(self.neocortical_store.search(query)) # Future

        # 병렬 조회 (최대 대기 시간 최적화)
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, str) and res:
                    sections.append(f"### [Knowledge Retrieval]\n{res}")

        # 컨텍스트 통합
        if short_term_ctx:
            sections.insert(0, f"### [Recent Conversation]\n{short_term_ctx}")
            
        # (향후 추가될 섹션들)
        # if mid_term_ctx: sections.append(f"### [Active Projects]\n{mid_term_ctx}")
        # if long_term_ctx: sections.append(f"### [Knowledge RAG]\n{long_term_ctx}")
        
        final_context = "\n\n".join(sections)
        
        if final_context:
            logger.info(f"🧠 Limbic context built for User {self.user_id} (Length: {len(final_context)})")
            
        return final_context

    def record_interaction(self, role: str, content: str, importance: float = 0.5):
        """상호작용을 기억에 기록"""
        self.working_memory.add_trace(role, content, emotional_weight=importance)
        
    async def _fetch_mid_term_context(self, query: str) -> str:
        """해마(Obsidian)에서 중기 맥락 조회"""
        # TODO: Implement Phase 3/4
        return ""

    async def _fetch_long_term_context(self, query: str) -> str:
        """신피질(Pinecone)에서 장기 지식 조회"""
        # TODO: Implement Phase 4/5
        return ""
