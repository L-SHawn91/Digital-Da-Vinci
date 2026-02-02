#!/bin/bash
# Shawn-BOT 모니터링 및 관리 스크립트

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"

case "$1" in
    start)
        echo "Shawn-BOT 시작 중..."
        
        # Shawn-BOT PID 파일 확인
        if [ ! -f "$BOT_DIR/shawnbot.pid" ]; then
            cd $BOT_DIR
            # Use system python3 if venv not available
            if [ -f "../.venv/bin/activate" ]; then
                source ../.venv/bin/activate
            fi
            nohup python3 main.py >> $BOT_DIR/shawnbot.log 2>&1 &
            echo $! > $BOT_DIR/shawnbot.pid
            echo "Shawn-BOT 시작됨 (PID: $(cat $BOT_DIR/shawnbot.pid))"
        else
            echo "Shawn-BOT 이미 실행 중 (PID: $(cat $BOT_DIR/shawnbot.pid))"
        fi
        ;;
    stop)
        echo "Shawn-BOT 중지 중..."
        
        # Shawn-BOT 중지
        if [ -f "$BOT_DIR/shawnbot.pid" ]; then
            PID=$(cat $BOT_DIR/shawnbot.pid)
            kill $PID 2>/dev/null
            rm -f $BOT_DIR/shawnbot.pid
            echo "Shawn-BOT 중지됨 (PID: $PID)"
        else
            echo "Shawn-BOT PID 파일 없음"
        fi
        ;;
    restart)
        $0 stop
        sleep 3
        $0 start
        ;;
    status)
        echo "Shawn-BOT 상태 확인:"
        
        if [ -f "$BOT_DIR/shawnbot.pid" ]; then
            PID=$(cat $BOT_DIR/shawnbot.pid)
            if ps -p $PID > /dev/null; then
                echo "✅ Shawn-BOT 실행 중 (PID: $PID)"
            else
                echo "❌ Shawn-BOT PID 파일 존재, 프로세스 없음 (PID: $PID)"
            fi
        else
            echo "🔴 Shawn-BOT 실행 중 아님"
        fi
        ;;
    *)
        echo "사용법: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac