# 260205-STAGE5-PHASE2-COMPLETE-PLAN.md - Phase 2 상세 계획서

**날짜**: 2026-02-05  
**단계**: Stage 5 Phase 2 (REST API 확장)  
**예상 소요**: 2-3일  
**예상 라인**: 1,500줄  

---

## 📋 **Phase 2 목표**

### 🎯 **주요 목표**

1. **40+ REST API 엔드포인트 추가**
   - 신경 라우팅 API 확장
   - 성능 모니터링 API 심화
   - 모델 관리 API 고도화
   - 정책 관리 API 완성
   - 학습 데이터 API 추가
   - 배포/롤백 API

2. **실제 데이터 연동**
   - 데이터베이스 쿼리 최적화
   - 신경계 시스템 실시간 데이터 수집
   - 성능 메트릭 통계 계산

3. **인증 & 보안**
   - JWT 토큰 인증
   - API 키 관리
   - Rate limiting

4. **고급 기능**
   - 배치 작업 API
   - 웹훅 지원
   - 이벤트 스트리밍

---

## 🏗️ **Phase 2 구조 (450줄 추가)**

### **1️⃣ 신경 라우팅 API 확장 (100줄)**

```python
# POST /api/neural/route/batch
# 다중 작업 일괄 라우팅

# GET /api/neural/allocation
# 현재 신경 할당 상태

# POST /api/neural/simulate
# 신경 라우팅 시뮬레이션

# GET /api/neural/history
# 신경 라우팅 이력
```

**특징**:
- 배치 라우팅 (최대 100개 작업)
- 시뮬레이션 모드 (실행 없이 예측)
- 이력 조회 (날짜 범위 필터)
- 통계 요약

### **2️⃣ 성능 모니터링 API 심화 (150줄)**

```python
# GET /api/performance/by-level
# 신경 레벨별 성능

# GET /api/performance/by-model
# 모델별 성능 상세

# GET /api/performance/timeline
# 성능 시계열 데이터

# GET /api/performance/anomalies
# 이상 탐지

# POST /api/performance/baseline
# 성능 기준선 설정
```

**특징**:
- 신경 레벨별 성능 분석
- 모델별 상세 메트릭
- 시계열 데이터 (1시간/1일/1주)
- 자동 이상 탐지
- 기준선 대비 비교

### **3️⃣ 모델 관리 API 고도화 (100줄)**

```python
# GET /api/models/stats
# 모델 통계

# POST /api/models/{id}/test
# 모델 성능 테스트

# GET /api/models/ranking
# 모델 순위

# POST /api/models/compare
# 모델 비교

# GET /api/models/{id}/logs
# 모델별 로그
```

**특징**:
- 모델별 상세 통계
- 성능 테스트 (자동 실행)
- 실시간 순위
- 모델 비교 분석
- 모델별 이벤트 로그

### **4️⃣ 정책 관리 API 완성 (100줄)**

```python
# POST /api/policies/create
# 새 정책 생성

# GET /api/policies/validate
# 정책 검증

# POST /api/policies/{id}/test
# 정책 테스트

# GET /api/policies/history
# 정책 배포 이력

# POST /api/policies/{id}/rollback
# 정책 즉시 롤백
```

**특징**:
- 정책 생성 & 검증
- A/B 테스트 지원
- 배포 이력 추적
- 즉시 롤백 기능
- 성능 비교

### **5️⃣ 학습 데이터 API (50줄)**

```python
# GET /api/learning/metrics
# 강화학습 메트릭

# GET /api/learning/convergence
# 수렴 상태

# POST /api/learning/evaluate
# 정책 평가

# GET /api/learning/replay
# 경험 재생
```

**특징**:
- Q-Learning 메트릭
- 수렴 모니터링
- 정책 성능 평가
- 경험 재생 데이터

### **6️⃣ 배포/롤백 API (50줄)**

```python
# GET /api/deployments
# 배포 이력

# POST /api/deployments/schedule
# 배포 스케줄링

# POST /api/deployments/{id}/cancel
# 배포 취소

# GET /api/deployments/{id}/status
# 배포 상태 조회
```

**특징**:
- 배포 이력 추적
- 스케줄링 배포
- 배포 취소 기능
- 실시간 상태 조회

---

## 🔐 **인증 & 보안 (200줄)**

### **1️⃣ JWT 인증 (80줄)**

```python
# POST /api/auth/login
# 로그인 & 토큰 발급

# POST /api/auth/refresh
# 토큰 갱신

# GET /api/auth/verify
# 토큰 검증

# POST /api/auth/logout
# 로그아웃
```

**특징**:
- JWT 토큰 발급
- Access & Refresh 토큰
- 토큰 자동 갱신
- 만료 시간 관리

### **2️⃣ API 키 관리 (70줄)**

```python
# POST /api/keys/create
# API 키 생성

# GET /api/keys
# API 키 목록

# DELETE /api/keys/{id}
# API 키 삭제

# POST /api/keys/{id}/rotate
# API 키 로테이션
```

**특징**:
- API 키 생성/삭제
- 키 로테이션
- 권한 관리
- 사용 내역 추적

### **3️⃣ Rate Limiting (50줄)**

```python
# 글로벌 Rate Limit: 10,000 req/min
# 사용자별 Rate Limit: 1,000 req/min
# 엔드포인트별 제한 설정

# Header: X-RateLimit-Remaining
# Header: X-RateLimit-Reset
```

---

## 📈 **데이터베이스 쿼리 최적화 (150줄)**

### **1️⃣ 신경 성능 집계 (50줄)**

```python
# 시간대별 성능 집계
# 모델별 성능 집계
# 신경 레벨별 성능 집계
# 인덱스 최적화
```

### **2️⃣ 성능 메트릭 계산 (50줄)**

```python
# 가용성 계산 (% 업타임)
# 레이턴시 통계 (평균, P50, P95, P99)
# 토큰 효율성 계산
# 성공률 계산
```

### **3️⃣ 이상 탐지 (50줄)**

```python
# 표준 편차 기반 이상 탐지
# 이동 평균 활용
# 임계값 기반 경고
# 자동 알림 생성
```

---

## 🔄 **웹훅 & 이벤트 스트리밍 (100줄)**

### **1️⃣ 웹훅 (60줄)**

```python
# POST /api/webhooks
# 웹훅 등록

# DELETE /api/webhooks/{id}
# 웹훅 삭제

# POST /api/webhooks/{id}/test
# 웹훅 테스트

# 이벤트 타입:
#   - neural_route_complete
#   - model_performance_alert
#   - policy_deployed
#   - policy_rolled_back
```

### **2️⃣ 이벤트 스트리밍 (40줄)**

```python
# GET /api/events/stream
# 실시간 이벤트 스트림 (SSE)

# 이벤트:
#   - NeuralRouteEvent
#   - PerformanceEvent
#   - PolicyEvent
#   - AlertEvent
```

---

## 📊 **Phase 2 파일 구조**

```
systems/api/
├── main.py                    (기존)
├── models.py                  (기존)
├── schemas.py                 (기존)
├── migrate.py                 (기존)
├── requirements.txt           (기존)
│
├── routers/
│   ├── __init__.py
│   ├── neural.py              (100줄) NEW
│   ├── performance.py         (150줄) NEW
│   ├── models.py              (100줄) NEW
│   ├── policies.py            (100줄) NEW
│   ├── learning.py            (50줄) NEW
│   └── deployments.py         (50줄) NEW
│
├── auth/
│   ├── __init__.py
│   ├── jwt.py                 (80줄) NEW
│   ├── keys.py                (70줄) NEW
│   └── rate_limit.py          (50줄) NEW
│
├── utils/
│   ├── __init__.py
│   ├── metrics.py             (100줄) NEW
│   ├── anomaly.py             (50줄) NEW
│   ├── webhooks.py            (60줄) NEW
│   └── events.py              (40줄) NEW
│
└── EXPANSION_GUIDE.md         (NEW)
```

---

## 🎯 **구현 순서 (우선순위)**

### **Day 1 (0.5일, 500줄)**

1. **신경 라우팅 API 확장** (100줄)
   - `POST /api/neural/route/batch`
   - `GET /api/neural/allocation`
   - `GET /api/neural/history`

2. **성능 모니터링 API** (150줄)
   - `GET /api/performance/by-level`
   - `GET /api/performance/timeline`
   - `GET /api/performance/anomalies`

3. **모델 관리 API** (100줄)
   - `GET /api/models/stats`
   - `GET /api/models/ranking`
   - `POST /api/models/{id}/test`

4. **JWT 인증** (80줄)
   - Login/Logout
   - Token refresh
   - Token verification

5. **마이그레이션 & 커밋**

### **Day 2 (0.5일, 500줄)**

1. **정책 관리 API** (100줄)
   - Create/Validate/Test
   - History & Rollback

2. **학습 데이터 API** (50줄)
   - Metrics & Convergence
   - Evaluation

3. **배포/롤백 API** (50줄)
   - Schedule & Status
   - Cancel

4. **Rate Limiting** (50줄)
   - Global limits
   - Per-user limits

5. **웹훅 & 이벤트** (100줄)
   - Webhook registration
   - Event streaming (SSE)

6. **데이터베이스 최적화** (100줄)
   - 인덱스 추가
   - 쿼리 최적화

7. **마이그레이션 & 커밋**

### **Day 3 (0.5일, 500줄)**

1. **React 연동**
   - API 호출 업데이트
   - 에러 처리
   - 로딩 상태

2. **통합 테스트**
   - API 엔드포인트 검증
   - 데이터 흐름 확인

3. **문서화**
   - API 명세서
   - 사용 예제

4. **최종 커밋**

---

## 📝 **API 엔드포인트 요약 (40+개)**

### **신경 라우팅 (6개)**
- `GET /api/neural/status`
- `GET /api/neural/models`
- `GET /api/neural/levels`
- `POST /api/neural/route`
- `POST /api/neural/route/batch` ✨
- `GET /api/neural/allocation` ✨
- `GET /api/neural/history` ✨

### **성능 모니터링 (7개)**
- `GET /api/performance/overview`
- `GET /api/performance/by-model`
- `GET /api/performance/by-level` ✨
- `GET /api/performance/timeline` ✨
- `GET /api/performance/anomalies` ✨
- `POST /api/performance/baseline` ✨

### **모델 관리 (6개)**
- `GET /api/models`
- `GET /api/models/{id}`
- `GET /api/models/stats` ✨
- `POST /api/models/{id}/test` ✨
- `GET /api/models/ranking` ✨
- `POST /api/models/compare` ✨

### **정책 관리 (6개)**
- `GET /api/policies`
- `POST /api/policies/deploy`
- `POST /api/policies/create` ✨
- `GET /api/policies/validate` ✨
- `POST /api/policies/{id}/test` ✨
- `POST /api/policies/{id}/rollback` ✨

### **학습 데이터 (4개)**
- `GET /api/learning/metrics` ✨
- `GET /api/learning/convergence` ✨
- `POST /api/learning/evaluate` ✨
- `GET /api/learning/replay` ✨

### **배포/롤백 (4개)**
- `GET /api/deployments` ✨
- `POST /api/deployments/schedule` ✨
- `POST /api/deployments/{id}/cancel` ✨
- `GET /api/deployments/{id}/status` ✨

### **인증 (4개)**
- `POST /api/auth/login` ✨
- `POST /api/auth/refresh` ✨
- `GET /api/auth/verify` ✨
- `POST /api/auth/logout` ✨

### **API 키 (3개)**
- `POST /api/keys/create` ✨
- `GET /api/keys` ✨
- `DELETE /api/keys/{id}` ✨

### **웹훅 (3개)**
- `POST /api/webhooks` ✨
- `DELETE /api/webhooks/{id}` ✨
- `POST /api/webhooks/{id}/test` ✨

### **로그/상태 (3개)**
- `GET /api/logs`
- `GET /api/status`
- `GET / (루트)`

---

## 📊 **예상 성과**

### **라인 수**
- Phase 1: 3,470줄
- Phase 2: 1,500줄 (예상)
- 누적: 4,970줄

### **API 엔드포인트**
- Phase 1: 17개
- Phase 2: +30개 (총 47개)

### **시간**
- 예상: 2-3일
- 현재 속도: 1,410줄/시간
- 필요: 1.1일

### **완성도**
- Phase 1: 100%
- Phase 2: 0% → 100%
- Stage 5: 65% → 95%

---

## ✅ **완료 체크리스트**

### **Day 1**
- [ ] 신경 라우팅 API 확장
- [ ] 성능 모니터링 API 심화
- [ ] 모델 관리 API 고도화
- [ ] JWT 인증 구현
- [ ] 커밋

### **Day 2**
- [ ] 정책 관리 API 완성
- [ ] 학습 데이터 API
- [ ] 배포/롤백 API
- [ ] Rate Limiting
- [ ] 웹훅 & 이벤트
- [ ] DB 최적화
- [ ] 커밋

### **Day 3**
- [ ] React 연동
- [ ] 통합 테스트
- [ ] 문서화
- [ ] 최종 커밋

---

## 🚀 **다음 Phase 미리보기**

### **Phase 3: 배포 (Docker/Kubernetes)**

- Docker 컨테이너화
- Docker Compose
- Kubernetes 설정
- GitHub Actions CI/CD
- 모니터링 (Prometheus/Grafana)

**예상**: 3일, 500줄

---

## 💡 **기술적 결정사항**

### **1. API 라우터 분리**
- 각 도메인별 라우터 (neural, performance, etc)
- 재사용 가능한 구조
- 확장 용이

### **2. JWT vs API Key**
- 사용자 인증: JWT
- 서비스 인증: API Key
- Rate Limiting: 모두 지원

### **3. 웹훅 vs WebSocket**
- 단방향 알림: 웹훅
- 양방향 실시간: 이벤트 스트림 (SSE)
- 비용 효율적

### **4. 데이터베이스 최적화**
- 인덱스 추가
- 쿼리 배치 처리
- 캐싱 (Redis)

---

## 📈 **성능 목표**

- **API 응답 시간**: < 100ms
- **처리량**: 10,000 req/min
- **가용성**: 99.9%
- **에러율**: < 0.1%

---

## 🎯 **최종 목표**

**2026-02-07까지 Phase 2 완료**
- 40+ API 엔드포인트
- 인증 & 보안
- 웹훅 & 이벤트
- React 완전 통합
- Stage 5 총 완성도 95%

---

**준비 완료! 내일 Phase 2 개발 시작!** 🚀
