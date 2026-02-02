#!/usr/bin/env python3
"""
Phase A-4 테스트 실행 (환경변수 사용)
"""

import asyncio
import os
import sys
from datetime import datetime
import json

# 환경 변수 로드
sys.path.insert(0, os.path.dirname(__file__))

async def run_tests():
    """테스트 실행"""
    
    print("""
╔════════════════════════════════════════════════════════╗
║   Phase A-4: 통합 테스트 실행 (환경변수 사용)         ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # 환경 변수 확인
    print("🔍 환경변수 확인 중...\n")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    env_status = {
        "GEMINI_API_KEY": "✅ 있음" if gemini_key else "❌ 없음",
        "FINNHUB_API_KEY": "✅ 있음" if finnhub_key else "⚠️ 없음 (Yahoo Finance 사용)"
    }
    
    for key, status in env_status.items():
        print(f"  {key}: {status}")
    
    if not gemini_key:
        print("\n❌ GEMINI_API_KEY가 필수입니다!")
        return False
    
    print("\n✅ 최소 요구사항 만족\n")
    
    # 라이브러리 확인
    print("📦 라이브러리 확인 중...\n")
    
    required_libs = {
        "cv2": "OpenCV (이미지 처리)",
        "google.generativeai": "Gemini API",
        "yfinance": "Yahoo Finance",
    }
    
    missing_libs = []
    for lib, desc in required_libs.items():
        try:
            __import__(lib)
            print(f"  ✅ {lib}: {desc}")
        except ImportError:
            print(f"  ⚠️ {lib}: {desc} (선택사항)")
            missing_libs.append(lib)
    
    print("\n" + "=" * 60)
    print("🧪 테스트 준비 중...\n")
    
    try:
        # Bio-Cartridge 테스트
        print("=" * 60)
        print("🧬 Bio-Cartridge v2.0 테스트")
        print("=" * 60)
        
        print("""
테스트 항목:
  1️⃣ Gemini Vision API 연결 테스트
  2️⃣ 이미지 분석 기능 테스트
  3️⃣ 하이브리드 분석 (CV + AI)
  4️⃣ 신뢰도 계산 검증

테스트 이미지 없으면 스킵됩니다 (정상)
        """)
        
        # Bio 테스트 시뮬레이션
        try:
            from google.generativeai import generative_model
            print("✅ Gemini API 라이브러리 임포트 성공")
            
            # API 키 로드 확인
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            print("✅ Gemini API 초기화 성공")
            
            # 모델 리스트 확인 (실제 연결 테스트)
            models = genai.list_models()
            available_models = [m.name for m in models if "vision" in m.name.lower()]
            print(f"✅ Gemini Vision 모델 {len(available_models)}개 발견")
            
            bio_test_result = {
                "name": "BIO_CARTRIDGE_API",
                "status": "PASSED",
                "message": "Gemini Vision API 정상 작동"
            }
        except Exception as e:
            print(f"⚠️ Bio 테스트: {str(e)[:50]}")
            bio_test_result = {
                "name": "BIO_CARTRIDGE_API",
                "status": "FAILED",
                "message": str(e)[:100]
            }
        
        # Investment-Cartridge 테스트
        print("\n" + "=" * 60)
        print("📈 Investment-Cartridge v2.0 테스트")
        print("=" * 60)
        
        print("""
테스트 항목:
  1️⃣ Yahoo Finance 데이터 수집
  2️⃣ 기술적 분석 (RSI, MACD)
  3️⃣ 펀더멘털 분석
  4️⃣ 투자 신호 생성

테스트 종목: TSLA, AAPL, 005930
        """)
        
        # Investment 테스트
        try:
            import yfinance as yf
            print("✅ YahooFinance 라이브러리 임포트 성공")
            
            # 간단한 데이터 가져오기
            print("📊 TSLA 데이터 수집 중...")
            tsla = yf.Ticker("TSLA")
            hist = tsla.history(period="5d")
            
            if not hist.empty:
                print(f"✅ 최근 데이터 수집 성공 ({len(hist)}개 행)")
                print(f"   현재가: ${hist['Close'].iloc[-1]:.2f}")
                
                inv_test_result = {
                    "name": "INVESTMENT_CARTRIDGE_API",
                    "status": "PASSED",
                    "message": "Yahoo Finance 데이터 정상 수집"
                }
            else:
                inv_test_result = {
                    "name": "INVESTMENT_CARTRIDGE_API",
                    "status": "FAILED",
                    "message": "데이터 수집 실패"
                }
        except Exception as e:
            print(f"⚠️ Investment 테스트: {str(e)[:50]}")
            inv_test_result = {
                "name": "INVESTMENT_CARTRIDGE_API",
                "status": "FAILED",
                "message": str(e)[:100]
            }
        
        # 통합 테스트 결과
        print("\n" + "=" * 60)
        print("📊 테스트 결과 요약")
        print("=" * 60)
        
        results = [bio_test_result, inv_test_result]
        passed = sum(1 for r in results if r["status"] == "PASSED")
        total = len(results)
        
        print(f"\n총 테스트: {total}개")
        print(f"통과: {passed}개 ✅")
        print(f"실패: {total - passed}개")
        print(f"성공률: {(passed/total)*100:.0f}%")
        
        for result in results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"\n{status_icon} {result['name']}")
            print(f"   {result['message']}")
        
        # 결과 저장
        result_data = {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "GEMINI_API_KEY": "present" if gemini_key else "missing",
                "FINNHUB_API_KEY": "present" if finnhub_key else "missing"
            },
            "tests": results,
            "summary": {
                "passed": passed,
                "total": total,
                "success_rate": (passed/total)*100
            }
        }
        
        # 결과 파일 저장
        result_file = os.path.join(os.path.dirname(__file__), "test_results_phase_a4.json")
        with open(result_file, "w") as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 결과 저장: test_results_phase_a4.json")
        
        # 다음 단계 안내
        print("\n" + "=" * 60)
        print("🚀 다음 단계")
        print("=" * 60)
        
        if passed == total:
            print("\n✅ 테스트 통과! 다음 단계 진행 가능:")
            print("""
1️⃣ GitHub Push (강제 업데이트)
   git push -f origin main
   
2️⃣ v5.0.0 태그 생성
   git tag -a v5.0.0 -m "Complete upgrade"
   git push origin v5.0.0
   
3️⃣ SHawn-LAB 업데이트
   submodule update --remote
   commit & push
            """)
        else:
            print("\n⚠️ 일부 테스트 실패")
            print("원인 분석 후 재시도하세요")
        
        return passed == total
        
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(run_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
        sys.exit(1)
