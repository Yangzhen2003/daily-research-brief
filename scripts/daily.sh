#!/usr/bin/env bash
# Run the daily briefing agent once. Safe to invoke from cron/launchd.
set -euo pipefail
cd "$(dirname "$0")/.."
export TZ=Asia/Shanghai
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
DSH_BIN="${DSH_BIN:-$(command -v dsh || true)}"
if [ -z "$DSH_BIN" ]; then
  echo "dsh not found; set DSH_BIN or add it to PATH." >&2
  exit 1
fi
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
  "$DSH_BIN" --profile headless "$(cat prompts/daily.md)"
  echo "===== $(date '+%F %T %Z') done ====="
} 2>&1 | tee -a "$LOG"
