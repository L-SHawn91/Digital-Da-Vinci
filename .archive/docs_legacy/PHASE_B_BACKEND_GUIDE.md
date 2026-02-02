# 🎨 Phase B Backend 프로토타입 - 상세 구현 가이드

## 📋 개요

이 문서는 SHawn-Web Dashboard의 백엔드 구현을 위한 완전한 프로토타입입니다.

**프레임워크**: FastAPI + WebSocket
**데이터베이스**: SQLite (개발) → PostgreSQL (프로덕션)
**실시간 통신**: WebSocket (Socket.io)

---

## 🔧 Step 1: 프로젝트 설정 (30분)

### 1.1 디렉토리 구조
```
phase_b_backend/
├── main.py                  # FastAPI 앱
├── database.py              # 데이터베이스 관리
├── models.py                # Pydantic 모델
├── routers/
│   ├── models.py            # /api/models endpoints
│   ├── metrics.py           # /api/metrics endpoints
│   ├── dcrs.py              # /api/dcrs endpoints
│   └── cartridges.py        # /api/cartridges endpoints
├── websocket/
│   └── manager.py           # WebSocket 연결 관리
├── requirements.txt
└── docker-compose.yml
```

### 1.2 requirements.txt
```
fastapi==0.104.0
uvicorn==0.24.0
sqlalchemy==2.0.0
pydantic==2.0.0
python-socketio==5.10.0
python-multipart==0.0.6
```

### 1.3 설치 명령어
```bash
pip install -r requirements.txt
```

---

## 🗄️ Step 2: 데이터베이스 스키마 (30분)

### 2.1 Models 테이블
```sql
CREATE TABLE models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    api_type TEXT NOT NULL,
    last_score REAL DEFAULT 0,
    response_time INTEGER DEFAULT 0,
    uptime_percent REAL DEFAULT 100,
    status TEXT DEFAULT 'healthy',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 초기 데이터
INSERT INTO models (name, api_type, last_score, response_time, uptime_percent) VALUES
('Gemini', 'google', 9.9, 2300, 100),
('Groq', 'groq', 9.7, 1200, 100),
('Anthropic', 'anthropic', 9.4, 2100, 100),
('Mistral', 'mistral', 9.1, 1900, 99.8),
('DeepSeek', 'deepseek', 8.7, 2000, 99.5),
('OpenRouter', 'openrouter', 9.0, 1800, 99.7),
('OpenAI', 'openai', 8.9, 2400, 99.3),
('SambaNova', 'sambanova', 8.8, 1500, 99.9),
('Cerebras', 'cerebras', 8.6, 800, 99.0),
('Others', 'others', 8.8, 1700, 99.4);
```

### 2.2 Daily Metrics 테이블
```sql
CREATE TABLE daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    model_id INTEGER NOT NULL,
    score REAL NOT NULL,
    response_time INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- 인덱스
CREATE INDEX idx_date ON daily_metrics(date);
CREATE INDEX idx_model_id ON daily_metrics(model_id);
```

### 2.3 DCRS Logs 테이블
```sql
CREATE TABLE dcrs_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    execution_time DATETIME NOT NULL,
    total_tests INTEGER NOT NULL,
    avg_score REAL NOT NULL,
    best_model TEXT NOT NULL,
    changes_applied BOOLEAN DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_dcrs_date ON dcrs_logs(date);
```

---

## 🔌 Step 3: REST API Endpoints 구현 (60분)

### 3.1 기본 헬스 체크
```python
@app.get("/")
async def root():
    return {
        "status": "🟢 Online",
        "system": "SHawn-Brain Neural Dashboard API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
```

### 3.2 모델 관련 Endpoints
```python
# GET /api/models - 모든 모델 조회
@app.get("/api/models")
async def get_all_models():
    """
    모든 모델의 현재 상태를 반환
    
    Response:
    {
        "models": [
            {
                "id": 1,
                "name": "Gemini",
                "last_score": 9.9,
                "response_time": 2300,
                "uptime_percent": 100
            }
        ],
        "average_score": 9.09,
        "timestamp": "2026-02-01T08:00:00"
    }
    """
    pass

# GET /api/models/{model_id} - 특정 모델 조회
@app.get("/api/models/{model_id}")
async def get_model(model_id: int):
    """특정 모델의 상세 정보 반환"""
    pass
```

### 3.3 메트릭 Endpoints
```python
# GET /api/metrics - 실시간 메트릭
@app.get("/api/metrics")
async def get_metrics():
    """
    최근 24시간 메트릭 반환
    
    Response:
    {
        "metrics": [
            {
                "model": "Gemini",
                "score": 9.9,
                "response_time": 2300,
                "timestamp": "2026-02-01T08:00:00"
            }
        ]
    }
    """
    pass

# GET /api/metrics?model_id=1&days=7 - 필터링된 메트릭
@app.get("/api/metrics")
async def get_filtered_metrics(model_id: int = None, days: int = 1):
    """특정 모델, 특정 기간의 메트릭"""
    pass
```

### 3.4 DCRS Endpoints
```python
# GET /api/dcrs/status - 현재 DCRS 상태
@app.get("/api/dcrs/status")
async def get_dcrs_status():
    """
    최근 DCRS 실행 결과 반환
    
    Response:
    {
        "date": "2026-02-01",
        "execution_time": "2026-02-01T08:00:00",
        "total_tests": 10,
        "avg_score": 9.09,
        "best_model": "Gemini",
        "changes_applied": true
    }
    """
    pass

# GET /api/dcrs/history - DCRS 히스토리
@app.get("/api/dcrs/history")
async def get_dcrs_history(days: int = 7):
    """지난 N일간의 DCRS 실행 기록"""
    pass
```

### 3.5 카트리지 Endpoints
```python
# GET /api/cartridges - 카트리지 상태
@app.get("/api/cartridges")
async def get_cartridges():
    """
    Response:
    {
        "cartridges": [
            {
                "name": "Bio-Cartridge",
                "status": "healthy",
                "last_execution": "2026-02-01T07:30:00",
                "success_rate": 98.5
            },
            {
                "name": "Investment-Cartridge",
                "status": "healthy",
                "last_execution": "2026-02-01T07:45:00",
                "success_rate": 99.2
            }
        ]
    }
    """
    pass

# GET /api/cartridges/{cartridge_name}/results - 최근 실행 결과
@app.get("/api/cartridges/{cartridge_name}/results")
async def get_cartridge_results(cartridge_name: str):
    """카트리지의 최근 실행 결과"""
    pass
```

### 3.6 수동 테스트 Endpoint
```python
# POST /api/manual-test - 수동 모델 테스트 실행
@app.post("/api/manual-test")
async def manual_test(models: List[str] = None):
    """
    특정 모델들의 테스트를 수동으로 실행
    
    Request:
    {
        "models": ["Gemini", "Groq"]  # 생략 시 모든 모델 테스트
    }
    
    Response:
    {
        "status": "testing",
        "models": ["Gemini", "Groq"],
        "start_time": "2026-02-01T08:10:00"
    }
    """
    pass
```

---

## 📡 Step 4: WebSocket 실시간 업데이트 (45분)

### 4.1 WebSocket Manager
```python
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """새로운 WebSocket 연결"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """WebSocket 연결 해제"""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """모든 연결된 클라이언트에게 메시지 전송"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error: {e}")
    
    async def broadcast_personal(self, websocket: WebSocket, message: dict):
        """특정 클라이언트에게만 메시지 전송"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error: {e}")

manager = ConnectionManager()
```

### 4.2 WebSocket Endpoint
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 연결
    
    사용 예:
    ws = new WebSocket("ws://localhost:8000/ws")
    ws.onmessage = function(event) {
        console.log(JSON.parse(event.data))
    }
    """
    
    await manager.connect(websocket)
    
    try:
        while True:
            # 클라이언트 메시지 수신
            data = await websocket.receive_text()
            
            # 명령 처리
            if data == "get_models":
                # 모든 모델 상태 전송
                message = {
                    "type": "models_update",
                    "models": [...],
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast_personal(websocket, message)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    
    finally:
        manager.disconnect(websocket)
```

### 4.3 백그라운드 업데이트 작업
```python
import asyncio
from datetime import datetime

async def update_models_periodically():
    """주기적으로 모델 상태 업데이트"""
    
    while True:
        # 5초마다 실행
        await asyncio.sleep(5)
        
        # 모든 모델 상태 조회
        models = await get_all_models()
        
        # 모든 클라이언트에 브로드캐스트
        message = {
            "type": "model_update",
            "models": models,
            "timestamp": datetime.now().isoformat()
        }
        
        await manager.broadcast(message)

# 서버 시작 시 백그라운드 작업 시작
@app.on_event("startup")
async def startup():
    asyncio.create_task(update_models_periodically())
```

### 4.4 WebSocket 이벤트 타입

| Event Type | 설명 | Frequency |
|-----------|------|-----------|
| `model_update` | 모델 점수/상태 업데이트 | 5초 |
| `neural_signal` | 신경신호 강도 변화 | 1분 |
| `alert` | 시스템 알림 | 필요시 |
| `dcrs_progress` | DCRS 실행 진행률 | 08:00-08:05 |
| `cartridge_result` | 카트리지 실행 결과 | 필요시 |

---

## 🧪 Step 5: 테스트 & 디버깅 (30분)

### 5.1 테스트 스크립트
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 헬스 체크
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())

# 모든 모델 조회
response = requests.get(f"{BASE_URL}/api/models")
print(json.dumps(response.json(), indent=2))

# 특정 모델 조회
response = requests.get(f"{BASE_URL}/api/models/1")
print(json.dumps(response.json(), indent=2))

# 실시간 메트릭
response = requests.get(f"{BASE_URL}/api/metrics")
print(json.dumps(response.json(), indent=2))

# DCRS 상태
response = requests.get(f"{BASE_URL}/api/dcrs/status")
print(json.dumps(response.json(), indent=2))

# 카트리지 상태
response = requests.get(f"{BASE_URL}/api/cartridges")
print(json.dumps(response.json(), indent=2))
```

### 5.2 WebSocket 테스트
```javascript
// 브라우저 콘솔
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
    console.log("Connected");
    ws.send("get_models");
};

ws.onmessage = (event) => {
    console.log("Received:", JSON.parse(event.data));
};

ws.onerror = (error) => {
    console.error("Error:", error);
};

ws.onclose = () => {
    console.log("Disconnected");
};
```

### 5.3 API 문서
```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## 🚀 Step 6: 실행 방법

### 6.1 개발 서버 시작
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6.2 프로덕션 배포
```bash
# Gunicorn + Uvicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# 또는 Docker
docker build -t shawn-brain-api .
docker run -p 8000:8000 shawn-brain-api
```

---

## 📊 구현 진행 상황

✅ 프로젝트 구조 설계 (30분)
✅ 데이터베이스 스키마 (30분)
✅ REST API Endpoints (60분)
✅ WebSocket 구현 (45분)
✅ 테스트 스크립트 (30분)

**총 소요 예상 시간: 2-3시간**

---

## 🎯 다음 단계 (Phase B Frontend)

Backend 완료 후:
1. React 프로젝트 설정
2. 대시보드 UI 구현
3. API 연결 & WebSocket 통합
4. 실시간 차트 구현
5. 성능 최적화

**예상 시간: 2-3시간**

---

**준비 완료!** 🚀
