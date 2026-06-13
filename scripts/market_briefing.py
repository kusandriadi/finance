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
from datetime import datetime, timezone

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


_ID_DAYS = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]  # Mon..Sun


def as_of_label(market_time, gmtoffset):
    """Format the last-quote time in the exchange's own timezone.

    Returns e.g. 'Jum 12/6 16:00', or None if we can't tell. Using the
    exchange tz (not WIB) keeps the close date correct — converting a US
    16:00 close to WIB would roll it to the next day."""
    if market_time is None:
        return None
    try:
        # Shift the UTC epoch by the exchange offset, then read the wall-clock
        # components — gives exchange-local date/time without a tz database.
        local = datetime.fromtimestamp(
            int(market_time) + int(gmtoffset or 0), tz=timezone.utc)
        return f"{_ID_DAYS[local.weekday()]} {local.day}/{local.month} {local:%H:%M}"
    except Exception:
        return None


def fetch_quote(symbol, retries=3):
    """Return (last, prev_close, as_of) or None. as_of may be None."""
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
            as_of = as_of_label(meta.get("regularMarketTime"), meta.get("gmtoffset"))
            return float(last), float(prev), as_of
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
    now = datetime.now().strftime("%A, %d %b %Y, %H:%M WIB")
    lines = [
        f"📊 *Market Briefing* — {now}",
        "Angka = harga penutupan terakhir tiap pasar.",
        "",
    ]
    quotes = {}
    for symbol, label, kind in BASKET:
        q = fetch_quote(symbol)
        if q is None:
            continue
        last, prev, as_of = q
        pct = (last - prev) / prev * 100 if prev else 0.0
        quotes[symbol] = {"label": label, "last": last, "prev": prev,
                          "pct": pct, "as_of": as_of}
        tail = f" · tutup {as_of}" if as_of else ""
        lines.append(f"{arrow(pct)} {label}: {fmt_value(last, kind)} ({pct:+.2f}%){tail}")
    if len(lines) <= 3:
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
