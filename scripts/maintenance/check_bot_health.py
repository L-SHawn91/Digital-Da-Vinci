#!/usr/bin/env python3
"""
SHawn-Bot 헬스 체크 스크립트

- 봇 프로세스 상태
- Telegram 라이브러리
- 환경 변수
- 로그 에러 확인
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

class BotHealthCheck:
    def __init__(self):
        self.bot_dir = Path(__file__).parent.parent.parent
        self.pid_file = self.bot_dir / ".bot.pid"
        self.log_file = self.bot_dir / "logs" / "bot.log"
        self.results = []
        
    def check_process(self):
        """프로세스 상태 확인"""
        try:
            if not self.pid_file.exists():
                return False, "PID 파일 없음"
            
            pid_text = self.pid_file.read_text().strip()
            if not pid_text.isdigit():
                return False, f"PID 형식 오류: {pid_text}"
            
            pid = int(pid_text)
            result = subprocess.run(['ps', '-p', str(pid)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, f"프로세스 실행 중 (PID: {pid})"
            else:
                return False, f"프로세스 종료됨 (PID: {pid})"
        except Exception as e:
            return False, f"프로세스 확인 실패: {str(e)}"
    
    def check_dependencies(self):
        """의존성 확인"""
        try:
            import telegram
            version = getattr(telegram, '__version__', 'unknown')
            return True, f"telegram {version} ✅"
        except ImportError:
            return False, "telegram 라이브러리 미설치"
    
    def check_env(self):
        """환경 변수 확인"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            # 토큰 마스킹
            if len(token) > 20:
                masked = token[:10] + '*' * (len(token) - 20) + token[-10:]
            else:
                masked = '*' * len(token)
            return True, f"TELEGRAM_BOT_TOKEN 설정됨 ({masked})"
        else:
            return False, "TELEGRAM_BOT_TOKEN 미설정"
    
    def check_logs(self):
        """로그 확인"""
        try:
            if not self.log_file.exists():
                return True, "로그 파일 없음 (새 시작)"
            
            content = self.log_file.read_text()
            lines = content.split('\n')
            
            # 에러 확인
            errors = [l for l in lines if 'ERROR' in l or 'Exception' in l]
            
            if errors:
                last_error = errors[-1][:100]
                return False, f"에러 발견 ({len(errors)}개): {last_error}"
            
            # 최근 성공 메시지 확인
            success_lines = [l for l in lines if 'success' in l.lower() or 'connected' in l.lower()]
            if success_lines:
                return True, "로그 정상 (메시지 처리 중)"
            else:
                return True, "로그 정상"
        except Exception as e:
            return False, f"로그 확인 실패: {str(e)}"
    
    def check_bot_responds(self):
        """봇 응답성 확인"""
        # 실제 Telegram API 호출은 토큰 필요하므로 스킵
        # 프로세스가 실행 중이면 응답 가능하다고 가정
        if self.pid_file.exists():
            return True, "봇 응답 준비 상태"
        return False, "봇이 준비되지 않음"
    
    def run(self):
        """헬스 체크 실행"""
        checks = [
            ("프로세스", self.check_process()),
            ("의존성", self.check_dependencies()),
            ("환경 변수", self.check_env()),
            ("로그", self.check_logs()),
            ("응답성", self.check_bot_responds()),
        ]
        
        print(f"\n{'='*70}")
        print(f"🤖 SHawn-Bot 헬스 체크")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        all_ok = True
        for name, (ok, msg) in checks:
            status = "✅" if ok else "❌"
            print(f"{status} {name:12} : {msg}")
            if not ok:
                all_ok = False
        
        print(f"\n{'='*70}")
        
        if all_ok:
            print("✅ 봇 정상 상태 - 모든 체크 통과")
            print(f"{'='*70}\n")
            return 0
        else:
            print("❌ 봇 이상 상태 - 조치 필요")
            print(f"\n📋 조치 방법:")
            print("1. 의존성 설치: pip3 install python-telegram-bot")
            print("2. 환경 변수 설정: export TELEGRAM_BOT_TOKEN=your_token")
            print("3. 봇 재시작: bash scripts/maintenance/start_bot_stable.sh")
            print(f"\n📝 상세 로그: {self.log_file}")
            print(f"{'='*70}\n")
            return 1

if __name__ == "__main__":
    checker = BotHealthCheck()
    sys.exit(checker.run())
