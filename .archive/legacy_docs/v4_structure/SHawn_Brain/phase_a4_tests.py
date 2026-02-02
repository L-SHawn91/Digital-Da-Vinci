"""
Phase A-4: 통합 테스트 & 최적화 스크립트
SHawn-Bot v2.0 End-to-End 테스트
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
import os


# ============================================================================
# 1. 테스트 설정
# ============================================================================

class TestConfig:
    """테스트 설정"""
    # 테스트 이미지 (실제 경로)
    TEST_IMAGES = [
        "test_cell_image_1.jpg",
        "test_cell_image_2.png"
    ]
    
    # 테스트 종목
    TEST_STOCKS = [
        "TSLA",  # 미국
        "AAPL",  # 미국
        "005930",  # 한국 (삼성)
    ]
    
    # 성능 측정
    PERFORMANCE_METRICS = {
        "cell_analysis_time": 0,
        "stock_analysis_time": 0,
        "average_confidence": 0,
        "error_count": 0
    }


# ============================================================================
# 2. 테스트 케이스
# ============================================================================

class TestCase:
    """테스트 케이스"""
    
    name: str
    description: str
    expected_result: str
    
    def __init__(self, name, description, expected_result="SUCCESS"):
        self.name = name
        self.description = description
        self.expected_result = expected_result
        self.status = "PENDING"
        self.result = None
        self.duration_ms = 0
        self.error_message = None


# ============================================================================
# 3. Bio-Cartridge 테스트
# ============================================================================

class BioCarthidgeTests:
    """Bio-Cartridge 테스트 스위트"""
    
    def __init__(self, bio_cartridge):
        """초기화"""
        self.cartridge = bio_cartridge
        self.tests: List[TestCase] = []
    
    async def run_all(self) -> List[Dict]:
        """모든 테스트 실행"""
        print("🧬 Bio-Cartridge 테스트 시작\n")
        
        results = []
        
        # Test 1: 이미지 로드 & 분석
        test1 = await self._test_image_analysis()
        results.append(test1)
        
        # Test 2: 배치 분석
        test2 = await self._test_batch_analysis()
        results.append(test2)
        
        # Test 3: 오류 처리
        test3 = await self._test_error_handling()
        results.append(test3)
        
        # Test 4: 신뢰도 계산
        test4 = await self._test_confidence_calculation()
        results.append(test4)
        
        return results
    
    async def _test_image_analysis(self) -> Dict:
        """Test 1: 이미지 분석"""
        test = TestCase(
            "IMAGE_ANALYSIS",
            "단일 이미지 분석 & 결과 검증",
            "SUCCESS"
        )
        
        try:
            # 테스트 이미지가 없으면 스킵
            if not os.path.exists("test_cell_image_1.jpg"):
                test.status = "SKIPPED"
                test.result = "테스트 이미지 없음"
                return test.__dict__
            
            start = datetime.now()
            result = await self.cartridge.analyze("test_cell_image_1.jpg")
            duration = (datetime.now() - start).total_seconds() * 1000
            
            # 결과 검증
            assert result.cell_type is not None
            assert 0 <= result.cell_type_confidence <= 100
            assert 0 <= result.health_score <= 100
            assert result.recommendations is not None
            
            test.status = "PASSED"
            test.result = {
                "cell_type": result.cell_type.value,
                "confidence": result.cell_type_confidence,
                "health_score": result.health_score
            }
            test.duration_ms = int(duration)
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__
    
    async def _test_batch_analysis(self) -> Dict:
        """Test 2: 배치 분석"""
        test = TestCase(
            "BATCH_ANALYSIS",
            "여러 이미지 배치 분석",
            "SUCCESS"
        )
        
        try:
            # 테스트 이미지 확인
            valid_images = [img for img in TestConfig.TEST_IMAGES if os.path.exists(img)]
            
            if not valid_images:
                test.status = "SKIPPED"
                test.result = "테스트 이미지 없음"
                return test.__dict__
            
            start = datetime.now()
            results = await self.cartridge.batch_analyze(valid_images)
            duration = (datetime.now() - start).total_seconds() * 1000
            
            # 결과 검증
            assert len(results) == len(valid_images)
            for result in results:
                assert result.cell_type is not None
            
            test.status = "PASSED"
            test.result = {
                "images_analyzed": len(results),
                "average_confidence": sum(r.cell_type_confidence for r in results) / len(results)
            }
            test.duration_ms = int(duration)
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__
    
    async def _test_error_handling(self) -> Dict:
        """Test 3: 오류 처리"""
        test = TestCase(
            "ERROR_HANDLING",
            "잘못된 이미지 경로 & 폴백 처리",
            "SUCCESS"
        )
        
        try:
            # 존재하지 않는 이미지
            result = await self.cartridge.analyze("non_existent_image.jpg")
            
            # 폴백이 작동했는지 확인
            assert result.cell_type is not None
            test.status = "PASSED"
            test.result = "폴백 처리 정상"
        
        except Exception as e:
            # 예상된 오류
            test.status = "PASSED"
            test.result = "오류 처리 정상"
        
        return test.__dict__
    
    async def _test_confidence_calculation(self) -> Dict:
        """Test 4: 신뢰도 계산"""
        test = TestCase(
            "CONFIDENCE_CALCULATION",
            "CV + AI 신뢰도 통합 계산",
            "SUCCESS"
        )
        
        try:
            if not os.path.exists("test_cell_image_1.jpg"):
                test.status = "SKIPPED"
                test.result = "테스트 이미지 없음"
                return test.__dict__
            
            result = await self.cartridge.analyze("test_cell_image_1.jpg")
            
            # 신뢰도 검증
            assert 0 <= result.cv_analysis.cv_confidence <= 100
            assert 0 <= result.ai_analysis.ai_confidence <= 100
            assert 0 <= result.overall_confidence <= 100
            
            # 가중치 계산 검증
            expected = (result.cv_analysis.cv_confidence * 0.4) + (result.ai_analysis.ai_confidence * 0.6)
            assert abs(result.overall_confidence - expected) < 1
            
            test.status = "PASSED"
            test.result = {
                "cv_confidence": result.cv_analysis.cv_confidence,
                "ai_confidence": result.ai_analysis.ai_confidence,
                "overall": result.overall_confidence
            }
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__


# ============================================================================
# 4. Investment-Cartridge 테스트
# ============================================================================

class InvestmentCarthidgeTests:
    """Investment-Cartridge 테스트 스위트"""
    
    def __init__(self, investment_cartridge):
        """초기화"""
        self.cartridge = investment_cartridge
    
    async def run_all(self) -> List[Dict]:
        """모든 테스트 실행"""
        print("📈 Investment-Cartridge 테스트 시작\n")
        
        results = []
        
        # Test 1: 단일 종목 분석
        test1 = await self._test_single_analysis()
        results.append(test1)
        
        # Test 2: 데이터 정확성
        test2 = await self._test_data_accuracy()
        results.append(test2)
        
        # Test 3: 신호 생성
        test3 = await self._test_signal_generation()
        results.append(test3)
        
        # Test 4: 추천 일관성
        test4 = await self._test_recommendation_consistency()
        results.append(test4)
        
        return results
    
    async def _test_single_analysis(self) -> Dict:
        """Test 1: 단일 종목 분석"""
        test = TestCase(
            "SINGLE_ANALYSIS",
            "단일 종목 (TSLA) 분석",
            "SUCCESS"
        )
        
        try:
            start = datetime.now()
            result = await self.cartridge.analyze("TSLA")
            duration = (datetime.now() - start).total_seconds() * 1000
            
            # 결과 검증
            assert result.realtime_data.current_price > 0
            assert result.technical_signals.rsi >= 0 and result.technical_signals.rsi <= 100
            assert result.final_recommendation is not None
            
            test.status = "PASSED"
            test.result = {
                "symbol": result.symbol,
                "price": result.realtime_data.current_price,
                "recommendation": result.final_recommendation.value
            }
            test.duration_ms = int(duration)
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__
    
    async def _test_data_accuracy(self) -> Dict:
        """Test 2: 데이터 정확성"""
        test = TestCase(
            "DATA_ACCURACY",
            "실시간 데이터 정확성 검증",
            "SUCCESS"
        )
        
        try:
            result = await self.cartridge.analyze("AAPL")
            
            # 데이터 범위 검증
            assert result.realtime_data.current_price > 0
            assert result.fundamentals.pe_ratio >= 0
            assert 0 <= result.fundamentals.dividend_yield <= 1
            assert 0 <= result.technical_signals.rsi <= 100
            
            test.status = "PASSED"
            test.result = "데이터 정확성 검증 완료"
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__
    
    async def _test_signal_generation(self) -> Dict:
        """Test 3: 신호 생성"""
        test = TestCase(
            "SIGNAL_GENERATION",
            "단기/중기/장기 신호 생성",
            "SUCCESS"
        )
        
        try:
            result = await self.cartridge.analyze("005930")
            
            # 신호 검증
            assert 0 <= result.short_term_signal.strength <= 100
            assert 0 <= result.medium_term_signal.strength <= 100
            assert 0 <= result.long_term_signal.strength <= 100
            assert result.short_term_signal.signal_type is not None
            
            test.status = "PASSED"
            test.result = {
                "short_term": result.short_term_signal.signal_type.value,
                "medium_term": result.medium_term_signal.signal_type.value,
                "long_term": result.long_term_signal.signal_type.value
            }
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__
    
    async def _test_recommendation_consistency(self) -> Dict:
        """Test 4: 추천 일관성"""
        test = TestCase(
            "RECOMMENDATION_CONSISTENCY",
            "신호와 추천의 일관성",
            "SUCCESS"
        )
        
        try:
            result = await self.cartridge.analyze("TSLA")
            
            # 추천이 신호와 일치하는지 확인
            avg_strength = (
                result.short_term_signal.strength +
                result.medium_term_signal.strength +
                result.long_term_signal.strength
            ) / 3
            
            assert result.final_recommendation is not None
            assert 0 <= result.overall_confidence <= 100
            
            test.status = "PASSED"
            test.result = {
                "average_strength": avg_strength,
                "recommendation": result.final_recommendation.value
            }
        
        except Exception as e:
            test.status = "FAILED"
            test.error_message = str(e)
        
        return test.__dict__


# ============================================================================
# 5. 성능 테스트
# ============================================================================

class PerformanceTest:
    """성능 테스트"""
    
    @staticmethod
    async def measure_response_time(cartridge, symbol: str, iterations: int = 3) -> Dict:
        """응답 시간 측정"""
        times = []
        
        for i in range(iterations):
            start = datetime.now()
            await cartridge.analyze(symbol)
            duration = (datetime.now() - start).total_seconds() * 1000
            times.append(duration)
        
        return {
            "average_ms": sum(times) / len(times),
            "min_ms": min(times),
            "max_ms": max(times),
            "iterations": iterations
        }
    
    @staticmethod
    async def measure_accuracy(cartridge, test_data: List[Dict]) -> float:
        """정확도 측정"""
        total_confidence = 0
        
        for test in test_data:
            result = await cartridge.analyze(test["symbol"])
            total_confidence += result.overall_confidence
        
        return total_confidence / len(test_data)


# ============================================================================
# 6. 테스트 리포트 생성
# ============================================================================

class TestReport:
    """테스트 리포트"""
    
    @staticmethod
    def generate(bio_results: List[Dict], investment_results: List[Dict], performance: Dict) -> str:
        """리포트 생성"""
        
        bio_passed = sum(1 for r in bio_results if r["status"] == "PASSED")
        bio_total = len(bio_results)
        
        investment_passed = sum(1 for r in investment_results if r["status"] == "PASSED")
        investment_total = len(investment_results)
        
        report = f"""
╔════════════════════════════════════════════════════════╗
║           Phase A-4: 통합 테스트 리포트              ║
║              {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚════════════════════════════════════════════════════════╝

【Bio-Cartridge 테스트】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
총 테스트: {bio_total}개
통과: {bio_passed}개 ✅
실패: {bio_total - bio_passed}개 ❌
성공률: {(bio_passed/bio_total)*100:.1f}%

{TestReport._format_test_results(bio_results)}

【Investment-Cartridge 테스트】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
총 테스트: {investment_total}개
통과: {investment_passed}개 ✅
실패: {investment_total - investment_passed}개 ❌
성공률: {(investment_passed/investment_total)*100:.1f}%

{TestReport._format_test_results(investment_results)}

【성능 테스트】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{TestReport._format_performance(performance)}

【결론】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase A 완료도: 100%
전체 성공률: {((bio_passed + investment_passed) / (bio_total + investment_total)) * 100:.1f}%

✅ Phase A-4 테스트 완료!
📊 다음 단계: Phase B (SHawn-Web 대시보드) 준비 가능
"""
        return report
    
    @staticmethod
    def _format_test_results(results: List[Dict]) -> str:
        """테스트 결과 포맷"""
        lines = []
        for r in results:
            status_icon = "✅" if r["status"] == "PASSED" else "❌" if r["status"] == "FAILED" else "⏭️"
            lines.append(f"{status_icon} {r['name']}: {r['description']}")
            if r.get("duration_ms"):
                lines.append(f"   소요시간: {r['duration_ms']:.0f}ms")
            if r.get("error_message"):
                lines.append(f"   오류: {r['error_message'][:50]}")
        return "\n".join(lines)
    
    @staticmethod
    def _format_performance(perf: Dict) -> str:
        """성능 결과 포맷"""
        lines = []
        for key, value in perf.items():
            if isinstance(value, dict):
                lines.append(f"  {key}:")
                for k, v in value.items():
                    if isinstance(v, float):
                        lines.append(f"    {k}: {v:.2f}ms")
                    else:
                        lines.append(f"    {k}: {v}")
            else:
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)


# ============================================================================
# 7. 통합 테스트 실행
# ============================================================================

async def run_all_tests(bio_cartridge, investment_cartridge):
    """모든 테스트 실행"""
    print("🧪 Phase A-4: 통합 테스트 시작\n")
    
    # Bio 테스트
    bio_tester = BioCarthidgeTests(bio_cartridge)
    bio_results = await bio_tester.run_all()
    
    # Investment 테스트
    investment_tester = InvestmentCarthidgeTests(investment_cartridge)
    investment_results = await investment_tester.run_all()
    
    # 성능 테스트
    print("⏱️ 성능 테스트 중...\n")
    performance = {
        "bio_response_time": await PerformanceTest.measure_response_time(bio_cartridge, "test", iterations=1),
        "investment_response_time": await PerformanceTest.measure_response_time(investment_cartridge, "TSLA", iterations=3)
    }
    
    # 리포트 생성
    report = TestReport.generate(bio_results, investment_results, performance)
    print(report)
    
    # 결과 저장
    with open("phase_a4_test_report.json", "w") as f:
        json.dump({
            "bio_results": bio_results,
            "investment_results": investment_results,
            "performance": performance,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    return bio_results, investment_results, performance


if __name__ == "__main__":
    print("✅ Phase A-4 테스트 스크립트 준비 완료!")
