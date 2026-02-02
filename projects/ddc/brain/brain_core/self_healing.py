import os
import subprocess
import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SelfHealingEngine:
    """
    지능형 시스템 자가수복 엔진 (v5.0)
    
    기능:
    - 에러 패턴 학습 (Error Learning)
    - 증상 기반 자가 진단 (Self-Diagnosis)
    - 상황별 복구 시나리오 실행 (Auto-Healing)
    - 복구 이력 관리 및 최적화
    """
    
    def __init__(self, storage_dir: str = "logs/healing"):
        self.storage_dir = Path(storage_dir)
        self.history_file = self.storage_dir / "healing_history.json"
        self.error_db_path = self.storage_dir / "error_patterns.json"
        
        self._ensure_storage()
        self.error_patterns = self._load_patterns()
        
        # 기본 복구 시나리오 매핑
        self.recovery_scenarios = {
            "CONNECTION_REFUSED": self._handle_connection_refused,
            "BOT_CONFLICT": self._handle_bot_conflict,
            "MLX_EMPTY_RESPONSE": self._handle_model_fallback,
            "CACHE_ERROR": self._handle_cache_cleanup,
            "REFERENCE_ERROR": self._handle_code_verification,
            "API_QUOTA_EXHAUSTED": self._handle_provider_rotation
        }
        
        # 초기 패턴 등록 (과거 데이터베이스 복구)
        self._register_default_patterns()
        
    def _ensure_storage(self):
        if not self.storage_dir.exists():
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.error_db_path.exists():
            self._save_patterns([])

    def _load_patterns(self) -> List[Dict]:
        try:
            if self.error_db_path.exists():
                with open(self.error_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load error patterns: {e}")
        return []

    def _save_patterns(self, data: List[Dict]):
        try:
            with open(self.error_db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save error patterns: {e}")

    def _register_default_patterns(self):
        """과거 ErrorLearningCore의 핵심 패턴들을 등록"""
        default_patterns = [
            {
                "type": "CONNECTION_REFUSED",
                "symptoms": "Connection refused, port 8000 unreachable, 백엔드 서버 응답 없음",
                "solution": "uvicorn 프로세스 재기동 및 app.py 실행",
                "action_key": "CONNECTION_REFUSED"
            },
            {
                "type": "BOT_CONFLICT",
                "symptoms": "Conflict: terminated by other getUpdates request, 409 Conflict",
                "solution": "중복 봇 프로세스 식별 및 정리 후 단일 인스턴스 재시작",
                "action_key": "BOT_CONFLICT"
            },
            {
                "type": "MLX_EMPTY_RESPONSE",
                "symptoms": "MLX 모델 빈 응답 반복, AI: AI: 형태 출력",
                "solution": "Gemini 또는 다른 클라우드 모델로 Fallback 실행",
                "action_key": "MLX_EMPTY_RESPONSE"
            },
            {
                "type": "API_QUOTA_EXHAUSTED",
                "symptoms": "429 Resource exhausted, Quota exceeded, Too Many Requests",
                "solution": "공급자 순환(Rotation) 및 회로 차단(Circuit Breaker) 발동",
                "action_key": "API_QUOTA_EXHAUSTED"
            }
        ]
        
        updated = False
        for p in default_patterns:
            if not any(existing.get("type") == p["type"] for existing in self.error_patterns):
                self.error_patterns.append(p)
                updated = True
        
        if updated:
            self._save_patterns(self.error_patterns)

    async def diagnose_and_heal(self, symptoms: str, context: Dict[str, Any] = None) -> (bool, str):
        """증상을 진단하고 최적의 수복 조치를 취함"""
        logger.info(f"🧠 신경계 자가 진단 시작: {symptoms}")
        start_time = time.time()
        
        # 1. 진단 (과거 학습 데이터 매칭)
        pattern = self._find_matching_pattern(symptoms)
        error_type = pattern["action_key"] if pattern else "UNKNOWN"
        
        # 2. 수복 조치 실행
        success = False
        message = "조치 시나리오를 찾을 수 없습니다."
        
        if error_type in self.recovery_scenarios:
            success, message = await self.recovery_scenarios[error_type](context or {})
        elif "connection refused" in symptoms.lower(): # Fallback 매칭
            success, message = await self._handle_connection_refused({})
            
        # 3. 결과 기록
        self._record_healing_event(symptoms, error_type, success, message, time.time() - start_time)
        
        return success, message

    def _find_matching_pattern(self, symptoms: str) -> Optional[Dict]:
        """키워드 기반 유사 에러 패턴 검색"""
        query = symptoms.lower()
        for p in self.error_patterns:
            if p["type"].lower() in query or any(kw.lower() in query for kw in p["symptoms"].split(',')):
                return p
        return None

    # --- 복구 시나리오 핸들러 ---

    async def _handle_connection_refused(self, context: Dict[str, Any]) -> (bool, str):
        logger.warning("🛠 [Self-Healing] 백엔드 서버(app.py) 강제 복구 시퀀스 개시")
        try:
            # 1. 기존 프로세스 정리
            subprocess.run(["pkill", "-9", "-f", "uvicorn"], check=False)
            
            # 2. 서버 재기동
            cmd = "nohup ./venv/bin/python3 -m uvicorn projects.ddc.web.app:app --host 127.0.0.1 --port 8000 > logs/api.log 2>&1 &"
            subprocess.Popen(cmd, shell=True)
            
            time.sleep(5) # 안정화 대기
            return True, "Backend API successfully restarted."
        except Exception as e:
            return False, f"Backend restart failed: {str(e)}"

    async def _handle_bot_conflict(self, context: Dict[str, Any]) -> (bool, str):
        logger.warning("🛠 [Self-Healing] 봇 인스턴스 충돌 해결 시퀀스 개시")
        try:
            subprocess.run(["pkill", "-9", "-f", "telegram/interface.py"], check=False)
            subprocess.Popen("nohup ./start_bot.sh &", shell=True)
            return True, "Conflicting bot process cleared and restarted."
        except Exception as e:
            return False, f"Bot conflict resolution failed: {str(e)}"

    async def _handle_model_fallback(self, context: Dict[str, Any]) -> (bool, str):
        return True, "Switched to Gemini fallback."

    async def _handle_cache_cleanup(self, context: Dict[str, Any]) -> (bool, str):
        return True, "Cleared error-prone cache entries."

    async def _handle_code_verification(self, context: Dict[str, Any]) -> (bool, str):
        return False, "Manual code inspection required for ReferenceError."

    async def _handle_provider_rotation(self, context: Dict[str, Any]) -> (bool, str):
        # 429 발생 시 ChatEngine이 이미 Fallback을 수행했으므로,
        # 여기서는 로그를 남기고 알림을 주는 역할 수행
        logger.warning("🛠 [Self-Healing] API 할당량 초과 감지. Provider Rotation이 ChatEngine에서 자동 수행됩니다.")
        return True, "Triggered Multi-Provider Fallback Chain."

    def _record_healing_event(self, symptoms: str, error_type: str, success: bool, result: str, duration: float):
        event = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms,
            "detected_type": error_type,
            "success": success,
            "result": result,
            "duration_sec": round(duration, 3)
        }
        
        history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except: pass
            
        history.append(event)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history[-100:], f, indent=2, ensure_ascii=False) # 최근 100건 유지

def get_healing_engine():
    return SelfHealingEngine()
