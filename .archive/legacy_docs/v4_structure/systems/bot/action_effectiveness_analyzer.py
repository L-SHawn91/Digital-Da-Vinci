#!/usr/bin/env python3
"""
action_effectiveness_analyzer.py - 행동(액션) 효율성 분석

Week 2 Step 2: 각 액션별 성공률 분석 및 최적화 추천

역할:
  ├─ 각 액션(Action)별 성공률 계산
  ├─ 상태별 최적 액션 파악
  ├─ 비효율적 액션 감지 (< 30% 성공률)
  ├─ 액션 조합 최적화
  └─ 성능 개선 추천

5가지 액션:
  1. RESTART_IMMEDIATELY: 즉시 재시작 (빠르지만 위험)
  2. CHECK_DEPENDENCIES_FIRST: 의존성 확인 후 재시작 (느리지만 안전)
  3. WAIT_AND_RETRY: 대기 후 재시도 (가장 느림, 최후 수단)
  4. ESCALATE_TO_MANUAL: 수동 개입 (사람이 할 때까지 대기)
  5. RESTART_WITH_CLEAN_ENV: 환경 초기화 후 재시작 (가장 안전)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import statistics


class ActionEffectivenessAnalyzer:
    """액션 효율성 분석"""
    
    def __init__(self, q_table_path: str = "systems/bot/watchdog_q_table.json"):
        self.q_table_path = Path(q_table_path)
        self.q_values: Dict[str, float] = {}
        self.state_action_map: Dict[str, List[str]] = {}
        self.load_q_table()
        self._build_state_action_map()
    
    def load_q_table(self) -> None:
        """Q-Table 로드"""
        if self.q_table_path.exists():
            with open(self.q_table_path, 'r') as f:
                data = json.load(f)
                self.q_values = data.get('q_values', {})
            print(f"✅ Q-Table 로드: {len(self.q_values)}개 항목")
        else:
            print(f"❌ Q-Table 없음")
            self._create_sample_data()
    
    def _create_sample_data(self) -> None:
        """샘플 데이터 생성"""
        self.q_values = {
            "running_restart_immediately": 8.5,
            "running_check_dependencies": 7.2,
            "running_wait_and_retry": 6.8,
            "down_restart_immediately": 15.0,
            "down_check_dependencies": 13.5,
            "down_wait_and_retry": 12.5,
            "down_escalate_manual": 5.0,
            "down_restart_clean": 14.0,
            "sleeping_check_dependencies": 9.5,
            "sleeping_wait_and_retry": 8.0,
            "error_escalate_manual": 6.0,
            "error_restart_clean": 11.0,
            "zombie_restart_clean": 13.5,
            "zombie_escalate_manual": 4.5,
        }
    
    def _build_state_action_map(self) -> None:
        """상태-액션 맵 구축"""
        for state_action, q_value in self.q_values.items():
            if '_' in state_action:
                parts = state_action.rsplit('_', 1)
                if len(parts) == 2:
                    state = parts[0]
                    action = parts[1]
                    
                    if state not in self.state_action_map:
                        self.state_action_map[state] = []
                    
                    self.state_action_map[state].append(action)
    
    def analyze_action_effectiveness(self) -> Dict:
        """각 액션의 효율성 분석"""
        
        print("\n" + "="*80)
        print("📊 액션 효율성 분석")
        print("="*80)
        
        action_stats = self._calculate_action_statistics()
        
        print(f"""
🎯 각 액션별 Q 값 통계:
""")
        
        # 액션별 통계 출력
        sorted_actions = sorted(
            action_stats.items(),
            key=lambda x: x[1]['avg_q'],
            reverse=True
        )
        
        for action, stats in sorted_actions:
            print(f"""
   {action}:
      • 평균 Q 값: {stats['avg_q']:.2f}
      • 최댓값: {stats['max_q']:.2f}
      • 최솟값: {stats['min_q']:.2f}
      • 사용 횟수: {stats['count']}
      • 평균 성공률 추정: {stats['estimated_success_rate']:.1%}
""")
        
        return action_stats
    
    def _calculate_action_statistics(self) -> Dict[str, Dict]:
        """액션별 통계 계산"""
        
        actions = {}
        
        for state_action, q_value in self.q_values.items():
            if '_' in state_action:
                parts = state_action.rsplit('_', 1)
                if len(parts) == 2:
                    action = parts[1]
                    
                    if action not in actions:
                        actions[action] = {
                            'q_values': [],
                            'count': 0,
                            'states': set()
                        }
                    
                    actions[action]['q_values'].append(q_value)
                    actions[action]['count'] += 1
                    actions[action]['states'].add(parts[0])
        
        # 통계 계산
        result = {}
        for action, data in actions.items():
            q_vals = data['q_values']
            avg_q = statistics.mean(q_vals) if q_vals else 0
            
            # Q 값을 성공률로 근사 (Q값이 높을수록 성공률 높음)
            # 정규화: (Q - min) / (max - min) * 100
            if q_vals:
                min_q = min(q_vals)
                max_q = max(q_vals)
                estimated_success_rate = (avg_q - min_q) / (max_q - min_q) if max_q != min_q else 0.5
            else:
                estimated_success_rate = 0.5
            
            result[action] = {
                'avg_q': avg_q,
                'max_q': max(q_vals) if q_vals else 0,
                'min_q': min(q_vals) if q_vals else 0,
                'count': data['count'],
                'states': len(data['states']),
                'estimated_success_rate': max(0, min(1, estimated_success_rate))
            }
        
        return result
    
    def identify_ineffective_actions(self, threshold: float = 0.3) -> Dict:
        """비효율적 액션 감지"""
        
        print("\n" + "="*80)
        print("🚨 비효율적 액션 감지")
        print("="*80)
        
        action_stats = self._calculate_action_statistics()
        ineffective = []
        
        for action, stats in action_stats.items():
            success_rate = stats['estimated_success_rate']
            
            if success_rate < threshold:
                ineffective.append({
                    'action': action,
                    'success_rate': success_rate,
                    'avg_q': stats['avg_q'],
                    'recommendation': self._get_recommendation(action, stats)
                })
                
                print(f"""
⚠️ {action}:
   • 성공률: {success_rate:.1%} (기준: {threshold:.1%})
   • 평균 Q 값: {stats['avg_q']:.2f}
   • 사용된 상태: {stats['states']}개
   • 추천: {self._get_recommendation(action, stats)}
""")
        
        if not ineffective:
            print("✅ 모든 액션이 효율적입니다 (성공률 > 30%)")
        
        return {
            'ineffective_actions': ineffective,
            'threshold': threshold
        }
    
    def _get_recommendation(self, action: str, stats: Dict) -> str:
        """액션별 개선 권장사항"""
        
        recommendations = {
            'restart_immediately': "빠르지만 위험함. 전제 조건 추가 검사 필요",
            'check_dependencies': "안전하지만 느림. 캐싱으로 속도 개선 필요",
            'wait_and_retry': "효율 낮음. 감소 추천 또는 제거 검토",
            'escalate_manual': "수동 개입 필요. 자동화 가능성 검토",
            'restart_clean': "안전함. 계속 사용 권장"
        }
        
        for key, rec in recommendations.items():
            if key in action:
                return rec
        
        return "개선 필요"
    
    def optimize_by_state(self) -> Dict:
        """상태별 최적 액션 추천"""
        
        print("\n" + "="*80)
        print("🎯 상태별 최적 액션 추천")
        print("="*80)
        
        state_optimal_actions = {}
        
        for state, actions in self.state_action_map.items():
            best_q = -float('inf')
            best_action = None
            
            for action in actions:
                key = f"{state}_{action}"
                q_value = self.q_values.get(key, -float('inf'))
                
                if q_value > best_q:
                    best_q = q_value
                    best_action = action
            
            state_optimal_actions[state] = {
                'best_action': best_action,
                'q_value': best_q
            }
            
            print(f"""
상태: {state}
   • 최적 액션: {best_action}
   • Q 값: {best_q:.2f}
   • 모든 액션: {', '.join(actions)}
""")
        
        return state_optimal_actions
    
    def generate_optimization_report(self) -> Dict:
        """최적화 리포트 생성"""
        
        print("\n" + "="*80)
        print("📋 최적화 리포트 생성")
        print("="*80)
        
        action_effectiveness = self.analyze_action_effectiveness()
        ineffective = self.identify_ineffective_actions()
        optimal_by_state = self.optimize_by_state()
        
        # 전체 요약
        total_actions = len(action_effectiveness)
        ineffective_count = len(ineffective['ineffective_actions'])
        effective_count = total_actions - ineffective_count
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'action_effectiveness': action_effectiveness,
            'ineffective_actions': ineffective['ineffective_actions'],
            'optimal_actions_by_state': optimal_by_state,
            'summary': {
                'total_actions': total_actions,
                'effective_actions': effective_count,
                'ineffective_actions': ineffective_count,
                'overall_effectiveness': (effective_count / total_actions * 100) if total_actions > 0 else 0
            },
            'recommendations': self._generate_recommendations(
                action_effectiveness,
                ineffective['ineffective_actions'],
                optimal_by_state
            )
        }
        
        # 리포트 저장
        report_path = Path("logs/neural_efficiency/action_effectiveness_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ 리포트 저장: {report_path}")
        
        return report
    
    def _generate_recommendations(self, effectiveness: Dict, ineffective: List, optimal: Dict) -> Dict:
        """최적화 권장사항 생성"""
        
        recommendations = {
            'immediate_actions': [],
            'medium_term_improvements': [],
            'long_term_optimizations': []
        }
        
        # 즉시 조치 필요 (성공률 < 20%)
        for item in ineffective:
            if item['success_rate'] < 0.2:
                recommendations['immediate_actions'].append(
                    f"❌ {item['action']} 비활성화 (성공률 {item['success_rate']:.1%})"
                )
        
        # 단기 개선 (성공률 20-40%)
        for action, stats in effectiveness.items():
            if 0.2 < stats['estimated_success_rate'] < 0.4:
                recommendations['medium_term_improvements'].append(
                    f"⚠️ {action} 개선 (성공률 {stats['estimated_success_rate']:.1%})"
                )
        
        # 장기 최적화
        recommendations['long_term_optimizations'].append(
            "✅ 상태별 최적 액션 우선 사용"
        )
        recommendations['long_term_optimizations'].append(
            "✅ Q-Learning 수렴 후 정책 배포"
        )
        recommendations['long_term_optimizations'].append(
            "✅ 액션 조합 방식 도입 (여러 액션 순차 실행)"
        )
        
        return recommendations


def main():
    """메인 실행"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║  📊 액션 효율성 분석                                                        ║
║     Week 2 Step 2: 복구 전략 최적화                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    analyzer = ActionEffectivenessAnalyzer()
    report = analyzer.generate_optimization_report()
    
    # 최종 요약
    summary = report['summary']
    recommendations = report['recommendations']
    
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ 분석 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 요약:
   • 총 액션: {summary['total_actions']}개
   • 효율적 액션: {summary['effective_actions']}개
   • 비효율적 액션: {summary['ineffective_actions']}개
   • 전체 효율: {summary['overall_effectiveness']:.1f}%

📋 즉시 조치:
""")
    
    if recommendations['immediate_actions']:
        for rec in recommendations['immediate_actions']:
            print(f"   {rec}")
    else:
        print("   ✅ 모두 양호합니다")
    
    print(f"""
📋 단기 개선:
""")
    
    if recommendations['medium_term_improvements']:
        for rec in recommendations['medium_term_improvements']:
            print(f"   {rec}")
    else:
        print("   ✅ 없음")
    
    print(f"""
📋 장기 최적화:
""")
    
    for rec in recommendations['long_term_optimizations']:
        print(f"   {rec}")
    
    print(f"""
상세 리포트: logs/neural_efficiency/action_effectiveness_report.json
""")


if __name__ == "__main__":
    main()
