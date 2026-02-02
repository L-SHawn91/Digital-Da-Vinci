"""
📊 작업 추적기 (Work Tracker)
신경계 기반 작업 실행 및 효율성 추적

역할: 작업 시작 → 신경계 할당 → 작업 실행 → 효율성 리포트
특징: 자동 신경계 활성화, 실시간 추적, 최종 리포트 생성
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from neural_router import NeuralModelRouter
import json


class WorkTracker:
    """신경계 기반 작업 추적 시스템"""
    
    def __init__(self):
        self.router = NeuralModelRouter()
        self.current_work = None
        self.work_history = []
    
    def start_work(
        self,
        task_name: str,
        neural_levels: List[str],
        description: str = ""
    ) -> Dict:
        """
        작업 시작 - 신경계 할당 및 추적 시작
        
        Args:
            task_name: 작업명
            neural_levels: 필요한 신경계 레벨 (예: ["L1", "L2", "L3", "L4"])
            description: 작업 설명
        
        Returns:
            {
                "task_id": "WORK_2026020117590001",
                "task_name": "Workspace 정리",
                "start_time": "2026-02-01T17:59:00Z",
                "neural_levels": ["L1", "L2", "L3", "L4"],
                "allocations": {...}
            }
        """
        
        # 작업 ID 생성
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:14]
        task_id = f"WORK_{timestamp}"
        
        # 신경계 할당
        report = self.router.get_neural_allocation_report(task_name, neural_levels)
        
        # 작업 정보 저장
        self.current_work = {
            "task_id": task_id,
            "task_name": task_name,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "neural_levels": neural_levels,
            "allocations": report["allocations"],
            "efficiency_target": report["total_efficiency"],
            "status": "in_progress",
            "steps": []
        }
        
        # 콘솔 출력
        print(f"\n🚀 작업 시작: {task_name}")
        print(f"📋 작업 ID: {task_id}")
        print(f"⏱️  시작: {self.current_work['start_time']}")
        print(f"🧠 신경계 레벨: {neural_levels}")
        print(f"⭐ 목표 효율: {report['total_efficiency']:.1f}/10")
        print("\n신경계 할당:")
        
        for level, alloc in report["allocations"].items():
            if "primary" in alloc:
                print(f"  {level}: {alloc['primary']} ({alloc['score']:.1f}%)")
        
        print()
        
        return {
            "task_id": task_id,
            "status": "started",
            "allocations": report["allocations"]
        }
    
    def log_step(
        self,
        step_name: str,
        neural_level: str,
        model: str,
        status: str,
        quality_score: int = 100,
        response_time_ms: int = 0,
        tokens_used: int = 0
    ) -> Dict:
        """
        작업 진행 단계 기록
        
        Args:
            step_name: 단계명
            neural_level: 사용한 신경계 레벨
            model: 사용한 모델
            status: "success" | "partial" | "failure" | "api_error"
            quality_score: 0-100
            response_time_ms: 응답 시간
            tokens_used: 토큰 사용량
        
        Returns:
            업데이트 결과
        """
        
        if not self.current_work:
            return {"error": "작업을 먼저 시작해주세요"}
        
        # 단계 기록
        step = {
            "step_name": step_name,
            "neural_level": neural_level,
            "model": model,
            "status": status,
            "quality_score": quality_score,
            "response_time_ms": response_time_ms,
            "tokens_used": tokens_used,
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_work["steps"].append(step)
        
        # 모델 점수 업데이트
        update_result = self.router.update_score(
            neural_level,
            model,
            {
                "status": status,
                "quality_score": quality_score,
                "response_time_ms": response_time_ms,
                "tokens_used": tokens_used
            }
        )
        
        # 콘솔 출력
        status_icon = {
            "success": "✅",
            "partial": "⚠️ ",
            "failure": "❌",
            "api_error": "🔴"
        }.get(status, "❓")
        
        print(f"{status_icon} {step_name}")
        print(f"   모델: {model} ({neural_level})")
        print(f"   점수: {update_result['old_score']:.1f} → {update_result['new_score']:.1f} ({update_result['change']})")
        print(f"   응답: {response_time_ms}ms | 품질: {quality_score}%")
        print()
        
        return update_result
    
    def end_work(self, final_status: str = "completed") -> Dict:
        """
        작업 완료 - 최종 리포트 생성
        
        Args:
            final_status: "completed" | "failed" | "cancelled"
        
        Returns:
            최종 리포트
        """
        
        if not self.current_work:
            return {"error": "활성 작업이 없습니다"}
        
        # 소요 시간 계산
        start_time = datetime.fromisoformat(self.current_work["start_time"])
        end_time = datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()
        
        # 효율성 계산
        step_scores = [s.get("quality_score", 100) for s in self.current_work["steps"]]
        avg_quality = sum(step_scores) / len(step_scores) if step_scores else 100
        actual_efficiency = (avg_quality / 100) * 10
        
        # 토큰 사용 계산
        total_tokens = sum(s.get("tokens_used", 0) for s in self.current_work["steps"])
        
        # 최종 리포트
        report = {
            "task_id": self.current_work["task_id"],
            "task_name": self.current_work["task_name"],
            "status": final_status,
            "start_time": self.current_work["start_time"],
            "end_time": end_time.isoformat(),
            "duration_seconds": duration_seconds,
            "neural_levels": self.current_work["neural_levels"],
            "steps_executed": len(self.current_work["steps"]),
            "efficiency": {
                "target": self.current_work["efficiency_target"],
                "actual": round(actual_efficiency, 1),
                "variance": round(actual_efficiency - self.current_work["efficiency_target"], 1)
            },
            "quality": {
                "average_score": round(avg_quality, 1),
                "success_rate": sum(1 for s in self.current_work["steps"] if s["status"] == "success") / len(self.current_work["steps"]) if self.current_work["steps"] else 0
            },
            "resources": {
                "total_tokens": total_tokens,
                "avg_response_time_ms": round(sum(s.get("response_time_ms", 0) for s in self.current_work["steps"]) / len(self.current_work["steps"]), 0) if self.current_work["steps"] else 0
            },
            "allocations": self.current_work["allocations"]
        }
        
        # 히스토리에 추가
        self.work_history.append(report)
        
        # 콘솔 출력
        print(f"\n{'='*60}")
        print(f"✅ 작업 완료: {self.current_work['task_name']}")
        print(f"{'='*60}")
        print(f"작업 ID: {report['task_id']}")
        print(f"상태: {final_status.upper()}")
        print(f"⏱️  소요시간: {duration_seconds:.1f}초")
        print(f"\n📊 효율성:")
        print(f"  목표: {report['efficiency']['target']:.1f}/10")
        print(f"  실제: {report['efficiency']['actual']:.1f}/10")
        print(f"  편차: {report['efficiency']['variance']:+.1f}")
        print(f"\n📈 품질:")
        print(f"  평균 점수: {report['quality']['average_score']:.1f}%")
        print(f"  성공률: {report['quality']['success_rate']*100:.1f}%")
        print(f"\n💾 리소스:")
        print(f"  사용 토큰: {report['resources']['total_tokens']}")
        print(f"  평균 응답: {report['resources']['avg_response_time_ms']:.0f}ms")
        print(f"{'='*60}\n")
        
        # 작업 초기화
        self.current_work = None
        
        return report
    
    def get_work_history(self, limit: int = 10) -> List[Dict]:
        """최근 작업 히스토리 조회"""
        return self.work_history[-limit:]
    
    def save_report(self, report: Dict, filename: Optional[str] = None):
        """리포트를 파일로 저장"""
        if filename is None:
            filename = f"work_report_{report['task_id']}.json"
        
        filepath = Path(__file__).parent / "reports" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return {"saved": True, "path": str(filepath)}


# 사용 예시
if __name__ == "__main__":
    tracker = WorkTracker()
    
    # 1. 작업 시작
    tracker.start_work(
        task_name="Workspace 정리",
        neural_levels=["L1", "L2", "L3", "L4"],
        description="GitHub 저장소와 Workspace 동기화"
    )
    
    # 2. 단계별 진행
    tracker.log_step(
        step_name="GitHub 상태 진단",
        neural_level="L1",
        model="Groq",
        status="success",
        quality_score=98,
        response_time_ms=230,
        tokens_used=1200
    )
    
    tracker.log_step(
        step_name="우선순위 판단",
        neural_level="L2",
        model="Gemini",
        status="success",
        quality_score=95,
        response_time_ms=1200,
        tokens_used=3400
    )
    
    # 3. 작업 완료
    report = tracker.end_work(final_status="completed")
