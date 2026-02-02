"""
Quant Cartridge Interface - 신피질과의 연결

신피질의 Parietal (두정엽)과 Prefrontal (전두엽)을 활용한 정량 분석
"""

from typing import Dict, Any, List, Tuple
import os

# neocortex 임포트
try:
    from ddc.brain.neocortex.parietal import innovation_engine
    from ddc.brain.neocortex.prefrontal import decision_framework
    NEOCORTEX_AVAILABLE = True
except ImportError:
    NEOCORTEX_AVAILABLE = False
    print("⚠️ Warning: neocortex 모듈을 찾을 수 없습니다.")


class QuantCartridgeInterface:
    """Quant Cartridge Interface - neocortex와 협력"""
    
    def __init__(self):
        """초기화"""
        self.innovation_engine = innovation_engine if NEOCORTEX_AVAILABLE else None
        self.decision_framework = decision_framework if NEOCORTEX_AVAILABLE else None
    
    def analyze_data(
        self,
        data: List[float],
        data_type: str = "timeseries"
    ) -> Dict[str, Any]:
        """
        정량 데이터 분석 (neocortex 협력)
        
        Args:
            data: 분석할 데이터 리스트
            data_type: 데이터 유형 (timeseries, distribution, correlation)
            
        Returns:
            분석 결과
        """
        
        result = {
            'data_type': data_type,
            'data_length': len(data),
            'neocortex_integration': {}
        }
        
        if not NEOCORTEX_AVAILABLE:
            return result
        
        # Step 1: Parietal (두정엽) - 공간/통계 분석
        print("🧠 Parietal (두정엽): 정량 분석")
        try:
            quant_analysis = self.innovation_engine.analyze_data(
                data=data,
                data_type=data_type
            )
            result['neocortex_integration']['quantitative'] = quant_analysis
        except Exception as e:
            print(f"⚠️ Parietal 처리 오류: {e}")
        
        # Step 2: Prefrontal (전두엽) - 의사결정 및 해석
        print("🧠 Prefrontal (전두엽): 의사결정")
        try:
            decision = self.decision_framework.interpret_data(
                quant_data=result['neocortex_integration'].get('quantitative', {})
            )
            result['neocortex_integration']['interpretation'] = decision
        except Exception as e:
            print(f"⚠️ Prefrontal 처리 오류: {e}")
        
        result['neocortex_integration']['status'] = 'complete'
        return result
    
    def calculate_statistics(self, data: List[float]) -> Dict[str, float]:
        """기본 통계 계산"""
        print("🧠 Parietal: 통계 계산")
        
        if not data:
            return {'error': 'No data provided'}
        
        try:
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            std_dev = variance ** 0.5
            
            return {
                'mean': mean,
                'median': sorted(data)[len(data) // 2],
                'min': min(data),
                'max': max(data),
                'std_dev': std_dev,
                'variance': variance,
                'range': max(data) - min(data)
            }
        except Exception as e:
            print(f"⚠️ 통계 계산 오류: {e}")
            return {'error': str(e)}
    
    def analyze_correlation(self, series1: List[float], series2: List[float]) -> Dict[str, Any]:
        """상관관계 분석"""
        print("🧠 Parietal: 상관관계 분석")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'correlation': 0}
        
        try:
            correlation = self.innovation_engine.calculate_correlation(series1, series2)
            return {'status': 'success', 'correlation': correlation}
        except Exception as e:
            print(f"⚠️ 상관관계 분석 오류: {e}")
            return {'status': 'error', 'correlation': 0}
    
    def detect_anomalies(self, data: List[float], threshold: float = 2.0) -> Dict[str, Any]:
        """이상치 탐지"""
        print("🧠 Parietal: 이상치 탐지")
        
        stats = self.calculate_statistics(data)
        mean = stats.get('mean', 0)
        std_dev = stats.get('std_dev', 1)
        
        anomalies = []
        for i, value in enumerate(data):
            if abs((value - mean) / std_dev) > threshold:
                anomalies.append({
                    'index': i,
                    'value': value,
                    'deviation': (value - mean) / std_dev
                })
        
        return {
            'status': 'success',
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'anomaly_percentage': (len(anomalies) / len(data)) * 100
        }
    
    def trend_analysis(self, data: List[float]) -> Dict[str, Any]:
        """추세 분석"""
        print("🧠 Prefrontal: 추세 분석")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'trend': 'unknown'}
        
        try:
            trend = self.decision_framework.analyze_trend(data)
            return {'status': 'success', 'trend': trend}
        except Exception as e:
            print(f"⚠️ 추세 분석 오류: {e}")
            return {'status': 'error', 'trend': 'unknown'}


# 편의 함수
def analyze_quantitative(data: List[float]) -> Dict[str, Any]:
    """간단한 정량 분석"""
    interface = QuantCartridgeInterface()
    return interface.analyze_data(data)


if __name__ == "__main__":
    print("📊 Quant Cartridge Interface 테스트")
    print(f"neocortex 상태: {'✅ Available' if NEOCORTEX_AVAILABLE else '❌ Not Available'}")
