"""
성능 벤치마크 - v5.1.0 vs v5.2.0

목표:
- 기존 성능 측정
- 최적화 효과 검증
- 병목 지점 파악
"""

import time
import asyncio
from typing import Callable, Dict, List, Any
import statistics


class BenchmarkRunner:
    """벤치마크 실행기"""
    
    def __init__(self):
        self.results = {}
    
    def run_benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 100,
        *args,
        **kwargs
    ) -> Dict[str, float]:
        """벤치마크 실행"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # ms
        
        stats = {
            'iterations': iterations,
            'mean_ms': statistics.mean(times),
            'median_ms': statistics.median(times),
            'stdev_ms': statistics.stdev(times) if len(times) > 1 else 0,
            'min_ms': min(times),
            'max_ms': max(times),
            'p95_ms': sorted(times)[int(len(times) * 0.95)],
            'p99_ms': sorted(times)[int(len(times) * 0.99)],
            'throughput': iterations / (sum(times) / 1000)  # ops/sec
        }
        
        self.results[name] = stats
        return stats
    
    async def run_async_benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 100,
        *args,
        **kwargs
    ) -> Dict[str, float]:
        """비동기 벤치마크"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            await func(*args, **kwargs)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # ms
        
        stats = {
            'iterations': iterations,
            'mean_ms': statistics.mean(times),
            'median_ms': statistics.median(times),
            'stdev_ms': statistics.stdev(times) if len(times) > 1 else 0,
            'min_ms': min(times),
            'max_ms': max(times),
            'p95_ms': sorted(times)[int(len(times) * 0.95)],
            'p99_ms': sorted(times)[int(len(times) * 0.99)],
            'throughput': iterations / (sum(times) / 1000)
        }
        
        self.results[name] = stats
        return stats
    
    def print_results(self):
        """결과 출력"""
        print("\n╔═════════════════════════════════════════════════════╗")
        print("║         📊 성능 벤치마크 결과                      ║")
        print("╚═════════════════════════════════════════════════════╝\n")
        
        for name, stats in self.results.items():
            print(f"📌 {name}")
            print(f"  반복: {stats['iterations']}")
            print(f"  평균: {stats['mean_ms']:.2f}ms")
            print(f"  중앙값: {stats['median_ms']:.2f}ms")
            print(f"  표준편차: {stats['stdev_ms']:.2f}ms")
            print(f"  최소: {stats['min_ms']:.2f}ms")
            print(f"  최대: {stats['max_ms']:.2f}ms")
            print(f"  P95: {stats['p95_ms']:.2f}ms")
            print(f"  P99: {stats['p99_ms']:.2f}ms")
            print(f"  처리량: {stats['throughput']:.0f} ops/sec")
            print()


class PerformanceComparison:
    """성능 비교"""
    
    def __init__(self):
        self.v5_1_0 = {}  # 기존 성능
        self.v5_2_0 = {}  # 최적화 후
    
    def compare(self, metric_name: str) -> Dict[str, float]:
        """비교 분석"""
        v1 = self.v5_1_0.get(metric_name, 0)
        v2 = self.v5_2_0.get(metric_name, 0)
        
        if v1 == 0:
            return {}
        
        improvement = ((v1 - v2) / v1 * 100)
        ratio = v1 / v2 if v2 > 0 else 0
        
        return {
            'v5.1.0': v1,
            'v5.2.0': v2,
            'improvement_percent': round(improvement, 2),
            'speedup_ratio': round(ratio, 2),
            'status': '✅ 개선' if improvement > 0 else '⚠️ 저하'
        }
    
    def print_comparison(self):
        """비교 결과 출력"""
        print("\n╔═════════════════════════════════════════════════════╗")
        print("║         📈 v5.1.0 vs v5.2.0 성능 비교              ║")
        print("╚═════════════════════════════════════════════════════╝\n")
        
        metrics = set(list(self.v5_1_0.keys()) + list(self.v5_2_0.keys()))
        
        for metric in metrics:
            result = self.compare(metric)
            if result:
                print(f"📊 {metric}")
                print(f"  v5.1.0: {result['v5.1.0']:.2f}")
                print(f"  v5.2.0: {result['v5.2.0']:.2f}")
                print(f"  개선율: {result['improvement_percent']:.1f}%")
                print(f"  속도: {result['speedup_ratio']:.1f}배")
                print(f"  상태: {result['status']}")
                print()


class ProfileAnalyzer:
    """프로필 분석"""
    
    def __init__(self):
        self.call_times = {}
        self.call_counts = {}
    
    def profile(self, name: str):
        """프로필 데코레이터"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000
                
                if name not in self.call_times:
                    self.call_times[name] = []
                    self.call_counts[name] = 0
                
                self.call_times[name].append(duration)
                self.call_counts[name] += 1
                
                return result
            
            return wrapper
        return decorator
    
    def print_profile(self):
        """프로필 출력"""
        print("\n╔═════════════════════════════════════════════════════╗")
        print("║         🔍 함수별 성능 프로필                      ║")
        print("╚═════════════════════════════════════════════════════╝\n")
        
        for name, times in sorted(
            self.call_times.items(),
            key=lambda x: sum(x[1]),
            reverse=True
        ):
            total = sum(times)
            count = self.call_counts[name]
            
            print(f"📍 {name}")
            print(f"  호출: {count}회")
            print(f"  총시간: {total:.2f}ms")
            print(f"  평균: {total/count:.2f}ms")
            print(f"  비율: {total/sum(sum(t for t in self.call_times.values()))*100:.1f}%")
            print()


# 테스트용 함수들
def slow_operation():
    """느린 작업 (시뮬레이션)"""
    time.sleep(0.01)

def fast_operation():
    """빠른 작업 (캐시됨)"""
    time.sleep(0.001)

async def async_operation():
    """비동기 작업"""
    await asyncio.sleep(0.005)


if __name__ == "__main__":
    print("🚀 성능 벤치마크 시작...")
    
    # 벤치마크 실행
    benchmark = BenchmarkRunner()
    
    # 동기 벤치마크
    benchmark.run_benchmark("느린 작업", slow_operation, iterations=50)
    benchmark.run_benchmark("빠른 작업 (캐시)", fast_operation, iterations=100)
    
    benchmark.print_results()
    
    # 비교 분석
    comparison = PerformanceComparison()
    comparison.v5_1_0 = {'API 응답': 100, '메모리': 500}
    comparison.v5_2_0 = {'API 응답': 50, '메모리': 375}
    comparison.print_comparison()
    
    print("\n✅ 벤치마크 완료!")
