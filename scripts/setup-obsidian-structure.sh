#!/bin/bash

# Obsidian 폴더 구조 자동 생성 및 정리 스크립트

OBSIDIAN_BASE="/Users/soohyunglee/Obsidian/SHawn"

# 필요한 폴더 구조
FOLDERS=(
    "50-Lab/SHawn-Brain-Lab/Projects"
    "50-Lab/SHawn-Brain-Lab/Reports"
    "50-Lab/SHawn-Brain-Lab/2026-02"
    "10-Projects/SHawn-Brain/Plans"
    "10-Projects/SHawn-Brain/Archive"
    "40-Sources/SHawnMemory"
)

echo "🧠 Obsidian SHawn-Brain 폴더 구조 정리 시작..."
echo "Base: $OBSIDIAN_BASE"
echo ""

# 각 폴더 생성
for folder in "${FOLDERS[@]}"; do
    full_path="$OBSIDIAN_BASE/$folder"
    
    if [ -d "$full_path" ]; then
        echo "✅ 이미 존재: $folder"
    else
        mkdir -p "$full_path"
        echo "📁 생성됨: $folder"
    fi
done

echo ""
echo "📝 README 파일 생성..."

# README 파일 생성
create_readme() {
    local path=$1
    local title=$2
    local description=$3
    local readme_file="$OBSIDIAN_BASE/$path/README.md"
    
    if [ ! -f "$readme_file" ]; then
        cat > "$readme_file" << EOF
# $title

## 설명
$description

## 폴더 구조
- 파일명 형식: YYMMDD-PROJECT-NAME.md
- 예시: 260201-Stage4-Step1-Log.md

## 최신 업데이트
$(date '+%Y-%m-%d %H:%M:%S')

---
**관리자**: MoltBot
EOF
        echo "✅ 생성: $path/README.md"
    fi
}

# 각 폴더별 README
create_readme "50-Lab/SHawn-Brain-Lab/Projects" \
    "SHawn-Brain Projects" \
    "프로젝트/Stage별 일지 (PROJECT-LOG) 저장소. 작업 진행 중 기록되는 모든 내용을 시간대별로 정리합니다."

create_readme "50-Lab/SHawn-Brain-Lab/Reports" \
    "SHawn-Brain Reports" \
    "프로젝트/Stage 완료 후 작성되는 결과 리포트 (COMPLETION-REPORT) 저장소. 목표 vs 성과, 통계, 배운점을 포함합니다."

create_readme "10-Projects/SHawn-Brain/Plans" \
    "SHawn-Brain Plans" \
    "다음 단계의 상세 계획서 (STEP-PLAN) 저장소. 목표, 일정, 예상 비용, 성공 기준을 포함합니다."

create_readme "40-Sources/SHawnMemory" \
    "SHawn-Brain Memory" \
    "핵심 메모리 및 결정 기록. MEMORY.md의 백업 및 장기 보관용."

echo ""
echo "📊 폴더 구조 확인..."
tree "$OBSIDIAN_BASE" -L 3 -I 'node_modules' 2>/dev/null || \
    find "$OBSIDIAN_BASE" -maxdepth 3 -type d | sort

echo ""
echo "🎉 폴더 정리 완료!"
echo ""
echo "📋 생성된 폴더 요약:"
echo "├── 50-Lab/SHawn-Brain-Lab/"
echo "│   ├── Projects/ (프로젝트 일지)"
echo "│   ├── Reports/ (결과 리포트)"
echo "│   ├── 2026-02/ (월별 일지)"
echo "│   └── README.md"
echo "├── 10-Projects/SHawn-Brain/"
echo "│   ├── Plans/ (계획서)"
echo "│   ├── Archive/ (과거 파일)"
echo "│   └── README.md"
echo "└── 40-Sources/SHawnMemory/"
echo "    └── README.md"
echo ""
echo "✨ 다음 단계:"
echo "1. 260201-STAGE4-STEP123-PROJECT-LOG.md → Projects/"
echo "2. 260201-STAGE234-COMPLETION-REPORT.md → Reports/"
echo "3. 260202-STAGE4-STEP4-PLAN.md → Plans/"
