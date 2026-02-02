"""
지식 그래프 & 관계 분석 - 엔티티 연결 관리

역할:
- 엔티티 관계 추적
- 지식 그래프 구축
- 네트워크 분석
- 인사이트 도출
"""

from typing import Dict, Any, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    """지식 그래프 엔티티"""
    id: str
    name: str
    entity_type: str  # person, company, product, concept
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    """관계"""
    source_id: str
    target_id: str
    relation_type: str  # owns, manages, related_to, etc
    strength: float  # 0-1
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class KnowledgeGraph:
    """지식 그래프"""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.analytics_cache = {}
    
    def add_entity(
        self,
        entity_id: str,
        name: str,
        entity_type: str,
        properties: Dict = None
    ) -> Entity:
        """엔티티 추가"""
        
        entity = Entity(
            id=entity_id,
            name=name,
            entity_type=entity_type,
            properties=properties or {}
        )
        
        self.entities[entity_id] = entity
        return entity
    
    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        strength: float = 1.0,
        properties: Dict = None
    ) -> Optional[Relationship]:
        """관계 추가"""
        
        if source_id not in self.entities or target_id not in self.entities:
            return None
        
        relationship = Relationship(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=min(1.0, max(0.0, strength)),
            properties=properties or {}
        )
        
        self.relationships.append(relationship)
        return relationship
    
    def get_entity_connections(self, entity_id: str) -> Dict[str, List[str]]:
        """엔티티 연결 조회"""
        
        incoming = []
        outgoing = []
        
        for rel in self.relationships:
            if rel.source_id == entity_id:
                outgoing.append(f"{rel.target_id} ({rel.relation_type})")
            elif rel.target_id == entity_id:
                incoming.append(f"{rel.source_id} ({rel.relation_type})")
        
        return {
            'incoming': incoming,
            'outgoing': outgoing,
            'total_connections': len(incoming) + len(outgoing)
        }
    
    def find_path(self, source_id: str, target_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """경로 찾기 (BFS)"""
        
        if source_id not in self.entities or target_id not in self.entities:
            return None
        
        from collections import deque
        
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            if current == target_id:
                return path
            
            # 다음 노드 탐색
            for rel in self.relationships:
                if rel.source_id == current and rel.target_id not in visited:
                    visited.add(rel.target_id)
                    queue.append((rel.target_id, path + [rel.target_id]))
        
        return None
    
    def get_network_centrality(self) -> Dict[str, float]:
        """네트워크 중심성 계산 (학위 중심성)"""
        
        centrality = {}
        
        for entity_id in self.entities.keys():
            degree = sum(1 for rel in self.relationships 
                        if rel.source_id == entity_id or rel.target_id == entity_id)
            centrality[entity_id] = degree
        
        # 정규화
        max_degree = max(centrality.values()) if centrality else 1
        centrality = {k: v / max_degree for k, v in centrality.items()}
        
        return centrality
    
    def detect_communities(self) -> Dict[str, List[str]]:
        """커뮤니티 감지 (간단한 구현)"""
        
        communities = {}
        visited = set()
        community_id = 0
        
        for entity_id in self.entities.keys():
            if entity_id not in visited:
                # BFS로 연결된 컴포넌트 찾기
                community = []
                from collections import deque
                
                queue = deque([entity_id])
                visited.add(entity_id)
                
                while queue:
                    current = queue.popleft()
                    community.append(current)
                    
                    for rel in self.relationships:
                        if rel.source_id == current and rel.target_id not in visited:
                            visited.add(rel.target_id)
                            queue.append(rel.target_id)
                        elif rel.target_id == current and rel.source_id not in visited:
                            visited.add(rel.source_id)
                            queue.append(rel.source_id)
                
                communities[f"community_{community_id}"] = community
                community_id += 1
        
        return communities
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """그래프 통계"""
        
        entity_types = {}
        for entity in self.entities.values():
            if entity.entity_type not in entity_types:
                entity_types[entity.entity_type] = 0
            entity_types[entity.entity_type] += 1
        
        relation_types = {}
        for rel in self.relationships:
            if rel.relation_type not in relation_types:
                relation_types[rel.relation_type] = 0
            relation_types[rel.relation_type] += 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_entities': len(self.entities),
            'total_relationships': len(self.relationships),
            'entity_types': entity_types,
            'relation_types': relation_types,
            'avg_connections': len(self.relationships) * 2 / len(self.entities) if self.entities else 0,
            'communities': len(self.detect_communities())
        }


class RelationshipAnalyzer:
    """관계 분석기"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.kg = knowledge_graph
    
    def analyze_influence(self, entity_id: str) -> Dict[str, Any]:
        """영향력 분석"""
        
        centrality = self.kg.get_network_centrality()
        connections = self.kg.get_entity_connections(entity_id)
        
        entity = self.kg.entities.get(entity_id)
        
        return {
            'entity_id': entity_id,
            'entity_name': entity.name if entity else 'Unknown',
            'centrality_score': centrality.get(entity_id, 0),
            'direct_connections': connections['total_connections'],
            'influence_level': self._determine_influence(centrality.get(entity_id, 0))
        }
    
    def _determine_influence(self, centrality: float) -> str:
        """영향력 수준 결정"""
        if centrality > 0.8:
            return 'very_high'
        elif centrality > 0.6:
            return 'high'
        elif centrality > 0.4:
            return 'medium'
        elif centrality > 0.2:
            return 'low'
        else:
            return 'minimal'
    
    def find_related_entities(
        self,
        entity_id: str,
        depth: int = 2
    ) -> List[Tuple[str, float]]:
        """관련 엔티티 찾기"""
        
        related = set()
        visited = {entity_id}
        
        def explore(current_id, current_depth):
            if current_depth > depth:
                return
            
            for rel in self.kg.relationships:
                if rel.source_id == current_id and rel.target_id not in visited:
                    visited.add(rel.target_id)
                    related.add((rel.target_id, rel.strength))
                    explore(rel.target_id, current_depth + 1)
                
                elif rel.target_id == current_id and rel.source_id not in visited:
                    visited.add(rel.source_id)
                    related.add((rel.source_id, rel.strength))
                    explore(rel.source_id, current_depth + 1)
        
        explore(entity_id, 1)
        
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def get_analysis_report(self) -> Dict[str, Any]:
        """분석 리포트"""
        
        centrality = self.kg.get_network_centrality()
        communities = self.kg.detect_communities()
        
        top_entities = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'graph_stats': self.kg.get_graph_statistics(),
            'top_entities': [
                {
                    'id': eid,
                    'name': self.kg.entities[eid].name,
                    'centrality': score
                }
                for eid, score in top_entities
            ],
            'communities': communities,
            'network_density': len(self.kg.relationships) / (len(self.kg.entities) * (len(self.kg.entities) - 1) / 2) if len(self.kg.entities) > 1 else 0
        }


if __name__ == "__main__":
    print("🔗 지식 그래프 테스트\n")
    
    kg = KnowledgeGraph()
    
    # 엔티티 생성
    kg.add_entity("person_1", "Alice", "person", {"role": "CEO"})
    kg.add_entity("person_2", "Bob", "person", {"role": "CTO"})
    kg.add_entity("company_1", "TechCorp", "company", {"industry": "AI"})
    kg.add_entity("product_1", "SHawn-Brain", "product", {"version": "5.3"})
    
    # 관계 추가
    kg.add_relationship("person_1", "company_1", "manages", 0.95)
    kg.add_relationship("person_2", "company_1", "works_for", 0.90)
    kg.add_relationship("company_1", "product_1", "produces", 0.99)
    kg.add_relationship("person_1", "person_2", "collaborates_with", 0.85)
    
    print("✅ 그래프 구축 완료!")
    
    # 분석
    analyzer = RelationshipAnalyzer(kg)
    report = analyzer.get_analysis_report()
    
    print(f"✅ 분석 완료!")
    print(f"엔티티: {report['graph_stats']['total_entities']}")
    print(f"관계: {report['graph_stats']['total_relationships']}")
    print(f"커뮤니티: {report['graph_stats']['communities']}")
