#!/usr/bin/env python3
"""
font_legibility_scan.py — figür etiketi yazı tipini ÖLÇEREK seçer.

Neden bu script var (Faz 2 bulgusu):

  `TYPOGRAPHY_STANDARD § 3.3` figür etiketleri için yedek yazı tipi
  olarak **Atkinson Hyperlegible**'ı adlandırmıştı. Faz 2'nin glif
  taraması bu yedeğin ürünün KENDİ gereksinimini (`Y1` — bayağı kesir
  glifleri ve inç işareti) KARŞILAMADIĞINI ölçtü: ⅛ ⅜ ⅝ ⅞ ve ″
  glifleri hem klasik hem de "Next" sürümünde YOKTUR. Bir ölçü
  kitabının figür etiketi ⅝ yazamıyorsa o yazı tipi yedek olamaz.

  Bu script yerine geçecek adayı SEÇMEZ — ÖLÇER. Karar ölçümden sonra
  `DECISIONS.md`'ye yazılır.

İki eksen:
  ① `Y1` — kesir ve inç glifleri var mı (ikili: var/yok).
  ② `Y3` — karıştırılabilir karakter çiftlerinin GERÇEK PİKSEL farkı.
     Her çift 6,5 pt'de 600 dpi'de rasterlanır, kendi sınırlayıcı
     kutusunun merkezine hizalanır ve normalize edilmiş piksel
     uyuşmazlığı hesaplanır.

⚠ SINIR — bu script okunabilirliği ÖLÇMEZ. Piksel farkı, bir okurun
  6,5 pt'de basılmış bir `1` ile `l`'yi ayırt edebildiğini
  KANITLAMAZ. `T3` üç insan okuyucu gerektirir ve gerçek kâğıtta
  yapılır (`TYPOGRAPHY_STANDARD § 4`, `EXTERNAL_DEPENDENCIES.md D-05`).
  Bu ölçüm yalnızca AÇIKÇA kötü adayları eler ve sıralama üretir.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFontFile  # noqa: E402

Y1_GLYPHS = "⅛¼⅜½⅝¾⅞″"
CONFUSABLE = [("1", "l"), ("1", "I"), ("l", "I"), ("0", "O"), ("0", "o"),
              ("6", "8"), ("8", "9"), ("6", "9"), ("3", "8"), ("5", "6"),
              ("2", "Z"), ("rn", "m")]

CANDIDATES = {
    "SourceSans3": "ttf/SourceSans3-Regular.ttf",
    "AtkinsonHyperlegible": "ttf/AtkinsonHyperlegible-Regular.ttf",
    "AtkinsonHyperlegibleNext": "ttf/AHNext.ttf",
    "IBMPlexSans": "ttf/IBMPlexSans.ttf",
    "Inter": "ttf/Inter.ttf",
    "Lexend": "ttf/Lexend.ttf",
}


def y1_coverage(path: Path) -> dict:
    f = TTFontFile(str(path))
    cm = f.charToGlyph
    missing = [c for c in Y1_GLYPHS if ord(c) not in cm]
    return {"glyph_count": len(cm), "missing": missing, "pass": not missing}


def _bitmap(path: Path, ch: str, px_size: int) -> Image.Image:
    fnt = ImageFont.truetype(str(path), px_size)
    box = 4 * px_size
    im = Image.new("L", (box, box), 255)
    d = ImageDraw.Draw(im)
    d.text((box // 4, box // 4), ch, font=fnt, fill=0)
    bb = im.point(lambda v: 255 if v < 128 else 0).getbbox()
    if bb is None:
        return None
    return im.crop(bb)


def _align_and_compare(a: Image.Image, b: Image.Image) -> float:
    """Normalize edilmiş piksel uyuşmazlığı: 0 = aynı, 1 = tamamen farklı."""
    w = max(a.width, b.width); h = max(a.height, b.height)
    best = 0.0
    for img_pair in ((a, b),):
        ca = Image.new("L", (w, h), 255); ca.paste(img_pair[0], ((w - a.width) // 2,
                                                                (h - a.height) // 2))
        cb = Image.new("L", (w, h), 255); cb.paste(img_pair[1], ((w - b.width) // 2,
                                                                (h - b.height) // 2))
        pa = [1 if v < 128 else 0 for v in ca.getdata()]
        pb = [1 if v < 128 else 0 for v in cb.getdata()]
        union = sum(1 for x, y in zip(pa, pb) if x or y)
        diff = sum(1 for x, y in zip(pa, pb) if x != y)
        best = max(best, diff / union if union else 0.0)
    return best


def y3_scan(path: Path, size_pt: float, dpi: int) -> dict:
    px_size = max(4, int(round(size_pt * dpi / 72.0)))
    pairs, skipped = {}, []
    for a, b in CONFUSABLE:
        ia, ib = _bitmap(path, a, px_size), _bitmap(path, b, px_size)
        if ia is None or ib is None:
            skipped.append(f"{a}/{b}")
            continue
        pairs[f"{a}/{b}"] = round(_align_and_compare(ia, ib), 4)
    vals = list(pairs.values())
    return {"size_pt": size_pt, "dpi": dpi, "px_size": px_size,
            "pair_dissimilarity": pairs,
            "worst_pair": min(pairs, key=pairs.get) if pairs else None,
            "worst_value": round(min(vals), 4) if vals else None,
            "mean": round(sum(vals) / len(vals), 4) if vals else None,
            "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=float, default=6.5)
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    results = {}
    for name, rel in CANDIDATES.items():
        p = paths.VISUAL_FONTS / rel
        if not p.exists():
            results[name] = {"error": "dosya yok — 06_BUILD/fetch_fonts.py"}
            continue
        y1 = y1_coverage(p)
        y3 = y3_scan(p, args.size, args.dpi)
        results[name] = {"file": rel, "Y1": y1, "Y3": y3,
                         "eligible": y1["pass"]}

    ranked = sorted([(n, r) for n, r in results.items()
                     if r.get("eligible") and r["Y3"]["worst_value"] is not None],
                    key=lambda kv: (-kv[1]["Y3"]["worst_value"], -kv[1]["Y3"]["mean"]))

    report = {
        "$comment": [
            "FONT LEGIBILITY SCAN — 06_BUILD/font_legibility_scan.py çıktısı.",
            "Y1 = kesir/inç glif kapsaması (ELEYİCİ). Y3 = karıştırılabilir",
            "çiftlerin piksel farkı (SIRALAYICI, kanıt DEĞİL).",
            "T3'ün insan okuma testinin YERİNE GEÇMEZ.",
        ],
        "measured_on": "2026-08-28",
        "settings": {"size_pt": args.size, "dpi": args.dpi},
        "candidates": results,
        "eliminated_by_Y1": [n for n, r in results.items()
                             if r.get("eligible") is False],
        "ranking_by_worst_pair": [{"font": n,
                                   "worst_pair": r["Y3"]["worst_pair"],
                                   "worst_value": r["Y3"]["worst_value"],
                                   "mean": r["Y3"]["mean"]} for n, r in ranked],
    }
    out = Path(args.out) if args.out else paths.VISUAL / "font_legibility_scan.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")

    print("▸ font_legibility_scan.py")
    for n, r in results.items():
        if "error" in r:
            print(f"  {n:<26} {r['error']}"); continue
        y1 = "Y1 ✓" if r["Y1"]["pass"] else "Y1 ✗ eksik: " + "".join(r["Y1"]["missing"])
        y3 = r["Y3"]
        print(f"  {n:<26} {y1:<26} en kötü çift {y3['worst_pair']}={y3['worst_value']} "
              f"· ortalama {y3['mean']}")
    print("  ── Y1'i geçenler, en kötü çifte göre sıralı ──")
    for i, row in enumerate(report["ranking_by_worst_pair"], 1):
        print(f"   {i}. {row['font']:<22} en kötü {row['worst_pair']}="
              f"{row['worst_value']} · ortalama {row['mean']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
