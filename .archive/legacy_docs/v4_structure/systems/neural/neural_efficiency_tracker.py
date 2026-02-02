"""
# neural_efficiency_tracker.py - 신경계 효율 추적 시스템

신경계별, 모델별 효율성을 매번 체크하고 기록하는 시스템

용도:
  ├─ 각 신경계(L1-L4)가 어떤 모델을 사용했는지 추적
  ├─ 각 모델의 효율 점수 (0-10)
  ├─ 신경계별 기여도 측정
  ├─ 시간 경과에 따른 효율 개선 추적
  └─ 마일스톤 달성 시 성과 검증

구조:
  ├─ NeuralLevel (L1-L4 정의)
  ├─ ModelInfo (모델 정보)
  ├─ EfficiencyMetric (효율 측정)
  ├─ NeuralTask (개별 작업 추적)
  └─ NeuralEfficiencyTracker (통합 추적)
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path


# ============================================================================
# 1. 신경계 정의
# ============================================================================

class NeuralLevel(Enum):
    """신경계 계층"""
    L1_BRAINSTEM = ("L1_BRAINSTEM", "뇌간", "Adrenaline")
    L2_LIMBIC = ("L2_LIMBIC", "변연계", "Serotonin")
    L3_NEOCORTEX = ("L3_NEOCORTEX", "신피질", "Acetylcholine")
    L4_NEURONET = ("L4_NEURONET", "신경망", "Dopamine")
    
    def __init__(self, code: str, korean: str, neurotransmitter: str):
        self.code = code
        self.korean = korean
        self.neurotransmitter = neurotransmitter


# ============================================================================
# 2. 모델 정보
# ============================================================================

@dataclass
class ModelInfo:
    """모델 정보"""
    model_id: str                    # "groq", "gemini", "claude", etc
    model_name: str                  # "Groq Llama 3.1"
    provider: str                    # "Groq", "Google", "Anthropic"
    category: str                    # "coding", "analysis", "general", "creative"
    cost_per_1k_tokens: float        # $
    speed_ms_per_1k_tokens: float    # ms
    quality_score_out_of_10: float   # 0-10 baseline


@dataclass
class EfficiencyMetric:
    """효율 측정"""
    neural_level: NeuralLevel
    model_used: ModelInfo
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 입력
    task_description: str = ""
    input_tokens: int = 0
    
    # 출력
    output_tokens: int = 0
    response_time_ms: int = 0
    success: bool = True
    error_message: str = ""
    
    # 효율 점수 (0-10)
    efficiency_score: float = 0.0      # 속도 기반
    quality_score: float = 0.0         # 결과 품질
    cost_efficiency_score: float = 0.0 # 비용 효율
    overall_score: float = 0.0         # 종합 (0-10)
    
    def calculate_scores(self, target_response_time_ms: int = 3000):
        """효율 점수 계산"""
        if not self.success:
            self.efficiency_score = 0.0
            self.quality_score = 0.0
            self.cost_efficiency_score = 0.0
            self.overall_score = 0.0
            return
        
        # 1. 효율성 점수 (속도 기반) - 0-10
        # 목표: target_response_time_ms 이내
        efficiency_ratio = min(1.0, target_response_time_ms / self.response_time_ms)
        self.efficiency_score = efficiency_ratio * 10.0
        
        # 2. 품질 점수 - 모델의 baseline + 조정
        # (실제로는 LLM 판정이 필요하지만, 여기선 baseline 사용)
        self.quality_score = self.model_used.quality_score_out_of_10
        
        # 3. 비용 효율 점수 - 0-10
        # 더 저렴할수록 높은 점수
        total_cost = (self.input_tokens + self.output_tokens) / 1000 * self.model_used.cost_per_1k_tokens
        
        # $0.001 = 10점, $0.1 = 0점 (로그 스케일)
        if total_cost <= 0.001:
            cost_efficiency = 10.0
        elif total_cost >= 0.1:
            cost_efficiency = 0.0
        else:
            # 로그 스케일: ln(0.1/total_cost) / ln(100)
            import math
            cost_efficiency = min(10.0, max(0.0, 
                (math.log(0.1 / total_cost) / math.log(100)) * 10.0
            ))
        
        self.cost_efficiency_score = cost_efficiency
        
        # 4. 종합 점수 (0-10)
        # efficiency(3) + quality(4) + cost_efficiency(3)
        self.overall_score = (
            self.efficiency_score * 0.3 +
            self.quality_score * 0.4 +
            self.cost_efficiency_score * 0.3
        )
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'timestamp': self.timestamp,
            'neural_level': self.neural_level.code,
            'model': self.model_used.model_id,
            'model_name': self.model_used.model_name,
            'task': self.task_description,
            'tokens': {
                'input': self.input_tokens,
                'output': self.output_tokens,
                'total': self.input_tokens + self.output_tokens
            },
            'timing': {
                'response_time_ms': self.response_time_ms,
                'speed_per_1k_tokens_ms': (
                    self.response_time_ms / ((self.input_tokens + self.output_tokens) / 1000)
                    if (self.input_tokens + self.output_tokens) > 0 else 0
                )
            },
            'cost': {
                'total_cost_usd': (
                    (self.input_tokens + self.output_tokens) / 1000 *
                    self.model_used.cost_per_1k_tokens
                ),
                'cost_per_1k_tokens_usd': self.model_used.cost_per_1k_tokens
            },
            'scores': {
                'efficiency': round(self.efficiency_score, 2),      # 속도
                'quality': round(self.quality_score, 2),            # 품질
                'cost_efficiency': round(self.cost_efficiency_score, 2),  # 비용
                'overall': round(self.overall_score, 2)             # 종합
            },
            'success': self.success,
            'error': self.error_message if not self.success else None
        }


# ============================================================================
# 3. 신경계 작업 추적
# ============================================================================

@dataclass
class NeuralTask:
    """개별 작업"""
    task_id: str
    neural_level: NeuralLevel
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    task_type: str = ""              # "analysis", "coding", "decision", etc
    description: str = ""
    
    metrics: List[EfficiencyMetric] = field(default_factory=list)
    
    def add_metric(self, metric: EfficiencyMetric):
        """메트릭 추가"""
        self.metrics.append(metric)
    
    def get_best_model(self) -> Optional[Tuple[str, float]]:
        """가장 좋은 모델 반환"""
        if not self.metrics:
            return None
        
        best_metric = max(self.metrics, key=lambda m: m.overall_score)
        return (best_metric.model_used.model_id, best_metric.overall_score)
    
    def get_average_score(self) -> float:
        """평균 점수"""
        if not self.metrics:
            return 0.0
        
        return sum(m.overall_score for m in self.metrics) / len(self.metrics)
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'task_id': self.task_id,
            'neural_level': self.neural_level.code,
            'neural_level_korean': self.neural_level.korean,
            'neurotransmitter': self.neural_level.neurotransmitter,
            'timestamp': self.timestamp,
            'task_type': self.task_type,
            'description': self.description,
            'metrics_count': len(self.metrics),
            'metrics': [m.to_dict() for m in self.metrics],
            'average_score': round(self.get_average_score(), 2),
            'best_model': self.get_best_model()
        }


# ============================================================================
# 4. 신경계 효율 추적 시스템
# ============================================================================

class NeuralEfficiencyTracker:
    """신경계 효율 통합 추적"""
    
    def __init__(self, output_dir: str = "logs/neural_efficiency"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 모델 저장소
        self.models: Dict[str, ModelInfo] = {}
        self._init_models()
        
        # 작업 저장소
        self.tasks: Dict[str, NeuralTask] = {}
        
        # 신경계별 통계
        self.neural_stats: Dict[str, Dict] = {
            level.code: {
                'tasks': 0,
                'total_score': 0.0,
                'avg_score': 0.0,
                'best_score': 0.0,
                'models_used': {}
            }
            for level in NeuralLevel
        }
    
    def _init_models(self):
        """모델 초기화"""
        models_config = [
            # L1 뇌간 (빠르고 저렴)
            ModelInfo("groq", "Groq Llama 3.1", "Groq", "general", 0.00005, 500, 7.5),
            ModelInfo("cerebras", "Cerebras", "Cerebras", "general", 0.000, 800, 7.0),
            
            # L2 변연계 (균형)
            ModelInfo("gemini", "Gemini 2.5 Pro", "Google", "analysis", 0.00075, 2300, 9.9),
            ModelInfo("groq-extended", "Groq Extended", "Groq", "analysis", 0.0001, 600, 8.5),
            
            # L3 신피질 (고품질, 느림)
            ModelInfo("claude", "Claude 3.5 Sonnet", "Anthropic", "coding", 0.003, 2100, 9.4),
            ModelInfo("openai", "GPT-4 Turbo", "OpenAI", "coding", 0.01, 2400, 9.5),
            
            # L4 신경망 (최고 품질)
            ModelInfo("deepseek", "DeepSeek R1", "DeepSeek", "analysis", 0.0014, 2000, 8.7),
            ModelInfo("openrouter", "OpenRouter Multi", "OpenRouter", "general", 0.002, 1800, 8.6),
        ]
        
        for model in models_config:
            self.models[model.model_id] = model
    
    def create_task(
        self,
        task_id: str,
        neural_level: NeuralLevel,
        task_type: str,
        description: str
    ) -> NeuralTask:
        """작업 생성"""
        task = NeuralTask(
            task_id=task_id,
            neural_level=neural_level,
            task_type=task_type,
            description=description
        )
        self.tasks[task_id] = task
        return task
    
    def add_metric(
        self,
        task_id: str,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        response_time_ms: int,
        success: bool = True,
        error_message: str = ""
    ) -> EfficiencyMetric:
        """메트릭 추가"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        task = self.tasks[task_id]
        model = self.models[model_id]
        
        # 메트릭 생성
        metric = EfficiencyMetric(
            neural_level=task.neural_level,
            model_used=model,
            task_description=task.description,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            response_time_ms=response_time_ms,
            success=success,
            error_message=error_message
        )
        
        # 점수 계산
        metric.calculate_scores()
        
        # 작업에 추가
        task.add_metric(metric)
        
        # 신경계 통계 업데이트
        self._update_neural_stats(task.neural_level, metric, model_id)
        
        return metric
    
    def _update_neural_stats(self, neural_level: NeuralLevel, metric: EfficiencyMetric, model_id: str):
        """신경계 통계 업데이트"""
        stats = self.neural_stats[neural_level.code]
        
        stats['tasks'] += 1
        stats['total_score'] += metric.overall_score
        stats['avg_score'] = stats['total_score'] / stats['tasks']
        stats['best_score'] = max(stats['best_score'], metric.overall_score)
        
        # 모델별 사용 횟수
        if model_id not in stats['models_used']:
            stats['models_used'][model_id] = {'count': 0, 'total_score': 0.0}
        
        stats['models_used'][model_id]['count'] += 1
        stats['models_used'][model_id]['total_score'] += metric.overall_score
    
    def generate_neural_report(self) -> Dict:
        """신경계 효율 리포트 생성"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'neural_levels': self.neural_stats,
            'tasks': {
                task_id: task.to_dict()
                for task_id, task in self.tasks.items()
            }
        }
    
    def save_report(self, filename: str = "neural_efficiency_report.json"):
        """리포트 저장"""
        report = self.generate_neural_report()
        
        report_path = self.output_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_path
    
    def print_summary(self):
        """요약 출력"""
        print("\n" + "="*80)
        print("🧠 신경계 효율 추적 리포트")
        print("="*80)
        
        for level in NeuralLevel:
            stats = self.neural_stats[level.code]
            
            print(f"\n{level.korean} ({level.code})")
            print(f"  신경전달물질: {level.neurotransmitter}")
            print(f"  작업 수: {stats['tasks']}")
            print(f"  평균 점수: {stats['avg_score']:.2f}/10")
            print(f"  최고 점수: {stats['best_score']:.2f}/10")
            
            if stats['models_used']:
                print(f"  사용 모델:")
                for model_id, model_stats in stats['models_used'].items():
                    model_name = self.models[model_id].model_name
                    avg = model_stats['total_score'] / model_stats['count']
                    print(f"    - {model_name}: {model_stats['count']}회, 평균 {avg:.2f}/10")
        
        print("\n" + "="*80)


# ============================================================================
# 5. 사용 예시
# ============================================================================

if __name__ == "__main__":
    # 추적 시스템 초기화
    tracker = NeuralEfficiencyTracker()
    
    # L1 뇌간 작업 생성
    task1 = tracker.create_task(
        "watchdog_001",
        NeuralLevel.L1_BRAINSTEM,
        "monitoring",
        "프로세스 모니터링 및 자동 복구"
    )
    
    # Groq 모델 사용
    tracker.add_metric(
        "watchdog_001",
        "groq",
        input_tokens=150,
        output_tokens=50,
        response_time_ms=800,
        success=True
    )
    
    # L2 변연계 작업
    task2 = tracker.create_task(
        "analysis_001",
        NeuralLevel.L2_LIMBIC,
        "analysis",
        "감정 분석 및 우선순위 결정"
    )
    
    # Gemini 모델 사용
    tracker.add_metric(
        "analysis_001",
        "gemini",
        input_tokens=500,
        output_tokens=200,
        response_time_ms=2500,
        success=True
    )
    
    # L3 신피질 작업
    task3 = tracker.create_task(
        "coding_001",
        NeuralLevel.L3_NEOCORTEX,
        "coding",
        "코드 생성 및 최적화"
    )
    
    # Claude 모델 사용
    tracker.add_metric(
        "coding_001",
        "claude",
        input_tokens=1000,
        output_tokens=800,
        response_time_ms=2100,
        success=True
    )
    
    # 리포트 생성 및 출력
    report_path = tracker.save_report()
    print(f"\n✅ 리포트 저장됨: {report_path}")
    
    tracker.print_summary()
