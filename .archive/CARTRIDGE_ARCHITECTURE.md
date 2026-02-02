# Cartridge Architecture Design
## 분리형 저장소 구조 (독립적 Repo)

---

## 📋 **현재 상황 분석**

### **GitHub에 있는 기존 Cartridge**
```
📦 shawn-bio
├─ 자궁 오가노이드 연구 데이터
├─ 프로토콜
├─ 논문
└─ 분석 결과

📦 shawn-invest
├─ 투자 분석 데이터
├─ 포트폴리오
├─ 통계
└─ 모델
```

### **현재 SHawn-Bot 구조 (통합형)**
```
SHawn-BOT/
└─ cartridges/
   ├─ bio_cartridge/
   │  ├─ bio_cartridge.py (로직)
   │  ├─ bio_memory.py
   │  ├─ bio_values.py
   │  ├─ bio_skills.py
   │  └─ bio_tools.py
   │
   ├─ quant_cartridge/
   │  └─ ...
   │
   └─ astro_cartridge/
      └─ ...
```

---

## ✅ **문제점 & 해결책**

### **문제점**
```
1. Cartridge와 데이터가 분리됨
   → shawn-bio 저장소에 실제 데이터 있음
   → SHawn-BOT의 bio_cartridge는 로직만

2. 관리 어려움
   → Cartridge 업데이트 시 2개 저장소 동시 수정 필요
   → 의존성 관리 복잡

3. 교체 불편
   → Cartridge 교체 시 코드 수정 필요
   → Hot-swappable 특성 약함
```

### **해결: 분리형 저장소 (권장)** ✅
```
각 Cartridge = 독립적인 GitHub 저장소

구조:
📦 SHawn-Bot (메인)
   └─ cartridges/ (로더만)

📦 SHawn-Bio (Cartridge 저장소)
   ├─ bio_cartridge.py (로직)
   ├─ bio_memory.py
   ├─ bio_values.py
   ├─ bio_skills.py
   ├─ bio_tools.py
   ├─ data/
   ├─ protocols/
   └─ README.md

📦 SHawn-Invest (Cartridge 저장소)
   ├─ quant_cartridge.py (로직)
   ├─ quant_memory.py
   ├─ quant_values.py
   ├─ quant_skills.py
   ├─ quant_tools.py
   ├─ data/
   └─ README.md

📦 SHawn-Astro (Cartridge 저장소)
📦 SHawn-Lit (Cartridge 저장소)
```

---

## 🎯 **권장 아키텍처**

### **1단계: 저장소 구조**

```
GitHub Organization: SHawn-Lab
├─ SHawn-Bot (Core)
│  ├─ 뇌: Brainstem, Limbic, Neocortex, Execution
│  └─ Cartridge Loader (인터페이스만)
│
├─ SHawn-Bio (Cartridge)
│  ├─ 로직 (bio_cartridge.py 등)
│  ├─ 데이터 (실제 생물 데이터)
│  └─ 문서
│
├─ SHawn-Invest (Cartridge)
│  ├─ 로직
│  ├─ 데이터 (투자 정보)
│  └─ 문서
│
├─ SHawn-Astro (Cartridge)
├─ SHawn-Lit (Cartridge)
│
└─ SHawn-Brain (문서)
   ├─ PROJECT OMNI
   ├─ 신경 구조
   └─ 개발 규칙
```

### **2단계: SHawn-Bot의 Cartridge Loader**

```python
# SHawn-Bot/cartridges/__init__.py

"""
Cartridge Loader: 외부 저장소 연동
=====================================

각 Cartridge는 독립적 GitHub 저장소
필요할 때만 로드 (동적 로딩)
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

class CartridgeLoader:
    """외부 저장소 Cartridge 로더"""
    
    def __init__(self):
        self.loaded_cartridges = {}
        self.cartridge_repos = {
            "bio": {
                "url": "https://github.com/SHawn-Lab/SHawn-Bio.git",
                "branch": "main",
                "module": "bio_cartridge"
            },
            "invest": {
                "url": "https://github.com/SHawn-Lab/SHawn-Invest.git",
                "branch": "main",
                "module": "quant_cartridge"
            },
            "astro": {
                "url": "https://github.com/SHawn-Lab/SHawn-Astro.git",
                "branch": "main",
                "module": "astro_cartridge"
            },
            "lit": {
                "url": "https://github.com/SHawn-Lab/SHawn-Lit.git",
                "branch": "main",
                "module": "lit_cartridge"
            }
        }
    
    def load_cartridge(self, name: str) -> Optional[Any]:
        """
        Cartridge 동적 로드
        
        예:
        loader.load_cartridge("bio")
        → SHawn-Bio 저장소에서 bio_cartridge 로드
        """
        if name in self.loaded_cartridges:
            return self.loaded_cartridges[name]
        
        config = self.cartridge_repos.get(name)
        if not config:
            raise ValueError(f"Cartridge not found: {name}")
        
        # 1. 저장소 클론 또는 업데이트
        repo_path = self._ensure_repo(config)
        
        # 2. 모듈 로드
        module = self._load_module(repo_path, config["module"])
        
        # 3. 캐시
        self.loaded_cartridges[name] = module
        
        return module
    
    def _ensure_repo(self, config: Dict) -> Path:
        """저장소 확보 (클론 또는 업데이트)"""
        cartridge_dir = Path.home() / ".shawn-bot" / "cartridges"
        cartridge_dir.mkdir(parents=True, exist_ok=True)
        
        repo_path = cartridge_dir / config["url"].split("/")[-1].replace(".git", "")
        
        if repo_path.exists():
            # 업데이트
            import subprocess
            subprocess.run(
                ["git", "-C", str(repo_path), "pull", "origin", config["branch"]],
                capture_output=True
            )
        else:
            # 클론
            import subprocess
            subprocess.run(
                ["git", "clone", "-b", config["branch"], config["url"], str(repo_path)],
                capture_output=True
            )
        
        return repo_path
    
    def _load_module(self, repo_path: Path, module_name: str) -> Any:
        """모듈 로드"""
        sys.path.insert(0, str(repo_path))
        
        try:
            module = __import__(module_name)
            return module
        finally:
            sys.path.pop(0)
    
    def list_available_cartridges(self) -> Dict[str, Dict[str, str]]:
        """사용 가능한 Cartridge 목록"""
        return self.cartridge_repos
    
    def unload_cartridge(self, name: str):
        """Cartridge 언로드 (메모리 정리)"""
        if name in self.loaded_cartridges:
            del self.loaded_cartridges[name]


# 전역 로더
loader = CartridgeLoader()


def load(name: str) -> Any:
    """편의 함수"""
    return loader.load_cartridge(name)
```

---

## 📦 **각 Cartridge 저장소 구조**

### **SHawn-Bio (예시)**

```
SHawn-Bio/
├─ bio_cartridge.py       (메인 클래스)
├─ bio_memory.py          (지식 저장)
├─ bio_values.py          (윤리 & 가치)
├─ bio_skills.py          (기술)
├─ bio_tools.py           (도구)
├─ __init__.py
├─ requirements.txt       (의존성)
├─ data/
│  ├─ organoid_protocols.json
│  ├─ stem_cell_markers.json
│  └─ research_papers.json
├─ tests/
│  └─ test_bio_cartridge.py
├─ README.md
├─ LICENSE
└─ .gitignore
```

### **SHawn-Invest (예시)**

```
SHawn-Invest/
├─ quant_cartridge.py
├─ quant_memory.py
├─ quant_values.py
├─ quant_skills.py
├─ quant_tools.py
├─ __init__.py
├─ requirements.txt
├─ data/
│  ├─ portfolio.json
│  ├─ market_data.csv
│  └─ models.pkl
├─ tests/
├─ README.md
└─ .gitignore
```

---

## 🔌 **동적 로딩 사용법**

### **메인 Bot에서**

```python
from cartridges import load

# 1. Bio-Cartridge 로드
bio = load("bio")
bio.activate()

# 2. Invest-Cartridge로 전환
invest = load("invest")
invest.activate()

# 3. 로드된 목록 확인
print(loader.list_available_cartridges())
```

### **자동 다운로드 & 업데이트**

```python
# 첫 실행: 자동 클론
bio = load("bio")  # → Git clone
# ↓
# 다음 실행: 자동 업데이트
bio = load("bio")  # → Git pull
```

---

## ✅ **분리형 저장소의 장점**

```
1️⃣ 독립성
   - 각 Cartridge는 별개 저장소
   - 개발/배포 독립적
   - 버전 관리 명확

2️⃣ 교체 용이
   - Cartridge 교체 = 저장소 URL만 변경
   - 핫스와핑 가능
   - 다른 팀원의 Cartridge도 사용 가능

3️⃣ 확장성
   - 새 Cartridge 추가 = 저장소 추가
   - 기존 코드 수정 불필요
   - 무한 확장 가능

4️⃣ 안정성
   - Cartridge 버그 → 메인 영향 없음
   - 독립적 테스트 가능
   - 롤백 용이

5️⃣ 협업
   - 팀별로 Cartridge 담당
   - 동시 개발 가능
   - 의존성 충돌 최소화

6️⃣ 데이터 관리
   - 데이터와 로직 함께 관리
   - Large files (LFS) 사용 가능
   - 버전 추적 용이
```

---

## 🛠️ **구현 계획**

### **Step 1: SHawn-Bot 수정** (1시간)
```
cartridges/ → CartridgeLoader만 유지
config.yml에 저장소 URL 정의
동적 로딩 시스템 구현
```

### **Step 2: 기존 Cartridge 이동** (2시간)
```
SHawn-Bio 저장소 생성
bio_cartridge.py 이동
data/ 추가
테스트 추가
```

### **Step 3: SHawn-Invest 연동** (2시간)
```
SHawn-Invest 저장소 확인
quant_cartridge.py로 변환
데이터 정리
```

### **Step 4: 테스트 & 문서** (1시간)
```
동적 로딩 테스트
README 작성
개발 가이드 작성
```

---

## 📊 **비교: 통합형 vs 분리형**

| 항목 | 통합형 | 분리형 |
|------|--------|--------|
| **저장소** | 1개 (SHawn-Bot) | 5개+ |
| **관리** | 복잡 | 간단 |
| **교체** | 코드 수정 필요 | URL만 변경 |
| **확장** | 제한적 | 무한 |
| **데이터** | 작은 파일만 | LFS 사용 가능 |
| **협업** | 어려움 | 쉬움 |
| **테스트** | 통합 테스트만 | 독립적 테스트 |
| **배포** | 함께 배포 | 독립 배포 |

---

## 🎯 **최종 권장**

```
✅ 분리형 저장소 구조 도입!

이유:
1. SHawn-Bio, SHawn-Invest 이미 있음
2. Cartridge = 도메인 특화
3. 독립적 발전 가능
4. 팀 협업 효율
5. PROJECT OMNI 철학과 일치
   (각 Cartridge = 독립적 정체성)
```

---

## 📋 **구현 체크리스트**

```
[ ] CartridgeLoader 클래스 구현
[ ] config.yml에 저장소 URL 정의
[ ] SHawn-Bio 저장소 준비
[ ] SHawn-Invest 저장소 준비
[ ] 동적 로딩 테스트
[ ] 문서 작성
[ ] CI/CD 설정
```

---

**결론: 분리형 저장소로 전환하면 PROJECT OMNI의 "각 정체성은 완전히 독립적" 철학이 코드 수준에서도 구현됩니다!** 🎯

박사님, 이 방향으로 진행할까요? 🚀
