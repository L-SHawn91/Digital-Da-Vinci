"""
AI 모델 통합 강화 - 자동 모델 선택 & 폴백

역할:
- 작업 유형별 최적 모델 선택
- 모델 성능 추적
- 자동 폴백 메커니즘
- 비용 최적화
"""

from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass
import time


class TaskType(Enum):
    """작업 유형"""
    IMAGE_ANALYSIS = "image_analysis"      # 이미지 분석 (Occipital)
    TEXT_ANALYSIS = "text_analysis"        # 텍스트 분석 (Temporal)
    QUANTITATIVE = "quantitative"          # 정량 분석 (Parietal)
    DECISION_MAKING = "decision_making"    # 의사결정 (Prefrontal)
    RAPID_RESPONSE = "rapid_response"      # 빠른 응답 (Brainstem)
    GENERAL = "general"                    # 일반 대화


@dataclass
class ModelProfile:
    """모델 프로필"""
    name: str
    task_types: List[TaskType]
    cost_per_call: float
    avg_latency_ms: float
    accuracy_score: float  # 0-1
    success_rate: float    # 0-1
    available: bool = True


class ModelSelector:
    """모델 선택기"""
    
    def __init__(self):
        # 모델 프로필 정의
        self.models = {
            'gemini_2_5_pro': ModelProfile(
                name='Gemini 2.5 Pro',
                task_types=[
                    TaskType.IMAGE_ANALYSIS,
                    TaskType.TEXT_ANALYSIS,
                    TaskType.DECISION_MAKING,
                    TaskType.GENERAL
                ],
                cost_per_call=0.01,
                avg_latency_ms=2300,
                accuracy_score=0.99,
                success_rate=0.98
            ),
            'claude_opus': ModelProfile(
                name='Claude Opus',
                task_types=[
                    TaskType.DECISION_MAKING,
                    TaskType.TEXT_ANALYSIS,
                    TaskType.GENERAL
                ],
                cost_per_call=0.015,
                avg_latency_ms=2100,
                accuracy_score=0.99,
                success_rate=0.97
            ),
            'groq_llama': ModelProfile(
                name='Groq Llama',
                task_types=[
                    TaskType.RAPID_RESPONSE,
                    TaskType.GENERAL
                ],
                cost_per_call=0.0,
                avg_latency_ms=800,
                accuracy_score=0.92,
                success_rate=0.95
            ),
            'deepseek': ModelProfile(
                name='DeepSeek',
                task_types=[
                    TaskType.QUANTITATIVE,
                    TaskType.TEXT_ANALYSIS
                ],
                cost_per_call=0.002,
                avg_latency_ms=1500,
                accuracy_score=0.95,
                success_rate=0.93
            ),
            'claude_sonnet': ModelProfile(
                name='Claude Sonnet',
                task_types=[
                    TaskType.TEXT_ANALYSIS,
                    TaskType.GENERAL
                ],
                cost_per_call=0.003,
                avg_latency_ms=1800,
                accuracy_score=0.97,
                success_rate=0.96
            ),
            'gemini_flash': ModelProfile(
                name='Gemini Flash',
                task_types=[
                    TaskType.RAPID_RESPONSE,
                    TaskType.GENERAL
                ],
                cost_per_call=0.0005,
                avg_latency_ms=900,
                accuracy_score=0.90,
                success_rate=0.94
            )
        }
        
        # 작업 유형별 우선순위
        self.task_preferences = {
            TaskType.IMAGE_ANALYSIS: ['gemini_2_5_pro', 'claude_opus'],
            TaskType.TEXT_ANALYSIS: ['claude_opus', 'gemini_2_5_pro', 'claude_sonnet'],
            TaskType.QUANTITATIVE: ['deepseek', 'gemini_2_5_pro'],
            TaskType.DECISION_MAKING: ['claude_opus', 'gemini_2_5_pro'],
            TaskType.RAPID_RESPONSE: ['groq_llama', 'gemini_flash'],
            TaskType.GENERAL: ['gemini_2_5_pro', 'claude_sonnet', 'groq_llama']
        }
    
    def select_model(
        self,
        task_type: TaskType,
        priority: str = 'balanced'  # 'cost', 'speed', 'accuracy', 'balanced'
    ) -> ModelProfile:
        """모델 선택"""
        candidates = self.task_preferences.get(task_type, [])
        
        # 사용 가능한 모델만 필터링
        available = [
            self.models[m] for m in candidates
            if m in self.models and self.models[m].available
        ]
        
        if not available:
            # 폴백: 첫 번째 사용 가능 모델
            for model in self.models.values():
                if model.available:
                    return model
        
        # 우선순위에 따라 정렬
        if priority == 'cost':
            available.sort(key=lambda x: x.cost_per_call)
        elif priority == 'speed':
            available.sort(key=lambda x: x.avg_latency_ms)
        elif priority == 'accuracy':
            available.sort(key=lambda x: x.accuracy_score, reverse=True)
        else:  # balanced
            # 비용-성능 비율 계산
            available.sort(key=lambda x: x.accuracy_score / (x.cost_per_call + 0.001), reverse=True)
        
        return available[0]
    
    def get_alternatives(self, task_type: TaskType, count: int = 3) -> List[ModelProfile]:
        """대체 모델 목록"""
        candidates = self.task_preferences.get(task_type, [])
        
        available = [
            self.models[m] for m in candidates
            if m in self.models and self.models[m].available
        ]
        
        available.sort(key=lambda x: x.accuracy_score, reverse=True)
        return available[:count]


class FallbackStrategy:
    """폴백 전략"""
    
    def __init__(self, selector: ModelSelector):
        self.selector = selector
        self.fallback_chain = []
        self.attempt_count = {}
    
    def execute_with_fallback(
        self,
        task_type: TaskType,
        func: Callable,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """폴백과 함께 실행"""
        models = [self.selector.select_model(task_type)] + self.selector.get_alternatives(task_type, 2)
        
        for i, model in enumerate(models):
            try:
                # 모델 사용 시도
                print(f"🤖 시도 {i+1}: {model.name}")
                
                # 모델 지정
                kwargs['model'] = model.name
                
                result = func(*args, **kwargs)
                print(f"✅ {model.name}으로 성공!")
                return result
                
            except Exception as e:
                print(f"⚠️ {model.name} 실패: {str(e)}")
                
                if i == len(models) - 1:
                    # 모든 모델 실패
                    print(f"❌ 모든 모델 실패!")
                    return None
                
                continue


class ModelMonitor:
    """모델 모니터링"""
    
    def __init__(self):
        self.call_history = {
            'success': {},
            'failure': {},
            'latency': {},
            'cost': {}
        }
    
    def record_call(
        self,
        model_name: str,
        task_type: str,
        duration_ms: float,
        cost: float,
        success: bool
    ):
        """호출 기록"""
        key = f"{model_name}_{task_type}"
        
        if success:
            self.call_history['success'][key] = self.call_history['success'].get(key, 0) + 1
        else:
            self.call_history['failure'][key] = self.call_history['failure'].get(key, 0) + 1
        
        if key not in self.call_history['latency']:
            self.call_history['latency'][key] = []
        self.call_history['latency'][key].append(duration_ms)
        
        if key not in self.call_history['cost']:
            self.call_history['cost'][key] = 0
        self.call_history['cost'][key] += cost
    
    def get_model_stats(self, model_name: str) -> Dict[str, Any]:
        """모델 통계"""
        keys = [k for k in self.call_history['success'].keys() if k.startswith(model_name)]
        
        total_success = sum(self.call_history['success'].get(k, 0) for k in keys)
        total_failure = sum(self.call_history['failure'].get(k, 0) for k in keys)
        total_calls = total_success + total_failure
        
        if total_calls == 0:
            return {}
        
        all_latencies = []
        for k in keys:
            all_latencies.extend(self.call_history['latency'].get(k, []))
        
        total_cost = sum(self.call_history['cost'].get(k, 0) for k in keys)
        
        return {
            'total_calls': total_calls,
            'success_rate': total_success / total_calls,
            'failure_rate': total_failure / total_calls,
            'avg_latency_ms': sum(all_latencies) / len(all_latencies) if all_latencies else 0,
            'total_cost': total_cost,
            'cost_per_call': total_cost / total_calls if total_calls > 0 else 0
        }
    
    def print_stats(self):
        """통계 출력"""
        print("\n╔═════════════════════════════════════════════════════╗")
        print("║         🤖 모델별 성능 통계                        ║")
        print("╚═════════════════════════════════════════════════════╝\n")
        
        models = set(k.split('_')[0] for k in self.call_history['success'].keys())
        
        for model in models:
            stats = self.get_model_stats(model)
            if stats:
                print(f"📊 {model}")
                print(f"  호출: {stats['total_calls']}")
                print(f"  성공률: {stats['success_rate']*100:.1f}%")
                print(f"  평균 지연: {stats['avg_latency_ms']:.0f}ms")
                print(f"  총 비용: ${stats['total_cost']:.4f}")
                print(f"  호출당 비용: ${stats['cost_per_call']:.6f}")
                print()


if __name__ == "__main__":
    print("🤖 AI 모델 통합 강화 테스트\n")
    
    # 모델 선택기 생성
    selector = ModelSelector()
    
    # 다양한 작업 유형에 대해 최적 모델 선택
    test_tasks = [
        TaskType.IMAGE_ANALYSIS,
        TaskType.RAPID_RESPONSE,
        TaskType.DECISION_MAKING,
        TaskType.QUANTITATIVE
    ]
    
    for task in test_tasks:
        model = selector.select_model(task, priority='balanced')
        print(f"📌 {task.value}")
        print(f"  선택: {model.name}")
        print(f"  정확도: {model.accuracy_score*100:.0f}%")
        print(f"  비용: ${model.cost_per_call}")
        print()
    
    print("✅ 테스트 완료!")
