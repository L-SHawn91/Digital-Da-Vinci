"""
테스트 & QA 자동화 - 품질 보증

역할:
- 단위 테스트
- 통합 테스트
- 성능 테스트
- 자동 리포트
"""

from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestCase:
    """테스트 케이스"""
    name: str
    test_func: Callable
    expected_result: Any = None
    tags: List[str] = None


@dataclass
class TestResult:
    """테스트 결과"""
    test_name: str
    status: str  # passed, failed, skipped
    duration_ms: float
    error_message: str = None
    timestamp: datetime = None


class TestRunner:
    """테스트 러너"""
    
    def __init__(self):
        self.test_cases: Dict[str, TestCase] = {}
        self.test_results: List[TestResult] = []
    
    def register_test(self, name: str, test_func: Callable, tags: List[str] = None):
        """테스트 등록"""
        
        test_case = TestCase(
            name=name,
            test_func=test_func,
            tags=tags or []
        )
        
        self.test_cases[name] = test_case
    
    async def run_test(self, test_name: str) -> TestResult:
        """단일 테스트 실행"""
        
        if test_name not in self.test_cases:
            return TestResult(
                test_name=test_name,
                status='skipped',
                duration_ms=0,
                error_message='Test not found'
            )
        
        test_case = self.test_cases[test_name]
        start_time = datetime.now()
        
        try:
            import asyncio
            
            if asyncio.iscoroutinefunction(test_case.test_func):
                result = await test_case.test_func()
            else:
                result = test_case.test_func()
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            test_result = TestResult(
                test_name=test_name,
                status='passed',
                duration_ms=duration_ms,
                timestamp=start_time
            )
        
        except AssertionError as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            test_result = TestResult(
                test_name=test_name,
                status='failed',
                duration_ms=duration_ms,
                error_message=str(e),
                timestamp=start_time
            )
        
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            test_result = TestResult(
                test_name=test_name,
                status='failed',
                duration_ms=duration_ms,
                error_message=f"Unexpected error: {str(e)}",
                timestamp=start_time
            )
        
        self.test_results.append(test_result)
        return test_result
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """모든 테스트 실행"""
        
        results = []
        
        for test_name in self.test_cases.keys():
            result = await self.run_test(test_name)
            results.append(result)
        
        return self._generate_report(results)
    
    async def run_tests_by_tag(self, tag: str) -> Dict[str, Any]:
        """태그별 테스트 실행"""
        
        results = []
        
        for test_case in self.test_cases.values():
            if tag in test_case.tags:
                result = await self.run_test(test_case.name)
                results.append(result)
        
        return self._generate_report(results)
    
    def _generate_report(self, results: List[TestResult]) -> Dict[str, Any]:
        """리포트 생성"""
        
        passed = sum(1 for r in results if r.status == 'passed')
        failed = sum(1 for r in results if r.status == 'failed')
        skipped = sum(1 for r in results if r.status == 'skipped')
        
        total_duration_ms = sum(r.duration_ms for r in results)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(results),
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'pass_rate': (passed / len(results) * 100) if results else 0
            },
            'duration_ms': total_duration_ms,
            'results': [
                {
                    'name': r.test_name,
                    'status': r.status,
                    'duration_ms': r.duration_ms,
                    'error': r.error_message
                }
                for r in results
            ]
        }


class PerformanceTester:
    """성능 테스터"""
    
    def __init__(self):
        self.benchmarks = []
    
    async def benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 100
    ) -> Dict[str, Any]:
        """벤치마크 테스트"""
        
        durations = []
        
        for _ in range(iterations):
            import time
            start = time.time()
            
            try:
                import asyncio
                
                if asyncio.iscoroutinefunction(func):
                    await func()
                else:
                    func()
            
            except Exception:
                pass
            
            duration = (time.time() - start) * 1000
            durations.append(duration)
        
        import statistics
        
        benchmark_result = {
            'name': name,
            'iterations': iterations,
            'min_ms': min(durations),
            'max_ms': max(durations),
            'avg_ms': statistics.mean(durations),
            'median_ms': statistics.median(durations),
            'stdev_ms': statistics.stdev(durations) if len(durations) > 1 else 0,
            'p95_ms': sorted(durations)[int(len(durations) * 0.95)]
        }
        
        self.benchmarks.append(benchmark_result)
        
        return benchmark_result


class CoverageAnalyzer:
    """커버리지 분석기"""
    
    def __init__(self):
        self.covered_lines = set()
        self.total_lines = 0
    
    def add_coverage(self, module_name: str, line_numbers: List[int]):
        """커버리지 추가"""
        
        self.covered_lines.update(line_numbers)
        self.total_lines = max(self.total_lines, max(line_numbers))
    
    def get_coverage_report(self) -> Dict[str, Any]:
        """커버리지 리포트"""
        
        coverage_percent = (len(self.covered_lines) / self.total_lines * 100) if self.total_lines > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_lines': self.total_lines,
            'covered_lines': len(self.covered_lines),
            'coverage_percent': coverage_percent,
            'status': 'good' if coverage_percent > 80 else 'warning' if coverage_percent > 60 else 'poor'
        }


class QAAutomation:
    """QA 자동화 플랫폼"""
    
    def __init__(self):
        self.test_runner = TestRunner()
        self.performance_tester = PerformanceTester()
        self.coverage_analyzer = CoverageAnalyzer()
        self.qa_report = None
    
    async def run_qa_suite(self) -> Dict[str, Any]:
        """QA 스위트 실행"""
        
        qa_start = datetime.now()
        
        # 1. 단위 테스트 실행
        unit_test_report = await self.test_runner.run_all_tests()
        
        # 2. 커버리지 분석
        coverage_report = self.coverage_analyzer.get_coverage_report()
        
        # 3. 통합 리포트
        qa_duration = (datetime.now() - qa_start).total_seconds() * 1000
        
        self.qa_report = {
            'timestamp': qa_start.isoformat(),
            'total_duration_ms': qa_duration,
            'unit_tests': unit_test_report,
            'coverage': coverage_report,
            'overall_status': 'passed' if unit_test_report['summary']['failed'] == 0 else 'failed'
        }
        
        return self.qa_report
    
    def get_qa_report(self) -> Dict[str, Any]:
        """QA 리포트 조회"""
        return self.qa_report or {'status': 'no_report'}


if __name__ == "__main__":
    print("🧪 테스트 & QA 자동화 테스트\n")
    
    qa = QAAutomation()
    
    # 테스트 등록
    def test_addition():
        assert 2 + 2 == 4, "Addition failed"
    
    def test_subtraction():
        assert 5 - 3 == 2, "Subtraction failed"
    
    def test_failing():
        assert 1 == 2, "This test fails"
    
    qa.test_runner.register_test('test_addition', test_addition, tags=['math'])
    qa.test_runner.register_test('test_subtraction', test_subtraction, tags=['math'])
    qa.test_runner.register_test('test_failing', test_failing, tags=['math'])
    
    print("✅ 테스트 등록 완료!")
    
    # 테스트 실행
    import asyncio
    
    async def test():
        report = await qa.run_qa_suite()
        
        print(f"✅ QA 스위트 완료!")
        print(f"총 테스트: {report['unit_tests']['summary']['total']}")
        print(f"통과: {report['unit_tests']['summary']['passed']}")
        print(f"실패: {report['unit_tests']['summary']['failed']}")
        print(f"통과율: {report['unit_tests']['summary']['pass_rate']:.1f}%")
    
    asyncio.run(test())
