"""
🧠 신경 실행자 (Neural Executor)
신경계 모델 할당을 기반으로 실제 작업 실행

역할: 신경 라우터에서 선택한 모델로 실제 작업 실행
특징: 모델 호출, 토큰 추적, 결과 평가, 점수 업데이트
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from enum import Enum


class ExecutionStatus(Enum):
    """실행 상태"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    API_ERROR = "api_error"
    TIMEOUT = "timeout"


class NeuralExecutor:
    """신경계 기반 작업 실행자"""
    
    def __init__(self):
        self.registry_path = Path(__file__).parent / "neural_model_registry.json"
        self.execution_log_path = Path(__file__).parent / "execution_log.json"
        self.registry = self._load_registry()
        self.execution_log = self._load_execution_log()
    
    def _load_registry(self) -> Dict:
        """레지스트리 로드"""
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"models": {}}
    
    def _load_execution_log(self) -> Dict:
        """실행 로그 로드"""
        try:
            with open(self.execution_log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"executions": []}
    
    def execute_with_neural_routing(
        self,
        task_id: str,
        task_name: str,
        neural_level: str,
        task_func: Callable,
        timeout_seconds: int = 30,
        *args,
        **kwargs
    ) -> Dict:
        """
        신경 라우팅을 통한 작업 실행
        
        Args:
            task_id: 작업 ID
            task_name: 작업 이름
            neural_level: L1-L4 신경계 레벨
            task_func: 실행할 함수
            timeout_seconds: 타임아웃
            *args, **kwargs: task_func에 전달할 인자
        
        Returns:
            실행 결과 및 평가
        """
        
        start_time = time.time()
        start_datetime = datetime.now().isoformat()
        
        # 1단계: 신경 라우팅으로 최적 모델 선택
        routing_result = self._route_to_model(neural_level)
        model_name = routing_result.get("model")
        
        if not model_name:
            return {
                "task_id": task_id,
                "task_name": task_name,
                "neural_level": neural_level,
                "status": ExecutionStatus.API_ERROR.value,
                "error": "사용 가능한 모델 없음",
                "timestamp": start_datetime,
                "duration_ms": 0
            }
        
        # 2단계: 작업 실행
        execution_result = self._execute_task(
            task_func,
            model_name,
            timeout_seconds,
            *args,
            **kwargs
        )
        
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)
        
        # 3단계: 결과 평가
        quality_score = self._evaluate_result(execution_result)
        
        # 4단계: 모델 점수 업데이트
        tokens_used = execution_result.get("tokens_used", 0)
        self._update_model_score(
            model_name,
            neural_level,
            execution_result["status"],
            quality_score,
            tokens_used,
            duration_ms
        )
        
        # 5단계: 결과 반환
        result = {
            "task_id": task_id,
            "task_name": task_name,
            "neural_level": neural_level,
            "model": model_name,
            "neurotransmitter": routing_result.get("neurotransmitter"),
            "status": execution_result["status"],
            "quality_score": quality_score,
            "tokens_used": tokens_used,
            "duration_ms": duration_ms,
            "response_time_percentile": self._get_response_percentile(model_name, duration_ms),
            "timestamp": start_datetime,
            "end_timestamp": datetime.now().isoformat(),
            "result": execution_result.get("result"),
            "error": execution_result.get("error")
        }
        
        # 로그에 저장
        self.execution_log["executions"].append(result)
        self._save_execution_log()
        
        return result
    
    def _route_to_model(self, neural_level: str) -> Dict:
        """신경 라우팅 (최적 모델 선택)"""
        
        best_model = None
        best_score = -1
        
        for model_name, model_data in self.registry["models"].items():
            # API 키 확인
            api_key_env = model_data.get("api_key_env")
            if not api_key_env or not os.getenv(api_key_env):
                continue
            
            # 신경계 레벨 점수
            if neural_level not in model_data["levels"]:
                continue
            
            level_score = model_data["levels"][neural_level]["score"]
            
            # 토큰 체크
            tokens = model_data["daily_tokens"]
            if tokens["used"] >= tokens["limit"] * 0.9:
                level_score *= 0.3
            
            if level_score > best_score:
                best_score = level_score
                best_model = model_name
        
        if not best_model:
            return {"model": None}
        
        return {
            "model": best_model,
            "score": best_score,
            "neurotransmitter": self.registry["models"][best_model].get("neurotransmitter")
        }
    
    def _execute_task(
        self,
        task_func: Callable,
        model_name: str,
        timeout_seconds: int,
        *args,
        **kwargs
    ) -> Dict:
        """실제 작업 실행"""
        
        try:
            # 모델 정보 추가
            model_data = self.registry["models"].get(model_name, {})
            kwargs["model"] = model_name
            kwargs["provider"] = model_data.get("provider")
            
            # 함수 실행
            start = time.time()
            result = task_func(*args, **kwargs)
            duration = time.time() - start
            
            # 타임아웃 체크
            if duration > timeout_seconds:
                return {
                    "status": ExecutionStatus.TIMEOUT.value,
                    "error": f"타임아웃 ({duration:.2f}s > {timeout_seconds}s)",
                    "result": result,
                    "tokens_used": 0
                }
            
            # 성공
            return {
                "status": ExecutionStatus.SUCCESS.value,
                "result": result,
                "tokens_used": kwargs.get("tokens_used", 0)
            }
        
        except Exception as e:
            return {
                "status": ExecutionStatus.FAILURE.value,
                "error": str(e),
                "result": None,
                "tokens_used": 0
            }
    
    def _evaluate_result(self, execution_result: Dict) -> int:
        """결과 평가 (0-100 점수)"""
        
        status = execution_result["status"]
        
        if status == ExecutionStatus.SUCCESS.value:
            return 100
        elif status == ExecutionStatus.PARTIAL.value:
            return 50
        elif status == ExecutionStatus.FAILURE.value:
            return 0
        elif status == ExecutionStatus.API_ERROR.value:
            return -10
        elif status == ExecutionStatus.TIMEOUT.value:
            return 25
        else:
            return 50
    
    def _update_model_score(
        self,
        model_name: str,
        neural_level: str,
        status: str,
        quality_score: int,
        tokens_used: int,
        response_time_ms: int
    ):
        """모델 점수 업데이트"""
        
        if model_name not in self.registry["models"]:
            return
        
        # 학습률 설정
        learning_rates = {
            ExecutionStatus.SUCCESS.value: 0.8,
            ExecutionStatus.PARTIAL.value: 0.9,
            ExecutionStatus.FAILURE.value: 0.5,
            ExecutionStatus.API_ERROR.value: 0.3,
            ExecutionStatus.TIMEOUT.value: 0.4
        }
        
        learning_rate = learning_rates.get(status, 0.5)
        
        # 점수 계산
        old_score = self.registry["models"][model_name]["levels"][neural_level]["score"]
        new_score = (old_score * learning_rate) + (quality_score * (1 - learning_rate))
        
        # 새로운 점수 저장
        self.registry["models"][model_name]["levels"][neural_level]["score"] = new_score
        
        # 통계 업데이트
        stats = self.registry["models"][model_name]["stats"]
        stats["total_calls"] += 1
        if status == ExecutionStatus.SUCCESS.value:
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1
        
        # 토큰 사용 추적
        self.registry["models"][model_name]["daily_tokens"]["used"] += tokens_used
        
        # 저장
        self._save_registry()
    
    def _get_response_percentile(self, model_name: str, response_time_ms: int) -> str:
        """응답시간 백분위"""
        
        # 일반적인 범위 (ms)
        if response_time_ms < 100:
            return "P99"  # 매우 빠름
        elif response_time_ms < 500:
            return "P95"  # 빠름
        elif response_time_ms < 1000:
            return "P75"  # 평균
        elif response_time_ms < 2000:
            return "P50"  # 느림
        else:
            return "P10"  # 매우 느림
    
    def _save_registry(self):
        """레지스트리 저장"""
        self.registry["last_updated"] = datetime.now().isoformat()
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def _save_execution_log(self):
        """실행 로그 저장"""
        with open(self.execution_log_path, "w", encoding="utf-8") as f:
            json.dump(self.execution_log, f, indent=2, ensure_ascii=False)
    
    def get_execution_summary(self) -> Dict:
        """실행 요약"""
        
        logs = self.execution_log["executions"]
        
        if not logs:
            return {"total": 0}
        
        total = len(logs)
        success = sum(1 for l in logs if l["status"] == ExecutionStatus.SUCCESS.value)
        avg_quality = sum(l.get("quality_score", 0) for l in logs) / total if total > 0 else 0
        avg_duration = sum(l.get("duration_ms", 0) for l in logs) / total if total > 0 else 0
        
        return {
            "total_executions": total,
            "success_count": success,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0,
            "avg_quality_score": round(avg_quality, 1),
            "avg_duration_ms": round(avg_duration, 0),
            "timestamp": datetime.now().isoformat()
        }


# 테스트용 함수
def sample_task(model=None, provider=None, tokens_used=100, **kwargs) -> Dict:
    """샘플 작업"""
    return {
        "result": f"작업 완료 ({model})",
        "tokens_used": tokens_used
    }


# 사용 예시
if __name__ == "__main__":
    executor = NeuralExecutor()
    
    print("🧠 신경 실행자 테스트\n")
    
    # 테스트: L1 뇌간 작업 (빠른 진단)
    result1 = executor.execute_with_neural_routing(
        task_id="task_001",
        task_name="빠른 진단",
        neural_level="L1",
        task_func=sample_task,
        tokens_used=50
    )
    
    print(f"✅ {result1['task_name']}")
    print(f"   모델: {result1['model']}")
    print(f"   상태: {result1['status']}")
    print(f"   시간: {result1['duration_ms']}ms\n")
    
    # 요약
    summary = executor.get_execution_summary()
    print(f"📊 실행 요약")
    print(f"   총 실행: {summary['total_executions']}")
    print(f"   성공률: {summary['success_rate']}%")
    print(f"   평균 점수: {summary['avg_quality_score']}/100")
