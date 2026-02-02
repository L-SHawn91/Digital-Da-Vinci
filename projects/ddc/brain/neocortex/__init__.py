"""
Neocortex: 4-lobe cognitive architecture
- Prefrontal: Decision & Planning
- Temporal: Semantic & Memory
- Parietal: Integration & Attention
- Occipital: Analysis & Visualization
"""

# 각 엽 동적 로드
from . import prefrontal, temporal, parietal, occipital

class NeocortexConnector:
    """신피질 4개 엽을 통합 관리"""
    
    def __init__(self):
        self.prefrontal = prefrontal
        self.temporal = temporal
        self.parietal = parietal
        self.occipital = occipital
    
    def process(self, task):
        """4개 엽이 협력하여 처리"""
        return {
            'prefrontal': 'planning',
            'temporal': 'memory',
            'parietal': 'integration',
            'occipital': 'analysis'
        }

neocortex_connector = NeocortexConnector()

__all__ = ['neocortex_connector', 'prefrontal', 'temporal', 'parietal', 'occipital']
