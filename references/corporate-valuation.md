# Corporate Valuation (DCF & metode lain)

**Lanjutan / teknis.** Cara menaksir **nilai intrinsik** sebuah bisnis — inti dari
"harga vs nilai" di `market-analysis.md`. Berguna untuk investor fundamental serius,
analisis emiten, atau menilai bisnis sendiri. Lengkapi dengan `reading-financials.md`
(sumber angkanya).

> Valuasi = **estimasi, bukan kebenaran**. Output sangat sensitif terhadap asumsi
> ("garbage in, garbage out"). Selalu pakai rentang & skenario, bukan satu angka pasti.

## Dua pendekatan besar

### 1. Intrinsic — DCF (Discounted Cash Flow)

Nilai = sekarang dari semua arus kas masa depan, didiskonto ke nilai kini.

**Langkah:**
1. **Proyeksikan Free Cash Flow** (FCF = arus kas operasi − capex) beberapa tahun
   (mis. 5–10 th), berbasis asumsi pertumbuhan & margin yang realistis.
2. **Tentukan discount rate** = **WACC** (biaya modal rata-rata tertimbang utang+ekuitas).
   Makin berisiko/tak pasti → diskonto makin tinggi → nilai makin rendah.
3. **Terminal value** untuk arus kas setelah periode proyeksi — biasanya **Gordon Growth**:
   TV = FCF×(1+g) ÷ (WACC − g), dengan g (pertumbuhan abadi) konservatif (≤ pertumbuhan
   ekonomi jangka panjang). TV sering **mayoritas** nilai — hati-hati, di sinilah asumsi
   paling rawan.
4. **Diskontokan** semua FCF + TV ke nilai sekarang → **Enterprise Value**.
5. EV − utang bersih = **Equity Value** ÷ jumlah saham = **nilai wajar per saham**.

Hitung present value dengan `scripts/calc.py pv` per arus kas (rumus PV = FV ÷ (1+r)^n).

**Kelemahan DCF:** sangat sensitif ke WACC & g (selisih 1% bisa mengubah nilai puluhan
persen). Bagus untuk bisnis stabil & terprediksi; payah untuk perusahaan rugi/awal/siklikal.

### 2. Relative — multiple/comparable

Bandingkan dengan emiten sejenis pakai rasio (lihat `market-analysis.md`):
- **P/E, P/BV, EV/EBITDA, P/S, PEG** (P/E ÷ pertumbuhan).
- Ambil multiple median sektor × metrik emiten → taksiran nilai.
- **Cepat & berbasis pasar**, tapi ikut "salah harga" pasar; pilih pembanding yang benar-benar sebanding.

### Pelengkap
- **Asset-based / NAV:** nilai aset bersih — untuk holding, properti, bank, likuidasi.
- **Dividend Discount Model (DDM):** untuk emiten dividen stabil (mirip DCF atas dividen).

## Konsep pendukung

- **WACC:** tertimbang biaya ekuitas (sering via CAPM: rf + β×equity risk premium) & biaya
  utang setelah pajak. Di **emerging market (ID)** tambahkan country risk premium → WACC
  cenderung lebih tinggi.
- **Margin of safety (Graham/Buffett):** beli hanya bila harga **jauh di bawah** nilai
  wajar — bantalan untuk salah asumsi. Inti investasi nilai.
- **Sensitivity & scenario:** buat tabel nilai vs (WACC × g), plus skenario bear/base/bull.
  Hasilnya **rentang**, dan keputusan dibuat dari rentang itu.

## Disiplin

- **Asumsi > rumus.** Pertumbuhan & margin harus dibumikan ke realitas bisnis/industri,
  bukan ekstrapolasi optimis (`market-analysis.md` — bias konfirmasi).
- **Triangulasi:** bandingkan DCF dengan multiple & NAV; kalau jomplang, cari tahu kenapa.
- **Kualitas dulu, harga kemudian:** valuasi murah atas bisnis rusak = jebakan nilai
  (`reading-financials.md`).
- **Bank/asuransi divaluasi beda** (P/BV, ROE, model dividen) — FCF/EV/EBITDA kurang pas.
- Untuk investor pasif, ini **tidak wajib** — index/reksadana melewati kebutuhan valuasi
  satu per satu (`investing-basics.md`).
