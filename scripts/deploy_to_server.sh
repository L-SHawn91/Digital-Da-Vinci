#!/bin/bash

# Configuration
SERVER_IP="139.59.231.62"
USER="root"
REMOTE_DIR="/root/SHawn-Brain"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🚀 Deploying SHawn-Brain to ${USER}@${SERVER_IP}:${REMOTE_DIR}..."

# Ensure remote directory exists
ssh ${USER}@${SERVER_IP} "mkdir -p ${REMOTE_DIR}"

# Sync using rsync
# We sync .env because the server needs secrets to run the bot.
# We exclude strictly local/heavy/generated files.
rsync -avz --progress --delete \
    --exclude ".git" \
    --exclude ".DS_Store" \
    --exclude "__pycache__" \
    --exclude "venv" \
    --exclude "node_modules" \
    --exclude "daily_reports" \
    --exclude "logs" \
    --exclude "downloads" \
    --exclude "*.pyc" \
    "$LOCAL_DIR/" "${USER}@${SERVER_IP}:${REMOTE_DIR}/"

echo "✅ Sync Complete."
echo "🔄 Verification suggestions:"
echo "   1. SSH into server: ssh ${USER}@${SERVER_IP}"
echo "   2. Go to dir: cd ${REMOTE_DIR}"
echo "   3. Check .env exists"
echo "   4. Rebuild venv if requirements changed."
