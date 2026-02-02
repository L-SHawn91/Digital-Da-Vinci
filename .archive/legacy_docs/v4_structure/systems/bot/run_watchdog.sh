#!/bin/bash

# run_watchdog.sh - Watchdog 실행 스크립트
# 사용법: bash run_watchdog.sh

set -e

echo "🧠 숀봇 신경계 L1 뇌간 (아드레날린) - Watchdog 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 현재 디렉토리 확인
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "📁 작업 디렉토리: $SCRIPT_DIR"

# 2. 가상환경 확인
if [ ! -d ".venv_bot" ]; then
    echo "⚠️  가상환경 .venv_bot 없음 - 생성 중..."
    python3 -m venv .venv_bot
fi

# 3. 가상환경 활성화
echo "🐍 가상환경 활성화..."
source .venv_bot/bin/activate

# 4. psutil 설치 확인
echo "📦 필요한 패키지 확인..."
pip install -q psutil

# 5. 로그 디렉토리 생성
mkdir -p logs/watchdog

# 6. Watchdog 시작
echo ""
echo "🚀 Watchdog 시작..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$SCRIPT_DIR"
python3 shawn_bot_watchdog.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 Watchdog 종료"
