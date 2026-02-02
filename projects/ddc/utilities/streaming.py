"""
실시간 데이터 스트리밍 & 처리 - 고속 데이터 파이프라인

역할:
- 실시간 데이터 수집
- 스트림 처리
- 이벤트 기반 분석
- 즉시 알림
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import asyncio
from collections import deque


@dataclass
class StreamEvent:
    """스트림 이벤트"""
    event_id: str
    timestamp: datetime
    source: str
    data: Dict[str, Any]
    priority: int  # 0-10
    processed: bool = False


class RealTimeStreamProcessor:
    """실시간 스트림 처리기"""
    
    def __init__(self, buffer_size: int = 10000):
        self.event_buffer = deque(maxlen=buffer_size)
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.statistics = {
            'total_events': 0,
            'processed_events': 0,
            'dropped_events': 0,
            'avg_latency_ms': 0
        }
        self.latencies = deque(maxlen=1000)
    
    async def subscribe(self, event_type: str, handler: Callable):
        """이벤트 핸들러 등록"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def publish_event(self, event: StreamEvent):
        """이벤트 발행"""
        start_time = datetime.now()
        
        self.event_buffer.append(event)
        self.statistics['total_events'] += 1
        
        # 등록된 핸들러 실행
        handlers = self.event_handlers.get(event.source, [])
        handlers += self.event_handlers.get('*', [])  # 모든 이벤트
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
                
                event.processed = True
                self.statistics['processed_events'] += 1
            
            except Exception as e:
                print(f"Handler error: {e}")
        
        # 지연시간 기록
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        self.latencies.append(latency_ms)
        
        if self.latencies:
            self.statistics['avg_latency_ms'] = sum(self.latencies) / len(self.latencies)
    
    async def process_batch(self, events: List[StreamEvent]) -> Dict[str, Any]:
        """배치 처리"""
        batch_start = datetime.now()
        successful = 0
        failed = 0
        
        for event in events:
            try:
                await self.publish_event(event)
                successful += 1
            except Exception as e:
                failed += 1
                self.statistics['dropped_events'] += 1
        
        batch_duration_ms = (datetime.now() - batch_start).total_seconds() * 1000
        
        return {
            'total': len(events),
            'successful': successful,
            'failed': failed,
            'duration_ms': batch_duration_ms,
            'throughput_events_per_sec': successful / (batch_duration_ms / 1000) if batch_duration_ms > 0 else 0
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계 조회"""
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.statistics,
            'buffer_size': len(self.event_buffer),
            'handlers_count': sum(len(h) for h in self.event_handlers.values())
        }


class EventAggregator:
    """이벤트 집계기"""
    
    def __init__(self, window_size_seconds: int = 60):
        self.window_size_seconds = window_size_seconds
        self.events_by_type: Dict[str, List[StreamEvent]] = {}
        self.aggregations = []
    
    async def aggregate_events(self, events: List[StreamEvent]) -> Dict[str, Any]:
        """이벤트 집계"""
        
        aggregation = {
            'timestamp': datetime.now().isoformat(),
            'window_seconds': self.window_size_seconds,
            'total_events': len(events),
            'by_source': {},
            'by_priority': {},
            'processed_rate': 0
        }
        
        # 소스별 집계
        for event in events:
            if event.source not in aggregation['by_source']:
                aggregation['by_source'][event.source] = 0
            aggregation['by_source'][event.source] += 1
            
            # 우선순위별 집계
            priority_key = f"priority_{event.priority}"
            if priority_key not in aggregation['by_priority']:
                aggregation['by_priority'][priority_key] = 0
            aggregation['by_priority'][priority_key] += 1
        
        # 처리율
        processed = sum(1 for e in events if e.processed)
        aggregation['processed_rate'] = processed / len(events) if events else 0
        
        self.aggregations.append(aggregation)
        
        return aggregation


class AlertSystem:
    """알림 시스템"""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules: List[Dict[str, Any]] = []
    
    def add_alert_rule(
        self,
        name: str,
        condition: Callable,
        severity: str,
        action: Callable
    ):
        """알림 규칙 추가"""
        self.alert_rules.append({
            'name': name,
            'condition': condition,
            'severity': severity,
            'action': action
        })
    
    async def check_and_alert(self, event: StreamEvent) -> Optional[Dict[str, Any]]:
        """알림 확인 & 발송"""
        
        for rule in self.alert_rules:
            if rule['condition'](event):
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'rule_name': rule['name'],
                    'severity': rule['severity'],
                    'event': {
                        'id': event.event_id,
                        'source': event.source,
                        'data': event.data
                    }
                }
                
                self.alerts.append(alert)
                
                # 알림 액션 실행
                if asyncio.iscoroutinefunction(rule['action']):
                    await rule['action'](alert)
                else:
                    rule['action'](alert)
                
                return alert
        
        return None


class DataPipeline:
    """통합 데이터 파이프라인"""
    
    def __init__(self):
        self.stream_processor = RealTimeStreamProcessor()
        self.event_aggregator = EventAggregator()
        self.alert_system = AlertSystem()
        self.pipeline_stats = {
            'start_time': datetime.now(),
            'events_processed': 0,
            'alerts_triggered': 0
        }
    
    async def setup_default_alerts(self):
        """기본 알림 규칙 설정"""
        
        # 높은 우선순위 이벤트
        self.alert_system.add_alert_rule(
            name='high_priority_event',
            condition=lambda e: e.priority >= 8,
            severity='high',
            action=lambda a: print(f"🚨 High priority: {a['rule_name']}")
        )
        
        # 에러 이벤트
        self.alert_system.add_alert_rule(
            name='error_detected',
            condition=lambda e: e.data.get('type') == 'error',
            severity='critical',
            action=lambda a: print(f"❌ Error alert: {a['rule_name']}")
        )
        
        # 성능 저하
        self.alert_system.add_alert_rule(
            name='performance_degradation',
            condition=lambda e: e.data.get('latency_ms', 0) > 1000,
            severity='medium',
            action=lambda a: print(f"⚠️ Performance: {a['rule_name']}")
        )
    
    async def process_stream(self, events: List[StreamEvent]) -> Dict[str, Any]:
        """스트림 처리"""
        
        # 1. 스트림 처리
        processing_result = await self.stream_processor.process_batch(events)
        self.pipeline_stats['events_processed'] += processing_result['successful']
        
        # 2. 이벤트 집계
        aggregation = await self.event_aggregator.aggregate_events(events)
        
        # 3. 알림 확인
        alerts_count = 0
        for event in events:
            alert = await self.alert_system.check_and_alert(event)
            if alert:
                alerts_count += 1
        
        self.pipeline_stats['alerts_triggered'] += alerts_count
        
        return {
            'timestamp': datetime.now().isoformat(),
            'processing': processing_result,
            'aggregation': aggregation,
            'alerts': alerts_count,
            'statistics': self.stream_processor.get_statistics()
        }
    
    def get_pipeline_report(self) -> Dict[str, Any]:
        """파이프라인 리포트"""
        uptime = (datetime.now() - self.pipeline_stats['start_time']).total_seconds()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime,
            'events_processed': self.pipeline_stats['events_processed'],
            'alerts_triggered': self.pipeline_stats['alerts_triggered'],
            'throughput_eps': self.pipeline_stats['events_processed'] / uptime if uptime > 0 else 0,
            'processor': self.stream_processor.get_statistics(),
            'alert_rules': len(self.alert_system.alert_rules)
        }


if __name__ == "__main__":
    print("📡 실시간 스트림 처리 테스트\n")
    
    async def test():
        pipeline = DataPipeline()
        await pipeline.setup_default_alerts()
        
        # 테스트 이벤트
        events = [
            StreamEvent(
                event_id=f"evt_{i}",
                timestamp=datetime.now(),
                source="market_data",
                data={'price': 100 + i, 'volume': 1000 * i, 'type': 'trade'},
                priority=5
            )
            for i in range(100)
        ]
        
        # 몇 개는 높은 우선순위로
        events[10].priority = 9
        events[50].data['type'] = 'error'
        events[75].data['latency_ms'] = 2000
        
        result = await pipeline.process_stream(events)
        
        print("✅ 스트림 처리 완료!")
        print(f"처리된 이벤트: {result['processing']['successful']}")
        print(f"발생한 알림: {result['alerts']}")
        
        report = pipeline.get_pipeline_report()
        print(f"\n✅ 파이프라인 리포트:")
        print(f"총 이벤트: {report['events_processed']}")
        print(f"알림: {report['alerts_triggered']}")
    
    asyncio.run(test())
