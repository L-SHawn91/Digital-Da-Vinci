# 📋 파일 분류 및 Obsidian 연동 규칙

## 🎯 3가지 파일 타입 정의

### 1️⃣ **일지 (Project Log)** 📝
**정의**: 프로젝트/Stage 작성할 때마다 진행 중인 작업의 실시간 기록

특징:
- 프로젝트 단위 시간순 기록
- 어떤 일이 일어났는가
- 오류, 발견사항, 메모
- 시간 스탬프 포함

파일명: `260201-STAGE4-PROJECT-LOG.md` (프로젝트명 포함)
위치: `/memory/logs/`
Obsidian: `50-Lab/SHawn-Brain-Lab/Projects/260201-Stage4-Log.md`
**빈도**: 프로젝트/Stage 작성할 때마다 (매일 아님)

내용 예시:
```
# 260201 Daily Log

## 08:00 - 신경계 10개 모델 통합 시작
- 환경변수 검토: 완료
- 모델 레지스트리 업데이트: 진행 중

## 10:30 - 이슈 발생
- NeuralExecutor 임포트 에러
- 수정: neural_model_registry.json 경로 확인

## 12:00 - Daily Allocator 완성
- 318줄 코드 작성
- 4가지 시간대 로직 구현
```

---

### 2️⃣ **결과 리포트 (Result Report)** ✅
**정의**: 프로젝트/Stage 완료 후 최종 성과 정리

특징:
- 목표 vs 실제 성과 비교
- 통계, 메트릭, 수치
- Before/After
- 결론 및 배운점

파일명: `260201-STAGE4-COMPLETION-REPORT.md`
위치: `/docs/reports/`
Obsidian: `50-Lab/SHawn-Brain-Lab/Reports/260201-Stage4-Completion.md`

내용 예시:
```
# Stage 4 완료 리포트

## 목표
- Step 1,2,3 완성
- 신경 할당 자동화
- 작업 추적 통합

## 성과
✅ daily_allocator.py (318줄)
✅ neural_executor.py (374줄)
✅ work_executor.py (354줄)

## 통계
- 총 신규 코드: 1,046줄
- 총 용량: 34.7KB
- 구현 시간: 2시간 30분

## 배운점
- TimeOfDay 분석의 효율성
- 신경계 기반 라우팅의 안정성
```

---

### 3️⃣ **계획서 (Plan Document)** 📐
**정의**: 다음 단계/프로젝트의 상세 계획

특징:
- 목표, 일정, 예상 비용
- 단계별 상세 계획
- 성공 기준
- 위험 요소 및 대응

파일명: `260202-STAGE4-STEP4-PLAN.md`
위치: `/docs/plans/`
Obsidian: `10-Projects/SHawn-Brain/Plans/260202-Stage4-Step4-Plan.md`

내용 예시:
```
# Stage 4 Step 4 계획서 (2026-02-02)

## 목표
- 성능 모니터링 시스템 구축
- 폴백 메커니즘 구현
- 99%+ 가용성 보장

## 일정
- 08:00-09:00: performance_monitor.py (1시간)
- 09:00-11:00: fallback_manager.py (2시간)
- 11:00-12:00: circuit_breaker.py (1시간)

## 예상 비용
- 토큰: ~1500개
- 금액: ~$0.05
```

---

## 📁 파일 구조 및 Obsidian 매핑

```
workspace/
├── memory/
│   ├── logs/                          ← 프로젝트별 일지 저장
│   │   ├── 260201-STAGE4-PROJECT-LOG.md
│   │   ├── 260202-STAGE5-PROJECT-LOG.md
│   │   └── ...
│   └── MEMORY.md                      ← 장기 메모리
│
├── docs/
│   ├── reports/                       ← 결과 리포트
│   │   ├── 260201-STAGE4-COMPLETION-REPORT.md
│   │   ├── 260202-PERFORMANCE-ANALYSIS.md
│   │   └── ...
│   │
│   └── plans/                         ← 계획서
│       ├── 260202-STAGE4-STEP4-PLAN.md
│       ├── 260203-STAGE5-PLAN.md
│       └── ...
│
└── MEMORY.md                          ← 핵심 요약

Obsidian (SHawn-Brain-Lab):
├── 50-Lab/SHawn-Brain-Lab/
│   ├── Projects/                      ← 프로젝트별 일지
│   │   ├── 260201-Stage4-Log.md
│   │   ├── 260202-Stage5-Log.md
│   │   └── ...
│   │
│   ├── Reports/                       ← 완료 리포트
│   │   ├── 260201-Stage4-Completion.md
│   │   ├── 260202-Performance-Analysis.md
│   │   └── ...
│   │
│   └── ...
│
├── 10-Projects/SHawn-Brain/
│   ├── Plans/                         ← 다음 단계 계획
│   │   ├── 260202-Stage4-Step4-Plan.md
│   │   ├── 260203-Stage5-Plan.md
│   │   └── ...
│   │
│   └── ...
```

---

## 🔄 워크플로우

### **프로젝트/Stage 시작**
```
1. 계획서 작성 (혹은 기존 계획 확인)
   ↓
2. 작업 진행
   ↓
3. 프로젝트/Stage 완료 후
   - 일지 작성 (해당 프로젝트의 작업 기록)
   - 결과 리포트 작성 (성과 정리)
   - 다음 단계 계획서 작성
```

---

## 📝 파일명 규칙

### 일지 (프로젝트 단위)
```
260201-STAGE4-PROJECT-LOG.md
260202-STAGE5-PROJECT-LOG.md
260202-STAGE4-STEP4-PROJECT-LOG.md
```

### 리포트 (Stage/프로젝트 완료)
```
260201-STAGE4-COMPLETION-REPORT.md          (주요 리포트)
260201-PERFORMANCE-ANALYSIS.md              (성능 분석)
260201-COST-ANALYSIS.md                     (비용 분석)
260201-NEURAL-SYSTEM-EFFICIENCY-REPORT.md   (효율 분석)
```

### 계획서 (다음 단계)
```
260202-STAGE4-STEP4-PLAN.md                 (상세 계획)
260203-STAGE5-PLAN.md                       (다음 Stage)
260301-PHASE-B-PLAN.md                      (장기 계획)
```

---

## 🔗 Obsidian 연동

### 매일 저녁 자동 동기화
```bash
# 일지 동기화
cp memory/logs/260201-DAILY-LOG.md \
   /Obsidian/SHawn/50-Lab/SHawn-Brain-Lab/2026-02/

# 리포트 동기화 (주 1회)
cp docs/reports/*.md \
   /Obsidian/SHawn/50-Lab/SHawn-Brain-Lab/Reports/

# 계획서 동기화 (Stage 완료 후)
cp docs/plans/*.md \
   /Obsidian/SHawn/10-Projects/SHawn-Brain/Plans/
```

---

## 📊 3가지 타입 요약표

| 항목 | 일지 | 리포트 | 계획서 |
|------|------|--------|--------|
| **목적** | 프로젝트 진행 기록 | 성과 정리 | 다음 준비 |
| **시점** | 프로젝트 완료 후 | 완료 후 | 완료 후 |
| **단위** | 프로젝트/Stage 단위 | 프로젝트/Stage 단위 | 다음 단계 |
| **내용** | 시간순 기록 | 통계, 메트릭 | 목표, 일정 |
| **저장소** | memory/logs/ | docs/reports/ | docs/plans/ |
| **Obsidian** | 50-Lab/Projects/ | 50-Lab/Reports/ | 10-Projects/Plans/ |
| **파일명** | PROJECT-LOG.md | COMPLETION-REPORT.md | STEP-PLAN.md |
| **빈도** | 프로젝트마다 | 프로젝트마다 | 프로젝트마다 |

---

## ✅ 즉시 적용 (2026-02-01 현재)

### Step 1: 이번 프로젝트(Stage 4 Step 1-3)의 일지 생성
```
260201-STAGE4-STEP123-PROJECT-LOG.md 작성
- 신경계 할당 자동화
- 신경 실행 시스템
- 작업 추적 시스템
```

### Step 2: 결과 리포트 생성
```
260201-STAGE234-COMPLETION-REPORT.md
```

### Step 3: 다음 단계(Step 4) 계획서 생성
```
260202-STAGE4-STEP4-PLAN.md
- Step 4 상세 계획
- 모니터링 & 폴백 시스템
```

### Step 4: Obsidian 동기화
```
Obsidian 폴더 구조 확인
- 50-Lab/SHawn-Brain-Lab/Projects/
- 50-Lab/SHawn-Brain-Lab/Reports/
- 10-Projects/SHawn-Brain/Plans/
```

---

**이 규칙을 적용하면:**
- ✅ 작업 진행: 일지에 기록
- ✅ Stage 완료: 리포트 + 계획서 + Obsidian 동기화
- ✅ 장기 추적: Obsidian에 누적
- ✅ 분석 용이: 타입별로 명확한 구분
