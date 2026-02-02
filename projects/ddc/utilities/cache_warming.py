"""
캐시 워밍 & 사전 계산 - 성능 최적화

역할:
- 자주 사용되는 데이터 사전 캐싱
- 계산 결과 미리 저장
- 메모리 효율 관리
- 응답 시간 단축
"""

from typing import Dict, Any, List, Callable, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import OrderedDict


@dataclass
class CacheEntry:
    """캐시 항목"""
    key: str
    value: Any
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    ttl_seconds: int = 3600  # 기본 1시간


class PreComputationCache:
    """사전 계산 캐시"""
    
    def __init__(self, max_size: int = 10000):
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
        self.computation_tasks = []
    
    def register_precomputation(
        self,
        key: str,
        computation_func: Callable,
        schedule: str = 'hourly'  # hourly, daily, on_demand
    ):
        """사전 계산 등록"""
        
        self.computation_tasks.append({
            'key': key,
            'func': computation_func,
            'schedule': schedule,
            'last_computed': None
        })
    
    async def warmup(self):
        """캐시 워밍"""
        
        for task in self.computation_tasks:
            if task['schedule'] == 'on_demand':
                continue
            
            try:
                import asyncio
                
                if asyncio.iscoroutinefunction(task['func']):
                    result = await task['func']()
                else:
                    result = task['func']()
                
                self.set(task['key'], result, ttl_seconds=3600)
                task['last_computed'] = datetime.now()
            
            except Exception as e:
                print(f"Precomputation error for {task['key']}: {e}")
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """캐시 설정"""
        
        now = datetime.now()
        
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            accessed_at=now,
            ttl_seconds=ttl_seconds
        )
        
        self.cache[key] = entry
        
        # LRU 정책: 최대 크기 초과 시 가장 오래된 항목 제거
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    def get(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        
        if key not in self.cache:
            self.miss_count += 1
            return None
        
        entry = self.cache[key]
        
        # TTL 확인
        if datetime.now() - entry.created_at > timedelta(seconds=entry.ttl_seconds):
            del self.cache[key]
            self.miss_count += 1
            return None
        
        # 접근 정보 업데이트
        entry.accessed_at = datetime.now()
        entry.access_count += 1
        
        self.hit_count += 1
        return entry.value
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계"""
        
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate_percent': hit_rate,
            'precomputation_tasks': len(self.computation_tasks)
        }


class ComputationOptimizer:
    """계산 최적화"""
    
    def __init__(self):
        self.cache = PreComputationCache()
        self.computation_log = []
    
    async def compute_with_caching(
        self,
        key: str,
        computation_func: Callable,
        force_recompute: bool = False
    ) -> Dict[str, Any]:
        """캐싱과 함께 계산"""
        
        start_time = datetime.now()
        
        # 캐시 확인
        if not force_recompute:
            cached_value = self.cache.get(key)
            if cached_value is not None:
                return {
                    'status': 'cached',
                    'value': cached_value,
                    'duration_ms': 0
                }
        
        # 계산 수행
        try:
            import asyncio
            
            if asyncio.iscoroutinefunction(computation_func):
                result = await computation_func()
            else:
                result = computation_func()
            
            # 캐시에 저장
            self.cache.set(key, result)
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # 로그 기록
            self.computation_log.append({
                'timestamp': start_time.isoformat(),
                'key': key,
                'duration_ms': duration_ms,
                'status': 'computed'
            })
            
            return {
                'status': 'computed',
                'value': result,
                'duration_ms': duration_ms
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'error_type': type(e).__name__
            }
    
    def batch_precompute(
        self,
        tasks: List[Tuple[str, Callable]]
    ) -> Dict[str, Any]:
        """배치 사전 계산"""
        
        results = {}
        
        for key, func in tasks:
            try:
                import asyncio
                
                if asyncio.iscoroutinefunction(func):
                    result = asyncio.run(func())
                else:
                    result = func()
                
                self.cache.set(key, result)
                results[key] = {'status': 'success'}
            
            except Exception as e:
                results[key] = {'status': 'error', 'message': str(e)}
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(tasks),
            'results': results,
            'cache_stats': self.cache.get_cache_stats()
        }
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """최적화 리포트"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cache': self.cache.get_cache_stats(),
            'recent_computations': self.computation_log[-10:] if self.computation_log else [],
            'avg_computation_time_ms': sum(
                log['duration_ms'] for log in self.computation_log
            ) / len(self.computation_log) if self.computation_log else 0
        }


class QueryCache:
    """쿼리 결과 캐싱"""
    
    def __init__(self):
        self.query_cache: Dict[str, CacheEntry] = {}
        self.query_patterns = {}
    
    def cache_query_result(
        self,
        query: str,
        result: Any,
        ttl_seconds: int = 300
    ):
        """쿼리 결과 캐싱"""
        
        # 쿼리를 정규화하여 키 생성
        import hashlib
        query_hash = hashlib.md5(query.encode()).hexdigest()
        
        entry = CacheEntry(
            key=query_hash,
            value=result,
            created_at=datetime.now(),
            accessed_at=datetime.now(),
            ttl_seconds=ttl_seconds
        )
        
        self.query_cache[query_hash] = entry
    
    def get_cached_query_result(self, query: str) -> Optional[Any]:
        """캐시된 쿼리 결과 조회"""
        
        import hashlib
        query_hash = hashlib.md5(query.encode()).hexdigest()
        
        if query_hash not in self.query_cache:
            return None
        
        entry = self.query_cache[query_hash]
        
        # TTL 확인
        if datetime.now() - entry.created_at > timedelta(seconds=entry.ttl_seconds):
            del self.query_cache[query_hash]
            return None
        
        entry.access_count += 1
        return entry.value
    
    def invalidate_pattern(self, pattern: str):
        """패턴 기반 캐시 무효화"""
        
        import re
        
        regex = re.compile(pattern)
        
        to_delete = [
            key for key in self.query_cache.keys()
            if regex.search(key)
        ]
        
        for key in to_delete:
            del self.query_cache[key]
        
        return {'invalidated': len(to_delete)}


if __name__ == "__main__":
    print("⚡ 캐시 워밍 & 사전 계산 테스트\n")
    
    optimizer = ComputationOptimizer()
    
    # 사전 계산 함수
    def compute_analytics():
        import time
        time.sleep(0.1)  # 시뮬레이션
        return {'metrics': 'analytics_data', 'timestamp': datetime.now().isoformat()}
    
    # 캐시 워밍
    import asyncio
    
    async def test():
        # 첫 번째 계산
        result1 = await optimizer.compute_with_caching(
            'analytics',
            compute_analytics
        )
        print(f"첫 번째: {result1['status']} ({result1['duration_ms']:.1f}ms)")
        
        # 두 번째 계산 (캐시됨)
        result2 = await optimizer.compute_with_caching(
            'analytics',
            compute_analytics
        )
        print(f"두 번째: {result2['status']} ({result2['duration_ms']:.1f}ms)")
        
        # 통계
        report = optimizer.get_optimization_report()
        print(f"\n✅ 최적화 리포트:")
        print(f"캐시 크기: {report['cache']['cache_size']}")
        print(f"히트율: {report['cache']['hit_rate_percent']:.1f}%")
    
    asyncio.run(test())
