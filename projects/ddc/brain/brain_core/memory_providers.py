"""
🔌 Pluggable Memory Providers
- Pinecone, Obsidian, OneDrive, LocalJSON 등 교체 가능
- 모든 Provider는 MemoryProvider 인터페이스를 구현

Author: Dr. SHawn (Digital Da Vinci Project)
Version: 1.0.0
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False

from .memory_cartridge import MemoryProvider

logger = logging.getLogger(__name__)


# ============================================================
# 1. LocalJsonProvider (개발/테스트용)
# ============================================================

class LocalJsonProvider(MemoryProvider):
    """
    로컬 JSON 파일 기반 Provider
    
    용도: 개발 및 테스트 환경
    특징: 
    - 외부 의존성 없음
    - 파일 시스템 기반 저장
    - 단순 키워드 매칭 검색
    """
    
    def __init__(self, storage_path: str = "./memory_store"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 LocalJsonProvider initialized: {self.storage_path}")
    
    async def save(self, key: str, value: Dict[str, Any], metadata: dict = None) -> bool:
        """데이터 저장"""
        filepath = self.storage_path / f"{self._sanitize_key(key)}.json"
        data = {
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        
        try:
            if AIOFILES_AVAILABLE:
                async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"💾 Saved: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
            return False
    
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """단순 키워드 매칭 검색 (실제로는 벡터 검색 권장)"""
        results = []
        query_lower = query.lower()
        
        try:
            for filepath in self.storage_path.glob("*.json"):
                try:
                    if AIOFILES_AVAILABLE:
                        async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                            content = await f.read()
                    else:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    data = json.loads(content)
                    
                    # 단순 키워드 매칭
                    if query_lower in str(data.get("value", {})).lower():
                        results.append(data["value"])
                        
                        if len(results) >= top_k:
                            break
                            
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
        
        logger.debug(f"🔍 Search '{query}': {len(results)} results")
        return results
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """키로 직접 조회"""
        filepath = self.storage_path / f"{self._sanitize_key(key)}.json"
        
        if not filepath.exists():
            return None
        
        try:
            if AIOFILES_AVAILABLE:
                async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                    content = await f.read()
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            data = json.loads(content)
            return data.get("value")
            
        except Exception as e:
            logger.error(f"❌ Get failed: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """삭제"""
        filepath = self.storage_path / f"{self._sanitize_key(key)}.json"
        
        if filepath.exists():
            try:
                filepath.unlink()
                logger.debug(f"🗑️ Deleted: {key}")
                return True
            except Exception as e:
                logger.error(f"❌ Delete failed: {e}")
                return False
        return False
    
    async def list_all(self) -> List[str]:
        """모든 키 목록 반환"""
        keys = []
        for filepath in self.storage_path.glob("*.json"):
            keys.append(filepath.stem)
        return keys
    
    def _sanitize_key(self, key: str) -> str:
        """파일명에 사용 가능하도록 키 정제"""
        # 특수문자 제거/치환
        sanitized = key.replace("/", "_").replace("\\", "_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c in "_-.")
        return sanitized[:100]  # 길이 제한


# ============================================================
# 2. PineconeProvider (벡터 검색용)
# ============================================================

class PineconeProvider(MemoryProvider):
    """
    Pinecone 벡터 DB Provider
    
    용도: 프로덕션 환경의 시맨틱 검색
    특징:
    - 벡터 기반 유사도 검색
    - 대규모 데이터 처리
    - 임베딩 모델 연동 필요
    """
    
    def __init__(self, api_key: str = None, index_name: str = "shawn-memory"):
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.index_name = index_name
        self._index = None
        self._initialized = False
        
        if self.api_key:
            self._initialize()
    
    def _initialize(self):
        """Pinecone 클라이언트 초기화"""
        try:
            from pinecone import Pinecone
            
            pc = Pinecone(api_key=self.api_key)
            self._index = pc.Index(self.index_name)
            self._initialized = True
            logger.info(f"🌲 PineconeProvider initialized: {self.index_name}")
            
        except ImportError:
            logger.warning("⚠️ Pinecone not installed. Run: pip install pinecone-client")
        except Exception as e:
            logger.error(f"❌ Pinecone init failed: {e}")
    
    async def save(self, key: str, value: Dict[str, Any], metadata: dict = None) -> bool:
        """벡터 저장 (임베딩 필요)"""
        if not self._initialized:
            logger.warning("⚠️ Pinecone not initialized")
            return False
        
        # TODO: 임베딩 생성 및 upsert
        # embedding = await self._get_embedding(value.get("content", ""))
        # self._index.upsert([(key, embedding, {**value, **(metadata or {})})])
        
        raise NotImplementedError("Pinecone save() 구현 예정 - 임베딩 모델 연동 필요")
    
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """벡터 유사도 검색"""
        if not self._initialized:
            return []
        
        # TODO: 쿼리 임베딩 생성 및 검색
        # query_embedding = await self._get_embedding(query)
        # results = self._index.query(vector=query_embedding, top_k=top_k)
        
        raise NotImplementedError("Pinecone search() 구현 예정")
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """ID로 직접 조회"""
        if not self._initialized:
            return None
        
        try:
            result = self._index.fetch([key])
            if key in result.vectors:
                return result.vectors[key].metadata
        except Exception as e:
            logger.error(f"❌ Pinecone get failed: {e}")
        
        return None
    
    async def delete(self, key: str) -> bool:
        """삭제"""
        if not self._initialized:
            return False
        
        try:
            self._index.delete(ids=[key])
            return True
        except Exception as e:
            logger.error(f"❌ Pinecone delete failed: {e}")
            return False
    
    async def list_all(self) -> List[str]:
        """전체 목록 (Pinecone에서는 비효율적)"""
        logger.warning("⚠️ list_all() is not efficient for Pinecone")
        return []


# ============================================================
# 3. ObsidianProvider (마크다운 노트)
# ============================================================

class ObsidianProvider(MemoryProvider):
    """
    Obsidian Vault (Markdown) Provider
    
    용도: 연구 노트 및 문서 기반 기억
    특징:
    - 마크다운 파일 기반
    - 양방향 링크 지원
    - 기존 Hippocampus 로직 활용
    """
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or os.getenv("OBSIDIAN_VAULT_PATH", ""))
        
        if not self.vault_path.exists():
            logger.warning(f"⚠️ Obsidian vault not found: {self.vault_path}")
    
    async def save(self, key: str, value: Dict[str, Any], metadata: dict = None) -> bool:
        """마크다운 노트 생성"""
        if not self.vault_path.exists():
            return False
        
        content = value.get("content", "")
        filepath = self.vault_path / f"{self._sanitize_filename(key)}.md"
        
        # YAML frontmatter 생성
        frontmatter = f"""---
created: {datetime.now().isoformat()}
tags: [shawn-memory]
"""
        if metadata:
            for k, v in metadata.items():
                frontmatter += f"{k}: {v}\n"
        frontmatter += "---\n\n"
        
        full_content = frontmatter + content
        
        try:
            filepath.write_text(full_content, encoding='utf-8')
            logger.debug(f"📝 Obsidian note saved: {filepath.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Obsidian save failed: {e}")
            return False
    
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """마크다운 파일 내용 검색"""
        if not self.vault_path.exists():
            return []
        
        results = []
        query_lower = query.lower()
        
        try:
            for filepath in self.vault_path.rglob("*.md"):
                try:
                    content = filepath.read_text(encoding='utf-8')
                    if query_lower in content.lower():
                        results.append({
                            "content": content,
                            "path": str(filepath),
                            "title": filepath.stem
                        })
                        
                        if len(results) >= top_k:
                            break
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Obsidian search failed: {e}")
        
        return results
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """노트 직접 조회"""
        if not self.vault_path.exists():
            return None
        
        filepath = self.vault_path / f"{self._sanitize_filename(key)}.md"
        
        if filepath.exists():
            return {"content": filepath.read_text(encoding='utf-8')}
        
        return None
    
    async def delete(self, key: str) -> bool:
        """노트 삭제"""
        if not self.vault_path.exists():
            return False
        
        filepath = self.vault_path / f"{self._sanitize_filename(key)}.md"
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    async def list_all(self) -> List[str]:
        """모든 노트 목록"""
        if not self.vault_path.exists():
            return []
        
        return [f.stem for f in self.vault_path.rglob("*.md")]
    
    def _sanitize_filename(self, name: str) -> str:
        """파일명 정제"""
        sanitized = name.replace("/", "_").replace("\\", "_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c in "_- ")
        return sanitized[:100]


# ============================================================
# 4. Provider Factory
# ============================================================

class MemoryProviderFactory:
    """메모리 프로바이더 팩토리"""
    
    @staticmethod
    def create(provider_type: str, **kwargs) -> MemoryProvider:
        """
        프로바이더 생성
        
        Args:
            provider_type: "local", "pinecone", "obsidian"
            **kwargs: 프로바이더별 설정
            
        Returns:
            MemoryProvider 인스턴스
        """
        providers = {
            "local": LocalJsonProvider,
            "pinecone": PineconeProvider,
            "obsidian": ObsidianProvider
        }
        
        if provider_type not in providers:
            raise ValueError(f"Unknown provider: {provider_type}. Available: {list(providers.keys())}")
        
        return providers[provider_type](**kwargs)
    
    @staticmethod
    def get_default() -> MemoryProvider:
        """기본 프로바이더 반환 (LocalJson)"""
        return LocalJsonProvider("./memory_store")
