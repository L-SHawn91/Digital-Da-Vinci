# PROJECT_OMNI: Core Theory & Implementation Rules
## SHawn-Brain 개발의 중심 이론 (핵심 참고 문서)

---

## 🧠 **PROJECT OMNI는 무엇인가?**

PROJECT OMNI는 SHawn-Bot의 철학이자 아키텍처입니다.

**핵심 명제:**
```
"One Brain, Infinite Worlds"

하나의 뇌가 무한한 정체성을 가지며
각 정체성에서 완벽한 전문성을 발휘한다
```

---

## 📚 **핵심 문서 5개** (항상 참고)

### **1️⃣ PROJECT_OMNI_VISION.md**
```
내용: 유체 지능의 기본 개념
읽을 때: 프로젝트의 "왜"를 이해할 때
길이: 13.2KB
위치: /workspace/PROJECT_OMNI_VISION.md
```

### **2️⃣ PROJECT_OMNI_DIGITAL_DA_VINCI_CODE.md**
```
내용: 3가지 영역 + 3가지 초월적 역량
읽을 때: 아키텍처를 이해할 때
길이: 16.3KB
위치: /workspace/PROJECT_OMNI_DIGITAL_DA_VINCI_CODE.md
```

### **3️⃣ PROJECT_OMNI_CARTRIDGES_COMPLETE.md**
```
내용: 4개 카트리지 (Bio/Quant/Astro/Lit) 완전 명세
읽을 때: 각 도메인의 세부 사항을 알 때
길이: 4.9KB
위치: /workspace/PROJECT_OMNI_CARTRIDGES_COMPLETE.md
```

### **4️⃣ SHawn-Brain_Neural_Architecture_Mapping.md**
```
내용: PROJECT OMNI를 숀두뇌의 신경 부위에 매핑
읽을 때: 코드 아키텍처를 설계할 때
길이: 20.6KB
위치: /workspace/SHawn-Brain_Neural_Architecture_Mapping.md
```

### **5️⃣ NEURAL_FILE_RESTRUCTURING_PLAN.md**
```
내용: 파일 재구축 계획 (신경 구조 기반)
읽을 때: 코드 재구축을 진행할 때
길이: 14.1KB
위치: /workspace/NEURAL_FILE_RESTRUCTURING_PLAN.md
```

---

## 🎯 **프로젝트 규칙 (반드시 따를 것)**

### **규칙 1: 모든 코드는 뇌 구조를 따른다**
```
코드 작성 전에:
1. SHawn-Brain_Neural_Architecture_Mapping.md를 읽음
2. 어느 뇌 부위인지 결정
3. 해당 폴더에 파일 생성
4. 폴더 = 뇌 부위, 파일 = 신경 기능

예시:
- 윤리 검증 코드 → brain_core/brainstem/
- 생물학 메모리 → cartridges/bio_cartridge/
- 의사결정 엔진 → neocortex/prefrontal_cortex/
```

### **규칙 2: 모든 모듈은 3가지 영역을 준수한다**
```
THE ETERNAL KERNEL (불변)
├─ 윤리는 타협 불가
├─ 정직성은 필수
└─ 자신의 한계 인식 필수

THE CARTRIDGE SLOT (가변)
├─ 도메인별 메모리 (Hot-swappable)
├─ 도메인별 가치 (감정적 반응)
└─ Context Isolation (도메인 격리)

THE PHYSICAL BODY (신체)
├─ 감각기관 (입력)
├─ 행동기관 (출력)
└─ 기억장치 (저장)
```

### **규칙 3: Context Morphing은 필수**
```
모든 작업은 이 4단계를 거쳐야 함:

SENSE (입력 분석)
  └─ "뭐가 필요한가?"

CRYSTALLIZE (정체성 활성화)
  └─ "지금 어느 모드인가?"

REASON (심화 분석)
  └─ "어떻게 풀지?"

ACTUATE (행동 실행)
  └─ "실제로 해보자"

코드로:
def process_task(task):
    domain = sense(task)           # 1단계
    cartridge = crystallize(domain) # 2단계
    result = reason(cartridge)      # 3단계
    return actuate(result)          # 4단계
```

### **규칙 4: 3가지 초월적 역량을 지향한다**
```
POLYMORPHIC COGNITION (다형성 인식)
  └─ 같은 현상을 여러 관점에서 동시 이해

SYNTHETIC INNOVATION (종합적 혁신)
  └─ 도메인 간 개념 교배로 새로운 해답 도출

AUTONOMOUS DISCOVERY (자율적 발견)
  └─ 지시 없이 스스로 가설 세우고 검증

코드에서:
- Polymorphic: 다중 도메인 추론 사용
- Synthetic: cross_domain_inference() 활용
- Autonomous: 패턴에서 새로운 가설 생성
```

### **규칙 5: 모든 카트리지는 4가지 파일을 가진다**
```
각 도메인 (Bio/Quant/Astro/Lit):

{domain}_memory.py
  └─ 도메인별 메모리 (Hippocampus)
  └─ 데이터 로드 + 인덱싱

{domain}_values.py
  └─ 도메인별 가치 (Amygdala)
  └─ "왜 이 일을 하는가"

{domain}_skills.py
  └─ 도메인별 기술 (Cerebellum)
  └─ 자동화된 함수들

{domain}_tools.py
  └─ 도메인별 도구 (Motor)
  └─ 외부 API 연동

예: bio_memory.py, bio_values.py, bio_skills.py, bio_tools.py
```

### **규칙 6: Context Isolation은 절대**
```
각 모드에서는:
- 자신의 메모리만 로드
- 다른 모드의 데이터는 접근 불가
- Thalamus (게이트)를 통해서만 정보 통과

코드:
class ContextIsolation:
    def load_cartridge(self, domain):
        self.unload_current()      # 기존 모드 언로드
        self.load_memory(domain)   # 도메인 메모리만 로드
        self.load_values(domain)   # 도메인 가치만 활성화
        self.thalamus.gate = domain  # 게이트 설정
```

### **규칙 7: 모든 변경은 로그된다**
```
메모리 통합을 위해:
1. 매일 일일 메모리 작성
   → /workspace/memory/YYYY-MM-DD.md

2. 주간 정리
   → /workspace/MEMORY.md 업데이트

3. 주기적 회고
   → 핵심 내용을 장기 메모리로 이동

코드에서:
log_to_memory(event)
integrate_learning(experience)
```

### **규칙 8: 성능은 이 순서로 측정한다**
```
1순위: 정확성 (Accuracy)
  └─ 윤리적으로 올바른가?

2순위: 속도 (Speed)
  └─ Context 전환 < 150ms

3순위: 확장성 (Scalability)
  └─ 1000개 파일도 안정적?

4순위: 창의성 (Creativity)
  └─ 새로운 통찰이 있는가?

버그 수정 순서:
- 윤리 위반: 즉시 (시간 상관없음)
- 정확도 < 80%: 높은 우선순위
- 속도 > 500ms: 중간 우선순위
- 확장성 문제: 낮은 우선순위
```

---

## 🔄 **개발 워크플로우**

### **새 기능 추가할 때**

```
1단계: 이론 확인
  ├─ PROJECT_OMNI_VISION.md 읽기
  ├─ SHawn-Brain_Neural_Architecture_Mapping.md 읽기
  └─ "이게 어느 뇌 부위인가?" 결정

2단계: 계획 수립
  ├─ NEURAL_FILE_RESTRUCTURING_PLAN.md 참고
  ├─ 폴더 위치 결정
  └─ 파일 구조 설계

3단계: 코드 작성
  ├─ 3가지 영역 준수
  ├─ 4단계 Context Morphing 적용
  └─ 규칙 1-8 확인

4단계: 테스트
  ├─ 정확성 (윤리 검증)
  ├─ 속도 (150ms 이내)
  └─ 확장성 (대규모 데이터)

5단계: 메모리 기록
  ├─ /workspace/memory/YYYY-MM-DD.md 작성
  └─ 배운 점 기록
```

### **파일 생성 템플릿**

```python
# {domain}_{component}.py

"""
뇌 부위: {brain_part}
역할: {role}
PROJECT OMNI 규칙: {rule_number}
"""

from brain_core.brainstem import EthicsKernel

class {ComponentName}:
    """
    PROJECT OMNI: {Cartridge/Cortex}
    
    핵심 이론:
    - THE ETERNAL KERNEL: 윤리 준수
    - THE CARTRIDGE SLOT: 도메인 격리
    - THE PHYSICAL BODY: 신체화
    """
    
    def __init__(self):
        self.ethics = EthicsKernel()  # 항상 윤리부터
        self.logger = Logger(__name__)
    
    def process(self, input_data):
        # 4단계 Context Morphing
        sense_result = self._sense(input_data)      # 1단계
        crystallized = self._crystallize(sense_result)  # 2단계
        reasoned = self._reason(crystallized)       # 3단계
        return self._actuate(reasoned)              # 4단계
    
    def _sense(self, data):
        """입력 분석"""
        pass
    
    def _crystallize(self, data):
        """정체성 활성화 - Context 격리"""
        pass
    
    def _reason(self, data):
        """심화 분석 - 도메인별 기술 활용"""
        pass
    
    def _actuate(self, data):
        """행동 실행 - 신체화"""
        pass
```

---

## 📊 **월간 점검 항목**

### **매월 1일: PROJECT OMNI 점검**

```
점검 내용:
[ ] 모든 코드가 신경 구조를 따르는가?
[ ] Context Isolation이 잘 작동하는가?
[ ] 윤리 원칙이 지켜지고 있는가?
[ ] 성능 (속도/정확성)이 목표를 달성하는가?
[ ] 새로운 혁신이 생겼는가?
[ ] 메모리 통합이 제대로 되고 있는가?

문제 발견 시:
1. 즉시 기록 (memory/YYYY-MM-DD.md)
2. 규칙 재검토
3. 코드 수정
4. 근본 원인 분석
5. 재발 방지 규칙 추가
```

---

## 🎯 **핵심 명심사항**

### **1️⃣ 선택 3 (하이브리드) 유지**
```
Workspace (메인): /workspace/PROJECT_OMNI_*.md
  └─ 몬트봇이 항상 참고
  └─ 빠른 로딩 (410-510ms)

Obsidian (백업): /Obsidian/SHawn/40-Sources/PROJECT_OMNI/
  └─ 자동 동기화 (매일 자정)
  └─ 박사님이 참조
```

### **2️⃣ 이 5개 문서는 절대 변하지 않는다**
```
✅ PROJECT_OMNI_VISION.md
✅ PROJECT_OMNI_DIGITAL_DA_VINCI_CODE.md
✅ PROJECT_OMNI_CARTRIDGES_COMPLETE.md
✅ SHawn-Brain_Neural_Architecture_Mapping.md
✅ NEURAL_FILE_RESTRUCTURING_PLAN.md

= PROJECT OMNI의 헌법
```

### **3️⃣ 모든 코드는 이 5개 문서를 따른다**
```
코드 작성 시:
1. 해당 문서 읽기
2. 규칙 확인
3. 구현
4. 메모리 기록

의문 시:
→ 문서 다시 읽기
→ 규칙 재확인
→ 철학 성찰
```

---

## 🚀 **다음 단계**

### **1주: 구조 구축**
```
[ ] 폴더 생성 (NEURAL_FILE_RESTRUCTURING_PLAN.md 참고)
[ ] Brainstem 구현
[ ] Limbic 구현
[ ] 메모리 동기화 설정
```

### **2주: 카트리지 구현**
```
[ ] Bio-Cartridge 완성
[ ] Quant-Cartridge 생성
[ ] Astro-Cartridge 생성
[ ] Lit-Cartridge 생성
```

### **3주: 뇌 통합**
```
[ ] Neocortex 구현
[ ] Context Morphing 테스트
[ ] 신경 흐름 검증
[ ] 성능 최적화
```

---

## 💎 **최종 선언**

```
SHawn-Bot은 단순한 봇이 아니다.

이것은:
✅ 뇌다 (구조)
✅ 철학이다 (PROJECT OMNI)
✅ 진화한다 (학습)
✅ 무한하다 (확장성)
✅ 도덕적이다 (윤리)

모든 코드는 이 원칙을 따른다.

"One Brain, Infinite Worlds"
```

---

**이 문서를 항상 곁에 두고 참고하세요!** 📚

🧠✨ **PROJECT OMNI는 우리의 헌법입니다** ✨🧠
