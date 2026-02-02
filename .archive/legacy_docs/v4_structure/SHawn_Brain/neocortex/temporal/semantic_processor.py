"""
SemanticProcessor - Temporal Cortex의 의미 처리
개념 간 관계 매핑, 맥락 이해, 패턴 인식
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class Concept:
    """개념"""
    name: str
    domain: str
    definition: str
    related_concepts: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    abstraction_level: float = 0.5  # 0: 구체적 ~ 1: 추상적


@dataclass
class Relationship:
    """개념 간 관계"""
    source: str
    target: str
    relation_type: str  # "is_part_of", "is_related_to", "causes", "follows"
    strength: float = 0.5  # 0 ~ 1
    bidirectional: bool = False


class SemanticProcessor:
    """
    의미 처리 시스템
    - 개념 간 관계 매핑
    - 맥락 이해
    - 패턴 인식
    - 역사적 맥락 통합
    """
    
    def __init__(self):
        """시맨틱 프로세서 초기화"""
        self.concepts: Dict[str, Concept] = {}
        self.relationships: List[Relationship] = []
        self.context_history: List[Dict] = []
        self.pattern_library: Dict[str, List[str]] = defaultdict(list)
    
    def add_concept(
        self,
        name: str,
        domain: str,
        definition: str,
        abstraction_level: float = 0.5
    ) -> Concept:
        """개념 추가"""
        concept = Concept(
            name=name,
            domain=domain,
            definition=definition,
            abstraction_level=abstraction_level
        )
        self.concepts[name] = concept
        return concept
    
    def link_concepts(
        self,
        source: str,
        target: str,
        relation_type: str,
        strength: float = 0.5,
        bidirectional: bool = False
    ):
        """개념 연결"""
        relationship = Relationship(
            source=source,
            target=target,
            relation_type=relation_type,
            strength=strength,
            bidirectional=bidirectional
        )
        self.relationships.append(relationship)
        
        # 개념에 추가
        if source in self.concepts:
            if target not in self.concepts[source].related_concepts:
                self.concepts[source].related_concepts.append(target)
        
        if bidirectional and target in self.concepts:
            if source not in self.concepts[target].related_concepts:
                self.concepts[target].related_concepts.append(source)
    
    def understand_context(
        self,
        text: str,
        domain: str = "general"
    ) -> Dict:
        """맥락 이해"""
        # 텍스트에서 개념 추출 (간단한 구현)
        concepts_found = []
        for concept_name in self.concepts.keys():
            if concept_name.lower() in text.lower():
                concepts_found.append(concept_name)
        
        # 관계 분석
        relationships_found = []
        for rel in self.relationships:
            if rel.source in concepts_found and rel.target in concepts_found:
                relationships_found.append({
                    'source': rel.source,
                    'target': rel.target,
                    'type': rel.relation_type
                })
        
        context = {
            'text': text[:100] + "..." if len(text) > 100 else text,
            'domain': domain,
            'concepts_identified': concepts_found,
            'relationships_identified': relationships_found,
            'timestamp': datetime.now().isoformat()
        }
        
        self.context_history.append(context)
        return context
    
    def recognize_pattern(
        self,
        concept_sequence: List[str]
    ) -> Optional[str]:
        """패턴 인식"""
        pattern_key = " → ".join(concept_sequence)
        
        if pattern_key not in self.pattern_library:
            self.pattern_library[pattern_key] = concept_sequence
            return "new_pattern_recorded"
        else:
            return "pattern_recognized"
    
    def get_semantic_network(self, domain: str = None) -> Dict:
        """시맨틱 네트워크 조회"""
        if domain:
            domain_concepts = {
                name: concept for name, concept in self.concepts.items()
                if concept.domain == domain
            }
        else:
            domain_concepts = self.concepts
        
        return {
            'concepts': len(domain_concepts),
            'relationships': len(self.relationships),
            'domains_covered': len(set(c.domain for c in self.concepts.values()))
        }


# 테스트
if __name__ == "__main__":
    processor = SemanticProcessor()
    
    # 개념 추가
    processor.add_concept("organoid", "biology", "Self-organizing tissue structure")
    processor.add_concept("stem_cell", "biology", "Undifferentiated cell with potential")
    processor.add_concept("differentiation", "biology", "Process of cell specialization")
    
    # 관계 연결
    processor.link_concepts("stem_cell", "differentiation", "causes", 0.9, True)
    processor.link_concepts("differentiation", "organoid", "leads_to", 0.8)
    
    # 맥락 이해
    context = processor.understand_context(
        "Stem cells undergo differentiation to form organoid structures",
        domain="biology"
    )
    print(f"✅ Context understood: {context['concepts_identified']}")
    
    # 패턴 인식
    pattern = processor.recognize_pattern(["stem_cell", "differentiation", "organoid"])
    print(f"✅ Pattern: {pattern}")
    
    # 네트워크
    network = processor.get_semantic_network("biology")
    print(f"✅ Network: {network['concepts']} concepts")
