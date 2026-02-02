"""
Brain Structure Modeling & Playback System
뇌 구조를 모델링하고 재생/시각화하는 시스템
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class NeuralRegion(Enum):
    """신경 부위"""
    BRAINSTEM = "brainstem"
    LIMBIC = "limbic_system"
    NEOCORTEX = "neocortex"
    CARTRIDGES = "cartridges"
    EXECUTION = "execution"


@dataclass
class NeuralActivity:
    """신경 활동"""
    region: NeuralRegion
    component: str
    activity_type: str  # "activation", "inhibition", "modulation"
    intensity: float  # 0.0 ~ 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)


@dataclass
class BrainState:
    """뇌 상태 스냅샷"""
    timestamp: datetime
    brainstem_state: Dict
    limbic_state: Dict
    neocortex_state: Dict
    cartridge_state: Dict
    execution_state: Dict
    active_processes: List[str]
    total_intensity: float


class BrainStructureModel:
    """
    뇌 구조 모델
    신경 부위별 활동을 추적하고 모니터링
    """
    
    def __init__(self):
        """초기화"""
        self.brain_structure = {
            "brainstem": {
                "ethics_engine": {"active": False, "intensity": 0.0},
                "reasoning_engine": {"active": False, "intensity": 0.0},
                "awareness_monitor": {"active": False, "intensity": 0.0}
            },
            "limbic_system": {
                "memory_manager": {"active": False, "intensity": 0.0},
                "emotion_processor": {"active": False, "intensity": 0.0},
                "value_assessment": {"active": False, "intensity": 0.0}
            },
            "neocortex": {
                "prefrontal_cortex": {"active": False, "intensity": 0.0},
                "temporal_cortex": {"active": False, "intensity": 0.0},
                "parietal_cortex": {"active": False, "intensity": 0.0},
                "occipital_cortex": {"active": False, "intensity": 0.0}
            },
            "cartridges": {
                "bio_cartridge": {"active": False, "intensity": 0.0},
                "quant_cartridge": {"active": False, "intensity": 0.0},
                "astro_cartridge": {"active": False, "intensity": 0.0},
                "lit_cartridge": {"active": False, "intensity": 0.0}
            },
            "execution": {
                "execution_framework": {"active": False, "intensity": 0.0}
            }
        }
        
        self.activity_log: List[NeuralActivity] = []
        self.state_history: List[BrainState] = []
    
    def activate_component(
        self,
        region: str,
        component: str,
        intensity: float = 0.8
    ) -> bool:
        """컴포넌트 활성화"""
        if region not in self.brain_structure:
            return False
        
        if component not in self.brain_structure[region]:
            return False
        
        self.brain_structure[region][component]["active"] = True
        self.brain_structure[region][component]["intensity"] = intensity
        
        # 활동 기록
        activity = NeuralActivity(
            region=NeuralRegion(region),
            component=component,
            activity_type="activation",
            intensity=intensity
        )
        self.activity_log.append(activity)
        
        return True
    
    def deactivate_component(self, region: str, component: str) -> bool:
        """컴포넌트 비활성화"""
        if region not in self.brain_structure:
            return False
        
        if component not in self.brain_structure[region]:
            return False
        
        self.brain_structure[region][component]["active"] = False
        self.brain_structure[region][component]["intensity"] = 0.0
        
        # 활동 기록
        activity = NeuralActivity(
            region=NeuralRegion(region),
            component=component,
            activity_type="deactivation",
            intensity=0.0
        )
        self.activity_log.append(activity)
        
        return True
    
    def get_active_components(self) -> List[Tuple[str, str, float]]:
        """활성 컴포넌트 조회"""
        active = []
        
        for region, components in self.brain_structure.items():
            for component, state in components.items():
                if state["active"]:
                    active.append((region, component, state["intensity"]))
        
        return active
    
    def get_brain_state(self) -> BrainState:
        """현재 뇌 상태 조회"""
        state = BrainState(
            timestamp=datetime.now(),
            brainstem_state=self.brain_structure["brainstem"].copy(),
            limbic_state=self.brain_structure["limbic_system"].copy(),
            neocortex_state=self.brain_structure["neocortex"].copy(),
            cartridge_state=self.brain_structure["cartridges"].copy(),
            execution_state=self.brain_structure["execution"].copy(),
            active_processes=[f"{r}:{c}" for r, c, _ in self.get_active_components()],
            total_intensity=sum(s["intensity"] for r in self.brain_structure.values() for s in r.values())
        )
        
        self.state_history.append(state)
        return state
    
    def get_state_history(self, limit: int = 10) -> List[BrainState]:
        """상태 히스토리 조회"""
        return self.state_history[-limit:]


class BrainPlaybackSystem:
    """
    뇌 구조 재생 시스템
    기록된 활동을 재생하고 시각화
    """
    
    def __init__(self, model: BrainStructureModel):
        """초기화"""
        self.model = model
        self.playback_speed = 1.0
        self.is_playing = False
        self.playback_position = 0
    
    def record_scenario(
        self,
        name: str,
        scenario_steps: List[Dict]
    ) -> Dict:
        """시나리오 기록"""
        """
        시나리오 예:
        [
            {"action": "activate", "region": "brainstem", "component": "ethics_engine", "intensity": 0.9},
            {"action": "activate", "region": "limbic_system", "component": "memory_manager", "intensity": 0.7},
            {"action": "activate", "region": "neocortex", "component": "prefrontal_cortex", "intensity": 0.8},
        ]
        """
        
        scenario = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "steps": scenario_steps,
            "duration_steps": len(scenario_steps)
        }
        
        return scenario
    
    def playback_scenario(
        self,
        scenario: Dict,
        verbose: bool = True
    ) -> List[BrainState]:
        """시나리오 재생"""
        
        states = []
        
        for i, step in enumerate(scenario["steps"]):
            action = step.get("action")
            region = step.get("region")
            component = step.get("component")
            intensity = step.get("intensity", 0.8)
            
            if verbose:
                print(f"Step {i+1}: {action} {region}:{component}")
            
            if action == "activate":
                self.model.activate_component(region, component, intensity)
            elif action == "deactivate":
                self.model.deactivate_component(region, component)
            
            # 현재 상태 기록
            state = self.model.get_brain_state()
            states.append(state)
        
        return states
    
    def visualize_state(self, state: BrainState) -> str:
        """뇌 상태 시각화"""
        
        visualization = f"""
╔════════════════════════════════════════════════════════════╗
║          🧠 BRAIN STATE VISUALIZATION 🧠                  ║
╚════════════════════════════════════════════════════════════╝

⏰ Timestamp: {state.timestamp.strftime('%H:%M:%S')}

📊 BRAINSTEM (불변 윤리 중추):
   Ethics Engine:      {'█' * int(state.brainstem_state['ethics_engine']['intensity'] * 10)} {state.brainstem_state['ethics_engine']['intensity']:.1f}
   Reasoning Engine:   {'█' * int(state.brainstem_state['reasoning_engine']['intensity'] * 10)} {state.brainstem_state['reasoning_engine']['intensity']:.1f}
   Awareness Monitor:  {'█' * int(state.brainstem_state['awareness_monitor']['intensity'] * 10)} {state.brainstem_state['awareness_monitor']['intensity']:.1f}

🎭 LIMBIC SYSTEM (감정-가치 중추):
   Memory Manager:     {'█' * int(state.limbic_state['memory_manager']['intensity'] * 10)} {state.limbic_state['memory_manager']['intensity']:.1f}
   Emotion Processor:  {'█' * int(state.limbic_state['emotion_processor']['intensity'] * 10)} {state.limbic_state['emotion_processor']['intensity']:.1f}
   Value Assessment:   {'█' * int(state.limbic_state['value_assessment']['intensity'] * 10)} {state.limbic_state['value_assessment']['intensity']:.1f}

🧬 NEOCORTEX (인지 중추):
   Prefrontal Cortex:  {'█' * int(state.neocortex_state['prefrontal_cortex']['intensity'] * 10)} {state.neocortex_state['prefrontal_cortex']['intensity']:.1f}
   Temporal Cortex:    {'█' * int(state.neocortex_state['temporal_cortex']['intensity'] * 10)} {state.neocortex_state['temporal_cortex']['intensity']:.1f}
   Parietal Cortex:    {'█' * int(state.neocortex_state['parietal_cortex']['intensity'] * 10)} {state.neocortex_state['parietal_cortex']['intensity']:.1f}
   Occipital Cortex:   {'█' * int(state.neocortex_state['occipital_cortex']['intensity'] * 10)} {state.neocortex_state['occipital_cortex']['intensity']:.1f}

💾 CARTRIDGES (도메인 전문성):
   Bio Cartridge:      {'█' * int(state.cartridge_state['bio_cartridge']['intensity'] * 10)} {state.cartridge_state['bio_cartridge']['intensity']:.1f}
   Quant Cartridge:    {'█' * int(state.cartridge_state['quant_cartridge']['intensity'] * 10)} {state.cartridge_state['quant_cartridge']['intensity']:.1f}
   Astro Cartridge:    {'█' * int(state.cartridge_state['astro_cartridge']['intensity'] * 10)} {state.cartridge_state['astro_cartridge']['intensity']:.1f}
   Lit Cartridge:      {'█' * int(state.cartridge_state['lit_cartridge']['intensity'] * 10)} {state.cartridge_state['lit_cartridge']['intensity']:.1f}

⚙️ EXECUTION (행동 실행):
   Execution Framework:{'█' * int(state.execution_state['execution_framework']['intensity'] * 10)} {state.execution_state['execution_framework']['intensity']:.1f}

📈 METRICS:
   Active Processes: {len(state.active_processes)}
   Total Intensity: {state.total_intensity:.2f}
   Active: {', '.join(state.active_processes) if state.active_processes else 'None'}

╚════════════════════════════════════════════════════════════╝
"""
        return visualization


# 테스트 시나리오
if __name__ == "__main__":
    print("🧠 Brain Structure Modeling & Playback System Test\n")
    
    # 1. 모델 생성
    print("1️⃣ Creating Brain Model...")
    model = BrainStructureModel()
    print("✅ Brain Model created\n")
    
    # 2. 재생 시스템 생성
    print("2️⃣ Creating Playback System...")
    playback = BrainPlaybackSystem(model)
    print("✅ Playback System created\n")
    
    # 3. 시나리오 생성: "윤리 검증 + 의사결정 프로세스"
    print("3️⃣ Creating Scenario: Ethical Decision Making")
    scenario1 = playback.record_scenario(
        "Ethical Decision Making Process",
        [
            {"action": "activate", "region": "brainstem", "component": "ethics_engine", "intensity": 0.95},
            {"action": "activate", "region": "brainstem", "component": "reasoning_engine", "intensity": 0.9},
            {"action": "activate", "region": "limbic_system", "component": "value_assessment", "intensity": 0.8},
            {"action": "activate", "region": "neocortex", "component": "prefrontal_cortex", "intensity": 0.85},
            {"action": "activate", "region": "execution", "component": "execution_framework", "intensity": 0.7}
        ]
    )
    print(f"✅ Scenario created: {scenario1['name']}\n")
    
    # 4. 시나리오 재생
    print("4️⃣ Playing back scenario...")
    states = playback.playback_scenario(scenario1)
    print(f"✅ Played {len(states)} steps\n")
    
    # 5. 최종 상태 시각화
    print("5️⃣ Final Brain State:")
    final_state = states[-1]
    visualization = playback.visualize_state(final_state)
    print(visualization)
    
    # 6. 다른 시나리오: "생물학 연구 모드"
    print("\n6️⃣ Creating Scenario: Biology Research Mode")
    scenario2 = playback.record_scenario(
        "Biology Research Analysis",
        [
            {"action": "activate", "region": "brainstem", "component": "reasoning_engine", "intensity": 0.85},
            {"action": "activate", "region": "limbic_system", "component": "memory_manager", "intensity": 0.9},
            {"action": "activate", "region": "cartridges", "component": "bio_cartridge", "intensity": 0.95},
            {"action": "activate", "region": "neocortex", "component": "temporal_cortex", "intensity": 0.8},
            {"action": "activate", "region": "neocortex", "component": "parietal_cortex", "intensity": 0.75}
        ]
    )
    
    states2 = playback.playback_scenario(scenario2)
    print(f"\n7️⃣ Biology Mode - Final State:")
    visualization2 = playback.visualize_state(states2[-1])
    print(visualization2)
    
    # 7. 금융 분석 모드
    print("\n8️⃣ Creating Scenario: Financial Analysis Mode")
    scenario3 = playback.record_scenario(
        "Financial Analysis & Decision",
        [
            {"action": "activate", "region": "brainstem", "component": "reasoning_engine", "intensity": 0.9},
            {"action": "activate", "region": "limbic_system", "component": "value_assessment", "intensity": 0.85},
            {"action": "activate", "region": "cartridges", "component": "quant_cartridge", "intensity": 0.95},
            {"action": "activate", "region": "neocortex", "component": "prefrontal_cortex", "intensity": 0.9},
            {"action": "activate", "region": "execution", "component": "execution_framework", "intensity": 0.8}
        ]
    )
    
    states3 = playback.playback_scenario(scenario3)
    print(f"\n9️⃣ Finance Mode - Final State:")
    visualization3 = playback.visualize_state(states3[-1])
    print(visualization3)
    
    print("\n✅ Brain Structure Modeling & Playback System Test Complete!")
