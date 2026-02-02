#!/bin/bash
# 텔레그램 봇 자동 재시작 스크립트
# 봇이 종료되면 자동으로 재시작합니다.

PROJECT_ROOT="/Users/soohyunglee/GitHub/SHawn-Brain"
PYTHON_BIN="/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python"
BOT_SCRIPT="$PROJECT_ROOT/scripts/maintenance/run_telegram_bot.py"
LOG_FILE="/private/tmp/telegram_bot_restart.log"

echo "🤖 텔레그램 봇 자동 재시작 모니터 시작" | tee -a "$LOG_FILE"
echo "📅 $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 기존 텔레그램 봇 프로세스 모두 종료
echo "🔄 기존 프로세스 정리 중..." | tee -a "$LOG_FILE"
pkill -f "run_telegram_bot.py" 2>/dev/null
pkill -f "telegram.*interface" 2>/dev/null
sleep 3

# 무한 루프: 봇이 종료되면 자동 재시작
while true; do
    echo "" | tee -a "$LOG_FILE"
    echo "🚀 텔레그램 봇 시작 ($(date))" | tee -a "$LOG_FILE"
    
    # 봇 실행 (충돌 시 종료 코드 반환)
    cd "$PROJECT_ROOT"
    "$PYTHON_BIN" "$BOT_SCRIPT" 2>&1 | tee -a "$LOG_FILE"
    
    EXIT_CODE=$?
    echo "⚠️  봇이 종료되었습니다 (Exit Code: $EXIT_CODE)" | tee -a "$LOG_FILE"
    
    # 정상 종료(Ctrl+C)인 경우 루프 중단
    if [ $EXIT_CODE -eq 0 ] || [ $EXIT_CODE -eq 130 ]; then
        echo "✅ 정상 종료 감지. 재시작 중단." | tee -a "$LOG_FILE"
        break
    fi
    
    # 5초 대기 후 재시작
    echo "⏳ 5초 후 재시작..." | tee -a "$LOG_FILE"
    sleep 5
done

echo "🛑 자동 재시작 모니터 종료" | tee -a "$LOG_FILE"
