# Buku Wisuda STIA Amuntai 2026

Repository kerja untuk desain, editorial, pengelolaan data, dan persiapan produksi buku wisuda.

## Ringkasan
- Tema: **Untukmu Cinta**
- Ukuran jadi: **A5 portrait**
- Gaya: futuristic, elegan, glassmorphism
- Palet: `#EBF8FF` (60%), `#3081DB` (30%), `#FFE031` (10%)
- Direktori: 4 wisudawan per halaman, susunan 2 × 2
- Software utama: Adobe InDesign 2020

## Mulai
1. Baca `AGENT.md`.
2. Untuk Claude Code, baca `CLAUDE.md` juga; file tersebut mengarahkan agent agar mengikuti `AGENT.md`.
3. Simpan logo/foto grup resmi di `02-Aset-Resmi/`.
4. Simpan data asli di `03-Data/Sumber-Asli/` dan jangan mengedit salinannya.
5. Simpan CSV Data Merge di `03-Data/CSV-DataMerge/`.
6. Simpan dokumen InDesign dan Links di `05-InDesign/`.
7. Simpan PDF pemeriksaan di `06-Proof/` dan keluaran disetujui di `07-Final-Cetak/`.

## Struktur
```text
AGENT.md / CLAUDE.md / README.md
01-Brief-Referensi/
02-Aset-Resmi/
03-Data/
04-Foto-Wisudawan/
05-InDesign/
06-Proof/
07-Final-Cetak/
docs/
scripts/
```

## Privasi dan GitHub
Buku ini dapat memuat foto, NIM, tanggal lahir, IPK, dan informasi pribadi. **Jangan unggah data asli atau foto wisudawan ke repository publik.** Gunakan repository private jika memang perlu, dan pertimbangkan menyimpan data sensitif di penyimpanan internal dengan akses terbatas. Git LFS dapat membantu file besar, tetapi bukan pengganti kontrol akses.

Ini adalah starter structure. Folder kosong memakai `.gitkeep`; template desain, data asli, dan file `.indd` final belum dibuat otomatis.
