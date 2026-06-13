# Rates & Thresholds (angka volatil)

Satu tempat untuk **angka yang bisa berubah** (pajak, threshold, suku bunga, batas).
Dok lain merujuk ke sini, jadi pembaruan cukup di satu file. Refresh lewat `update/`.

> **Terakhir diverifikasi: 2026-06-13** (sumber resmi: DJP, LPS, BI, BPS, Antam).
> Tetap konfirmasi ulang sebelum keputusan/angka kritis. Tanda ⚠️ = sering berubah,
> pasti cek lagi (apalagi yang ber-snapshot tanggal).

## Pajak penghasilan orang pribadi (PPh OP)

- **PTKP (lajang, TK/0):** Rp54.000.000/tahun (masih mengacu PMK 101/2016, belum berubah
  s/d 2026). Tambahan: +Rp4,5jt (WP kawin) dan +Rp4,5jt per tanggungan (maks 3); istri
  yang penghasilannya digabung +Rp54jt.
- **Tarif progresif (UU HPP No. 7/2021) — tetap berlaku 2026:**
  - 5% — 0 s/d Rp60jt
  - 15% — >Rp60jt s/d Rp250jt
  - 25% — >Rp250jt s/d Rp500jt
  - 30% — >Rp500jt s/d Rp5miliar
  - 35% — >Rp5miliar
- **PPh 21 karyawan:** pemotongan bulanan pakai **tarif efektif rata-rata (TER)**
  Jan–Nov, lalu progresif Pasal 17 di Desember/masa terakhir.
- **SPT Tahunan OP:** lapor sebelum **31 Maret**.

## Pajak instrumen investasi (umumnya final)

- **Penjualan saham (IDX):** 0,1% final dari nilai jual.
- **Dividen dalam negeri:** bebas PPh bila diinvestasikan kembali di Indonesia sesuai
  syarat (UU HPP/Cipta Kerja); jika tidak, masuk objek pajak.
- **Kupon SBN ritel (ORI/SBR/SR/ST):** 10% final.
- **Bunga deposito/tabungan:** 20% final.
- **Capital gain reksadana (investor ritel):** bukan objek pajak.
- **Penjualan properti (penjual):** PPh final 2,5% dari nilai pengalihan.
- **BPHTB (pembeli properti):** 5% × (NPOP − NPOPTKP). NPOPTKP beda per daerah. ⚠️

## Pajak usaha / UMKM — DIPERBARUI (PP 20/2026)

**PP 20 Tahun 2026** (berlaku **22 April 2026**) merevisi PP 55/2022:

- **Tarif PPh final UMKM 0,5%** dari omzet bruto kini **permanen / tanpa batas waktu**
  untuk **orang pribadi** & **perseroan perorangan** (batas 7 th OP / 4 th perseroan
  perorangan **dihapus**).
- **Peserta dipersempit** — hanya boleh: orang pribadi, perseroan perorangan, dan
  **koperasi (maks 4 tahun)**. **CV, Firma, PT biasa, BUMN, BUMDes tidak lagi berhak**
  (yang sudah memakai boleh lanjut sampai jangka waktunya habis).
- **Omzet ≤ Rp500jt/tahun (OP):** bagian sampai Rp500jt **tidak kena** PPh final 0,5%.
- **Batas omzet UMKM:** tetap **Rp4,8miliar/tahun**; di atasnya pakai tarif normal/pembukuan.
- **Wajib PKP (pungut PPN):** peredaran bruto > Rp4,8miliar/tahun.

## PPN

- **Tarif umum: 11%** untuk mayoritas barang/jasa (tetap, tidak naik di 2026).
- **12%** hanya untuk **barang mewah** (objek PPnBM): mis. mobil/motor mewah, hunian
  mewah, kapal pesiar, pesawat. ⚠️
- **Bebas PPN (0%):** kebutuhan pokok (beras, daging, ikan, telur, sayur, susu segar),
  jasa pendidikan, kesehatan, angkutan umum, rumah sederhana, air minum.

## Jaminan & suku bunga

- **LPS — penjaminan simpanan:** hingga **Rp2miliar** per nasabah per bank (syarat bunga
  ≤ tingkat penjaminan LPS).
- **Tingkat Bunga Penjaminan (TBP) LPS — snapshot 1 Jun–30 Sep 2026:** ⚠️
  rupiah bank umum **3,50%**, BPR **6,00%**, valas bank umum **2,00%**.
- **BI-Rate — snapshot 9 Jun 2026: 5,50%** (naik 25 bps; deposit facility 4,50%,
  lending facility 6,25%). ⚠️ **berubah tiap RDG — cek bi.go.id saat dipakai.**

## Zakat

- **Nisab zakat maal:** 85 gram emas × harga emas/gram. Tarif 2,5%, haul 1 tahun.
- **Snapshot harga emas Antam 13 Jun 2026: ~Rp2.711.000/gram** → nisab 85 gram
  **≈ Rp230,4jt**. ⚠️ harga emas bergerak harian — cek saat menghitung.
- **Zakat penghasilan:** 2,5% di atas nisab (bisa dibayar bulanan).
- Bisa jadi pengurang penghasilan bruto bila lewat BAZNAS/LAZ resmi.

## Asumsi perencanaan (konvensi skill ini, bukan aturan)

Default di `scripts/calc.py` & dok perencanaan. Sesuaikan per kasus.

- **Inflasi umum:** ~3%/tahun (BPS Mei 2026: **3,08% yoy**; target BI 2,5%±1%).
- **Inflasi pendidikan:** ~10%/tahun (lebih tinggi dari umum).
- **Safe withdrawal rate (FIRE) di ID:** 3–3,5% (lebih konservatif dari 4% ala AS).
- **Return realistis jangka panjang:** RDPU/deposito ~4–6%, obligasi/SBN ~6–7%,
  saham/RD saham ~8–12% (volatil, tidak dijamin). Pakai yang konservatif saat menghitung.
