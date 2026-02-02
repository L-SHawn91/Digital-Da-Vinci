"""
마이크로서비스 오케스트레이션 - 분산 시스템 관리

역할:
- 서비스 발견 & 레지스트리
- 로드 밸런싱
- 서비스 간 통신
- 장애 처리 & 복구
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class ServiceStatus(Enum):
    """서비스 상태"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"


@dataclass
class ServiceInstance:
    """서비스 인스턴스"""
    id: str
    name: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.HEALTHY
    last_heartbeat: datetime = None
    response_time_ms: float = 0.0
    error_count: int = 0
    request_count: int = 0
    
    def __post_init__(self):
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()
    
    def get_health_score(self) -> float:
        """건강도 점수 (0-1)"""
        if self.status == ServiceStatus.OFFLINE:
            return 0.0
        elif self.status == ServiceStatus.UNHEALTHY:
            return 0.3
        elif self.status == ServiceStatus.DEGRADED:
            return 0.6
        
        # 응답시간 & 에러 기반 점수
        time_score = max(0, 1 - self.response_time_ms / 1000)
        
        if self.request_count > 0:
            error_score = 1 - (self.error_count / self.request_count)
        else:
            error_score = 1.0
        
        return (time_score + error_score) / 2


class ServiceRegistry:
    """서비스 레지스트리"""
    
    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.service_metadata: Dict[str, Dict[str, Any]] = {}
        self.heartbeat_timeout = 30  # 초
    
    def register_service(
        self,
        service_name: str,
        instance: ServiceInstance,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """서비스 등록"""
        
        if service_name not in self.services:
            self.services[service_name] = []
        
        self.services[service_name].append(instance)
        
        if service_name not in self.service_metadata:
            self.service_metadata[service_name] = {}
        
        if metadata:
            self.service_metadata[service_name].update(metadata)
        
        return {
            'status': 'registered',
            'service': service_name,
            'instance_id': instance.id,
            'total_instances': len(self.services[service_name])
        }
    
    def deregister_service(self, service_name: str, instance_id: str) -> Dict[str, Any]:
        """서비스 등록 해제"""
        
        if service_name in self.services:
            self.services[service_name] = [
                i for i in self.services[service_name]
                if i.id != instance_id
            ]
        
        return {'status': 'deregistered', 'instance_id': instance_id}
    
    def heartbeat(self, service_name: str, instance_id: str) -> Dict[str, Any]:
        """하트비트 수신"""
        
        if service_name in self.services:
            for instance in self.services[service_name]:
                if instance.id == instance_id:
                    instance.last_heartbeat = datetime.now()
                    instance.status = ServiceStatus.HEALTHY
                    return {'status': 'acknowledged'}
        
        return {'status': 'error', 'message': 'Instance not found'}
    
    def get_healthy_instances(self, service_name: str) -> List[ServiceInstance]:
        """건강한 인스턴스 조회"""
        
        if service_name not in self.services:
            return []
        
        # 하트비트 타임아웃 확인
        now = datetime.now()
        
        healthy = []
        for instance in self.services[service_name]:
            if instance.last_heartbeat:
                elapsed = (now - instance.last_heartbeat).total_seconds()
                if elapsed > self.heartbeat_timeout:
                    instance.status = ServiceStatus.OFFLINE
                elif instance.status == ServiceStatus.HEALTHY:
                    healthy.append(instance)
        
        return healthy
    
    def get_service_health(self, service_name: str) -> Dict[str, Any]:
        """서비스 건강도"""
        
        instances = self.services.get(service_name, [])
        
        if not instances:
            return {'status': 'service_not_found'}
        
        health_scores = [i.get_health_score() for i in instances]
        
        return {
            'service_name': service_name,
            'total_instances': len(instances),
            'healthy_instances': len(self.get_healthy_instances(service_name)),
            'avg_health_score': sum(health_scores) / len(health_scores),
            'min_health_score': min(health_scores),
            'max_health_score': max(health_scores),
            'instances': [
                {
                    'id': i.id,
                    'host': i.host,
                    'status': i.status.value,
                    'health_score': i.get_health_score()
                }
                for i in instances
            ]
        }


class LoadBalancer:
    """로드 밸런서"""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.routing_policy = 'round_robin'  # round_robin, least_connections, health_based
        self.request_count = 0
    
    def select_instance(self, service_name: str) -> Optional[ServiceInstance]:
        """인스턴스 선택"""
        
        healthy_instances = self.registry.get_healthy_instances(service_name)
        
        if not healthy_instances:
            return None
        
        if self.routing_policy == 'round_robin':
            selected = healthy_instances[self.request_count % len(healthy_instances)]
        
        elif self.routing_policy == 'least_connections':
            selected = min(healthy_instances, key=lambda i: i.request_count)
        
        elif self.routing_policy == 'health_based':
            # 건강도 가중치로 선택
            selected = max(healthy_instances, key=lambda i: i.get_health_score())
        
        else:
            selected = healthy_instances[0]
        
        self.request_count += 1
        return selected
    
    def route_request(
        self,
        service_name: str,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """요청 라우팅"""
        
        instance = self.select_instance(service_name)
        
        if not instance:
            return {
                'status': 'error',
                'message': f'No healthy instances for {service_name}'
            }
        
        # 요청 카운트 증가
        instance.request_count += 1
        
        return {
            'status': 'routed',
            'service': service_name,
            'instance': instance.id,
            'endpoint': f"http://{instance.host}:{instance.port}",
            'request_id': f"req_{self.request_count}"
        }


class CircuitBreaker:
    """서킷 브레이커 (장애 격리)"""
    
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
    
    async def call(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """함수 호출 (서킷 브레이커 로직)"""
        
        now = datetime.now()
        
        # 상태 관리
        if self.state == 'open':
            # 타임아웃 경과 확인
            if self.last_failure_time:
                elapsed = (now - self.last_failure_time).total_seconds()
                if elapsed > self.timeout_seconds:
                    self.state = 'half_open'
                    self.failure_count = 0
                else:
                    return {
                        'status': 'error',
                        'message': 'Circuit breaker is OPEN',
                        'retry_after_seconds': self.timeout_seconds - int(elapsed)
                    }
        
        # 함수 실행
        try:
            result = await func(*args, **kwargs) if hasattr(func, '__await__') else func(*args, **kwargs)
            
            # 성공
            if self.state == 'half_open':
                self.state = 'closed'
                self.failure_count = 0
            
            return {'status': 'success', 'result': result}
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = now
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
            
            return {
                'status': 'error',
                'message': str(e),
                'circuit_state': self.state
            }


class ServiceMeshOrchestrator:
    """서비스 메시 오케스트레이터"""
    
    def __init__(self):
        self.registry = ServiceRegistry()
        self.load_balancer = LoadBalancer(self.registry)
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def register_service_instance(
        self,
        service_name: str,
        host: str,
        port: int,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """서비스 인스턴스 등록"""
        
        instance = ServiceInstance(
            id=f"{service_name}_{host}_{port}",
            name=service_name,
            host=host,
            port=port
        )
        
        return self.registry.register_service(service_name, instance, metadata)
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """서킷 브레이커 조회"""
        
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        
        return self.circuit_breakers[service_name]
    
    def get_mesh_status(self) -> Dict[str, Any]:
        """메시 상태"""
        
        services_health = {}
        
        for service_name in self.registry.services.keys():
            services_health[service_name] = self.registry.get_service_health(service_name)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_services': len(services_health),
            'services': services_health,
            'load_balancer_policy': self.load_balancer.routing_policy,
            'circuit_breakers': {
                name: {
                    'state': cb.state,
                    'failure_count': cb.failure_count
                }
                for name, cb in self.circuit_breakers.items()
            }
        }


if __name__ == "__main__":
    print("🔗 마이크로서비스 오케스트레이션 테스트\n")
    
    mesh = ServiceMeshOrchestrator()
    
    # 서비스 등록
    mesh.register_service_instance("api", "localhost", 8001)
    mesh.register_service_instance("api", "localhost", 8002)
    mesh.register_service_instance("api", "localhost", 8003)
    
    mesh.register_service_instance("database", "db.local", 5432)
    mesh.register_service_instance("database", "db-replica.local", 5432)
    
    print("✅ 서비스 등록 완료!")
    
    # 하트비트
    for instance in mesh.registry.services["api"]:
        mesh.registry.heartbeat("api", instance.id)
    
    print("✅ 하트비트 수신 완료!")
    
    # 요청 라우팅
    for i in range(5):
        routing = mesh.load_balancer.route_request("api", {"query": "test"})
        print(f"요청 {i+1}: {routing['instance']}")
    
    print("\n✅ 메시 상태:")
    status = mesh.get_mesh_status()
    print(f"서비스: {status['total_services']}")
    for svc_name, health in status['services'].items():
        print(f"  {svc_name}: {health['avg_health_score']:.2f}")
