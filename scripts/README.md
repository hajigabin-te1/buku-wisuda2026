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

**Yang diperiksa:** kolom wajib, field kosong, NIM duplikat, nama ganda, No bukan angka, IPK di luar 0–4 / tidak dua desimal / campuran koma-titik, judul > 250 karakter, nama > 45 karakter, foto hilang, nama file foto tanpa NIM, resolusi foto (< 260×346 px = ERROR, < 600×800 px = WARNING), rasio bukan 3:4, data berlabel DUMMY. File masukan tidak pernah diubah; spasi ganda/tab/enter hanya dirapikan di keluaran.

**Status uji:** diuji di Linux dengan `03-Data/CSV-DataMerge/DUMMY-contoh-wisudawan.csv` (CSV & XLSX, foto dummy hilang/kecil/tidak 3:4). Belum diuji dengan data asli di Windows. Impor `*-datamerge.txt` ke InDesign 2020 belum diuji — periksa karakter (é, “ ”, —) di Preview Data Merge.

## 2. `indesign/setup-dokumen.jsx` — dokumen sistem A5
**Prasyarat:** Adobe InDesign 2020 (Windows). Font Montserrat, Source Sans 3, Playfair Display, Cinzel, Satisfy terpasang (bila tidak, skrip memakai Arial dan memberi tahu). Struktur folder repo utuh, karena skrip mengambil SVG dari `05-InDesign/Links/` (jalankan dulu `scripts/aset/buat_aset_svg.py` bila folder itu kosong).

**Jalankan:**
1. InDesign → Window → Utilities → Scripts.
2. Panel Scripts → klik kanan **User** → *Reveal in Explorer* → salin `setup-dokumen.jsx` ke folder itu. Saat dijalankan dari sana, skrip akan meminta Anda memilih folder `05-InDesign\Links` proyek (untuk ikon & ornamen SVG).
3. Klik dua kali skrip di panel. Dokumen baru dibuat; dokumen lain tidak disentuh.
4. Baca pesan akhir (font pengganti / langkah yang dilewati), lalu *Save As* `05-InDesign/INDD/00-TEMPLATE-Sistem.indd`.

**Hasil:** A5 facing pages + bleed 3 mm, margin atas 12 / bawah 15 / dalam 18 / luar 12 (spesifikasi percetakan); swatch UC-*; paragraph styles Bagian-Judul, Bagian-Sub, Sampul-Judul, Script-Tema, H1-Bab, H2-Subjudul, Isi, Puitis, Lirik, Dir-*, Folio; object styles Kaca-Kartu, Chip-Emas, Foto-Bingkai, Teks-Kartu; master A-Isi, B-Direktori (judul bagian gaya referensi), C-Tanpa-Nomor dengan ornamen sudut SVG; halaman 1 (halaman kanan) berisi satu kartu contoh 56.5 × 81 mm gaya referensi (ikon SVG inline di label) dengan teks penanda `«Nama»` dsb., plus catatan non-cetak di pasteboard (hapus sebelum merge).

**Batasan:** BELUM DIUJI di InDesign (hanya cek sintaks JavaScript). Penempatan SVG (ornamen & ikon) memerlukan dukungan impor SVG di InDesign 2020; bila gagal, dicatat di pesan akhir — ikon/ornamen lalu dipasang manual, atau SVG dikonversi ke PDF/AI terlebih dulu. Pengaturan efek (opasitas, drop shadow, gradient feather, sudut membulat) dibungkus `try` — bila gagal, dicatat di pesan akhir dan perlu diatur manual di Object Styles. Ubah angka bleed/margin di blok `CFG` setelah spesifikasi vendor diterima.

## 3. `indesign/rapikan-direktori.jsx` — rapikan kartu setelah merge
Margin dalam (18 mm) ≠ luar (12 mm), sedangkan Data Merge belum tentu mencerminkan posisi kartu di halaman kiri. Skrip ini menggeser semua objek halaman (bukan master) di setiap halaman agar tepi kiri kartu menempel ke margin yang benar: halaman kanan → 18 mm, halaman kiri → 12 mm. Objek di pasteboard diabaikan.

**Jalankan:** buka dokumen **hasil** merge (mis. `11-Direktori-Bisnis.indd`) → klik dua kali skrip di panel Scripts → periksa beberapa halaman kiri & kanan. Satu kali Ctrl+Z membatalkan seluruh pergeseran. Aman dijalankan ulang.

**Penting:** halaman kiri/kanan ditentukan nomor halaman. Jalankan skrip setelah urutan halaman di Book final (atau jalankan ulang bila halaman sebelumnya bertambah/berkurang ganjil).

**Batasan:** BELUM DIUJI di InDesign (hanya cek sintaks).

## 4. `aset/buat_aset_svg.py` — ornamen & ikon (aset desain, bukan aset resmi)
Membuat `05-InDesign/Links/ornamen/` (ornamen-sudut, ornamen-tepi, sapuan-emas, toga) dan `05-InDesign/Links/ikon/` (nim, nama, ttl, ipk, predikat, judul) mengikuti gaya `01-Brief-Referensi/referensi.png` dan palet resmi. **Jalankan:** `python scripts/aset/buat_aset_svg.py`. **Status:** SVG tervalidasi dirender Chromium di mockup; belum diuji place di InDesign.

## 5. `mockup/buat_mockup.py` — mockup konsep
**Prasyarat:** Python 3 + Pillow, Node.js + `playwright` (Chromium), internet untuk Google Fonts.
**Jalankan:** `python scripts/mockup/buat_mockup.py` → 14 PNG (konsep v3, gaya referensi), `00-ringkasan.png`, dan `KONSEP-Buku-Wisuda-2026.pdf` di `06-Proof/konsep/`. Memakai logo resmi `02-Aset-Resmi/Logo/STIA.png` dan aset dari skrip no. 4. Margin mengikuti spesifikasi percetakan; sisi jilid ditandai merah.
**Batasan:** hanya acuan visual dari data DUMMY dan placeholder; bukan file cetak dan bukan file InDesign.
