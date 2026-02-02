"""
Memory Management - Limbic System
기억 관리: 감정과 가치와 함께 저장
"""

class MemoryManager:
    """도메인별 기억 관리"""
    
    def __init__(self):
        self.memories = {}
        self.values = {}
        self.confidence = {}
    
    def store(self, domain: str, data: dict, confidence: float = 1.0):
        """기억 저장"""
        self.memories[domain] = data
        self.confidence[domain] = confidence
