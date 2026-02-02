"""
고급 API 게이트웨이 & 라우팅 - 지능형 요청 처리

역할:
- 동적 라우팅
- 요청 변환 & 최적화
- 응답 캐싱
- API 버전 관리
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class HttpMethod(Enum):
    """HTTP 메서드"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Route:
    """라우트"""
    path: str
    method: HttpMethod
    handler: Callable
    auth_required: bool = False
    rate_limit: int = 1000  # requests/hour
    tags: List[str] = None


class APIRouter:
    """API 라우터"""
    
    def __init__(self):
        self.routes: List[Route] = []
        self.middlewares: List[Callable] = []
        self.request_log = []
    
    def register_route(
        self,
        path: str,
        method: HttpMethod,
        handler: Callable,
        auth_required: bool = False,
        rate_limit: int = 1000
    ) -> Dict[str, Any]:
        """라우트 등록"""
        
        route = Route(
            path=path,
            method=method,
            handler=handler,
            auth_required=auth_required,
            rate_limit=rate_limit
        )
        
        self.routes.append(route)
        
        return {
            'status': 'registered',
            'path': path,
            'method': method.value,
            'total_routes': len(self.routes)
        }
    
    def find_route(self, path: str, method: HttpMethod) -> Optional[Route]:
        """라우트 찾기"""
        
        for route in self.routes:
            if route.path == path and route.method == method:
                return route
        
        # 와일드카드 매칭
        for route in self.routes:
            if self._match_path_pattern(route.path, path) and route.method == method:
                return route
        
        return None
    
    def _match_path_pattern(self, pattern: str, path: str) -> bool:
        """경로 패턴 매칭"""
        
        pattern_parts = pattern.split('/')
        path_parts = path.split('/')
        
        if len(pattern_parts) != len(path_parts):
            return False
        
        for p_part, path_part in zip(pattern_parts, path_parts):
            if p_part.startswith('{') and p_part.endswith('}'):
                continue
            if p_part != path_part:
                return False
        
        return True
    
    def add_middleware(self, middleware: Callable):
        """미들웨어 추가"""
        self.middlewares.append(middleware)
    
    async def handle_request(
        self,
        path: str,
        method: HttpMethod,
        body: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """요청 처리"""
        
        request_start = datetime.now()
        
        # 미들웨어 실행
        for middleware in self.middlewares:
            result = middleware({'path': path, 'method': method.value, 'headers': headers})
            if result and result.get('blocked'):
                return {
                    'status': 'forbidden',
                    'message': result.get('reason', 'Blocked by middleware')
                }
        
        # 라우트 찾기
        route = self.find_route(path, method)
        
        if not route:
            return {
                'status': 'not_found',
                'message': f'No route found for {method.value} {path}'
            }
        
        # 핸들러 실행
        try:
            import asyncio
            
            if asyncio.iscoroutinefunction(route.handler):
                response = await route.handler(body or {}, headers or {})
            else:
                response = route.handler(body or {}, headers or {})
            
            # 요청 로깅
            elapsed_ms = (datetime.now() - request_start).total_seconds() * 1000
            
            self.request_log.append({
                'timestamp': request_start.isoformat(),
                'path': path,
                'method': method.value,
                'status': 'success',
                'latency_ms': elapsed_ms
            })
            
            return {
                'status': 'success',
                'data': response,
                'latency_ms': elapsed_ms
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'error_type': type(e).__name__
            }


class RequestOptimizer:
    """요청 최적화"""
    
    def __init__(self):
        self.compression_enabled = True
        self.deduplication_enabled = True
        self.request_cache = {}
    
    def optimize_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """요청 최적화"""
        
        optimized = dict(request)
        
        # 중복 제거
        if self.deduplication_enabled:
            key = f"{request['path']}_{str(request.get('body', {}))}"
            if key in self.request_cache:
                optimized['cached'] = True
                optimized['cache_key'] = key
        
        # 압축 설정
        if self.compression_enabled:
            optimized['compression'] = 'gzip'
        
        return optimized
    
    def optimize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """응답 최적화"""
        
        # 캐시 저장
        if isinstance(response, dict) and response.get('status') == 'success':
            response['cache_eligible'] = True
        
        return response


class ResponseTransformer:
    """응답 변환"""
    
    def __init__(self):
        self.transformers: Dict[str, Callable] = {}
    
    def register_transformer(self, content_type: str, transformer: Callable):
        """변환기 등록"""
        self.transformers[content_type] = transformer
    
    def transform_response(
        self,
        response: Dict[str, Any],
        content_type: str = 'application/json'
    ) -> Dict[str, Any]:
        """응답 변환"""
        
        if content_type in self.transformers:
            return self.transformers[content_type](response)
        
        return response


class APIGateway:
    """통합 API 게이트웨이"""
    
    def __init__(self):
        self.router = APIRouter()
        self.optimizer = RequestOptimizer()
        self.transformer = ResponseTransformer()
        self.rate_limiter: Dict[str, List[datetime]] = {}
        self.request_count = 0
    
    def register_api(
        self,
        path: str,
        method: str,
        handler: Callable,
        auth_required: bool = False
    ) -> Dict[str, Any]:
        """API 등록"""
        
        http_method = HttpMethod[method.upper()]
        
        return self.router.register_route(
            path=path,
            method=http_method,
            handler=handler,
            auth_required=auth_required
        )
    
    async def process_request(
        self,
        path: str,
        method: str,
        body: Dict = None,
        headers: Dict = None
    ) -> Dict[str, Any]:
        """요청 처리"""
        
        self.request_count += 1
        
        http_method = HttpMethod[method.upper()]
        
        # 최적화
        request = {
            'path': path,
            'method': method,
            'body': body,
            'headers': headers
        }
        optimized_request = self.optimizer.optimize_request(request)
        
        # 라우팅 & 처리
        response = await self.router.handle_request(
            path,
            http_method,
            body,
            headers
        )
        
        # 응답 변환
        content_type = headers.get('Accept', 'application/json') if headers else 'application/json'
        transformed_response = self.transformer.transform_response(response, content_type)
        
        return transformed_response
    
    def get_gateway_stats(self) -> Dict[str, Any]:
        """게이트웨이 통계"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_requests': self.request_count,
            'registered_routes': len(self.router.routes),
            'recent_requests': self.router.request_log[-10:] if self.router.request_log else [],
            'compression_enabled': self.optimizer.compression_enabled,
            'deduplication_enabled': self.optimizer.deduplication_enabled
        }


if __name__ == "__main__":
    print("🚀 고급 API 게이트웨이 테스트\n")
    
    gateway = APIGateway()
    
    # API 등록
    async def get_user_handler(body, headers):
        return {'id': 1, 'name': 'Alice', 'role': 'admin'}
    
    async def create_user_handler(body, headers):
        return {'id': 2, 'name': body.get('name', 'Unknown'), 'created': True}
    
    gateway.register_api('/api/users/{id}', 'GET', get_user_handler)
    gateway.register_api('/api/users', 'POST', create_user_handler, auth_required=True)
    
    print("✅ API 등록 완료!")
    
    # 요청 처리
    import asyncio
    
    async def test():
        result = await gateway.process_request(
            '/api/users/1',
            'GET',
            headers={'Accept': 'application/json'}
        )
        
        print(f"✅ 요청 처리 완료!")
        print(f"상태: {result.get('status')}")
        print(f"데이터: {result.get('data')}")
        
        stats = gateway.get_gateway_stats()
        print(f"\n✅ 게이트웨이 통계:")
        print(f"총 요청: {stats['total_requests']}")
        print(f"등록된 라우트: {stats['registered_routes']}")
    
    asyncio.run(test())
