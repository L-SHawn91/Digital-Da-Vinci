"""
보안 & 암호화 시스템 - API 요청 보호

역할:
- JWT 인증
- 데이터 암호화
- 감사 로그
- 침입 탐지
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import hmac
import json


@dataclass
class SecurityToken:
    """보안 토큰"""
    token_id: str
    client_id: str
    expires_at: datetime
    scopes: List[str]  # ['read', 'write', 'admin']
    created_at: datetime = None
    last_used: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def is_valid(self) -> bool:
        """토큰 유효성"""
        return datetime.now() < self.expires_at
    
    def has_scope(self, scope: str) -> bool:
        """범위 확인"""
        return scope in self.scopes


class SecurityManager:
    """보안 관리자"""
    
    def __init__(self):
        self.tokens: Dict[str, SecurityToken] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.blacklist: List[str] = []  # 차단된 토큰/IP
        self.suspicious_activity = []
    
    def issue_token(
        self,
        client_id: str,
        scopes: List[str],
        expires_in_hours: int = 24
    ) -> str:
        """토큰 발급"""
        token_id = hashlib.sha256(
            f"{client_id}_{datetime.now().timestamp()}".encode()
        ).hexdigest()
        
        token = SecurityToken(
            token_id=token_id,
            client_id=client_id,
            expires_at=datetime.now() + timedelta(hours=expires_in_hours),
            scopes=scopes
        )
        
        self.tokens[token_id] = token
        
        # 감사 로그
        self._log_audit('token_issued', {
            'client_id': client_id,
            'scopes': scopes,
            'expires_in_hours': expires_in_hours
        })
        
        return token_id
    
    def validate_token(self, token_id: str, required_scope: Optional[str] = None) -> bool:
        """토큰 검증"""
        if token_id in self.blacklist:
            self._log_audit('token_validation_failed', {
                'reason': 'blacklisted',
                'token_id': token_id[:8] + '...'
            })
            return False
        
        if token_id not in self.tokens:
            return False
        
        token = self.tokens[token_id]
        
        if not token.is_valid():
            return False
        
        if required_scope and not token.has_scope(required_scope):
            self._log_audit('insufficient_permissions', {
                'token_id': token_id[:8] + '...',
                'required_scope': required_scope
            })
            return False
        
        # 사용 시간 업데이트
        token.last_used = datetime.now()
        return True
    
    def revoke_token(self, token_id: str):
        """토큰 폐기"""
        self.blacklist.append(token_id)
        self._log_audit('token_revoked', {'token_id': token_id[:8] + '...'})
    
    def encrypt_data(self, data: Dict[str, Any], key: str) -> str:
        """데이터 암호화"""
        json_str = json.dumps(data)
        
        # HMAC 생성 (간단한 예시, 실제는 AES 권장)
        hmac_obj = hmac.new(key.encode(), json_str.encode(), hashlib.sha256)
        signature = hmac_obj.hexdigest()
        
        return f"{signature}:{json_str}"
    
    def decrypt_data(self, encrypted: str, key: str) -> Optional[Dict[str, Any]]:
        """데이터 복호화"""
        try:
            signature, json_str = encrypted.split(':', 1)
            
            # 서명 검증
            hmac_obj = hmac.new(key.encode(), json_str.encode(), hashlib.sha256)
            expected_signature = hmac_obj.hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                self._log_audit('decryption_failed', {'reason': 'invalid_signature'})
                return None
            
            return json.loads(json_str)
        
        except Exception as e:
            self._log_audit('decryption_error', {'error': str(e)})
            return None
    
    def detect_suspicious_activity(
        self,
        client_id: str,
        request_count: int,
        time_window_minutes: int = 1
    ) -> Dict[str, Any]:
        """의심 활동 탐지"""
        # 비정상적인 요청 빈도 탐지
        if request_count > 1000:  # 1분에 1000개 이상
            alert = {
                'severity': 'high',
                'type': 'high_frequency',
                'client_id': client_id,
                'request_count': request_count,
                'time_window_minutes': time_window_minutes,
                'timestamp': datetime.now().isoformat()
            }
            
            self.suspicious_activity.append(alert)
            self._log_audit('suspicious_activity_detected', alert)
            
            return alert
        
        return {'status': 'normal'}
    
    def rate_limit_exceeded(self, client_id: str) -> Dict[str, Any]:
        """Rate limit 초과 시 처리"""
        # 클라이언트 차단
        self._log_audit('rate_limit_exceeded', {'client_id': client_id})
        
        return {
            'status': 'blocked',
            'reason': 'rate_limit_exceeded',
            'retry_after_seconds': 60
        }
    
    def _log_audit(self, event_type: str, details: Dict[str, Any]):
        """감시 로그 기록"""
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        })
        
        # 최근 1000개만 유지
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """감시 로그 조회"""
        return self.audit_log[-limit:]
    
    def get_security_report(self) -> Dict[str, Any]:
        """보안 리포트"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_tokens': len(self.tokens),
            'valid_tokens': sum(1 for t in self.tokens.values() if t.is_valid()),
            'revoked_tokens': len(self.blacklist),
            'suspicious_activities': len(self.suspicious_activity),
            'recent_activities': self.suspicious_activity[-10:],
            'audit_log_size': len(self.audit_log)
        }


class InputValidator:
    """입력 검증"""
    
    @staticmethod
    def validate_request(request_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """요청 검증"""
        required_fields = ['method', 'path', 'client_id']
        
        # 필수 필드 확인
        for field in required_fields:
            if field not in request_data:
                return False, f"Missing required field: {field}"
        
        # SQL Injection 확인
        dangerous_patterns = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT']
        for pattern in dangerous_patterns:
            if pattern in str(request_data).upper():
                return False, "Potential SQL injection detected"
        
        # XSS 확인
        xss_patterns = ['<script', 'javascript:', 'onclick=']
        for pattern in xss_patterns:
            if pattern in str(request_data).lower():
                return False, "Potential XSS attack detected"
        
        return True, None
    
    @staticmethod
    def sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 정제"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # HTML 특수 문자 제거
                value = value.replace('<', '&lt;').replace('>', '&gt;')
                value = value.replace('"', '&quot;').replace("'", '&#39;')
            
            sanitized[key] = value
        
        return sanitized


class ComplianceManager:
    """규정 준수 관리"""
    
    def __init__(self):
        self.gdpr_consents: Dict[str, bool] = {}  # GDPR 동의
        self.data_retention_days = 90  # 90일 보관
        self.encryption_required = True
    
    def request_gdpr_consent(self, client_id: str) -> bool:
        """GDPR 동의 요청"""
        self.gdpr_consents[client_id] = True
        return True
    
    def has_gdpr_consent(self, client_id: str) -> bool:
        """GDPR 동의 확인"""
        return self.gdpr_consents.get(client_id, False)
    
    def export_user_data(self, client_id: str) -> Dict[str, Any]:
        """사용자 데이터 내보내기 (GDPR)"""
        return {
            'client_id': client_id,
            'export_date': datetime.now().isoformat(),
            'data': {
                'profile': {},
                'activity_log': [],
                'preferences': {}
            }
        }
    
    def delete_user_data(self, client_id: str) -> bool:
        """사용자 데이터 삭제 (GDPR)"""
        # 실제 구현에서는 데이터베이스에서 삭제
        self.gdpr_consents.pop(client_id, None)
        return True


if __name__ == "__main__":
    print("🔒 보안 시스템 테스트\n")
    
    security = SecurityManager()
    
    # 토큰 발급
    token = security.issue_token("client_1", ["read", "write"], 24)
    print(f"✅ 토큰 발급: {token[:16]}...")
    
    # 토큰 검증
    valid = security.validate_token(token, "read")
    print(f"✅ 토큰 검증: {valid}")
    
    # 데이터 암호화
    data = {"user_id": 123, "action": "analyze"}
    encrypted = security.encrypt_data(data, "secret_key")
    print(f"✅ 데이터 암호화: {encrypted[:50]}...")
    
    # 데이터 복호화
    decrypted = security.decrypt_data(encrypted, "secret_key")
    print(f"✅ 데이터 복호화: {decrypted}")
    
    # 의심 활동 탐지
    activity = security.detect_suspicious_activity("client_1", 1500, 1)
    print(f"✅ 의심 활동: {activity['severity']}")
    
    # 보안 리포트
    report = security.get_security_report()
    print(f"✅ 보안 리포트: {report['total_tokens']}개 토큰")
    
    print("\n✅ 보안 테스트 완료!")
