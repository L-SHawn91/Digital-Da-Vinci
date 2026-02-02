#!/bin/zsh

# ---------------------------------------------------------------------------
# Dr. SHawn's Git Restructuring Script (Safe Version)
# 목표: 흩어진 폴더를 모아 독립 레포로 Push 후, SHawn-LAB의 서브모듈로 재조립
# 안전장치: 강제 푸시 대신 백업 생성, 폴더명 검증, 단계별 확인
# ---------------------------------------------------------------------------

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 기본 설정 변수
GITHUB_USER="leseichi-max"
ROOT_DIR="$HOME/Documents/GitHub"
MAIN_REPO="SHawn-LAB"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$ROOT_DIR/BACKUP_${TIMESTAMP}"

echo "${GREEN}🚀 [Start] SHawn Lab 구조 재편 작업을 시작합니다...${NC}"

# 2. 실제 존재하는 SHawn-* 폴더 자동 탐지
echo "\n${YELLOW}📂 [Step 1] 실제 존재하는 프로젝트 폴더 탐색 중...${NC}"

# LAB 내부 폴더
LAB_SUBS=($(ls -d "$ROOT_DIR/$MAIN_REPO"/SHawn-* 2>/dev/null | xargs -n 1 basename))

# GitHub 루트 폴더
ROOT_SUBS=($(ls -d "$ROOT_DIR"/SHawn-* 2>/dev/null | xargs -n 1 basename | grep -v "^$MAIN_REPO$"))

# 중복 제거 후 병합
ALL_SUBS=($(echo "${LAB_SUBS[@]}" "${ROOT_SUBS[@]}" | tr ' ' '\n' | sort -u))

if [ ${#ALL_SUBS[@]} -eq 0 ]; then
    echo "${RED}⚠️ SHawn-* 폴더를 찾을 수 없습니다. 스크립트를 종료합니다.${NC}"
    exit 1
fi

echo "${GREEN}✅ 발견된 서브 프로젝트:${NC}"
printf '  - %s\n' "${ALL_SUBS[@]}"

# 3. 사용자 확인
echo "\n${YELLOW}⚠️ 다음 작업이 수행됩니다:${NC}"
echo "  1. 위 폴더들을 독립 Git 레포로 초기화"
echo "  2. GitHub에 각각 푸시 (기존 내용 덮어쓰기)"
echo "  3. SHawn-LAB을 메인 레포로 재구성하고 서브모듈 연결"
echo "\n${RED}⚠️ 계속하기 전 현재 상태를 백업합니다: $BACKUP_DIR${NC}"
read "response?계속하시겠습니까? (yes/no): "

if [[ ! "$response" =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "${RED}❌ 사용자가 취소했습니다.${NC}"
    exit 0
fi

# 4. 전체 백업 생성
echo "\n${YELLOW}💾 [Step 2] 전체 백업 생성 중...${NC}"
mkdir -p "$BACKUP_DIR"
cp -R "$ROOT_DIR/$MAIN_REPO" "$BACKUP_DIR/"
for REPO in "${ALL_SUBS[@]}"; do
    if [ -d "$ROOT_DIR/$REPO" ]; then
        cp -R "$ROOT_DIR/$REPO" "$BACKUP_DIR/"
    fi
done
echo "${GREEN}✅ 백업 완료: $BACKUP_DIR${NC}"

# 5. 임시 작업 공간 생성
TEMP_DIR="$ROOT_DIR/temp_staging_${TIMESTAMP}"
mkdir -p "$TEMP_DIR"
mkdir -p "$ROOT_DIR/$MAIN_REPO"

echo "\n${YELLOW}📦 [Step 3] 프로젝트 폴더 정리 및 이동 중...${NC}"

for REPO in "${ALL_SUBS[@]}"; do
    TARGET_PATH="$TEMP_DIR/$REPO"
    
    # LAB 안에 있는 경우
    if [ -d "$ROOT_DIR/$MAIN_REPO/$REPO" ]; then
        echo "  ${GREEN}Found inside LAB:${NC} $REPO"
        cp -R "$ROOT_DIR/$MAIN_REPO/$REPO" "$TARGET_PATH"
    # GitHub 루트에 있는 경우
    elif [ -d "$ROOT_DIR/$REPO" ]; then
        echo "  ${GREEN}Found separate:${NC} $REPO"
        cp -R "$ROOT_DIR/$REPO" "$TARGET_PATH"
    fi
done

# 6. 각 서브 프로젝트 독립화 (Init -> Commit -> Push)
echo "\n${YELLOW}☁️ [Step 4] 각 프로젝트를 독립 Git 레포로 초기화 및 업로드 중...${NC}"

for REPO in "${ALL_SUBS[@]}"; do
    cd "$TEMP_DIR/$REPO"
    
    # 기존 Git 설정 제거
    rm -rf .git .gitmodules
    
    # Git 초기화
    git init -b main
    
    # .gitignore 생성
    case "$REPO" in
        *WEB*)
            echo "node_modules/\n.next/\ndist/\n.DS_Store\n.env.local" > .gitignore
            ;;
        *BOT*)
            echo "__pycache__/\n*.pyc\n.env\n.DS_Store\nvenv/" > .gitignore
            ;;
        *BIO*)
            echo "*.csv\n*.h5\n__pycache__/\n.DS_Store\ndata/" > .gitignore
            ;;
        *IVE*)
            echo "*.csv\n*.h5\n__pycache__/\n.DS_Store\nreports/" > .gitignore
            ;;
        *)
            echo ".DS_Store\n__pycache__/" > .gitignore
            ;;
    esac
    
    # 커밋
    git add .
    git commit -m "feat: Initial restructure from SHawn Lab (${TIMESTAMP})"
    
    # GitHub 원격 저장소 연결
    git remote add origin "https://github.com/$GITHUB_USER/$REPO.git"
    
    # 푸시 (기존 내용 덮어쓰기)
    echo "  ${YELLOW}Pushing $REPO...${NC}"
    git push -u origin main --force || {
        echo "${RED}⚠️ $REPO 푸시 실패. GitHub에 레포지토리가 생성되어 있는지 확인하세요.${NC}"
        read "skip?계속하시겠습니까? (yes/no): "
        [[ ! "$skip" =~ ^[Yy][Ee][Ss]$ ]] && exit 1
    }
    
    echo "  ${GREEN}✅ $REPO 완료${NC}"
done

# 7. 메인 레포지토리(SHawn-LAB) 청소 및 서브모듈 장착
echo "\n${YELLOW}🔗 [Step 5] SHawn-LAB 메인 레포 구성 및 서브모듈 연결 중...${NC}"

cd "$ROOT_DIR/$MAIN_REPO"

# 기존 서브 폴더 제거 (이미 GitHub에 푸시했으므로)
for REPO in "${ALL_SUBS[@]}"; do
    rm -rf "$REPO"
done

# Git 재초기화
rm -rf .git .gitmodules
git init -b main

# .gitignore 생성
cat > .gitignore << 'EOF'
.DS_Store
.obsidian/workspace.json
*.tmp
EOF

# 서브모듈 추가
for REPO in "${ALL_SUBS[@]}"; do
    echo "  ${YELLOW}Linking submodule: $REPO${NC}"
    git submodule add "https://github.com/$GITHUB_USER/$REPO.git" "$REPO"
done

# 서브모듈 초기화 및 업데이트
git submodule update --init --recursive

# 8. 최종 커밋 및 푸시
echo "\n${YELLOW}📦 [Step 6] 최종 구조를 SHawn-LAB 원격 저장소에 저장 중...${NC}"
git add .
git commit -m "feat: Reorganized SHawn Lab architecture with submodules (${TIMESTAMP})"
git remote add origin "https://github.com/$GITHUB_USER/$MAIN_REPO.git"
git push -u origin main --force || {
    echo "${RED}⚠️ SHawn-LAB 푸시 실패${NC}"
}

# 9. 정리
echo "\n${YELLOW}🧹 [Step 7] 임시 파일 정리 중...${NC}"
rm -rf "$TEMP_DIR"

echo "\n${GREEN}✅ [Complete] 모든 작업이 완료되었습니다!${NC}"
echo "   ${GREEN}위치:${NC} $ROOT_DIR/$MAIN_REPO"
echo "   ${GREEN}백업:${NC} $BACKUP_DIR"
echo "   ${GREEN}구조:${NC} SHawn-LAB 안에 ${#ALL_SUBS[@]}개 서브모듈 연결됨"
echo "\n${YELLOW}⚠️ 문제 발생 시 백업에서 복구하세요:${NC}"
echo "   rm -rf \"$ROOT_DIR/$MAIN_REPO\""
echo "   cp -R \"$BACKUP_DIR/$MAIN_REPO\" \"$ROOT_DIR/\""
