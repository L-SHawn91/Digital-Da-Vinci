# src 폴더 구조: 의미와 프로젝트 레이아웃

## 🎯 **"src"의 의미**

### **src = Source Code (소스 코드)**

```
전체 프로젝트 구조:
project_root/
├─ src/                    ← 실제 작동하는 코드
│  ├─ brain/              (뇌 코드)
│  ├─ cartridges/         (카트리지 코드)
│  ├─ utils.py            (유틸리티)
│  └─ __init__.py
│
├─ tests/                 ← 테스트 코드
├─ docs/                  ← 문서
├─ data/                  ← 데이터 (git 미포함)
├─ .gitignore            ← git이 무시할 파일
├─ requirements.txt       ← 필요한 라이브러리
├─ README.md             ← 프로젝트 설명
└─ main.py               ← 진입점
```

---

## 📦 **src 폴더의 역할**

### **왜 src를 사용할까?**

```
✅ 전문적 구조
   - 소스 코드를 한곳에 모음
   - 테스트, 문서와 분리
   - 패키지화 및 배포 용이

✅ 명확한 분리
   src/       = "실제 작동하는 코드"
   tests/     = "테스트 코드"
   docs/      = "문서"
   data/      = "데이터 파일"

✅ 패키징/배포 시 편리
   - Python 패키지로 배포할 때
   - pip install로 설치 가능
   - from src import ... 로 임포트

✅ 대규모 프로젝트 표준
   - Google, Meta, Microsoft 등
   - 오픈소스 프로젝트 표준
```

---

## 🧠 **SHawn-Brain의 src 구조**

### **완전한 구조**

```
SHawn-Brain/
│
├─ src/                           ← "소스 코드" 폴더
│  │
│  ├─ brain/                      (D-CNS 신경계 코드)
│  │  ├─ __init__.py
│  │  ├─ brain_core/
│  │  │  ├─ brainstem/            (L1: 뇌간)
│  │  │  ├─ limbic_system/        (L2: 변린계)
│  │  │  └─ cartridge_system/     (카트리지 관리)
│  │  │
│  │  ├─ neocortex/               (L3: 신피질)
│  │  │  ├─ prefrontal/           (전두엽)
│  │  │  ├─ temporal/             (측두엽)
│  │  │  ├─ parietal/             (두정엽)
│  │  │  └─ occipital/            (후두엽)
│  │  │
│  │  └─ neuronet/                (L4: 신경망)
│  │
│  ├─ cartridges/                 (카트리지 - 전문 기능)
│  │  ├─ __init__.py
│  │  ├─ bio/                     (생물학 카트리지)
│  │  ├─ inv/                     (투자 카트리지)
│  │  ├─ lit/                     (문학 카트리지)
│  │  ├─ quant/                   (정량 카트리지)
│  │  └─ astro/                   (천문 카트리지)
│  │
│  ├─ utils/                      (유틸리티 함수)
│  │  ├─ __init__.py
│  │  ├─ helpers.py
│  │  ├─ config.py
│  │  └─ logger.py
│  │
│  └─ __init__.py
│
├─ tests/                         ← "테스트 코드"
│  ├─ test_brain.py
│  ├─ test_cartridges.py
│  └─ integration/
│
├─ docs/                          ← "문서"
│  ├─ README.md
│  ├─ API.md
│  └─ ARCHITECTURE.md
│
├─ data/                          ← "데이터" (git 미포함)
│  ├─ models/
│  ├─ datasets/
│  └─ logs/
│
├─ .gitignore                    ← git이 무시할 파일
├─ requirements.txt              ← 필요한 라이브러리
├─ setup.py                      ← 패키지 설정
├─ README.md                     ← 프로젝트 소개
└─ main.py                       ← 진입점
```

---

## 💡 **Import 방식**

### **src를 사용할 때의 import**

```python
# src/brain/brain_core/brainstem/initializer.py 에서:

from src.brain.neocortex.prefrontal import decision_maker
from src.cartridges.bio import bio_cartridge
from src.utils import logger

# 또는 (프로젝트 루트에서 실행할 때):

from brain.neocortex.prefrontal import decision_maker
from cartridges.bio import bio_cartridge
```

### **src 없이 하는 경우**

```
project_root/
├─ brain/            ← src/ 폴더 없음
├─ cartridges/
├─ utils/
├─ tests/
└─ main.py

from brain.neocortex import ...
```

---

## 🎯 **SHawn-Brain에서 src를 사용하는 이유**

### **전문적 구조의 이점**

```
1️⃣ 명확한 분리
   - src/: 실제 작동 코드
   - tests/: 테스트
   - docs/: 문서
   - data/: 데이터

2️⃣ 배포 가능
   # requirements.txt에 추가
   -e .
   
   # 그러면 설치 가능
   pip install -e .
   
   # 그러면 어디서나 import 가능
   import src.brain
   from src.cartridges import bio_cartridge

3️⃣ 팀 협력에 유리
   - 구조가 명확
   - 어느 파일이 "실제 코드"인지 알기 쉬움
   - 누가 봐도 구조 이해 가능

4️⃣ 오픈소스 표준
   - GitHub의 대규모 프로젝트들이 사용
   - 새로운 개발자도 쉽게 이해
```

---

## 📊 **구체적 예시: Bio Cartridge**

### **파일 위치 & Import**

```python
# 파일 위치
src/cartridges/bio/bio_cartridge.py

# 내용
from src.brain.neocortex.occipital import visual_processor
from src.brain.neocortex.temporal import memory_manager
from src.utils import logger

def analyze_cell_image(image_path):
    logger.info(f"세포 이미지 분석 시작: {image_path}")
    
    # Occipital (후두엽) 호출
    visual_features = visual_processor.extract_features(image_path)
    
    # Temporal (측두엽) 호출
    learned_patterns = memory_manager.get_cell_patterns()
    
    result = {
        'visual': visual_features,
        'patterns': learned_patterns
    }
    
    logger.info(f"분석 완료")
    return result
```

---

## 🔄 **Phase 1에서 src 사용**

### **카트리지 통합 시 정확한 경로**

```bash
# Step 2: Bio Cartridge 통합
cd /Users/soohyunglee/.openclaw/workspace

# 파일 위치 확인
ls -la src/cartridges/bio/

# bio_cartridge.py 생성
cat > src/cartridges/bio/bio_cartridge.py << 'EOF'
"""Bio Cartridge - 생물학 분석"""

from src.brain.neocortex.occipital import visual_processor
from src.brain.neocortex.temporal import memory_manager

def analyze_cell_image(image_path):
    visual = visual_processor.extract_features(image_path)
    patterns = memory_manager.get_cell_patterns()
    return {'visual': visual, 'patterns': patterns}
EOF

# bio_interface.py 생성
cat > src/cartridges/bio/bio_interface.py << 'EOF'
"""Bio Cartridge Interface"""

from .bio_cartridge import analyze_cell_image

__all__ = ['analyze_cell_image']
EOF

# __init__.py 생성
cat > src/cartridges/bio/__init__.py << 'EOF'
from .bio_interface import analyze_cell_image
__all__ = ['analyze_cell_image']
EOF

# 테스트
pytest src/cartridges/bio/tests/

# 커밋
git add src/cartridges/bio/
git commit -m "feat: Bio Cartridge 추가 (src/cartridges/bio/)"
```

---

## 📈 **현재 구조 정리**

### **Phase 1 전**

```
현재 프로젝트:
SHawn_Brain/
├─ brain_core/
├─ neocortex/
├─ cartridges/
├─ utilities/
└─ [기타]

문제: 
- src/가 없음
- 구조가 명확하지 않음
```

### **Phase 1 후 (목표)**

```
정리된 프로젝트:
SHawn-Brain/
├─ src/                 ← 추가!
│  ├─ brain/
│  ├─ cartridges/
│  └─ utils/
├─ tests/
├─ docs/
├─ data/
├─ requirements.txt
└─ README.md

장점:
- 구조 명확
- 전문적
- 배포 가능
```

---

## ✅ **결론**

### **src의 의미**

```
src = Source Code (소스 코드)

역할:
1. 실제 작동하는 코드를 한곳에 모음
2. 테스트, 문서와 분리
3. 전문적이고 표준적인 구조
4. 배포 및 패키징 용이
```

### **Phase 1에서의 역할**

```
src/brain/neocortex/     ← 4개 엽 (도구)
src/cartridges/          ← 카트리지 (역할)

카트리지가 neocortex를 import해서 사용:
from src.brain.neocortex.occipital import ...
from src.brain.neocortex.prefrontal import ...
```

---

**상태: src의 의미와 구조 명확화** ✅
**다음: Phase 1 실행 시작!** 🚀
