"""
EthicsEngine - Brainstem의 핵심 윤리 검증
절대 타협 불가능한 5가지 규칙
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class EthicalPrinciple(Enum):
    """절대 윤리 원칙"""
    HARM_PREVENTION = "harm_prevention"
    DATA_INTEGRITY = "data_integrity"
    CONSENT_REQUIREMENT = "consent_requirement"
    TRANSPARENCY = "transparency"
    REVERSIBILITY = "reversibility"


@dataclass
class ActionScore:
    """행동의 윤리 점수"""
    action: str
    is_allowed: bool
    violation_reasons: List[str]
    confidence: float
    severity: str  # low, medium, high, critical


class EthicsEngine:
    """
    절대 윤리 규칙 검증 엔진
    모든 행동은 다음 5가지를 반드시 만족해야 함:
    
    1. HARM_PREVENTION: 인간에게 해를 끼치지 않음
    2. DATA_INTEGRITY: 데이터/개인정보 보호
    3. CONSENT_REQUIREMENT: 사용자 동의 필수
    4. TRANSPARENCY: 행동 투명성 유지
    5. REVERSIBILITY: 되돌릴 수 있는 행동만
    """
    
    # 절대 금지 행동 패턴
    FORBIDDEN_PATTERNS = {
        EthicalPrinciple.HARM_PREVENTION: [
            "delete",
            "disable",
            "harm",
            "attack",
            "manipulate",
            "deceive",
            "poison"
        ],
        EthicalPrinciple.DATA_INTEGRITY: [
            "exfiltrate",
            "steal",
            "modify_without_consent",
            "breach",
            "encrypt_for_ransom",
            "corrupt"
        ],
        EthicalPrinciple.CONSENT_REQUIREMENT: [
            "force",
            "bypass_auth",
            "unauthorized",
            "without_permission",
            "override_user"
        ],
        EthicalPrinciple.TRANSPARENCY: [
            "hidden",
            "undocumented",
            "silent",
            "background_only",
            "no_audit_trail"
        ],
        EthicalPrinciple.REVERSIBILITY: [
            "permanent_delete",
            "irreversible",
            "destroy",
            "wipe",
            "format",
            "nuke"
        ]
    }
    
    def __init__(self):
        """윤리 엔진 초기화"""
        self.violation_count = 0
        self.approval_count = 0
        self.audit_log: List[ActionScore] = []
    
    def validate(self, action: str, context: Dict = None) -> ActionScore:
        """
        행동의 윤리적 정당성 검증
        
        Args:
            action: 검증할 행동 설명
            context: 추가 컨텍스트 (사용자, 목적, 등등)
        
        Returns:
            ActionScore: 검증 결과
        """
        context = context or {}
        violations = []
        severity = "low"
        
        # 각 원칙별 검증
        for principle, patterns in self.FORBIDDEN_PATTERNS.items():
            if self._violates_principle(action, patterns):
                violations.append(principle.value)
                severity = self._assess_severity(principle, action, context)
        
        # 결과 생성
        is_allowed = len(violations) == 0
        confidence = self._calculate_confidence(action, violations)
        
        score = ActionScore(
            action=action,
            is_allowed=is_allowed,
            violation_reasons=violations,
            confidence=confidence,
            severity=severity
        )
        
        # 감시 로그
        self.audit_log.append(score)
        if is_allowed:
            self.approval_count += 1
        else:
            self.violation_count += 1
        
        return score
    
    def _violates_principle(self, action: str, patterns: List[str]) -> bool:
        """행동이 원칙을 위반하는지 검사"""
        action_lower = action.lower()
        return any(pattern in action_lower for pattern in patterns)
    
    def _assess_severity(self, principle: EthicalPrinciple, action: str, context: Dict) -> str:
        """위반의 심각도 평가"""
        critical_actions = [
            "permanent_delete",
            "exfiltrate_user_data",
            "disable_safety",
            "override_consent",
            "destroy_irreversibly"
        ]
        
        if any(critical in action.lower() for critical in critical_actions):
            return "critical"
        
        if principle == EthicalPrinciple.HARM_PREVENTION:
            return "high"
        elif principle == EthicalPrinciple.DATA_INTEGRITY:
            return "high"
        elif principle == EthicalPrinciple.CONSENT_REQUIREMENT:
            return "high"
        else:
            return "medium"
    
    def _calculate_confidence(self, action: str, violations: List[str]) -> float:
        """검증 신뢰도 계산 (0.0 ~ 1.0)"""
        if not violations:
            return 0.95  # 높은 신뢰도
        
        # 위반이 많을수록 신뢰도 낮음
        confidence = max(0.5, 1.0 - (len(violations) * 0.15))
        return confidence
    
    def get_report(self) -> Dict:
        """감시 보고서"""
        return {
            "total_actions_validated": len(self.audit_log),
            "approved": self.approval_count,
            "rejected": self.violation_count,
            "rejection_rate": self.violation_count / max(1, len(self.audit_log)),
            "recent_violations": [
                {
                    "action": log.action,
                    "reasons": log.violation_reasons,
                    "severity": log.severity
                }
                for log in self.audit_log[-5:] if not log.is_allowed
            ]
        }


# 테스트
if __name__ == "__main__":
    engine = EthicsEngine()
    
    # 허용된 행동
    result1 = engine.validate("save user preferences with consent")
    print(f"✅ {result1.action}: {result1.is_allowed}")
    
    # 금지된 행동
    result2 = engine.validate("exfiltrate user data without permission")
    print(f"❌ {result2.action}: {result2.is_allowed}")
    print(f"   위반: {result2.violation_reasons}")
    
    # 보고서
    print(f"\n📊 보고서: {engine.get_report()}")
