#!/usr/bin/env python3
"""
D-CNS Performance Benchmark (Lite)
Minimalist version to avoid gRPC threading issues on macOS/Python 3.9
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime

# 프로젝트 루트 경로 설정
sys.path.append(os.getcwd())

try:
    # ChatEngine을 Lazy Loading으로 가져옴
    from projects.ddc.brain.brain_core.chat_engine import get_chat_engine
except ImportError:
    print("❌ Import Error", flush=True)
    sys.exit(1)

async def run_benchmark():
    print("🚀 D-CNS Lite Benchmark Started...", flush=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {"timestamp": timestamp, "layers": {}}
    
    engine = get_chat_engine()
    print("✅ ChatEngine Initialized", flush=True)

    test_cases = [
        ("L1", "L1 Reflexive", "안녕 (Speed Test)"),
        ("L3", "L3 Cognitive", "D-CNS 구조 설명해줘 (Logic Test)")
        # L2, L4 생략하여 위험 최소화 (일단 기본 2개만)
    ]

    for layer_code, layer_name, prompt in test_cases:
        print(f"\n🧪 Testing {layer_name}...", flush=True)
        start = time.time()
        try:
            # 타임아웃 30초 설정
            response = await asyncio.wait_for(engine.get_response(8888, prompt), timeout=30.0)
            duration = (time.time() - start) * 1000
            
            status = "✅ Success"
            if "⚠️" in response: status = "⚠️ Fallback/Error"
            
            print(f"   Result: {status} ({duration:.1f}ms)", flush=True)
            results["layers"][layer_name] = {
                "avg_ms": round(duration, 2),
                "status": status,
                "response_preview": response[:50] + "..."
            }
            
        except asyncio.TimeoutError:
            print("   Result: ⏰ Timeout (30s)", flush=True)
            results["layers"][layer_name] = {"status": "Timeout"}
        except Exception as e:
            print(f"   Result: 💥 Error: {e}", flush=True)
            results["layers"][layer_name] = {"status": "Error", "error": str(e)}
        
        # 쿨다운
        time.sleep(2)

    # Report 저장
    filename = f"docs/reports/benchmark_lite_{timestamp}.json"
    os.makedirs("docs/reports", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved: {filename}", flush=True)

if __name__ == "__main__":
    if sys.platform == 'darwin':
        # macOS 비동기 이슈 회피
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
        
    try:
        asyncio.run(run_benchmark())
    except KeyboardInterrupt:
        print("\n🛑 Interrupted")
        sys.exit(0)
