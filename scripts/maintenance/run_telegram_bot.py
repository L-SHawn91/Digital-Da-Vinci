#!/usr/bin/env python3
"""
🤖 SHawn-Brain Telegram Bot Launcher
텔레그램 봇을 실행합니다.

사용법:
    python run_telegram_bot.py

필수 설정:
    1. .env 파일에 TELEGRAM_BOT_TOKEN 설정
    2. FastAPI 백엔드 실행 중 (localhost:8000)
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "projects"))
sys.path.insert(0, str(project_root))

from ddc.bot.telegram.interface import TelegramBot


async def main():
    """메인 함수"""
    from dotenv import load_dotenv

    # .env 파일 로드
    load_dotenv()

    # Telegram Bot Token 확인
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        print("❌ TELEGRAM_BOT_TOKEN이 설정되어 있지 않습니다.")
        print("\n설정 방법:")
        print("1. .env 파일 생성 (또는 .env.example 복사):")
        print("   cp .env.example .env")
        print("\n2. TELEGRAM_BOT_TOKEN 값 설정:")
        print("   TELEGRAM_BOT_TOKEN=your_actual_token")
        print("\n3. Token 얻는 방법:")
        print("   - Telegram에서 @BotFather와 대화 시작")
        print("   - /newbot 명령어 실행")
        print("   - 봇 이름 설정")
        print("   - 받은 Token을 .env에 저장")
        return

    print("🚀 SHawn-Brain Telegram Bot 시작")
    print(f"📝 Token: {token[:10]}...{token[-10:]}")
    print("🔗 API Server: http://localhost:8000")
    print("\n⏳ 봇 초기화 중...")

    # 봇 생성
    bot = TelegramBot(token=token)

    # 봇 시작
    try:
        print("✅ 봇이 실행 중입니다...")
        print("🛑 중지하려면 Ctrl+C를 누르세요")
        print("\n📱 Telegram에서 @YourBotName을 찾아 /start를 입력하세요\n")

        await bot.run_async()
    except KeyboardInterrupt:
        print("\n\n✅ 봇이 정지되었습니다")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ 종료됨")
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)
