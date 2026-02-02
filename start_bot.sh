#!/bin/bash

# SHawn-Brain D-CNS v5.5 Unified Launcher
# Fast-API Server (Brain) + Telegram Bot (Body)

export PYTHONPATH=$(pwd)
PYTHON_EXEC="./venv/bin/python3"

echo "=================================================="
echo "🚀 SHawn-Brain D-CNS System Boot (Phase 5)"
echo "=================================================="

# 1. Cleanup Old Processes
echo "🧹 Cleaning up previous instances..."
pkill -f "uvicorn projects.ddc.api.app:app" 2>/dev/null
pkill -f "projects/ddc/bot/telegram/interface.py" 2>/dev/null
sleep 1

# 2. Start Brain Server (Background)
echo "🧠 [1/2] Starting Brain Server (FastAPI)..."
nohup $PYTHON_EXEC -m uvicorn projects.ddc.api.app:app --host 0.0.0.0 --port 8000 > logs/brain_server.log 2>&1 &
SERVER_PID=$!

echo "⏳ Waiting for Brain to load (Approx. 15s)..."

# 3. Wait for Health Check
MAX_RETRIES=30
COUNT=0
ONLINE=0

while [ $COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health | grep "healthy" > /dev/null; then
        echo "✅ Brain Online!"
        ONLINE=1
        break
    fi
    printf "."
    sleep 2
    COUNT=$((COUNT+1))
done

echo ""

if [ $ONLINE -eq 0 ]; then
    echo "❌ Server Boot Failed. Check logs/brain_server.log"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 4. Start Body (Bot Interface)
echo "🤖 [2/2] Connecting Body (Telegram Bot Client)..."
$PYTHON_EXEC projects/ddc/bot/telegram/interface.py

# 5. Shutdown Sequence (Bot 종료 시 서버도 종료)
echo "💤 Shutting down D-CNS..."
kill $SERVER_PID 2>/dev/null
echo "👋 Bye!"
