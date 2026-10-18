#!/usr/bin/env bash
# Install (or remove) a launchd job that runs scripts/daily.sh every day at 10:00 local time.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO=$(pwd)
LABEL="com.local.daily-research-brief"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
if [ "${1:-install}" = "remove" ]; then
  launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed ${LABEL}."
  exit 0
fi
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>${REPO}/scripts/daily.sh</string></array>
  <key>WorkingDirectory</key><string>${REPO}</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>${REPO}/.logs/launchd.out.log</string>
  <key>StandardErrorPath</key><string>${REPO}/.logs/launchd.err.log</string>
</dict>
</plist>
PLIST
launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Installed ${LABEL} -> ${REPO}/scripts/daily.sh at 10:00 daily."
echo "Check: launchctl print gui/$(id -u)/${LABEL} | head"
