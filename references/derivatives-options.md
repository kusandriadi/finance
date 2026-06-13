# Derivatives & Options

**Lanjutan / berisiko tinggi.** Derivatif = kontrak yang nilainya *diturunkan* dari aset
lain (saham, indeks, komoditas, mata uang). Alat untuk **hedging** atau **spekulasi
berleverage** — pisau bermata dua. Untuk mayoritas investor ritel: **tidak wajib, dan
mudah bikin rugi besar.** Pahami dulu sebelum sentuh.

> Aturan emas tetap berlaku (`risk-management.md`): leverage memperbesar untung DAN rugi.
> Banyak yang blow up di derivatif justru karena merasa "sudah paham".

## Jenis utama

- **Futures (kontrak berjangka):** janji beli/jual aset di harga & tanggal tertentu.
  Wajib settle. Bermargin → leverage tinggi. Di ID: futures indeks (mis. LQ45 Futures di
  IDX), komoditas via **bursa berjangka (JFX/ICDX, diawasi Bappebti)**.
- **Options (opsi):** *hak* (bukan kewajiban) beli/jual aset di **strike price** sampai
  **expiry**. Beli opsi = bayar **premi**; rugi maksimal = premi (buyer). Penjual opsi
  (writer) menerima premi tapi risiko bisa besar/tak terbatas.
  - **Call** = hak **beli** (bullish). **Put** = hak **jual** (bearish/proteksi).
  - Di ID ada **KOS (Kontrak Opsi Saham)** di IDX tapi likuiditas tipis; lebih ramai di pasar AS.
- **Warrant (waran):** mirip call jangka panjang yang diterbitkan emiten; umum di IDX,
  sering "nempel" saat right issue. Bisa kedaluwarsa tak bernilai.
- **Swap:** tukar arus kas (mis. bunga tetap ↔ mengambang). Ranah institusi.
- **CFD:** kontrak selisih harga, sangat berleverage — banyak ditawarkan broker luar,
  **hati-hati legalitas & broker bodong**.

## Mekanika opsi yang wajib dipahami

- **Payoff asimetris:** buyer rugi terbatas (premi), untung bisa besar. Writer kebalikannya.
- **Premi = nilai intrinsik + nilai waktu.** Makin dekat expiry, nilai waktu meluruh
  (**theta decay**) — opsi adalah aset yang "meleleh".
- **Greeks** (sensitivitas): **delta** (vs harga aset), **theta** (waktu), **vega**
  (volatilitas), **gamma** (perubahan delta). Volatilitas implied (**IV**) sering lebih
  menentukan harga opsi daripada arah.
- **Moneyness:** ITM (in-the-money), ATM, OTM. Beli OTM murah tapi sering berakhir nol.

## Kegunaan sah (bukan cuma judi)

- **Hedging:** beli **put** sebagai "asuransi" portofolio saham terhadap penurunan.
- **Income:** **covered call** (jual call atas saham yang dimiliki) untuk tambahan premi —
  imbalannya membatasi upside.
- **Leverage terukur:** ekspos lebih besar dengan modal kecil — tapi inilah jebakan ritel.

## Jebakan & risiko

- **Leverage → margin call → kerugian melebihi modal** (terutama futures/CFD).
- **Theta decay:** beli opsi lalu "benar arah tapi telat" → tetap rugi karena waktu habis.
- **Likuiditas tipis** (KOS/waran ID): spread lebar, susah keluar di harga wajar.
- **Kompleksitas:** salah paham payoff/Greeks = salah ukur risiko.
- **Broker/skema ilegal:** "binary option", robot trading berkedok opsi — banyak yang
  **bukan derivatif sungguhan, melainkan judi/penipuan** (lihat `forex-trading.md`).

## Pajak & legal (Indonesia, garis besar)

- Transaksi berjangka komoditas via bursa resmi (Bappebti) ada ketentuan PPh tersendiri.
- Opsi/warrant saham mengikuti rezim pajak saham/penghasilan — **verifikasi ke DJP**
  karena perlakuannya bisa berbeda per instrumen (`rates.md`).
- Pastikan bursa & broker **berizin (IDX/Bappebti/OJK)** sebelum transaksi.

## Sikap yang waras

- Untuk kebanyakan orang: **cukup proteksi lewat diversifikasi & alokasi**, bukan opsi.
- Kalau mau masuk: mulai dari **buyer opsi (rugi terbatas)**, ukuran sangat kecil, sebagai
  belajar — bukan sumber penghasilan utama. **Jangan jadi writer telanjang (naked).**
- Kalau tak bisa jelaskan payoff & risiko maksimalmu dalam satu kalimat → belum siap.
