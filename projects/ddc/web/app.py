"""
FastAPI Backend - SHawn-Brain Web 서버

역할:
- 카트리지 API 제공
- 신경계 상태 모니터링
- WebSocket 실시간 통신
- 문서 자동 생성 (Swagger)

의존성:
- fastapi
- uvicorn
- pydantic
- aiofiles
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import json
import logging
from scripts.maintenance.auto_router import AutoRouter
from projects.ddc.brain.brain_core.chat_engine import get_chat_engine

# ============================================================================
# 1. 설정
# ============================================================================

app = FastAPI(
    title="Digital Da Vinci API",
    description="Digital Da Vinci v0.0.1 (Prototype) - 신경계 기반 AI 서버",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 설정 (React 프론트엔드 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 2. 데이터 모델
# ============================================================================

class BioAnalysisRequest(BaseModel):
    """Bio Cartridge 분석 요청"""
    image_path: str
    cell_type: Optional[str] = None
    use_neocortex: bool = True

class BioAnalysisResponse(BaseModel):
    """Bio Cartridge 분석 응답"""
    status: str
    cell_type: str
    health_status: str
    confidence: float
    neocortex_features: Dict[str, Any]
    timestamp: str

class InvAnalysisRequest(BaseModel):
    """Inv Cartridge 분석 요청"""
    ticker: str
    use_neocortex: bool = True

class InvAnalysisResponse(BaseModel):
    """Inv Cartridge 분석 응답"""
    status: str
    ticker: str
    technical_score: float
    fundamental_score: float
    recommendation: str
    neocortex_decision: Dict[str, Any]
    timestamp: str

class ChatRequest(BaseModel):
    """일반 대화 요청"""
    message: str
    user_id: Optional[Any] = "default_user"  # 문자열 또는 정수 모두 허용
    level: Optional[str] = "L3"  # L1 (Fast) or L3 (Deep)

class ChatResponse(BaseModel):
    """일반 대화 응답"""
    status: str
    response: str
    task_type: str
    model_used: str
    confidence: float
    timestamp: str

class SystemStatus(BaseModel):
    """시스템 상태"""
    status: str
    version: str
    uptime: float
    models_available: List[str]
    cartridges_active: List[str]
    neural_health: Dict[str, float]

# ============================================================================
# 3. 신경계 상태 추적
# ============================================================================

class NeuralSystemMonitor:
    """신경계 모니터링"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.api_calls = {
            'bio': 0,
            'inv': 0,
            'total': 0
        }
        self.neural_health = {
            'brainstem': 0.95,        # L1
            'limbic': 0.93,           # L2
            'neocortex': 0.94,        # L3
            'neuronet': 0.98,         # L4
            'avg': 0.95
        }
    
    def record_call(self, cartridge: str):
        """API 호출 기록"""
        self.api_calls[cartridge] += 1
        self.api_calls['total'] += 1
    
    def get_status(self) -> SystemStatus:
        """시스템 상태 반환"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return SystemStatus(
            status="🟢 healthy",
            version="0.0.1",
            uptime=uptime,
            models_available=["Gemini", "Groq", "Claude", "DeepSeek", "OpenRouter"],
            cartridges_active=["bio", "inv", "lit", "quant", "astro"],
            neural_health=self.neural_health
        )

monitor = NeuralSystemMonitor()
router = AutoRouter()
chat_engine = get_chat_engine()

# ============================================================================
# 4. 라우트: 헬스 체크
# ============================================================================

@app.get("/", tags=["System"])
async def root():
    """루트 엔드포인트"""
    return {
        "name": "Digital Da Vinci API",
        "project": "Digital Da Vinci v0.0.1 (Prototype)",
        "version": "0.0.1",
        "status": "🟢 Running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["System"])
async def health_check():
    """헬스 체크"""
    return {
        "status": "🟢 healthy",
        "timestamp": datetime.now().isoformat(),
        "neural_system": monitor.neural_health
    }

@app.get("/status", tags=["System"], response_model=SystemStatus)
async def system_status():
    """시스템 상태"""
    return monitor.get_status()

# ============================================================================
# 5. 라우트: Bio Cartridge
# ============================================================================

@app.post("/api/bio/analyze_image", tags=["Bio Cartridge"], response_model=BioAnalysisResponse)
async def analyze_bio_image(request: BioAnalysisRequest):
    """
    세포/오가노이드 이미지 분석
    
    - **image_path**: 이미지 파일 경로
    - **cell_type**: 세포 종류 (자동 감지)
    - **use_neocortex**: neocortex 협력 사용
    
    Returns:
        BioAnalysisResponse: 분석 결과
    """
    try:
        monitor.record_call('bio')
        
        logger.info(f"Bio 분석 시작: {request.image_path}")
        
        # 실제 구현시: bio_interface.py 호출
        # from ddc.cartridges.bio import bio_interface
        # result = bio_interface.analyze_bio_image(request.image_path)
        
        # 임시 응답 (시뮬레이션)
        return BioAnalysisResponse(
            status="success",
            cell_type="Human ESC",
            health_status="healthy",
            confidence=0.94,
            neocortex_features={
                "occipital_visual": 0.92,      # 시각 특성 (후두엽)
                "temporal_memory": 0.95        # 기억 패턴 (측두엽)
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Bio 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bio/analyze_video", tags=["Bio Cartridge"])
async def analyze_bio_video(file: UploadFile = File(...)):
    """
    비디오 파일 분석 (시계열)
    """
    try:
        monitor.record_call('bio')
        
        logger.info(f"Bio 비디오 분석: {file.filename}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "frames_analyzed": 100,
            "developmental_stages": [
                {"day": 1, "status": "initial"},
                {"day": 3, "status": "proliferation"},
                {"day": 7, "status": "differentiation"}
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Bio 비디오 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# 6. 라우트: Inv Cartridge
# ============================================================================

@app.post("/api/inv/analyze_stock", tags=["Inv Cartridge"], response_model=InvAnalysisResponse)
async def analyze_investment(request: InvAnalysisRequest):
    """
    주식 분석
    
    - **ticker**: 종목 코드 (e.g., TSLA, 005930)
    - **use_neocortex**: neocortex 협력 사용
    
    Returns:
        InvAnalysisResponse: 투자 분석 결과
    """
    try:
        monitor.record_call('inv')
        
        logger.info(f"Inv 분석 시작: {request.ticker}")
        
        # 실제 구현시: inv_interface.py 호출
        # from ddc.cartridges.inv import inv_interface
        # result = inv_interface.analyze_stock_with_neocortex(request.ticker, {})
        
        # 임시 응답
        return InvAnalysisResponse(
            status="success",
            ticker=request.ticker,
            technical_score=0.85,
            fundamental_score=0.78,
            recommendation="🟢 BUY",
            neocortex_decision={
                "parietal_analysis": 0.88,     # 수치 분석 (두정엽)
                "prefrontal_decision": 0.92    # 의사결정 (전두엽)
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Inv 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inv/portfolio_optimization", tags=["Inv Cartridge"])
async def portfolio_optimization(holdings: Dict[str, float]):
    """
    포트폴리오 최적화
    
    Args:
        holdings: 현재 보유 종목 {'TSLA': 0.3, '005930': 0.7}
    """
    try:
        monitor.record_call('inv')
        
        logger.info(f"포트폴리오 최적화: {list(holdings.keys())}")
        
        return {
            "status": "success",
            "current_portfolio": holdings,
            "optimized_portfolio": {
                k: v * 1.05 for k, v in holdings.items()  # 임시
            },
            "improvement": "3.2%",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"포트폴리오 최적화 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# 7. 라우트: Chat Engine (General Conversation)
# ============================================================================

@app.post("/api/chat/ask", tags=["Chat Engine"], response_model=ChatResponse)
async def chat_ask(request: ChatRequest):
    """
    일반 대화 및 질문 처리
    
    - **message**: 사용자 입력 메시지
    - **user_id**: 사용자 식별자
    
    Returns:
        ChatResponse: L2 감정 분석이 포함된 응답
    """
    try:
        monitor.record_call('total')
        
        # ChatEngine의 get_response 호출 (L2 감정 분석 포함)
        logger.info(f"Chat Request from user {request.user_id}: {request.message}")
        
        # user_id를 정수로 변환 (기본값: 0)
        try:
            user_id_int = int(request.user_id) if request.user_id != "default_user" else 0
        except ValueError:
            user_id_int = 0
        
        response_text = await chat_engine.get_response(
            text=request.message,
            user_id=user_id_int
        )
        
        return ChatResponse(
            status="success",
            response=response_text,
            task_type="general_conversation",
            model_used="gemini-1.5-pro",  # 실제 주력 모델로 수정
            confidence=0.95,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Chat Engine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# 7. 라우트: 신경계 모니터링
# ============================================================================

@app.get("/api/neural/health", tags=["Neural System"])
async def neural_health():
    """신경계 건강도"""
    return {
        "status": "🟢 healthy",
        "neural_levels": {
            "L1_Brainstem": {
                "status": "🟢 active",
                "health": 0.95,
                "function": "기본 기능"
            },
            "L2_Limbic": {
                "status": "🟢 active",
                "health": 0.93,
                "function": "감정/주의"
            },
            "L3_Neocortex": {
                "status": "🟢 active",
                "health": 0.94,
                "function": "학습/분석"
            },
            "L4_NeuroNet": {
                "status": "🟢 active",
                "health": 0.98,
                "function": "신경망"
            }
        },
        "average_health": 0.95,
        "api_calls": monitor.api_calls,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/neural/cartridges", tags=["Neural System"])
async def cartridges_status():
    """카트리지 상태"""
    return {
        "active_cartridges": {
            "bio": {
                "status": "🟢 active",
                "neocortex_lobes": ["occipital", "temporal"],
                "api_calls": monitor.api_calls['bio']
            },
            "inv": {
                "status": "🟢 active",
                "neocortex_lobes": ["prefrontal", "parietal"],
                "api_calls": monitor.api_calls['inv']
            },
            "planned": ["lit", "quant", "astro"]
        },
        "total_api_calls": monitor.api_calls['total'],
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 8. WebSocket (실시간 통신)
# ============================================================================

@app.websocket("/ws/neural_stream")
async def websocket_neural_stream(websocket: WebSocket):
    """
    실시간 신경 신호 스트리밍
    """
    await websocket.accept()
    try:
        while True:
            # 신경계 상태 실시간 전송
            data = {
                "type": "neural_update",
                "timestamp": datetime.now().isoformat(),
                "levels": monitor.neural_health,
                "api_calls": monitor.api_calls
            }
            await websocket.send_json(data)
            await asyncio.sleep(2)  # 2초마다 업데이트
    except Exception as e:
        logger.error(f"WebSocket 오류: {e}")
    finally:
        await websocket.close()

# ============================================================================
# 9. 에러 핸들러
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# 10. 시작/종료 이벤트
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """서버 시작"""
    logger.info("🚀 SHawn-Brain API 시작!")
    logger.info("📊 D-CNS 신경계 활성화")
    logger.info("🧬 카트리지 초기화")
    logger.info("📡 API 문서: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료"""
    logger.info("🛑 SHawn-Brain API 종료")
    logger.info(f"📊 총 API 호출: {monitor.api_calls['total']}")

# ============================================================================
# 11. 메인
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
