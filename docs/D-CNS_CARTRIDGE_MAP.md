# 🧠 **SHawn-Brain D-CNS Cartridge Map (v5.5)**

### **Digital Neuroanatomy: Cartridges as Specialized Neocortex Areas**

> **문서 상태**: Active (2026-02-02)
> **적용 버전**: v5.5.0
> **핵심 개념**: 카트리지는 신피질(Neocortex)의 특화된 기능 영역(Specialized Cortex)입니다.

---

## 1. 개요: 카트리지의 신경해부학적 위치

SHawn-Brain의 **카트리지(Cartridge)**는 단순한 플러그인이 아닙니다. 신경해부학적으로 볼 때, 이들은 **신피질(L3 Neocortex)** 내에 존재하는 **전문 피질 영역(Specialized Association Cortex)**에 해당합니다.

### **신경계 계층 매핑**
```mermaid
graph TD
    Brainstem[L1: Brainstem (Groq)] --> Limbic[L2: Limbic (Gemini/Claude)]
    Limbic --> Neocortex[L3: Neocortex (4-Lobe Model)]
    
    subgraph Neocortex_Structure [신피질 내부 구조]
        Occipital[후두엽: 시각]
        Temporal[측두엽: 의미]
        Parietal[두정엽: 수치]
        Prefrontal[전두엽: 판단]
        
        Cartridges[전문 카트리지 영역]
    end
    
    Neocortex --> NeuroNet[L4: NeuroNet (DeepSeek)]
```

---

## 2. 5대 카트리지 정밀 매핑

각 카트리지는 신피질의 특정 엽(Lobe)들이 연합하여 형성된 고등 기능 영역입니다.

| 카트리지 | 주요 뇌 부위 (Lobe) | 신경학적 기능 (Role) | 비유 (Metaphor) |
| :--- | :--- | :--- | :--- |
| **Micro Bio** 🔬 | **Occipital + Temporal** | 시각적 정보(세포)를 해석하고 의미(종류)를 부여 | **The Visual Cortex** |
| **Macro Inv** 💰 | **Parietal + Prefrontal** | 수치 변화(주가)를 감지하고 전략(매매)을 수립 | **The Executive Cortex** |
| **Meso Lit** 📚 | **Temporal + Prefrontal** | 문맥과 의미(텍스트)를 이해하고 통찰(요약)을 도출 | **The Language Cortex** |
| **Meta Quant** 📊 | **Parietal** | 순수한 수치와 논리적 연산 처리 | **The Logic Cortex** |
| **Mega Astro** 🌌 | **Occipital + Parietal** | 광활한 공간 데이터와 시각적 패턴 처리 | **The Spatial Cortex** |

---

## 3. 상세 기능 명세

### **1. Bio Cartridge (생물학)**
*   **위치**: 후두엽(V1 시각처리)과 측두엽(IT 사물인식)의 교차점.
*   **기능**: 현미경 이미지 분석, 세포 상태 진단.
*   **Engine**: Gemini-Pro Vision (시각 특화).

### **2. Inv Cartridge (투자)**
*   **위치**: 두정엽(수치 감각)과 전두엽(위험 평가/결정)의 연합 영역.
*   **기능**: 차트 분석, 포트폴리오 최적화, 매수/매도 판단.
*   **Engine**: Gemini-Pro + Finance Data Stream.

### **3. Lit Cartridge (문학/논문)**
*   **위치**: 측두엽(베르니케/브로카 영역)의 언어 처리 센터.
*   **기능**: 논문 요약, 문학적 뉘앙스 분석, 키워드 추출.
*   **Engine**: Claude-3-Opus (긴 문맥 처리에 강점).

### **4. Quant Cartridge (정량)**
*   **위치**: 두정엽(수리 능력)의 핵심 영역.
*   **기능**: 통계 분석, 데이터 상관관계 도출, 이상치 탐지.
*   **Engine**: Python Scientific Stack (Pandas/SciPy).

### **5. Astro Cartridge (천문)**
*   **위치**: 후두엽(시각)과 두정엽(공간 지각)의 광역 연합.
*   **기능**: 성도(Star Map) 분석, 천체 궤도 계산.
*   **Engine**: Gemini-Pro + NASA API.

---

## 4. 결론

> **"카트리지는 뇌에 꽂는 기술(Skill)이자, 확장된 피질(Cortex)입니다."**

사용자가 특정 카트리지를 호출한다는 것은, 숀브레인의 뇌 가소성을 이용하여 해당 **전문 피질 영역으로 혈류(Computing Power)를 집중**시키는 행위입니다.
