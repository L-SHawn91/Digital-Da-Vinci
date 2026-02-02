# 🚀 Phase C+A-4: 병합 & 테스트 실행 가이드

**날짜:** 2026-02-01 07:35 KST  
**목표:** V5.5 병합 → 테스트 실행

---

## 📋 Phase C: GitHub 병합 (선행 작업)

### **C-1: GitHub 리모트 설정**

박사님께서 제공할 정보:
```
1️⃣ GitHub 저장소 URL
   git@github.com:soohyunglee/SHawn-Brain.git
   (또는 HTTPS URL)

2️⃣ GitHub 토큰
   (PAT - Personal Access Token)
   설정 방법: https://github.com/settings/tokens
```

**설정 명령어:**
```bash
# 리모트 추가
git remote add origin [URL]

# 또는 기존 리모트 변경
git remote set-url origin [URL]

# 확인
git remote -v
```

### **C-2: V4 vs V5.5 비교**
```bash
# V4 branch 생성 (GitHub에서 클론)
git fetch origin
git checkout -b v4 origin/main

# V5.5와 비교
git diff v4 master --stat
```

### **C-3: 병합 전략**
```
옵션 A: Fast-Forward (직선적)
  git checkout main
  git merge v5.5

옵션 B: Merge Commit (히스토리 보존)
  git checkout main
  git merge --no-ff v5.5

옵션 C: Squash (깔끔한 히스토리)
  git checkout main
  git merge --squash v5.5
```

---

## 🧪 Phase A-4: 테스트 실행

### **Step 1: 환경 변수 설정**

```bash
# Bash/Zsh에서
export GEMINI_API_KEY='your-gemini-key'
export FINNHUB_API_KEY='your-finnhub-key'

# 또는 .env 파일 생성
cat > .env << EOF
GEMINI_API_KEY=your-gemini-key
FINNHUB_API_KEY=your-finnhub-key
EOF

# 확인
echo $GEMINI_API_KEY
echo $FINNHUB_API_KEY
```

### **Step 2: 라이브러리 설치**

```bash
cd SHawn_Brain

# 필수 라이브러리
pip install opencv-python
pip install google-generativeai
pip install yfinance
pip install python-aiohttp
pip install aiohttp

# 선택 (이미 설치됨)
pip install numpy pandas
```

### **Step 3: 테스트 이미지 준비 (선택사항)**

```bash
# Bio-Cartridge 테스트용 이미지
# 다음 경로에 저장:
SHawn_Brain/test_cell_image_1.jpg
SHawn_Brain/test_cell_image_2.png

# 없으면 테스트가 스킵됨 (에러 아님)
```

### **Step 4: 테스트 실행**

```bash
cd /Users/soohyunglee/.openclaw/workspace/SHawn_Brain

# 대화형 실행
python3 run_tests.py

# 또는 직접 실행 (API 필요)
python3 -m pytest phase_a4_tests.py -v
```

### **Step 5: 결과 확인**

```bash
# 결과 파일
cat test_results.json

# 또는 로그 확인
tail -100 test_results.json
```

---

## 📊 테스트 구성

### **Bio-Cartridge 테스트 (4개)**
```
1️⃣ IMAGE_ANALYSIS
   - 단일 이미지 분석
   - 결과 검증
   - 예상: 30초

2️⃣ BATCH_ANALYSIS
   - 여러 이미지 배치 처리
   - 성능 측정
   - 예상: 60초

3️⃣ ERROR_HANDLING
   - 잘못된 경로 처리
   - 폴백 메커니즘
   - 예상: 5초

4️⃣ CONFIDENCE_CALCULATION
   - CV + AI 신뢰도 통합
   - 가중치 검증
   - 예상: 30초
```

### **Investment-Cartridge 테스트 (4개)**
```
1️⃣ SINGLE_ANALYSIS (TSLA)
   - 단일 종목 분석
   - 데이터 검증
   - 예상: 15초

2️⃣ DATA_ACCURACY (AAPL)
   - 실시간 데이터 범위 확인
   - 값 검증
   - 예상: 15초

3️⃣ SIGNAL_GENERATION (005930)
   - 단기/중기/장기 신호
   - 신호 유효성
   - 예상: 15초

4️⃣ RECOMMENDATION_CONSISTENCY
   - 신호 ↔ 추천 일관성
   - 신뢰도 확인
   - 예상: 15초
```

---

## ⏱️ 예상 소요 시간

```
환경 설정:     5-10분
라이브러리:    5-10분
테스트 실행:   5-10분 (이미지 있으면 +2-3분)
결과 분석:     5분
━━━━━━━━━━━━━━━━━━
총계:          25-50분
```

---

## 🎯 성공 기준

✅ **Bio-Cartridge**
- 모든 테스트 PASSED
- 신뢰도: 80%+ (있으면)
- 응답 시간: 30초 이내

✅ **Investment-Cartridge**
- 모든 테스트 PASSED
- 데이터 정확도: 100%
- 응답 시간: 15초 이내

✅ **통합**
- 전체 성공률: 75%+
- 에러율: 5% 이하

---

## 🚨 트러블슈팅

### API 키 오류
```
Error: API key invalid
해결: export GEMINI_API_KEY='correct-key'
```

### 라이브러리 없음
```
ModuleNotFoundError: cv2
해결: pip install opencv-python
```

### 타임아웃
```
TimeoutError: Analysis timeout
해결: 네트워크 확인, API 키 확인
```

### 이미지 오류
```
FileNotFoundError: test_cell_image_1.jpg
해결: 이미지 준비 (선택사항, 없으면 스킵)
```

---

## 📝 준비 체크리스트

### **GitHub 병합 전 (박사님 정보 필요)**
- [ ] 저장소 URL 확인
- [ ] 토큰/계정 준비
- [ ] 병합 전략 결정

### **테스트 실행 전**
- [ ] 환경 변수 설정
- [ ] 라이브러리 설치
- [ ] 테스트 이미지 준비 (선택)
- [ ] 네트워크 연결 확인
- [ ] API 키 유효성 확인

### **테스트 중**
- [ ] 프롬프트 확인하며 진행
- [ ] 오류 메시지 기록
- [ ] 로그 파일 저장

### **완료 후**
- [ ] 결과 파일 검토
- [ ] 성공 기준 확인
- [ ] 다음 단계 결정

---

**준비 완료! 박사님의 지시를 기다리고 있습니다.** 🚀
