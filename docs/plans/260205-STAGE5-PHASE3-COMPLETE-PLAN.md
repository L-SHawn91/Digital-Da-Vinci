# 260205-STAGE5-PHASE3-COMPLETE-PLAN.md - Phase 3 상세 계획서

**날짜**: 2026-02-05  
**단계**: Stage 5 Phase 3 (배포 & CI/CD)  
**예상 소요**: 2-3일  
**예상 라인**: 500줄  

---

## 📋 **Phase 3 목표**

### 🎯 **주요 목표**

1. **Docker 컨테이너화**
   - FastAPI 컨테이너
   - React 컨테이너
   - PostgreSQL 컨테이너
   - Nginx 리버스 프록시

2. **Kubernetes 배포**
   - Pod 설정
   - Service 설정
   - ConfigMap & Secret
   - Ingress 설정

3. **CI/CD 자동화**
   - GitHub Actions 파이프라인
   - 자동 테스트
   - 자동 빌드
   - 자동 배포

4. **모니터링 & 로깅**
   - Prometheus 메트릭
   - Grafana 대시보드
   - ELK 스택 (선택)

---

## 🐳 **Docker (200줄)**

### **1️⃣ FastAPI Dockerfile (60줄)**

```dockerfile
# Dockerfile.api
FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY systems/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 복사
COPY systems/api .

# 포트 노출
EXPOSE 8000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 실행
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**특징**:
- 멀티 스테이지 빌드 (선택)
- 헬스 체크
- 환경 변수 지원
- 비루트 사용자

### **2️⃣ React Dockerfile (50줄)**

```dockerfile
# Dockerfile.web
FROM node:18-alpine AS builder

WORKDIR /app

# 의존성 설치
COPY systems/web/package*.json ./
RUN npm ci

# 빌드
COPY systems/web .
RUN npm run build

# 프로덕션 단계
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**특징**:
- 멀티 스테이지 빌드
- Nginx 리버스 프록시
- 최소 이미지 크기

### **3️⃣ Docker Compose (90줄)**

```yaml
version: '3.8'

services:
  # FastAPI
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/shawn
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    networks:
      - shawn-network

  # React
  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "80:80"
    depends_on:
      - api
    networks:
      - shawn-network

  # PostgreSQL
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=shawn
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - shawn-network

  # Redis
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - shawn-network

volumes:
  postgres-data:

networks:
  shawn-network:
    driver: bridge
```

**특징**:
- 4개 서비스 정의
- 환경 변수 관리
- 볼륨 매핑
- 네트워크 격리

---

## ☸️ **Kubernetes (150줄)**

### **1️⃣ FastAPI Deployment (60줄)**

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shawn-api
  labels:
    app: shawn-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shawn-api
  template:
    metadata:
      labels:
        app: shawn-api
    spec:
      containers:
      - name: api
        image: shawn-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### **2️⃣ Service & Ingress (50줄)**

```yaml
# k8s/api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: shawn-api-service
spec:
  selector:
    app: shawn-api
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shawn-ingress
spec:
  rules:
  - host: api.shawn-brain.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: shawn-api-service
            port:
              number: 80
  - host: app.shawn-brain.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: shawn-web-service
            port:
              number: 80
```

### **3️⃣ ConfigMap & Secret (40줄)**

```yaml
# k8s/config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  redis-url: "redis://cache:6379"
  log-level: "INFO"

---
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  url: "postgresql://user:password@db:5432/shawn"
  user: "user"
  password: "password"
```

---

## 🔄 **GitHub Actions CI/CD (150줄)**

### **1️⃣ 자동 테스트 파이프라인 (70줄)**

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r systems/api/requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest systems/api/tests/ -v --cov
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### **2️⃣ 자동 빌드 & 푸시 (50줄)**

```yaml
# .github/workflows/build.yml
name: Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push API
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.api
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/shawn-api:latest
    
    - name: Build and push Web
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.web
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/shawn-web:latest
```

### **3️⃣ 자동 배포 (30줄)**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Kubernetes
      run: |
        echo ${{ secrets.KUBE_CONFIG }} | base64 -d > kubeconfig
        kubectl --kubeconfig=kubeconfig apply -f k8s/
        kubectl --kubeconfig=kubeconfig rollout status deployment/shawn-api
        kubectl --kubeconfig=kubeconfig rollout status deployment/shawn-web
```

---

## 📊 **모니터링 & 로깅 (100줄)**

### **1️⃣ Prometheus 설정 (50줄)**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'shawn-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  - job_name: 'shawn-db'
    static_configs:
      - targets: ['localhost:5432']
```

### **2️⃣ Grafana 대시보드 (50줄)**

```json
{
  "dashboard": {
    "title": "SHawn-Brain Monitoring",
    "panels": [
      {
        "title": "API Requests/sec",
        "targets": [
          {
            "expr": "rate(http_requests_total[1m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds)"
          }
        ]
      },
      {
        "title": "Database Connections",
        "targets": [
          {
            "expr": "pg_stat_activity_count"
          }
        ]
      },
      {
        "title": "Model Performance",
        "targets": [
          {
            "expr": "model_success_rate"
          }
        ]
      }
    ]
  }
}
```

---

## 📁 **Phase 3 파일 구조**

```
project/
├── Dockerfile.api                (60줄) NEW
├── Dockerfile.web                (50줄) NEW
├── docker-compose.yml            (90줄) NEW
├── nginx.conf                    (30줄) NEW
│
├── k8s/
│   ├── api-deployment.yaml       (60줄) NEW
│   ├── web-deployment.yaml       (60줄) NEW
│   ├── api-service.yaml          (20줄) NEW
│   ├── web-service.yaml          (20줄) NEW
│   ├── ingress.yaml              (30줄) NEW
│   ├── config.yaml               (30줄) NEW
│   └── README.md
│
├── .github/workflows/
│   ├── test.yml                  (70줄) NEW
│   ├── build.yml                 (50줄) NEW
│   └── deploy.yml                (30줄) NEW
│
├── monitoring/
│   ├── prometheus.yml            (50줄) NEW
│   ├── grafana-dashboard.json    (50줄) NEW
│   └── docker-compose-monitor.yml
│
└── DEPLOYMENT_GUIDE.md           (NEW)
```

---

## 🎯 **구현 순서 (우선순위)**

### **Day 1 (1일, 250줄)**

1. **Docker 설정** (100줄)
   - Dockerfile.api
   - Dockerfile.web
   - docker-compose.yml
   - nginx.conf

2. **로컬 테스트** (50줄)
   - Docker build & run
   - 통합 테스트

3. **Kubernetes 기본** (100줄)
   - Deployment
   - Service
   - ConfigMap & Secret

### **Day 2 (1일, 150줄)**

1. **GitHub Actions** (150줄)
   - Test 파이프라인
   - Build & Push
   - Deploy

2. **모니터링** (100줄)
   - Prometheus 설정
   - Grafana 대시보드

3. **문서화**
   - DEPLOYMENT_GUIDE.md

### **Day 3 (0.5일, 100줄)**

1. **통합 테스트**
   - 전체 배포 흐름 테스트
   - 롤백 시나리오

2. **최종 최적화**
   - 이미지 크기 최적화
   - 성능 튜닝

---

## ✅ **배포 체크리스트**

### **로컬 테스트**
- [ ] Docker build 성공
- [ ] docker-compose up 성공
- [ ] http://localhost 접속 가능
- [ ] API & React 모두 작동

### **Kubernetes 설정**
- [ ] kubectl apply 성공
- [ ] Pod 실행 확인
- [ ] Service 연결 확인
- [ ] Ingress 설정 확인

### **CI/CD 자동화**
- [ ] GitHub Actions 트리거 확인
- [ ] 자동 테스트 통과
- [ ] 자동 빌드 성공
- [ ] 자동 배포 성공

### **모니터링**
- [ ] Prometheus 메트릭 수집
- [ ] Grafana 대시보드 표시
- [ ] 알림 설정

---

## 🚀 **배포 프로세스**

### **로컬 개발**
```bash
docker-compose up
# http://localhost
```

### **프로덕션 배포**
```bash
# 1. 태그 생성
git tag v1.0.0

# 2. GitHub에 푸시 (자동 배포 시작)
git push --tags

# 3. Kubernetes에 배포 (자동)
kubectl apply -f k8s/

# 4. 상태 확인
kubectl get pods
kubectl logs -f pod/shawn-api-xxx
```

### **롤백**
```bash
kubectl rollout undo deployment/shawn-api
```

---

## 📊 **예상 성과**

### **라인 수**
- Phase 1: 3,470줄
- Phase 2: 1,500줄 (예상)
- Phase 3: 500줄 (예상)
- 누적: 5,470줄

### **배포 환경**
- 로컬: Docker Compose
- 클라우드: Kubernetes
- CI/CD: GitHub Actions

### **모니터링**
- 메트릭: Prometheus
- 대시보드: Grafana
- 로깅: ELK (선택)

---

## 🎯 **최종 목표**

**2026-02-07까지 Stage 5 완료**
- Phase 1: 웹 대시보드 ✅
- Phase 2: REST API ✅
- Phase 3: 배포 ✅

**프로덕션 배포 준비 완료**
- 프로덕션 환경 설정
- 자동 배포 파이프라인
- 모니터링 & 알림

---

**다음 단계: Phase 2 개발 시작!** 🚀

