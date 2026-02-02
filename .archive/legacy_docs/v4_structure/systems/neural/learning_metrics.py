"""
Learning Metrics - Q-Learning 수렴 속도 및 효율성 메트릭

학습 진행도를 추적하고 수렴 속도를 측정합니다.
"""

import json
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ConvergenceMetric:
    """수렴 메트릭"""
    episode: int
    q_mean: float
    q_std: float
    q_change: float
    epsilon: float
    exploration_rate: float
    timestamp: float


class LearningMetrics:
    """학습 메트릭 추적기"""
    
    def __init__(self, window_size: int = 50):
        """
        초기화
        
        Args:
            window_size: 윈도우 크기
        """
        self.window_size = window_size
        self.convergence_metrics: List[ConvergenceMetric] = []
        self.episode_rewards: List[float] = []
        self.episode_q_values: List[float] = []
    
    def record_convergence(
        self,
        episode: int,
        q_table: Dict,
        epsilon: float,
        last_q_change: float
    ) -> None:
        """
        수렴 메트릭 기록
        
        Args:
            episode: 현재 에피소드
            q_table: Q-테이블
            epsilon: 현재 ε값
            last_q_change: 마지막 Q값 변화
        """
        # Q값 통계 계산
        all_q_values = []
        for state_q in q_table.values():
            all_q_values.extend(state_q.values())
        
        q_mean = float(np.mean(all_q_values)) if all_q_values else 0.0
        q_std = float(np.std(all_q_values)) if all_q_values else 0.0
        
        # 탐색률 계산 (ε 역수)
        exploration_rate = 1.0 - epsilon
        
        metric = ConvergenceMetric(
            episode=episode,
            q_mean=q_mean,
            q_std=q_std,
            q_change=last_q_change,
            epsilon=epsilon,
            exploration_rate=exploration_rate,
            timestamp=datetime.now().timestamp()
        )
        
        self.convergence_metrics.append(metric)
    
    def record_episode_reward(self, reward: float, q_value: float) -> None:
        """에피소드 보상 기록"""
        self.episode_rewards.append(reward)
        self.episode_q_values.append(q_value)
    
    def get_convergence_status(self) -> Dict:
        """수렴 상태 조회"""
        if not self.convergence_metrics:
            return {}
        
        recent = self.convergence_metrics[-1]
        
        # 수렴 기준: Q값 변화 < 0.01
        converged = recent.q_change < 0.01
        
        return {
            'episode': recent.episode,
            'q_mean': f"{recent.q_mean:.4f}",
            'q_std': f"{recent.q_std:.4f}",
            'q_change': f"{recent.q_change:.6f}",
            'epsilon': f"{recent.epsilon:.4f}",
            'exploration_rate': f"{recent.exploration_rate:.1%}",
            'converged': converged,
            'convergence_progress': self._calculate_convergence_progress()
        }
    
    def _calculate_convergence_progress(self) -> str:
        """수렴 진행도 계산"""
        if len(self.convergence_metrics) < 2:
            return "0%"
        
        # 초기 vs 최근 Q값 변화 비교
        initial_change = abs(
            self.convergence_metrics[0].q_mean - 
            self.convergence_metrics[1].q_mean
        )
        
        recent_change = self.convergence_metrics[-1].q_change
        
        if initial_change == 0:
            progress = 0.0
        else:
            progress = min(1.0, 1.0 - (recent_change / max(initial_change, 0.01)))
        
        return f"{progress*100:.1f}%"
    
    def get_reward_statistics(self) -> Dict:
        """보상 통계"""
        if not self.episode_rewards:
            return {}
        
        rewards = np.array(self.episode_rewards)
        
        return {
            'total_episodes': len(self.episode_rewards),
            'mean_reward': f"{np.mean(rewards):.4f}",
            'std_reward': f"{np.std(rewards):.4f}",
            'min_reward': f"{np.min(rewards):.4f}",
            'max_reward': f"{np.max(rewards):.4f}",
            'cumulative_reward': f"{np.sum(rewards):.2f}"
        }
    
    def get_q_learning_efficiency(self) -> Dict:
        """Q-Learning 효율성"""
        if len(self.convergence_metrics) < 2:
            return {}
        
        metrics = self.convergence_metrics
        
        # 초기 대비 현재 Q값 개선
        initial_q_mean = metrics[0].q_mean
        current_q_mean = metrics[-1].q_mean
        
        # 에피소드당 Q값 증가율
        episodes_per_10 = (metrics[-1].episode - metrics[0].episode) / 10
        
        return {
            'initial_q_mean': f"{initial_q_mean:.4f}",
            'current_q_mean': f"{current_q_mean:.4f}",
            'improvement': f"{current_q_mean - initial_q_mean:.4f}",
            'improvement_percent': f"{((current_q_mean - initial_q_mean) / max(abs(initial_q_mean), 0.01)) * 100:.1f}%",
            'convergence_speed': self._estimate_convergence_speed(),
            'estimated_episodes_to_convergence': self._estimate_episodes_to_convergence()
        }
    
    def _estimate_convergence_speed(self) -> str:
        """수렴 속도 추정"""
        if len(self.convergence_metrics) < 10:
            return "Insufficient data"
        
        recent_10 = self.convergence_metrics[-10:]
        q_changes = [m.q_change for m in recent_10]
        
        # 로그 스케일로 감소율 계산
        if q_changes[0] > 0:
            decay_rate = 1.0 - (q_changes[-1] / q_changes[0])
            
            if decay_rate < 0.1:
                return "Slow"
            elif decay_rate < 0.3:
                return "Moderate"
            else:
                return "Fast"
        
        return "Unknown"
    
    def _estimate_episodes_to_convergence(self) -> str:
        """수렴까지 예상 에피소드"""
        if len(self.convergence_metrics) < 2:
            return "Unknown"
        
        recent = self.convergence_metrics[-1]
        
        # 수렴됨
        if recent.q_change < 0.01:
            return "Converged"
        
        # 선형 외삽
        if len(self.convergence_metrics) >= 10:
            recent_10 = self.convergence_metrics[-10:]
            episodes_elapsed = recent_10[-1].episode - recent_10[0].episode
            q_change_reduction = recent_10[0].q_change - recent_10[-1].q_change
            
            if q_change_reduction > 0:
                episodes_needed = (
                    (recent.q_change - 0.01) / 
                    (q_change_reduction / episodes_elapsed)
                )
                return f"{int(max(1, episodes_needed))} episodes"
        
        return "Unknown"
    
    def analyze_learning_curve(self) -> Dict:
        """학습 곡선 분석"""
        if len(self.convergence_metrics) < 3:
            return {'status': 'Insufficient data'}
        
        # 구간별 분석
        total = len(self.convergence_metrics)
        seg1 = self.convergence_metrics[:total//3]
        seg2 = self.convergence_metrics[total//3:2*total//3]
        seg3 = self.convergence_metrics[2*total//3:]
        
        def segment_stats(segment):
            q_changes = [m.q_change for m in segment]
            return {
                'avg_q_change': f"{np.mean(q_changes):.6f}",
                'episodes': len(segment)
            }
        
        return {
            'phase_1_early': segment_stats(seg1),
            'phase_2_middle': segment_stats(seg2),
            'phase_3_late': segment_stats(seg3),
            'overall_trend': self._analyze_trend()
        }
    
    def _analyze_trend(self) -> str:
        """전체 추세 분석"""
        if len(self.convergence_metrics) < 5:
            return "Insufficient data"
        
        recent_5 = self.convergence_metrics[-5:]
        earlier_5 = self.convergence_metrics[-10:-5]
        
        if len(earlier_5) < 5:
            return "Insufficient data"
        
        recent_avg = np.mean([m.q_change for m in recent_5])
        earlier_avg = np.mean([m.q_change for m in earlier_5])
        
        improvement = earlier_avg - recent_avg
        
        if improvement > 0.01:
            return "Converging (Good)"
        elif improvement > 0:
            return "Slowly converging"
        else:
            return "Diverging (Warning)"
    
    def export_metrics(self, filename: str) -> None:
        """메트릭 내보내기"""
        data = {
            'exported_at': datetime.now().isoformat(),
            'convergence_status': self.get_convergence_status(),
            'reward_statistics': self.get_reward_statistics(),
            'learning_efficiency': self.get_q_learning_efficiency(),
            'learning_curve': self.analyze_learning_curve(),
            'metrics_history': [asdict(m) for m in self.convergence_metrics],
            'total_episodes': len(self.convergence_metrics)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def generate_report(self) -> str:
        """학습 리포트 생성 (Markdown)"""
        report = []
        
        report.append("# Q-Learning 학습 리포트")
        report.append("")
        
        # 수렴 상태
        convergence = self.get_convergence_status()
        report.append("## 수렴 상태")
        report.append(f"- 에피소드: {convergence.get('episode', 'N/A')}")
        report.append(f"- Q값 평균: {convergence.get('q_mean', 'N/A')}")
        report.append(f"- Q값 표준편차: {convergence.get('q_std', 'N/A')}")
        report.append(f"- Q값 변화: {convergence.get('q_change', 'N/A')}")
        report.append(f"- 수렴: {convergence.get('converged', False)}")
        report.append("")
        
        # 보상 통계
        rewards = self.get_reward_statistics()
        report.append("## 보상 통계")
        for key, value in rewards.items():
            report.append(f"- {key}: {value}")
        report.append("")
        
        # 학습 효율성
        efficiency = self.get_q_learning_efficiency()
        report.append("## 학습 효율성")
        for key, value in efficiency.items():
            report.append(f"- {key}: {value}")
        report.append("")
        
        # 학습 곡선
        curve = self.analyze_learning_curve()
        report.append("## 학습 곡선")
        report.append(f"- 전체 추세: {curve.get('overall_trend', 'N/A')}")
        report.append("")
        
        return "\n".join(report)


# 테스트 코드
if __name__ == "__main__":
    metrics = LearningMetrics()
    
    # 시뮬레이션
    import numpy as np
    
    q_table = {f"state_{i}": {f"model_{j}": 0.0 for j in range(8)} 
              for i in range(32)}
    
    for episode in range(100):
        # Q값 시뮬레이션 (수렴으로 향함)
        for state_q in q_table.values():
            for model in state_q:
                state_q[model] += np.random.normal(0.01, 0.005)
        
        epsilon = 0.1 * (0.995 ** episode)
        q_change = np.random.exponential(0.1 / (1 + episode * 0.01))
        
        metrics.record_convergence(episode, q_table, epsilon, q_change)
        metrics.record_episode_reward(np.random.normal(0, 0.3), q_change)
    
    # 리포트 출력
    print(metrics.generate_report())
