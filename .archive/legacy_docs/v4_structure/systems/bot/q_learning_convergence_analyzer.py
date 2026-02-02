#!/usr/bin/env python3
"""
q_learning_convergence_analyzer.py - Q-Learning 수렴 분석 (순수 Python)

Week 2 Step 1: Q-Table 수렴 추적 및 분석

역할:
  ├─ Q 값 변화율 모니터링
  ├─ 최적 정책 안정성 확인
  ├─ 탐험 vs 활용 비율 분석
  ├─ 국소 최적값 감지
  └─ 학습 곡선 시각화
"""

import json
import statistics
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class QLearningConvergenceAnalyzer:
    """Q-Learning 수렴 분석"""
    
    def __init__(self, q_table_path: str = "systems/bot/watchdog_q_table.json"):
        self.q_table_path = Path(q_table_path)
        self.current_q_table: Dict = {}
        self.load_q_table()
    
    def load_q_table(self) -> None:
        """현재 Q-Table 로드"""
        if self.q_table_path.exists():
            with open(self.q_table_path, 'r') as f:
                data = json.load(f)
                # q_values 또는 q_table에서 데이터 추출
                self.current_q_table = data.get('q_values', data.get('q_table', {}))
            print(f"✅ Q-Table 로드: {self.q_table_path}")
            print(f"   상태-액션 쌍: {len(self.current_q_table)}")
        else:
            print(f"❌ Q-Table 없음: {self.q_table_path}")
            print("   시뮬레이션 데이터로 진행합니다")
            self._create_sample_q_table()
    
    def _create_sample_q_table(self) -> None:
        """샘플 Q-Table 생성"""
        self.current_q_table = {
            "running_restart_immediately": 8.5,
            "running_check_dependencies": 7.2,
            "down_restart_immediately": 15.0,
            "down_wait_and_retry": 12.5,
            "down_restart_clean": 14.0,
            "sleeping_check_dependencies": 9.5,
            "error_escalate_manual": 6.0,
            "error_restart_clean": 11.0,
        }
    
    def analyze_convergence(self) -> Dict:
        """수렴 분석"""
        
        print("\n" + "="*80)
        print("📊 Q-Learning 수렴 분석")
        print("="*80)
        
        if not self.current_q_table:
            return {"error": "Q-Table이 없습니다"}
        
        # Q 값 추출
        q_values = [
            v for v in self.current_q_table.values() 
            if isinstance(v, (int, float))
        ]
        
        if not q_values:
            print("❌ Q 값이 없습니다")
            return {"error": "Q 값이 없습니다"}
        
        # 기본 통계
        avg_q = statistics.mean(q_values)
        std_q = statistics.stdev(q_values) if len(q_values) > 1 else 0
        max_q = max(q_values)
        min_q = min(q_values)
        
        print(f"""
🎯 Q 값 통계:
   • 평균: {avg_q:.2f}
   • 표준편차: {std_q:.2f}
   • 최댓값: {max_q:.2f}
   • 최솟값: {min_q:.2f}
   • 범위: {max_q - min_q:.2f}
   • 총 상태-액션 쌍: {len(q_values)}
""")
        
        # 수렴 지표
        convergence_indicators = self._calculate_convergence_indicators(q_values)
        
        print(f"""
📈 수렴 지표:
   • Q 값 분포 정규성: {convergence_indicators['normality']:.1%}
   • 최적값 집중도: {convergence_indicators['concentration']:.1%}
   • 다양성 점수: {convergence_indicators['diversity']:.2f}/10.0
   • 수렴 추정 진행도: {convergence_indicators['convergence_progress']:.1%}
""")
        
        return convergence_indicators
    
    def _calculate_convergence_indicators(self, q_values: List[float]) -> Dict:
        """수렴 지표 계산"""
        
        # 1. 정규성 (중앙값 주변 값의 집중도)
        median_q = statistics.median(q_values)
        std_q = statistics.stdev(q_values) if len(q_values) > 1 else 1
        q_near_median = sum(1 for q in q_values if abs(q - median_q) < std_q)
        normality = q_near_median / len(q_values) if q_values else 0
        
        # 2. 최적값 집중도 (상위 25% 값의 비율)
        sorted_q = sorted(q_values)
        threshold = sorted_q[int(len(q_values) * 0.75)]
        concentration = sum(1 for q in q_values if q >= threshold) / len(q_values)
        
        # 3. 다양성 점수 (낮을수록 수렴)
        diversity = min(10.0, std_q / (abs(statistics.mean(q_values)) or 1) * 5)
        
        # 4. 수렴 진행도
        avg_q = statistics.mean(q_values)
        max_q = max(q_values)
        convergence_progress = 1 - (max_q - avg_q) / (max_q or 1)
        
        return {
            'normality': max(0, normality),
            'concentration': max(0, concentration),
            'diversity': max(0, diversity),
            'convergence_progress': max(0, convergence_progress)
        }
    
    def detect_local_optima(self, threshold: float = 0.95) -> Dict:
        """국소 최적값 감지"""
        
        print("\n" + "="*80)
        print("🎯 국소 최적값 감지")
        print("="*80)
        
        if not self.current_q_table:
            return {"error": "Q-Table이 없습니다"}
        
        # 상태별로 Q 값 그룹화
        state_groups = self._group_by_state()
        
        local_optima_detected = False
        recommendations = []
        
        for state, q_values in state_groups.items():
            if not q_values:
                continue
            
            max_q = max(q_values.values())
            min_q = min(q_values.values())
            avg_q = statistics.mean(q_values.values())
            
            # 최댓값과 다른 값들의 차이
            gap = max_q - avg_q
            gap_ratio = gap / (abs(avg_q) or 1)
            
            if gap_ratio > threshold:
                local_optima_detected = True
                best_action = max(q_values, key=q_values.get)
                
                print(f"\n⚠️ 상태 '{state}'에서 가능한 국소 최적값:")
                print(f"   • 최적 액션: {best_action} (Q={max_q:.2f})")
                print(f"   • 갭 비율: {gap_ratio:.1%}")
                print(f"   • 액션 다양성: {len(q_values)}")
                
                if gap_ratio > threshold * 1.2:
                    recommendations.append({
                        'state': state,
                        'issue': '국소 최적값에 갇혔을 가능성',
                        'action': '탐험률(ε) 증가 권장',
                        'suggested_epsilon': 0.20
                    })
        
        if not local_optima_detected:
            print("✅ 국소 최적값 감지 안 됨 (좋은 신호!)")
        
        return {
            'local_optima_detected': local_optima_detected,
            'recommendations': recommendations
        }
    
    def _group_by_state(self) -> Dict[str, Dict]:
        """상태별로 Q 값 그룹화"""
        
        state_groups = {}
        
        for state_action, q_value in self.current_q_table.items():
            if isinstance(state_action, str) and '_' in state_action:
                parts = state_action.rsplit('_', 1)
                if len(parts) == 2:
                    state = parts[0]
                    action = parts[1]
                    
                    if state not in state_groups:
                        state_groups[state] = {}
                    
                    if isinstance(q_value, (int, float)):
                        state_groups[state][action] = q_value
        
        return state_groups
    
    def optimize_exploration_rate(self) -> Dict:
        """탐험률(ε) 최적화 제안"""
        
        print("\n" + "="*80)
        print("🎯 탐험률(ε) 최적화")
        print("="*80)
        
        convergence = self.analyze_convergence()
        
        if 'convergence_progress' not in convergence:
            return {"error": "수렴 분석 실패"}
        
        progress = convergence['convergence_progress']
        diversity = convergence['diversity']
        
        print(f"""
현재 상태:
   • 수렴 진행도: {progress:.1%}
   • 다양성: {diversity:.2f}/10.0
""")
        
        # ε 최적화 추천
        if progress > 0.9:
            recommendation = 0.10
            reason = "수렴했지만 다양성 유지 필요"
        elif progress > 0.7:
            recommendation = 0.15
            reason = "적당히 수렴, 현재 수준 유지"
        else:
            recommendation = 0.15
            reason = "적절한 탐험 수준"
        
        print(f"""
📊 ε (탐험률) 최적화:
   • 권장값: {recommendation:.2f}
   • 이유: {reason}
   
   탐험 vs 활용:
   • 탐험 (새로운 액션): {recommendation:.1%}
   • 활용 (최고 Q 값): {1-recommendation:.1%}
""")
        
        return {
            'recommended_epsilon': recommendation,
            'reason': reason,
            'convergence_progress': progress,
            'diversity_score': diversity
        }
    
    def generate_report(self) -> Dict:
        """최종 리포트 생성"""
        
        print("\n" + "="*80)
        print("📋 최종 수렴 분석 리포트")
        print("="*80)
        
        convergence = self.analyze_convergence()
        local_optima = self.detect_local_optima()
        epsilon_optimization = self.optimize_exploration_rate()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'convergence': convergence,
            'local_optima': local_optima,
            'epsilon_optimization': epsilon_optimization,
            'summary': self._generate_summary(convergence, local_optima, epsilon_optimization)
        }
        
        # 리포트 저장
        report_path = Path("logs/neural_efficiency/q_convergence_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ 리포트 저장: {report_path}")
        
        return report
    
    def _generate_summary(self, convergence: Dict, local_optima: Dict, epsilon: Dict) -> Dict:
        """요약 생성"""
        
        progress = convergence.get('convergence_progress', 0)
        
        # 수렴 상태
        if progress > 0.95:
            convergence_status = "🟢 거의 완전히 수렴"
        elif progress > 0.8:
            convergence_status = "🟡 수렴 중"
        elif progress > 0.5:
            convergence_status = "🟠 탐험 중 (정상)"
        else:
            convergence_status = "🔴 초기 탐험 중"
        
        # 건강도 평가
        concentration = convergence.get('concentration', 0)
        
        if concentration > 0.8 and progress > 0.9:
            health_score = 9.5
            health_status = "⭐⭐⭐⭐⭐ 매우 양호"
        elif concentration > 0.6 and progress > 0.7:
            health_score = 8.0
            health_status = "⭐⭐⭐⭐ 양호"
        elif progress > 0.5:
            health_score = 6.0
            health_status = "⭐⭐⭐ 보통"
        else:
            health_score = 4.0
            health_status = "⭐⭐ 개선 필요"
        
        return {
            'convergence_status': convergence_status,
            'health_score': health_score,
            'health_status': health_status,
            'recommendation': '계속 모니터링' if health_score > 7 else '파라미터 조정 필요'
        }


def main():
    """메인 실행"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║  📊 Q-Learning 수렴 분석                                                    ║
║     Week 2 Step 1: 신경학습 안정성 확인                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    analyzer = QLearningConvergenceAnalyzer()
    report = analyzer.generate_report()
    
    # 최종 요약
    summary = report['summary']
    
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ 최종 평가
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 수렴 상태: {summary['convergence_status']}
⚡ 건강도: {summary['health_status']} ({summary['health_score']:.1f}/10.0)
📝 권장사항: {summary['recommendation']}

상세 리포트: logs/neural_efficiency/q_convergence_report.json
""")


if __name__ == "__main__":
    main()
