"""
🧠 Hippocampus: 해마 (Memory Indexing & Consolidation)
- 역할: 작업 기억(WM)을 장기 지식(LTM)으로 전이 및 색인
- 학술 근거: Frankland & Bontempi (2005) 기억 공고화 연구
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Pinecone & Embeddings
try:
    from pinecone import Pinecone
    import openai
    import google.generativeai as genai
    PINECONE_AVAILABLE = True
except ImportError as e:
    PINECONE_AVAILABLE = False
    logging.warning(f"⚠️ VectorDB dependency missing: {e}")

logger = logging.getLogger(__name__)

class Hippocampus:
    """
    해마 모델: 단기 기억의 중요 정보를 색인화하고 장기 기억(신피질)으로 전송
    """
    
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = vault_path or os.path.expanduser("~/Library/CloudStorage/OneDrive-개인/Obsidian/SHawn")
        
        # API Keys (from environment)
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.jina_api_key = os.getenv("JINA_API_KEY")
        
        # Pinecone 초기화
        self.index = None
        if self.pinecone_api_key:
            try:
                # global scope에서 Pinecone이 정의되었는지 확인
                if 'Pinecone' in globals():
                    pc = Pinecone(api_key=self.pinecone_api_key)
                    self.index = pc.Index("papers") 
                    logger.info("🌲 Pinecone Index 'papers' connected via Hippocampus")
                else:
                    logger.warning("⚠️ Pinecone library not installed. Skipping.")
            except Exception as e:
                logger.warning(f"⚠️ Pinecone connection failed: {e}")

        # Embedding Clients Setup
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except: pass
            
        if os.getenv("GEMINI_API_KEY"):
            try:
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                self.gemini_available = True
            except: self.gemini_available = False

        # 메타데이터 로드 (로컬 캐시)
        self.meta_path = os.path.expanduser("~/.openclaw/workspace/obsidian_metadata.json")
        self.obsidian_meta = self._load_json(self.meta_path)

    async def _get_embedding(self, text: str) -> List[float]:
        """
        임베딩 생성 (Fallback Chain: OpenAI -> Gemini)
        """
        # 1. Primary: OpenAI (text-embedding-3-small)
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            except Exception as e:
                logger.warning(f"⚠️ OpenAI Embedding failed: {e}")
        
        # 2. Secondary: Gemini (text-embedding-004)
        if getattr(self, 'gemini_available', False):
            try:
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_query"
                )
                return result['embedding']
            except Exception as e:
                logger.warning(f"⚠️ Gemini Embedding failed: {e}")
                
        return []

    def _load_json(self, path: str) -> Dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"total_files": 0, "folders": {}}

    async def search(self, query: str, top_k: int = 3) -> str:
        """
        통합 기억 검색 (해마 색인 호출)
        1. Obsidian 메타데이터 기반 로컬 폴더 추천
        2. Pinecone 기반 의미론적 조각 검색 (활성화 시)
        """
        results = []
        
        # 1. Obsidian Context (PARA 구조 기반 추천)
        # 단순 키워드 매칭 (나중에 더 고도화 가능)
        for folder in ["10-Projects", "50-Lab"]:
            if folder in str(self.obsidian_meta.get("folders", {})):
                results.append(f"📁 관련 로컬 저장소: {folder}")
                break
        
        # 2. Pinecone Semantic Search (실제 벡터 검색)
        if self.index:
             try:
                 query_vector = await self._get_embedding(query)
                 if query_vector:
                     matches = self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
                     for match in matches['matches']:
                         score = match['score']
                         if score > 0.75: # 임계값
                             meta = match['metadata']
                             results.append(f"🧠 기억 조각 ({score:.2f}): {meta.get('text', 'No text')[:200]}...")
             except Exception as e:
                 logger.error(f"⚠️ Pinecone search error: {e}")
        
        return "\n".join(results) if results else ""

    async def consolidate(self, working_memory_traces: List[Any]):
        """
        기억 공고화 (Consolidation)
        중요도가 높은 작업 기억(WorkingMemory)을 영구 저장소로 이전 시도
        """
        # 중요도(importance) > 0.8 인 흔적들 필터링
        important_traces = [t for t in working_memory_traces if getattr(t, 'emotional_weight', 0.5) > 0.8]
        
        if not important_traces:
            return

        logger.info(f"🧬 Consolidating {len(important_traces)} important traces to long-term memory...")
        
        for trace in important_traces:
            # 1. Obsidian 'Daily Logs' 또는 'Consolidated' 폴더에 기록 가능 (추후 구현)
            # 2. Pinecone에 벡터로 인덱싱하여 영구화 (추후 구현)
            pass

    def health_check(self) -> Dict:
        return {
            "status": "operational",
            "pinecone": self.index is not None,
            "obsidian_vault": os.path.exists(self.vault_path),
            "layers": 3
        }
