# Rencana Produksi — Buku Wisuda STIA Amuntai 2026

Dokumen kerja dari persiapan data sampai PDF siap cetak. Spesifikasi visual ada di `docs/SPEK-DESAIN.md`.

Legenda status: ☐ belum · ◐ berjalan · ☑ selesai

## Tahap 0 — Konfirmasi dan pengumpulan bahan
☐ Spesifikasi percetakan: bleed, margin jilid, jenis jilid (kawat/lem), kelipatan halaman, jenis kertas, format PDF (PDF/X-1a atau X-4), profil warna, halaman tunggal atau spread, crop marks.
☐ Logo resmi STIA Amuntai (vektor: AI/EPS/SVG/PDF) → `02-Aset-Resmi/Logo/`.
☐ Foto grup/kenangan resmi → `02-Aset-Resmi/Foto-Grup/`.
☐ Naskah resmi: Kata Pengantar, Mars, Hymne, Sambutan Ketua, Visi-Misi (STIA, Prodi Bisnis, Prodi Publik), Janji Wisudawan, Filosofi.
☐ Daftar nama dan jabatan: Yayasan Bakti Muslimin, Pimpinan, Senat (beserta foto bila ada).
☐ Data wisudawan per prodi (Excel) → `03-Data/Sumber-Asli/` (**jangan diedit**).
☐ Font terpasang di komputer produksi (Montserrat, Source Sans 3, Playfair Display — atau pengganti yang disetujui).

## Tahap 1 — Persiapan data
1. Salin file asli ke `03-Data/Data-Bersih/` (yang diedit hanya salinan).
2. Pisahkan per prodi: `bisnis.xlsx` dan `publik.xlsx` (atau satu file dengan kolom prodi lalu dipisah).
3. Pastikan header persis: `No, NIM, Nama, TTL, IPK, Predikat, Judul, Foto`.
4. Rapikan: spasi ganda, kapitalisasi nama (sesuai ijazah — jangan diubah sembarangan), format TTL konsisten (`Amuntai, 12 Januari 2003`), IPK dua desimal.
5. Judul skripsi: periksa ejaan dengan dokumen resmi akademik; jangan disingkat.

## Tahap 2 — Validasi data (skrip)
Jalankan di komputer produksi (lihat `scripts/README.md`):
```
python scripts/validasi_data.py 03-Data/Data-Bersih/bisnis.xlsx --foto-dir 04-Foto-Wisudawan/bisnis --out 03-Data/CSV-DataMerge/bisnis
```
Skrip melaporkan field kosong, NIM duplikat, nama ganda, IPK tidak wajar, foto hilang, foto yang namanya tidak mengandung NIM, dan judul terpanjang. Perbaiki **di salinan bersih**, lalu jalankan ulang sampai tidak ada ERROR.

## Tahap 3 — Foto
1. Ganti nama file foto menjadi NIM (`2201010001.jpg`).
2. Crop 3:4, wajah konsisten (Photoshop: Crop tool rasio 3:4, lalu Image Processor/Action untuk batch).
3. Minimal 600 × 800 px, simpan JPG kualitas tinggi atau TIFF. Warna RGB boleh; konversi CMYK terjadi saat ekspor PDF.
4. Tandai foto yang perlu diganti (blur, gelap, salah orang) dan kirim daftar ke panitia.

## Tahap 4 — Sistem desain di InDesign
1. Jalankan `scripts/indesign/setup-dokumen.jsx` (lihat panduan di `scripts/README.md`). Skrip membuat dokumen A5, swatch, paragraph/character/object styles, dan master A/B/C.
2. Periksa hasilnya; sesuaikan bleed/margin dengan spesifikasi vendor.
3. Simpan sebagai `05-InDesign/INDD/00-TEMPLATE-Sistem.indd` (jadikan sumber style untuk semua file lain).

## Tahap 5 — Konsep visual (persetujuan)
Mockup di `06-Proof/konsep/` (data DUMMY, logo/foto berupa placeholder). Pilih:
- Varian kartu direktori A atau B.
- Arah cover & halaman editorial.
Setelah disetujui, desain dibangun ulang di InDesign sebagai objek editable.

## Tahap 6 — Template direktori + Data Merge (per prodi)
Lakukan sekali untuk Administrasi Bisnis, lalu ulangi untuk Administrasi Publik.

1. Buka `00-TEMPLATE-Sistem.indd`, *Save As* `05-InDesign/INDD/10-Direktori-Bisnis-TEMPLATE.indd`. Pastikan hanya ada **satu halaman** dengan master `B-Direktori` (halaman 1 hasil skrip sudah berisi kartu contoh). Cek Layout → Margins and Columns: atas 26 mm, bawah 15 mm, kiri = kanan 13.5 mm.
   Margin direktori sengaja simetris, sehingga hasil merge tetap benar baik dokumen facing pages maupun tidak. Bila *Preview Multiple Record Layout* terlihat janggal di facing pages, matikan facing pages pada template (File → Document Setup) — posisi kartu tidak berubah.
2. Di master `B-Direktori`, ketik nama prodi di pita header (mis. “Wisudawan Program Studi Administrasi Bisnis”).
3. Di halaman (bukan master) hanya boleh ada **satu kartu** di pojok kiri-atas area margin (sudah dibuat skrip: latar kaca, chip No, frame foto, frame info, chip IPK, frame judul). Sesuaikan desainnya dengan konsep yang disetujui; jangan meng-group frame foto ke dalam group bertingkat.
4. **Window → Utilities → Data Merge** → menu panel → *Select Data Source* → pilih file `.txt` UTF-16 hasil skrip (centang *Show Import Options*: Delimiter **Tab**, Encoding **Unicode**).
5. Seleksi teks contoh `«Nama»` dan seterusnya, lalu klik nama field di panel untuk menggantinya dengan field asli `<<No>>`, `<<Nama>>`, `<<NIM>>`, `<<TTL>>`, `<<IPK>>`, `<<Predikat>>`, `<<Judul>>`. Pilih frame foto lalu klik field `Foto`.
6. Panel Data Merge → *Content Placement Options*: Fitting **Fill Frames Proportionally**, centang **Center in Frame**, centang *Link Images*, centang *Remove Blank Lines for Empty Fields*.
7. Centang **Preview** di panel; periksa beberapa record, termasuk record dengan judul terpanjang (lihat laporan skrip).
8. *Create Merged Document* → Records per Document Page: **Multiple Records** → tab *Multiple Record Layout*: Margin sesuai template, **Spacing between Columns 5 mm, between Rows 5 mm**, Arrange By Rows. Centang *Preview Multiple Record Layout* untuk memastikan 2 × 2 tepat.
9. Tab *Options*: centang *Generate Overset Text Report with Document Creation* dan biarkan *Alert When Images Are Missing* tetap aktif.
10. Simpan hasil sebagai `05-InDesign/INDD/11-Direktori-Bisnis.indd`. Periksa laporan overset; tangani judul yang meluap (perlebar area judul, bukan mengecilkan huruf di bawah 7.5 pt).

Catatan penting Data Merge:
- Pada mode Multiple Records, **semua objek di halaman diduplikasi per record**, sedangkan objek di **master tidak**. Karena itu pita header dan nomor halaman wajib di master.
- Halaman terakhir yang tidak penuh (mis. 2 kartu) itu normal; isi sisa ruang dengan ornamen ringan atau biarkan bersih.
- Bila data berubah setelah merge: perbaiki CSV → jalankan skrip ulang → merge ulang. Jangan mengedit teks hasil merge satu per satu kecuali terpaksa (dan catat perubahannya kembali ke data).

## Tahap 7 — Halaman editorial
Buat file per bagian (memakai style dari template sistem):
- `01-Depan.indd` — cover, cover slogan, kata pengantar, mars, hymne, sambutan, unsur yayasan/pimpinan/senat, visi-misi, janji, filosofi.
- `12-Kenangan.indd` — 4 halaman foto kenangan.
- `13-Penutup.indd` — teks penutup (docs/EDITORIAL.md), cover penutup, cover belakang.

## Tahap 8 — Penggabungan (InDesign Book)
1. **File → New → Book** → `05-InDesign/Buku-Wisuda-2026.indb`.
2. Tambahkan urut: `01-Depan`, `11-Direktori-Bisnis`, `11b-Direktori-Publik`, `12-Kenangan`, `13-Penutup`.
3. Jadikan `00-TEMPLATE-Sistem.indd` sebagai *Style Source*, lalu *Synchronize* agar style seragam.
4. *Book Page Numbering Options*: Continue from previous document; periksa halaman kiri/kanan setiap bab.
5. Cek total halaman sesuai kelipatan yang diminta vendor; tambahkan halaman catatan/kosong bila perlu.

## Tahap 9 — Proof
1. Ekspor PDF proof (preset *[High Quality Print]*, tanpa crop marks) → `06-Proof/proof-vN-YYYYMMDD.pdf`.
2. Bagikan ke panitia untuk pemeriksaan: ejaan nama, NIM, TTL, IPK, predikat, judul, kecocokan foto.
3. Kumpulkan koreksi dalam satu daftar; koreksi data dilakukan di data bersih → merge ulang.
4. Ulangi sampai ada persetujuan tertulis panitia.

## Tahap 10 — Preflight & ekspor final
☐ Window → Output → Preflight: 0 error (missing/modified links, overset, font hilang).
☐ Resolusi gambar efektif ≥ 300 ppi (foto) / logo vektor.
☐ Bleed terisi pada objek yang menyentuh tepi; teks penting di dalam margin.
☐ Nomor halaman benar, cover tanpa nomor.
☐ Window → Output → Separations Preview / Flattener Preview untuk efek transparansi.
☐ Ekspor dengan preset dari vendor (PDF/X-1a atau X-4, profil warna, bleed, crop marks sesuai permintaan) → `07-Final-Cetak/`.
☐ Cetak uji (dummy fisik) minimal beberapa halaman direktori & cover sebelum cetak massal.

## Tahap 11 — Arsip
File → Package dari setiap `.indd` (atau dari Book) → salin Links, Fonts, laporan, plus CSV final dan PDF final. Simpan di penyimpanan internal yang aksesnya terbatas.

## Keterbatasan
- Skrip `.jsx` ditulis untuk InDesign 2020 (ExtendScript) tetapi **belum diuji di InDesign**; jalankan di salinan dokumen dulu.
- Mockup konsep dirender dari HTML dengan data DUMMY; ini acuan visual, bukan file cetak.
- Status “siap cetak” hanya setelah Tahap 9–10 lolos dan spesifikasi vendor terkonfirmasi.
