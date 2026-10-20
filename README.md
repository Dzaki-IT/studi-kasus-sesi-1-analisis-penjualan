# Studi Kasus Sesi 1: Analisis Penjualan Toko Fiktif

## 1. Latar Belakang
Pemilik toko kecil mempunyai catatan transaksi, tetapi belum memiliki ringkasan yang mudah digunakan untuk melihat omzet, keuntungan, tren bulanan, dan perbedaan performa produk. Studi kasus ini membuat alur analisis yang dapat diulang menggunakan Python.

**Keterkaitan dengan seminar:** proyek menerapkan analisis deskriptif untuk menjawab apa yang terjadi, serta eksplorasi diagnostik untuk merumuskan pertanyaan tentang kemungkinan faktor yang berkaitan dengan hasil penjualan. Proyek juga menekankan validasi data karena data yang buruk dapat menghasilkan kesimpulan yang keliru.

## 2. Tujuan
- Memvalidasi data transaksi sebelum analisis.
- Menghitung omzet setelah diskon, biaya, dan keuntungan perkiraan.
- Membandingkan omzet bulanan dan keuntungan tiap produk.
- Menghasilkan tabel dan grafik yang bisa diperiksa kembali.
- Menuliskan batasan analisis agar temuan tidak dianggap sebagai bukti sebab-akibat.

## 3. Data
File `data/penjualan.csv` berisi **data sintetis** yang dibuat khusus untuk latihan, bukan data bisnis sungguhan. Setiap baris adalah satu catatan transaksi produk.

| Kolom | Arti |
|---|---|
| `tanggal` | Tanggal transaksi |
| `produk` | Nama produk |
| `kategori` | Kategori produk |
| `jumlah_terjual` | Unit terjual dalam transaksi |
| `harga_satuan` | Harga per unit sebelum diskon, rupiah |
| `biaya_satuan` | Perkiraan biaya per unit, rupiah |
| `diskon` | Diskon dalam bentuk proporsi: 0.10 berarti 10% |
| `kanal` | Kanal transaksi: Toko atau Online |

Rumus yang digunakan:
- `omzet = jumlah_terjual × harga_satuan × (1 − diskon)`
- `total_biaya = jumlah_terjual × biaya_satuan`
- `keuntungan = omzet − total_biaya`
- `margin keuntungan = total keuntungan ÷ total omzet × 100%`

Perhitungan keuntungan adalah estimasi sederhana karena belum mencakup biaya operasional, pengiriman, retur, pajak, dan biaya lain.

## 4. Struktur Proyek
```text
studi-kasus-sesi-1-analisis-penjualan/
├── data/
│   └── penjualan.csv
├── src/
│   └── analisis_penjualan.py
├── tests/
│   └── test_analisis_penjualan.py
├── outputs/
│   └── charts/             # grafik dibuat ketika program dijalankan
├── README.md
└── requirements.txt
```

## 5. Persiapan (Windows)
1. Pasang Python 3.10 atau yang lebih baru dari https://www.python.org/downloads/.
2. Saat instalasi, centang **Add Python to PATH** jika opsi itu tersedia.
3. Pasang Visual Studio Code dari https://code.visualstudio.com/.
4. Buka folder proyek ini di VS Code melalui **File → Open Folder**.
5. Buka terminal VS Code melalui **Terminal → New Terminal**.

Periksa Python:
```bash
python --version
```
Jika perintah `python` tidak dikenali, coba:
```bash
py --version
```

## 6. Instalasi dan Menjalankan
Di terminal, pastikan direktori aktif adalah folder proyek yang berisi `README.md`.

Buat virtual environment:
```bash
python -m venv .venv
```

Aktifkan di Windows Command Prompt:
```bat
.venv\Scripts\activate
```
Jika menggunakan PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Jika PowerShell memblokir aktivasi, kamu bisa memakai Command Prompt atau menjalankan pip melalui `.venv\Scripts\python.exe`.

Pasang library:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Jalankan analisis:
```bash
python src/analisis_penjualan.py
```

Hasil yang dibuat:
- `outputs/ringkasan_umum.csv`
- `outputs/ringkasan_bulanan.csv`
- `outputs/ringkasan_produk.csv`
- `outputs/temuan.md`
- `outputs/charts/omzet_bulanan.png`
- `outputs/charts/keuntungan_produk.png`
- `outputs/charts/diskon_vs_keuntungan.png`

Folder dan file hasil dibuat otomatis saat skrip dijalankan.

## 7. Menjalankan Pengujian
Jalankan:
```bash
python -m unittest discover -s tests -v
```
Pengujian memeriksa data valid, rumus omzet setelah diskon, penolakan diskon yang tidak valid, dan pembuatan file hasil.

## 8. Cara Membaca Hasil
- Grafik omzet bulanan memperlihatkan perubahan nilai omzet dari bulan ke bulan.
- Grafik keuntungan per produk membandingkan kontribusi keuntungan total dari tiap produk.
- Grafik diskon dan keuntungan membantu eksplorasi, tetapi tidak membuktikan bahwa diskon adalah penyebab perubahan keuntungan.
- Buka `outputs/temuan.md` untuk ringkasan otomatis yang dihasilkan dari dataset.

## 9. Kesimpulan
Proyek ini menunjukkan alur sederhana yang dapat diulang: membaca data, memvalidasi kualitas data, menghitung metrik, merangkum hasil, membuat visualisasi, dan menyusun pertanyaan lanjutan. Sebelum digunakan untuk keputusan nyata, data dan asumsi perhitungan harus divalidasi.

## 10. Batasan dan Etika
- Data merupakan data sintetis, bukan data pelanggan atau toko nyata.
- Jangan mengunggah data pelanggan atau data bisnis rahasia ke repository publik.
- Ringkasan korelasi atau pola tidak otomatis menunjukkan hubungan sebab-akibat.
- Keputusan bisnis harus mempertimbangkan konteks dan bukti tambahan.

## 11. Lisensi
Materi kode dan dataset contoh ini disediakan untuk tujuan pembelajaran.
