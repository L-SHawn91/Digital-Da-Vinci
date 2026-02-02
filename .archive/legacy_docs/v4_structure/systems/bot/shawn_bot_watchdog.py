# shawn_bot_watchdog.py - 숀봇 Watchdog 시스템 (L1 뇌간)

"""
숀봇 안정성 강화 모듈 (Week 1-3)
신경전달물질: 아드레날린
목표: 안정성 3/10 → 10/10 (99.99% 가용성)

Week 1 (이번주): Watchdog 시스템 설계 & 구현
Week 2: 성능 최적화
Week 3: 자동화 완성
"""

import os
import sys
import time
import subprocess
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import signal
import psutil

# ============================================================================
# 1. 로깅 설정 (상세 추적)
# ============================================================================

class WatchdogLogger:
    """모든 이벤트를 기록하는 로거"""
    
    def __init__(self, log_dir: str = "logs/watchdog"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 일일 로그 파일
        self.log_file = self.log_dir / f"{datetime.now().strftime('%Y%m%d')}_watchdog.log"
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("Watchdog")
    
    def log_startup(self, process_name: str):
        self.logger.info(f"🚀 Watchdog 시작 - 모니터링 대상: {process_name}")
    
    def log_process_check(self, is_alive: bool, pid: Optional[int] = None):
        status = "✅ 정상" if is_alive else "❌ 다운"
        msg = f"프로세스 상태 확인: {status}"
        if pid:
            msg += f" (PID: {pid})"
        self.logger.debug(msg)
    
    def log_process_down(self, pid: Optional[int], reason: str = "Unknown"):
        self.logger.critical(f"🔴 프로세스 다운 감지! (PID: {pid}) - 이유: {reason}")
    
    def log_restart_attempt(self, attempt: int):
        self.logger.warning(f"🔧 재시작 시도 #{attempt}")
    
    def log_restart_success(self, new_pid: int, elapsed_ms: int):
        self.logger.info(f"✅ 재시작 성공! (새 PID: {new_pid}, 소요시간: {elapsed_ms}ms)")
    
    def log_restart_failure(self, error: str):
        self.logger.error(f"❌ 재시작 실패! 에러: {error}")
    
    def log_dependency_check(self, module: str, status: str):
        self.logger.info(f"📦 의존성 확인: {module} - {status}")


# ============================================================================
# 2. 프로세스 모니터링 (5초마다)
# ============================================================================

class ProcessMonitor:
    """프로세스 상태를 지속적으로 모니터링"""
    
    def __init__(self, process_pid: Optional[int] = None):
        self.process_pid = process_pid
        self.process = None
        self.logger = WatchdogLogger()
        self.is_running = False
    
    def is_process_alive(self) -> bool:
        """프로세스가 실행 중인지 확인"""
        if self.process is None:
            return False
        
        try:
            # psutil을 사용하여 정확한 상태 확인
            proc = psutil.Process(self.process.pid)
            status = proc.status()
            
            # 가능한 상태:
            # psutil.STATUS_RUNNING: 실행 중
            # psutil.STATUS_SLEEPING: 슬립
            # psutil.STATUS_ZOMBIE: 좀비 프로세스
            # psutil.STATUS_STOPPED: 중지
            # psutil.STATUS_DEAD: 종료됨
            
            is_alive = proc.is_running() and status != psutil.STATUS_ZOMBIE
            self.logger.log_process_check(is_alive, self.process.pid)
            return is_alive
        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self.logger.log_process_check(False, self.process_pid)
            return False
    
    def get_process_metrics(self) -> Dict:
        """프로세스 리소스 사용량 조회"""
        if self.process is None:
            return {}
        
        try:
            proc = psutil.Process(self.process.pid)
            return {
                "pid": self.process.pid,
                "status": proc.status(),
                "memory_mb": proc.memory_info().rss / 1024 / 1024,
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "num_threads": proc.num_threads(),
                "open_files": len(proc.open_files()),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}


# ============================================================================
# 3. 의존성 자동 복구
# ============================================================================

class DependencyRecovery:
    """import 실패 시 자동 복구"""
    
    def __init__(self):
        self.logger = WatchdogLogger()
        self.required_modules = [
            "python-telegram-bot",
            "aiohttp",
            "pillow",
            "requests",
            "pandas",
        ]
    
    def check_dependencies(self) -> Dict[str, bool]:
        """모든 의존성 확인"""
        status = {}
        
        for module in self.required_modules:
            try:
                # import name을 module name으로 변환
                import_name = module.replace("-", "_")
                __import__(import_name)
                status[module] = True
                self.logger.log_dependency_check(module, "✅ 설치됨")
            except ImportError:
                status[module] = False
                self.logger.log_dependency_check(module, "❌ 미설치")
        
        return status
    
    def auto_install_missing(self) -> bool:
        """누락된 의존성 자동 설치"""
        status = self.check_dependencies()
        missing = [m for m, s in status.items() if not s]
        
        if not missing:
            self.logger.logger.info("✅ 모든 의존성 설치됨")
            return True
        
        self.logger.logger.warning(f"🔧 누락 의존성 자동 설치 중: {missing}")
        
        for module in missing:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", module],
                    capture_output=True,
                    timeout=60
                )
                self.logger.log_dependency_check(module, "✅ 설치 성공")
            except Exception as e:
                self.logger.logger.error(f"❌ {module} 설치 실패: {e}")
                # 대체 모듈 사용 시도
                self._use_fallback_module(module)
        
        return True
    
    def _use_fallback_module(self, module: str):
        """대체 모듈 사용 (선택사항)"""
        fallback_map = {
            "pillow": "PIL",  # 이미 대부분 포함됨
            "requests": "urllib",  # 표준 라이브러리
        }
        
        if module in fallback_map:
            self.logger.logger.info(f"🔄 {module} 대신 {fallback_map[module]} 사용")


# ============================================================================
# 4. 환경 변수 자동 초기화
# ============================================================================

class EnvironmentInitializer:
    """필수 환경 변수 자동 설정"""
    
    def __init__(self):
        self.logger = WatchdogLogger()
        self.required_vars = [
            "TELEGRAM_BOT_TOKEN",
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
        ]
    
    def check_and_initialize(self) -> bool:
        """환경 변수 확인 및 초기화"""
        missing = []
        
        for var in self.required_vars:
            if not os.getenv(var):
                missing.append(var)
                self.logger.logger.warning(f"⚠️  환경 변수 미설정: {var}")
        
        if missing:
            self.logger.logger.critical(f"🔴 필수 환경 변수 누락: {missing}")
            self.logger.logger.info("💡 다음을 설정해주세요:")
            for var in missing:
                self.logger.logger.info(f"   export {var}='your_value'")
            
            # 대기 모드: 환경 변수가 설정될 때까지 기다리기
            self._wait_for_env_vars(missing)
            return False
        
        self.logger.logger.info("✅ 모든 환경 변수 설정됨")
        return True
    
    def _wait_for_env_vars(self, vars_list: List[str], timeout: int = 300):
        """환경 변수 설정될 때까지 대기 (최대 5분)"""
        start = time.time()
        
        while time.time() - start < timeout:
            still_missing = [v for v in vars_list if not os.getenv(v)]
            
            if not still_missing:
                self.logger.logger.info("✅ 환경 변수 감지! 재시작 중...")
                return
            
            self.logger.logger.info(f"⏳ 대기 중... ({int(time.time() - start)}초 경과)")
            time.sleep(5)
        
        self.logger.logger.critical("❌ 타임아웃! 환경 변수 설정 안 됨")


# ============================================================================
# 5. 프로세스 재시작 (< 5초)
# ============================================================================

class ProcessRestarter:
    """프로세스 빠른 재시작 (< 5초 목표)"""
    
    def __init__(self, bot_script: str = "shawn_bot_telegram.py"):
        self.bot_script = bot_script
        self.logger = WatchdogLogger()
        self.max_restart_attempts = 3
        self.restart_delay = 1  # 초 단위
    
    def restart_process(self) -> Optional[subprocess.Popen]:
        """프로세스 재시작"""
        
        for attempt in range(1, self.max_restart_attempts + 1):
            self.logger.log_restart_attempt(attempt)
            
            try:
                start_time = time.time()
                
                # 봇 프로세스 시작
                process = subprocess.Popen(
                    [sys.executable, self.bot_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                
                # 프로세스 시작 확인 (1초 대기)
                time.sleep(1)
                
                if process.poll() is None:  # 프로세스가 실행 중
                    elapsed_ms = int((time.time() - start_time) * 1000)
                    self.logger.log_restart_success(process.pid, elapsed_ms)
                    return process
                else:
                    # 프로세스가 즉시 종료됨
                    self.logger.logger.warning(f"⚠️  프로세스가 즉시 종료됨 (시도 {attempt}/{self.max_restart_attempts})")
                    
                    if attempt < self.max_restart_attempts:
                        time.sleep(self.restart_delay)
                        self.restart_delay *= 2  # 지수 백오프
            
            except Exception as e:
                self.logger.log_restart_failure(str(e))
                
                if attempt < self.max_restart_attempts:
                    time.sleep(self.restart_delay)
        
        self.logger.log_restart_failure("모든 재시작 시도 실패")
        return None


# ============================================================================
# 6. Watchdog 메인 루프 (5초마다 모니터링)
# ============================================================================

class BotWatchdog:
    """메인 Watchdog 시스템"""
    
    def __init__(self, bot_script: str = "shawn_bot_telegram.py"):
        self.logger = WatchdogLogger()
        self.monitor = ProcessMonitor()
        self.restarter = ProcessRestarter(bot_script)
        self.dependency_recovery = DependencyRecovery()
        self.env_init = EnvironmentInitializer()
        
        self.bot_process = None
        self.is_running = False
        self.check_interval = 5  # 초
        
        # 신호 처리 (Ctrl+C 안전 종료)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """안전 종료"""
        self.logger.logger.info("\n🛑 Watchdog 종료 신호 수신")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Watchdog 시작"""
        self.logger.log_startup("SHawn-Bot (Telegram)")
        
        # 1단계: 의존성 확인
        if not self.dependency_recovery.check_dependencies():
            self.logger.logger.warning("⚠️  누락 의존성 감지 - 자동 설치 시작")
            self.dependency_recovery.auto_install_missing()
        
        # 2단계: 환경 변수 확인
        if not self.env_init.check_and_initialize():
            self.logger.logger.error("❌ 환경 설정 실패")
            return
        
        # 3단계: 봇 프로세스 시작
        self.bot_process = self.restarter.restart_process()
        
        if self.bot_process is None:
            self.logger.logger.critical("❌ 봇 시작 실패")
            return
        
        self.is_running = True
        self.monitor.process = self.bot_process
        
        # 4단계: 모니터링 루프
        self._monitoring_loop()
    
    def _monitoring_loop(self):
        """5초마다 프로세스 상태 확인"""
        self.logger.logger.info("✅ Watchdog 모니터링 시작 (5초 주기)")
        
        consecutive_down_count = 0
        
        while self.is_running:
            try:
                # 프로세스 상태 확인
                if not self.monitor.is_process_alive():
                    consecutive_down_count += 1
                    self.logger.logger.warning(
                        f"⚠️  프로세스 다운 감지 (연속: {consecutive_down_count}회)"
                    )
                    
                    if consecutive_down_count >= 2:  # 2회 연속 다운 확인
                        self.logger.log_process_down(self.bot_process.pid)
                        
                        # 재시작 시도
                        new_process = self.restarter.restart_process()
                        if new_process:
                            self.bot_process = new_process
                            self.monitor.process = new_process
                            consecutive_down_count = 0
                        else:
                            self.logger.logger.critical("❌ 프로세스 복구 실패 - Watchdog 중지")
                            self.stop()
                            break
                else:
                    # 프로세스 정상
                    if consecutive_down_count > 0:
                        self.logger.logger.info("✅ 프로세스 복구됨")
                    consecutive_down_count = 0
                    
                    # 프로세스 메트릭 출력
                    metrics = self.monitor.get_process_metrics()
                    if metrics:
                        self.logger.logger.debug(
                            f"📊 메트릭: 메모리 {metrics['memory_mb']:.1f}MB, "
                            f"CPU {metrics['cpu_percent']:.1f}%, "
                            f"스레드 {metrics['num_threads']}"
                        )
                
                # 5초 대기
                time.sleep(self.check_interval)
            
            except KeyboardInterrupt:
                self.logger.logger.info("⌨️  사용자 중단")
                self.stop()
                break
            
            except Exception as e:
                self.logger.logger.error(f"❌ 모니터링 오류: {e}")
                time.sleep(self.check_interval)
    
    def stop(self):
        """Watchdog 중지"""
        self.is_running = False
        
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=5)
                self.logger.logger.info("✅ 봇 프로세스 종료됨")
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
                self.logger.logger.warning("⚠️  봇 프로세스 강제 종료됨")


# ============================================================================
# 7. 실행
# ============================================================================

if __name__ == "__main__":
    watchdog = BotWatchdog()
    watchdog.start()
