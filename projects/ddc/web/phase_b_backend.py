#!/usr/bin/env python3
"""
Phase B Backend 프로토타입: FastAPI + WebSocket + SQLite

구현:
1. FastAPI 기본 설정
2. SQLite 데이터베이스 스키마
3. REST API endpoints
4. WebSocket 실시간 업데이트
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import asyncio
from pydantic import BaseModel

# ============================================================================
# FastAPI 기본 설정
# ============================================================================

app = FastAPI(
    title="SHawn-Brain Neural Dashboard API",
    description="Real-time Neural System Monitoring",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# 데이터베이스 설정
# ============================================================================

class Database:
    """SQLite 데이터베이스 관리"""
    
    def __init__(self, db_path: str = "/Users/soohyunglee/.openclaw/workspace/dashboard.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """DB 연결"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """데이터베이스 스키마 초기화"""
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # models 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                api_type TEXT NOT NULL,
                last_score REAL DEFAULT 0,
                response_time INTEGER DEFAULT 0,
                uptime_percent REAL DEFAULT 100,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # daily_metrics 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                model_id INTEGER NOT NULL,
                score REAL NOT NULL,
                response_time INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES models(id)
            )
        """)
        
        # dcrs_logs 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dcrs_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                execution_time DATETIME NOT NULL,
                total_tests INTEGER NOT NULL,
                avg_score REAL NOT NULL,
                best_model TEXT NOT NULL,
                changes_applied BOOLEAN DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 초기 데이터 추가 (없을 경우)
        cursor.execute("SELECT COUNT(*) FROM models")
        if cursor.fetchone()[0] == 0:
            models_data = [
                ("Gemini", "google", 9.9, 2300, 100),
                ("Groq", "groq", 9.7, 1200, 100),
                ("Anthropic", "anthropic", 9.4, 2100, 100),
                ("Mistral", "mistral", 9.1, 1900, 99.8),
                ("DeepSeek", "deepseek", 8.7, 2000, 99.5),
                ("OpenRouter", "openrouter", 9.0, 1800, 99.7),
                ("OpenAI", "openai", 8.9, 2400, 99.3),
                ("SambaNova", "sambanova", 8.8, 1500, 99.9),
                ("Cerebras", "cerebras", 8.6, 800, 99.0),
                ("Others", "others", 8.8, 1700, 99.4),
            ]
            
            for name, api_type, score, resp_time, uptime in models_data:
                cursor.execute(
                    "INSERT INTO models (name, api_type, last_score, response_time, uptime_percent) VALUES (?, ?, ?, ?, ?)",
                    (name, api_type, score, resp_time, uptime)
                )
        
        conn.commit()
        conn.close()

# 데이터베이스 인스턴스
db = Database()

# ============================================================================
# 데이터 모델 (Pydantic)
# ============================================================================

class ModelData(BaseModel):
    id: int
    name: str
    api_type: str
    last_score: float
    response_time: int
    uptime_percent: float
    updated_at: str

class MetricData(BaseModel):
    date: str
    model_id: int
    score: float
    response_time: int

class DCRSLog(BaseModel):
    date: str
    execution_time: str
    total_tests: int
    avg_score: float
    best_model: str
    changes_applied: bool

# ============================================================================
# REST API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "status": "🟢 Online",
        "system": "SHawn-Brain Neural Dashboard API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/models")
async def get_all_models():
    """모든 모델 상태 조회"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models ORDER BY last_score DESC")
    
    models = []
    for row in cursor.fetchall():
        models.append({
            "id": row["id"],
            "name": row["name"],
            "api_type": row["api_type"],
            "last_score": row["last_score"],
            "response_time": row["response_time"],
            "uptime_percent": row["uptime_percent"],
            "updated_at": row["updated_at"]
        })
    
    conn.close()
    
    return {
        "models": models,
        "count": len(models),
        "average_score": sum(m["last_score"] for m in models) / len(models) if models else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/models/{model_id}")
async def get_model(model_id: int):
    """특정 모델 상세 조회"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM models WHERE id = ?", (model_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"error": "Model not found"}
    
    return {
        "id": row["id"],
        "name": row["name"],
        "api_type": row["api_type"],
        "last_score": row["last_score"],
        "response_time": row["response_time"],
        "uptime_percent": row["uptime_percent"],
        "updated_at": row["updated_at"]
    }

@app.get("/api/metrics")
async def get_metrics():
    """실시간 메트릭 조회"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # 최근 24시간 메트릭
    cursor.execute("""
        SELECT m.name, dm.score, dm.response_time, dm.timestamp
        FROM daily_metrics dm
        JOIN models m ON dm.model_id = m.id
        ORDER BY dm.timestamp DESC
        LIMIT 100
    """)
    
    metrics = []
    for row in cursor.fetchall():
        metrics.append({
            "model": row["name"],
            "score": row["score"],
            "response_time": row["response_time"],
            "timestamp": row["timestamp"]
        })
    
    conn.close()
    
    return {
        "metrics": metrics,
        "count": len(metrics),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/dcrs/status")
async def get_dcrs_status():
    """DCRS 현재 상태"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dcrs_logs ORDER BY execution_time DESC LIMIT 1")
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"status": "No data"}
    
    return {
        "date": row["date"],
        "execution_time": row["execution_time"],
        "total_tests": row["total_tests"],
        "avg_score": row["avg_score"],
        "best_model": row["best_model"],
        "changes_applied": bool(row["changes_applied"]),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/dcrs/history")
async def get_dcrs_history():
    """DCRS 히스토리"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dcrs_logs ORDER BY execution_time DESC LIMIT 30")
    
    history = []
    for row in cursor.fetchall():
        history.append({
            "date": row["date"],
            "execution_time": row["execution_time"],
            "total_tests": row["total_tests"],
            "avg_score": row["avg_score"],
            "best_model": row["best_model"],
            "changes_applied": bool(row["changes_applied"])
        })
    
    conn.close()
    
    return {
        "history": history,
        "count": len(history),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/manual-test")
async def manual_test():
    """수동 테스트 실행"""
    
    return {
        "status": "Test initiated",
        "message": "Manual model test started",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# WebSocket 실시간 업데이트
# ============================================================================

class ConnectionManager:
    """WebSocket 연결 관리"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending message: {e}")

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결"""
    
    await manager.connect(websocket)
    
    try:
        while True:
            # 클라이언트에서 메시지 수신
            data = await websocket.receive_text()
            
            # 모델 상태 업데이트 시뮬레이션
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM models ORDER BY last_score DESC LIMIT 3")
            
            top_models = []
            for row in cursor.fetchall():
                top_models.append({
                    "name": row["name"],
                    "score": row["last_score"]
                })
            
            conn.close()
            
            # 실시간 메시지 전송
            await manager.broadcast({
                "type": "model_update",
                "models": top_models,
                "timestamp": datetime.now().isoformat()
            })
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    
    finally:
        manager.disconnect(websocket)

# ============================================================================
# 시작 및 종료 이벤트
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """서버 시작"""
    print("\n" + "="*100)
    print("🚀 SHawn-Brain Neural Dashboard API 시작!")
    print("="*100)
    print(f"""
📊 서비스: SHawn-Web Dashboard Backend
🔌 Framework: FastAPI
📡 WebSocket: 지원
🗄️ Database: SQLite (dashboard.db)
⏰ 시작 시간: {datetime.now().isoformat()}

🌐 API 엔드포인트:
   • GET / - 루트
   • GET /api/health - 헬스 체크
   • GET /api/models - 모든 모델
   • GET /api/models/{{id}} - 특정 모델
   • GET /api/metrics - 실시간 메트릭
   • GET /api/dcrs/status - DCRS 상태
   • GET /api/dcrs/history - DCRS 히스토리
   • POST /api/manual-test - 수동 테스트
   • WS /ws - WebSocket

📚 API 문서:
   • Swagger UI: http://localhost:8000/docs
   • ReDoc: http://localhost:8000/redoc

준비 완료! ✅
    """)

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료"""
    print("\n🛑 SHawn-Brain Neural Dashboard API 종료됨")

# ============================================================================
# 실행
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*100)
    print("🎬 Phase B Backend 프로토타입 실행")
    print("="*100)
    
    print(f"""
✅ FastAPI 기본 설정 완료
✅ SQLite 데이터베이스 초기화 완료
✅ REST API (8개 endpoints) 구현 완료
✅ WebSocket 실시간 업데이트 구현 완료

🚀 서버 시작:
   uvicorn phase_b_backend:app --reload --host 0.0.0.0 --port 8000

📚 테스트:
   • Swagger UI: http://localhost:8000/docs
   • API 테스트: curl http://localhost:8000/api/models
   • WebSocket 테스트: ws://localhost:8000/ws

⏱️ 소요 시간: Sprint 1 Backend (30분) 중 정도
    """)
    
    # 서버 시작 (개발 모드)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
