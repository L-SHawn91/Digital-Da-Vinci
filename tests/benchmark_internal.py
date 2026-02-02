#!/usr/bin/env python3
"""
D-CNS Zero-Base 3-Round Benchmark
초기화된 상태에서 모든 모델을 3회 연속 테스트 (Internal Module Load)
"""

import asyncio
import sys
import os
import logging
import json

# 프로젝트 경로 설정
sys.path.append(os.getcwd())

# 로깅 설정 (콘솔 출력용)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Benchmark")

from projects.ddc.brain.brain_core.chat_engine import ChatEngine, get_chat_engine
from projects.ddc.brain.neuronet.circadian_rhythm import CircadianRhythm

async def run_benchmark():
    print("=" * 80)
    print("🧠 D-CNS Zero-Base 3-Round Benchmark (Internal Mode)")
    print("=" * 80)
    
    # 1. 엔진 초기화 (여기서 Priors만 로드됨)
    print("⏳ 엔진 초기화 중...")
    engine = await get_chat_engine_async() # 비동기 래퍼 필요할 수 있음
    # get_chat_engine은 동기 함수지만 내부 init은 동기.
    # 하지만 실제로는 app.py에서 lifespan으로 띄우는 방식임.
    # 여기서는 직접 인스턴스화
    
    print(f"✅ 엔진 로드 완료. 활성 클라이언트: {list(engine.clients.keys())}")
    
    circadian = CircadianRhythm(engine)
    
    # 2. 3라운드 수행
    for round_num in range(1, 4):
        print(f"\n🥊 [Round {round_num}/3] 자가 진단 사이클 시작...")
        results = await circadian.run_full_diagnostic()
        
        success_cnt = len([r for r in results if r['status']=='PASS'])
        print(f"   => 결과: {success_cnt}/{len(results)} 성공")
        
    # 3. 결과 리포트 (메모리 덤프)
    print("\n" + "="*80)
    print("🏆 최종 성적표 (3 Rounds Average)")
    print("="*80)
    
    # 메모리 파일 직접 읽기 지양, 엔진 내부 객체 활용
    scores = engine.learner.model_scores
    
    headers = ["Model ID", "Speed", "Quality", "TokEff", "Cost", "Mem", "Rel", "L1 Score", "L3 Score"]
    print(f"{headers[0]:<25} | {headers[1]:<5} | {headers[2]:<5} | {headers[3]:<6} | {headers[4]:<5} | {headers[5]:<3} | {headers[6]:<3} | {headers[7]:<8} | {headers[8]:<8}")
    print("-" * 110)
    
    for mid, s in scores.items():
        sp = s.get("speed", 0.5)
        qu = s.get("quality", 0.5)
        te = s.get("token_eff", 0.5)
        co = s.get("cost", 0.5)
        me = s.get("memory", 0.5)
        re = s.get("reliability", 0.8)
        
        # 계산
        l1_score = (sp * 0.45) + (re * 0.30) + (co * 0.15) + (te * 0.10)
        l3_score = (qu * 0.40) + (te * 0.25) + (me * 0.20) + (sp * 0.15)
        
        print(f"{mid[:25]:<25} | {sp:.2f}  | {qu:.2f}  | {te:.2f}   | {co:.2f}  | {me:.2f} | {re:.2f} | {l1_score:.3f}    | {l3_score:.3f}")

    print("-" * 110)

async def get_chat_engine_async():
    # 동기 함수를 비동기 컨텍스트에서 실행하기 위한 헬퍼 (필요 시)
    return get_chat_engine()

if __name__ == "__main__":
    # 이벤트 루프 이슈 방지
    try:
        asyncio.run(run_benchmark())
    except KeyboardInterrupt:
        print("\n중단됨.")
