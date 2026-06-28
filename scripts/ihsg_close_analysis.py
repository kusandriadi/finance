#!/usr/bin/env python3
"""ihsg_close_analysis.py — weekday morning analysis for prior IHSG close.

Fetches prior-close market context plus fresh headlines, then formats a short
WhatsApp-friendly analysis focused on IHSG.
"""
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ihsg-close-analysis/1.0"}

MARKETS = [
    ("^JKSE", "IHSG", "pts"),
    ("^GSPC", "S&P 500", "pts"),
    ("^IXIC", "Nasdaq", "pts"),
    ("^N225", "Nikkei 225", "pts"),
    ("^HSI", "Hang Seng", "pts"),
    ("000001.SS", "Shanghai Composite", "pts"),
    ("IDR=X", "USD/IDR", "idr"),
    ("BZ=F", "Brent", "usd"),
    ("CL=F", "WTI", "usd"),
]

RSS_QUERIES = {
    "regional": [
        ("Regional/global", "Asian markets OR China economy OR Federal Reserve OR Treasury yields OR oil prices OR Wall Street"),
    ],
    "domestic": [
        ("Ekonomi/politik RI", "Bursa Efek Indonesia OR OJK OR Bank Indonesia OR rupiah OR ekonomi Indonesia OR APBN OR kebijakan pemerintah"),
    ],
    "index_review": [
        ("MSCI/FTSE", "IHSG MSCI FTSE OR MSCI Indonesia OR FTSE Russell Indonesia"),
    ],
}

POSITIVE_WORDS = {
    "naik", "menguat", "surplus", "rebound", "stimulus", "deal", "optimis",
    "cut", "pangkas", "mereda", "melonggar", "solid", "growth", "support",
}
NEGATIVE_WORDS = {
    "turun", "melemah", "defisit", "hawkish", "inflasi", "selloff", "war",
    "perang", "tarif", "ketegangan", "konflik", "krisis", "drop", "anjlok",
    "tekan", "outflow", "panic", "panic", "gejolak",
}

ID_DAYS = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]


def as_of_label(market_time, gmtoffset):
    if market_time is None:
        return None
    try:
        local = datetime.fromtimestamp(
            int(market_time) + int(gmtoffset or 0), tz=timezone.utc
        )
        return f"{ID_DAYS[local.weekday()]} {local.day}/{local.month} {local:%H:%M}"
    except Exception:
        return None


def fetch_quote(symbol, retries=3):
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
            result = r.json()["chart"]["result"][0]
            meta = result.get("meta", {})
            closes = [
                c for c in result["indicators"]["quote"][0]["close"] if c is not None
            ]
            if len(closes) >= 2:
                last = meta.get("regularMarketPrice") or closes[-1]
                prev = closes[-2]
            else:
                last = meta.get("regularMarketPrice")
                prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            if last is None or prev is None:
                return None
            return {
                "last": float(last),
                "prev": float(prev),
                "pct": ((float(last) - float(prev)) / float(prev) * 100) if prev else 0.0,
                "as_of": as_of_label(meta.get("regularMarketTime"), meta.get("gmtoffset")),
            }
        except Exception:
            time.sleep(1 + attempt)
    return None


def fmt_value(val, kind):
    if kind == "idr":
        return f"{val:,.0f}".replace(",", ".")
    if kind == "usd":
        return f"${val:,.2f}"
    return f"{val:,.2f}"


def arrow(pct):
    if pct > 0.05:
        return "🟢▲"
    if pct < -0.05:
        return "🔴▼"
    return "⚪️="


def fetch_rss(query, limit=3):
    encoded = urllib.parse.quote(query)
    url = (
        "https://news.google.com/rss/search?q="
        + encoded
        + "&hl=id&gl=ID&ceid=ID:id"
    )
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    items = []
    for item in root.findall("./channel/item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        source = ""
        source_node = item.find("source")
        if source_node is not None and source_node.text:
            source = source_node.text.strip()
        items.append({"title": title, "link": link, "source": source})
    return items


def headline_score(text):
    lower = text.lower()
    pos = sum(1 for word in POSITIVE_WORDS if word in lower)
    neg = sum(1 for word in NEGATIVE_WORDS if word in lower)
    return pos - neg


def classify_effect(text):
    score = headline_score(text)
    if score > 0:
        return "cenderung positif"
    if score < 0:
        return "cenderung negatif"
    return "campuran/netral"


def summarize_market_effect(quotes):
    ihsg = quotes.get("IHSG")
    us = quotes.get("Nasdaq")
    spx = quotes.get("S&P 500")
    nikkei = quotes.get("Nikkei 225")
    usd = quotes.get("USD/IDR")
    brent = quotes.get("Brent")

    signals = []
    if spx and us:
        if spx["pct"] > 0 and us["pct"] > 0:
            signals.append("sentimen risk-on global cukup bantu pembukaan IHSG")
        elif spx["pct"] < 0 and us["pct"] < 0:
            signals.append("sentimen risk-off global bisa menekan IHSG")
    if nikkei:
        if nikkei["pct"] > 0:
            signals.append("bursa Asia pagi relatif memberi tailwind")
        elif nikkei["pct"] < 0:
            signals.append("bursa Asia pagi memberi tekanan awal")
    if usd:
        if usd["pct"] > 0.2:
            signals.append("rupiah yang melemah berisiko menahan saham sensitif impor/asing")
        elif usd["pct"] < -0.2:
            signals.append("rupiah yang menguat bisa bantu sentimen domestik")
    if brent:
        if brent["pct"] > 1:
            signals.append("minyak yang naik cenderung bantu emiten energi, tapi tekan inflasi")
        elif brent["pct"] < -1:
            signals.append("minyak yang turun bisa meringankan tekanan inflasi, tapi membebani saham energi")

    if not signals:
        return "pembukaannya cenderung netral, jadi fokus pasar kemungkinan pindah ke headline domestik."
    return "; ".join(signals) + "."


def build_macro_takeaways(quotes):
    points = []
    us = quotes.get("Nasdaq")
    spx = quotes.get("S&P 500")
    hs = quotes.get("Hang Seng")
    sh = quotes.get("Shanghai Composite")
    nikkei = quotes.get("Nikkei 225")
    usd = quotes.get("USD/IDR")
    brent = quotes.get("Brent")
    wti = quotes.get("WTI")

    if spx and us:
        if spx["pct"] > 0.5 and us["pct"] > 0.5:
            points.append(
                "Wall Street ditutup kuat, jadi risk appetite global sebenarnya masih ada. "
                "Kalau IHSG tetap lemah, berarti pasar domestik sedang dihukum oleh faktor lokal atau arus keluar asing."
            )
        elif spx["pct"] < -0.5 and us["pct"] < -0.5:
            points.append(
                "Wall Street melemah kompak, jadi tekanan ke IHSG lebih masuk akal kalau datang dari risk-off global."
            )

    asia_weak = sum(
        1 for q in [hs, sh] if q and q["pct"] < -0.3
    )
    if nikkei and nikkei["pct"] > 0.3 and asia_weak:
        points.append(
            "Bursa Asia tidak satu arah. Jepang relatif kuat, tapi China/Hong Kong lemah. "
            "Artinya pasar kawasan masih pilih-pilih, belum benar-benar risk-on penuh."
        )

    if usd:
        if usd["pct"] > 0.3:
            points.append(
                "Rupiah yang melemah biasanya bikin investor asing lebih hati-hati, terutama ke bank besar dan saham likuid, "
                "karena return saham bisa tergerus pelemahan kurs."
            )
        elif usd["pct"] < -0.3:
            points.append(
                "Rupiah yang menguat bisa bantu sentimen domestik dan menurunkan tekanan outflow jangka pendek."
            )

    oil_down = any(q and q["pct"] < -1 for q in [brent, wti])
    if oil_down:
        points.append(
            "Minyak yang turun cukup dalam cenderung positif buat narasi inflasi dan import bill Indonesia, "
            "tapi kurang bagus untuk ekspektasi saham energi/komoditas minyak."
        )

    if not points:
        points.append(
            "Peta global pagi ini belum memberi sinyal ekstrem, jadi penjelas utama gerak IHSG kemungkinan tetap datang dari faktor domestik dan positioning investor."
        )
    return points[:3]


def build_domestic_takeaways(domestic_items):
    titles = " ".join(item["title"] for item in domestic_items).lower()
    points = []
    if any(word in titles for word in ["bei", "ojk", "direksi", "bursa"]):
        points.append(
            "Headline soal BEI/OJK lebih berpengaruh ke persepsi governance dan kepercayaan pasar daripada ke laba emiten secara langsung. "
            "Efeknya biasanya ke sentimen, bukan ke fundamental jangka pendek."
        )
    if any(word in titles for word in ["rupiah", "bank indonesia", "bi-rate", "suku bunga"]):
        points.append(
            "Kalau fokus headline bergeser ke rupiah atau BI, pasar biasanya cepat mem-price dampaknya ke perbankan, consumer, dan arus dana asing."
        )
    if any(word in titles for word in ["apbn", "pemerintah", "kebijakan", "pajak"]):
        points.append(
            "Kalau isu kebijakan fiskal/pemerintah menguat, pasar akan lebih sensitif ke sektor yang sangat bergantung pada regulasi dan belanja negara."
        )
    if any(word in titles for word in ["msci", "ftse", "russell", "rebalancing", "review indeks", "review index"]):
        points.append(
            "Isu MSCI/FTSE penting karena biasanya berhubungan dengan arus dana pasif, potensi inflow/outflow, dan tekanan teknikal di saham-saham big caps. "
            "Efeknya sering terasa cepat ke BBCA, BBRI, BMRI, TLKM, dan nama-nama likuid lain, bahkan sebelum fundamental berubah."
        )
    if not points:
        points.append(
            "Dari sisi domestik, belum terlihat satu katalis besar yang jelas bullish. Jadi nada pasar kemungkinan masih hati-hati, menunggu validasi dari aliran dana dan rupiah."
        )
    return points[:2]


def build_focus_watch(quotes):
    usd = quotes.get("USD/IDR")
    brent = quotes.get("Brent")
    ihsg = quotes.get("IHSG")
    points = []
    if usd:
        points.append("pantau USD/IDR; kalau dolar lanjut naik, IHSG biasanya lebih susah rebound lebar")
    if ihsg:
        points.append("lihat apakah IHSG mampu stabil setelah penurunan kemarin, atau justru lanjut distribusi di saham-saham big caps")
    if brent:
        points.append("cek reaksi saham energi/komoditas terhadap harga minyak yang melemah")
    return points[:3]


def build_report():
    now = datetime.now().strftime("%A, %d %b %Y, %H:%M WIB")
    quotes = {}
    for symbol, label, kind in MARKETS:
        q = fetch_quote(symbol)
        if q:
            q["label"] = label
            q["kind"] = kind
            quotes[label] = q

    ihsg = quotes.get("IHSG")
    if not ihsg:
        return None

    regional_items = []
    domestic_items = []
    index_review_items = []
    for _, query in RSS_QUERIES["regional"]:
        regional_items.extend(fetch_rss(query, limit=3))
    for _, query in RSS_QUERIES["domestic"]:
        domestic_items.extend(fetch_rss(query, limit=3))
    for _, query in RSS_QUERIES["index_review"]:
        index_review_items.extend(fetch_rss(query, limit=3))

    # Keep the first two unique headlines per bucket.
    def uniq(items):
        seen = set()
        out = []
        for item in items:
            key = item["title"]
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(item)
            if len(out) == 2:
                break
        return out

    regional_items = uniq(regional_items)
    domestic_items = uniq(domestic_items)
    index_review_items = uniq(index_review_items)

    lines = [
        f"🧭 *Analisa Penutupan IHSG* — {now}",
        f"IHSG penutupan sebelumnya: {arrow(ihsg['pct'])} {fmt_value(ihsg['last'], ihsg['kind'])} ({ihsg['pct']:+.2f}%)"
        + (f" · tutup {ihsg['as_of']}" if ihsg.get("as_of") else ""),
        "",
        "Gambaran besar",
    ]

    for point in build_macro_takeaways(quotes):
        lines.append(f"- {point}")

    lines.extend([
        "",
        "Isu regional/global",
    ])
    if regional_items:
        for item in regional_items:
            effect = classify_effect(item["title"])
            src = f" [{item['source']}]" if item["source"] else ""
            lines.append(f"- {item['title']}{src}")
            lines.append(f"  Artinya: {effect} untuk sentimen, tapi tetap perlu lihat apakah efeknya kena rupiah, arus asing, atau sektor tertentu.")
    else:
        lines.append("- Tidak ada headline regional yang berhasil diambil pagi ini.")

    lines.extend([
        "",
        "Isu MSCI / FTSE",
    ])
    if index_review_items:
        for item in index_review_items:
            effect = classify_effect(item["title"])
            src = f" [{item['source']}]" if item["source"] else ""
            lines.append(f"- {item['title']}{src}")
            lines.append(
                "  Artinya: "
                + effect
                + "; ini penting karena keputusan MSCI/FTSE sering memicu inflow/outflow pasif dan tekanan teknikal di saham-saham big caps."
            )
    else:
        lines.append("- Belum ada headline MSCI/FTSE yang ketarik pagi ini.")

    lines.extend([
        "",
        "Isu ekonomi/politik RI",
    ])
    if domestic_items:
        for item in domestic_items:
            effect = classify_effect(item["title"])
            src = f" [{item['source']}]" if item["source"] else ""
            lines.append(f"- {item['title']}{src}")
            lines.append(f"  Artinya: {effect}; dampaknya lebih ke kepercayaan pasar dan positioning investor daripada langsung ke semua sektor.")
    else:
        lines.append("- Tidak ada headline domestik yang berhasil diambil pagi ini.")

    lines.extend([
        "",
        "Pembacaan lebih dalam",
    ])
    for point in build_domestic_takeaways(domestic_items + index_review_items):
        lines.append(f"- {point}")

    lines.extend([
        "",
        "Fokus pasar hari ini",
        f"- {summarize_market_effect(quotes)}",
    ])
    for point in build_focus_watch(quotes):
        lines.append(f"- {point}")
    lines.extend([
        "",
        "_Bukan saran finansial. Data harga: Yahoo Finance. Headline: Google News RSS / media sumber pada headline._",
    ])
    return "\n".join(lines)


def main():
    report = build_report()
    if not report:
        raise SystemExit("No report generated.")
    print(report)


if __name__ == "__main__":
    main()
