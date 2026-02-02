#!/bin/bash

# SHawn-Bot 안정적 시작 스크립트
# 봇 프로세스 관리 및 안정성 확보

set -e

BOT_DIR="/Users/soohyunglee/.openclaw/workspace"
LOG_DIR="$BOT_DIR/logs"
BOT_PID_FILE="$BOT_DIR/.bot.pid"

# 컬러 출력
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 로그 디렉토리 생성
mkdir -p "$LOG_DIR"

echo -e "${YELLOW}=== SHawn-Bot 안정화 시작 ===${NC}"

# 1. 기존 프로세스 확인 & 중단
echo -e "${YELLOW}1️⃣ 기존 프로세스 확인...${NC}"
if [ -f "$BOT_PID_FILE" ]; then
    OLD_PID=$(cat "$BOT_PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}   기존 봇 프로세스 중단 (PID: $OLD_PID)${NC}"
        kill "$OLD_PID" 2>/dev/null || true
        sleep 2
    fi
fi

# 대체 방법: 모든 python 관련 bot 프로세스 확인
echo -e "${YELLOW}   실행 중인 봇 프로세스 확인...${NC}"
ps aux | grep -E "(run_telegram_bot|shawn_bot)" | grep -v grep || echo "   실행 중인 프로세스 없음"

# 2. 의존성 확인 & 설치
echo -e "${YELLOW}2️⃣ 의존성 확인...${NC}"

# telegram 확인
if python3 -c "import telegram; print(f'   ✅ telegram {telegram.__version__} 설치됨')" 2>/dev/null; then
    :
else
    echo -e "${RED}   telegram 라이브러리 설치 중...${NC}"
    pip3 install --upgrade python-telegram-bot
    echo -e "${GREEN}   ✅ 설치 완료${NC}"
fi

# 기타 의존성 확인
for pkg in aiohttp PIL requests pandas; do
    if python3 -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}   ✅ $pkg 설치됨${NC}"
    else
        echo -e "${YELLOW}   ⚠️  $pkg 설치 권장${NC}"
    fi
done

# 3. 환경 변수 확인
echo -e "${YELLOW}3️⃣ 환경 변수 확인...${NC}"
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}   ❌ TELEGRAM_BOT_TOKEN 미설정${NC}"
    echo -e "${YELLOW}   설정 방법: export TELEGRAM_BOT_TOKEN=your_token${NC}"
    exit 1
fi
echo -e "${GREEN}   ✅ TELEGRAM_BOT_TOKEN 설정됨${NC}"

# 4. 봇 시작
echo -e "${YELLOW}4️⃣ SHawn-Bot 시작 중...${NC}"
cd "$BOT_DIR"

# 봇 실행
python3 scripts/maintenance/run_telegram_bot.py >> "$LOG_DIR/bot.log" 2>&1 &
NEW_PID=$!

# PID 저장
echo $NEW_PID > "$BOT_PID_FILE"

echo -e "${GREEN}   ✅ 봇 시작 (PID: $NEW_PID)${NC}"
echo -e "${YELLOW}   📝 로그: $LOG_DIR/bot.log${NC}"

# 5. 프로세스 확인
sleep 3
echo -e "${YELLOW}5️⃣ 프로세스 상태 확인...${NC}"

if ps -p "$NEW_PID" > /dev/null; then
    echo -e "${GREEN}✅ 봇 정상 실행 중${NC}"
    ps -p "$NEW_PID" -o pid,etime,%mem,cmd | tail -1
else
    echo -e "${RED}❌ 봇 실행 실패${NC}"
    echo -e "${YELLOW}최근 로그:${NC}"
    tail -30 "$LOG_DIR/bot.log"
    exit 1
fi

echo -e "${GREEN}=== SHawn-Bot 안정화 완료 ===${NC}"
