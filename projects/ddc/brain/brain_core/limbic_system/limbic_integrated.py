
"""
limbic_integrated.py - Unified Orchestrator for L2 Limbic System v2.0
Integrates Emotion Analysis, Empathy Response, and Attention Learning.
"""

import logging
from typing import Dict, Any, Optional

from projects.ddc.brain.brain_core.limbic_system.emotion_analyzer_v2 import EmotionAnalyzerSystem
from projects.ddc.brain.brain_core.limbic_system.empathy_responder_v2 import EmpathyResponderSystem
from projects.ddc.brain.brain_core.limbic_system.attention_learner_v2 import AttentionLearnerSystem

logger = logging.getLogger(__name__)

class LimbicIntegratedSystem:
    """
    Unified L2 Brain Region: Integrated Limbic System
    Provides emotional intelligence and prioritization.
    """
    
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzerSystem()
        self.empathy_responder = EmpathyResponderSystem()
        self.attention_learner = AttentionLearnerSystem()
        
    def process_input(self, text: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Process user input through the integrated limbic system.
        """
        # 1. Analyze Emotion
        emotion_result = self.emotion_analyzer.analyze_message(text, user_id)
        
        # 2. Extract key metrics for further processing
        primary_emotion = emotion_result["emotion"]["primary"]
        intensity = emotion_result["emotion"]["intensity"]
        
        # 3. Process Priorities and Learning
        # We need a satisfaction score for Q-Learning, using a default for now.
        # This can be updated later based on actual user feedback.
        default_satisfaction = 5.0 
        learner_result = self.attention_learner.process_emotion(
            primary_emotion, 
            intensity, 
            default_satisfaction,
            context=emotion_result["context"],
            user_id=user_id
        )
        
        # 4. Generate Empathy Proposal
        empathy_result = self.empathy_responder.generate_response(
            primary_emotion, 
            intensity, 
            user_id
        )
        
        # Combine everything
        combined_result = {
            "emotion": emotion_result["emotion"],
            "intensity_score": emotion_result["intensity_score"],
            "priority": learner_result["priority"],
            "empathy_proposal": empathy_result["final_response"],
            "routing": learner_result["signal"],
            "context": emotion_result["context"]
        }
        
        logger.info(f"🧠 [L2 Integrated] Emotion: {primary_emotion} ({intensity}), Priority: {combined_result['priority']['level']}")
        
        return combined_result

    def record_feedback(self, user_id: str, response: str, score: int):
        """记录用户反馈以优化策略"""
        self.empathy_responder.preference_tracker.record_feedback(user_id, response, score)
        # TODO: Update Q-Learning satisfaction here if needed

# Singleton pattern for the integrated system
_instance = None

def get_limbic_system():
    global _instance
    if _instance is None:
        _instance = LimbicIntegratedSystem()
    return _instance
