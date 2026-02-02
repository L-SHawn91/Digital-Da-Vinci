
"""
🤖 SHawn-Brain Telegram Bot Interface (D-CNS v5.5)
The Digital Central Nervous System Interface - API Client Mode
"""

import os
import sys
import logging
import asyncio
import httpx
from typing import Optional

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- API Configuration ---
# FastAPI 서버 주소 (start_bot.sh에서 실행된 서버)
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 60.0

class TelegramBot:
    """SHawn-Brain D-CNS Telegram Interface (Client)"""

    def __init__(self, token: str):
        self.token = token
        self.app = Application.builder().token(token).build()
        self._register_handlers()
        
        logger.info(f"🤖 Bot Client Initialized (Targeting {API_BASE_URL})")

    def _register_handlers(self):
        """Register Handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("restart", self.cmd_restart))
        
        # Messages (Natural Language)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Errors
        self.app.add_error_handler(self.error_handler)

    # --- Interaction Logic ---

    async def get_brain_response(self, user_id: int, text: str) -> str:
        """Call D-CNS API Server"""
        try:
            async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
                response = await client.post(
                    f"{API_BASE_URL}/v1/chat",
                    json={"user_id": user_id, "text": text}
                )
                response.raise_for_status()
                data = response.json()
                
                # 메타데이터 (Provider, Latency) 활용 가능
                return f"{data['response']}\n\n_⚡ {data['provider']} / {data['latency_ms']}ms_"

        except httpx.ConnectError:
            return "⚠️ **Neural Server Offline**\n뇌(Brain) 서버 연결 실패. `start_bot.sh`를 실행해주세요."
        except httpx.TimeoutException:
            return "⚠️ **Neural Timeout**\n생각이 너무 길어지고 있습니다. 잠시 후 다시 시도해주세요."
        except Exception as e:
            logger.error(f"API Error: {e}")
            return f"⚠️ **Transmission Error**: {str(e)}"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive User Message -> Call API -> Reply"""
        user_id = update.effective_user.id
        user_text = update.message.text
        
        # 1. Thought Notification (UI)
        thought_msg = await update.message.reply_text(
            "🧬 **Synapse Firing...**", 
            parse_mode="Markdown"
        )
        
        # 2. Get Response from Brain Server
        response_text = await self.get_brain_response(user_id, user_text)
        
        # 3. Update Message
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=thought_msg.message_id,
                text=response_text,
                parse_mode="Markdown"
            )
        except Exception:
            # Markdown 파싱 에러 시 Plain Text로 재시도
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=thought_msg.message_id,
                text=response_text,
                parse_mode=None
            )

    # --- Commands ---

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🧬 **SHawn-Brain D-CNS v5.5 Online**\n"
            "Fast-API Neural Interface Connected.\n\n"
            "무엇을 도와드릴까요?",
            parse_mode="Markdown"
        )

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📚 **Manual**\n"
            "- 자연어로 대화하세요.\n"
            "- /status : 시스템 및 뇌 건강도 확인\n"
            "- /restart : 봇 재시작",
            parse_mode="Markdown"
        )

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check Server Health via API"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{API_BASE_URL}/health")
                data = resp.json()
                status = "🟢 Online" if resp.status_code == 200 else "🔴 Error"
                
            await update.message.reply_text(
                f"**System Status**: {status}\n"
                f"• Brain: `{data.get('brain')}`\n"
                f"• Version: `{data.get('version')}`",
                parse_mode="Markdown"
            )
        except Exception:
            await update.message.reply_text("⚠️ **Brain Server Offline**")

    async def cmd_restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔄 Restarting Bot Interface...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        logger.info("🚀 Starting Telegram Polling...")
        self.app.run_polling()

if __name__ == "__main__":
    # Token 우선순위: Argument > Env Var > Hardcoded (Dev)
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8208574497:AAFngIP-8iJCsPvVj2rdU7dHmZF7WY5Tq1o"
    
    if not TOKEN:
        logger.critical("❌ Telegram Token missing!")
        sys.exit(1)
        
    try:
        bot = TelegramBot(TOKEN)
        bot.run()
    except Exception as e:
        logger.critical(f"🔥 Fatal Error: {e}")
