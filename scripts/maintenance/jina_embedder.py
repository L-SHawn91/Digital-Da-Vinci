#!/usr/bin/env python3
"""
Zotero 논문 메타데이터 + Jina AI 임베딩
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict
import time

ZOTERO_PATH = "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인/Papers/Zotero/papers"
JINA_API_KEY = "***REDACTED_JINA***"
JINA_API_URL = "https://api.jina.ai/v1/embeddings"

def extract_paper_metadata(paper_path: str) -> Dict:
    """폴더에서 논문 메타 추출"""
    folder_name = os.path.basename(paper_path)
    
    # 메타데이터 파일 찾기
    meta_files = {
        'title': None,
        'authors': None,
        'year': None,
        'doi': None,
        'abstract': None
    }
    
    # 텍스트 파일 수집
    texts = []
    for file in os.listdir(paper_path):
        file_path = os.path.join(paper_path, file)
        if os.path.isfile(file_path) and file.endswith(('.txt', '.md')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:500]  # 처음 500자만
                    texts.append(content)
            except:
                pass
    
    # 메타데이터 구성
    metadata_text = f"{folder_name}\n" + "\n".join(texts[:3])
    
    return {
        "id": folder_name.replace("/", "_").replace("-", "_"),
        "folder": folder_name,
        "path": paper_path,
        "category": paper_path.split('/')[-2] if '/' in paper_path else "Unknown",
        "text": metadata_text[:1000]  # 최대 1000자
    }

def embed_with_jina(texts: List[str]) -> List[List[float]]:
    """Jina AI로 텍스트 임베딩"""
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept-Encoding": "gzip"
    }
    
    data = {
        "model": "jina-embeddings-v3",
        "task": "retrieval.passage",
        "dimensions": 1024,
        "late_chunking": False,
        "embedding_type": "float",
        "input": texts
    }
    
    try:
        response = requests.post(JINA_API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        embeddings = [item['embedding'] for item in result['data']]
        return embeddings
    except Exception as e:
        print(f"❌ Jina API 에러: {e}")
        return None

def main():
    print("🚀 Jina AI 임베딩 시작...")
    
    # 1. 메타 추출
    papers = []
    for root, dirs, files in os.walk(ZOTERO_PATH):
        # 깊이 2~3 레벨의 폴더만 처리
        depth = root.replace(ZOTERO_PATH, "").count(os.sep)
        if depth >= 2 and depth <= 3:
            if files:  # 파일이 있는 폴더만
                meta = extract_paper_metadata(root)
                papers.append(meta)
    
    print(f"📄 추출된 논문: {len(papers)}개")
    
    if not papers:
        print("❌ 논문을 찾을 수 없습니다.")
        return
    
    # 2. Jina AI 임베딩 (배치)
    print("\n🔄 Jina AI로 임베딩 중...")
    
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(papers), batch_size):
        batch = papers[i:i+batch_size]
        texts = [p['text'] for p in batch]
        
        print(f"  배치 {i//batch_size + 1}: {len(texts)}개 임베딩...")
        
        embeddings = embed_with_jina(texts)
        if embeddings:
            for j, paper in enumerate(batch):
                paper['embedding'] = embeddings[j]
                all_embeddings.append(paper)
        
        time.sleep(1)  # Rate limiting
    
    print(f"\n✅ 임베딩 완료: {len(all_embeddings)}개")
    
    # 3. 결과 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/zotero_embeddings.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(all_embeddings),
            "model": "jina-embeddings-v3",
            "dimension": 1024,
            "papers": all_embeddings
        }, f, ensure_ascii=False)
    
    print(f"\n💾 저장: {output_file}")
    print(f"   총 {len(all_embeddings)}개 논문")
    print(f"   다음: Pinecone 로드")

if __name__ == "__main__":
    main()
