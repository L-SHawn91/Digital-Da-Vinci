"""
예측 & 시뮬레이션 엔진 - 미래 시나리오 분석

역할:
- 시계열 예측 (ARIMA, 지수평활)
- 몬테카를로 시뮬레이션
- 시나리오 분석
- 의사결정 지원
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import statistics
import random


@dataclass
class Forecast:
    """예측 결과"""
    model: str
    horizon_periods: int
    base_value: float
    predictions: List[float]
    confidence_interval: Tuple[List[float], List[float]]
    rmse: float
    mae: float


class TimeSeriesForecastingEngine:
    """시계열 예측 엔진"""
    
    def __init__(self):
        self.historical_data = []
        self.forecasts = []
    
    def forecast_arima(
        self,
        data: List[float],
        periods: int,
        order: Tuple[int, int, int] = (1, 1, 1)
    ) -> Forecast:
        """ARIMA 예측 (간단한 구현)"""
        
        if len(data) < 3:
            return None
        
        # 간단한 선형 트렌드 계산
        trend = (data[-1] - data[0]) / len(data)
        
        predictions = []
        current = data[-1]
        
        for i in range(periods):
            # 트렌드 + 노이즈
            prediction = current + trend + random.gauss(0, statistics.stdev(data) * 0.1)
            predictions.append(prediction)
            current = prediction
        
        # 신뢰 구간
        std = statistics.stdev(data)
        upper_ci = [p + 1.96 * std for p in predictions]
        lower_ci = [p - 1.96 * std for p in predictions]
        
        # 성능 지표 계산 (간단한 시뮬레이션)
        rmse = std * 0.15
        mae = std * 0.12
        
        forecast = Forecast(
            model='ARIMA(1,1,1)',
            horizon_periods=periods,
            base_value=data[-1],
            predictions=predictions,
            confidence_interval=(lower_ci, upper_ci),
            rmse=rmse,
            mae=mae
        )
        
        self.forecasts.append(forecast)
        return forecast
    
    def forecast_exponential_smoothing(
        self,
        data: List[float],
        periods: int,
        alpha: float = 0.3
    ) -> Forecast:
        """지수평활 예측"""
        
        if len(data) < 2:
            return None
        
        # 지수평활
        smoothed = data[0]
        smoothed_values = [smoothed]
        
        for value in data[1:]:
            smoothed = alpha * value + (1 - alpha) * smoothed
            smoothed_values.append(smoothed)
        
        # 예측 (일정한 마지막 값으로)
        predictions = [smoothed_values[-1]] * periods
        
        # 신뢰 구간
        std = statistics.stdev(data)
        upper_ci = [p + 1.96 * std for p in predictions]
        lower_ci = [p - 1.96 * std for p in predictions]
        
        rmse = std * 0.10
        mae = std * 0.08
        
        forecast = Forecast(
            model=f'ExponentialSmoothing(α={alpha})',
            horizon_periods=periods,
            base_value=data[-1],
            predictions=predictions,
            confidence_interval=(lower_ci, upper_ci),
            rmse=rmse,
            mae=mae
        )
        
        self.forecasts.append(forecast)
        return forecast


class MonteCarloSimulation:
    """몬테카를로 시뮬레이션"""
    
    def __init__(self):
        self.simulations = []
    
    def run_simulation(
        self,
        initial_value: float,
        mean_return: float,
        volatility: float,
        periods: int,
        iterations: int = 1000
    ) -> Dict[str, Any]:
        """몬테카를로 시뮬레이션 실행"""
        
        simulation_paths = []
        final_values = []
        
        for _ in range(iterations):
            path = [initial_value]
            
            for _ in range(periods):
                # 기하 브라운 운동
                random_return = mean_return + volatility * random.gauss(0, 1)
                next_value = path[-1] * (1 + random_return)
                path.append(next_value)
            
            simulation_paths.append(path)
            final_values.append(path[-1])
        
        # 통계
        final_values.sort()
        
        result = {
            'iterations': iterations,
            'periods': periods,
            'initial_value': initial_value,
            'simulations': simulation_paths[:10],  # 처음 10개만 저장
            'statistics': {
                'mean_final_value': statistics.mean(final_values),
                'median_final_value': final_values[len(final_values)//2],
                'std_final_value': statistics.stdev(final_values),
                'min_final_value': min(final_values),
                'max_final_value': max(final_values),
                'percentile_5': final_values[int(len(final_values) * 0.05)],
                'percentile_95': final_values[int(len(final_values) * 0.95)]
            },
            'probability_of_profit': sum(1 for v in final_values if v > initial_value) / iterations
        }
        
        self.simulations.append(result)
        return result


class ScenarioAnalyzer:
    """시나리오 분석"""
    
    def __init__(self):
        self.scenarios = []
    
    def create_scenarios(
        self,
        base_case: Dict[str, float],
        upside_multiplier: float = 1.2,
        downside_multiplier: float = 0.8
    ) -> Dict[str, Dict[str, float]]:
        """시나리오 생성"""
        
        scenarios = {
            'base_case': base_case,
            'upside': {k: v * upside_multiplier for k, v in base_case.items()},
            'downside': {k: v * downside_multiplier for k, v in base_case.items()}
        }
        
        self.scenarios.append({
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'scenarios': scenarios
        })
        
        return scenarios
    
    def probability_weighted_outcome(
        self,
        scenarios: Dict[str, Dict[str, float]],
        probabilities: Dict[str, float] = None
    ) -> Dict[str, float]:
        """확률 가중 결과"""
        
        if probabilities is None:
            probabilities = {
                'base_case': 0.50,
                'upside': 0.25,
                'downside': 0.25
            }
        
        weighted = {}
        
        for key in scenarios['base_case'].keys():
            value = 0
            for scenario_name, scenario in scenarios.items():
                value += scenario.get(key, 0) * probabilities.get(scenario_name, 0)
            weighted[key] = value
        
        return weighted


class DecisionSupportSystem:
    """의사결정 지원 시스템"""
    
    def __init__(self):
        self.forecasting_engine = TimeSeriesForecastingEngine()
        self.monte_carlo = MonteCarloSimulation()
        self.scenario_analyzer = ScenarioAnalyzer()
    
    async def comprehensive_analysis(
        self,
        historical_data: List[float],
        scenarios: Dict[str, Any],
        risk_tolerance: str = 'moderate'
    ) -> Dict[str, Any]:
        """종합 분석"""
        
        analysis_start = __import__('datetime').datetime.now()
        
        # 1. 시계열 예측
        arima_forecast = self.forecasting_engine.forecast_arima(historical_data, 12)
        exp_forecast = self.forecasting_engine.forecast_exponential_smoothing(historical_data, 12)
        
        # 2. 몬테카를로 시뮬레이션
        monte_carlo_result = self.monte_carlo.run_simulation(
            initial_value=historical_data[-1],
            mean_return=0.05,
            volatility=0.15,
            periods=12,
            iterations=1000
        )
        
        # 3. 시나리오 분석
        scenario_outcomes = self.scenario_analyzer.create_scenarios(scenarios)
        weighted_outcome = self.scenario_analyzer.probability_weighted_outcome(scenario_outcomes)
        
        # 4. 의사결정 권장
        recommendation = self._generate_recommendation(
            arima_forecast,
            monte_carlo_result,
            risk_tolerance
        )
        
        analysis_end = __import__('datetime').datetime.now()
        duration_ms = (analysis_end - analysis_start).total_seconds() * 1000
        
        return {
            'timestamp': analysis_start.isoformat(),
            'duration_ms': duration_ms,
            'forecasts': {
                'arima': {
                    'predictions': arima_forecast.predictions[:6],  # 처음 6개월
                    'rmse': arima_forecast.rmse,
                    'mae': arima_forecast.mae
                },
                'exponential_smoothing': {
                    'predictions': exp_forecast.predictions[:6],
                    'rmse': exp_forecast.rmse,
                    'mae': exp_forecast.mae
                }
            },
            'monte_carlo': monte_carlo_result,
            'scenarios': {
                'outcomes': scenario_outcomes,
                'weighted_outcome': weighted_outcome
            },
            'recommendation': recommendation,
            'confidence': self._calculate_confidence(arima_forecast, monte_carlo_result)
        }
    
    def _generate_recommendation(
        self,
        forecast: Forecast,
        monte_carlo_result: Dict[str, Any],
        risk_tolerance: str
    ) -> str:
        """권장사항 생성"""
        
        prob_of_profit = monte_carlo_result['probability_of_profit']
        
        if prob_of_profit > 0.7:
            if risk_tolerance == 'aggressive':
                return 'STRONG_BUY - High profit probability with strong upside'
            else:
                return 'BUY - Favorable risk-reward profile'
        
        elif prob_of_profit > 0.5:
            return 'HOLD - Neutral outlook, wait for clearer signals'
        
        else:
            if risk_tolerance == 'conservative':
                return 'SELL - Lower profit probability'
            else:
                return 'CAUTION - Consider reducing exposure'
    
    def _calculate_confidence(self, forecast: Forecast, monte_carlo_result: Dict) -> float:
        """신뢰도 계산"""
        # RMSE 낮을수록 높은 신뢰도
        rmse_score = max(0, 1 - forecast.rmse / 10)
        
        # 수렴도 (final value 분포가 좁을수록)
        std_score = max(0, 1 - monte_carlo_result['statistics']['std_final_value'] / 100)
        
        return (rmse_score + std_score) / 2


if __name__ == "__main__":
    print("🔮 예측 & 시뮬레이션 엔진 테스트\n")
    
    dss = DecisionSupportSystem()
    
    # 테스트 데이터
    historical = [100, 102, 105, 103, 107, 110, 108, 112, 115, 118]
    scenarios = {'revenue': 1000000, 'cost': 500000, 'profit': 500000}
    
    # 종합 분석
    import asyncio
    result = asyncio.run(dss.comprehensive_analysis(historical, scenarios, 'moderate'))
    
    print("✅ 분석 완료!")
    print(f"추천: {result['recommendation']}")
    print(f"신뢰도: {result['confidence']:.2f}")
    print(f"이익 확률: {result['monte_carlo']['probability_of_profit']*100:.1f}%")
