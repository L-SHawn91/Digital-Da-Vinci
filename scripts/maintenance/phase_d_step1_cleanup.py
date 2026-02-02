#!/usr/bin/env python3
"""
Phase D Step 1: 워크스페이스 정리 스크립트
모델: github-copilot/claude-sonnet-4 (복잡한 코드/자동화)

목표:
1. 가상환경 정리 (venv 제거, shawn_env 유지)
2. __pycache__ 정소
3. 레거시 카트리지 제거
4. 메모리 폴더 정규화
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime


class WorkspaceOrganizer:
    """워크스페이스 정리기"""
    
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "operations": [],
            "size_before": 0,
            "size_after": 0,
            "files_deleted": 0,
            "dirs_cleaned": 0
        }
    
    def calculate_size(self, path):
        """디렉토리 크기 계산"""
        total = 0
        try:
            for entry in Path(path).rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass
        return total
    
    def step1_cleanup_venv(self):
        """Step 1: 가상환경 정리"""
        print("\n" + "="*70)
        print("🧹 Step 1: 가상환경 정리")
        print("="*70)
        
        venv_path = self.workspace / "venv"
        shawn_env_path = self.workspace / "shawn_env"
        
        # venv 제거 (불필요)
        if venv_path.exists():
            size = self.calculate_size(venv_path)
            print(f"\n❌ venv/ 제거 중... ({size/1024/1024:.1f}MB)")
            shutil.rmtree(venv_path)
            self.stats["size_before"] += size
            self.stats["files_deleted"] += 1
            self.stats["operations"].append({
                "type": "remove_venv",
                "size_mb": size/1024/1024,
                "status": "✅ 완료"
            })
            print("✅ venv/ 제거 완료")
        
        # shawn_env 유지 확인
        if shawn_env_path.exists():
            size = self.calculate_size(shawn_env_path)
            print(f"✅ shawn_env/ 유지 ({size/1024/1024:.1f}MB)")
            self.stats["operations"].append({
                "type": "keep_shawn_env",
                "size_mb": size/1024/1024,
                "status": "✅ 유지"
            })
    
    def step2_cleanup_pycache(self):
        """Step 2: __pycache__ 정소"""
        print("\n" + "="*70)
        print("🗑️ Step 2: __pycache__ 정소")
        print("="*70)
        
        pycache_dirs = list(self.workspace.rglob("__pycache__"))
        total_size = 0
        
        print(f"\n발견된 __pycache__ 디렉토리: {len(pycache_dirs)}개")
        
        for pycache in pycache_dirs:
            size = self.calculate_size(pycache)
            total_size += size
            print(f"  🗑️ {pycache.relative_to(self.workspace)}")
            shutil.rmtree(pycache)
        
        self.stats["size_before"] += total_size
        self.stats["dirs_cleaned"] += len(pycache_dirs)
        self.stats["operations"].append({
            "type": "cleanup_pycache",
            "count": len(pycache_dirs),
            "size_mb": total_size/1024/1024,
            "status": "✅ 완료"
        })
        
        print(f"\n✅ 총 {len(pycache_dirs)}개 디렉토리 정소 ({total_size/1024/1024:.1f}MB)")
    
    def step3_cleanup_legacy_cartridges(self):
        """Step 3: 레거시 카트리지 정리"""
        print("\n" + "="*70)
        print("🗑️ Step 3: 레거시 카트리지 정리")
        print("="*70)
        
        cartridges_path = self.workspace / "SHawn_Brain" / "cartridges"
        legacy_files = [
            "bio_cartridge.py",      # v1
            "bio_cartridge_v2.py",   # v2
            "investment_cartridge.py" # v1
        ]
        
        kept_files = [
            "bio_cartridge_v2_1.py",      # v2.1 최신
            "investment_cartridge_v2.py"   # v2 최신
        ]
        
        print("\n🗑️ 제거할 레거시 카트리지:")
        total_size = 0
        
        for legacy_file in legacy_files:
            legacy_path = cartridges_path / legacy_file
            if legacy_path.exists():
                size = legacy_path.stat().st_size
                total_size += size
                print(f"  ❌ {legacy_file} ({size/1024:.1f}KB)")
                legacy_path.unlink()
        
        print("\n✅ 유지할 최신 카트리지:")
        for kept_file in kept_files:
            kept_path = cartridges_path / kept_file
            if kept_path.exists():
                size = kept_path.stat().st_size
                print(f"  ✅ {kept_file} ({size/1024:.1f}KB)")
        
        self.stats["size_before"] += total_size
        self.stats["files_deleted"] += len(legacy_files)
        self.stats["operations"].append({
            "type": "cleanup_legacy_cartridges",
            "files": legacy_files,
            "size_mb": total_size/1024/1024,
            "status": "✅ 완료"
        })
        
        print(f"\n✅ {len(legacy_files)}개 레거시 파일 제거 ({total_size/1024:.1f}KB)")
    
    def step4_organize_memory(self):
        """Step 4: 메모리 폴더 정규화"""
        print("\n" + "="*70)
        print("📁 Step 4: 메모리 폴더 정규화")
        print("="*70)
        
        memory_path = self.workspace / "memory"
        
        if not memory_path.exists():
            print("\n✅ memory/ 폴더 없음 - 생성")
            memory_path.mkdir(exist_ok=True)
        
        # 서브 폴더 구조 확인
        subfolders = [
            "Daily_Logs",
            "Archive"
        ]
        
        print("\n📁 메모리 폴더 구조:")
        for subfolder in subfolders:
            subfolder_path = memory_path / subfolder
            if not subfolder_path.exists():
                subfolder_path.mkdir(exist_ok=True)
                print(f"  ✅ {subfolder}/ 생성")
            else:
                file_count = len(list(subfolder_path.glob("*")))
                print(f"  ✅ {subfolder}/ ({file_count}개 파일)")
        
        self.stats["operations"].append({
            "type": "organize_memory",
            "folders": subfolders,
            "status": "✅ 완료"
        })
        
        print("\n✅ 메모리 폴더 정규화 완료")
    
    def run(self):
        """전체 정리 실행"""
        print("\n" + "="*70)
        print("🧹 Phase D Step 1: 워크스페이스 정리 시작")
        print("="*70)
        
        # 정리 전 크기
        self.stats["size_before"] = self.calculate_size(self.workspace) / 1024 / 1024
        print(f"\n📊 정리 전 용량: {self.stats['size_before']:.1f}MB")
        
        # 각 단계 실행
        self.step1_cleanup_venv()
        self.step2_cleanup_pycache()
        self.step3_cleanup_legacy_cartridges()
        self.step4_organize_memory()
        
        # 정리 후 크기
        self.stats["size_after"] = self.calculate_size(self.workspace) / 1024 / 1024
        
        # 최종 결과
        self.print_summary()
    
    def print_summary(self):
        """최종 요약"""
        print("\n" + "="*70)
        print("📊 최종 결과")
        print("="*70)
        
        size_reduction = self.stats["size_before"]
        reduction_percent = (size_reduction / (self.stats["size_before"] + self.stats["size_after"])) * 100 if (self.stats["size_before"] + self.stats["size_after"]) > 0 else 0
        
        print(f"\n📈 크기 변화:")
        print(f"  정리 전: {self.stats['size_before']:.1f}MB")
        print(f"  정리 후: {self.stats['size_after']:.1f}MB")
        print(f"  감소: {size_reduction:.1f}MB ({reduction_percent:.0f}%)")
        
        print(f"\n🗑️ 정리 내역:")
        print(f"  삭제 파일: {self.stats['files_deleted']}개")
        print(f"  정소 폴더: {self.stats['dirs_cleaned']}개")
        
        print(f"\n✅ 완료 시간: {datetime.now().isoformat()}")
        
        # JSON 저장
        self.stats["end_time"] = datetime.now().isoformat()
        result_file = self.workspace / "workspace_cleanup_result.json"
        with open(result_file, "w") as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"📝 결과 저장: workspace_cleanup_result.json")


if __name__ == "__main__":
    workspace = Path("/Users/soohyunglee/.openclaw/workspace")
    organizer = WorkspaceOrganizer(workspace)
    organizer.run()
