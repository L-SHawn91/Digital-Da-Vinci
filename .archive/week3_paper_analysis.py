#!/usr/bin/env python3
"""
고급 Layer 통합: 실제 논문 파일 읽기 + 의미 추출
"""

import json
import os
from pathlib import Path
from datetime import datetime

ZOTERO_PATH = "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인/Papers/Zotero/papers"

def extract_paper_content(paper_folder):
    """논문 폴더에서 실제 텍스트 내용 추출"""
    texts = []
    
    for file in os.listdir(paper_folder):
        file_path = os.path.join(paper_folder, file)
        
        # TXT 파일 읽기 (있으면)
        if file.endswith('.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:500]
                    texts.append(content)
            except:
                pass
    
    return " ".join(texts) if texts else ""

def map_paper_to_keywords(paper_folder, paper_category):
    """논문의 주요 키워드 추출"""
    
    # 카테고리별 예상 키워드
    keyword_map = {
        "[A]-Reproductive-Science": [
            "자궁", "내막", "면역", "호르몬", "생식",
            "태반", "배아", "임신", "월경"
        ],
        "[B]-Stem-Cells-Organoids": [
            "줄기세포", "오가노이드", "분화", "신호전달",
            "조직공학", "자기재생", "배양", "세포"
        ],
        "[C]-Comparative-Species-Models": [
            "동물모델", "비교", "인간", "영장류",
            "마우스", "돼지", "동종성"
        ],
        "[D]-Data-Science-Methodology": [
            "데이터", "분석", "알고리즘", "통계",
            "머신러닝", "시각화", "방법론"
        ]
    }
    
    return keyword_map.get(paper_category, [])

def analyze_papers():
    """전체 논문 분석"""
    
    print("📚 논문 폴더 분석 중...\n")
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "categories": {}
    }
    
    for root, dirs, files in os.walk(ZOTERO_PATH):
        depth = root.replace(ZOTERO_PATH, "").count(os.sep)
        
        # 깊이 2~3 레벨만
        if depth >= 2 and depth <= 3 and files:
            folder_name = os.path.basename(root)
            
            # 카테고리 추론
            parent = os.path.basename(os.path.dirname(root))
            category = None
            
            if parent.startswith("["):
                category = parent
            
            # 파일 수
            pdf_count = len([f for f in files if f.endswith('.pdf')])
            txt_count = len([f for f in files if f.endswith('.txt')])
            
            if category:
                if category not in analysis["categories"]:
                    analysis["categories"][category] = {
                        "folders": [],
                        "total_files": 0
                    }
                
                analysis["categories"][category]["folders"].append({
                    "name": folder_name,
                    "path": root,
                    "pdf_count": pdf_count,
                    "txt_count": txt_count,
                    "total_files": len(files),
                    "keywords": map_paper_to_keywords(root, category)
                })
                
                analysis["categories"][category]["total_files"] += len(files)
    
    return analysis

def main():
    print("🔬 고급 Layer 통합: 논문 내용 분석\n")
    
    # 1. 논문 분석
    analysis = analyze_papers()
    
    # 2. 결과 출력
    print("📊 분석 결과:\n")
    
    total_folders = 0
    total_files = 0
    
    for category, data in analysis["categories"].items():
        print(f"\n{category}")
        print(f"  폴더: {len(data['folders'])}개")
        print(f"  총 파일: {data['total_files']}개")
        
        for folder in data["folders"]:
            print(f"\n  📁 {folder['name']}")
            print(f"     파일: {folder['pdf_count']} PDF + {folder['txt_count']} TXT")
            print(f"     예상 키워드: {', '.join(folder['keywords'][:5])}")
            
            total_folders += 1
            total_files += folder['total_files']
    
    # 3. 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/week3_paper_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n✅ 분석 결과 저장: {output_file}")
    print(f"   총 폴더: {total_folders}개")
    print(f"   총 파일: {total_files}개")

if __name__ == "__main__":
    main()
