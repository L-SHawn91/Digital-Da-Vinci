"""
Inv Cartridge Interface - 신피질과의 연결

신피질의 Prefrontal (전두엽)과 Parietal (두정엽)을 활용한 투자 분석
"""

from typing import Dict, Any, Optional, List
import os

# neocortex 임포트
try:
    from ddc.brain.neocortex.prefrontal import decision_framework
    from ddc.brain.neocortex.parietal import innovation_engine
    NEOCORTEX_AVAILABLE = True
except ImportError:
    NEOCORTEX_AVAILABLE = False
    print("⚠️ Warning: neocortex 모듈을 찾을 수 없습니다.")


class InvCartridgeInterface:
    """Inv Cartridge Interface - neocortex와 협력"""
    
    def __init__(self):
        """초기화"""
        self.decision_framework = decision_framework if NEOCORTEX_AVAILABLE else None
        self.innovation_engine = innovation_engine if NEOCORTEX_AVAILABLE else None
    
    def analyze_stock_with_neocortex(
        self,
        ticker: str,
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        주식 분석 (neocortex 협력)
        
        Args:
            ticker: 종목 코드 (e.g., 'TSLA', '005930')
            analysis_data: 투자 카트리지의 기본 분석 데이터
                - technical_analysis: 기술 분석 결과
                - fundamental_analysis: 기본 분석 결과
                - analyst_opinions: 애널리스트 의견
                
        Returns:
            최종 투자 추천
        """
        
        result = {
            'ticker': ticker,
            'basic_analysis': analysis_data,
            'neocortex_integration': {}
        }
        
        if not NEOCORTEX_AVAILABLE:
            return result
        
        # Step 1: Parietal (두정엽) - 수치 분석 & 공간 통합
        print(f"🧠 Parietal (두정엽): 수치 분석 및 통합")
        try:
            numerical_analysis = self.innovation_engine.analyze_numerical_data(
                ticker=ticker,
                technical_data=analysis_data.get('technical_analysis', {}),
                fundamental_data=analysis_data.get('fundamental_analysis', {})
            )
            result['neocortex_integration']['numerical_analysis'] = numerical_analysis
        except Exception as e:
            print(f"⚠️ Parietal 처리 오류: {e}")
        
        # Step 2: Prefrontal (전두엽) - 의사결정
        print(f"🧠 Prefrontal (전두엽): 최종 의사결정")
        try:
            decision_input = {
                'ticker': ticker,
                'numerical': result['neocortex_integration'].get('numerical_analysis', {}),
                'analyst_opinions': analysis_data.get('analyst_opinions', []),
                'risk_level': analysis_data.get('risk_level', 'medium')
            }
            
            final_decision = self.decision_framework.make_investment_decision(
                decision_input
            )
            result['neocortex_integration']['final_decision'] = final_decision
        except Exception as e:
            print(f"⚠️ Prefrontal 처리 오류: {e}")
        
        # Step 3: 신피질 통합 분석
        print(f"🧠 신피질 통합 분석 완료")
        result['neocortex_integration']['status'] = 'complete'
        
        return result
    
    def compare_multiple_stocks(
        self,
        tickers: List[str],
        analyses_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        여러 종목 비교 분석 (Parietal 공간 통합)
        
        Args:
            tickers: 비교할 종목 코드 리스트
            analyses_data: 각 종목의 분석 데이터
                예: {'TSLA': {...}, 'NIO': {...}, '005930': {...}}
                
        Returns:
            비교 분석 결과
        """
        
        results = []
        for ticker in tickers:
            print(f"\n📊 {ticker} 분석 중...")
            analysis = self.analyze_stock_with_neocortex(
                ticker,
                analyses_data.get(ticker, {})
            )
            results.append(analysis)
        
        # Parietal (두정엽)로 상대 비교 분석
        if NEOCORTEX_AVAILABLE and self.innovation_engine:
            print("\n🧠 Parietal: 상대 비교 분석")
            try:
                comparative_analysis = self.innovation_engine.compare_investments(
                    analyses=results
                )
                
                return {
                    'individual_analyses': results,
                    'comparative_ranking': comparative_analysis,
                    'best_opportunity': self._find_best_opportunity(comparative_analysis)
                }
            except Exception as e:
                print(f"⚠️ 비교 분석 오류: {e}")
        
        return {'individual_analyses': results}
    
    def portfolio_optimization(
        self,
        holdings: Dict[str, float],
        analyses_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        포트폴리오 최적화 (Prefrontal 의사결정 + Parietal 통합)
        
        Args:
            holdings: 현재 보유 종목 및 비율
                예: {'TSLA': 0.3, '005930': 0.3, 'NIO': 0.4}
            analyses_data: 각 종목의 분석 데이터
            
        Returns:
            포트폴리오 재구성 추천
        """
        
        print("🧠 포트폴리오 최적화 시작")
        
        # Step 1: 각 종목 분석
        individual_results = {}
        for ticker, weight in holdings.items():
            analysis = self.analyze_stock_with_neocortex(
                ticker,
                analyses_data.get(ticker, {})
            )
            individual_results[ticker] = {
                'analysis': analysis,
                'current_weight': weight
            }
        
        # Step 2: Parietal + Prefrontal로 최적화
        result = {
            'current_portfolio': holdings,
            'individual_analyses': individual_results,
            'recommendations': {}
        }
        
        if NEOCORTEX_AVAILABLE:
            try:
                # Parietal: 포트폴리오 공간 분석
                portfolio_space = self.innovation_engine.analyze_portfolio_space(
                    holdings=holdings,
                    analyses=list(individual_results.values())
                )
                
                # Prefrontal: 최적화 의사결정
                optimized = self.decision_framework.optimize_portfolio(
                    current=holdings,
                    space_analysis=portfolio_space
                )
                
                result['recommendations'] = optimized
            except Exception as e:
                print(f"⚠️ 포트폴리오 최적화 오류: {e}")
        
        return result
    
    @staticmethod
    def _find_best_opportunity(comparative_analysis: Dict[str, Any]) -> Optional[str]:
        """최고의 투자 기회 찾기"""
        try:
            if 'ranking' in comparative_analysis:
                return comparative_analysis['ranking'][0]
        except:
            pass
        return None


# 편의 함수
def analyze_stock(ticker: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """간단한 주식 분석 (neocortex 협력)"""
    interface = InvCartridgeInterface()
    return interface.analyze_stock_with_neocortex(ticker, analysis_data)


if __name__ == "__main__":
    # 테스트
    print("💰 Inv Cartridge Interface 테스트")
    print(f"neocortex 상태: {'✅ Available' if NEOCORTEX_AVAILABLE else '❌ Not Available'}")
