
"""
일주기 리듬 (Circadian Rhythm) Engine v1.0
24시간 주기 자가 진단 및 신경가소성 지표 정규화 (Sleep-Cycle Learning)
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger("CircadianRhythm")

class CircadianRhythm:
    def __init__(self, engine):
        self.engine = engine  # ChatEngine instance
        self.is_running = False
        self.diagnostic_queries = {
            "L1": "Hello",
            "L2": "What are your core functions?",
            "L3": "Explain the significance of organoid research in 2026.",
            "L4": "Write a Python script for binary search."
        }

    async def start_clock(self, interval_seconds: int = 86400):
        """24시간 주기로 자가 진단 시작"""
        if self.is_running:
            return
            
        self.is_running = True
        logger.info("🕒 Circadian Rhythm: Sleep-Cycle Learning started (24h interval).")
        
        while self.is_running:
            try:
                # 1. 자가 진단 수행
                await self.run_full_diagnostic()
                
                # 2. 다음 주기까지 대기
                logger.info(f"💤 Circadian Rhythm: Entering sleep mode. Next diagnostic in {interval_seconds/3600} hours.")
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"⚠️ Circadian Rhythm Error: {e}")
                await asyncio.sleep(600) # 오류 시 10분 후 재시도

    async def run_full_diagnostic(self):
        """모든 가용 모델 전수 조사 (Self-Testing)"""
        logger.info("🧠 [Diagnostic] Starting Full System Examination (Circadian Cycle)...")
        
        # 1. 모든 계층의 후보 모델 추출
        all_candidates = []
        for level in ["L4", "L3", "L2", "L1"]: # 고부하 -> 저부하 순
            for candidate in self.engine.candidates.get(level, []):
                # 중복 방지 (여러 계층에 속할 수 있음)
                if candidate["id"] not in [c["id"] for c in all_candidates]:
                    all_candidates.append(candidate)

        # 2. 모델별 테스트 수행
        results = []
        for candidate in all_candidates:
            model_id = candidate["id"]
            # 해당 모델이 속한 첫 번째 계층 찾기
            target_level = "L3"
            for level, cands in self.engine.candidates.items():
                if any(c["id"] == model_id for c in cands):
                    target_level = level
                    break
            
            query = self.diagnostic_queries.get(target_level, "Self-diagnostic pulse.")
            
            logger.info(f"🧪 [Diagnostic] Testing Model: {model_id} (Level: {target_level})")
            
            try:
                # 강제 모델 지정 호출
                response = await self.engine.get_response(
                    user_id=8888, # System User ID 
                    text=query, 
                    force_model_id=model_id
                )
                status = "PASS"
            except Exception as e:
                logger.error(f"❌ [Diagnostic] Model {model_id} Failed: {e}")
                status = f"FAIL: {str(e)}"
            
            results.append({"model": model_id, "status": status})
            await asyncio.sleep(2) # API Rate Limit 방지

        logger.info(f"✅ [Diagnostic] Cycle Completed. Tested {len(all_candidates)} models.")
        return results

    def stop(self):
        self.is_running = False
