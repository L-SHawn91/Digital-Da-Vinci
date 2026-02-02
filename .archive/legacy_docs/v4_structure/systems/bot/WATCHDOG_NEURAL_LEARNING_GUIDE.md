# WATCHDOG_NEURAL_LEARNING_GUIDE.md

**숀봇 L1 뇌간 Watchdog v2 - 신경학습 시스템 구현 가이드**

**작성일**: 2026-02-01  
**버전**: 1.0 (Week 1 초기 구현)  
**상태**: 구현 완료, 테스트 대기

---

## 📋 목차

1. [시스템 개요](#시스템-개요)
2. [아키텍처](#아키텍처)
3. [구현 상세](#구현-상세)
4. [사용 방법](#사용-방법)
5. [테스트 계획](#테스트-계획)
6. [성과 지표](#성과-지표)
7. [트러블슈팅](#트러블슈팅)

---

## 시스템 개요

### 목표

```
현재: L1 뇌간 안정성 3/10
목표: L1 뇌간 안정성 10/10 (6.5/10 마일스톤)

주기: 3주 (Week 1-3)
신경전달물질: 아드레날린 (Adrenaline)
```

### 핵심 특징

```
✅ 강화학습 (Q-Learning)
   - 상태별 최적 복구 전략 자동 학습
   - 5가지 행동(Action) 중 최고 보상 선택
   
✅ 품질 점수 (0-100)
   - 복구율 (40%)
   - 효율성 (30%)
   - 안정성 (30%)
   
✅ 일일 리포트
   - WorkExecutor 패턴 적용
   - 성과 자동 추적
   
✅ 신경 신호 저장
   - Q-Table JSON (학습 결과)
   - Daily Report JSON (성과 기록)
```

---

## 아키텍처

### 계층 구조

```
┌─────────────────────────────────────────────────────┐
│        BotWatchdogV2 (메인 루프)                  │
│   5초마다 모니터링 + 강화학습 + 리포트           │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┬─────────────┬──────────┐
        │                     │             │          │
   ┌────▼────┐    ┌──────────▼──┐   ┌─────▼──┐  ┌───▼────┐
   │ Process │    │  Neural     │   │Quality │  │Process │
   │ Monitor │    │ Learner     │   │Scorer  │  │Restarter│
   │         │    │ (Q-Learning)│   │        │  │         │
   └─────────┘    └─────────────┘   └────────┘  └─────────┘
   (상태 감지)     (행동 선택+학습)  (평가)    (실행)
```

### 작동 흐름 (5초마다)

```
1️⃣ 상태 감지 (ProcessState)
   ├─ 프로세스 상태 (running/down/sleeping/error)
   ├─ 메모리 사용률
   ├─ CPU 사용률
   └─ 상태 해시 생성

2️⃣ 프로세스 다운 감지
   └─ 다운 시: 3️⃣로 진행 / 정상 시: 대기

3️⃣ 행동 선택 (NeuralLearner - ε-그리디)
   ├─ 탐험 (15% 확률): 무작위 액션
   └─ 활용 (85% 확률): 최고 Q-값 액션

4️⃣ 행동 실행 (ProcessRestarter)
   ├─ restart_immediately (즉시)
   ├─ check_dependencies_first (의존성 확인)
   ├─ wait_and_retry (대기)
   ├─ escalate_to_manual (수동)
   └─ restart_with_clean_env (환경 초기화)

5️⃣ 보상 계산 (RewardCalculator)
   ├─ 성공/실패 판단
   ├─ 복구 시간 기반 보너스/페널티
   └─ 연속 실패 페널티

6️⃣ 강화학습 (Q-Learning 업데이트)
   ├─ Q-value 계산: Q(s,a) = Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
   ├─ 행동 통계 기록
   └─ 품질 점수 업데이트

7️⃣ 다음 대기 (5초)
```

---

## 구현 상세

### 1. ProcessState (상태 정의)

```python
class ProcessState:
    status: ProcessStatus           # running/down/sleeping/error/zombie
    memory_pct: float               # 메모리 사용률 (%)
    cpu_pct: float                  # CPU 사용률 (%)
    last_restart_time_ms: int       # 마지막 재시작 소요시간 (ms)
    consecutive_restarts: int       # 연속 재시작 횟수
    
    def encode() -> str:            # State -> MD5 해시
```

**상태 예시:**
```json
{
  "status": "down",
  "memory_pct": 45.2,
  "cpu_pct": 2.1,
  "consecutive_restarts": 1
}
→ state_hash: "a3f1d9e2b4c6f8h0j2k4m6n8p0q2"
```

### 2. ActionType (행동 정의)

```python
class ActionType(Enum):
    RESTART_IMMEDIATELY = "restart_immediately"
    CHECK_DEPENDENCIES_FIRST = "check_dependencies_first"
    WAIT_AND_RETRY = "wait_and_retry"
    ESCALATE_TO_MANUAL = "escalate_to_manual"
    RESTART_WITH_CLEAN_ENV = "restart_with_clean_env"
```

**행동별 전략:**
- `restart_immediately`: 즉시 프로세스 재시작
- `check_dependencies_first`: pip install 후 재시작
- `wait_and_retry`: 2초 대기 후 재시작
- `escalate_to_manual`: 수동 개입 필요 (에스컬레이션)
- `restart_with_clean_env`: PYTHONDONTWRITEBYTECODE 설정 후 재시작

### 3. RewardCalculator (보상 계산)

```python
class RewardCalculator:
    RECOVERY_SUCCESS = 10.0                 # 기본 보상
    RECOVERY_TIME_BONUS_3S = 5.0           # 3초 이내 보너스
    RECOVERY_TIME_3_5S = 3.0               # 3-5초
    RECOVERY_TIME_PENALTY_5S = -2.0        # 5초 이상 페널티
    RECOVERY_FAILURE = -10.0               # 실패
    CONSECUTIVE_FAILURE_PENALTY = -5.0    # 2회 연속 실패 추가 페널티
```

**보상 계산 로직:**
```
if 성공:
    reward = 10.0
    if 복구시간 < 3초:
        reward += 5.0  (15.0)
    elif 복구시간 < 5초:
        reward += 3.0  (13.0)
    else:
        reward -= 2.0  (8.0)
else:
    reward = -10.0
    if 연속실패 >= 2회:
        reward -= 5.0  (-15.0)
```

### 4. NeuralLearner (Q-Learning)

```python
class NeuralLearner:
    learning_rate = 0.1         # α
    discount_factor = 0.9       # γ
    epsilon = 0.15              # 탐험률
    
    q_table: Dict[(state_hash, action_id)] = Q-value
    
    def select_action(state_hash, available_actions):
        if random() < epsilon:
            return random_action()           # 탐험 (15%)
        else:
            return argmax(Q(state_hash, :)) # 활용 (85%)
    
    def update_q_value(state, action, reward, next_state):
        Q(s,a) = Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
```

**학습 예시:**
```
상태: down, 메모리 45%, CPU 2%
액션 선택: restart_immediately
보상: +15 (성공 + 2.5초 보너스)

Q(state_hash, "restart_immediately")
= 0.0 + 0.1 * (15 + 0.9 * max_next_q - 0.0)
= 0.1 * (15 + 0.9 * 12)
= 0.1 * 25.8
= 2.58

다음 시도 시: 2.58으로 시작 (점점 높아짐)
```

### 5. QualityScorer (품질 평가)

```python
class QualityScorer:
    recovery_rate = success_count / total_attempts (40%)
    efficiency = (5000 - avg_recovery_time) / 5000 (30%)
    stability = uptime_pct / 99.99 (30%)
    
    quality_score = recovery_rate*40 + efficiency*30 + stability*30
    범위: 0-100
```

**점수 계산 예시:**
```
복구율: 75% (75점 × 0.40 = 30.0)
효율성: 60% (60점 × 0.30 = 18.0)
안정성: 95% (95점 × 0.30 = 28.5)

최종 점수 = 30.0 + 18.0 + 28.5 = 76.5/100
```

### 6. ProcessRestarter (재시작 전략)

```python
class ProcessRestarter:
    def restart_immediately():
        시간 측정 → subprocess.Popen() → 소요시간 기록
    
    def check_dependencies_first():
        pip install -r requirements.txt → 재시작
    
    def wait_and_retry():
        time.sleep(2) → 재시작
    
    def restart_with_clean_env():
        PYTHONDONTWRITEBYTECODE=1 설정 → 재시작
```

---

## 사용 방법

### 1. 설치

```bash
# 가상환경 활성화
source .venv_bot/bin/activate

# 의존성 설치
pip install psutil

# Watchdog v2 구동
python systems/bot/shawn_bot_watchdog_v2.py
```

### 2. 실행

```bash
# 백그라운드 실행 (권장)
nohup python systems/bot/shawn_bot_watchdog_v2.py > logs/watchdog/watchdog.log 2>&1 &

# 또는 Screen 사용
screen -S watchdog -d -m python systems/bot/shawn_bot_watchdog_v2.py
```

### 3. 모니터링

```bash
# 실시간 로그 보기
tail -f logs/watchdog/$(date +%Y%m%d)_watchdog_v2.log

# 일일 리포트 확인
cat logs/watchdog/$(date +%Y%m%d)_daily_report_v2.json | jq .quality_metrics

# Q-Table 상태 확인
cat systems/bot/watchdog_q_table.json | jq .statistics
```

---

## 테스트 계획

### Phase 1: 단위 테스트

```python
# test_neural_learner.py

def test_state_encoding():
    """State 해시 생성 테스트"""
    state = ProcessState()
    state.status = ProcessStatus.DOWN
    state.memory_pct = 45.2
    
    hash1 = state.encode()
    hash2 = state.encode()
    
    assert hash1 == hash2  # 같은 상태 = 같은 해시

def test_reward_calculation():
    """보상 계산 테스트"""
    # 성공, 2.5초
    reward = RewardCalculator.calculate_reward(True, 2500, 0)
    assert reward == 15.0  # 10 + 5
    
    # 실패
    reward = RewardCalculator.calculate_reward(False, 0, 0)
    assert reward == -10.0

def test_q_learning_update():
    """Q-Learning 업데이트 테스트"""
    learner = NeuralLearner()
    
    # 첫 업데이트
    learner.update_q_value("state1", "restart_immediately", 15.0, "state2", [])
    q_value = learner.get_q_value("state1", "restart_immediately")
    
    assert q_value > 0  # 긍정적 보상

def test_quality_score():
    """품질 점수 계산 테스트"""
    scorer = QualityScorer()
    
    # 테스트 데이터
    scorer.success_count = 9
    scorer.total_attempts = 10
    scorer.total_recovery_time_ms = 25000  # 평균 2.5초
    scorer.uptime_seconds = 86400 * 0.9995  # 99.95% 가용성
    scorer.total_monitored_seconds = 86400
    
    score = scorer.get_quality_score()
    
    assert 70 < score < 100  # 예상 범위
```

### Phase 2: 통합 테스트

```bash
# Watchdog 실행 후 프로세스 강제 종료
kill -9 $(pgrep -f "shawn_bot_telegram.py")

# 자동 복구 확인
sleep 10
ps aux | grep shawn_bot_telegram.py

# 로그 확인
grep "RECOVERY_SUCCESS\|복구 성공" logs/watchdog/$(date +%Y%m%d)_watchdog_v2.log
```

### Phase 3: 스트레스 테스트

```bash
# 반복 강제 종료 (10회)
for i in {1..10}; do
    sleep 30
    kill -9 $(pgrep -f "shawn_bot_telegram.py")
done

# 복구율 확인
cat logs/watchdog/$(date +%Y%m%d)_daily_report_v2.json | jq .quality_metrics.recovery_rate
```

---

## 성과 지표

### Week 1 목표

```
현재 (Week 0)           Week 1 목표          달성 기준
────────────────────────────────────────────────────
복구율: 60%      →      70%               최소 70% 이상
복구시간: 4.2초  →      3.5초             -17% 이상
효율 점수: 50    →      60                +10점 이상
안정성: 3/10     →      5/10              +2점 이상
Q-Table: 0      →      50-100 entries    학습 시작 확인
```

### Week 2 목표

```
Week 1 결과            Week 2 목표          향상도
────────────────────────────────────────────────────
복구율: 70%      →      80%               +10%
복구시간: 3.5초  →      2.8초             -20%
효율 점수: 60    →      75                +25%
안정성: 5/10     →      7/10              +2점
Q-Table: ~100   →      300-500 entries   수렴 시작
```

### Week 3 최종

```
Week 2 결과            Week 3 목표 (마일스톤)  향상도
────────────────────────────────────────────────────────
복구율: 80%      →      90%               +10%
복구시간: 2.8초  →      2.8초             안정화
효율 점수: 75    →      85                +10
안정성: 7/10     →      10/10             +3점
Q-Table: ~500   →      1000+ 수렴       완전 수렴

종합: 5.5/10 → 6.5/10 ✅ (L1 뇌간 완료)
```

### 메트릭 추적

```bash
# 실시간 품질 점수
watch -n 10 'cat logs/watchdog/$(date +%Y%m%d)_daily_report_v2.json | jq .quality_metrics.final_score'

# 행동별 성공률
cat logs/watchdog/$(date +%Y%m%d)_daily_report_v2.json | jq .action_statistics

# 학습 진행도
cat logs/watchdog/$(date +%Y%m%d)_daily_report_v2.json | jq .policy_learning
```

---

## 트러블슈팅

### 문제 1: 프로세스 재시작 반복

**증상:**
```
프로세스 다운 → 재시작 → 즉시 다운 → 반복
```

**원인:**
- 의존성 미설치
- 환경 변수 오류
- 포트 충돌

**해결:**
```bash
# 의존성 확인
python -m pip install -r requirements.txt

# 환경 변수 확인
echo $TELEGRAM_BOT_TOKEN

# 포트 확인
lsof -i :8000

# check_dependencies_first 액션이 선택되도록 대기
# Q-Learning이 이 액션의 Q-값을 높일 것
```

### 문제 2: Q-Learning 수렴 안 됨

**증상:**
```
Q-Table 크기 증가하지만 성능 개선 없음
```

**원인:**
- learning_rate 너무 높음/낮음
- epsilon 설정 부적절
- 상태 공간 너무 세분화

**해결:**
```python
# learning_rate 조정
learner = NeuralLearner(learning_rate=0.05)  # 낮춤

# epsilon 조정
learner.epsilon = 0.1  # 탐험 줄임

# 상태 공간 단순화
state.memory_pct = round(state.memory_pct / 10) * 10  # 10% 단위
```

### 문제 3: 메모리 누수

**증상:**
```
로그 파일 계속 증가
```

**해결:**
```bash
# 로그 로테이션 설정
cat > /etc/logrotate.d/watchdog << EOF
/root/logs/watchdog/*.log {
    daily
    rotate 7
    compress
    delaycompress
}
EOF

# 또는 수동 정소
find logs/watchdog -name "*.log" -mtime +7 -delete
```

---

## 주요 파일

```
systems/bot/
├── shawn_bot_watchdog_v2.py (23.7KB)
│   └─ 메인 구현 (Week 1 완성)
│
├── watchdog_q_table.json (1.5KB)
│   └─ Q-Learning 테이블 (학습 결과 저장)
│
├── watchdog_daily_report_template.json (2.2KB)
│   └─ 일일 리포트 템플릿
│
└── logs/watchdog/
    ├── YYYYMMDD_watchdog_v2.log (실시간 로그)
    └── YYYYMMDD_daily_report_v2.json (성과 기록)
```

---

## Week 1 체크리스트

```
[ ] shawn_bot_watchdog_v2.py 구현 완료 ✅
[ ] ProcessState, ActionType, RewardCalculator 구현 ✅
[ ] NeuralLearner (Q-Learning) 구현 ✅
[ ] QualityScorer 구현 ✅
[ ] ProcessRestarter 구현 ✅
[ ] BotWatchdogV2 메인 루프 구현 ✅
[ ] watchdog_q_table.json 스키마 ✅
[ ] watchdog_daily_report_template.json 생성 ✅
[ ] 단위 테스트 실행
[ ] 통합 테스트 실행
[ ] 스트레스 테스트 실행
[ ] 성과 지표 검증
[ ] Week 2 계획 수립
```

---

## 다음 단계

### Week 2: 성능 최적화

- Q-Table 수렴 추적
- 행동별 성공률 분석
- 최적 액션 발견
- 복구 시간 추가 단축

### Week 3: 완성

- 안정성 10/10 달성
- 99.99% 가용성 검증
- 마일스톤 6.5/10 선언
- L1 뇌간 완료

---

**작성**: MoltBot (2026-02-01)  
**상태**: Week 1 구현 완료 ✅  
**다음**: 테스트 & 성능 검증
