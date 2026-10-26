# Scripts

Simpan skrip otomasi InDesign atau pemeriksaan data di sini. Sertakan cara penggunaan, prasyarat, dan catatan pengujian. Jangan simpan password, token, atau data pribadi di dalam kode.

## 1. `validasi_data.py` — validasi data & sumber Data Merge
**Prasyarat:** Python 3.8+ (Windows: python.org). Opsional: `pip install openpyxl pillow` (untuk membaca `.xlsx` dan mengecek resolusi foto).

**Jalankan** dari folder proyek (Command Prompt / PowerShell):
```
python scripts\validasi_data.py 03-Data\Data-Bersih\bisnis.xlsx ^
  --foto-dir 04-Foto-Wisudawan\bisnis ^
  --foto-base "D:\BukuWisuda2026\04-Foto-Wisudawan\bisnis" ^
  --out 03-Data\CSV-DataMerge\bisnis
```
- `--foto-dir`: folder foto di komputer ini (untuk cek ada/tidak & resolusi).
- `--foto-base`: path folder foto **persis seperti yang akan dibuka InDesign** (path absolut Windows). Bila dikosongkan, dipakai path absolut dari `--foto-dir`.
- `--nomor-otomatis`: isi kolom `No` yang kosong berdasarkan urutan baris.
- `--paksa`: tetap menulis keluaran walau ada ERROR (hanya untuk uji layout).

**Keluaran:**
- `bisnis-datamerge.txt` — UTF-16, dipisah Tab, header `No NIM Nama TTL IPK Predikat Judul @Foto`. **File ini yang dipilih di panel Data Merge.**
- `bisnis-cek.csv` — salinan yang sama untuk dibuka di Excel.
- `bisnis-laporan.txt` — daftar ERROR/WARNING, nilai predikat, dan 5 judul terpanjang.

**Yang diperiksa:** kolom wajib, field kosong, NIM duplikat, nama ganda, No bukan angka, IPK di luar 0–4 / tidak dua desimal / campuran koma-titik, judul > 330 karakter, nama > 45 karakter, foto hilang, nama file foto tanpa NIM, resolusi foto (< 260×346 px = ERROR, < 600×800 px = WARNING), rasio bukan 3:4, data berlabel DUMMY. File masukan tidak pernah diubah; spasi ganda/tab/enter hanya dirapikan di keluaran.

**Status uji:** diuji di Linux dengan `03-Data/CSV-DataMerge/DUMMY-contoh-wisudawan.csv` (CSV & XLSX, foto dummy hilang/kecil/tidak 3:4). Belum diuji dengan data asli di Windows. Impor `*-datamerge.txt` ke InDesign 2020 belum diuji — periksa karakter (é, “ ”, —) di Preview Data Merge.

## 2. `indesign/setup-dokumen.jsx` — dokumen sistem A5
**Prasyarat:** Adobe InDesign 2020 (Windows). Font Montserrat, Source Sans 3, Playfair Display terpasang (bila tidak, skrip memakai Arial dan memberi tahu).

**Jalankan:**
1. InDesign → Window → Utilities → Scripts.
2. Panel Scripts → klik kanan **User** → *Reveal in Explorer* → salin `setup-dokumen.jsx` ke folder itu.
3. Klik dua kali skrip di panel. Dokumen baru dibuat; dokumen lain tidak disentuh.
4. Baca pesan akhir (font pengganti / langkah yang dilewati), lalu *Save As* `05-InDesign/INDD/00-TEMPLATE-Sistem.indd`.

**Hasil:** A5 facing pages + bleed 3 mm; swatch UC-*; paragraph styles H1-Bab, H2-Subjudul, Isi, Puitis, Lirik, Dir-*, Folio; character style Dir-Label-Inline; object styles Kaca-Kartu, Kaca-Header, Chip-Emas, Chip-IPK, Foto-Bingkai, Ornamen-Lingkaran, Teks-Kartu; master A-Isi, B-Direktori, C-Tanpa-Nomor; halaman 1 berisi satu kartu contoh Varian A dengan teks penanda `«Nama»` dsb.

**Batasan:** BELUM DIUJI di InDesign (hanya cek sintaks JavaScript). Pengaturan efek (opasitas, drop shadow, gradient feather, sudut membulat) dibungkus `try` — bila gagal, dicatat di pesan akhir dan perlu diatur manual di Object Styles. Ubah angka bleed/margin di blok `CFG` setelah spesifikasi vendor diterima.

## 3. `mockup/buat_mockup.py` — mockup konsep
**Prasyarat:** Python 3 + Pillow, Node.js + `playwright` (Chromium), internet untuk Google Fonts.
**Jalankan:** `python scripts/mockup/buat_mockup.py` → PNG + `KONSEP-Buku-Wisuda-2026.pdf` di `06-Proof/konsep/`.
**Batasan:** hanya acuan visual dari data DUMMY dan placeholder; bukan file cetak dan bukan file InDesign.
