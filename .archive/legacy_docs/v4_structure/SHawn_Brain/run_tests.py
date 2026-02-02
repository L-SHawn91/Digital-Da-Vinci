#!/usr/bin/env python3
"""
Phase A-4 테스트 실행 스크립트
Bio-Cartridge v2.0 & Investment-Cartridge v2.0 통합 테스트
"""

import asyncio
import sys
import os
from datetime import datetime

# 경로 설정
sys.path.insert(0, os.path.dirname(__file__))

async def main():
    """메인 테스트 실행"""
    
    print("""
╔════════════════════════════════════════════════════════╗
║     Phase A-4: 통합 테스트 실행 스크립트              ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # 환경 변수 확인
    print("🔍 환경 변수 확인 중...\n")
    
    required_env = {
        "GEMINI_API_KEY": "Gemini API 키",
        "FINNHUB_API_KEY": "Finnhub API 키"
    }
    
    missing = []
    for env_var, desc in required_env.items():
        if not os.getenv(env_var):
            missing.append(f"  ❌ {env_var}: {desc}")
        else:
            print(f"  ✅ {env_var}: 설정됨")
    
    if missing:
        print("\n⚠️ 누락된 환경 변수:")
        for m in missing:
            print(m)
        print("\n설정 방법:")
        print("  export GEMINI_API_KEY='your-key'")
        print("  export FINNHUB_API_KEY='your-key'")
        return False
    
    print("\n✅ 모든 환경 변수 준비됨\n")
    
    # 라이브러리 확인
    print("📦 라이브러리 확인 중...\n")
    
    required_libs = {
        "cv2": "OpenCV (이미지 처리)",
        "google.generativeai": "Gemini API",
        "yfinance": "Yahoo Finance",
        "aiohttp": "비동기 HTTP"
    }
    
    missing_libs = []
    for lib, desc in required_libs.items():
        try:
            __import__(lib)
            print(f"  ✅ {lib}: {desc}")
        except ImportError:
            missing_libs.append(f"  ❌ {lib}: {desc}")
    
    if missing_libs:
        print("\n⚠️ 누락된 라이브러리:")
        for m in missing_libs:
            print(m)
        print("\n설치 방법:")
        print("  pip install opencv-python google-generativeai yfinance python-aiohttp")
        return False
    
    print("\n✅ 모든 라이브러리 설치됨\n")
    
    # 테스트 실행 준비
    print("🧪 테스트 실행 준비 중...\n")
    
    try:
        # Bio-Cartridge 테스트
        print("=" * 60)
        print("🧬 Bio-Cartridge v2.0 테스트")
        print("=" * 60)
        
        print("""
테스트 준비:
1. 테스트 이미지 준비 (JPG/PNG)
   - test_cell_image_1.jpg
   - test_cell_image_2.png
   (없으면 스킵됨)

테스트 케이스:
  1️⃣ 이미지 분석
  2️⃣ 배치 분석
  3️⃣ 오류 처리
  4️⃣ 신뢰도 계산

예상 시간: ~30초/이미지
        """)
        
        # Investment-Cartridge 테스트
        print("=" * 60)
        print("📈 Investment-Cartridge v2.0 테스트")
        print("=" * 60)
        
        print("""
테스트 케이스:
  1️⃣ 단일 종목 분석 (TSLA)
  2️⃣ 데이터 정확성 (AAPL)
  3️⃣ 신호 생성 (005930 삼성)
  4️⃣ 추천 일관성

예상 시간: ~15초/종목
        """)
        
        # 테스트 실행 여부 확인
        print("\n" + "=" * 60)
        response = input("🚀 테스트를 실행하시겠습니까? (y/n): ").lower()
        
        if response != 'y':
            print("❌ 테스트 취소됨")
            return False
        
        # 실제 테스트 import
        from phase_a4_tests import (
            BioCarthidgeTests,
            InvestmentCarthidgeTests,
            TestReport
        )
        from bio_cartridge_v2 import BioCartridgeV2
        from investment_cartridge_v2 import InvestmentCartridgeV2
        
        print("\n🔧 카트리지 초기화 중...\n")
        
        # 카트리지 초기화
        bio_cartridge = BioCartridgeV2()
        investment_cartridge = InvestmentCartridgeV2()
        
        # Bio 테스트
        bio_tester = BioCarthidgeTests(bio_cartridge)
        print("\n🧬 Bio-Cartridge 테스트 시작...\n")
        bio_results = await bio_tester.run_all()
        
        # Investment 테스트
        investment_tester = InvestmentCarthidgeTests(investment_cartridge)
        print("\n📈 Investment-Cartridge 테스트 시작...\n")
        investment_results = await investment_tester.run_all()
        
        # 리포트 생성
        print("\n" + "=" * 60)
        report = TestReport.generate(bio_results, investment_results, {})
        print(report)
        
        # 결과 저장
        import json
        with open("test_results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "bio_results": bio_results,
                "investment_results": investment_results
            }, f, indent=2)
        
        print("✅ 결과 저장: test_results.json\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
        sys.exit(1)
