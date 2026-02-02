"""
Adaptive Neural System - 학습된 정책 적용 & 자동 롤백

Q-Learning으로 학습한 최적 정책을 실제로 적용하고, 성능 저하 시 자동으로 롤백합니다.
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum


class PolicyStatus(Enum):
    """정책 상태"""
    BASELINE = "baseline"      # 기준선 (학습 이전)
    LEARNING = "learning"      # 학습 중
    DEPLOYED = "deployed"      # 배포됨 (새 정책)
    STABLE = "stable"          # 안정적
    DEGRADING = "degrading"    # 성능 저하
    ROLLED_BACK = "rolled_back"


@dataclass
class PolicyMetric:
    """정책 성능 메트릭"""
    timestamp: float
    policy_version: str
    status: str
    success_rate: float
    avg_latency: float
    token_efficiency: float
    overall_score: float


class AdaptiveNeuralSystem:
    """적응형 신경계 시스템"""
    
    def __init__(
        self,
        baseline_performance: Dict[str, float],
        degradation_threshold: float = 0.05
    ):
        """
        초기화
        
        Args:
            baseline_performance: 기준 성능 (success_rate, latency, efficiency)
            degradation_threshold: 성능 저하 임계값 (예: 0.05 = 5%)
        """
        self.baseline = baseline_performance
        self.degradation_threshold = degradation_threshold
        
        # 정책 관리
        self.current_policy = None
        self.previous_policy = None
        self.policy_history: List[Dict] = []
        
        # 성능 추적
        self.metrics: List[PolicyMetric] = []
        self.performance_windows: Dict[str, List[float]] = {
            'success_rate': [],
            'latency': [],
            'efficiency': []
        }
        
        # A/B 테스트
        self.ab_test_active = False
        self.ab_test_results: Dict[str, Dict] = {}
    
    def deploy_new_policy(
        self,
        policy_name: str,
        policy: Dict[str, str]
    ) -> bool:
        """
        새 정책 배포
        
        Args:
            policy_name: 정책명 (예: "q_learning_v1")
            policy: 상태→모델 매핑
            
        Returns:
            배포 성공 여부
        """
        self.previous_policy = self.current_policy
        
        self.current_policy = {
            'name': policy_name,
            'policy': policy,
            'deployed_at': datetime.now().isoformat(),
            'status': PolicyStatus.DEPLOYED.value
        }
        
        self.policy_history.append(self.current_policy)
        
        return True
    
    def record_performance(
        self,
        success_rate: float,
        avg_latency: float,
        token_efficiency: float
    ) -> None:
        """
        성능 기록
        
        Args:
            success_rate: 성공률 (0-1)
            avg_latency: 평균 지연시간 (ms)
            token_efficiency: 토큰 효율성 (0-1)
        """
        # 정규화된 점수 계산
        latency_score = max(0, 1.0 - (avg_latency / 5000))  # 5초 기준
        overall_score = (
            success_rate * 0.5 +
            latency_score * 0.25 +
            token_efficiency * 0.25
        )
        
        metric = PolicyMetric(
            timestamp=time.time(),
            policy_version=self.current_policy['name'] if self.current_policy else 'unknown',
            status=self.current_policy['status'] if self.current_policy else 'unknown',
            success_rate=success_rate,
            avg_latency=avg_latency,
            token_efficiency=token_efficiency,
            overall_score=overall_score
        )
        
        self.metrics.append(metric)
        
        # 윈도우 업데이트 (최근 100개 유지)
        self.performance_windows['success_rate'].append(success_rate)
        self.performance_windows['latency'].append(avg_latency)
        self.performance_windows['efficiency'].append(token_efficiency)
        
        for window in self.performance_windows.values():
            if len(window) > 100:
                window.pop(0)
    
    def check_performance_degradation(self) -> Tuple[bool, Dict]:
        """
        성능 저하 확인
        
        Returns:
            (저하 여부, 세부 정보)
        """
        if len(self.metrics) < 10:
            return False, {'reason': 'insufficient_data'}
        
        # 최근 10개 메트릭 평균
        recent = self.metrics[-10:]
        current_perf = {
            'success_rate': sum(m.success_rate for m in recent) / len(recent),
            'latency': sum(m.avg_latency for m in recent) / len(recent),
            'efficiency': sum(m.token_efficiency for m in recent) / len(recent)
        }
        
        # 기준선 대비 저하 확인
        degradation_details = {}
        is_degraded = False
        
        for metric_name, current_value in current_perf.items():
            baseline_value = self.baseline.get(metric_name, 0.85)
            
            if metric_name == 'latency':
                # 레이턴시는 높을수록 나쁨
                degradation = (current_value - baseline_value) / max(baseline_value, 1)
                if degradation > self.degradation_threshold:
                    is_degraded = True
                    degradation_details[metric_name] = {
                        'baseline': baseline_value,
                        'current': current_value,
                        'degradation': degradation
                    }
            else:
                # 성공률, 효율성은 낮을수록 나쁨
                degradation = (baseline_value - current_value) / baseline_value
                if degradation > self.degradation_threshold:
                    is_degraded = True
                    degradation_details[metric_name] = {
                        'baseline': baseline_value,
                        'current': current_value,
                        'degradation': degradation
                    }
        
        return is_degraded, degradation_details
    
    def auto_rollback(self) -> bool:
        """
        성능 저하 시 자동 롤백
        
        Returns:
            롤백 성공 여부
        """
        is_degraded, details = self.check_performance_degradation()
        
        if not is_degraded:
            return False
        
        if not self.previous_policy:
            return False
        
        # 이전 정책으로 롤백
        self.current_policy = self.previous_policy
        self.current_policy['status'] = PolicyStatus.ROLLED_BACK.value
        self.current_policy['rolled_back_at'] = datetime.now().isoformat()
        self.current_policy['rollback_reason'] = details
        
        return True
    
    def start_ab_test(self, policy_a: Dict[str, str], policy_b: Dict[str, str]) -> None:
        """
        A/B 테스트 시작
        
        Args:
            policy_a: 정책 A (현재)
            policy_b: 정책 B (신규)
        """
        self.ab_test_active = True
        self.ab_test_results = {
            'policy_a': {'metrics': [], 'count': 0},
            'policy_b': {'metrics': [], 'count': 0},
            'started_at': datetime.now().isoformat()
        }
    
    def record_ab_test_result(
        self,
        policy: str,
        success: bool,
        latency: float,
        efficiency: float
    ) -> None:
        """
        A/B 테스트 결과 기록
        
        Args:
            policy: 정책 ('A' 또는 'B')
            success: 성공 여부
            latency: 레이턴시
            efficiency: 효율성
        """
        if not self.ab_test_active:
            return
        
        key = f"policy_{policy.lower()}"
        if key not in self.ab_test_results:
            return
        
        self.ab_test_results[key]['metrics'].append({
            'success': success,
            'latency': latency,
            'efficiency': efficiency
        })
        self.ab_test_results[key]['count'] += 1
    
    def analyze_ab_test(self) -> Dict:
        """
        A/B 테스트 분석
        
        Returns:
            분석 결과
        """
        if not self.ab_test_results:
            return {'status': 'no_test'}
        
        def calculate_stats(metrics):
            if not metrics:
                return None
            
            successes = sum(1 for m in metrics if m['success'])
            success_rate = successes / len(metrics)
            avg_latency = sum(m['latency'] for m in metrics) / len(metrics)
            avg_efficiency = sum(m['efficiency'] for m in metrics) / len(metrics)
            
            return {
                'count': len(metrics),
                'success_rate': success_rate,
                'avg_latency': avg_latency,
                'avg_efficiency': avg_efficiency
            }
        
        stats_a = calculate_stats(self.ab_test_results['policy_a'].get('metrics', []))
        stats_b = calculate_stats(self.ab_test_results['policy_b'].get('metrics', []))
        
        result = {
            'policy_a': stats_a,
            'policy_b': stats_b,
            'recommendation': 'insufficient_data'
        }
        
        # 통계적 유의성 확인 (간단한 버전)
        if stats_a and stats_b and stats_a['count'] >= 30 and stats_b['count'] >= 30:
            # 성공률 비교
            if stats_b['success_rate'] > stats_a['success_rate'] * 1.1:  # 10% 이상 개선
                result['recommendation'] = 'deploy_b'
            elif stats_a['success_rate'] > stats_b['success_rate'] * 1.1:
                result['recommendation'] = 'keep_a'
            else:
                result['recommendation'] = 'equivalent'
        
        return result
    
    def get_system_status(self) -> Dict:
        """시스템 상태 조회"""
        is_degraded, degradation = self.check_performance_degradation()
        
        return {
            'current_policy': self.current_policy['name'] if self.current_policy else None,
            'policy_status': self.current_policy['status'] if self.current_policy else None,
            'is_degraded': is_degraded,
            'degradation_details': degradation,
            'metrics_count': len(self.metrics),
            'ab_test_active': self.ab_test_active,
            'last_metric': asdict(self.metrics[-1]) if self.metrics else None
        }
    
    def export_system_report(self, filename: str) -> None:
        """시스템 리포트 내보내기"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'baseline_performance': self.baseline,
            'current_policy': self.current_policy,
            'system_status': self.get_system_status(),
            'metrics_summary': {
                'total_metrics': len(self.metrics),
                'recent_10': [asdict(m) for m in self.metrics[-10:]]
            },
            'policy_history': self.policy_history,
            'ab_test_results': self.ab_test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def generate_deployment_report(self) -> str:
        """배포 리포트 생성 (Markdown)"""
        report = []
        
        report.append("# 신경계 적응형 시스템 배포 리포트")
        report.append("")
        
        # 현재 상태
        status = self.get_system_status()
        report.append("## 현재 상태")
        report.append(f"- 정책: {status.get('current_policy', 'N/A')}")
        report.append(f"- 상태: {status.get('policy_status', 'N/A')}")
        report.append(f"- 성능 저하: {'예' if status.get('is_degraded') else '아니오'}")
        report.append("")
        
        # 성능 저하 세부사항
        if status.get('is_degraded'):
            report.append("## 성능 저하 세부사항")
            for metric, details in status.get('degradation_details', {}).items():
                report.append(f"- {metric}")
                report.append(f"  - 기준선: {details.get('baseline'):.4f}")
                report.append(f"  - 현재: {details.get('current'):.4f}")
                report.append(f"  - 저하도: {details.get('degradation'):.2%}")
            report.append("")
        
        # 메트릭 요약
        report.append("## 메트릭 요약")
        if self.metrics:
            last = status.get('last_metric', {})
            report.append(f"- 성공률: {last.get('success_rate', 0):.2%}")
            report.append(f"- 평균 레이턴시: {last.get('avg_latency', 0):.2f}ms")
            report.append(f"- 토큰 효율성: {last.get('token_efficiency', 0):.2%}")
            report.append(f"- 종합 점수: {last.get('overall_score', 0):.4f}")
        report.append("")
        
        # A/B 테스트
        if self.ab_test_active:
            report.append("## A/B 테스트 진행 중")
            ab_analysis = self.analyze_ab_test()
            report.append(f"- 권장사항: {ab_analysis.get('recommendation')}")
        
        return "\n".join(report)


# 테스트 코드
if __name__ == "__main__":
    baseline = {
        'success_rate': 0.85,
        'latency': 2000,
        'efficiency': 0.8
    }
    
    system = AdaptiveNeuralSystem(baseline)
    
    # 정책 배포
    policy = {f"state_{i}": f"model_{i%8}" for i in range(32)}
    system.deploy_new_policy("q_learning_v1", policy)
    
    # 성능 기록
    for i in range(50):
        import random
        success_rate = 0.82 + random.gauss(0, 0.02)
        latency = 1800 + random.gauss(0, 200)
        efficiency = 0.79 + random.gauss(0, 0.02)
        
        system.record_performance(success_rate, latency, efficiency)
    
    # 리포트
    print(system.generate_deployment_report())
    
    # 상태
    print("\n=== 시스템 상태 ===")
    import json
    print(json.dumps(system.get_system_status(), indent=2, default=str))
