#!/bin/bash
# cron_ihsg_close_analysis.sh — fetch the prior-close IHSG analysis and push it
# to the configured channel (Telegram/WhatsApp). Invoked by cron on weekdays.
set -uo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/home/kusa/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANALYZER="$SCRIPT_DIR/ihsg_close_analysis.py"
ENV_FILE="$SCRIPT_DIR/../../../skill.env"
SENDER="/home/kusa/bin/send-reminder.sh"
LOG_FILE="/home/kusa/data/trading/cron_ihsg_close_analysis.log"

# Defaults (overridden by skill.env)
NOTIFY_CHANNEL="whatsapp"
NOTIFY_TARGETS=""
# shellcheck disable=SC1090
[ -f "$ENV_FILE" ] && source "$ENV_FILE"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"; }

log "IHSG close analysis started"

REPORT="$(timeout 180 python3 "$ANALYZER" 2>>"$LOG_FILE")"
RC=$?

if [ $RC -ne 0 ] || [ -z "$REPORT" ]; then
    log "IHSG close analysis failed (rc=$RC) or empty; skipping notification"
    exit 0
fi

if [ -x "$SENDER" ] && [ -n "${NOTIFY_TARGETS:-}" ]; then
    # shellcheck disable=SC2086
    if "$SENDER" "$REPORT" "$NOTIFY_CHANNEL" $NOTIFY_TARGETS >/dev/null 2>&1; then
        log "IHSG close analysis sent via $NOTIFY_CHANNEL to $NOTIFY_TARGETS"
    else
        log "IHSG close analysis send FAILED via $NOTIFY_CHANNEL to $NOTIFY_TARGETS"
    fi
else
    log "No sender/targets configured; IHSG close analysis not sent"
fi

log "IHSG close analysis completed"
