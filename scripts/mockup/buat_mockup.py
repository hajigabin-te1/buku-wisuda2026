#!/usr/bin/env python3
"""Render mockup KONSEP (bukan file cetak) Buku Wisuda STIA Amuntai 2026.

Membuat HTML berukuran A5 dari data DUMMY dan placeholder, lalu merendernya ke
PNG, satu PDF gabungan, dan satu lembar ringkasan (contact sheet) di
06-Proof/konsep/ memakai Playwright + Chromium.
Prasyarat: Python 3, Pillow, Node.js dengan paket `playwright`, akses internet
(Google Fonts). Jalankan dari root repo: python scripts/mockup/buat_mockup.py

Naskah resmi (kata pengantar, sambutan, mars, hymne, visi-misi, nama pimpinan)
BELUM tersedia, jadi digambar sebagai balok placeholder — bukan teks karangan.
"""

import csv
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "03-Data/CSV-DataMerge/DUMMY-contoh-wisudawan.csv"
OUT = ROOT / "06-Proof/konsep"

# Spesifikasi percetakan (dikonfirmasi): A5, margin atas 12, bawah 15, dalam 18, luar 12
W, H = 148, 210
M_ATAS, M_BAWAH, M_DALAM, M_LUAR = 12, 15, 18, 12
KARTU_L, KARTU_T, JARAK, DIR_ATAS = 56.5, 82, 5, 26

FONTS = ("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800"
         "&family=Source+Sans+3:wght@400;600&family=Playfair+Display:ital,wght@1,400;1,600&display=swap")

CSS = """
:root{--p:#EBF8FF;--s:#3081DB;--a:#FFE031;--ink:#12355E}
*{box-sizing:border-box;margin:0;padding:0}
.page{width:148mm;height:210mm;position:relative;overflow:hidden;background:var(--p);
  font-family:'Source Sans 3',sans-serif;color:var(--ink)}
.abs{position:absolute}
.blob{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 40%,rgba(48,129,219,.28),rgba(48,129,219,0) 70%)}
.grid{position:absolute;inset:0;background-image:radial-gradient(rgba(48,129,219,.18) .25mm,transparent .3mm);
  background-size:5mm 5mm;-webkit-mask-image:linear-gradient(160deg,#000 0%,transparent 45%)}
.hair{position:absolute;height:.1mm;background:rgba(48,129,219,.5)}
.glass{background:linear-gradient(135deg,rgba(255,255,255,.85),rgba(255,255,255,.55));
  border:.18mm solid rgba(255,255,255,.95);box-shadow:0 .8mm 2.5mm rgba(48,129,219,.15);
  backdrop-filter:blur(2mm);-webkit-backdrop-filter:blur(2mm)}
.ring{position:absolute;border-radius:50%;border:.25mm solid rgba(48,129,219,.35)}
.folio{position:absolute;bottom:6mm;left:0;right:0;text-align:center;font:500 8pt Montserrat;color:var(--s)}
.folio:before,.folio:after{content:'';display:inline-block;width:6mm;height:.15mm;background:var(--s);opacity:.5;vertical-align:middle;margin:0 2.5mm}
.watermark{position:absolute;left:0;right:0;bottom:1.5mm;text-align:center;font:600 5pt Montserrat;letter-spacing:.4mm;color:#c0392b;opacity:.8}
.jilid{position:absolute;top:0;bottom:0;width:4mm;display:flex;align-items:center;justify-content:center}
.jilid span{writing-mode:vertical-rl;font:600 4.5pt Montserrat;letter-spacing:.5mm;color:#c0392b;opacity:.7}
.catatan{position:absolute;font:600 5pt Montserrat;letter-spacing:.3mm;color:#c0392b}
/* direktori */
.header{position:absolute;top:12mm;height:10mm;border-radius:2mm;
  background:linear-gradient(120deg,rgba(48,129,219,.95),rgba(48,129,219,.78));box-shadow:0 .8mm 2.5mm rgba(48,129,219,.25);
  display:flex;align-items:center;justify-content:center;font:700 8.5pt/11pt Montserrat;letter-spacing:.45mm;
  text-transform:uppercase;color:#fff;overflow:hidden;white-space:nowrap}
.header:after{content:'';position:absolute;right:6mm;top:0;bottom:0;width:14mm;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.25),transparent)}
.header i{display:inline-block;width:2mm;height:2mm;background:var(--a);border-radius:.5mm;transform:rotate(45deg);margin:0 3mm}
.card{position:absolute;border-radius:3mm}
.foto{position:absolute;border-radius:2mm;border:.35mm solid #fff;overflow:hidden;
  background:linear-gradient(160deg,#d6ecfb,#b9daf5);display:flex;align-items:flex-end;justify-content:center}
.foto svg{width:80%}
.foto span{position:absolute;top:1mm;left:0;right:0;text-align:center;font:600 4.5pt Montserrat;color:var(--s);opacity:.8}
.no{position:absolute;height:4.5mm;min-width:8mm;border-radius:1.5mm;background:var(--a);
  font:700 7pt/4.5mm Montserrat;text-align:center;color:var(--ink)}
.nama{font:600 8.5pt/10pt Montserrat;margin-bottom:1mm;hyphens:none}
.data{font:400 7.5pt/9pt 'Source Sans 3'}
.lbl{font:600 5.5pt 'Source Sans 3';letter-spacing:.15mm;text-transform:uppercase;color:var(--s);margin-right:.8mm}
.ipk{position:absolute;height:5mm;border-radius:1.5mm;background:rgba(255,224,49,.3);border:.18mm solid var(--a);
  font:600 7.5pt/4.7mm 'Source Sans 3';padding:0 2mm;white-space:nowrap;overflow:hidden}
.judul{position:absolute;font:400 8pt/10pt 'Source Sans 3';hyphens:none}
.judul .lbl{display:block;font-size:5.5pt;line-height:7pt;margin-bottom:.5mm}
.accent{position:absolute;width:.6mm;border-radius:.3mm;background:var(--a)}
/* editorial */
.kicker{font:600 6.5pt Montserrat;letter-spacing:.8mm;text-transform:uppercase;color:var(--s)}
.h1{font:700 18pt/22pt Montserrat;color:var(--s)}
.puitis{font-family:'Playfair Display',serif;font-style:italic;color:var(--s)}
.ph{position:absolute;border:.3mm dashed rgba(48,129,219,.7);border-radius:2mm;display:flex;align-items:center;
  justify-content:center;text-align:center;font:600 5.5pt/7pt Montserrat;color:var(--s);background:rgba(255,255,255,.35);padding:1mm}
.bar{height:2.2mm;border-radius:1.1mm;background:rgba(18,53,94,.13);margin-bottom:2.1mm}
.bar.c{margin-left:auto;margin-right:auto}
.tag{display:inline-block;font:600 5pt Montserrat;letter-spacing:.3mm;color:#c0392b;border:.2mm solid rgba(192,57,43,.5);
  border-radius:1mm;padding:.4mm 1.2mm;background:rgba(255,255,255,.6)}
"""

SILUET = ('<svg viewBox="0 0 60 70"><circle cx="30" cy="24" r="13" fill="#fff" opacity=".85"/>'
          '<path d="M4 70c2-18 13-26 26-26s24 8 26 26z" fill="#fff" opacity=".85"/></svg>')
WM = '<div class="watermark">KONSEP · DATA DUMMY / PLACEHOLDER · BUKAN FILE CETAK</div>'
NASKAH = '<span class="tag">PLACEHOLDER — MENUNGGU NASKAH RESMI</span>'


def e(t):
    return html.escape(t)


def kiri_kanan(sisi):
    """Margin kiri & kanan halaman: halaman kanan (R) jilid di kiri, halaman kiri (L) jilid di kanan."""
    return (M_DALAM, M_LUAR) if sisi == "R" else (M_LUAR, M_DALAM)


def halaman(sisi, isi, folio=None, latar=True, extra_latar="", style=""):
    ml, mr = kiri_kanan(sisi)
    flip = "right:-35mm" if sisi == "R" else "left:-35mm"
    flip2 = "left:-30mm" if sisi == "R" else "right:-30mm"
    bg = ('<div class="grid"></div>'
          f'<div class="blob" style="width:90mm;height:90mm;{flip};top:-30mm"></div>'
          f'<div class="blob" style="width:70mm;height:70mm;{flip2};bottom:-25mm;opacity:.7"></div>') if latar else ""
    jilid = ("left:0" if sisi == "R" else "right:0")
    f = f'<div class="folio" style="left:{ml}mm;right:{mr}mm">{folio}</div>' if folio else ""
    return (f'<section class="page" style="{style}">{bg}{extra_latar}{isi}{f}'
            f'<div class="jilid" style="{jilid}"><span>SISI JILID</span></div>{WM}</section>')


def bars(widths, center=False):
    c = " c" if center else ""
    return "".join(f'<div class="bar{c}" style="width:{w}%"></div>' for w in widths)


def foto(top, left, w, h, label="FOTO DUMMY 3:4"):
    return (f'<div class="foto" style="top:{top}mm;left:{left}mm;width:{w}mm;height:{h}mm">'
            f'<span>{label}</span>{SILUET}</div>')


# ---------- direktori ----------
def kartu_a(d, x, y):
    r = KARTU_L - 3  # tepi kanan isi kartu
    return f'''<div class="card glass" style="left:{x}mm;top:{y}mm;width:{KARTU_L}mm;height:{KARTU_T}mm">
  {foto(3, 3, 22, 29.3)}
  <div class="no" style="top:3mm;left:28mm">{int(d["No"]):02d}</div>
  <div class="abs" style="top:8.5mm;left:28mm;width:{r - 28}mm">
    <div class="nama">{e(d["Nama"])}</div>
    <div class="data"><span class="lbl">NIM</span>{e(d["NIM"])}</div>
    <div class="data"><span class="lbl">TTL</span>{e(d["TTL"])}</div>
  </div>
  <div class="ipk" style="top:37mm;left:3mm;width:{r - 3}mm"><span class="lbl">IPK</span>{e(d["IPK"])} &nbsp;·&nbsp; {e(d["Predikat"])}</div>
  <div class="accent" style="top:45.5mm;left:3mm;height:5mm"></div>
  <div class="judul" style="top:45mm;left:5mm;width:{r - 5}mm;height:34mm"><span class="lbl">Judul Skripsi</span>{e(d["Judul"])}</div>
</div>'''


def direktori(rows, sisi, prodi, folio, catatan):
    ml, mr = kiri_kanan(sisi)
    xs = [ml, ml + KARTU_L + JARAK]
    ys = [DIR_ATAS, DIR_ATAS + KARTU_T + JARAK]
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[0], ys[1]), (xs[1], ys[1])]
    cards = "".join(kartu_a(d, x, y) for d, (x, y) in zip(rows, pos))
    isi = (f'<div class="header" style="left:{ml}mm;right:{mr}mm">Wisudawan <i></i> {e(prodi)}</div>{cards}'
           f'<div class="catatan" style="top:197.5mm;left:{ml}mm">{e(catatan)}</div>')
    return halaman(sisi, isi, folio)


# ---------- cover & editorial ----------
def cover_1():
    isi = f'''
<div class="hair" style="top:20mm;left:{M_DALAM}mm;width:40mm"></div>
<div class="ph" style="top:26mm;left:{M_DALAM}mm;width:16mm;height:16mm;border-radius:50%">LOGO<br>RESMI</div>
<div class="abs kicker" style="top:30mm;left:{M_DALAM + 20}mm">Buku Wisuda</div>
<div class="abs" style="top:34mm;left:{M_DALAM + 20}mm;font:600 7pt Montserrat">Sekolah Tinggi Ilmu Administrasi (STIA) Amuntai</div>
<div class="glass abs" style="top:52mm;left:22mm;width:112mm;height:96mm;border-radius:5mm;transform:rotate(-4deg);opacity:.6"></div>
<div class="glass abs" style="top:56mm;left:18mm;width:118mm;height:90mm;border-radius:5mm;padding:3mm">
  <div class="ph" style="position:relative;width:100%;height:100%">FOTO GRUP RESMI<br>(placeholder — dari 02-Aset-Resmi/Foto-Grup)</div>
</div>
<div class="abs" style="top:132mm;left:96mm;width:40mm;height:22mm;border-radius:3mm;background:linear-gradient(135deg,rgba(48,129,219,.95),rgba(48,129,219,.7));
  box-shadow:0 1mm 3mm rgba(48,129,219,.35);display:flex;align-items:center;justify-content:center;font:800 18pt Montserrat;color:#fff;letter-spacing:.6mm">2026</div>
<div class="abs puitis" style="top:156mm;left:{M_DALAM}mm;font-size:34pt;line-height:36pt">Untukmu<br>Cinta</div>
<div class="abs" style="top:194mm;left:{M_DALAM}mm;width:22mm;height:.8mm;background:var(--a);border-radius:.4mm"></div>
<div class="catatan" style="top:4mm;right:4mm">COVER OPSI 1 — FOTO GRUP DALAM PANEL KACA</div>'''
    return halaman("R", isi, style="background:linear-gradient(170deg,#EBF8FF 0%,#d5ecfd 55%,#EBF8FF 100%)",
                   extra_latar='<div class="blob" style="width:120mm;height:120mm;left:20mm;top:60mm;opacity:.8"></div>')


def cover_2():
    cx, cy = 92, 92
    rings = "".join(f'<div class="ring" style="width:{d}mm;height:{d}mm;left:{cx - d / 2}mm;top:{cy - d / 2}mm;opacity:{o}"></div>'
                    for d, o in [(150, .5), (118, .7), (88, 1)])
    isi = f'''
<div class="abs" style="left:{cx - 44}mm;top:{cy - 44}mm;width:88mm;height:88mm;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.9),rgba(48,129,219,.35) 75%);box-shadow:0 2mm 6mm rgba(48,129,219,.25)"></div>
{rings}
<div class="glass abs" style="left:{M_DALAM}mm;top:104mm;width:{W - M_DALAM - M_LUAR}mm;height:56mm;border-radius:5mm"></div>
<div class="abs" style="left:{M_DALAM + 7}mm;top:112mm">
  <div class="kicker">Buku Wisuda · STIA Amuntai</div>
  <div class="puitis" style="font-size:38pt;line-height:40pt;margin-top:3mm">Untukmu Cinta</div>
  <div style="font:600 6.5pt Montserrat;letter-spacing:.5mm;text-transform:uppercase;margin-top:5mm;color:var(--ink)">
    Kenangan <span style="color:var(--a)">◆</span> Perjuangan <span style="color:var(--a)">◆</span> Harapan</div>
</div>
<div class="abs" style="left:{M_DALAM}mm;top:166mm;font:800 44pt/44pt Montserrat;color:transparent;-webkit-text-stroke:.35mm var(--s);letter-spacing:1mm">2026</div>
<div class="ph" style="top:{M_ATAS + 4}mm;left:{M_DALAM}mm;width:16mm;height:16mm;border-radius:50%">LOGO<br>RESMI</div>
<div class="abs" style="top:{M_ATAS + 9}mm;left:{M_DALAM + 20}mm;font:600 6.5pt/8pt Montserrat;width:60mm">Sekolah Tinggi Ilmu Administrasi<br>(STIA) Amuntai</div>
<div class="abs" style="top:186mm;right:{M_LUAR}mm;width:18mm;height:.8mm;background:var(--a);border-radius:.4mm"></div>
<div class="catatan" style="top:4mm;right:4mm">COVER OPSI 2 — TIPOGRAFIS, TANPA FOTO</div>'''
    return halaman("R", isi)


def cover_belakang():
    isi = f'''
<div class="ring" style="width:120mm;height:120mm;left:14mm;top:45mm"></div>
<div class="ring" style="width:90mm;height:90mm;left:29mm;top:60mm;opacity:.6"></div>
<div class="glass abs" style="left:34mm;top:80mm;width:80mm;height:50mm;border-radius:5mm;text-align:center;padding-top:9mm">
  <div class="puitis" style="font-size:16pt">Untukmu, cinta.</div>
  <div class="kicker" style="margin-top:4mm">Buku Wisuda 2026</div>
</div>
<div class="ph" style="top:172mm;left:66mm;width:16mm;height:16mm;border-radius:50%">LOGO<br>RESMI</div>
<div class="catatan" style="top:4mm;left:4mm">COVER BELAKANG — KONSEP</div>'''
    return halaman("L", isi)


def slogan():
    kata = ["kenangan", "perjuangan", "harapan"]
    dots = '<span style="display:inline-block;width:1.6mm;height:1.6mm;background:var(--a);transform:rotate(45deg);margin:0 3mm;vertical-align:middle"></span>'
    isi = f'''
<div class="glass abs" style="top:72mm;left:{M_DALAM}mm;width:{W - M_DALAM - M_LUAR}mm;height:62mm;border-radius:5mm"></div>
<div class="abs" style="top:82mm;left:{M_DALAM}mm;width:{W - M_DALAM - M_LUAR}mm;text-align:center">
  <div class="kicker">Untukmu Cinta · 2026</div>
  <div class="puitis" style="font-size:16pt;line-height:23pt;margin:9mm 9mm 8mm">Merangkai kenangan, menuntaskan perjuangan, menjemput harapan.</div>
  <div style="font:600 7pt Montserrat;letter-spacing:.6mm;text-transform:uppercase">{dots.join(kata)}</div>
</div>'''
    return halaman("R", isi, extra_latar='<div class="blob" style="width:100mm;height:100mm;left:28mm;top:55mm"></div>')


def judul_bab(sisi, kicker, judul, top=24):
    ml, _ = kiri_kanan(sisi)
    return (f'<div class="hair" style="top:{top}mm;left:{ml}mm;width:24mm"></div>'
            f'<div class="abs kicker" style="top:{top + 3}mm;left:{ml}mm">{kicker}</div>'
            f'<div class="abs h1" style="top:{top + 8}mm;left:{ml}mm;width:110mm">{judul}</div>')


def kata_pengantar():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    isi = judul_bab("L", "Pengantar", "Kata Pengantar") + f'''
<div class="abs" style="top:52mm;left:{ml}mm;width:{lebar}mm">{NASKAH}</div>
<div class="abs" style="top:60mm;left:{ml}mm;width:{lebar}mm">
  {bars([100, 97, 99, 94, 100, 62])}<div style="height:2mm"></div>
  {bars([100, 98, 96, 100, 99, 93, 100, 48])}<div style="height:2mm"></div>
  {bars([98, 100, 95, 99, 71])}<div style="height:2mm"></div>
  {bars([100, 96, 99, 55])}
</div>
<div class="glass abs" style="top:158mm;left:{ml + lebar - 58}mm;width:58mm;height:22mm;border-radius:3mm;padding:3mm 4mm">
  <div class="lbl" style="display:block">Penanda tangan</div>
  <div style="font:600 7pt Montserrat;margin-top:1.5mm;color:var(--s)">[Nama &amp; gelar resmi]</div>
  <div style="font:400 7pt 'Source Sans 3'">[Jabatan]</div>
</div>
<div class="accent" style="top:60mm;left:{ml - 3}mm;height:16mm;width:.8mm"></div>'''
    return halaman("L", isi, folio=2)


def sambutan():
    ml, mr = kiri_kanan("R")
    lebar = W - ml - mr
    isi = judul_bab("R", "Sambutan", "Sambutan Ketua<br>STIA Amuntai") + f'''
<div class="glass abs" style="top:62mm;left:{ml}mm;width:38mm;height:48mm;border-radius:4mm;padding:2.5mm">
  {foto(2.5, 2.5, 33, 43, "FOTO RESMI KETUA")}
</div>
<div class="abs" style="top:62mm;left:{ml + 43}mm;width:{lebar - 43}mm">{NASKAH}<div style="height:3mm"></div>
  {bars([100, 96, 100, 92, 99, 100, 95, 98, 60])}</div>
<div class="abs" style="top:116mm;left:{ml}mm;width:{lebar}mm">
  {bars([100, 98, 96, 100, 99, 93, 52])}<div style="height:2mm"></div>{bars([97, 100, 95, 68])}
</div>
<div class="abs" style="top:170mm;left:{ml}mm">
  <div class="lbl" style="display:block">Ketua STIA Amuntai</div>
  <div style="font:600 8pt Montserrat;color:var(--s);margin-top:1mm">[Nama &amp; gelar resmi]</div>
</div>'''
    return halaman("R", isi, folio=3)


def mars():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    bait = lambda ws: f'<div style="margin-bottom:6mm">{bars(ws, center=True)}</div>'
    isi = f'''
<div class="abs" style="top:24mm;left:{ml}mm;width:{lebar}mm;text-align:center">
  <div class="kicker">Lagu Resmi</div>
  <div class="h1" style="margin-top:2mm">Mars STIA</div>
  <div class="puitis" style="font-size:9pt;margin-top:1mm">Cipt. [nama pencipta resmi]</div>
  <div style="margin-top:4mm">{NASKAH}</div>
</div>
<div class="glass abs" style="top:62mm;left:{ml + 6}mm;width:{lebar - 12}mm;height:112mm;border-radius:5mm;padding:9mm 10mm">
  {bait([70, 78, 66, 74])}{bait([80, 64, 76, 70])}<div class="lbl" style="display:block;text-align:center;margin-bottom:3mm">Reff.</div>{bait([72, 82, 68, 60])}
</div>
<div class="abs" style="top:64mm;left:{ml + 2}mm;font:800 40pt Montserrat;color:var(--a);opacity:.9">♪</div>
<div class="catatan" style="top:185mm;left:{ml}mm">Hymne STIA memakai tata letak yang sama di halaman berikutnya.</div>'''
    return halaman("L", isi, folio=4)


def pimpinan():
    ml, mr = kiri_kanan("R")
    lebar = W - ml - mr
    cw, gap = (lebar - 2 * 5) / 3, 5
    kartu = ""
    for r in range(3):
        for c in range(3):
            x, y = ml + c * (cw + gap), 56 + r * 44
            kartu += f'''<div class="card glass" style="left:{x}mm;top:{y}mm;width:{cw}mm;height:40mm">
  {foto(2.5, 2.5, cw - 5, 24, "FOTO RESMI")}
  <div class="abs" style="top:28.5mm;left:2.5mm;right:2.5mm;text-align:center">
    <div style="font:600 6.5pt/8pt Montserrat">[Nama &amp; gelar]</div>
    <div style="font:400 6pt/7.5pt 'Source Sans 3';color:var(--s)">[Jabatan]</div></div></div>'''
    isi = judul_bab("R", "Unsur Pimpinan", "Pimpinan<br>STIA Amuntai") + kartu + \
        f'<div class="catatan" style="top:189mm;left:{ml}mm">Pola yang sama untuk Yayasan Bakti Muslimin &amp; Senat; jumlah kartu mengikuti data resmi.</div>'
    return halaman("R", isi, folio=7)


def visi_misi():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    misi = "".join(f'''<div style="display:flex;gap:3mm;margin-bottom:3.5mm">
  <div class="no" style="position:static;flex:none">{i:02d}</div><div style="flex:1;padding-top:.8mm">{bars([100, 72 - i * 4])}</div></div>'''
                   for i in range(1, 6))
    isi = judul_bab("L", "Visi &amp; Misi", "STIA Amuntai") + f'''
<div class="abs" style="top:46mm;left:{ml}mm">{NASKAH}</div>
<div class="glass abs" style="top:54mm;left:{ml}mm;width:{lebar}mm;height:40mm;border-radius:5mm;padding:7mm 8mm;text-align:center">
  <div class="lbl" style="display:block;margin-bottom:4mm">Visi</div>
  <div class="puitis" style="font-size:11pt">“</div>{bars([88, 94, 70], center=True)}
</div>
<div class="abs" style="top:103mm;left:{ml}mm;width:{lebar}mm">
  <div class="lbl" style="display:block;margin-bottom:4mm">Misi</div>{misi}
</div>'''
    return halaman("L", isi, folio=10)


def pembatas():
    isi = f'''
<div class="ring" style="width:160mm;height:160mm;left:20mm;top:20mm"></div>
<div class="ring" style="width:120mm;height:120mm;left:40mm;top:40mm;opacity:.7"></div>
<div class="abs" style="left:58mm;top:58mm;width:84mm;height:84mm;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95),rgba(48,129,219,.45) 80%)"></div>
<div class="glass abs" style="left:{M_DALAM}mm;top:120mm;width:{W - M_DALAM - M_LUAR}mm;height:52mm;border-radius:5mm;padding:8mm 9mm">
  <div class="kicker">Daftar Wisudawan</div>
  <div class="h1" style="margin-top:3mm">Program Studi<br>Administrasi Bisnis</div>
  <div style="width:18mm;height:.8mm;background:var(--a);border-radius:.4mm;margin-top:5mm"></div>
</div>
<div class="catatan" style="top:4mm;right:4mm">PEMBATAS BAB — MASTER C (TANPA NOMOR)</div>'''
    return halaman("R", isi)


def kenangan():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    def ph(t, l, w, h):
        return (f'<div class="glass abs" style="top:{t}mm;left:{l}mm;width:{w}mm;height:{h}mm;border-radius:4mm;padding:2mm">'
                f'<div class="ph" style="position:relative;width:100%;height:100%">FOTO KENANGAN<br>(resmi)</div></div>')
    isi = judul_bab("L", "Kenangan", "Foto Kenangan", top=18) + \
        ph(46, ml, lebar, 62) + ph(114, ml, lebar * .55, 66) + ph(114, ml + lebar * .55 + 4, lebar * .45 - 4, 31) + \
        ph(149, ml + lebar * .55 + 4, lebar * .45 - 4, 31) + \
        f'<div class="catatan" style="top:186mm;left:{ml}mm">4 halaman; komposisi bingkai bervariasi per halaman.</div>'
    return halaman("L", isi, folio=86)


def penutup():
    ml, mr = kiri_kanan("R")
    isi = judul_bab("R", "Penutup", 'Pada Akhirnya,<br><span class="puitis" style="font-weight:400">Untukmu Cinta</span>', top=30) + f'''
<div class="glass abs" style="top:78mm;left:{ml}mm;width:{W - ml - mr}mm;padding:8mm 9mm;border-radius:4mm;font:400 10pt/15pt 'Source Sans 3'">
  <p>Di antara kenangan yang kita simpan, perjuangan yang kita tuntaskan, dan harapan yang kita titipkan pada masa depan, ada cinta yang senantiasa menjadi alasan untuk terus melangkah.</p>
  <p style="margin-top:4mm;font-weight:600">Sebab pada akhirnya, kenangan akan tinggal, perjuangan akan bermakna, dan harapan akan menemukan jalannya.</p>
  <p class="puitis" style="margin-top:6mm;font-size:13pt;text-align:right">Untukmu, cinta.</p>
</div>
<div class="accent" style="top:86mm;left:{ml}mm;height:12mm;width:.8mm"></div>'''
    return halaman("R", isi, folio=89)


def main():
    with open(DATA, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    prodi = "Program Studi Administrasi Bisnis"
    pages = {
        "01-cover-opsi-1": cover_1(),
        "02-cover-opsi-2": cover_2(),
        "03-slogan": slogan(),
        "04-kata-pengantar": kata_pengantar(),
        "05-sambutan-ketua": sambutan(),
        "06-mars": mars(),
        "07-unsur-pimpinan": pimpinan(),
        "08-visi-misi": visi_misi(),
        "09-pembatas-direktori": pembatas(),
        "10-direktori-kanan": direktori([rows[0], rows[1], rows[2], rows[4]], "R", prodi, 17,
                                        "HALAMAN KANAN — jilid di kiri (18 mm)"),
        "11-direktori-kiri": direktori([rows[3], rows[5], rows[1], rows[0]], "L", prodi, 18,
                                       "HALAMAN KIRI — jilid di kanan (18 mm)"),
        "12-foto-kenangan": kenangan(),
        "13-penutup": penutup(),
        "14-cover-belakang": cover_belakang(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "src"
    src.mkdir(exist_ok=True)
    for old in list(OUT.glob("*.png")) + list(src.glob("*.html")):
        old.unlink()
    for name, body in pages.items():
        (src / f"{name}.html").write_text(
            f'<!doctype html><html lang="id"><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")

    js = r"""
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out, ...names] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 3, viewport: { width: 600, height: 900 } });
  for (const n of names) {
    await p.goto('file://' + path.join(src, n + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.locator('.page').screenshot({ path: path.join(out, n + '.png') });
  }
  await b.close();
})();
"""
    js_path = src / "_render.js"
    js_path.write_text(js, encoding="utf-8")
    subprocess.run(["node", str(js_path), str(src), str(OUT), *pages], check=True)
    js_path.unlink()

    from PIL import Image, ImageDraw
    imgs = [Image.open(OUT / f"{n}.png").convert("RGB") for n in pages]
    imgs[0].save(OUT / "KONSEP-Buku-Wisuda-2026.pdf", save_all=True, append_images=imgs[1:], resolution=287)

    # lembar ringkasan: semua halaman kecil dalam satu gambar
    tw, th, kol, pad = 420, 596, 5, 24
    baris = -(-len(imgs) // kol)
    sheet = Image.new("RGB", (kol * (tw + pad) + pad, baris * (th + pad + 28) + pad), "#dfe7ef")
    dr = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(zip(pages, imgs)):
        x, y = pad + (i % kol) * (tw + pad), pad + (i // kol) * (th + pad + 28)
        sheet.paste(im.resize((tw, th)), (x, y))
        dr.text((x, y + th + 6), n, fill="#12355E")
    sheet.save(OUT / "00-ringkasan.png")
    print("Mockup ditulis ke", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
