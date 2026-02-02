"""
ExecutionFramework - Motor Cortex의 행동 실행 엔진
행동 실행, 이벤트 핸들링, 외부 API 연결
"""

from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ExecutionState(Enum):
    """실행 상태"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Action:
    """행동"""
    name: str
    target_module: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: float = 0.5
    state: ExecutionState = ExecutionState.PENDING
    timestamp: datetime = field(default_factory=datetime.now)
    result: Optional[str] = None


@dataclass
class Event:
    """이벤트"""
    event_type: str
    source: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    handled: bool = False


class ExecutionFramework:
    """
    행동 실행 프레임워크
    - 행동 실행
    - 이벤트 핸들링
    - 외부 API 연결 (준비)
    - 상태 관리
    """
    
    def __init__(self):
        """실행 프레임워크 초기화"""
        self.actions: List[Action] = []
        self.events: List[Event] = []
        self.action_queue: List[Action] = []
        self.handlers: Dict[str, List[Callable]] = {}
        self.state: Dict[str, Any] = {}
        self.execution_log: List[Dict] = []
    
    def register_handler(
        self,
        event_type: str,
        handler: Callable
    ):
        """이벤트 핸들러 등록"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def create_action(
        self,
        name: str,
        target_module: str,
        parameters: Dict = None,
        priority: float = 0.5
    ) -> Action:
        """행동 생성"""
        action = Action(
            name=name,
            target_module=target_module,
            parameters=parameters or {},
            priority=priority
        )
        self.actions.append(action)
        return action
    
    def queue_action(self, action: Action):
        """행동을 대기열에 추가"""
        self.action_queue.append(action)
        
        # 우선순위로 정렬
        self.action_queue.sort(key=lambda a: a.priority, reverse=True)
    
    def execute_action(self, action: Action) -> Dict:
        """행동 실행"""
        action.state = ExecutionState.RUNNING
        
        try:
            # 타겟 모듈 시뮬레이션
            result_message = f"Executed {action.name} on {action.target_module}"
            
            # 결과 저장
            action.result = result_message
            action.state = ExecutionState.COMPLETED
            
            # 로그
            log_entry = {
                'action': action.name,
                'module': action.target_module,
                'state': action.state.value,
                'timestamp': datetime.now().isoformat(),
                'result': action.result
            }
            self.execution_log.append(log_entry)
            
            return {
                'status': 'success',
                'action': action.name,
                'result': action.result
            }
        
        except Exception as e:
            action.state = ExecutionState.FAILED
            return {
                'status': 'error',
                'action': action.name,
                'error': str(e)
            }
    
    def process_queue(self) -> List[Dict]:
        """대기열 처리"""
        results = []
        
        while self.action_queue:
            action = self.action_queue.pop(0)
            result = self.execute_action(action)
            results.append(result)
        
        return results
    
    def emit_event(
        self,
        event_type: str,
        source: str,
        data: Dict = None
    ) -> Event:
        """이벤트 발행"""
        event = Event(
            event_type=event_type,
            source=source,
            data=data or {}
        )
        self.events.append(event)
        
        # 핸들러 호출
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(event)
                    event.handled = True
                except Exception as e:
                    print(f"Handler error: {e}")
        
        return event
    
    def update_state(self, key: str, value: Any):
        """상태 업데이트"""
        self.state[key] = value
    
    def get_state(self) -> Dict:
        """현재 상태 조회"""
        return {
            'current_state': self.state.copy(),
            'pending_actions': len([a for a in self.actions if a.state == ExecutionState.PENDING]),
            'completed_actions': len([a for a in self.actions if a.state == ExecutionState.COMPLETED]),
            'failed_actions': len([a for a in self.actions if a.state == ExecutionState.FAILED]),
            'total_events': len(self.events),
            'handled_events': len([e for e in self.events if e.handled])
        }
    
    def get_execution_report(self) -> Dict:
        """실행 보고서"""
        return {
            'total_actions': len(self.actions),
            'completed': len([a for a in self.actions if a.state == ExecutionState.COMPLETED]),
            'failed': len([a for a in self.actions if a.state == ExecutionState.FAILED]),
            'pending': len([a for a in self.actions if a.state == ExecutionState.PENDING]),
            'success_rate': self._calculate_success_rate(),
            'total_events': len(self.events),
            'log_entries': len(self.execution_log)
        }
    
    def _calculate_success_rate(self) -> float:
        """성공률 계산"""
        completed = len([a for a in self.actions if a.state == ExecutionState.COMPLETED])
        total = len([a for a in self.actions if a.state in [ExecutionState.COMPLETED, ExecutionState.FAILED]])
        
        if total == 0:
            return 0.0
        
        return completed / total


# 테스트
if __name__ == "__main__":
    framework = ExecutionFramework()
    
    print("🧪 ExecutionFramework Test\n")
    
    # 1. 이벤트 핸들러 등록
    print("1️⃣ Registering event handler:")
    def on_research_complete(event):
        print(f"  Event handled: {event.event_type}")
    
    framework.register_handler("research_complete", on_research_complete)
    print("  ✅ Handler registered")
    
    # 2. 행동 생성 및 큐에 추가
    print("\n2️⃣ Creating and queueing actions:")
    action1 = framework.create_action(
        name="Analyze Data",
        target_module="biology",
        priority=0.8
    )
    framework.queue_action(action1)
    print(f"  ✅ Action queued: {action1.name}")
    
    # 3. 큐 처리
    print("\n3️⃣ Processing action queue:")
    results = framework.process_queue()
    print(f"  ✅ {len(results)} action(s) executed")
    
    # 4. 이벤트 발행
    print("\n4️⃣ Emitting event:")
    event = framework.emit_event(
        event_type="research_complete",
        source="biology_module",
        data={"status": "success"}
    )
    print(f"  ✅ Event emitted and handled: {event.handled}")
    
    # 5. 보고서
    print("\n5️⃣ Execution Report:")
    report = framework.get_execution_report()
    print(f"  Completed: {report['completed']}/{report['total_actions']}")
    print(f"  Success rate: {report['success_rate']:.0%}")
    
    print("\n✅ ExecutionFramework working!")
