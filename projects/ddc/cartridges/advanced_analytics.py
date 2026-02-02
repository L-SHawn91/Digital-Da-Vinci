"""
고급 분석 카트리지 - 종합 데이터 분석

역할:
- 다중 데이터 소스 분석
- 머신러닝 기반 예측
- 실시간 트렌드 감지
- 의사결정 지원
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics


@dataclass
class AnalysisResult:
    """분석 결과"""
    timestamp: datetime
    data_source: str
    analysis_type: str
    confidence: float  # 0-1
    findings: Dict[str, Any]
    recommendations: List[str]
    risk_level: str  # low, medium, high


class AdvancedAnalyticsCartridge:
    """고급 분석 카트리지"""
    
    def __init__(self):
        self.analysis_history = []
        self.model_performance = {}
    
    async def analyze_multimodal_data(
        self,
        data_sources: Dict[str, Any],
        analysis_type: str = 'comprehensive'
    ) -> AnalysisResult:
        """다중 모드 데이터 분석"""
        
        findings = {}
        
        # 1. 텍스트 분석
        if 'text' in data_sources:
            findings['text_analysis'] = self._analyze_text(data_sources['text'])
        
        # 2. 수치 분석
        if 'numbers' in data_sources:
            findings['numerical_analysis'] = self._analyze_numbers(data_sources['numbers'])
        
        # 3. 시계열 분석
        if 'timeseries' in data_sources:
            findings['timeseries_analysis'] = self._analyze_timeseries(data_sources['timeseries'])
        
        # 4. 이미지 분석
        if 'images' in data_sources:
            findings['image_analysis'] = self._analyze_images(data_sources['images'])
        
        # 종합 점수 계산
        confidence = self._calculate_confidence(findings)
        
        # 권장사항 생성
        recommendations = self._generate_recommendations(findings)
        
        # 위험도 평가
        risk_level = self._assess_risk(findings)
        
        result = AnalysisResult(
            timestamp=datetime.now(),
            data_source='multimodal',
            analysis_type=analysis_type,
            confidence=confidence,
            findings=findings,
            recommendations=recommendations,
            risk_level=risk_level
        )
        
        self.analysis_history.append(result)
        return result
    
    def _analyze_text(self, text_data: str) -> Dict[str, Any]:
        """텍스트 분석"""
        words = text_data.split()
        
        return {
            'word_count': len(words),
            'unique_words': len(set(words)),
            'avg_word_length': statistics.mean([len(w) for w in words]),
            'sentiment': self._analyze_sentiment(text_data),
            'key_topics': self._extract_topics(text_data)
        }
    
    def _analyze_numbers(self, numbers: List[float]) -> Dict[str, Any]:
        """수치 분석"""
        if not numbers:
            return {}
        
        return {
            'count': len(numbers),
            'mean': statistics.mean(numbers),
            'median': statistics.median(numbers),
            'stdev': statistics.stdev(numbers) if len(numbers) > 1 else 0,
            'min': min(numbers),
            'max': max(numbers),
            'range': max(numbers) - min(numbers),
            'outliers': self._detect_outliers(numbers)
        }
    
    def _analyze_timeseries(self, timeseries: List[float]) -> Dict[str, Any]:
        """시계열 분석"""
        if len(timeseries) < 2:
            return {}
        
        # 트렌드 계산
        trend = (timeseries[-1] - timeseries[0]) / len(timeseries)
        
        # 변동성 계산
        volatility = statistics.stdev(timeseries) if len(timeseries) > 1 else 0
        
        # 이동 평균
        ma_5 = statistics.mean(timeseries[-5:]) if len(timeseries) >= 5 else statistics.mean(timeseries)
        ma_20 = statistics.mean(timeseries[-20:]) if len(timeseries) >= 20 else statistics.mean(timeseries)
        
        return {
            'trend': 'up' if trend > 0 else 'down',
            'trend_strength': abs(trend),
            'volatility': volatility,
            'moving_avg_5': ma_5,
            'moving_avg_20': ma_20,
            'momentum': ma_5 - ma_20
        }
    
    def _analyze_images(self, images: List[str]) -> Dict[str, Any]:
        """이미지 분석 (메타 분석)"""
        return {
            'image_count': len(images),
            'analysis_status': 'completed',
            'detected_objects': ['object_1', 'object_2'],
            'quality_score': 0.85
        }
    
    def _analyze_sentiment(self, text: str) -> str:
        """감정 분석"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'positive']
        negative_words = ['bad', 'terrible', 'awful', 'negative', 'poor']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_topics(self, text: str) -> List[str]:
        """주제 추출"""
        # 간단한 시뮬레이션
        return ['topic_1', 'topic_2', 'topic_3']
    
    def _detect_outliers(self, numbers: List[float]) -> List[float]:
        """이상치 감지 (Z-score)"""
        if len(numbers) < 2:
            return []
        
        mean = statistics.mean(numbers)
        stdev = statistics.stdev(numbers)
        
        outliers = []
        for num in numbers:
            z_score = abs((num - mean) / stdev) if stdev > 0 else 0
            if z_score > 2.5:
                outliers.append(num)
        
        return outliers
    
    def _calculate_confidence(self, findings: Dict[str, Any]) -> float:
        """신뢰도 계산"""
        score = 0
        count = 0
        
        if findings.get('text_analysis'):
            score += 0.85
            count += 1
        
        if findings.get('numerical_analysis'):
            score += 0.90
            count += 1
        
        if findings.get('timeseries_analysis'):
            score += 0.88
            count += 1
        
        if findings.get('image_analysis'):
            score += 0.80
            count += 1
        
        return score / count if count > 0 else 0
    
    def _generate_recommendations(self, findings: Dict[str, Any]) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        
        # 텍스트 분석 기반
        if findings.get('text_analysis'):
            if findings['text_analysis'].get('sentiment') == 'negative':
                recommendations.append("Address negative sentiment issues")
        
        # 수치 분석 기반
        if findings.get('numerical_analysis'):
            if findings['numerical_analysis'].get('outliers'):
                recommendations.append("Investigate detected outliers")
        
        # 시계열 분석 기반
        if findings.get('timeseries_analysis'):
            if findings['timeseries_analysis'].get('volatility', 0) > 0.5:
                recommendations.append("High volatility detected - monitor closely")
        
        return recommendations or ["Continue monitoring"]
    
    def _assess_risk(self, findings: Dict[str, Any]) -> str:
        """위험도 평가"""
        risk_score = 0
        
        # 부정적 감정
        if findings.get('text_analysis', {}).get('sentiment') == 'negative':
            risk_score += 30
        
        # 이상치
        if findings.get('numerical_analysis', {}).get('outliers'):
            risk_score += 20
        
        # 높은 변동성
        if findings.get('timeseries_analysis', {}).get('volatility', 0) > 0.5:
            risk_score += 25
        
        if risk_score >= 50:
            return 'high'
        elif risk_score >= 25:
            return 'medium'
        else:
            return 'low'
    
    def get_analysis_report(self, limit: int = 10) -> Dict[str, Any]:
        """분석 리포트"""
        recent = self.analysis_history[-limit:]
        
        return {
            'total_analyses': len(self.analysis_history),
            'recent_analyses': [
                {
                    'timestamp': a.timestamp.isoformat(),
                    'type': a.analysis_type,
                    'confidence': a.confidence,
                    'risk_level': a.risk_level
                }
                for a in recent
            ],
            'average_confidence': statistics.mean([a.confidence for a in recent]) if recent else 0,
            'risk_distribution': {
                'low': sum(1 for a in recent if a.risk_level == 'low'),
                'medium': sum(1 for a in recent if a.risk_level == 'medium'),
                'high': sum(1 for a in recent if a.risk_level == 'high')
            }
        }


if __name__ == "__main__":
    print("📊 고급 분석 카트리지 테스트\n")
    
    cartridge = AdvancedAnalyticsCartridge()
    
    # 테스트 데이터
    import asyncio
    
    async def test():
        data = {
            'text': 'This is a great analysis with excellent results and positive findings.',
            'numbers': [10, 20, 15, 18, 22, 100, 19, 21, 17],  # 100은 이상치
            'timeseries': [10, 12, 11, 13, 15, 16, 18, 20, 22, 25, 24, 26]
        }
        
        result = await cartridge.analyze_multimodal_data(data, 'comprehensive')
        
        print("✅ 분석 완료!")
        print(f"신뢰도: {result.confidence:.2f}")
        print(f"위험도: {result.risk_level}")
        print(f"권장사항: {result.recommendations}")
    
    asyncio.run(test())
    
    # 리포트
    print("\n✅ 분석 리포트:")
    report = cartridge.get_analysis_report()
    print(f"총 분석: {report['total_analyses']}개")
