# Indonesia Context

Instrumen, aturan, dan kewajiban khas Indonesia. Pakai ini agar saran lokal-akurat.

> Aturan/tarif/threshold bisa berubah. Untuk angka pajak/zakat/program yang kritis,
> verifikasi ke sumber resmi (DJP, OJK, BPS, BI) sebelum dipastikan.

## Instrumen investasi lokal

### Reksadana (paling pemula-friendly)

Dana kolektif dikelola Manajer Investasi (MI). Jenis:
- **RDPU (Pasar Uang)** — paling aman, likuid, untuk dana darurat/jangka pendek.
- **RDPT (Pendapatan Tetap)** — mayoritas obligasi; risiko-return menengah.
- **Campuran** — mix saham+obligasi.
- **RD Saham** — mayoritas saham; jangka panjang, paling volatil.
- **RD Index/ETF** — pasif, ikut indeks (mis. IDX30, LQ45), biaya rendah.

Beli lewat APERD/platform (Bibit, Bareksa, Ajaib, dll) atau bank. Perhatikan
**expense ratio**. Capital gain reksadana **bukan objek pajak** bagi investor ritel
(keuntungan sudah di level reksadana) — keunggulan vs saham langsung.

### SBN Ritel (Surat Berharga Negara)

Utang negara, relatif aman (dijamin negara), kupon rutin:
- **ORI** — kupon tetap, bisa diperjualbelikan di pasar sekunder.
- **SBR** — kupon mengambang (floating, ada batas bawah), tidak bisa dijual di sekunder
  (ada early redemption terbatas).
- **SR (Sukuk Ritel) / ST** — versi syariah (akad, bukan "bunga").
- **FR** — seri non-ritel di pasar sekunder.

Pajak kupon SBN ritel **10% final** (lebih rendah dari deposito 20%). Minimal beli
biasanya Rp1jt. Dijual periodik via mitra distribusi.

### Saham IDX (.JK)

Bursa Efek Indonesia. Lot = 100 lembar. Indeks acuan: IHSG (komposit), LQ45, IDX30.
- **Pajak penjualan saham:** 0,1% final dari nilai jual (dipungat otomatis broker).
- **Dividen:** kena PPh; sejak UU Cipta Kerja, dividen dalam negeri **bebas pajak**
  bila diinvestasikan kembali di Indonesia sesuai syarat (kalau tidak, kena tarif).
- Biaya broker beli/jual (mis. ~0,15% beli / ~0,25% jual, beda per broker).
- Skill `ihsg-swing-trading` mensimulasikan ini (fee + materai) untuk paper trading.

### Emas

- Fisik **Antam/UBS** (ada sertifikat) atau emas digital (Pegadaian, platform).
- Lindung nilai inflasi/krisis, tidak hasilkan arus kas, ada spread beli-jual.
- Emas batangan (bukan perhiasan) lebih efisien untuk investasi.

### Deposito

Dijamin **LPS** hingga Rp2 miliar/nasabah/bank (syarat suku bunga ≤ tingkat penjaminan
LPS). Bunga deposito kena **pajak final 20%**. Aman, return modest.

## Pajak pribadi (PPh OP)

> Angka pajak (PTKP, tarif, threshold) dipusatkan di **`rates.md`** — selalu rujuk
> ke sana, dan verifikasi ke DJP untuk keputusan kritis. Di bawah ini konsepnya.

- **NPWP** untuk wajib pajak (kini terintegrasi NIK); lapor **SPT Tahunan** sebelum 31 Maret.
- **PTKP** (penghasilan tidak kena pajak) untuk lajang — di bawahnya tidak kena PPh.
  Tambah untuk status kawin/tanggungan. Angka di `rates.md`.
- **Tarif progresif** berlapis (5% → 35%) sesuai lapisan penghasilan kena pajak (`rates.md`).
- Banyak instrumen investasi pakai **pajak final** (saham, kupon SBN, bunga deposito) —
  terpisah dari progresif. Tarif di `rates.md`.

## Pajak usaha / UMKM

Buat yang punya usaha/side income — beda jalur dari karyawan:

- **PPh final UMKM (kini PP 20/2026):** tarif **0,5%** dari omzet bruto bulanan — simpel,
  cocok usaha kecil. Sejak 22 April 2026 jadi **permanen untuk orang pribadi** (batas waktu
  dihapus); peserta dipersempit (CV/Firma/PT biasa tidak lagi berhak). Detail di `rates.md`.
- **Omzet kecil bebas:** bagian omzet OP sampai batas tertentu (`rates.md`) tidak kena
  PPh final.
- **PKP & PPN:** kalau peredaran bruto lewat batas (`rates.md`), wajib jadi **PKP** dan
  pungut **PPN**. Di bawah itu, tidak wajib.
- **Pisahkan keuangan usaha & pribadi** — rekening, catatan, dan "gaji" sendiri yang jelas.
  Cashflow usaha ≠ kekayaan pribadi (lihat `budgeting-cashflow.md`).
- **NPPN / pembukuan:** usaha kecil bisa pakai Norma Penghitungan; usaha lebih besar wajib
  pembukuan. Konsultasikan ke konsultan pajak saat skala naik.

## Zakat (bila relevan bagi Muslim)

- **Zakat maal:** 2,5% dari harta (termasuk tabungan, emas, investasi) yang mencapai
  **nisab** (≈ 85 gram emas) dan sudah dimiliki **1 tahun (haul)**.
- **Zakat penghasilan/profesi:** 2,5% dari penghasilan (di atas nisab), bisa bulanan.
- Bisa jadi pengurang penghasilan bruto bila lewat lembaga resmi (BAZNAS/LAZ).

## Jaminan sosial

- **BPJS Kesehatan** — wajib, premi per kelas. Proteksi kesehatan dasar (utamakan
  sebelum asuransi swasta).
- **BPJS Ketenagakerjaan** — JHT (hari tua), JP (pensiun), JKK (kecelakaan), JKM
  (kematian). JHT bisa jadi salah satu pos dana pensiun.

## Catatan kultural-finansial

- **THR** (tunjangan hari raya) → manfaatkan sebagian untuk dana darurat/investasi,
  jangan habis ke konsumtif lebaran. Sinking fund untuk pengeluaran lebaran.
- **Arisan** — menabung sosial, tapi tidak memberi return riil & ada risiko
  bandar/ketua kabur. Bukan pengganti investasi.
- Waspada **investasi bodong** berkedok syariah/komunitas/robot trading — cek izin
  OJK/Bappebti dulu. "Fixed return tinggi" = bendera merah.
