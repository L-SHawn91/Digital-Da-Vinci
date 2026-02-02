#!/usr/bin/env python3
"""
여분 모델 테스트: Claude Sonnet-4 vs Haiku
"""

import json
from datetime import datetime

# 테스트 시나리오
TEST_SCENARIOS = [
    {
        "name": "Scenario 1: 간단한 질문",
        "query": "자궁 오가노이드란?",
        "complexity": "low"
    },
    {
        "name": "Scenario 2: 분석 요청",
        "query": "줄기세포 분화 메커니즘을 설명하고, 자궁 오가노이드 개발에 적용 가능한 방법은?",
        "complexity": "high"
    },
    {
        "name": "Scenario 3: 데이터 해석",
        "query": "FACS 분석 결과에서 CD34+ 세포의 비율이 감소했다. 이것이 의미하는 바와 앞으로의 실험 방향은?",
        "complexity": "high"
    }
]

def main():
    print("🧪 여분 모델 테스트 계획\n")
    
    results = {
        "test_time": datetime.now().isoformat(),
        "model_comparison": {
            "primary": "github-copilot/claude-haiku-4.5",
            "fallback": "github-copilot/claude-sonnet-4"
        },
        "scenarios": []
    }
    
    for scenario in TEST_SCENARIOS:
        print(f"\n📋 {scenario['name']}")
        print(f"   복잡도: {scenario['complexity']}")
        print(f"   쿼리: '{scenario['query']}'")
        print(f"   \n   예상:")
        
        if scenario['complexity'] == 'low':
            print(f"   - Haiku (기본): 충분한 응답 ✅")
            print(f"   - Sonnet (여분): 더 상세한 응답")
            model = "haiku"
        else:
            print(f"   - Haiku (기본): 제한적 응답 ⚠️")
            print(f"   - Sonnet (여분): 전환 필요 🔄")
            print(f"   - 재시도 Sonnet: 우수한 응답 ✅")
            model = "sonnet"
        
        results["scenarios"].append({
            "name": scenario['name'],
            "query": scenario['query'],
            "complexity": scenario['complexity'],
            "recommended_model": model,
            "status": "준비됨"
        })
    
    # 저장
    output_file = "/Users/soohyunglee/.openclaw/workspace/week3_model_test_plan.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n✅ 테스트 계획 저장: {output_file}")
    print(f"   시나리오: {len(TEST_SCENARIOS)}개")
    print(f"   모델 비교:")
    print(f"   - Primary: Haiku (빠르고 효율적)")
    print(f"   - Fallback: Sonnet-4 (복잡한 작업)")

if __name__ == "__main__":
    main()
