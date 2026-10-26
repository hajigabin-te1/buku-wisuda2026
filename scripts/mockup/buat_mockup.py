#!/usr/bin/env python3
"""Render mockup KONSEP (bukan file cetak) Buku Wisuda STIA Amuntai 2026.

Gaya visual mengikuti 01-Brief-Referensi/referensi.png (konsep v3):
latar biru muda, pecahan kaca diagonal biru-emas di sudut, judul sampul serif
kapital, tulisan script "Untukmu Cinta" dengan sapuan emas, kartu direktori
berikon dengan nomor emas di pojok foto.

Membuat HTML berukuran A5 dari data DUMMY dan placeholder, lalu merendernya ke
PNG, satu PDF gabungan, dan satu lembar ringkasan di 06-Proof/konsep/.
Prasyarat: Python 3, Pillow, Node.js dengan paket `playwright`, akses internet
(Google Fonts), dan aset dari scripts/aset/buat_aset_svg.py.
Jalankan dari root repo: python scripts/mockup/buat_mockup.py

Naskah resmi (kata pengantar, sambutan, mars, visi-misi, nama pimpinan) BELUM
tersedia, jadi digambar sebagai balok placeholder — bukan teks karangan.
"""

import csv
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "03-Data/CSV-DataMerge/DUMMY-contoh-wisudawan.csv"
OUT = ROOT / "06-Proof/konsep"
REL = "../../../"  # dari 06-Proof/konsep/src ke root repo
LOGO = REL + "02-Aset-Resmi/Logo/STIA.png"
ORN = REL + "05-InDesign/Links/ornamen/"
IKON = ROOT / "05-InDesign/Links/ikon"

# Spesifikasi percetakan (dikonfirmasi): A5, margin atas 12, bawah 15, dalam 18, luar 12
W, H = 148, 210
M_ATAS, M_BAWAH, M_DALAM, M_LUAR = 12, 15, 18, 12
KARTU_L, KARTU_T, JARAK, DIR_ATAS = 56.5, 81, 5, 27

FONTS = ("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800"
         "&family=Source+Sans+3:wght@400;600&family=Playfair+Display:ital,wght@1,400;1,600"
         "&family=Cinzel:wght@600;700&family=Satisfy&display=swap")

CSS = """
:root{--p:#EBF8FF;--s:#3081DB;--a:#FFE031;--ink:#12355E}
*{box-sizing:border-box;margin:0;padding:0}
.page{width:148mm;height:210mm;position:relative;overflow:hidden;
  background:radial-gradient(ellipse 90mm 60mm at 30% 20%,rgba(255,255,255,.9),transparent 70%),
             radial-gradient(ellipse 80mm 50mm at 80% 75%,rgba(255,255,255,.6),transparent 70%),
             linear-gradient(165deg,#f4fbff 0%,var(--p) 45%,#dcefff 100%);
  font-family:'Source Sans 3',sans-serif;color:var(--ink)}
.abs{position:absolute}
.orn{position:absolute;width:62mm;height:62mm}
.folio{position:absolute;bottom:6mm;text-align:center;font:600 7.5pt Montserrat;color:var(--s)}
.watermark{position:absolute;left:0;right:0;bottom:1.5mm;text-align:center;font:600 5pt Montserrat;letter-spacing:.4mm;color:#c0392b;opacity:.8}
.jilid{position:absolute;top:0;bottom:0;width:4mm;display:flex;align-items:center;justify-content:center}
.jilid span{writing-mode:vertical-rl;font:600 4.5pt Montserrat;letter-spacing:.5mm;color:#c0392b;opacity:.7}
.catatan{position:absolute;font:600 5pt Montserrat;letter-spacing:.3mm;color:#c0392b}
.glass{background:linear-gradient(135deg,rgba(255,255,255,.88),rgba(255,255,255,.6));
  border:.2mm solid rgba(48,129,219,.28);box-shadow:0 .6mm 2mm rgba(48,129,219,.12)}
/* judul bagian ala referensi */
.sec-t{font:700 12.5pt/14pt Montserrat;letter-spacing:.45mm;text-transform:uppercase;color:var(--s)}
.sec-s{font:600 6.5pt Montserrat;letter-spacing:.55mm;text-transform:uppercase;color:var(--s);opacity:.85;margin-top:1.2mm}
.sec-line{position:absolute;height:.15mm;background:rgba(48,129,219,.35)}
.sec-line i{position:absolute;right:0;top:-.25mm;height:.65mm;width:38%;background:var(--a);border-radius:.3mm}
.sec-line b{position:absolute;right:-1mm;top:-.55mm;width:1.2mm;height:1.2mm;border-radius:50%;background:var(--s)}
.script{font-family:Satisfy,cursive;color:var(--s);line-height:1}
.serif{font-family:Cinzel,serif;color:var(--s)}
.puitis{font-family:'Playfair Display',serif;font-style:italic;color:var(--s)}
.ph{position:absolute;border:.3mm dashed rgba(48,129,219,.6);border-radius:2mm;display:flex;align-items:center;
  justify-content:center;text-align:center;font:600 5.5pt/7pt Montserrat;color:var(--s);background:rgba(255,255,255,.35);padding:1mm}
.bar{height:2.2mm;border-radius:1.1mm;background:rgba(18,53,94,.12);margin-bottom:2.1mm}
.bar.c{margin-left:auto;margin-right:auto}
.tag{display:inline-block;font:600 5pt Montserrat;letter-spacing:.3mm;color:#c0392b;border:.2mm solid rgba(192,57,43,.5);
  border-radius:1mm;padding:.4mm 1.2mm;background:rgba(255,255,255,.6)}
/* kartu direktori */
.card{position:absolute;border-radius:3mm}
.foto{position:absolute;border-radius:2mm;overflow:hidden;
  background:linear-gradient(160deg,#cfe7fb,#a9d0f3);display:flex;align-items:flex-end;justify-content:center}
.foto svg{width:80%}
.foto span{position:absolute;top:1mm;left:0;right:0;text-align:center;font:600 4.5pt Montserrat;color:var(--s);opacity:.8}
.badge{position:absolute;height:4.6mm;min-width:7.5mm;padding:0 1mm;border-radius:1.6mm;background:var(--a);
  font:700 7pt/4.6mm Montserrat;text-align:center;color:var(--ink);box-shadow:0 .3mm .8mm rgba(0,0,0,.12)}
.lab{display:flex;gap:1mm;align-items:center;font:600 6pt/3mm 'Source Sans 3';color:var(--s);margin-bottom:.3mm;white-space:nowrap}
.lab img{width:2.8mm;height:2.8mm;flex:none}
.val{font:400 7.5pt/9pt 'Source Sans 3';color:var(--ink)}
.val.nama{font:600 8pt/9.5pt Montserrat}
.judul .val{font:400 8pt/10pt 'Source Sans 3';hyphens:none}
"""

SILUET = ('<svg viewBox="0 0 60 70"><circle cx="30" cy="24" r="13" fill="#fff" opacity=".85"/>'
          '<path d="M4 70c2-18 13-26 26-26s24 8 26 26z" fill="#fff" opacity=".85"/></svg>')
WM = '<div class="watermark">KONSEP v3 · MENGIKUTI REFERENSI · DATA DUMMY / PLACEHOLDER · BUKAN FILE CETAK</div>'
NASKAH = '<span class="tag">PLACEHOLDER — MENUNGGU NASKAH RESMI</span>'


def e(t):
    return html.escape(t)


def ikon(nama):
    return f'<img src="{REL}05-InDesign/Links/ikon/ikon-{nama}.svg">'


def kiri_kanan(sisi):
    """Halaman kanan (R): jilid di kiri. Halaman kiri (L): jilid di kanan."""
    return (M_DALAM, M_LUAR) if sisi == "R" else (M_LUAR, M_DALAM)


def orn(pos, size=62, opacity=1):
    """Ornamen pecahan kaca di sudut: br, tr, bl, tl."""
    tf = {"br": "", "tr": "transform:scaleY(-1);", "bl": "transform:scaleX(-1);", "tl": "transform:scale(-1,-1);"}[pos]
    v = "bottom:-3mm" if pos[0] == "b" else "top:-3mm"
    h = "right:-3mm" if pos[1] == "r" else "left:-3mm"
    return f'<img class="orn" src="{ORN}ornamen-sudut.svg" style="{v};{h};width:{size}mm;height:{size}mm;{tf}opacity:{opacity}">'


def halaman(sisi, isi, folio=None, sudut=("br",), style=""):
    ml, mr = kiri_kanan(sisi)
    # ornamen utama di sisi luar halaman
    luar = "r" if sisi == "R" else "l"
    o = "".join(orn(s[0] + luar, *(s[1:] if len(s) > 1 else ())) if isinstance(s, tuple) else orn(s[0] + luar)
                for s in sudut)
    jilid = "left:0" if sisi == "R" else "right:0"
    f = f'<div class="folio" style="left:{ml}mm;right:{mr}mm">{folio}</div>' if folio else ""
    return (f'<section class="page" style="{style}">{o}{isi}{f}'
            f'<div class="jilid" style="{jilid}"><span>SISI JILID</span></div>{WM}</section>')


def judul_bagian(sisi, judul, sub, top=M_ATAS + 4, nomor=None):
    ml, mr = kiri_kanan(sisi)
    return (f'<div class="abs" style="top:{top}mm;left:{ml}mm;right:{mr}mm">'
            f'<div class="sec-t">{judul}</div><div class="sec-s">{sub}</div></div>'
            f'<div class="sec-line" style="top:{top + 10.5}mm;left:{ml}mm;right:{mr + 1}mm"><i></i><b></b></div>')


def bars(widths, center=False):
    c = " c" if center else ""
    return "".join(f'<div class="bar{c}" style="width:{w}%"></div>' for w in widths)


def foto(top, left, w, h, label="FOTO DUMMY 3:4"):
    return (f'<div class="foto" style="top:{top}mm;left:{left}mm;width:{w}mm;height:{h}mm">'
            f'<span>{label}</span>{SILUET}</div>')


def sapuan(top, left, w, rot=-4):
    return f'<img class="abs" src="{ORN}sapuan-emas.svg" style="top:{top}mm;left:{left}mm;width:{w}mm;transform:rotate({rot}deg)">'


# ---------- direktori ----------
def kartu(d, x, y):
    r = KARTU_L - 3
    kol = 28
    def lab(ik, lbl):
        return f'<div class="lab">{ikon(ik)}<span>{lbl}</span></div>'
    def mini(ik, lbl, val, w):
        return f'<div style="width:{w}mm">{lab(ik, lbl)}<div class="val">{e(val)}</div></div>'
    return f'''<div class="card glass" style="left:{x}mm;top:{y}mm;width:{KARTU_L}mm;height:{KARTU_T}mm">
  {foto(3, 3, 22, 29.3)}
  <div class="badge" style="top:2mm;left:20.5mm">{int(d["No"]):02d}</div>
  <div class="abs" style="top:3.5mm;left:{kol}mm;width:{r - kol}mm">
    {lab("nama", "Nama")}<div class="val nama" style="margin-bottom:1.2mm">{e(d["Nama"])}</div>
    {lab("ttl", "Tempat, Tgl. Lahir")}<div class="val">{e(d["TTL"])}</div>
  </div>
  <div class="abs" style="top:34.5mm;left:3mm;width:{r - 3}mm;display:flex;gap:1.5mm;padding-top:1.2mm;border-top:.15mm solid rgba(48,129,219,.22)">
    {mini("nim", "NIM", d["NIM"], 16)}{mini("ipk", "IPK", d["IPK"], 9.5)}{mini("predikat", "Predikat", d["Predikat"], 22)}
  </div>
  <div class="abs judul" style="top:46.5mm;left:3mm;width:{r - 3}mm">
    {lab("judul", "Judul Skripsi")}<div class="val" style="padding-left:3.8mm">{e(d["Judul"])}</div>
  </div>
</div>'''


def direktori(rows, sisi, prodi, folio, catatan):
    ml, mr = kiri_kanan(sisi)
    xs = [ml, ml + KARTU_L + JARAK]
    ys = [DIR_ATAS, DIR_ATAS + KARTU_T + JARAK]
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[0], ys[1]), (xs[1], ys[1])]
    cards = "".join(kartu(d, x, y) for d, (x, y) in zip(rows, pos))
    isi = (judul_bagian(sisi, "Daftar Wisudawan", f"{e(prodi)} · Wisuda 2026", top=M_ATAS) + cards +
           f'<div class="catatan" style="top:201mm;left:{ml}mm">{e(catatan)}</div>')
    return halaman(sisi, isi, folio, sudut=(("b", 40, .9),))


# ---------- sampul ----------
def sampul_depan():
    togas = "".join(f'<img class="abs" src="{ORN}toga.svg" style="top:{t}mm;left:{l}mm;width:{w}mm;transform:rotate({r}deg)">'
                    for t, l, w, r in [(86, 30, 9, -18), (92, 56, 7, 12), (84, 82, 8, -6), (94, 104, 7, 20), (80, 118, 6, -25)])
    isi = f'''
<img class="abs" src="{ORN}ornamen-tepi.svg" style="top:-3mm;left:3mm;height:216mm;width:10mm">
<img class="abs" src="{LOGO}" style="top:14mm;left:18mm;width:13mm">
<div class="abs" style="top:16.5mm;left:33mm;font:700 6pt/7.6pt Montserrat;letter-spacing:.2mm;color:var(--s)">SEKOLAH TINGGI ILMU<br>ADMINISTRASI (STIA) AMUNTAI</div>
<div class="abs" style="top:15mm;right:14mm;text-align:right;color:var(--s)">
  <div style="font:700 5.5pt Montserrat;letter-spacing:.4mm">WISUDA</div><div style="font:800 15pt/16pt Montserrat">2026</div></div>
<div class="abs serif" style="top:40mm;left:0;right:0;text-align:center">
  <div style="font-weight:600;font-size:27pt;line-height:28pt;letter-spacing:.6mm">UNTUKMU</div>
  <div style="font-weight:700;font-size:56pt;line-height:54pt;letter-spacing:1mm">CINTA</div></div>
<div class="abs" style="top:76mm;left:0;right:0;text-align:center;font:600 7.2pt/9.5pt Montserrat;color:var(--ink)">
  Merangkai kenangan, menuntaskan perjuangan,<br>menjemput harapan.</div>
{togas}
<div class="ph" style="top:100mm;left:16mm;width:120mm;height:80mm;border-radius:6mm;
  background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.65))">FOTO GRUP WISUDAWAN RESMI<br>(cutout PNG/PSD transparan, ≥ 300 ppi)<br>dari 02-Aset-Resmi/Foto-Grup</div>
<div class="abs" style="top:176mm;left:-5mm;width:160mm;height:30mm;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.85) 40%)"></div>
<div class="abs" style="top:181mm;left:18mm;font:700 6.2pt/8pt Montserrat;letter-spacing:.3mm;color:var(--s)">BUKU WISUDA<br>STIA AMUNTAI<br>TAHUN 2026</div>
<div class="abs" style="top:199mm;left:18mm;font:600 5.5pt Montserrat;letter-spacing:.6mm;color:var(--s)">KENANGAN &nbsp;•&nbsp; PERJUANGAN &nbsp;•&nbsp; HARAPAN</div>
<div class="catatan" style="top:4mm;right:4mm">SAMPUL DEPAN — dicetak terpisah (perfect binding)</div>'''
    return halaman("R", isi, sudut=(("b", 70), ("t", 46, .8)))


def sampul_belakang():
    isi = f'''
<img class="abs" src="{LOGO}" style="top:52mm;left:63mm;width:22mm">
<div class="abs" style="top:78mm;left:0;right:0;text-align:center;font:700 6.5pt/8.5pt Montserrat;letter-spacing:.3mm;color:var(--s)">SEKOLAH TINGGI ILMU<br>ADMINISTRASI (STIA) AMUNTAI</div>
<div class="ph" style="top:100mm;left:16mm;width:116mm;height:52mm;opacity:.8">FOTO GEDUNG KAMPUS RESMI (opsional)<br>dibuat pudar ±30% — hanya jika foto resmi tersedia</div>
<div class="abs script" style="top:158mm;left:0;right:0;text-align:center;font-size:24pt;transform:rotate(-4deg)">Untukmu, cinta.</div>
{sapuan(170, 50, 48)}
<div class="abs" style="top:192mm;left:{M_LUAR}mm;font:700 5.5pt/7pt Montserrat;letter-spacing:.3mm;color:var(--s)">STIA AMUNTAI<br>2026</div>
<div class="catatan" style="top:4mm;left:4mm">SAMPUL BELAKANG — dicetak terpisah</div>'''
    return halaman("L", isi, sudut=(("b", 60), ("t", 40, .7)))


def pembuka():
    isi = f'''
<div class="abs" style="top:24mm;left:{M_DALAM + 4}mm;font:700 6pt/8pt Montserrat;letter-spacing:.4mm;color:var(--s)">BUKU WISUDA 2026<br>STIA AMUNTAI</div>
<div class="abs script" style="top:62mm;left:26mm;font-size:52pt;transform:rotate(-10deg)">Untukmu</div>
<div class="abs script" style="top:84mm;left:48mm;font-size:52pt;transform:rotate(-10deg)">Cinta</div>
{sapuan(104, 46, 66, -9)}
<div class="abs" style="top:126mm;left:{M_DALAM}mm;right:{M_LUAR}mm;text-align:center;font:400 9pt/14pt 'Source Sans 3'">
  Merangkai kenangan, menuntaskan perjuangan,<br>menjemput harapan.</div>
<div class="abs" style="top:146mm;left:69mm;width:16mm;height:.3mm;background:var(--s);opacity:.6"></div>
<div class="abs" style="top:150mm;left:{M_DALAM}mm;right:{M_LUAR}mm;text-align:center;font:700 6.5pt/8.5pt Montserrat;letter-spacing:.4mm;color:var(--s)">STIA AMUNTAI<br>2026</div>
<div class="catatan" style="top:4mm;right:4mm">HALAMAN PEMBUKA (cover kedua: slogan tema)</div>'''
    return halaman("R", isi, sudut=(("b", 56), ("t", 40, .8)))


# ---------- editorial ----------
def daftar_isi():
    ml, mr = kiri_kanan("L")
    item = ["Kata Pengantar", "Mars & Hymne STIA", "Sambutan Ketua STIA Amuntai", "Unsur Yayasan, Pimpinan & Senat",
            "Visi & Misi", "Janji Wisudawan & Filosofi", "Daftar Wisudawan Administrasi Bisnis",
            "Daftar Wisudawan Administrasi Publik", "Foto Kenangan", "Penutup"]
    rows = "".join(f'''<div style="display:flex;align-items:center;gap:3mm;padding:2.1mm 0;border-bottom:.15mm solid rgba(48,129,219,.25)">
  <div style="width:4.6mm;height:4.6mm;border-radius:50%;background:var(--a);font:700 6.5pt/4.6mm Montserrat;text-align:center">{i}</div>
  <div style="flex:1;font:500 8pt Montserrat">{t}</div><div style="font:600 7.5pt Montserrat;color:var(--s)">…</div></div>'''
                   for i, t in enumerate(item, 1))
    isi = judul_bagian("L", "Daftar Isi", "Wisuda 2026", top=24) + f'''
<div class="abs" style="top:46mm;left:{ml}mm;right:{mr}mm">{rows}</div>
<div class="abs script" style="top:166mm;left:{ml + 4}mm;font-size:24pt;transform:rotate(-8deg)">Untukmu Cinta</div>
{sapuan(176, ml + 4, 46, -8)}
<div class="catatan" style="top:4mm;left:4mm">OPSIONAL — ada di referensi, belum ada di daftar isi brief</div>'''
    return halaman("L", isi, folio="i")


def sambutan():
    ml, mr = kiri_kanan("R")
    lebar = W - ml - mr
    isi = judul_bagian("R", "Sambutan", "Ketua STIA Amuntai", top=24) + f'''
<div class="abs" style="top:47mm;left:{ml}mm;width:38mm;height:48mm;border-radius:3mm;border:.6mm solid var(--a);transform:translate(1.5mm,1.5mm)"></div>
<div class="glass abs" style="top:47mm;left:{ml}mm;width:38mm;height:48mm;border-radius:3mm;padding:2mm">{foto(2, 2, 34, 44, "FOTO RESMI KETUA")}</div>
<div class="abs" style="top:44mm;left:{ml + 45}mm;font:700 30pt Montserrat;color:var(--a)">“</div>
<div class="abs" style="top:58mm;left:{ml + 45}mm;width:{lebar - 45}mm">{NASKAH}<div style="height:3mm"></div>{bars([96, 100, 88, 94, 60])}</div>
<div class="abs" style="top:104mm;left:{ml}mm;width:{lebar}mm">{bars([100, 97, 99, 94, 100, 62])}<div style="height:2mm"></div>{bars([98, 100, 95, 71])}</div>
<div class="abs" style="top:160mm;left:{ml}mm">
  <div style="font:700 7.5pt Montserrat;color:var(--ink)">[Nama &amp; gelar resmi]</div>
  <div style="font:400 7pt 'Source Sans 3';color:var(--s)">Ketua STIA Amuntai</div></div>'''
    return halaman("R", isi, folio=3, sudut=(("b", 44), ("t", 34, .8)))


def kata_pengantar():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    isi = judul_bagian("L", "Kata Pengantar", "Buku Wisuda 2026", top=24) + f'''
<div class="abs" style="top:46mm;left:{ml}mm">{NASKAH}</div>
<div class="abs" style="top:54mm;left:{ml}mm;width:{lebar}mm">
  {bars([100, 97, 99, 94, 100, 62])}<div style="height:2mm"></div>{bars([100, 98, 96, 100, 99, 93, 100, 48])}
  <div style="height:2mm"></div>{bars([98, 100, 95, 99, 71])}</div>
<div class="abs" style="top:150mm;right:{mr}mm;text-align:right">
  <div class="lbl" style="font:600 6pt 'Source Sans 3';color:var(--s)">Penanda tangan</div>
  <div style="font:700 7.5pt Montserrat">[Nama &amp; gelar resmi]</div><div style="font:400 7pt 'Source Sans 3'">[Jabatan]</div></div>'''
    return halaman("L", isi, folio=2, sudut=(("b", 44),))


def mars():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    bait = lambda ws: f'<div style="margin-bottom:6mm">{bars(ws, center=True)}</div>'
    isi = judul_bagian("L", "Mars STIA", "Lagu resmi · cipt. [nama pencipta resmi]", top=24) + f'''
<div class="abs" style="top:46mm;left:{ml}mm">{NASKAH}</div>
<div class="glass abs" style="top:56mm;left:{ml + 6}mm;width:{lebar - 12}mm;height:112mm;border-radius:4mm;padding:10mm">
  {bait([70, 78, 66, 74])}{bait([80, 64, 76, 70])}<div style="text-align:center;font:600 6pt 'Source Sans 3';color:var(--s);margin-bottom:3mm">Reff.</div>{bait([72, 82, 68, 60])}</div>
<div class="catatan" style="top:185mm;left:{ml}mm">Hymne STIA memakai tata letak yang sama di halaman berikutnya.</div>'''
    return halaman("L", isi, folio=4, sudut=(("b", 44),))


def pimpinan():
    ml, mr = kiri_kanan("R")
    lebar = W - ml - mr
    cw, gap = (lebar - 2 * 5) / 3, 5
    kartu_p = ""
    for r in range(3):
        for c in range(3):
            x, y = ml + c * (cw + gap), 48 + r * 46
            kartu_p += f'''<div class="card glass" style="left:{x}mm;top:{y}mm;width:{cw}mm;height:42mm">
  {foto(2.5, 2.5, cw - 5, 26, "FOTO RESMI")}
  <div class="abs" style="top:30.5mm;left:2mm;right:2mm;text-align:center">
    <div style="font:700 6.3pt/8pt Montserrat">[Nama &amp; gelar]</div>
    <div style="font:400 6pt/7.5pt 'Source Sans 3';color:var(--s)">[Jabatan]</div></div></div>'''
    isi = judul_bagian("R", "Unsur Pimpinan", "STIA Amuntai", top=24) + kartu_p + \
        f'<div class="catatan" style="top:189mm;left:{ml}mm">Pola sama untuk Yayasan Bakti Muslimin &amp; Senat; jumlah kartu mengikuti data resmi.</div>'
    return halaman("R", isi, folio=7, sudut=(("b", 40, .9),))


def visi_misi():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    misi = "".join(f'''<div style="display:flex;gap:3mm;margin-bottom:3.5mm">
  <div style="flex:none;width:4.6mm;height:4.6mm;border-radius:50%;background:var(--a);font:700 6.5pt/4.6mm Montserrat;text-align:center">{i}</div>
  <div style="flex:1;padding-top:.8mm">{bars([100, 72 - i * 4])}</div></div>''' for i in range(1, 6))
    isi = judul_bagian("L", "Visi &amp; Misi", "STIA Amuntai", top=24) + f'''
<div class="abs" style="top:44mm;left:{ml}mm">{NASKAH}</div>
<div class="glass abs" style="top:52mm;left:{ml}mm;width:{lebar}mm;height:40mm;border-radius:4mm;padding:7mm 8mm;text-align:center">
  <div style="font:600 6pt 'Source Sans 3';color:var(--s);letter-spacing:.4mm;margin-bottom:4mm">VISI</div>{bars([88, 94, 70], center=True)}</div>
<div class="abs" style="top:101mm;left:{ml}mm;width:{lebar}mm">
  <div style="font:600 6pt 'Source Sans 3';color:var(--s);letter-spacing:.4mm;margin-bottom:4mm">MISI</div>{misi}</div>'''
    return halaman("L", isi, folio=10, sudut=(("b", 44),))


def pembatas():
    isi = f'''
<div class="abs" style="top:70mm;left:{M_DALAM}mm;right:{M_LUAR}mm">
  <div class="sec-s" style="font-size:7pt">Daftar Wisudawan</div>
  <div class="sec-t" style="font-size:17pt;line-height:21pt;margin-top:3mm">Program Studi<br>Administrasi Bisnis</div></div>
<div class="sec-line" style="top:104mm;left:{M_DALAM}mm;right:{M_LUAR + 1}mm"><i></i><b></b></div>
<div class="abs script" style="top:118mm;left:{M_DALAM + 30}mm;font-size:30pt;transform:rotate(-8deg)">Untukmu Cinta</div>
{sapuan(131, M_DALAM + 32, 56, -8)}
<div class="catatan" style="top:4mm;right:4mm">PEMBATAS BAB — MASTER C (TANPA NOMOR)</div>'''
    return halaman("R", isi, sudut=(("b", 80), ("t", 50, .8)))


def kenangan():
    ml, mr = kiri_kanan("L")
    lebar = W - ml - mr
    def ph(t, l, w, h):
        return (f'<div class="abs" style="top:{t}mm;left:{l}mm;width:{w}mm;height:{h}mm;border-radius:2.5mm;padding:1.2mm;'
                f'background:#fff;box-shadow:0 .6mm 2mm rgba(48,129,219,.18);border:.35mm solid var(--a)">'
                f'<div class="ph" style="position:relative;width:100%;height:100%">FOTO KENANGAN<br>(resmi)</div></div>')
    g = 4
    isi = f'''
<div class="abs script" style="top:20mm;left:{ml}mm;font-size:28pt;transform:rotate(-6deg)">Foto Kenangan</div>
{sapuan(33, ml + 2, 50, -6)}
''' + ph(48, ml, lebar, 56) + ph(108, ml, (lebar - g) / 2, 34) + ph(108, ml + (lebar + g) / 2, (lebar - g) / 2, 34) + \
        ph(146, ml, (lebar - 2 * g) / 3, 36) + ph(146, ml + (lebar + g) / 3, (lebar - 2 * g) / 3, 36) + \
        ph(146, ml + 2 * (lebar + g) / 3, (lebar - 2 * g) / 3, 36)
    return halaman("L", isi, folio=86, sudut=(("b", 40, .9), ("t", 36, .7)))


def penutup():
    ml, mr = kiri_kanan("R")
    isi = judul_bagian("R", "Penutup", "Buku Wisuda 2026", top=24) + f'''
<div class="abs" style="top:46mm;left:{ml}mm;font:700 15pt Montserrat;color:var(--ink)">Pada Akhirnya,</div>
<div class="abs script" style="top:54mm;left:{ml + 6}mm;font-size:30pt;transform:rotate(-6deg)">Untukmu Cinta</div>
{sapuan(67, ml + 8, 56, -6)}
<div class="glass abs" style="top:86mm;left:{ml}mm;width:{W - ml - mr}mm;padding:8mm 9mm;border-radius:4mm;font:400 10pt/15pt 'Source Sans 3'">
  <p>Di antara kenangan yang kita simpan, perjuangan yang kita tuntaskan, dan harapan yang kita titipkan pada masa depan, ada cinta yang senantiasa menjadi alasan untuk terus melangkah.</p>
  <p style="margin-top:4mm;font-weight:600">Sebab pada akhirnya, kenangan akan tinggal, perjuangan akan bermakna, dan harapan akan menemukan jalannya.</p>
  <p class="script" style="margin-top:6mm;font-size:17pt;text-align:right">Untukmu, cinta.</p>
</div>'''
    return halaman("R", isi, folio=89, sudut=(("b", 50), ("t", 36, .7)))


def main():
    for f in [IKON / "ikon-nim.svg", ROOT / "02-Aset-Resmi/Logo/STIA.png"]:
        if not f.exists():
            sys.exit(f"Tidak ditemukan: {f}. Jalankan scripts/aset/buat_aset_svg.py dan pastikan logo resmi ada.")
    with open(DATA, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    prodi = "Program Studi Administrasi Bisnis"
    pages = {
        "01-sampul-depan": sampul_depan(),
        "02-sampul-belakang": sampul_belakang(),
        "03-pembuka-slogan": pembuka(),
        "04-daftar-isi-opsional": daftar_isi(),
        "05-kata-pengantar": kata_pengantar(),
        "06-sambutan-ketua": sambutan(),
        "07-mars": mars(),
        "08-unsur-pimpinan": pimpinan(),
        "09-visi-misi": visi_misi(),
        "10-pembatas-direktori": pembatas(),
        "11-direktori-kanan": direktori([rows[0], rows[1], rows[2], rows[4]], "R", prodi, 17,
                                        "HALAMAN KANAN — jilid di kiri (18 mm)"),
        "12-direktori-kiri": direktori([rows[3], rows[5], rows[1], rows[0]], "L", prodi, 18,
                                       "HALAMAN KIRI — jilid di kanan (18 mm)"),
        "13-foto-kenangan": kenangan(),
        "14-penutup": penutup(),
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
    await p.waitForTimeout(400);
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
