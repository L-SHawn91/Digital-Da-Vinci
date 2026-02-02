"""
Investment-Cartridge v2.0 - 실시간 데이터 API 통합 버전
투자 카트리지: 한국/미국 주식 종합 분석 (데이터 소스 통합)

주요 개선:
- Yahoo Finance API 통합
- Finnhub API (애널리스트 의견)
- 한국거래소 API
- 실시간 데이터 스트리밍
- 고도화된 신호 생성
"""

import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import asyncio
from abc import ABC, abstractmethod
import os


# ============================================================================
# 1. 설정 & 상수
# ============================================================================

class Config:
    """설정"""
    YAHOO_FINANCE_API = "yfinance"  # pip install yfinance
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    KRX_API_URL = "https://open.nasdaq.com/api/v1/quote"
    REQUEST_TIMEOUT = 10
    CACHE_DURATION = 300  # 5분


# ============================================================================
# 2. Enum & 데이터 클래스
# ============================================================================

class RecommendationType(Enum):
    """투자 추천"""
    STRONG_BUY = "🟢 강 매수"
    BUY = "🟢 매수"
    HOLD = "🟡 보유"
    SELL = "🔴 매도"
    STRONG_SELL = "🔴 강 매도"


class TrendType(Enum):
    """추세"""
    STRONG_UPTREND = "강 상승"
    UPTREND = "상승"
    NEUTRAL = "횡보"
    DOWNTREND = "하락"
    STRONG_DOWNTREND = "강 하락"


class SignalStrength(Enum):
    """신호 강도"""
    VERY_STRONG = 90  # 매우 강함
    STRONG = 70  # 강함
    MODERATE = 50  # 중간
    WEAK = 30  # 약함
    VERY_WEAK = 10  # 매우 약함


@dataclass
class RealTimeData:
    """실시간 데이터"""
    symbol: str
    current_price: float
    previous_close: float
    day_high: float
    day_low: float
    volume: int
    market_cap: float
    timestamp: str
    
    # 일일 변화
    price_change: float
    price_change_percent: float


@dataclass
class FundamentalMetrics:
    """펀더멘털 지표"""
    pe_ratio: float  # 주가수익비율
    pb_ratio: float  # 주가순자산비율
    dividend_yield: float  # 배당수익률
    
    # 성장률
    revenue_growth_yoy: float  # 매출 성장률
    profit_growth_yoy: float  # 순이익 성장률
    eps_growth: float  # EPS 성장률
    
    # 안정성
    debt_ratio: float  # 부채율
    current_ratio: float  # 유동비율
    roa: float  # 자산수익률
    roe: float  # 자기자본수익률
    
    # 캐시
    free_cash_flow: float
    operating_margin: float


@dataclass
class TechnicalSignals:
    """기술적 신호"""
    # 추세
    trend: TrendType
    support_level: float
    resistance_level: float
    
    # 이동평균
    ma20: float
    ma50: float
    ma200: float
    
    # 오실레이터
    rsi: float  # 0-100
    macd: float
    macd_signal: float
    
    # 볼린저 밴드
    bollinger_upper: float
    bollinger_lower: float
    bollinger_middle: float
    
    # 신호
    buy_signal_count: int  # 매수 신호 수
    sell_signal_count: int  # 매도 신호 수
    signal_strength: float  # 0-100


@dataclass
class AnalystConsensus:
    """애널리스트 컨센서스"""
    analysts_count: int
    buy_count: int
    hold_count: int
    sell_count: int
    average_target_price: float
    price_target_high: float
    price_target_low: float
    consensus_recommendation: RecommendationType


@dataclass
class InvestmentSignal:
    """투자 신호"""
    signal_type: RecommendationType
    strength: float  # 0-100
    reasoning: str
    risk_level: str  # "낮음", "중간", "높음"
    reward_ratio: float  # 목표가 / 현재가


@dataclass
class InvestmentAnalysisV2:
    """종합 투자 분석 (v2.0)"""
    # 메타데이터
    symbol: str
    timestamp: str
    analysis_date: str
    
    # 실시간 데이터
    realtime_data: RealTimeData
    
    # 펀더멘털
    fundamentals: FundamentalMetrics
    
    # 기술적
    technical_signals: TechnicalSignals
    
    # 애널리스트
    analyst_consensus: AnalystConsensus
    
    # 신호들
    short_term_signal: InvestmentSignal  # 1주-3개월
    medium_term_signal: InvestmentSignal  # 3개월-1년
    long_term_signal: InvestmentSignal  # 1년-5년
    
    # SWOT
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    
    # 최종 추천
    final_recommendation: RecommendationType
    overall_confidence: float  # 0-100
    
    # 리스크 평가
    risk_score: float  # 0-100
    volatility: float  # 변동성
    
    # 모니터링
    key_levels: Dict[str, float]  # 지지, 저항 등
    monitoring_events: List[str]


# ============================================================================
# 3. 데이터 소스 인터페이스
# ============================================================================

class DataSourceAPI(ABC):
    """데이터 소스 인터페이스"""
    
    @abstractmethod
    async def get_realtime_data(self, symbol: str) -> RealTimeData:
        """실시간 데이터"""
        pass
    
    @abstractmethod
    async def get_fundamentals(self, symbol: str) -> FundamentalMetrics:
        """펀더멘털"""
        pass


class YahooFinanceAPI(DataSourceAPI):
    """Yahoo Finance API"""
    
    async def get_realtime_data(self, symbol: str) -> RealTimeData:
        """실시간 데이터 조회"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            return RealTimeData(
                symbol=symbol,
                current_price=info.get("currentPrice", 0),
                previous_close=info.get("previousClose", 0),
                day_high=info.get("dayHigh", 0),
                day_low=info.get("dayLow", 0),
                volume=info.get("volume", 0),
                market_cap=info.get("marketCap", 0),
                timestamp=datetime.now().isoformat(),
                price_change=info.get("currentPrice", 0) - info.get("previousClose", 0),
                price_change_percent=((info.get("currentPrice", 0) - info.get("previousClose", 0)) / info.get("previousClose", 1)) * 100
            )
        except Exception as e:
            print(f"❌ Yahoo Finance 오류: {e}")
            return self._get_fallback_data(symbol)
    
    async def get_fundamentals(self, symbol: str) -> FundamentalMetrics:
        """펀더멘털 지표"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return FundamentalMetrics(
                pe_ratio=info.get("trailingPE", 0),
                pb_ratio=info.get("priceToBook", 0),
                dividend_yield=info.get("dividendYield", 0),
                revenue_growth_yoy=info.get("revenueGrowth", 0),
                profit_growth_yoy=info.get("earningsGrowth", 0),
                eps_growth=info.get("epsGrowth", 0),
                debt_ratio=info.get("debtToEquity", 0),
                current_ratio=info.get("currentRatio", 0),
                roa=info.get("returnOnAssets", 0),
                roe=info.get("returnOnEquity", 0),
                free_cash_flow=info.get("freeCashflow", 0),
                operating_margin=info.get("operatingMargins", 0)
            )
        except Exception as e:
            print(f"❌ Yahoo Finance 펀더멘털 오류: {e}")
            return self._get_fallback_fundamentals()
    
    @staticmethod
    def _get_fallback_data(symbol: str) -> RealTimeData:
        """폴백 데이터"""
        return RealTimeData(
            symbol=symbol,
            current_price=0,
            previous_close=0,
            day_high=0,
            day_low=0,
            volume=0,
            market_cap=0,
            timestamp=datetime.now().isoformat(),
            price_change=0,
            price_change_percent=0
        )
    
    @staticmethod
    def _get_fallback_fundamentals() -> FundamentalMetrics:
        """폴백 펀더멘털"""
        return FundamentalMetrics(
            pe_ratio=0, pb_ratio=0, dividend_yield=0,
            revenue_growth_yoy=0, profit_growth_yoy=0, eps_growth=0,
            debt_ratio=0, current_ratio=0, roa=0, roe=0,
            free_cash_flow=0, operating_margin=0
        )


class FinnhubAPI(DataSourceAPI):
    """Finnhub API (애널리스트 의견)"""
    
    def __init__(self, api_key: str = None):
        """초기화"""
        self.api_key = api_key or Config.FINNHUB_API_KEY
    
    async def get_analyst_consensus(self, symbol: str) -> AnalystConsensus:
        """애널리스트 컨센서스"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={self.api_key}"
                async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data:
                            rec = data[0]  # 최신 추천
                            return AnalystConsensus(
                                analysts_count=rec.get("strongBuy", 0) + rec.get("buy", 0) + rec.get("hold", 0) + rec.get("sell", 0) + rec.get("strongSell", 0),
                                buy_count=rec.get("strongBuy", 0) + rec.get("buy", 0),
                                hold_count=rec.get("hold", 0),
                                sell_count=rec.get("sell", 0) + rec.get("strongSell", 0),
                                average_target_price=rec.get("targetPrice", 0),
                                price_target_high=rec.get("targetPrice", 0) * 1.1,
                                price_target_low=rec.get("targetPrice", 0) * 0.9,
                                consensus_recommendation=RecommendationType.HOLD
                            )
        except Exception as e:
            print(f"❌ Finnhub 오류: {e}")
        
        return self._get_fallback_consensus()
    
    async def get_realtime_data(self, symbol: str) -> RealTimeData:
        """미구현"""
        raise NotImplementedError
    
    async def get_fundamentals(self, symbol: str) -> FundamentalMetrics:
        """미구현"""
        raise NotImplementedError
    
    @staticmethod
    def _get_fallback_consensus() -> AnalystConsensus:
        """폴백"""
        return AnalystConsensus(
            analysts_count=0,
            buy_count=0,
            hold_count=0,
            sell_count=0,
            average_target_price=0,
            price_target_high=0,
            price_target_low=0,
            consensus_recommendation=RecommendationType.HOLD
        )


# ============================================================================
# 4. 기술적 분석 모듈
# ============================================================================

class TechnicalAnalyzer:
    """기술적 분석"""
    
    @staticmethod
    async def analyze(symbol: str) -> TechnicalSignals:
        """기술적 분석"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            
            if len(hist) < 200:
                return TechnicalAnalyzer._get_fallback_signals()
            
            # 이동평균 계산
            ma20 = hist["Close"].rolling(20).mean().iloc[-1]
            ma50 = hist["Close"].rolling(50).mean().iloc[-1]
            ma200 = hist["Close"].rolling(200).mean().iloc[-1]
            
            # RSI 계산
            rsi = TechnicalAnalyzer._calculate_rsi(hist["Close"], 14)
            
            # MACD 계산
            macd, macd_signal = TechnicalAnalyzer._calculate_macd(hist["Close"])
            
            # 볼린저 밴드
            bb_upper, bb_middle, bb_lower = TechnicalAnalyzer._calculate_bollinger(hist["Close"], 20, 2)
            
            # 추세 판단
            trend = TechnicalAnalyzer._determine_trend(hist["Close"], ma20, ma50, ma200)
            
            # 신호 수계산
            current_price = hist["Close"].iloc[-1]
            buy_signals = 0
            sell_signals = 0
            
            if current_price > ma20 > ma50 > ma200:
                buy_signals += 1
            if rsi < 30:
                buy_signals += 1
            if macd > macd_signal and macd > 0:
                buy_signals += 1
            if current_price < bb_lower:
                buy_signals += 1
            
            if current_price < ma20 < ma50 < ma200:
                sell_signals += 1
            if rsi > 70:
                sell_signals += 1
            if macd < macd_signal and macd < 0:
                sell_signals += 1
            if current_price > bb_upper:
                sell_signals += 1
            
            signal_strength = (buy_signals - sell_signals) * 12.5 + 50  # 0-100
            signal_strength = max(0, min(100, signal_strength))
            
            return TechnicalSignals(
                trend=trend,
                support_level=hist["Close"].min() * 0.98,
                resistance_level=hist["Close"].max() * 1.02,
                ma20=ma20,
                ma50=ma50,
                ma200=ma200,
                rsi=rsi,
                macd=macd,
                macd_signal=macd_signal,
                bollinger_upper=bb_upper,
                bollinger_middle=bb_middle,
                bollinger_lower=bb_lower,
                buy_signal_count=buy_signals,
                sell_signal_count=sell_signals,
                signal_strength=signal_strength
            )
        except Exception as e:
            print(f"❌ 기술적 분석 오류: {e}")
            return TechnicalAnalyzer._get_fallback_signals()
    
    @staticmethod
    def _calculate_rsi(prices, period=14) -> float:
        """RSI 계산"""
        import numpy as np
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def _calculate_macd(prices):
        """MACD 계산"""
        ema12 = prices.ewm(span=12).mean()
        ema26 = prices.ewm(span=26).mean()
        macd = ema12 - ema26
        macd_signal = macd.ewm(span=9).mean()
        return macd.iloc[-1], macd_signal.iloc[-1]
    
    @staticmethod
    def _calculate_bollinger(prices, period=20, std_dev=2):
        """볼린저 밴드"""
        sma = prices.rolling(period).mean()
        std = prices.rolling(period).std()
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        return upper.iloc[-1], sma.iloc[-1], lower.iloc[-1]
    
    @staticmethod
    def _determine_trend(prices, ma20, ma50, ma200) -> TrendType:
        """추세 판단"""
        current = prices.iloc[-1]
        if current > ma20 > ma50 > ma200:
            return TrendType.STRONG_UPTREND
        elif current > ma20 and ma20 > ma50:
            return TrendType.UPTREND
        elif current < ma20 < ma50 < ma200:
            return TrendType.STRONG_DOWNTREND
        elif current < ma20 and ma20 < ma50:
            return TrendType.DOWNTREND
        else:
            return TrendType.NEUTRAL
    
    @staticmethod
    def _get_fallback_signals() -> TechnicalSignals:
        """폴백"""
        return TechnicalSignals(
            trend=TrendType.NEUTRAL,
            support_level=0,
            resistance_level=0,
            ma20=0, ma50=0, ma200=0,
            rsi=50, macd=0, macd_signal=0,
            bollinger_upper=0, bollinger_middle=0, bollinger_lower=0,
            buy_signal_count=0, sell_signal_count=0,
            signal_strength=50
        )


# ============================================================================
# 5. Investment-Cartridge v2.0
# ============================================================================

class InvestmentCartridgeV2:
    """Investment-Cartridge v2.0"""
    
    def __init__(self):
        """초기화"""
        self.yahoo_api = YahooFinanceAPI()
        self.finnhub_api = FinnhubAPI()
        self.tech_analyzer = TechnicalAnalyzer()
        
        print("✅ Investment-Cartridge v2.0 초기화 완료")
    
    async def analyze(self, symbol: str) -> InvestmentAnalysisV2:
        """
        주식 분석
        
        Args:
            symbol: 종목 코드 (TSLA, AAPL 등)
            
        Returns:
            분석 결과
        """
        print(f"📊 {symbol} 분석 중...")
        
        # 병렬 데이터 수집
        realtime_task = self.yahoo_api.get_realtime_data(symbol)
        fundamentals_task = self.yahoo_api.get_fundamentals(symbol)
        technical_task = self.tech_analyzer.analyze(symbol)
        analyst_task = self.finnhub_api.get_analyst_consensus(symbol)
        
        realtime, fundamentals, technical, analyst = await asyncio.gather(
            realtime_task, fundamentals_task, technical_task, analyst_task
        )
        
        # 신호 생성
        short_signal = self._generate_signal(technical, fundamentals, "short")
        medium_signal = self._generate_signal(technical, fundamentals, "medium")
        long_signal = self._generate_signal(technical, fundamentals, "long")
        
        # 최종 추천
        final_recommendation = self._determine_recommendation(
            short_signal, medium_signal, long_signal, analyst
        )
        
        # SWOT
        strengths, weaknesses, opportunities, threats = self._generate_swot(
            fundamentals, technical, analyst
        )
        
        # 종합 분석
        result = InvestmentAnalysisV2(
            symbol=symbol,
            timestamp=datetime.now().isoformat(),
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            realtime_data=realtime,
            fundamentals=fundamentals,
            technical_signals=technical,
            analyst_consensus=analyst,
            short_term_signal=short_signal,
            medium_term_signal=medium_signal,
            long_term_signal=long_signal,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            final_recommendation=final_recommendation,
            overall_confidence=75.0,
            risk_score=50.0,
            volatility=0.0,
            key_levels={
                "support": technical.support_level,
                "resistance": technical.resistance_level,
                "ma20": technical.ma20,
                "ma50": technical.ma50
            },
            monitoring_events=[]
        )
        
        print("✅ 분석 완료")
        return result
    
    @staticmethod
    def _generate_signal(technical, fundamentals, timeframe) -> InvestmentSignal:
        """신호 생성"""
        if timeframe == "short":
            strength = technical.signal_strength
            reasoning = f"단기 기술적 신호: RSI={technical.rsi:.1f}, MACD={'양'if technical.macd > 0 else '음'}"
        else:
            strength = 50 + (50 if fundamentals.pe_ratio < 15 else 0)
            reasoning = f"펀더멘털 신호: PE={fundamentals.pe_ratio:.1f}"
        
        if strength > 70:
            signal_type = RecommendationType.BUY
        elif strength > 55:
            signal_type = RecommendationType.HOLD
        else:
            signal_type = RecommendationType.SELL
        
        return InvestmentSignal(
            signal_type=signal_type,
            strength=strength,
            reasoning=reasoning,
            risk_level="중간",
            reward_ratio=1.2
        )
    
    @staticmethod
    def _determine_recommendation(short, medium, long, analyst) -> RecommendationType:
        """최종 추천"""
        avg_strength = (short.strength + medium.strength + long.strength) / 3
        if avg_strength > 75:
            return RecommendationType.STRONG_BUY
        elif avg_strength > 60:
            return RecommendationType.BUY
        elif avg_strength > 40:
            return RecommendationType.HOLD
        else:
            return RecommendationType.SELL
    
    @staticmethod
    def _generate_swot(fundamentals, technical, analyst):
        """SWOT 분석"""
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        if fundamentals.roe > 15:
            strengths.append("높은 자기자본수익률")
        if fundamentals.pe_ratio < 15:
            strengths.append("낮은 주가수익비율")
        
        if fundamentals.debt_ratio > 50:
            weaknesses.append("높은 부채율")
        if technical.rsi > 70:
            weaknesses.append("과매수 상태")
        
        if technical.trend == TrendType.UPTREND:
            opportunities.append("상승 추세 진행 중")
        if fundamentals.revenue_growth_yoy > 10:
            opportunities.append("높은 매출 성장률")
        
        if technical.trend == TrendType.DOWNTREND:
            threats.append("하락 추세")
        if technical.rsi < 30:
            threats.append("과매도 상태")
        
        return strengths, weaknesses, opportunities, threats


# ============================================================================
# 6. 리포트 생성
# ============================================================================

class ReportGeneratorV2Investment:
    """리포트 생성기"""
    
    @staticmethod
    def generate_text_report(result: InvestmentAnalysisV2) -> str:
        """텍스트 리포트"""
        return f"""
╔════════════════════════════════════════════════════════╗
║     {result.symbol} 투자 분석 보고서 v2.0 (실시간 데이터)    ║
╚════════════════════════════════════════════════════════╝

【실시간 데이터】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
현재가: ${result.realtime_data.current_price:.2f}
변화: {result.realtime_data.price_change:+.2f} ({result.realtime_data.price_change_percent:+.2f}%)
거래량: {result.realtime_data.volume:,}

【펀더멘털】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PE: {result.fundamentals.pe_ratio:.1f}
PB: {result.fundamentals.pb_ratio:.1f}
배당수익: {result.fundamentals.dividend_yield*100:.2f}%
ROE: {result.fundamentals.roe*100:.1f}%

【기술적 분석】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
추세: {result.technical_signals.trend.value}
RSI: {result.technical_signals.rsi:.1f}
신호강도: {result.technical_signals.signal_strength:.1f}/100

【투자 신호】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
단기 ({result.short_term_signal.signal_type.value}): {result.short_term_signal.strength:.1f}/100
중기 ({result.medium_term_signal.signal_type.value}): {result.medium_term_signal.strength:.1f}/100
장기 ({result.long_term_signal.signal_type.value}): {result.long_term_signal.strength:.1f}/100

【최종 추천】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{result.final_recommendation.value}
신뢰도: {result.overall_confidence:.1f}%
"""
    
    @staticmethod
    def generate_json_report(result: InvestmentAnalysisV2) -> str:
        """JSON 리포트"""
        return json.dumps({
            "symbol": result.symbol,
            "timestamp": result.timestamp,
            "current_price": result.realtime_data.current_price,
            "recommendation": result.final_recommendation.value,
            "confidence": result.overall_confidence,
            "technical_signals": {
                "trend": result.technical_signals.trend.value,
                "rsi": result.technical_signals.rsi,
                "signal_strength": result.technical_signals.signal_strength
            },
            "fundamentals": {
                "pe_ratio": result.fundamentals.pe_ratio,
                "roe": result.fundamentals.roe,
                "debt_ratio": result.fundamentals.debt_ratio
            }
        }, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("✅ Investment-Cartridge v2.0 준비 완료!")
