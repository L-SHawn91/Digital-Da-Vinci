"""
Tests - SHawn-Brain Telegram Bot

텔레그램 봇의 모든 기능을 테스트합니다.
- 명령어 핸들러
- 버튼 콜백
- 분석 기능
- 신경계 연동
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def mock_update():
    """Mock Telegram Update"""
    update = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()
    update.message.chat.send_action = AsyncMock()
    update.message.photo = [MagicMock()]
    update.message.text = "test"
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    """Mock Context"""
    return MagicMock()


@pytest.fixture
def telegram_bot():
    """텔레그램 봇 인스턴스"""
    with patch('ddc.bot.telegram_interface.TELEGRAM_AVAILABLE', True):
        from ddc.bot.telegram_interface import TelegramBot
        bot = TelegramBot(token="TEST_TOKEN")
        return bot


# ============================================================================
# Tests - Basic Bot Functions
# ============================================================================

class TestTelegramBotBasic:
    """텔레그램 봇 기본 기능 테스트"""

    def test_bot_initialization(self):
        """봇 초기화 테스트"""
        from ddc.bot.telegram_interface import TelegramBot

        bot = TelegramBot(token="TEST_TOKEN")
        assert bot.token == "TEST_TOKEN"
        assert bot.api_base == "http://localhost:8000"
        assert isinstance(bot.user_sessions, dict)

    def test_bot_with_custom_api(self):
        """커스텀 API URL로 봇 초기화"""
        from ddc.bot.telegram_interface import TelegramBot

        bot = TelegramBot(token="TEST_TOKEN")
        bot.api_base = "http://custom:8000"
        assert bot.api_base == "http://custom:8000"


# ============================================================================
# Tests - Commands
# ============================================================================

@pytest.mark.asyncio
async def test_cmd_start(mock_update, mock_context, telegram_bot):
    """시작 명령어 테스트"""
    await telegram_bot.cmd_start(mock_update, mock_context)

    # reply_text가 호출되었는지 확인
    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args

    # 버튼이 포함되어 있는지 확인
    assert "SHawn-Brain Bot" in call_args[0][0]
    assert call_args[1]["parse_mode"] == "Markdown"


@pytest.mark.asyncio
async def test_cmd_help(mock_update, mock_context, telegram_bot):
    """도움말 명령어 테스트"""
    await telegram_bot.cmd_help(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "도움말" in call_args[0][0] or "Help" in call_args[0][0]


@pytest.mark.asyncio
async def test_cmd_bio(mock_update, mock_context, telegram_bot):
    """Bio 분석 명령어 테스트"""
    await telegram_bot.cmd_bio(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "Bio" in call_args[0][0] or "세포" in call_args[0][0]


@pytest.mark.asyncio
async def test_cmd_inv(mock_update, mock_context, telegram_bot):
    """Inv 분석 명령어 테스트"""
    await telegram_bot.cmd_inv(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "Investment" in call_args[0][0] or "주식" in call_args[0][0]


@pytest.mark.asyncio
async def test_cmd_code(mock_update, mock_context, telegram_bot):
    """자가 코딩 명령어 테스트"""
    await telegram_bot.cmd_code(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "Self-Coding" in call_args[0][0] or "코딩" in call_args[0][0]


# ============================================================================
# Tests - Status Commands
# ============================================================================

@pytest.mark.asyncio
async def test_cmd_status_success(mock_update, mock_context, telegram_bot):
    """시스템 상태 조회 성공 테스트"""
    mock_response = {
        "status": "🟢 healthy",
        "neural_health": {
            "brainstem": 0.95,
            "limbic": 0.93,
            "neocortex": 0.94,
            "neuronet": 0.98,
            "avg": 0.95
        },
        "models_available": ["Gemini", "Claude"],
        "cartridges_active": ["bio", "inv"],
        "version": "5.1.0",
        "uptime": 1000.5
    }

    with patch('ddc.bot.telegram_interface.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        await telegram_bot.cmd_status(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "시스템 상태" in call_args[0][0] or "System Status" in call_args[0][0]


@pytest.mark.asyncio
async def test_cmd_neural_success(mock_update, mock_context, telegram_bot):
    """신경계 상태 조회 성공 테스트"""
    mock_response = {
        "status": "🟢 healthy",
        "average_health": 0.95,
        "neural_levels": {
            "L1_Brainstem": {
                "status": "🟢 active",
                "health": 0.95,
                "function": "기본 기능"
            },
            "L2_Limbic": {
                "status": "🟢 active",
                "health": 0.93,
                "function": "감정/주의"
            },
            "L3_Neocortex": {
                "status": "🟢 active",
                "health": 0.94,
                "function": "학습/분석"
            },
            "L4_NeuroNet": {
                "status": "🟢 active",
                "health": 0.98,
                "function": "신경망"
            }
        }
    }

    with patch('ddc.bot.telegram_interface.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        await telegram_bot.cmd_neural(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "신경계" in call_args[0][0] or "Neural" in call_args[0][0]


# ============================================================================
# Tests - Message Handling
# ============================================================================

@pytest.mark.asyncio
async def test_handle_message_inv_analysis(mock_update, mock_context, telegram_bot):
    """주식 분석 메시지 처리 테스트"""
    from ddc.bot.telegram_interface import ConversationState

    user_id = mock_update.effective_user.id
    telegram_bot.user_sessions[user_id] = {"state": ConversationState.INV_ANALYSIS}
    mock_update.message.text = "TSLA"

    mock_response = {
        "status": "success",
        "ticker": "TSLA",
        "technical_score": 0.85,
        "fundamental_score": 0.78,
        "recommendation": "🟢 BUY",
        "neocortex_decision": {
            "parietal_analysis": 0.88,
            "prefrontal_decision": 0.92
        }
    }

    with patch('ddc.bot.telegram_interface.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        await telegram_bot.handle_message(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "주식" in call_args[0][0] or "Stock" in call_args[0][0]


@pytest.mark.asyncio
async def test_handle_message_self_coding(mock_update, mock_context, telegram_bot):
    """자가 코딩 메시지 처리 테스트"""
    from ddc.bot.telegram_interface import ConversationState

    user_id = mock_update.effective_user.id
    telegram_bot.user_sessions[user_id] = {"state": ConversationState.SELF_CODING}
    mock_update.message.text = "분석"

    await telegram_bot.handle_message(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "분석" in call_args[0][0] or "Analysis" in call_args[0][0]


# ============================================================================
# Tests - Callback Queries (Buttons)
# ============================================================================

@pytest.mark.asyncio
async def test_button_callback_main_menu(mock_update, mock_context, telegram_bot):
    """메인 메뉴 버튼 테스트"""
    mock_update.callback_query.data = "main_menu"

    await telegram_bot.button_callback(mock_update, mock_context)

    mock_update.callback_query.answer.assert_called_once()
    mock_update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_button_callback_cartridge_bio(mock_update, mock_context, telegram_bot):
    """Bio 카트리지 버튼 테스트"""
    mock_update.callback_query.data = "cartridge_bio"

    await telegram_bot.button_callback(mock_update, mock_context)

    mock_update.callback_query.answer.assert_called_once()


# ============================================================================
# Tests - User Session Management
# ============================================================================

class TestUserSessionManagement:
    """사용자 세션 관리 테스트"""

    def test_user_session_creation(self, telegram_bot):
        """사용자 세션 생성 테스트"""
        user_id = 12345
        telegram_bot.user_sessions[user_id] = {"state": "test"}

        assert user_id in telegram_bot.user_sessions
        assert telegram_bot.user_sessions[user_id]["state"] == "test"

    def test_multiple_user_sessions(self, telegram_bot):
        """다중 사용자 세션 테스트"""
        telegram_bot.user_sessions[111] = {"state": "state1"}
        telegram_bot.user_sessions[222] = {"state": "state2"}
        telegram_bot.user_sessions[333] = {"state": "state3"}

        assert len(telegram_bot.user_sessions) == 3
        assert telegram_bot.user_sessions[222]["state"] == "state2"


# ============================================================================
# Tests - Integration with Brain
# ============================================================================

class TestBrainIntegration:
    """신경계 통합 테스트"""

    def test_bot_with_brain(self):
        """봇과 신경계 통합 테스트"""
        mock_brain = MagicMock()
        from ddc.bot.telegram_interface import TelegramBot

        bot = TelegramBot(brain=mock_brain, token="TEST_TOKEN")
        assert bot.brain == mock_brain

    def test_api_endpoint_configuration(self):
        """API 엔드포인트 설정 테스트"""
        from ddc.bot.telegram_interface import TelegramBot

        bot = TelegramBot(token="TEST_TOKEN")
        assert bot.api_base == "http://localhost:8000"


# ============================================================================
# Tests - Error Handling
# ============================================================================

@pytest.mark.asyncio
async def test_handle_api_error(mock_update, mock_context, telegram_bot):
    """API 오류 처리 테스트"""
    with patch('ddc.bot.telegram_interface.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        await telegram_bot.cmd_status(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "연결할 수 없습니다" in call_args[0][0] or "Cannot connect" in call_args[0][0]


@pytest.mark.asyncio
async def test_handle_exception(mock_update, mock_context, telegram_bot):
    """예외 처리 테스트"""
    with patch('ddc.bot.telegram_interface.requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")
        await telegram_bot.cmd_status(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "오류" in call_args[0][0] or "Error" in call_args[0][0]


# ============================================================================
# Tests - Self-Coding Functions
# ============================================================================

@pytest.mark.asyncio
async def test_self_coding_analyze(mock_update, mock_context, telegram_bot):
    """자가 코딩 분석 기능 테스트"""
    await telegram_bot.handle_self_coding(mock_update, mock_context, "분석")

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "분석" in call_args[0][0]


@pytest.mark.asyncio
async def test_self_coding_improve(mock_update, mock_context, telegram_bot):
    """자가 코딩 개선 기능 테스트"""
    await telegram_bot.handle_self_coding(mock_update, mock_context, "개선")

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "개선" in call_args[0][0]


@pytest.mark.asyncio
async def test_self_coding_apply(mock_update, mock_context, telegram_bot):
    """자가 코딩 적용 기능 테스트"""
    await telegram_bot.handle_self_coding(mock_update, mock_context, "적용")

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "적용" in call_args[0][0]


@pytest.mark.asyncio
async def test_self_coding_test(mock_update, mock_context, telegram_bot):
    """자가 코딩 테스트 기능 테스트"""
    await telegram_bot.handle_self_coding(mock_update, mock_context, "테스트")

    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args
    assert "테스트" in call_args[0][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
