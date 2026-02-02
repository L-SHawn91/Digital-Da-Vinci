"""
최종 설정 파일 - 모든 시스템 파라미터

역할:
- 중앙화된 설정 관리
- 환경별 설정
- 실시간 설정 변경
- 설정 버전 관리
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class NeuralSystemConfig:
    """신경계 설정"""
    
    # L1 뇌간
    brainstem_latency_target_ms: int = 50
    brainstem_health_threshold: float = 0.7
    
    # L2 변린계
    limbic_response_time_ms: int = 100
    limbic_alert_threshold: float = 0.6
    
    # L3 신피질
    neocortex_decision_time_ms: int = 150
    neocortex_confidence_threshold: float = 0.75
    
    # L4 신경망
    neuronet_routing_latency_ms: int = 80
    neuronet_learning_rate: float = 0.01
    
    # 공통
    health_check_interval_seconds: int = 60
    optimization_interval_seconds: int = 300


@dataclass
class CachingConfig:
    """캐싱 설정"""
    
    # 메모리 캐시
    memory_cache_enabled: bool = True
    memory_cache_max_mb: int = 200
    memory_cache_ttl_minutes: int = 30
    
    # Redis 캐시
    redis_enabled: bool = False  # 선택사항
    redis_url: str = "redis://localhost:6379"
    redis_ttl_minutes: int = 60
    
    # Pinecone 벡터 DB
    pinecone_enabled: bool = False  # 선택사항
    pinecone_api_key: str = ""
    pinecone_environment: str = "production"
    
    # 정책
    cache_hit_target_percent: float = 85.0
    lru_policy_enabled: bool = True
    auto_eviction_enabled: bool = True


@dataclass
class PerformanceConfig:
    """성능 설정"""
    
    # 비동기 처리
    async_workers: int = 5
    async_queue_size: int = 1000
    async_timeout_seconds: int = 30
    
    # 모니터링
    metrics_collection_interval_seconds: int = 5
    metrics_buffer_size: int = 1000
    anomaly_detection_enabled: bool = True
    anomaly_z_score_threshold: float = 2.5
    
    # 벤치마크
    benchmark_enabled: bool = True
    benchmark_interval_hours: int = 1
    benchmark_duration_seconds: int = 60


@dataclass
class ModelConfig:
    """모델 설정"""
    
    # 주요 모델
    default_model: str = "gemini_2_5_pro"
    fallback_model: str = "claude_opus"
    fast_model: str = "groq_llama"
    
    # 가중치 (분배 비율)
    model_weights: Dict[str, float] = None
    
    # 타임아웃
    model_timeout_seconds: int = 30
    model_retry_count: int = 3
    
    def __post_init__(self):
        if self.model_weights is None:
            self.model_weights = {
                'gemini_2_5_pro': 0.40,
                'claude_opus': 0.30,
                'groq_llama': 0.15,
                'deepseek': 0.15
            }


@dataclass
class SecurityConfig:
    """보안 설정"""
    
    # 토큰
    token_expiry_hours: int = 24
    token_refresh_enabled: bool = True
    
    # 암호화
    encryption_enabled: bool = True
    encryption_algorithm: str = "HMAC-SHA256"
    
    # Rate limiting
    rate_limit_free_requests_per_minute: int = 100
    rate_limit_basic_requests_per_minute: int = 1000
    rate_limit_pro_requests_per_minute: int = 10000
    
    # 감시
    audit_log_max_entries: int = 1000
    suspicious_activity_threshold: int = 1000
    
    # GDPR
    gdpr_enabled: bool = True
    data_retention_days: int = 90


@dataclass
class APIConfig:
    """API 설정"""
    
    # 서버
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # 버전
    current_version: str = "v5.2"
    supported_versions: list = None
    
    # CORS
    cors_enabled: bool = True
    cors_origins: list = None
    
    # 문서
    swagger_enabled: bool = True
    swagger_url: str = "/docs"
    
    def __post_init__(self):
        if self.supported_versions is None:
            self.supported_versions = ["v1", "v4", "v5", "v5.2"]
        if self.cors_origins is None:
            self.cors_origins = ["*"]


@dataclass
class DeploymentConfig:
    """배포 설정"""
    
    # 환경
    environment: str = "production"  # development, staging, production
    debug: bool = False
    
    # 로깅
    log_level: str = "INFO"
    log_file: str = "/var/log/shawn-brain.log"
    log_retention_days: int = 30
    
    # 데이터베이스
    database_url: str = "postgresql://localhost/shawn_brain"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # 모니터링
    monitoring_enabled: bool = True
    prometheus_enabled: bool = True
    grafana_enabled: bool = False
    
    # 백업
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    backup_retention_days: int = 7


class ConfigManager:
    """설정 관리자"""
    
    def __init__(self):
        self.neural = NeuralSystemConfig()
        self.caching = CachingConfig()
        self.performance = PerformanceConfig()
        self.model = ModelConfig()
        self.security = SecurityConfig()
        self.api = APIConfig()
        self.deployment = DeploymentConfig()
        
        self.version = "0.0.1"  # Prototype Version
        self.last_updated = datetime.now().isoformat()
        self.history = []
    
    def get_all_config(self) -> Dict[str, Any]:
        """모든 설정 조회"""
        return {
            'version': self.version,
            'last_updated': self.last_updated,
            'neural': asdict(self.neural),
            'caching': asdict(self.caching),
            'performance': asdict(self.performance),
            'model': asdict(self.model),
            'security': asdict(self.security),
            'api': asdict(self.api),
            'deployment': asdict(self.deployment)
        }
    
    def update_config(self, section: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """설정 업데이트"""
        
        config_obj = getattr(self, section, None)
        if not config_obj:
            return {'status': 'error', 'message': f'Invalid section: {section}'}
        
        # 이전 설정 저장
        old_config = asdict(config_obj)
        
        # 업데이트
        for key, value in updates.items():
            if hasattr(config_obj, key):
                setattr(config_obj, key, value)
        
        # 히스토리 기록
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'section': section,
            'old_values': old_config,
            'new_values': asdict(config_obj)
        })
        
        self.last_updated = datetime.now().isoformat()
        
        return {
            'status': 'success',
            'section': section,
            'updated_fields': list(updates.keys())
        }
    
    def export_config(self) -> str:
        """설정 내보내기 (JSON)"""
        return json.dumps(self.get_all_config(), indent=2)
    
    def import_config(self, json_str: str) -> Dict[str, Any]:
        """설정 가져오기 (JSON)"""
        try:
            config_data = json.loads(json_str)
            
            for section, config in config_data.items():
                if section in ['version', 'last_updated', 'history']:
                    continue
                
                self.update_config(section, config)
            
            return {'status': 'success', 'message': 'Configuration imported'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def reset_to_defaults(self) -> Dict[str, Any]:
        """기본 설정으로 리셋"""
        self.neural = NeuralSystemConfig()
        self.caching = CachingConfig()
        self.performance = PerformanceConfig()
        self.model = ModelConfig()
        self.security = SecurityConfig()
        self.api = APIConfig()
        self.deployment = DeploymentConfig()
        
        self.last_updated = datetime.now().isoformat()
        
        return {'status': 'success', 'message': 'Reset to default configuration'}
    
    def get_config_report(self) -> Dict[str, Any]:
        """설정 리포트"""
        return {
            'timestamp': datetime.now().isoformat(),
            'version': self.version,
            'total_updates': len(self.history),
            'configuration': self.get_all_config(),
            'recent_updates': self.history[-5:] if self.history else []
        }


# 글로벌 설정 인스턴스
default_config = ConfigManager()


if __name__ == "__main__":
    print("⚙️ 설정 시스템 테스트\n")
    
    config = ConfigManager()
    
    # 현재 설정 조회
    print("✅ 신경계 설정:")
    print(f"  - Brainstem latency target: {config.neural.brainstem_latency_target_ms}ms")
    print(f"  - Neocortex decision time: {config.neural.neocortex_decision_time_ms}ms")
    
    print("\n✅ 캐싱 설정:")
    print(f"  - Memory cache: {config.caching.memory_cache_max_mb}MB")
    print(f"  - Cache hit target: {config.caching.cache_hit_target_percent}%")
    
    print("\n✅ 성능 설정:")
    print(f"  - Async workers: {config.performance.async_workers}")
    
    # 설정 업데이트
    print("\n✅ 설정 업데이트:")
    result = config.update_config('performance', {
        'async_workers': 8,
        'metrics_collection_interval_seconds': 10
    })
    print(f"  - Result: {result['status']}")
    
    print("\n✅ 설정 리포트:")
    report = config.get_config_report()
    print(f"  - Total updates: {report['total_updates']}")
    print(f"  - Configuration version: {report['version']}")
