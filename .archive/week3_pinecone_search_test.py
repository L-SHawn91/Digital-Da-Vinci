#!/usr/bin/env python3
"""
Pinecone 의미 검색 테스트
"""

import json
from pinecone import Pinecone
from datetime import datetime

PINECONE_API_KEY = "pcsk_4W6SdJ_R5gJNbqkvXTXRD8wXkd5THZcTc9tkZg73Tcd5XoUrQk4655BAyHViX4W5MBvL76"

def search_pinecone(query_embeddings: list) -> dict:
    """Pinecone에서 의미 검색"""
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("papers")
    
    results = {
        "test_time": datetime.now().isoformat(),
        "searches": []
    }
    
    for item in query_embeddings:
        if "embedding" not in item:
            continue
        
        query = item["query"]
        embedding = item["embedding"]
        
        # Pinecone 검색
        search_result = index.query(
            vector=embedding,
            top_k=5,
            namespace="default",
            include_metadata=True
        )
        
        matches = []
        for match in search_result.matches:
            matches.append({
                "folder": match.metadata["folder"],
                "category": match.metadata["category"],
                "score": float(match.score),
                "id": match.id
            })
        
        results["searches"].append({
            "query": query,
            "matches": matches,
            "total_matches": len(matches)
        })
        
        print(f"\n🔍 쿼리: '{query}'")
        print(f"   결과: {len(matches)}개")
        for i, match in enumerate(matches, 1):
            print(f"   {i}. {match['folder']} ({match['category']}) - 스코어: {match['score']:.4f}")
    
    return results

def main():
    print("🚀 Pinecone 의미 검색 테스트\n")
    
    # 쿼리 임베딩 로드
    with open("/Users/soohyunglee/.openclaw/workspace/week3_query_embeddings.json") as f:
        query_data = json.load(f)
    
    # 검색
    results = search_pinecone(query_data["queries"])
    
    # 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/week3_pinecone_search_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 검색 결과 저장: {output_file}")
    print(f"   테스트: {len(results['searches'])}개 쿼리")

if __name__ == "__main__":
    main()
