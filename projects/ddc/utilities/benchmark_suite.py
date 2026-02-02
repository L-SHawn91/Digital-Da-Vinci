#!/usr/bin/env python3
"""
D-CNS Performance Benchmark Suite (v1.0)
학술 논문 및 성능 최적화를 위한 정량적 데이터 수집 도구
"""

import os
import sys
import time
import json
import asyncio
import statistics
from datetime import datetime
from typing import Dict, List, Any

# 프로젝트 루트 경로 설정
sys.path.append(os.getcwd())

try:
    from projects.ddc.brain.brain_core.chat_engine import get_chat_engine
except ImportError:
    print("❌ 프로젝트 경로 설정 오류. Root에서 실행해주세요.")
    sys.exit(1)

class BenchmarkSuite:
    def __init__(self):
        self.engine = get_chat_engine()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": "Local (MacBook)",
            "layers": {}
        }
        
    async def measure_latency(self, layer: str, model_id: str, prompt: str, trials: int = 3) -> Dict:
        """단일 모델 Latency 및 성공률 측정"""
        print(f"\n🧪 Testing {layer} [{model_id}] ({trials} trials)...")
        latencies = []
        errors = 0
        
        for i in range(trials):
            start_time = time.time()
            try:
                # ChatEngine의 내부 메서드를 직접 호출하거나 get_response 호출
                # 여기서는 라우팅 테스트를 겸해 get_response 사용하되, 특정 키워드로 유도
                response = await self.engine.get_response(999999, prompt)
                duration = (time.time() - start_time) * 1000 # ms
                
                if "⚠️" in response or "Error" in response:
                    print(f"   Trial {i+1}: ❌ Failed ({duration:.1f}ms)")
                    errors += 1
                else:
                    print(f"   Trial {i+1}: ✅ {duration:.1f}ms")
                    latencies.append(duration)
                    
            except Exception as e:
                print(f"   Trial {i+1}: 💥 Exception: {e}")
                errors += 1
            
            # Rate Limit 방지
            await asyncio.sleep(1)

        if not latencies:
            return {"avg_ms": 0, "p99_ms": 0, "success_rate": 0.0}

        return {
            "model": model_id,
            "samples": trials,
            "avg_ms": round(statistics.mean(latencies), 2),
            "min_ms": round(min(latencies), 2),
            "max_ms": round(max(latencies), 2),
            "p99_ms": round(statistics.quantiles(latencies, n=100)[98] if len(latencies) > 1 else max(latencies), 2),
            "success_rate": round((trials - errors) / trials * 100, 1)
        }

    async def run_full_benchmark(self):
        """L1-L4 전체 계층 벤치마크 수행"""
        print("="*60)
        print("🚀 D-CNS Neural Benchmark Started")
        print("="*60)

        # Test Cases (각 레이어를 유도하는 프롬프트)
        scenarios = [
            ("L1", "L1 Reflexive", "안녕! 빨리 대답해줘. (Speed Test)"),
            ("L2", "L2 Affective", "오늘 연구가 너무 힘들어서 좀 우울해. (Emotion Test)"),
            ("L3", "L3 Cognitive", "D-CNS 아키텍처의 장점을 논리적으로 분석해줘. (Logic Test)"),
            ("L4", "L4 NeuroNet", "Python으로 생명게임 구현하는 코드 짜줘. (Coding Test)")
        ]

        total_start = time.time()

        for layer_code, layer_name, prompt in scenarios:
            # 해당 레이어의 대표 모델 (ChatEngine 로직 참조)
            # 동적 라우팅이므로 실제 호출된 모델이 다를 수 있음 -> 로그 확인 필요하지만
            # 여기서는 성능 지표 수집에 집중
            
            result = await self.measure_latency(layer_code, "Auto-Routed", prompt, trials=3)
            self.results["layers"][layer_name] = result

        total_duration = time.time() - total_start
        self.results["total_duration_sec"] = round(total_duration, 2)
        
        self.save_report()

    def save_report(self):
        """결과 레포트 저장"""
        filename = f"docs/reports/benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 디렉토리 확인
        os.makedirs("docs/reports", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        print("\n" + "="*60)
        print(f"💾 Benchmark Report Saved: {filename}")
        print("="*60)
        
        # 요약 출력
        print(f"\n📊 Summary (Environment: {self.results['environment']})")
        for layer, data in self.results["layers"].items():
            status = "🟢" if data['success_rate'] > 90 else "🔴"
            print(f"{status} {layer}: {data['avg_ms']}ms (Success: {data['success_rate']}%)")

if __name__ == "__main__":
    benchmark = BenchmarkSuite()
    asyncio.run(benchmark.run_full_benchmark())
