#!/usr/bin/env python3
"""
Obsidian 메타데이터 추출 (PARA 구조)
"""

import os
import json
from pathlib import Path
from datetime import datetime

OBSIDIAN_PATH = "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인/Obsidian/SHawn"

# PARA 폴더 가중치
FOLDER_WEIGHTS = {
    "10-Projects": 1.5,
    "20-Areas": 1.0,
    "30-Concepts": 0.8,
    "40-Sources": 0.9,
    "50-Lab": 1.3,
    "60-Writing": 0.7,
}

def extract_obsidian_metadata():
    """Obsidian PARA 구조에서 메타 추출"""
    
    metadata = {
        "extracted_at": datetime.now().isoformat(),
        "path": OBSIDIAN_PATH,
        "folders": {},
        "total_files": 0,
        "total_size_mb": 0
    }
    
    for folder_name in FOLDER_WEIGHTS.keys():
        folder_path = os.path.join(OBSIDIAN_PATH, folder_name)
        
        if not os.path.exists(folder_path):
            continue
        
        # 폴더 통계
        md_files = []
        total_size = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    md_files.append({
                        "name": file,
                        "relative_path": os.path.relpath(file_path, folder_path),
                        "size_kb": os.path.getsize(file_path) / 1024
                    })
                    total_size += os.path.getsize(file_path)
        
        metadata["folders"][folder_name] = {
            "weight": FOLDER_WEIGHTS[folder_name],
            "md_files": len(md_files),
            "size_mb": total_size / (1024 * 1024),
            "files": md_files[:10]  # 샘플 (처음 10개만)
        }
        
        metadata["total_files"] += len(md_files)
        metadata["total_size_mb"] += total_size / (1024 * 1024)
    
    return metadata

def main():
    print("🔍 Obsidian 메타데이터 추출 중...")
    
    meta = extract_obsidian_metadata()
    
    print(f"\n📊 Obsidian 구조:")
    for folder, data in meta["folders"].items():
        print(f"  {folder}")
        print(f"    - Markdown 파일: {data['md_files']}개")
        print(f"    - 크기: {data['size_mb']:.1f}MB")
        print(f"    - 가중치: {data['weight']}x")
    
    print(f"\n📈 합계:")
    print(f"  - 총 파일: {meta['total_files']}개")
    print(f"  - 총 크기: {meta['total_size_mb']:.1f}MB")
    
    # 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/obsidian_metadata.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 저장: {output_file}")

if __name__ == "__main__":
    main()
