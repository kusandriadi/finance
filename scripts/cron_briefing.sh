#!/bin/bash
# cron_briefing.sh — fetch the daily market snapshot and push it to the
# configured channel (Telegram/WhatsApp). Invoked by cron each morning.
set -uo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/home/kusa/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRIEFING="$SCRIPT_DIR/market_briefing.py"
ENV_FILE="$SCRIPT_DIR/briefing.env"
SENDER="/home/kusa/bin/send-reminder.sh"
LOG_FILE="/home/kusa/data/trading/cron_briefing.log"

# Defaults (overridden by briefing.env)
NOTIFY_CHANNEL="whatsapp"
NOTIFY_TARGET="+62XXXXXXXXXX"
# shellcheck disable=SC1090
[ -f "$ENV_FILE" ] && source "$ENV_FILE"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"; }

log "Briefing started"

REPORT="$(timeout 120 python3 "$BRIEFING" 2>>"$LOG_FILE")"
RC=$?

if [ $RC -ne 0 ] || [ -z "$REPORT" ]; then
    log "Briefing failed (rc=$RC) or empty; skipping notification"
    exit 0
fi

if [ -x "$SENDER" ] && [ -n "${NOTIFY_TARGET:-}" ]; then
    if "$SENDER" "$REPORT" "$NOTIFY_CHANNEL" "$NOTIFY_TARGET" >/dev/null 2>&1; then
        log "Briefing sent via $NOTIFY_CHANNEL to $NOTIFY_TARGET"
    else
        log "Briefing send FAILED via $NOTIFY_CHANNEL to $NOTIFY_TARGET"
    fi
else
    log "No sender/target configured; briefing not sent"
fi

log "Briefing completed"
