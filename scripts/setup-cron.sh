#!/bin/bash
# setup-cron.sh — install/repair the daily market briefing cron.
# Default: 07:30 WIB Mon-Fri (before IDX opens at 09:00).
# Safe to re-run: it removes any prior finance-briefing lines first.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WRAPPER="$SCRIPT_DIR/cron_briefing.sh"
chmod +x "$WRAPPER" "$SCRIPT_DIR/market_briefing.py" 2>/dev/null || true

# Briefing time (WIB). Override by editing this line.
SCHEDULE=("30 7 * * 1-5")

TMP="$(mktemp)"
crontab -l 2>/dev/null | grep -v -E "finance/(scripts/)?cron_briefing\.sh" > "$TMP" || true

{
  echo "# Finance — daily market briefing (Mon-Fri, WIB)"
  for expr in "${SCHEDULE[@]}"; do
    echo "$expr $WRAPPER"
  done
} >> "$TMP"

crontab "$TMP"
rm -f "$TMP"

echo "✅ Briefing cron installed:"
crontab -l | grep "cron_briefing.sh"
