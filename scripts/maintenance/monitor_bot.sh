#!/bin/bash

# SHawn-Bot 모니터링 스크립트
# 봇 상태 주기적 확인 및 재시작

BOT_DIR="/Users/soohyunglee/.openclaw/workspace"
BOT_PID_FILE="$BOT_DIR/.bot.pid"
LOG_DIR="$BOT_DIR/logs"

# 컬러
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== SHawn-Bot 모니터링 시작 ===${NC}"
echo -e "${YELLOW}업데이트 간격: 10초 | Ctrl+C로 종료${NC}\n"

check_count=0

while true; do
    check_count=$((check_count + 1))
    
    echo -ne "\r${YELLOW}[확인 #$check_count]${NC} "
    
    # 1. PID 파일 확인
    if [ ! -f "$BOT_PID_FILE" ]; then
        echo -e "${RED}봇 미실행 (PID 파일 없음)${NC}"
        echo "재시작 중..."
        bash "$BOT_DIR/scripts/maintenance/start_bot_stable.sh"
        sleep 3
        continue
    fi
    
    PID=$(cat "$BOT_PID_FILE")
    
    # 2. 프로세스 확인
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${RED}봇 프로세스 종료 (PID: $PID)${NC}"
        echo "재시작 중..."
        bash "$BOT_DIR/scripts/maintenance/start_bot_stable.sh"
        sleep 3
        continue
    fi
    
    # 3. 로그 에러 확인
    if [ -f "$LOG_DIR/bot.log" ]; then
        error_count=$(grep -c "ERROR\|Exception" "$LOG_DIR/bot.log" 2>/dev/null || echo 0)
        if [ "$error_count" -gt 0 ]; then
            echo -e "${YELLOW}봇 실행 중 (PID: $PID, 에러: $error_count)${NC}"
        else
            echo -e "${GREEN}봇 정상 (PID: $PID)${NC}"
        fi
    else
        echo -e "${GREEN}봇 정상 (PID: $PID)${NC}"
    fi
    
    sleep 10
done
