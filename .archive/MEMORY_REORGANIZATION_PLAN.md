# 메모리 폴더 재구성 - 최종 구조

## 📂 **새로운 메모리 구조**

```
/workspace/memory/
├─ README.md (새로 만들 것)
│  └─ 메모리 폴더 사용 설명
│
├─ Daily/
│  ├─ 2026-01-30.md
│  ├─ 2026-01-30-SESSION-COMPLETE.md
│  ├─ 2026-01-30-WEEK1-COMPLETE.md
│  ├─ 2026-01-31.md
│  ├─ 2026-01-31-final-checkpoint.md
│  ├─ 2026-01-31-phase9-plan.md
│  └─ (YYYY-MM-DD.md 형식)
│
├─ SHawn-Bot/
│  ├─ SHAWN_BOT_ARCHITECTURE_REVIEW.md
│  ├─ SHAWN_BOT_ANALYSIS.md
│  ├─ SHAWN_BOT_FIX_PLAN.md
│  ├─ SHAWN_BOT_FIX_COMPLETE.md
│  ├─ SHAWN_BOT_INFO.md
│  └─ PROJECT_OMNI_*.md (모두)
│
├─ SHawn-Brain/
│  ├─ SHAWN_BRAIN_V5_5_COMPLETE_4WEEK_PLAN.md ⭐ (핵심)
│  ├─ SHAWN_BRAIN_V5_5_QUICK_SUMMARY.md
│  ├─ SHAWN_BRAIN_V5_5_MODULAR_ARCHITECTURE.md
│  └─ SHAWN_LAB_LEARNING_REPORT.md
│
├─ SHawn-Web/
│  └─ (웹사이트 관련 파일)
│
├─ Projects/
│  ├─ PLAN.md
│  ├─ WEEK2_PLAN_RAG_ENGINE.md
│  └─ 각종 계획 문서
│
├─ Decisions/
│  ├─ MEMORY_ARCHITECTURE_4LAYERS_STRATEGY.md
│  ├─ MEMORY_COMPARISON_TABLE.md
│  ├─ MEMORY_LOCATION_OPTIONS.md
│  ├─ OPTION3_*.md
│  └─ 주요 결정 기록
│
├─ TechRef/
│  ├─ OBSIDIAN_VS_PINECONE.md
│  ├─ PINECONE_INTEGRATION_PLAN.md
│  ├─ WINDOWS_*.md
│  ├─ GATEWAY_TOKEN_SETUP.md
│  ├─ GITHUB_USAGE_MONITOR.md
│  ├─ MODEL_CHANGE_PLAN.md
│  ├─ CONTEXT_EXPLAINED.md
│  └─ 기술 레퍼런스
│
├─ Obsidian-Sync/
│  └─ (Obsidian과 동기화되는 메모리)
│  └─ 구조: workspace/memory/ = 복제본
│
└─ Archived/
   ├─ README_PROTECTED.md
   ├─ SITUATION_MODELS.md
   └─ 이전 파일들
```

---

## 🔄 **이동할 파일 목록**

### Daily/
```
✅ 2026-01-30.md
✅ 2026-01-30-SESSION-COMPLETE.md
✅ 2026-01-30-WEEK1-COMPLETE.md
✅ 2026-01-31.md
✅ 2026-01-31-final-checkpoint.md
✅ 2026-01-31-phase9-plan.md
```

### SHawn-Bot/
```
→ SHAWN_BOT_ARCHITECTURE_REVIEW.md
→ SHAWN_BOT_ANALYSIS.md
→ SHAWN_BOT_FIX_PLAN.md
→ SHAWN_BOT_FIX_COMPLETE.md
→ SHAWN_BOT_INFO.md
→ PROJECT_OMNI_TECHNICAL_SPEC.md
→ PROJECT_OMNI_COMPREHENSIVE_ASSESSMENT.md
→ PROJECT_OMNI_RULES_AND_PRINCIPLES.md
```

### SHawn-Brain/
```
→ SHAWN_BRAIN_V5_5_COMPLETE_4WEEK_PLAN.md ⭐
→ SHAWN_BRAIN_V5_5_QUICK_SUMMARY.md
→ SHAWN_BRAIN_V5_5_MODULAR_ARCHITECTURE.md
→ SHAWN_LAB_LEARNING_REPORT.md
```

### Projects/
```
→ PLAN.md
→ WEEK2_PLAN_RAG_ENGINE.md
```

### Decisions/
```
→ MEMORY_ARCHITECTURE_4LAYERS_STRATEGY.md
→ MEMORY_COMPARISON_TABLE.md
→ MEMORY_LOCATION_OPTIONS.md
→ OPTION3_IMPLEMENTATION_COMPLETE.md
→ OPTION3_OBSIDIAN_MEMORY.md
```

### TechRef/
```
→ OBSIDIAN_VS_PINECONE.md
→ PINECONE_INTEGRATION_PLAN.md
→ WINDOWS_INDEPENDENT_GUIDE.md
→ WINDOWS_OPENCLAW_INSTALL.md
→ GATEWAY_TOKEN_SETUP.md
→ GITHUB_USAGE_MONITOR.md
→ MODEL_CHANGE_PLAN.md
→ CONTEXT_EXPLAINED.md
→ SITUATION_MODELS.md
```

### Archived/
```
→ README_PROTECTED.md
```

---

## 🎯 **실행 단계**

### **Step 1: 폴더 생성** ✅ (완료)

```bash
mkdir -p memory/{Daily,Projects,SHawn-Bot,SHawn-Web,SHawn-Brain,Decisions,TechRef,Archived,Obsidian-Sync}
```

### **Step 2: 파일 이동** (다음)

```bash
# Daily 폴더로
mv 2026-01-30.md Daily/
mv 2026-01-30-SESSION-COMPLETE.md Daily/
# ... 등등
```

### **Step 3: README 생성** (그 다음)

메모리 폴더의 사용 규칙 문서화

---

## 📌 **메모리 사용 규칙 (확정)**

### **1. Daily/ 폴더**
- 매일 작업 내용 기록
- 파일명: `YYYY-MM-DD.md`
- 내용: 생 기록, 상세 내용
- 주기: 매일

### **2. Projects/ 폴더**
- 계획서, 로드맵
- 파일명: 자유
- 내용: 계획, 일정
- 주기: 필요시 업데이트

### **3. SHawn-Bot/, SHawn-Brain/, SHawn-Web/**
- 프로젝트별 문서
- 상세 분석, 계획, 리뷰
- 참고용

### **4. Decisions/**
- 주요 결정 기록
- 아키텍처 선택, 기술 결정
- 이유와 함께 기록

### **5. TechRef/**
- 기술 레퍼런스
- 설정, 설치, 기술 자료
- 참고용

### **6. Obsidian-Sync/**
- Obsidian 메모리 동기화
- workspace/memory/의 복제본
- 필요시 자동 동기화

### **7. Archived/**
- 이전 파일, deprecated
- 참고만 필요할 때

---

## ⚠️ **보호되는 파일**

```
읽기 전용:
├─ /workspace/MEMORY.md (공식 기록)
├─ /workspace/AGENTS.md
├─ /workspace/SOUL.md
├─ /workspace/USER.md
└─ /workspace/IDENTITY.md

수정 금지:
└─ 박사님 권지 없이 변경 금지
```

---

## ✅ **다음 액션**

1️⃣ **파일 이동** (자동화 필요)
2️⃣ **README.md 생성** (메모리 폴더용)
3️⃣ **Obsidian-Sync 설정** (필요시)
4️⃣ **MEMORY.md 업데이트** (통합 내용)

---

**준비 완료! 파일 이동을 시작하겠습니다!** 🚀
