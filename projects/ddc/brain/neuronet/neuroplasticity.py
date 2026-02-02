
"""
신경가소성 (Neuroplasticity) v2.0 - Multi-Criteria Learning Engine
박사님 5계층 평가 프레임워크 통합 (효율성 계층 중심)

[핵심 개선]
1. Speed Score + Quality Score 분리
2. Layer별 가중치 차등 (L1: 속도80%, L3: 품질70%)
3. 토큰 효율성 추적
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class NeuroplasticityLearner:
    """
    Multi-Criteria Adaptive Learning Engine
    박사님 5계층 프레임워크 기반 강화학습
    """
    
    # [v3.0] Layer별 평가 가중치 (박사님 5계층 프레임워크 완전 반영)
    LAYER_WEIGHTS = {
        "L1": {  # Reflexive: 속도 + 신뢰성 최우선
            "speed": 0.45,
            "reliability": 0.30,  # [NEW] 성공률 × 일관성
            "cost": 0.15,
            "token_eff": 0.10
        },
        "L2": {  # Affective: 균형 + 일관성
            "speed": 0.25,
            "quality": 0.40,
            "reliability": 0.20,
            "memory": 0.15
        },
        "L3": {  # Cognitive: 품질 + 효율성
            "quality": 0.40,
            "token_eff": 0.25,
            "memory": 0.20,
            "speed": 0.15
        },
        "L4": {  # NeuroNet: 창의성 + 신뢰성
            "quality": 0.35,
            "token_eff": 0.25,
            "reliability": 0.20,
            "cost": 0.10,
            "speed": 0.10
        }
    }

    # [v3.0] 엔진별 초기 가상 점수 (6차원 Prior)
    ENGINE_PRIORS = {
        "Groq": {
            "speed": 0.99, "quality": 0.60, "token_eff": 0.90, 
            "cost": 0.95, "memory": 0.50, "reliability": 0.95
        },
        "Gemini": {
            "speed": 0.50, "quality": 0.95, "token_eff": 0.80, 
            "cost": 0.85, "memory": 0.70, "reliability": 0.85
        },
        "Claude": {
            "speed": 0.40, "quality": 0.99, "token_eff": 0.85, 
            "cost": 0.30, "memory": 0.60, "reliability": 0.70  # 크레딧 이슈
        },
        "DeepSeek": {
            "speed": 0.80, "quality": 0.70, "token_eff": 0.92, 
            "cost": 0.98, "memory": 0.65, "reliability": 0.85
        },
        "OpenAI": {
            "speed": 0.55, "quality": 0.90, "token_eff": 0.75, 
            "cost": 0.60, "memory": 0.70, "reliability": 0.80
        }
    }

    def __init__(self, memory_path=None):
        self.memory_path = memory_path or os.path.expanduser("~/.openclaw/workspace/neuro_memory.json")
        self.model_scores = {}
        self.learning_history = []
        self.learning_rate = 0.05
        
        self.load_weights()
    
    def load_weights(self):
        """저장된 학습 데이터 로드"""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # v2.0 체크
                    if data.get("version") == "2.0":
                        self.model_scores = data.get("model_scores", {})
                    else:
                        # v1 -> v2 변환 시에도 Prior 적용
                        logger.info("🔄 Converting v1 weights with Engine Priors...")
                        # v1 가중치를 기반으로 초기화
                        self.model_scores = self._convert_v1_to_v2(data.get("weights", {}))
                    
                    self.learning_history = data.get("history", [])
                    logger.info(f"🧠 Loaded neuro-memory: {len(self.model_scores)} models tracked")
            except Exception as e:
                logger.error(f"Failed to load neuro-memory: {e}")
        else:
            logger.info("🧠 No previous memory found. Starting fresh with Priors.")

    def _convert_v1_to_v2(self, old_weights: dict) -> dict:
        """v1 (단일 가중치) -> v3 (6차원 지표) 변환"""
        new_scores = {}
        for model_id, weight in old_weights.items():
            new_scores[model_id] = {
                "speed": 0.5,
                "quality": weight,
                "token_eff": 0.5,
                "cost": 0.5,
                "memory": 0.5,
                "reliability": 0.8,  # 초기 신뢰도
                "success_count": 0,
                "call_count": 0,
                "latency_history": []  # 속도 변동성 추적
            }
        return new_scores

    def save_weights(self):
        """학습 데이터 영구 저장 (v2 형식)"""
        try:
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
            data = {
                "version": "2.0",
                "model_scores": self.model_scores,
                "history": self.learning_history[-100:],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug("💾 Neuro-weights saved (v2).")
        except Exception as e:
            logger.error(f"Failed to save neuro-memory: {e}")

    def record_interaction(
        self, 
        user_id: str, 
        model_id: str, 
        context: dict, 
        latency_ms: float,
        quality_score: float = 0.8,
        tokens_used: int = 0,
        memory_latency: float = 0.0,
        is_success: bool = True  # [NEW] 성공/실패 명시
    ):
        """
        상호작용 기록 및 학습 (6-Criteria Hebbian Update + Reliability)
        """
        level = context.get("level", "L3")
        
        # 1. Speed Score 계산
        target_latency = {"L1": 1000, "L2": 3000, "L3": 10000, "L4": 5000}.get(level, 10000)
        speed_score = max(0.1, min(1.0, target_latency / max(latency_ms, 1)))
        
        # 2. Token Efficiency (토큰 효율성: 적을수록 좋음)
        # 1000토큰 기준으로 정규화 (0~1000 토큰 -> 1.0~0.0)
        token_eff_score = max(0.1, min(1.0, 1.0 - (tokens_used / 2000.0)))
        
        # 3. Cost (비용 효율성: 모델별 단가 고려)
        # 간단한 추정: Groq/DeepSeek = 저렴(0.9), Gemini = 중간(0.7), Claude/OpenAI = 비쌈(0.3)
        cost_score = 0.7  # 기본값 (추후 실제 API 단가 반영)
        
        # 4. Memory Overhead (메모리 부담도: 낮을수록 좋음)
        total_time = latency_ms + memory_latency
        memory_score = 1.0 - (memory_latency / max(total_time, 1)) if total_time > 0 else 1.0
        
        # 5. Model Scores 업데이트 (v3.1: 6차원 + Reliability)
        if model_id not in self.model_scores:
            self.model_scores[model_id] = {
                "speed": 0.5,
                "quality": 0.5,
                "token_eff": 0.5,
                "cost": 0.5,
                "memory": 0.5,
                "reliability": 0.8,
                "success_count": 0,
                "call_count": 0,
                "latency_history": []
            }
        
        current = self.model_scores[model_id]
        
        # Success Rate 업데이트
        if is_success:
            current["success_count"] += 1
        current["call_count"] += 1
        success_rate = current["success_count"] / max(current["call_count"], 1)
        
        # Latency Variance (일관성) 계산
        current["latency_history"].append(latency_ms)
        if len(current["latency_history"]) > 20:  # 최근 20개만 유지
            current["latency_history"] = current["latency_history"][-20:]
        
        import statistics
        if len(current["latency_history"]) > 2:
            stdev = statistics.stdev(current["latency_history"])
            mean = statistics.mean(current["latency_history"])
            # CV (Coefficient of Variation): 낮을수록 일관적
            cv = stdev / max(mean, 1)
            consistency = max(0.1, 1.0 - min(cv, 1.0))  # 변동 클수록 낮음
        else:
            consistency = 0.8  # 초기값
        
        # Reliability = Success Rate × Consistency
        reliability_score = success_rate * consistency
        
        # 학습 반영
        current["speed"] += self.learning_rate * (speed_score - current["speed"])
        current["quality"] += self.learning_rate * (quality_score - current["quality"])
        current["token_eff"] += self.learning_rate * (token_eff_score - current["token_eff"])
        current["cost"] += self.learning_rate * (cost_score - current["cost"])
        current["memory"] += self.learning_rate * (memory_score - current["memory"])
        current["reliability"] += self.learning_rate * (reliability_score - current["reliability"])
        
        # 3. History Logging
        record = {
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "model": model_id,
            "level": level,
            "latency_ms": latency_ms,
            "speed_score": speed_score,
            "quality_score": quality_score,
            "tokens": tokens_used,
            "memory_ms": memory_latency
        }
        self.learning_history.append(record)
        
        # 4. Auto Save
        self.save_weights()
        logger.info(f"🧠 Learning: {model_id} | Speed={speed_score:.2f} Quality={quality_score:.2f}")

    def select_best_model(self, level: str, candidates: List[dict]) -> str:
        """
        Layer별 가중치를 적용한 최적 모델 선택 (v3.1: 6차원 지표)
        """
        if not candidates:
            return "gemini-2.0-flash"
        
        # 1. Exploration (10%)
        if len(candidates) > 1 and (hash(datetime.now()) % 100) < 10:
            picked = candidates[hash(datetime.now()) % len(candidates)]
            return picked["id"]
        
        # 2. Exploitation (6차원 가중 합산)
        weights = self.LAYER_WEIGHTS.get(level, {"speed": 0.5, "quality": 0.5})
        best_model = candidates[0]
        best_score = -1.0
        
        for model in candidates:
            model_id = model["id"]
            engine = model.get("engine", "Unknown")
            
            # 모델 점수 조회 (없으면 박사님 Priors 적용)
            if model_id not in self.model_scores:
                prior = self.ENGINE_PRIORS.get(engine, {
                    "speed": 0.5, "quality": 0.5, "token_eff": 0.5, 
                    "cost": 0.5, "memory": 0.5, "reliability": 0.8
                })
                scores = prior
            else:
                scores = self.model_scores[model_id]
            
            # 가중 합산 (지표별로 가중치 있으면 적용, 없으면 Skip)
            final_score = 0.0
            for metric, weight in weights.items():
                final_score += scores.get(metric, 0.5) * weight
            
            # 노이즈 추가
            noise = (hash(model_id + str(datetime.now())) % 100) / 10000.0
            final_score += noise
            
            if final_score > best_score:
                best_score = final_score
                best_model = model
                
        logger.info(f"🧠 [{level}] Select: {best_model['id']} | Score={best_score:.3f}")
        return best_model["id"]
    
    def rank_models(self, level: str, candidates: List[dict]) -> List[tuple[dict, float]]:
        """
        신경가소성 학습 데이터 기반으로 모든 후보를 점수 순으로 정렬
        
        Returns:
            List[(model_dict, score)]: 점수 내림차순 정렬된 (모델, 점수) 튜플 리스트
        """
        if not candidates:
            return []
        
        weights = self.LAYER_WEIGHTS.get(level, {"speed": 0.5, "quality": 0.5})
        ranked = []
        
        for model in candidates:
            model_id = model["id"]
            engine = model.get("engine", "Unknown")
            
            # 모델 점수 조회 (없으면 Priors 적용)
            if model_id not in self.model_scores:
                prior = self.ENGINE_PRIORS.get(engine, {
                    "speed": 0.5, "quality": 0.5, "token_eff": 0.5, 
                    "cost": 0.5, "memory": 0.5, "reliability": 0.8
                })
                scores = prior
            else:
                scores = self.model_scores[model_id]
            
            # 가중 합산
            final_score = 0.0
            for metric, weight in weights.items():
                final_score += scores.get(metric, 0.5) * weight
            
            ranked.append((model, final_score))
        
        # 점수 내림차순 정렬
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"🧠 [{level}] Ranked {len(ranked)} models | Top: {ranked[0][0]['id']} ({ranked[0][1]:.3f})")
        return ranked
