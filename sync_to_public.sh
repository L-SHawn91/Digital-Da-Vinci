#!/bin/bash

# SHawn-Brain Work -> Public Sync Script
# 개인 데이터(memory, env, logs)를 제외한 순수 코드만 복사합니다.

SOURCE="/Users/soohyunglee/GitHub/SHawn-Brain"
DEST="/Users/soohyunglee/GitHub/Digital-Da-Vinci"

echo "🎨 Syncing SHawn-Brain-Work to SHawn-Brain-Public..."

# 1. Ensure Destination exists
mkdir -p "$DEST"

# 2. Sync core files (Excluding personal data)
rsync -av --progress "$SOURCE/" "$DEST/" \
    --exclude ".git" \
    --exclude ".env*" \
    --exclude "memory" \
    --exclude "memory_store" \
    --exclude "neuro_memory.json" \
    --exclude "logs" \
    --exclude "daily_logs" \
    --exclude "daily_reports" \
    --exclude "knowledge_base" \
    --exclude "outputs" \
    --exclude "__pycache__" \
    --exclude ".DS_Store" \
    --exclude "venv" \
    --exclude "node_modules" \
    --exclude ".next" \
    --exclude "dist" \
    --exclude "build"

echo "✅ Sync Complete!"
echo "🚀 Now go to $DEST and run 'git push' to deploy."
