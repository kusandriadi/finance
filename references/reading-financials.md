# Reading Financial Statements

Cara membaca **laporan keuangan** emiten agar analisis fundamental tidak berhenti di
rasio hafalan. Tiga laporan inti + cara baca + sinyal bahaya. Lengkapi dengan
`market-analysis.md` (rasio) dan `indonesia-context.md` (pajak/instrumen).

> Sumber resmi: laporan tahunan/triwulan di **IDX (idx.co.id)** atau situs IR emiten.
> Baca yang **diaudit** (opini auditor: *wajar tanpa pengecualian* = WTP itu ideal).

## Tiga laporan yang harus nyambung

### 1. Laba-Rugi (Income Statement) — kinerja selama periode

Alur dari atas ke bawah:
- **Pendapatan / Revenue** (top line) — penjualan. Tumbuh konsisten?
- **− HPP (COGS)** → **Laba Kotor** → **Gross margin** = laba kotor ÷ pendapatan.
- **− Beban operasi** (gaji, pemasaran, umum) → **Laba Operasi (EBIT)**.
- **− Beban bunga & pajak** → **Laba Bersih** (bottom line) → **Net margin**.
- **EPS** (laba per saham) = laba bersih ÷ jumlah saham. Dasar dari PER.

Baca **tren beberapa tahun & margin**, bukan sekadar "untung/rugi". Laba naik tapi
margin turun = tumbuh tapi makin tidak efisien / perang harga.

### 2. Neraca (Balance Sheet) — posisi pada satu titik waktu

**Aset = Liabilitas + Ekuitas.** (selalu balance)
- **Aset:** lancar (kas, piutang, persediaan) vs tidak lancar (pabrik, goodwill).
- **Liabilitas:** jangka pendek (utang ≤1 th) vs jangka panjang.
- **Ekuitas:** hak pemegang saham (modal + laba ditahan). Dasar dari PBV & ROE.

Cek: **DER** (utang/ekuitas), **current ratio** (aset lancar ÷ liabilitas lancar,
≥1 sehat), porsi **utang berbunga**, dan apakah laba ditahan tumbuh.

### 3. Arus Kas (Cash Flow) — uang nyata masuk/keluar (paling jujur)

- **Operasi (CFO)** — kas dari bisnis inti. **Harus positif & sehat.** Bandingkan
  dengan laba bersih: kalau laba besar tapi CFO kecil/negatif → laba "di atas kertas",
  red flag (piutang menumpuk / akuntansi agresif).
- **Investasi (CFI)** — beli/jual aset (capex). Negatif wajar untuk perusahaan tumbuh.
- **Pendanaan (CFF)** — utang baru, bayar utang, dividen, buyback.
- **Free Cash Flow (FCF)** = CFO − capex. Inti kemampuan bayar dividen & tumbuh tanpa
  numpuk utang.

## Menyatukannya — pertanyaan yang dijawab

- **Tumbuh?** Revenue & laba beberapa tahun (bukan satu kuartal beruntung).
- **Efisien?** ROE konsisten tinggi, margin stabil/naik.
- **Aman?** DER terkendali, current ratio ≥1, utang berbunga tidak mengkhawatirkan.
- **Nyata?** CFO sejalan dengan laba; FCF positif. **Cash is king.**
- **Murah?** Baru lihat PER/PBV — *setelah* kualitas di atas oke, bukan sebelumnya.
  Murah karena bisnis rusak ≠ murah karena salah harga (lihat `market-analysis.md`).

## Sinyal bahaya (red flags)

- **Laba naik, arus kas operasi turun/negatif** — kualitas laba buruk.
- **Piutang/persediaan tumbuh jauh lebih cepat dari penjualan** — barang/uang nyangkut.
- **Utang berbunga membengkak** sementara laba stagnan — rapuh saat bunga naik.
- **Opini auditor selain WTP**, sering ganti auditor, atau lapkeu telat terus.
- **Laba bergantung "pendapatan lain-lain"** (jual aset, untung sekali) bukan operasi inti.
- **Dividen/buyback dibiayai utang**, bukan FCF.
- **Saham gorengan:** likuiditas tipis, fundamental tak mendukung lonjakan harga
  (lihat `investing-basics.md` — jebakan umum).

## Catatan

- **Bandingkan antar emiten sesektor & vs historis sendiri** — angka absolut tidak
  bermakna sendirian.
- **Bank/keuangan beda total** (tidak ada COGS; lihat NIM, NPL, CAR) — kerangka di atas
  untuk perusahaan non-keuangan.
- Untuk skor teknikal cepat saham IDX, ada engine di skill `ihsg-swing-trading`. Dok ini
  soal **kualitas bisnis**, bukan timing.
