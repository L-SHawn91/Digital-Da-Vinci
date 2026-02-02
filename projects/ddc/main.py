"""
SHawn-BOT Main Entry Point
Initializes and runs the complete system
"""

import sys
import threading
import uvicorn
import time
from ddc.brain import Brainstem
from ddc.bot import TelegramBot
from ddc.web.backend.main import app as dashboard_app

# 🧠 신경계 시스템 초기화
try:
    from systems.neural.work_tracker import WorkTracker
    neural_tracker = WorkTracker()
    NEURAL_SYSTEM_AVAILABLE = True
except ImportError:
    NEURAL_SYSTEM_AVAILABLE = False
    neural_tracker = None

def run_dashboard():
    """Run dashboard in specific thread"""
    print("📊 Dashboard Server Starting on port 8000...")
    uvicorn.run(dashboard_app, host="0.0.0.0", port=8000, log_level="error")

def main():
    """Main entry point"""
    print("🚀 Digital Da Vinci v0.0.1 (Prototype) 시작 중...")
    
    # 🧠 신경계 시스템 상태
    if NEURAL_SYSTEM_AVAILABLE:
        print("✅ D-CNS 신경계 시스템 활성화")
    else:
        print("⚠️  D-CNS 신경계 시스템 미로드 (systems/neural 확인 필요)")
    
    # 1. Start Dashboard Server (Background)
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a moment for server to warm up
    time.sleep(1)
    print("✅ Dashboard Active at http://localhost:8000")

    print("📊 D-CNS 신경계 초기화...")
    
    # Initialize brain
    brain = Brainstem()
    print("✅ 뇌간 (Brainstem) 활성화")
    
    # Initialize bot
    bot = TelegramBot(brain=brain)
    print("✅ Telegram 봇 활성화")
    
    # Start
    bot.run()

if __name__ == "__main__":
    main()
