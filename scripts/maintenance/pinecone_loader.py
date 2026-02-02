#!/usr/bin/env python3
"""
Pinecone에 논문 벡터 로드
"""

import json
import time
from pinecone import Pinecone

PINECONE_API_KEY = "pcsk_4W6SdJ_R5gJNbqkvXTXRD8wXkd5THZcTc9tkZg73Tcd5XoUrQk4655BAyHViX4W5MBvL76"
EMBEDDING_FILE = "/Users/soohyunglee/.openclaw/workspace/zotero_embeddings.json"

def main():
    print("🚀 Pinecone 로드 시작...")
    
    # 1. Pinecone 초기화
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # 2. Index 확인 또는 생성
    index_name = "papers"
    
    try:
        index = pc.Index(index_name)
        print(f"✅ Index '{index_name}' 사용 중")
    except:
        print(f"📋 Index '{index_name}' 생성 중...")
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )
        time.sleep(60)  # Index 생성 대기
        index = pc.Index(index_name)
        print(f"✅ Index '{index_name}' 생성 완료")
    
    # 3. 임베딩 파일 로드
    print("\n📄 임베딩 파일 로드 중...")
    with open(EMBEDDING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = data['papers']
    print(f"   총 {len(papers)}개 논문")
    
    # 4. Pinecone에 업로드
    print("\n🔄 Pinecone에 벡터 업로드 중...")
    
    vectors_to_upsert = []
    for paper in papers:
        vector = (
            paper['id'],
            paper['embedding'],
            {
                "folder": paper['folder'],
                "category": paper['category'],
                "path": paper['path'],
                "text_preview": paper['text'][:100]
            }
        )
        vectors_to_upsert.append(vector)
    
    # Batch 업로드
    batch_size = 100
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i+batch_size]
        index.upsert(vectors=batch, namespace="default")
        print(f"  ✓ {min(i+batch_size, len(vectors_to_upsert))}/{len(vectors_to_upsert)} 업로드 완료")
    
    # 5. 통계
    print(f"\n✅ Pinecone 업로드 완료!")
    
    stats = index.describe_index_stats()
    print(f"\n📊 Index 통계:")
    print(f"   총 벡터: {stats.total_vector_count}")
    print(f"   네임스페이스: {list(stats.namespaces.keys())}")
    
    # 6. 테스트 쿼리
    print(f"\n🔍 테스트 쿼리 실행 중...")
    
    test_query = [0.1] * 1024  # 더미 벡터
    results = index.query(
        vector=test_query,
        top_k=3,
        namespace="default",
        include_metadata=True
    )
    
    print(f"   검색 결과: {len(results.matches)}개")
    for i, match in enumerate(results.matches):
        print(f"   {i+1}. {match.metadata['folder']} (유사도: {match.score:.2f})")

if __name__ == "__main__":
    main()
