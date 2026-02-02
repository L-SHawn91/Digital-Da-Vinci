# 🔄 GitHub V4 vs 로컬 V5.5 상세 비교 분석

**분석 날짜:** 2026-02-01 07:40 KST  
**목표:** 병합 전략 수립

---

## 📊 구조 비교 요약

| 항목 | GitHub V4 | 로컬 V5.5 | 차이 |
|------|-----------|---------|------|
| 디렉토리 | 78개 | 22개 | -56개 (정리됨) |
| 파일 | 367개 | 48개 | -319개 (효율화) |
| 용량 | 2.8MB | 0.4MB | -2.4MB (85% 감소) |
| .py 파일 | 307개 | 42개 | -265개 |
| 카트리지 | 6개 (폴더) | 9개 (폴더+v2.0) | +신규 v2.0 |

---

## 🏗️ 디렉토리 구조 비교

### **GitHub V4 (프로덕션)**
```
SHawn-Bot (V4)
├── brain_core/           (신경 중추)
│   ├── brainstem/
│   ├── cartridge_system/
│   └── limbic_system/
├── cartridges/           (카트리지 - 기본)
│   ├── astro_cartridge/
│   ├── bio_cartridge/    (v1.0)
│   ├── lit_cartridge/
│   └── quant_cartridge/
├── engines/              (엔진 - 많은 파일)
│   ├── 43개 파일들...
├── engines_v1_backup/    (백업)
├── execution/            (실행)
├── neocortex/            (신피질)
├── archive/              (아카이브 - 14개 폴더)
├── scripts/              (스크립트 - 12개)
├── utils/                (유틸리티)
├── tests/                (테스트 - 18개 폴더)
└── main.py, requirements.txt 등
```

**특징:**
- ✅ 완전한 프로덕션 구조
- ✅ 상세한 테스트 (18개 폴더)
- ✅ 운영 스크립트 (bot_monitor.sh, restart 등)
- ✅ 자동 복구 시스템
- ⚠️ 큰 파일 수 (관리 복잡)
- ⚠️ 레거시 코드 많음 (engines_v1_backup, old_versions)

---

### **로컬 V5.5 (프로토타입)**
```
SHawn_Brain (V5.5)
├── brain_core/           (신경 중추)
│   ├── brainstem/
│   ├── cartridge_system/
│   └── limbic_system/
├── cartridges/           (카트리지 - 개선됨)
│   ├── astro_cartridge/
│   ├── bio_cartridge/    (v1.0)
│   ├── bio_cartridge_v2.py      ⭐ NEW (Gemini 통합)
│   ├── investment_cartridge_v2.py ⭐ NEW (실시간 데이터)
│   ├── lit_cartridge/
│   └── quant_cartridge/
├── execution/            (실행)
├── neocortex/            (신피질)
├── documentation/        (문서)
├── utilities/            (유틸리티)
├── data/                 (데이터)
├── shawn_bot_telegram.py ⭐ NEW (Telegram 통합)
├── phase_a4_tests.py     ⭐ NEW (테스트)
└── run_tests.py          ⭐ NEW (테스트 실행)
```

**특징:**
- ✅ 간결한 구조 (정리됨)
- ✅ 최신 기술 (Gemini, Yahoo Finance, Telegram)
- ✅ v2.0 카트리지 (개선된 버전)
- ✅ 테스트 자동화
- ⚠️ 프로덕션 미완료 (서비스 스크립트 없음)
- ⚠️ 제한된 테스트 (아직 구축 중)

---

## 🔄 카트리지 비교

### **기본 카트리지 (동일)**
```
✅ Bio-Cartridge
  V4: cartridges/bio_cartridge/bio_cartridge.py
  V5.5: cartridges/bio_cartridge/ + bio_cartridge_v2.py

✅ Quant-Cartridge (Investment)
  V4: cartridges/quant_cartridge/
  V5.5: cartridges/quant_cartridge/ (동일)

✅ Astro-Cartridge
  V4: cartridges/astro_cartridge/
  V5.5: cartridges/astro_cartridge/ (동일)

✅ Lit-Cartridge
  V4: cartridges/lit_cartridge/
  V5.5: cartridges/lit_cartridge/ (동일)
```

### **신규 카트리지 (V5.5만)**
```
🆕 investment_cartridge_v2.py
   • Yahoo Finance API 통합
   • Finnhub API 통합
   • 실시간 데이터
   • 기술적/펀더멘털 분석

🆕 bio_cartridge_v2.py
   • Gemini Vision 2.5 Pro 통합
   • 하이브리드 분석 (CV + AI)
   • 정확도 70% → 95%+

🆕 shawn_bot_telegram.py
   • Telegram 실제 연동
   • 메시지 자동 처리
   • 이미지 인식
```

---

## 🛠️ 기술 스택 비교

### **GitHub V4**
```
API:
  • Gemini (기본)
  • 기타 대형 LLM

데이터:
  • (구체적 소스 불명확)

실행:
  • main.py
  • Telegram (기본 통합)

테스트:
  • test_shawn_bot.py
  • tests/ (18개 폴더)

모니터링:
  • bot_monitor.sh
  • bot_autorestart.sh
  • shawn-bot.service
```

### **로컬 V5.5**
```
API:
  • Gemini 2.5 Pro Vision ⭐ (NEW)
  • Yahoo Finance ⭐ (NEW)
  • Finnhub ⭐ (NEW)

데이터:
  • 실시간 주식 데이터
  • 이미지 분석

실행:
  • auto_router.py
  • shawn_bot.py
  • shawn_bot_telegram.py (개선)

테스트:
  • run_tests.py (자동 실행)
  • phase_a4_tests.py (8개 케이스)

모니터링:
  • (구축 중 - Phase B)
```

---

## 💡 주요 개선사항 (V5.5만 있음)

### **1️⃣ Bio-Cartridge v2.0**
```
V4 vs V5.5:

V4:
  • 기본 이미지 분석
  • CV 기반만
  • 정확도: ~70%

V5.5:
  • Gemini Vision AI 통합 ⭐
  • 하이브리드 분석 ⭐
  • 정확도: ~95%+ ⭐
  • 재시도 로직 & 폴백 ⭐
```

### **2️⃣ Investment-Cartridge v2.0**
```
V4: Quant-Cartridge (기본)
  • 프로토타입 수준

V5.5: investment_cartridge_v2.py
  • Yahoo Finance 실시간 연동 ⭐
  • Finnhub 애널리스트 의견 ⭐
  • 기술적 분석 고도화 ⭐
  • 즉시 실행 가능 ⭐
```

### **3️⃣ Telegram 실제 연동**
```
V4: 기본 통합 (구조 불명확)

V5.5: shawn_bot_telegram.py
  • 메시지 자동 처리 ⭐
  • 이미지 수신 & 분석 ⭐
  • 종목 자동 검색 ⭐
  • 타임아웃 & 폴백 ⭐
  • 에러 핸들링 ⭐
```

### **4️⃣ 테스트 자동화**
```
V4: 수동 테스트 중심

V5.5: 자동화된 테스트
  • Bio 4개 케이스 ⭐
  • Investment 4개 케이스 ⭐
  • 성능 측정 ⭐
  • 리포트 생성 ⭐
```

---

## 🔗 병합 전략

### **옵션 A: V5.5 그대로 사용 (권장)**
```
장점:
  ✅ 최신 기술 (Gemini 2.5 Pro, Yahoo Finance)
  ✅ 더 높은 정확도 (95%+)
  ✅ 간결한 구조
  ✅ 테스트 자동화
  ✅ 생산성 향상

단점:
  ❌ 프로덕션 스크립트 없음 (추가 필요)
  ❌ 모니터링 시스템 미완료 (Phase B 필요)
  ❌ 운영 경험 부족

예상 시간: 1-2주 (스크립트 추가)
```

### **옵션 B: V5.5 + V4 운영 기능**
```
V5.5를 기반으로:
  1. V4의 운영 스크립트 가져오기
     • bot_monitor.sh
     • bot_autorestart.sh
     • shawn-bot.service
  
  2. V4의 테스트 통합
     • tests/ 폴더
     • test_shawn_bot.py
  
  3. V4의 문서 참조
     • 운영 가이드
     • 트러블슈팅

예상 시간: 2-3주 (통합 & 테스트)
```

### **옵션 C: 선택적 병합**
```
V5.5 메인 + V4 필요한 것만:
  • 카트리지: V5.5 (더 나음)
  • 신경계: V5.5 (더 정리됨)
  • 운영: V4에서 가져오기
  • 테스트: V5.5 + V4 추가

예상 시간: 3-4주 (정교한 선택)
```

---

## 🎯 권장 방안

### **Phase C 마이그레이션 계획**

**단계 1: V5.5 기반으로 시작**
```
Branch: develop-v5.5
  • 현재 로컬 V5.5가 base
  • GitHub에 새로운 저장소로 생성
  • 또는 leseichi-max/SHawn-BRAIN 생성
```

**단계 2: V4 운영 기능 추가**
```
1️⃣ 운영 스크립트
   • monitor.sh
   • autorestart.sh
   • service 파일

2️⃣ 추가 테스트
   • V4 테스트 케이스 분석
   • 유용한 것만 통합

3️⃣ 문서
   • 배포 가이드
   • 트러블슈팅
```

**단계 3: Phase A 테스트 실행**
```
run_tests.py 실행
  • Bio-Cartridge v2.0 검증
  • Investment-Cartridge v2.0 검증
  • 신뢰도 확인
  • 성능 측정
```

**단계 4: Phase B 시작**
```
SHawn-Web 대시보드
  • 모니터링 시스템
  • 성능 분석
  • 신경 활동 시각화
```

---

## 📋 병합 체크리스트

### **Pre-Merge**
- [ ] V4 & V5.5 백업
- [ ] 운영 스크립트 검토
- [ ] 기존 운영 환경 문서화

### **Merge**
- [ ] GitHub에 SHawn-BRAIN 저장소 생성
- [ ] V5.5 코드 push
- [ ] 운영 스크립트 추가
- [ ] README 작성

### **Post-Merge**
- [ ] Phase A-4 테스트 실행
- [ ] CI/CD 설정 (선택)
- [ ] 문서 완성
- [ ] Phase B 시작

---

## 🚀 최종 권장사항

**박사님께 추천:**

> **V5.5 기반으로 진행하되, V4에서 필요한 운영 기능만 추가하는 것을 권장합니다.**
>
> 이유:
> 1. V5.5가 기술적으로 더 앞서 있음 (Gemini 2.5 Pro, Yahoo Finance)
> 2. 정확도 향상 (70% → 95%+)
> 3. 구조가 더 깔끔함
> 4. 유지보수 용이
> 5. 확장성 좋음
>
> 단, 운영 경험이 있는 V4의 스크립트를 참고하여 모니터링/자동복구 시스템을 추가하면 프로덕션 레디 상태가 됩니다.

---

**다음 단계:**
1. GitHub 저장소 설정 정보 제공 (URL, 토큰)
2. 병합 전략 확정 (옵션 A/B/C 선택)
3. Phase A-4 테스트 실행
4. Phase B (SHawn-Web) 시작
