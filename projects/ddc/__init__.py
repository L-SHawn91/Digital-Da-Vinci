"""
DDC (Digital Da Vinci Code)

SHawn-Brain 프로젝트의 핵심 코드 아키텍처입니다.

폴더 구조:
- brain/: D-CNS 신경계 (Brainstem, Limbic, Neocortex, NeuroNet)
- cartridges/: 전문 기능 (Bio, Inv, Lit, Quant, Astro)
- bot/: Telegram 인터페이스
- utils/: 공통 유틸리티

폴더명이 "src"가 아닌 "ddc"인 이유:
DDC = Digital Da Vinci Code
= "Digital Leonardo da Vinci Project"의 핵심 구현부

비유:
생명의 DNA = 생명의 기본 정보
프로젝트의 DDC = 프로젝트의 기본 코드 아키텍처

레오나르도 다빈치의 정신을 이어받은
기술, 과학, 예술의 융합 구조입니다.
"""

__version__ = "0.0.1"  # Prototype Version
__author__ = "Dr. SHawn (이수형)"
__project__ = "SHawn-Brain (Digital Leonardo da Vinci Project)"

# 🧠 신경계 시스템 import (D-CNS)
# 지연 로드 (lazy loading) - 모듈이 필요할 때 로드
_neural_system_loaded = False
_neural_router = None
_work_tracker = None

def get_neural_router():
    """신경 라우터 획득 (필요 시 로드)"""
    global _neural_system_loaded, _neural_router
    if not _neural_system_loaded:
        try:
            from systems.neural.neural_router import NeuralModelRouter
            _neural_router = NeuralModelRouter
            _neural_system_loaded = True
        except (ImportError, ModuleNotFoundError):
            pass
    return _neural_router

def get_work_tracker():
    """작업 추적기 획득 (필요 시 로드)"""
    global _neural_system_loaded, _work_tracker
    if not _neural_system_loaded:
        try:
            from systems.neural.work_tracker import WorkTracker
            _work_tracker = WorkTracker
            _neural_system_loaded = True
        except (ImportError, ModuleNotFoundError):
            pass
    return _work_tracker

# 즉시 확인용 플래그
try:
    from systems.neural.neural_router import NeuralModelRouter as _nr
    __has_neural_system__ = True
except (ImportError, ModuleNotFoundError):
    __has_neural_system__ = False
