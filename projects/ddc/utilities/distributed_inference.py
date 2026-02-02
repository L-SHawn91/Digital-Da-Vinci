"""
분산 추론 시스템 - 멀티 GPU/클라우드 최적화

역할:
- 분산 연산 관리
- 로드 밸런싱
- 장애 복구
- 비용 최적화
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime


class ComputeNodeType(Enum):
    """컴퓨트 노드 타입"""
    LOCAL_CPU = "local_cpu"
    LOCAL_GPU = "local_gpu"
    AWS_GPU = "aws_gpu"
    GOOGLE_TPU = "google_tpu"
    CLOUD_FUNCTION = "cloud_function"


@dataclass
class ComputeNode:
    """컴퓨트 노드"""
    id: str
    node_type: ComputeNodeType
    capacity: int  # 최대 동시 작업
    current_load: int  # 현재 작업 수
    latency_ms: float
    cost_per_hour: float
    availability: float  # 0-1
    available: bool = True
    
    def get_utilization(self) -> float:
        """사용률"""
        return self.current_load / self.capacity if self.capacity > 0 else 0
    
    def get_cost_per_task(self, duration_ms: float) -> float:
        """작업당 비용"""
        return (self.cost_per_hour / 3600000) * duration_ms


class LoadBalancer:
    """로드 밸런서"""
    
    def __init__(self):
        self.nodes: Dict[str, ComputeNode] = {}
        self.task_history = []
    
    def register_node(self, node: ComputeNode):
        """노드 등록"""
        self.nodes[node.id] = node
    
    def select_best_node(self, task_priority: str = 'balanced') -> Optional[ComputeNode]:
        """최적 노드 선택"""
        available_nodes = [
            n for n in self.nodes.values()
            if n.available and n.current_load < n.capacity
        ]
        
        if not available_nodes:
            return None
        
        if task_priority == 'speed':
            # 가장 빠른 노드
            return min(available_nodes, key=lambda x: x.latency_ms)
        
        elif task_priority == 'cost':
            # 가장 저렴한 노드
            return min(available_nodes, key=lambda x: x.cost_per_hour)
        
        else:  # balanced
            # 비용-성능 균형
            return min(
                available_nodes,
                key=lambda x: (x.latency_ms / 1000) / (x.cost_per_hour + 0.001)
            )
    
    def distribute_load(self, tasks: List[Dict[str, Any]], priority: str = 'balanced') -> Dict[str, List]:
        """작업 분배"""
        distribution = {node_id: [] for node_id in self.nodes.keys()}
        
        for task in tasks:
            node = self.select_best_node(priority)
            if node:
                distribution[node.id].append(task)
                node.current_load += 1
                self.task_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'task': task,
                    'node': node.id
                })
        
        return distribution


class DistributedInferenceSystem:
    """분산 추론 시스템"""
    
    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.cache = {}
        self.results = {}
        
        # 기본 노드 설정
        self._initialize_nodes()
    
    def _initialize_nodes(self):
        """기본 노드 초기화"""
        nodes = [
            ComputeNode(
                id="local_cpu_1",
                node_type=ComputeNodeType.LOCAL_CPU,
                capacity=4,
                current_load=0,
                latency_ms=50,
                cost_per_hour=0,
                availability=0.99
            ),
            ComputeNode(
                id="local_gpu_1",
                node_type=ComputeNodeType.LOCAL_GPU,
                capacity=8,
                current_load=0,
                latency_ms=30,
                cost_per_hour=0.5,
                availability=0.95
            ),
            ComputeNode(
                id="aws_gpu_1",
                node_type=ComputeNodeType.AWS_GPU,
                capacity=16,
                current_load=0,
                latency_ms=150,
                cost_per_hour=2.5,
                availability=0.99
            ),
            ComputeNode(
                id="cloud_function_1",
                node_type=ComputeNodeType.CLOUD_FUNCTION,
                capacity=100,
                current_load=0,
                latency_ms=200,
                cost_per_hour=0.1,
                availability=0.98
            )
        ]
        
        for node in nodes:
            self.load_balancer.register_node(node)
    
    async def inference_on_node(
        self,
        node: ComputeNode,
        model: str,
        input_data: Any,
        timeout_ms: int = 5000
    ) -> Dict[str, Any]:
        """노드에서 추론 실행"""
        try:
            # 시뮬레이션: 실제로는 원격 호출
            await asyncio.sleep(node.latency_ms / 1000)
            
            result = {
                'model': model,
                'node': node.id,
                'latency_ms': node.latency_ms,
                'status': 'success',
                'result': f"Inference result from {node.id}",
                'timestamp': datetime.now().isoformat()
            }
            
            # 비용 계산
            result['cost'] = node.get_cost_per_task(node.latency_ms)
            
            return result
        
        except asyncio.TimeoutError:
            return {
                'status': 'timeout',
                'node': node.id,
                'error': 'Inference timeout'
            }
    
    async def distributed_inference(
        self,
        model: str,
        tasks: List[Any],
        strategy: str = 'balanced'
    ) -> Dict[str, Any]:
        """분산 추론"""
        
        # 작업 생성
        task_list = [{'input': task, 'model': model} for task in tasks]
        
        # 로드 밸런싱
        distribution = self.load_balancer.distribute_load(task_list, strategy)
        
        # 병렬 실행
        inference_tasks = []
        for node_id, node_tasks in distribution.items():
            node = self.load_balancer.nodes[node_id]
            for task in node_tasks:
                inference_tasks.append(
                    self.inference_on_node(node, model, task['input'])
                )
        
        # 모든 작업 완료 대기
        results = await asyncio.gather(*inference_tasks)
        
        # 결과 분석
        successful = sum(1 for r in results if r.get('status') == 'success')
        total_cost = sum(r.get('cost', 0) for r in results)
        avg_latency = sum(r.get('latency_ms', 0) for r in results) / len(results) if results else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'total_tasks': len(tasks),
            'successful': successful,
            'failed': len(tasks) - successful,
            'success_rate': successful / len(tasks) if tasks else 0,
            'total_cost': total_cost,
            'avg_latency_ms': avg_latency,
            'results': results
        }
    
    def get_node_stats(self) -> Dict[str, Any]:
        """노드 통계"""
        stats = {}
        total_capacity = 0
        total_load = 0
        total_cost = 0
        
        for node_id, node in self.load_balancer.nodes.items():
            stats[node_id] = {
                'type': node.node_type.value,
                'utilization': node.get_utilization(),
                'current_load': node.current_load,
                'capacity': node.capacity,
                'latency_ms': node.latency_ms,
                'cost_per_hour': node.cost_per_hour,
                'availability': node.availability
            }
            
            total_capacity += node.capacity
            total_load += node.current_load
            total_cost += node.cost_per_hour
        
        return {
            'nodes': stats,
            'system_utilization': total_load / total_capacity if total_capacity > 0 else 0,
            'total_capacity': total_capacity,
            'total_load': total_load,
            'total_hourly_cost': total_cost
        }
    
    def optimize_configuration(self) -> Dict[str, Any]:
        """구성 최적화 제안"""
        stats = self.get_node_stats()
        
        recommendations = []
        
        # 활용도 분석
        for node_id, node_stats in stats['nodes'].items():
            utilization = node_stats['utilization']
            
            if utilization > 0.8:
                recommendations.append({
                    'node': node_id,
                    'action': 'scale_up',
                    'reason': f"High utilization: {utilization*100:.1f}%"
                })
            elif utilization < 0.2 and node_stats['cost_per_hour'] > 0:
                recommendations.append({
                    'node': node_id,
                    'action': 'scale_down',
                    'reason': f"Low utilization: {utilization*100:.1f}%"
                })
        
        return {
            'recommendations': recommendations,
            'current_stats': stats
        }


if __name__ == "__main__":
    print("🔄 분산 추론 시스템 테스트\n")
    
    system = DistributedInferenceSystem()
    
    # 테스트 작업
    test_tasks = ["input_1", "input_2", "input_3", "input_4", "input_5"]
    
    # 비동기 실행
    import asyncio
    result = asyncio.run(
        system.distributed_inference(
            "gemini_2_5_pro",
            test_tasks,
            strategy='balanced'
        )
    )
    
    print("✅ 분산 추론 완료!")
    print(f"성공: {result['successful']}/{result['total_tasks']}")
    print(f"총 비용: ${result['total_cost']:.4f}")
    print(f"평균 지연: {result['avg_latency_ms']:.0f}ms")
    
    # 노드 통계
    print("\n📊 노드 통계:")
    stats = system.get_node_stats()
    print(f"시스템 활용도: {stats['system_utilization']*100:.1f}%")
