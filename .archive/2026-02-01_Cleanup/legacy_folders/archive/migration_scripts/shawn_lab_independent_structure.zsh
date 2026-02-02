#!/bin/zsh

# ---------------------------------------------------------------------------
# Dr. SHawn's Git Independent Structure Script
# 목표: 각 프로젝트를 완전히 독립된 Git 레포지토리로 분리
# SHawn-IVE → SHawn-INV 이름 변경 포함
# ---------------------------------------------------------------------------

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. 기본 설정
GITHUB_USER="leseichi-max"
ROOT_DIR="$HOME/Documents/GitHub"
MAIN_REPO="SHawn-LAB"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$ROOT_DIR/BACKUP_${TIMESTAMP}"

# 독립시킬 프로젝트 목록 (SHawn-IVE는 SHawn-INV로 변경)
declare -A PROJECTS=(
    ["SHawn-WEB"]="SHawn-WEB"
    ["SHawn-BOT"]="SHawn-BOT"
    ["SHawn-BIO"]="SHawn-BIO"
    ["SHawn-IVE"]="SHawn-INV"  # 원본 폴더명 → 새 레포명
)

echo "${GREEN}🚀 [Start] SHawn Lab 독립 구조 재편 시작${NC}\n"

# 2. 현재 상태 확인
echo "${BLUE}📋 [Step 1] 현재 프로젝트 폴더 확인${NC}"
for OLD_NAME in ${(k)PROJECTS}; do
    NEW_NAME=${PROJECTS[$OLD_NAME]}
    
    if [ -d "$ROOT_DIR/$MAIN_REPO/$OLD_NAME" ]; then
        echo "  ${GREEN}✓${NC} Found: $MAIN_REPO/$OLD_NAME → 독립 레포 $NEW_NAME"
    elif [ -d "$ROOT_DIR/$OLD_NAME" ]; then
        echo "  ${GREEN}✓${NC} Found: $OLD_NAME (이미 독립됨) → $NEW_NAME"
    else
        echo "  ${RED}✗${NC} Not found: $OLD_NAME"
    fi
done

# SHawn-LAB 자체도 확인
if [ -d "$ROOT_DIR/$MAIN_REPO" ]; then
    echo "  ${GREEN}✓${NC} Found: $MAIN_REPO (메인 레포)"
else
    echo "  ${RED}✗${NC} Not found: $MAIN_REPO"
    exit 1
fi

# 3. 사용자 확인
echo "\n${YELLOW}⚠️  다음 작업이 수행됩니다:${NC}"
echo "  1. 전체 백업 생성: $BACKUP_DIR"
echo "  2. SHawn-LAB 안의 폴더들을 GitHub 루트로 이동"
echo "  3. 각 폴더를 독립 Git 레포로 초기화 (SHawn-IVE → SHawn-INV)"
echo "  4. GitHub에 각각 푸시 (force push)"
echo "  5. SHawn-LAB은 서브 프로젝트 제외하고 메인 레포로 유지"
echo "\n${RED}⚠️  GitHub에 다음 레포지토리가 생성되어 있어야 합니다:${NC}"
echo "  - https://github.com/$GITHUB_USER/SHawn-LAB"
echo "  - https://github.com/$GITHUB_USER/SHawn-WEB"
echo "  - https://github.com/$GITHUB_USER/SHawn-BOT"
echo "  - https://github.com/$GITHUB_USER/SHawn-BIO"
echo "  - https://github.com/$GITHUB_USER/SHawn-INV"

read "response?\n계속하시겠습니까? (yes/no): "
if [[ ! "$response" =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "${RED}❌ 사용자가 취소했습니다.${NC}"
    exit 0
fi

# 4. 전체 백업
echo "\n${BLUE}💾 [Step 2] 전체 백업 생성 중...${NC}"
mkdir -p "$BACKUP_DIR"
if [ -d "$ROOT_DIR/$MAIN_REPO" ]; then
    cp -R "$ROOT_DIR/$MAIN_REPO" "$BACKUP_DIR/"
fi
echo "${GREEN}✅ 백업 완료: $BACKUP_DIR${NC}"

# 5. 각 프로젝트 독립화
echo "\n${BLUE}📦 [Step 3] 프로젝트 독립화 및 GitHub 푸시${NC}\n"

for OLD_NAME in ${(k)PROJECTS}; do
    NEW_NAME=${PROJECTS[$OLD_NAME]}
    SOURCE_PATH=""
    TARGET_PATH="$ROOT_DIR/$NEW_NAME"
    
    # 소스 경로 확인
    if [ -d "$ROOT_DIR/$MAIN_REPO/$OLD_NAME" ]; then
        SOURCE_PATH="$ROOT_DIR/$MAIN_REPO/$OLD_NAME"
    elif [ -d "$ROOT_DIR/$OLD_NAME" ]; then
        SOURCE_PATH="$ROOT_DIR/$OLD_NAME"
    else
        echo "${YELLOW}⚠️  $OLD_NAME 폴더를 찾을 수 없습니다. 건너뜁니다.${NC}"
        continue
    fi
    
    echo "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${YELLOW}📁 처리 중: $OLD_NAME → $NEW_NAME${NC}"
    
    # 이름이 다르면 이동 & 이름 변경
    if [ "$SOURCE_PATH" != "$TARGET_PATH" ]; then
        echo "  ${BLUE}→${NC} 이동: $SOURCE_PATH → $TARGET_PATH"
        
        # 대상 위치에 이미 존재하면 백업
        if [ -d "$TARGET_PATH" ]; then
            echo "  ${YELLOW}⚠️  기존 $NEW_NAME 발견. 백업 중...${NC}"
            mv "$TARGET_PATH" "$TARGET_PATH.backup_${TIMESTAMP}"
        fi
        
        mv "$SOURCE_PATH" "$TARGET_PATH"
    fi
    
    # Git 초기화
    cd "$TARGET_PATH"
    
    echo "  ${BLUE}→${NC} Git 재초기화"
    rm -rf .git .gitmodules
    git init -b main
    
    # .gitignore 생성
    echo "  ${BLUE}→${NC} .gitignore 생성"
    case "$NEW_NAME" in
        *WEB*)
            cat > .gitignore << 'EOF'
node_modules/
.next/
dist/
build/
.DS_Store
.env.local
.env.production
*.log
EOF
            ;;
        *BOT*)
            cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.env
.DS_Store
venv/
*.log
.pytest_cache/
EOF
            ;;
        *BIO*)
            cat > .gitignore << 'EOF'
*.csv
*.h5
*.hdf5
__pycache__/
.DS_Store
data/raw/
*.log
.ipynb_checkpoints/
EOF
            ;;
        *INV*)
            cat > .gitignore << 'EOF'
*.csv
*.h5
__pycache__/
.DS_Store
reports/*.html
*.log
.ipynb_checkpoints/
venv/
EOF
            ;;
        *)
            echo ".DS_Store" > .gitignore
            ;;
    esac
    
    # 커밋
    echo "  ${BLUE}→${NC} 파일 커밋 중..."
    git add .
    git commit -m "feat: Independent repository restructure from SHawn Lab (${TIMESTAMP})" -m "Migrated from monorepo structure to independent repository"
    
    # GitHub 연결 및 푸시
    echo "  ${BLUE}→${NC} GitHub 푸시: https://github.com/$GITHUB_USER/$NEW_NAME.git"
    
    # 기존 remote 제거 후 재설정
    git remote remove origin 2>/dev/null
    git remote add origin "https://github.com/$GITHUB_USER/$NEW_NAME.git"
    
    # 푸시
    if git push -u origin main --force; then
        echo "  ${GREEN}✅ $NEW_NAME 푸시 성공${NC}\n"
    else
        echo "  ${RED}❌ $NEW_NAME 푸시 실패${NC}"
        echo "  ${YELLOW}GitHub에 레포지토리가 생성되어 있는지 확인하세요.${NC}\n"
    fi
done

# 6. SHawn-LAB 메인 레포 정리
echo "${BLUE}🏠 [Step 4] SHawn-LAB 메인 레포 정리${NC}\n"

cd "$ROOT_DIR/$MAIN_REPO"

# 독립시킨 폴더들 제거
for OLD_NAME in ${(k)PROJECTS}; do
    if [ -d "$OLD_NAME" ]; then
        echo "  ${BLUE}→${NC} 제거: $OLD_NAME (이미 독립됨)"
        rm -rf "$OLD_NAME"
    fi
done

# Git 재초기화
echo "  ${BLUE}→${NC} SHawn-LAB Git 재초기화"
rm -rf .git .gitmodules
git init -b main

# .gitignore 생성 (Obsidian Vault용)
cat > .gitignore << 'EOF'
.DS_Store
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
*.tmp
EOF

# README 업데이트
cat > README.md << 'EOF'
# SHawn-LAB

박사님의 메인 작업 공간 (Obsidian Vault + 문서 저장소)

## 관련 프로젝트 (독립 레포지토리)

각 프로젝트는 독립적인 Git 레포지토리로 관리됩니다:

- **[SHawn-WEB](https://github.com/leseichi-max/SHawn-WEB)**: 웹 애플리케이션 프로젝트
- **[SHawn-BOT](https://github.com/leseichi-max/SHawn-BOT)**: Telegram 봇 시스템
- **[SHawn-BIO](https://github.com/leseichi-max/SHawn-BIO)**: 바이오인포매틱스 분석 도구
- **[SHawn-INV](https://github.com/leseichi-max/SHawn-INV)**: 투자 분석 시스템 (Dual Quant System)

## 구조

```
~/Documents/GitHub/
├── SHawn-LAB/    # 메인 Vault (이 레포)
├── SHawn-WEB/    # 독립 레포
├── SHawn-BOT/    # 독립 레포
├── SHawn-BIO/    # 독립 레포
└── SHawn-INV/    # 독립 레포
```

---

Last updated: $(date +%Y-%m-%d)
EOF

# 커밋 및 푸시
echo "  ${BLUE}→${NC} 변경사항 커밋 중..."
git add .
git commit -m "refactor: Migrate to independent project structure" -m "Removed subprojects (now independent repos): WEB, BOT, BIO, INV"

echo "  ${BLUE}→${NC} GitHub 푸시: https://github.com/$GITHUB_USER/$MAIN_REPO.git"
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$GITHUB_USER/$MAIN_REPO.git"

if git push -u origin main --force; then
    echo "  ${GREEN}✅ SHawn-LAB 푸시 성공${NC}\n"
else
    echo "  ${RED}❌ SHawn-LAB 푸시 실패${NC}\n"
fi

# 7. 완료 보고
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}✅ [Complete] 모든 작업 완료!${NC}\n"

echo "${BLUE}📂 최종 구조:${NC}"
echo "  $ROOT_DIR/"
echo "  ├── SHawn-LAB/    ${GREEN}(메인 Vault)${NC}"
echo "  ├── SHawn-WEB/    ${YELLOW}(독립 레포)${NC}"
echo "  ├── SHawn-BOT/    ${YELLOW}(독립 레포)${NC}"
echo "  ├── SHawn-BIO/    ${YELLOW}(독립 레포)${NC}"
echo "  └── SHawn-INV/    ${YELLOW}(독립 레포 - SHawn-IVE에서 변경)${NC}"

echo "\n${BLUE}💾 백업 위치:${NC} $BACKUP_DIR"

echo "\n${BLUE}🔗 GitHub 레포지토리:${NC}"
echo "  - https://github.com/$GITHUB_USER/SHawn-LAB"
echo "  - https://github.com/$GITHUB_USER/SHawn-WEB"
echo "  - https://github.com/$GITHUB_USER/SHawn-BOT"
echo "  - https://github.com/$GITHUB_USER/SHawn-BIO"
echo "  - https://github.com/$GITHUB_USER/SHawn-INV"

echo "\n${YELLOW}⚠️  문제 발생 시 백업에서 복구:${NC}"
echo "  rm -rf \"$ROOT_DIR/$MAIN_REPO\""
echo "  cp -R \"$BACKUP_DIR/$MAIN_REPO\" \"$ROOT_DIR/\""
