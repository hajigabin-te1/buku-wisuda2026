// setup-dokumen.jsx - Buku Wisuda STIA Amuntai 2026
// Membuat dokumen A5 dengan swatch, paragraph & object styles, master A-Isi,
// B-Direktori, C-Tanpa-Nomor, dan satu kartu contoh (Varian A, gaya referensi
// 01-Brief-Referensi/referensi.png) sebagai titik awal template Data Merge.
// Ikon & ornamen (PDF, cadangan SVG) diambil dari 05-InDesign/Links/.
//
// Target  : Adobe InDesign 2020 (ExtendScript), Windows.
// Status  : v2 - perbaikan setelah laporan gagal di InDesign 2020 (documents.add,
//           pelaporan error per baris). Belum diuji ulang di InDesign oleh pembuat skrip.
//           Skrip membuat dokumen baru; dokumen lain tidak disentuh.
// Cara    : Window > Utilities > Scripts > klik kanan "User" > Reveal in Explorer,
//           salin file ini ke folder tersebut, lalu klik dua kali di panel Scripts.
// Spesifikasi angka: docs/SPEK-DESAIN.md. Bleed 3 mm & margin dikonfirmasi percetakan (perfect binding).

#target indesign

function main() {
    // ---------- Konfigurasi (ubah di sini) ----------
    var CFG = {
        lebar: 148, tinggi: 210, bleed: 3,             // spesifikasi percetakan
        mAtas: 12, mBawah: 15, mDalam: 18, mLuar: 12,  // margin dalam 18 mm: jilid lem panas
        dirAtas: 27,                                   // halaman direktori: kartu mulai di bawah judul bagian
        kartuL: 56.5, kartuT: 81, jarak: 5,
        warna: [
            ["UC-Primer-60", [235, 248, 255]],
            ["UC-Sekunder-30", [48, 129, 219]],
            ["UC-Aksen-10", [255, 224, 49]],
            ["UC-Tinta", [18, 53, 94]]
        ],
        fontJudul: "Montserrat", fontIsi: "Source Sans 3", fontPuitis: "Playfair Display",
        fontSampul: "Cinzel", fontScript: "Satisfy",
        cadangan: "Arial"
    };

    // folder Links relatif terhadap skrip: scripts/indesign/ -> root repo
    var LINKS = File($.fileName).parent.parent.parent.fsName + "/05-InDesign/Links/";
    if (!Folder(LINKS + "ikon").exists) {
        // skrip disalin ke folder Scripts Panel: minta lokasi folder Links proyek
        var pilih = Folder.selectDialog("Pilih folder 05-InDesign/Links di folder proyek Buku Wisuda");
        LINKS = pilih ? pilih.fsName + "/" : LINKS;
    }

    var log = [];
    function coba(label, fn) {
        try { return fn(); } catch (e) { log.push("Dilewati: " + label + " (" + e.message + ")"); }
    }

    // InDesign 2020: argumen pertama documents.add() adalah showingWindow (boolean),
    // jadi properti dokumen diatur SETELAH dokumen dibuat.
    var doc = app.documents.add(true);
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    var dp = doc.documentPreferences;
    dp.facingPages = true;
    dp.pagesPerDocument = 1;
    dp.pageWidth = CFG.lebar;
    dp.pageHeight = CFG.tinggi;
    dp.documentBleedUniformSize = true;
    dp.documentBleedTopOffset = CFG.bleed;
    doc.viewPreferences.rulerOrigin = RulerOrigin.PAGE_ORIGIN;
    doc.zeroPoint = [0, 0];
    doc.marginPreferences.properties = { top: CFG.mAtas, bottom: CFG.mBawah, left: CFG.mDalam, right: CFG.mLuar };

    // ---------- Swatch (RGB; konversi CMYK saat ekspor dengan profil vendor) ----------
    var sw = {};
    for (var i = 0; i < CFG.warna.length; i++) {
        var nm = CFG.warna[i][0];
        var c = doc.colors.itemByName(nm);
        if (!c.isValid) {
            c = doc.colors.add({ name: nm, model: ColorModel.PROCESS, space: ColorSpace.RGB, colorValue: CFG.warna[i][1] });
        }
        sw[nm] = c;
    }
    var PAPER = doc.swatches.itemByName("Paper");
    var NONE = doc.swatches.itemByName("None");

    // ---------- Font ----------
    var fontHilang = {};
    function setFont(target, fam, gaya) {
        var f = app.fonts.itemByName(fam + "\t" + gaya);
        if (!f.isValid) {
            fontHilang[fam + " " + gaya] = true;
            fam = CFG.cadangan;
            gaya = (/Bold|SemiBold|Semibold|Medium/.test(gaya)) ? "Bold" : (/Italic/.test(gaya) ? "Italic" : "Regular");
        }
        target.appliedFont = fam;
        coba("font style " + gaya, function () { target.fontStyle = gaya; });
    }

    // ---------- Paragraph Styles ----------
    var bahasaOK = true;
    function pStyle(nama, p) {
        var s = doc.paragraphStyles.itemByName(nama);
        if (!s.isValid) s = doc.paragraphStyles.add({ name: nama });
        setFont(s, p.font, p.gaya);
        s.pointSize = p.size;
        s.leading = p.lead || Leading.AUTO;
        s.fillColor = p.warna || sw["UC-Tinta"];
        s.justification = p.rata || Justification.LEFT_ALIGN;
        s.hyphenation = !!p.hyph;
        if (p.caps) s.capitalization = Capitalization.ALL_CAPS;
        if (p.track) s.tracking = p.track;
        if (p.after) s.spaceAfter = p.after;
        if (p.before) s.spaceBefore = p.before;
        if (p.indent) s.leftIndent = p.indent;
        if (bahasaOK) {
            try { s.appliedLanguage = "Indonesian"; }
            catch (e) { bahasaOK = false; log.push("Kamus bahasa Indonesia tidak tersedia; hyphenation memakai bahasa bawaan."); }
        }
        return s;
    }
    var J = CFG.fontJudul, S = CFG.fontIsi, P = CFG.fontPuitis;
    var BIRU = sw["UC-Sekunder-30"];
    var ps = {
        h1: pStyle("H1-Bab", { font: J, gaya: "Bold", size: 20, lead: 24, warna: BIRU, after: 4 }),
        h2: pStyle("H2-Subjudul", { font: J, gaya: "SemiBold", size: 12, lead: 15, before: 3, after: 2 }),
        secJudul: pStyle("Bagian-Judul", { font: J, gaya: "Bold", size: 12.5, lead: 14, warna: BIRU, caps: true, track: 45 }),
        secSub: pStyle("Bagian-Sub", { font: J, gaya: "SemiBold", size: 6.5, lead: 8, warna: BIRU, caps: true, track: 55 }),
        sampul: pStyle("Sampul-Judul", { font: CFG.fontSampul, gaya: "Bold", size: 56, lead: 54, warna: BIRU, rata: Justification.CENTER_ALIGN, track: 40 }),
        script: pStyle("Script-Tema", { font: CFG.fontScript, gaya: "Regular", size: 30, lead: 32, warna: BIRU }),
        isi: pStyle("Isi", { font: S, gaya: "Regular", size: 10, lead: 14, rata: Justification.LEFT_JUSTIFIED, hyph: true, after: 2 }),
        puitis: pStyle("Puitis", { font: P, gaya: "Italic", size: 12, lead: 17, warna: BIRU, rata: Justification.CENTER_ALIGN }),
        lirik: pStyle("Lirik", { font: S, gaya: "Regular", size: 10, lead: 15, rata: Justification.CENTER_ALIGN }),
        dirNo: pStyle("Dir-No", { font: J, gaya: "Bold", size: 7, lead: 8, rata: Justification.CENTER_ALIGN }),
        dirLabel: pStyle("Dir-Label", { font: S, gaya: "Semibold", size: 6, lead: 8, warna: BIRU }),
        dirNama: pStyle("Dir-Nama", { font: J, gaya: "SemiBold", size: 8, lead: 9.5, after: 1.2 }),
        dirData: pStyle("Dir-Data", { font: S, gaya: "Regular", size: 7.5, lead: 9 }),
        dirJudul: pStyle("Dir-Judul", { font: S, gaya: "Regular", size: 8, lead: 10, indent: 3.8 }),
        folio: pStyle("Folio", { font: J, gaya: "SemiBold", size: 7.5, warna: BIRU, rata: Justification.CENTER_ALIGN })
    };

    // ---------- Object Styles ----------
    function oStyle(nama, f) {
        var s = doc.objectStyles.itemByName(nama);
        if (!s.isValid) s = doc.objectStyles.add({ name: nama });
        coba(nama + " dasar", function () { f(s); });
        return s;
    }
    function sudut(s, r) {
        coba("sudut " + s.name, function () {
            s.enableStrokeAndCornerOptions = true;
            s.topLeftCornerOption = s.topRightCornerOption = s.bottomLeftCornerOption = s.bottomRightCornerOption = CornerOptions.ROUNDED_CORNER;
            s.topLeftCornerRadius = s.topRightCornerRadius = s.bottomLeftCornerRadius = s.bottomRightCornerRadius = r;
        });
    }
    function opasitas(s, o) {
        coba("opasitas " + s.name, function () { s.transparencySettings.blendingSettings.opacity = o; });
    }
    function bayangan(s) {
        coba("bayangan " + s.name, function () {
            var d = s.transparencySettings.dropShadowSettings;
            d.mode = ShadowMode.DROP; d.effectColor = sw["UC-Sekunder-30"]; d.opacity = 15;
            d.useGlobalLight = false; d.angle = 90; d.distance = 0.8; d.size = 2.5;
        });
    }
    function inset(s, arr, tengah) {
        coba("inset " + s.name, function () {
            s.enableTextFrameGeneralOptions = true;
            s.textFramePreferences.insetSpacing = arr;
            if (tengah) s.textFramePreferences.verticalJustification = VerticalJustification.CENTER_ALIGN;
        });
    }

    var osKartu = oStyle("Kaca-Kartu", function (s) { s.fillColor = PAPER; s.strokeColor = BIRU; s.strokeTint = 30; s.strokeWeight = 0.5; });
    opasitas(osKartu, 80); sudut(osKartu, 3); bayangan(osKartu);
    coba("gradient feather Kaca-Kartu", function () {
        var g = osKartu.transparencySettings.gradientFeatherSettings;
        g.applied = true; g.type = GradientType.LINEAR; g.angle = -45;
    });

    var osChip = oStyle("Chip-Emas", function (s) { s.fillColor = sw["UC-Aksen-10"]; s.strokeColor = NONE; });
    sudut(osChip, 1.5); inset(osChip, [0, 0.5, 0, 0.5], true);

    var osFoto = oStyle("Foto-Bingkai", function (s) { s.fillColor = sw["UC-Primer-60"]; s.strokeColor = NONE; });
    sudut(osFoto, 2);
    coba("fitting Foto-Bingkai", function () {
        osFoto.enableFrameFittingOptions = true;
        osFoto.frameFittingOptions.fittingOnEmptyFrame = EmptyFrameFittingOptions.FILL_PROPORTIONALLY;
        osFoto.frameFittingOptions.fittingAlignment = AnchorPoint.TOP_CENTER_ANCHOR;
    });

    var osTeksKartu = oStyle("Teks-Kartu", function (s) { s.fillColor = NONE; s.strokeColor = NONE; });
    inset(osTeksKartu, [0, 0, 0, 0], false);

    // ---------- Master ----------
    function batasX(page, dalam, luar) {
        // halaman kiri: sisi dalam di kanan
        return (page.side == PageSideOptions.LEFT_HAND) ? [luar, CFG.lebar - dalam] : [dalam, CFG.lebar - luar];
    }
    function latar(page) {
        var r = page.rectangles.add({ geometricBounds: [-CFG.bleed, -CFG.bleed, CFG.tinggi + CFG.bleed, CFG.lebar + CFG.bleed] });
        r.fillColor = sw["UC-Primer-60"]; r.strokeColor = NONE;
        r.locked = true;
    }
    function aset(rel) {
        // utamakan PDF (pasti didukung InDesign 2020), cadangan SVG
        var pdf = File(LINKS + rel + ".pdf");
        if (pdf.exists) return pdf;
        var svg = File(LINKS + rel + ".svg");
        if (svg.exists) return svg;
        throw Error("file tidak ada: " + LINKS + rel + ".pdf/.svg");
    }
    function pasangSvg(page, file, b, balikH, balikV) {
        coba("place " + file, function () {
            var f = aset(file);
            var r = page.rectangles.add({ geometricBounds: b });
            r.fillColor = NONE; r.strokeColor = NONE;
            r.place(f);
            r.fit(FitOptions.PROPORTIONALLY);
            if (balikH) r.flipItem(Flip.HORIZONTAL, AnchorPoint.CENTER_ANCHOR);
            if (balikV) r.flipItem(Flip.VERTICAL, AnchorPoint.CENTER_ANCHOR);
            r.locked = true;
        });
    }
    function ornamenSudut(page, ukuran) {
        // pecahan kaca biru-emas di sudut bawah sisi luar (seperti referensi)
        var kiri = page.side == PageSideOptions.LEFT_HAND;
        var y2 = CFG.tinggi + CFG.bleed, y1 = y2 - ukuran;
        var b = kiri ? [y1, -CFG.bleed, y2, -CFG.bleed + ukuran] : [y1, CFG.lebar + CFG.bleed - ukuran, y2, CFG.lebar + CFG.bleed];
        pasangSvg(page, "ornamen/ornamen-sudut", b, kiri, false);
    }
    function garis(page, y, x1, x2, warna, tebal, tint) {
        var g = page.graphicLines.add();
        g.paths[0].pathPoints[0].anchor = [x1, y];
        g.paths[0].pathPoints[1].anchor = [x2, y];
        g.strokeWeight = tebal; g.strokeColor = warna;
        if (tint) g.strokeTint = tint;
        return g;
    }
    function judulBagian(page, judul, sub, top) {
        // judul kapital biru + subjudul + garis tipis dengan segmen emas dan titik (gaya referensi)
        var x = batasX(page, CFG.mDalam, CFG.mLuar);
        var t = page.textFrames.add({ geometricBounds: [top, x[0], top + 9.5, x[1]] });
        t.contents = judul + "\r" + sub;
        t.paragraphs[0].appliedParagraphStyle = ps.secJudul;
        t.paragraphs[1].appliedParagraphStyle = ps.secSub;
        garis(page, top + 10.5, x[0], x[1], BIRU, 0.4, 35);
        garis(page, top + 10.5, x[1] - (x[1] - x[0]) * 0.38, x[1], sw["UC-Aksen-10"], 1.8);
        var d = page.ovals.add({ geometricBounds: [top + 9.9, x[1] - 0.6, top + 11.1, x[1] + 0.6] });
        d.fillColor = BIRU; d.strokeColor = NONE;
    }
    function folio(page) {
        var tf = page.textFrames.add({ geometricBounds: [CFG.tinggi - 11, CFG.lebar / 2 - 15, CFG.tinggi - 6, CFG.lebar / 2 + 15] });
        tf.contents = SpecialCharacters.AUTO_PAGE_NUMBER;
        tf.paragraphs[0].appliedParagraphStyle = ps.folio;
        tf.textFramePreferences.verticalJustification = VerticalJustification.CENTER_ALIGN;
    }

    var mA = doc.masterSpreads.item(0);
    mA.namePrefix = "A"; mA.baseName = "Isi";
    var mB = doc.masterSpreads.add(2, { namePrefix: "B", baseName: "Direktori" });
    var mC = doc.masterSpreads.add(2, { namePrefix: "C", baseName: "Tanpa-Nomor" });

    var pg, k;
    for (k = 0; k < mA.pages.length; k++) {
        pg = mA.pages[k];
        pg.marginPreferences.properties = { top: CFG.mAtas, bottom: CFG.mBawah, left: CFG.mDalam, right: CFG.mLuar };
        latar(pg); ornamenSudut(pg, 44); folio(pg);
    }
    for (k = 0; k < mB.pages.length; k++) {
        pg = mB.pages[k];
        pg.marginPreferences.properties = { top: CFG.dirAtas, bottom: CFG.mBawah, left: CFG.mDalam, right: CFG.mLuar };
        latar(pg); ornamenSudut(pg, 40); folio(pg);
        judulBagian(pg, "Daftar Wisudawan", "Program Studi [ISI NAMA PRODI] \u00B7 Wisuda 2026", CFG.mAtas);
    }
    for (k = 0; k < mC.pages.length; k++) { latar(mC.pages[k]); ornamenSudut(mC.pages[k], 70); }

    // ---------- Halaman 1: kartu contoh Varian A (titik awal Data Merge) ----------
    var hal = doc.pages[0];
    hal.appliedMaster = mB;
    hal.marginPreferences.properties = { top: CFG.dirAtas, bottom: CFG.mBawah, left: CFG.mDalam, right: CFG.mLuar };
    var x0 = batasX(hal, CFG.mDalam, CFG.mLuar)[0], y0 = CFG.dirAtas; // halaman 1 = halaman kanan

    function kotak(b, os) {
        var r = hal.rectangles.add({ geometricBounds: [y0 + b[0], x0 + b[1], y0 + b[2], x0 + b[3]] });
        r.appliedObjectStyle = os; return r;
    }
    function teks(b, os, isi) {
        var t = hal.textFrames.add({ geometricBounds: [y0 + b[0], x0 + b[1], y0 + b[2], x0 + b[3]] });
        t.appliedObjectStyle = os;
        t.contents = isi[0][1];
        for (var n = 1; n < isi.length; n++) t.insertionPoints[-1].contents = "\r" + isi[n][1];
        for (n = 0; n < isi.length; n++) t.paragraphs[n].appliedParagraphStyle = isi[n][0];
        return t;
    }

    function ikonLabel(par, nama) {
        // ikon garis (SVG) sebagai inline graphic di awal paragraf label
        coba("ikon " + nama, function () {
            var f = aset("ikon/ikon-" + nama);
            par.insertionPoints[0].contents = "\u2002";
            par.insertionPoints[0].place(f);
        });
    }

    var bg = kotak([0, 0, CFG.kartuT, CFG.kartuL], osKartu); bg.name = "kartu-latar";
    var foto = kotak([3, 3, 32.3, 25], osFoto); foto.name = "kartu-foto";
    var no = teks([2, 20.5, 6.6, 28], osChip, [[ps.dirNo, "\u00ABNo\u00BB"]]); no.name = "kartu-no";
    var info = teks([3.5, 28, 33.5, 53.5], osTeksKartu, [
        [ps.dirLabel, "Nama"], [ps.dirNama, "\u00ABNama\u00BB"],
        [ps.dirLabel, "Tempat, Tgl. Lahir"], [ps.dirData, "\u00ABTTL\u00BB"]
    ]);
    info.name = "kartu-info";
    ikonLabel(info.paragraphs[0], "nama"); ikonLabel(info.paragraphs[2], "ttl");
    var pemisah = garis(hal, y0 + 34.5, x0 + 3, x0 + 53.5, BIRU, 0.25, 30); pemisah.name = "kartu-pemisah";
    var mini = [["nim", "NIM", "NIM", 3, 19], ["ipk", "IPK", "IPK", 20.5, 30], ["predikat", "Predikat", "Predikat", 31.5, 53.5]];
    for (var m = 0; m < mini.length; m++) {
        var t = teks([35.7, mini[m][3], 45.5, mini[m][4]], osTeksKartu,
            [[ps.dirLabel, mini[m][1]], [ps.dirData, "\u00AB" + mini[m][2] + "\u00BB"]]);
        t.name = "kartu-" + mini[m][0];
        ikonLabel(t.paragraphs[0], mini[m][0]);
    }
    var judul = teks([46.5, 3, 78.5, 53.5], osTeksKartu, [[ps.dirLabel, "Judul Skripsi"], [ps.dirJudul, "\u00ABJudul\u00BB"]]);
    judul.name = "kartu-judul";
    ikonLabel(judul.paragraphs[0], "judul");

    // catatan non-cetak di pasteboard
    var cat = hal.textFrames.add({ geometricBounds: [0, CFG.lebar + 8, 60, CFG.lebar + 68] });
    cat.contents = "CATATAN (tidak tercetak):\rKartu contoh Varian A.\rGanti setiap \u00AB...\u00BB dengan field dari panel Data Merge, lalu pilih frame foto dan klik field Foto.\rHeader prodi diubah di master B-Direktori.";
    cat.nonprinting = true;

    var pesan = "Setup selesai. Simpan dokumen (File > Save As) ke 05-InDesign/INDD/.\n\n";
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
