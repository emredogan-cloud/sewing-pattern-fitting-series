#!/usr/bin/env python3
"""
build_pilot.py — Faz 3 pilot kesitini (MALZEME A) dizer.

`BOOK-01/00_SPEC/DIFFERENTIATION_TEST.md § 6.1`:

  · kaynak: Bölüm 11 (Göğüs)
  · kapsam: bölge anatomisi + bu bölgede okunan ölçüler + en az 3
    belirti girişi + akış şeması + "bu bölgede neyi henüz değiştirmeyin"
  · uzunluk: 6–8 sayfa
  · biçim: NİHAİ SAYFA GEOMETRİSİNDE basılmış, MARKASIZ
  · görsel: Faz 2'nin GERÇEK figürleri — taslak/eskiz kullanılmaz
  · yasak: seri adı, yazar adı, kapak, "Kitap 2'yi alın" ifadesi

Bu script o kuralları **dayatır**: markasız olma kuralı bir dilek değil,
bir denetimdir (`check_unbranded`). Seri adı, yazar adı veya kitap
göndermesi geçerse **çıktı üretilmez**.

Figürler `figure_engine.render()` ile AYNI motordan gelir; ikinci bir
çizim yolu yoktur. Dizilmiş sayfadaki bir akış şeması, tek başına
üretilen PDF'le birebir aynıdır.

Çıktı: BOOK-01/09_OUTPUT/PILOT_MATERIAL_A.pdf (.gitignore § ⑥)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from figure_engine import Engine  # noqa: E402
from typeset import Typesetter, run_blocks  # noqa: E402  (TEK KOPYA — typeset.py)

# MARKASIZLIK — DIFFERENTIATION_TEST § 5.4 madde 2 / § 6.1 yasak listesi
#
# ⚠ Eşleşme KELİME SINIRLIDIR. İlk sürüm çıplak "press" arıyordu ve
# "pressure" kelimesini yakalayıp geçerli bir cümleyi reddetti. Bir
# denetim, yakalaması gerekeni yakalamalı ve BAŞKA HİÇBİR ŞEYİ
# yakalamamalıdır — yanlış pozitif bir kapıyı işe yaramaz hâle getirir.
FORBIDDEN = [r"before you cut", r"true fit", r"vâliçe", r"valice",
             r"vâliçe press", r"valice press",
             r"book\s?[123]\b", r"kitap\s?[123]\b",
             r"measure & diagnose", r"adjustment atlas", r"draft your own"]


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def check_unbranded(blocks: list) -> list:
    """§ 6.1 yasak listesi bir DENETİMDİR."""
    import re
    pats = [re.compile(f, re.I) for f in FORBIDDEN]
    bad = []
    for b in blocks:
        for field in ("text", "caption", "title"):
            v = b.get(field)
            if not isinstance(v, str):
                continue
            for f, pat in zip(FORBIDDEN, pats):
                if pat.search(v):
                    bad.append(f"{f!r} → {v[:60]!r}")
        for it in b.get("items", []) or []:
            for f, pat in zip(FORBIDDEN, pats):
                if pat.search(str(it)):
                    bad.append(f"{f!r} → {str(it)[:60]!r}")
        for r in b.get("rows", []) or []:
            for cell in r:
                for f, pat in zip(FORBIDDEN, pats):
                    if pat.search(str(cell)):
                        bad.append(f"{f!r} → {str(cell)[:60]!r}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--content", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    bdir = paths.BOOK_DIRS[args.book]
    content_path = Path(args.content) if args.content else \
        bdir / "04_EDITORIAL" / "pilot" / "PILOT_MATERIAL_A.json"
    if not content_path.exists():
        print(f"✗ pilot içeriği yok: {content_path}")
        return 2
    doc = load(content_path)
    blocks = doc["blocks"]

    bad = check_unbranded(blocks)
    if bad:
        print("✗ MARKASIZLIK İHLALİ — pilot malzemesi markasız OLMALIDIR "
              "(DIFFERENTIATION_TEST § 5.4 / § 6.1):")
        for b in bad:
            print(f"    - {b}")
        return 1

    figs = load(paths.book_figures(args.book))
    meta_by_key = {m["source_file"].rsplit(".", 1)[0]: m
                   for m in figs["figure_meta"].values() if m.get("source_file")}

    geom = load(paths.PAGE_GEOMETRY)
    out = Path(args.out) if args.out else bdir / "09_OUTPUT" / "PILOT_MATERIAL_A.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    eng = Engine(args.book)
    # Pilot MARKASIZDIR: üst bilgi yok, çünkü üst bilgi kitabın adını
    # taşır (DIFFERENTIATION_TEST § 6.1 yasak listesi).
    ts = Typesetter(out, geom, eng, running_head=None)
    errs = run_blocks(ts, blocks, meta_by_key)
    if errs:
        for e in errs:
            print(f"✗ {e}")
        return 1
    used_figs = ts.figures_used
    ts.save()

    print(f"▸ build_pilot.py — {out.relative_to(paths.ROOT)}")
    print(f"  {ts.page} sayfa · {len(used_figs)} figür · markasızlık denetimi ✓")
    print(f"  figürler: {', '.join(used_figs)}")
    spec_lo, spec_hi = doc.get("target_pages", [6, 8])
    if not (spec_lo <= ts.page <= spec_hi):
        print(f"  ⚠ UZUNLUK HEDEF DIŞI: {ts.page} sayfa, hedef {spec_lo}–{spec_hi} "
              f"(DIFFERENTIATION_TEST § 6.1). Malzeme B ile karşılaştırılabilirlik "
              f"bozulur.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
