#!/bin/bash

# before_development.sh
# 새로운 기능 개발 전에 기존 기능을 자동으로 체크하는 스크립트

set -e

cd /Users/soohyunglee/.openclaw/workspace

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║  🤖 새로운 기능 개발 전 기존 기능 자동 체크                                  ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 사용법 확인
if [ $# -eq 0 ]; then
    echo "📝 사용법:"
    echo "  ./scripts/before_development.sh <키워드> [설명]"
    echo ""
    echo "예시:"
    echo "  ./scripts/before_development.sh 신경계추적 '신경계별 모델 효율 추적'"
    echo "  ./scripts/before_development.sh 'API 트래킹' 'API 사용량 모니터링'"
    echo ""
    echo "모든 기능 보기:"
    echo "  python3 check_existing_features.py"
    echo ""
    exit 0
fi

KEYWORD="$1"
DESCRIPTION="${2:-}"

echo "🔍 검색 중: '$KEYWORD'"
if [ -n "$DESCRIPTION" ]; then
    echo "   설명: $DESCRIPTION"
fi
echo ""

# Python으로 검색 실행
python3 << EOF
import sys
sys.path.insert(0, '/Users/soohyunglee/.openclaw/workspace')

from check_existing_features import FeatureChecker

checker = FeatureChecker()

# 검색 실행
keyword = "$KEYWORD"
description = "$DESCRIPTION"

results = checker.check_feature(keyword, description)

# 결과 요약
if results['found']:
    print("\n" + "="*80)
    print("✅ 결과: 이미 있는 기능이 있습니다!")
    print("="*80)
    print(f"\n찾은 기능: {len(results['found'])}개")
    for item in results['found']:
        print(f"\n📦 {item['name']}")
        print(f"   📂 경로: {item['path']}")
        print(f"   📝 설명: {item['description']}")
        print(f"   🚀 사용: {item['usage']}")
    
    print("\n" + "="*80)
    print("💡 제안: 이 기능을 사용하거나 확장하세요!")
    print("="*80)
    
    sys.exit(0)

elif results['similar']:
    print("\n" + "="*80)
    print("⚠️  결과: 유사한 기능이 있습니다!")
    print("="*80)
    print(f"\n유사 기능: {len(results['similar'])}개")
    for item in results['similar']:
        print(f"\n📦 {item['name']} (일치도: {item['relevance']})")
        print(f"   📂 경로: {item['path']}")
        print(f"   📝 설명: {item['description']}")
    
    print("\n" + "="*80)
    print("💡 제안: 이 기능들을 먼저 확인해보세요!")
    print("="*80)
    
    sys.exit(1)

else:
    print("\n" + "="*80)
    print("✨ 결과: 새로운 기능입니다!")
    print("="*80)
    print("\n이미 있는 기능이 없으므로 새로 만들어도 됩니다.")
    print("하지만 다시 한 번 확인하세요:")
    print("  1. 더 다양한 키워드로 검색")
    print("  2. 유사 기능 문서 읽어보기")
    print("  3. 이미 있는 모든 기능 확인 (python3 check_existing_features.py)")
    
    sys.exit(0)

EOF

