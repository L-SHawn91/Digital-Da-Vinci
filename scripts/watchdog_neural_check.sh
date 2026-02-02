#!/bin/bash

# watchdog_neural_check.sh
# Week 진행 시마다 신경계별 모델 효율을 체크하는 자동 스크립트

set -e

cd /Users/soohyunglee/.openclaw/workspace

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║  🧠 Watchdog 신경계 효율 체크 - 매번 실행                                  ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 1. 현재 진행 상황 확인
echo "📋 현재 상태:"
echo "  └─ Git 상태 확인중..."
git status --short | head -5
echo ""

# 2. 신경계 모델 로테이션 테스트 실행
echo "🔄 신경계별 모델 로테이션 테스트 실행 (3개 신경계 × 3개 모델)..."
python3 systems/neural/watchdog_weekly_neural_model_rotation.py 2>&1 | tail -40

# 3. 리포트 파일 경로
REPORT_FILE="logs/neural_efficiency/weekly_rotation/week1_watchdog_neural_rotation.json"

# 4. 리포트 요약 출력
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║  📊 Week 1 신경계 모델 선택 결과                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

if [ -f "$REPORT_FILE" ]; then
    cat "$REPORT_FILE" | jq '.best_models_by_level | to_entries[] | {
        "신경계": .key,
        "이름": (.value | "\(.model_name) ⭐ \(.overall_score)/10"),
        "테스트": (.value.test_count | "3회 테스트"),
        "평균": (.value.avg_score | "평균 \(.)/10")
    }' | jq -r '.[] | "\(.신경계)\n  → \(.이름)\n  → \(.테스트) / \(.평균)\n"'
fi

echo ""
echo "✅ 신경계 효율 체크 완료!"
echo "📁 상세 리포트: $REPORT_FILE"
echo ""
