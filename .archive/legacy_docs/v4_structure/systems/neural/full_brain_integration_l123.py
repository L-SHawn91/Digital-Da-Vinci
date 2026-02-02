"""
L1+L2+L3 완전 통합 시스템 (뇌간+변린계+신피질)

워크플로우:
1. L1 뇌간: 기본 상태 감지 & 안정성
2. L2 변린계: 감정 & 우선순위 분석
3. L3 신피질: 고급 인지 처리 & 의사결정
4. 최종 행동 생성
"""

import json
from datetime import datetime
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrainSystemL123:
    """L1+L2+L3 완전 뇌 시스템"""
    
    def __init__(self):
        # L1 뇌간 시뮬레이션
        self.brainstem_status = "normal"
        self.stability_score = 0.95
        
        # L2 변린계 (이전 구현)
        self.emotions = ["joy", "anger", "anxiety", "sadness", "neutral", "mixed"]
        self.priorities = ["low", "medium", "high", "critical"]
        
        # L3 신피질 (새로운 구현)
        self.neocortex_lobes = ["prefrontal", "temporal", "parietal", "occipital"]
        
        self.processing_results = []

    def process_full_pipeline(self, user_input: str) -> Dict:
        """완전한 신경 처리 파이프라인"""
        logger.info("🧠 L1→L2→L3 전체 뇌 처리 시작")
        
        # L1: 뇌간 체크
        l1_output = self._process_l1_brainstem(user_input)
        
        if l1_output["status"] != "normal":
            return {
                "error": "Brain system unstable",
                "l1_status": l1_output,
                "action": "system_recovery"
            }
        
        # L2: 변린계 감정분석
        l2_output = self._process_l2_limbic(user_input)
        
        # L3: 신피질 고급처리
        l3_output = self._process_l3_neocortex(user_input, l2_output)
        
        # 최종 결정
        final_action = self._make_final_action(l1_output, l2_output, l3_output)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input[:50],
            "l1_brainstem": l1_output,
            "l2_limbic": l2_output,
            "l3_neocortex": l3_output,
            "final_action": final_action,
            "confidence": (l1_output["score"] + l2_output["score"] + l3_output["score"]) / 3
        }
        
        self.processing_results.append(result)
        return result

    def _process_l1_brainstem(self, text: str) -> Dict:
        """L1: 뇌간 - 기본 생존 기능"""
        # 상태 확인
        is_stable = True
        
        # 신뢰도
        stability = self.stability_score
        
        return {
            "lobe": "brainstem",
            "status": "normal" if is_stable else "critical",
            "stability": stability,
            "score": 0.95
        }

    def _process_l2_limbic(self, text: str) -> Dict:
        """L2: 변린계 - 감정 & 우선순위"""
        text_lower = text.lower()
        
        # 감정 감지
        emotion = "neutral"
        if any(kw in text_lower for kw in ["기쁜", "좋음", "설렘"]):
            emotion = "joy"
        elif any(kw in text_lower for kw in ["화나", "분노", "짜증"]):
            emotion = "anger"
        elif any(kw in text_lower for kw in ["불안", "걱정"]):
            emotion = "anxiety"
        elif any(kw in text_lower for kw in ["슬픔", "우울"]):
            emotion = "sadness"
        
        # 우선순위
        priority = "low"
        if any(kw in text_lower for kw in ["신경계", "모델", "논문검수"]):
            priority = "critical"
        elif any(kw in text_lower for kw in ["문제", "불안", "걱정"]):
            priority = "high"
        
        return {
            "lobe": "limbic_system",
            "emotion": emotion,
            "priority": priority,
            "emotional_intensity": 0.8,
            "score": 0.85
        }

    def _process_l3_neocortex(self, text: str, l2_output: Dict) -> Dict:
        """L3: 신피질 - 고급 인지 처리"""
        text_lower = text.lower()
        
        # 전두엽: 계획
        if l2_output["priority"] == "critical":
            plan = "긴급 처리"
        else:
            plan = "단계별 처리"
        
        # 측두엽: 맥락
        context = "research" if "논문" in text_lower or "모델" in text_lower else "general"
        
        # 두정엽: 통합
        integrated_priority = l2_output["priority"]
        
        # 후두엽: 분석
        analysis = {
            "word_count": len(text.split()),
            "complexity": "high" if len(text) > 50 else "medium"
        }
        
        return {
            "lobe": "neocortex",
            "prefrontal_plan": plan,
            "temporal_context": context,
            "parietal_integration": integrated_priority,
            "occipital_analysis": analysis,
            "score": 0.88
        }

    def _make_final_action(self, l1: Dict, l2: Dict, l3: Dict) -> str:
        """최종 행동 결정"""
        if l1["status"] != "normal":
            return "시스템 복구 필요"
        
        if l2["priority"] == "critical":
            return "긴급 처리 시작"
        elif l2["priority"] == "high":
            return "우선 처리 진행"
        else:
            return "일반 처리"


def main():
    """테스트"""
    logger.info("=" * 70)
    logger.info("🧠 L1+L2+L3 완전 뇌 시스템 테스트")
    logger.info("=" * 70)
    
    brain = BrainSystemL123()
    
    test_cases = [
        "신경계 모델 최적화가 필요해요.",
        "기쁘지만 동시에 불안해요. 합격했는데 준비가 부족한 것 같아서.",
        "논문 검수 피드백을 받았어요.",
        "오늘 날씨가 좋네요."
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        logger.info(f"\n📝 테스트 {i}: {test}")
        
        result = brain.process_full_pipeline(test)
        results.append(result)
        
        logger.info(f"  L1 뇌간: {result['l1_brainstem']['status']}")
        logger.info(f"  L2 감정: {result['l2_limbic']['emotion']} (우선순위: {result['l2_limbic']['priority']})")
        logger.info(f"  L3 계획: {result['l3_neocortex']['prefrontal_plan']}")
        logger.info(f"  🎯 행동: {result['final_action']}")
        logger.info(f"  신뢰도: {result['confidence']:.2f}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ 완료: {len(results)}개 테스트 케이스 처리")
    logger.info("=" * 70)
    
    # JSON 저장
    with open("/Users/soohyunglee/.openclaw/workspace/systems/neural/l123_full_brain_test.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "system": "L1+L2+L3 Full Brain",
            "total_tests": len(results),
            "results": results,
            "average_confidence": sum(r["confidence"] for r in results) / len(results)
        }, f, indent=2, ensure_ascii=False)
    
    return results


if __name__ == "__main__":
    main()
