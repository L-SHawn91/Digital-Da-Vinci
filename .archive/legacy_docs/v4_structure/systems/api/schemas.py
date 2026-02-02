"""
Pydantic 요청/응답 스키마 - SHawn-Brain API

FastAPI 데이터 검증 및 자동 문서화
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ==================== 신경 성능 관련 ====================

class NeuralPerformanceCreate(BaseModel):
    """신경 성능 기록 생성"""
    level: str = Field(..., description="신경 레벨 (L1-L4)")
    model_selected: str = Field(..., description="선택된 모델")
    response_time_ms: float = Field(..., description="응답 시간 (ms)")
    tokens_used: int = Field(..., description="사용한 토큰")
    token_cost: float = Field(..., description="토큰 비용")
    success: bool = Field(default=True, description="성공 여부")
    task_type: Optional[str] = None
    hour_of_day: Optional[int] = None
    priority: Optional[str] = None
    neural_score: Optional[float] = None
    efficiency: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class NeuralPerformanceResponse(NeuralPerformanceCreate):
    """신경 성능 응답"""
    id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class NeuralStatusResponse(BaseModel):
    """신경계 상태 응답"""
    timestamp: datetime
    neural_levels: Dict[str, str] = Field(..., description="각 레벨의 모델")
    health: str = Field(..., description="상태 (operational, degraded, down)")
    availability: float = Field(..., description="가용성 %")
    uptime_hours: float = Field(..., description="가동 시간")


# ==================== 모델 메트릭 관련 ====================

class ModelMetricsResponse(BaseModel):
    """모델 메트릭 응답"""
    model_name: str
    total_requests: int
    success_requests: int
    failed_requests: int
    success_rate: float = Field(..., description="성공률 %")
    avg_response_time_ms: float
    avg_tokens_used: float
    avg_token_cost: float
    
    # 신경 레벨별 점수
    l1_score: float = Field(..., description="뇌간 점수")
    l2_score: float = Field(..., description="변린계 점수")
    l3_score: float = Field(..., description="신피질 점수")
    l4_score: float = Field(..., description="신경망 점수")
    
    status: str = Field(..., description="상태 (operational, degraded, down)")
    last_updated: datetime


class ModelListResponse(BaseModel):
    """모델 목록 응답"""
    models: List[Dict[str, Any]]
    count: int
    timestamp: datetime


class PerformanceOverviewResponse(BaseModel):
    """성능 개요 응답"""
    availability: str = Field(..., description="전체 가용성")
    avg_latency_ms: float = Field(..., description="평균 레이턴시")
    token_efficiency: float = Field(..., description="토큰 효율성 (0-1)")
    models_operational: int = Field(..., description="작동 중인 모델 수")
    total_models: int = Field(..., description="전체 모델 수")
    timestamp: datetime


class ModelPerformanceResponse(BaseModel):
    """모델별 성능"""
    name: str
    success_rate: float
    avg_latency: float
    tokens_used: int


# ==================== 정책 관련 ====================

class PolicyCreate(BaseModel):
    """정책 생성"""
    policy_id: str = Field(..., description="정책 ID")
    policy_name: str = Field(..., description="정책 이름")
    policy_config: Dict[str, Any] = Field(..., description="정책 설정")
    expected_performance: float = Field(..., description="예상 성능")
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PolicyResponse(PolicyCreate):
    """정책 응답"""
    id: int
    status: str = Field(..., description="상태 (active, inactive, backup)")
    version: str
    actual_performance: Optional[float]
    degradation_threshold: float
    created_at: datetime
    deployed_at: Optional[datetime]
    rolled_back_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PolicyListResponse(BaseModel):
    """정책 목록 응답"""
    policies: List[PolicyResponse]
    active_policy: Optional[str]
    backup_policies: List[str]
    timestamp: datetime


class PolicyDeployRequest(BaseModel):
    """정책 배포 요청"""
    policy_id: str = Field(..., description="배포할 정책 ID")
    force: bool = Field(default=False, description="강제 배포")


class PolicyDeployResponse(BaseModel):
    """정책 배포 응답"""
    policy_id: str
    status: str
    message: str
    deployed_at: datetime
    validation_status: str = Field(..., description="validated, in_progress, rollback_required")


# ==================== 로그 관련 ====================

class ExecutionLogCreate(BaseModel):
    """실행 로그 생성"""
    work_id: str = Field(..., description="작업 ID")
    task_type: str = Field(..., description="작업 유형")
    neural_level: str = Field(..., description="신경 레벨")
    selected_model: str = Field(..., description="선택 모델")
    priority: Optional[str] = None
    message: Optional[str] = None


class ExecutionLogResponse(ExecutionLogCreate):
    """실행 로그 응답"""
    id: int
    timestamp: datetime
    status: str = Field(..., description="상태 (queued, running, completed, failed)")
    success: Optional[bool]
    duration_ms: Optional[float]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class LogQueryResponse(BaseModel):
    """로그 조회 응답"""
    logs: List[ExecutionLogResponse]
    total: int
    displayed: int
    timestamp: datetime


# ==================== 알림 관련 ====================

class AlertCreate(BaseModel):
    """알림 생성"""
    level: str = Field(..., description="알림 레벨 (info, warning, critical)")
    title: str = Field(..., description="알림 제목")
    message: str = Field(..., description="알림 메시지")
    source: str = Field(..., description="발생 원인")
    component: str = Field(..., description="컴포넌트")
    metadata: Optional[Dict[str, Any]] = None


class AlertResponse(AlertCreate):
    """알림 응답"""
    id: int
    alert_id: str
    timestamp: datetime
    resolved: bool
    resolved_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """알림 목록 응답"""
    alerts: List[AlertResponse]
    unresolved_count: int
    critical_count: int
    timestamp: datetime


# ==================== 라우팅 관련 ====================

class RouteRequest(BaseModel):
    """라우팅 요청"""
    task: str = Field(..., description="작업 설명")
    priority: str = Field(default="normal", description="우선순위")
    level: Optional[str] = None


class RouteResponse(BaseModel):
    """라우팅 응답"""
    work_id: str = Field(..., description="작업 ID")
    task: str
    selected_model: str = Field(..., description="선택된 모델")
    status: str = Field(..., description="상태")
    timestamp: datetime


# ==================== 상태 관련 ====================

class HealthCheckResponse(BaseModel):
    """헬스 체크 응답"""
    status: str = Field(..., description="상태 (healthy, degraded, unhealthy)")
    timestamp: datetime
    neural_system: str = Field(..., description="신경계 시스템 상태")
    uptime_seconds: float


class SystemStatusResponse(BaseModel):
    """전체 시스템 상태"""
    system: str = Field(default="SHawn-Brain")
    version: str
    status: str = Field(..., description="상태 (operational, degraded, down)")
    uptime: float = Field(..., description="가동 시간 (초)")
    neural_levels: int = Field(default=4)
    models: int
    availability: str
    timestamp: datetime


# ==================== 에러 응답 ====================

class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str = Field(..., description="에러 메시지")
    code: str = Field(..., description="에러 코드")
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime


# ==================== 페이지네이션 ====================

class PaginationParams(BaseModel):
    """페이지네이션 파라미터"""
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)
    sort_by: Optional[str] = None
    order: str = Field(default="desc", regex="^(asc|desc)$")


# ==================== 필터링 ====================

class PerformanceFilter(BaseModel):
    """성능 필터"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    model_name: Optional[str] = None
    neural_level: Optional[str] = None
    min_success_rate: Optional[float] = None
    max_latency_ms: Optional[float] = None


class LogFilter(BaseModel):
    """로그 필터"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    work_id: Optional[str] = None
    status: Optional[str] = None
    task_type: Optional[str] = None
    model_name: Optional[str] = None
