"""
L3 신피질 (Neocortex) - 4개 엽 통합 구조

구조:
├─ 전두엽 (Prefrontal Cortex): 계획 & 의사결정
├─ 측두엽 (Temporal Cortex): 기억 & 맥락
├─ 두정엽 (Parietal Cortex): 공간 & 통합
└─ 후두엽 (Occipital Cortex): 시각 & 분석

역할:
- L1(뇌간) + L2(변린계) 입력 받기
- 4개 엽이 협력하여 고급 인지 처리
- 최종 의사결정 및 행동 생성
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CortexLobe(Enum):
    """신피질 엽"""
    PREFRONTAL = "prefrontal"  # 전두엽
    TEMPORAL = "temporal"      # 측두엽
    PARIETAL = "parietal"      # 두정엽
    OCCIPITAL = "occipital"    # 후두엽


@dataclass
class NeurocortexInput:
    """신피질 입력"""
    emotion: str  # L2에서 받은 감정
    priority: str  # L2에서 받은 우선순위
    text: str  # 원본 텍스트
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class PrefrontalCortex:
    """전두엽: 계획 & 의사결정"""
    
    def __init__(self):
        self.planning_strategies = {
            "research": ["분석", "진행", "설계", "최적화"],
            "urgent": ["즉시", "지금", "급", "긴급"],
            "learning": ["배우기", "이해", "학습", "개선"],
            "creative": ["창의", "새로운", "혁신", "아이디어"]
        }
        self.decision_rules = []

    def plan_action(self, input_data: NeurocortexInput) -> Dict:
        """행동 계획 수립"""
        # 1. 전략 선택
        strategy = self._select_strategy(input_data.text)
        
        # 2. 의사결정
        decision = self._make_decision(input_data, strategy)
        
        # 3. 계획 생성
        plan = self._generate_plan(decision, strategy)
        
        return {
            "lobe": "prefrontal",
            "strategy": strategy,
            "decision": decision,
            "plan": plan,
            "confidence": 0.85
        }

    def _select_strategy(self, text: str) -> str:
        """전략 선택"""
        text_lower = text.lower()
        
        for strategy, keywords in self.planning_strategies.items():
            if any(kw in text_lower for kw in keywords):
                return strategy
        
        return "balanced"

    def _make_decision(self, input_data: NeurocortexInput, strategy: str) -> str:
        """의사결정"""
        if input_data.priority == "critical":
            return "prioritize_immediately"
        elif strategy == "urgent":
            return "fast_track"
        elif strategy == "creative":
            return "explore_options"
        else:
            return "standard_process"

    def _generate_plan(self, decision: str, strategy: str) -> List[str]:
        """계획 생성"""
        plans = {
            "prioritize_immediately": ["긴급 처리", "즉시 실행", "결과 추적"],
            "fast_track": ["간단히 처리", "빠른 피드백", "완료"],
            "explore_options": ["다양한 옵션 검토", "최선 선택", "실행"],
            "standard_process": ["단계별 처리", "검증", "완료"]
        }
        
        return plans.get(decision, ["기본 처리"])


class TemporalCortex:
    """측두엽: 기억 & 맥락"""
    
    def __init__(self):
        self.memory_buffer = []
        self.context_history = {}
        self.max_memory = 100

    def analyze_context(self, input_data: NeurocortexInput) -> Dict:
        """맥락 분석"""
        # 1. 과거 기억 검색
        relevant_memory = self._search_memory(input_data.text)
        
        # 2. 맥락 추론
        context = self._infer_context(input_data, relevant_memory)
        
        # 3. 패턴 인식
        patterns = self._recognize_patterns(input_data)
        
        return {
            "lobe": "temporal",
            "relevant_memory": relevant_memory,
            "context": context,
            "patterns": patterns,
            "relevance_score": 0.80
        }

    def _search_memory(self, text: str) -> List[str]:
        """기억 검색"""
        # 시뮬레이션: 키워드 기반 검색
        keywords = text.lower().split()
        
        relevant = []
        for memory in self.memory_buffer[-10:]:  # 최근 10개
            if any(kw in memory.lower() for kw in keywords):
                relevant.append(memory)
        
        return relevant[:3]  # 상위 3개

    def _infer_context(self, input_data: NeurocortexInput, memory: List[str]) -> str:
        """맥락 추론"""
        if memory:
            return f"ongoing_research"
        elif input_data.priority == "critical":
            return "urgent_matter"
        else:
            return "general_task"

    def _recognize_patterns(self, input_data: NeurocortexInput) -> List[str]:
        """패턴 인식"""
        patterns = []
        
        if "논문" in input_data.text or "분석" in input_data.text:
            patterns.append("research_pattern")
        
        if input_data.emotion in ["anxiety", "mixed"]:
            patterns.append("emotional_urgency")
        
        if input_data.priority == "critical":
            patterns.append("critical_priority")
        
        return patterns

    def store_memory(self, text: str):
        """메모리 저장"""
        self.memory_buffer.append(text)
        
        if len(self.memory_buffer) > self.max_memory:
            self.memory_buffer.pop(0)


class ParietalCortex:
    """두정엽: 공간 & 통합"""
    
    def __init__(self):
        self.integration_rules = {}
        self.lobes_state = {}

    def integrate_lobes(self, prefrontal: Dict, temporal: Dict, 
                       visual: Dict = None) -> Dict:
        """엽 간 통합"""
        # 1. 정보 통합
        integrated = self._merge_information(prefrontal, temporal, visual)
        
        # 2. 충돌 해결
        resolved = self._resolve_conflicts(integrated)
        
        # 3. 우선순위 재조정
        prioritized = self._reprioritize(resolved)
        
        return {
            "lobe": "parietal",
            "integrated_info": integrated,
            "resolved_conflicts": resolved,
            "final_priority": prioritized,
            "integration_score": 0.88
        }

    def _merge_information(self, prefrontal: Dict, temporal: Dict, 
                          visual: Dict = None) -> Dict:
        """정보 통합"""
        merged = {
            "decision": prefrontal.get("decision"),
            "context": temporal.get("context"),
            "plan": prefrontal.get("plan"),
            "patterns": temporal.get("patterns"),
        }
        
        if visual:
            merged["visual_analysis"] = visual.get("analysis")
        
        return merged

    def _resolve_conflicts(self, integrated: Dict) -> Dict:
        """충돌 해결"""
        # 예: 계획과 맥락이 충돌할 경우 조정
        return integrated  # 현재는 충돌 없음

    def _reprioritize(self, resolved: Dict) -> str:
        """우선순위 재조정"""
        if "critical_priority" in resolved.get("patterns", []):
            return "critical"
        elif "research_pattern" in resolved.get("patterns", []):
            return "high"
        else:
            return "medium"


class OccipitalCortex:
    """후두엽: 시각 & 분석"""
    
    def __init__(self):
        self.analysis_rules = []
        self.visualization_cache = {}

    def analyze_data(self, input_data: NeurocortexInput) -> Dict:
        """데이터 분석"""
        # 1. 텍스트 분석
        text_analysis = self._analyze_text(input_data.text)
        
        # 2. 감정 시각화
        emotion_viz = self._visualize_emotion(input_data.emotion)
        
        # 3. 관계 분석
        relationships = self._analyze_relationships(input_data.text)
        
        return {
            "lobe": "occipital",
            "text_analysis": text_analysis,
            "emotion_visualization": emotion_viz,
            "relationships": relationships,
            "analysis_score": 0.82
        }

    def _analyze_text(self, text: str) -> Dict:
        """텍스트 분석"""
        words = text.split()
        
        return {
            "word_count": len(words),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "complexity": "high" if len(words) > 20 else "medium" if len(words) > 10 else "low"
        }

    def _visualize_emotion(self, emotion: str) -> str:
        """감정 시각화"""
        emotion_visuals = {
            "joy": "😊",
            "anger": "😠",
            "anxiety": "😰",
            "sadness": "😢",
            "neutral": "😐",
            "mixed": "🤔"
        }
        
        return emotion_visuals.get(emotion, "😐")

    def _analyze_relationships(self, text: str) -> List[str]:
        """관계 분석"""
        # 주요 엔티티 간 관계 추출
        relationships = []
        
        if "논문" in text and "신경계" in text:
            relationships.append("research_neural_connection")
        
        if "모델" in text and "최적화" in text:
            relationships.append("model_optimization_link")
        
        return relationships


class NeocortexIntegration:
    """신피질 통합 (4개 엽)"""
    
    def __init__(self):
        self.prefrontal = PrefrontalCortex()
        self.temporal = TemporalCortex()
        self.parietal = ParietalCortex()
        self.occipital = OccipitalCortex()
        self.processing_log = []

    def process_input(self, input_data: NeurocortexInput) -> Dict:
        """신피질 처리 (4개 엽 협력)"""
        logger.info(f"🧠 신피질 처리 시작: {input_data.text[:30]}...")
        
        # 1단계: 각 엽이 독립적으로 분석
        prefrontal_output = self.prefrontal.plan_action(input_data)
        temporal_output = self.temporal.analyze_context(input_data)
        occipital_output = self.occipital.analyze_data(input_data)
        
        # 2단계: 두정엽이 통합
        parietal_output = self.parietal.integrate_lobes(
            prefrontal_output, temporal_output, occipital_output
        )
        
        # 3단계: 최종 결정
        final_decision = self._make_final_decision(
            prefrontal_output, temporal_output, parietal_output, occipital_output
        )
        
        # 메모리 저장
        self.temporal.store_memory(input_data.text)
        
        # 로그 저장
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_data.text[:50],
            "prefrontal": prefrontal_output,
            "temporal": temporal_output,
            "parietal": parietal_output,
            "occipital": occipital_output,
            "final_decision": final_decision
        }
        self.processing_log.append(log_entry)
        
        return final_decision

    def _make_final_decision(self, prefrontal, temporal, parietal, occipital) -> Dict:
        """최종 의사결정"""
        return {
            "action": prefrontal.get("plan")[0] if prefrontal.get("plan") else "처리 진행",
            "context": temporal.get("context"),
            "priority": parietal.get("final_priority"),
            "confidence": (
                prefrontal.get("confidence", 0.85) +
                temporal.get("relevance_score", 0.80) +
                parietal.get("integration_score", 0.88) +
                occipital.get("analysis_score", 0.82)
            ) / 4,
            "all_lobes_engaged": True
        }


def main():
    """메인 테스트"""
    logger.info("=" * 70)
    logger.info("🧠 L3 신피질 (Neocortex) 4개 엽 시스템 시작")
    logger.info("=" * 70)
    
    # 신피질 초기화
    neocortex = NeocortexIntegration()
    
    # 테스트 케이스
    test_cases = [
        NeurocortexInput(
            emotion="neutral",
            priority="critical",
            text="신경계 모델 최적화가 필요해요."
        ),
        NeurocortexInput(
            emotion="mixed",
            priority="high",
            text="기쁘지만 동시에 불안해요. 합격했는데 준비가 부족한 것 같아서."
        ),
        NeurocortexInput(
            emotion="anxiety",
            priority="high",
            text="논문 검수 피드백을 받았어요. 정말 중요합니다."
        ),
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        logger.info(f"\n📝 테스트 {i}: {test.text[:40]}...")
        
        result = neocortex.process_input(test)
        results.append(result)
        
        logger.info(f"  ✅ 행동: {result['action']}")
        logger.info(f"  🎯 우선순위: {result['priority']}")
        logger.info(f"  📊 신뢰도: {result['confidence']:.2f}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ L3 신피질 테스트 완료: {len(results)}개 케이스 처리")
    logger.info("=" * 70)
    
    # JSON 저장
    with open("/Users/soohyunglee/.openclaw/workspace/systems/neural/l3_neocortex_test_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results


if __name__ == "__main__":
    main()
