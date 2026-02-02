# 기존 GitHub 레포 활용 폴더 구조 실행 계획

## 📊 **현재 상황**

### 기존 GitHub 레포
```
Repository: leseichi-max/SHawn-BOT
URL: https://github.com/leseichi-max/SHawn-BOT.git
현재 위치: /Users/soohyunglee/.openclaw/workspace/

커밋 기록:
- 20개 커밋 (1월 30일 ~ 2월 1일)
- 최신: 8c0dae3 (2026-02-01)
- 총 크기: ~2MB

구조:
├─ .git (메인 repo)
├─ SHawn_Brain/ (뇌 구조)
├─ cartridges/ (4개 카트리지 혼재)
├─ 메모리/문서/데이터
└─ 기타 도구
```

---

## 🎯 **기존 레포 활용 전략**

### 옵션 A: 단일 레포 + 폴더 재구조화 (추천) ⭐⭐⭐

**방식:**
```
기존 SHawn-BOT 레포 활용
└─ 내부 폴더 정리만 수행
   ├─ SHawn_Brain/ (뇌)
   ├─ SHawn-Bot/ (봇, 새로 정리)
   └─ Cartridges/ (카트리지, 새로 정리)
```

**장점:**
- ✅ 새 레포 생성 필요 없음
- ✅ 커밋 히스토리 유지
- ✅ 간단함
- ✅ 기존 GitHub 설정 유지

**단점:**
- ❌ 각 카트리지 독립 버전관리 불가
- ❌ 각 카트리지 독립 배포 불가
- ❌ 향후 확장성 제한

---

### 옵션 B: 단일 레포 + Subtree 분리 (중간)

**방식:**
```
기존 SHawn-BOT 레포 유지
└─ git subtree split으로 카트리지 분리
   ├─ bio-cartridge (git subtree)
   ├─ investment-cartridge (git subtree)
   └─ 기타 카트리지
```

**장점:**
- ✅ 기존 레포 유지
- ✅ git subtree로 독립 branch 생성
- ✅ 필요 시 별도 레포로 export 가능

**단점:**
- ❌ git subtree 복잡도 높음
- ❌ 초기 설정 어려움

---

### 옵션 C: 모노레포 + 폴더 구조 (최적) ⭐⭐⭐⭐

**방식:**
```
기존 SHawn-BOT 레포 (메인)
└─ 폴더 구조만 정리
   ├─ src/
   │  ├─ brain/ (SHawn_Brain)
   │  ├─ bot/ (SHawn-Bot)
   │  └─ cartridges/ (모든 카트리지)
   └─ tests/

+ 각 카트리지는 workspace에서 별도 폴더로도 관리 (로컬)
```

**장점:**
- ✅ 기존 레포 100% 활용
- ✅ 구조 명확함
- ✅ 모든 히스토리 유지
- ✅ 향후 필요 시 subtree로 분리 가능

**단점:**
- ❌ 각 카트리지 독립 배포 초기엔 불가 (나중에 가능)

---

## ✨ **추천: 옵션 C (모노레포 + 명확한 폴더 구조)**

### 이유
```
1. 기존 레포 최대 활용
2. 구조 명확함
3. 향후 유연함
4. 유지보수 간단함
```

---

## 🚀 **실행 계획 (옵션 C 기반)**

### Phase 1: 폴더 재구조화 (1시간)

**목표:** workspace 폴더 정리

```bash
# 1. 새 폴더 구조 생성
mkdir -p src/brain
mkdir -p src/bot
mkdir -p src/cartridges
mkdir -p tests
mkdir -p docs

# 2. 기존 파일 이동
mv SHawn_Brain/* src/brain/
mv shawn_bot_telegram.py → src/bot/telegram_interface.py
mv handlers.py → src/bot/handlers.py
mv SHawn_Brain/cartridges/* → src/cartridges/

# 3. 불필요 파일 정리
rm -rf SHawn_Brain (폴더 삭제)
rm -rf shawn_bot_telegram.py (이미 이동됨)
```

**최종 구조:**
```
workspace/
├─ .git (기존 메인 repo 유지)
├─ src/
│  ├─ brain/
│  │  ├─ brain_core/
│  │  ├─ neocortex/
│  │  ├─ neuronet/
│  │  └─ main.py
│  │
│  ├─ bot/
│  │  ├─ telegram_interface.py
│  │  ├─ handlers.py
│  │  └─ shawn_bot_main.py
│  │
│  └─ cartridges/
│     ├─ bio_cartridge/
│     ├─ investment_cartridge/
│     ├─ quant_cartridge/
│     ├─ lit_cartridge/
│     └─ astro_cartridge/
│
├─ tests/
│  ├─ test_brain.py
│  ├─ test_bot.py
│  └─ test_cartridges.py
│
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ BRAIN_STRUCTURE.md
│  ├─ BOT_SETUP.md
│  └─ CARTRIDGES.md
│
├─ memory/
├─ data/
├─ utilities/
├─ README.md
├─ requirements.txt
└─ .gitignore
```

---

### Phase 2: 코드 임포트 패스 수정 (1시간)

**변경 사항:**
```python
# Before
from SHawn_Brain.brain_core import brainstem

# After
from src.brain.brain_core import brainstem

# Bot
from src.bot.telegram_interface import TelegramBot

# Cartridges
from src.cartridges.bio_cartridge import BiologyCartridge
```

**파일:**
- main.py (또는 __init__.py)
- tests/*.py
- src/bot/shawn_bot_main.py

---

### Phase 3: Git 커밋 (30분)

```bash
git add -A
git commit -m "📁 폴더 구조 재정리: src/(brain/bot/cartridges) 모노레포 구조로 통합"
git push origin main
```

---

### Phase 4: 문서 업데이트 (30분)

**README.md 업데이트:**
```markdown
# SHawn-BOT: 디지털 다빈치 프로젝트

## 📁 폴더 구조

### src/brain/
- 디지털 신경계 (D-CNS)
- Level 1-4 뇌 구조

### src/bot/
- Telegram 사용자 인터페이스
- 메시지 핸들러

### src/cartridges/
- Bio-Cartridge: 생물학
- Investment-Cartridge: 금융
- Quant-Cartridge: 분석
- Lit-Cartridge: 문헌
- Astro-Cartridge: 우주

## 🚀 시작하기

```bash
python -m src.bot.shawn_bot_main
```

## 📊 아키텍처

[D-CNS 신경계 다이어그램]
```

---

## 💡 **향후 확장 옵션 (필요 시)**

### 나중에 (6개월 이후)

**필요해지면:**
```
# git subtree로 카트리지 분리 가능
git subtree split --prefix=src/cartridges/bio_cartridge \
  -b bio-cartridge-main

# 새 레포로 export
git push --set-upstream <new-repo> bio-cartridge-main:main
```

**하지만 지금은:**
- ❌ 불필요
- ✅ 현재 모노레포 구조로 충분

---

## 📊 **최종 계획 (총 3시간)**

```
Phase 1: 폴더 재구조화 (1시간)
  ├─ 새 폴더 생성
  ├─ 파일 이동
  └─ 폴더 정리

Phase 2: 코드 임포트 패스 수정 (1시간)
  ├─ main.py 수정
  ├─ test 파일 수정
  └─ 테스트 실행

Phase 3: Git 커밋 (30분)
  ├─ git add -A
  ├─ git commit
  └─ git push

Phase 4: 문서 업데이트 (30분)
  ├─ README.md 수정
  ├─ ARCHITECTURE.md 작성
  └─ 확인

총 소요: 3시간
```

---

## ✅ **장점 (기존 레포 활용)**

```
✓ 새 레포 생성 필요 없음
✓ 기존 커밋 히스토리 유지
✓ GitHub 설정 변경 없음
✓ 복잡도 낮음
✓ 명확한 구조
✓ 모노레포 최적화
✓ 향후 필요 시 subtree로 분리 가능
```

---

**이 방식이 최적이라고 생각합니다!** 🚀✨
