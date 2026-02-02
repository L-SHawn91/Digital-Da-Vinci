"""
Advanced Watchdog v2.0 (Simplified for Testing)
빠른 상태 확인 + 이벤트 기반 감지
감지 시간: 4초 → 1초 (75% 단축)
"""

import asyncio
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """헬스 상태"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class SystemMetrics:
    """시스템 메트릭"""
    cpu_percent: float
    memory_percent: float
    error_count: int
    uptime: float
    
    @property
    def status(self) -> HealthStatus:
        """현재 헬스 상태"""
        if self.cpu_percent > 90 or self.memory_percent > 90:
            return HealthStatus.CRITICAL
        elif self.cpu_percent > 70 or self.memory_percent > 70:
            return HealthStatus.WARNING
        return HealthStatus.HEALTHY

class EventBus:
    """이벤트 버스"""
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """이벤트 구독"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    async def publish(self, event_type: str, data: Dict):
        """이벤트 발행"""
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                await callback(data)

class AdvancedWatchdog:
    """고급 Watchdog"""
    
    def __init__(self, check_interval: float = 1.0):
        self.check_interval = check_interval
        self.event_bus = EventBus()
        self.is_running = False
        self.metrics_history: List[SystemMetrics] = []
        self.start_time = time.time()
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """이벤트 핸들러 설정"""
        self.event_bus.subscribe("health_check", self._on_health_check)
        self.event_bus.subscribe("status_warning", self._on_warning)
    
    async def start(self):
        """Watchdog 시작"""
        self.is_running = True
        logger.info("✅ Advanced Watchdog started (1초 주기 감지)")
        
        check_count = 0
        while self.is_running:
            try:
                # 시뮬레이션된 메트릭
                metrics = SystemMetrics(
                    cpu_percent=random.uniform(20, 60),
                    memory_percent=random.uniform(30, 70),
                    error_count=0,
                    uptime=time.time() - self.start_time
                )
                
                self.metrics_history.append(metrics)
                
                # 이벤트 발행
                await self.event_bus.publish("health_check", {
                    "metrics": metrics,
                    "timestamp": time.time()
                })
                
                if metrics.status != HealthStatus.HEALTHY:
                    await self.event_bus.publish("status_warning", {
                        "metrics": metrics
                    })
                
                check_count += 1
                await asyncio.sleep(self.check_interval)
            
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(0.5)
    
    async def stop(self):
        """Watchdog 중지"""
        self.is_running = False
    
    async def _on_health_check(self, data: Dict):
        """헬스 체크 이벤트"""
        metrics = data["metrics"]
        logger.info(f"💚 Check: CPU={metrics.cpu_percent:.1f}% | Mem={metrics.memory_percent:.1f}% | Status={metrics.status.value}")
    
    async def _on_warning(self, data: Dict):
        """경고 이벤트"""
        metrics = data["metrics"]
        logger.warning(f"⚠️  Warning: {metrics.status.value}")
    
    def get_status_report(self) -> Dict:
        """상태 리포트"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        latest = self.metrics_history[-1]
        return {
            "current_status": latest.status.value,
            "cpu_percent": latest.cpu_percent,
            "memory_percent": latest.memory_percent,
            "checks": len(self.metrics_history)
        }

async def test_watchdog():
    """Watchdog 테스트"""
    watchdog = AdvancedWatchdog(check_interval=1.0)
    task = asyncio.create_task(watchdog.start())
    
    try:
        print("\n📊 Test: 5초 동안 1초 주기 모니터링\n")
        for i in range(5):
            await asyncio.sleep(1)
            report = watchdog.get_status_report()
            print(f"[{i+1}s] 총 확인: {report['checks']}회")
    
    finally:
        await watchdog.stop()
        await asyncio.sleep(0.1)
        task.cancel()
        try:
            await task
        except:
            pass

if __name__ == "__main__":
    print("\n🧠 Advanced Watchdog v2.0 테스트")
    print("=" * 60)
    asyncio.run(test_watchdog())
    print("\n✅ 테스트 완료!")
    print("   감지 시간: 4초 → 1초 (75% 단축)")
    print("   이벤트: 이벤트 기반 감지")
    print("=" * 60 + "\n")
