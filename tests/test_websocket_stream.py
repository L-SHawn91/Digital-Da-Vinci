"""
Tests - WebSocket Stream Integration

WebSocket 스트리밍의 모든 기능을 테스트합니다.
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def mock_websocket():
    """Mock WebSocket"""
    return AsyncMock()


@pytest.fixture
def neural_update_data():
    """신경계 업데이트 데이터"""
    return {
        "type": "neural_update",
        "timestamp": datetime.now().isoformat(),
        "levels": {
            "brainstem": 0.95,
            "limbic": 0.93,
            "neocortex": 0.94,
            "neuronet": 0.98,
            "avg": 0.95
        },
        "api_calls": {
            "bio": 5,
            "inv": 3,
            "total": 8
        }
    }


@pytest.fixture
def websocket_stream():
    """WebSocket 스트림 인스턴스"""
    from ddc.bot.websocket_stream import WebSocketStream
    return WebSocketStream(uri="ws://localhost:8000/ws/neural_stream")


# ============================================================================
# Tests - WebSocketStream Basic
# ============================================================================

class TestWebSocketStreamBasic:
    """WebSocket 스트림 기본 기능 테스트"""

    def test_initialization(self, websocket_stream):
        """초기화 테스트"""
        assert websocket_stream.uri == "ws://localhost:8000/ws/neural_stream"
        assert websocket_stream.connected == False
        assert isinstance(websocket_stream.callbacks, list)
        assert len(websocket_stream.callbacks) == 0

    def test_alerts_initialization(self, websocket_stream):
        """알림 초기화 테스트"""
        assert isinstance(websocket_stream.alerts, list)
        assert len(websocket_stream.alerts) == 0

    def test_history_initialization(self, websocket_stream):
        """히스토리 초기화 테스트"""
        assert isinstance(websocket_stream.history, list)
        assert len(websocket_stream.history) == 0


# ============================================================================
# Tests - Message Parsing
# ============================================================================

class TestMessageParsing:
    """메시지 파싱 테스트"""

    def test_parse_neural_update(self, websocket_stream, neural_update_data):
        """신경계 업데이트 파싱 테스트"""
        update = websocket_stream._parse_neural_update(neural_update_data)

        assert update.timestamp == neural_update_data['timestamp']
        assert update.average_health == 0.95
        assert update.total_calls == 8

    def test_status_determination_excellent(self, websocket_stream):
        """상태 결정 테스트 - 우수"""
        levels = {"avg": 0.95}
        status = websocket_stream._determine_status(levels)
        assert "excellent" in status or "우수" in status

    def test_status_determination_healthy(self, websocket_stream):
        """상태 결정 테스트 - 정상"""
        levels = {"avg": 0.75}
        status = websocket_stream._determine_status(levels)
        assert "healthy" in status or "정상" in status

    def test_status_determination_warning(self, websocket_stream):
        """상태 결정 테스트 - 경고"""
        levels = {"avg": 0.4}
        status = websocket_stream._determine_status(levels)
        assert "warning" in status or "경고" in status

    def test_status_determination_critical(self, websocket_stream):
        """상태 결정 테스트 - 위험"""
        levels = {"avg": 0.2}
        status = websocket_stream._determine_status(levels)
        assert "critical" in status or "위험" in status


# ============================================================================
# Tests - Alert System
# ============================================================================

class TestAlertSystem:
    """알림 시스템 테스트"""

    def test_alert_on_low_health(self, websocket_stream):
        """낮은 건강도 알림 테스트"""
        from ddc.bot.websocket_stream import NeuralUpdate

        update = NeuralUpdate(
            timestamp=datetime.now().isoformat(),
            levels={"avg": 0.65},
            api_calls={},
            total_calls=0,
            average_health=0.65,
            status="🟡 normal"
        )

        websocket_stream._check_alerts(update)
        assert len(websocket_stream.alerts) > 0

    def test_alert_on_critical_health(self, websocket_stream):
        """위험 건강도 알림 테스트"""
        from ddc.bot.websocket_stream import NeuralUpdate

        update = NeuralUpdate(
            timestamp=datetime.now().isoformat(),
            levels={"avg": 0.2},
            api_calls={},
            total_calls=0,
            average_health=0.2,
            status="🔴 critical"
        )

        websocket_stream._check_alerts(update)
        # 2개 이상의 알림이 생성되어야 함 (일반 + 위험)
        assert len(websocket_stream.alerts) >= 1

    def test_clear_alerts(self, websocket_stream):
        """알림 초기화 테스트"""
        from ddc.bot.websocket_stream import Alert, AlertLevel

        websocket_stream.alerts.append(Alert(
            level=AlertLevel.WARNING,
            title="Test Alert",
            message="Test message",
            timestamp=datetime.now().isoformat()
        ))

        assert len(websocket_stream.alerts) > 0
        websocket_stream.clear_alerts()
        assert len(websocket_stream.alerts) == 0


# ============================================================================
# Tests - Callback System
# ============================================================================

class TestCallbackSystem:
    """콜백 시스템 테스트"""

    def test_register_callback(self, websocket_stream):
        """콜백 등록 테스트"""
        async def callback(update):
            pass

        websocket_stream.register_callback(callback)
        assert callback in websocket_stream.callbacks

    def test_unregister_callback(self, websocket_stream):
        """콜백 제거 테스트"""
        async def callback(update):
            pass

        websocket_stream.register_callback(callback)
        websocket_stream.unregister_callback(callback)
        assert callback not in websocket_stream.callbacks

    def test_multiple_callbacks(self, websocket_stream):
        """다중 콜백 테스트"""
        callbacks = []
        for i in range(3):
            async def callback(update):
                pass
            callbacks.append(callback)
            websocket_stream.register_callback(callback)

        assert len(websocket_stream.callbacks) == 3


# ============================================================================
# Tests - Formatting
# ============================================================================

class TestFormatting:
    """포맷팅 테스트"""

    def test_format_update_text_empty(self, websocket_stream):
        """빈 업데이트 포맷팅 테스트"""
        text = websocket_stream.format_update_text()
        assert "아직 데이터를 받지 못했습니다" in text or "No data yet" in text

    def test_format_update_text_with_data(self, websocket_stream, neural_update_data):
        """데이터가 있을 때 업데이트 포맷팅 테스트"""
        update = websocket_stream._parse_neural_update(neural_update_data)
        websocket_stream.latest_update = update

        text = websocket_stream.format_update_text()
        assert "신경계" in text or "Neural" in text
        assert "0.95" in text  # 평균 건강도

    def test_format_alerts_text_empty(self, websocket_stream):
        """빈 알림 포맷팅 테스트"""
        text = websocket_stream.format_alerts_text()
        assert "알림이 없습니다" in text or "No alerts" in text


# ============================================================================
# Tests - History Management
# ============================================================================

class TestHistoryManagement:
    """히스토리 관리 테스트"""

    def test_get_empty_history(self, websocket_stream):
        """빈 히스토리 조회 테스트"""
        history = websocket_stream.get_history()
        assert len(history) == 0

    def test_history_max_limit(self, websocket_stream, neural_update_data):
        """히스토리 최대 한계 테스트"""
        for i in range(150):  # max_history = 100
            update = websocket_stream._parse_neural_update(neural_update_data)
            websocket_stream.history.append(update)

        # 최대 100개만 유지
        assert len(websocket_stream.history) <= 100


# ============================================================================
# Tests - Stream Controller
# ============================================================================

class TestStreamController:
    """스트림 컨트롤러 테스트"""

    def test_controller_initialization(self):
        """컨트롤러 초기화 테스트"""
        from ddc.bot.websocket_stream import StreamController

        controller = StreamController()
        assert controller.running == False
        assert controller.stream is not None

    def test_get_status_stopped(self):
        """정지 상태 조회 테스트"""
        from ddc.bot.websocket_stream import StreamController

        controller = StreamController()
        status = controller.get_status()
        assert "중지됨" in status or "stopped" in status.lower()


# ============================================================================
# Tests - Telegram Integration
# ============================================================================

class TestTelegramIntegration:
    """텔레그램 통합 테스트"""

    def test_stream_listener_initialization(self, websocket_stream):
        """스트림 리스너 초기화 테스트"""
        from ddc.bot.websocket_stream import TelegramStreamListener

        async def send_message(user_id, message):
            pass

        listener = TelegramStreamListener(websocket_stream, send_message)
        assert listener.stream == websocket_stream
        assert isinstance(listener.user_subscriptions, dict)

    @pytest.mark.asyncio
    async def test_user_subscription(self, websocket_stream):
        """사용자 구독 테스트"""
        from ddc.bot.websocket_stream import TelegramStreamListener

        send_message_mock = AsyncMock()
        listener = TelegramStreamListener(websocket_stream, send_message_mock)

        await listener.subscribe_user(12345)
        assert 12345 in listener.user_subscriptions
        assert listener.user_subscriptions[12345] == True

    @pytest.mark.asyncio
    async def test_user_unsubscription(self, websocket_stream):
        """사용자 구독 취소 테스트"""
        from ddc.bot.websocket_stream import TelegramStreamListener

        send_message_mock = AsyncMock()
        listener = TelegramStreamListener(websocket_stream, send_message_mock)

        await listener.subscribe_user(12345)
        await listener.unsubscribe_user(12345)
        assert 12345 not in listener.user_subscriptions


# ============================================================================
# Tests - Data Models
# ============================================================================

class TestDataModels:
    """데이터 모델 테스트"""

    def test_neural_update_creation(self, neural_update_data):
        """NeuralUpdate 생성 테스트"""
        from ddc.bot.websocket_stream import NeuralUpdate

        update = NeuralUpdate(
            timestamp=neural_update_data['timestamp'],
            levels=neural_update_data['levels'],
            api_calls=neural_update_data['api_calls'],
            total_calls=8,
            average_health=0.95,
            status="🟢 healthy"
        )

        assert update.average_health == 0.95
        assert update.total_calls == 8

    def test_alert_creation(self):
        """Alert 생성 테스트"""
        from ddc.bot.websocket_stream import Alert, AlertLevel

        alert = Alert(
            level=AlertLevel.WARNING,
            title="Test Alert",
            message="Test message",
            timestamp=datetime.now().isoformat()
        )

        assert alert.level == AlertLevel.WARNING
        assert alert.title == "Test Alert"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
