#!/usr/bin/env python3
"""
typeset.py — TEK dizgi motoru.

⚠ NEDEN AYRI BİR DOSYA: Faz 3'te dizgi kodu `build_pilot.py`'nin
içindeydi. Faz 4 tam kitabı dizmek zorunda ve o kodu KOPYALAMAK iki
dizgi yolu yaratırdı — figür sisteminde bilinçle kaçınılan şeyin
(`figure_engine.render()` tek yoldur) dizgi katmanındaki tekrarı.
İki yol olsaydı pilotun 8 sayfası ile kitabın aynı bölümü FARKLI
dizilebilirdi ve fark testi (`D-01`) karşılaştırılamaz hâle gelirdi.

Desen: `trfold.py` (K16) — bir davranış, bir kopya.

Bu modül SAYFA bilir, İÇERİK bilmez. Ne bölüm ne kitap kavramı vardır;
yalnızca blok dizer ve nerede olduğunu söyler. Bölüm/parça/ön-arka
madde `build_book.py`'nin işidir.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_tokens import font, register_fonts  # noqa: E402

from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402


class Typesetter:
    """Bir PDF'e blok dizer.

    running_head verilirse her sayfaya bir üst bilgi yazılır; pilot
    MARKASIZ olmak zorunda olduğu için orada None geçilir.
    """

    def __init__(self, out: Path, geom: dict, engine, *, running_head=None,
                 start_page: int = 1, folio: bool = True):
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
        self.page = start_page - 1
        self.folio = folio
        # Bir sayfaya bir şey çizildi mi. Yayıncılık konvansiyonu: boş
        # sayfa SAYILIR ama NUMARALANMAZ. Bunu bilmek için sayfanın
        # kapanışını beklemek gerekir — bu yüzden üst bilgi ve folyo
        # sayfa AÇILIŞINDA değil KAPANIŞINDA yazılır.
        self._dirty = False
        self.running_head = running_head
        self._head_left = None
        self._head_right = None
        self.figures_used: list = []
        self._new_page()

    # ── sayfa ─────────────────────────────────────────────────────────
    def set_running_head(self, left: str | None, right: str | None):
        """Sol sayfa: parça/kitap · sağ sayfa: bölüm. Sonraki sayfadan geçerli."""
        self._head_left, self._head_right = left, right

    def _new_page(self):
        if self.page:
            self._close_page()
            self.c.showPage()
        self.page += 1
        self._dirty = False
        recto = self.page % 2 == 1
        gut = self.g["margins"]["gutter_pt"]; out = self.g["margins"]["outside_pt"]
        self.x_text = gut if recto else out
        self.x_side = self.x_text + self.tw + self.gap
        if not recto:
            self.x_text = out + self.side_w + self.gap
            self.x_side = out
        self.y = self.top

    def _close_page(self):
        """Sayfa kapanırken sayfa mobilyasını yaz — BOŞSA YAZMA."""
        if self._dirty:
            self._chrome(self.page % 2 == 1)

    def _touch(self):
        self._dirty = True

    def _chrome(self, recto: bool):
        head = self._head_right if recto else self._head_left
        if head:
            self.c.setFillGray(0.45)
            self.c.setFont(font("sans"), 7.5)
            x = self.x_text if recto else self.x_side
            w = self.tw if recto else self.side_w
            if recto:
                self.c.drawRightString(self.x_text + self.tw, self.top + 16.0, head)
            else:
                self.c.drawString(self.x_side, self.top + 16.0, head)
            del w, x
        if self.folio:
            self.c.setFillGray(0.45)
            self.c.setFont(font("sans"), 7.5)
            self.c.drawCentredString(self.W / 2, self.bottom - 22.0, str(self.page))
        self.c.setFillGray(0.0)

    def _room(self, h: float) -> bool:
        return self.y - h >= self.bottom

    def _need(self, h: float):
        if not self._room(h):
            self._new_page()

    def page_break(self):
        self._new_page()

    def start_recto(self):
        """Bölüm açılışı TEK sayfada başlar — kitap konvansiyonu."""
        if self.y < self.top - 1e-6:
            self._new_page()
        if self.page % 2 == 0:
            self._new_page()

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
             space_after=None, gray=0.0, width=None):
        self._touch()
        size = size or self.body
        lead = lead or self.lead
        w = (width or self.tw) - indent
        lines = self._wrap(s, w, face, size)
        self._need(min(len(lines), 2) * lead)
        self.c.setFillGray(gray)
        for ln in lines:
            if not self._room(lead):
                self._new_page(); self.c.setFillGray(gray)
            self.y -= lead
            self.c.setFont(font(face), size)
            self.c.drawString(self.x_text + indent, self.y, ln)
        self.y -= (self.lead * 0.45 if space_after is None else space_after)
        self.c.setFillGray(0.0)

    def h1(self, s: str, kicker: str | None = None):
        self._touch()
        self._need(self.lead * 4)
        self.y -= self.lead * 1.4
        if kicker:
            self.c.setFillGray(0.45)
            self.c.setFont(font("sans-semibold"), 9.0)
            self.c.drawString(self.x_text, self.y, kicker.upper())
            self.c.setFillGray(0.0)
            # 9 pt kicker'dan 20 pt başlığa geçiş: 0,85 satır (12,3 pt)
            # 20 pt bir harf yüksekliğinin ALTINDADIR ve iki satır
            # birbirine giriyordu. Sayfaya BAKILARAK bulundu; hiçbir
            # otomatik kapı iki metin bloğunun çakıştığını görmüyor.
            self.y -= self.lead * 1.55
        self.c.setFont(font("sans-bold"), 20.0)
        for ln in self._wrap(s, self.tw, "sans-bold", 20.0):
            self.c.drawString(self.x_text, self.y, ln)
            self.y -= self.lead * 1.05
        self.y += self.lead * 0.15

    def h2(self, s: str):
        self._touch()
        self._need(self.lead * 3.2)
        self.y -= self.lead * 1.1
        self.c.setFont(font("sans-semibold"), 13.0)
        for ln in self._wrap(s, self.tw, "sans-semibold", 13.0):
            self.c.drawString(self.x_text, self.y, ln)
            self.y -= self.lead * 0.75
        self.y -= self.lead * 0.05

    def h3(self, s: str):
        self._touch()
        self._need(self.lead * 2.6)
        self.y -= self.lead * 0.85
        self.c.setFont(font("sans-semibold"), 10.5)
        for ln in self._wrap(s, self.tw, "sans-semibold", 10.5):
            self.c.drawString(self.x_text, self.y, ln)
            self.y -= self.lead * 0.62
        self.y -= self.lead * 0.02

    def bullets(self, items: list, marker="—"):
        self._touch()
        for it in items:
            lines = self._wrap(it, self.tw - 14.0, "serif", self.body)
            self._need(min(len(lines), 2) * self.lead)
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

    def numbered(self, items: list, start: int = 1):
        self._touch()
        for i, it in enumerate(items, start):
            lines = self._wrap(it, self.tw - 18.0, "serif", self.body)
            self._need(min(len(lines), 2) * self.lead)
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
                self.c.drawString(self.x_text + 18.0, self.y, ln)
        self.y -= self.lead * 0.45

    def side_note(self, title: str, body: str):
        """Yan sütun notu — gövde akışını KESMEZ (K39)."""
        self._touch()
        size = 8.0; lead = 10.4
        lines = self._wrap(body, self.side_w - 8.0, "sans", size)
        y = self.y + self.lead
        if y - lead * (len(lines) + 1.6) < self.bottom:
            y = self.top
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
        self._touch()
        self._need(self.lead)
        self.y -= self.lead * 0.5
        self.c.setStrokeGray(gray); self.c.setLineWidth(0.5)
        self.c.line(self.x_text, self.y, self.x_text + self.tw, self.y)
        self.y -= self.lead * 0.5

    def callout(self, title: str, lines_in: list, *, rule_gray=0.0):
        """DO NOT CHANGE YET kutusu — kitabın imza uyarı formu.

        Kenarlık yok: kutu çizgisi 1-bit baskıda gri bir bloğa dönüşür.
        Sol kenarda kalın bir kural + sans başlık yeterli ve daha ucuz.
        """
        self._touch()
        size = self.body - 0.5
        wrapped = []
        for it in lines_in:
            wrapped.append(self._wrap(it, self.tw - 22.0, "sans", size))
        need = self.lead * 1.5 + sum(len(w) for w in wrapped) * (self.lead * 0.92)
        self._need(min(need, self.lead * 5))
        self.y -= self.lead * 0.7
        y0 = self.y + self.lead * 0.55
        self.c.setFont(font("sans-bold"), size + 0.5)
        self.y -= self.lead * 0.85
        self.c.drawString(self.x_text + 14.0, self.y, title.upper())
        for w in wrapped:
            first = True
            for ln in w:
                if not self._room(self.lead * 0.92):
                    self.c.setStrokeGray(rule_gray); self.c.setLineWidth(2.2)
                    self.c.line(self.x_text + 4.0, y0, self.x_text + 4.0, self.y - 3.0)
                    self._new_page(); y0 = self.y
                self.y -= self.lead * 0.92
                self.c.setFont(font("sans"), size)
                self.c.drawString(self.x_text + 14.0 + (0 if first else 8.0), self.y, ln)
                first = False
        self.c.setStrokeGray(rule_gray); self.c.setLineWidth(2.2)
        self.c.line(self.x_text + 4.0, y0, self.x_text + 4.0, self.y - 3.0)
        self.y -= self.lead * 0.75

    def table(self, rows: list, widths: list, size=9.0):
        self._touch()
        rowh = size * 1.7
        self._need(rowh * min(len(rows), 3) + self.lead * 0.6)
        self.y -= self.lead * 0.4
        for i, r in enumerate(rows):
            cells = [self._wrap(str(cell), widths[j] * self.tw - 8.0,
                                "sans-semibold" if i == 0 else "sans", size)[:3]
                     for j, cell in enumerate(r)]
            h = rowh + (max(len(c) for c in cells) - 1) * size * 1.12
            if not self._room(h):
                self._new_page()
            self.y -= h
            x = self.x_text
            face = "sans-semibold" if i == 0 else "sans"
            for j, lines in enumerate(cells):
                self.c.setFont(font(face), size)
                for k, ln in enumerate(lines):
                    self.c.drawString(x, self.y + h - rowh + 3.0 - k * (size * 1.12), ln)
                x += widths[j] * self.tw
            self.c.setStrokeGray(0.0 if i == 0 else 0.45)
            self.c.setLineWidth(0.7 if i == 0 else 0.4)
            self.c.line(self.x_text, self.y - 2.5, self.x_text + self.tw, self.y - 2.5)
        self.y -= self.lead * 0.6

    def figure(self, key: str, caption: str, meta: dict, full=False):
        self._touch()
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
        self.figures_used.append(key)
        self.y -= 9.0
        self.c.setFillGray(0.0)
        for ln in cap_lines:
            self.y -= 11.0
            self.c.setFont(font("sans-italic"), 8.5)
            self.c.drawString(x0, self.y, ln)
        self.y -= self.lead * 0.6

    def save(self):
        # Son sayfanın mobilyası kapanışta yazılır; showPage onu emit eder.
        #
        # ⚠ DÜZELTME KAYDI: burada bir "fazladan boş sayfa" hatası
        # olduğunu sandım. YOKTU. pdftotext'in çıktısı sondaki form-feed
        # yüzünden N+1 parça veriyor; pdfinfo sayfa sayısını 230 olarak
        # doğruluyor. Bir ölçüm aracının biçimi, ölçtüğü şeyin özelliği
        # sanılmamalıdır.
        self._close_page()
        self.c.showPage()
        self.c.save()


# ── blok yürütücü — build_pilot ve build_book AYNI yolu kullanır ──────
def run_blocks(ts: Typesetter, blocks: list, meta_by_key: dict) -> list:
    """Blokları dizer. Bilinmeyen blok türü SESSİZCE ATLANMAZ — patlar."""
    errors: list = []
    for b in blocks:
        k = b["type"]
        if k == "h1":
            ts.h1(b["text"], kicker=b.get("kicker"))
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
            ts.numbered(b["items"], start=b.get("start", 1))
        elif k == "table":
            ts.table(b["rows"], b["widths"])
        elif k == "figtable":
            # Sicildeki tablo figürü — metin ızgarasında dizilir.
            # Veri figür kaydından gelir; ikinci bir kopya YOKTUR.
            m = meta_by_key.get(b["key"])
            if m is None or "data" not in m:
                errors.append(f"tablo figürü sicilde yok ya da verisi eksik: {b['key']}")
                continue
            ts.table(m["data"], b.get("widths") or m["col_ratio"])
            # Sicilden gelen bir tablo da BİR FİGÜRDÜR. Sayılmazsa figür
            # bütçesi (§ 25) gerçekten kullanılanı göstermez.
            ts.figures_used.append(b["key"])
            if b.get("caption"):
                ts.para(b["caption"], face="sans-italic", size=8.5)
        elif k == "rule":
            ts.rule()
        elif k == "side":
            ts.side_note(b["title"], b["text"])
        elif k == "callout":
            ts.callout(b["title"], b["items"])
        elif k == "figure":
            key = b["key"]
            if key not in meta_by_key:
                errors.append(f"figür sicilde yok: {key}")
                continue
            ts.figure(key, b["caption"], meta_by_key[key], full=b.get("full", False))
        elif k == "pagebreak":
            ts.page_break()
        elif k == "recto":
            ts.start_recto()
        else:
            errors.append(f"bilinmeyen blok türü: {k}")
    return errors
