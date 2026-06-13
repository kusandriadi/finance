#!/usr/bin/env python3
"""market_briefing.py — daily market snapshot for Kus.

Self-contained: needs only `requests` (no numpy/pandas/yfinance). Fetches a
small basket of instruments from Yahoo Finance and prints a chat-friendly
briefing (no markdown tables — WhatsApp/Telegram safe).

Usage:
    python3 market_briefing.py            # full briefing
    python3 market_briefing.py --json     # raw quotes as JSON
"""
import sys
import json
import time
import urllib.parse
from datetime import datetime

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) finance-briefing/1.0"}

# (symbol, label, value_format)  — value_format: "idr", "usd", "num", "pts"
BASKET = [
    ("^JKSE",    "IHSG",            "pts"),
    ("IDR=X",    "USD/IDR",         "idr"),
    ("XAUUSD=X", "Emas (XAU/USD)",  "usd"),
    ("GC=F",     "Emas Futures",    "usd"),
    ("^GSPC",    "S&P 500",         "pts"),
    ("^IXIC",    "Nasdaq",          "pts"),
    ("^N225",    "Nikkei 225",      "pts"),
    ("CL=F",     "Minyak (WTI)",    "usd"),
    ("BTC-USD",  "Bitcoin",         "usd"),
]


def fetch_quote(symbol, retries=3):
    """Return (last, prev_close) or None."""
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        + urllib.parse.quote(symbol)
        + "?interval=1d&range=5d"
    )
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=UA, timeout=15)
            if r.status_code != 200:
                time.sleep(1 + attempt)
                continue
            res = r.json()["chart"]["result"][0]
            meta = res.get("meta", {})
            closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
            # Daily change = two most recent daily closes (today vs yesterday).
            # Fall back to meta only if we don't have two valid closes.
            if len(closes) >= 2:
                last = meta.get("regularMarketPrice") or closes[-1]
                prev = closes[-2]
            else:
                last = meta.get("regularMarketPrice")
                prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            if last is None or prev is None:
                return None
            return float(last), float(prev)
        except Exception:
            time.sleep(1 + attempt)
    return None


def fmt_value(val, kind):
    if kind == "idr":
        return f"{val:,.0f}".replace(",", ".")
    if kind == "usd":
        return f"${val:,.2f}"
    if kind == "pts":
        return f"{val:,.2f}"
    return f"{val:,.2f}"


def arrow(pct):
    if pct > 0.05:
        return "🟢▲"
    if pct < -0.05:
        return "🔴▼"
    return "⚪️="


def build_briefing():
    today = datetime.now().strftime("%A, %d %B %Y")
    lines = [f"📊 *Market Briefing* — {today}", ""]
    quotes = {}
    for symbol, label, kind in BASKET:
        q = fetch_quote(symbol)
        if q is None:
            continue
        last, prev = q
        pct = (last - prev) / prev * 100 if prev else 0.0
        quotes[symbol] = {"label": label, "last": last, "prev": prev, "pct": pct}
        lines.append(f"{arrow(pct)} {label}: {fmt_value(last, kind)} ({pct:+.2f}%)")
    if len(lines) <= 2:
        return None, {}
    lines.append("")
    lines.append("_Bukan saran finansial. Data: Yahoo Finance (delayed)._")
    return "\n".join(lines), quotes


def main():
    if "--json" in sys.argv:
        _, quotes = build_briefing()
        print(json.dumps(quotes, indent=2, ensure_ascii=False))
        return
    text, _ = build_briefing()
    if text is None:
        sys.stderr.write("No quotes fetched; skipping.\n")
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
