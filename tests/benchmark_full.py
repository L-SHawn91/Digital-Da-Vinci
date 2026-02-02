#!/usr/bin/env python3
"""
신경가소성 v2.5 종합 벤치마크 (Whole-Brain Evaluation)
LLM 생성 속도 + 임베딩 검색 속도(Memory Latency) 통합 측정
"""

import asyncio
import httpx
import time
from typing import List, Dict
import statistics

API_BASE = "http://localhost:8000"

# 테스트 시나리오 (Layer별) - 임베딩 부하 테스트 포함
TEST_SCENARIOS = {
    "L1": [ # Reflexive (Memory Skip)
        "안녕",
        "너는 누구야",
        "1+1은?",
    ],
    "L3": [ # Cognitive (Memory Intensive)
        "오가노이드 연구 동향에 대해 알려줘", # 임베딩 필요
        "최근 숀브레인 아키텍처 변경사항은?", # 임베딩 필요
        "파이썬 코딩 컨벤션에 대해 설명해줘"  # 임베딩 필요
    ]
}

async def test_query(client: httpx.AsyncClient, user_id: int, text: str) -> Dict:
    """단일 쿼리 테스트"""
    start = time.time()
    try:
        response = await client.post(
            f"{API_BASE}/v1/chat",
            json={"user_id": user_id, "text": text},
            timeout=60.0 # 넉넉하게
        )
        response.raise_for_status()
        data = response.json()
        
        # API가 memory_latency를 반환한다고 가정 (실제로는 안 줄 수도 있으니 전체 시간에서 유추하거나 로그 확인 필요)
        # 현재 API 응답 포맷: {"response": ..., "provider": ..., "latency_ms": ...}
        # memory_latency는 내부 로그로만 남으므로, 여기서는 Total Time - Latency(LLM)로 간접 추정
        
        llm_latency = data.get("latency_ms", 0)
        total_time = (time.time() - start) * 1000
        overhead = max(0, total_time - llm_latency)
        
        return {
            "text": text,
            "provider": data.get("provider", "Unknown"),
            "llm_latency_ms": llm_latency,
            "total_time_ms": total_time,
            "memory_overhead_ms": overhead, # 추정치 (Network Latency 포함됨)
            "status": "success"
        }
    except Exception as e:
        return {
            "text": text,
            "provider": "Error",
            "llm_latency_ms": 0,
            "total_time_ms": (time.time() - start) * 1000,
            "status": f"failed: {str(e)}"
        }

async def run_benchmark():
    """Whole-Brain 벤치마크 실행"""
    print("=" * 80)
    print("🧠 D-CNS v5.5 Whole-Brain 벤치마크 (LLM + Embedding)")
    print("=" * 80)
    
    async with httpx.AsyncClient() as client:
        # Health Check
        try:
            await client.get(f"{API_BASE}/health", timeout=5.0)
            print(f"✅ Server Online\n")
        except:
            print(f"❌ Server Offline. start_bot.sh 실행 필요.")
            return
        
        results_by_layer = {}
        
        for level, queries in TEST_SCENARIOS.items():
            print(f"\n{'='*80}")
            print(f"📊 Testing {level} Layer")
            print(f"{'='*80}\n")
            
            results = []
            for i, query in enumerate(queries, 1):
                print(f"[{i}] Q: \"{query}\"")
                result = await test_query(client, user_id=99999, text=query)
                results.append(result)
                
                print(f"  → Provider: {result['provider']}")
                print(f"  → Total Latency: {result['total_time_ms']:.0f}ms")
                print(f"  → LLM Gen Time : {result['llm_latency_ms']:.0f}ms")
                print(f"  → Memory/Net   : {result['memory_overhead_ms']:.0f}ms")
                print(f"  → Status: {result['status']}\n")
                
                await asyncio.sleep(1)
            
            results_by_layer[level] = results
        
        # 종합 리포트 출력
        print("\n" + "#" * 80)
        print("📑 숀-봇 신경가소성 종합 평가 리포트")
        print("#" * 80)
        
        for level, rs in results_by_layer.items():
            success_rs = [r for r in rs if r["status"] == "success"]
            if not success_rs: continue
            
            avg_total = statistics.mean([r["total_time_ms"] for r in success_rs])
            avg_llm = statistics.mean([r["llm_latency_ms"] for r in success_rs])
            avg_mem = statistics.mean([r["memory_overhead_ms"] for r in success_rs])
            providers = set([r["provider"] for r in success_rs])
            
            print(f"\n🧠 [{level} 계층 평가]")
            print(f"- 선택된 엔진: {', '.join(providers)}")
            print(f"- 평균 전체 응답 속도: {avg_total:.0f}ms")
            print(f"  ├─ LLM 생성 (Thinking): {avg_llm:.0f}ms ({avg_llm/avg_total*100:.1f}%)")
            print(f"  └─ 임베딩/검색/네트워크: {avg_mem:.0f}ms ({avg_mem/avg_total*100:.1f}%)")
            
            if level == "L1":
                if avg_mem < 100:
                    print("✅ L1 최적화 성공: 메모리 조회 생략됨 (Overhead 최소)")
                else:
                    print("⚠️ L1 최적화 필요: 오버헤드가 높음")
            elif level == "L3":
                print(f"ℹ️ 임베딩 부하 확인: 약 {avg_mem:.0f}ms 소요됨")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
