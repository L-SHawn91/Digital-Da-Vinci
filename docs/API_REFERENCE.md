# SHawn-Brain API Reference

## 📚 목차

- [개요](#개요)
- [설치](#설치)
- [시작하기](#시작하기)
- [API 엔드포인트](#api-엔드포인트)
- [예제](#예제)
- [배포](#배포)

---

## 개요

**SHawn-Brain**은 Digital Leonardo da Vinci Project의 핵심 API 서버입니다.

### 특징

- 🧠 **D-CNS 신경계**: 4계층 신경 아키텍처
- 🧬 **5개 카트리지**: Bio, Inv, Lit, Quant, Astro
- 🖥️ **REST API**: FastAPI 기반
- 📊 **실시간 모니터링**: WebSocket 스트리밍
- 🚀 **프로덕션 준비**: Docker & Kubernetes

### 기술 스택

- **Backend**: FastAPI + Uvicorn
- **Database**: PostgreSQL + Redis
- **Container**: Docker + Docker Compose
- **API Docs**: Swagger UI + ReDoc

---

## 설치

### 전제 조건

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (프론트엔드)

### 방법 1: Local Development

```bash
# 저장소 클론
git clone https://github.com/yourusername/SHawn-Brain.git
cd SHawn-Brain

# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일 수정 (API 키 등)

# 서버 실행
uvicorn ddc.web.app:app --reload

# 프론트엔드 개발 서버
cd ddc/web/frontend
npm install
npm run dev
```

### 방법 2: Docker

```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f backend

# 서비스 중지
docker-compose down
```

---

## 시작하기

### API 서버 실행

```bash
# 개발 모드
uvicorn ddc.web.app:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
gunicorn ddc.web.app:app -w 4 -b 0.0.0.0:8000
```

### 상태 확인

```bash
# 헬스 체크
curl http://localhost:8000/health

# API 문서
open http://localhost:8000/docs  # Swagger UI
open http://localhost:8000/redoc # ReDoc
```

---

## API 엔드포인트

### 시스템

#### GET `/`
루트 엔드포인트

```bash
curl http://localhost:8000/
```

**응답:**
```json
{
  "name": "SHawn-Brain API",
  "project": "Digital Leonardo da Vinci Project",
  "version": "5.1.0",
  "status": "🟢 Running"
}
```

#### GET `/health`
헬스 체크

```bash
curl http://localhost:8000/health
```

#### GET `/status`
시스템 상태

```bash
curl http://localhost:8000/status
```

### Bio Cartridge

#### POST `/api/bio/analyze_image`
세포/오가노이드 이미지 분석

```bash
curl -X POST http://localhost:8000/api/bio/analyze_image \
  -H "Content-Type: application/json" \
  -d '{
    "image_path": "/path/to/image.jpg",
    "use_neocortex": true
  }'
```

**응답:**
```json
{
  "status": "success",
  "cell_type": "Human ESC",
  "health_status": "healthy",
  "confidence": 0.94,
  "neocortex_features": {
    "occipital_visual": 0.92,
    "temporal_memory": 0.95
  },
  "timestamp": "2026-02-01T10:30:00"
}
```

### Inv Cartridge

#### POST `/api/inv/analyze_stock`
주식 분석

```bash
curl -X POST http://localhost:8000/api/inv/analyze_stock \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "TSLA",
    "use_neocortex": true
  }'
```

**응답:**
```json
{
  "status": "success",
  "ticker": "TSLA",
  "technical_score": 0.85,
  "fundamental_score": 0.78,
  "recommendation": "🟢 BUY",
  "neocortex_decision": {
    "parietal_analysis": 0.88,
    "prefrontal_decision": 0.92
  },
  "timestamp": "2026-02-01T10:30:00"
}
```

### 신경계 모니터링

#### GET `/api/neural/health`
신경계 건강도

```bash
curl http://localhost:8000/api/neural/health
```

#### GET `/api/neural/cartridges`
카트리지 상태

```bash
curl http://localhost:8000/api/neural/cartridges
```

#### WS `/ws/neural_stream`
실시간 신경 신호 스트리밍

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/neural_stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Neural Update:', data);
};
```

---

## 예제

### Python 예제

```python
import requests

# Bio 분석
response = requests.post(
    'http://localhost:8000/api/bio/analyze_image',
    json={
        'image_path': '/path/to/cell.jpg',
        'use_neocortex': True
    }
)
print(response.json())

# Inv 분석
response = requests.post(
    'http://localhost:8000/api/inv/analyze_stock',
    json={
        'ticker': 'TSLA',
        'use_neocortex': True
    }
)
print(response.json())
```

### JavaScript 예제

```javascript
// Bio 분석
const bioResponse = await fetch('http://localhost:8000/api/bio/analyze_image', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    image_path: '/path/to/cell.jpg',
    use_neocortex: true
  })
});

const bioData = await bioResponse.json();
console.log(bioData);

// Inv 분석
const invResponse = await fetch('http://localhost:8000/api/inv/analyze_stock', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ticker: 'TSLA',
    use_neocortex: true
  })
});

const invData = await invResponse.json();
console.log(invData);
```

---

## 배포

### AWS Lambda

```bash
# SAM으로 배포
sam deploy --guided
```

### Vercel (프론트엔드)

```bash
# Vercel CLI로 배포
vercel deploy
```

### Docker Hub

```bash
# 이미지 푸시
docker tag shawn-brain:latest yourusername/shawn-brain:latest
docker push yourusername/shawn-brain:latest
```

### Kubernetes

```bash
# Helm으로 배포
helm install shawn-brain ./helm-chart
```

---

## 지원

- 📧 이메일: support@shawn-brain.com
- 📚 문서: https://docs.shawn-brain.com
- 🐛 이슈: https://github.com/yourusername/SHawn-Brain/issues

---

**버전**: 5.1.0  
**마지막 업데이트**: 2026-02-01
