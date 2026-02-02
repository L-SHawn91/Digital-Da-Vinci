"""
🧠 MoltBot Obsidian Memory Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: ~/.openclaw/workspace/obsidian_memory.py

Purpose: Obsidian Vault를 메모리 검색 소스로 활용

Architecture: 옵션 3
- Obsidian의 모든 .md 파일을 메모리 소스로 사용
- 폴더별 가중치 적용
- 캐싱으로 성능 최적화

Author: MoltBot
Date: 2026-01-30
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ObsidianMemory:
    """Obsidian Vault를 메모리로 사용하는 클래스"""
    
    def __init__(self, vault_path: str):
        """
        초기화
        
        Args:
            vault_path: Obsidian Vault 경로
        """
        self.vault_path = Path(vault_path)
        
        # 설정
        self.included_folders = [
            "10-Projects",
            "20-Areas", 
            "30-Concepts",
            "40-Sources",
            "50-Lab",
            "60-Writing"
        ]
        
        self.excluded_folders = {
            ".obsidian", ".smart-env", ".smtcmp_json_db",
            "99-System", "80-Assets", "90-Archive"
        }
        
        self.folder_weights = {
            "10-Projects": 1.5,
            "50-Lab": 1.3,
            "20-Areas": 1.0,
            "40-Sources": 0.9,
            "30-Concepts": 0.8,
            "60-Writing": 0.7
        }
        
        # 캐시
        self.cache_dir = Path.home() / ".openclaw/workspace/.cache/obsidian-index"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = 3600  # 1시간
        
        # 인덱스
        self.file_index = {}
        self._load_cache()
        
        logger.info(f"✅ ObsidianMemory initialized: {vault_path}")
    
    def index_vault(self) -> Dict[str, Any]:
        """
        Obsidian Vault 전체 인덱싱
        
        Returns:
            {
                "indexed_count": 125,
                "folders": ["10-Projects", ...],
                "file_count": {
                    "10-Projects": 45,
                    ...
                },
                "timestamp": "2026-01-30T22:10:00"
            }
        """
        
        indexed = 0
        folder_counts = {}
        all_files = []
        
        try:
            # 각 폴더 순회
            for folder in self.included_folders:
                folder_path = self.vault_path / folder
                
                if not folder_path.exists():
                    logger.warning(f"⚠️ Folder not found: {folder}")
                    continue
                
                md_files = list(folder_path.rglob("*.md"))
                folder_counts[folder] = len(md_files)
                
                for file_path in md_files:
                    try:
                        # 파일 메타데이터
                        stat = file_path.stat()
                        
                        file_record = {
                            "path": str(file_path),
                            "relative_path": str(file_path.relative_to(self.vault_path)),
                            "folder": folder,
                            "name": file_path.stem,
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "weight": self.folder_weights.get(folder, 1.0)
                        }
                        
                        all_files.append(file_record)
                        indexed += 1
                    
                    except Exception as e:
                        logger.error(f"❌ Error processing {file_path}: {e}")
                        continue
            
            # 인덱스 저장
            self.file_index = {f["path"]: f for f in all_files}
            self._save_cache(all_files)
            
            result = {
                "indexed_count": indexed,
                "folders": list(folder_counts.keys()),
                "file_count": folder_counts,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Indexed {indexed} files from {len(folder_counts)} folders")
            return result
        
        except Exception as e:
            logger.error(f"❌ Indexing failed: {e}")
            raise
    
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        메모리 검색
        
        Args:
            query: 검색 쿼리
            max_results: 반환할 최대 결과 수
        
        Returns:
            [
                {
                    "path": "/10-Projects/...",
                    "folder": "10-Projects",
                    "name": "파일명",
                    "weight": 1.5,
                    "modified": "2026-01-30T...",
                    "preview": "파일 내용 미리보기"
                },
                ...
            ]
        """
        
        if not self.file_index:
            self.index_vault()
        
        query_lower = query.lower()
        results = []
        
        try:
            for file_path, metadata in self.file_index.items():
                # 1. 파일명으로 매칭
                score = 0
                if query_lower in metadata["name"].lower():
                    score += 10 * metadata["weight"]
                
                # 2. 폴더명으로 매칭
                if query_lower in metadata["folder"].lower():
                    score += 5 * metadata["weight"]
                
                # 3. 파일 내용 검색 (선택)
                try:
                    content = Path(file_path).read_text(encoding='utf-8')
                    if query_lower in content.lower():
                        occurrences = content.lower().count(query_lower)
                        score += (2 + occurrences) * metadata["weight"]
                        
                        # 미리보기 추출
                        lines = content.split('\n')
                        preview = '\n'.join(lines[:3])[:200]
                        metadata["preview"] = preview
                
                except Exception as e:
                    logger.warning(f"⚠️ Cannot read {file_path}: {e}")
                
                if score > 0:
                    results.append({
                        **metadata,
                        "score": score
                    })
            
            # 점수로 정렬
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:max_results]
            
            logger.info(f"✅ Found {len(results)} results for '{query}'")
            return results
        
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def read_file(self, file_path: str) -> Optional[str]:
        """
        파일 내용 읽기
        
        Args:
            file_path: 파일 경로
        
        Returns:
            파일 내용 (Markdown)
        """
        
        try:
            full_path = Path(file_path)
            if not full_path.exists():
                full_path = self.vault_path / file_path
            
            content = full_path.read_text(encoding='utf-8')
            logger.info(f"✅ Read {file_path} ({len(content)} bytes)")
            return content
        
        except Exception as e:
            logger.error(f"❌ Cannot read {file_path}: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        메모리 통계
        
        Returns:
            {
                "total_files": 125,
                "total_size_mb": 15.3,
                "folders": {...},
                "last_indexed": "2026-01-30T..."
            }
        """
        
        if not self.file_index:
            return {"status": "not_indexed"}
        
        total_size = sum(f["size"] for f in self.file_index.values())
        folder_stats = {}
        
        for folder in self.included_folders:
            folder_files = [f for f in self.file_index.values() if f["folder"] == folder]
            if folder_files:
                folder_stats[folder] = {
                    "file_count": len(folder_files),
                    "size_mb": sum(f["size"] for f in folder_files) / (1024*1024),
                    "weight": self.folder_weights.get(folder, 1.0)
                }
        
        return {
            "total_files": len(self.file_index),
            "total_size_mb": round(total_size / (1024*1024), 2),
            "folders": folder_stats,
            "vault_path": str(self.vault_path),
            "last_indexed": self._get_cache_time()
        }
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 내부 헬퍼 메서드
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _save_cache(self, files: List[Dict]) -> None:
        """캐시 저장"""
        cache_file = self.cache_dir / "vault-index.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(files, f, indent=2)
            logger.info(f"✅ Cache saved: {cache_file}")
        except Exception as e:
            logger.warning(f"⚠️ Cache save failed: {e}")
    
    def _load_cache(self) -> bool:
        """캐시 로드"""
        cache_file = self.cache_dir / "vault-index.json"
        
        if not cache_file.exists():
            return False
        
        # 캐시 유효 기간 확인
        mtime = cache_file.stat().st_mtime
        if (datetime.now() - datetime.fromtimestamp(mtime)).total_seconds() > self.cache_ttl:
            logger.info("⚠️ Cache expired")
            return False
        
        try:
            with open(cache_file, 'r') as f:
                files = json.load(f)
            self.file_index = {f["path"]: f for f in files}
            logger.info(f"✅ Cache loaded: {len(self.file_index)} files")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Cache load failed: {e}")
            return False
    
    def _get_cache_time(self) -> Optional[str]:
        """캐시 생성 시간"""
        cache_file = self.cache_dir / "vault-index.json"
        if cache_file.exists():
            mtime = cache_file.stat().st_mtime
            return datetime.fromtimestamp(mtime).isoformat()
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 사용 예시
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 1. 초기화
    obsidian = ObsidianMemory(
        "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인/Obsidian/SHawn"
    )
    
    # 2. Vault 인덱싱
    print("📇 Indexing Obsidian Vault...")
    index_result = obsidian.index_vault()
    print(f"✅ Indexed {index_result['indexed_count']} files")
    
    # 3. 검색
    print("\n🔍 Searching...")
    results = obsidian.search("SHawn-Brain", max_results=5)
    for r in results:
        print(f"  • {r['relative_path']} (weight: {r['weight']})")
    
    # 4. 통계
    print("\n📊 Statistics:")
    stats = obsidian.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
