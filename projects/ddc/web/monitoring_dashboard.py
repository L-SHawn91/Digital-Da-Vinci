"""
모니터링 대시보드 - SHawn-Brain 신경계 모니터링

역할:
- 신경계 4계층 실시간 모니터링
- 카트리지 성능 추적
- API 사용량 분석
- DCRS (Daily Cerebellar Recalibration) 시각화
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import json


class MonitoringDashboard:
    """신경계 모니터링 대시보드"""
    
    def __init__(self):
        """초기화"""
        self.start_time = datetime.now()
        self.neural_logs = {
            'L1_Brainstem': [],
            'L2_Limbic': [],
            'L3_Neocortex': [],
            'L4_NeuroNet': []
        }
        self.cartridge_metrics = {
            'bio': {'calls': 0, 'avg_time': 0, 'errors': 0},
            'inv': {'calls': 0, 'avg_time': 0, 'errors': 0},
            'lit': {'calls': 0, 'avg_time': 0, 'errors': 0},
            'quant': {'calls': 0, 'avg_time': 0, 'errors': 0},
            'astro': {'calls': 0, 'avg_time': 0, 'errors': 0}
        }
        self.api_metrics = []
    
    def record_neural_activity(
        self,
        level: str,
        health: float,
        latency: float,
        throughput: int
    ) -> None:
        """신경 활동 기록"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'health': health,
            'latency': latency,
            'throughput': throughput
        }
        self.neural_logs[level].append(log_entry)
    
    def record_cartridge_call(
        self,
        cartridge: str,
        duration: float,
        success: bool
    ) -> None:
        """카트리지 호출 기록"""
        metrics = self.cartridge_metrics[cartridge]
        metrics['calls'] += 1
        if not success:
            metrics['errors'] += 1
        
        # 평균 시간 업데이트
        old_avg = metrics['avg_time']
        metrics['avg_time'] = (old_avg * (metrics['calls'] - 1) + duration) / metrics['calls']
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """대시보드 데이터 생성"""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime': (datetime.now() - self.start_time).total_seconds(),
            'neural_system': self._get_neural_summary(),
            'cartridges': self._get_cartridge_summary(),
            'performance': self._get_performance_metrics(),
            'alerts': self._check_alerts()
        }
    
    def _get_neural_summary(self) -> Dict[str, Any]:
        """신경계 요약"""
        summary = {}
        for level, logs in self.neural_logs.items():
            if logs:
                latest = logs[-1]
                summary[level] = {
                    'health': latest['health'],
                    'latency': latest['latency'],
                    'status': '🟢' if latest['health'] > 0.8 else '🟡' if latest['health'] > 0.6 else '🔴'
                }
        return summary
    
    def _get_cartridge_summary(self) -> Dict[str, Any]:
        """카트리지 요약"""
        summary = {}
        for cartridge, metrics in self.cartridge_metrics.items():
            if metrics['calls'] > 0:
                error_rate = (metrics['errors'] / metrics['calls']) * 100
                summary[cartridge] = {
                    'calls': metrics['calls'],
                    'avg_time_ms': round(metrics['avg_time'] * 1000, 2),
                    'error_rate': round(error_rate, 2),
                    'status': '🟢' if error_rate < 5 else '🟡' if error_rate < 10 else '🔴'
                }
        return summary
    
    def _get_performance_metrics(self) -> Dict[str, float]:
        """성능 메트릭"""
        total_calls = sum(m['calls'] for m in self.cartridge_metrics.values())
        total_errors = sum(m['errors'] for m in self.cartridge_metrics.values())
        
        return {
            'total_api_calls': total_calls,
            'total_errors': total_errors,
            'success_rate': ((total_calls - total_errors) / total_calls * 100) if total_calls > 0 else 100,
            'avg_latency_ms': sum(
                m.get('latency', 0) for logs in self.neural_logs.values() 
                for m in logs
            ) / sum(len(logs) for logs in self.neural_logs.values()) if sum(len(logs) for logs in self.neural_logs.values()) > 0 else 0
        }
    
    def _check_alerts(self) -> List[Dict[str, str]]:
        """알림 확인"""
        alerts = []
        
        # 신경계 건강도 알림
        for level, logs in self.neural_logs.items():
            if logs and logs[-1]['health'] < 0.7:
                alerts.append({
                    'type': 'neural_health',
                    'level': level,
                    'message': f'{level} 건강도 경고'
                })
        
        # 카트리지 에러율 알림
        for cartridge, metrics in self.cartridge_metrics.items():
            if metrics['calls'] > 0:
                error_rate = (metrics['errors'] / metrics['calls']) * 100
                if error_rate > 10:
                    alerts.append({
                        'type': 'error_rate',
                        'cartridge': cartridge,
                        'message': f'{cartridge} 에러율 {error_rate:.1f}%'
                    })
        
        return alerts
    
    def generate_report(self) -> str:
        """모니터링 리포트 생성"""
        data = self.get_dashboard_data()
        
        report = f"""
╔═══════════════════════════════════════════════╗
║     SHawn-Brain 모니터링 대시보드 리포트          ║
╚═══════════════════════════════════════════════╝

📊 시스템 상태
  가동 시간: {data['uptime']:.1f}초
  타임스탬프: {data['timestamp']}

🧠 신경계 상태
"""
        for level, status in data['neural_system'].items():
            report += f"  {level}: {status['status']} (건강도: {status['health']:.1%}, 지연: {status['latency']:.1f}ms)\n"
        
        report += "\n📦 카트리지 성능\n"
        for cartridge, metrics in data['cartridges'].items():
            report += f"  {cartridge}: {metrics['status']} (호출: {metrics['calls']}, 에러율: {metrics['error_rate']:.1f}%)\n"
        
        report += f"\n📈 전체 성능\n"
        report += f"  총 API 호출: {data['performance']['total_api_calls']}\n"
        report += f"  총 에러: {data['performance']['total_errors']}\n"
        report += f"  성공률: {data['performance']['success_rate']:.1f}%\n"
        
        if data['alerts']:
            report += f"\n⚠️ 활성 알림 ({len(data['alerts'])}개)\n"
            for alert in data['alerts']:
                report += f"  - {alert['message']}\n"
        
        return report


# 전역 모니터링 인스턴스
monitor = MonitoringDashboard()


def log_neural_activity(level: str, health: float, latency: float = 0, throughput: int = 0):
    """신경 활동 로깅 (편의 함수)"""
    monitor.record_neural_activity(level, health, latency, throughput)


def log_cartridge_call(cartridge: str, duration: float, success: bool = True):
    """카트리지 호출 로깅 (편의 함수)"""
    monitor.record_cartridge_call(cartridge, duration, success)


def get_monitoring_report() -> str:
    """모니터링 리포트 조회"""
    return monitor.generate_report()


if __name__ == "__main__":
    print("🔍 모니터링 대시보드 테스트")
    
    # 테스트 데이터 생성
    monitor.record_neural_activity('L1_Brainstem', 0.95, 5.2, 1000)
    monitor.record_neural_activity('L2_Limbic', 0.93, 3.1, 900)
    monitor.record_neural_activity('L3_Neocortex', 0.94, 2.8, 950)
    monitor.record_neural_activity('L4_NeuroNet', 0.98, 0.1, 1200)
    
    monitor.record_cartridge_call('bio', 0.45, True)
    monitor.record_cartridge_call('inv', 0.38, True)
    monitor.record_cartridge_call('bio', 0.42, True)
    
    # 리포트 출력
    print(get_monitoring_report())
