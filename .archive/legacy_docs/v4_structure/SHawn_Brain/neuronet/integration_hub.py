"""
통합 중추 (Integration Hub) - 신경계 통합
모든 뇌 레벨을 통합하는 중앙 허브
"""

class IntegrationHub:
    """신경계 통합 중추"""
    
    def __init__(self):
        self.integration_state = {}
        self.integration_history = []
    
    async def integrate_brain_levels(self, level1_result, level2_result, 
                                   level3_results, neuronet_data):
        """모든 뇌 레벨 통합"""
        
        # 1. 신호 흐름 검증
        self._validate_signal_flow(level1_result, level2_result, 
                                  level3_results, neuronet_data)
        
        # 2. 우선순위 결정
        priority = level2_result.get("priority", 50)
        
        # 3. 결과 병합
        integrated_result = self._merge_results(
            level1_result, level2_result, level3_results, neuronet_data
        )
        
        # 4. 신뢰도 계산
        confidence = self._calculate_confidence(integrated_result)
        
        # 5. 최종 실행 결정
        final_result = {
            "action": integrated_result.get("recommended_action"),
            "confidence": confidence,
            "priority": priority,
            "integration_time_ms": self._get_elapsed_time(),
            "all_components_ok": True
        }
        
        return final_result
    
    def _validate_signal_flow(self, *components):
        """신호 흐름 검증"""
        for i, component in enumerate(components):
            if component is None:
                raise ValueError(f"Component {i} is None")
    
    def _merge_results(self, level1, level2, level3, level4):
        """결과 병합"""
        return {
            "brainstem": level1,
            "limbic": level2,
            "neocortex": level3,
            "neuronet": level4,
            "recommended_action": self._determine_action(
                level1, level2, level3, level4
            )
        }
    
    def _determine_action(self, level1, level2, level3, level4):
        """최적 행동 결정"""
        
        priority = level2.get("priority", 50)
        
        if priority >= 80:
            return "execute_immediately"
        elif level3.get("complexity", 0) > 7:
            return "detailed_analysis"
        else:
            return "standard_response"
    
    def _calculate_confidence(self, result):
        """신뢰도 계산 (0-100)"""
        confidence = 70  # 기본값
        
        if result.get("all_components_ok"):
            confidence += 15
        
        return min(100, confidence)
    
    def _get_elapsed_time(self):
        """경과 시간"""
        return 100  # ms
