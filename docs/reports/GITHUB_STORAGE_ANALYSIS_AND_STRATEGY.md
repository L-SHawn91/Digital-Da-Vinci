# GitHub 레포 용량 분석 & 전략 수정

## 📊 **현재 GitHub 레포 용량 현황**

### 레포별 상세 분석

| # | 레포명 | 용량 | 언어 | 설명 | 상태 |
|-|-|-|-|-|-|
| 1 | SHawn-Lab-Vault | **109GB** ⚠️⚠️⚠️ | HTML | SHawn-Lab 저장소 | 위험 |
| 2 | Bioinfo_git | **12.5GB** ⚠️⚠️ | Python | 생물정보학 | 매우 높음 |
| 3 | SHawn-BOT | **1.2GB** ⚠️ | Python | 메인 봇 | 높음 |
| 4 | SHawn-INV | **409MB** | HTML | 투자 데이터 | 중간 |
| 5 | SHawn-WEB | **437MB** | HTML | 웹사이트 | 중간 |
| 6 | SHawn-LAB | **279MB** | 혼합 | R&D Lab | 중간 |
| 7 | quant_git | **204MB** | HTML | 웹 개발 | 중간 |
| 8 | web_git | **127MB** | TypeScript | Quant 전략 | 낮음 |
| 9 | SHawn-BIO | **31MB** | Python | Bio 데이터 | 낮음 |

**총합: ~125GB** 🔴 (GitHub 한계 인접)

---

## 🚨 **용량 한계 분석**

### GitHub 제한사항
```
GitHub 무료 용량: 무제한 (하지만 운영상 제한)
├─ 파일당 최대 크기: 100MB (초과 시 LFS 필요)
├─ 레포당 추천: 5-10GB 이내
└─ 사용자당 총합: 실제로는 제한 없음

하지만 실제 문제:
❌ SHawn-Lab-Vault: 109GB (이미 문제 상태)
❌ Bioinfo_git: 12.5GB (곧 문제될 수 있음)
❌ SHawn-BOT: 1.2GB (계속 증가 예상)
```

### 용량 초과의 원인
```
일반적인 원인:
❌ 커밋 히스토리 누적
❌ 바이너리 파일 포함 (이미지, 데이터)
❌ LFS 사용 부실
❌ 대용량 데이터셋 포함
```

---

## 💡 **전략 수정: 지속 가능한 구조**

### 현재 문제
```
SHawn-BOT (1.2GB) + 모든 것을 담으면:
├─ brain (코드 100MB)
├─ bot (코드 50MB)
├─ cartridges (코드 50MB)
├─ 데이터 (?)
├─ 로그 (?)
└─ 메모리 (?)
= 빠르게 증가할 가능성 높음
```

---

## ✅ **최적 전략: 분산 구조 (신규 전략) ⭐⭐⭐**

### 재수정 방안

#### 1️⃣ SHawn-BOT (메인, 코드 중심) - 유지
```
레포: leseichi-max/SHawn-BOT (기존)
용량 목표: 500MB 이내
구성:
├─ src/ (코드만)
│  ├─ brain/
│  ├─ bot/
│  └─ cartridges/
├─ tests/
├─ docs/
├─ requirements.txt
└─ .gitignore (데이터/로그 제외)

제외 사항:
❌ memory/ (용량 증가)
❌ data/ (용량 증가)
❌ logs/ (용량 증가)
```

#### 2️⃣ SHawn-Lab-Vault (기존, 정리 필요) ⚠️
```
현재: 109GB (위험)
대책: 
- 정리 필요 (오래된 데이터 삭제)
- 또는 전용 스토리지 이용
```

#### 3️⃣ 각 카트리지 (선택적 독립)
```
옵션 A (권장): 코드만 SHawn-BOT에 유지
└─ 별도 GitHub 레포 불필요

옵션 B (향후): 필요 시 분리
└─ 각 카트리지 독립 레포 생성
   ├─ SHawn-bio-cartridge
   ├─ SHawn-investment-cartridge
   └─ etc (그때 생성)
```

---

## 🎯 **수정된 실행 계획**

### Phase 1: SHawn-BOT 정리 (코드 중심) - 1시간

```bash
# 1. .gitignore 강화
echo "memory/" >> .gitignore
echo "data/" >> .gitignore
echo "logs/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".cache/" >> .gitignore

# 2. 폴더 구조만 정리
mkdir -p src/{brain,bot,cartridges}
mkdir -p tests/
mkdir -p docs/

# 3. 코드 파일만 이동
# (데이터/로그/메모리는 local 폴더로 관리)

# 4. 커밋
git add -A
git commit -m "📁 코드 중심 모노레포: src/(brain/bot/cartridges), 데이터 제외"
```

### Phase 2: 로컬 관리 폴더 설정 - 30분

```
workspace (Git 추적)
├─ src/ (GitHub에 커밋)
├─ tests/
├─ docs/
└─ .gitignore (memory/, data/, logs/ 제외)

workspace (로컬 관리만)
├─ memory/ (.gitignore)
├─ data/ (.gitignore)
├─ logs/ (.gitignore)
└─ .cache/ (.gitignore)
```

### Phase 3: 용량 정리 (선택사항) - 30분

```bash
# Git 히스토리에서 대용량 파일 제거 (필요 시)
git filter-branch --tree-filter 'find . -name "*.pyc" -delete' HEAD

# 또는 BFG Repo-Cleaner 사용
bfg --delete-files "*.pyc" <repo>
```

---

## 📈 **최종 구조**

### GitHub (코드 중심)
```
SHawn-BOT (500MB 목표)
├─ src/
├─ tests/
├─ docs/
└─ requirements.txt

+ 기타 기존 레포들 유지
```

### 로컬 (데이터/메모리 관리)
```
workspace/
├─ memory/ (로컬만, Git 추적 X)
├─ data/ (로컬만, Git 추적 X)
├─ logs/ (로컬만, Git 추적 X)
└─ src/ (GitHub에 커밋)
```

---

## 💾 **용량 절감 효과**

### Before (문제 상황)
```
SHawn-BOT (1.2GB)
+ 모든 데이터/로그/메모리
= 빠르게 증가 (매월 +100MB 예상)
```

### After (최적화)
```
SHawn-BOT (500MB 목표)
+ 로컬 폴더 (Git 추적 X)
= 안정적 유지 (매월 +5MB 코드만)

용량 절감: -55% (1.2GB → 500MB)
```

---

## ✅ **최종 권장사항**

### 지금 할 것
```
1. SHawn-BOT에 .gitignore 강화
2. 폴더 구조 정리 (코드만)
3. memory/, data/, logs/ 로컬 관리로 전환
```

### 나중에 할 것 (필요 시)
```
- 각 카트리지 독립 레포 생성 (선택)
- SHawn-Lab-Vault 정리 (필수)
- 대용량 데이터 전용 스토리지 이용
```

### 하지 말아야 할 것
```
❌ 모든 파일을 하나의 레포에 계속 쌓기
❌ 데이터/로그를 GitHub에 계속 커밋
❌ 신규 카트리지마다 새 대용량 레포 생성
```

---

**이 방식이 GitHub 용량 제한 내에서 지속 가능합니다!** 🚀✨
