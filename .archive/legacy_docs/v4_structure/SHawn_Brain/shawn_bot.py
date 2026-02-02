"""
SHawn-Bot Implementation
숀봇: 카트리지 기반 실행 도구

역할:
  1. 카트리지 로드 & 관리
  2. 박사님 요청 이해
  3. 적절한 카트리지 선택
  4. 카트리지 실행
  5. 결과 정리 & 제시
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime


# ============================================================================
# 1. 데이터 클래스 & Enum
# ============================================================================

class CartridgeType(Enum):
    """카트리지 타입"""
    BIO = "bio"
    INVESTMENT = "investment"
    UNKNOWN = "unknown"


class RequestType(Enum):
    """요청 타입"""
    CELL_ANALYSIS = "cell_analysis"  # 세포 분석
    STOCK_ANALYSIS = "stock_analysis"  # 주식 분석
    HELP = "help"  # 도움
    UNKNOWN = "unknown"


@dataclass
class UserRequest:
    """사용자 요청"""
    text: str
    request_type: RequestType
    cartridge: CartridgeType
    parameters: Dict[str, Any]
    timestamp: str


@dataclass
class CartridgeResult:
    """카트리지 실행 결과"""
    cartridge_type: CartridgeType
    status: str  # "success" or "error"
    data: Any
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0


# ============================================================================
# 2. 카트리지 인터페이스
# ============================================================================

class CartridgeInterface:
    """카트리지 인터페이스 (모든 카트리지가 상속)"""
    
    def __init__(self):
        self.name = "BaseCartridge"
        self.version = "1.0"
    
    def execute(self, **kwargs) -> Any:
        """카트리지 실행"""
        raise NotImplementedError
    
    def validate_params(self, **kwargs) -> bool:
        """매개변수 검증"""
        raise NotImplementedError


# ============================================================================
# 3. 카트리지 구현 (프로토타입)
# ============================================================================

class BioCartridgeAdapter(CartridgeInterface):
    """Bio-Cartridge 어댑터"""
    
    def __init__(self):
        super().__init__()
        self.name = "Bio-Cartridge"
        self.version = "1.0-Alpha"
    
    def execute(self, image_path: str = None, **kwargs) -> Dict:
        """
        Bio-Cartridge 실행
        
        Args:
            image_path: 이미지 경로
            
        Returns:
            분석 결과
        """
        if not self.validate_params(image_path=image_path):
            return {"error": "Invalid parameters"}
        
        # 프로토타입: 모의 데이터 반환
        # 실제로는 bio_cartridge.py의 BioCartridge 클래스 사용
        result = {
            "cell_type": "Human ESC H9",
            "cell_type_confidence": 94.0,
            "differentiation_stage": "Stage 3",
            "stage_confidence": 85.0,
            "health_score": 95.0,
            "health_status": "Excellent",
            "morphology": "중간 밀도, 정상 형태",
            "density": 52.3,
            "aggregation": 45.2,
            "anomalies": ["none"],
            "anomaly_severity": 0.0,
            "recommendations": [
                "계속 배양, 다음 단계 진행 가능",
                "상태 모니터링 지속"
            ],
            "analysis_confidence": 89.5,
            "image_quality": "우수 (선명)"
        }
        
        return result
    
    def validate_params(self, **kwargs) -> bool:
        """매개변수 검증"""
        return "image_path" in kwargs and kwargs["image_path"] is not None


class InvestmentCartridgeAdapter(CartridgeInterface):
    """Investment-Cartridge 어댑터"""
    
    def __init__(self):
        super().__init__()
        self.name = "Investment-Cartridge"
        self.version = "1.0-Alpha"
    
    def execute(self, symbol: str = None, market: str = "USA", **kwargs) -> Dict:
        """
        Investment-Cartridge 실행
        
        Args:
            symbol: 주식 심볼 (예: "TSLA")
            market: 시장 ("USA" 또는 "KOREA")
            
        Returns:
            분석 결과
        """
        if not self.validate_params(symbol=symbol):
            return {"error": "Invalid parameters"}
        
        # 프로토타입: 모의 데이터 반환
        # 실제로는 investment_cartridge.py의 InvestmentCartridge 클래스 사용
        result = {
            "symbol": symbol,
            "market": market,
            "current_price": 245.0,
            "short_term": {
                "signal": "매수",
                "target_price": 265.0,
                "stop_loss": 230.0,
                "take_profit": 280.0,
                "risk_reward": 2.3
            },
            "long_term": {
                "signal": "매수",
                "target_price": 318.5,
                "growth_potential": "중간-높음"
            },
            "technical": {
                "trend": "상승",
                "rsi": 55.0,
                "signal_strength": 70.0
            },
            "analyst_consensus": {
                "buy_count": 15,
                "hold_count": 3,
                "sell_count": 2,
                "average_target_price": 265.0
            },
            "final_recommendation": "BUY",
            "confidence": 85.0
        }
        
        return result
    
    def validate_params(self, **kwargs) -> bool:
        """매개변수 검증"""
        return "symbol" in kwargs and kwargs["symbol"] is not None


# ============================================================================
# 4. 카트리지 관리자
# ============================================================================

class CartridgeManager:
    """카트리지 로드, 관리, 실행"""
    
    def __init__(self):
        """카트리지 초기화"""
        self.cartridges: Dict[CartridgeType, CartridgeInterface] = {
            CartridgeType.BIO: BioCartridgeAdapter(),
            CartridgeType.INVESTMENT: InvestmentCartridgeAdapter()
        }
        print("✅ CartridgeManager 초기화 완료")
    
    def get_cartridge(self, cartridge_type: CartridgeType) -> Optional[CartridgeInterface]:
        """카트리지 획득"""
        return self.cartridges.get(cartridge_type)
    
    def execute_cartridge(self, 
                         cartridge_type: CartridgeType,
                         **kwargs) -> CartridgeResult:
        """
        카트리지 실행
        
        Args:
            cartridge_type: 카트리지 타입
            **kwargs: 카트리지 매개변수
            
        Returns:
            CartridgeResult: 실행 결과
        """
        import time
        
        cartridge = self.get_cartridge(cartridge_type)
        if not cartridge:
            return CartridgeResult(
                cartridge_type=cartridge_type,
                status="error",
                data=None,
                error_message=f"카트리지를 찾을 수 없음: {cartridge_type}"
            )
        
        try:
            start_time = time.time()
            result = cartridge.execute(**kwargs)
            execution_time = (time.time() - start_time) * 1000
            
            return CartridgeResult(
                cartridge_type=cartridge_type,
                status="success",
                data=result,
                execution_time_ms=execution_time
            )
        
        except Exception as e:
            return CartridgeResult(
                cartridge_type=cartridge_type,
                status="error",
                data=None,
                error_message=str(e)
            )
    
    def list_cartridges(self) -> List[str]:
        """사용 가능한 카트리지 목록"""
        return [c.name for c in self.cartridges.values()]


# ============================================================================
# 5. 요청 분석기 (NLU - Natural Language Understanding)
# ============================================================================

class RequestAnalyzer:
    """사용자 요청 분석"""
    
    def __init__(self):
        """분석기 초기화"""
        # 세포 분석 키워드
        self.cell_keywords = [
            "세포", "오가노이드", "organoid", "cell",
            "배양", "culture", "ESC", "iPS",
            "줄기세포", "stem", "분석", "analyze"
        ]
        
        # 주식 분석 키워드
        self.stock_keywords = [
            "주식", "stock", "종목", "매수", "매도",
            "buy", "sell", "투자", "investment",
            "목표가", "target", "분석", "analyze",
            "TSLA", "AAPL", "삼성", "005930"
        ]
    
    def analyze(self, text: str) -> UserRequest:
        """
        사용자 요청 분석
        
        Args:
            text: 사용자 입력 텍스트
            
        Returns:
            UserRequest: 분석된 요청
        """
        text_lower = text.lower()
        
        # 요청 타입 판단
        request_type = self._classify_request(text_lower)
        
        # 카트리지 선택
        cartridge = self._select_cartridge(request_type)
        
        # 매개변수 추출
        parameters = self._extract_parameters(text, request_type)
        
        return UserRequest(
            text=text,
            request_type=request_type,
            cartridge=cartridge,
            parameters=parameters,
            timestamp=datetime.now().isoformat()
        )
    
    def _classify_request(self, text: str) -> RequestType:
        """요청 타입 분류"""
        text_lower = text.lower()
        
        # 도움 요청 (우선 순위 높음)
        if any(kw in text_lower for kw in ["도움", "help", "뭘 할 수", "어떻게", "뭘 도와"]):
            return RequestType.HELP
        
        # 주식 심볼 확인 (TSLA, 005930 등)
        if re.search(r'\b[A-Z]{1,5}\b', text) or any(kw in text_lower for kw in ["주식", "stock", "종목", "매수", "매도", "buy", "sell", "투자", "investment", "목표가", "target", "분석"]):
            return RequestType.STOCK_ANALYSIS
        
        # 세포 분석 요청
        if any(kw in text_lower for kw in self.cell_keywords):
            return RequestType.CELL_ANALYSIS
        
        return RequestType.UNKNOWN
    
    def _select_cartridge(self, request_type: RequestType) -> CartridgeType:
        """요청에 맞는 카트리지 선택"""
        if request_type == RequestType.CELL_ANALYSIS:
            return CartridgeType.BIO
        elif request_type == RequestType.STOCK_ANALYSIS:
            return CartridgeType.INVESTMENT
        else:
            return CartridgeType.UNKNOWN
    
    def _extract_parameters(self, text: str, request_type: RequestType) -> Dict[str, Any]:
        """매개변수 추출"""
        params = {}
        
        if request_type == RequestType.CELL_ANALYSIS:
            # 이미지 경로 추출 (간단한 정규식)
            image_match = re.search(r'([^\s]+\.(jpg|jpeg|png|tiff))', text, re.IGNORECASE)
            if image_match:
                params["image_path"] = image_match.group(1)
            else:
                # 이미지 경로 없으면 모의 경로 사용
                params["image_path"] = "sample_cell.jpg"
        
        elif request_type == RequestType.STOCK_ANALYSIS:
            # 주식 심볼 추출 (대문자 1-5자)
            symbol_match = re.search(r'\b([A-Z]{1,5})\b', text)
            if symbol_match:
                params["symbol"] = symbol_match.group(1)
            elif "삼성" in text:
                params["symbol"] = "005930"
            else:
                params["symbol"] = "TSLA"  # 기본값
            
            # 시장 판단
            if "한국" in text or "KRX" in text or any(kw in text for kw in ["005", "삼성", "현대", "LG"]):
                params["market"] = "KOREA"
            else:
                params["market"] = "USA"
        
        return params


# ============================================================================
# 6. 결과 포맷터
# ============================================================================

class ResultFormatter:
    """결과를 사용자 친화적으로 포맷팅"""
    
    @staticmethod
    def format_bio_result(data: Dict) -> str:
        """Bio-Cartridge 결과 포맷팅"""
        if "error" in data:
            return f"❌ 오류: {data['error']}"
        
        report = f"""
✅ **세포 분석 완료**

【기본 정보】
• 세포 타입: {data.get('cell_type', 'N/A')} (신뢰도: {data.get('cell_type_confidence', 0):.1f}%)
• 분화 단계: {data.get('differentiation_stage', 'N/A')} (신뢰도: {data.get('stage_confidence', 0):.1f}%)

【건강도】
• 점수: {data.get('health_score', 0):.0f}/100
• 상태: {data.get('health_status', 'N/A')}

【특성】
• 형태: {data.get('morphology', 'N/A')}
• 밀도: {data.get('density', 0):.1f}%
• 응집도: {data.get('aggregation', 0):.1f}%

【이상 탐지】
• 이상: {', '.join(data.get('anomalies', []))}
• 심각도: {data.get('anomaly_severity', 0):.1f}%

【권장 조치】
{chr(10).join(f'• {r}' for r in data.get('recommendations', []))}

【메타정보】
• 분석 신뢰도: {data.get('analysis_confidence', 0):.1f}%
• 이미지 품질: {data.get('image_quality', 'N/A')}
"""
        return report.strip()
    
    @staticmethod
    def format_investment_result(data: Dict) -> str:
        """Investment-Cartridge 결과 포맷팅"""
        if "error" in data:
            return f"❌ 오류: {data['error']}"
        
        report = f"""
✅ **주식 분석 완료**

【종목 정보】
• 심볼: {data.get('symbol', 'N/A')} ({data.get('market', 'N/A')})
• 현재가: ${data.get('current_price', 0):,.2f}

【단기 분석 (1주-3개월)】
• 추천: {data.get('short_term', {}).get('signal', 'N/A')}
• 목표가: ${data.get('short_term', {}).get('target_price', 0):,.2f}
• 손절가: ${data.get('short_term', {}).get('stop_loss', 0):,.2f}
• 익절가: ${data.get('short_term', {}).get('take_profit', 0):,.2f}
• 리스크/보상: 1:{data.get('short_term', {}).get('risk_reward', 0):.1f}

【장기 분석 (1년-5년)】
• 추천: {data.get('long_term', {}).get('signal', 'N/A')}
• 목표가: ${data.get('long_term', {}).get('target_price', 0):,.2f}
• 성장성: {data.get('long_term', {}).get('growth_potential', 'N/A')}

【기술적 분석】
• 추세: {data.get('technical', {}).get('trend', 'N/A')}
• RSI: {data.get('technical', {}).get('rsi', 0):.1f}
• 신호 강도: {data.get('technical', {}).get('signal_strength', 0):.0f}%

【애널리스트 의견】
• 매수: {data.get('analyst_consensus', {}).get('buy_count', 0)}명
• 보유: {data.get('analyst_consensus', {}).get('hold_count', 0)}명
• 매도: {data.get('analyst_consensus', {}).get('sell_count', 0)}명
• 평균 목표가: ${data.get('analyst_consensus', {}).get('average_target_price', 0):,.2f}

【최종 추천】
• 신호: {data.get('final_recommendation', 'N/A')}
• 신뢰도: {data.get('confidence', 0):.0f}%
"""
        return report.strip()
    
    @staticmethod
    def format_help() -> str:
        """도움말 포맷팅"""
        return """
🤖 **SHawn-Bot 도움말**

제가 할 수 있는 일:

1️⃣ **세포 분석** (Bio-Cartridge)
   예: "이 세포 사진 분석해줄래?" [사진 업로드]
   → 세포 타입, 분화 단계, 건강도 평가

2️⃣ **주식 분석** (Investment-Cartridge)
   예: "TSLA 분석해줘", "테슬라 주식은?"
   → 단기/장기 분석, 목표가, 투자 추천

3️⃣ **도움말**
   예: "뭘 할 수 있어?", "도움말"
   → 이 메시지 출력

준비가 된 카트리지:
• Bio-Cartridge (v1.0-Alpha) ✅
• Investment-Cartridge (v1.0-Alpha) ✅

박사님, 뭘 도와드릴까요? 😊
"""


# ============================================================================
# 7. SHawn-Bot 메인 클래스
# ============================================================================

class SHawnBot:
    """
    숀봇: 디지털 다빈치의 손
    
    역할:
      • 카트리지 로드 & 관리
      • 박사님 요청 이해
      • 적절한 카트리지 선택 & 실행
      • 결과 정리 & 제시
    """
    
    def __init__(self):
        """초기화"""
        self.name = "SHawn-Bot"
        self.version = "1.0-Alpha"
        self.cartridge_manager = CartridgeManager()
        self.request_analyzer = RequestAnalyzer()
        self.result_formatter = ResultFormatter()
        
        print("✅ SHawn-Bot 초기화 완료")
        print(f"   version: {self.version}")
        print(f"   cartridges: {self.cartridge_manager.list_cartridges()}")
    
    def process_request(self, user_input: str) -> str:
        """
        사용자 요청 처리
        
        Args:
            user_input: 사용자 입력
            
        Returns:
            str: 응답 메시지
        """
        print(f"\n📨 요청 수신: {user_input}")
        
        # 1. 요청 분석
        request = self.request_analyzer.analyze(user_input)
        print(f"🔍 분석 완료: {request.request_type.value}")
        print(f"🎯 카트리지 선택: {request.cartridge.value}")
        
        # 2. 도움말 요청 처리
        if request.request_type == RequestType.HELP:
            return self.result_formatter.format_help()
        
        # 3. 알 수 없는 요청 처리
        if request.request_type == RequestType.UNKNOWN or request.cartridge == CartridgeType.UNKNOWN:
            return """
❓ 죄송하지만, 요청을 이해하지 못했습니다.

제가 할 수 있는 일:
• 세포 분석 (이미지 업로드)
• 주식 분석 (종목명 입력)

더 자세한 정보는 "도움말"을 입력해주세요.
"""
        
        # 4. 카트리지 실행
        print(f"⚙️  카트리지 실행 중...")
        result = self.cartridge_manager.execute_cartridge(
            request.cartridge,
            **request.parameters
        )
        print(f"✅ 실행 완료 ({result.execution_time_ms:.1f}ms)")
        
        # 5. 결과 포맷팅
        if result.status == "error":
            return f"❌ 오류: {result.error_message}"
        
        if request.cartridge == CartridgeType.BIO:
            formatted = self.result_formatter.format_bio_result(result.data)
        elif request.cartridge == CartridgeType.INVESTMENT:
            formatted = self.result_formatter.format_investment_result(result.data)
        else:
            formatted = str(result.data)
        
        return formatted
    
    def get_status(self) -> str:
        """봇 상태 반환"""
        return f"""
🤖 **SHawn-Bot 상태**

• 이름: {self.name}
• 버전: {self.version}
• 상태: ✅ 정상 작동 중
• 카트리지: {', '.join(self.cartridge_manager.list_cartridges())}
• 준비: 100% 완료

박사님, 준비됐습니다! 🚀
"""


# ============================================================================
# 8. 사용 예시
# ============================================================================

if __name__ == "__main__":
    # SHawn-Bot 초기화
    bot = SHawnBot()
    
    print("\n" + "="*60)
    print("🤖 SHawn-Bot 테스트")
    print("="*60)
    
    # 테스트 요청들
    test_requests = [
        "도움말",
        "TSLA 분석해줘",
        "삼성전자 주식은?",
        "이 세포 사진 분석해줄래?",
        "안녕하세요"
    ]
    
    for request in test_requests:
        print(f"\n📨 사용자: {request}")
        print("-" * 60)
        response = bot.process_request(request)
        print(response)
        print("-" * 60)
    
    print("\n" + "="*60)
    print(bot.get_status())
    print("="*60)
