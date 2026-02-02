"""
# check_existing_features.py
# 새로운 기능을 만들기 전에 이미 있는 기능을 자동으로 체크하는 시스템

용도:
  ├─ 새로운 기능 요청 시 자동으로 이미 있는지 검색
  ├─ 유사한 기능들의 위치와 사용법 제시
  ├─ 중복 개발 방지
  └─ 기존 코드 재활용 최대화
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import subprocess


class FeatureChecker:
    """기존 기능 체크 시스템"""
    
    def __init__(self):
        self.workspace = Path("/Users/soohyunglee/.openclaw/workspace")
        self.feature_db = self._build_feature_database()
        self.timestamp = datetime.now().isoformat()
    
    def _build_feature_database(self) -> Dict[str, List[Dict]]:
        """기존 기능 데이터베이스 구축"""
        return {
            "신경계_추적": [
                {
                    "name": "neural_system_efficiency_analysis.py",
                    "path": "projects/ddc/brain/neuronet/neural_system_efficiency_analysis.py",
                    "description": "L1-L4 신경계 레벨별 모델 할당 & 효율성 분석",
                    "features": [
                        "뇌간(L1): Groq 중심 기본 진단",
                        "변연계(L2): Gemini 중심 신경신호 재가중화",
                        "신피질(L3): 4개 엽 협력 통합학습",
                        "신경망(L4): 신경신호 라우팅 & 자동학습"
                    ],
                    "efficiency_scores": {
                        "L1": "9.6/10",
                        "L2": "9.5/10",
                        "L3": "9.4/10",
                        "L4": "9.8/10"
                    },
                    "usage": "python3 projects/ddc/brain/neuronet/neural_system_efficiency_analysis.py"
                }
            ],
            "API_추적": [
                {
                    "name": "api_tracker_unified.py",
                    "path": "projects/ddc/utilities/api_tracker_unified.py",
                    "description": "통합 API 추적 시스템 (10개 모델)",
                    "features": [
                        "API별 사용량 추적",
                        "응답시간 모니터링",
                        "비용 계산",
                        "효율성 점수"
                    ],
                    "usage": "python3 projects/ddc/utilities/api_tracker_unified.py"
                },
                {
                    "name": "groq_usage_tracker.py",
                    "path": "projects/ddc/utilities/groq_usage_tracker.py",
                    "description": "Groq 특화 사용량 추적",
                    "features": ["Groq 응답시간", "토큰 추적", "비용"],
                    "usage": "python3 projects/ddc/utilities/groq_usage_tracker.py"
                },
                {
                    "name": "model_usage_tracker.py",
                    "path": "projects/ddc/utilities/model_usage_tracker.py",
                    "description": "모델별 사용량 추적",
                    "features": ["모델별 통계", "성능 메트릭", "최고 모델"],
                    "usage": "python3 projects/ddc/utilities/model_usage_tracker.py"
                }
            ],
            "강화학습": [
                {
                    "name": "shawn_bot_watchdog_v2.py",
                    "path": "systems/bot/shawn_bot_watchdog_v2.py",
                    "description": "Watchdog Q-Learning 신경학습 시스템",
                    "features": [
                        "ProcessState: 상태 감지",
                        "NeuralLearner: Q-Learning 구현",
                        "RewardCalculator: 보상 계산",
                        "QualityScorer: 효율 점수"
                    ],
                    "efficiency_scores": {
                        "복구율": "60%",
                        "효율": "9/10",
                        "안정성": "3/10"
                    },
                    "usage": "python3 systems/bot/shawn_bot_watchdog_v2.py"
                }
            ],
            "신경라우팅": [
                {
                    "name": "neural_router.py",
                    "path": "systems/neural/neural_router.py",
                    "description": "작업을 최적 모델로 라우팅",
                    "features": [
                        "NeuralModelRouter: 신경 라우팅",
                        "신경계 기반 모델 선택",
                        "동적 가중치 조정"
                    ],
                    "usage": "from systems.neural.neural_router import NeuralModelRouter"
                },
                {
                    "name": "work_tracker.py",
                    "path": "systems/neural/work_tracker.py",
                    "description": "작업 효율 추적",
                    "features": [
                        "WorkTracker: 작업 기록",
                        "효율 메트릭 계산",
                        "일일 리포트 생성"
                    ],
                    "usage": "from systems.neural.work_tracker import WorkTracker"
                }
            ],
            "신경계_시스템": [
                {
                    "name": "adaptive_neural_system.py",
                    "path": "systems/neural/adaptive_neural_system.py",
                    "description": "적응형 신경계 시스템",
                    "features": [
                        "신경계별 모델 자동 선택",
                        "성능 기반 적응",
                        "실시간 최적화"
                    ],
                    "usage": "from systems.neural.adaptive_neural_system import AdaptiveNeuralSystem"
                },
                {
                    "name": "neural_executor.py",
                    "path": "systems/neural/neural_executor.py",
                    "description": "신경계 기반 작업 실행",
                    "features": [
                        "작업 → 모델 선택 → 실행 → 평가",
                        "신경계별 최적화",
                        "피드백 학습"
                    ],
                    "usage": "from systems.neural.neural_executor import NeuralExecutor"
                }
            ]
        }
    
    def check_feature(self, keyword: str, description: str = "") -> Dict:
        """기능 검색"""
        
        print("\n" + "="*100)
        print(f"🔍 기존 기능 검색: '{keyword}'")
        if description:
            print(f"   설명: {description}")
        print("="*100 + "\n")
        
        results = {
            "keyword": keyword,
            "description": description,
            "timestamp": self.timestamp,
            "found": [],
            "similar": []
        }
        
        # 1. 정확한 키워드 매칭
        for category, features in self.feature_db.items():
            for feature in features:
                if keyword.lower() in feature["name"].lower() or \
                   keyword.lower() in feature["description"].lower():
                    results["found"].append({
                        "category": category,
                        **feature
                    })
        
        # 2. 유사 기능 찾기
        if not results["found"]:
            keywords = keyword.lower().split()
            for category, features in self.feature_db.items():
                for feature in features:
                    match_count = sum(
                        1 for kw in keywords
                        if kw in feature["description"].lower() or
                           kw in feature["name"].lower()
                    )
                    if match_count > 0:
                        results["similar"].append({
                            "category": category,
                            "relevance": f"{(match_count / len(keywords) * 100):.0f}%",
                            **feature
                        })
        
        # 결과 출력
        if results["found"]:
            print("✅ 이미 있는 기능을 찾았습니다!\n")
            
            for idx, item in enumerate(results["found"], 1):
                self._print_feature_details(idx, item)
        
        if results["similar"]:
            print("\n💡 유사한 기능들:\n")
            
            for idx, item in enumerate(results["similar"], 1):
                print(f"{idx}. 📦 {item['category']} > {item['name']}")
                print(f"   설명: {item['description']}")
                print(f"   일치도: {item['relevance']}")
                print()
        
        if not results["found"] and not results["similar"]:
            print("❌ 찾을 수 없습니다. 새로 만들어야 할 것 같습니다.\n")
        
        return results
    
    def _print_feature_details(self, idx: int, item: Dict):
        """기능 상세 정보 출력"""
        
        print(f"{idx}. 📦 {item['category']} > {item['name']}")
        print(f"   📝 설명: {item['description']}")
        print(f"   📂 경로: {item['path']}")
        
        if "features" in item:
            print(f"   ✨ 기능:")
            for feature in item["features"]:
                print(f"      • {feature}")
        
        if "efficiency_scores" in item:
            print(f"   📊 효율성 점수:")
            for key, score in item["efficiency_scores"].items():
                print(f"      • {key}: {score}")
        
        print(f"   🚀 사용법: {item['usage']}")
        print()
    
    def list_all_features(self):
        """모든 기능 목록 출력"""
        
        print("\n" + "="*100)
        print("📚 구현된 모든 기능 목록")
        print("="*100 + "\n")
        
        for category, features in self.feature_db.items():
            print(f"\n🧠 {category}")
            print("  " + "-"*80)
            
            for feature in features:
                print(f"  📦 {feature['name']}")
                print(f"     설명: {feature['description']}")
                print(f"     경로: {feature['path']}")
                print(f"     사용: {feature['usage']}")
                print()
    
    def create_checklist(self):
        """새로운 기능 개발 전 체크리스트"""
        
        checklist = """
╔════════════════════════════════════════════════════════════════════════════════╗
║  ✅ 새로운 기능 개발 전 체크리스트                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

📋 단계별 체크:

1️⃣ 기능명 정의
   [ ] 개발하려는 기능의 이름/목적 명확히 정의
   [ ] 키워드 3-5개 작성 (예: "신경계", "추적", "효율")

2️⃣ 기존 기능 검색 (필수!)
   [ ] 이 도구로 검색: python3 check_existing_features.py
   [ ] 검색 키워드: 기능명 + 관련 키워드
   [ ] 결과 확인: 찾은 기능이 요구사항 충족하는지 검토

3️⃣ 검색 결과 판단
   ✅ 이미 있고 충분하면:
      → 기존 코드 사용 (중복 방지!)
      → 필요하면 확장/수정
   
   ⚠️  있지만 부족하면:
      → 기존 코드 이해
      → 확장 기능만 추가
   
   ❌ 없으면:
      → 새로 만들기
      → 완성 후 이 DB에 등록

4️⃣ 개발
   [ ] 기존 패턴 따르기 (PEP 8, 타입힌팅)
   [ ] 문서화 (docstring, 주석)
   [ ] 로그 및 테스트

5️⃣ 완성 후 체크
   [ ] 새 기능 DB에 등록
   [ ] README 업데이트
   [ ] 사용 예시 작성

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 빠른 체크 방법:

# 기능 검색
python3 check_existing_features.py "신경계 추적"

# 또는 직접 검색
from check_existing_features import FeatureChecker
checker = FeatureChecker()
results = checker.check_feature("neural", "신경계 기반 시스템")

# 모든 기능 보기
checker.list_all_features()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 팁:
   • 검색 결과에 경로(path)와 사용법(usage)이 나옵니다
   • "유사한 기능"도 확인해보세요 - 거의 같을 수 있습니다
   • 모르면 일단 검색하세요! (5초 vs 1시간 중복 개발)

"""
        
        print(checklist)
        return checklist
    
    def save_feature_db(self):
        """기능 DB 저장"""
        
        db_path = self.workspace / "feature_database.json"
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(self.feature_db, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 기능 DB 저장: {db_path}")
        return db_path


def main():
    """메인 실행"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║  🤖 기존 기능 자동 체크 시스템                                              ║
║  (새로운 기능을 만들기 전에 이미 있는 기능을 자동으로 검색)                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    checker = FeatureChecker()
    
    # 테스트 검색들
    test_searches = [
        ("신경계 추적", "신경계별 모델 효율 추적"),
        ("API 트래킹", "API 사용량 모니터링"),
        ("Q-Learning", "강화학습 시스템"),
        ("신경라우팅", "작업을 최적 모델로 라우팅"),
    ]
    
    print("\n📋 테스트 검색들:\n")
    
    for keyword, description in test_searches:
        results = checker.check_feature(keyword, description)
        input("\n[Enter 누르세요 계속...]")
    
    # 체크리스트 출력
    checker.create_checklist()
    
    # DB 저장
    checker.save_feature_db()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 명령줄에서 검색
        keyword = sys.argv[1]
        description = sys.argv[2] if len(sys.argv) > 2 else ""
        
        checker = FeatureChecker()
        checker.check_feature(keyword, description)
    else:
        # 대화형 모드
        main()
