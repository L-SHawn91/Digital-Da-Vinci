"""
🧠 Amygdala: 편도체
- 역할: 입력 생존 위협(중요도) 감지, 감정 가중치 부여
- 학술 근거: Joseph LeDoux (1996) 'The Emotional Brain'
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Amygdala:
    """
    입력 신호의 감정적 가중치와 중요도를 즉각적으로 평가하는 모듈
    """
    
    def __init__(self):
        # 감정 키워드 사전 (간이 버전)
        self.salience_keywords = {
            "emergency": 1.0, "danger": 1.0, "critical": 0.9,
            "error": 0.8, "bug": 0.8, "important": 0.7,
            "success": 0.8, "congratulations": 0.9,
            "failure": 0.7, "problem": 0.6
        }

    def assess_salience(self, text: str) -> Dict[str, float]:
        """
        텍스트의 생존/작업 중요도(Salience) 및 감정 가중치(Valence) 평가
        
        Returns:
            {
                "importance": 0.0 ~ 1.0,
                "valence": -1.0 (부정) ~ 1.0 (긍정)
            }
        """
        text_lower = text.lower()
        importance = 0.5  # 기본 중요도
        valence = 0.0     # 중립
        
        # 키워드 기반 단순 평가 (향후 NLP/LLM 기반으로 고도화 가능)
        for kw, score in self.salience_keywords.items():
            if kw in text_lower:
                importance = max(importance, score)
                
        # 부정적 감정 키워드 (예시)
        negative_kws = ["error", "fail", "slow", "bad", "wrong", "문제", "오류", "안돼"]
        positive_kws = ["good", "great", "thanks", "success", "좋아", "성공", "고마워"]
        
        if any(k in text_lower for k in negative_kws):
            valence -= 0.5
        if any(k in text_lower for k in positive_kws):
            valence += 0.5
            
        # 범위 조정
        valence = max(-1.0, min(1.0, valence))
        
        logger.debug(f"❤️ Amygdala Assessment: Importance={importance:.2f}, Valence={valence:.2f}")
        
        return {
            "importance": importance,
            "valence": valence
        }

if __name__ == "__main__":
    amy = Amygdala()
    print(amy.assess_salience("이 코드는 에러가 너무 많이 발생해서 심각한 문제야!"))
    print(amy.assess_salience("프로젝트가 성공적으로 완료되었습니다. 고생하셨습니다!"))
