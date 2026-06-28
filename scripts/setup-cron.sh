#!/bin/bash
# setup-cron.sh — install/repair the daily market briefing cron.
# Default: 08:30 WIB Mon-Fri.
# Safe to re-run: it removes any prior finance-briefing lines first.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WRAPPER="$SCRIPT_DIR/cron_briefing.sh"
MIDDAY_WRAPPER="$SCRIPT_DIR/cron_ihsg_daily_briefing.sh"
CLOSE_ANALYSIS_WRAPPER="$SCRIPT_DIR/cron_ihsg_close_analysis.sh"
chmod +x "$WRAPPER" "$MIDDAY_WRAPPER" "$CLOSE_ANALYSIS_WRAPPER" \
  "$SCRIPT_DIR/market_briefing.py" "$SCRIPT_DIR/ihsg_close_analysis.py" 2>/dev/null || true

# Briefing times (WIB). Override by editing these lines.
SCHEDULE=("30 8 * * 1-5")
ANALYSIS_SCHEDULE=("35 8 * * 1-5")
MIDDAY_SCHEDULE=("30 12 * * 1-5")
AFTER_CLOSE_SCHEDULE=("45 16 * * 1-5")

TMP="$(mktemp)"
crontab -l 2>/dev/null | grep -v -E "finance/(scripts/)?cron_briefing\.sh|finance/(scripts/)?cron_ihsg_daily_briefing\.sh|finance/(scripts/)?cron_ihsg_fx_briefing\.sh|finance/(scripts/)?cron_ihsg_close_analysis\.sh|# Finance —" > "$TMP" || true

{
  echo "# Finance — daily market briefing (Mon-Fri, WIB)"
  for expr in "${SCHEDULE[@]}"; do
    echo "$expr $WRAPPER"
  done
  echo "# Finance — IHSG prior-close analysis (Mon-Fri, WIB)"
  for expr in "${ANALYSIS_SCHEDULE[@]}"; do
    echo "$expr $CLOSE_ANALYSIS_WRAPPER"
  done
  echo "# Finance — midday IHSG + forex briefing (Mon-Fri, WIB)"
  for expr in "${MIDDAY_SCHEDULE[@]}"; do
    echo "$expr $MIDDAY_WRAPPER"
  done
  echo "# Finance — late afternoon IHSG + forex briefing (Mon-Fri, WIB)"
  for expr in "${AFTER_CLOSE_SCHEDULE[@]}"; do
    echo "$expr $MIDDAY_WRAPPER"
  done
} >> "$TMP"

crontab "$TMP"
rm -f "$TMP"

echo "✅ Briefing cron installed:"
crontab -l | grep -E "cron_briefing\.sh|cron_ihsg_daily_briefing\.sh|cron_ihsg_close_analysis\.sh"
