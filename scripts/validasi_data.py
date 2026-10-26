#!/usr/bin/env python3
"""Validasi data wisudawan dan siapkan sumber Data Merge InDesign.

Buku Wisuda STIA Amuntai 2026. Lihat scripts/README.md untuk cara pakai.

Masukan : .xlsx atau .csv (salinan di 03-Data/Data-Bersih/, BUKAN file asli)
          dengan header: No, NIM, Nama, TTL, IPK, Predikat, Judul, Foto
Keluaran: <out>-datamerge.txt  (UTF-16, tab, header @Foto) -> untuk InDesign
          <out>-cek.csv        (UTF-8 BOM) -> untuk dibuka di Excel
          <out>-laporan.txt    laporan validasi
File masukan tidak pernah ditulis ulang.
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path, PureWindowsPath

KOLOM = ["No", "NIM", "Nama", "TTL", "IPK", "Predikat", "Judul", "Foto"]
EKSTENSI_FOTO = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".psd"}
BATAS_JUDUL = 250  # karakter; kapasitas 8 baris area judul kartu (SPEK §6)
BATAS_NAMA = 45
MIN_PX = (260, 346)  # 22 x 29.3 mm @ 300 ppi
SARAN_PX = (600, 800)


def baca_csv(path):
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            with open(path, newline="", encoding=enc) as f:
                teks = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        sys.exit(f"Tidak bisa membaca encoding {path}")
    dialek = csv.Sniffer().sniff(teks.splitlines()[0], delimiters=",;\t")
    baris = list(csv.reader(teks.splitlines(), dialek))
    return baris[0], baris[1:], enc


def baca_xlsx(path, sheet):
    try:
        import openpyxl
    except ImportError:
        sys.exit("Membaca .xlsx butuh openpyxl: pip install openpyxl (atau simpan sebagai CSV UTF-8)")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    baris = [["" if v is None else str(v) for v in r] for r in ws.iter_rows(values_only=True)]
    baris = [r for r in baris if any(c.strip() for c in r)]
    return baris[0], baris[1:], "xlsx"


def rapikan(teks):
    teks = teks.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return re.sub(r" {2,}", " ", teks).strip()


def parse_ipk(teks):
    try:
        return float(teks.replace(",", "."))
    except ValueError:
        return None


def ukuran_foto(path):
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def cari_foto(foto_dir, nama_file, nim):
    p = foto_dir / nama_file
    if nama_file and p.is_file():
        return p
    # cadangan: cari file yang namanya = NIM dengan ekstensi apa pun
    for f in foto_dir.iterdir():
        if f.stem == nim and f.suffix.lower() in EKSTENSI_FOTO:
            return f
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("masukan", type=Path)
    ap.add_argument("--sheet", help="nama sheet Excel (default: sheet pertama)")
    ap.add_argument("--foto-dir", type=Path, help="folder foto di komputer ini, untuk cek keberadaan & resolusi")
    ap.add_argument("--foto-base", help=r"path folder foto yang dipakai InDesign, mis. D:\BukuWisuda2026\04-Foto-Wisudawan\bisnis")
    ap.add_argument("--out", type=Path, help="awalan file keluaran, mis. 03-Data/CSV-DataMerge/bisnis")
    ap.add_argument("--nomor-otomatis", action="store_true", help="isi kolom No berurutan 1..n bila kosong")
    ap.add_argument("--paksa", action="store_true", help="tetap tulis keluaran walau ada ERROR (hanya untuk uji layout)")
    a = ap.parse_args()

    if a.masukan.suffix.lower() in (".xlsx", ".xlsm"):
        header, rows, enc = baca_xlsx(a.masukan, a.sheet)
    else:
        header, rows, enc = baca_csv(a.masukan)

    header = [rapikan(h).lstrip("@") for h in header]
    hilang = [k for k in KOLOM if k not in header]
    if hilang:
        sys.exit(f"ERROR: kolom tidak ditemukan: {', '.join(hilang)}. Header terbaca: {header}")
    idx = {k: header.index(k) for k in KOLOM}

    error, warn, info = [], [], []
    data = []
    jumlah_dirapikan = 0
    for n, r in enumerate(rows, start=2):
        r = r + [""] * (len(header) - len(r))
        rec = {}
        for k in KOLOM:
            asli = r[idx[k]]
            bersih = rapikan(asli)
            jumlah_dirapikan += asli != bersih
            rec[k] = bersih
        rec["_baris"] = n
        data.append(rec)

    if a.nomor_otomatis:
        for i, rec in enumerate(data, start=1):
            if not rec["No"]:
                rec["No"] = str(i)
        info.append("Kolom No yang kosong diisi otomatis berdasarkan urutan baris.")

    nim_count = Counter(d["NIM"] for d in data if d["NIM"])
    nama_count = Counter(d["Nama"].casefold() for d in data if d["Nama"])
    pemisah_ipk = set()

    for d in data:
        lok = f"baris {d['_baris']} ({d['NIM'] or 'tanpa NIM'})"
        for k in KOLOM:
            if not d[k]:
                error.append(f"{lok}: kolom {k} kosong")
        if d["NIM"] and nim_count[d["NIM"]] > 1:
            error.append(f"{lok}: NIM duplikat")
        if d["Nama"] and nama_count[d["Nama"].casefold()] > 1:
            warn.append(f"{lok}: nama sama dengan wisudawan lain ({d['Nama']}) — pastikan memang orang berbeda")
        if d["No"] and not d["No"].isdigit():
            warn.append(f"{lok}: No bukan angka ({d['No']})")
        if d["IPK"]:
            v = parse_ipk(d["IPK"])
            if v is None or not 0 <= v <= 4:
                error.append(f"{lok}: IPK tidak valid ({d['IPK']})")
            else:
                pemisah_ipk.add("," if "," in d["IPK"] else ".")
                if not re.fullmatch(r"\d[.,]\d{2}", d["IPK"]):
                    warn.append(f"{lok}: IPK tidak dua desimal ({d['IPK']})")
        if len(d["Judul"]) > BATAS_JUDUL:
            warn.append(f"{lok}: judul {len(d['Judul'])} karakter (> {BATAS_JUDUL}) — cek overset di InDesign")
        if len(d["Nama"]) > BATAS_NAMA:
            warn.append(f"{lok}: nama {len(d['Nama'])} karakter — cek pemenggalan baris")
        for k in KOLOM:
            if d[k].startswith('"'):
                warn.append(f"{lok}: kolom {k} diawali tanda kutip; bisa salah terbaca Data Merge")
        if "DUMMY" in d["Nama"].upper() or "DUMMY" in d["NIM"].upper():
            warn.append(f"{lok}: data DUMMY — hanya untuk uji layout, bukan publikasi")

        nama_file = PureWindowsPath(d["Foto"]).name if d["Foto"] else ""
        if nama_file and d["NIM"] and d["NIM"] not in nama_file:
            warn.append(f"{lok}: nama file foto ({nama_file}) tidak memuat NIM — rawan tertukar")
        d["_foto_file"] = nama_file
        if a.foto_dir:
            p = cari_foto(a.foto_dir, nama_file, d["NIM"]) if a.foto_dir.is_dir() else None
            if p is None:
                error.append(f"{lok}: foto tidak ditemukan di {a.foto_dir}")
            else:
                d["_foto_file"] = p.name
                d["_foto_path"] = p.resolve()
                sz = ukuran_foto(p)
                if sz:
                    w, h = sz
                    if w < MIN_PX[0] or h < MIN_PX[1]:
                        error.append(f"{lok}: foto {w}×{h}px terlalu kecil (min {MIN_PX[0]}×{MIN_PX[1]})")
                    elif w < SARAN_PX[0] or h < SARAN_PX[1]:
                        warn.append(f"{lok}: foto {w}×{h}px di bawah saran {SARAN_PX[0]}×{SARAN_PX[1]}")
                    if abs(w / h - 0.75) > 0.05:
                        info.append(f"{lok}: rasio foto {w}×{h} bukan 3:4 — akan di-crop otomatis oleh frame")

    if a.foto_dir and not a.foto_dir.is_dir():
        error.append(f"Folder foto tidak ada: {a.foto_dir}")
    if len(pemisah_ipk) > 1:
        warn.append("IPK memakai campuran koma dan titik — seragamkan (mis. 3,75)")
    if jumlah_dirapikan:
        info.append(f"{jumlah_dirapikan} sel dirapikan (spasi ganda/tab/enter/spasi tepi) di keluaran.")

    terpanjang = sorted(data, key=lambda d: len(d["Judul"]), reverse=True)[:5]
    predikat = Counter(d["Predikat"] for d in data)

    lap = [
        f"Laporan validasi: {a.masukan} (encoding: {enc})",
        f"Jumlah record: {len(data)} -> {-(-len(data) // 4)} halaman direktori (4 per halaman)",
        f"ERROR: {len(error)}  WARNING: {len(warn)}  INFO: {len(info)}",
        "",
        *[f"ERROR   {e}" for e in error],
        *[f"WARNING {w}" for w in warn],
        *[f"INFO    {i}" for i in info],
        "",
        "Nilai Predikat (cek konsistensi penulisan):",
        *[f"  {v!r}: {c}" for v, c in predikat.most_common()],
        "",
        "5 judul terpanjang (pakai untuk uji layout):",
        *[f"  {len(d['Judul'])} kar — baris {d['_baris']} — {d['NIM']}" for d in terpanjang],
    ]
    teks_lap = "\n".join(lap)
    print(teks_lap)

    if not a.out:
        print("\n(Tidak ada --out: keluaran tidak ditulis.)")
        return 1 if error else 0
    if error and not a.paksa:
        print("\nKeluaran TIDAK ditulis karena ada ERROR. Perbaiki data, atau pakai --paksa untuk uji layout saja.")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        Path(f"{a.out}-laporan.txt").write_text(teks_lap, encoding="utf-8")
        return 1

    a.out.parent.mkdir(parents=True, exist_ok=True)

    def path_foto(d):
        if a.foto_base:
            return str(PureWindowsPath(a.foto_base) / d["_foto_file"])
        if d.get("_foto_path"):
            return str(d["_foto_path"])
        return d["Foto"]

    hdr = KOLOM[:-1] + ["@Foto"]
    isi = [[d[k] for k in KOLOM[:-1]] + [path_foto(d)] for d in data]

    # InDesign Data Merge: UTF-16 + tab paling aman untuk huruf/tanda baca non-ASCII
    with open(f"{a.out}-datamerge.txt", "w", encoding="utf-16", newline="") as f:
        for r in [hdr] + isi:
            f.write("\t".join(r) + "\r\n")
    with open(f"{a.out}-cek.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows([hdr] + isi)
    Path(f"{a.out}-laporan.txt").write_text(teks_lap, encoding="utf-8")
    print(f"\nDitulis: {a.out}-datamerge.txt, {a.out}-cek.csv, {a.out}-laporan.txt")
    return 1 if error else 0


if __name__ == "__main__":
    sys.exit(main())
