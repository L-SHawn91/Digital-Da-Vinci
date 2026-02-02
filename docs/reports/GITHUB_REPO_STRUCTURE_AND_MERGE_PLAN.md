# 🔄 Phase C: GitHub 폴더별 레포 구조 & 병합 전략

**분석 날짜:** 2026-02-01 07:50 KST  
**목표:** 로컬 V5.5를 GitHub 폴더 구조에 병합

---

## 📊 GitHub 현재 구조 (Submodule 기반)

### **SHawn-LAB (메인 통합 저장소)**
```
SHawn-LAB (Root)
├── SHawn-BOT/      → leseichi-max/SHawn-BOT (메인 봇)
├── SHawn-WEB/      → leseichi-max/SHawn-WEB (웹사이트)
├── SHawn-BIO/      → leseichi-max/SHawn-BIO (생물학)
├── SHawn-INV/      → leseichi-max/SHawn-INV (투자)
└── README.md       (전체 구조 설명)
```

**특징:**
- ✅ Submodule 기반 (독립적 레포)
- ✅ 각 폴더는 별도 저장소
- ✅ 중앙 통합 관리

---

## 🏛️ 각 폴더별 레포 분석

### **1️⃣ SHawn-BOT (메인 봇)**
```
폴더: 20개
파일: 367개
크기: 2.8MB
구성:
  • brain_core/ (신경 중추)
  • cartridges/ (4개 카트리지)
  • engines/ (엔진 - 43개)
  • execution/ (실행)
  • neocortex/ (신피질)
  • tests/ (18개 테스트)
  • main.py (메인 파일)
```

**현재 상태:** V4 (프로덕션)

---

### **2️⃣ SHawn-WEB (웹사이트)**
```
폴더: 8개
파일: 107개
크기: 6.2MB
구성:
  • app/ (Next.js 앱)
  • components/ (React 컴포넌트)
  • public/ (정적 파일)
  • Posts/ (블로그 포스트)
  • package.json (Node.js)
```

**현재 상태:** 운영 중 (독립 프로젝트)

---

### **3️⃣ SHawn-BIO (생물학 분석)**
```
폴더: 6개
파일: 8개
크기: 0.0MB
구성:
  • analysis/ (분석 코드)
  • papers/ (논문)
  • concepts/ (개념)
```

**현재 상태:** 초기 단계

---

### **4️⃣ SHawn-INV (투자 분석)**
```
폴더: 5개
파일: 41개
크기: 1.2MB
구성:
  • Dual_Quant_System/ (Quant 시스템)
  • strategies/ (전략)
  • scripts/ (스크립트)
  • reports/ (리포트)
```

**현재 상태:** 개발 중

---

## 🔄 병합 전략

### **옵션 1: SHawn-BOT에 V5.5 통합 (권장)**

**구조:**
```
SHawn-BOT (기존)
├── brain_core/           (기존)
├── cartridges/           (기존)
│   ├── astro_cartridge/  (기존)
│   ├── bio_cartridge/    (기존 v1.0)
│   ├── bio_cartridge_v2.py      ⭐ V5.5에서 추가
│   ├── investment_cartridge_v2.py ⭐ V5.5에서 추가
│   ├── lit_cartridge/    (기존)
│   └── quant_cartridge/  (기존)
├── execution/            (V5.5로 업그레이드)
├── neocortex/            (V5.5로 업그레이드)
├── tests/                (V5.5 테스트 추가)
├── main.py               (V5.5 버전)
├── shawn_bot_telegram.py ⭐ V5.5에서 추가
├── phase_a4_tests.py     ⭐ V5.5에서 추가
└── run_tests.py          ⭐ V5.5에서 추가
```

**장점:**
✅ 단순 (기존 구조 유지)
✅ 기존 운영 스크립트 활용 가능
✅ 테스트 환경 완벽

**단점:**
❌ 파일 충돌 가능성
❌ 히스토리 정리 필요

**진행 방식:**
```
1. GitHub SHawn-BOT 클론
2. 로컬 V5.5를 별도 브랜치로 merge
3. 충돌 해결
4. PR 생성 & 테스트
5. main에 병합
```

---

### **옵션 2: 새 저장소 SHawn-BRAIN 생성 (더 깔끔)**

**구조:**
```
SHawn-LAB (메인)
├── SHawn-BOT/   (기존 V4 유지)
├── SHawn-BRAIN/ ⭐ 새로 추가 (V5.5)
├── SHawn-WEB/
├── SHawn-BIO/
├── SHawn-INV/
└── README.md    (업데이트)
```

**새 레포 구성:**
```
SHawn-BRAIN (V5.5 기반)
├── brain_core/
├── cartridges/
│   ├── bio_cartridge/
│   ├── bio_cartridge_v2.py
│   ├── investment_cartridge_v2.py
│   ├── quant_cartridge/
│   ├── astro_cartridge/
│   └── lit_cartridge/
├── execution/
├── neocortex/
├── utilities/
├── tests/
├── shawn_bot_telegram.py
├── phase_a4_tests.py
├── run_tests.py
├── main.py
└── README.md (V5.5 설명)
```

**장점:**
✅ 구조 깔끔 (충돌 없음)
✅ 히스토리 정리 (신규 시작)
✅ V4/V5.5 병행 가능 (A/B 테스트)
✅ 차이 명확 (비교 용이)

**단점:**
❌ 새 레포 생성 필요
❌ 운영 프로세스 변경
❌ 초기 배포 시간 필요

**진행 방식:**
```
1. GitHub에 SHawn-BRAIN 저장소 생성
2. 로컬 V5.5를 push
3. SHawn-LAB에 submodule 추가
4. Phase A-4 테스트 실행
5. 병행 운영 또는 V4 → V5.5 마이그레이션
```

---

### **옵션 3: 선택적 병합 (혼합)**

**구조:**
```
SHawn-BOT (V4)
├── 기존 구조 유지
└── V5.5의 카트리지만 병합
    ├── cartridges/bio_cartridge_v2.py
    └── cartridges/investment_cartridge_v2.py

별도 보관:
├── SHawn-BRAIN (실험용 - V5.5 전체)
└── 검증 후 SHawn-BOT로 병합
```

**특징:**
✅ 위험 최소화
✅ 단계적 통합
✅ 롤백 용이

---

## 🎯 권장 방안: 옵션 2 (새 저장소)

### **이유:**

1. **구조 명확성**
   - V4는 프로덕션 (안정성)
   - V5.5는 신기술 (혁신성)
   - 명확한 분리 가능

2. **위험 최소화**
   - 기존 V4 운영 영향 없음
   - 충돌 해결 불필요
   - 롤백 용이

3. **병행 테스트 가능**
   - V4와 V5.5 동시 운영
   - 성능 비교 가능
   - 점진적 마이그레이션

4. **미래 확장성**
   - V6, V7 준비 용이
   - 아키텍처 버전 관리 명확

---

## 📋 실행 계획 (Option 2)

### **Phase C-1: 새 저장소 생성 (1시간)**

```bash
# 1. GitHub에 SHawn-BRAIN 저장소 생성
#    (Private, Description: "SHawn-Brain v5.5: Neural Architecture with AI Integration")

# 2. 로컬에서 push
cd /Users/soohyunglee/.openclaw/workspace/SHawn_Brain
git remote add origin https://github.com/leseichi-max/SHawn-BRAIN.git
git branch -M main
git push -u origin main
```

---

### **Phase C-2: SHawn-LAB에 Submodule 추가 (30분)**

```bash
# 1. SHawn-LAB 클론
cd /tmp
git clone https://github.com/leseichi-max/SHawn-LAB.git
cd SHawn-LAB

# 2. submodule 추가
git submodule add https://github.com/leseichi-max/SHawn-BRAIN.git SHawn-BRAIN

# 3. commit & push
git add .gitmodules SHawn-BRAIN
git commit -m "Add SHawn-BRAIN (v5.5) as submodule"
git push origin main
```

---

### **Phase C-3: Phase A-4 테스트 실행 (30-60분)**

```bash
# 환경 설정
export GEMINI_API_KEY='...'
export FINNHUB_API_KEY='...'

# 테스트 실행
cd SHawn_Brain
python3 run_tests.py
```

---

### **Phase C-4: 문서 작성 (30분)**

```
1. SHawn-BRAIN/README.md
   - 프로젝트 소개
   - 아키텍처
   - 설치 가이드
   - 테스트 결과

2. SHawn-LAB/README.md 업데이트
   - SHawn-BRAIN 설명 추가
   - 마이그레이션 정보
```

---

### **Phase C-5: Phase B 시작 (1주)**

```
SHawn-Web 대시보드
  • 모니터링 시스템
  • 신경 활동 시각화
  • 성능 분석
```

---

## 🗺️ GitHub 최종 구조 (Option 2 적용 후)

```
SHawn-LAB (Root)
├── README.md
│   "SHawn Lab 3.2: V4 (Production) + V5.5 (Innovation)"
├── ARCHITECTURE_HISTORY.md
├── .gitmodules
│
├── SHawn-BOT/
│   └── V4 (기존 프로덕션)
│       ├── main.py
│       ├── cartridges/
│       ├── tests/ (18개)
│       └── ...
│
├── SHawn-BRAIN/           ⭐ NEW
│   └── V5.5 (신기술)
│       ├── main.py (개선)
│       ├── cartridges/
│       │   ├── bio_cartridge_v2.py (Gemini)
│       │   └── investment_cartridge_v2.py (Yahoo)
│       ├── tests/ (8개 - Phase A-4)
│       ├── run_tests.py
│       ├── shawn_bot_telegram.py
│       └── phase_a4_tests.py
│
├── SHawn-WEB/
│   └── 웹사이트 (React/Next.js)
│
├── SHawn-BIO/
│   └── 생물학 분석
│
└── SHawn-INV/
    └── 투자 분석
```

---

## ⏱️ 예상 소요 시간

```
Phase C-1: 새 저장소 생성    → 1시간
Phase C-2: Submodule 추가   → 30분
Phase C-3: 테스트 실행      → 1시간
Phase C-4: 문서 작성        → 30분
───────────────────────────────
총계: 약 3시간
```

---

## ✅ 체크리스트

### **준비 단계**
- [ ] GitHub 저장소 생성 권한 확인
- [ ] API 키 준비 (테스트용)
- [ ] 백업 완료

### **Phase C-1: 새 저장소 생성**
- [ ] SHawn-BRAIN 레포 생성
- [ ] 로컬 V5.5 push
- [ ] README.md 작성

### **Phase C-2: Submodule 추가**
- [ ] SHawn-LAB clone
- [ ] Submodule 추가
- [ ] Commit & push

### **Phase C-3: 테스트**
- [ ] 환경 변수 설정
- [ ] run_tests.py 실행
- [ ] 결과 검증

### **Phase C-4: 문서**
- [ ] README 업데이트
- [ ] 마이그레이션 가이드
- [ ] 배포 계획

---

## 🚀 최종 권장안

> **새로운 SHawn-BRAIN 저장소를 생성하여 V5.5를 독립적으로 관리하되,**  
> **SHawn-LAB의 Submodule로 통합 관리하는 것을 권장합니다.**
>
> **이유:**
> 1. V4와 V5.5 병행 운영 가능
> 2. 충돌 최소화 & 명확한 버전 관리
> 3. 단계적 마이그레이션 가능
> 4. 프로덕션 안정성 보장
> 5. 향후 V6+ 준비 용이

---

**박사님의 결정을 기다립니다:**
1. ✅ Option 2 (새 저장소) 진행
2. ❓ Option 1 (SHawn-BOT에 통합)
3. ❓ Option 3 (선택적 병합)
4. ❓ 커스텀 방안
