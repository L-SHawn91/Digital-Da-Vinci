"""
Daily Report Generator - 일일 모니터링 리포트 자동 생성

신경계 성능을 분석하고 일일 리포트를 Markdown 형식으로 생성합니다.
"""

import json
from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ModelRank:
    """모델 순위"""
    rank: int
    model: str
    score: float
    success_rate: float
    response_time: float
    tokens_used: int


class DailyReportGenerator:
    """일일 모니터링 리포트 생성기"""
    
    def __init__(self, monitor):
        """
        초기화
        
        Args:
            monitor: PerformanceMonitor 인스턴스
        """
        self.monitor = monitor
        self.report_date = datetime.now()
    
    def generate_daily_report(self) -> str:
        """
        일일 리포트 생성
        
        Returns:
            Markdown 형식의 리포트
        """
        report = []
        
        # 헤더
        report.append(f"# 일일 신경계 모니터링 리포트")
        report.append(f"**생성 일시**: {self.report_date.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 신경계 상태
        report.append("## 🧠 신경계 상태")
        report.append(self._format_neural_health())
        report.append("")
        
        # 모델 순위
        report.append("## 🏆 모델 성과 순위")
        report.append(self._format_model_rankings())
        report.append("")
        
        # 비용 분석
        report.append("## 💰 비용 분석")
        report.append(self._format_cost_analysis())
        report.append("")
        
        # 이상 탐지
        report.append("## ⚠️ 이상 탐지")
        report.append(self._format_anomalies())
        report.append("")
        
        # 권장 조치
        report.append("## 📋 권장 조치")
        report.append(self._format_recommendations())
        report.append("")
        
        return "\n".join(report)
    
    def _format_neural_health(self) -> str:
        """신경계 상태 포맷팅"""
        health = self.monitor.get_neural_health_status()
        lines = []
        
        for level in ['L1', 'L2', 'L3', 'L4']:
            stats = health.get(level, {})
            perf_level = stats.get('performance_level', 'unknown')
            
            # 이모지 선택
            emoji_map = {
                'excellent': '🟢',
                'good': '🟡',
                'normal': '🟠',
                'poor': '🔴',
                'critical': '⛔'
            }
            emoji = emoji_map.get(perf_level, '❓')
            
            lines.append(f"{emoji} **{level}**: {perf_level}")
            lines.append(f"  - 성공률: {stats.get('success_rate', 'N/A')}")
            lines.append(f"  - 응답시간: {stats.get('avg_response_time', 'N/A')}")
            lines.append(f"  - 호출: {stats.get('total_calls', 0)}회")
        
        return "\n".join(lines)
    
    def _format_model_rankings(self) -> str:
        """모델 순위 포맷팅"""
        model_health = self.monitor.get_model_health_status()
        
        # 점수 계산
        rankings = []
        for model, stats in model_health.items():
            # 성공률에서 % 제거
            success_rate = float(stats['success_rate'].rstrip('%'))
            response_time = float(stats['avg_response_time'].rstrip('ms'))
            
            # 점수 = 성공률 * 0.5 + (1000 / 응답시간) * 0.5
            score = (success_rate * 0.5) + ((1000 / max(response_time, 1)) * 0.5)
            
            rankings.append(ModelRank(
                rank=0,
                model=model,
                score=score,
                success_rate=success_rate,
                response_time=response_time,
                tokens_used=int(stats['total_tokens'])
            ))
        
        # 순위 정렬
        rankings.sort(key=lambda x: x.score, reverse=True)
        for i, rank in enumerate(rankings, 1):
            rank.rank = i
        
        # 테이블 생성
        lines = ["| 순위 | 모델 | 점수 | 성공률 | 응답시간 | 토큰 |"]
        lines.append("|------|------|--------|--------|---------|------|")
        
        for rank in rankings:
            lines.append(
                f"| {rank.rank} | {rank.model} | {rank.score:.1f} | "
                f"{rank.success_rate:.1f}% | {rank.response_time:.0f}ms | "
                f"{rank.tokens_used} |"
            )
        
        return "\n".join(lines)
    
    def _format_cost_analysis(self) -> str:
        """비용 분석 포맷팅"""
        model_health = self.monitor.get_model_health_status()
        
        lines = []
        total_tokens = 0
        
        # 모델별 토큰 사용량
        lines.append("### 모델별 토큰 사용량")
        lines.append("| 모델 | 호출 | 총 토큰 | 호출당 평균 |")
        lines.append("|------|------|--------|-----------|")
        
        for model, stats in sorted(model_health.items(), 
                                  key=lambda x: x[1]['total_tokens'], 
                                  reverse=True):
            tokens = stats['total_tokens']
            total_tokens += tokens
            lines.append(
                f"| {model} | {stats['total_calls']} | "
                f"{tokens} | {stats['tokens_per_call']} |"
            )
        
        lines.append("")
        
        # 비용 추정 (1M 토큰당 가격 기반)
        lines.append("### 추정 비용")
        lines.append(f"- 총 토큰: {total_tokens:,}")
        
        # 간단한 비용 추정 (평균 $0.001/1K 토큰)
        estimated_cost = total_tokens / 1000 * 0.001
        lines.append(f"- 예상 비용: ${estimated_cost:.4f}")
        lines.append(f"- 일 호출당 평균 토큰: {total_tokens / max(1, len(model_health)):.0f}")
        
        return "\n".join(lines)
    
    def _format_anomalies(self) -> str:
        """이상 탐지 포맷팅"""
        anomalies = self.monitor.detect_anomalies()
        
        if not anomalies:
            return "✅ 감지된 이상 없음"
        
        lines = []
        for anomaly in anomalies:
            anomaly_type = anomaly.get('type', 'unknown')
            value = anomaly.get('value', 'N/A')
            threshold = anomaly.get('threshold', 'N/A')
            
            lines.append(f"- **{anomaly_type}**: {value} (임계값: {threshold})")
            if 'model' in anomaly:
                lines.append(f"  모델: {anomaly['model']}")
            if 'level' in anomaly:
                lines.append(f"  신경계: {anomaly['level']}")
        
        return "\n".join(lines) if lines else "✅ 감지된 이상 없음"
    
    def _format_recommendations(self) -> str:
        """권장 조치 생성"""
        health = self.monitor.get_neural_health_status()
        recommendations = []
        
        # 신경계별 조치
        for level, stats in health.items():
            success_rate = float(stats['success_rate'].rstrip('%'))
            
            if success_rate < 70:
                recommendations.append(
                    f"⚠️ {level} 신경계 성공률 저하: "
                    f"다른 모델로 대체하거나 토큰 리셋 고려"
                )
            elif success_rate < 85:
                recommendations.append(
                    f"💡 {level} 신경계 모니터링: "
                    f"지속적인 성능 추적 필요"
                )
        
        # 고토큰 모델
        model_health = self.monitor.get_model_health_status()
        for model, stats in model_health.items():
            tokens_per_call = int(float(stats['tokens_per_call']))
            if tokens_per_call > 500:
                recommendations.append(
                    f"💰 {model} 토큰 사용량 높음: "
                    f"프롬프트 최적화 또는 폴백 모델 검토"
                )
        
        if not recommendations:
            recommendations.append("✅ 현재 시스템 성능이 양호합니다")
        
        return "\n".join(f"- {rec}" for rec in recommendations)
    
    def save_report(self, filename: str) -> None:
        """리포트를 파일로 저장"""
        report = self.generate_daily_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def analyze_model_performance(self) -> Dict:
        """모델 성능 분석"""
        model_health = self.monitor.get_model_health_status()
        analysis = {}
        
        for model, stats in model_health.items():
            success_rate = float(stats['success_rate'].rstrip('%'))
            response_time = float(stats['avg_response_time'].rstrip('ms'))
            
            analysis[model] = {
                'success_rate': success_rate,
                'response_time': response_time,
                'efficiency': (success_rate / max(response_time, 1)) * 100,
                'total_calls': stats['total_calls'],
                'total_tokens': stats['total_tokens']
            }
        
        return analysis
    
    def calculate_daily_cost(self) -> Dict:
        """일일 비용 계산"""
        model_health = self.monitor.get_model_health_status()
        
        total_tokens = sum(stats['total_tokens'] for stats in model_health.values())
        
        # 모델별 가격 (1M 토큰당)
        model_prices = {
            'Gemini': 0.075,
            'Claude': 0.8,
            'Groq': 0.05,
            'DeepSeek': 0.07,
            'default': 0.1
        }
        
        cost_breakdown = {}
        total_cost = 0
        
        for model, stats in model_health.items():
            tokens = stats['total_tokens']
            price = model_prices.get(model, model_prices['default'])
            cost = (tokens / 1_000_000) * price
            cost_breakdown[model] = {
                'tokens': tokens,
                'price_per_1m': price,
                'cost': cost
            }
            total_cost += cost
        
        return {
            'date': self.report_date.strftime('%Y-%m-%d'),
            'total_tokens': total_tokens,
            'total_cost': total_cost,
            'breakdown': cost_breakdown
        }


# 테스트 코드
if __name__ == "__main__":
    from performance_monitor import PerformanceMonitor
    
    monitor = PerformanceMonitor()
    monitor.record_execution(1200, 500, True, "Gemini", "L1")
    monitor.record_execution(1500, 600, True, "Claude", "L2")
    monitor.record_execution(900, 400, True, "Groq", "L3")
    
    generator = DailyReportGenerator(monitor)
    report = generator.generate_daily_report()
    print(report)
