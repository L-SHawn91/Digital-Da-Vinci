#!/usr/bin/env python3
"""
신경가소성 v2.0 종합 벤치마크
모든 환경변수 기반 모델에 대해 Multi-Criteria Learning 테스트
"""

import asyncio
import httpx
import time
from typing import List, Dict

API_BASE = "http://localhost:8000"

# 테스트 시나리오 (Layer별)
TEST_SCENARIOS = {
    "L1": [
        "안녕",
        "너는 누구야",
        "뭐해",
        "ㅎㅇ",
        "빨리 대답해"
    ],
    "L2": [
        "기분이 어때",
        "오늘 날씨 좋네",
        "감정 분석해줘"
    ],
    "L3": [
        "오가노이드에 대해 상세히 설명해줘",
        "자궁내막 오가노이드 배양 프로토콜을 분석해줘",
        "이 논문의 핵심 내용을 요약해줘"
    ],
    "L4": [
        "Python으로 피보나치 수열 코드 작성해줘",
        "이 시스템의 아키텍처를 설계해줘"
    ]
}

async def test_query(client: httpx.AsyncClient, user_id: int, text: str) -> Dict:
    """단일 쿼리 테스트"""
    start = time.time()
    try:
        response = await client.post(
            f"{API_BASE}/v1/chat",
            json={"user_id": user_id, "text": text},
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "text": text,
            "provider": data.get("provider", "Unknown"),
            "latency_ms": data.get("latency_ms", 0),
            "total_time_ms": (time.time() - start) * 1000,
            "status": "success"
        }
    except Exception as e:
        return {
            "text": text,
            "provider": "Error",
            "latency_ms": 0,
            "total_time_ms": (time.time() - start) * 1000,
            "status": f"failed: {str(e)}"
        }

async def run_benchmark():
    """전체 벤치마크 실행"""
    print("=" * 80)
    print("🧠 신경가소성 v2.0 종합 벤치마크")
    print("=" * 80)
    
    async with httpx.AsyncClient() as client:
        # Health Check
        try:
            health = await client.get(f"{API_BASE}/health", timeout=5.0)
            print(f"✅ Server Status: {health.json()}\n")
        except Exception as e:
            print(f"❌ Server Offline: {e}")
            return
        
        results_by_layer = {}
        
        for level, queries in TEST_SCENARIOS.items():
            print(f"\n{'='*80}")
            print(f"📊 Testing {level} Layer ({len(queries)} queries)")
            print(f"{'='*80}\n")
            
            results = []
            for i, query in enumerate(queries, 1):
                print(f"[{i}/{len(queries)}] Query: \"{query[:50]}...\"")
                result = await test_query(client, user_id=10000 + i, text=query)
                results.append(result)
                
                print(f"  → Provider: {result['provider']}")
                print(f"  → Latency: {result['latency_ms']:.0f}ms")
                print(f"  → Total: {result['total_time_ms']:.0f}ms")
                print(f"  → Status: {result['status']}\n")
                
                # 서버 부하 방지
                await asyncio.sleep(1)
            
            results_by_layer[level] = results
        
        # 결과 요약
        print("\n" + "=" * 80)
        print("📈 벤치마크 결과 요약")
        print("=" * 80)
        
        for level, results in results_by_layer.items():
            providers = {}
            total_latency = 0
            success_count = 0
            
            for r in results:
                if r["status"] == "success":
                    success_count += 1
                    total_latency += r["latency_ms"]
                    providers[r["provider"]] = providers.get(r["provider"], 0) + 1
            
            print(f"\n[{level}]")
            print(f"  성공률: {success_count}/{len(results)} ({success_count/len(results)*100:.0f}%)")
            if success_count > 0:
                print(f"  평균 응답 시간: {total_latency/success_count:.0f}ms")
            print(f"  모델 분포:")
            for provider, count in sorted(providers.items(), key=lambda x: -x[1]):
                print(f"    - {provider}: {count}회 ({count/len(results)*100:.0f}%)")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
