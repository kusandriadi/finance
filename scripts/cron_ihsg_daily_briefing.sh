#!/bin/bash
# cron_ihsg_daily_briefing.sh — fetch the midday/late-day IHSG + forex snapshot and push it
# to the configured channel (Telegram/WhatsApp). Invoked by cron on weekdays.
set -uo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/home/kusa/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRIEFING="$SCRIPT_DIR/market_briefing.py"
ENV_FILE="$SCRIPT_DIR/../../../skill.env"
SENDER="/home/kusa/bin/send-reminder.sh"
LOG_FILE="/home/kusa/data/trading/cron_ihsg_fx_briefing.log"

# Defaults (overridden by skill.env)
NOTIFY_CHANNEL="whatsapp"
NOTIFY_TARGETS=""
# shellcheck disable=SC1090
[ -f "$ENV_FILE" ] && source "$ENV_FILE"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"; }

log "IHSG/forex briefing started"

REPORT="$(timeout 120 python3 "$BRIEFING" --mode ihsg-fx 2>>"$LOG_FILE")"
RC=$?

if [ $RC -ne 0 ] || [ -z "$REPORT" ]; then
    log "IHSG/forex briefing failed (rc=$RC) or empty; skipping notification"
    exit 0
fi

if [ -x "$SENDER" ] && [ -n "${NOTIFY_TARGETS:-}" ]; then
    # shellcheck disable=SC2086
    if "$SENDER" "$REPORT" "$NOTIFY_CHANNEL" $NOTIFY_TARGETS >/dev/null 2>&1; then
        log "IHSG/forex briefing sent via $NOTIFY_CHANNEL to $NOTIFY_TARGETS"
    else
        log "IHSG/forex briefing send FAILED via $NOTIFY_CHANNEL to $NOTIFY_TARGETS"
    fi
else
    log "No sender/targets configured; IHSG/forex briefing not sent"
fi

log "IHSG/forex briefing completed"
