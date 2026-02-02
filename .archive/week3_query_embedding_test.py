#!/usr/bin/env python3
"""
Week 3: 쿼리 임베딩 + 의미 검색 테스트
"""

import json
import requests
from datetime import datetime

JINA_API_KEY = "***REDACTED_JINA***"
JINA_API_URL = "https://api.jina.ai/v1/embeddings"

# 테스트 쿼리들
TEST_QUERIES = [
    "자궁 오가노이드 분화",
    "줄기세포 신호전달",
    "데이터 분석 방법론",
    "면역 반응 메커니즘",
    "조직공학 기술"
]

def embed_query(query: str) -> dict:
    """Jina AI로 쿼리 임베딩"""
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept-Encoding": "gzip"
    }
    
    data = {
        "model": "jina-embeddings-v3",
        "task": "retrieval.query",  # 쿼리는 query 태스크 사용!
        "dimensions": 1024,
        "late_chunking": False,
        "embedding_type": "float",
        "input": [query]
    }
    
    try:
        response = requests.post(JINA_API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        embedding = result['data'][0]['embedding']
        
        return {
            "query": query,
            "embedding": embedding,
            "dimension": len(embedding),
            "status": "✅ 성공"
        }
    except Exception as e:
        print(f"❌ 에러: {e}")
        return {
            "query": query,
            "status": f"❌ 실패: {str(e)}"
        }

def main():
    print("🚀 Week 3: 쿼리 임베딩 테스트 시작!\n")
    
    results = {
        "test_time": datetime.now().isoformat(),
        "queries": []
    }
    
    print("📝 테스트 쿼리들:")
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n  {i}. '{query}'")
        
        # 임베딩
        result = embed_query(query)
        results["queries"].append(result)
        
        if "embedding" in result:
            print(f"     ✅ 임베딩 완료 ({result['dimension']}-dim)")
            print(f"     첫 10개 값: {result['embedding'][:10]}")
        else:
            print(f"     {result['status']}")
    
    # 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/week3_query_embeddings.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 결과 저장: {output_file}")
    print(f"   테스트된 쿼리: {len(TEST_QUERIES)}개")
    print(f"   성공: {sum(1 for q in results['queries'] if 'embedding' in q)}개")

if __name__ == "__main__":
    main()
