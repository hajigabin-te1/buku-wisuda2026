// buat-sampul-depan.jsx - Buku Wisuda STIA Amuntai 2026
// Membuat dokumen SAMPUL DEPAN A5 (148 x 210 mm, bleed 3 mm) yang editable,
// mengikuti gaya 01-Brief-Referensi/referensi.png dan mockup
// 06-Proof/konsep/01-sampul-depan.png.
//
// Isi: latar gradasi biru muda, ornamen pecahan kaca (PDF), logo resmi
// (02-Aset-Resmi/Logo/STIA.png), nama institusi, WISUDA 2026, judul UNTUKMU CINTA,
// slogan resmi, toga, bingkai foto grup (opsional langsung dipilih), teks kaki.
// Semua teks memakai Paragraph Styles "Sampul-*"; objek dipisah per layer.
//
// Target : Adobe InDesign 2020 (ExtendScript), Windows.
// Status : BELUM DIUJI di InDesign oleh pembuat skrip (cek sintaks saja).
//          Bila gagal, muncul pesan berisi nomor baris + isi error.
// Catatan: Jilid lem panas -> sampul dicetak terpisah sebagai bentangan
//          (belakang + punggung + depan). Lebar punggung belum diketahui, jadi
//          skrip ini membuat halaman depan saja; isinya bisa disalin ke file
//          bentangan setelah percetakan memberi lebar punggung.

#target indesign

function main() {
    var CFG = {
        lebar: 148, tinggi: 210, bleed: 3,
        warna: [
            ["UC-Primer-60", [235, 248, 255]],
            ["UC-Sekunder-30", [48, 129, 219]],
            ["UC-Aksen-10", [255, 224, 49]],
            ["UC-Tinta", [18, 53, 94]],
            // turunan terang/gelap dari warna primer, hanya untuk gradasi latar
            ["UC-Primer-Terang", [244, 251, 255]],
            ["UC-Primer-Gelap", [220, 239, 255]]
        ],
        fontJudul: "Montserrat", fontSampul: "Cinzel", cadangan: "Arial",
        slogan: "Merangkai kenangan, menuntaskan perjuangan, menjemput harapan."
    };

    var log = [];
    function coba(label, fn) {
        try { return fn(); } catch (e) { log.push("Dilewati: " + label + " (" + e.message + ")"); }
    }

    // ---------- Lokasi folder proyek ----------
    var ROOT = File($.fileName).parent.parent.parent.fsName + "/";
    if (!File(ROOT + "02-Aset-Resmi/Logo/STIA.png").exists) {
        var pilih = Folder.selectDialog("Pilih folder proyek Buku Wisuda (yang berisi 02-Aset-Resmi dan 05-InDesign)");
        if (pilih) ROOT = pilih.fsName + "/";
    }
    function berkas(rel) {
        var f = File(ROOT + rel);
        if (!f.exists) throw Error("file tidak ada: " + f.fsName);
        return f;
    }
    function aset(rel) {
        // utamakan PDF (pasti didukung InDesign 2020), cadangan SVG
        var pdf = File(ROOT + "05-InDesign/Links/" + rel + ".pdf");
        if (pdf.exists) return pdf;
        return berkas("05-InDesign/Links/" + rel + ".svg");
    }

    // ---------- Dokumen ----------
    var doc = app.documents.add(true);
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    var dp = doc.documentPreferences;
    dp.facingPages = false;
    dp.pagesPerDocument = 1;
    dp.pageWidth = CFG.lebar;
    dp.pageHeight = CFG.tinggi;
    dp.documentBleedUniformSize = true;
    dp.documentBleedTopOffset = CFG.bleed;
    doc.viewPreferences.rulerOrigin = RulerOrigin.PAGE_ORIGIN;
    doc.zeroPoint = [0, 0];
    doc.marginPreferences.properties = { top: 12, bottom: 12, left: 12, right: 12 };
    coba("transparansi PDF", function () { app.pdfPlacePreferences.transparentBackground = true; });

    // ---------- Layer ----------
    var layer = {};
    var urutan = ["Teks", "Ornamen", "Foto", "Latar"]; // atas -> bawah
    doc.layers[0].name = "Latar";
    layer.Latar = doc.layers[0];
    for (var li = urutan.length - 2; li >= 0; li--) {
        layer[urutan[li]] = doc.layers.add({ name: urutan[li] });
    }

    // ---------- Swatch ----------
    var sw = {};
    for (var i = 0; i < CFG.warna.length; i++) {
        var nm = CFG.warna[i][0];
        var c = doc.colors.itemByName(nm);
        if (!c.isValid) c = doc.colors.add({ name: nm, model: ColorModel.PROCESS, space: ColorSpace.RGB, colorValue: CFG.warna[i][1] });
        sw[nm] = c;
    }
    var BIRU = sw["UC-Sekunder-30"];
    var PAPER = doc.swatches.itemByName("Paper");
    var NONE = doc.swatches.itemByName("None");

    // ---------- Paragraph styles ----------
    var fontHilang = {};
    function setFont(target, fam, gaya) {
        var f = app.fonts.itemByName(fam + "\t" + gaya);
        if (!f.isValid) {
            fontHilang[fam + " " + gaya] = true;
            fam = CFG.cadangan;
            gaya = (/Bold|SemiBold|Semibold|Medium|Black/.test(gaya)) ? "Bold" : "Regular";
        }
        target.appliedFont = fam;
        coba("font style " + gaya, function () { target.fontStyle = gaya; });
    }
    function pStyle(nama, p) {
        var s = doc.paragraphStyles.itemByName(nama);
        if (!s.isValid) s = doc.paragraphStyles.add({ name: nama });
        setFont(s, p.font, p.gaya);
        s.pointSize = p.size;
        s.leading = p.lead || Leading.AUTO;
        s.fillColor = p.warna || BIRU;
        s.justification = p.rata || Justification.LEFT_ALIGN;
        s.hyphenation = false;
        if (p.track) s.tracking = p.track;
        return s;
    }
    var J = CFG.fontJudul;
    var ps = {
        institusi: pStyle("Sampul-Institusi", { font: J, gaya: "Bold", size: 6, lead: 7.6, track: 20 }),
        wisuda: pStyle("Sampul-Wisuda", { font: J, gaya: "Bold", size: 5.5, lead: 7, track: 40, rata: Justification.RIGHT_ALIGN }),
        tahun: pStyle("Sampul-Tahun", { font: J, gaya: "ExtraBold", size: 15, lead: 16, rata: Justification.RIGHT_ALIGN }),
        judul1: pStyle("Sampul-Judul-1", { font: CFG.fontSampul, gaya: "SemiBold", size: 27, lead: 28, track: 60, rata: Justification.CENTER_ALIGN }),
        judul2: pStyle("Sampul-Judul-2", { font: CFG.fontSampul, gaya: "Bold", size: 56, lead: 54, track: 100, rata: Justification.CENTER_ALIGN }),
        slogan: pStyle("Sampul-Slogan", { font: J, gaya: "SemiBold", size: 7.2, lead: 9.5, warna: sw["UC-Tinta"], rata: Justification.CENTER_ALIGN }),
        kaki: pStyle("Sampul-Kaki", { font: J, gaya: "Bold", size: 6.2, lead: 8, track: 30 }),
        tema: pStyle("Sampul-Tema", { font: J, gaya: "SemiBold", size: 5.5, lead: 7, track: 60 })
    };

    // ---------- Pembantu objek ----------
    var pg = doc.pages[0];
    function teks(b, isi, gaya, lyr, nama) {
        var t = pg.textFrames.add({ geometricBounds: b, itemLayer: layer[lyr || "Teks"] });
        t.textFramePreferences.insetSpacing = [0, 0, 0, 0];
        t.contents = isi[0];
        for (var n = 1; n < isi.length; n++) t.insertionPoints[-1].contents = "\r" + isi[n];
        for (n = 0; n < isi.length; n++) t.paragraphs[n].appliedParagraphStyle = gaya[n];
        t.name = nama;
        return t;
    }
    function pasang(file, b, lyr, nama, opsi) {
        return coba("place " + nama, function () {
            var r = pg.rectangles.add({ geometricBounds: b, itemLayer: layer[lyr] });
            r.fillColor = NONE; r.strokeColor = NONE;
            r.place(file);
            r.fit(FitOptions.PROPORTIONALLY);
            r.fit(FitOptions.CENTER_CONTENT);
            r.name = nama;
            if (opsi && opsi.balikV) r.flipItem(Flip.VERTICAL, AnchorPoint.CENTER_ANCHOR);
            if (opsi && opsi.putar) r.rotationAngle = opsi.putar;
            if (opsi && opsi.opasitas) r.transparencySettings.blendingSettings.opacity = opsi.opasitas;
            return r;
        });
    }
    function feather(item, sudut) {
        coba("gradient feather " + item.name, function () {
            var g = item.transparencySettings.gradientFeatherSettings;
            g.applied = true; g.type = GradientType.LINEAR; g.angle = sudut;
        });
    }

    // ---------- 1. Latar (gradasi biru muda sampai bleed) ----------
    var B = CFG.bleed;
    var latar = pg.rectangles.add({ geometricBounds: [-B, -B, CFG.tinggi + B, CFG.lebar + B], itemLayer: layer.Latar });
    latar.strokeColor = NONE;
    latar.fillColor = sw["UC-Primer-60"];
    latar.name = "latar";
    coba("gradasi latar", function () {
        var g = doc.gradients.itemByName("UC-Gradasi-Sampul");
        if (!g.isValid) {
            g = doc.gradients.add({ name: "UC-Gradasi-Sampul", type: GradientType.LINEAR });
            g.gradientStops[0].stopColor = sw["UC-Primer-Terang"]; g.gradientStops[0].location = 0;
            g.gradientStops[1].stopColor = sw["UC-Primer-Gelap"]; g.gradientStops[1].location = 100;
            g.gradientStops.add({ stopColor: sw["UC-Primer-60"], location: 50 });
        }
        latar.fillColor = g;
        latar.gradientFillAngle = -80;
    });
    latar.locked = true;

    // ---------- 2. Ornamen ----------
    var orn = {};
    coba("aset ornamen", function () {
        orn.tepi = aset("ornamen/ornamen-tepi");
        orn.sudut = aset("ornamen/ornamen-sudut");
        orn.toga = aset("ornamen/toga");
    });
    if (orn.tepi) pasang(orn.tepi, [-B, 3, CFG.tinggi + B, 13], "Ornamen", "ornamen-tepi");
    if (orn.sudut) {
        pasang(orn.sudut, [CFG.tinggi + B - 70, CFG.lebar + B - 70, CFG.tinggi + B, CFG.lebar + B], "Ornamen", "ornamen-sudut-bawah");
        pasang(orn.sudut, [-B, CFG.lebar + B - 46, -B + 46, CFG.lebar + B], "Ornamen", "ornamen-sudut-atas",
            { balikV: true, opasitas: 80 });
    }

    // ---------- 3. Logo resmi + identitas ----------
    coba("logo resmi", function () {
        pasang(berkas("02-Aset-Resmi/Logo/STIA.png"), [14, 18, 26.5, 31], "Teks", "logo-STIA");
    });
    teks([16, 33, 25, 95], ["SEKOLAH TINGGI ILMU", "ADMINISTRASI (STIA) AMUNTAI"], [ps.institusi, ps.institusi], "Teks", "institusi");
    teks([15, 100, 27, 134], ["WISUDA", "2026"], [ps.wisuda, ps.tahun], "Teks", "wisuda-2026");

    // ---------- 4. Judul + slogan ----------
    teks([40, 8, 72, 140], ["UNTUKMU", "CINTA"], [ps.judul1, ps.judul2], "Teks", "judul");
    teks([76, 26, 88, 122], [CFG.slogan], [ps.slogan], "Teks", "slogan");

    // ---------- 5. Toga (dekorasi) ----------
    if (orn.toga) {
        var toga = [[86, 30, 9, 18], [92, 56, 7, -12], [84, 82, 8, 6], [94, 104, 7, -20], [80, 118, 6, 25]];
        for (var k = 0; k < toga.length; k++) {
            var t = toga[k], h = t[2] * 20 / 24;
            pasang(orn.toga, [t[0], t[1], t[0] + h, t[1] + t[2]], "Ornamen", "toga-" + (k + 1), { putar: t[3] });
        }
    }

    // ---------- 6. Bingkai foto grup ----------
    var foto = pg.rectangles.add({ geometricBounds: [100, 16, 180, 136], itemLayer: layer.Foto });
    foto.name = "FOTO-GRUP (ganti dengan foto resmi)";
    foto.fillColor = NONE; foto.strokeColor = NONE;
    coba("sudut foto", function () {
        foto.topLeftCornerOption = foto.topRightCornerOption = CornerOptions.ROUNDED_CORNER;
        foto.topLeftCornerRadius = foto.topRightCornerRadius = 6;
    });
    coba("fitting foto", function () {
        foto.frameFittingOptions.fittingOnEmptyFrame = EmptyFrameFittingOptions.FILL_PROPORTIONALLY;
        foto.frameFittingOptions.fittingAlignment = AnchorPoint.TOP_CENTER_ANCHOR;
    });
    feather(foto, -90); // bagian bawah foto memudar ke latar seperti referensi
    var fotoFile = File.openDialog("Opsional: pilih FOTO GRUP RESMI (cutout PNG/PSD/TIFF, >= 300 ppi). Batal = biarkan bingkai kosong.");
    if (fotoFile) {
        coba("place foto grup", function () { foto.place(fotoFile); foto.fit(FitOptions.FILL_PROPORTIONALLY); });
    }

    // kabut putih di bawah foto agar teks kaki terbaca
    var kabut = pg.ovals.add({ geometricBounds: [176, -5, 206, CFG.lebar + 5], itemLayer: layer.Foto });
    kabut.fillColor = PAPER; kabut.strokeColor = NONE; kabut.name = "kabut-bawah";
    coba("opasitas kabut", function () { kabut.transparencySettings.blendingSettings.opacity = 85; });
    feather(kabut, 90); // bawah pekat, atas transparan

    // ---------- 7. Teks kaki ----------
    teks([181, 18, 195, 80], ["BUKU WISUDA", "STIA AMUNTAI", "TAHUN 2026"], [ps.kaki, ps.kaki, ps.kaki], "Teks", "kaki-judul");
    teks([198.5, 18, 203, 120], ["KENANGAN  \u2022  PERJUANGAN  \u2022  HARAPAN"], [ps.tema], "Teks", "kaki-tema");

    // ---------- Selesai ----------
    var pesan = "Sampul depan selesai dibuat.\nSimpan: File > Save As > 05-InDesign/INDD/00-Sampul-Depan.indd\n\n" +
        "Langkah berikut:\n- Ganti isi bingkai FOTO-GRUP (layer Foto) dengan foto grup resmi bila belum.\n" +
        "- Cek View > Overprint Preview dan Window > Output > Preflight.\n\n";
    var daftar = [];
    for (var f in fontHilang) daftar.push(f);
    if (daftar.length) pesan += "Font tidak ditemukan, diganti " + CFG.cadangan + ":\n- " + daftar.join("\n- ") + "\n\n";
    if (log.length) pesan += "Catatan:\n- " + log.join("\n- ");
    alert(pesan);
}

try {
    app.scriptPreferences.enableRedraw = false;
    main();
} catch (e) {
    alert("Skrip berhenti karena error.\n\nBaris: " + e.line + "\nPesan: " + e.message +
          "\n\nCatat/screenshot pesan ini dan kirimkan agar skrip bisa diperbaiki.");
} finally {
    app.scriptPreferences.enableRedraw = true;
}
