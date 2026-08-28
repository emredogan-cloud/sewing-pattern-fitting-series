#!/usr/bin/env python3
"""
selftest_visual.py — RENDER KATMANININ kendi testi.

`07_TESTS/selftest.py` üçüncü taraf paket GEREKTİRMEZ ve CI'nin sekiz
kapı işi onunla çalışır. Bu dosya ayrıdır çünkü çizim katmanı
(`06_BUILD/figure_tokens.py`) **reportlab**'a, kalibrasyon
(`calibrate_tokens.py`) ayrıca **Pillow**'a ve `pdftoppm`'e bağlıdır.

Bağımlılık gizlenmedi, AYRILDI: veri kapıları bağımlılıksız kalır,
render kapısı bağımlılığını açıkça beyan eder
(`07_TESTS/requirements-render.txt`, CI işi `render`).

Kanıtladığı şey `selftest.py` ile aynı ilkedir:

    "Yakalamayan bir kapı, kapı değildir."

Her denetim kasıtlı olarak kusurlu bir çizim dener ve
`figure_tokens.ForbiddenDrawing` fırlatıldığını doğrular — yanlış
pozitif testleriyle birlikte.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "06_BUILD"))
import paths            # noqa: E402

try:
    import figure_tokens  # noqa: E402
except ModuleNotFoundError as e:
    print("✗ selftest_visual.py render bağımlılıklarını bulamadı: " + str(e))
    print("  pip install -r 07_TESTS/requirements-render.txt")
    sys.exit(2)

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, condition: bool, detail: str = ""):
    global CHECKS
    CHECKS += 1
    print(f"  {'✓' if condition else '✗'} {name}")
    if not condition:
        FAILURES.append(f"{name} — {detail}")


def _fc(w=200.0, h=200.0, surface="diagram"):
    return figure_tokens.FigureCanvas(w, h, surface=surface)


def _raises(fn) -> bool:
    try:
        fn()
    except figure_tokens.ForbiddenDrawing:
        return True
    except Exception:
        return False
    return False


def test_drawing_prohibitions_are_executable():
    """VISUAL_STANDARD § 5'in her yasağı bir İSTİSNA üretmelidir."""
    check("sayısal etiketsiz TK-02 (spread) çizimi REDDEDİLİYOR",
          _raises(lambda: _fc().tk02_spread_arrow(10, 10, 60, 10, "")),
          "etiketsiz spread oku çizilebildi")
    check("sayısal etiketsiz TK-03 (overlap) çizimi REDDEDİLİYOR",
          _raises(lambda: _fc().tk03_overlap_arrow(10, 10, 60, 10, "  ")),
          "etiketsiz overlap oku çizilebildi")
    check("ETİKETLİ spread oku SERBEST (yanlış pozitif yok)",
          not _raises(lambda: _fc().tk02_spread_arrow(10, 10, 60, 10, "1 in")),
          "etiketli ok reddedildi")
    check("vücut figüründe TK-01 (slash line) REDDEDİLİYOR",
          _raises(lambda: _fc(surface="body").tk01_slash_line(10, 10, 60, 60)),
          "vücutta slash line çizilebildi")
    check("KALIP yüzeyinde TK-01 SERBEST (yasak yüzeye özgüdür)",
          not _raises(lambda: _fc(surface="pattern").tk01_slash_line(10, 10, 60, 60)),
          "kalıpta slash line reddedildi")
    check("ölçek beyanı olmayan kalıp parçası REDDEDİLİYOR",
          _raises(lambda: _fc(surface="pattern").finish()),
          "ölçeksiz kalıp parçası kapanabildi")
    check("ölçek BEYAN EDİLİRSE kalıp parçası kapanıyor",
          not _raises(lambda: _fc(surface="pattern").declare_scale("şematik") or
                      None),
          "ölçek beyanı çalışmıyor")
    check("figür kutusunun DIŞINA çizim REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 10, 400)),
          "taşan çizgi çizilebildi")
    check("izin listesi dışı GRİ TONU REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 60, 10, gray=0.30)),
          "tanımsız gri kullanılabildi")
    check("baskı asgarisinin ALTINDA çizgi REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 60, 10, width=0.15)),
          "0,15 pt çizgi çizilebildi")
    check("asgari punto ALTINDA etiket REDDEDİLİYOR",
          _raises(lambda: _fc().text(10, 10, "x", size=4.0)),
          "4 pt etiket yazılabildi")
    check("TK-14 adım numarası 1'den KÜÇÜK olamıyor",
          _raises(lambda: _fc().tk14_step(50, 50, 0)),
          "0. adım çizilebildi")
    check("TK-18 devir düğümü AF etiketi OLMADAN çizilemiyor",
          _raises(lambda: _fc().tk18_handoff_node(10, 10, 120, 30, "x", "")),
          "AF'siz devir düğümü çizilebildi")
    check("tanımsız token kullanımı REDDEDİLİYOR",
          _raises(lambda: _fc().use("TK-99")),
          "TK-99 kullanılabildi")


def test_reader_facing_figures_carry_no_internal_ids():
    """İç kayıt kimlikleri OKURA BASILAMAZ (TYPOGRAPHY_STANDARD § 3.4)."""
    fc = _fc()
    fc.text(10, 100, "See AF-01")
    check("okura dönük figürde AF-xx kimliği REDDEDİLİYOR",
          _raises(lambda: fc.finish()), "AF-01 basılabildi")
    fc2 = _fc()
    fc2.text(10, 100, "SYM-016")
    check("okura dönük figürde SYM-xxx kimliği REDDEDİLİYOR",
          _raises(lambda: fc2.finish()), "SYM-016 basılabildi")
    fc3 = _fc()
    fc3.text(10, 100, "Bust volume")
    check("normal etiket SERBEST (yanlış pozitif yok)",
          not _raises(lambda: fc3.finish()), "normal etiket reddedildi")
    fc4 = _fc()
    fc4.text(10, 100, "AF-01")
    check("İÇ ARAÇ figüründe kimlik SERBEST (internal_marks)",
          not _raises(lambda: fc4.finish(internal_marks=True)),
          "iç araç figürü reddedildi")


def test_labels_do_not_overlap():
    """Çakışan iki ölçü etiketi yanlış okunur — bu bir HATA'dır."""
    fc = _fc()
    fc.text(20, 100, "high bust")
    fc.text(24, 101, "bust apex")
    check("ÜST ÜSTE BİNEN etiketler REDDEDİLİYOR",
          _raises(lambda: fc.finish()), "çakışan etiketler geçti")
    fc2 = _fc()
    fc2.text(20, 100, "high bust")
    fc2.text(20, 130, "bust apex")
    check("ayrık etiketler SERBEST (yanlış pozitif yok)",
          not _raises(lambda: fc2.finish()), "ayrık etiketler reddedildi")


def test_token_usage_is_measured_not_declared():
    """figures.json'daki notation_tokens BEYAN değil ÖLÇÜMDÜR."""
    fc = _fc()
    fc.tk08_apex(60, 60)
    fc.tk04_pivot_point(120, 60)
    used = fc.finish()
    check("kullanılan token'lar çizimden TÜRETİLİYOR",
          set(used) == {"TK-08", "TK-04"}, f"used={used}")
    fc2 = _fc()
    check("hiç çizim yapılmayan figürde token listesi BOŞ",
          fc2.finish() == [], "boş figür token bildirdi")


def test_engine_is_reproducible():
    """Motor DETERMİNİSTİK olmalıdır: aynı veri, aynı figür sicili."""
    import figure_engine
    a = figure_engine.Engine("book-01"); a.out_dir.mkdir(parents=True, exist_ok=True)
    figure_engine.Engine._meta = {}
    figs_a = [dict(f) for f in a.run()]
    figure_engine.Engine._meta = {}
    b = figure_engine.Engine("book-01")
    figs_b = [dict(f) for f in b.run()]
    check("figür motoru DETERMİNİSTİK (aynı veri → aynı sicil)",
          figs_a == figs_b, f"{len(figs_a)} vs {len(figs_b)} figür, içerik farklı")
    check("motorun ürettiği sicil diskteki figures.json ile UYUŞUYOR",
          [f["figure_id"] for f in figs_a] ==
          [f["figure_id"] for f in json.loads(
              paths.book_figures("book-01").read_text(encoding="utf-8"))["figures"]],
          "figures.json bayat — `python3 06_BUILD/figure_engine.py --book book-01`")


def main():
    print("▸ selftest_visual.py — render katmanının kendi testi\n")
    for fn in (
        test_drawing_prohibitions_are_executable,
        test_reader_facing_figures_carry_no_internal_ids,
        test_labels_do_not_overlap,
        test_token_usage_is_measured_not_declared,
        test_engine_is_reproducible,
    ):
        fn()
    print(f"\n{CHECKS} denetim çalıştı, {len(FAILURES)} başarısız.")
    if FAILURES:
        print("\n✗ BAŞARISIZ DENETİMLER:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("✓ Çizim yasakları kusurlu çizimleri doğru reddetti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
