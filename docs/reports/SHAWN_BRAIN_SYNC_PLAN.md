# SHawn-Brain 레포 명명법 동기화 실행

## 🎯 **박사님 결정 사항**

```
✅ 메인 레포: SHawn-Brain (GitHub에서 이미 변경됨)
✅ 명명법: 신경계 생물학 기반 (뇌 구조 반영)
✅ 규칙: 모노레포만 SHawn 붙이고 나머지는 떼기

구현:
- 로컬 동기화
- 코드 수정 (import, 링크 등)
- 문서 업데이트
- 배포 설정 변경
```

---

## 📋 **동기화 작업 목록**

### **1️⃣ Git 원격 저장소 동기화 (10분)**

```
현재: origin → https://github.com/leseichi-max/SHawn-BOT.git
변경: origin → https://github.com/leseichi-max/SHawn-Brain.git

작업:
1. git remote set-url origin <새 URL>
2. git fetch origin
3. git checkout main
4. git pull origin main
```

### **2️⃣ 코드 경로 업데이트 (15분)**

```
모든 import 문, 설정 파일 등에서:
- "SHawn-BOT" 제거
- GitHub URL 업데이트
- 배포 경로 업데이트

파일:
- requirements.txt (URL 참조 제거)
- README.md
- .github/workflows/*.yml
- vercel.json
- setup.py (있으면)
```

### **3️⃣ 문서 업데이트 (20분)**

```
- README.md: SHawn-Brain으로 업데이트
- CONTRIBUTING.md: 새 레포 URL
- API 문서: 배포 URL 확인
- 시작 가이드: 명명법 설명 추가
```

### **4️⃣ 내부 신경계 구조 명명 표준화 (30분)**

```
src/ 구조에서:
- 뇌 구조 폴더명 명확화
- 카트리지 명명: cortex-{domain}
- 인터페이스 명명: interface-{type}
- 도구 명명: tools-{purpose}
```

### **5️⃣ CI/CD & 배포 설정 업데이트 (20분)**

```
- GitHub Actions: 새 레포명 반영
- Vercel: 레포 링크 확인
- 환경 변수: 필요시 업데이트
```

---

## 🔄 **실행 계획 (신경계 레벨)**

### **Level 1 (뇌간): 기본 동기화** (9.6/10)

```
✅ Step 1: git remote 업데이트
   └─ origin URL 변경 → SHawn-Brain

✅ Step 2: 로컬 변경사항 확인
   └─ git status
   └─ 깨끗한 상태 확인

✅ Step 3: 원격 동기화
   └─ git fetch origin main
   └─ git pull origin main
```

### **Level 2 (변린계): 코드 업데이트** (9.5/10)

```
✅ Step 4: 파일 검색 & 변경
   └─ "SHawn-BOT" 모든 참조 찾기
   └─ "SHawn-Brain" 또는 뇌 구조명으로 변경

✅ Step 5: 신경계 명명 표준화
   └─ src/brain/brain_core/limbic_system/ ✓ (이미 정함)
   └─ src/cartridges/ 구조 확인
   └─ 모듈 이름 일관성 검증
```

### **Level 3 (신피질): 문서 정리** (9.4/10)

```
✅ Step 6: README.md 업데이트
   └─ "SHawn-Brain" 설명 추가
   └─ D-CNS 신경계 철학 설명
   └─ 뇌 구조 명명법 가이드

✅ Step 7: 배포 관련 문서
   └─ Vercel 설정 확인
   └─ API 문서 업데이트
   └─ 깃허브 링크 수정
```

### **Level 4 (신경망): CI/CD 최적화** (9.8/10 ⭐⭐)

```
✅ Step 8: GitHub Actions 워크플로우
   └─ 레포명 참조 업데이트
   └─ 배포 경로 수정

✅ Step 9: Vercel 배포 설정
   └─ 프로젝트 연결 확인
   └─ 자동 배포 테스트

✅ Step 10: 최종 테스트
   └─ 로컬 빌드 확인
   └─ 배포 파이프라인 작동 확인
```

---

## 💾 **상세 동기화 스크립트**

### **작업 1: Git 원격 저장소 변경**

```bash
# 현재 원격 저장소 확인
git remote -v

# 새 URL로 업데이트
git remote set-url origin https://github.com/leseichi-max/SHawn-Brain.git

# 확인
git remote -v

# 최신 데이터 가져오기
git fetch origin main
git pull origin main
```

### **작업 2: "SHawn-BOT" 문자열 찾아 변경**

```bash
# 모든 파일에서 "SHawn-BOT" 찾기
grep -r "SHawn-BOT" . --include="*.py" --include="*.md" --include="*.yml" --include="*.json" --include="*.txt" --exclude-dir=.git --exclude-dir=__pycache__

# 결과 예상:
# ./README.md: SHawn-BOT is...
# ./.github/workflows/test.yml: repo: SHawn-BOT
# ./requirements.txt: SHawn-BOT
```

### **작업 3: 파일별 변경**

```bash
# README.md
sed -i 's/SHawn-BOT/SHawn-Brain/g' README.md

# GitHub Actions 워크플로우
sed -i 's/SHawn-BOT/SHawn-Brain/g' .github/workflows/*.yml

# 기타 설정 파일
sed -i 's/SHawn-BOT/SHawn-Brain/g' $(find . -name "*.json" -o -name "*.txt" -o -name "*.md" | grep -v ".git")
```

### **작업 4: 신경계 명명법 검증**

```bash
# 뇌 구조 폴더 확인
tree -d -L 2 src/brain/

# 예상 구조:
# src/brain/
# ├─ brain_core/
# │  ├─ brainstem/
# │  ├─ limbic_system/
# │  └─ cartridge_system/
# ├─ neocortex/
# │  ├─ prefrontal/
# │  ├─ temporal/
# │  ├─ parietal/
# │  └─ occipital/
# └─ neuronet/
```

---

## 📝 **업데이트할 파일 목록**

### **우선순위 1: 중요 파일**

```
□ README.md
  - 제목: "SHawn-Brain: Digital Central Nervous System"
  - 설명: D-CNS 신경계 철학
  - 링크: https://github.com/leseichi-max/SHawn-Brain
  
□ .github/workflows/test.yml
  - repository 참조 업데이트
  
□ .github/workflows/deploy.yml
  - repository 참조 업데이트
  
□ vercel.json
  - 배포 설정 확인
```

### **우선순위 2: 문서 파일**

```
□ CONTRIBUTING.md
  - 레포 링크 업데이트
  - 개발 가이드 확인
  
□ docs/API.md
  - API 문서 업데이트
  
□ docs/ARCHITECTURE.md
  - 뇌 구조 명명법 설명 추가
```

### **우선순위 3: 코드 파일**

```
□ src/main.py
  - import 경로 확인
  
□ src/bot/telegram_interface.py
  - 배포 URL 확인
  
□ web/backend/main.py
  - API 엔드포인트 확인
```

---

## ✅ **동기화 체크리스트**

```
Phase 1: Git 동기화
□ git remote set-url 실행
□ git fetch & pull 완료
□ 로컬 상태 깨끗함 확인

Phase 2: 코드 검색 & 변경
□ "SHawn-BOT" 모든 참조 찾기 완료
□ "SHawn-Brain" 또는 명확한 이름으로 변경
□ grep으로 남은 참조 없는지 확인

Phase 3: 문서 업데이트
□ README.md 업데이트 (제목, 링크)
□ CONTRIBUTING.md 업데이트
□ API 문서 링크 확인
□ GitHub 배지/링크 수정

Phase 4: CI/CD 업데이트
□ GitHub Actions 워크플로우 확인
□ Vercel 프로젝트 연결 확인
□ 환경 변수 확인

Phase 5: 최종 검증
□ 로컬 테스트 실행
□ 빌드 성공 확인
□ 배포 파이프라인 작동 확인
□ 모든 링크 정상 작동 확인

완료
□ git commit & push
□ 완료 메시지 작성
```

---

## 🧠 **신경계 명명법 최종 정의**

### **공식 명명 규칙**

```
레포 이름:
└─ SHawn-Brain (모노레포 - 모든 신경 시스템 포함)

내부 폴더 구조 (뇌 해부학 기반):
├─ brainstem (뇌간 - 기본 생존 기능)
├─ limbic_system (변린계 - 감정, 의사결정, 기억)
├─ neocortex (신피질 - 학습, 분석, 고등 기능)
│  ├─ prefrontal (전두엽 - 계획, 의사결정)
│  ├─ temporal (측두엽 - 기억, 음성)
│  ├─ parietal (두정엽 - 통합, 공간)
│  └─ occipital (후두엽 - 시각, 분석)
└─ neuronet (신경망 - 신호 처리, 학습)

카트리지 (피질 영역 특화):
├─ cortex-bio (생물학)
├─ cortex-inv (투자)
├─ cortex-lit (문학)
├─ cortex-quant (정량)
└─ cortex-astro (천문)

인터페이스:
├─ interface-bot (Telegram)
└─ interface-web (Web)

도구:
├─ tools-bioinfo (생물정보)
└─ tools-quant (정량)
```

---

## 🎯 **실행 결과 (예상)**

### **동기화 완료 후**

```
✅ 로컬 레포
   - git remote origin → SHawn-Brain
   - 모든 코드 업데이트
   - 문서 동기화

✅ GitHub
   - 메인 레포명: SHawn-Brain ✓ (이미 변경됨)
   - 코드: 최신 상태
   - CI/CD: 작동 중

✅ 배포
   - Vercel: 자동 배포 활성화
   - API: 정상 작동
   - 웹사이트: 정상 작동

상태: 🟢 완전히 동기화됨
```

---

## 🚀 **다음 단계**

```
1. 동기화 완료 확인
2. v5.0.1 커밋
3. Phase 1 (카트리지 통합) 시작
4. 4주 모노레포 완성 로드맵 진행
```

---

**상태: 동기화 계획 완성** ✅
**다음: 실제 실행**
