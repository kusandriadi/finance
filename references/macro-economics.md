# Macro & Economics

Kerangka makro buat baca "cuaca" ekonomi yang menggerakkan semua aset. Pelengkap
`market-analysis.md` (yang fokus emiten & teknikal). Untuk angka terkini (BI-Rate,
inflasi), lihat `references/rates.md`.

## Siklus ekonomi (4 fase)

1. **Ekspansi** — pertumbuhan naik, pengangguran turun, kredit longgar, optimisme.
   Saham & komoditas cenderung kuat.
2. **Puncak (peak)** — ekonomi panas, inflasi naik, bank sentral mulai mengetat.
3. **Kontraksi/resesi** — pertumbuhan melambat/negatif, PHK, kredit seret. Saham tertekan,
   obligasi & kas/emas jadi pelindung.
4. **Palung (trough) → pemulihan** — bank sentral melonggarkan, fondasi pemulihan.

Tidak ada yang bisa *timing* siklus dengan tepat. Gunanya: tahu **di mana kira-kira kita**
untuk kalibrasi ekspektasi & risiko, bukan untuk all-in/all-out.

## Kebijakan moneter (Bank Indonesia / The Fed)

- **Alat utama: suku bunga acuan (BI-Rate).** Naik → meredam inflasi & jaga kurs, tapi
  menekan harga saham/obligasi & memperlambat ekonomi. Turun → sebaliknya (stimulus).
- **Transmisi:** bunga acuan → bunga kredit/deposito → konsumsi & investasi → harga aset.
- **The Fed (AS) penting buat ID:** Fed naik → dolar menguat, modal asing bisa keluar dari
  emerging market (termasuk IDX/SBN), tekanan ke Rupiah. BI sering harus ikut menjaga selisih.
- **Quantitative easing/tightening:** bank sentral besar menambah/menarik likuiditas global.

## Kebijakan fiskal (pemerintah)

- **Belanja & pajak.** Defisit/stimulus → dorong permintaan jangka pendek. Konsolidasi →
  rem. Pajak baru/insentif (mis. PPN, insentif UMKM) langsung kena dompet & emiten.
- **Utang & rasio defisit** memengaruhi yield SBN & rating utang negara.

## Indikator yang dipantau

- **Pertumbuhan PDB** (yoy) — kesehatan ekonomi keseluruhan.
- **Inflasi (IHK, yoy)** — daya beli & arah kebijakan bunga. Target BI 2,5%±1%.
- **Pengangguran & belanja konsumen** — mesin ekonomi ID (konsumsi ~separuh PDB).
- **Neraca dagang & transaksi berjalan (CAD)** — surplus = topang Rupiah.
- **Cadangan devisa** — amunisi BI menjaga kurs.
- **USD/IDR** — barometer sentimen asing & tekanan impor/utang USD.
- **Harga komoditas** (batu bara, CPO, nikel, minyak) — ID eksportir; gerakkan emiten & ekspor.
- **PMI manufaktur** — >50 ekspansi, <50 kontraksi (leading indicator).

## Yield curve & obligasi (sinyal yang sering diabaikan)

- **Yield naik → harga obligasi turun** (hubungan terbalik). Penting buat pemegang SBN/RDPT.
- **Kurva normal** (tenor panjang > pendek) = ekspektasi sehat. **Inverted** (pendek >
  panjang) sering jadi sinyal awal perlambatan/resesi.
- **Spread vs US Treasury** menentukan daya tarik SBN buat asing.

## Kelas aset di tiap rezim (panduan kasar, bukan dogma)

- **Pertumbuhan↑ inflasi↓ ("goldilocks"):** saham favorit.
- **Pertumbuhan↑ inflasi↑:** komoditas, emiten komoditas, sebagian saham.
- **Pertumbuhan↓ inflasi↑ (stagflasi):** sulit — emas/komoditas/kas relatif bertahan.
- **Pertumbuhan↓ inflasi↓ (resesi/disinflasi):** obligasi/SBN & kas; saham defensif.

## Disiplin makro

- **Makro itu konteks, bukan timing.** Jangan jual semua karena satu berita resesi —
  pasar sering sudah *priced in* dan mendahului ekonomi riil.
- **Diversifikasi lintas rezim** lebih andal daripada menebak satu skenario (lihat
  `risk-management.md` & `model-portfolios.md`).
- **Yang bisa dikontrol:** alokasi, biaya, saving rate, horizon. Suku bunga global tidak.
- Inflasi adalah pajak diam-diam — pikirkan **return riil**, bukan nominal
  (`scripts/calc.py real`).
