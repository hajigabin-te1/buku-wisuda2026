# Spesifikasi Desain — Buku Wisuda STIA Amuntai 2026

Status: **v0.3** — spesifikasi percetakan dikonfirmasi; kartu direktori **Varian A**; gaya visual mengikuti **`01-Brief-Referensi/referensi.png`** (Okt 2026). Profil warna & standar PDF/X masih perlu ditanyakan ke percetakan.

## 0. Referensi visual
Acuan utama: `01-Brief-Referensi/referensi.png`. Unsur yang diambil:
- Latar biru sangat muda dengan gradasi lembut; **pecahan kaca diagonal biru-emas** di sudut halaman (sisi luar) dan pita tipis di tepi sampul.
- Sampul: logo + nama institusi kiri atas, “WISUDA 2026” kanan atas, judul **UNTUKMU / CINTA** serif kapital besar, foto grup wisudawan (cutout) dengan toga dilempar, “KENANGAN • PERJUANGAN • HARAPAN” di bawah.
- Halaman dalam: judul bagian **kapital biru berspasi lebar + subjudul + garis tipis dengan segmen emas dan titik**; tulisan **script “Untukmu Cinta” dengan sapuan emas**.
- Direktori: kartu kaca putih bergaris tipis biru, foto kiri, **nomor emas di pojok kanan atas foto**, data dengan **ikon garis + label biru + nilai**.
- Galeri: foto berbingkai putih dengan aksen emas.

Yang **tidak** diambil dari referensi (belum dikonfirmasi / bertentangan dengan brief):
- Teks “Sebuah perjalanan, sebuah perjuangan, sebuah masa depan.”, “Bersama Menuju Masa Depan Yang Lebih Baik”, puisi di halaman pembuka, kutipan sambutan, dan nama pejabat/wisudawan di referensi — semuanya contoh; diganti slogan resmi atau placeholder.
- Nomor halaman di pojok (referensi) → tetap **tengah footer** sesuai brief.
- “Daftar Mahasiswa” → memakai istilah brief “Daftar Wisudawan”.
- Halaman **Profil Wisudawan 1 orang/halaman**, **Daftar Isi**, dan **Sambutan Ketua Yayasan** ada di referensi tetapi tidak ada di daftar isi brief → menunggu keputusan pemilik proyek (Daftar Isi dibuat sebagai mockup opsional).
- Foto gedung kampus: hanya bila foto resmi tersedia (AGENT.md melarang foto kampus sembarangan).

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

## 3. Tipografi (semua lisensi bebas untuk cetak: SIL OFL / Apache 2.0)
| Peran | Font | Catatan |
|---|---|---|
| Judul sampul “UNTUKMU CINTA” | **Cinzel** Bold/SemiBold | Serif kapital klasik, mendekati referensi |
| Tulisan script tema (“Untukmu Cinta”, “Foto Kenangan”) | **Satisfy** | Script kuas miring seperti referensi; hanya untuk frasa pendek |
| Judul bagian, nama wisudawan, angka | **Montserrat** (SemiBold/Bold) | Kapital berspasi lebar untuk judul bagian |
| Teks isi, data, judul skripsi | **Source Sans 3** (Regular/Semibold) | Hemat lebar, terbaca di ukuran kecil |
| Kutipan (sambutan) | **Playfair Display** Italic | Serif miring seperti kutipan di referensi |

Instal kelima font di komputer produksi (Windows) **sebelum** menjalankan skrip setup. Jika font lain dipakai, ganti nama font di blok `CFG` skrip `scripts/indesign/setup-dokumen.jsx` dan di tabel ini. Simpan berkas lisensi bersama paket akhir.

## 4. Paragraph & Character Styles
Ukuran dalam pt; leading dalam kurung.

| Style | Font | Ukuran | Warna | Pemakaian |
|---|---|---|---|---|
| `Bagian-Judul` | Montserrat Bold, kapital, tracking 45 | 12.5 (14) | UC-Sekunder-30 | Judul bagian (DAFTAR WISUDAWAN, SAMBUTAN, …) |
| `Bagian-Sub` | Montserrat SemiBold, kapital, tracking 55 | 6.5 (8) | UC-Sekunder-30 | Subjudul di bawah judul bagian |
| `Sampul-Judul` | Cinzel Bold, tracking 40 | 56 (54) | UC-Sekunder-30 | “CINTA” di sampul (“UNTUKMU” ±27 pt, override lokal) |
| `Script-Tema` | Satisfy | 30 (32) | UC-Sekunder-30 | Frasa script + sapuan emas |
| `H1-Bab` | Montserrat Bold | 20 (24) | UC-Sekunder-30 | Judul besar (pembatas bab) |
| `H2-Subjudul` | Montserrat SemiBold | 12 (15) | UC-Tinta | Subjudul |
| `Isi` | Source Sans 3 Regular | 10 (14) | UC-Tinta | Teks naskah, rata kiri-kanan |
| `Puitis` | Playfair Display Italic | 12 (17) | UC-Sekunder-30 | Kutipan |
| `Lirik` | Source Sans 3 Regular | 10 (15) | UC-Tinta | Mars & Hymne, rata tengah |
| `Dir-No` | Montserrat Bold | 7 (8) | UC-Tinta | Nomor urut di chip emas |
| `Dir-Label` | Source Sans 3 Semibold | 6 (8) | UC-Sekunder-30 | Label berikon: Nama, Tempat/Tgl. Lahir, NIM, IPK, Predikat, Judul Skripsi |
| `Dir-Nama` | Montserrat SemiBold | 8 (9.5) | UC-Tinta | Nama wisudawan (maks. 4 baris) |
| `Dir-Data` | Source Sans 3 Regular | 7.5 (9) | UC-Tinta | TTL, NIM, IPK, Predikat |
| `Dir-Judul` | Source Sans 3 Regular, indent kiri 3.8 mm | 8 (10) | UC-Tinta | Judul skripsi, sejajar label setelah ikon |
| `Folio` | Montserrat SemiBold | 7.5 | UC-Sekunder-30 | Nomor halaman tengah footer |

Batas bawah ukuran teks direktori: **7.5 pt**. Jika judul terpanjang tidak muat, tambah tinggi area judul atau kurangi spasi lain — jangan mengecilkan huruf di bawah batas ini.

## 5. Master Pages (InDesign 2020)
| Master | Isi | Dipakai di |
|---|---|---|
| `A-Isi` | Latar UC-Primer-60, ornamen pecahan kaca di sudut bawah sisi luar, nomor halaman tengah footer | Halaman editorial |
| `B-Direktori` | Latar, ornamen sudut, judul bagian “DAFTAR WISUDAWAN” + subjudul prodi + garis biru-emas, nomor halaman | Direktori wisudawan |
| `C-Tanpa-Nomor` | Latar + ornamen sudut besar, tanpa nomor | Halaman pembuka, pembatas bab, halaman penutup tanpa nomor |

Sampul depan & belakang **tidak** di dokumen isi: dibuat di file sampul terpisah (bentangan) setelah lebar punggung diketahui.

Nomor halaman memakai *Current Page Number* (Type → Insert Special Character → Markers) di master, rata tengah, baseline sekitar 8 mm dari tepi bawah.

## 6. Grid halaman direktori (2 × 2)
```
A5 148 × 210 mm — halaman KANAN (jilid di kiri). Halaman kiri = cermin.
┌────────────────────────────────────────────┐
│ 18  DAFTAR WISUDAWAN                     12│  ← judul bagian di Master B, y = 12
│     PROGRAM STUDI … · WISUDA 2026          │
│     ───────────────────────────▬▬▬▬▬▬●     │  ← garis y = 22.5
│    ┌─ Kartu 1 ────┐ 5 ┌─ Kartu 2 ────┐     │  ← kartu mulai y = 27
│    │ 56.5 × 81 mm │   │              │     │
│    └──────────────┘   └──────────────┘     │
│    ┌─ Kartu 3 ────┐   ┌─ Kartu 4 ────┐     │
│    └──────────────┘   └──────────────┘     │  ← berakhir y = 194
│                     17                     │  ← folio, tengah footer
└────────────────────────────────────────────┘
```
- Lebar kartu: (118 − 5) / 2 = **56.5 mm**. Tinggi kartu: **81 mm** (27 + 81 + 5 + 81 = 194 ≤ 195).
- Margin halaman direktori: **atas 27 mm**, bawah 15, dalam 18, luar 12.
- Karena margin dalam ≠ luar, setelah Data Merge jalankan `scripts/indesign/rapikan-direktori.jsx` (lihat PLAN Tahap 6).

### Kartu Varian A — gaya referensi (FINAL)
```
┌──────────────────────────────┐
│ ┌──────[01]  ◦Nama          │
│ │ FOTO │     NAMA WISUDAWAN   │
│ │ 3:4  │     ◦Tempat, Tgl. Lahir
│ │22×29 │     Amuntai, 12 …    │
│ └──────┘                      │
│ ───────────────────────────── │
│ ◦NIM      ◦IPK  ◦Predikat │
│ 2201…       3,xx    Dengan …  │
│ ◦Judul Skripsi              │
│    Judul skripsi mengalir     │
│    selebar kartu, maks. 8 baris
└──────────────────────────────┘
```
Posisi frame relatif terhadap pojok kartu (y1–y2 / x1–x2, mm):
| Frame | Posisi | Isi |
|---|---|---|
| Latar kartu | 0–81 / 0–56.5 | Object Style `Kaca-Kartu` |
| Foto | 3–32.3 / 3–25 | `Foto-Bingkai`, field `@Foto` |
| Nomor | 2–6.6 / 20.5–28 | `Chip-Emas`, field `No` (menumpang pojok foto) |
| Info | 3.5–33.5 / 28–53.5 | Label Nama + `Nama`, label Tempat/Tgl. Lahir + `TTL` |
| Garis pemisah | y 34.5 / 3–53.5 | 0.25 pt biru 30% |
| NIM | 35.7–45.5 / 3–19 | Label + `NIM` |
| IPK | 35.7–45.5 / 20.5–30 | Label + `IPK` |
| Predikat | 35.7–45.5 / 31.5–53.5 | Label + `Predikat` (boleh 2 baris) |
| Judul | 46.5–78.5 / 3–53.5 | Label + `Judul` (indent 3.8 mm) |

- Ikon: SVG di `05-InDesign/Links/ikon/` (dibuat skrip, bukan aset resmi), disisipkan sebagai inline graphic di awal label.
- Kapasitas judul: **8 baris ≈ 250 karakter** (uji mockup: 254 karakter tepat 8 baris). Bila ada judul lebih panjang: (1) cek laporan validasi, (2) untuk kartu itu saja turunkan `Dir-Judul` ke 7.5/9.5 pt (batas bawah), atau (3) diskusikan pemadatan tata letak. Jangan memotong judul.
- Nama: maks. 4 baris (uji: 49 karakter muat). TTL: maks. 2 baris.

### Varian B — tidak dipakai
Ditolak pemilik proyek (Okt 2026).

## 7. Bahasa visual (glassmorphism gaya referensi) di InDesign
1. **Latar**: UC-Primer-60 penuh hingga bleed (di master).
2. **Pecahan kaca sudut**: `05-InDesign/Links/ornamen/ornamen-sudut.svg` — di-place pada master di sudut bawah sisi luar (cermin untuk halaman kiri). Sampul memakai juga `ornamen-tepi.svg` di tepi kiri.
3. **Kartu kaca**: fill Putih opacity 80%, stroke biru tint 30% 0.5 pt, sudut 3 mm, drop shadow halus (biru 15%, distance 0.8 mm, size 2.5 mm), gradient feather linear.
4. **Judul bagian**: teks kapital biru + garis 0.4 pt biru 35% + segmen emas 1.8 pt di 38% kanan + titik biru.
5. **Script + sapuan emas**: `Script-Tema` + `ornamen/sapuan-emas.svg` di bawahnya, diputar ±−6°.
6. **Toga** (sampul): `ornamen/toga.svg`, beberapa buah, diputar acak — hanya bila foto grup bukan foto yang sudah berisi toga terbang.
7. **Bila butuh blur sungguhan** (mis. kaca di atas foto sampul): buat di Photoshop, simpan PSD/TIFF 300 ppi, lalu place.
8. Object Styles: `Kaca-Kartu`, `Chip-Emas`, `Foto-Bingkai`, `Teks-Kartu`.

Catatan cetak: efek transparansi akan di-*flatten* saat ekspor PDF/X-1a. Untuk menghindari garis putih tipis (*stitching*), lebih aman pakai PDF/X-4 bila percetakan menerima. Percetakan baru menyebut “PDF” — **tanyakan PDF/X-1a atau PDF/X-4, dan profil warnanya**.

## 8. Foto wisudawan
- Rasio **3:4** potret, wajah di sepertiga atas, latar seragam bila memungkinkan.
- Resolusi efektif ≥ 300 ppi pada 22 × 29.3 mm → minimal **260 × 346 px** (disarankan ≥ 600 × 800 px).
- Nama file = **NIM** (mis. `2201010001.jpg`), bukan urutan nomor.
- Object Style `Foto-Bingkai`: Fitting **Fill Frame Proportionally**, Align Top Center.
