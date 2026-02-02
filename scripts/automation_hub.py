#!/usr/bin/env python3
"""
자동화 허브(메뉴):

요구사항 구현:
- 사용자가 "자동화"라고 입력하면(외치면) 등록된 자동화 스크립트들을 번호로 리스트업
- 각 스크립트 설명을 표 형태(시각화)로 보여줌
- 번호 선택 → (선택적 추가 인자 입력) → 실행 → 결과 표시(공용 러너로 보장) + 리포트 저장
- 다음 스크립트를 실행할지 묻거나 종료
- 스크립트는 registry(번호) 기반으로 관리하며, 새 스크립트 추가 시 registry 등록을 강제/경고

비대화형(테스트/자동실행) 모드:
  python3 automation_scripts/automation_hub.py --list
  python3 automation_scripts/automation_hub.py --run 1 -- --path /workspace --max-depth 4
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


REGISTRY_PATH = "automation_scripts/automation_registry.json"
AUTOMATION_DIR = "automation_scripts"


def _abs(p: str) -> str:
    return os.path.abspath(p)


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _load_registry() -> dict:
    path = _abs(REGISTRY_PATH)
    data = json.loads(_read_text(path))
    if "scripts" not in data or not isinstance(data["scripts"], list):
        raise ValueError("registry 형식 오류: scripts 배열이 필요합니다.")
    return data


def _scan_unregistered_py(reg: dict) -> List[str]:
    """automation_scripts/ 내 *.py 중 registry 미등록 파일을 반환(허브/러너 등은 제외 가능)."""
    registered = set()
    for s in reg["scripts"]:
        p = s.get("path", "")
        if isinstance(p, str) and p:
            registered.add(os.path.normpath(p))

    py_files = []
    root = _abs(AUTOMATION_DIR)
    try:
        for name in os.listdir(root):
            if not name.endswith(".py"):
                continue
            if name in {"automation_hub.py"}:
                continue
            py_files.append(os.path.normpath(os.path.join(AUTOMATION_DIR, name)))
    except OSError:
        return []

    return sorted([p for p in py_files if os.path.normpath(p) not in registered])


def _render_table(reg: dict) -> str:
    rows = []
    rows.append("| No | script | type | description |")
    rows.append("|---:|---|---|---|")
    for s in sorted(reg["scripts"], key=lambda x: int(x.get("id", 10**9))):
        if bool(s.get("hidden", False)):
            continue
        sid = s.get("id")
        path = s.get("path", "")
        typ = s.get("type", "")
        desc = s.get("description", "")
        rows.append(f"| {sid} | `{path}` | {typ} | {desc} |")
    return "\n".join(rows)


def _get_script_by_id(reg: dict, sid: int) -> Optional[dict]:
    for s in reg["scripts"]:
        if int(s.get("id", -1)) == sid:
            return s
    return None


def _confirm(prompt: str) -> bool:
    ans = input(prompt).strip().lower()
    return ans in {"y", "yes", "ㅇ", "예", "네", "ok", "ㅇㅇ"}


def _prompt_line(prompt: str, default: str = "") -> str:
    s = input(prompt).strip()
    return s if s else default


def _run_via_runner(script_entry: dict, extra_args: List[str]) -> int:
    """
    공용 러너(run_and_report.py)를 import하여 실행.
    - stdout/stderr/exit code 표시 + report 저장이 항상 수행됨.
    """
    # runner 모듈 import를 위해 automation_scripts를 path에 추가
    sys.path.insert(0, _abs(AUTOMATION_DIR))
    try:
        import run_and_report  # type: ignore
    finally:
        # 중복 추가 방지: 단순 pop 대신 안전하게 제거
        try:
            sys.path.remove(_abs(AUTOMATION_DIR))
        except ValueError:
            pass

    base_cmd = script_entry.get("run")
    if not isinstance(base_cmd, list) or not base_cmd:
        print("[hub] registry 오류: run 커맨드가 없습니다.", file=sys.stderr)
        return 2

    sid = int(script_entry.get("id", 0))
    name = script_entry.get("path", "script").split("/")[-1]
    # 기본 정책: 리포트 파일 저장은 하지 않고(바로 화면 출력), 필요하면 러너를 직접 --save로 실행
    runner_argv = ["--name", f"{sid:02d}_{name}", "--no-save", "--"] + [str(x) for x in base_cmd] + list(extra_args)
    return int(run_and_report.main(runner_argv))


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="자동화 허브(번호 목록/선택 실행/결과 표시/다음 실행 여부 질문)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--list", action="store_true", help="등록된 자동화 스크립트 목록 출력 후 종료")
    p.add_argument("--run", type=int, default=0, help="번호로 스크립트 1회 실행(비대화형). 0이면 대화형")
    p.add_argument("args", nargs=argparse.REMAINDER, help="--run 사용 시 대상 스크립트에 넘길 인자(앞의 --는 허용)")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    reg = _load_registry()

    # registry 미등록 파일 경고(강제성)
    unreg = _scan_unregistered_py(reg)
    if unreg:
        print("[hub] ⚠️ registry 미등록 자동화 스크립트가 있습니다(번호 부여 필요):")
        for p in unreg:
            print(f"  - {p}")
        print(f"[hub] 등록 파일: {REGISTRY_PATH}")

    if args.list:
        print("## 자동화 스크립트 목록(번호)\n")
        print(_render_table(reg))
        return 0

    # 비대화형 1회 실행
    if args.run and args.run > 0:
        sid = int(args.run)
        entry = _get_script_by_id(reg, sid)
        if not entry:
            print(f"[hub] 번호 {sid}는 registry에 없습니다.", file=sys.stderr)
            return 2
        extra = list(args.args)
        if extra and extra[0] == "--":
            extra = extra[1:]
        rc = _run_via_runner(entry, extra_args=extra)
        print("\n## 자동화 스크립트 목록(번호)\n")
        print(_render_table(reg))
        return int(rc)

    # 대화형 모드
    print("자동화 허브입니다.")
    print("아래처럼 입력하면 됩니다:")
    print("- '자동화' : 자동화 스크립트 목록 보기")
    print("- 번호(예: 1) : 해당 스크립트 실행")
    print("- 'q' : 종료")

    last_shown = False
    while True:
        cmd = input("\n> ").strip()
        if cmd in {"q", "quit", "exit"}:
            print("종료합니다.")
            return 0

        if cmd in {"자동화", "list", "ls"}:
            print("\n## 자동화 스크립트 목록(번호)\n")
            print(_render_table(reg))
            last_shown = True
            continue

        # 숫자 선택
        try:
            sid = int(cmd)
        except ValueError:
            print("입력을 이해하지 못했습니다. '자동화' 또는 번호(예: 1) 또는 'q'를 입력하세요.")
            continue

        entry = _get_script_by_id(reg, sid)
        if not entry:
            print(f"번호 {sid}는 목록에 없습니다. '자동화'로 목록을 확인하세요.")
            continue

        # 추가 인자 입력(선택)
        print(f"\n선택: {sid} - {entry.get('name','')}")
        print(f"- script: {entry.get('path','')}")
        ex_args = entry.get("example_args", [])
        if isinstance(ex_args, list) and ex_args:
            print(f"- 예시 인자: {' '.join(map(str, ex_args))}")

        arg_line = _prompt_line("추가 인자 입력(없으면 엔터, 예: --path /workspace --max-depth 4): ", default="")
        extra_args = shlex.split(arg_line) if arg_line else []

        # 실행
        rc = _run_via_runner(entry, extra_args=extra_args)
        print("\n## 자동화 스크립트 목록(번호)\n")
        print(_render_table(reg))

        # 다음 실행 여부 질문
        if not _confirm("\n다음 스크립트를 실행할까요? (y/n): "):
            print("종료합니다.")
            return int(rc)
        # 사용자가 목록을 안 봤으면 다음 라운드에 유도
        if not last_shown:
            print("\n(팁) '자동화'를 입력하면 번호 목록을 다시 볼 수 있어요.")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

