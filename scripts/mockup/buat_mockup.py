#!/usr/bin/env python3
"""Render mockup KONSEP (bukan file cetak) Buku Wisuda STIA Amuntai 2026.

Membuat HTML berukuran A5 dari data DUMMY, lalu merendernya ke PNG dan
satu PDF gabungan di 06-Proof/konsep/ memakai Playwright + Chromium.
Prasyarat: Python 3, Pillow, Node.js dengan paket `playwright`, akses internet
(Google Fonts). Jalankan dari root repo: python scripts/mockup/buat_mockup.py
"""

import csv
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "03-Data/CSV-DataMerge/DUMMY-contoh-wisudawan.csv"
OUT = ROOT / "06-Proof/konsep"

FONTS = ("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800"
         "&family=Source+Sans+3:wght@400;600&family=Playfair+Display:ital,wght@1,400;1,600&display=swap")

CSS = """
:root{--p:#EBF8FF;--s:#3081DB;--a:#FFE031;--ink:#12355E}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888}
.page{width:148mm;height:210mm;position:relative;overflow:hidden;background:var(--p);
  font-family:'Source Sans 3',sans-serif;color:var(--ink);margin:0 auto 10mm}
.abs{position:absolute}
.blob{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 40%,rgba(48,129,219,.28),rgba(48,129,219,0) 70%)}
.grid{position:absolute;inset:0;background-image:radial-gradient(rgba(48,129,219,.18) .25mm,transparent .3mm);
  background-size:5mm 5mm;-webkit-mask-image:linear-gradient(160deg,#000 0%,transparent 45%)}
.hair{position:absolute;height:.1mm;background:rgba(48,129,219,.5)}
.glass{background:linear-gradient(135deg,rgba(255,255,255,.85),rgba(255,255,255,.55));
  border:.18mm solid rgba(255,255,255,.95);box-shadow:0 .8mm 2.5mm rgba(48,129,219,.15);
  backdrop-filter:blur(2mm);-webkit-backdrop-filter:blur(2mm)}
.folio{position:absolute;bottom:6mm;left:0;right:0;text-align:center;font:500 8pt Montserrat;color:var(--s)}
.folio:before,.folio:after{content:'';display:inline-block;width:6mm;height:.15mm;background:var(--s);opacity:.5;vertical-align:middle;margin:0 2.5mm}
.watermark{position:absolute;left:0;right:0;bottom:1.5mm;text-align:center;font:600 5pt Montserrat;letter-spacing:.4mm;color:#c0392b;opacity:.8}
/* direktori */
.header{position:absolute;top:12mm;left:13.5mm;right:13.5mm;height:10mm;border-radius:2mm;
  background:linear-gradient(120deg,rgba(48,129,219,.95),rgba(48,129,219,.78));box-shadow:0 .8mm 2.5mm rgba(48,129,219,.25);
  display:flex;align-items:center;justify-content:center;font:700 9pt/11pt Montserrat;letter-spacing:.5mm;
  text-transform:uppercase;color:#fff;overflow:hidden}
.header:after{content:'';position:absolute;right:6mm;top:0;bottom:0;width:14mm;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.25),transparent)}
.header i{display:inline-block;width:2mm;height:2mm;background:var(--a);border-radius:.5mm;transform:rotate(45deg);margin:0 3mm}
.card{position:absolute;width:58mm;height:82mm;border-radius:3mm}
.card .foto{position:absolute;border-radius:2mm;border:.35mm solid #fff;overflow:hidden;
  background:linear-gradient(160deg,#d6ecfb,#b9daf5);display:flex;align-items:flex-end;justify-content:center}
.card .foto svg{width:80%}
.card .foto span{position:absolute;top:1mm;left:0;right:0;text-align:center;font:600 4.5pt Montserrat;color:var(--s);opacity:.8}
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
.puitis{font-family:'Playfair Display',serif;font-style:italic;color:var(--s)}
.ph{position:absolute;border:.3mm dashed rgba(48,129,219,.7);border-radius:2mm;display:flex;align-items:center;
  justify-content:center;text-align:center;font:600 6pt Montserrat;color:var(--s);background:rgba(255,255,255,.35)}
"""

SILUET = ('<svg viewBox="0 0 60 70"><circle cx="30" cy="24" r="13" fill="#fff" opacity=".85"/>'
          '<path d="M4 70c2-18 13-26 26-26s24 8 26 26z" fill="#fff" opacity=".85"/></svg>')
WM = '<div class="watermark">KONSEP · DATA DUMMY · BUKAN FILE CETAK</div>'


def e(t):
    return html.escape(t)


def latar(extra=""):
    return ('<div class="grid"></div>'
            '<div class="blob" style="width:90mm;height:90mm;right:-35mm;top:-30mm"></div>'
            '<div class="blob" style="width:70mm;height:70mm;left:-30mm;bottom:-25mm;opacity:.7"></div>' + extra)


def foto(top, left, w, h):
    return (f'<div class="foto" style="top:{top}mm;left:{left}mm;width:{w}mm;height:{h}mm">'
            f'<span>FOTO DUMMY 3:4</span>{SILUET}</div>')


def kartu_a(d, x, y):
    return f'''<div class="card glass" style="left:{x}mm;top:{y}mm">
  {foto(3, 3, 22, 29.3)}
  <div class="no" style="top:3mm;left:28mm">{int(d["No"]):02d}</div>
  <div class="abs" style="top:8.5mm;left:28mm;width:27mm">
    <div class="nama">{e(d["Nama"])}</div>
    <div class="data"><span class="lbl">NIM</span>{e(d["NIM"])}</div>
    <div class="data"><span class="lbl">TTL</span>{e(d["TTL"])}</div>
  </div>
  <div class="ipk" style="top:37mm;left:3mm;width:52mm"><span class="lbl">IPK</span>{e(d["IPK"])} &nbsp;·&nbsp; {e(d["Predikat"])}</div>
  <div class="accent" style="top:45.5mm;left:3mm;height:5mm"></div>
  <div class="judul" style="top:45mm;left:5mm;width:50mm;height:34mm"><span class="lbl">Judul Skripsi</span>{e(d["Judul"])}</div>
</div>'''


def kartu_b(d, x, y):
    return f'''<div class="card glass" style="left:{x}mm;top:{y}mm">
  {foto(3, 3, 22, 29.3)}
  <div class="no" style="top:35mm;left:3mm;width:22mm">{int(d["No"]):02d}</div>
  <div class="abs" style="top:3mm;left:27.5mm;width:27.5mm;height:76mm;overflow:hidden">
    <div class="nama">{e(d["Nama"])}</div>
    <div class="data"><span class="lbl">NIM</span>{e(d["NIM"])}</div>
    <div class="data"><span class="lbl">TTL</span>{e(d["TTL"])}</div>
    <div class="data" style="margin:1mm 0"><span class="lbl">IPK</span><b>{e(d["IPK"])}</b> · {e(d["Predikat"])}</div>
    <div class="judul" style="position:static"><span class="lbl">Judul Skripsi</span>{e(d["Judul"])}</div>
  </div>
</div>'''


def direktori(rows, kartu, prodi, folio, catatan):
    pos = [(13.5, 26), (76.5, 26), (13.5, 113), (76.5, 113)]
    cards = "".join(kartu(d, x, y) for d, (x, y) in zip(rows, pos))
    return f'''<section class="page">{latar()}
<div class="header">Wisudawan <i></i> {e(prodi)}</div>{cards}
<div class="abs kicker" style="top:197mm;left:13.5mm;font-size:5pt;color:#c0392b">{e(catatan)}</div>
<div class="folio">{folio}</div>{WM}</section>'''


def cover():
    return f'''<section class="page" style="background:linear-gradient(170deg,#EBF8FF 0%,#d5ecfd 55%,#EBF8FF 100%)">
{latar('<div class="blob" style="width:120mm;height:120mm;left:20mm;top:60mm;opacity:.8"></div>')}
<div class="hair" style="top:20mm;left:12mm;width:40mm"></div>
<div class="ph" style="top:12mm;left:12mm;width:16mm;height:16mm;border-radius:50%;top:26mm">LOGO<br>RESMI</div>
<div class="abs kicker" style="top:30mm;left:32mm">Buku Wisuda</div>
<div class="abs" style="top:34mm;left:32mm;font:600 7pt Montserrat;color:var(--ink)">Sekolah Tinggi Ilmu Administrasi (STIA) Amuntai</div>
<div class="glass abs" style="top:52mm;left:18mm;width:112mm;height:96mm;border-radius:5mm;transform:rotate(-4deg);opacity:.6"></div>
<div class="glass abs" style="top:56mm;left:14mm;width:120mm;height:90mm;border-radius:5mm;padding:3mm">
  <div class="ph" style="position:relative;width:100%;height:100%">FOTO GRUP RESMI<br>(placeholder — gunakan foto dari 02-Aset-Resmi)</div>
</div>
<div class="abs" style="top:132mm;left:96mm;width:40mm;height:22mm;border-radius:3mm;background:linear-gradient(135deg,rgba(48,129,219,.95),rgba(48,129,219,.7));
  box-shadow:0 1mm 3mm rgba(48,129,219,.35);display:flex;align-items:center;justify-content:center;font:800 18pt Montserrat;color:#fff;letter-spacing:.6mm">2026</div>
<div class="abs puitis" style="top:156mm;left:12mm;font-size:34pt;line-height:36pt">Untukmu<br>Cinta</div>
<div class="abs" style="top:194mm;left:12mm;width:22mm;height:.8mm;background:var(--a);border-radius:.4mm"></div>
{WM}</section>'''


def slogan():
    kata = ["kenangan", "perjuangan", "harapan"]
    dots = '<span style="display:inline-block;width:1.6mm;height:1.6mm;background:var(--a);transform:rotate(45deg);margin:0 3mm;vertical-align:middle"></span>'
    return f'''<section class="page">{latar('<div class="blob" style="width:100mm;height:100mm;left:24mm;top:55mm"></div>')}
<div class="glass abs" style="top:72mm;left:16mm;width:116mm;height:62mm;border-radius:5mm"></div>
<div class="abs" style="top:82mm;left:16mm;width:116mm;text-align:center">
  <div class="kicker">Untukmu Cinta · 2026</div>
  <div class="puitis" style="font-size:17pt;line-height:24pt;margin:9mm 10mm 8mm">Merangkai kenangan, menuntaskan perjuangan, menjemput harapan.</div>
  <div style="font:600 7pt Montserrat;letter-spacing:.6mm;text-transform:uppercase;color:var(--ink)">{dots.join(kata)}</div>
</div>
{WM}</section>'''


def penutup():
    return f'''<section class="page">{latar()}
<div class="hair" style="top:30mm;left:15mm;width:24mm"></div>
<div class="abs kicker" style="top:33mm;left:15mm">Penutup</div>
<div class="abs" style="top:39mm;left:15mm;width:110mm;font:700 18pt/22pt Montserrat;color:var(--s)">Pada Akhirnya,<br><span class="puitis" style="font-weight:400">Untukmu Cinta</span></div>
<div class="glass abs" style="top:78mm;left:15mm;width:118mm;padding:8mm 9mm;border-radius:4mm;font:400 10pt/15pt 'Source Sans 3'">
  <p>Di antara kenangan yang kita simpan, perjuangan yang kita tuntaskan, dan harapan yang kita titipkan pada masa depan, ada cinta yang senantiasa menjadi alasan untuk terus melangkah.</p>
  <p style="margin-top:4mm;font-weight:600">Sebab pada akhirnya, kenangan akan tinggal, perjuangan akan bermakna, dan harapan akan menemukan jalannya.</p>
  <p class="puitis" style="margin-top:6mm;font-size:13pt;text-align:right">Untukmu, cinta.</p>
</div>
<div class="accent" style="top:86mm;left:15mm;height:12mm;width:.8mm"></div>
<div class="folio">88</div>{WM}</section>'''


def main():
    with open(DATA, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    sel = [rows[0], rows[1], rows[2], rows[4]]  # termasuk nama & judul terpanjang
    pages = {
        "01-cover": cover(),
        "02-slogan": slogan(),
        "03-direktori-varian-A": direktori(sel, kartu_a, "Program Studi Administrasi Bisnis", 24,
                                          "VARIAN A (direkomendasikan) — judul selebar kartu"),
        "04-direktori-varian-B": direktori(sel, kartu_b, "Program Studi Administrasi Bisnis", 24,
                                          "VARIAN B — semua data di kolom kanan"),
        "05-penutup": penutup(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "src"
    src.mkdir(exist_ok=True)
    for name, body in pages.items():
        (src / f"{name}.html").write_text(
            f'<!doctype html><html lang="id"><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>{CSS}body{{background:none}}.page{{margin:0}}</style></head><body>{body}</body></html>',
            encoding="utf-8")

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

    from PIL import Image
    imgs = [Image.open(OUT / f"{n}.png").convert("RGB") for n in pages]
    imgs[0].save(OUT / "KONSEP-Buku-Wisuda-2026.pdf", save_all=True, append_images=imgs[1:], resolution=287)
    print("Mockup ditulis ke", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
