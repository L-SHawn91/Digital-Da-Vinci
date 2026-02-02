"""
고급 모니터링 시스템 - 실시간 분석

역할:
- 실시간 메트릭 수집
- 이상 탐지
- 자동 알림
- 트렌드 분석
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
import statistics


class MetricsCollector:
    """메트릭 수집기"""
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.metrics = {
            'api_latency': deque(maxlen=max_samples),
            'neural_health': deque(maxlen=max_samples),
            'cartridge_performance': deque(maxlen=max_samples),
            'error_rate': deque(maxlen=max_samples),
            'cache_hit_rate': deque(maxlen=max_samples)
        }
        self.alerts = []
    
    def record_metric(self, metric_type: str, value: float, metadata: Dict = None):
        """메트릭 기록"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'value': value,
            'metadata': metadata or {}
        }
        
        if metric_type in self.metrics:
            self.metrics[metric_type].append(entry)
    
    def get_stats(self, metric_type: str) -> Dict[str, float]:
        """통계 계산"""
        if not self.metrics[metric_type]:
            return {}
        
        values = [m['value'] for m in self.metrics[metric_type]]
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'p95': sorted(values)[int(len(values) * 0.95)] if len(values) > 1 else values[0],
            'p99': sorted(values)[int(len(values) * 0.99)] if len(values) > 1 else values[0]
        }


class AnomalyDetector:
    """이상 탐지"""
    
    def __init__(self, std_threshold: float = 2.5):
        self.std_threshold = std_threshold
        self.baseline = {}
    
    def detect_anomaly(self, metric_type: str, value: float, stats: Dict) -> Optional[Dict]:
        """이상 탐지"""
        if 'stdev' not in stats or stats['stdev'] == 0:
            return None
        
        mean = stats['mean']
        stdev = stats['stdev']
        
        # Z-score 계산
        z_score = abs((value - mean) / stdev)
        
        if z_score > self.std_threshold:
            return {
                'type': 'anomaly',
                'metric': metric_type,
                'value': value,
                'expected': mean,
                'z_score': round(z_score, 2),
                'severity': 'high' if z_score > 3 else 'medium',
                'timestamp': datetime.now().isoformat()
            }
        
        return None


class AlertManager:
    """알림 관리자"""
    
    def __init__(self):
        self.active_alerts = []
        self.alert_history = []
        self.thresholds = {
            'api_latency_ms': 500,
            'error_rate_percent': 5,
            'cache_hit_rate_percent': 50,
            'neural_health': 0.7
        }
    
    def check_thresholds(self, metrics: Dict[str, Any]) -> List[Dict]:
        """임계값 확인"""
        new_alerts = []
        
        for threshold_key, threshold_value in self.thresholds.items():
            metric_name = threshold_key.replace('_percent', '').replace('_ms', '')
            
            if metric_name in metrics:
                if metrics[metric_name] < threshold_value:
                    alert = {
                        'type': 'threshold_breach',
                        'metric': metric_name,
                        'threshold': threshold_value,
                        'current': metrics[metric_name],
                        'severity': 'high' if abs(metrics[metric_name] - threshold_value) / threshold_value > 0.2 else 'medium',
                        'timestamp': datetime.now().isoformat()
                    }
                    new_alerts.append(alert)
        
        return new_alerts
    
    def add_alert(self, alert: Dict):
        """알림 추가"""
        self.active_alerts.append(alert)
        self.alert_history.append(alert)
    
    def resolve_alert(self, alert_id: str):
        """알림 해결"""
        self.active_alerts = [
            a for a in self.active_alerts
            if a.get('id') != alert_id
        ]
    
    def get_active_alerts(self) -> List[Dict]:
        """활성 알림"""
        return self.active_alerts


class TrendAnalyzer:
    """트렌드 분석기"""
    
    @staticmethod
    def analyze_trend(values: List[float], window: int = 10) -> Dict[str, Any]:
        """추세 분석"""
        if len(values) < window:
            return {'status': 'insufficient_data'}
        
        recent = values[-window:]
        previous = values[-(2*window):-window]
        
        avg_recent = statistics.mean(recent)
        avg_previous = statistics.mean(previous)
        
        change_percent = ((avg_recent - avg_previous) / avg_previous * 100) if avg_previous != 0 else 0
        
        return {
            'trend': 'improving' if change_percent > 0 else 'degrading',
            'change_percent': round(change_percent, 2),
            'velocity': round(change_percent / window, 2),
            'direction': 'up' if change_percent > 0 else 'down',
            'confidence': 'high' if abs(change_percent) > 5 else 'low'
        }
    
    @staticmethod
    def forecast(values: List[float], periods: int = 5) -> List[float]:
        """간단한 예측 (이동 평균)"""
        if len(values) < 3:
            return []
        
        forecast = []
        recent_avg = statistics.mean(values[-3:])
        
        for i in range(periods):
            forecast.append(recent_avg)
        
        return forecast


class HealthScore:
    """건강도 점수"""
    
    def __init__(self):
        self.components = {
            'api_performance': 1.0,
            'error_rate': 1.0,
            'cache_efficiency': 1.0,
            'neural_stability': 1.0
        }
    
    def update_scores(self, metrics: Dict[str, Any]):
        """점수 업데이트"""
        # API 성능 (0-1)
        if 'api_latency_ms' in metrics:
            latency = metrics['api_latency_ms']
            self.components['api_performance'] = max(0, 1 - (latency / 1000))
        
        # 에러율 (0-1)
        if 'error_rate_percent' in metrics:
            error_rate = metrics['error_rate_percent']
            self.components['error_rate'] = max(0, 1 - (error_rate / 100))
        
        # 캐시 효율성 (0-1)
        if 'cache_hit_rate_percent' in metrics:
            hit_rate = metrics['cache_hit_rate_percent']
            self.components['cache_efficiency'] = hit_rate / 100
        
        # 신경계 안정성 (0-1)
        if 'neural_health' in metrics:
            self.components['neural_stability'] = metrics['neural_health']
    
    def get_overall_score(self) -> float:
        """전체 점수"""
        scores = list(self.components.values())
        return round(statistics.mean(scores), 2)
    
    def get_breakdown(self) -> Dict[str, float]:
        """점수 분해"""
        return self.components.copy()


class RealtimeDashboard:
    """실시간 대시보드"""
    
    def __init__(self):
        self.collector = MetricsCollector()
        self.anomaly_detector = AnomalyDetector()
        self.alert_manager = AlertManager()
        self.trend_analyzer = TrendAnalyzer()
        self.health_score = HealthScore()
    
    def generate_dashboard_data(self) -> Dict[str, Any]:
        """대시보드 데이터 생성"""
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'anomalies': [],
            'alerts': self.alert_manager.get_active_alerts(),
            'trends': {},
            'health_score': {
                'overall': self.health_score.get_overall_score(),
                'breakdown': self.health_score.get_breakdown()
            }
        }
        
        # 각 메트릭별 통계
        for metric_type in self.collector.metrics.keys():
            stats = self.collector.get_stats(metric_type)
            dashboard['metrics'][metric_type] = stats
            
            # 트렌드 분석
            values = [m['value'] for m in self.collector.metrics[metric_type]]
            if len(values) >= 10:
                dashboard['trends'][metric_type] = self.trend_analyzer.analyze_trend(values)
        
        return dashboard
    
    def generate_html_report(self) -> str:
        """HTML 리포트 생성"""
        data = self.generate_dashboard_data()
        
        html = f"""
        <html>
        <head>
            <title>SHawn-Brain 실시간 모니터링</title>
            <style>
                body {{ font-family: monospace; background: #0f172a; color: #f1f5f9; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .metric {{ background: #1e293b; padding: 15px; margin: 10px 0; border-radius: 8px; }}
                .alert {{ background: #ef4444; padding: 10px; margin: 5px 0; border-radius: 4px; }}
                .health {{ font-size: 24px; font-weight: bold; }}
                .good {{ color: #10b981; }}
                .warning {{ color: #f59e0b; }}
                .critical {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧠 SHawn-Brain 실시간 모니터링 대시보드</h1>
                <p>업데이트: {data['timestamp']}</p>
                
                <h2>📊 건강도 점수</h2>
                <div class="metric">
                    <div class="health good">{data['health_score']['overall']}/10</div>
                </div>
                
                <h2>⚠️ 활성 알림 ({len(data['alerts'])})</h2>
                {''.join(f'<div class="alert">{a}</div>' for a in data['alerts'])}
                
                <h2>📈 메트릭</h2>
                {''.join(f'<div class="metric"><pre>{m}: {v}</pre></div>' for m, v in data['metrics'].items())}
            </div>
        </body>
        </html>
        """
        
        return html


if __name__ == "__main__":
    print("📊 고급 모니터링 시스템 테스트")
    
    dashboard = RealtimeDashboard()
    
    # 테스트 데이터
    dashboard.collector.record_metric('api_latency', 150)
    dashboard.collector.record_metric('error_rate', 2.5)
    dashboard.collector.record_metric('cache_hit_rate', 85)
    
    # 대시보드 생성
    data = dashboard.generate_dashboard_data()
    print(f"건강도: {data['health_score']['overall']}/10")
