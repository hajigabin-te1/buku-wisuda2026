// setup-dokumen.jsx — Buku Wisuda STIA Amuntai 2026
// Membuat dokumen A5 dengan swatch, paragraph/character/object styles,
// master A-Isi, B-Direktori, C-Tanpa-Nomor, dan satu kartu contoh (Varian A)
// sebagai titik awal template Data Merge.
//
// Target  : Adobe InDesign 2020 (ExtendScript), Windows.
// Status  : BELUM DIUJI di InDesign. Jalankan pada dokumen baru; dokumen lain tidak disentuh.
// Cara    : Window > Utilities > Scripts > klik kanan "User" > Reveal in Explorer,
//           salin file ini ke folder tersebut, lalu klik dua kali di panel Scripts.
// Spesifikasi angka: docs/SPEK-DESAIN.md. Bleed & margin jilid WAJIB dicek ke percetakan.

#target indesign

(function () {
    // ---------- Konfigurasi (ubah di sini) ----------
    var CFG = {
        lebar: 148, tinggi: 210, bleed: 3,             // bleed: konfirmasi vendor
        mAtas: 12, mBawah: 15, mDalam: 15, mLuar: 12,  // halaman editorial
        dirSamping: 13.5, dirAtas: 26,                 // halaman direktori: margin simetris
        kartuL: 58, kartuT: 82, jarak: 5,
        warna: [
            ["UC-Primer-60", [235, 248, 255]],
            ["UC-Sekunder-30", [48, 129, 219]],
            ["UC-Aksen-10", [255, 224, 49]],
            ["UC-Tinta", [18, 53, 94]]
        ],
        fontJudul: "Montserrat", fontIsi: "Source Sans 3", fontPuitis: "Playfair Display",
        cadangan: "Arial"
    };

    var log = [];
    function coba(label, fn) {
        try { return fn(); } catch (e) { log.push("Dilewati: " + label + " (" + e.message + ")"); }
    }

    var doc = app.documents.add({
        documentPreferences: {
            pageWidth: CFG.lebar + "mm", pageHeight: CFG.tinggi + "mm",
            facingPages: true, pagesPerDocument: 1,
            documentBleedUniformSize: true, documentBleedTopOffset: CFG.bleed + "mm"
        }
    });
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.MILLIMETERS;
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

    // ---------- Paragraph & Character Styles ----------
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
        coba("bahasa " + nama, function () { s.appliedLanguage = "Indonesian"; });
        return s;
    }
    var J = CFG.fontJudul, S = CFG.fontIsi, P = CFG.fontPuitis;
    var ps = {
        h1: pStyle("H1-Bab", { font: J, gaya: "Bold", size: 20, lead: 24, warna: sw["UC-Sekunder-30"], after: 4 }),
        h2: pStyle("H2-Subjudul", { font: J, gaya: "SemiBold", size: 12, lead: 15, before: 3, after: 2 }),
        isi: pStyle("Isi", { font: S, gaya: "Regular", size: 10, lead: 14, rata: Justification.LEFT_JUSTIFIED, hyph: true, after: 2 }),
        puitis: pStyle("Puitis", { font: P, gaya: "Italic", size: 12, lead: 17, warna: sw["UC-Sekunder-30"], rata: Justification.CENTER_ALIGN }),
        lirik: pStyle("Lirik", { font: S, gaya: "Regular", size: 10, lead: 15, rata: Justification.CENTER_ALIGN }),
        dirHeader: pStyle("Dir-Header", { font: J, gaya: "Bold", size: 9, lead: 11, warna: PAPER, caps: true, track: 50, rata: Justification.CENTER_ALIGN }),
        dirNo: pStyle("Dir-No", { font: J, gaya: "Bold", size: 7, lead: 8, rata: Justification.CENTER_ALIGN }),
        dirNama: pStyle("Dir-Nama", { font: J, gaya: "SemiBold", size: 8.5, lead: 10, after: 1 }),
        dirLabel: pStyle("Dir-Label", { font: S, gaya: "Semibold", size: 5.5, lead: 7, warna: sw["UC-Sekunder-30"], caps: true, track: 40, after: 0.5 }),
        dirData: pStyle("Dir-Data", { font: S, gaya: "Regular", size: 7.5, lead: 9 }),
        dirIpk: pStyle("Dir-IPK", { font: S, gaya: "Semibold", size: 7.5, lead: 9 }),
        dirJudul: pStyle("Dir-Judul", { font: S, gaya: "Regular", size: 8, lead: 10 }),
        folio: pStyle("Folio", { font: J, gaya: "Medium", size: 8, warna: sw["UC-Sekunder-30"], rata: Justification.CENTER_ALIGN })
    };
    var csLabel = doc.characterStyles.itemByName("Dir-Label-Inline");
    if (!csLabel.isValid) csLabel = doc.characterStyles.add({ name: "Dir-Label-Inline" });
    setFont(csLabel, S, "Semibold");
    csLabel.pointSize = 5.5; csLabel.capitalization = Capitalization.ALL_CAPS;
    csLabel.fillColor = sw["UC-Sekunder-30"]; csLabel.tracking = 40;

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

    var osKartu = oStyle("Kaca-Kartu", function (s) { s.fillColor = PAPER; s.strokeColor = PAPER; s.strokeWeight = 0.5; });
    opasitas(osKartu, 70); sudut(osKartu, 3); bayangan(osKartu);
    coba("gradient feather Kaca-Kartu", function () {
        var g = osKartu.transparencySettings.gradientFeatherSettings;
        g.applied = true; g.type = GradientType.LINEAR; g.angle = -45;
    });

    var osHeader = oStyle("Kaca-Header", function (s) { s.fillColor = sw["UC-Sekunder-30"]; s.strokeColor = NONE; });
    opasitas(osHeader, 90); sudut(osHeader, 2); inset(osHeader, [0, 3, 0, 3], true);

    var osChip = oStyle("Chip-Emas", function (s) { s.fillColor = sw["UC-Aksen-10"]; s.strokeColor = NONE; });
    sudut(osChip, 1.5); inset(osChip, [0, 0.5, 0, 0.5], true);

    var osChipIpk = oStyle("Chip-IPK", function (s) {
        s.fillColor = sw["UC-Aksen-10"]; s.fillTint = 30; s.strokeColor = sw["UC-Aksen-10"]; s.strokeWeight = 0.5;
    });
    sudut(osChipIpk, 1.5); inset(osChipIpk, [0, 2, 0, 2], true);

    var osFoto = oStyle("Foto-Bingkai", function (s) { s.fillColor = sw["UC-Primer-60"]; s.strokeColor = PAPER; s.strokeWeight = 1; });
    sudut(osFoto, 2);
    coba("fitting Foto-Bingkai", function () {
        osFoto.enableFrameFittingOptions = true;
        osFoto.frameFittingOptions.fittingOnEmptyFrame = EmptyFrameFittingOptions.FILL_PROPORTIONALLY;
        osFoto.frameFittingOptions.fittingAlignment = AnchorPoint.TOP_CENTER_ANCHOR;
    });

    var osOrnamen = oStyle("Ornamen-Lingkaran", function (s) { s.fillColor = sw["UC-Sekunder-30"]; s.strokeColor = NONE; });
    opasitas(osOrnamen, 15);
    coba("gradient feather Ornamen", function () {
        var g = osOrnamen.transparencySettings.gradientFeatherSettings;
        g.applied = true; g.type = GradientType.RADIAL;
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
    function ornamen(page) {
        var luarKanan = page.side != PageSideOptions.LEFT_HAND;
        var cx = luarKanan ? CFG.lebar : 0;
        var o = page.ovals.add({ geometricBounds: [-25, cx - 30, 35, cx + 30] });
        o.appliedObjectStyle = osOrnamen;
        var g = page.graphicLines.add();
        g.paths[0].pathPoints[0].anchor = [luarKanan ? CFG.lebar - 40 : 0, 40];
        g.paths[0].pathPoints[1].anchor = [luarKanan ? CFG.lebar : 40, 40];
        g.strokeWeight = 0.25; g.strokeColor = sw["UC-Sekunder-30"];
        coba("opasitas garis", function () { g.transparencySettings.blendingSettings.opacity = 50; });
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
        latar(pg); ornamen(pg); folio(pg);
    }
    for (k = 0; k < mB.pages.length; k++) {
        pg = mB.pages[k];
        pg.marginPreferences.properties = { top: CFG.dirAtas, bottom: CFG.mBawah, left: CFG.dirSamping, right: CFG.dirSamping };
        latar(pg); folio(pg);
        var hx = [CFG.dirSamping, CFG.lebar - CFG.dirSamping];
        var hd = pg.textFrames.add({ geometricBounds: [CFG.mAtas, hx[0], CFG.mAtas + 10, hx[1]] });
        hd.contents = "Wisudawan Program Studi [ISI NAMA PRODI]";
        hd.appliedObjectStyle = osHeader;
        hd.paragraphs[0].appliedParagraphStyle = ps.dirHeader;
    }
    for (k = 0; k < mC.pages.length; k++) { latar(mC.pages[k]); }

    // ---------- Halaman 1: kartu contoh Varian A (titik awal Data Merge) ----------
    var hal = doc.pages[0];
    hal.appliedMaster = mB;
    hal.marginPreferences.properties = { top: CFG.dirAtas, bottom: CFG.mBawah, left: CFG.dirSamping, right: CFG.dirSamping };
    var x0 = CFG.dirSamping, y0 = CFG.dirAtas;

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

    var bg = kotak([0, 0, CFG.kartuT, CFG.kartuL], osKartu); bg.name = "kartu-latar";
    var foto = kotak([3, 3, 32.3, 25], osFoto); foto.name = "kartu-foto";
    var no = teks([3, 28, 7.5, 36], osChip, [[ps.dirNo, "\u00ABNo\u00BB"]]); no.name = "kartu-no";
    var info = teks([8.5, 28, 35.5, 55], osTeksKartu, [
        [ps.dirNama, "\u00ABNama\u00BB"],
        [ps.dirData, "NIM  \u00ABNIM\u00BB"],
        [ps.dirData, "TTL  \u00ABTTL\u00BB"]
    ]);
    info.name = "kartu-info";
    coba("label inline", function () {
        info.paragraphs[1].characters.itemByRange(0, 2).appliedCharacterStyle = csLabel;
        info.paragraphs[2].characters.itemByRange(0, 2).appliedCharacterStyle = csLabel;
    });
    var ipk = teks([37, 3, 42, 55], osChipIpk, [[ps.dirIpk, "IPK \u00ABIPK\u00BB  \u00B7  \u00ABPredikat\u00BB"]]); ipk.name = "kartu-ipk";
    var judul = teks([45, 3, 79, 55], osTeksKartu, [[ps.dirLabel, "Judul Skripsi"], [ps.dirJudul, "\u00ABJudul\u00BB"]]);
    judul.name = "kartu-judul";

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
})();
