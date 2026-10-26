// rapikan-direktori.jsx - Buku Wisuda STIA Amuntai 2026
// Jalankan pada dokumen HASIL Data Merge direktori (bukan template).
// Margin jilid tidak simetris (dalam 18 mm, luar 12 mm). Skrip ini menggeser
// seluruh kartu di setiap halaman agar tepi kirinya menempel ke margin yang benar:
// halaman kanan -> margin dalam, halaman kiri -> margin luar.
// Aman dijalankan berulang (hanya menggeser bila belum pas). Bisa di-undo sekali (Ctrl+Z).
//
// Target : Adobe InDesign 2020 (ExtendScript). Status: BELUM DIUJI di InDesign.

#target indesign

function rapikan(doc) {
    var vp = doc.viewPreferences;
    var simpan = [vp.horizontalMeasurementUnits, vp.rulerOrigin];
    vp.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    vp.rulerOrigin = RulerOrigin.PAGE_ORIGIN;

    var digeser = 0, diperiksa = 0;
    for (var i = 0; i < doc.pages.length; i++) {
        var pg = doc.pages[i];
        var lebar = pg.bounds[3] - pg.bounds[1];
        var items = [], minX = null;
        for (var k = 0; k < pg.pageItems.length; k++) {
            var it = pg.pageItems[k];
            var b = it.geometricBounds;               // [y1, x1, y2, x2]
            if (b[1] >= lebar || b[3] <= 0) continue; // abaikan objek di pasteboard
            items.push(it);
            if (minX === null || b[1] < minX) minX = b[1];
        }
        if (!items.length) continue;
        diperiksa++;
        // facing pages: marginPreferences.left = dalam, .right = luar
        var target = (pg.side == PageSideOptions.LEFT_HAND) ? pg.marginPreferences.right : pg.marginPreferences.left;
        var dx = target - minX;
        if (Math.abs(dx) < 0.05) continue;
        for (k = 0; k < items.length; k++) {
            if (items[k].locked) items[k].locked = false;
            items[k].move(undefined, [dx, 0]);
        }
        digeser++;
    }

    vp.horizontalMeasurementUnits = simpan[0];
    vp.rulerOrigin = simpan[1];
    return [diperiksa, digeser];
}

if (!app.documents.length) {
    alert("Buka dokumen hasil merge direktori dulu.");
} else {
    var hasil = null;
    try {
        app.doScript(function () { hasil = rapikan(app.activeDocument); },
            ScriptLanguage.JAVASCRIPT, undefined, UndoModes.ENTIRE_SCRIPT, "Rapikan kartu direktori");
        alert("Selesai. Halaman berisi kartu: " + hasil[0] + ", digeser: " + hasil[1] +
              ".\nPeriksa beberapa halaman kiri dan kanan dengan View > Grids & Guides > Show Guides.");
    } catch (e) {
        alert("Skrip berhenti karena error.\n\nBaris: " + e.line + "\nPesan: " + e.message);
    }
}
