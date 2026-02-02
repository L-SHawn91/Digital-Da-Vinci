# Contributing to SHawn-Brain D-CNS

Digital Da Vinci 프로젝트에 관심을 가져주셔서 감사합니다! D-CNS 아키텍처를 함께 발전시키기 위한 가이드라인입니다.

## 🤝 기여 방법 (How to Contribute)

### 1. 이슈 리포팅 (Issues)
-   버그를 발견하거나 새로운 기능을 제안하고 싶다면 [Issue](https://github.com/leseichi-max/SHawn-Brain/issues)를 생성해주세요.
-   가능한 구체적으로(재현 단계, 로그 포함) 작성해주시길 바랍니다.

### 2. 풀 리퀘스트 (Pull Requests)
1.  이 저장소를 **Fork** 합니다.
2.  작업 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3.  변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4.  브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5.  **Pull Request**를 생성합니다.

---

## 💻 개발 가이드라인 (Development)

### 코딩 스타일 (Style Guide)
-   Python 코드는 **PEP 8** 표준을 준수합니다.
-   타입 힌트(`typing`) 사용을 권장합니다.
-   주석은 **한국어** 또는 **영어**로 명확하게 작성합니다.

### 테스트 (Testing)
PR을 제출기 전, 반드시 테스트를 통과해야 합니다.
```bash
# 가상환경 활성화
source venv/bin/activate

# 테스트 실행
pytest tests/
```
새로운 기능을 추가할 경우, 관련된 **단위 테스트(Unit Test)**를 반드시 포함해야 합니다.

---

## 📜 라이선스 (License)
이 프로젝트는 **MIT License** 하에 배포됩니다. 기여하신 코드는 자동으로 이 라이선스를 따르게 됩니다.
