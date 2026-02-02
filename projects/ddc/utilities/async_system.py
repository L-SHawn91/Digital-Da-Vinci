"""
비동기 처리 시스템 - 성능 최적화

역할:
- 병렬 카트리지 처리
- 배경 작업 큐
- 우선순위 기반 처리
"""

import asyncio
from typing import Callable, Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class Priority(Enum):
    """우선순위"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


@dataclass
class AsyncTask:
    """비동기 작업"""
    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: Priority = Priority.NORMAL
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class AsyncTaskQueue:
    """비동기 작업 큐"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.queue: List[AsyncTask] = []
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_tasks: List[AsyncTask] = []
    
    def add_task(
        self,
        name: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        priority: Priority = Priority.NORMAL
    ) -> str:
        """작업 추가"""
        import uuid
        
        task_id = str(uuid.uuid4())
        task = AsyncTask(
            id=task_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs or {},
            priority=priority
        )
        
        self.queue.append(task)
        self._sort_queue()
        
        return task_id
    
    def _sort_queue(self) -> None:
        """우선순위에 따라 정렬"""
        self.queue.sort(key=lambda x: x.priority.value)
    
    async def process_queue(self) -> None:
        """큐 처리"""
        while self.queue:
            # 여유 있을 때까지 작업 시작
            while len(self.running_tasks) < self.max_workers and self.queue:
                task = self.queue.pop(0)
                self.running_tasks[task.id] = asyncio.create_task(
                    self._execute_task(task)
                )
            
            # 작업 완료 대기
            if self.running_tasks:
                done, pending = await asyncio.wait(
                    self.running_tasks.values(),
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # 완료된 작업 정리
                for task_future in done:
                    # 작업 ID 찾기
                    task_id = [
                        tid for tid, tfut in self.running_tasks.items()
                        if tfut == task_future
                    ][0]
                    del self.running_tasks[task_id]
    
    async def _execute_task(self, task: AsyncTask) -> None:
        """작업 실행"""
        try:
            task.started_at = datetime.now()
            
            # 동기 함수도 비동기로 처리
            if asyncio.iscoroutinefunction(task.func):
                task.result = await task.func(*task.args, **task.kwargs)
            else:
                task.result = task.func(*task.args, **task.kwargs)
            
            task.completed_at = datetime.now()
        except Exception as e:
            task.error = str(e)
            task.completed_at = datetime.now()
        finally:
            self.completed_tasks.append(task)
    
    def get_status(self) -> Dict[str, Any]:
        """큐 상태"""
        return {
            'queued': len(self.queue),
            'running': len(self.running_tasks),
            'completed': len(self.completed_tasks),
            'max_workers': self.max_workers
        }


class ParallelCartridgeProcessor:
    """병렬 카트리지 처리"""
    
    def __init__(self, cache_manager=None):
        self.cache = cache_manager
        self.queue = AsyncTaskQueue(max_workers=5)
    
    async def process_multiple_cartridges(
        self,
        cartridge_tasks: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """여러 카트리지 병렬 처리"""
        
        for name, task in cartridge_tasks.items():
            self.queue.add_task(
                name=name,
                func=task['func'],
                args=task.get('args', ()),
                kwargs=task.get('kwargs', {}),
                priority=task.get('priority', Priority.NORMAL)
            )
        
        await self.queue.process_queue()
        
        # 결과 수집
        results = {}
        for task in self.queue.completed_tasks:
            if task.error:
                results[task.name] = {'status': 'error', 'error': task.error}
            else:
                results[task.name] = {
                    'status': 'success',
                    'result': task.result,
                    'duration': (task.completed_at - task.started_at).total_seconds()
                }
        
        return results
    
    async def process_neural_layers_parallel(
        self,
        layer_funcs: Dict[str, Callable]
    ) -> Dict[str, Any]:
        """신경계 계층 병렬 처리"""
        
        priority_map = {
            'L1_Brainstem': Priority.URGENT,
            'L2_Limbic': Priority.HIGH,
            'L3_Neocortex': Priority.NORMAL,
            'L4_NeuroNet': Priority.LOW
        }
        
        for level, func in layer_funcs.items():
            self.queue.add_task(
                name=level,
                func=func,
                priority=priority_map.get(level, Priority.NORMAL)
            )
        
        await self.queue.process_queue()
        
        results = {}
        for task in self.queue.completed_tasks:
            results[task.name] = {
                'result': task.result,
                'error': task.error,
                'duration_ms': (task.completed_at - task.started_at).total_seconds() * 1000
            }
        
        return results


class BatchProcessor:
    """배치 처리"""
    
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def process_batch(
        self,
        items: List[Any],
        process_func: Callable
    ) -> List[Any]:
        """배치 처리"""
        results = []
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            # 배치 내 항목 병렬 처리
            tasks = [process_func(item) for item in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        
        return results


# 유틸리티 함수
async def run_async_operations(
    operations: Dict[str, Callable],
    timeout: int = 30
) -> Dict[str, Any]:
    """여러 비동기 작업 동시 실행"""
    try:
        tasks = {
            name: asyncio.create_task(func())
            for name, func in operations.items()
        }
        
        results = await asyncio.wait_for(
            asyncio.gather(*tasks.values()),
            timeout=timeout
        )
        
        return dict(zip(tasks.keys(), results))
    except asyncio.TimeoutError:
        return {'error': f'Timeout after {timeout}s'}


if __name__ == "__main__":
    print("⚡ 비동기 처리 시스템 테스트")
    
    # 테스트 함수
    async def test_task(name: str, duration: float = 1.0):
        await asyncio.sleep(duration)
        return f"{name} 완료"
    
    # 실행
    async def main():
        processor = ParallelCartridgeProcessor()
        
        # 병렬 처리
        results = await run_async_operations({
            'task1': lambda: test_task('작업1', 0.5),
            'task2': lambda: test_task('작업2', 0.5),
            'task3': lambda: test_task('작업3', 0.5)
        })
        
        print(f"결과: {results}")
    
    asyncio.run(main())
