# FastAPI + React 통합 가이드

**작성**: 2026-02-04  
**상태**: Phase 1 진행 중

---

## 📋 설치 & 실행

### 1️⃣ FastAPI 백엔드 설정

```bash
# 1. 폴더 이동
cd systems/api

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 데이터베이스 초기화
python migrate.py init      # 테이블 생성
python migrate.py seed      # 샘플 데이터 삽입

# 4. 서버 실행
python -m uvicorn main:app --reload --port 8000
```

**결과**:
- ✅ FastAPI 서버: http://localhost:8000
- ✅ Swagger UI: http://localhost:8000/docs
- ✅ ReDoc: http://localhost:8000/redoc

### 2️⃣ React 프론트엔드 설정

```bash
# 1. Node 프로젝트 초기화 (처음 한 번)
npm create vite@latest frontend -- --template react
cd frontend
npm install

# 2. 환경 변수 설정
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# 3. 의존성 추가
npm install axios recharts @reduxjs/toolkit react-redux

# 4. 개발 서버 실행
npm run dev
```

**결과**:
- ✅ React 개발 서버: http://localhost:5173

---

## 🔗 API 통합 확인

### FastAPI 엔드포인트 (17개)

**신경 라우팅**:
```bash
# 신경계 상태 확인
curl http://localhost:8000/api/neural/status

# 모델 목록
curl http://localhost:8000/api/neural/models

# 신경 레벨 정보
curl http://localhost:8000/api/neural/levels

# 작업 라우팅
curl -X POST http://localhost:8000/api/neural/route \
  -H "Content-Type: application/json" \
  -d '{"task": "image_analysis", "priority": "normal"}'
```

**성능 모니터링**:
```bash
# 성능 개요
curl http://localhost:8000/api/performance/overview

# 모델별 성능
curl http://localhost:8000/api/performance/by-model
```

**모델 관리**:
```bash
# 모델 목록
curl http://localhost:8000/api/models

# 특정 모델 상세
curl http://localhost:8000/api/models/0
```

**정책 관리**:
```bash
# 정책 목록
curl http://localhost:8000/api/policies

# 정책 배포
curl -X POST http://localhost:8000/api/policies/deploy \
  -H "Content-Type: application/json" \
  -d '{"policy_id": "policy_001"}'
```

**로그 & 상태**:
```bash
# 실행 로그
curl http://localhost:8000/api/logs?limit=50

# 시스템 상태
curl http://localhost:8000/api/status

# 헬스 체크
curl http://localhost:8000/api/health
```

---

## 🧪 테스트 프로세스

### 1단계: 기본 연결 테스트

```bash
# Terminal 1: FastAPI 시작
cd systems/api
python -m uvicorn main:app --reload

# Terminal 2: API 테스트
curl http://localhost:8000/health
# 예상: {"status": "healthy", "timestamp": "...", "neural_system": "..."}
```

### 2단계: 데이터베이스 확인

```bash
python migrate.py status

# 출력:
# neural_performance: 0 행
# model_metrics: 8 행
# policies: 2 행
# execution_logs: 10 행
# alerts: 0 행
```

### 3단계: React 대시보드 연결

```bash
# Terminal 3: React 개발 서버
cd frontend
npm run dev

# 브라우저에서 http://localhost:5173 열기
```

### 4단계: 데이터 흐름 검증

```
React Dashboard
  ↓
API 호출 (axios)
  ↓
FastAPI 엔드포인트
  ↓
신경계 시스템 (NeuralModelRouter)
  ↓
응답 반환
  ↓
UI 업데이트
```

---

## 📊 기대 결과

### FastAPI 응답 예시

```json
{
  "timestamp": "2026-02-04T12:00:00",
  "neural_levels": {
    "L1": "Groq",
    "L2": "Claude",
    "L3": "Gemini",
    "L4": "DeepSeek"
  },
  "health": "operational",
  "availability": "99.7%",
  "uptime_hours": 4.5
}
```

### React 대시보드 표시

```
┌─────────────────────────────────────┐
│  🧠 SHawn-Brain 신경계 대시보드    │
│  v5.3.0 | 12:00:00                 │
└─────────────────────────────────────┘

[신경 상태 카드 4개]
┌─────┬─────┬─────┬─────┐
│ L1  │ L2  │ L3  │ L4  │
│Groq │Clau │Gemi │Deep │
│     │de   │ni   │Seek │
└─────┴─────┴─────┴─────┘

[성능 메트릭]
가용성:      99.7% ████████░
레이턴시:    1200ms
토큰 효율성: 87%
작동 모델:   8/8

[실시간 로그]
[12:00:00] [neural_router] 신경 라우팅 완료
[12:00:01] [performance] L1 응답 시간: 1200ms
...
```

---

## 🐛 트러블슈팅

### FastAPI 포트 충돌
```bash
# 다른 포트 사용
python -m uvicorn main:app --reload --port 8001
```

### React CORS 에러
```javascript
// .env 파일 확인
REACT_APP_API_URL=http://localhost:8000

// 또는 FastAPI CORS 설정 확인 (main.py)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

### 데이터베이스 에러
```bash
# 데이터베이스 초기화
rm shawn_brain.db
python migrate.py init
python migrate.py seed
```

---

## ✅ 통합 체크리스트

- [ ] FastAPI 서버 실행 (port 8000)
- [ ] React 개발 서버 실행 (port 5173)
- [ ] 데이터베이스 테이블 생성
- [ ] 샘플 데이터 삽입
- [ ] /health 엔드포인트 테스트
- [ ] /api/neural/status 응답 확인
- [ ] React Dashboard 로드 확인
- [ ] 신경 상태 카드 표시 확인
- [ ] 성능 메트릭 표시 확인
- [ ] 실시간 로그 표시 확인

---

## 📈 다음 단계

1. **데이터베이스 실제 데이터 연동**
   - 신경 성능 로그 저장
   - 모델 메트릭 업데이트

2. **추가 API 엔드포인트**
   - Phase 2에서 40+ 엔드포인트 확장

3. **성능 최적화**
   - 캐싱 추가
   - 배치 쿼리 최적화

4. **배포 준비**
   - Docker 컨테이너화
   - Kubernetes 배포

---

**상태**: 통합 가이드 작성 완료 ✅  
**다음**: Phase 1 Day 2 추가 컴포넌트 개발
