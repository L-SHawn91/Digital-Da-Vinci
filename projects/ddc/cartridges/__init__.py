"""
Cartridges (카트리지) - 신피질의 전문 기능 영역

각 카트리지는 신피질의 특정 엽들을 조합하여 특정 도메인의 작업을 수행합니다:

- Bio (생물학): Occipital (후두엽) + Temporal (측두엽)
  = 세포/오가노이드 이미지 분석

- Inv (투자): Prefrontal (전두엽) + Parietal (두정엽)
  = 주식/포트폴리오 분석 및 의사결정

- Lit (문학): Temporal (측두엽) + Prefrontal (전두엽)
  = 텍스트 분석 및 의미 추출

- Quant (정량): Parietal (두정엽) + Prefrontal (전두엽)
  = 정량 분석 및 수학 처리

- Astro (천문): Occipital (후두엽) + Parietal (두정엽)
  = 우주 데이터 시각화 및 분석
"""

from .bio import bio_interface
from .inv import inv_interface

__all__ = [
    'bio_interface',
    'inv_interface',
]

__version__ = "5.1.0"
__description__ = "SHawn-Brain Cartridges - 신피질의 전문 기능 영역"
