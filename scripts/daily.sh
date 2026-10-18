#!/usr/bin/env bash
# Run the daily briefing agent once. Safe to invoke from cron/launchd.
set -euo pipefail
cd "$(dirname "$0")/.."
export TZ=Asia/Shanghai
DAY=$(date +%F)
LOG=".logs/daily-${DAY}.log"
mkdir -p .logs
{
  echo "===== $(date '+%F %T %Z') start ====="
  if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree not clean; refusing to run." >&2
    git status --short >&2
    exit 1
  fi
  git pull --rebase origin main
  dsh --profile headless "$(cat prompts/daily.md)"
  echo "===== $(date '+%F %T %Z') done ====="
} 2>&1 | tee -a "$LOG"
