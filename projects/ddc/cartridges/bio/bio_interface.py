"""
Bio Cartridge Interface - 신피질과의 연결

신피질의 Occipital (후두엽)과 Temporal (측두엽)을 활용한 생물학 분석
"""

from typing import Dict, Any, Optional
import os

# neocortex 임포트
try:
    from ddc.brain.neocortex.occipital import visualization_engine
    from ddc.brain.neocortex.temporal import semantic_processor
    NEOCORTEX_AVAILABLE = True
except ImportError:
    NEOCORTEX_AVAILABLE = False
    print("⚠️ Warning: neocortex 모듈을 찾을 수 없습니다.")

# Bio Cartridge v2.1 임포트
from .bio_cartridge_v2_1 import BioCartridge, CellType, HealthStatus


class BioCartridgeInterface:
    """Bio Cartridge Interface - neocortex와 협력"""
    
    def __init__(self):
        """초기화"""
        self.bio_cartridge = BioCartridge()
        self.visualization_engine = visualization_engine if NEOCORTEX_AVAILABLE else None
        self.semantic_processor = semantic_processor if NEOCORTEX_AVAILABLE else None
    
    def analyze_cell_image_with_neocortex(
        self, 
        image_path: str,
        use_neocortex: bool = True
    ) -> Dict[str, Any]:
        """
        세포 이미지 분석 (neocortex 협력)
        
        Args:
            image_path: 이미지 경로
            use_neocortex: neocortex 사용 여부
            
        Returns:
            분석 결과
        """
        
        # Step 1: Bio Cartridge v2.1로 이미지 분석
        print(f"📊 Bio Cartridge v2.1으로 이미지 분석 중: {image_path}")
        bio_result = self.bio_cartridge.analyze_image_async(image_path)
        
        result = {
            'bio_analysis': bio_result,
            'neocortex_integration': {}
        }
        
        if not use_neocortex or not NEOCORTEX_AVAILABLE:
            return result
        
        # Step 2: Occipital (후두엽) - 시각 처리
        print("🧠 Occipital (후두엽): 시각 특성 추출")
        try:
            visual_features = self.visualization_engine.extract_visual_features(
                image_path=image_path,
                cell_type=bio_result.get('cell_type', 'UNKNOWN')
            )
            result['neocortex_integration']['visual_features'] = visual_features
        except Exception as e:
            print(f"⚠️ Occipital 처리 오류: {e}")
        
        # Step 3: Temporal (측두엽) - 의미 처리
        print("🧠 Temporal (측두엽): 의미/패턴 처리")
        try:
            semantic_analysis = self.semantic_processor.process_cell_semantics(
                cell_type=bio_result.get('cell_type', 'UNKNOWN'),
                health_status=bio_result.get('health_status', 'UNKNOWN'),
                confidence=bio_result.get('confidence', 0)
            )
            result['neocortex_integration']['semantic_analysis'] = semantic_analysis
        except Exception as e:
            print(f"⚠️ Temporal 처리 오류: {e}")
        
        # Step 4: 최종 종합 분석
        print("🧠 신피질 통합 분석 완료")
        result['neocortex_integration']['status'] = 'complete'
        
        return result
    
    def analyze_organoid_development(
        self,
        image_sequence: list,
        time_labels: list
    ) -> Dict[str, Any]:
        """
        오가노이드 발달 과정 분석 (시계열)
        
        Args:
            image_sequence: 시간 순서대로 정렬된 이미지 경로 리스트
            time_labels: 각 이미지의 시간 레이블 (e.g., ['Day 1', 'Day 3', 'Day 7'])
            
        Returns:
            발달 분석 결과
        """
        
        results = []
        for image_path, time_label in zip(image_sequence, time_labels):
            print(f"\n📅 {time_label} 분석 중...")
            analysis = self.analyze_cell_image_with_neocortex(image_path)
            analysis['time_label'] = time_label
            results.append(analysis)
        
        # Temporal (측두엽)로 발달 패턴 분석
        if NEOCORTEX_AVAILABLE and self.semantic_processor:
            print("\n🧠 Temporal: 발달 패턴 추적")
            try:
                development_pattern = self.semantic_processor.analyze_temporal_pattern(
                    analyses=results
                )
                return {
                    'developmental_stages': results,
                    'pattern_analysis': development_pattern
                }
            except Exception as e:
                print(f"⚠️ 발달 패턴 분석 오류: {e}")
        
        return {'developmental_stages': results}


# 편의 함수
def analyze_bio_image(image_path: str) -> Dict[str, Any]:
    """간단한 이미지 분석 (neocortex 협력)"""
    interface = BioCartridgeInterface()
    return interface.analyze_cell_image_with_neocortex(image_path)


if __name__ == "__main__":
    # 테스트
    print("🧬 Bio Cartridge Interface 테스트")
    print(f"neocortex 상태: {'✅ Available' if NEOCORTEX_AVAILABLE else '❌ Not Available'}")
