#!/usr/bin/env python3
"""
자동화 스크립트 공용 러너: 실행 후 결과를 항상 보여주기(기본) + 필요 시 저장.

What:
- 어떤 커맨드든 실행하고(stdout/stderr/exit code) 결과를 요약 출력
- 출력이 너무 길면 화면에는 제한만 보여주고(토큰 절약), 필요하면 리포트 파일로 저장

How:
  python3 automation_scripts/run_and_report.py -- python3 automation_scripts/summarize_tree.py --path /workspace

옵션:
  --name NAME         리포트 파일명 prefix (미지정 시 자동)
  --outdir DIR        리포트 저장 디렉토리 (기본: automation_scripts/reports)
  --max-bytes N       화면에 보여줄 최대 바이트(기본 6000). 초과분은 생략
  --timeout SEC       실행 타임아웃(초) (기본 없음)
  --save              리포트 파일 저장(기본은 저장 안 함)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class RunResult:
    cmd: List[str]
    cwd: str
    started_at: str
    duration_sec: float
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _sanitize_name(s: str) -> str:
    s = s.strip() or "run"
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:80]


def _truncate_bytes(text: str, max_bytes: int) -> str:
    b = text.encode("utf-8", errors="replace")
    if len(b) <= max_bytes:
        return text
    cut = b[:max_bytes]
    return cut.decode("utf-8", errors="replace") + f"\n… (truncated, max-bytes={max_bytes})\n"


def run_command(cmd: List[str], timeout_sec: Optional[int]) -> RunResult:
    cwd = os.getcwd()
    started = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    timed_out = False

    try:
        proc = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_sec if timeout_sec and timeout_sec > 0 else None,
        )
        rc = int(proc.returncode)
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as e:
        timed_out = True
        rc = 124
        stdout = (e.stdout or "") if isinstance(e.stdout, str) else ""
        stderr = (e.stderr or "") if isinstance(e.stderr, str) else ""
        stderr = (stderr + "\n" if stderr else "") + f"[runner] TIMEOUT after {timeout_sec}s\n"

    dt = time.time() - t0
    return RunResult(
        cmd=cmd,
        cwd=cwd,
        started_at=started,
        duration_sec=dt,
        returncode=rc,
        stdout=stdout,
        stderr=stderr,
        timed_out=timed_out,
    )


def render_report_text(r: RunResult) -> str:
    lines = []
    lines.append("## automation run report")
    lines.append(f"- started_at: {r.started_at}")
    lines.append(f"- cwd: {r.cwd}")
    lines.append(f"- cmd: {' '.join(r.cmd)}")
    lines.append(f"- returncode: {r.returncode}")
    lines.append(f"- duration_sec: {r.duration_sec:.3f}")
    lines.append(f"- timed_out: {r.timed_out}")
    lines.append("")
    lines.append("### stdout")
    lines.append("```")
    lines.append(r.stdout.rstrip())
    lines.append("```")
    lines.append("")
    lines.append("### stderr")
    lines.append("```")
    lines.append(r.stderr.rstrip())
    lines.append("```")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="자동화 스크립트를 실행하고 결과를 표시/저장하는 공용 러너",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--name", default="", help="리포트 파일명 prefix")
    p.add_argument("--outdir", default="automation_scripts/reports", help="리포트 저장 디렉토리")
    p.add_argument("--max-bytes", type=int, default=6000, help="화면 출력 최대 바이트(stdout/stderr 각각)")
    p.add_argument("--timeout", type=int, default=0, help="실행 타임아웃(초). 0이면 제한 없음")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--save", action="store_true", help="리포트 파일 저장(기본은 저장 안 함)")
    g.add_argument("--no-save", action="store_true", help="(호환) 저장 안 함(기본값)")
    p.add_argument("cmd", nargs=argparse.REMAINDER, help="실행할 커맨드. 예: -- python3 x.py ...")
    args = p.parse_args(argv)

    # allow leading "--"
    if args.cmd and args.cmd[0] == "--":
        args.cmd = args.cmd[1:]
    return args


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    if not args.cmd:
        print("Usage: python3 automation_scripts/run_and_report.py -- <command...>", file=sys.stderr)
        return 2

    name = _sanitize_name(args.name) if args.name else _sanitize_name(os.path.basename(args.cmd[0]))
    stamp = _now_stamp()
    outdir = os.path.abspath(args.outdir)
    report_path = os.path.join(outdir, f"{stamp}__{name}.md")

    r = run_command(args.cmd, timeout_sec=args.timeout if args.timeout > 0 else None)

    # 화면에 결과(토큰절약형)
    print(f"[runner] cmd: {' '.join(args.cmd)}")
    print(f"[runner] rc={r.returncode} duration={r.duration_sec:.3f}s timeout={r.timed_out}")
    # 기본은 저장 안 함(사용자가 --save를 준 경우에만 저장)
    if bool(getattr(args, "save", False)):
        os.makedirs(outdir, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(render_report_text(r))
        print(f"[runner] report: {report_path}")

    if r.stdout:
        print("\n[runner] stdout (possibly truncated)")
        print(_truncate_bytes(r.stdout, max(200, args.max_bytes)).rstrip())
    if r.stderr:
        print("\n[runner] stderr (possibly truncated)", file=sys.stderr)
        print(_truncate_bytes(r.stderr, max(200, args.max_bytes)).rstrip(), file=sys.stderr)

    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

