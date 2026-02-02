"""
Lit Cartridge Interface - 신피질과의 연결

신피질의 Temporal (측두엽)과 Prefrontal (전두엽)을 활용한 문학/텍스트 분석
"""

from typing import Dict, Any, Optional, List
import os

# neocortex 임포트
try:
    from ddc.brain.neocortex.temporal import semantic_processor
    from ddc.brain.neocortex.prefrontal import decision_framework
    NEOCORTEX_AVAILABLE = True
except ImportError:
    NEOCORTEX_AVAILABLE = False
    print("⚠️ Warning: neocortex 모듈을 찾을 수 없습니다.")


class LitCartridgeInterface:
    """Lit Cartridge Interface - neocortex와 협력"""
    
    def __init__(self):
        """초기화"""
        self.semantic_processor = semantic_processor if NEOCORTEX_AVAILABLE else None
        self.decision_framework = decision_framework if NEOCORTEX_AVAILABLE else None
    
    def analyze_text(
        self,
        text: str,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        텍스트 분석 (neocortex 협력)
        
        Args:
            text: 분석할 텍스트
            analysis_type: 분석 유형 (sentiment, semantic, entity, comprehensive)
            
        Returns:
            분석 결과
        """
        
        result = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'text_length': len(text),
            'analysis_type': analysis_type,
            'neocortex_integration': {}
        }
        
        if not NEOCORTEX_AVAILABLE:
            return result
        
        # Step 1: Temporal (측두엽) - 의미 처리
        print("🧠 Temporal (측두엽): 텍스트 의미 분석")
        try:
            semantic_result = self.semantic_processor.process_text(
                text=text,
                analysis_type=analysis_type
            )
            result['neocortex_integration']['semantic'] = semantic_result
        except Exception as e:
            print(f"⚠️ Temporal 처리 오류: {e}")
        
        # Step 2: Prefrontal (전두엽) - 의사결정
        print("🧠 Prefrontal (전두엽): 의견/추천 생성")
        try:
            decision_result = self.decision_framework.recommend_interpretation(
                semantic_data=result['neocortex_integration'].get('semantic', {})
            )
            result['neocortex_integration']['recommendation'] = decision_result
        except Exception as e:
            print(f"⚠️ Prefrontal 처리 오류: {e}")
        
        result['neocortex_integration']['status'] = 'complete'
        return result
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """명명된 엔터티 추출"""
        print("🧠 Temporal: 엔터티 추출")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'entities': []}
        
        try:
            entities = self.semantic_processor.extract_entities(text)
            return {'status': 'success', 'entities': entities}
        except Exception as e:
            print(f"⚠️ 엔터티 추출 오류: {e}")
            return {'status': 'error', 'entities': []}
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """감정 분석"""
        print("🧠 Temporal: 감정 분석")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'sentiment': 'neutral', 'score': 0.5}
        
        try:
            sentiment = self.semantic_processor.analyze_sentiment(text)
            return {'status': 'success', **sentiment}
        except Exception as e:
            print(f"⚠️ 감정 분석 오류: {e}")
            return {'status': 'error', 'sentiment': 'neutral', 'score': 0.5}
    
    def summarize_text(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """텍스트 요약"""
        print("🧠 Prefrontal: 텍스트 요약")
        
        if not NEOCORTEX_AVAILABLE:
            return {'status': 'pending', 'summary': ''}
        
        try:
            summary = self.decision_framework.summarize(text, max_length)
            return {'status': 'success', 'summary': summary}
        except Exception as e:
            print(f"⚠️ 요약 오류: {e}")
            return {'status': 'error', 'summary': ''}


# 편의 함수
def analyze_literature(text: str) -> Dict[str, Any]:
    """간단한 문학 분석"""
    interface = LitCartridgeInterface()
    return interface.analyze_text(text)


if __name__ == "__main__":
    print("📚 Lit Cartridge Interface 테스트")
    print(f"neocortex 상태: {'✅ Available' if NEOCORTEX_AVAILABLE else '❌ Not Available'}")
