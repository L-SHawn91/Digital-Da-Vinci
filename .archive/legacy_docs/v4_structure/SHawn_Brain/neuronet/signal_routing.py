"""
신경 신호 라우팅 (Neural Signal Routing)
뇌간 → 변연계 → 신피질 → 신경망 경로 최적화
"""

class NeuralSignalRouter:
    """신경 신호 라우팅"""
    
    def __init__(self):
        self.routes = {}
        self.performance_log = []
    
    async def route_signal(self, signal, context=None):
        """신호를 적절한 뇌 영역으로 라우팅"""
        
        # 1. 신호 특성 분석
        signal_type = self._analyze_signal_type(signal)
        priority = self._calculate_priority(signal)
        complexity = self._assess_complexity(signal)
        
        # 2. 라우팅 경로 결정
        route = self._select_route(signal_type, priority, complexity)
        
        # 3. 병렬 처리 최적화
        parallel_tasks = self._prepare_parallel_tasks(signal, route)
        
        # 4. 신경망 통합
        result = await self._integrate_results(parallel_tasks)
        
        # 5. 학습 기록
        self._log_routing(signal, route, result)
        
        return result
    
    def _analyze_signal_type(self, signal):
        """신호 타입 분석"""
        keywords = {
            "urgent": ["빨리", "지금", "긴급"],
            "emotional": ["기분", "느낌", "감정"],
            "complex": ["분석", "전략", "계획"],
            "simple": ["안녕", "감사", "날씨"]
        }
        
        for signal_type, keywords_list in keywords.items():
            if any(kw in signal for kw in keywords_list):
                return signal_type
        
        return "general"
    
    def _calculate_priority(self, signal):
        """우선순위 계산 (0-100)"""
        base_priority = 50
        
        if "긴급" in signal or "중요" in signal:
            base_priority += 40
        elif "질문" in signal or "분석" in signal:
            base_priority += 20
        elif "안녕" in signal or "감사" in signal:
            base_priority -= 10
        
        return min(100, max(0, base_priority))
    
    def _assess_complexity(self, signal):
        """복잡도 평가 (1-10)"""
        word_count = len(signal.split())
        unique_words = len(set(signal.split()))
        
        complexity = (word_count + unique_words) / 10
        return min(10, max(1, complexity))
    
    def _select_route(self, signal_type, priority, complexity):
        """라우팅 경로 선택"""
        
        if priority >= 80:
            return "brainstem"  # 즉시 처리
        elif signal_type == "emotional":
            return "limbic_system"  # 감정 처리
        elif complexity >= 7:
            return "neocortex"  # 고급 분석
        else:
            return "default"  # 기본 처리
    
    def _prepare_parallel_tasks(self, signal, route):
        """병렬 처리 태스크 준비"""
        
        tasks = {
            "prefrontal": self._analyze_prefrontal(signal),
            "temporal": self._analyze_temporal(signal),
            "parietal": self._analyze_parietal(signal),
            "occipital": self._analyze_occipital(signal)
        }
        
        return tasks
    
    def _analyze_prefrontal(self, signal):
        """전전두엽: 계획 & 의사결정"""
        return {"type": "prefrontal", "analysis": "계획 수립"}
    
    def _analyze_temporal(self, signal):
        """측두엽: 기억 & 맥락"""
        return {"type": "temporal", "analysis": "기억 검색"}
    
    def _analyze_parietal(self, signal):
        """두정엽: 공간 & 통합"""
        return {"type": "parietal", "analysis": "통합 분석"}
    
    def _analyze_occipital(self, signal):
        """후두엽: 시각 & 분석"""
        return {"type": "occipital", "analysis": "시각 처리"}
    
    async def _integrate_results(self, parallel_tasks):
        """결과 통합"""
        integrated = {
            "route": "neuronet",
            "tasks": parallel_tasks,
            "timestamp": datetime.now().isoformat()
        }
        return integrated
    
    def _log_routing(self, signal, route, result):
        """라우팅 기록"""
        log_entry = {
            "signal": signal[:50],
            "route": route,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        self.performance_log.append(log_entry)
