# Model Portfolios

Contoh alokasi aset sebagai **titik awal diskusi**, bukan resep wajib. Sesuaikan dengan
horizon, toleransi risiko, dan tujuan (lihat `financial-planning.md` & `risk-management.md`).
Semua angka ilustratif — bukan rekomendasi beli instrumen tertentu.

> **Aturan #1: fondasi dulu.** Dana darurat penuh + utang bunga tinggi lunas + proteksi
> dasar **sebelum** portofolio agresif. Alokasi di bawah mengasumsikan fondasi sudah ada.

## Berdasarkan profil risiko

Komposisi kasar **saham : obligasi/SBN : kas/emas**. "Saham" boleh lewat RD saham/index.

- **Konservatif** (horizon pendek / tidak tahan turun):
  ~20% saham, 50% obligasi/SBN, 30% kas/RDPU + sedikit emas.
- **Moderat** (horizon menengah, seimbang):
  ~50% saham, 35% obligasi/SBN, 15% kas/emas.
- **Agresif** (horizon panjang >10 th, tahan volatil):
  ~80% saham, 15% obligasi/SBN, 5% kas/emas.

Panduan usia kasar: **bobot saham ≈ (100 − usia)%** — geser sesuai kapasitas & psikologis
(`financial-planning.md`). Emas sebagai diversifier biasanya porsi kecil (5–10%).

## Berdasarkan horizon tujuan (paling menentukan)

- **< 2 tahun** (dana darurat, DP dekat) → 100% kas/RDPU/deposito. **Jangan saham.**
- **2–5 tahun** → mayoritas pendapatan tetap/SBN + RD campuran; saham porsi kecil.
- **5–10 tahun** → campuran condong saham (mis. 60/40).
- **> 10 tahun** (pensiun jauh) → mayoritas saham/RD saham; volatilitas terserap waktu.

**Glide path:** makin dekat tujuan, geser bertahap dari agresif → konservatif untuk
mengunci hasil (mis. 3 th sebelum DP rumah, pindahkan ke instrumen aman).

## Pola praktis

### Core–satellite
- **Core (80–90%):** RD index/saham + SBN — murah, pasif, stabil. Mesin utama.
- **Satellite (10–20%):** saham pilihan / tematik / sedikit crypto — ruang main aktif
  tanpa mempertaruhkan inti. Kalau satelit jeblok, tujuan inti tetap aman.

### Three-fund sederhana (ala Bogleheads, versi ID)
- RD/ETF saham domestik (mis. ikut IDX30/LQ45) + (opsional) saham global +
  SBN/RD pendapatan tetap + RDPU sebagai kas. Murah, mudah, sulit dikalahkan jangka panjang.

### Lazy all-weather (tahan segala cuaca)
- Sebar lintas saham, obligasi, emas, kas agar tak ada satu rezim makro yang menghancurkan
  (lihat `macro-economics.md`). Return lebih kalem, drawdown lebih dangkal.

## Contoh: alokasi untuk satu tujuan

Misal **DP rumah Rp200jt dalam 4 tahun** (horizon menengah, dana tak boleh rugi besar):
- Mayoritas di RDPU/SBN/deposito; porsi kecil RD campuran.
- Hitung setoran bulanan: `python3 scripts/calc.py dca --goal 200000000 --years 4 --rate 6`.
- Tahun ke-4 (mendekati pakai) → geser semua ke kas. Jangan biarkan saham mengancam timing.

## Disiplin pengelolaan

- **Rebalancing berkala** (tahunan atau saat deviasi >5%): jual yang naik, beli yang turun,
  kembali ke target. Mekanis, lawan emosi (`risk-management.md`).
- **Otomatisasi setoran** (DCA) tepat setelah gajian — konsistensi > timing.
- **Minimalkan biaya & pajak** — expense ratio rendah, jangan over-trading
  (`investing-basics.md`).
- **Satu portofolio, banyak tujuan:** boleh pisahkan per-tujuan (ember/bucket) agar horizon
  tiap dana jelas dan tidak saling ganggu.
- **Jangan utak-atik karena berita.** Rencana yang dipegang konsisten mengalahkan rencana
  "bagus" yang sering diganti.
