"""
SQLAlchemy 데이터베이스 모델 - SHawn-Brain

신경계 성능 데이터, 모델 메트릭, 정책, 로그 저장
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 데이터베이스 URL (SQLite 기본값)
DATABASE_URL = "sqlite:///./shawn_brain.db"
# PostgreSQL 사용 시:
# DATABASE_URL = "postgresql://user:password@localhost/shawn_brain"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== 1. 신경 성능 테이블 ====================

class NeuralPerformance(Base):
    """신경계 성능 기록"""
    __tablename__ = "neural_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 신경 레벨
    level = Column(String, index=True)  # L1, L2, L3, L4
    model_selected = Column(String, index=True)  # 선택된 모델
    
    # 성능 메트릭
    response_time_ms = Column(Float)
    tokens_used = Column(Integer)
    token_cost = Column(Float)
    success = Column(Boolean, default=True)
    
    # 상세 정보
    task_type = Column(String)
    hour_of_day = Column(Integer)  # 0-23
    priority = Column(String)  # low, normal, high
    
    # 추가 필드
    neural_score = Column(Float)  # 0.0-10.0
    efficiency = Column(Float)  # 효율성
    metadata = Column(JSON)  # 추가 데이터
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<NeuralPerformance {self.id}: {self.level} - {self.model_selected}>"


# ==================== 2. 모델 메트릭 테이블 ====================

class ModelMetrics(Base):
    """모델별 성능 메트릭"""
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, unique=True, index=True)
    
    # 성능 통계
    total_requests = Column(Integer, default=0)
    success_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    
    # 메트릭
    avg_response_time_ms = Column(Float, default=0.0)
    avg_tokens_used = Column(Float, default=0.0)
    avg_token_cost = Column(Float, default=0.0)
    
    # 신경 레벨별 점수
    l1_score = Column(Float, default=0.0)  # 뇌간
    l2_score = Column(Float, default=0.0)  # 변린계
    l3_score = Column(Float, default=0.0)  # 신피질
    l4_score = Column(Float, default=0.0)  # 신경망
    
    # 추가 정보
    status = Column(String, default="operational")  # operational, degraded, down
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)
    
    def get_success_rate(self) -> float:
        """성공률 계산"""
        if self.total_requests == 0:
            return 0.0
        return (self.success_requests / self.total_requests) * 100
    
    def __repr__(self):
        return f"<ModelMetrics {self.model_name}: {self.get_success_rate():.1f}%>"


# ==================== 3. 정책 테이블 ====================

class Policy(Base):
    """신경계 정책"""
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(String, unique=True, index=True)
    policy_name = Column(String)
    
    # 상태
    status = Column(String, default="inactive")  # active, inactive, backup, rollback
    version = Column(String, default="1.0")
    
    # 정책 내용 (Q-Learning 정책, 모델 가중치 등)
    policy_config = Column(JSON)
    
    # 성능
    expected_performance = Column(Float)  # 예상 성능
    actual_performance = Column(Float)  # 실제 성능
    degradation_threshold = Column(Float, default=-5.0)  # -5% 자동 롤백
    
    # 배포 정보
    created_at = Column(DateTime, default=datetime.utcnow)
    deployed_at = Column(DateTime, nullable=True)
    rolled_back_at = Column(DateTime, nullable=True)
    
    # 메타데이터
    description = Column(String, nullable=True)
    metadata = Column(JSON)
    
    def __repr__(self):
        return f"<Policy {self.policy_id}: {self.status}>"


# ==================== 4. 실행 로그 테이블 ====================

class ExecutionLog(Base):
    """작업 실행 로그"""
    __tablename__ = "execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 작업 정보
    task_type = Column(String, index=True)
    priority = Column(String)
    
    # 신경계 라우팅
    neural_level = Column(String)
    selected_model = Column(String, index=True)
    
    # 실행 상태
    status = Column(String)  # queued, running, completed, failed
    message = Column(String)
    
    # 성능
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    duration_ms = Column(Float, nullable=True)
    
    # 결과
    success = Column(Boolean, nullable=True)
    result_data = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExecutionLog {self.work_id}: {self.status}>"


# ==================== 5. 알림 테이블 ====================

class Alert(Base):
    """시스템 알림"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 알림 정보
    level = Column(String)  # info, warning, critical
    title = Column(String)
    message = Column(String)
    
    # 발생 원인
    source = Column(String)  # neural_router, performance_monitor, etc
    component = Column(String)  # L1, L2, L3, L4, model_name, etc
    
    # 상태
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    
    # 메타데이터
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Alert {self.alert_id}: {self.level}>"


# ==================== 데이터베이스 초기화 ====================

def init_db():
    """데이터베이스 테이블 생성"""
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료")


def get_db():
    """데이터베이스 세션 获得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 샘플 데이터 삽입 ====================

def seed_initial_data():
    """초기 샘플 데이터 삽입"""
    db = SessionLocal()
    
    # 모델 메트릭 초기화
    models = [
        "Groq", "Gemini", "Claude", "DeepSeek",
        "OpenAI", "Mistral", "SambaNova", "Cerebras"
    ]
    
    for model in models:
        existing = db.query(ModelMetrics).filter(ModelMetrics.model_name == model).first()
        if not existing:
            metric = ModelMetrics(
                model_name=model,
                total_requests=0,
                success_requests=0,
                failed_requests=0,
                status="operational"
            )
            db.add(metric)
    
    # 초기 정책 생성
    policy = Policy(
        policy_id="policy_001",
        policy_name="Q-Learning v1",
        status="active",
        version="1.0",
        policy_config={"epsilon": 0.1, "learning_rate": 0.1},
        expected_performance=95.0
    )
    
    existing_policy = db.query(Policy).filter(Policy.policy_id == "policy_001").first()
    if not existing_policy:
        db.add(policy)
    
    db.commit()
    db.close()
    print("✅ 초기 데이터 삽입 완료")


if __name__ == "__main__":
    init_db()
    seed_initial_data()
