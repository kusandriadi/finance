#!/usr/bin/env python3
"""market_briefing.py — daily market snapshot for Kus.

Self-contained: needs only `requests` (no numpy/pandas/yfinance). Fetches a
small basket of instruments from Yahoo Finance and prints a chat-friendly
briefing (no markdown tables — WhatsApp/Telegram safe).

Usage:
    python3 market_briefing.py            # full briefing
    python3 market_briefing.py --json     # raw quotes as JSON
    python3 market_briefing.py --mode ihsg-fx
"""
import sys
import json
import time
import urllib.parse
from datetime import datetime, timezone

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) finance-briefing/1.0"}

# (symbol, label, value_format)  — value_format: "idr", "usd", "num", "pts"
MARKET_BASKET = [
    ("^JKSE", "IHSG", "pts"),
    ("XAUUSD=X", "Emas (XAU/USD)", "usd"),
    ("GC=F", "Emas Futures", "usd"),
    ("^GSPC", "S&P 500", "pts"),
    ("^IXIC", "Nasdaq", "pts"),
    ("^N225", "Nikkei 225", "pts"),
    ("CL=F", "Minyak (WTI)", "usd"),
    ("BZ=F", "Minyak (Brent)", "usd"),
    ("BTC-USD", "Bitcoin", "usd"),
]

US_STOCKS = [
    ("NVDA", "NVDA", "usd"),
    ("GOOG", "GOOG", "usd"),
    ("AAPL", "AAPL", "usd"),
    ("MSFT", "MSFT", "usd"),
    ("AMZN", "AMZN", "usd"),
    ("SPCX", "SPCX", "usd"),
    ("TSLA", "TSLA", "usd"),
    ("AMD", "AMD", "usd"),
    ("INTC", "INTC", "usd"),
    ("GRAB", "GRAB", "usd"),
]

ID_STOCKS = [
    ("BBCA.JK", "BBCA", "idr"),
    ("BMRI.JK", "BMRI", "idr"),
    ("BBRI.JK", "BBRI", "idr"),
    ("BBNI.JK", "BBNI", "idr"),
    ("BRIS.JK", "BRIS", "idr"),
    ("BBTN.JK", "BBTN", "idr"),
    ("TLKM.JK", "TLKM", "idr"),
    ("ANTM.JK", "ANTM", "idr"),
    ("PGAS.JK", "PGAS", "idr"),
    ("ADMR.JK", "ADMR", "idr"),
]

FX_BASKET = [
    ("SGDIDR=X", "SGD/IDR", "idr"),
    ("MYRIDR=X", "RM/IDR", "idr"),
    ("IDR=X", "USD/IDR", "idr"),
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


def arrow_for_item(symbol, pct):
    # FX quotes are stored as foreign-currency/IDR, but Kus wants color from
    # Rupiah's perspective: green when IDR strengthens, red when IDR weakens.
    if symbol in {item[0] for item in FX_BASKET}:
        return arrow(-pct)
    return arrow(pct)


def display_pct_for_item(symbol, pct):
    if symbol in {item[0] for item in FX_BASKET}:
        return -pct
    return pct


def collect_quotes(items):
    quotes = {}
    for symbol, label, kind in items:
        q = fetch_quote(symbol)
        if q is None:
            quotes[symbol] = {"label": label, "kind": kind, "error": True}
            continue
        last, prev, as_of = q
        pct = (last - prev) / prev * 100 if prev else 0.0
        quotes[symbol] = {
            "label": label,
            "kind": kind,
            "last": last,
            "prev": prev,
            "pct": pct,
            "as_of": as_of,
        }
    return quotes


def append_section(lines, title, items, quotes):
    lines.append(title)
    for symbol, label, _ in items:
        q = quotes.get(symbol)
        if not q or q.get("error"):
            lines.append(f"⚪️= {label}: data tidak tersedia")
            continue
        pct = q["pct"]
        display_pct = display_pct_for_item(symbol, pct)
        tail = f" · tutup {q['as_of']}" if q.get("as_of") else ""
        lines.append(
            f"{arrow_for_item(symbol, pct)} {q['label']}: {fmt_value(q['last'], q['kind'])} ({display_pct:+.2f}%){tail}"
        )
    lines.append("")


def ihsg_summary(quotes):
    ihsg = quotes.get("^JKSE")
    if not ihsg or ihsg.get("error"):
        return "IHSG"
    pct = ihsg["pct"]
    if pct > 0.05:
        return f"IHSG naik {pct:.2f}%"
    if pct < -0.05:
        return f"IHSG turun {abs(pct):.2f}%"
    return "IHSG flat 0.00%"


def build_briefing(mode="full"):
    now = datetime.now().strftime("%A, %d %b %Y, %H:%M WIB")
    quotes = {}
    quotes.update(collect_quotes(MARKET_BASKET))
    quotes.update(collect_quotes(ID_STOCKS))
    quotes.update(collect_quotes(FX_BASKET))
    if mode == "full":
        quotes.update(collect_quotes(US_STOCKS))

    if mode == "ihsg-fx":
        lines = [
            f"📊 *IHSG Briefing* — {now}",
            "",
        ]
        append_section(lines, f"Saham IHSG ({ihsg_summary(quotes)})", ID_STOCKS, quotes)
        append_section(lines, "Mata uang asing ke rupiah", FX_BASKET, quotes)
    else:
        lines = [
            f"📊 *Market Briefing* — {now}",
            "Angka = harga penutupan terakhir tiap pasar/saham.",
            "",
        ]
        append_section(lines, "Pasar utama", MARKET_BASKET, quotes)
        append_section(lines, "Saham NASDAQ", US_STOCKS, quotes)
        append_section(lines, f"Saham IHSG ({ihsg_summary(quotes)})", ID_STOCKS, quotes)
        append_section(lines, "Mata uang asing ke rupiah", FX_BASKET, quotes)

    if len(lines) <= 7:
        return None, {}
    lines.append("_Bukan saran finansial. Data: Yahoo Finance (delayed)._")
    return "\n".join(lines), quotes


def main():
    mode = "full"
    if "--mode" in sys.argv:
        try:
            mode = sys.argv[sys.argv.index("--mode") + 1]
        except Exception:
            sys.stderr.write("Missing value for --mode.\n")
            sys.exit(2)
    if "--json" in sys.argv:
        _, quotes = build_briefing(mode=mode)
        print(json.dumps(quotes, indent=2, ensure_ascii=False))
        return
    text, _ = build_briefing(mode=mode)
    if text is None:
        sys.stderr.write("No quotes fetched; skipping.\n")
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
