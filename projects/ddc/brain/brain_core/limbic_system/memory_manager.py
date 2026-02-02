"""
MemoryManager - Limbic System의 기억 관리
감정과 가치와 함께 저장
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemoryType(Enum):
    """기억의 종류"""
    EPISODIC = "episodic"      # 경험적 기억
    SEMANTIC = "semantic"      # 의미적 기억
    PROCEDURAL = "procedural"  # 절차적 기억
    EMOTIONAL = "emotional"    # 감정적 기억


@dataclass
class Memory:
    """개별 기억"""
    content: str
    memory_type: MemoryType
    domain: str
    timestamp: datetime = field(default_factory=datetime.now)
    emotional_valence: float = 0.0  # -1.0 (negative) ~ 1.0 (positive)
    importance: float = 0.5         # 0.0 ~ 1.0
    associated_values: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    access_count: int = 0


class MemoryManager:
    """
    기억 관리 시스템
    - 도메인별 기억 저장/검색
    - 감정 + 가치 함께 저장
    - 기억 강도 및 중요도 추적
    - 관련 기억 연결
    """
    
    def __init__(self):
        """메모리 관리자 초기화"""
        self.memories: Dict[str, List[Memory]] = {
            "biology": [],
            "finance": [],
            "astronomy": [],
            "literature": [],
            "general": []
        }
        
        self.memory_index = {}  # 빠른 검색용 인덱스
        self.total_memories = 0
    
    def store(
        self,
        content: str,
        memory_type: MemoryType,
        domain: str = "general",
        emotional_valence: float = 0.0,
        importance: float = 0.5,
        associated_values: List[str] = None
    ) -> Memory:
        """
        기억 저장
        
        Args:
            content: 기억 내용
            memory_type: 기억 종류
            domain: 도메인
            emotional_valence: 감정 가중치 (-1 ~ 1)
            importance: 중요도 (0 ~ 1)
            associated_values: 관련 가치들
        
        Returns:
            저장된 Memory 객체
        """
        memory = Memory(
            content=content,
            memory_type=memory_type,
            domain=domain,
            emotional_valence=emotional_valence,
            importance=importance,
            associated_values=associated_values or []
        )
        
        # 도메인에 저장
        if domain not in self.memories:
            self.memories[domain] = []
        
        self.memories[domain].append(memory)
        
        # 인덱스 업데이트
        memory_id = f"{domain}_{self.total_memories}"
        self.memory_index[memory_id] = memory
        self.total_memories += 1
        
        return memory
    
    def retrieve(
        self,
        domain: str = "general",
        memory_type: Optional[MemoryType] = None,
        min_importance: float = 0.0
    ) -> List[Memory]:
        """
        기억 검색
        
        Args:
            domain: 도메인
            memory_type: 기억 종류 (선택)
            min_importance: 최소 중요도
        
        Returns:
            조건을 만족하는 기억들
        """
        if domain not in self.memories:
            return []
        
        memories = self.memories[domain]
        
        # 필터링
        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]
        
        memories = [m for m in memories if m.importance >= min_importance]
        
        # 최근순으로 정렬
        memories.sort(key=lambda m: m.timestamp, reverse=True)
        
        # 접근 횟수 업데이트
        for memory in memories:
            memory.access_count += 1
        
        return memories
    
    def search_by_content(self, query: str, domain: str = None) -> List[Memory]:
        """내용으로 기억 검색"""
        results = []
        domains_to_search = [domain] if domain else self.memories.keys()
        
        for d in domains_to_search:
            if d in self.memories:
                for memory in self.memories[d]:
                    if query.lower() in memory.content.lower():
                        results.append(memory)
        
        # 중요도 높은 순으로 정렬
        results.sort(key=lambda m: m.importance, reverse=True)
        return results
    
    def link_memories(self, memory1_id: int, memory2_id: int):
        """두 기억을 연결"""
        # 간단한 구현 (실제로는 더 복잡할 수 있음)
        pass
    
    def get_emotional_memory_profile(self, domain: str = "general") -> Dict:
        """도메인의 감정적 프로필"""
        if domain not in self.memories or not self.memories[domain]:
            return {
                'domain': domain,
                'total_memories': 0,
                'average_valence': 0.0
            }
        
        memories = self.memories[domain]
        total = len(memories)
        
        avg_valence = sum(m.emotional_valence for m in memories) / total if total > 0 else 0.0
        
        positive_count = len([m for m in memories if m.emotional_valence > 0.2])
        negative_count = len([m for m in memories if m.emotional_valence < -0.2])
        neutral_count = total - positive_count - negative_count
        
        return {
            'domain': domain,
            'total_memories': total,
            'average_valence': avg_valence,
            'emotional_distribution': {
                'positive': positive_count,
                'neutral': neutral_count,
                'negative': negative_count
            },
            'emotional_tendency': self._interpret_valence(avg_valence)
        }
    
    def _interpret_valence(self, valence: float) -> str:
        """감정 가중치 해석"""
        if valence > 0.5:
            return "Very Positive"
        elif valence > 0.2:
            return "Positive"
        elif valence > -0.2:
            return "Neutral"
        elif valence > -0.5:
            return "Negative"
        else:
            return "Very Negative"
    
    def get_statistics(self) -> Dict:
        """전체 기억 통계"""
        stats = {
            'total_memories': self.total_memories,
            'by_domain': {},
            'by_type': {
                'episodic': 0,
                'semantic': 0,
                'procedural': 0,
                'emotional': 0
            },
            'average_importance': 0.0
        }
        
        total_importance = 0.0
        
        for domain, memories in self.memories.items():
            stats['by_domain'][domain] = len(memories)
            
            for memory in memories:
                stats['by_type'][memory.memory_type.value] += 1
                total_importance += memory.importance
        
        if self.total_memories > 0:
            stats['average_importance'] = total_importance / self.total_memories
        
        return stats


# 테스트
if __name__ == "__main__":
    manager = MemoryManager()
    
    # 기억 저장
    m1 = manager.store(
        content="Uterine organoids successfully differentiated into endometrial epithelium",
        memory_type=MemoryType.EPISODIC,
        domain="biology",
        emotional_valence=0.8,  # 긍정적
        importance=0.9,
        associated_values=["achievement", "progress"]
    )
    
    m2 = manager.store(
        content="Portfolio allocation: 40% tech, 30% healthcare, 20% utilities, 10% bonds",
        memory_type=MemoryType.SEMANTIC,
        domain="finance",
        emotional_valence=0.3,
        importance=0.7,
        associated_values=["strategy", "balance"]
    )
    
    # 검색
    print("📚 Biology Memories:")
    for m in manager.retrieve("biology"):
        print(f"  • {m.content}")
    
    print("\n💰 Finance Memories:")
    for m in manager.retrieve("finance"):
        print(f"  • {m.content}")
    
    # 감정 프로필
    print("\n❤️ Biology Emotional Profile:")
    profile = manager.get_emotional_memory_profile("biology")
    print(f"  Average valence: {profile['average_valence']:.2f}")
    print(f"  Tendency: {profile['emotional_tendency']}")
    
    # 통계
    print("\n📊 Statistics:")
    stats = manager.get_statistics()
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Average importance: {stats['average_importance']:.2f}")
