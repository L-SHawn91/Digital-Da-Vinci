"""
Astro Cartridge Interface - 신피질과의 연결

신피질의 Occipital (후두엽)과 Parietal (두정엽)을 활용한 천문/우주 데이터 분석
"""

from typing import Dict, Any, List
import os

# neocortex 임포트
try:
    from ddc.brain.neocortex.occipital import visualization_engine
    from ddc.brain.neocortex.parietal import innovation_engine
    NEOCORTEX_AVAILABLE = True
except ImportError:
    NEOCORTEX_AVAILABLE = False
    print("⚠️ Warning: neocortex 모듈을 찾을 수 없습니다.")


class AstroCartridgeInterface:
    """Astro Cartridge Interface - neocortex와 협력"""
    
    def __init__(self):
        """초기화"""
        self.visualization_engine = visualization_engine if NEOCORTEX_AVAILABLE else None
        self.innovation_engine = innovation_engine if NEOCORTEX_AVAILABLE else None
    
    def analyze_celestial_data(
        self,
        object_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        천문 데이터 분석 (neocortex 협력)
        
        Args:
            object_type: 천체 유형 (star, planet, galaxy, nebula)
            data: 천문 데이터
            
        Returns:
            분석 결과
        """
        
        result = {
            'object_type': object_type,
            'data': data,
            'neocortex_integration': {}
        }
        
        if not NEOCORTEX_AVAILABLE:
            return result
        
        # Step 1: Occipital (후두엽) - 시각 분석
        print("🧠 Occipital (후두엽): 천체 시각 분석")
        try:
            visual_analysis = self.visualization_engine.analyze_celestial_image(
                object_type=object_type,
                data=data
            )
            result['neocortex_integration']['visual'] = visual_analysis
        except Exception as e:
            print(f"⚠️ Occipital 처리 오류: {e}")
        
        # Step 2: Parietal (두정엽) - 공간/수치 분석
        print("🧠 Parietal (두정엽): 공간 분석")
        try:
            spatial_analysis = self.innovation_engine.analyze_celestial_space(
                object_type=object_type,
                data=data
            )
            result['neocortex_integration']['spatial'] = spatial_analysis
        except Exception as e:
            print(f"⚠️ Parietal 처리 오류: {e}")
        
        result['neocortex_integration']['status'] = 'complete'
        return result
    
    def visualize_star_map(
        self,
        coordinates: List[Dict[str, float]],
        magnitude_range: tuple = (0, 6)
    ) -> Dict[str, Any]:
        """
        별지도 시각화
        
        Args:
            coordinates: 별의 좌표 리스트 [{'ra': 0, 'dec': 0, 'magnitude': 3.5}, ...]
            magnitude_range: 겉보기 등급 범위
        """
        print("🧠 Occipital: 별지도 시각화")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'visualization': None}
        
        try:
            visualization = self.visualization_engine.create_star_map(
                coordinates=coordinates,
                magnitude_range=magnitude_range
            )
            return {'status': 'success', 'visualization': visualization}
        except Exception as e:
            print(f"⚠️ 별지도 시각화 오류: {e}")
            return {'status': 'error', 'visualization': None}
    
    def analyze_exoplanet(self, planet_data: Dict[str, Any]) -> Dict[str, Any]:
        """외계 행성 분석"""
        print("🧠 Parietal: 외계 행성 분석")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'habitability': 'unknown'}
        
        try:
            analysis = self.innovation_engine.analyze_exoplanet(planet_data)
            return {'status': 'success', **analysis}
        except Exception as e:
            print(f"⚠️ 외계 행성 분석 오류: {e}")
            return {'status': 'error', 'habitability': 'unknown'}
    
    def analyze_light_spectrum(
        self,
        wavelengths: List[float],
        intensities: List[float]
    ) -> Dict[str, Any]:
        """광 스펙트럼 분석"""
        print("🧠 Occipital: 광 스펙트럼 분석")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'composition': {}}
        
        try:
            spectrum = self.visualization_engine.analyze_spectrum(
                wavelengths=wavelengths,
                intensities=intensities
            )
            return {'status': 'success', 'spectrum': spectrum}
        except Exception as e:
            print(f"⚠️ 광 스펙트럼 분석 오류: {e}")
            return {'status': 'error', 'spectrum': {}}
    
    def calculate_orbital_mechanics(
        self,
        mass: float,
        distance: float,
        orbital_period: float
    ) -> Dict[str, Any]:
        """궤도 역학 계산"""
        print("🧠 Parietal: 궤도 역학 계산")
        
        try:
            mechanics = self.innovation_engine.calculate_orbital_mechanics(
                mass=mass,
                distance=distance,
                orbital_period=orbital_period
            )
            return {'status': 'success', 'mechanics': mechanics}
        except Exception as e:
            print(f"⚠️ 궤도 역학 계산 오류: {e}")
            return {'status': 'error', 'mechanics': {}}
    
    def detect_cosmic_events(
        self,
        event_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """우주 사건 감지"""
        print("🧠 Occipital + Parietal: 우주 사건 감지")
        
        result = {
            'detected_events': [],
            'status': 'success'
        }
        
        try:
            # Occipital로 이상 시각 탐지
            visual_anomalies = self.visualization_engine.detect_visual_anomalies(event_data)
            
            # Parietal로 공간적 이상 탐지
            spatial_anomalies = self.innovation_engine.detect_spatial_anomalies(event_data)
            
            result['detected_events'] = visual_anomalies + spatial_anomalies
            return result
        except Exception as e:
            print(f"⚠️ 우주 사건 감지 오류: {e}")
            return {'detected_events': [], 'status': 'error'}


# 편의 함수
def analyze_astronomical_data(object_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """간단한 천문 분석"""
    interface = AstroCartridgeInterface()
    return interface.analyze_celestial_data(object_type, data)


if __name__ == "__main__":
    print("🌌 Astro Cartridge Interface 테스트")
    print(f"neocortex 상태: {'✅ Available' if NEOCORTEX_AVAILABLE else '❌ Not Available'}")
