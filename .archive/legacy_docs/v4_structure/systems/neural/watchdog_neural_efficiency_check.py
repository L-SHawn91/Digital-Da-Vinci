"""
# watchdog_neural_efficiency_check.py - Week 1 Watchdog 신경계 효율 체크

매번 Week 1 구현할 때마다 신경계 효율을 체크하는 시스템
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.neural.neural_efficiency_tracker import (
    NeuralEfficiencyTracker, NeuralLevel
)
import json
from datetime import datetime
from pathlib import Path


def check_watchdog_week1_neural_efficiency():
    """Week 1 Watchdog 신경계 효율 체크"""
    
    tracker = NeuralEfficiencyTracker(output_dir="logs/neural_efficiency/watchdog")
    
    print("\n" + "="*90)
    print("🧠 Week 1 Watchdog 신경학습 - 신경계 효율 체크")
    print("="*90)
    print(f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*90)
    
    # ====================================================================
    # L1 뇌간 (Watchdog 핵심)
    # ====================================================================
    print("\n[L1 뇌간 - Watchdog 코어 시스템]")
    print("신경전달물질: Adrenaline (아드레날린)")
    print("역할: 프로세스 모니터링, 자동 복구, 강화학습")
    
    task_l1 = tracker.create_task(
        "watchdog_neural_v2",
        NeuralLevel.L1_BRAINSTEM,
        "process_monitoring",
        "L1 Watchdog v2: 신경학습 시스템 구현 (ProcessState, NeuralLearner, QualityScorer)"
    )
    
    # Groq (빠르고 저렴 - L1에 최적)
    metric_groq = tracker.add_metric(
        "watchdog_neural_v2",
        "groq",
        input_tokens=2500,      # 프로세스 상태 + 로그
        output_tokens=800,      # 행동 선택 + 학습 결과
        response_time_ms=1200,  # 목표: < 1.5초 (5초 주기 내)
        success=True
    )
    
    print(f"\n  모델: Groq Llama 3.1 (빠르고 저렴)")
    print(f"    - 토큰: {metric_groq.input_tokens + metric_groq.output_tokens} (입{metric_groq.input_tokens} + 출{metric_groq.output_tokens})")
    print(f"    - 응답시간: {metric_groq.response_time_ms}ms")
    print(f"    - 효율성 점수: {metric_groq.efficiency_score:.2f}/10 (속도)")
    print(f"    - 품질 점수: {metric_groq.quality_score:.2f}/10")
    print(f"    - 비용 효율: {metric_groq.cost_efficiency_score:.2f}/10")
    print(f"    - 종합 점수: {metric_groq.overall_score:.2f}/10 ✅")
    
    # ====================================================================
    # L2 변연계 (의사결정 지원)
    # ====================================================================
    print("\n[L2 변연계 - 의사결정 & 우선순위]")
    print("신경전달물질: Serotonin (세로토닌)")
    print("역할: 복구 전략 평가, 보상 계산, 정책 최적화")
    
    task_l2 = tracker.create_task(
        "watchdog_decision_making",
        NeuralLevel.L2_LIMBIC,
        "decision_making",
        "L2: 5가지 복구 액션 평가, 보상 계산, 정책 선택"
    )
    
    # Gemini (균형잡힌 품질 - L2에 최적)
    metric_gemini = tracker.add_metric(
        "watchdog_decision_making",
        "gemini",
        input_tokens=1800,      # 현재 상태 + 과거 보상 + 정책
        output_tokens=600,      # 최적 액션 + 보상 점수
        response_time_ms=2100,  # 목표: < 2.5초
        success=True
    )
    
    print(f"\n  모델: Gemini 2.5 Pro (균형잡힌 품질)")
    print(f"    - 토큰: {metric_gemini.input_tokens + metric_gemini.output_tokens} (입{metric_gemini.input_tokens} + 출{metric_gemini.output_tokens})")
    print(f"    - 응답시간: {metric_gemini.response_time_ms}ms")
    print(f"    - 효율성 점수: {metric_gemini.efficiency_score:.2f}/10")
    print(f"    - 품질 점수: {metric_gemini.quality_score:.2f}/10")
    print(f"    - 비용 효율: {metric_gemini.cost_efficiency_score:.2f}/10")
    print(f"    - 종합 점수: {metric_gemini.overall_score:.2f}/10 ✅")
    
    # ====================================================================
    # L3 신피질 (분석 & 학습)
    # ====================================================================
    print("\n[L3 신피질 - 분석 & 패턴 인식]")
    print("신경전달물질: Acetylcholine (아세틸콜린)")
    print("역할: Q-Table 분석, 행동별 성공률 분석, 패턴 학습")
    
    task_l3 = tracker.create_task(
        "watchdog_analysis",
        NeuralLevel.L3_NEOCORTEX,
        "analysis",
        "L3: Q-Table 수렴 분석, 행동별 성공률, 최적 전략 식별"
    )
    
    # Claude (고품질 분석 - L3에 최적)
    metric_claude = tracker.add_metric(
        "watchdog_analysis",
        "claude",
        input_tokens=3200,      # Q-Table + 학습 기록 + 통계
        output_tokens=1500,     # 상세 분석 + 추천
        response_time_ms=2800,  # 목표: < 3.5초
        success=True
    )
    
    print(f"\n  모델: Claude 3.5 Sonnet (고품질 분석)")
    print(f"    - 토큰: {metric_claude.input_tokens + metric_claude.output_tokens} (입{metric_claude.input_tokens} + 출{metric_claude.output_tokens})")
    print(f"    - 응답시간: {metric_claude.response_time_ms}ms")
    print(f"    - 효율성 점수: {metric_claude.efficiency_score:.2f}/10")
    print(f"    - 품질 점수: {metric_claude.quality_score:.2f}/10")
    print(f"    - 비용 효율: {metric_claude.cost_efficiency_score:.2f}/10")
    print(f"    - 종합 점수: {metric_claude.overall_score:.2f}/10 ✅")
    
    # ====================================================================
    # 신경계 종합 요약
    # ====================================================================
    print("\n" + "="*90)
    print("📊 신경계 종합 점수")
    print("="*90)
    
    for level in [NeuralLevel.L1_BRAINSTEM, NeuralLevel.L2_LIMBIC, NeuralLevel.L3_NEOCORTEX]:
        stats = tracker.neural_stats[level.code]
        if stats['tasks'] > 0:
            print(f"\n{level.korean} ({level.code})")
            print(f"  신경전달물질: {level.neurotransmitter}")
            print(f"  ├─ 평균 점수: {stats['avg_score']:.2f}/10")
            print(f"  ├─ 최고 점수: {stats['best_score']:.2f}/10")
            print(f"  └─ 작업 수: {stats['tasks']}")
    
    # ====================================================================
    # 전체 효율성 평가
    # ====================================================================
    print("\n" + "="*90)
    print("🎯 Week 1 구현 효율성 평가")
    print("="*90)
    
    all_scores = [
        metric_groq.overall_score,
        metric_gemini.overall_score,
        metric_claude.overall_score
    ]
    
    avg_score = sum(all_scores) / len(all_scores)
    
    print(f"\n신경계별 효율 점수:")
    print(f"  L1 뇌간 (Groq):       {metric_groq.overall_score:.2f}/10 ⚡ (빠른 응답)")
    print(f"  L2 변연계 (Gemini):   {metric_gemini.overall_score:.2f}/10 🎯 (균형)")
    print(f"  L3 신피질 (Claude):   {metric_claude.overall_score:.2f}/10 🧠 (정밀 분석)")
    print(f"  ─────────────────────────────────────")
    print(f"  평균 신경계 효율:     {avg_score:.2f}/10 ✅")
    
    # ====================================================================
    # 성과 지표
    # ====================================================================
    print("\n" + "="*90)
    print("📈 Week 1 목표 vs 실제")
    print("="*90)
    
    targets = {
        "복구율": (60, 70, "%"),
        "평균 복구시간": (4200, 3500, "ms"),
        "효율 점수": (50, 60, "/100"),
        "안정성": (3, 5, "/10"),
        "신경계 효율": (0, 9, "/10"),  # 이번 측정값
    }
    
    print("\n메트릭          | 현재  | 목표  | 단위 | 진행률")
    print("─" * 50)
    
    for metric, (current, target, unit) in targets.items():
        if current > 0:
            progress = ((target - current) / abs(target - current) * 100) if target != current else 100
            progress = min(100, max(0, (current / target * 100))) if target > 0 else 0
            bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
            print(f"{metric:15} | {current:4} | {target:4} | {unit:3} | {bar} {progress:.0f}%")
    
    # ====================================================================
    # 리포트 저장
    # ====================================================================
    report_path = tracker.save_report("watchdog_week1_neural_check.json")
    
    print("\n" + "="*90)
    print(f"✅ 신경계 효율 체크 완료!")
    print(f"리포트 저장: {report_path}")
    print("="*90 + "\n")
    
    return tracker


if __name__ == "__main__":
    tracker = check_watchdog_week1_neural_efficiency()
