"""
신경가소성 (Neuroplasticity) - 자동 학습
Hebbian 원칙: "Neurons that fire together, wire together"
"""

class NeuroplasticityLearner:
    """신경가소성 학습"""
    
    def __init__(self):
        self.neural_weights = {}
        self.learning_history = []
        self.learning_rate = 0.01
    
    def learn_from_interaction(self, interaction):
        """상호작용에서 학습"""
        
        # 1. 상호작용 평가
        success_score = self._evaluate_interaction(interaction)
        
        # 2. 신경 가중치 조정 (Hebbian Learning)
        delta = self.learning_rate * (success_score - 0.5)
        
        for neuron_id in interaction.get("active_neurons", []):
            if neuron_id not in self.neural_weights:
                self.neural_weights[neuron_id] = 0.5
            
            # 가중치 업데이트
            if success_score > 0.7:
                self.neural_weights[neuron_id] += delta
            else:
                self.neural_weights[neuron_id] -= delta
            
            # 범위 유지 (0-1)
            self.neural_weights[neuron_id] = max(0, min(1, 
                self.neural_weights[neuron_id]))
        
        # 3. 학습 기록
        self._record_learning(interaction, success_score)
        
        return success_score
    
    def _evaluate_interaction(self, interaction):
        """상호작용 평가 (0-1)"""
        
        score = 0.5
        
        if interaction.get("user_satisfied"):
            score += 0.3
        
        if interaction.get("response_time_ms", 5000) < 1000:
            score += 0.1
        
        if interaction.get("accuracy_percent", 0) > 90:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _record_learning(self, interaction, score):
        """학습 기록"""
        record = {
            "interaction": interaction.get("id"),
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "weights_count": len(self.neural_weights)
        }
        self.learning_history.append(record)
    
    def get_learned_strategy(self):
        """학습된 전략 반환"""
        return {
            "weights": self.neural_weights,
            "history_length": len(self.learning_history),
            "avg_score": sum(h.get("score", 0) for h in self.learning_history) / 
                        max(1, len(self.learning_history))
        }
