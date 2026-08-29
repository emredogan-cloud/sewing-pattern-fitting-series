#!/usr/bin/env python3
"""
build_book.py — Kitap 1'in TAM manüskriptini dizer ve ÖLÇER.

Faz 4. Pilot (`build_pilot.py`) tek bir kesiti dizerdi; bu script
kitabın tamamını dizer ve üç şeyi aynı anda üretir:

  ① 09_OUTPUT/BOOK_01.pdf            — dizilmiş kitap (.gitignore § ⑥)
  ② 02_CONTENT/public/manuscript_index.public.json
                                     — ÖLÇÜM: bölüm, sayfa, figür, iddia
  ③ stdout                           — sayfa bütçesi raporu

② PROZA TAŞIMAZ. Depo bir yayın-öncesi metin arşivi değildir
(`.gitignore § ①`, `DECISIONS.md K9`); ölçüm public, metin protected.

DİZGİ: `typeset.py` — pilotla AYNI motor. İkinci bir dizgi yolu yoktur.
FİGÜR: `figure_engine.render()` — ikinci bir çizim yolu yoktur.

SAYFA BÜTÇESİ bir uyarı değil, bir KAPIDIR: `series_config.json`
`pageTargetProvisional` bandının dışına çıkılırsa çıkış kodu 1'dir.
Çelişmeli inceleme `B-08` bunu Faz 4 kısıtı olarak yazdı; cilt payı
300 sayfada değişir ve bütün sayfa geometrisi yeniden hesaplanır.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from figure_engine import Engine  # noqa: E402
from typeset import Typesetter, run_blocks  # noqa: E402
from atlas import AtlasBuilder  # noqa: E402

from bookplan import (MANUSCRIPT_DIR, GENERATED, PARTS,  # noqa: E402
                      INTERNAL_ID)  # TEK KOPYA — bookplan.py

READER_FIELDS = ("text", "caption", "title")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def check_reader_language(blocks: list, where: str) -> list:
    """İç kayıt kimliği okura dönük metinde GEÇEMEZ.

    Faz 2'de aynı kusur figürlerde bulundu (B-10 / K46) ve orada
    kapatıldı. Aynı kapı metin katmanında da olmalıdır; yoksa kusur
    yalnızca yer değiştirmiş olur."""
    bad = []
    for i, b in enumerate(blocks):
        vals = [b.get(f) for f in READER_FIELDS if isinstance(b.get(f), str)]
        vals += [str(x) for x in (b.get("items") or [])]
        for r in (b.get("rows") or []):
            vals += [str(c) for c in r]
        for v in vals:
            m = INTERNAL_ID.search(v)
            if m:
                bad.append(f"{where} blok {i} ({b['type']}): iç kimlik {m.group(0)!r} "
                           f"okur metninde — «{v[:70]}»")
    return bad


def build_front_matter(cfg: dict, book: dict) -> list:
    return [
        {"type": "h1", "text": book["title"], "kicker": book.get("series")},
        {"type": "lead", "text": book["subtitle"]},
        {"type": "para", "text": book["front_note"]},
        {"type": "pagebreak"},
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-charts", action="store_true",
                    help="belirti akış şemalarını ATLA — sayfa bütçesi ölçümü için")
    ap.add_argument("--only", default=None, help="virgülle ayrılmış bölüm anahtarları")
    ap.add_argument("--index", default=None, help="ölçüm dosyası yolu")
    args = ap.parse_args()

    bdir = paths.BOOK_DIRS[args.book]
    mdir = bdir / MANUSCRIPT_DIR
    if not mdir.exists():
        print(f"✗ manüskript dizini yok: {mdir.relative_to(paths.ROOT)}")
        return 2

    figs = load(paths.book_figures(args.book))
    # İÇ ARAÇ figürleri (tbl_af_index gibi) üretim/denetim içindir ve
    # KİTABA GİRMEZ. Sicilde `internal` bayrağıyla durur; burada meta
    # tablosuna hiç ALINMAZ, böylece bir bölüm onları çağırırsa
    # "figür sicilde yok" hatası verir ve sessizce basılmaz.
    meta_by_key = {m["source_file"].rsplit(".", 1)[0]: m
                   for m in figs["figure_meta"].values()
                   if m.get("source_file") and not m.get("internal")}
    internal_keys = {m["source_file"].rsplit(".", 1)[0]
                     for m in figs["figure_meta"].values()
                     if m.get("source_file") and m.get("internal")}
    geom = load(paths.PAGE_GEOMETRY)
    cfg = load(paths.SERIES_CONFIG)
    bookcfg = load(bdir / "book_config.json")

    out = Path(args.out) if args.out else bdir / "09_OUTPUT" / "BOOK_01.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    eng = Engine(args.book)
    atlas = AtlasBuilder(args.book, mdir)

    only = set(args.only.split(",")) if args.only else None
    ts = Typesetter(out, geom, eng)
    ts.set_running_head(bookcfg.get("titleWorking", ""), None)

    chapters: list = []
    missing: list = []
    errors: list = []
    claims_seen: dict = {}

    for pnum, ptitle, keys in PARTS:
        part_started = False
        for key in keys:
            if only and key not in only:
                continue
            if key == "ch02":
                blocks, sids = atlas.measurement_chapter(), []
            elif key in GENERATED:
                blocks, sids = atlas.chapter(GENERATED[key],
                                             with_charts=not args.no_charts)
            else:
                f = mdir / f"{key}.json"
                if not f.exists():
                    missing.append(key)
                    continue
                doc = load(f)
                blocks = doc["blocks"]
                sids = doc.get("signs_covered", [])
            errors.extend(check_reader_language(blocks, key))
            for b in blocks:
                if b.get("type") == "figure" and b.get("key") in internal_keys:
                    errors.append(f"{key}: İÇ ARAÇ figürü kitaba konulamaz — "
                                  f"{b['key']} (figures.json internal=true)")
            if not part_started and pnum > 0:
                ts.start_recto()
                ts.h1(f"Part {pnum}", kicker=None)
                ts.para(ptitle, face="serif-italic", size=13.0)
                ts.page_break()
                part_started = True
            p0 = ts.page
            f0 = len(ts.figures_used)
            ts.set_running_head(bookcfg.get("titleWorking", ""), None)
            errors.extend(run_blocks(ts, blocks, meta_by_key))
            chapters.append({
                "key": key, "part": pnum, "generated": key in GENERATED,
                "page_start": p0, "page_end": ts.page, "pages": ts.page - p0 + 1,
                "figures": len(ts.figures_used) - f0,
                "signs_covered": sids,
                "blocks": len(blocks),
                "words": sum(len(str(b.get("text", "")).split()) for b in blocks)
                         + sum(len(str(x).split()) for b in blocks
                               for x in (b.get("items") or [])),
            })
            for b in blocks:
                for cid in (b.get("claims") or []):
                    claims_seen.setdefault(cid, key)

    if errors:
        print(f"✗ {len(errors)} DİZGİ/OKUR DİLİ HATASI:")
        for e in errors[:30]:
            print(f"    - {e}")
        return 1

    ts.save()
    total = ts.page

    band = next((b["pageTargetProvisional"] for b in cfg["books"]
                 if b["id"] == args.book), None)

    index = {
        "$comment": [
            "ÜRETİLMİŞ ÖLÇÜM DOSYASI — proza TAŞIMAZ (.gitignore § ①).",
            "Kaynak: 06_BUILD/build_book.py. Her sayı dizgi çıktısından okunur.",
        ],
        "generated_by": "06_BUILD/build_book.py",
        "book": args.book,
        "charts_included": not args.no_charts,
        "pages_total": total,
        "page_target": band,
        "figures_used": len(ts.figures_used),
        "figures_distinct": len(set(ts.figures_used)),
        "chapters_expected": sum(len(k) for _, _, k in PARTS),
        "chapters_built": len(chapters),
        "chapters_missing": missing,
        "signs_covered": sorted({s for c in chapters for s in c["signs_covered"]}),
        "claims_referenced": sorted(claims_seen),
        "chapters": chapters,
    }
    idx_path = Path(args.index) if args.index else \
        bdir / "02_CONTENT" / "public" / "manuscript_index.public.json"
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    print(f"▸ build_book.py — {out.relative_to(paths.ROOT)}")
    print(f"  {total} sayfa · {len(ts.figures_used)} figür yerleşimi "
          f"({len(set(ts.figures_used))} ayrı figür) · {len(chapters)} bölüm")
    atlas_pages = sum(c["pages"] for c in chapters if c["generated"])
    print(f"  bölge atlası: {atlas_pages} sayfa")
    if missing:
        print(f"  ⚠ YAZILMAMIŞ bölüm: {', '.join(missing)}")
    if band:
        lo, hi = band
        if missing:
            print(f"  · sayfa bütçesi {lo}–{hi} — eksik bölümler yüzünden DEĞERLENDİRİLMEDİ")
        elif not (lo <= total <= hi):
            print(f"  ✗ SAYFA BÜTÇESİ DIŞI: {total}, hedef {lo}–{hi} "
                  f"(çelişmeli inceleme B-08 · cilt payı 300 sayfada değişir)")
            return 1
        else:
            print(f"  ✓ sayfa bütçesi içinde ({lo}–{hi})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
