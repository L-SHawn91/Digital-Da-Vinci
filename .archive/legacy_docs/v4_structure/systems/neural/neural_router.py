"""
🧠 신경 라우터 (Neural Router)
D-CNS 신경계별 최적 모델 자동 선택 시스템

역할: 작업의 신경계 레벨에 따라 최적의 모델을 동적으로 선택
특징: 실시간 토큰 추적, 강화학습 기반 점수 업데이트
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class NeuralModelRouter:
    """신경계 기반 지능형 모델 라우터"""
    
    def __init__(self):
        self.registry_path = Path(__file__).parent / "neural_model_registry.json"
        self.registry = self._load_registry()
    
    def select_model(self, neural_level: str, task_type: str = "general") -> Dict:
        """
        신경계 레벨에 따라 최적 모델 선택
        
        Args:
            neural_level: "L1" | "L2" | "L3" | "L4"
            task_type: 작업 유형 (일반)
        
        Returns:
            {
                "primary": "Groq",
                "score": 92.3,
                "level": "L1",
                "neurotransmitter": "노르에피네프린",
                "alternatives": [("DeepSeek", 85.7), ...],
                "reason": "빠른 진단 필요"
            }
        """
        
        if neural_level not in ["L1", "L2", "L3", "L4"]:
            return {"error": f"Invalid neural level: {neural_level}"}
        
        # 1. 신경계별 가중치로 점수 재계산
        scores = {}
        for model_name, model_data in self.registry["models"].items():
            if neural_level in model_data["levels"]:
                level_score = model_data["levels"][neural_level]["score"]
                
                # 토큰 가용성 확인
                tokens = model_data["daily_tokens"]
                token_availability = tokens["used"] / tokens["limit"]
                
                # 토큰 90% 이상 사용 시 제외
                if token_availability >= 0.90:
                    continue
                
                scores[model_name] = {
                    "score": level_score,
                    "neurotransmitter": model_data["neurotransmitter"],
                    "token_available": tokens["limit"] - tokens["used"]
                }
        
        if not scores:
            return {
                "error": "모든 모델 토큰 부족",
                "fallback": "Groq",
                "recommendation": "토큰 리셋 대기"
            }
        
        # 2. 최적 모델 선택
        best_model = max(scores.items(), key=lambda x: x[1]["score"])
        
        # 3. 대체 모델 목록
        alternatives = sorted(
            [(name, data["score"]) for name, data in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )[1:]
        
        return {
            "primary": best_model[0],
            "score": best_model[1]["score"],
            "neurotransmitter": best_model[1]["neurotransmitter"],
            "level": neural_level,
            "task_type": task_type,
            "alternatives": alternatives,
            "reason": self._explain_choice(neural_level, best_model[0]),
            "token_remaining": best_model[1]["token_available"]
        }
    
    def update_score(
        self,
        neural_level: str,
        model: str,
        result: Dict
    ) -> Dict:
        """
        강화학습으로 모델 점수 업데이트
        
        Args:
            neural_level: "L1" | "L2" | "L3" | "L4"
            model: 모델명
            result: {
                "status": "success" | "partial" | "failure" | "api_error",
                "quality_score": 0-100 (optional),
                "response_time_ms": 123,
                "tokens_used": 456
            }
        
        Returns:
            {
                "model": "Groq",
                "level": "L1",
                "old_score": 92.3,
                "new_score": 93.1,
                "change": "+0.8"
            }
        """
        
        if model not in self.registry["models"]:
            return {"error": f"Unknown model: {model}"}
        
        # 1. 성공도 판정
        status = result.get("status", "unknown")
        
        if status == "success":
            quality = result.get("quality_score", 100)
            learning_rate = 0.8
            bonus = 10
        elif status == "partial":
            quality = 50
            learning_rate = 0.9
            bonus = 0
        elif status == "failure":
            quality = 0
            learning_rate = 0.5
            bonus = -20
        elif status == "api_error":
            quality = -10
            learning_rate = 0.3
            bonus = -30
        else:
            quality = 25
            learning_rate = 0.7
            bonus = 0
        
        # 2. 점수 계산 (강화학습)
        old_score = self.registry["models"][model]["levels"][neural_level]["score"]
        new_score = (old_score * learning_rate) + (quality * (1 - learning_rate)) + bonus
        new_score = max(0, min(100, new_score))
        
        # 3. 점수 업데이트
        self.registry["models"][model]["levels"][neural_level]["score"] = new_score
        
        # 4. 통계 업데이트
        self.registry["models"][model]["stats"]["total_calls"] += 1
        if status == "success":
            self.registry["models"][model]["stats"]["success_count"] += 1
        else:
            self.registry["models"][model]["stats"]["failure_count"] += 1
        
        self.registry["models"][model]["stats"]["last_success"] = datetime.now().isoformat()
        
        # 5. 토큰 사용량 업데이트
        tokens_used = result.get("tokens_used", 0)
        self.registry["models"][model]["daily_tokens"]["used"] += tokens_used
        
        # 6. 저장
        self._save_registry()
        
        change = new_score - old_score
        
        return {
            "model": model,
            "level": neural_level,
            "status": status,
            "old_score": round(old_score, 1),
            "new_score": round(new_score, 1),
            "change": f"{change:+.1f}",
            "learning_rate": learning_rate,
            "tokens_used": tokens_used,
            "total_tokens_used": self.registry["models"][model]["daily_tokens"]["used"]
        }
    
    def get_neural_allocation_report(self, task_name: str, neural_levels: List[str]) -> Dict:
        """
        작업의 신경계 할당 리포트 생성
        
        Args:
            task_name: 작업 이름
            neural_levels: 사용할 신경계 레벨 목록
        
        Returns:
            {
                "task": "작업명",
                "neural_levels": ["L1", "L2", ...],
                "allocations": {
                    "L1": {"primary": "Groq", "score": 92.3, ...},
                    ...
                },
                "total_efficiency": 9.5,
                "estimated_cost": 0.015
            }
        """
        
        allocations = {}
        scores = []
        
        for level in neural_levels:
            allocation = self.select_model(level)
            allocations[level] = allocation
            if "score" in allocation:
                scores.append(allocation["score"])
        
        avg_efficiency = sum(scores) / len(scores) if scores else 0
        total_efficiency = (avg_efficiency / 100) * 10  # 10점 만점
        
        return {
            "task": task_name,
            "neural_levels": neural_levels,
            "allocations": allocations,
            "total_efficiency": round(total_efficiency, 1),
            "estimated_cost": round(len(neural_levels) * 0.01, 4),
            "timestamp": datetime.now().isoformat()
        }
    
    def _explain_choice(self, neural_level: str, model: str) -> str:
        """모델 선택 이유 설명"""
        
        reasons = {
            "L1": "빠른 진단 필요",
            "L2": "정확한 우선순위 판단",
            "L3": "복잡한 분석 & 창의성",
            "L4": "라우팅 & 최적화"
        }
        
        return f"{reasons.get(neural_level, '작업 실행')} - {model}"
    
    def _load_registry(self) -> Dict:
        """레지스트리 로드"""
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"models": {}, "version": "2.0"}
    
    def _save_registry(self):
        """레지스트리 저장"""
        self.registry["last_updated"] = datetime.now().isoformat()
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)


# 사용 예시
if __name__ == "__main__":
    router = NeuralModelRouter()
    
    # 1. 신경계별 모델 선택
    print("🧠 L1 뇌간 - 빠른 진단")
    result_l1 = router.select_model("L1")
    print(f"선택: {result_l1['primary']} ({result_l1['score']:.1f}%)\n")
    
    # 2. 작업 할당 리포트
    print("📋 작업 신경계 할당")
    report = router.get_neural_allocation_report(
        "Workspace 정리",
        ["L1", "L2", "L3", "L4"]
    )
    print(f"작업: {report['task']}")
    print(f"전체 효율: {report['total_efficiency']}/10")
    print(f"예상 비용: ${report['estimated_cost']}")
