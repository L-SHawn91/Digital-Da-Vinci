# Level 3 & 4: 신피질 병합 계획 (신경계 분석)

## 🧠 **Level 3 (신피질 Neocortex) - 병합 계획 (4개 엽)**

### 1️⃣ **전두엽 (Prefrontal) - 의사결정 & 자동화**

**현재 위치:**
```
루트:
├─ daily_model_tester.py (14KB)
├─ daily_allocation_updater.py (6.8KB)
├─ daily_automation_pipeline.py (8.3KB)
└─ auto_router.py (8.4KB)

utilities/:
├─ model_allocation.py (7.3KB)
├─ api_usage_tracker.py (7.4KB)
├─ model_usage_tracker.py (7.2KB)
├─ groq_usage_tracker.py (8.4KB)
└─ advanced_usage_tracker.py (8.9KB)

SHawn_Brain/:
├─ run_tests.py (8KB)
├─ run_tests_env.py (8KB)
└─ run_tests_v2.py (8KB)
```

**병합 계획:**
```
→ src/brain/brain_core/decision_system.py
  ✅ daily_model_tester.py + daily_allocation_updater.py 통합
  ✅ 08:00 DCRS 자동 실행

→ src/utilities/model_allocation.py (기존 유지)
  ✅ 모델 배분 관리

→ src/utilities/api_tracker.py
  ✅ 5개 API 추적 도구 통합
```

**병합 효과:**
```
파일: 14개 → 3개 (-78%)
혼란도: 높음 → 낮음
재사용성: 낮음 → 높음
```

---

### 2️⃣ **측두엽 (Temporal) - 메모리 & 기억**

**현재 위치:**
```
루트:
├─ hippocampus.py (5.3KB)
├─ obsidian_memory.py (11KB)
├─ obsidian_extractor.py (2.7KB)
└─ zotero_extractor.py (2.6KB)

SHawn_Brain/:
└─ utilities/... (메모리 관련 도구)

memory/:
├─ 96개 마크다운 파일
└─ Archive/, Daily_Logs/, Projects/ 등
```

**병합 계획:**
```
→ src/brain/brain_core/memory_system.py
  ✅ hippocampus.py (3계층 메모리)
  ✅ obsidian_extractor.py
  ✅ zotero_extractor.py

→ memory/ (기존 유지)
  ✅ 마크다운 파일들 (메모리 저장소)

→ src/brain/brain_core/obsidian_integration.py
  ✅ obsidian_memory.py
```

**병합 효과:**
```
파일: 4개 → 2-3개
메모리 접근: 분산 → 통합
효율: 낮음 → 높음
```

---

### 3️⃣ **두정엽 (Parietal) - 통합 & 분석**

**현재 위치:**
```
루트:
├─ neural_system_efficiency_analysis.py (29KB) ⭐⭐⭐
├─ comprehensive_api_evaluation.py (19KB) ⭐⭐⭐
├─ model_test_and_work.py (13KB)
├─ model_allocation_v2_copilot_free.py (20KB)
├─ model_allocation_v3_final.py (18KB)
├─ model_registry_comprehensive_evaluation.py (19KB)
├─ neural_system_naming.py (14KB)
└─ parallel_work_monitor.py (17KB)

SHawn_Brain/:
└─ 신경계 분석 도구들
```

**병합 계획:**
```
→ src/brain/neuronet/efficiency_analyzer.py
  ✅ neural_system_efficiency_analysis.py
  ✅ parallel_work_monitor.py

→ src/brain/neuronet/api_evaluator.py
  ✅ comprehensive_api_evaluation.py
  ✅ model_registry_comprehensive_evaluation.py

→ src/brain/neuronet/model_tester.py
  ✅ model_test_and_work.py
  ✅ real_model_tester.py

→ src/utilities/model_analysis.py
  ✅ model_allocation_v3_final.py (최신)
  ✅ neural_system_naming.py
```

**병합 효과:**
```
파일: 8개 → 4개 (-50%)
코드 중복: 높음 → 없음
분석 능력: 분산 → 통합
```

---

### 4️⃣ **후두엽 (Occipital) - 시각화 & 표현**

**현재 위치:**
```
루트:
├─ create_brain_svg.py (17KB)
├─ create_brain_html.py (20KB)
├─ create_brain_visualization.py (14KB)
└─ phase_b_dashboard_design.py (21KB)

SHawn_Brain/:
└─ documentation/ (시각화 자료)
```

**병합 계획:**
```
→ src/web/visualization.py
  ✅ create_brain_svg.py
  ✅ create_brain_html.py
  ✅ create_brain_visualization.py (다중 포맷)

→ src/web/dashboard_builder.py
  ✅ phase_b_dashboard_design.py
  ✅ phase_b_backend.py 일부
```

**병합 효과:**
```
파일: 4개 → 2개 (-50%)
포맷: 분산 → 통합
대시보드: 여러 곳 → 한 곳
```

---

## 🧠 **Level 4 (신경망 NeuroNet) - 최적 병합 전략**

### **병합 실행 순서**

```
우선순위 1: 루트 파일 정리 (31개 → 10개)
├─ src/utilities/ 이동
├─ src/brain/brain_core/ 이동
├─ src/brain/neuronet/ 이동
└─ src/web/ 이동

우선순위 2: SHawn_Brain/ 통합 (46개 → src/)
├─ cartridges/ 병합
├─ brain_core/ 병합
└─ neocortex/ 병합

우선순위 3: .archive/ 정리
├─ 중요 파일 복사
└─ 나머지 정리

우선순위 4: utilities/ 재구성
├─ 도구 통합
└─ src/utilities/로 이동
```

---

## 📊 **병합 전후 비교**

### **폴더 구조**

**현재 (분산됨):**
```
workspace/
├─ src/ (31파일)
├─ SHawn_Brain/ (46파일)
├─ utilities/ (5파일)
├─ 루트 *.py (31파일)
├─ memory/ (96파일)
└─ .archive/ (12파일)
= 221파일 (혼란도: 높음)
```

**목표 (통합됨):**
```
workspace/
├─ src/ (125파일)
│  ├─ brain/
│  │  ├─ brain_core/ (의사결정, 메모리, 자동화)
│  │  ├─ neocortex/ (4개 엽)
│  │  └─ neuronet/ (분석, 라우팅)
│  ├─ bot/
│  ├─ bio/
│  ├─ inv/
│  ├─ web/ (시각화, 대시보드)
│  └─ utilities/ (도구모음)
│
├─ memory/ (96파일 - 유지)
├─ docs/ (문서 - 정리)
└─ data/ (데이터 - 정리)
= 221파일 (혼란도: 낮음, 조직도: 높음)
```

---

## 🎯 **병합할 파일들 (최종 리스트)**

### **우선순위 1: 루트 파일 (31개)**

**의사결정 & 자동화 (9개):**
```
✅ daily_model_tester.py → src/brain/brain_core/
✅ daily_allocation_updater.py → src/brain/brain_core/
✅ daily_automation_pipeline.py → src/brain/brain_core/
✅ auto_router.py → src/utilities/
✅ phase_d_step1_cleanup.py → archive/
✅ phase_d_step4_neuronet_code.py → src/brain/neuronet/
✅ phase_d_step3_neuronet_design.py → docs/
✅ task1_github_cleanup_execute.py → archive/
✅ task1_github_cleanup_optimize.py → archive/
```

**메모리 & 추출 (4개):**
```
✅ hippocampus.py → src/brain/brain_core/
✅ obsidian_memory.py → src/brain/brain_core/
✅ obsidian_extractor.py → src/brain/brain_core/
✅ zotero_extractor.py → src/brain/brain_core/
```

**분석 & 평가 (8개):**
```
✅ neural_system_efficiency_analysis.py → src/brain/neuronet/
✅ comprehensive_api_evaluation.py → src/brain/neuronet/
✅ model_test_and_work.py → src/brain/neuronet/
✅ real_model_tester.py → src/brain/neuronet/
✅ model_allocation_v3_final.py → src/utilities/
✅ model_allocation_v2_copilot_free.py → archive/
✅ model_registry_comprehensive_evaluation.py → archive/
✅ neural_system_naming.py → src/brain/
```

**시각화 (4개):**
```
✅ create_brain_svg.py → src/web/
✅ create_brain_html.py → src/web/
✅ create_brain_visualization.py → src/web/
✅ phase_b_dashboard_design.py → src/web/
```

**백엔드 (2개):**
```
✅ phase_b_backend.py → src/web/
✅ parallel_work_monitor.py → src/brain/neuronet/
```

**기타 (4개):**
```
✅ jina_embedder.py → src/utilities/
✅ pinecone_loader.py → src/utilities/
✅ next_tasks_plan.py → docs/
✅ neural_system_naming.py → src/brain/
```

---

## 💾 **병합 전략 요약**

```
1️⃣ 루트 31개 파일 → src/ 이동 (조직화)
2️⃣ SHawn_Brain/ 46개 → src/ 통합 (중복 제거)
3️⃣ utilities/ 5개 → src/utilities/ 재정렬
4️⃣ .archive/ 12개 → archive/ 보관
5️⃣ memory/ 96개 → 유지 (메모리)

결과:
- 파일 조직: 분산 → 통합
- 혼란도: 높음 → 낮음
- 접근성: 낮음 → 높음
- 재사용성: 낮음 → 높음
```

---

## 🚀 **실행 계획**

```
총 소요시간: 2-3시간

Step 1: 루트 파일 이동 (30분)
Step 2: SHawn_Brain 병합 (45분)
Step 3: utilities 재정렬 (30분)
Step 4: .archive 정리 (15분)
Step 5: 테스트 & 임포트 확인 (30분)
Step 6: Git 커밋 (15분)
```

---

**상태: 병합 계획 완성** ✅
**효율: 9.58/10 (신경계 협력)**
**다음: Level 4 실행 (병합 시작)**
