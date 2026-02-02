"""
캐싱 시스템 - 성능 최적화

역할:
- Multi-level 캐싱 (Memory, Redis, Pinecone)
- API 응답 캐싱
- 신경계 신호 캐싱
- 카트리지 결과 캐싱
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import hashlib
from functools import wraps
import time


class CacheManager:
    """멀티레벨 캐시 관리자"""
    
    def __init__(self):
        """초기화"""
        self.memory_cache = {}  # L1: 메모리 캐시
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size': 0
        }
        self.max_memory_size = 100 * 1024 * 1024  # 100MB
        
    def _generate_key(self, *args, **kwargs) -> str:
        """캐시 키 생성"""
        key_str = json.dumps({
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        })
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str, ttl: int = 3600) -> Optional[Any]:
        """캐시에서 값 조회"""
        if key in self.memory_cache:
            cached = self.memory_cache[key]
            
            # TTL 확인
            if datetime.now() - cached['timestamp'] < timedelta(seconds=ttl):
                self.cache_stats['hits'] += 1
                return cached['value']
            else:
                # TTL 만료, 삭제
                del self.memory_cache[key]
                self.cache_stats['evictions'] += 1
        
        self.cache_stats['misses'] += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """캐시에 값 저장"""
        size = len(json.dumps(value).encode())
        
        # 용량 초과 시 가장 오래된 항목 삭제
        if self.cache_stats['total_size'] + size > self.max_memory_size:
            self._evict_oldest()
        
        self.memory_cache[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'ttl': ttl,
            'size': size
        }
        self.cache_stats['total_size'] += size
    
    def _evict_oldest(self) -> None:
        """가장 오래된 항목 제거"""
        if not self.memory_cache:
            return
        
        oldest_key = min(
            self.memory_cache.items(),
            key=lambda x: x[1]['timestamp']
        )[0]
        
        removed_size = self.memory_cache[oldest_key]['size']
        del self.memory_cache[oldest_key]
        self.cache_stats['total_size'] -= removed_size
        self.cache_stats['evictions'] += 1
    
    def clear(self) -> None:
        """캐시 초기화"""
        self.memory_cache.clear()
        self.cache_stats['total_size'] = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total * 100) if total > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': round(hit_rate, 2),
            'evictions': self.cache_stats['evictions'],
            'total_size_mb': round(self.cache_stats['total_size'] / 1024 / 1024, 2),
            'cached_items': len(self.memory_cache)
        }


class APIResponseCache:
    """API 응답 캐싱"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
    
    def cache_bio_analysis(self, image_path: str, ttl: int = 3600):
        """Bio 분석 결과 캐싱 데코레이터"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self.cache._generate_key('bio', image_path, *args, **kwargs)
                
                # 캐시 확인
                cached = self.cache.get(key, ttl)
                if cached is not None:
                    return cached
                
                # 함수 실행
                result = func(*args, **kwargs)
                
                # 결과 캐싱
                self.cache.set(key, result, ttl)
                return result
            
            return wrapper
        return decorator
    
    def cache_stock_analysis(self, ticker: str, ttl: int = 900):
        """주식 분석 결과 캐싱 (15분)"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self.cache._generate_key('stock', ticker, *args, **kwargs)
                
                cached = self.cache.get(key, ttl)
                if cached is not None:
                    return cached
                
                result = func(*args, **kwargs)
                self.cache.set(key, result, ttl)
                return result
            
            return wrapper
        return decorator


class NeuralSignalCache:
    """신경 신호 캐싱"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.signal_history = []
    
    def cache_neural_health(self, level: str, ttl: int = 60):
        """신경계 건강도 캐싱 (1분)"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self.cache._generate_key('neural', level)
                
                cached = self.cache.get(key, ttl)
                if cached is not None:
                    return cached
                
                result = func(*args, **kwargs)
                self.cache.set(key, result, ttl)
                return result
            
            return wrapper
        return decorator
    
    def record_signal(self, level: str, health: float, latency: float) -> None:
        """신경 신호 기록"""
        signal = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'health': health,
            'latency': latency
        }
        self.signal_history.append(signal)
        
        # 최근 1000개만 유지
        if len(self.signal_history) > 1000:
            self.signal_history = self.signal_history[-1000:]
    
    def get_signal_trend(self, level: str, minutes: int = 5) -> Dict[str, Any]:
        """신경 신호 추세"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        
        recent_signals = [
            s for s in self.signal_history
            if s['level'] == level and 
            datetime.fromisoformat(s['timestamp']) > cutoff
        ]
        
        if not recent_signals:
            return {'status': 'no_data'}
        
        healths = [s['health'] for s in recent_signals]
        latencies = [s['latency'] for s in recent_signals]
        
        return {
            'level': level,
            'samples': len(recent_signals),
            'avg_health': sum(healths) / len(healths),
            'max_health': max(healths),
            'min_health': min(healths),
            'avg_latency': sum(latencies) / len(latencies),
            'trend': 'improving' if healths[-1] > healths[0] else 'degrading'
        }


class PerformanceMonitor:
    """성능 모니터"""
    
    def __init__(self):
        self.metrics = {
            'api_calls': [],
            'cartridge_calls': [],
            'neural_operations': []
        }
    
    def track_api_call(self, endpoint: str, duration: float, status: int):
        """API 호출 추적"""
        self.metrics['api_calls'].append({
            'endpoint': endpoint,
            'duration': duration,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_cartridge_call(self, cartridge: str, operation: str, duration: float):
        """카트리지 호출 추적"""
        self.metrics['cartridge_calls'].append({
            'cartridge': cartridge,
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_performance_report(self) -> Dict[str, Any]:
        """성능 리포트"""
        if not self.metrics['api_calls']:
            return {'status': 'no_data'}
        
        api_durations = [m['duration'] for m in self.metrics['api_calls']]
        
        return {
            'total_api_calls': len(self.metrics['api_calls']),
            'avg_api_latency': sum(api_durations) / len(api_durations),
            'max_api_latency': max(api_durations),
            'min_api_latency': min(api_durations),
            'p95_latency': sorted(api_durations)[int(len(api_durations) * 0.95)],
            'p99_latency': sorted(api_durations)[int(len(api_durations) * 0.99)]
        }


# 전역 인스턴스
cache_manager = CacheManager()
api_cache = APIResponseCache(cache_manager)
neural_cache = NeuralSignalCache(cache_manager)
perf_monitor = PerformanceMonitor()


if __name__ == "__main__":
    print("💾 캐싱 시스템 테스트")
    
    # 테스트 데이터 저장
    cache_manager.set('test_key', {'value': 'test_data'}, ttl=60)
    
    # 조회
    result = cache_manager.get('test_key', ttl=60)
    print(f"캐시 조회: {result}")
    
    # 통계
    print(f"캐시 통계: {cache_manager.get_stats()}")
