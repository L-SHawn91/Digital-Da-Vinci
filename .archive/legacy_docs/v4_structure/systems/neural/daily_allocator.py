"""
🧠 일일 신경 할당자 (Daily Neural Allocator)
신경계 기반 일일 작업 모델 할당 시스템

역할: 매일 08:00, 12:00, 17:00에 실행되어 최적 모델 할당
특징: 시간대별 작업 특성 반영, 토큰 사용량 자동 관리
"""

import json
import os
from datetime import datetime, time
from pathlib import Path
from typing import Dict, List, Tuple
from enum import Enum


class TimeOfDay(Enum):
    """하루의 시간대"""
    MORNING = "morning"      # 06:00-11:00
    AFTERNOON = "afternoon"  # 11:00-17:00
    EVENING = "evening"      # 17:00-23:00
    NIGHT = "night"          # 23:00-06:00


class DailyNeuralAllocator:
    """일일 신경 할당자"""
    
    def __init__(self):
        self.registry_path = Path(__file__).parent / "neural_model_registry.json"
        self.allocations_path = Path(__file__).parent / "daily_allocations.json"
        self.registry = self._load_registry()
        self.allocations = self._load_allocations()
    
    def _load_registry(self) -> Dict:
        """신경 모델 레지스트리 로드"""
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"models": {}, "version": "2.1"}
    
    def _load_allocations(self) -> Dict:
        """일일 할당 이력 로드"""
        try:
            with open(self.allocations_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"allocations": []}
    
    def get_time_of_day(self) -> TimeOfDay:
        """현재 시간대 판정"""
        hour = datetime.now().hour
        
        if 6 <= hour < 11:
            return TimeOfDay.MORNING
        elif 11 <= hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour < 23:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
    
    def get_daily_work_characteristics(self, time_of_day: TimeOfDay) -> Dict:
        """시간대별 작업 특성"""
        
        characteristics = {
            TimeOfDay.MORNING: {
                "priority": "planning",          # 계획, 의사결정
                "neural_levels": ["L2", "L3"],  # 변린계, 신피질
                "task_types": ["analysis", "strategy", "design"],
                "speed_priority": False,
                "cost_priority": False,
                "quality_priority": True,
            },
            TimeOfDay.AFTERNOON: {
                "priority": "execution",         # 실행, 구현
                "neural_levels": ["L3", "L4"],  # 신피질, 신경망
                "task_types": ["coding", "integration", "testing"],
                "speed_priority": False,
                "cost_priority": True,
                "quality_priority": True,
            },
            TimeOfDay.EVENING: {
                "priority": "monitoring",        # 모니터링, 리뷰
                "neural_levels": ["L1", "L4"],  # 뇌간, 신경망
                "task_types": ["monitoring", "review", "report"],
                "speed_priority": True,
                "cost_priority": False,
                "quality_priority": False,
            },
            TimeOfDay.NIGHT: {
                "priority": "optimization",      # 최적화, 자동화
                "neural_levels": ["L4"],        # 신경망
                "task_types": ["optimization", "learning", "maintenance"],
                "speed_priority": False,
                "cost_priority": True,
                "quality_priority": False,
            }
        }
        
        return characteristics.get(time_of_day, {})
    
    def allocate_daily_models(self) -> Dict:
        """
        일일 모델 할당 실행
        
        Returns:
            {
                "timestamp": "2026-02-01T19:09:00",
                "time_of_day": "evening",
                "allocations": {
                    "L1": {"model": "Cerebras", "reason": "초고속"},
                    "L2": {"model": "Gemini", "reason": "의사결정"},
                    "L3": {"model": "Claude", "reason": "고급분석"},
                    "L4": {"model": "DeepSeek", "reason": "라우팅최적화"}
                },
                "token_budget": {...},
                "cost_estimate": 0.015
            }
        """
        
        time_of_day = self.get_time_of_day()
        characteristics = self.get_daily_work_characteristics(time_of_day)
        
        allocations = {}
        total_cost = 0
        
        # L1-L4 각 신경계별 모델 할당
        for level in ["L1", "L2", "L3", "L4"]:
            best_model = self._select_best_model_for_level(
                level,
                characteristics
            )
            
            if best_model:
                model_name = best_model["model"]
                model_data = self.registry["models"][model_name]
                
                allocations[level] = {
                    "model": model_name,
                    "score": best_model["score"],
                    "neurotransmitter": model_data.get("neurotransmitter"),
                    "tier": model_data.get("tier"),
                    "reason": best_model["reason"],
                    "cost_per_1k": model_data["levels"][level].get("cost_per_1k_tokens", 0),
                    "tokens_available": model_data["daily_tokens"]["limit"] - model_data["daily_tokens"]["used"]
                }
                
                total_cost += allocations[level]["cost_per_1k"]
        
        # 토큰 예산 계산
        token_budget = self._calculate_token_budget(time_of_day)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time_of_day": time_of_day.value,
            "priority": characteristics.get("priority"),
            "allocations": allocations,
            "token_budget": token_budget,
            "cost_estimate": round(total_cost, 6),
            "status": "allocated"
        }
        
        # 저장
        self.allocations["allocations"].append(result)
        self._save_allocations()
        
        return result
    
    def _select_best_model_for_level(
        self,
        neural_level: str,
        characteristics: Dict
    ) -> Dict:
        """신경계 레벨과 특성에 따른 최적 모델 선택"""
        
        scores = {}
        
        for model_name, model_data in self.registry["models"].items():
            if neural_level not in model_data["levels"]:
                continue
            
            # API 키 확인
            api_key_env = model_data.get("api_key_env")
            if not api_key_env or not os.getenv(api_key_env):
                continue
            
            # 신경계 레벨 점수
            level_score = model_data["levels"][neural_level]["score"]
            
            # 토큰 가용성 체크
            tokens = model_data["daily_tokens"]
            if tokens["used"] >= tokens["limit"] * 0.9:
                level_score *= 0.3  # 토큰 부족 패널티
            
            # 시간대 특성 반영
            if characteristics.get("speed_priority"):
                # 빠른 응답 필요
                response_ms = model_data["levels"][neural_level].get("avg_response_ms", 1000)
                level_score = (level_score * 0.6) + ((5000 - response_ms) / 5000 * 100 * 0.4)
            
            if characteristics.get("cost_priority"):
                # 저비용 필요
                cost = model_data["levels"][neural_level].get("cost_per_1k_tokens", 0.001)
                level_score = (level_score * 0.6) + ((0.01 - cost) / 0.01 * 100 * 0.4)
            
            if characteristics.get("quality_priority"):
                # 품질 중시
                level_score = (level_score * 0.9)
            
            scores[model_name] = {
                "score": level_score,
                "tier": model_data.get("tier")
            }
        
        if not scores:
            return None
        
        best = max(scores.items(), key=lambda x: x[1]["score"])
        
        return {
            "model": best[0],
            "score": round(best[1]["score"], 1),
            "reason": self._explain_selection(neural_level, best[0])
        }
    
    def _calculate_token_budget(self, time_of_day: TimeOfDay) -> Dict:
        """시간대별 토큰 예산 계산"""
        
        budgets = {
            TimeOfDay.MORNING: {
                "L1": 2000,   # 뇌간: 계획 (필요 적음)
                "L2": 5000,   # 변린계: 의사결정 (필요 중)
                "L3": 8000,   # 신피질: 분석 (필요 많음)
                "L4": 3000,   # 신경망: 라우팅 (필요 적음)
            },
            TimeOfDay.AFTERNOON: {
                "L1": 3000,
                "L2": 4000,
                "L3": 10000,  # 구현 (가장 많이 필요)
                "L4": 5000,
            },
            TimeOfDay.EVENING: {
                "L1": 5000,   # 모니터링 (빠른 처리)
                "L2": 2000,
                "L3": 3000,
                "L4": 8000,   # 라우팅 최적화
            },
            TimeOfDay.NIGHT: {
                "L1": 1000,
                "L2": 1000,
                "L3": 1000,
                "L4": 10000,  # 자동화, 최적화
            }
        }
        
        return budgets.get(time_of_day, {})
    
    def _explain_selection(self, neural_level: str, model: str) -> str:
        """모델 선택 이유"""
        
        reasons = {
            "L1": f"{model} - 빠른 진단",
            "L2": f"{model} - 의사결정",
            "L3": f"{model} - 고급 분석",
            "L4": f"{model} - 라우팅 최적화"
        }
        
        return reasons.get(neural_level, f"{model} - 선택됨")
    
    def _save_allocations(self):
        """할당 정보 저장"""
        with open(self.allocations_path, "w", encoding="utf-8") as f:
            json.dump(self.allocations, f, indent=2, ensure_ascii=False)
    
    def get_allocation_report(self) -> str:
        """할당 리포트 생성"""
        
        if not self.allocations["allocations"]:
            return "할당 정보 없음"
        
        latest = self.allocations["allocations"][-1]
        
        report = []
        report.append("🧠 일일 신경 할당 리포트")
        report.append(f"📅 {latest['date']}")
        report.append(f"⏰ {latest['time_of_day'].upper()}")
        report.append(f"🎯 우선순위: {latest['priority']}")
        report.append("")
        
        for level, alloc in latest["allocations"].items():
            report.append(f"{level} {alloc['neurotransmitter']}")
            report.append(f"   ✅ 모델: {alloc['model']} ({alloc['tier']})")
            report.append(f"   📊 점수: {alloc['score']}%")
            report.append(f"   💰 비용: ${alloc['cost_per_1k']:.6f}/1K")
            report.append(f"   📦 토큰: {alloc['tokens_available']:,}개 남음")
            report.append("")
        
        report.append(f"💵 예상 비용: ${latest['cost_estimate']:.6f}")
        
        return "\n".join(report)


# 사용 예시
if __name__ == "__main__":
    allocator = DailyNeuralAllocator()
    
    print("🧠 일일 신경 할당자 시작\n")
    
    # 일일 할당 실행
    result = allocator.allocate_daily_models()
    
    # 리포트 출력
    print(allocator.get_allocation_report())
    
    print("\n✅ 일일 할당 완료!")
