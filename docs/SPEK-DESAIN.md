# Spesifikasi Desain — Buku Wisuda STIA Amuntai 2026

Status: **v0.2** — spesifikasi percetakan sudah dikonfirmasi pemilik proyek (Okt 2026). Kartu direktori: **Varian A** (final). Profil warna & standar PDF/X masih perlu ditanyakan ke percetakan.

## 1. Format (dikonfirmasi percetakan)
| Item | Nilai | Status |
|---|---|---|
| Ukuran jadi | A5 portrait, 148 × 210 mm | Final |
| Ukuran dengan bleed | 154 × 216 mm | Final |
| Bleed | 3 mm (atas, bawah, dalam, luar) | Final |
| Margin atas | 12 mm | Final |
| Margin bawah | 15 mm (ruang nomor halaman) | Final |
| Margin dalam (sisi jilid) | **18 mm** | Final |
| Margin luar | 12 mm | Final |
| Area aman (live area) | 118 × 183 mm | Turunan |
| Jilid | **Lem panas (perfect binding)** | Final |
| Format serah | PDF | Final — standar PDF/X & profil warna: **tanyakan ke percetakan** |
| Facing pages | Ya; margin dalam/luar bergantian di halaman kiri/kanan | Final |

Konsekuensi perfect binding:
- **Sampul (depan + punggung + belakang) biasanya dicetak terpisah** sebagai satu bentangan. Lebar punggung (*spine*) bergantung pada jumlah halaman & jenis kertas isi — **minta angkanya ke percetakan** setelah jumlah halaman final. Sampai saat itu cover didesain per halaman A5.
- Jangan menaruh teks/wajah penting melintasi lipatan tengah spread; area 18 mm di sisi jilid sebagian “tertelan” lem.
- Isi diekspor sebagai **halaman tunggal** (bukan spread) dengan bleed 3 mm, kecuali percetakan meminta lain.
- Jumlah halaman isi umumnya genap; tanyakan apakah percetakan butuh kelipatan tertentu (mis. 4/8/16).

## 2. Palet warna (60-30-10)
| Swatch InDesign | Hex | RGB | Peran |
|---|---|---|---|
| `UC-Primer-60` | `#EBF8FF` | 235 248 255 | Latar halaman, bidang luas (60%) |
| `UC-Sekunder-30` | `#3081DB` | 48 129 219 | Header, bidang kaca berwarna, garis, ikon (30%) |
| `UC-Aksen-10` | `#FFE031` | 255 224 49 | Highlight kecil: nomor urut, chip predikat, garis aksen (10%) |
| `UC-Tinta` | `#12355E` | 18 53 94 | **Turunan pendukung** (bukan warna palet baru) — hanya untuk teks agar kontras tinggi |
| `Paper` / putih | `#FFFFFF` | — | Bidang kaca (transparansi 55–75%) |

Catatan warna:
- Swatch dibuat dalam **RGB** dan dikonversi ke CMYK saat ekspor PDF memakai profil dari percetakan. Jangan menebak nilai CMYK; mintalah profil (mis. *Coated FOGRA39* atau profil lokal vendor).
- `#FFE031` di atas `#EBF8FF` kontrasnya rendah → **jangan** dipakai untuk teks; gunakan sebagai bidang/garis, dengan teks `UC-Tinta` di atasnya.
- `#3081DB` dan biru terang cenderung bergeser saat dicetak CMYK. Cetak uji (proof warna) sangat disarankan.

## 3. Tipografi (usulan, semua lisensi SIL OFL — gratis dan boleh dipakai untuk cetak)
| Peran | Font | Catatan |
|---|---|---|
| Judul, nama wisudawan | **Montserrat** (SemiBold/Bold) | Geometris, modern, cocok nuansa futuristic |
| Teks isi, data, judul skripsi | **Source Sans 3** (Regular/Semibold) | Hemat lebar, sangat terbaca di ukuran kecil |
| Aksen puitis (“Untukmu Cinta”, slogan, penutup) | **Playfair Display** Italic | Elegan, editorial |

Instal ketiga font di komputer produksi (Windows) **sebelum** menjalankan skrip setup. Jika font lain dipakai, ganti nama font di skrip `scripts/indesign/setup-dokumen.jsx` dan di tabel ini. Simpan berkas lisensi OFL bersama paket akhir.

## 4. Paragraph & Character Styles
Ukuran dalam pt; leading dalam kurung.

| Style | Font | Ukuran | Warna | Pemakaian |
|---|---|---|---|---|
| `H1-Bab` | Montserrat Bold | 20 (24) | UC-Sekunder-30 | Judul bagian (Kata Pengantar, dsb.) |
| `H2-Subjudul` | Montserrat SemiBold | 12 (15) | UC-Tinta | Subjudul |
| `Isi` | Source Sans 3 Regular | 10 (14) | UC-Tinta | Teks naskah, rata kiri-kanan, hyphenation bahasa Indonesia |
| `Puitis` | Playfair Display Italic | 12 (17) | UC-Sekunder-30 | Slogan, kutipan, penutup |
| `Lirik` | Source Sans 3 Regular | 10 (15) | UC-Tinta | Mars & Hymne, rata tengah |
| `Dir-Header` | Montserrat Bold, kapital, tracking 50 | 9 (11) | Putih | Pita header direktori (nama prodi) |
| `Dir-No` | Montserrat Bold | 7 (8) | UC-Tinta | Nomor urut di chip emas |
| `Dir-Nama` | Montserrat SemiBold | 8.5 (10) | UC-Tinta | Nama wisudawan (maks. 4 baris) |
| `Dir-Label` | Source Sans 3 Semibold, kapital, tracking 40 | 5.5 (7) | UC-Sekunder-30 | Label “JUDUL SKRIPSI” |
| `Dir-Label-Inline` (character style) | Source Sans 3 Semibold, kapital | 5.5 | UC-Sekunder-30 | Label NIM/TTL sebaris dengan datanya |
| `Dir-Data` | Source Sans 3 Regular | 7.5 (9) | UC-Tinta | NIM, TTL |
| `Dir-IPK` | Source Sans 3 Semibold | 7.5 (9) | UC-Tinta | IPK & predikat (di chip) |
| `Dir-Judul` | Source Sans 3 Regular | 8 (10) | UC-Tinta | Judul skripsi — rata kiri, tanpa mengecilkan otomatis |
| `Folio` | Montserrat Medium | 8 | UC-Sekunder-30 | Nomor halaman tengah footer |

Batas bawah ukuran teks direktori: **7.5 pt**. Jika judul terpanjang tidak muat, tambah tinggi area judul atau kurangi spasi lain — jangan mengecilkan huruf di bawah batas ini.

## 5. Master Pages (InDesign 2020)
| Master | Isi | Dipakai di |
|---|---|---|
| `A-Isi` | Latar UC-Primer-60, ornamen kaca tipis di sudut, nomor halaman tengah footer | Halaman editorial |
| `B-Direktori` | Latar, pita header prodi (kaca biru), garis tipis, nomor halaman tengah footer | Direktori wisudawan |
| `C-Tanpa-Nomor` | Latar saja, tanpa nomor | Cover, cover slogan, pembatas bab, cover penutup/belakang |

Nomor halaman memakai *Current Page Number* (Type → Insert Special Character → Markers) di master, rata tengah, baseline sekitar 8 mm dari tepi bawah.

## 6. Grid halaman direktori (2 × 2)
```
A5 148 × 210 mm — halaman KANAN (jilid di kiri). Halaman kiri = cermin.
┌────────────────────────────────────────────┐
│ 18 ▓▓▓ Pita header prodi (tinggi 10 mm) ▓▓▓ 12│  ← di Master B, y = 12–22
│                                            │
│    ┌─ Kartu 1 ────┐ 5 ┌─ Kartu 2 ────┐     │  ← kartu mulai y = 26
│    │ 56.5 × 82 mm │   │              │     │
│    └──────────────┘   └──────────────┘     │
│              5 mm jarak baris              │
│    ┌─ Kartu 3 ────┐   ┌─ Kartu 4 ────┐     │
│    └──────────────┘   └──────────────┘     │  ← berakhir y = 195
│                   — 17 —                   │  ← folio, tengah footer
└────────────────────────────────────────────┘
```
- Lebar kartu: (118 − 5) / 2 = **56.5 mm**. Tinggi kartu: (183 − 10 header − 4 jarak − 5) / 2 = **82 mm**.
- Margin halaman direktori: **atas 26 mm** (12 + 10 header + 4 jarak), bawah 15, dalam 18, luar 12.
- Karena margin dalam ≠ luar, setelah Data Merge jalankan `scripts/indesign/rapikan-direktori.jsx` agar kartu di halaman kiri ikut bergeser ke margin yang benar (lihat PLAN Tahap 6).

### Varian A — FINAL (foto kiri, judul selebar kartu)
```
┌─────────────────────────────┐
│ ┌──────┐ (01) chip emas      │
│ │ FOTO │ NAMA WISUDAWAN      │
│ │ 3:4  │ NIM 2201…           │
│ │22×29 │ TTL Kota, tgl lahir │
│ └──────┘                     │
│ ▭ IPK 3,xx · Predikat ▭      │
│ ▌JUDUL SKRIPSI               │
│ ▌Judul skripsi mengalir      │
│  selebar kartu (48.5 mm),    │
│  maksimum ±9 baris.          │
└─────────────────────────────┘
```
- Padding kartu 3 mm. Foto 22 × 29.3 mm (rasio 3:4), sudut membulat 2 mm.
- Kolom teks samping foto: lebar 25.5 mm (Nama, lalu NIM dan TTL dengan label sebaris).
- Posisi frame relatif terhadap pojok kartu (y, x dalam mm): foto 3–32.3 / 3–25; chip No 3–7.5 / 28–36; info 8.5–35.5 / 28–53.5 (nama boleh sampai 4 baris); chip IPK 37–42 / 3–53.5; judul 45–79 / 3–53.5 (teks mulai x = 5 setelah garis aksen emas).
- Area judul ±9 baris pada 8/10 pt (±310 karakter). Diuji di mockup dengan judul 254 karakter (7 baris) dan nama 49 karakter (pas, tanpa ruang sisa) — nama > 45 karakter tetap perlu dicek.

### Varian B — tidak dipakai
Semua data di kolom kanan (±20 karakter per baris); judul panjang terpotong pada uji mockup v1. Ditolak pemilik proyek (Okt 2026).

## 7. Bahasa visual glassmorphism di InDesign
InDesign tidak punya *background blur*. Cara mensimulasikannya:
1. **Bidang kaca**: rectangle fill Putih, Opacity 60–70%, stroke 0.5 pt Putih Opacity 90%, sudut membulat 3 mm.
2. **Kedalaman**: Effects → Drop Shadow halus (warna UC-Sekunder-30, opacity 15%, distance 1 mm, size 3 mm).
3. **Highlight**: Gradient Feather linear dari kiri-atas (100%) ke kanan-bawah (40%).
4. **Ornamen latar**: lingkaran/bidang membulat UC-Sekunder-30 opacity 10–20% dengan Gradient Feather, garis hairline 0.25 pt, titik-titik grid kecil.
5. **Bila butuh blur sungguhan** (mis. cover dengan foto grup): buat di Photoshop, simpan PSD/TIFF 300 ppi, lalu place ke InDesign.
6. Simpan semuanya sebagai **Object Styles**: `Kaca-Kartu`, `Kaca-Header`, `Chip-Emas`, `Foto-Bingkai`, `Ornamen-Lingkaran`.

Catatan cetak: efek transparansi akan di-*flatten* saat ekspor PDF/X-1a. Untuk menghindari garis putih tipis (*stitching*), lebih aman pakai PDF/X-4 bila percetakan menerima. Percetakan baru menyebut “PDF” — **tanyakan PDF/X-1a atau PDF/X-4, dan profil warnanya**.

## 8. Foto wisudawan
- Rasio **3:4** potret, wajah di sepertiga atas, latar seragam bila memungkinkan.
- Resolusi efektif ≥ 300 ppi pada 22 × 29.3 mm → minimal **260 × 346 px** (disarankan ≥ 600 × 800 px).
- Nama file = **NIM** (mis. `2201010001.jpg`), bukan urutan nomor.
- Object Style `Foto-Bingkai`: Fitting **Fill Frame Proportionally**, Align Top Center.
