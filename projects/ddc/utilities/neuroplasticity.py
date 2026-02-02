"""
신경가소성 학습 시스템 - 자동 최적화

역할:
- 성능 데이터 기반 학습
- 신경 가중치 자동 조정
- 적응형 임계값 관리
- 장기 메모리 저장
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics
import json


@dataclass
class NeuralWeight:
    """신경 가중치"""
    layer: str  # L1, L2, L3, L4
    model: str  # 사용 모델
    base_weight: float  # 기본값 (0-1)
    current_weight: float  # 현재값
    adjustment_history: List[float]  # 조정 이력
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class NeuroplasticityEngine:
    """신경가소성 엔진"""
    
    def __init__(self):
        # 신경 가중치 초기화
        self.weights = {
            'L1_Brainstem': NeuralWeight('L1', 'groq', 0.15, 0.15, []),
            'L2_Limbic': NeuralWeight('L2', 'gemini_flash', 0.12, 0.12, []),
            'L3_Neocortex_Occipital': NeuralWeight('L3', 'gemini_2_5_pro', 0.15, 0.15, []),
            'L3_Neocortex_Temporal': NeuralWeight('L3', 'claude_opus', 0.15, 0.15, []),
            'L3_Neocortex_Parietal': NeuralWeight('L3', 'deepseek', 0.12, 0.12, []),
            'L3_Neocortex_Prefrontal': NeuralWeight('L3', 'claude_opus', 0.18, 0.18, []),
            'L4_NeuroNet': NeuralWeight('L4', 'gemini_2_5_pro', 0.13, 0.13, [])
        }
        
        # 적응형 임계값
        self.adaptive_thresholds = {
            'api_latency_ms': 100,
            'error_rate_percent': 5,
            'cache_hit_rate_percent': 50,
            'neural_health': 0.7
        }
        
        self.performance_history = []
        self.learning_rate = 0.01  # 학습률
        self.min_weight = 0.05
        self.max_weight = 0.30
    
    def learn_from_performance(
        self,
        metrics: Dict[str, float],
        outcomes: Dict[str, bool]
    ) -> Dict[str, float]:
        """성능 데이터로부터 학습"""
        adjustments = {}
        
        # 각 신경 계층별 학습
        for weight_key, weight in self.weights.items():
            # 성공률 계산
            successes = sum(outcomes.values())
            total = len(outcomes)
            success_rate = successes / total if total > 0 else 0
            
            # 성능 점수 계산 (0-1)
            api_score = max(0, 1 - (metrics.get('api_latency_ms', 100) / 200))
            cache_score = metrics.get('cache_hit_rate_percent', 50) / 100
            success_score = success_rate
            
            # 종합 점수
            performance_score = (api_score + cache_score + success_score) / 3
            
            # 가중치 조정
            adjustment = (performance_score - 0.5) * self.learning_rate
            new_weight = max(self.min_weight, min(self.max_weight, weight.current_weight + adjustment))
            
            # 히스토리 기록
            weight.adjustment_history.append(adjustment)
            if len(weight.adjustment_history) > 100:
                weight.adjustment_history = weight.adjustment_history[-100:]
            
            weight.current_weight = new_weight
            weight.last_updated = datetime.now()
            
            adjustments[weight_key] = {
                'previous': weight.current_weight - adjustment,
                'new': new_weight,
                'adjustment': adjustment,
                'performance_score': performance_score
            }
        
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'adjustments': adjustments
        })
        
        return adjustments
    
    def get_optimized_weights(self) -> Dict[str, float]:
        """최적화된 가중치 조회"""
        return {
            key: weight.current_weight
            for key, weight in self.weights.items()
        }
    
    def adapt_thresholds(self, recent_metrics: List[Dict[str, float]]):
        """임계값 자동 조정"""
        if len(recent_metrics) < 10:
            return
        
        # 최근 메트릭 분석
        api_latencies = [m.get('api_latency_ms', 100) for m in recent_metrics]
        error_rates = [m.get('error_rate_percent', 5) for m in recent_metrics]
        cache_hits = [m.get('cache_hit_rate_percent', 50) for m in recent_metrics]
        neural_healths = [m.get('neural_health', 0.7) for m in recent_metrics]
        
        # 동적 임계값 계산 (P95)
        self.adaptive_thresholds['api_latency_ms'] = sorted(api_latencies)[int(len(api_latencies) * 0.95)]
        self.adaptive_thresholds['error_rate_percent'] = statistics.mean(error_rates) * 1.5
        self.adaptive_thresholds['cache_hit_rate_percent'] = statistics.mean(cache_hits) * 0.9
        self.adaptive_thresholds['neural_health'] = statistics.mean(neural_healths) * 0.95
    
    def predict_performance(self, lookback_hours: int = 24) -> Dict[str, Any]:
        """성능 예측"""
        recent_history = [
            h for h in self.performance_history
            if datetime.fromisoformat(h['timestamp']) > datetime.now() - timedelta(hours=lookback_hours)
        ]
        
        if len(recent_history) < 5:
            return {'status': 'insufficient_data'}
        
        # 트렌드 분석
        api_trend = []
        for h in recent_history:
            api_trend.append(h['metrics'].get('api_latency_ms', 100))
        
        # 선형 회귀로 추세 계산
        if len(api_trend) >= 2:
            slope = (api_trend[-1] - api_trend[0]) / len(api_trend)
            predicted_latency = api_trend[-1] + slope
        else:
            predicted_latency = api_trend[-1] if api_trend else 100
        
        return {
            'predicted_api_latency_ms': round(predicted_latency, 2),
            'trend': 'improving' if slope < 0 else 'degrading',
            'confidence': 'high' if len(api_trend) > 20 else 'medium'
        }


class LongTermMemory:
    """장기 메모리 저장"""
    
    def __init__(self):
        self.memory_entries = []
    
    def save_learning(self, learning_data: Dict[str, Any]) -> str:
        """학습 결과 저장"""
        entry = {
            'id': f"mem_{len(self.memory_entries)}_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'data': learning_data,
            'importance': self._calculate_importance(learning_data)
        }
        
        self.memory_entries.append(entry)
        
        # 중요도 순으로 정렬하여 상위 100개만 유지
        self.memory_entries.sort(key=lambda x: x['importance'], reverse=True)
        if len(self.memory_entries) > 100:
            self.memory_entries = self.memory_entries[:100]
        
        return entry['id']
    
    def _calculate_importance(self, data: Dict[str, Any]) -> float:
        """중요도 계산"""
        importance = 0
        
        if 'performance_improvement' in data:
            importance += data['performance_improvement'] * 10
        
        if 'anomaly_detected' in data and data['anomaly_detected']:
            importance += 5
        
        if 'model_change' in data:
            importance += 3
        
        return min(importance, 10)  # 최대 10
    
    def get_important_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        """중요한 메모리 조회"""
        return self.memory_entries[:count]
    
    def export_to_json(self) -> str:
        """JSON으로 내보내기"""
        return json.dumps(self.memory_entries, indent=2)


class AdaptiveSystem:
    """적응형 시스템"""
    
    def __init__(self):
        self.neuroplasticity = NeuroplasticityEngine()
        self.memory = LongTermMemory()
        self.last_adaptation = datetime.now()
        self.adaptation_interval = timedelta(minutes=5)
    
    def run_learning_cycle(
        self,
        metrics: Dict[str, float],
        outcomes: Dict[str, bool],
        recent_metrics: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """학습 사이클 실행"""
        
        # 1. 신경가소성 학습
        adjustments = self.neuroplasticity.learn_from_performance(metrics, outcomes)
        
        # 2. 임계값 적응
        self.neuroplasticity.adapt_thresholds(recent_metrics)
        
        # 3. 성능 예측
        prediction = self.neuroplasticity.predict_performance()
        
        # 4. 학습 결과 저장
        learning_data = {
            'adjustments': adjustments,
            'thresholds': self.neuroplasticity.adaptive_thresholds,
            'prediction': prediction,
            'timestamp': datetime.now().isoformat()
        }
        
        memory_id = self.memory.save_learning(learning_data)
        
        # 마지막 적응 시간 업데이트
        self.last_adaptation = datetime.now()
        
        return {
            'status': 'success',
            'adjustments': adjustments,
            'prediction': prediction,
            'memory_id': memory_id,
            'weights': self.neuroplasticity.get_optimized_weights()
        }
    
    def should_adapt(self) -> bool:
        """적응 필요 여부"""
        return datetime.now() - self.last_adaptation >= self.adaptation_interval
    
    def get_system_report(self) -> Dict[str, Any]:
        """시스템 리포트"""
        return {
            'timestamp': datetime.now().isoformat(),
            'weights': self.neuroplasticity.get_optimized_weights(),
            'thresholds': self.neuroplasticity.adaptive_thresholds,
            'memory_count': len(self.memory.memory_entries),
            'important_memories': self.memory.get_important_memories(5)
        }


if __name__ == "__main__":
    print("🧠 신경가소성 학습 시스템 테스트\n")
    
    system = AdaptiveSystem()
    
    # 테스트 데이터
    metrics = {
        'api_latency_ms': 55,
        'error_rate_percent': 0.5,
        'cache_hit_rate_percent': 87,
        'neural_health': 0.96
    }
    
    outcomes = {
        'bio_analysis': True,
        'stock_analysis': True,
        'text_analysis': True,
        'decision': True
    }
    
    recent_metrics = [
        {'api_latency_ms': 50 + i*2, 'cache_hit_rate_percent': 85 + i}
        for i in range(20)
    ]
    
    # 학습 사이클 실행
    result = system.run_learning_cycle(metrics, outcomes, recent_metrics)
    
    print("✅ 학습 완료!")
    print(f"적응된 가중치: {system.neuroplasticity.get_optimized_weights()}")
    print(f"메모리 저장: {result['memory_id']}")
