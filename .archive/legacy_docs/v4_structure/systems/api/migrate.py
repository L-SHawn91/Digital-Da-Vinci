#!/usr/bin/env python
"""
데이터베이스 마이그레이션 & 초기화 스크립트

사용법:
  python migrate.py init      # 테이블 생성
  python migrate.py seed      # 샘플 데이터 삽입
  python migrate.py reset     # 전체 초기화
"""

import sys
import os
from datetime import datetime

# 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    engine, Base, SessionLocal,
    NeuralPerformance, ModelMetrics, Policy, ExecutionLog, Alert,
    init_db, seed_initial_data
)


def migrate_init():
    """테이블 생성"""
    print("🔧 데이터베이스 마이그레이션: 테이블 생성")
    print("-" * 50)
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 모든 테이블이 생성되었습니다")
        print("")
        print("생성된 테이블:")
        print("  1. neural_performance (신경 성능)")
        print("  2. model_metrics (모델 메트릭)")
        print("  3. policies (정책)")
        print("  4. execution_logs (실행 로그)")
        print("  5. alerts (알림)")
        return True
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False


def migrate_seed():
    """샘플 데이터 삽입"""
    print("🌱 샘플 데이터 삽입")
    print("-" * 50)
    
    try:
        db = SessionLocal()
        
        # 1. 모델 메트릭 초기화
        print("📊 모델 메트릭 초기화 중...")
        models = [
            ("Groq", 9.6, 9.8, 9.5, 8.9),
            ("Gemini", 9.7, 8.9, 9.9, 9.6),
            ("Claude", 9.5, 9.2, 9.8, 9.4),
            ("DeepSeek", 8.8, 9.0, 9.2, 9.5),
            ("OpenAI", 9.2, 8.5, 9.7, 9.6),
            ("Mistral", 8.9, 8.8, 9.0, 9.1),
            ("SambaNova", 8.7, 8.3, 9.0, 9.2),
            ("Cerebras", 8.6, 8.0, 8.8, 9.0),
        ]
        
        for model_name, l1, l2, l3, l4 in models:
            existing = db.query(ModelMetrics).filter(
                ModelMetrics.model_name == model_name
            ).first()
            
            if not existing:
                metric = ModelMetrics(
                    model_name=model_name,
                    total_requests=100 + (hash(model_name) % 900),
                    success_requests=90 + (hash(model_name) % 100),
                    failed_requests=10 + (hash(model_name) % 50),
                    avg_response_time_ms=1200.0 + (hash(model_name) % 500),
                    avg_tokens_used=500.0 + (hash(model_name) % 200),
                    avg_token_cost=0.0001 + (hash(model_name) % 100) / 1000000,
                    l1_score=l1,
                    l2_score=l2,
                    l3_score=l3,
                    l4_score=l4,
                    status="operational"
                )
                db.add(metric)
        
        db.commit()
        print(f"   ✅ {len(models)}개 모델 메트릭 추가됨")
        
        # 2. 정책 생성
        print("📐 정책 초기화 중...")
        policies = [
            {
                "policy_id": "policy_001",
                "policy_name": "Q-Learning v1",
                "status": "active",
                "config": {"epsilon": 0.1, "learning_rate": 0.1, "discount_factor": 0.95}
            },
            {
                "policy_id": "policy_002",
                "policy_name": "Standard Distribution",
                "status": "backup",
                "config": {"l1_ratio": 0.3, "l2_ratio": 0.25, "l3_ratio": 0.25, "l4_ratio": 0.2}
            },
        ]
        
        for policy_data in policies:
            existing = db.query(Policy).filter(
                Policy.policy_id == policy_data["policy_id"]
            ).first()
            
            if not existing:
                policy = Policy(
                    policy_id=policy_data["policy_id"],
                    policy_name=policy_data["policy_name"],
                    status=policy_data["status"],
                    version="1.0",
                    policy_config=policy_data["config"],
                    expected_performance=95.0 if policy_data["status"] == "active" else 93.0,
                    description=f"정책: {policy_data['policy_name']}"
                )
                db.add(policy)
        
        db.commit()
        print(f"   ✅ {len(policies)}개 정책 추가됨")
        
        # 3. 샘플 실행 로그
        print("📝 샘플 실행 로그 생성 중...")
        for i in range(10):
            log = ExecutionLog(
                work_id=f"work_{i:04d}",
                task_type=["neural_route", "performance_check", "model_test"][i % 3],
                neural_level=f"L{(i % 4) + 1}",
                selected_model=models[i % len(models)][0],
                priority=["low", "normal", "high"][i % 3],
                status="completed",
                success=i % 10 != 9,  # 10%는 실패
                duration_ms=1000.0 + (i * 100)
            )
            db.add(log)
        
        db.commit()
        print(f"   ✅ 10개 샘플 실행 로그 추가됨")
        
        db.close()
        return True
    
    except Exception as e:
        print(f"❌ 에러: {e}")
        db.close()
        return False


def migrate_reset():
    """전체 초기화"""
    print("🔄 데이터베이스 전체 초기화")
    print("-" * 50)
    
    try:
        response = input("⚠️  모든 데이터가 삭제됩니다. 계속하시겠습니까? (yes/no): ")
        if response.lower() != "yes":
            print("취소되었습니다")
            return False
        
        print("삭제 중...")
        Base.metadata.drop_all(bind=engine)
        print("✅ 모든 테이블 삭제됨")
        
        print("생성 중...")
        Base.metadata.create_all(bind=engine)
        print("✅ 모든 테이블 생성됨")
        
        return True
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False


def migrate_status():
    """데이터베이스 상태 확인"""
    print("📊 데이터베이스 상태")
    print("-" * 50)
    
    try:
        db = SessionLocal()
        
        # 각 테이블의 행 수
        neural_count = db.query(NeuralPerformance).count()
        metric_count = db.query(ModelMetrics).count()
        policy_count = db.query(Policy).count()
        log_count = db.query(ExecutionLog).count()
        alert_count = db.query(Alert).count()
        
        print(f"neural_performance: {neural_count} 행")
        print(f"model_metrics: {metric_count} 행")
        print(f"policies: {policy_count} 행")
        print(f"execution_logs: {log_count} 행")
        print(f"alerts: {alert_count} 행")
        print(f"\n📈 총 데이터: {neural_count + metric_count + policy_count + log_count + alert_count} 행")
        
        # 활성 정책
        active = db.query(Policy).filter(Policy.status == "active").first()
        if active:
            print(f"\n🎯 활성 정책: {active.policy_name} (v{active.version})")
        
        db.close()
        return True
    
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False


def main():
    """메인 함수"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║  SHawn-Brain 데이터베이스 마이그레이션 도구           ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("")
    
    if len(sys.argv) < 2:
        print("사용법: python migrate.py [command]")
        print("")
        print("명령어:")
        print("  init   - 테이블 생성")
        print("  seed   - 샘플 데이터 삽입")
        print("  reset  - 전체 초기화 (주의!)")
        print("  status - 데이터베이스 상태 확인")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        success = migrate_init()
    elif command == "seed":
        success = migrate_seed()
    elif command == "reset":
        success = migrate_reset()
    elif command == "status":
        success = migrate_status()
    else:
        print(f"❌ 알 수 없는 명령어: {command}")
        return
    
    print("")
    print("=" * 50)
    if success:
        print("✅ 완료!")
    else:
        print("❌ 실패!")


if __name__ == "__main__":
    main()
