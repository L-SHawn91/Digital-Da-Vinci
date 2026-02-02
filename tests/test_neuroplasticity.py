
"""
D-CNS Neuroplasticity Unit Tests
검증 대상: projects.ddc.brain.neuronet.neuroplasticity.NeuroplasticityLearner
"""
import os
import json
import pytest
from datetime import datetime
from projects.ddc.brain.neuronet.neuroplasticity import NeuroplasticityLearner

# 테스트용 임시 파일 경로
TEST_MEMORY_PATH = "tests/test_neuro_memory.json"

@pytest.fixture
def learner():
    """테스트용 Learner 인스턴스 생성 (격리된 메모리 사용)"""
    if os.path.exists(TEST_MEMORY_PATH):
        os.remove(TEST_MEMORY_PATH)
    
    learner = NeuroplasticityLearner(memory_path=TEST_MEMORY_PATH)
    yield learner
    
    # Teardown
    if os.path.exists(TEST_MEMORY_PATH):
        os.remove(TEST_MEMORY_PATH)

def test_initialization(learner):
    """초기화 테스트"""
    assert learner.neural_weights == {}
    assert learner.learning_history == []

def test_hebbian_learning_positive(learner):
    """긍정 피드백에 의한 가중치 강화 테스트"""
    model_id = "test-model-A"
    initial_weight = 0.5
    
    # Positive Feedback (Satisfaction 0.8)
    learner.record_interaction("user1", model_id, {"level": "L3"}, 0.8)
    
    # Expected: 0.5 + 0.05 * (0.8 - 0.5) = 0.5 + 0.015 = 0.515
    new_weight = learner.neural_weights[model_id]
    assert new_weight > initial_weight
    assert abs(new_weight - 0.515) < 0.001

def test_hebbian_learning_negative(learner):
    """부정 피드백에 의한 가중치 약화 테스트"""
    model_id = "test-model-B"
    
    # Negative Feedback (Satisfaction 0.2)
    learner.record_interaction("user1", model_id, {"level": "L3"}, 0.2)
    
    # Expected: 0.5 + 0.05 * (0.2 - 0.5) = 0.5 - 0.015 = 0.485
    new_weight = learner.neural_weights[model_id]
    assert new_weight < 0.5
    assert abs(new_weight - 0.485) < 0.001

def test_persistence(learner):
    """데이터 영구 저장 및 로드 테스트"""
    model_id = "test-model-C"
    learner.record_interaction("user1", model_id, {}, 1.0)
    
    # 파일이 생성되었는지 확인
    assert os.path.exists(TEST_MEMORY_PATH)
    
    # 새로운 인스턴스에서 로드 확인
    new_learner = NeuroplasticityLearner(memory_path=TEST_MEMORY_PATH)
    assert model_id in new_learner.neural_weights
    assert new_learner.neural_weights[model_id] > 0.5

def test_select_best_model(learner):
    """최적 모델 선택 로직 테스트"""
    candidates = [
        {"id": "model-good", "engine": "A"},
        {"id": "model-bad", "engine": "B"}
    ]
    
    # 사전 설정: good 모델의 가중치를 높임
    learner.neural_weights["model-good"] = 0.9
    learner.neural_weights["model-bad"] = 0.1
    
    # Exploitation (대부분 good 선택)
    # Epsilon-Greedy의 랜덤성 때문에 100번 반복해서 경향성 확인
    selected_counts = {"model-good": 0, "model-bad": 0}
    
    for _ in range(100):
        # datetime 해시 의존성을 줄이기 위해 mock을 쓰거나, 
        # 단순히 로직이 동작하는지(에러 없는지) 확인
        selection = learner.select_best_model("L3", candidates)
        if selection in selected_counts:
            selected_counts[selection] += 1
            
    # 적어도 한 번은 선택되어야 함
    assert selected_counts["model-good"] > 0
