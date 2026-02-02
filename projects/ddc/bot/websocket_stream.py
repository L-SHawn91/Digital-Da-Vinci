"""
🔌 SHawn-Brain WebSocket 스트리밍 통합
텔레그램 봇에 실시간 신경계 데이터를 스트리밍합니다.

기능:
- 신경계 상태 실시간 업데이트
- 카트리지 성능 모니터링
- API 호출 추적
- 알림 시스템
"""

import asyncio
import websockets
import json
import logging
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================

class AlertLevel(Enum):
    """알림 수준"""
    INFO = "ℹ️"
    WARNING = "⚠️"
    CRITICAL = "🔴"
    SUCCESS = "✅"


@dataclass
class NeuralUpdate:
    """신경계 업데이트"""
    timestamp: str
    levels: Dict[str, float]
    api_calls: Dict[str, int]
    total_calls: int
    average_health: float
    status: str


@dataclass
class Alert:
    """알림"""
    level: AlertLevel
    title: str
    message: str
    timestamp: str


# ============================================================================
# WebSocket Stream Handler
# ============================================================================

class WebSocketStream:
    """WebSocket 스트림 핸들러"""

    def __init__(self, uri: str = "ws://localhost:8000/ws/neural_stream"):
        """초기화"""
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.callbacks: List[Callable] = []
        self.alerts: List[Alert] = []
        self.latest_update: Optional[NeuralUpdate] = None
        self.history: List[NeuralUpdate] = []
        self.max_history = 100

    async def connect(self):
        """WebSocket 연결"""
        try:
            logger.info(f"🔌 WebSocket 연결 중: {self.uri}")
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info("✅ WebSocket 연결 성공")
            return True
        except Exception as e:
            logger.error(f"❌ WebSocket 연결 실패: {e}")
            self.connected = False
            return False

    async def disconnect(self):
        """연결 해제"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("✅ WebSocket 연결 해제")

    async def start_streaming(self):
        """스트리밍 시작"""
        if not self.connected:
            success = await self.connect()
            if not success:
                return

        try:
            logger.info("📡 신경계 스트리밍 시작")
            async for message in self.websocket:
                await self._handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("⚠️ WebSocket 연결이 끊어졌습니다")
            self.connected = False
        except Exception as e:
            logger.error(f"❌ 스트리밍 오류: {e}")
            self.connected = False

    async def _handle_message(self, message: str):
        """메시지 처리"""
        try:
            data = json.loads(message)
            update = self._parse_neural_update(data)

            # 히스토리 추가
            self.latest_update = update
            self.history.append(update)
            if len(self.history) > self.max_history:
                self.history.pop(0)

            # 알림 확인
            self._check_alerts(update)

            # 콜백 실행
            for callback in self.callbacks:
                try:
                    await callback(update)
                except Exception as e:
                    logger.error(f"콜백 오류: {e}")

        except json.JSONDecodeError:
            logger.error(f"JSON 파싱 오류: {message}")
        except Exception as e:
            logger.error(f"메시지 처리 오류: {e}")

    def _parse_neural_update(self, data: Dict) -> NeuralUpdate:
        """신경계 업데이트 파싱"""
        return NeuralUpdate(
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            levels=data.get('levels', {}),
            api_calls=data.get('api_calls', {}),
            total_calls=data.get('api_calls', {}).get('total', 0),
            average_health=data.get('levels', {}).get('avg', 0.5),
            status=self._determine_status(data.get('levels', {}))
        )

    def _determine_status(self, levels: Dict) -> str:
        """상태 결정"""
        avg = levels.get('avg', 0.5)
        if avg >= 0.9:
            return "🟢 excellent"
        elif avg >= 0.7:
            return "🟢 healthy"
        elif avg >= 0.5:
            return "🟡 normal"
        elif avg >= 0.3:
            return "🟠 warning"
        else:
            return "🔴 critical"

    def _check_alerts(self, update: NeuralUpdate):
        """알림 확인"""
        # 신경계 건강도 낮음
        if update.average_health < 0.7:
            self.alerts.append(Alert(
                level=AlertLevel.WARNING,
                title="신경계 건강도 낮음",
                message=f"평균 건강도: {update.average_health:.2f}",
                timestamp=update.timestamp
            ))

        # 신경계 위험 상태
        if update.average_health < 0.3:
            self.alerts.append(Alert(
                level=AlertLevel.CRITICAL,
                title="신경계 위험 상태!",
                message=f"긴급 조치 필요 (건강도: {update.average_health:.2f})",
                timestamp=update.timestamp
            ))

        # 특정 계층 문제
        for level, health in update.levels.items():
            if level != 'avg' and health < 0.5:
                self.alerts.append(Alert(
                    level=AlertLevel.WARNING,
                    title=f"{level} 문제",
                    message=f"건강도 낮음: {health:.2f}",
                    timestamp=update.timestamp
                ))

    def register_callback(self, callback: Callable):
        """콜백 등록"""
        self.callbacks.append(callback)
        logger.info(f"✅ 콜백 등록: {callback.__name__}")

    def unregister_callback(self, callback: Callable):
        """콜백 제거"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            logger.info(f"✅ 콜백 제거: {callback.__name__}")

    def get_latest_update(self) -> Optional[NeuralUpdate]:
        """최신 업데이트 획득"""
        return self.latest_update

    def get_history(self, limit: int = 10) -> List[NeuralUpdate]:
        """히스토리 획득"""
        return self.history[-limit:]

    def get_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """알림 획득"""
        if level:
            return [a for a in self.alerts if a.level == level]
        return self.alerts

    def clear_alerts(self):
        """알림 초기화"""
        self.alerts = []

    def format_update_text(self, update: Optional[NeuralUpdate] = None) -> str:
        """업데이트를 텍스트로 포맷"""
        if update is None:
            update = self.latest_update

        if not update:
            return "📡 아직 데이터를 받지 못했습니다."

        # 진행 바 생성
        bars = []
        for level, health in update.levels.items():
            if level != 'avg':
                bar = "█" * int(health * 10) + "░" * (10 - int(health * 10))
                bars.append(f"{level}: {bar} {health:.2f}")

        text = f"""
📊 **신경계 실시간 데이터**

{chr(10).join(bars)}

**평균 건강도:** {update.average_health:.2f}
**상태:** {update.status}
**총 API 호출:** {update.total_calls}
**업데이트:** {update.timestamp}
        """
        return text

    def format_alerts_text(self) -> str:
        """알림을 텍스트로 포맷"""
        if not self.alerts:
            return "✅ 현재 알림이 없습니다."

        text = "🔔 **활성 알림**\n\n"
        for alert in self.alerts[-5:]:  # 최근 5개만
            text += f"{alert.level.value} **{alert.title}**\n"
            text += f"  └ {alert.message}\n\n"

        return text


# ============================================================================
# Telegram Integration
# ============================================================================

class TelegramStreamListener:
    """텔레그램을 위한 스트림 리스너"""

    def __init__(self, stream: WebSocketStream, send_message_func):
        """초기화"""
        self.stream = stream
        self.send_message = send_message_func
        self.user_subscriptions: Dict[int, bool] = {}
        self.update_frequency = 5  # 5초마다 업데이트

    async def subscribe_user(self, user_id: int):
        """사용자 구독"""
        self.user_subscriptions[user_id] = True
        logger.info(f"✅ 사용자 {user_id} 구독")
        await self.send_message(
            user_id,
            "📡 실시간 모니터링 시작\n"
            "신경계 데이터를 5초마다 수신합니다."
        )

    async def unsubscribe_user(self, user_id: int):
        """사용자 구독 취소"""
        if user_id in self.user_subscriptions:
            del self.user_subscriptions[user_id]
            logger.info(f"✅ 사용자 {user_id} 구독 취소")
            await self.send_message(
                user_id,
                "📡 실시간 모니터링 중지"
            )

    async def broadcast_update(self):
        """모든 구독자에게 업데이트 전송"""
        update = self.stream.get_latest_update()
        if not update:
            return

        text = self.stream.format_update_text(update)

        for user_id in self.user_subscriptions:
            if self.user_subscriptions[user_id]:
                try:
                    await self.send_message(user_id, text)
                except Exception as e:
                    logger.error(f"메시지 전송 오류 (user {user_id}): {e}")

    async def broadcast_alert(self, alert: Alert):
        """모든 구독자에게 알림 전송"""
        text = f"{alert.level.value} **{alert.title}**\n\n{alert.message}"

        for user_id in self.user_subscriptions:
            if self.user_subscriptions[user_id]:
                try:
                    await self.send_message(user_id, text)
                except Exception as e:
                    logger.error(f"알림 전송 오류 (user {user_id}): {e}")


# ============================================================================
# Streaming Controller
# ============================================================================

class StreamController:
    """스트리밍 컨트롤러"""

    def __init__(self, uri: str = "ws://localhost:8000/ws/neural_stream"):
        """초기화"""
        self.stream = WebSocketStream(uri)
        self.running = False
        self.stream_task = None

    async def start(self):
        """스트리밍 시작"""
        if self.running:
            logger.warning("⚠️ 스트리밍이 이미 실행 중입니다.")
            return

        self.running = True
        self.stream_task = asyncio.create_task(self.stream.start_streaming())
        logger.info("✅ 스트리밍 시작")

    async def stop(self):
        """스트리밍 중지"""
        if not self.running:
            logger.warning("⚠️ 스트리밍이 실행 중이지 않습니다.")
            return

        self.running = False
        if self.stream_task:
            self.stream_task.cancel()
            try:
                await self.stream_task
            except asyncio.CancelledError:
                pass
        await self.stream.disconnect()
        logger.info("✅ 스트리밍 중지")

    def get_status(self) -> str:
        """상태 조회"""
        status = "🟢 실행 중" if self.running else "🔴 중지됨"
        connected = "✅ 연결됨" if self.stream.connected else "❌ 미연결"
        return f"{status} | {connected}"


if __name__ == "__main__":
    # 테스트 코드
    import sys

    logging.basicConfig(level=logging.INFO)

    async def test():
        stream = WebSocketStream()

        # 콜백 등록
        async def on_update(update: NeuralUpdate):
            print(stream.format_update_text(update))

        stream.register_callback(on_update)

        # 스트리밍 시작
        try:
            await stream.start_streaming()
        except KeyboardInterrupt:
            print("\n✅ 테스트 종료")
            await stream.disconnect()

    try:
        asyncio.run(test())
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)

__all__ = [
    'WebSocketStream',
    'TelegramStreamListener',
    'StreamController',
    'NeuralUpdate',
    'Alert',
    'AlertLevel'
]
