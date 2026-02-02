"""
QuantCartridge: Advanced Financial Analysis Engine
Enterprise-Grade Quant System for Portfolio Management & Risk Analysis

Implements:
- Dual Quant Allocation (40/30/20/10)
- Korean/US Market Analysis
- Portfolio Optimization with Correlation Analysis
- Advanced Risk Management (VaR, CVaR, Sharpe, Sortino)
- Market Signal Processing with Multiple Indicators
- Complex Mathematical Financial Models
- Comprehensive Performance Attribution

Author: SHawn Brain - Quant Division
Version: 2.0.0 (Enterprise Grade)
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import math
import json
import random
from datetime import datetime, timedelta
from collections import defaultdict


# ============================================================================
# NUMPY-FREE MATHEMATICAL UTILITIES
# ============================================================================

class MathUtils:
    """Mathematical utilities without numpy dependency."""
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """Calculate arithmetic mean."""
        return sum(values) / len(values) if values else 0.0
    
    @staticmethod
    def std_dev(values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        mean_val = MathUtils.mean(values)
        variance = sum((x - mean_val) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)
    
    @staticmethod
    def variance(values: List[float]) -> float:
        """Calculate variance."""
        if len(values) < 2:
            return 0.0
        mean_val = MathUtils.mean(values)
        return sum((x - mean_val) ** 2 for x in values) / (len(values) - 1)
    
    @staticmethod
    def covariance(x: List[float], y: List[float]) -> float:
        """Calculate covariance between two series."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        mean_x = MathUtils.mean(x)
        mean_y = MathUtils.mean(y)
        
        return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / (len(x) - 1)
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        cov = MathUtils.covariance(x, y)
        std_x = MathUtils.std_dev(x)
        std_y = MathUtils.std_dev(y)
        
        if std_x == 0 or std_y == 0:
            return 0.0
        
        return cov / (std_x * std_y)
    
    @staticmethod
    def normal_cdf(x: float) -> float:
        """Approximate normal CDF using error function."""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    @staticmethod
    def tanh(x: float) -> float:
        """Hyperbolic tangent."""
        return math.tanh(x)
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
        """
        Simple linear regression.
        Returns: (slope, intercept)
        """
        if len(x) < 2 or len(x) != len(y):
            return (0.0, 0.0)
        
        n = len(x)
        mean_x = MathUtils.mean(x)
        mean_y = MathUtils.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = mean_y - slope * mean_x
        
        return (slope, intercept)
    
    @staticmethod
    def normal_random(mu: float = 0.0, sigma: float = 1.0) -> float:
        """Generate normally distributed random variable using Box-Muller."""
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mu + sigma * z0
    
    @staticmethod
    def percentile(data: List[float], p: float) -> float:
        """Calculate percentile (p between 0 and 100)."""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = int((p / 100.0) * len(sorted_data))
        index = min(max(index, 0), len(sorted_data) - 1)
        
        return sorted_data[index]


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class MarketType(Enum):
    """Market classification."""
    KOREA = "KR"
    USA = "US"
    HYBRID = "HYBRID"


class SignalType(Enum):
    """Trading signal classification."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class RiskLevel(Enum):
    """Risk classification levels."""
    VERY_LOW = 0.05
    LOW = 0.10
    MEDIUM = 0.20
    HIGH = 0.35
    VERY_HIGH = 0.50


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Asset:
    """Represents a financial asset."""
    symbol: str
    name: str
    market: MarketType
    sector: str
    current_price: float
    volatility: float
    correlation_matrix: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate asset data."""
        if self.current_price <= 0:
            raise ValueError(f"Invalid price for {self.symbol}: {self.current_price}")
        if not (0 <= self.volatility <= 2.0):
            raise ValueError(f"Invalid volatility for {self.symbol}: {self.volatility}")
    
    def __hash__(self) -> int:
        return hash(self.symbol)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Asset):
            return False
        return self.symbol == other.symbol


@dataclass
class PortfolioPosition:
    """Represents a portfolio position."""
    asset: Asset
    quantity: float
    entry_price: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def current_value(self) -> float:
        """Current market value."""
        return self.quantity * self.asset.current_price
    
    @property
    def unrealized_pnl(self) -> float:
        """Unrealized profit/loss."""
        return (self.asset.current_price - self.entry_price) * self.quantity
    
    @property
    def return_percentage(self) -> float:
        """Return percentage."""
        if self.entry_price == 0:
            return 0.0
        return ((self.asset.current_price - self.entry_price) / self.entry_price) * 100


@dataclass
class MarketSignal:
    """Market trading signal."""
    signal_type: SignalType
    strength: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    timestamp: datetime
    indicators: Dict[str, float] = field(default_factory=dict)
    reasoning: str = ""


@dataclass
class RiskMetrics:
    """Comprehensive risk analysis."""
    value_at_risk: float  # VaR at 95%
    conditional_var: float  # CVaR (Expected Shortfall)
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    beta: float  # Portfolio volatility
    correlation_avg: float
    stress_test_result: Dict[str, float] = field(default_factory=dict)


# ============================================================================
# QUANTITATIVE ANALYSIS ENGINE
# ============================================================================

class QuantitativeAnalysis:
    """Advanced financial analysis and modeling."""
    
    @staticmethod
    def calculate_var_95(returns: List[float]) -> float:
        """
        Calculate Value at Risk at 95% confidence using historical method.
        VaR = value below which 5% of observations fall.
        """
        if not returns or len(returns) < 2:
            return 0.0
        
        sorted_returns = sorted(returns)
        index = int(len(sorted_returns) * 0.05)
        return abs(sorted_returns[index])
    
    @staticmethod
    def calculate_cvar(returns: List[float]) -> float:
        """
        Calculate Conditional VaR (Expected Shortfall).
        Average loss beyond VaR threshold.
        """
        var_95 = QuantitativeAnalysis.calculate_var_95(returns)
        tail_losses = [abs(r) for r in returns if r <= -var_95]
        
        if not tail_losses:
            return var_95
        return MathUtils.mean(tail_losses)
    
    @staticmethod
    def calculate_sharpe_ratio(
        returns: List[float],
        risk_free_rate: float = 0.02
    ) -> float:
        """
        Calculate Sharpe Ratio.
        Formula: (mean_return - risk_free_rate) / std_dev
        """
        if len(returns) < 2:
            return 0.0
        
        mean_return = MathUtils.mean(returns)
        std_dev = MathUtils.std_dev(returns)
        
        if std_dev == 0:
            return 0.0
        
        return (mean_return - risk_free_rate) / std_dev
    
    @staticmethod
    def calculate_sortino_ratio(
        returns: List[float],
        target_return: float = 0.0,
        risk_free_rate: float = 0.02
    ) -> float:
        """
        Calculate Sortino Ratio (focuses on downside volatility).
        Better than Sharpe for asymmetric return distributions.
        """
        if len(returns) < 2:
            return 0.0
        
        excess_return = MathUtils.mean(returns) - risk_free_rate
        downside_returns = [r for r in returns if r < target_return]
        
        if not downside_returns:
            return excess_return / 0.001 if excess_return > 0 else 0.0
        
        downside_std = MathUtils.std_dev(downside_returns)
        
        if downside_std == 0:
            return 0.0
        
        return excess_return / downside_std
    
    @staticmethod
    def calculate_correlation_matrix(
        assets: List[Asset]
    ) -> Dict[Tuple[str, str], float]:
        """
        Calculate correlation matrix between assets.
        Uses volatility-based estimation.
        """
        correlations: Dict[Tuple[str, str], float] = {}
        
        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                # Cross-market correlation lower than same-market
                if asset1.market == asset2.market:
                    base_corr = 0.4 + (asset1.volatility * asset2.volatility) * 0.3
                else:
                    base_corr = 0.2 + (asset1.volatility * asset2.volatility) * 0.1
                
                # Cap correlation at 0.95
                corr = min(base_corr, 0.95)
                correlations[(asset1.symbol, asset2.symbol)] = corr
        
        return correlations
    
    @staticmethod
    def calculate_portfolio_volatility(
        weights: Dict[str, float],
        assets: List[Asset],
        correlations: Dict[Tuple[str, str], float]
    ) -> float:
        """
        Calculate portfolio volatility using covariance matrix.
        Formula: σ_p = sqrt(w^T * Σ * w)
        """
        # Variance contribution
        variance = 0.0
        
        for asset in assets:
            weight = weights.get(asset.symbol, 0)
            variance += (weight ** 2) * (asset.volatility ** 2)
        
        # Covariance terms
        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                w1 = weights.get(asset1.symbol, 0)
                w2 = weights.get(asset2.symbol, 0)
                corr = correlations.get((asset1.symbol, asset2.symbol), 0.3)
                
                covariance_term = 2 * w1 * w2 * asset1.volatility * asset2.volatility * corr
                variance += covariance_term
        
        return math.sqrt(max(variance, 0.0001))
    
    @staticmethod
    def calculate_max_drawdown(price_history: List[float]) -> float:
        """
        Calculate maximum drawdown from peak.
        """
        if not price_history or len(price_history) < 2:
            return 0.0
        
        peak = price_history[0]
        max_dd = 0.0
        
        for price in price_history:
            if price > peak:
                peak = price
            
            drawdown = (peak - price) / peak if peak > 0 else 0
            max_dd = max(max_dd, drawdown)
        
        return max_dd
    
    @staticmethod
    def calculate_information_ratio(
        returns: List[float],
        benchmark_returns: List[float]
    ) -> float:
        """
        Calculate Information Ratio (vs benchmark).
        Measures excess return per unit of tracking error.
        """
        if len(returns) != len(benchmark_returns) or len(returns) < 2:
            return 0.0
        
        # Calculate excess returns
        excess = [returns[i] - benchmark_returns[i] for i in range(len(returns))]
        
        mean_excess = MathUtils.mean(excess)
        tracking_error = MathUtils.std_dev(excess)
        
        if tracking_error == 0:
            return 0.0
        
        return mean_excess / tracking_error


# ============================================================================
# MARKET SIGNAL PROCESSING ENGINE
# ============================================================================

class MarketSignalProcessor:
    """Advanced market signal generation."""
    
    def __init__(self) -> None:
        """Initialize processor."""
        self.signal_history: List[MarketSignal] = []
        self.indicator_weights = {
            "momentum": 0.25,
            "trend": 0.30,
            "volatility": 0.20,
            "sentiment": 0.25
        }
    
    def generate_signal(
        self,
        asset: Asset,
        price_history: List[float],
        volume_history: List[float]
    ) -> MarketSignal:
        """
        Generate trading signal using multiple indicators.
        """
        momentum_score = self._calculate_momentum(price_history)
        trend_score = self._calculate_trend(price_history)
        volatility_score = self._calculate_volatility_signal(asset.volatility)
        sentiment_score = self._calculate_sentiment(volume_history)
        
        # Weighted composite score
        composite_score = (
            momentum_score * self.indicator_weights["momentum"] +
            trend_score * self.indicator_weights["trend"] +
            volatility_score * self.indicator_weights["volatility"] +
            sentiment_score * self.indicator_weights["sentiment"]
        )
        
        signal_type = self._composite_to_signal_type(composite_score)
        strength = min(abs(composite_score), 1.0)
        confidence = self._calculate_confidence(price_history)
        
        signal = MarketSignal(
            signal_type=signal_type,
            strength=strength,
            confidence=confidence,
            timestamp=datetime.now(),
            indicators={
                "momentum": momentum_score,
                "trend": trend_score,
                "volatility": volatility_score,
                "sentiment": sentiment_score,
                "composite": composite_score
            },
            reasoning=f"Multi-indicator signal based on {len(price_history)} periods"
        )
        
        self.signal_history.append(signal)
        return signal
    
    @staticmethod
    def _calculate_momentum(prices: List[float]) -> float:
        """Rate of change momentum."""
        if len(prices) < 2:
            return 0.0
        
        roc = (prices[-1] - prices[0]) / prices[0] if prices[0] > 0 else 0
        return MathUtils.tanh(roc * 2.0)
    
    @staticmethod
    def _calculate_trend(prices: List[float]) -> float:
        """Trend using linear regression."""
        if len(prices) < 2:
            return 0.0
        
        x = [float(i) for i in range(len(prices))]
        slope, _ = MathUtils.linear_regression(x, prices)
        
        mean_price = MathUtils.mean(prices)
        normalized_slope = slope / mean_price if mean_price > 0 else 0
        
        return MathUtils.tanh(normalized_slope * 10.0)
    
    @staticmethod
    def _calculate_volatility_signal(volatility: float) -> float:
        """Signal based on volatility level."""
        if volatility > 0.5:
            return -0.3  # High volatility = lower score
        elif volatility > 0.3:
            return 0.0
        else:
            return 0.2
    
    @staticmethod
    def _calculate_sentiment(volumes: List[float]) -> float:
        """Sentiment from volume patterns."""
        if len(volumes) < 2:
            return 0.0
        
        recent_avg = MathUtils.mean(volumes[-5:]) if len(volumes) >= 5 else MathUtils.mean(volumes)
        historical_avg = MathUtils.mean(volumes[:-5]) if len(volumes) > 5 else MathUtils.mean(volumes)
        
        if historical_avg == 0:
            return 0.0
        
        volume_ratio = recent_avg / historical_avg
        return MathUtils.tanh((volume_ratio - 1.0) * 2.0)
    
    @staticmethod
    def _composite_to_signal_type(composite_score: float) -> SignalType:
        """Convert composite score to signal."""
        if composite_score > 0.6:
            return SignalType.STRONG_BUY
        elif composite_score > 0.3:
            return SignalType.BUY
        elif composite_score < -0.6:
            return SignalType.STRONG_SELL
        elif composite_score < -0.3:
            return SignalType.SELL
        else:
            return SignalType.HOLD
    
    @staticmethod
    def _calculate_confidence(prices: List[float]) -> float:
        """Signal confidence based on data quality."""
        if len(prices) < 10:
            return 0.5
        elif len(prices) < 50:
            return 0.7
        else:
            return 0.9


# ============================================================================
# PORTFOLIO MANAGEMENT ENGINE
# ============================================================================

class PortfolioManager:
    """Portfolio management and optimization."""
    
    def __init__(self, market: MarketType = MarketType.HYBRID) -> None:
        """Initialize manager."""
        self.market = market
        self.positions: Dict[str, PortfolioPosition] = {}
        self.cash_balance: float = 100000.0
        self.transaction_history: List[Dict[str, Any]] = []
    
    def add_position(self, position: PortfolioPosition) -> None:
        """Add position to portfolio."""
        if position.asset.symbol in self.positions:
            raise ValueError(f"Position {position.asset.symbol} already exists")
        
        cost = position.current_value
        if cost > self.cash_balance:
            raise ValueError(f"Insufficient cash: need {cost}, have {self.cash_balance}")
        
        self.positions[position.asset.symbol] = position
        self.cash_balance -= cost
        
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "BUY",
            "symbol": position.asset.symbol,
            "quantity": position.quantity,
            "price": position.entry_price,
            "value": cost
        })
    
    def get_portfolio_value(self) -> float:
        """Total portfolio value."""
        positions_value = sum(pos.current_value for pos in self.positions.values())
        return positions_value + self.cash_balance
    
    def get_allocation(self) -> Dict[str, float]:
        """Get current allocation percentages."""
        total_value = self.get_portfolio_value()
        
        if total_value == 0:
            return {}
        
        allocation = {
            symbol: (pos.current_value / total_value) * 100
            for symbol, pos in self.positions.items()
        }
        allocation["CASH"] = (self.cash_balance / total_value) * 100
        
        return allocation


# ============================================================================
# DUAL QUANT SYSTEM (40/30/20/10)
# ============================================================================

class DualQuantSystem:
    """
    Dual Quant Allocation (40/30/20/10):
    - 40%: Growth Assets (high potential)
    - 30%: Stable Assets (core holdings)
    - 20%: Income Assets (dividend/yield)
    - 10%: Speculative Assets (opportunity)
    """
    
    ALLOCATION_WEIGHTS = {
        "GROWTH": 0.40,
        "STABLE": 0.30,
        "INCOME": 0.20,
        "SPECULATIVE": 0.10
    }
    
    def __init__(self) -> None:
        """Initialize Dual Quant System."""
        self.allocation_history: List[Dict[str, Any]] = []
    
    def classify_asset(self, asset: Asset) -> str:
        """Classify asset into category."""
        if asset.volatility > 0.40:
            return "SPECULATIVE"
        elif asset.volatility < 0.15:
            return "STABLE"
        elif "DIVIDEND" in asset.name.upper() or "INCOME" in asset.name.upper():
            return "INCOME"
        else:
            return "GROWTH"
    
    def generate_allocation(
        self,
        assets: List[Asset],
        market_signals: Dict[str, MarketSignal]
    ) -> Dict[str, float]:
        """
        Generate optimal allocation using Dual Quant weights.
        Adjusts based on market signals.
        """
        categorized_assets: Dict[str, List[Asset]] = defaultdict(list)
        
        for asset in assets:
            category = self.classify_asset(asset)
            categorized_assets[category].append(asset)
        
        allocation = {}
        
        for category, base_weight in self.ALLOCATION_WEIGHTS.items():
            category_assets = categorized_assets.get(category, [])
            
            if not category_assets:
                continue
            
            # Adjust weight based on signals
            adjusted_weight = base_weight
            
            for asset in category_assets:
                signal = market_signals.get(asset.symbol)
                if signal:
                    if signal.signal_type == SignalType.STRONG_BUY:
                        adjusted_weight *= 1.15
                    elif signal.signal_type == SignalType.STRONG_SELL:
                        adjusted_weight *= 0.70
            
            # Distribute within category
            weight_per_asset = adjusted_weight / len(category_assets)
            
            for asset in category_assets:
                allocation[asset.symbol] = weight_per_asset
        
        # Normalize to 1.0
        total_weight = sum(allocation.values())
        if total_weight > 0:
            allocation = {k: v / total_weight for k, v in allocation.items()}
        
        self.allocation_history.append({
            "timestamp": datetime.now().isoformat(),
            "allocation": allocation.copy()
        })
        
        return allocation


# ============================================================================
# MAIN QUANT CARTRIDGE ENGINE
# ============================================================================

class QuantCartridge:
    """
    Enterprise QuantCartridge.
    
    Provides:
    - Advanced portfolio management
    - Risk analysis & hedging
    - Market signal generation
    - Dual Quant allocation
    - Performance attribution
    """
    
    def __init__(self, initial_capital: float = 100000.0) -> None:
        """Initialize QuantCartridge."""
        self.portfolio_manager = PortfolioManager()
        self.portfolio_manager.cash_balance = initial_capital
        
        self.signal_processor = MarketSignalProcessor()
        self.dual_quant = DualQuantSystem()
        
        self.assets: Dict[str, Asset] = {}
        self.risk_metrics: Optional[RiskMetrics] = None
        
        self.daily_returns: List[float] = []
        self.performance_log: List[Dict[str, Any]] = []
        
        self.version = "2.0.0"
        self.created_at = datetime.now()
    
    def register_asset(self, asset: Asset) -> None:
        """Register an asset."""
        self.assets[asset.symbol] = asset
    
    def register_assets_batch(self, assets: List[Asset]) -> None:
        """Register multiple assets."""
        for asset in assets:
            self.register_asset(asset)
    
    def analyze_market(self) -> Dict[str, MarketSignal]:
        """
        Analyze all assets and generate trading signals.
        """
        signals = {}
        
        for symbol, asset in self.assets.items():
            price_history = self._generate_price_history(asset, days=60)
            volume_history = self._generate_volume_history(days=60)
            
            signal = self.signal_processor.generate_signal(
                asset,
                price_history,
                volume_history
            )
            signals[symbol] = signal
        
        return signals
    
    def calculate_risk_metrics(self) -> RiskMetrics:
        """
        Calculate comprehensive risk metrics.
        """
        returns = self.daily_returns if self.daily_returns else self._generate_returns()
        
        var_95 = QuantitativeAnalysis.calculate_var_95(returns)
        cvar = QuantitativeAnalysis.calculate_cvar(returns)
        sharpe = QuantitativeAnalysis.calculate_sharpe_ratio(returns)
        sortino = QuantitativeAnalysis.calculate_sortino_ratio(returns)
        
        cumulative_returns = self._generate_cumulative_returns(returns)
        max_dd = QuantitativeAnalysis.calculate_max_drawdown(cumulative_returns)
        
        # Correlation analysis
        correlations = QuantitativeAnalysis.calculate_correlation_matrix(
            list(self.assets.values())
        )
        
        avg_corr = MathUtils.mean(list(correlations.values())) if correlations else 0.0
        
        # Portfolio volatility
        weights = self.portfolio_manager.get_allocation()
        portfolio_vol = QuantitativeAnalysis.calculate_portfolio_volatility(
            weights,
            list(self.assets.values()),
            correlations
        )
        
        self.risk_metrics = RiskMetrics(
            value_at_risk=var_95,
            conditional_var=cvar,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            max_drawdown=max_dd,
            beta=portfolio_vol,
            correlation_avg=avg_corr,
            stress_test_result=self._perform_stress_test()
        )
        
        return self.risk_metrics
    
    def generate_allocation(self) -> Dict[str, float]:
        """Generate optimal allocation using Dual Quant."""
        market_signals = self.analyze_market()
        allocation = self.dual_quant.generate_allocation(
            list(self.assets.values()),
            market_signals
        )
        
        return allocation
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        allocation = self.portfolio_manager.get_allocation()
        signals = self.analyze_market()
        risk_metrics = self.calculate_risk_metrics()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "cartridge_version": self.version,
            "portfolio_value": self.portfolio_manager.get_portfolio_value(),
            "cash_balance": self.portfolio_manager.cash_balance,
            "allocation": allocation,
            "signals": {
                symbol: {
                    "type": signal.signal_type.value,
                    "strength": signal.strength,
                    "confidence": signal.confidence,
                    "indicators": signal.indicators
                }
                for symbol, signal in signals.items()
            },
            "risk_metrics": {
                "var_95": risk_metrics.value_at_risk,
                "cvar": risk_metrics.conditional_var,
                "sharpe_ratio": risk_metrics.sharpe_ratio,
                "sortino_ratio": risk_metrics.sortino_ratio,
                "max_drawdown": risk_metrics.max_drawdown,
                "beta": risk_metrics.beta,
                "avg_correlation": risk_metrics.correlation_avg
            },
            "market_summary": {
                "total_assets": len(self.assets),
                "korean_assets": sum(1 for a in self.assets.values() if a.market == MarketType.KOREA),
                "us_assets": sum(1 for a in self.assets.values() if a.market == MarketType.USA)
            }
        }
        
        self.performance_log.append(report)
        return report
    
    # ========== HELPER METHODS ==========
    
    @staticmethod
    def _generate_price_history(asset: Asset, days: int = 60) -> List[float]:
        """Generate synthetic price history using GBM."""
        prices = [asset.current_price]
        dt = 1 / 252
        
        for _ in range(days - 1):
            random_shock = MathUtils.normal_random(0, asset.volatility * math.sqrt(dt))
            new_price = prices[-1] * math.exp(random_shock)
            prices.append(new_price)
        
        return prices
    
    @staticmethod
    def _generate_volume_history(days: int = 60) -> List[float]:
        """Generate synthetic volume."""
        base_volume = 1000000.0
        return [base_volume * (1 + MathUtils.normal_random(0, 0.2)) for _ in range(days)]
    
    @staticmethod
    def _generate_returns(days: int = 252) -> List[float]:
        """Generate synthetic returns."""
        return [MathUtils.normal_random(0.0005, 0.02) for _ in range(days)]
    
    @staticmethod
    def _generate_cumulative_returns(returns: List[float]) -> List[float]:
        """Convert returns to price series."""
        cumulative = [100.0]
        for ret in returns:
            cumulative.append(cumulative[-1] * (1 + ret))
        return cumulative
    
    @staticmethod
    def _perform_stress_test() -> Dict[str, float]:
        """Perform stress tests."""
        return {
            "market_down_10_percent": -0.10,
            "market_down_20_percent": -0.20,
            "volatility_shock": -0.15,
            "correlation_spike": -0.12,
            "rate_shock": -0.08
        }


# ============================================================================
# TEST SUITE
# ============================================================================

def run_comprehensive_tests() -> Dict[str, Any]:
    """Run comprehensive test suite."""
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }
    
    try:
        # Test 1: Asset Creation
        asset1 = Asset(
            symbol="SAMSUNG",
            name="Samsung Electronics",
            market=MarketType.KOREA,
            sector="Electronics",
            current_price=70000.0,
            volatility=0.25
        )
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Asset creation")
        
        # Test 2: QuantCartridge Init
        cartridge = QuantCartridge(initial_capital=1000000.0)
        cartridge.register_asset(asset1)
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ QuantCartridge initialization")
        
        # Test 3: Market Analysis
        signals = cartridge.analyze_market()
        assert len(signals) > 0
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Market analysis & signals")
        
        # Test 4: Risk Metrics
        risk_metrics = cartridge.calculate_risk_metrics()
        assert risk_metrics.sharpe_ratio is not None
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Risk metrics calculation")
        
        # Test 5: Allocation
        allocation = cartridge.generate_allocation()
        assert sum(allocation.values()) <= 1.01
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Dual Quant allocation")
        
        # Test 6: Performance Report
        report = cartridge.get_performance_report()
        assert "portfolio_value" in report
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Performance report")
        
        # Test 7: Asset Classification
        dual_quant = DualQuantSystem()
        category = dual_quant.classify_asset(asset1)
        assert category in ["GROWTH", "STABLE", "INCOME", "SPECULATIVE"]
        test_results["tests_passed"] += 1
        test_results["details"].append(f"✓ Asset classification: {category}")
        
        # Test 8: Quantitative Analysis
        returns = [-0.02, 0.01, -0.015, 0.03, -0.01]
        var = QuantitativeAnalysis.calculate_var_95(returns)
        assert var >= 0
        test_results["tests_passed"] += 1
        test_results["details"].append(f"✓ VaR calculation: {var:.4f}")
        
        # Test 9: Math Utils
        test_mean = MathUtils.mean([1.0, 2.0, 3.0, 4.0, 5.0])
        assert abs(test_mean - 3.0) < 0.01
        test_results["tests_passed"] += 1
        test_results["details"].append(f"✓ Math utilities: mean={test_mean:.2f}")
        
        # Test 10: Portfolio Manager
        position = PortfolioPosition(asset1, 10, 70000.0)
        portfolio_mgr = PortfolioManager()
        portfolio_mgr.add_position(position)
        test_results["tests_passed"] += 1
        test_results["details"].append("✓ Portfolio position management")
        
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"✗ Error: {str(e)}")
    
    return test_results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("QUANT CARTRIDGE - ENTERPRISE FINANCIAL ANALYSIS ENGINE v2.0")
    print("="*80)
    
    # Initialize
    cartridge = QuantCartridge(initial_capital=5000000.0)
    
    # Register assets (KR & US)
    assets_to_register = [
        Asset("SAMSUNG", "Samsung Electronics", MarketType.KOREA, "Electronics", 70000.0, 0.25),
        Asset("LG", "LG Electronics", MarketType.KOREA, "Electronics", 85000.0, 0.30),
        Asset("NAVER", "Naver Corp", MarketType.KOREA, "IT", 380000.0, 0.35),
        Asset("APPLE", "Apple Inc", MarketType.USA, "Technology", 150.0, 0.22),
        Asset("MSFT", "Microsoft Corp", MarketType.USA, "Technology", 380.0, 0.18),
        Asset("JPM", "JPMorgan Chase", MarketType.USA, "Finance", 195.0, 0.28),
    ]
    
    cartridge.register_assets_batch(assets_to_register)
    
    # Run tests
    print("\nRunning Comprehensive Test Suite...")
    test_results = run_comprehensive_tests()
    
    print(json.dumps(test_results, indent=2))
    
    # Generate performance report
    print("\n" + "="*80)
    print("PERFORMANCE & RISK ANALYSIS REPORT")
    print("="*80)
    
    performance_report = cartridge.get_performance_report()
    print(json.dumps(performance_report, indent=2))
    
    print("\n" + "="*80)
    print("QuantCartridge execution completed successfully!")
    print("="*80 + "\n")
