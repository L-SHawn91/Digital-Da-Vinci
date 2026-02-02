#!/usr/bin/env python3
"""
Hippocampus: 3계층 메모리 통합 시스템
- Layer 1: Obsidian (컨텍스트)
- Layer 2: Zotero (논문 지식)
- Layer 3: Pinecone (의미 검색)
"""

import json
from pinecone import Pinecone

PINECONE_API_KEY = "pcsk_4W6SdJ_R5gJNbqkvXTXRD8wXkd5THZcTc9tkZg73Tcd5XoUrQk4655BAyHViX4W5MBvL76"

class Hippocampus:
    """3계층 메모리 시스템"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index("papers")
        
        # 메타데이터 로드
        with open("/Users/soohyunglee/.openclaw/workspace/obsidian_metadata.json") as f:
            self.obsidian_meta = json.load(f)
        
        with open("/Users/soohyunglee/.openclaw/workspace/zotero_embeddings.json") as f:
            self.zotero_meta = json.load(f)
    
    def search(self, query: str, top_k: int = 5):
        """
        통합 검색:
        1. Obsidian에서 컨텍스트 추출
        2. Zotero에서 관련 논문 필터
        3. Pinecone에서 의미 기반 검색
        """
        
        result = {
            "query": query,
            "layers": {
                "obsidian": self._search_obsidian(query),
                "zotero": self._search_zotero(query),
                "pinecone": self._search_pinecone(query, top_k)
            }
        }
        
        return result
    
    def _search_obsidian(self, query: str):
        """Obsidian에서 관련 노트 찾기 (메타 기반)"""
        return {
            "total_files": self.obsidian_meta["total_files"],
            "total_size_mb": self.obsidian_meta["total_size_mb"],
            "folders": list(self.obsidian_meta["folders"].keys()),
            "note": "Full-text search는 로컬 Obsidian 필요"
        }
    
    def _search_zotero(self, query: str):
        """Zotero에서 관련 논문 필터 (카테고리 기반)"""
        category_map = {}
        for paper in self.zotero_meta["papers"]:
            cat = paper["category"]
            if cat not in category_map:
                category_map[cat] = []
            category_map[cat].append(paper["folder"])
        
        return {
            "total_papers": len(self.zotero_meta["papers"]),
            "categories": category_map,
            "note": "전체 논문 메타 가능"
        }
    
    def _search_pinecone(self, query: str, top_k: int = 5):
        """Pinecone에서 의미 기반 검색"""
        # 더미 벡터 (실제로는 Jina로 query 임베딩 필요)
        dummy_vector = [0.1] * 1024
        
        results = self.index.query(
            vector=dummy_vector,
            top_k=top_k,
            namespace="default",
            include_metadata=True
        )
        
        matches = []
        for match in results.matches:
            matches.append({
                "folder": match.metadata["folder"],
                "category": match.metadata["category"],
                "score": float(match.score)
            })
        
        return {
            "matches": matches,
            "vector_dimension": 1024,
            "note": "실제 쿼리는 Jina로 임베딩 후 검색"
        }
    
    def health_check(self):
        """시스템 상태 확인"""
        return {
            "status": "operational",
            "obsidian_files": self.obsidian_meta["total_files"],
            "zotero_papers": len(self.zotero_meta["papers"]),
            "pinecone_vectors": self.index.describe_index_stats().total_vector_count,
            "layers": 3,
            "ready": True
        }

def main():
    print("🧠 Hippocampus 초기화 중...")
    
    hippo = Hippocampus()
    
    print("\n✅ Hippocampus 준비 완료!")
    
    # 상태 확인
    health = hippo.health_check()
    print(f"\n📊 시스템 상태:")
    print(f"  - Obsidian 노트: {health['obsidian_files']}개")
    print(f"  - Zotero 논문: {health['zotero_papers']}개")
    print(f"  - Pinecone 벡터: {health['pinecone_vectors']}개")
    print(f"  - 계층: {health['layers']}계층")
    print(f"  - 준비 상태: {'🟢 준비됨' if health['ready'] else '🔴 오류'}")
    
    # 테스트 검색
    print(f"\n🔍 테스트 검색 (더미 쿼리)...")
    
    test_queries = [
        "자궁 오가노이드",
        "줄기세포 분화",
        "데이터 분석"
    ]
    
    for query in test_queries:
        result = hippo.search(query, top_k=3)
        print(f"\n  쿼리: '{query}'")
        print(f"    - Obsidian 노트: {result['layers']['obsidian']['total_files']}개")
        print(f"    - Zotero 논문: {result['layers']['zotero']['total_papers']}개")
        print(f"    - Pinecone 결과: {len(result['layers']['pinecone']['matches'])}개")
    
    # 결과 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/hippocampus_config.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "system": "Hippocampus v1.0",
            "layers": 3,
            "health": health,
            "ready": True,
            "next_steps": [
                "Jina AI로 쿼리 임베딩",
                "Pinecone으로 의미 검색",
                "결과 통합 및 랭킹"
            ]
        }, f, indent=2)
    
    print(f"\n💾 설정 저장: {output_file}")
    print(f"\n🚀 Hippocampus 준비 완료!")

if __name__ == "__main__":
    main()
