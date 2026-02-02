"""
VisualizationEngine - Occipital Cortex의 시각화 및 상상
정신적 모델 구성, 시나리오 생성, 미래 예측
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ScenarioType(Enum):
    """시나리오 종류"""
    OPTIMISTIC = "optimistic"      # 최선의 경우
    PESSIMISTIC = "pessimistic"    # 최악의 경우
    REALISTIC = "realistic"        # 현실적
    EXPLORATORY = "exploratory"    # 탐색적


@dataclass
class MentalModel:
    """정신적 모델"""
    name: str
    domain: str
    components: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    visualization: str = ""  # ASCII/텍스트 표현


@dataclass
class Scenario:
    """미래 시나리오"""
    name: str
    scenario_type: ScenarioType
    preconditions: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    outcome: str = ""
    probability: float = 0.5


class VisualizationEngine:
    """
    시각화 및 상상 엔진
    - 정신적 모델 구성
    - 시나리오 생성
    - 미래 예측
    - 추상화 능력
    """
    
    def __init__(self):
        """시각화 엔진 초기화"""
        self.mental_models: Dict[str, MentalModel] = {}
        self.scenarios: List[Scenario] = []
        self.future_predictions: List[Dict] = []
    
    def create_mental_model(
        self,
        name: str,
        domain: str,
        components: List[str]
    ) -> MentalModel:
        """정신적 모델 생성"""
        model = MentalModel(
            name=name,
            domain=domain,
            components=components
        )
        self.mental_models[name] = model
        return model
    
    def generate_scenario(
        self,
        name: str,
        scenario_type: ScenarioType,
        initial_state: str,
        events: List[str],
        num_steps: int = 5
    ) -> Scenario:
        """시나리오 생성"""
        scenario = Scenario(
            name=name,
            scenario_type=scenario_type,
            preconditions=[initial_state],
            events=events[:num_steps]
        )
        
        # 결과 예측
        if scenario_type == ScenarioType.OPTIMISTIC:
            scenario.outcome = "Positive outcome with benefits"
            scenario.probability = 0.3
        elif scenario_type == ScenarioType.PESSIMISTIC:
            scenario.outcome = "Negative outcome with challenges"
            scenario.probability = 0.2
        elif scenario_type == ScenarioType.REALISTIC:
            scenario.outcome = "Mixed outcome with trade-offs"
            scenario.probability = 0.4
        else:  # EXPLORATORY
            scenario.outcome = "Unexpected outcome with new insights"
            scenario.probability = 0.1
        
        self.scenarios.append(scenario)
        return scenario
    
    def predict_future(
        self,
        current_state: Dict,
        time_horizon: int = 12  # 개월
    ) -> Dict:
        """미래 예측"""
        prediction = {
            'current_state': current_state,
            'time_horizon_months': time_horizon,
            'predicted_states': [],
            'confidence': 0.0
        }
        
        # 단순 외삽법
        for month in range(1, time_horizon + 1):
            # 기존 데이터에서 추세 계산 (간단한 예)
            state = {
                'month': month,
                'confidence': max(0.1, 0.9 - (month * 0.05))  # 시간이 지나면서 신뢰도 감소
            }
            prediction['predicted_states'].append(state)
        
        avg_confidence = sum(s['confidence'] for s in prediction['predicted_states'])
        prediction['confidence'] = avg_confidence / max(1, len(prediction['predicted_states']))
        
        self.future_predictions.append(prediction)
        return prediction
    
    def visualize_model(self, model_name: str) -> str:
        """모델 시각화"""
        if model_name not in self.mental_models:
            return "Model not found"
        
        model = self.mental_models[model_name]
        
        # ASCII 시각화
        visualization = f"""
╔══════════════════════════════════╗
║  Mental Model: {model.name:20s} ║
╚══════════════════════════════════╝

Domain: {model.domain}

Components:
"""
        for i, component in enumerate(model.components, 1):
            visualization += f"  {i}. {component}\n"
        
        if model.relationships:
            visualization += "\nRelationships:\n"
            for source, targets in model.relationships.items():
                for target in targets:
                    visualization += f"  {source} → {target}\n"
        
        return visualization
    
    def explore_possibilities(
        self,
        starting_point: str,
        depth: int = 3
    ) -> List[str]:
        """가능성 탐색"""
        possibilities = [starting_point]
        
        for _ in range(depth):
            new_possibilities = []
            for possibility in possibilities[-5:]:  # 최근 5개만 사용
                # 각 가능성에서 2개의 분기
                for i in range(2):
                    new_poss = f"{possibility} → variant_{i+1}"
                    new_possibilities.append(new_poss)
            
            possibilities.extend(new_possibilities)
        
        return list(set(possibilities))


# 테스트
if __name__ == "__main__":
    engine = VisualizationEngine()
    
    # 정신적 모델 생성
    print("1️⃣ Creating mental model:")
    model = engine.create_mental_model(
        name="Organoid Development",
        domain="biology",
        components=["Stem Cells", "Growth Medium", "Differentiation", "Maturation"]
    )
    print(engine.visualize_model("Organoid Development"))
    
    # 시나리오 생성
    print("\n2️⃣ Generating scenarios:")
    scenario1 = engine.generate_scenario(
        name="Successful Development",
        scenario_type=ScenarioType.OPTIMISTIC,
        initial_state="High quality stem cells",
        events=["Optimal growth", "Perfect differentiation", "Full maturation"]
    )
    print(f"  ✅ {scenario1.name}: {scenario1.outcome}")
    
    # 미래 예측
    print("\n3️⃣ Future prediction:")
    prediction = engine.predict_future(
        current_state={"status": "initialization", "progress": 0},
        time_horizon=6
    )
    print(f"  Months: {len(prediction['predicted_states'])}")
    print(f"  Average confidence: {prediction['confidence']:.2f}")
    
    # 가능성 탐색
    print("\n4️⃣ Exploring possibilities:")
    possibilities = engine.explore_possibilities("Research begins", depth=2)
    print(f"  Generated {len(possibilities)} possibilities")
    
    print("\n✅ VisualizationEngine working!")
