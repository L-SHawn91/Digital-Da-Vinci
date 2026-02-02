#!/usr/bin/env python3
import subprocess
import datetime
import sys
import os

# 색상 코드 (터미널 출력용)
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_status(message, color=RESET):
    print(f"{color}[Git Sync] {message}{RESET}")

def run_command(command):
    try:
        # 명령어를 실행하고 출력을 캡처하지 않고 바로 보여줍니다 (실시간 진행상황 확인)
        result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Error executing: {command}", RED)
        return False

def check_git_repo():
    return os.path.exists(".git")

def main():
    # 1. Git 저장소 확인
    if not check_git_repo():
        print_status("현재 디렉토리는 Git 저장소가 아닙니다 (.git 폴더 없음).", RED)
        sys.exit(1)

    print_status("Git 동기화를 시작합니다...", YELLOW)
    print_status(f"대상 경로: {os.getcwd()}")

    # 2. Pull (원격 변경사항 가져오기)
    print_status("1. Pulling changes...", GREEN)
    if not run_command("git pull"):
        print_status("Pull 실패. 충돌을 확인하세요.", RED)
        sys.exit(1)

    # 3. Add (모든 변경사항 스테이징)
    print_status("2. Adding changes...", GREEN)
    run_command("git add .")

    # 4. Commit 확인
    # 변경사항이 있는지 확인
    status_output = subprocess.getoutput("git status --porcelain")
    if not status_output:
        print_status("변경사항이 없습니다. 동기화를 종료합니다.", GREEN)
        sys.exit(0)

    # 5. Commit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Auto-sync: {timestamp}"
    print_status(f"3. Committing with message: '{commit_message}'", GREEN)
    if not run_command(f'git commit -m "{commit_message}"'):
        sys.exit(1)

    # 6. Push
    print_status("4. Pushing to remote...", GREEN)
    if run_command("git push"):
        print_status("동기화가 성공적으로 완료되었습니다! 🎉", GREEN)
    else:
        print_status("Push 실패. 네트워크나 권한을 확인하세요.", RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
