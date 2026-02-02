# 원래 뇌 구조 파일명명법 복원 전략

## 🧠 **Level 3 (신피질 Neocortex) - 복원 계획**

### **문제 분석**

```
박사님 의문: "원래 뇌 구조 파일명명법으로 되돌려 왜 바꼨거야?"

상황:
- 원래: SHawn_Brain/ → brain_core/(brainstem, limbic_system, cartridge_system)
- 변경: src/brain/brain_core/ 에 새 파일들 추가
  └─ daily_model_tester.py
  └─ hippocampus.py
  └─ obsidian_memory.py
  └─ [기타]

문제: 원래 뇌 구조 폴더명명법이 아님
```

---

## 🎯 **원래 뇌 구조 이해**

### **SHawn_Brain/brain_core/ 구조**

```
brain_core/
├─ brainstem/ (기본 생존 기능)
│  ├─ __init__.py
│  ├─ brainstem.py (뇌간 핵심)
│  ├─ initialization.py (초기화)
│  ├─ survival_functions.py (생존 기능)
│  └─ [기타]
│
├─ limbic_system/ (감정 & 주의)
│  ├─ __init__.py
│  ├─ limbic_system.py (변린계 핵심)
│  ├─ hippocampus.py (해마 - 기억 통합)
│  ├─ amygdala.py (편도체 - 감정)
│  ├─ emotion_analysis.py (감정 분석)
│  └─ [기타]
│
└─ cartridge_system/ (카트리지 시스템)
   ├─ __init__.py
   ├─ cartridge_manager.py (카트리지 관리)
   └─ [기타]
```

---

## 🔧 **복원 전략**

### **Step 1: 루트 파일들의 올바른 위치**

```
현재 src/brain/brain_core/의 새 파일들:

1️⃣ daily_model_tester.py
   → 원래 위치: SHawn_Brain/의 루트 또는 utilities/
   → 복원: SHawn_Brain/daily_model_tester.py 유지
   → src에 복사할 때: src/utilities/ 또는 src/brain/utilities/

2️⃣ daily_allocation_updater.py
   → 원래 위치: SHawn_Brain/의 루트 또는 utilities/
   → 복원: SHawn_Brain/daily_allocation_updater.py 유지
   → src에 복사할 때: src/utilities/ 또는 src/brain/utilities/

3️⃣ daily_automation_pipeline.py
   → 원래 위치: SHawn_Brain/의 루트 또는 utilities/
   → 복원: SHawn_Brain/daily_automation_pipeline.py 유지
   → src에 복사할 때: src/utilities/ 또는 src/brain/utilities/

4️⃣ hippocampus.py
   → 원래 위치: SHawn_Brain/brain_core/limbic_system/
   → 복원: src/brain/brain_core/limbic_system/hippocampus.py
   
5️⃣ obsidian_memory.py
   → 원래 위치: SHawn_Brain/brain_core/limbic_system/ (기억 시스템)
   → 복원: src/brain/brain_core/limbic_system/obsidian_memory.py

6️⃣ obsidian_extractor.py
   → 원래 위치: SHawn_Brain/brain_core/limbic_system/ (기억 추출)
   → 복원: src/brain/brain_core/limbic_system/obsidian_extractor.py
```

---

## 📋 **복원 계획 (세부)**

### **원래 뇌 구조 유지 원칙**

```
1. brain_core/ 내부 구조는 절대 변경하지 않음
   └─ brainstem/
   └─ limbic_system/
   └─ cartridge_system/

2. 새 파일들은 올바른 폴더에 배치
   └─ 기억 관련 → limbic_system/
   └─ 자동화 스크립트 → utilities/ 또는 tools/
   └─ 분석 도구 → utilities/ 또는 neuronet/

3. src/ 구조는 SHawn_Brain 구조를 완벽히 복제
   └─ src/brain/brain_core/brainstem/
   └─ src/brain/brain_core/limbic_system/
   └─ src/brain/brain_core/cartridge_system/
```

---

## 🚀 **복원 실행 (Level 4)**

### **복원할 것**

```
1️⃣ src/brain/brain_core/ 정리
   ✅ brainstem/ 폴더 유지
   ✅ limbic_system/ 폴더 유지
   ✅ cartridge_system/ 폴더 유지
   
2️⃣ 새 파일들 올바른 위치로 이동
   ✅ hippocampus.py → src/brain/brain_core/limbic_system/
   ✅ obsidian_memory.py → src/brain/brain_core/limbic_system/
   ✅ obsidian_extractor.py → src/brain/brain_core/limbic_system/
   
3️⃣ 자동화 스크립트 분리
   ✅ daily_*.py → src/utilities/ 또는 별도 tools/ 폴더
   
4️⃣ 확인
   ✅ src/brain/brain_core/ 구조가 SHawn_Brain/brain_core/과 동일
   ✅ 모든 파일이 올바른 폴더에 위치
```

---

## ✅ **결론**

```
박사님 의도: 원래 뇌 구조 명명법 유지
우리 실수: 새 파일들을 섞어버림

복원 방법:
1. src/brain/brain_core/ 내부 폴더 구조는 유지
2. 새 파일들을 올바른 폴더에 배치
3. SHawn_Brain과 src의 구조 동기화

상태: 복원 준비 완료! 🧠
```
