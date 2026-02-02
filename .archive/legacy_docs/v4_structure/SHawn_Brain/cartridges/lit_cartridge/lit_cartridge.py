"""
LiteratureCartridge - 문학과 철학 카트리지
문학 작품 분석, 철학 개념 처리, 텍스트 해석
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LiteraryWork:
    """문학 작품"""
    title: str
    author: str
    period: str
    genre: str
    themes: List[str] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    cultural_impact: float = 0.5


@dataclass
class PhilosophicalConcept:
    """철학 개념"""
    name: str
    tradition: str  # Western, Eastern, etc
    time_period: str
    definition: str
    related_concepts: List[str] = field(default_factory=list)
    relevance: float = 0.5


class LiteratureCartridge:
    """
    문학과 철학 카트리지
    - 문학 작품 분석
    - 철학 개념 처리
    - 텍스트 해석
    - 문화적 맥락
    """
    
    def __init__(self):
        """문학 카트리지 초기화"""
        self.domain = "literature"
        self.expertise_level = 0.70
        
        # 기본 작품 라이브러리
        self.works: Dict[str, LiteraryWork] = {
            "one_hundred_years": LiteraryWork(
                title="One Hundred Years of Solitude",
                author="Gabriel García Márquez",
                period="20th century",
                genre="magical realism",
                themes=["solitude", "cyclical time", "family saga"],
                key_concepts=["magical realism", "cyclical narrative", "multigeneration"]
            ),
            "brothers_karamazov": LiteraryWork(
                title="The Brothers Karamazov",
                author="Fyodor Dostoevsky",
                period="19th century",
                genre="philosophical novel",
                themes=["faith", "suffering", "morality"],
                key_concepts=["existentialism", "theodicy", "moral choice"]
            ),
            "kafka_metamorphosis": LiteraryWork(
                title="The Metamorphosis",
                author="Franz Kafka",
                period="20th century",
                genre="surrealist",
                themes=["alienation", "absurdity", "transformation"],
                key_concepts=["absurdism", "bureaucracy", "existential dread"]
            )
        }
        
        # 철학 개념 라이브러리
        self.concepts: Dict[str, PhilosophicalConcept] = {
            "existentialism": PhilosophicalConcept(
                name="Existentialism",
                tradition="Western",
                time_period="20th century",
                definition="Philosophy emphasizing individual existence and freedom",
                related_concepts=["freedom", "authenticity", "absurdity"]
            ),
            "phenomenology": PhilosophicalConcept(
                name="Phenomenology",
                tradition="Western",
                time_period="20th century",
                definition="Study of consciousness and intentionality",
                related_concepts=["consciousness", "being", "experience"]
            ),
            "taoism": PhilosophicalConcept(
                name="Taoism",
                tradition="Eastern",
                time_period="Ancient China",
                definition="Philosophy of harmony with the Tao (way)",
                related_concepts=["yin-yang", "wu-wei", "naturalness"]
            )
        }
    
    def analyze_work(self, work_key: str) -> Dict:
        """문학 작품 분석"""
        if work_key not in self.works:
            return {"error": f"Work not found: {work_key}"}
        
        work = self.works[work_key]
        
        return {
            'title': work.title,
            'author': work.author,
            'period': work.period,
            'genre': work.genre,
            'themes': work.themes,
            'key_concepts': work.key_concepts,
            'cultural_impact': work.cultural_impact,
            'analysis_depth': 'detailed'
        }
    
    def explain_concept(self, concept_key: str) -> Dict:
        """철학 개념 설명"""
        if concept_key not in self.concepts:
            return {"error": f"Concept not found: {concept_key}"}
        
        concept = self.concepts[concept_key]
        
        return {
            'name': concept.name,
            'tradition': concept.tradition,
            'time_period': concept.time_period,
            'definition': concept.definition,
            'related_concepts': concept.related_concepts,
            'relevance': concept.relevance
        }
    
    def interpret_text(self, text: str, context: str = "general") -> Dict:
        """텍스트 해석"""
        # 간단한 키워드 분석
        text_lower = text.lower()
        
        relevant_themes = []
        for work in self.works.values():
            for theme in work.themes:
                if theme.lower() in text_lower:
                    relevant_themes.append(theme)
        
        relevant_concepts = []
        for concept in self.concepts.values():
            if concept.name.lower() in text_lower:
                relevant_concepts.append(concept.name)
        
        return {
            'context': context,
            'text_length': len(text),
            'relevant_themes': list(set(relevant_themes)),
            'relevant_concepts': list(set(relevant_concepts)),
            'interpretation_confidence': min(0.9, max(0.3, len(relevant_concepts) * 0.2)),
            'depth': 'symbolic' if relevant_concepts else 'literal'
        }
    
    def get_literary_context(self, period: str) -> Dict:
        """문학적 맥락 제공"""
        works_in_period = [
            w for w in self.works.values()
            if period.lower() in w.period.lower()
        ]
        
        return {
            'period': period,
            'works_count': len(works_in_period),
            'major_works': [w.title for w in works_in_period],
            'characteristic_genres': list(set(w.genre for w in works_in_period))
        }
    
    def activate(self) -> str:
        """카트리지 활성화"""
        return f"Literature Cartridge activated: {self.expertise_level:.0%} expertise"


# 테스트
if __name__ == "__main__":
    cartridge = LiteratureCartridge()
    
    print("🧪 LiteratureCartridge Test\n")
    
    # 1. 카트리지 활성화
    print(f"1️⃣ Activation: {cartridge.activate()}")
    
    # 2. 작품 분석
    print("\n2️⃣ Analyzing work:")
    analysis = cartridge.analyze_work("kafka_metamorphosis")
    print(f"  Title: {analysis['title']}")
    print(f"  Themes: {', '.join(analysis['themes'])}")
    
    # 3. 개념 설명
    print("\n3️⃣ Explaining concept:")
    concept = cartridge.explain_concept("existentialism")
    print(f"  Concept: {concept['name']}")
    print(f"  Definition: {concept['definition']}")
    
    # 4. 텍스트 해석
    print("\n4️⃣ Interpreting text:")
    interpretation = cartridge.interpret_text(
        "The protagonist struggles with alienation and absurdity",
        context="modernist literature"
    )
    print(f"  Relevant themes: {interpretation['relevant_themes']}")
    print(f"  Confidence: {interpretation['interpretation_confidence']:.0%}")
    
    print("\n✅ LiteratureCartridge working!")
