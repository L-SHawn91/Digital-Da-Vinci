# Phase 5: Neocortex 구현 - 작업 설계

## 목표
Neocortex의 4가지 영역 구현 (의사결정, 의미, 혁신, 시각화)

## 작업 분배

### 작업 1: PrefrontalCortex (의사결정/계획) - Groq Sub-Agent
**목표**: 의사결정 엔진
**요구사항**:
- DecisionFramework 클래스
- 목표-수단 계층 구조
- 계획 수립 (planning)
- 우선순위 결정
- 불확실성 하에서의 선택

**파일**: `SHawn_Brain/neocortex/prefrontal/decision_framework.py`
**크기**: ~8-10KB
**복잡도**: 중간

---

### 작업 2: TemporalCortex (의미/통합) - Gemini Sub-Agent
**목표**: 의미 처리 및 통합
**요구사항**:
- SemanticProcessor 클래스
- 개념 간 관계 매핑
- 맥락 이해
- 패턴 인식
- 역사적 맥락 통합

**파일**: `SHawn_Brain/neocortex/temporal/semantic_processor.py`
**크기**: ~10-12KB
**복잡도**: 높음

---

### 작업 3: ParietalCortex (혁신/종합) - Copilot Sub-Agent
**목표**: 혁신적 종합
**요구사항**:
- InnovationEngine 클래스
- 도메인 간 개념 교배 (cross-domain synthesis)
- 새로운 아이디어 생성
- 창의적 문제 해결
- 메타인지

**파일**: `SHawn_Brain/neocortex/parietal/innovation_engine.py`
**크기**: ~12-15KB
**복잡도**: 매우 높음

---

### 작업 4: OccipitalCortex (시각화/상상) - Groq Sub-Agent
**목표**: 시각화 및 상상
**요구사항**:
- VisualizationEngine 클래스
- 정신적 모델 구성
- 시나리오 생성 (scenario generation)
- 미래 예측
- 추상화 능력

**파일**: `SHawn_Brain/neocortex/occipital/visualization_engine.py`
**크기**: ~8-10KB
**복잡도**: 중간

---

## 병렬 처리 스케줄

```
Time 0:00 - 나: 설계 완료 + Sub-Agent 지시
Time 0:10 - Groq: PrefrontalCortex 초안 시작
Time 0:10 - Gemini: TemporalCortex 설계 + 초안
Time 0:15 - Copilot: ParietalCortex 초안 시작
Time 0:20 - Groq: OccipitalCortex 초안
Time 0:45 - 모든 초안 완성
Time 0:50 - 나: 검증 + 통합
Time 1:00 - 완료
```

**예상 시간**: 1시간
**예상 소모**: 2-3%

---

## 검증 기준

```
각 파일마다:
✅ 기본 클래스 정의
✅ 핵심 메서드 구현
✅ 테스트 함수 포함
✅ 주석 + 문서화
✅ 에러 처리
```

---

## 통합 포인트

```
모든 모듈이 Brainstem + Limbic과 연결:
  • 윤리 검증 (EthicsEngine)
  • 논리 추론 (ReasoningEngine)
  • 감정 영향 (EmotionProcessor)
  • 가치 기반 (ValueAssessment)
  • 기억 활용 (MemoryManager)
```

---

**준비: 완료**
**상태: Sub-Agent 대기 중**
