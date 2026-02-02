#!/usr/bin/env python3
"""
토큰절약형 디렉토리/파일 목록 요약 스크립트

목표:
- "현재 디렉토리 목록과 존재하는 파일리스트"를 자동으로 정리
- 출력이 너무 길어지지 않도록(= 토큰 절약) 깊이/개수 제한 + 요약 중심으로 출력

주요 특징:
- 디렉토리 트리(깊이 제한, 디렉토리당 출력 개수 제한, 전체 출력 개수 제한)
- 총 파일/디렉토리 개수, 총 바이트(파일만) 요약
- 상위 N개 대용량 파일(top N) 목록
- 기본 무시 폴더(.git, venv, node_modules 등) 제공

사용 예:
  python automation_scripts/summarize_tree.py
  python automation_scripts/summarize_tree.py --path /workspace --max-depth 6 --format md
  python automation_scripts/summarize_tree.py --path . --output structure.md --format md
  python automation_scripts/summarize_tree.py --no-default-ignore --include-hidden
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from datetime import datetime
from typing import Iterable, List, Optional, Tuple


DEFAULT_IGNORE_DIRNAMES = {
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
    ".venv",
    "venv",
    "env",
    "ENV",
    "node_modules",
    "dist",
    "build",
    ".Rproj.user",
}


@dataclasses.dataclass(frozen=True)
class WalkLimits:
    max_depth: int
    max_entries_per_dir: int
    max_total_entries: int
    include_hidden: bool
    ignore_dirnames: Tuple[str, ...]


@dataclasses.dataclass
class WalkStats:
    dirs_seen: int = 0
    files_seen: int = 0
    bytes_seen: int = 0
    entries_printed: int = 0
    truncated: bool = False
    trunc_reason: Optional[str] = None


def _is_hidden(name: str) -> bool:
    return name.startswith(".")


def _human_bytes(n: int) -> str:
    # token 절약을 위해 단순/짧게 표시
    units = ["B", "KB", "MB", "GB", "TB"]
    f = float(n)
    for u in units:
        if f < 1024.0 or u == units[-1]:
            if u == "B":
                return f"{int(f)}{u}"
            return f"{f:.1f}{u}"
        f /= 1024.0
    return f"{int(n)}B"


def _safe_stat(path: str) -> Optional[os.stat_result]:
    try:
        return os.stat(path, follow_symlinks=False)
    except OSError:
        return None


def _should_skip_dir(name: str, limits: WalkLimits) -> bool:
    if not limits.include_hidden and _is_hidden(name):
        return True
    return name in set(limits.ignore_dirnames)


def walk_tree_lines(
    root: str,
    limits: WalkLimits,
    stats: WalkStats,
    top_files: List[Tuple[int, str]],
) -> Iterable[str]:
    """
    root 아래를 DFS로 순회하며, 토큰 절약형 트리 라인 생성.
    - stats.entries_printed가 max_total_entries를 넘으면 중단(truncated).
    """

    root = os.path.abspath(root)

    def emit(line: str) -> Iterable[str]:
        if stats.entries_printed >= limits.max_total_entries:
            stats.truncated = True
            stats.trunc_reason = f"전체 출력 엔트리 수 제한({limits.max_total_entries}) 도달"
            return []
        stats.entries_printed += 1
        return [line]

    def dfs(dir_path: str, depth: int, prefix: str) -> Iterable[str]:
        if stats.truncated:
            return []
        if depth > limits.max_depth:
            return []

        try:
            with os.scandir(dir_path) as it:
                entries = list(it)
        except OSError:
            return list(emit(f"{prefix}└─ [접근불가] {os.path.basename(dir_path) or dir_path}"))

        # directories first, then files; stable name sort (짧게/예측가능하게)
        dirs = []
        files = []
        for e in entries:
            name = e.name
            if e.is_dir(follow_symlinks=False):
                dirs.append(e)
            else:
                files.append(e)

        dirs.sort(key=lambda x: x.name.lower())
        files.sort(key=lambda x: x.name.lower())

        # per-dir limit 적용
        combined = dirs + files
        shown = combined[: limits.max_entries_per_dir]
        hidden_count = len(combined) - len(shown)

        for idx, e in enumerate(shown):
            if stats.truncated:
                break

            is_last = idx == (len(shown) - 1)
            branch = "└─" if is_last else "├─"
            next_prefix = prefix + ("   " if is_last else "│  ")

            name = e.name
            # hidden skip (files/dirs 모두 적용)
            if not limits.include_hidden and _is_hidden(name):
                continue

            if e.is_dir(follow_symlinks=False):
                if _should_skip_dir(name, limits):
                    # 스킵은 표시만 하고 더 들어가지 않음
                    yield from emit(f"{prefix}{branch} {name}/ (skip)")
                    continue

                stats.dirs_seen += 1
                yield from emit(f"{prefix}{branch} {name}/")
                yield from dfs(os.path.join(dir_path, name), depth + 1, next_prefix)
            else:
                stats.files_seen += 1
                p = os.path.join(dir_path, name)
                st = _safe_stat(p)
                if st is not None:
                    stats.bytes_seen += int(st.st_size)
                    top_files.append((int(st.st_size), p))
                # 파일은 너무 길게 쓰지 않도록 사이즈만 간단히
                size_str = _human_bytes(int(st.st_size)) if st is not None else "?"
                yield from emit(f"{prefix}{branch} {name} ({size_str})")

        if hidden_count > 0 and not stats.truncated:
            # 디렉토리 안 항목이 너무 많으면 "… N more"만 출력
            yield from emit(f"{prefix}└─ … {hidden_count} more (dir limit {limits.max_entries_per_dir})")

    # root 출력
    stats.dirs_seen += 1
    for line in emit(f"{os.path.basename(root) or root}/"):
        yield line
    yield from dfs(root, depth=1, prefix="")


def build_report(
    root: str,
    limits: WalkLimits,
    top_n: int,
) -> dict:
    stats = WalkStats()
    top_files: List[Tuple[int, str]] = []
    lines = list(walk_tree_lines(root=root, limits=limits, stats=stats, top_files=top_files))

    # top N largest files
    top_files.sort(key=lambda x: x[0], reverse=True)
    top_files = top_files[: max(0, top_n)]

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": os.path.abspath(root),
        "limits": dataclasses.asdict(limits),
        "stats": dataclasses.asdict(stats),
        "tree_lines": lines,
        "top_files": [
            {"size_bytes": size, "size_human": _human_bytes(size), "path": path} for size, path in top_files
        ],
    }
    return report


def format_report(report: dict, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(report, ensure_ascii=False, indent=2)

    stats = report["stats"]
    limits = report["limits"]
    top_files = report["top_files"]
    tree_lines = report["tree_lines"]

    if fmt == "plain":
        out = []
        out.append(f"[dir-summary] root={report['root']}")
        out.append(
            f"- dirs={stats['dirs_seen']} files={stats['files_seen']} bytes={stats['bytes_seen']} ({_human_bytes(stats['bytes_seen'])})"
        )
        out.append(
            f"- limits: depth={limits['max_depth']} per_dir={limits['max_entries_per_dir']} total={limits['max_total_entries']} hidden={'Y' if limits['include_hidden'] else 'N'}"
        )
        if stats.get("truncated"):
            out.append(f"- TRUNCATED: {stats.get('trunc_reason')}")
        out.append("")
        out.extend(tree_lines)
        if top_files:
            out.append("")
            out.append("[top-largest-files]")
            for f in top_files:
                out.append(f"- {f['size_human']}\t{f['path']}")
        return "\n".join(out).rstrip() + "\n"

    # default: md
    out = []
    out.append(f"## 디렉토리/파일 요약 (토큰절약형)\n")
    out.append(f"- **root**: `{report['root']}`")
    out.append(
        f"- **count**: dirs={stats['dirs_seen']}, files={stats['files_seen']}, bytes={stats['bytes_seen']} ({_human_bytes(stats['bytes_seen'])})"
    )
    out.append(
        f"- **limits**: depth={limits['max_depth']}, per_dir={limits['max_entries_per_dir']}, total={limits['max_total_entries']}, include_hidden={limits['include_hidden']}"
    )
    if stats.get("truncated"):
        out.append(f"- **TRUNCATED**: {stats.get('trunc_reason')}")

    out.append("\n### 트리(제한 적용)\n")
    out.append("```")
    out.extend(tree_lines)
    out.append("```")

    out.append("\n### 상위 대용량 파일(top)\n")
    if not top_files:
        out.append("- (없음)")
    else:
        out.append("| size | path |")
        out.append("|---:|---|")
        for f in top_files:
            out.append(f"| {f['size_human']} | `{f['path']}` |")

    return "\n".join(out).rstrip() + "\n"


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="토큰절약형 디렉토리/파일 목록 자동 요약",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--path", default=".", help="대상 루트 경로")
    p.add_argument("--max-depth", type=int, default=5, help="트리 출력 최대 깊이")
    p.add_argument("--max-entries-per-dir", type=int, default=60, help="디렉토리당 최대 출력 엔트리 수")
    p.add_argument("--max-total-entries", type=int, default=600, help="전체 트리 최대 출력 라인 수")
    p.add_argument("--top-n", type=int, default=15, help="상위 대용량 파일 표시 개수")
    p.add_argument("--format", choices=["md", "plain", "json"], default="md", help="출력 포맷")
    p.add_argument("--output", default="", help="출력 파일 경로(미지정 시 stdout)")
    p.add_argument("--include-hidden", action="store_true", help="숨김 파일/폴더 포함(기본은 제외)")
    p.add_argument("--ignore", action="append", default=[], help="무시할 디렉토리명 추가(여러 번 지정 가능)")
    p.add_argument("--no-default-ignore", action="store_true", help="기본 무시 폴더 목록 사용 안함")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    ignore_dirnames = [] if args.no_default_ignore else sorted(DEFAULT_IGNORE_DIRNAMES)
    ignore_dirnames.extend(args.ignore or [])

    limits = WalkLimits(
        max_depth=max(0, args.max_depth),
        max_entries_per_dir=max(1, args.max_entries_per_dir),
        max_total_entries=max(20, args.max_total_entries),
        include_hidden=bool(args.include_hidden),
        ignore_dirnames=tuple(ignore_dirnames),
    )

    report = build_report(root=args.path, limits=limits, top_n=max(0, args.top_n))
    rendered = format_report(report, fmt=args.format)

    if args.output:
        out_path = os.path.abspath(args.output)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(out_path)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

