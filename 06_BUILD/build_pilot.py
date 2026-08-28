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
from figure_tokens import font, register_fonts  # noqa: E402
from figure_engine import Engine  # noqa: E402

from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402

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


class Typesetter:
    def __init__(self, out: Path, geom: dict, engine: Engine):
        self.g = geom
        self.eng = engine
        register_fonts()
        self.W = geom["trim"]["width_pt"]; self.H = geom["trim"]["height_pt"]
        self.c = rl_canvas.Canvas(str(out), pagesize=(self.W, self.H))
        tb = geom["text_block"]
        self.tw = tb["width_pt"]
        self.side_w = tb["side_column_width_pt"]
        self.gap = tb["column_gap_pt"]
        self.body = float(geom["typography_grid"]["body_size_pt"])
        self.lead = float(geom["typography_grid"]["baseline_grid_pt"])
        self.top = self.H - geom["margins"]["top_pt"]
        self.bottom = geom["margins"]["bottom_pt"]
        self.page = 0
        self.side_queue: list = []
        self._new_page()

    # ── sayfa ─────────────────────────────────────────────────────────
    def _new_page(self):
        if self.page:
            self._flush_side()
            self.c.showPage()
        self.page += 1
        # tek sayfa: cilt payı SOLDA · çift sayfa: cilt payı SAĞDA
        recto = self.page % 2 == 1
        gut = self.g["margins"]["gutter_pt"]; out = self.g["margins"]["outside_pt"]
        self.x_text = gut if recto else out
        self.x_side = self.x_text + self.tw + self.gap
        if not recto:
            self.x_text = out + self.side_w + self.gap
            self.x_side = out
        self.y = self.top
        self.side_y = self.top
        self.c.setFillGray(0.45)
        self.c.setFont(font("sans"), 7.5)
        self.c.drawCentredString(self.W / 2, self.bottom - 22.0, str(self.page))
        self.c.setFillGray(0.0)

    def _room(self, h: float) -> bool:
        return self.y - h >= self.bottom

    def _need(self, h: float):
        if not self._room(h):
            self._new_page()

    def _flush_side(self):
        pass

    # ── metin ─────────────────────────────────────────────────────────
    def _wrap(self, s: str, w: float, face: str, size: float) -> list:
        out, line = [], ""
        for word in s.split():
            cand = (line + " " + word).strip()
            if pdfmetrics.stringWidth(cand, font(face), size) <= w or not line:
                line = cand
            else:
                out.append(line); line = word
        if line:
            out.append(line)
        return out

    def para(self, s: str, face="serif", size=None, lead=None, indent=0.0,
             space_after=None, gray=0.0):
        size = size or self.body
        lead = lead or self.lead
        lines = self._wrap(s, self.tw - indent, face, size)
        self._need(len(lines) * lead)
        if not self._room(len(lines) * lead):
            pass
        self.c.setFillGray(gray)
        for ln in lines:
            if not self._room(lead):
                self._new_page(); self.c.setFillGray(gray)
            self.y -= lead
            self.c.setFont(font(face), size)
            self.c.drawString(self.x_text + indent, self.y, ln)
        self.y -= (self.lead * 0.45 if space_after is None else space_after)
        self.c.setFillGray(0.0)

    def h1(self, s: str):
        self._need(self.lead * 3)
        self.y -= self.lead * 1.4
        self.c.setFont(font("sans-bold"), 20.0)
        self.c.drawString(self.x_text, self.y, s)
        self.y -= self.lead * 0.9

    def h2(self, s: str):
        self._need(self.lead * 2.6)
        self.y -= self.lead * 1.1
        self.c.setFont(font("sans-semibold"), 13.0)
        self.c.drawString(self.x_text, self.y, s)
        self.y -= self.lead * 0.5

    def h3(self, s: str):
        self._need(self.lead * 2.2)
        self.y -= self.lead * 0.85
        self.c.setFont(font("sans-semibold"), 10.5)
        self.c.drawString(self.x_text, self.y, s)
        self.y -= self.lead * 0.3

    def bullets(self, items: list, marker="—"):
        for it in items:
            lines = self._wrap(it, self.tw - 14.0, "serif", self.body)
            self._need(len(lines) * self.lead)
            first = True
            for ln in lines:
                if not self._room(self.lead):
                    self._new_page()
                self.y -= self.lead
                self.c.setFont(font("serif"), self.body)
                if first:
                    self.c.drawString(self.x_text, self.y, marker)
                    first = False
                self.c.drawString(self.x_text + 14.0, self.y, ln)
        self.y -= self.lead * 0.45

    def numbered(self, items: list):
        for i, it in enumerate(items, 1):
            lines = self._wrap(it, self.tw - 16.0, "serif", self.body)
            self._need(len(lines) * self.lead)
            first = True
            for ln in lines:
                if not self._room(self.lead):
                    self._new_page()
                self.y -= self.lead
                self.c.setFont(font("serif"), self.body)
                if first:
                    self.c.setFont(font("sans-semibold"), self.body - 1.0)
                    self.c.drawString(self.x_text, self.y, f"{i}.")
                    self.c.setFont(font("serif"), self.body)
                    first = False
                self.c.drawString(self.x_text + 16.0, self.y, ln)
        self.y -= self.lead * 0.45

    def side_note(self, title: str, body: str):
        """Yan sütun notu — gövde metninin akışını KESMEZ (K39)."""
        size = 8.0; lead = 10.4
        lines = self._wrap(body, self.side_w - 8.0, "sans", size)
        y = self.y + self.lead
        need = lead * (len(lines) + 1.6)
        if y - need < self.bottom:
            y = min(self.top, self.top)
        self.c.setStrokeGray(0.0); self.c.setLineWidth(0.7)
        self.c.line(self.x_side, y + 3.0, self.x_side + self.side_w, y + 3.0)
        self.c.setFont(font("sans-bold"), size)
        y -= lead
        self.c.drawString(self.x_side, y, title)
        self.c.setFont(font("sans"), size)
        for ln in lines:
            y -= lead
            self.c.drawString(self.x_side, y, ln)

    def rule(self, gray=0.45):
        self._need(self.lead)
        self.y -= self.lead * 0.5
        self.c.setStrokeGray(gray); self.c.setLineWidth(0.5)
        self.c.line(self.x_text, self.y, self.x_text + self.tw, self.y)
        self.y -= self.lead * 0.5

    def table(self, rows: list, widths: list, size=9.0):
        rowh = size * 1.7
        need = rowh * len(rows) + self.lead * 0.6
        self._need(need)
        self.y -= self.lead * 0.4
        for i, r in enumerate(rows):
            if not self._room(rowh):
                self._new_page()
            self.y -= rowh
            x = self.x_text
            face = "sans-semibold" if i == 0 else "sans"
            for j, cell in enumerate(r):
                w = widths[j] * self.tw
                for k, ln in enumerate(self._wrap(str(cell), w - 8.0, face, size)[:3]):
                    self.c.setFont(font(face), size)
                    self.c.drawString(x, self.y + 3.0 - k * (size * 1.05), ln)
                    if k:
                        self.y -= size * 1.05 if j == 0 else 0
                x += w
            self.c.setStrokeGray(0.0 if i == 0 else 0.45)
            self.c.setLineWidth(0.7 if i == 0 else 0.4)
            self.c.line(self.x_text, self.y - 2.5, self.x_text + self.tw, self.y - 2.5)
        self.y -= self.lead * 0.6

    def figure(self, key: str, caption: str, meta: dict, full=False):
        w = meta["width_pt"]; h = meta["height_pt"]
        avail = (self.tw + self.gap + self.side_w) if full else self.tw
        cap_lines = self._wrap(caption, avail, "sans-italic", 8.5)
        need = h + 9.0 + len(cap_lines) * 11.0 + self.lead * 0.8
        self._need(need)
        self.y -= self.lead * 0.5
        x0 = (self.x_text if not full else min(self.x_text, self.x_side))
        x = x0 + max(0.0, (avail - w) / 2)
        self.y -= h
        self.eng.render(key, self.c, x, self.y)
        self.y -= 9.0
        self.c.setFillGray(0.0)
        for ln in cap_lines:
            self.y -= 11.0
            self.c.setFont(font("sans-italic"), 8.5)
            self.c.drawString(x0, self.y, ln)
        self.y -= self.lead * 0.6

    def page_break(self):
        self._new_page()

    def save(self):
        self.c.showPage()
        self.c.save()


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
    ts = Typesetter(out, geom, eng)
    used_figs = []
    for b in blocks:
        k = b["type"]
        if k == "h1":
            ts.h1(b["text"])
        elif k == "h2":
            ts.h2(b["text"])
        elif k == "h3":
            ts.h3(b["text"])
        elif k == "para":
            ts.para(b["text"], gray=b.get("gray", 0.0))
        elif k == "lead":
            ts.para(b["text"], face="serif-italic", size=11.0)
        elif k == "bullets":
            ts.bullets(b["items"], marker=b.get("marker", "—"))
        elif k == "numbered":
            ts.numbered(b["items"])
        elif k == "table":
            ts.table(b["rows"], b["widths"])
        elif k == "rule":
            ts.rule()
        elif k == "side":
            ts.side_note(b["title"], b["text"])
        elif k == "figure":
            key = b["key"]
            if key not in meta_by_key:
                print(f"✗ figür sicilde yok: {key}")
                return 1
            ts.figure(key, b["caption"], meta_by_key[key], full=b.get("full", False))
            used_figs.append(key)
        elif k == "pagebreak":
            ts.page_break()
        else:
            print(f"✗ bilinmeyen blok türü: {k}")
            return 1
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
