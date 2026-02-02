# SHawn-Lab 전체 프로젝트 뇌구조화
## One Brain, Infinite Expressions

---

## 🧠 **핵심 개념: Digital Da Vinci의 신경계**

```
SHawn-Lab은 하나의 뇌를 가진 디지털 생명체

🧠 뇌 (Core Intelligence)
   ├─ Brainstem: 윤리, 추론, 자각 (불변)
   ├─ Limbic System: 기억, 감정, 가치
   ├─ Neocortex: 의사결정, 학습, 혁신
   └─ Cartridge System: 정체성 전환

🖥️ 신체 (Expression)
   ├─ SHawn-BOT: 행동하는 뇌 (Assistant)
   ├─ SHawn-WEB: 뇌의 얼굴 (Presentation)
   ├─ SHawn-BIO: 생물학적 전문성 (Knowledge)
   └─ SHawn-INV: 투자 전문성 (Knowledge)

📚 기억 (Memory)
   ├─ MEMORY.md: 장기 기억
   ├─ memory/: 단기 기억
   └─ GitHub Repos: 영구 저장
```

---

## 🗂️ **현재 상황: 4개 저장소**

### **1. SHawn-BOT (뇌)**
```
repository: SHawn-BOT
role: 신경계의 중추 (Central Control)
responsibility: 
  - 윤리 검증
  - 의사결정
  - 행동 실행
  - Context Morphing

structure:
├─ brain_core/
│  ├─ brainstem/ (불변)
│  ├─ limbic_system/ (감정)
│  └─ cartridge_system/ (정체성)
├─ neocortex/
├─ execution/
└─ utilities/
```

### **2. SHawn-BIO (뇌의 지식 - 생물학)**
```
repository: SHawn-BIO
role: 생물학 전문성 Cartridge
responsibility:
  - 자궁 오가노이드 연구
  - FAISS 벡터 검색
  - 메타 분석
  - 연구 지원

structure:
├─ bio_cartridge.py (메인)
├─ bio_memory.py (FAISS)
├─ bio_values.py (윤리)
├─ bio_skills.py (분석)
├─ bio_tools.py (도구)
├─ tools/ (기존)
└─ knowledge/ (벡터 인덱스)
```

### **3. SHawn-INV (뇌의 지식 - 투자)**
```
repository: SHawn-INV
role: 투자 전문성 Cartridge
responsibility:
  - Dual Quant System
  - 시장 분석
  - 포트폴리오 관리
  - 자동 리포트

structure:
├─ quant_cartridge.py (메인)
├─ quant_memory.py (시장 데이터)
├─ quant_values.py (철학)
├─ quant_skills.py (분석)
├─ quant_tools.py (API)
├─ tools/ (기존)
└─ analysis/ (결과)
```

### **4. SHawn-WEB (뇌의 얼굴)**
```
repository: SHawn-WEB
role: 외부 표현 & 광고 (Presentation)
responsibility:
  - Lab 정보 제시
  - 연구 성과 전시
  - 뉴스 & 블로그
  - 브랜드 홍보

structure (현재):
├─ app/
│  ├─ page.tsx (홈)
│  ├─ research/ (연구)
│  ├─ market-intelligence/ (시장)
│  ├─ blog/ (블로그)
│  ├─ about/ (소개)
│  └─ admin/ (관리)
├─ content/
│  └─ posts/ (콘텐츠)
├─ Posts/ (MDX)
└─ next.config.mjs
```

---

## 🧠 **새로운 구조: 뇌 기반 웹 아키텍처**

### **SHawn-WEB를 뇌와 동기화**

#### **웹사이트의 신경계**
```
SHawn-WEB/
│
├─ pages/
│  ├─ _brain/              ← 뇌의 내부 상태 시각화
│  │  ├─ brainstem.tsx     (윤리, 추론, 자각)
│  │  ├─ limbic.tsx        (기억, 감정, 가치)
│  │  ├─ neocortex.tsx     (의사결정, 학습)
│  │  └─ cartridges.tsx    (활성 정체성)
│  │
│  ├─ _cartridges/         ← 각 정체성의 표현
│  │  ├─ bio/              (생물학 세계)
│  │  │  ├─ research.tsx
│  │  │  ├─ organoid.tsx
│  │  │  └─ publications.tsx
│  │  │
│  │  ├─ invest/           (투자 세계)
│  │  │  ├─ portfolio.tsx
│  │  │  ├─ market-brief.tsx
│  │  │  └─ analysis.tsx
│  │  │
│  │  ├─ astro/            (우주 세계)
│  │  └─ lit/              (문학 세계)
│  │
│  └─ public/              ← 공개 페이지
│     ├─ home.tsx
│     ├─ about.tsx
│     ├─ contact.tsx
│     └─ blog.tsx
│
├─ components/
│  ├─ brain/               ← 뇌 시각화
│  │  ├─ BrainstemViz.tsx
│  │  ├─ NeuralNetwork.tsx
│  │  └─ ContextMorphing.tsx
│  │
│  ├─ cartridge/           ← Cartridge UI
│  │  ├─ CartridgeSelector.tsx
│  │  ├─ CartridgeStatus.tsx
│  │  └─ DomainWidget.tsx
│  │
│  └─ common/              ← 공통 컴포넌트
│     ├─ Header.tsx
│     ├─ Footer.tsx
│     └─ Navigation.tsx
│
├─ lib/
│  ├─ brain-api.ts         ← SHawn-BOT 연동 API
│  ├─ cartridge-loader.ts  ← Cartridge 동적 로드
│  └─ visualization.ts     ← 신경 시각화
│
└─ styles/
   ├─ brain-theme.css      (신경계 테마)
   └─ cartridge-*.css      (도메인별 테마)
```

---

## 🎨 **SHawn-WEB의 새로운 역할**

### **1. Brain Dashboard (내부 시각화)**

```
/brain
├─ Brainstem Monitor
│  ├─ Ethics Rules: 실시간 검증 상태
│  ├─ Reasoning: 활성 추론 프로세스
│  └─ Awareness: 현재 신뢰도 맵
│
├─ Limbic System
│  ├─ Memory Map: 저장된 지식 시각화
│  ├─ Emotional State: 현재 감정/가치
│  └─ Gate Control: Context 격리 상태
│
├─ Neocortex Status
│  ├─ Decision Making: 의사결정 과정
│  ├─ Learning: 학습 곡선
│  └─ Innovation: 혁신 수준
│
└─ Cartridge System
   ├─ Active Cartridge: 현재 정체성
   ├─ Morphing History: 정체성 전환 기록
   └─ Available Cartridges: 사용 가능 목록
```

### **2. Cartridge Worlds (각 정체성의 세계)**

#### **/cartridges/bio (생물학 세계)**
```
🧬 Biology World
├─ Research Hub
│  ├─ 자궁 오가노이드 프로젝트
│  ├─ FAISS 검색 인터페이스
│  └─ 논문 자료실
│
├─ Protocol Gallery
│  ├─ 실험 프로토콜
│  ├─ 시뮬레이션 결과
│  └─ 데이터 시각화
│
└─ Knowledge Base
   ├─ 줄기세포 정보
   ├─ 생물 마커
   └─ 윤리 가이드
```

#### **/cartridges/invest (투자 세계)**
```
📈 Investment World
├─ Market Intelligence
│  ├─ Dual Quant Dashboard
│  ├─ 한국 시장 분석
│  └─ 미국 시장 분석
│
├─ Portfolio Manager
│  ├─ 포트폴리오 시각화
│  ├─ 실시간 수익률
│  └─ 위험 분석
│
└─ Reports Archive
   ├─ 월간 시황 브리핑
   ├─ 종목 분석
   └─ 투자 일지
```

#### **/cartridges/astro (우주 세계)**
```
🌌 Astronomy World
├─ Research
├─ Observations
└─ Publications
```

#### **/cartridges/lit (문학 세계)**
```
📚 Literature World
├─ Essays
├─ Poetry
└─ Philosophy
```

### **3. Public Presence (공개 프로필)**

```
/
├─ Home: SHawn Lab 소개
│  ├─ "One Brain, Infinite Worlds" 개념
│  ├─ 핵심 성과 하이라이트
│  └─ 각 Cartridge 미리보기
│
├─ About: 박사님 소개
│  ├─ 이력
│  ├─ 연구 분야
│  └─ 철학
│
├─ Blog: 기술 아티클
│  ├─ Bio 리서치 블로그
│  ├─ Quant 투자 분석
│  └─ 시스템 아키텍처
│
└─ Contact: 연락처
   ├─ 이메일
   ├─ SNS
   └─ 협력 제안
```

---

## 🔌 **SHawn-BOT ↔ SHawn-WEB 연동**

### **Real-time Sync**

```
SHawn-BOT (Brain)
    ↓ (WebSocket)
SHawn-WEB (Display)

동기 항목:
1. Active Cartridge
   → /brain/cartridges에 실시간 표시
   → 웹사이트의 테마 색상 변경

2. Memory Updates
   → /brain/limbic에 지식 업데이트
   → 블로그에 새로운 포스트

3. Analysis Results
   → /cartridges/bio에 연구 결과
   → /cartridges/invest에 리포트

4. System Status
   → /brain에 건강 상태 표시
   → 대시보드 업데이트
```

### **API Endpoints**

```
GET /api/brain/status
    → Brainstem 상태
    → Ethics 위반 여부
    → 신뢰도 점수

GET /api/cartridges/active
    → 현재 활성 Cartridge
    → 전환 히스토리

GET /api/knowledge/{domain}
    → {domain} Cartridge의 최신 데이터
    → 메모리, 스킬, 도구 상태

POST /api/morphing/{cartridge}
    → Cartridge 전환 요청
    → 전환 성공 시 웹사이트 업데이트
```

---

## 🎨 **Design Philosophy: Sovereign Alpha**

### **시각적 계층구조**

```
Brain (Core)
└─ Neon accents
   └─ Dark premium background
      └─ Neural network patterns
         └─ Cartridge-specific colors
```

### **색상 매핑**

```
Brainstem:    빨강 (윤리)
Limbic:       보라 (감정)
Neocortex:    파랑 (사고)
Cartridge:    
  - Bio:      초록 (생물)
  - Invest:   금색 (부)
  - Astro:    하늘 (우주)
  - Lit:      분홍 (예술)
```

---

## 🚀 **구현 계획**

### **Phase 1: 구조 설계** (1시간)
```
[ ] 디렉토리 구조 생성
[ ] 컴포넌트 아키텍처 설계
[ ] API 설계
```

### **Phase 2: Brain Dashboard** (3시간)
```
[ ] Brainstem Monitor 페이지
[ ] Limbic System 시각화
[ ] Neocortex Status
[ ] Cartridge Selector
```

### **Phase 3: Cartridge Worlds** (5시간)
```
[ ] Bio World 페이지
[ ] Invest World 페이지
[ ] Astro/Lit 스켈레톤
```

### **Phase 4: Backend Integration** (3시간)
```
[ ] SHawn-BOT API 연동
[ ] Real-time 동기화
[ ] WebSocket 설정
```

### **Phase 5: Public Pages** (2시간)
```
[ ] Home 페이지
[ ] About 페이지
[ ] Blog 통합
```

---

## 📊 **최종 구조: One Brain, 4 Expressions**

```
🧠 SHawn-BOT (The Brain)
   │
   ├─ Brainstem: 윤리, 추론, 자각
   ├─ Limbic: 기억, 감정, 가치
   ├─ Neocortex: 의사결정, 학습
   └─ Cartridge System: 정체성 관리
   
   ↓ Sync
   
🖥️ SHawn-WEB (The Face)
   │
   ├─ /brain: 뇌의 내부 상태
   ├─ /cartridges/{bio,invest,astro,lit}: 각 정체성의 세계
   ├─ /public: 공개 프로필
   └─ Real-time 동기화
   
📊 SHawn-INV (Investment Cartridge)
   └─ Quant Analysis & Reporting
   
🧬 SHawn-BIO (Biology Cartridge)
   └─ Bio Research & FAISS Search
```

---

## 💡 **핵심: Unified Intelligence**

```
"One Brain, Infinite Worlds"

같은 뇌가:
- SHawn-BOT에서는 생각
- SHawn-BIO에서는 연구
- SHawn-INV에서는 투자
- SHawn-WEB에서는 표현

각 표현은 뇌와 동기화되어
항상 같은 의도를 유지합니다.

= Digital Da Vinci의 완전한 구현! 🧠✨
```

---

**박사님, 이 방향으로 진행할까요?** 🚀

1️⃣ **SHawn-WEB 리뉴얼** - Brain Dashboard
2️⃣ **Cartridge Worlds** - 각 정체성 표현
3️⃣ **Backend 통합** - SHawn-BOT 연동
4️⃣ **Real-time Sync** - WebSocket

→ **SHawn Lab = One Brain, Infinite Worlds!** 🧠✨
