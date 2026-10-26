# Spesifikasi Desain — Buku Wisuda STIA Amuntai 2026

Status: **usulan v0.1 (konsep)**. Angka bleed, margin jilid, dan profil warna masih **menunggu konfirmasi percetakan**. Ubah dokumen ini setelah spesifikasi vendor diterima.

## 1. Format
| Item | Nilai | Status |
|---|---|---|
| Ukuran jadi | A5 portrait, 148 × 210 mm | Final |
| Facing pages | Ya (halaman kiri/kanan) | Usulan |
| Bleed | 3 mm semua sisi | **Konfirmasi vendor** |
| Margin atas | 12 mm | Usulan |
| Margin bawah | 15 mm (ruang nomor halaman) | Usulan |
| Margin dalam (jilid) | 15 mm | **Konfirmasi vendor** — jilid lem/perfect binding biasanya butuh lebih lebar daripada jilid kawat |
| Margin luar | 12 mm | Usulan |
| Area aman (live area) | 121 × 183 mm | Turunan dari margin di atas |
| Margin halaman direktori | atas 26, bawah 15, **dalam = luar = 13.5 mm** | Usulan — dibuat simetris agar posisi kartu sama di halaman kiri/kanan dan aman untuk Data Merge |
| Jumlah halaman | Kelipatan 4 (atau sesuai vendor) | **Konfirmasi vendor** |

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
| `Dir-Nama` | Montserrat SemiBold | 8.5 (10) | UC-Tinta | Nama wisudawan (maks. 3 baris) |
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
A5 148 × 210 mm, margin direktori: samping 13.5 (simetris) / atas 26 / bawah 15
┌──────────────────────────────────────────┐
│  ▓▓▓ Pita header prodi (tinggi 10 mm) ▓▓▓  │  ← di Master B, mulai y = 12
│                                          │
│  ┌─ Kartu 1 ─────┐ 5 ┌─ Kartu 2 ─────┐   │  ← kartu mulai y = 26
│  │ 58 × 82 mm    │   │               │   │
│  └───────────────┘   └───────────────┘   │
│           5 mm jarak baris               │
│  ┌─ Kartu 3 ─────┐   ┌─ Kartu 4 ─────┐   │
│  └───────────────┘   └───────────────┘   │  ← berakhir y = 195
│                  — 12 —                  │  ← folio, tengah footer
└──────────────────────────────────────────┘
```
- Lebar kartu: (121 − 5) / 2 = **58 mm**. Tinggi kartu: (169 − 5) / 2 = **82 mm**.
- Template Data Merge: **margin atas halaman template = 26 mm** (12 + 10 header + 4 jarak) agar kartu pertama tepat di bawah pita header.

### Varian A — direkomendasikan (foto kiri, judul lebar penuh)
```
┌──────────────────────────────┐
│ ┌──────┐ (01) chip emas       │
│ │ FOTO │ NAMA WISUDAWAN       │
│ │ 3:4  │ NIM 2201…            │
│ │22×29 │ TTL Kota, tgl lahir  │
│ └──────┘                      │
│ ▭ IPK 3,xx · Predikat ▭       │
│ JUDUL SKRIPSI                 │
│ Judul skripsi mengalir di     │
│ lebar penuh kartu (52 mm),    │
│ ±36 karakter per baris,       │
│ maksimum ±10 baris.           │
└──────────────────────────────┘
```
- Padding kartu 3 mm. Foto 22 × 29.3 mm (rasio 3:4), sudut membulat 2 mm.
- Kolom teks samping foto: lebar 27 mm (Nama, lalu NIM dan TTL dengan label sebaris).
- Posisi frame relatif terhadap pojok kartu (y, x dalam mm): foto 3–32.3 / 3–25; chip No 3–7.5 / 28–36; info 8.5–35.5 / 28–55 (nama boleh sampai 4 baris); chip IPK 37–42 / 3–55; judul 45–79 / 3–55.
- Area judul: 52 × 34 mm (termasuk label) → muat ±9 baris pada 8/10 pt (±330 karakter). Diuji di mockup dengan judul 254 karakter (7 baris) dan nama 49 karakter.

### Varian B — alternatif (foto kiri, semua data di kanan)
- Foto 22 × 29.3 mm di kiri, kolom data 30 mm di kanan sepanjang kartu.
- Lebih "rapi" secara konsep, tetapi judul ±20 karakter per baris → judul panjang menjadi 12–16 baris dan nama panjang mudah terpotong. Hanya cocok bila judul rata-rata pendek.

## 7. Bahasa visual glassmorphism di InDesign
InDesign tidak punya *background blur*. Cara mensimulasikannya:
1. **Bidang kaca**: rectangle fill Putih, Opacity 60–70%, stroke 0.5 pt Putih Opacity 90%, sudut membulat 3 mm.
2. **Kedalaman**: Effects → Drop Shadow halus (warna UC-Sekunder-30, opacity 15%, distance 1 mm, size 3 mm).
3. **Highlight**: Gradient Feather linear dari kiri-atas (100%) ke kanan-bawah (40%).
4. **Ornamen latar**: lingkaran/bidang membulat UC-Sekunder-30 opacity 10–20% dengan Gradient Feather, garis hairline 0.25 pt, titik-titik grid kecil.
5. **Bila butuh blur sungguhan** (mis. cover dengan foto grup): buat di Photoshop, simpan PSD/TIFF 300 ppi, lalu place ke InDesign.
6. Simpan semuanya sebagai **Object Styles**: `Kaca-Kartu`, `Kaca-Header`, `Chip-Emas`, `Foto-Bingkai`, `Ornamen-Lingkaran`.

Catatan cetak: efek transparansi akan di-*flatten* saat ekspor PDF/X-1a. Untuk menghindari garis putih tipis (*stitching*), lebih aman pakai PDF/X-4 bila vendor menerima. Konfirmasi ke vendor.

## 8. Foto wisudawan
- Rasio **3:4** potret, wajah di sepertiga atas, latar seragam bila memungkinkan.
- Resolusi efektif ≥ 300 ppi pada 22 × 29.3 mm → minimal **260 × 346 px** (disarankan ≥ 600 × 800 px).
- Nama file = **NIM** (mis. `2201010001.jpg`), bukan urutan nomor.
- Object Style `Foto-Bingkai`: Fitting **Fill Frame Proportionally**, Align Top Center.
