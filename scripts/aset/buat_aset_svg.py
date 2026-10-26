#!/usr/bin/env python3
"""Buat aset vektor desain (BUKAN aset resmi kampus) untuk Buku Wisuda 2026.

Gaya mengikuti 01-Brief-Referensi/referensi.png: pecahan kaca diagonal biru-emas
di sudut halaman, garis sapuan emas di bawah tulisan script, ikon garis untuk
kartu direktori, dan siluet toga untuk sampul.
Keluaran: 05-InDesign/Links/ornamen/*.svg dan 05-InDesign/Links/ikon/*.svg
(dipakai mockup dan dapat di-place ke InDesign 2020 — File > Place, SVG).
Jalankan dari root repo: python scripts/aset/buat_aset_svg.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORN = ROOT / "05-InDesign/Links/ornamen"
IKON = ROOT / "05-InDesign/Links/ikon"
BIRU, EMAS, TINTA = "#3081DB", "#FFE031", "#12355E"


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>\n')


def pita(a, lebar, n=70):
    """Pita diagonal melintasi sudut kanan-bawah kotak n x n."""
    return f"{n},{a} {n},{a + lebar} {a + lebar},{n} {a},{n}"


def ornamen_sudut():
    # sudut kanan-bawah; cerminkan untuk sudut lain
    defs = (f'<linearGradient id="gb" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{BIRU}" stop-opacity="0"/><stop offset="1" stop-color="{BIRU}" stop-opacity=".9"/></linearGradient>'
            f'<linearGradient id="gw" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".95"/></linearGradient>'
            f'<linearGradient id="ge" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{EMAS}" stop-opacity="0"/><stop offset=".6" stop-color="{EMAS}"/></linearGradient>')
    body = "".join([
        f'<polygon points="{pita(18, 10)}" fill="url(#gb)" opacity=".35"/>',
        f'<polygon points="{pita(30, 7)}" fill="url(#gw)" opacity=".9"/>',
        f'<polygon points="{pita(39, 2.2)}" fill="url(#ge)"/>',
        f'<polygon points="{pita(43, 9)}" fill="url(#gb)" opacity=".75"/>',
        f'<polygon points="{pita(53, 3)}" fill="url(#gw)" opacity=".8"/>',
        f'<polygon points="{pita(57, 13)}" fill="url(#gb)" opacity="1"/>',
        f'<polygon points="70,8 70,12 12,70 8,70" fill="url(#gb)" opacity=".25"/>',
    ])
    return svg(70, 70, body, defs)


def ornamen_tepi():
    # pita vertikal tipis untuk tepi luar sampul (seperti referensi), tinggi 216 mm (dengan bleed)
    defs = (f'<linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BIRU}" stop-opacity=".1"/>'
            f'<stop offset=".5" stop-color="{BIRU}" stop-opacity=".45"/><stop offset="1" stop-color="{BIRU}" stop-opacity=".1"/></linearGradient>')
    body = (f'<rect x="0" y="0" width="4" height="216" fill="url(#v)"/>'
            f'<rect x="5" y="0" width="1.2" height="216" fill="#fff" opacity=".8"/>'
            f'<polygon points="0,60 10,48 10,62 0,74" fill="{BIRU}" opacity=".35"/>'
            f'<polygon points="0,78 10,66 10,68.5 0,80.5" fill="{EMAS}"/>')
    return svg(10, 216, body, defs)


def sapuan_emas():
    body = (f'<path d="M2 9 C 25 3, 60 1, 98 4 C 70 4, 40 7, 6 12 Z" fill="{EMAS}"/>'
            f'<path d="M40 11 C 60 8, 80 7, 96 8" stroke="{EMAS}" stroke-width=".6" fill="none" stroke-linecap="round" opacity=".7"/>')
    return svg(100, 14, body)


def toga():
    body = (f'<polygon points="12,2 24,7 12,12 0,7" fill="#111a2b"/>'
            f'<path d="M5 9.2 L5 14 C 8 16, 16 16, 19 14 L19 9.2 L12 12 Z" fill="#0b1220"/>'
            f'<path d="M12 7 L21 9.5 L21 16" stroke="{EMAS}" stroke-width=".7" fill="none"/>'
            f'<path d="M21 16 l-1.2 3.5 h2.4 z" fill="{EMAS}"/>')
    return svg(24, 20, body)


IKON_PATH = {
    # garis 0.9 pada kotak 24, digambar sederhana
    "nim": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.5 16.5c.8-1.8 2-2.5 3.5-2.5s2.7.7 3.5 2.5M14.5 10h4M14.5 13.5h3"/>',
    "nama": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1.2-4 4-6 7.5-6s6.3 2 7.5 6"/>',
    "ttl": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z"/><circle cx="12" cy="10" r="2.4"/>',
    "ipk": '<path d="M4 19V11M10 19V6M16 19v-5M21 19H3"/><path d="M4 8l6-4 6 6 5-4"/>',
    "predikat": '<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"/><path d="M10 9l1.5 1.5L14.5 7.5"/>',
    "judul": '<path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5V19c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5z"/><path d="M12 6v13.5"/>',
}


def ikon(isi):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="2.8mm" height="2.8mm" viewBox="0 0 24 24" fill="none" '
            f'stroke="{BIRU}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{isi}</svg>\n')


def main():
    ORN.mkdir(parents=True, exist_ok=True)
    IKON.mkdir(parents=True, exist_ok=True)
    (ORN / "ornamen-sudut.svg").write_text(ornamen_sudut(), encoding="utf-8")
    (ORN / "ornamen-tepi.svg").write_text(ornamen_tepi(), encoding="utf-8")
    (ORN / "sapuan-emas.svg").write_text(sapuan_emas(), encoding="utf-8")
    (ORN / "toga.svg").write_text(toga(), encoding="utf-8")
    for nama, isi in IKON_PATH.items():
        (IKON / f"ikon-{nama}.svg").write_text(ikon(isi), encoding="utf-8")
    print("Aset ditulis ke", ORN, "dan", IKON)


if __name__ == "__main__":
    main()
