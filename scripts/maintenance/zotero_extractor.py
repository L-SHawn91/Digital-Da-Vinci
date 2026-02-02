#!/usr/bin/env python3
"""
Zotero 논문 메타데이터 추출 및 Jina AI 임베딩
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

ZOTERO_PATH = "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인/Papers/Zotero/papers"

def extract_metadata():
    """Zotero 폴더 구조에서 메타 추출"""
    papers = []
    
    # 모든 서브폴더 탐색
    for root, dirs, files in os.walk(ZOTERO_PATH):
        # 각 폴더를 논문으로 간주
        rel_path = os.path.relpath(root, ZOTERO_PATH)
        
        # 루트 폴더는 제외
        if rel_path == ".":
            continue
            
        # 메타데이터 파일 찾기
        meta_files = [f for f in files if f.endswith(('.json', '.txt', '.md'))]
        
        if meta_files or files:  # 파일이 있으면 논문으로 처리
            paper = {
                "id": rel_path.replace("/", "_").replace("-", "_"),
                "path": rel_path,
                "folder": os.path.basename(root),
                "title": os.path.basename(root),
                "files": files,
                "file_count": len(files)
            }
            papers.append(paper)
    
    return papers

def main():
    print("🔍 Zotero 메타데이터 추출 중...")
    
    papers = extract_metadata()
    
    print(f"\n📊 발견된 논문: {len(papers)}개")
    
    # 카테고리별 분류
    categories = {}
    for paper in papers:
        path = paper['path']
        category = path.split('/')[0] if '/' in path else 'Unknown'
        if category not in categories:
            categories[category] = []
        categories[category].append(paper)
    
    print("\n📚 카테고리별 분포:")
    for cat, items in sorted(categories.items()):
        print(f"  {cat}: {len(items)}개")
    
    # 샘플 출력
    print(f"\n📄 샘플 논문 (첫 5개):")
    for paper in papers[:5]:
        print(f"  - {paper['title']}")
        print(f"    경로: {paper['path']}")
        print(f"    파일: {paper['file_count']}개")
    
    # JSON으로 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/zotero_papers.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "extracted_at": datetime.now().isoformat(),
            "total_papers": len(papers),
            "categories": {k: len(v) for k, v in categories.items()},
            "papers": papers
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 메타데이터 저장: {output_file}")
    print(f"   총 논문: {len(papers)}개")

if __name__ == "__main__":
    main()
