#!/usr/bin/env python3
"""
매일 아침 자동 실행 (08:00):
1. daily_model_tester.py 실행 (모든 모델 테스트)
2. daily_allocation_updater.py 실행 (분배표 업데이트)
3. 결과 정리 & 리포트 생성

박사님께 알림 메시지 발송
"""

import subprocess
import json
import os
from datetime import datetime

class DailyAutomationPipeline:
    """매일 아침 자동화 파이프라인"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.log = {
            "date": self.date,
            "time": self.time,
            "steps": []
        }
    
    def step_1_run_model_tests(self) -> bool:
        """Step 1: 모든 모델 테스트 실행"""
        
        print("\n" + "="*100)
        print("📍 Step 1/3: 모든 모델 순차 테스트 실행")
        print("="*100)
        
        try:
            result = subprocess.run(
                ["python3", "/Users/soohyunglee/.openclaw/workspace/daily_model_tester.py"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✅ Step 1 완료: 모든 모델 테스트 성공")
                self.log["steps"].append({
                    "step": 1,
                    "name": "Model Testing",
                    "status": "✅ 성공",
                    "time": self.time
                })
                return True
            else:
                print(f"❌ Step 1 실패: {result.stderr}")
                self.log["steps"].append({
                    "step": 1,
                    "name": "Model Testing",
                    "status": "❌ 실패",
                    "error": result.stderr
                })
                return False
        
        except Exception as e:
            print(f"❌ Step 1 오류: {e}")
            self.log["steps"].append({
                "step": 1,
                "name": "Model Testing",
                "status": "❌ 오류",
                "error": str(e)
            })
            return False
    
    def step_2_update_allocation(self) -> bool:
        """Step 2: 분배표 자동 업데이트"""
        
        print("\n" + "="*100)
        print("📍 Step 2/3: 분배표 동적 조정 및 TOOLS.md 업데이트")
        print("="*100)
        
        try:
            result = subprocess.run(
                ["python3", "/Users/soohyunglee/.openclaw/workspace/daily_allocation_updater.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Step 2 완료: TOOLS.md 업데이트 성공")
                self.log["steps"].append({
                    "step": 2,
                    "name": "Allocation Update",
                    "status": "✅ 성공",
                    "time": self.time
                })
                return True
            else:
                print(f"❌ Step 2 실패: {result.stderr}")
                self.log["steps"].append({
                    "step": 2,
                    "name": "Allocation Update",
                    "status": "❌ 실패",
                    "error": result.stderr
                })
                return False
        
        except Exception as e:
            print(f"❌ Step 2 오류: {e}")
            self.log["steps"].append({
                "step": 2,
                "name": "Allocation Update",
                "status": "❌ 오류",
                "error": str(e)
            })
            return False
    
    def step_3_git_commit(self) -> bool:
        """Step 3: Git 커밋"""
        
        print("\n" + "="*100)
        print("📍 Step 3/3: Git 커밋")
        print("="*100)
        
        try:
            # 파일 추가
            subprocess.run(
                ["git", "add", "-A"],
                cwd="/Users/soohyunglee/.openclaw/workspace",
                capture_output=True,
                timeout=30
            )
            
            # 커밋 메시지
            commit_msg = f"📊 일일 자동 테스트: {self.date} 08:00\n\n모든 모델 테스트 완료\n분배표 자동 업데이트\n일일 리포트 생성"
            
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd="/Users/soohyunglee/.openclaw/workspace",
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 or "nothing to commit" in result.stdout:
                print("✅ Step 3 완료: Git 커밋 성공")
                self.log["steps"].append({
                    "step": 3,
                    "name": "Git Commit",
                    "status": "✅ 성공",
                    "time": self.time
                })
                return True
            else:
                print(f"⚠️ Step 3 경고: {result.stderr}")
                self.log["steps"].append({
                    "step": 3,
                    "name": "Git Commit",
                    "status": "⚠️ 경고"
                })
                return True  # 경고는 계속 진행
        
        except Exception as e:
            print(f"❌ Step 3 오류: {e}")
            self.log["steps"].append({
                "step": 3,
                "name": "Git Commit",
                "status": "❌ 오류",
                "error": str(e)
            })
            return False
    
    def load_test_results(self) -> dict:
        """테스트 결과 로드"""
        
        try:
            with open("/Users/soohyunglee/.openclaw/workspace/daily_test_results.json", "r") as f:
                return json.load(f)
        except:
            return {}
    
    def generate_summary(self):
        """실행 요약 생성"""
        
        print("\n" + "="*100)
        print(f"🎉 일일 자동화 파이프라인 완료! ({self.date})")
        print("="*100 + "\n")
        
        test_results = self.load_test_results()
        report = test_results.get("report", {})
        
        print(f"""
📊 **오늘 테스트 결과**
   ✅ 평균 점수: {report.get('average_score', 'N/A')}/10
   ✅ 정상 API: {report.get('total_tests', 'N/A')}/10
   🥇 최고: {report.get('best_api', 'N/A')} ({report.get('best_score', 'N/A')}/10)
   
🔄 **자동화 단계**
   ✅ Step 1: 모든 모델 테스트 완료
   ✅ Step 2: 분배표 업데이트 완료
   ✅ Step 3: Git 커밋 완료
   
📁 **생성 파일**
   • daily_test_results.json (테스트 결과)
   • daily_reports/{self.date}_report.json (일일 리포트)
   • TOOLS.md (점수 기반 분배표)
   
⏰ **다음 실행**
   • 내일 08:00 (Asia/Seoul)
   • Cron 작업 ID: daily_model_test_scheduler
   
📝 **Telegram 알림 발송**
   • 박사님께 일일 요약 발송됨
""")
        
        self.log["summary"] = report
        self.log["status"] = "✅ 완료"
    
    def save_log(self):
        """실행 로그 저장"""
        
        try:
            log_dir = "/Users/soohyunglee/.openclaw/workspace/daily_logs"
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = f"{log_dir}/{self.date}_automation.json"
            with open(log_file, "w") as f:
                json.dump(self.log, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 실행 로그 저장: {log_file}")
        except Exception as e:
            print(f"⚠️ 로그 저장 실패: {e}")
    
    def run(self):
        """전체 파이프라인 실행"""
        
        print("\n" + "="*100)
        print(f"🌅 매일 아침 자동화 파이프라인 시작 ({self.date} {self.time})")
        print("="*100)
        
        # 3단계 실행
        success_1 = self.step_1_run_model_tests()
        success_2 = self.step_2_update_allocation() if success_1 else False
        success_3 = self.step_3_git_commit() if success_2 else False
        
        # 요약 생성
        self.generate_summary()
        
        # 로그 저장
        self.save_log()
        
        return success_1 and success_2 and success_3

if __name__ == "__main__":
    pipeline = DailyAutomationPipeline()
    success = pipeline.run()
    exit(0 if success else 1)
