# SHawn-BIO & SHawn-INV 카트리지화 계획
## 기존 저장소를 Cartridge 구조로 개선

---

## 📊 **현재 상태 분석**

### **SHawn-BIO (생물학 전문)**
```
SHawn-BIO/
├─ tools/
│  ├─ sbi_pipeline.py (FAISS 벡터 검색)
│  ├─ research_engine.py (메타 분석 엔진)
│  ├─ verify_brain.py (검증)
│  └─ test_sbi_research.py (테스트)
├─ knowledge/
│  ├─ faiss_index.bin (벡터 인덱스)
│  └─ knowledge_data.pkl (지식 데이터)
├─ analysis/
│  └─ (분석 결과)
├─ requirements.txt
├─ manifest.yaml
└─ README.md
```

**현재 역할**: 자궁 오가노이드 & 생물학 분석
**강점**: FAISS 벡터 검색, 메타 분석
**데이터**: 논문, 연구 프로토콜

---

### **SHawn-INV (투자 전문)**
```
SHawn-INV/
├─ tools/
│  ├─ publish_reports.py (리포트 생성)
│  ├─ auto_commit.py (자동 커밋)
│  ├─ run_all.py (전체 실행)
│  ├─ Common_Lib/ (공통 라이브러리)
│  ├─ KR_Market/ (한국 시장)
│  └─ US_Market/ (미국 시장)
├─ analysis/
│  ├─ Market_Briefing_202601.md
│  ├─ Investment_Log_202601.md
│  └─ Bio_Insight_*.md
├─ knowledge/
│  └─ AI_Rules_Template.md
├─ pyproject.toml
├─ manifest.yaml
└─ README.md
```

**현재 역할**: Dual Quant System (주식 분석 & 리포트)
**강점**: 실시간 데이터, 자동 리포트
**데이터**: 시장 데이터, 기관 수급

---

## 🎯 **카트리지화 목표**

### **목표**
```
SHawn-BIO & SHawn-INV를 SHawn-BOT의 Cartridge로 완벽 통합

1. 로직 분리
   - tools/ → cartridge 로직으로 변환
   - Python 클래스 기반으로 정리

2. 구조 표준화
   - bio_cartridge.py (메인)
   - bio_memory.py (지식 저장)
   - bio_values.py (윤리 & 우선순위)
   - bio_skills.py (기술)
   - bio_tools.py (도구)

3. 통합
   - SHawn-BOT의 CartridgeLoader와 호환
   - Context Morphing 지원
   - 독립적 테스트 가능
```

---

## 📦 **SHawn-BIO 카트리지화**

### **Step 1: 구조 리팩토링**

```
SHawn-BIO/
├─ bio_cartridge.py         ← 새로 생성 (메인 클래스)
├─ bio_memory.py            ← 새로 생성 (지식 저장)
├─ bio_values.py            ← 새로 생성 (생물학 윤리)
├─ bio_skills.py            ← 새로 생성 (기술)
├─ bio_tools.py             ← 새로 생성 (도구)
├─ __init__.py              ← 새로 생성
├─ tools/ (기존)
│  ├─ sbi_pipeline.py       ← research_engine.py를 bio_tools.py로 이동
│  ├─ research_engine.py    ← bio_skills.py로 이동
│  ├─ verify_brain.py       ← 유지
│  └─ test_sbi_research.py  ← tests/로 이동
├─ knowledge/ (기존)
│  ├─ faiss_index.bin       ← bio_memory.py에서 로드
│  └─ knowledge_data.pkl
├─ tests/ (새로 생성)
│  ├─ test_bio_cartridge.py ← 새로 생성
│  └─ test_sbi_research.py  ← 기존 이동
├─ requirements.txt
└─ README.md
```

### **Step 2: 코드 매핑**

#### **bio_memory.py** (Hippocampus)
```python
# 기존: knowledge/ 폴더의 faiss_index.bin, knowledge_data.pkl
# 새로운: BioMemory 클래스

class BioMemory:
    """
    생물학 지식 저장소
    
    - FAISS 벡터 검색 (sbi_pipeline.py)
    - 논문 데이터베이스
    - 프로토콜 데이터베이스
    - 연구 히스토리
    """
    
    def __init__(self):
        self.faiss_index = self._load_faiss()  # knowledge/faiss_index.bin
        self.knowledge_data = self._load_pkl()  # knowledge/knowledge_data.pkl
    
    def search(self, query: str) -> List[Dict]:
        """논문 & 데이터 검색 (sbi_pipeline 사용)"""
        pass
    
    def add_research(self, data: Dict):
        """새로운 연구 추가"""
        pass
```

#### **bio_values.py** (Amygdala)
```python
class BioValues:
    """
    생물학 연구 가치 & 윤리
    
    - 생명 윤리 (Brainstem과 연동)
    - 연구 우선순위
    - 재현성 필수성
    - 번역 목표 (임상 응용)
    """
    
    def evaluate_research_priority(self, topic: str) -> float:
        """연구 우선순위 평가"""
        pass
    
    def apply_ethics_constraints(self, experiment: Dict) -> bool:
        """생명 윤리 검증 (동물 실험 최소화 등)"""
        pass
```

#### **bio_skills.py** (Cerebellum)
```python
class BioSkills:
    """
    생물학 분석 기술
    
    - research_engine.py (메타 분석)
    - 실험 설계
    - 데이터 해석
    - 통계 분석
    """
    
    def design_experiment(self, hypothesis: str) -> Dict:
        """실험 설계 (research_engine 사용)"""
        pass
    
    def analyze_data(self, raw_data: List) -> Dict:
        """데이터 분석"""
        pass
    
    def validate_reproducibility(self, results: Dict) -> bool:
        """재현성 검증"""
        pass
```

#### **bio_tools.py** (Motor)
```python
class BioTools:
    """
    생물학 외부 도구 & API
    
    - sbi_pipeline.py (FAISS 검색)
    - PubMed 문헌 검색
    - 유전자 정보 (GeneOntology 등)
    """
    
    def search_literature(self, keywords: List[str]) -> List[Dict]:
        """sbi_pipeline 사용"""
        pass
    
    def fetch_gene_data(self, gene: str) -> Dict:
        """유전자 정보 조회"""
        pass
```

#### **bio_cartridge.py** (Main)
```python
class BioCartridge:
    """
    Bio-Cartridge: 생물학 전문화 모드
    
    Context Morphing 지원:
    - activate(): 활성화
    - deactivate(): 비활성화
    - process_query(): 질문 처리
    """
    
    def __init__(self):
        self.memory = BioMemory()
        self.values = BioValues()
        self.skills = BioSkills()
        self.tools = BioTools()
    
    def activate(self):
        """활성화: "BIO-CARTRIDGE ACTIVATED"
        
        수행:
        - FAISS 인덱스 로드
        - 생명 윤리 제약 활성화
        - 연구 프로토콜 준비
        """
        pass
    
    def process_query(self, query: str) -> Dict:
        """자궁 오가노이드 & 생물학 질문 처리"""
        pass
```

---

## 📈 **SHawn-INV 카트리지화**

### **Step 1: 구조 리팩토링**

```
SHawn-INV/
├─ quant_cartridge.py       ← 새로 생성 (메인)
├─ quant_memory.py          ← 새로 생성 (시장 데이터)
├─ quant_values.py          ← 새로 생성 (투자 철학)
├─ quant_skills.py          ← 새로 생성 (분석 기술)
├─ quant_tools.py           ← 새로 생성 (시장 도구)
├─ __init__.py              ← 새로 생성
├─ tools/ (기존)
│  ├─ run_all.py            ← quant_skills.py로 이동
│  ├─ publish_reports.py    ← quant_tools.py로 이동
│  ├─ auto_commit.py        ← 유지 (CI/CD)
│  ├─ Common_Lib/           ← quant_tools.py에 통합
│  ├─ KR_Market/            ← quant_memory.py 데이터
│  └─ US_Market/            ← quant_memory.py 데이터
├─ analysis/ (기존)
│  └─ (리포트 결과)
├─ tests/ (새로 생성)
│  └─ test_quant_cartridge.py
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

### **Step 2: 코드 매핑**

#### **quant_memory.py** (Hippocampus)
```python
class QuantMemory:
    """
    시장 & 투자 데이터 저장소
    
    - 실시간 시장 데이터
    - 기관 & 외국인 수급
    - 매크로 경제 지표
    - 뉴스 감성 점수
    """
    
    def load_kr_market(self) -> Dict:
        """KR_Market/ 데이터"""
        pass
    
    def load_us_market(self) -> Dict:
        """US_Market/ 데이터"""
        pass
    
    def get_expert_score(self, stock: str) -> float:
        """기술 분석 스코어 (40%)"""
        pass
```

#### **quant_values.py** (Amygdala)
```python
class QuantValues:
    """
    투자 철학 & 우선순위
    
    - Sovereign Alpha 테마
    - 리스크 관리 원칙
    - 포트폴리오 배분 철학
    - 수익 목표
    """
    
    def evaluate_investment_priority(self, stock: str) -> float:
        """투자 우선순위"""
        pass
    
    def apply_risk_constraints(self, portfolio: Dict) -> bool:
        """리스크 제약 검증"""
        pass
```

#### **quant_skills.py** (Cerebellum)
```python
class QuantSkills:
    """
    정량 분석 기술
    
    - Dual Quant System (Expert 40%, Whale 30%, Macro 20%, News 10%)
    - 백테스팅
    - 포트폴리오 최적화
    """
    
    def analyze_dual_quant(self, stock: str) -> Dict:
        """Dual Quant 분석"""
        pass
    
    def generate_report(self, analysis: Dict) -> str:
        """리포트 생성 (publish_reports.py 사용)"""
        pass
    
    def backtest_strategy(self, strategy: str) -> Dict:
        """전략 백테스팅"""
        pass
```

#### **quant_tools.py** (Motor)
```python
class QuantTools:
    """
    시장 도구 & API
    
    - KRX API
    - US Market API
    - Report Generator
    """
    
    def fetch_kr_data(self, stock: str) -> Dict:
        """한국 주식 데이터"""
        pass
    
    def fetch_us_data(self, ticker: str) -> Dict:
        """미국 주식 데이터"""
        pass
    
    def publish_report(self, analysis: Dict) -> str:
        """리포트 발행"""
        pass
```

#### **quant_cartridge.py** (Main)
```python
class QuantCartridge:
    """
    Quant-Cartridge: 투자 분석 전문화
    
    Context Morphing 지원:
    - activate(): 시장 데이터 로드
    - process_query(): 투자 질문 처리
    - generate_report(): 자동 리포트
    """
    
    def __init__(self):
        self.memory = QuantMemory()
        self.values = QuantValues()
        self.skills = QuantSkills()
        self.tools = QuantTools()
    
    def activate(self):
        """활성화: 시장 모드
        
        수행:
        - 실시간 데이터 로드
        - Dual Quant 준비
        - 포트폴리오 분석 준비
        """
        pass
    
    def generate_report(self) -> str:
        """자동 리포트 생성"""
        pass
```

---

## 🔄 **마이그레이션 체크리스트**

### **SHawn-BIO**
```
[ ] bio_cartridge.py 작성
[ ] bio_memory.py 작성 (FAISS 로드 로직)
[ ] bio_values.py 작성 (생명 윤리)
[ ] bio_skills.py 작성 (research_engine 통합)
[ ] bio_tools.py 작성 (sbi_pipeline 통합)
[ ] __init__.py 작성
[ ] tests/test_bio_cartridge.py 작성
[ ] 기존 tools/ 정리
[ ] requirements.txt 업데이트
[ ] README.md 업데이트
```

### **SHawn-INV**
```
[ ] quant_cartridge.py 작성
[ ] quant_memory.py 작성 (시장 데이터)
[ ] quant_values.py 작성 (투자 철학)
[ ] quant_skills.py 작성 (Dual Quant 통합)
[ ] quant_tools.py 작성 (API 통합)
[ ] __init__.py 작성
[ ] tests/test_quant_cartridge.py 작성
[ ] 기존 tools/ 정리
[ ] pyproject.toml 업데이트
[ ] README.md 업데이트
```

---

## 📊 **작업 예상 시간**

```
SHawn-BIO 카트리지화:
├─ 코드 분석: 1시간
├─ 코드 작성: 3시간
├─ 테스트: 1시간
└─ 소계: 5시간

SHawn-INV 카트리지화:
├─ 코드 분석: 1시간
├─ 코드 작성: 3시간
├─ 테스트: 1시간
└─ 소계: 5시간

SHawn-BOT 연동:
├─ CartridgeLoader 수정: 1시간
├─ 통합 테스트: 2시간
└─ 소계: 3시간

전체: 13시간
```

---

## 🎯 **최종 구조**

```
SHawn-BOT (Core)
├─ brain_core/
├─ neocortex/
├─ execution/
├─ utilities/
└─ cartridges/
   ├─ cartridge_loader.py
   └─ __init__.py (로더만)

📦 SHawn-BIO (Cartridge)
├─ bio_cartridge.py
├─ bio_memory.py (FAISS)
├─ bio_values.py (윤리)
├─ bio_skills.py (분석)
├─ bio_tools.py (도구)
├─ tools/ (유지)
└─ knowledge/ (유지)

📦 SHawn-INV (Cartridge)
├─ quant_cartridge.py
├─ quant_memory.py (시장 데이터)
├─ quant_values.py (투자 철학)
├─ quant_skills.py (분석)
├─ quant_tools.py (도구)
└─ tools/ (유지)
```

---

## 🚀 **다음 단계**

**박사님, 어디서부터 시작할까요?**

1️⃣ **SHawn-BIO 먼저 카트리지화** (5시간)
2️⃣ **SHawn-INV 카트리지화** (5시간)
3️⃣ **SHawn-BOT 통합** (3시간)

→ 13시간으로 완벽한 분리형 구조 완성!
