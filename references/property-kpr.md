# Property & KPR

Beli rumah biasanya transaksi terbesar seumur hidup. Cara berpikir soal properti &
mekanik **KPR** (Kredit Pemilikan Rumah). Hitung angka konkret dengan
`scripts/calc.py loan`.

## Beli vs sewa — jangan otomatis "beli selalu menang"

- **Beli** masuk akal kalau: tinggal lama (>5-7 th), cicilan nyaman, sudah punya
  dana darurat + DP tanpa menguras semua, butuh stabilitas.
- **Sewa** masuk akal kalau: mobilitas tinggi, harga properti di area itu kemahalan
  vs sewa, atau selisih (DP+cicilan − sewa) bisa diinvestasikan dengan return lebih baik.
- Properti **tidak likuid** dan ada biaya tersembunyi (pajak, perawatan, renovasi).
  "Beli rumah" bukan keputusan murni finansial — ada nilai psikologis/keluarga juga.

## Mekanik KPR

- **DP (uang muka):** umumnya **10-30%** harga. DP lebih besar → cicilan & bunga total
  lebih kecil, peluang approval lebih tinggi.
- **Tenor:** 5-20 th (kadang 25-30). Tenor panjang → cicilan/bln ringan tapi **total
  bunga jauh lebih besar**. Bandingkan pakai kalkulator.
- **Jenis bunga:**
  - **Fixed** — tetap untuk periode awal (mis. 1-5 th). Pasti, enak buat anggaran.
  - **Floating** — mengambang ikut suku bunga acuan. Setelah masa fixed habis, cicilan
    bisa naik tajam ("**bom waktu KPR**"). Selalu cek floating rate, bukan cuma teaser fixed.
- **Anuitas:** cicilan/bln tetap, tapi komposisi berubah — awal **mayoritas bunga**,
  pokok terkikis pelan. Itu kenapa pelunasan awal terasa lambat (lihat output `calc.py loan`).

## Rasio & kesiapan (sebelum akad)

- **Cicilan ≤ 30-35%** penghasilan bulanan (semua utang digabung). Di atas itu, rawan.
- **Siapkan, di luar harga rumah:**
  - DP (10-30%).
  - **Biaya transaksi ~5-10% harga**: BPHTB, biaya KPR (provisi, admin, appraisal),
    notaris/AJB, balik nama, asuransi (jiwa + kebakaran).
  - Dana darurat **tetap utuh** — jangan kuras semua tabungan untuk DP.
  - Buffer renovasi/perabot.
- **Jaga DTI sehat** & skor kredit (SLIK OJK bersih) sebelum apply.

## Pajak & biaya properti (Indonesia)

- **BPHTB** (Bea Perolehan Hak atas Tanah dan Bangunan) — **5%** dari (NPOP − NPOPTKP),
  dibayar **pembeli**. NPOPTKP bervariasi per daerah.
- **PPh final penjual** — **2,5%** dari nilai pengalihan, dibayar **penjual**.
- **PBB** (Pajak Bumi & Bangunan) — tahunan, berbasis NJOP.
- **PPN** untuk rumah baru dari developer (cek tarif & insentif yang berlaku —
  pemerintah kadang beri insentif PPN DTP; verifikasi di `references/rates.md`).
- **Status hak:** SHM (milik penuh) > HGB (ada jangka, bisa diperpanjang). Cek sertifikat
  asli, tidak sengketa, dan IMB/PBG sebelum bayar.

## Strategi & jebakan

- **Lunasi lebih cepat (prepayment):** bayar ekstra ke pokok memangkas bunga total
  signifikan, terutama di tahun-tahun awal. Cek penalti pelunasan dipercepat di kontrak.
- **Refinancing / take-over KPR:** pindah ke bank dengan bunga lebih rendah saat
  floating-mu mahal. Hitung biaya pindah vs penghematan bunga.
- **Jangan over-budget** karena emosi/FOMO "harga naik terus". Rumah yang bikin cashflow
  tercekik = "rumah miskin" (house poor).
- **Properti sebagai investasi** beda dari rumah tinggal: pikirkan yield sewa (sewa/th ÷
  harga, sering cuma 3-5% di ID), likuiditas, biaya kosong, dan pajak. REIT/DIRE bisa jadi
  alternatif properti tanpa repot fisik (lihat `investing-basics.md`).
- **KPR syariah** (murabahah/MMQ): margin tetap, akad jual-beli/kongsi, bukan bunga —
  bandingkan total biaya, jangan asumsi otomatis lebih murah/mahal.

→ Untuk angka spesifik (cicilan, total bunga, rasio penghasilan), jalankan
`python3 scripts/calc.py loan --principal <pokok> --years <tenor> --rate <bunga> --income <gaji/bln>`.
