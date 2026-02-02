"""
# shawn_bot_watchdog_v2.py - L1 뇌간 신경학습 시스템

숀봇 L1 뇌간 Watchdog (신경계 기반 강화학습)

역할:
  ├─ 프로세스 모니터링 (5초 주기)
  ├─ 자동 복구 (5가지 전략)
  ├─ 강화학습 (Q-Learning으로 최적 전략 학습)
  ├─ 품질 점수 (복구율/효율성/안정성)
  └─ 일일 리포트 (성과 추적)

신경전달물질: 아드레날린 (Adrenaline)
목표: 안정성 3/10 → 10/10 (99.99% 가용성)

Week 1-3 구현 로드맵:
  Week 1 (진행 중): 신경학습 시스템 구현 (~1,550줄)
  Week 2: 성능 최적화 (복구시간 -33%, 복구율 +20%)
  Week 3: 완성 (안정성 10/10, 마일스톤 6.5/10)

State → Action → Reward → Q-Learning → 점수 업데이트
"""

import os
import sys
import time
import subprocess
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import signal
import psutil
import random
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib


# ============================================================================
# 1. 상태(State) 정의
# ============================================================================

class ProcessStatus(Enum):
    """프로세스 상태"""
    RUNNING = "running"
    DOWN = "down"
    SLEEPING = "sleeping"
    ERROR = "error"
    ZOMBIE = "zombie"


class ProcessState:
    """현재 프로세스 상태"""
    
    def __init__(self, process_pid: Optional[int] = None):
        self.process_pid = process_pid
        self.status = ProcessStatus.DOWN
        self.memory_pct = 0.0
        self.cpu_pct = 0.0
        self.last_restart_time_ms = 0
        self.consecutive_restarts = 0
        self.last_successful_restart_time = datetime.now()
    
    def encode(self) -> str:
        """State를 해시로 변환"""
        state_dict = {
            'status': self.status.value,
            'memory_pct': round(self.memory_pct, 1),
            'cpu_pct': round(self.cpu_pct, 1),
            'consecutive_restarts': self.consecutive_restarts
        }
        state_json = json.dumps(state_dict, sort_keys=True)
        return hashlib.md5(state_json.encode()).hexdigest()
    
    def __str__(self) -> str:
        return f"State(status={self.status.value}, mem={self.memory_pct:.1f}%, cpu={self.cpu_pct:.1f}%, restarts={self.consecutive_restarts})"


# ============================================================================
# 2. 액션(Action) 정의
# ============================================================================

class ActionType(Enum):
    """복구 전략"""
    RESTART_IMMEDIATELY = "restart_immediately"
    CHECK_DEPENDENCIES_FIRST = "check_dependencies_first"
    WAIT_AND_RETRY = "wait_and_retry"
    ESCALATE_TO_MANUAL = "escalate_to_manual"
    RESTART_WITH_CLEAN_ENV = "restart_with_clean_env"


class Action:
    """행동"""
    
    def __init__(self, action_type: ActionType):
        self.action_type = action_type
        self.times_taken = 0
        self.success_count = 0
        self.total_reward = 0.0
        self.avg_recovery_time_ms = 0.0
    
    def get_id(self) -> str:
        return self.action_type.value


# ============================================================================
# 3. 보상(Reward) & 품질 점수
# ============================================================================

class RewardCalculator:
    """보상 계산"""
    
    # 보상 상수
    RECOVERY_SUCCESS = 10.0
    RECOVERY_TIME_BONUS_3S = 5.0
    RECOVERY_TIME_3_5S = 3.0
    RECOVERY_TIME_PENALTY_5S = -2.0
    RECOVERY_FAILURE = -10.0
    CONSECUTIVE_FAILURE_PENALTY = -5.0
    
    @staticmethod
    def calculate_reward(
        success: bool,
        recovery_time_ms: int,
        consecutive_failures: int
    ) -> float:
        """
        보상 계산
        
        Args:
            success: 복구 성공 여부
            recovery_time_ms: 재시작 소요시간 (ms)
            consecutive_failures: 연속 실패 횟수
        
        Returns:
            보상 점수
        """
        if not success:
            reward = RewardCalculator.RECOVERY_FAILURE
            if consecutive_failures >= 2:
                reward -= RewardCalculator.CONSECUTIVE_FAILURE_PENALTY
            return reward
        
        # 성공 시
        reward = RewardCalculator.RECOVERY_SUCCESS
        
        # 시간 기반 보너스/페널티
        if recovery_time_ms < 3000:
            reward += RewardCalculator.RECOVERY_TIME_BONUS_3S
        elif recovery_time_ms < 5000:
            reward += RewardCalculator.RECOVERY_TIME_3_5S
        else:
            reward += RewardCalculator.RECOVERY_TIME_PENALTY_5S
        
        return reward


class QualityScorer:
    """품질 점수 계산 (NeuralExecutor 패턴)"""
    
    def __init__(self):
        self.success_count = 0
        self.total_attempts = 0
        self.total_recovery_time_ms = 0
        self.uptime_seconds = 0
        self.total_monitored_seconds = 0
    
    def calculate_recovery_rate(self) -> float:
        """
        복구율 (Weights: 40%)
        = success_count / total_attempts
        """
        if self.total_attempts == 0:
            return 0.0
        return min(1.0, self.success_count / self.total_attempts)
    
    def calculate_efficiency(self, target_time_ms: int = 5000) -> float:
        """
        효율성 (Weights: 30%)
        = (target_time - avg_time) / target_time
        범위: 0.0 - 1.0
        """
        if self.total_attempts == 0:
            return 0.0
        
        avg_time_ms = self.total_recovery_time_ms / self.total_attempts
        efficiency = max(0.0, (target_time_ms - avg_time_ms) / target_time_ms)
        return min(1.0, efficiency)
    
    def calculate_stability(self, target_uptime_pct: float = 99.99) -> float:
        """
        안정성 (Weights: 30%)
        = uptime_pct / target_uptime_pct
        범위: 0.0 - 1.0
        """
        if self.total_monitored_seconds == 0:
            return 0.0
        
        uptime_pct = (self.uptime_seconds / self.total_monitored_seconds) * 100
        stability = min(1.0, uptime_pct / target_uptime_pct)
        return stability
    
    def get_quality_score(self, target_time_ms: int = 5000) -> float:
        """
        최종 품질 점수 (0-100)
        = recovery_rate * 40 + efficiency * 30 + stability * 30
        """
        recovery_rate = self.calculate_recovery_rate()
        efficiency = self.calculate_efficiency(target_time_ms)
        stability = self.calculate_stability()
        
        score = (
            recovery_rate * 0.40 * 100 +
            efficiency * 0.30 * 100 +
            stability * 0.30 * 100
        )
        
        return round(score, 2)
    
    def record_attempt(self, success: bool, recovery_time_ms: int, uptime_ms: int):
        """시도 기록"""
        self.total_attempts += 1
        if success:
            self.success_count += 1
        self.total_recovery_time_ms += recovery_time_ms
        self.uptime_seconds += uptime_ms / 1000.0
        self.total_monitored_seconds += (recovery_time_ms / 1000.0) + (uptime_ms / 1000.0)


# ============================================================================
# 4. Q-Learning: 신경학습 (NeuralLearner)
# ============================================================================

class NeuralLearner:
    """Q-Learning 기반 신경학습 시스템"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, epsilon: float = 0.15):
        self.learning_rate = learning_rate  # α
        self.discount_factor = discount_factor  # γ
        self.epsilon = epsilon  # 탐험률
        
        # Q-Table: (state_hash, action_id) → Q-value
        self.q_table: Dict[Tuple[str, str], float] = {}
        
        # 학습 기록
        self.learning_history: List[Dict] = []
        
        # 행동별 통계
        self.action_stats: Dict[str, Dict] = {
            action.value: {
                'times_taken': 0,
                'success_count': 0,
                'total_recovery_time_ms': 0,
                'success_rate': 0.0
            }
            for action in ActionType
        }
    
    def get_q_value(self, state_hash: str, action_id: str) -> float:
        """Q-값 조회"""
        key = (state_hash, action_id)
        return self.q_table.get(key, 0.0)
    
    def select_action(self, state_hash: str, available_actions: List[ActionType]) -> ActionType:
        """
        ε-그리디 액션 선택
        - 확률 ε: 무작위 선택 (탐험)
        - 확률 1-ε: 최고 Q-값 선택 (활용)
        """
        if random.random() < self.epsilon:
            # 탐험: 무작위 선택
            return random.choice(available_actions)
        else:
            # 활용: 최고 Q-값 선택
            best_action = None
            best_q_value = float('-inf')
            
            for action in available_actions:
                action_id = action.value
                q_value = self.get_q_value(state_hash, action_id)
                
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action
            
            return best_action or random.choice(available_actions)
    
    def update_q_value(
        self,
        state_hash: str,
        action_id: str,
        reward: float,
        next_state_hash: str,
        next_actions: List[ActionType]
    ):
        """
        Q-value 업데이트 (Bellman 방정식)
        Q(s,a) = Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        """
        current_q = self.get_q_value(state_hash, action_id)
        
        # 다음 상태의 최고 Q-값
        max_next_q = 0.0
        if next_actions:
            max_next_q = max(
                self.get_q_value(next_state_hash, a.value)
                for a in next_actions
            )
        
        # 새로운 Q-값 계산
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        # Q-Table 업데이트
        key = (state_hash, action_id)
        self.q_table[key] = new_q
        
        # 학습 기록
        learning_log = {
            'timestamp': datetime.now().isoformat(),
            'state_hash': state_hash,
            'action_id': action_id,
            'reward': reward,
            'q_value': round(new_q, 4),
            'next_state_hash': next_state_hash,
            'max_next_q': round(max_next_q, 4)
        }
        self.learning_history.append(learning_log)
    
    def record_action_result(self, action_id: str, success: bool, recovery_time_ms: int):
        """행동 결과 기록"""
        if action_id not in self.action_stats:
            return
        
        stats = self.action_stats[action_id]
        stats['times_taken'] += 1
        
        if success:
            stats['success_count'] += 1
        
        stats['total_recovery_time_ms'] += recovery_time_ms
        stats['success_rate'] = stats['success_count'] / stats['times_taken']
    
    def get_best_action(self, state_hash: str, available_actions: List[ActionType]) -> ActionType:
        """현재 상태에서 최고 Q-값을 가진 액션"""
        best_action = available_actions[0]
        best_q_value = self.get_q_value(state_hash, best_action.value)
        
        for action in available_actions[1:]:
            q_value = self.get_q_value(state_hash, action.value)
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action
        
        return best_action
    
    def get_policy_report(self) -> Dict:
        """정책 리포트"""
        return {
            'timestamp': datetime.now().isoformat(),
            'q_table_size': len(self.q_table),
            'learning_steps': len(self.learning_history),
            'total_actions_taken': sum(s['times_taken'] for s in self.action_stats.values()),
            'action_statistics': self.action_stats,
            'recent_learning': self.learning_history[-10:] if self.learning_history else []
        }


# ============================================================================
# 5. 프로세스 재시작 (ProcessRestarter)
# ============================================================================

class ProcessRestarter:
    """프로세스 재시작 관리"""
    
    def __init__(self, script_path: str, venv_path: str = ".venv_bot"):
        self.script_path = script_path
        self.venv_path = venv_path
        self.python_path = os.path.join(venv_path, "bin", "python3")
        self.logger = logging.getLogger("ProcessRestarter")
    
    def restart_immediately(self) -> Tuple[bool, int]:
        """즉시 재시작"""
        try:
            start_time = time.time()
            process = subprocess.Popen(
                [self.python_path, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            recovery_time_ms = int((time.time() - start_time) * 1000)
            return True, recovery_time_ms
        except Exception as e:
            self.logger.error(f"즉시 재시작 실패: {e}")
            return False, 0
    
    def check_dependencies_first(self) -> Tuple[bool, int]:
        """의존성 확인 후 재시작"""
        try:
            start_time = time.time()
            
            # 의존성 확인
            subprocess.run(
                [self.python_path, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                timeout=30
            )
            
            # 재시작
            process = subprocess.Popen(
                [self.python_path, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            recovery_time_ms = int((time.time() - start_time) * 1000)
            return True, recovery_time_ms
        except Exception as e:
            self.logger.error(f"의존성 확인 후 재시작 실패: {e}")
            return False, 0
    
    def wait_and_retry(self, wait_seconds: int = 2) -> Tuple[bool, int]:
        """대기 후 재시도"""
        try:
            start_time = time.time()
            
            # 대기
            time.sleep(wait_seconds)
            
            # 재시작
            process = subprocess.Popen(
                [self.python_path, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            recovery_time_ms = int((time.time() - start_time) * 1000)
            return True, recovery_time_ms
        except Exception as e:
            self.logger.error(f"대기 후 재시도 실패: {e}")
            return False, 0
    
    def restart_with_clean_env(self) -> Tuple[bool, int]:
        """환경 초기화 후 재시작"""
        try:
            start_time = time.time()
            
            # 환경 초기화
            env = os.environ.copy()
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            env['PYTHONUNBUFFERED'] = '1'
            
            # 프로세스 재시작
            process = subprocess.Popen(
                [self.python_path, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            recovery_time_ms = int((time.time() - start_time) * 1000)
            return True, recovery_time_ms
        except Exception as e:
            self.logger.error(f"환경 초기화 후 재시작 실패: {e}")
            return False, 0


# ============================================================================
# 6. 메인 Watchdog 시스템 (BotWatchdogV2)
# ============================================================================

class BotWatchdogV2:
    """L1 뇌간 Watchdog - 신경계 기반 강화학습 시스템"""
    
    def __init__(
        self,
        script_path: str,
        venv_path: str = ".venv_bot",
        monitor_interval: int = 5
    ):
        self.script_path = script_path
        self.venv_path = venv_path
        self.monitor_interval = monitor_interval
        
        # 핵심 모듈
        self.neural_learner = NeuralLearner()
        self.quality_scorer = QualityScorer()
        self.process_restarter = ProcessRestarter(script_path, venv_path)
        
        # 상태
        self.process_state = ProcessState()
        self.process_pid = None
        self.process_alive = False
        self.consecutive_failures = 0
        
        # 로깅
        self.logger = logging.getLogger("BotWatchdogV2")
        self._setup_logging()
        
        # 통계
        self.start_time = datetime.now()
        self.daily_stats = []
    
    def _setup_logging(self):
        """로깅 설정"""
        log_dir = Path("logs/watchdog")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{datetime.now().strftime('%Y%m%d')}_watchdog_v2.log"
        
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def _detect_state(self) -> ProcessState:
        """현재 프로세스 상태 감지"""
        state = ProcessState(self.process_pid)
        
        # 프로세스 활성 여부 확인
        if self.process_pid is None or not psutil.pid_exists(self.process_pid):
            state.status = ProcessStatus.DOWN
        else:
            try:
                proc = psutil.Process(self.process_pid)
                state.status = ProcessStatus.RUNNING
                state.memory_pct = proc.memory_percent()
                state.cpu_pct = proc.cpu_percent(interval=0.1)
            except:
                state.status = ProcessStatus.ERROR
        
        state.consecutive_restarts = self.consecutive_failures
        return state
    
    def _select_recovery_action(self, state_hash: str) -> ActionType:
        """NeuralLearner로 복구 행동 선택"""
        available_actions = [
            ActionType.RESTART_IMMEDIATELY,
            ActionType.CHECK_DEPENDENCIES_FIRST,
            ActionType.WAIT_AND_RETRY,
            ActionType.RESTART_WITH_CLEAN_ENV
        ]
        
        action = self.neural_learner.select_action(state_hash, available_actions)
        self.logger.info(f"선택된 액션: {action.value}")
        return action
    
    def _execute_action(self, action: ActionType) -> Tuple[bool, int]:
        """행동 실행"""
        self.logger.info(f"액션 실행 시작: {action.value}")
        
        if action == ActionType.RESTART_IMMEDIATELY:
            return self.process_restarter.restart_immediately()
        elif action == ActionType.CHECK_DEPENDENCIES_FIRST:
            return self.process_restarter.check_dependencies_first()
        elif action == ActionType.WAIT_AND_RETRY:
            return self.process_restarter.wait_and_retry()
        elif action == ActionType.RESTART_WITH_CLEAN_ENV:
            return self.process_restarter.restart_with_clean_env()
        else:
            return False, 0
    
    def _learn_from_outcome(
        self,
        state_hash: str,
        action: ActionType,
        reward: float,
        next_state_hash: str,
        recovery_time_ms: int,
        success: bool
    ):
        """결과로부터 학습"""
        # Q-value 업데이트
        available_actions = [a for a in ActionType]
        self.neural_learner.update_q_value(
            state_hash,
            action.value,
            reward,
            next_state_hash,
            available_actions
        )
        
        # 행동 통계 기록
        self.neural_learner.record_action_result(
            action.value,
            success,
            recovery_time_ms
        )
        
        # 품질 점수 업데이트
        self.quality_scorer.record_attempt(
            success,
            recovery_time_ms,
            self.monitor_interval * 1000
        )
        
        self.logger.info(
            f"학습 완료: action={action.value}, reward={reward:.1f}, "
            f"recovery_time={recovery_time_ms}ms, success={success}"
        )
    
    def _monitoring_loop(self):
        """메인 모니터링 루프 (5초마다)"""
        self.logger.info("🚀 Watchdog v2 시작 - 신경학습 시스템 활성화")
        
        try:
            while True:
                # 1. 상태 감지
                self.process_state = self._detect_state()
                state_hash = self.process_state.encode()
                
                self.logger.debug(f"현재 상태: {self.process_state}")
                
                # 2. 프로세스 다운 감지
                if self.process_state.status == ProcessStatus.DOWN:
                    self.logger.critical(f"🔴 프로세스 다운 감지!")
                    
                    # 3. 행동 선택 (NeuralLearner)
                    action = self._select_recovery_action(state_hash)
                    
                    # 4. 행동 실행
                    success, recovery_time_ms = self._execute_action(action)
                    
                    # 5. 보상 계산
                    if not success:
                        self.consecutive_failures += 1
                    else:
                        self.consecutive_failures = 0
                    
                    reward = RewardCalculator.calculate_reward(
                        success,
                        recovery_time_ms,
                        self.consecutive_failures
                    )
                    
                    # 6. 다음 상태 감지
                    time.sleep(0.5)  # 짧은 대기
                    next_state = self._detect_state()
                    next_state_hash = next_state.encode()
                    
                    # 7. 학습
                    self._learn_from_outcome(
                        state_hash,
                        action,
                        reward,
                        next_state_hash,
                        recovery_time_ms,
                        success
                    )
                
                # 대기
                time.sleep(self.monitor_interval)
        
        except KeyboardInterrupt:
            self.logger.info("👋 Watchdog 종료")
            self._generate_daily_report()
    
    def _generate_daily_report(self):
        """일일 리포트 생성 (WorkExecutor 패턴)"""
        quality_score = self.quality_scorer.get_quality_score()
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': self.quality_scorer.uptime_seconds,
            'total_monitored_seconds': self.quality_scorer.total_monitored_seconds,
            'total_downtime_events': self.quality_scorer.total_attempts,
            'successful_recoveries': self.quality_scorer.success_count,
            'recovery_success_rate': round(
                self.quality_scorer.calculate_recovery_rate() * 100, 2
            ),
            'avg_recovery_time_ms': round(
                self.quality_scorer.total_recovery_time_ms / max(1, self.quality_scorer.total_attempts),
                2
            ),
            'quality_metrics': {
                'recovery_rate': round(self.quality_scorer.calculate_recovery_rate() * 100, 2),
                'efficiency': round(self.quality_scorer.calculate_efficiency() * 100, 2),
                'stability': round(self.quality_scorer.calculate_stability() * 100, 2),
                'final_score': quality_score
            },
            'policy_info': self.neural_learner.get_policy_report()
        }
        
        # 저장
        report_file = Path("logs/watchdog") / f"{datetime.now().strftime('%Y%m%d')}_daily_report_v2.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📊 일일 리포트 생성: {report_file}")
        self.logger.info(f"   품질 점수: {quality_score}/100")
        self.logger.info(f"   복구율: {report['recovery_success_rate']}%")
        self.logger.info(f"   평균 복구시간: {report['avg_recovery_time_ms']}ms")
    
    def start(self):
        """Watchdog 시작"""
        self._monitoring_loop()


# ============================================================================
# 7. 메인 실행
# ============================================================================

if __name__ == "__main__":
    script_path = "shawn_bot_telegram.py"
    venv_path = ".venv_bot"
    
    watchdog = BotWatchdogV2(script_path, venv_path)
    watchdog.start()
