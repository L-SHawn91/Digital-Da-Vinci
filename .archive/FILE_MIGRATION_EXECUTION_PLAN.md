# 파일 재구축 실행 계획
## 기존 70개 파일 → 신경 구조 기반 재구축

---

## 🚀 **마이그레이션 전략**

### **3단계 접근**

```
1단계: 안전한 파일부터 이동 (engines/)
   → 기능별로 이미 분류되어 있음
   → 신경 구조에 매핑하기 쉬움

2단계: Brainstem 관련 파일 이동
   → ethics, error, state, verify 파일들
   → 이미 구현된 brainstem 확장

3단계: Main 파일들 이동
   → SHawn_Brain.py → prefrontal_cortex
   → telegram_handler.py → execution
   → 점진적 통합
```

---

## 📂 **파일별 마이그레이션 매핑**

### **engines/ 폴더 → neocortex/**

```
engines/
├─ smart_router.py
│  → neocortex/prefrontal_cortex/task_router.py

├─ request_detector.py
│  → neocortex/prefrontal_cortex/request_classifier.py

├─ debate_engine.py
│  → neocortex/parietal_cortex/innovation_engine.py

├─ memory_manager.py
│  → brain_core/limbic_system/memory_bank.py

├─ feedback_system.py
│  → brain_core/limbic_system/value_system.py

├─ brainmap_context.py
│  → neocortex/prefrontal_cortex/context_mapper.py

├─ rag_pipeline.py
│  → cartridges/bio_cartridge/bio_memory.py

├─ content_engine.py
│  → neocortex/occipital_cortex/synthesis_engine.py

├─ sbi_pipeline.py
│  → utilities/utils/pipeline_utils.py

├─ parallel_processor.py
│  → utilities/utils/parallel_processing.py

├─ ensemble_validator.py
│  → utilities/utils/validation_utils.py

├─ error_handler.py (이미 brainstem에 통합)
│  → brain_core/brainstem/brainstem.py

├─ telegram_formatter.py
│  → execution/motor_cortex/action_executor.py

└─ etc... (12개 더)
```

### **Root 파일들 → 새 구조**

```
SHawn_Brain.py
├─ 핵심 엔진 부분
│  → neocortex/prefrontal_cortex/executive_function.py
│
└─ 보조 기능
   → utilities/config/neural_settings.yaml

config.py
→ utilities/config/config.py

brain_server.py
→ execution/neural_server.py

telegram_handler.py
→ execution/handlers/telegram_handler.py

run_telegram_bot.py
→ main.py (진입점)

memory_monitor_daemon.py
→ utilities/monitoring/neural_monitor.py

token_tracker.py
→ utilities/monitoring/performance_tracker.py

verify_soul.py (이미 brainstem에 통합)
→ brain_core/brainstem/brainstem.py
```

---

## 💾 **마이그레이션 실행 순서**

### **Step 1: engines/ 파일들 이동 (가장 안전)**

```bash
# 1. 백업 생성
cp -r engines/ engines_backup/

# 2. neocortex로 이동
cp engines/smart_router.py neocortex/prefrontal_cortex/task_router.py
cp engines/request_detector.py neocortex/prefrontal_cortex/request_classifier.py
cp engines/debate_engine.py neocortex/parietal_cortex/innovation_engine.py
...

# 3. limbic_system으로 이동
cp engines/memory_manager.py brain_core/limbic_system/memory_bank.py
cp engines/feedback_system.py brain_core/limbic_system/value_system.py
...

# 4. execution으로 이동
cp engines/telegram_formatter.py execution/motor_cortex/action_executor.py
...

# 5. utilities로 이동
cp engines/parallel_processor.py utilities/utils/parallel_processing.py
...
```

### **Step 2: Root 파일들 정리**

```bash
# 1. 주요 파일 이동
cp SHawn_Brain.py neocortex/prefrontal_cortex/executive_function.py
cp config.py utilities/config/config.py
cp telegram_handler.py execution/handlers/telegram_handler.py
...

# 2. 엔진 폴더 백업
mv engines/ engines_v1_backup/
```

### **Step 3: 진입점 정리**

```bash
# main.py, app.py 생성 (새 구조의 진입점)
# 기존 run_telegram_bot.py는 main.py로 이름 변경
mv run_telegram_bot.py main.py
# main.py 내용 업데이트 (새 import 경로로)
```

---

## 🎯 **마이그레이션 우선순위**

### **우선순위 1 (즉시): engines/ 파일들**

```
이유:
✅ 이미 분류됨 (위험 낮음)
✅ 코드 품질 높음
✅ 신경 구조에 명확히 매핑됨

파일 수: ~20개
예상 시간: 1-2시간
```

### **우선순위 2 (오늘): Root 핵심 파일들**

```
SHawn_Brain.py → prefrontal_cortex
brain_server.py → execution
telegram_handler.py → execution/handlers
config.py → utilities/config
memory_monitor_daemon.py → utilities/monitoring

파일 수: 5개
예상 시간: 2-3시간 (코드 수정 필요)
```

### **우선순위 3 (내일): 나머지 정리**

```
테스트 파일들
스크립트들
임시 파일들

파일 수: 30개
예상 시간: 1-2시간
```

---

## ⚠️ **마이그레이션 주의사항**

### **1️⃣ Import 경로 업데이트**

```python
# Before
from engines.smart_router import SmartRouter

# After
from neocortex.prefrontal_cortex.task_router import TaskRouter
```

### **2️⃣ 순환 참조 확인**

```
A → B → C 순환 구조 검증
신경 구조는 계층적이므로 역방향 참조 금지
```

### **3️⃣ 테스트 유지**

```
마이그레이션 후 매번 테스트 실행
기능 동일성 확인
```

---

## 📊 **마이그레이션 체크리스트**

### **Phase 1: 준비 (지금)**

- [ ] engines_backup/ 생성
- [ ] 파일 매핑 확인
- [ ] 위험도 평가

### **Phase 2: engines/ 이동**

- [ ] neocortex/* 파일 복사
- [ ] limbic_system/* 파일 복사
- [ ] execution/* 파일 복사
- [ ] utilities/* 파일 복사
- [ ] Import 경로 업데이트
- [ ] 테스트 실행

### **Phase 3: Root 파일 이동**

- [ ] SHawn_Brain.py → prefrontal_cortex
- [ ] config.py → utilities/config
- [ ] brain_server.py → execution
- [ ] telegram_handler.py → execution/handlers
- [ ] memory_monitor_daemon.py → utilities/monitoring
- [ ] Import 경로 대량 업데이트
- [ ] 테스트 실행

### **Phase 4: 정리**

- [ ] 나머지 파일들 정리
- [ ] 불필요한 파일 제거
- [ ] 폴더 구조 최적화
- [ ] 최종 테스트

---

## 🎯 **먼저 할 일**

### **즉시 실행할 마이그레이션**

```bash
# 1단계: engines/ 백업
cp -r engines/ engines_v1_backup/

# 2단계: 가장 안전한 파일부터 이동
# (사용처가 적은 유틸리티 먼저)
- sbi_pipeline.py → utilities/
- parallel_processor.py → utilities/
- validators.py → utilities/
- error_handler.py → brainstem (이미 구현됨)
- state_manager.py → brainstem (이미 구현됨)
```

### **패턴 1: 복사 후 업데이트 (안전)**

```bash
# 1. 복사
cp engines/smart_router.py neocortex/prefrontal_cortex/task_router.py

# 2. 코드 검토
# - import 경로 확인
# - 클래스명 변경 필요한지 확인
# - 함수 시그니처 확인

# 3. 업데이트 (필요시)
# - import 경로 수정
# - 의존성 조정

# 4. 테스트
# - 단위 테스트 실행
# - 통합 테스트 실행

# 5. 기존 파일 제거
# rm engines/smart_router.py
```

---

## 💡 **박사님 선택**

### **Option A: 빠른 진행 (지금 시작)**
```
- 백업만 하고 바로 파일 이동
- 마이그레이션하면서 테스트
- 하루 안에 완료 가능

위험: 코드 깨질 수 있음
```

### **Option B: 안전한 진행 (권장)**
```
1. engines/ 파일들부터 천천히 이동
2. 각 단계마다 철저히 테스트
3. 3-5일에 걸쳐 완료

이점: 안정성 확보
```

### **Option C: 하이브리드**
```
1. 안전한 유틸리티 파일들 먼저 이동
2. 핵심 파일들은 병렬로 준비
3. 2-3일에 완료
```

---

## 🚀 **다음 액션**

박사님의 선택:
1. **Option A**: "빠르게 진행해"
2. **Option B**: "안전하게 진행해" (권장)
3. **Option C**: "하이브리드로"

선택 후:
```
✅ engines_v1_backup/ 생성
✅ 파일 이동 시작
✅ Import 경로 업데이트
✅ 테스트 실행
```

---

**파일 재구축을 시작할까요?** 🚀
