"""
🧠 작업 실행자 (Work Executor)
WorkTracker와 NeuralExecutor를 통합

역할: start_work → execute → end_work의 완전한 작업 사이클 관리
특징: 신경계 기반 작업 추적, 자동 점수 업데이트, 효율 메트릭
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Callable, Optional, List
from enum import Enum


class WorkPhase(Enum):
    """작업 단계"""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkExecutor:
    """작업 실행 관리자"""
    
    def __init__(self):
        self.work_log_path = Path(__file__).parent / "work_execution_log.json"
        self.work_log = self._load_work_log()
    
    def _load_work_log(self) -> Dict:
        """작업 로그 로드"""
        try:
            with open(self.work_log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"works": []}
    
    def start_work(
        self,
        work_id: str,
        work_name: str,
        task_type: str,
        neural_level: str,
        estimated_tokens: int = 0,
        priority: str = "normal"
    ) -> Dict:
        """
        작업 시작
        
        Args:
            work_id: 작업 ID (고유)
            work_name: 작업 이름
            task_type: 작업 타입 (coding, analysis, design, etc)
            neural_level: L1-L4
            estimated_tokens: 예상 토큰
            priority: 우선순위 (low, normal, high, critical)
        
        Returns:
            작업 정보
        """
        
        work = {
            "work_id": work_id,
            "work_name": work_name,
            "task_type": task_type,
            "neural_level": neural_level,
            "priority": priority,
            "phase": WorkPhase.STARTED.value,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "estimated_tokens": estimated_tokens,
            "actual_tokens": 0,
            "status": "ready"
        }
        
        self.work_log["works"].append(work)
        self._save_work_log()
        
        return work
    
    def log_step(
        self,
        work_id: str,
        step_name: str,
        step_type: str,
        model: str,
        tokens_used: int,
        duration_ms: int,
        quality_score: int,
        details: Optional[Dict] = None
    ) -> Dict:
        """
        작업 단계 기록
        
        Args:
            work_id: 작업 ID
            step_name: 단계 이름
            step_type: 단계 타입 (analysis, coding, review, etc)
            model: 사용 모델
            tokens_used: 사용한 토큰
            duration_ms: 소요 시간 (ms)
            quality_score: 품질 점수 (0-100)
            details: 상세 정보
        
        Returns:
            기록된 단계 정보
        """
        
        # 작업 찾기
        work = self._find_work(work_id)
        if not work:
            return {"error": f"작업 {work_id} 없음"}
        
        # 단계 생성
        step = {
            "step_id": f"{work_id}_step_{len(work['steps']) + 1}",
            "step_name": step_name,
            "step_type": step_type,
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "tokens_used": tokens_used,
            "duration_ms": duration_ms,
            "quality_score": quality_score,
            "efficiency": self._calculate_efficiency(quality_score, tokens_used, duration_ms),
            "details": details or {}
        }
        
        # 작업에 추가
        work["steps"].append(step)
        work["actual_tokens"] += tokens_used
        work["phase"] = WorkPhase.IN_PROGRESS.value
        
        self._save_work_log()
        
        return step
    
    def end_work(
        self,
        work_id: str,
        final_status: str,
        final_quality: int,
        summary: Optional[Dict] = None
    ) -> Dict:
        """
        작업 종료
        
        Args:
            work_id: 작업 ID
            final_status: success, partial, failure
            final_quality: 최종 품질 점수 (0-100)
            summary: 작업 요약
        
        Returns:
            작업 결과
        """
        
        work = self._find_work(work_id)
        if not work:
            return {"error": f"작업 {work_id} 없음"}
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(work["start_time"])
        duration = (end_time - start_time).total_seconds()
        
        # 작업 결과 계산
        work["phase"] = WorkPhase.COMPLETED.value if final_status == "success" else WorkPhase.FAILED.value
        work["end_time"] = end_time.isoformat()
        work["duration_seconds"] = duration
        work["final_status"] = final_status
        work["final_quality"] = final_quality
        work["summary"] = summary or {}
        
        # 효율 메트릭
        avg_step_quality = sum(s.get("quality_score", 0) for s in work["steps"]) / len(work["steps"]) if work["steps"] else 0
        avg_step_efficiency = sum(s.get("efficiency", 0) for s in work["steps"]) / len(work["steps"]) if work["steps"] else 0
        
        work["metrics"] = {
            "total_steps": len(work["steps"]),
            "avg_quality": round(avg_step_quality, 1),
            "avg_efficiency": round(avg_step_efficiency, 1),
            "token_efficiency": round(work["actual_tokens"] / max(1, duration / 60), 1),  # tokens/min
            "time_efficiency": round(duration / len(work["steps"]), 1) if work["steps"] else 0,  # sec/step
            "token_vs_estimate": round(work["actual_tokens"] / max(1, work["estimated_tokens"]), 2) if work["estimated_tokens"] else 0
        }
        
        self._save_work_log()
        
        return work
    
    def get_work_summary(self, work_id: str) -> Dict:
        """작업 요약 조회"""
        
        work = self._find_work(work_id)
        if not work:
            return {"error": f"작업 {work_id} 없음"}
        
        return {
            "work_id": work_id,
            "work_name": work["work_name"],
            "status": work.get("phase"),
            "task_type": work["task_type"],
            "neural_level": work["neural_level"],
            "priority": work["priority"],
            "start_time": work["start_time"],
            "end_time": work.get("end_time"),
            "duration_seconds": work.get("duration_seconds", 0),
            "steps": len(work["steps"]),
            "tokens_used": work["actual_tokens"],
            "final_quality": work.get("final_quality", 0),
            "metrics": work.get("metrics", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_daily_work_report(self) -> Dict:
        """일일 작업 리포트"""
        
        today = datetime.now().date().isoformat()
        today_works = [
            w for w in self.work_log["works"]
            if w["start_time"].startswith(today)
        ]
        
        if not today_works:
            return {"date": today, "total_works": 0}
        
        total_works = len(today_works)
        completed = sum(1 for w in today_works if w.get("phase") == WorkPhase.COMPLETED.value)
        failed = sum(1 for w in today_works if w.get("phase") == WorkPhase.FAILED.value)
        
        total_duration = sum(w.get("duration_seconds", 0) for w in today_works)
        total_tokens = sum(w["actual_tokens"] for w in today_works)
        avg_quality = sum(w.get("final_quality", 0) for w in today_works) / total_works if total_works > 0 else 0
        
        # 신경계별 통계
        neural_stats = {}
        for level in ["L1", "L2", "L3", "L4"]:
            level_works = [w for w in today_works if w["neural_level"] == level]
            if level_works:
                neural_stats[level] = {
                    "count": len(level_works),
                    "avg_quality": round(sum(w.get("final_quality", 0) for w in level_works) / len(level_works), 1),
                    "total_tokens": sum(w["actual_tokens"] for w in level_works)
                }
        
        return {
            "date": today,
            "total_works": total_works,
            "completed": completed,
            "failed": failed,
            "completion_rate": round(completed / total_works * 100, 1) if total_works > 0 else 0,
            "total_duration_hours": round(total_duration / 3600, 2),
            "total_tokens": total_tokens,
            "avg_quality": round(avg_quality, 1),
            "neural_stats": neural_stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_work(self, work_id: str) -> Optional[Dict]:
        """작업 찾기"""
        for work in self.work_log["works"]:
            if work["work_id"] == work_id:
                return work
        return None
    
    def _calculate_efficiency(
        self,
        quality_score: int,
        tokens_used: int,
        duration_ms: int
    ) -> float:
        """효율 점수 계산 (0-100)"""
        
        # 품질 (40%)
        quality_score_norm = quality_score / 100 * 0.4
        
        # 토큰 효율 (30%) - 적을수록 좋음
        token_score = min(1, 1000 / max(1, tokens_used)) * 0.3
        
        # 속도 (30%) - 빠를수록 좋음
        speed_score = min(1, 1000 / max(1, duration_ms)) * 0.3
        
        efficiency = (quality_score_norm + token_score + speed_score) * 100
        
        return round(efficiency, 1)
    
    def _save_work_log(self):
        """작업 로그 저장"""
        with open(self.work_log_path, "w", encoding="utf-8") as f:
            json.dump(self.work_log, f, indent=2, ensure_ascii=False)


# 사용 예시
if __name__ == "__main__":
    executor = WorkExecutor()
    
    print("🧠 작업 실행자 테스트\n")
    
    # 작업 1: 분석 작업
    work1 = executor.start_work(
        work_id="work_001",
        work_name="신경계 성능 분석",
        task_type="analysis",
        neural_level="L3",
        estimated_tokens=5000,
        priority="high"
    )
    print(f"✅ 작업 시작: {work1['work_name']}\n")
    
    # 단계 1: 데이터 수집
    step1 = executor.log_step(
        work_id="work_001",
        step_name="데이터 수집",
        step_type="analysis",
        model="Gemini",
        tokens_used=1000,
        duration_ms=2000,
        quality_score=95
    )
    print(f"📝 단계: {step1['step_name']} ({step1['quality_score']}/100)\n")
    
    # 단계 2: 분석
    step2 = executor.log_step(
        work_id="work_001",
        step_name="성능 분석",
        step_type="analysis",
        model="Claude",
        tokens_used=3000,
        duration_ms=4000,
        quality_score=92
    )
    print(f"📝 단계: {step2['step_name']} ({step2['quality_score']}/100)\n")
    
    # 작업 종료
    result = executor.end_work(
        work_id="work_001",
        final_status="success",
        final_quality=94,
        summary={"analysis": "완료"}
    )
    print(f"✅ 작업 완료")
    print(f"   상태: {result['final_status']}")
    print(f"   품질: {result['final_quality']}/100")
    print(f"   소요시간: {result['duration_seconds']:.1f}초")
    print(f"   토큰: {result['actual_tokens']}\n")
    
    # 일일 리포트
    report = executor.get_daily_work_report()
    print(f"📊 일일 리포트")
    print(f"   총 작업: {report['total_works']}")
    print(f"   완료: {report['completed']}")
    print(f"   성공률: {report['completion_rate']}%")
    print(f"   평균 품질: {report['avg_quality']}/100")
