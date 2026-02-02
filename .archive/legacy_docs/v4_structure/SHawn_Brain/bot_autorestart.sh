#!/bin/bash
# Shawn-BOT Auto-Restart Script
# Checks if the bot is running, and if not, restarts it.

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$BOT_DIR/shawnbot.log"
PID_FILE="$BOT_DIR/shawnbot.pid"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Shawn-BOT Auto-Restart Guardian Activated${NC}"

while true; do
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            # Running fine
            sleep 10
        else
            echo -e "${RED}⚠️ PID file exists but process $PID is dead. Restarting...${NC}"
            rm "$PID_FILE"
            
            # Restart
            cd $BOT_DIR
            # Use system python3 if venv not available
            if [ -f "../.venv/bin/activate" ]; then
                source ../.venv/bin/activate
            fi
            nohup python3 main.py >> $LOG_FILE 2>&1 &
            echo $! > $PID_FILE
            echo -e "${GREEN}✅ Bot restarted with PID $(cat $PID_FILE)${NC}"
        fi
    else
        echo -e "${RED}⚠️ Bot is not running. Starting...${NC}"
        # Start
        cd $BOT_DIR
        # Use system python3 if venv not available
        if [ -f "../.venv/bin/activate" ]; then
            source ../.venv/bin/activate
        fi
        nohup python3 main.py >> $LOG_FILE 2>&1 &
        echo $! > $PID_FILE
        echo -e "${GREEN}✅ Bot started with PID $(cat $PID_FILE)${NC}"
    fi
    sleep 5
done
