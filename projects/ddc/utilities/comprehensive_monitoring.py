"""
종합 메트릭 수집 & 모니터링 - 전체 시스템 가시성

역할:
- 메트릭 수집 & 저장
- 실시간 대시보드
- 이상 탐지
- 성능 리포트
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import deque


@dataclass
class Metric:
    """메트릭"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None


class MetricsCollector:
    """메트릭 수집기"""
    
    def __init__(self, max_metrics: int = 100000):
        self.metrics: deque = deque(maxlen=max_metrics)
        self.aggregations: Dict[str, Dict[str, Any]] = {}
    
    def record_metric(
        self,
        name: str,
        value: float,
        tags: Dict[str, str] = None
    ):
        """메트릭 기록"""
        
        metric = Metric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        
        self.metrics.append(metric)
    
    def get_metrics_by_name(self, name: str) -> List[Metric]:
        """이름으로 메트릭 조회"""
        return [m for m in self.metrics if m.name == name]
    
    def aggregate_metrics(
        self,
        name: str,
        window_minutes: int = 5
    ) -> Dict[str, Any]:
        """메트릭 집계"""
        
        relevant_metrics = self.get_metrics_by_name(name)
        
        if not relevant_metrics:
            return {'status': 'no_data'}
        
        # 시간 윈도우 필터
        cutoff_time = datetime.now()
        cutoff_time = cutoff_time.replace(
            minute=cutoff_time.minute - window_minutes
        )
        
        windowed = [
            m for m in relevant_metrics
            if m.timestamp >= cutoff_time
        ]
        
        if not windowed:
            windowed = relevant_metrics[-100:]
        
        values = [m.value for m in windowed]
        
        import statistics
        
        aggregation = {
            'name': name,
            'window_minutes': window_minutes,
            'count': len(windowed),
            'sum': sum(values),
            'avg': statistics.mean(values),
            'min': min(values),
            'max': max(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'latest': windowed[-1].value if windowed else None
        }
        
        self.aggregations[f"{name}_{window_minutes}m"] = aggregation
        
        return aggregation


class SystemMetricsMonitor:
    """시스템 메트릭 모니터"""
    
    def __init__(self):
        self.collector = MetricsCollector()
        self.alerts = []
        self.thresholds = {
            'api_latency_ms': 500,
            'error_rate_percent': 5,
            'memory_usage_percent': 80,
            'cpu_usage_percent': 80
        }
    
    def record_api_call(
        self,
        endpoint: str,
        latency_ms: float,
        status_code: int,
        error: bool = False
    ):
        """API 호출 기록"""
        
        self.collector.record_metric(
            'api_latency_ms',
            latency_ms,
            {'endpoint': endpoint, 'status': str(status_code)}
        )
        
        if error:
            self.collector.record_metric(
                'api_error',
                1.0,
                {'endpoint': endpoint}
            )
    
    def record_resource_usage(
        self,
        memory_percent: float,
        cpu_percent: float,
        disk_percent: float
    ):
        """리소스 사용량 기록"""
        
        self.collector.record_metric('memory_usage_percent', memory_percent)
        self.collector.record_metric('cpu_usage_percent', cpu_percent)
        self.collector.record_metric('disk_usage_percent', disk_percent)
        
        # 임계값 확인
        if memory_percent > self.thresholds['memory_usage_percent']:
            self.alerts.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'high_memory',
                'value': memory_percent,
                'threshold': self.thresholds['memory_usage_percent']
            })
        
        if cpu_percent > self.thresholds['cpu_usage_percent']:
            self.alerts.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'high_cpu',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu_usage_percent']
            })
    
    def get_monitoring_report(self) -> Dict[str, Any]:
        """모니터링 리포트"""
        
        # 각 메트릭 집계
        api_latency_agg = self.collector.aggregate_metrics('api_latency_ms', 5)
        memory_agg = self.collector.aggregate_metrics('memory_usage_percent', 5)
        cpu_agg = self.collector.aggregate_metrics('cpu_usage_percent', 5)
        
        # 에러율 계산
        error_metrics = self.collector.get_metrics_by_name('api_error')
        api_metrics = self.collector.get_metrics_by_name('api_latency_ms')
        
        error_rate = 0
        if api_metrics:
            error_rate = len(error_metrics) / len(api_metrics) * 100
        
        return {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_metrics_recorded': len(self.collector.metrics),
                'active_alerts': len(self.alerts)
            },
            'api_performance': {
                'latency_ms': api_latency_agg,
                'error_rate_percent': error_rate
            },
            'resource_usage': {
                'memory_percent': memory_agg,
                'cpu_percent': cpu_agg
            },
            'recent_alerts': self.alerts[-10:] if self.alerts else [],
            'health_status': self._calculate_health_status(
                api_latency_agg,
                memory_agg,
                cpu_agg,
                error_rate
            )
        }
    
    def _calculate_health_status(
        self,
        latency: Dict,
        memory: Dict,
        cpu: Dict,
        error_rate: float
    ) -> str:
        """건강도 계산"""
        
        issues = 0
        
        if latency.get('avg', 0) > self.thresholds['api_latency_ms']:
            issues += 1
        
        if memory.get('max', 0) > self.thresholds['memory_usage_percent']:
            issues += 1
        
        if cpu.get('max', 0) > self.thresholds['cpu_usage_percent']:
            issues += 1
        
        if error_rate > self.thresholds['error_rate_percent']:
            issues += 1
        
        if issues == 0:
            return 'healthy'
        elif issues <= 1:
            return 'degraded'
        else:
            return 'critical'


class PerformanceBenchmark:
    """성능 벤치마크"""
    
    def __init__(self):
        self.benchmarks = []
    
    def run_benchmark(
        self,
        name: str,
        operations: int,
        duration_seconds: float
    ) -> Dict[str, Any]:
        """벤치마크 실행"""
        
        result = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'operations': operations,
            'duration_seconds': duration_seconds,
            'throughput_ops_per_sec': operations / duration_seconds if duration_seconds > 0 else 0,
            'latency_per_op_ms': (duration_seconds * 1000) / operations if operations > 0 else 0
        }
        
        self.benchmarks.append(result)
        
        return result
    
    def compare_benchmarks(self, name: str) -> Dict[str, Any]:
        """벤치마크 비교"""
        
        related = [b for b in self.benchmarks if b['name'] == name]
        
        if not related:
            return {'status': 'no_benchmarks'}
        
        throughputs = [b['throughput_ops_per_sec'] for b in related]
        latencies = [b['latency_per_op_ms'] for b in related]
        
        import statistics
        
        return {
            'name': name,
            'runs': len(related),
            'throughput': {
                'avg': statistics.mean(throughputs),
                'min': min(throughputs),
                'max': max(throughputs)
            },
            'latency_ms': {
                'avg': statistics.mean(latencies),
                'min': min(latencies),
                'max': max(latencies)
            },
            'trend': 'improving' if throughputs[-1] > throughputs[0] else 'degrading'
        }


if __name__ == "__main__":
    print("📊 종합 모니터링 테스트\n")
    
    monitor = SystemMetricsMonitor()
    
    # 메트릭 기록
    import random
    
    for i in range(50):
        monitor.record_api_call(
            f"/api/endpoint_{i % 5}",
            random.gauss(100, 30),  # latency
            200 if random.random() > 0.1 else 500,
            error=random.random() < 0.05
        )
    
    monitor.record_resource_usage(
        memory_percent=65.5,
        cpu_percent=45.2,
        disk_percent=52.1
    )
    
    print("✅ 메트릭 기록 완료!")
    
    # 리포트
    report = monitor.get_monitoring_report()
    print(f"\n✅ 모니터링 리포트:")
    print(f"상태: {report['health_status']}")
    print(f"API 지연: {report['api_performance']['latency_ms'].get('avg', 0):.0f}ms")
    print(f"에러율: {report['api_performance']['error_rate_percent']:.1f}%")
    
    # 벤치마크
    bench = PerformanceBenchmark()
    result = bench.run_benchmark("api_test", 1000, 5.0)
    print(f"\n✅ 벤치마크:")
    print(f"처리량: {result['throughput_ops_per_sec']:.0f} ops/sec")
    print(f"지연: {result['latency_per_op_ms']:.2f} ms/op")
