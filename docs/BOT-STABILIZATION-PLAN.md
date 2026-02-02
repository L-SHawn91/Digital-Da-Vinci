# 260205-BOT-STABILIZATION-PLAN.md - 봇 안정화 계획

**날짜**: 2026-02-05  
**목표**: SHawn-Bot Telegram 안정화  
**상태**: 진단 완료, 실행 준비  

---

## 🔍 **현재 상황 진단**

### **문제점**

1. **의존성 부족** ⚠️
   - `python-telegram-bot` 모듈 미설치
   - 현재 봇 프로세스 (PID 54157)는 실행 중이지만 정상 작동 안 함
   - Python 3.9 사용 (다른 환경)

2. **프로세스 상태**
   - 실행 중: `run_telegram_bot.py` (PID 54157)
   - 실행 시간: 8시간 1분 (오랫동안 실행 중)
   - 메모리: 0.1% (정상)
   - 하지만 실제 메시지 처리는 안 됨

3. **구조적 문제**
   - 두 가지 봇 파일: `shawn_bot.py` & `shawn_bot_telegram.py`
   - 실행 스크립트: `scripts/maintenance/run_telegram_bot.py`
   - 재시작 스크립트: `SHawn_Brain/bot_autorestart.sh` & `restart_bot.sh`

---

## 🔧 **안정화 전략 (우선순위 순)**

### **1️⃣ 즉시 대응 (30분)**

#### **Step 1: 봇 프로세스 확인 & 재시작**

```bash
# 현재 봇 프로세스 중단
kill 54157

# 환경 확인
python3 --version
pip3 list | grep telegram

# 의존성 설치
pip3 install python-telegram-bot --upgrade

# 봇 재시작
cd /Users/soohyunglee/.openclaw/workspace
python3 scripts/maintenance/run_telegram_bot.py &
```

#### **Step 2: 봇 로깅 설정**

```bash
# 로그 디렉토리 생성
mkdir -p logs/
touch logs/bot.log

# 봇 실행 (로그 기록)
python3 scripts/maintenance/run_telegram_bot.py > logs/bot.log 2>&1 &
```

### **2️⃣ 안정성 강화 (1시간)**

#### **파일 1: 통합 봇 실행 스크립트**

**파일**: `scripts/maintenance/start_bot_stable.sh`

```bash
#!/bin/bash

# SHawn-Bot 안정적 시작 스크립트

set -e  # 에러 시 중단

BOT_DIR="/Users/soohyunglee/.openclaw/workspace"
LOG_DIR="$BOT_DIR/logs"
BOT_PID_FILE="$BOT_DIR/.bot.pid"

# 로그 디렉토리 생성
mkdir -p "$LOG_DIR"

# 기존 프로세스 확인 & 중단
if [ -f "$BOT_PID_FILE" ]; then
    OLD_PID=$(cat "$BOT_PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "기존 봇 프로세스 중단 (PID: $OLD_PID)"
        kill "$OLD_PID" 2>/dev/null || true
        sleep 2
    fi
fi

# 의존성 확인 & 설치
echo "의존성 확인..."
python3 -c "import telegram" 2>/dev/null || {
    echo "telegram 라이브러리 설치 중..."
    pip3 install python-telegram-bot --upgrade
}

# 봇 환경 변수 확인
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️ TELEGRAM_BOT_TOKEN 환경 변수 설정 필요"
    echo "export TELEGRAM_BOT_TOKEN=your_token"
    exit 1
fi

# 봇 시작
echo "SHawn-Bot 시작..."
cd "$BOT_DIR"
python3 scripts/maintenance/run_telegram_bot.py >> "$LOG_DIR/bot.log" 2>&1 &
NEW_PID=$!

# PID 저장
echo $NEW_PID > "$BOT_PID_FILE"

echo "✅ 봇 시작 완료 (PID: $NEW_PID)"
echo "📝 로그: $LOG_DIR/bot.log"

sleep 2

# 프로세스 확인
if ps -p "$NEW_PID" > /dev/null; then
    echo "✅ 봇 정상 실행 중"
else
    echo "❌ 봇 실행 실패"
    echo "로그 확인:"
    tail -20 "$LOG_DIR/bot.log"
    exit 1
fi
```

#### **파일 2: 봇 모니터 스크립트**

**파일**: `scripts/maintenance/monitor_bot.sh`

```bash
#!/bin/bash

# SHawn-Bot 모니터링 스크립트

BOT_DIR="/Users/soohyunglee/.openclaw/workspace"
BOT_PID_FILE="$BOT_DIR/.bot.pid"
LOG_DIR="$BOT_DIR/logs"

echo "=== SHawn-Bot 상태 확인 ==="

if [ ! -f "$BOT_PID_FILE" ]; then
    echo "❌ 봇이 실행 중이 아님"
    exit 1
fi

PID=$(cat "$BOT_PID_FILE")

if ! ps -p "$PID" > /dev/null; then
    echo "❌ 봇 프로세스 (PID: $PID) 종료됨"
    echo "재시작 중..."
    bash "$BOT_DIR/scripts/maintenance/start_bot_stable.sh"
    exit $?
fi

echo "✅ 봇 정상 실행 중 (PID: $PID)"

# 상세 정보
echo ""
echo "=== 프로세스 정보 ==="
ps -p "$PID" -o pid,ppid,etime,rss,%mem

echo ""
echo "=== 최근 로그 ==="
tail -10 "$LOG_DIR/bot.log"
```

#### **파일 3: 봇 상태 체크 Python**

**파일**: `scripts/maintenance/check_bot_health.py`

```python
#!/usr/bin/env python3
"""
SHawn-Bot 헬스 체크

- 봇 프로세스 확인
- Telegram 연결 테스트
- 카트리지 연동 확인
- 이슈 레포팅
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class BotHealthCheck:
    def __init__(self):
        self.bot_dir = Path(__file__).parent.parent.parent
        self.pid_file = self.bot_dir / ".bot.pid"
        self.log_file = self.bot_dir / "logs" / "bot.log"
        
    def check_process(self):
        """프로세스 확인"""
        if not self.pid_file.exists():
            return False, "PID 파일 없음"
        
        pid = int(self.pid_file.read_text().strip())
        result = subprocess.run(['ps', '-p', str(pid)], 
                              capture_output=True)
        
        if result.returncode == 0:
            return True, f"프로세스 실행 중 (PID: {pid})"
        else:
            return False, f"프로세스 종료됨 (PID: {pid})"
    
    def check_dependencies(self):
        """의존성 확인"""
        try:
            import telegram
            return True, f"telegram {telegram.__version__} 설치됨"
        except ImportError:
            return False, "telegram 라이브러리 미설치"
    
    def check_env(self):
        """환경 변수 확인"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            masked = token[:10] + '*' * (len(token) - 20) + token[-10:]
            return True, f"TELEGRAM_BOT_TOKEN 설정됨 ({masked})"
        else:
            return False, "TELEGRAM_BOT_TOKEN 미설정"
    
    def check_logs(self):
        """로그 확인"""
        if not self.log_file.exists():
            return False, "로그 파일 없음"
        
        # 마지막 100줄 확인
        lines = self.log_file.read_text().split('\n')[-100:]
        errors = [l for l in lines if 'ERROR' in l or 'Exception' in l]
        
        if errors:
            return False, f"에러 발견 ({len(errors)}개): {errors[-1][:100]}"
        else:
            return True, "로그 정상"
    
    def run(self):
        """헬스 체크 실행"""
        checks = [
            ("프로세스", self.check_process()),
            ("의존성", self.check_dependencies()),
            ("환경 변수", self.check_env()),
            ("로그", self.check_logs()),
        ]
        
        print(f"{'='*60}")
        print(f"SHawn-Bot 헬스 체크 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"{'='*60}")
        
        all_ok = True
        for name, (ok, msg) in checks:
            status = "✅" if ok else "❌"
            print(f"{status} {name}: {msg}")
            if not ok:
                all_ok = False
        
        print(f"{'='*60}")
        
        if all_ok:
            print("✅ 봇 정상 상태")
            return 0
        else:
            print("❌ 봇 이상 상태 - 재시작 필요")
            return 1

if __name__ == "__main__":
    checker = BotHealthCheck()
    sys.exit(checker.run())
```

### **3️⃣ 자동 재시작 설정 (30분)**

#### **macOS Launchd 설정**

**파일**: `SHawn_Brain/shawn-bot.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.shawn.bot.telegram</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/soohyunglee/.openclaw/workspace/scripts/maintenance/start_bot_stable.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/soohyunglee/.openclaw/workspace/logs/bot-stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/soohyunglee/.openclaw/workspace/logs/bot-stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

---

## 📋 **실행 순서**

### **Step 1: 즉시 (지금)**

```bash
# 1. 현재 봇 중단
killall -9 run_telegram_bot.py

# 2. 의존성 설치
pip3 install python-telegram-bot --upgrade

# 3. 봇 재시작
cd /Users/soohyunglee/.openclaw/workspace
python3 scripts/maintenance/run_telegram_bot.py &
```

### **Step 2: 안정화 스크립트 생성 (30분)**

- `start_bot_stable.sh` 생성
- `monitor_bot.sh` 생성
- `check_bot_health.py` 생성

### **Step 3: 자동 재시작 설정 (30분)**

- Launchd plist 설정
- 자동 재시작 테스트

### **Step 4: 모니터링 (지속)**

- 정기적 헬스 체크
- 로그 모니터링
- 필요시 자동 재시작

---

## ✅ **검증 체크리스트**

### **봇 기본 기능**
- [ ] 봇 프로세스 실행 확인
- [ ] Telegram 메시지 수신
- [ ] `/start` 명령어 응답
- [ ] 일반 메시지 에코

### **카트리지 연동**
- [ ] Bio-Cartridge 정상 작동
- [ ] Investment-Cartridge 정상 작동
- [ ] 이미지 처리 정상

### **안정성**
- [ ] 오류 시 자동 재시작
- [ ] 메모리 누수 없음
- [ ] 로그 정상 기록

---

## 🚀 **다음 단계**

### **Phase 0 (현재): 봇 안정화**
- 의존성 설치
- 스크립트 생성
- 자동 재시작 설정

### **Phase 1 (완료): 웹 대시보드** ✅
- FastAPI + React 완성
- 17개 API 엔드포인트

### **Phase 2 (예정): REST API 확장**
- 40+ API 엔드포인트
- 인증 & 보안

### **Phase 3 (예정): 배포**
- Docker + K8s
- CI/CD

---

## 💡 **주의사항**

1. **환경 변수**
   - `TELEGRAM_BOT_TOKEN` 반드시 설정
   - 다른 환경 변수는 로드되지 않을 수 있음

2. **Python 버전**
   - 현재: Python 3.9 사용 중
   - 신규: Python 3.11+ 권장

3. **의존성**
   - `python-telegram-bot>=20.0` 설치 필수
   - 정기적 업데이트 확인

---

**준비 완료! 봇 안정화 시작하겠습니다!** 🔧
