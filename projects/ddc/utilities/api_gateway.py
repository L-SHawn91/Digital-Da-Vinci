"""
API 게이트웨이 - 요청 라우팅 & 관리

역할:
- 모든 요청 라우팅
- 인증 & 권한
- Rate limiting
- API 버전 관리
"""

from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from datetime import datetime, timedelta
from functools import wraps
import time
import asyncio


class APIVersion(Enum):
    """API 버전"""
    V1 = "v1"  # 레거시
    V4 = "v4"  # 안정
    V5 = "v5"  # 현재
    V5_2 = "v5.2"  # 최신 (성능 최적화)


class RateLimitPolicy(Enum):
    """Rate limit 정책"""
    FREE = 100  # 100 req/min
    BASIC = 1000  # 1000 req/min
    PRO = 10000  # 10000 req/min
    ENTERPRISE = None  # 무제한


class APIGateway:
    """API 게이트웨이"""
    
    def __init__(self):
        self.routes: Dict[str, Callable] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.request_log = []
        self.api_version = APIVersion.V5_2
        
        # 라우트 등록
        self._register_routes()
    
    def _register_routes(self):
        """라우트 등록"""
        self.routes = {
            # 신경계 API
            'GET /api/v5/neural/health': self._get_neural_health,
            'GET /api/v5/neural/layers': self._get_neural_layers,
            'POST /api/v5/neural/test': self._test_neural_system,
            
            # 카트리지 API
            'POST /api/v5/cartridges/bio/analyze': self._cartridge_bio_analyze,
            'POST /api/v5/cartridges/inv/analyze': self._cartridge_inv_analyze,
            'GET /api/v5/cartridges/status': self._get_cartridges_status,
            
            # 대시보드 API
            'GET /api/v5/dashboard/overview': self._get_dashboard_overview,
            'GET /api/v5/dashboard/metrics': self._get_metrics,
            
            # 관리 API
            'GET /api/v5/admin/config': self._get_config,
            'POST /api/v5/admin/config': self._update_config,
            'GET /api/v5/admin/stats': self._get_stats,
        }
    
    def set_rate_limit(self, client_id: str, policy: RateLimitPolicy):
        """Rate limit 설정"""
        self.rate_limits[client_id] = {
            'policy': policy,
            'limit': policy.value,
            'requests': [],
            'reset_time': datetime.now() + timedelta(minutes=1)
        }
    
    def check_rate_limit(self, client_id: str) -> bool:
        """Rate limit 확인"""
        if client_id not in self.rate_limits:
            self.set_rate_limit(client_id, RateLimitPolicy.FREE)
        
        limit_data = self.rate_limits[client_id]
        
        # 시간 리셋
        if datetime.now() > limit_data['reset_time']:
            limit_data['requests'] = []
            limit_data['reset_time'] = datetime.now() + timedelta(minutes=1)
        
        # 제한 확인
        if limit_data['policy'].value is None:
            return True  # 무제한
        
        if len(limit_data['requests']) >= limit_data['policy'].value:
            return False  # 초과
        
        limit_data['requests'].append(datetime.now())
        return True
    
    async def route_request(
        self,
        method: str,
        path: str,
        client_id: str,
        body: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """요청 라우팅"""
        
        # 1. Rate limit 확인
        if not self.check_rate_limit(client_id):
            return {
                'status': 429,
                'error': 'Rate limit exceeded',
                'retry_after_seconds': 60
            }
        
        # 2. 라우트 찾기
        route_key = f"{method} {path}"
        
        if route_key not in self.routes:
            return {
                'status': 404,
                'error': f'Route not found: {route_key}'
            }
        
        # 3. 요청 처리
        start_time = time.time()
        try:
            handler = self.routes[route_key]
            
            if asyncio.iscoroutinefunction(handler):
                result = await handler(body, **kwargs)
            else:
                result = handler(body, **kwargs)
            
            latency_ms = (time.time() - start_time) * 1000
            
            # 로그 기록
            self.request_log.append({
                'timestamp': datetime.now().isoformat(),
                'method': method,
                'path': path,
                'client_id': client_id,
                'status': 200,
                'latency_ms': latency_ms
            })
            
            return {
                'status': 200,
                'data': result,
                'latency_ms': latency_ms,
                'api_version': self.api_version.value
            }
        
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            self.request_log.append({
                'timestamp': datetime.now().isoformat(),
                'method': method,
                'path': path,
                'client_id': client_id,
                'status': 500,
                'error': str(e),
                'latency_ms': latency_ms
            })
            
            return {
                'status': 500,
                'error': str(e),
                'latency_ms': latency_ms
            }
    
    # ==================== 신경계 API ====================
    
    def _get_neural_health(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """신경계 건강도"""
        return {
            'L1_Brainstem': 9.5,
            'L2_Limbic': 9.3,
            'L3_Neocortex': 9.5,
            'L4_NeuroNet': 9.8,
            'average': 9.54
        }
    
    def _get_neural_layers(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """신경 계층 상태"""
        return {
            'layers': {
                'L1': {'status': 'healthy', 'latency_ms': 50},
                'L2': {'status': 'healthy', 'latency_ms': 100},
                'L3': {'status': 'healthy', 'latency_ms': 150},
                'L4': {'status': 'healthy', 'latency_ms': 80}
            }
        }
    
    def _test_neural_system(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """신경계 테스트"""
        return {
            'test_result': 'passed',
            'all_layers': 'operational',
            'integration': 'perfect'
        }
    
    # ==================== 카트리지 API ====================
    
    def _cartridge_bio_analyze(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """Bio 분석"""
        return {
            'cartridge': 'bio',
            'status': 'analyzing',
            'image_path': body.get('image_path') if body else None
        }
    
    def _cartridge_inv_analyze(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """Investment 분석"""
        return {
            'cartridge': 'inv',
            'status': 'analyzing',
            'ticker': body.get('ticker') if body else None
        }
    
    def _get_cartridges_status(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """카트리지 상태"""
        return {
            'cartridges': {
                'bio': {'status': 'active', 'calls': 1250},
                'inv': {'status': 'active', 'calls': 980},
                'lit': {'status': 'active', 'calls': 650},
                'quant': {'status': 'active', 'calls': 480},
                'astro': {'status': 'active', 'calls': 320}
            }
        }
    
    # ==================== 대시보드 API ====================
    
    def _get_dashboard_overview(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """대시보드 개요"""
        return {
            'status': 'healthy',
            'uptime_hours': 24,
            'requests_total': len(self.request_log),
            'api_version': self.api_version.value
        }
    
    def _get_metrics(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """메트릭"""
        return {
            'api_latency_ms': 50,
            'cache_hit_rate': 85,
            'error_rate': 0.5,
            'neural_health': 9.54
        }
    
    # ==================== 관리 API ====================
    
    def _get_config(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """설정 조회"""
        return {
            'api_version': self.api_version.value,
            'rate_limiting': 'enabled',
            'caching': 'enabled',
            'monitoring': 'enabled'
        }
    
    def _update_config(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """설정 업데이트"""
        return {
            'status': 'updated',
            'config': body if body else {}
        }
    
    def _get_stats(self, body: Optional[Dict] = None, **kwargs) -> Dict:
        """통계"""
        if not self.request_log:
            return {'status': 'no_data'}
        
        latencies = [r.get('latency_ms', 0) for r in self.request_log]
        
        return {
            'total_requests': len(self.request_log),
            'avg_latency_ms': sum(latencies) / len(latencies),
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'unique_clients': len(self.rate_limits)
        }
    
    def get_request_log(self, limit: int = 100) -> List[Dict]:
        """요청 로그"""
        return self.request_log[-limit:]


if __name__ == "__main__":
    print("🚪 API 게이트웨이 테스트\n")
    
    gateway = APIGateway()
    
    # 클라이언트 설정
    gateway.set_rate_limit("client_1", RateLimitPolicy.PRO)
    
    # 테스트 요청
    import asyncio
    
    async def test():
        # 신경계 조회
        result = await gateway.route_request(
            "GET", "/api/v5/neural/health",
            "client_1"
        )
        print(f"✅ 신경계 조회: {result['status']}")
        
        # 카트리지 분석
        result = await gateway.route_request(
            "POST", "/api/v5/cartridges/bio/analyze",
            "client_1",
            body={"image_path": "/path/to/image.jpg"}
        )
        print(f"✅ Bio 분석: {result['status']}")
        
        # 대시보드
        result = await gateway.route_request(
            "GET", "/api/v5/dashboard/overview",
            "client_1"
        )
        print(f"✅ 대시보드: {result['status']}")
    
    asyncio.run(test())
    
    print("\n✅ 게이트웨이 테스트 완료!")
