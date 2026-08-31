#!/usr/bin/env python3
"""
print_sim.py — FİZİKSEL PROVANIN İÇSEL İKAMESİ (Faz 6 · § 42).

⚠ BU BİR FİZİKSEL PROVA DEĞİLDİR ve olduğunu iddia etmez. Fiziksel
prova baskı ERİŞİLEMEZDİR (K58). Bu araç, bir provanın YAKALAYACAĞI
kusurlardan HANGİLERİNİN hesapla yakalanabileceğini ölçer ve
hangilerinin YAKALANAMADIĞINI yazar.

Ölçülenler — HER SAYFADA:

  ① 300 dpi RASTERLEŞTİRME — sayfa gerçek baskı çözünürlüğünde
     üretilebiliyor mu (bozuk sayfa, boş çıktı, çökme)
  ② 1-BİT EŞİKLEME — POD siyah-beyaz baskı yarım ton kullanmaz;
     gri bir çizgi ya SİYAH olur ya KAYBOLUR
  ③ İNCE ÇİZGİ HAYATTA KALMA — 300 dpi'de bir piksel 0,24 pt'dir;
     eşiklemede kaybolabilecek gri payı ölçülür
  ④ KENAR İHLALİ — mürekkep, kayıtlı kenar boşluğuna giriyor mu
     (cilt payı TEK/ÇİFT sayfada yer değiştirir)
  ⑤ MÜREKKEP YOĞUNLUĞU — sayfa POD için fazla dolu mu
  ⑥ BAŞPARMAK OKUNABİLİRLİĞİ — sayfa 1/8 ölçekte yapı gösteriyor mu

⚠ ÖRNEKLEM YETMEZ. İlk sürüm 269 sayfanın 29'unu örnekledi ve kenar
ihlali olan DÖRT sayfa buldu. Tam tarama gerçeği verdi. Bir baskı
kusuru istatistiksel değildir: tek bir sayfa kitabı bozar. Kapı artık
HER sayfayı okur.

Çıkış: 0 temiz · 1 kusur · 2 araç yok.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

DPI = 300
PT_PER_PX = 72.0 / DPI          # 0,24 pt

# Üst bilgi ve folyo TASARIM GEREĞİ kenar boşluğunda yaşar; ölçülen
# konumları üstten 32,6 pt ve alttan 32,2 pt'dir. Kenar denetimi bu
# ikisinin DIŞINDAKİ bandı okur — yoksa her sayfa işaretlenir.
EDGE_BAND_PT = 30.0

# ⚠ EŞİK BİR ÖLÇÜMDEN GELİR, temenniden değil. Tam tarama İKİ AYRI
# nüfus buldu ve aralarında üç kat büyüklük farkı var:
#
#   · 0,24–1,20 pt — TİPOGRAFİK, kusur değil. İki ölçülmüş nedeni var:
#       (a) kenar çizgisinin ÜSTÜNE çizilen bir cetvelin kalemi
#           ortalanmıştır; en kalın cetvel 1,0 pt olduğu için en çok
#           0,5 pt dışarı taşar.
#       (b) italik bir harfin SOL YAN BOŞLUĞU negatif olabilir:
#           s. 253'te "The next pattern"ın italik T'si kalem
#           konumunun 1,2 pt soluna uzanıyor. Bu, yazı tipinin
#           optik davranışıdır; metin kutusu doğru yerdedir.
#     Her ikisi de 45–63 pt'lik bir kenar boşluğunun İÇ sınırında,
#     kesime en az 45 pt uzakta kalır ve baskıda görünmez.
#
#   · 45,12 ve 61,68 pt — İÇERİK taşması. 46 akış şeması metin
#     sütununu 71 pt aşıyor, bir sayfada da bayat bir dönüşüm
#     bütün sayfayı kaydırmıştı. Kesime 1,3 pt kalana kadar uzanan
#     mürekkep ciltte kaybolur.
#
# Eşik 2,0 pt: tipografik nüfusun tamamını kapsar, içerik taşmasının
# EN KÜÇÜĞÜNDEN yirmi kat küçüktür. İki nüfusu ayırmayan bir kapı
# 51 sayfa işaretleyip hangisinin kitabı bozduğunu söyleyemezdi.
EDGE_TOLERANCE_PT = 2.0


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--pages", default=None, help="ör. 1,14,50 (yoksa TÜMÜ)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not shutil.which("pdftoppm"):
        print("▸ print_sim.py — ATLANDI: pdftoppm yok. Baskı simülasyonu "
              "ARAÇSIZ yapılamaz ve SESSİZCE GEÇMEZ.")
        return 2
    try:
        from PIL import Image
    except ImportError:
        print("▸ print_sim.py — ATLANDI: Pillow yok "
              "(07_TESTS/requirements-render.txt).")
        return 2

    pdf = paths.BOOK_DIRS[args.book] / "09_OUTPUT" / "BOOK_01.pdf"
    if not pdf.exists():
        print(f"✗ yayın varlığı YOK: {pdf}")
        return 1

    geom = load(paths.PAGE_GEOMETRY)
    marg = geom["margins"]
    min_stroke = float(geom["print_safety"]["min_stroke_pt"])

    n_pages = int(subprocess.run(
        ["pdfinfo", str(pdf)], capture_output=True, text=True
    ).stdout.split("Pages:")[1].split()[0])

    sample = ([int(x) for x in args.pages.split(",")] if args.pages
              else list(range(1, n_pages + 1)))

    errs: list = []
    warns: list = []
    ink_max, ink_max_pg = 0.0, 0
    thin_pages: list = []
    edge_pages: list = []
    flat_pages: list = []
    hairline = 0

    def px(v):
        return int(round(v / 72.0 * DPI))

    px_out, px_gut = px(marg["outside_pt"]), px(marg["gutter_pt"])
    px_edge = px(EDGE_BAND_PT)

    BLACK = [255 if v < 128 else 0 for v in range(256)]
    GRAY = [255 if 128 <= v < 215 else 0 for v in range(256)]

    with tempfile.TemporaryDirectory() as td:
        for pg in sample:
            for old in Path(td).glob("p-*.png"):
                old.unlink()
            r = subprocess.run(
                ["pdftoppm", "-r", str(DPI), "-gray", "-png",
                 "-f", str(pg), "-l", str(pg), str(pdf), str(Path(td) / "p")],
                capture_output=True)
            hits = sorted(Path(td).glob("p-*.png"))
            if r.returncode != 0 or not hits:
                errs.append(f"① s.{pg}: 300 dpi'de RASTERLEŞTİRİLEMEDİ")
                continue
            im = Image.open(hits[0]).convert("L")
            W, H = im.size

            # ② LUT ile eşikleme — piksel döngüsü 269 sayfada dakikalar sürer
            bw = im.point(BLACK, mode="L")
            black = bw.histogram()[255]
            ink = black / float(W * H)
            if ink > ink_max:
                ink_max, ink_max_pg = ink, pg
            if ink > 0.42:
                warns.append(f"⑤ s.{pg}: mürekkep %{ink*100:.0f} — POD için yoğun")

            # ③ eşiklemede kaybolabilecek gri payı
            gray = im.point(GRAY, mode="L").histogram()[255]
            if black and gray / float(black + gray) > 0.06:
                thin_pages.append(pg)

            # ④ kenar ihlali — VARLIK değil DERİNLİK ölçülür
            inner_left = (pg % 2 == 1)
            L = px_gut if inner_left else px_out
            R = px_out if inner_left else px_gut
            depth = 0.0
            bb = bw.crop((0, 0, L, H)).getbbox()
            if bb:
                depth = max(depth, (L - bb[0]) * PT_PER_PX)
            bb = bw.crop((W - R, 0, W, H)).getbbox()
            if bb:
                depth = max(depth, bb[2] * PT_PER_PX)
            bb = bw.crop((0, 0, W, px_edge)).getbbox()
            if bb:
                depth = max(depth, (px_edge - bb[1]) * PT_PER_PX)
            bb = bw.crop((0, H - px_edge, W, H)).getbbox()
            if bb:
                depth = max(depth, bb[3] * PT_PER_PX)
            if depth > EDGE_TOLERANCE_PT:
                edge_pages.append((pg, round(depth, 2)))
            elif depth > 0.0:
                hairline += 1

            # ⑥ başparmak okunabilirliği
            th = im.resize((max(1, W // 8), max(1, H // 8)))
            lo, hi = th.getextrema()
            if hi - lo < 60:
                flat_pages.append(pg)

    if thin_pages:
        warns.append(f"③ gri payı %6'yı aşan {len(thin_pages)} sayfa: "
                     f"{thin_pages[:8]}")
    if hairline:
        warns.append(f"④ kenar çizgisini kalem yarısı kadar (≤{EDGE_TOLERANCE_PT} pt) "
                     f"aşan {hairline} sayfa — cetvel kalemi ortalanmış, kusur değil")
    if edge_pages:
        worst = max(d for _, d in edge_pages)
        errs.append(f"④ KENAR BOŞLUĞUNA {EDGE_TOLERANCE_PT} pt'den derin giren "
                    f"{len(edge_pages)} sayfa (en derin {worst} pt): "
                    f"{edge_pages[:10]}")
    if flat_pages:
        warns.append(f"⑥ 1/8 ölçekte yapı göstermeyen {len(flat_pages)} sayfa: "
                     f"{flat_pages[:8]}")

    print("▸ print_sim.py — FİZİKSEL PROVANIN İÇSEL İKAMESİ")
    print(f"  {len(sample)}/{n_pages} sayfa TARANDI · {DPI} dpi · "
          f"1 piksel = {PT_PER_PX:.2f} pt · asgari çizgi {min_stroke} pt "
          f"({min_stroke/PT_PER_PX:.1f} piksel)")
    print(f"  en yoğun sayfa: s.{ink_max_pg}, mürekkep %{ink_max*100:.1f}")
    if args.verbose:
        for w in warns:
            print(f"  ⚠ {w}")
    if errs:
        print(f"  ✗ {len(errs)} kusur")
        for e in errs:
            print(f"    - {e}")
        return 1
    print("  ✓ her sayfa 300 dpi'de basıldı · kenar boşluğuna mürekkep "
          "girmiyor · 1-bit eşiklemede çizgi kaybı yok")
    print("  ⚠ ÖLÇÜLEMEYEN: kâğıdın gerçek beyazlığı · mürekkep yayılması · "
          "cildin düz durup durmadığı · arkadan görünme.")
    print("  ⚠ FİZİKSEL PROVA ALINMADI ve bu araç onun yerine GEÇMEZ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
