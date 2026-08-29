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
        self._outline: list = []
        self._head_page = None      # bu sayfada en son bir başlık çizildi mi
        self._side_used = None      # bu sayfada yan notun indiği en alt nokta
        self._side_pending: list = []
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
        self._side_used = None
        pending, self._side_pending = self._side_pending, []
        recto = self.page % 2 == 1
        gut = self.g["margins"]["gutter_pt"]; out = self.g["margins"]["outside_pt"]
        self._deferred = pending
        self.x_text = gut if recto else out
        self.x_side = self.x_text + self.tw + self.gap
        if not recto:
            self.x_text = out + self.side_w + self.gap
            self.x_side = out
        self.y = self.top
        for t, b in getattr(self, "_deferred", []):
            self.side_note(t, b)
        self._deferred = []

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
            self._flow_page()

    def _flow_page(self):
        """AKIŞ içinde sayfa açar — yeni sayfa KESİN mürekkep alacaktır.

        ⚠ Faz 5'te ÖLÇÜLEN kusur: `_new_page()` `_dirty` bayrağını
        sıfırlar, ama çizim yordamları `_touch()`'ı yalnızca BAŞTA bir
        kez çağırır. Bir paragrafın/listenin/tablonun taşan kuyruğu yeni
        sayfaya düştüğünde o sayfa "kirli" sayılmıyordu ve `_close_page`
        sayfa mobilyasını HİÇ yazmıyordu: sayfa 46 ve 236 metin taşıyıp
        SAYFA NUMARASI TAŞIMIYORDU. Akış içindeki her sayfa açılışı
        buradan geçer ve sayfayı derhâl işaretler.
        Regresyon: 07_TESTS/selftest.py § test_flowed_page_keeps_folio
        """
        self._new_page()
        self._touch()

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
                self._flow_page(); self.c.setFillGray(gray)
            self.y -= lead
            self.c.setFont(font(face), size)
            self.c.drawString(self.x_text + indent, self.y, ln)
        self.y -= (self.lead * 0.45 if space_after is None else space_after)
        self.c.setFillGray(0.0)

    def outline(self, title: str, level: int = 0):
        """PDF ana hattına bir giriş ekler.

        İkinci çelişmeli inceleme (A-05): PDF sıfır outline girişi
        taşıyordu. 231 sayfalık bir BAŞVURU kitabında bu, dijital
        okurun içeri girecek hiçbir kapısı olmaması demektir."""
        key = f"sec{len(self._outline)}"
        self.c.bookmarkPage(key)
        self.c.addOutlineEntry(title, key, level=level, closed=(level == 0))
        self._outline.append((title, level, self.page))

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
        self._head_page = None
        self._need(self.lead * 3.2)
        self.y -= self.lead * 1.1
        self.c.setFont(font("sans-semibold"), 13.0)
        for ln in self._wrap(s, self.tw, "sans-semibold", 13.0):
            self.c.drawString(self.x_text, self.y, ln)
            self.y -= self.lead * 0.75
        self.y -= self.lead * 0.05
        self._head_page = self.page

    def h3(self, s: str):
        self._touch()
        self._head_page = None
        self._need(self.lead * 2.6)
        self.y -= self.lead * 0.85
        self.c.setFont(font("sans-semibold"), 10.5)
        for ln in self._wrap(s, self.tw, "sans-semibold", 10.5):
            self.c.drawString(self.x_text, self.y, ln)
            self.y -= self.lead * 0.62
        self.y -= self.lead * 0.02
        self._head_page = self.page

    # ── BAŞLIK İÇERİĞİNDEN AYRILMAZ ───────────────────────────────────
    # ⚠ Faz 5: tabloyu/listeyi bütün tutma kuralı bir kusuru başka bir
    # kusurla değişti — başlık ve giriş paragrafı bir sayfada, tablo
    # ötekinde kalıyordu (s. 238, s. 245). Bir başlık, ardındaki İLK
    # BÖLÜNMEZ PARÇAYLA birlikte yer bulamıyorsa onunla birlikte kayar.
    # Ölçüm `run_blocks` seviyesinde yapılır; yalnızca orada ileriye
    # bakılabilir.
    # Regresyon: 07_TESTS/selftest.py § test_heading_travels_with_its_content

    def head_h(self, kind: str) -> float:
        return {"h1": self.lead * 4.0, "h2": self.lead * 3.2,
                "h3": self.lead * 2.6}.get(kind, 0.0)

    def table_h(self, rows: list, widths: list, size=9.0, row_pt=None,
                keep_after_pt: float = 0.0, full: bool = False) -> float:
        rowh = float(row_pt) if row_pt else size * 1.7
        tw = (self.tw + self.gap + self.side_w) if full else self.tw
        h = self.lead * 0.4 + self.lead * 0.6 + keep_after_pt
        for i, r in enumerate(rows):
            cells = [self._wrap(str(c), widths[j] * tw - 8.0,
                                "sans-semibold" if i == 0 else "sans", size)[:8]
                     for j, c in enumerate(r)]
            h += rowh + (max(max(len(c), 1) for c in cells) - 1) * size * 1.12
        return h

    def chunk_h(self, b: dict, meta: dict) -> float:
        """Bloğun BÖLÜNMEDEN yerleşmesi gereken en küçük yüksekliği."""
        k = b.get("type")
        page = self.top - self.bottom
        if k in ("para", "lead"):
            n = len(self._wrap(str(b.get("text", "")), self.tw, "serif", self.body))
            return min(n, 2) * self.lead
        if k in ("bullets", "numbered"):
            pad = 14.0 if k == "bullets" else 18.0
            n = sum(len(self._wrap(str(x), self.tw - pad, "serif", self.body))
                    for x in (b.get("items") or []))
            # min_tail + 1: kısa listeler TAMAMEN ayrılır, böylece
            # `_no_widow_break` başlığı yalnız bırakacak bir kaçış
            # yapmak zorunda kalmaz (iki kuralın çeliştiği yer).
            return min(n, 3) * self.lead
        if k in ("table", "figtable"):
            if k == "figtable":
                m = meta.get(b.get("key"))
                if not m or "data" not in m:
                    return 3 * self.lead
                rows = m["data"]; widths = b.get("widths") or m["col_ratio"]
                cap = b.get("caption") or ""
                cap_h = (self.lead * (len(self._wrap(cap, self.tw, "sans-italic", 8.5))
                                      + 1.05)) if cap else 0.0
            else:
                rows = b["rows"]; widths = b["widths"]; cap_h = 0.0
            # BOŞ FORM (row_pt verilmiş) bölünmez: yarısı bir sayfada
            # olan bir form doldurulamaz. Veri tablosu bölünebilir;
            # onun için yalnızca üç satırlık bir baş yer ayrılır.
            if b.get("row_pt"):
                tot = self.table_h(rows, widths, row_pt=b["row_pt"],
                                   keep_after_pt=cap_h)
                if tot <= page:
                    return tot
            return (9.0 * 1.7) * 3 + self.lead * 0.6 + cap_h
        if k == "figure":
            m = meta.get(b.get("key"))
            if not m:
                return 3 * self.lead
            avail = (self.tw + self.gap + self.side_w) if b.get("full") else self.tw
            cl = self._wrap(str(b.get("caption", "")), avail, "sans-italic", 8.5)
            return m["height_pt"] + 9.0 + len(cl) * 11.0 + self.lead * 0.8
        if k == "callout":
            n = sum(len(self._wrap(str(x), self.tw - 26.0, "serif", self.body - 0.5))
                    for x in (b.get("items") or []))
            return min(n + 1, 4) * self.lead
        return 0.0

    def full_h(self, b: dict, meta: dict) -> float:
        """Bloğun TAM yüksekliği (ilk parçası değil)."""
        k = b.get("type")
        if k in ("para", "lead"):
            return len(self._wrap(str(b.get("text", "")), self.tw, "serif",
                                  self.body)) * self.lead + self.lead * 0.45
        if k in ("bullets", "numbered"):
            pad = 14.0 if k == "bullets" else 18.0
            n = sum(len(self._wrap(str(x), self.tw - pad, "serif", self.body))
                    for x in (b.get("items") or []))
            return n * self.lead + self.lead * 0.45
        return self.chunk_h(b, meta)

    def reserve_group(self, blocks: list, i: int, meta: dict):
        """Başlık + ona yapışık metin + (varsa) ONA AİT FİGÜR.

        ⚠ Faz 5'te ÖLÇÜLEN kusur: Bölüm 2'de her ölçü birimi
        `h3 → para → bullets → figure` sırasındadır. Ayırma yalnızca ilk
        paragrafa kadar bakıyordu, figür 4. bloktaydı ve HİÇBİR ZAMAN
        aynı sayfaya sığmıyordu. Sonuç: 29 ölçüm figürünün hepsi kendi
        metninden BİR SAYFA SONRA basılıyor, üstelik BİR SONRAKİ ölçünün
        başlığının hemen ÜSTÜNDE duruyordu — okur şeridin yolunu yanlış
        ölçüye ait sanır. Birim bir sayfaya sığıyorsa artık bütün ayrılır.
        Regresyon: 07_TESTS/selftest.py § test_measurement_figure_travels_with_its_text
        """
        page = self.top - self.bottom
        ATTACH = ("para", "lead", "bullets", "numbered")
        # ① başlık + yapışık metin + İLK FİGÜR bir sayfaya sığıyor mu
        h = self.head_h(blocks[i]["type"])
        j = i + 1
        while j < len(blocks) and j - i <= 5:
            k = blocks[j].get("type")
            if k == "figure":
                h += self.chunk_h(blocks[j], meta)
                if h <= page:
                    self._need(h)
                    return
                break
            if k not in ATTACH:
                break
            h += self.full_h(blocks[j], meta)
            j += 1
        # ② genel kural: başlık + yapışık paragraflar + ilk bölünmez parça
        h = self.head_h(blocks[i]["type"])
        j = i + 1
        while j < len(blocks) and blocks[j].get("type") in ("para", "lead") \
                and j - i <= 3:
            h += self.chunk_h(blocks[j], meta)
            j += 1
        if j < len(blocks):
            h += self.chunk_h(blocks[j], meta)
        self._need(min(h, page))

    def _no_widow_break(self, line_counts: list, lead: float, min_tail: int = 2):
        """Bir listenin kuyruğunda dul satır kalacaksa listeyi bütün taşır.

        ⚠ Faz 5'te ÖLÇÜLEN kusur: s. 236'nın TEK içeriği üç maddelik bir
        listenin son maddesiydi. Liste bir sayfaya sığıyorsa ve
        bölünmesi kuyrukta `min_tail`'den az satır bırakacaksa, liste
        BAŞLAMADAN önce sayfa çevrilir.
        Regresyon: 07_TESTS/selftest.py § test_list_tail_is_not_widowed
        """
        total = sum(line_counts)
        if total == 0:
            return
        if total * lead > (self.top - self.bottom):
            return                       # tek sayfaya zaten sığmıyor
        room = int((self.y - self.bottom) // lead)
        if room >= total:
            return                       # tamamı sığıyor
        if total - room < min_tail:
            # Başlık BU sayfadaysa listeyi tümden taşımak başlığı yalnız
            # bırakır — dul bir satır, sahipsiz bir başlıktan iyidir.
            if self._head_page == self.page:
                return
            self._flow_page()

    def bullets(self, items: list, marker="—"):
        self._touch()
        wrapped = [self._wrap(it, self.tw - 14.0, "serif", self.body)
                   for it in items]
        self._no_widow_break([len(w) for w in wrapped], self.lead)
        for lines in wrapped:
            self._need(min(len(lines), 2) * self.lead)
            first = True
            for ln in lines:
                if not self._room(self.lead):
                    self._flow_page()
                self.y -= self.lead
                self.c.setFont(font("serif"), self.body)
                if first:
                    self.c.drawString(self.x_text, self.y, marker)
                    first = False
                self.c.drawString(self.x_text + 14.0, self.y, ln)
        self.y -= self.lead * 0.45

    def numbered(self, items: list, start: int = 1):
        self._touch()
        wrapped = [self._wrap(it, self.tw - 18.0, "serif", self.body)
                   for it in items]
        self._no_widow_break([len(w) for w in wrapped], self.lead)
        for i, lines in enumerate(wrapped, start):
            self._need(min(len(lines), 2) * self.lead)
            first = True
            for ln in lines:
                if not self._room(self.lead):
                    self._flow_page()
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
        # ⚠ Faz 5'te ÖLÇÜLEN kusur: GÖVDE sarılıyordu, BAŞLIK sarılmıyordu.
        # 36 yan notun 3'ünün başlığı 108 pt'lik sütundan taşıyordu ve
        # `drawString` hiçbir sınır tanımadığı için taşan kısım komşu
        # alana BASILIYORDU: verso sayfada metin bloğunun üstüne
        # (s. 50'de 4,3 pt, s. 72'de 33,2 pt — harfler üst üste),
        # recto sayfada dış kenar boşluğuna (s. 61'de 17,4 pt).
        # Başlık artık gövdeyle AYNI genişliğe sarılır.
        # Regresyon: 07_TESTS/selftest.py § test_side_note_title_stays_in_column
        title_lines = self._wrap(title, self.side_w - 8.0, "sans-bold", size)
        need = lead * (len(lines) + len(title_lines) + 0.6)
        y = self.y + self.lead
        # ⚠ İlk sürüm yer kalmadığında koşulsuz `self.top`'a atlıyordu.
        # İki sorun: (a) aynı sayfadaki İKİNCİ bir yan not birincinin
        # ÜZERİNE yazıyordu, (b) üst bilgiyle çakışabiliyordu. Notlar
        # artık sayfa başına YIĞILIR ve sığmıyorsa bir sonraki sayfaya
        # bırakılır — üst üste basılmaz.
        floor = self._side_used if self._side_used is not None else self.top
        if y - need < self.bottom or y > floor:
            y = floor
        if y - need < self.bottom:
            self._side_pending.append((title, body))
            return
        self._side_used = y - need - lead * 0.6
        self.c.setStrokeGray(0.0); self.c.setLineWidth(0.7)
        self.c.line(self.x_side, y + 3.0, self.x_side + self.side_w, y + 3.0)
        self.c.setFont(font("sans-bold"), size)
        for ln in title_lines:
            y -= lead
            self.c.drawString(self.x_side, y, ln)
        self.c.setFont(font("sans"), size)
        for ln in lines:
            y -= lead
            self.c.drawString(self.x_side, y, ln)

    def toc_line(self, title: str, page: int, level: int = 0):
        """İçindekiler satırı — nokta lideriyle."""
        self._touch()
        size = self.body - (0.5 if level else 0.0)
        face = "sans-semibold" if level == 0 else "sans"
        indent = 0.0 if level == 0 else 14.0
        self._need(self.lead)
        if not self._room(self.lead):
            self._flow_page()
        self.y -= self.lead * (1.0 if level else 1.25)
        self.c.setFont(font(face), size)
        self.c.drawString(self.x_text + indent, self.y, title)
        num = str(page)
        self.c.drawRightString(self.x_text + self.tw, self.y, num)
        w1 = pdfmetrics.stringWidth(title, font(face), size) + indent
        w2 = pdfmetrics.stringWidth(num, font(face), size)
        gap_l = self.x_text + w1 + 5.0
        gap_r = self.x_text + self.tw - w2 - 5.0
        if gap_r > gap_l:
            self.c.setFillGray(0.55)
            self.c.setFont(font("sans"), size)
            dot_w = pdfmetrics.stringWidth(" .", font("sans"), size)
            n = max(0, int((gap_r - gap_l) / dot_w))
            self.c.drawString(gap_l, self.y, " ." * n)
            self.c.setFillGray(0.0)

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
                    self._flow_page(); y0 = self.y
                self.y -= self.lead * 0.92
                self.c.setFont(font("sans"), size)
                self.c.drawString(self.x_text + 14.0 + (0 if first else 8.0), self.y, ln)
                first = False
        self.c.setStrokeGray(rule_gray); self.c.setLineWidth(2.2)
        self.c.line(self.x_text + 4.0, y0, self.x_text + 4.0, self.y - 3.0)
        self.y -= self.lead * 0.75

    def table(self, rows: list, widths: list, size=9.0, row_pt=None,
              keep_after_pt: float = 0.0, full: bool = False):
        """keep_after_pt: SON satırın altında ayrılacak yer.

        ⚠ Faz 5'te ÖLÇÜLEN kusur: `figtable` bloğu önce tabloyu, sonra
        AYRI bir `para()` ile başlığı diziyordu. Tablo sayfanın dibinde
        bittiğinde başlık tek başına sonraki sayfaya düşüyordu —
        s. 46'nın TEK içeriği ölçü kartının başlığıydı. Son satır artık
        altındaki başlığa yer kalmıyorsa birlikte kayar.
        Regresyon: 07_TESTS/selftest.py § test_figtable_caption_is_not_orphaned
        """
        self._touch()
        tw = (self.tw + self.gap + self.side_w) if full else self.tw
        x0 = min(self.x_text, self.x_side) if full else self.x_text
        # Boş bir form ELLE DOLDURULUR. 9 pt metin satırı (15,3 pt ≈ 5,4 mm)
        # okunur ama YAZILAMAZ. Form satırları ayrıca belirtilir.
        rowh = float(row_pt) if row_pt else size * 1.7
        # Tablo + başlığı bir sayfaya SIĞIYORSA bölünmez: bir formun
        # yarısı bir sayfada, başlığı ötekinde işe yaramaz. Sığmıyorsa
        # eski davranış sürer ve tablo satır satır bölünür.
        if row_pt:
            all_h = self.table_h(rows, widths, size=size, row_pt=row_pt,
                                 keep_after_pt=keep_after_pt)
            if all_h <= (self.top - self.bottom) and not self._room(all_h):
                self._flow_page()
            else:
                self._need(rowh * min(len(rows), 3) + self.lead * 0.6)
        else:
            self._need(rowh * min(len(rows), 3) + self.lead * 0.6 + keep_after_pt)
        self.y -= self.lead * 0.4
        for i, r in enumerate(rows):
            # ⚠ Satır başına en fazla ÜÇ satır sarılıyordu ve fazlası
            # SESSİZCE ATILIYORDU. Kaynak ekinde bu, bir yayının ne için
            # kullanıldığının yarısının kaybolması demekti. Sınır bir
            # emniyet payıdır, bir biçim tercihi değil: sekize çıkarıldı
            # ve aşılırsa metin kesilmez, satır uzar.
            cells = [self._wrap(str(cell), widths[j] * tw - 8.0,
                                "sans-semibold" if i == 0 else "sans", size)[:8]
                     for j, cell in enumerate(r)]
            # ⚠ Faz 5'te ÖLÇÜLEN kusur: BOŞ bir hücre `_wrap("") == []`
            # döndürüyor, yani 0 satır. `(0 - 1) * 9 * 1,12` NEGATİFTİR
            # ve satır yüksekliğini 15,3 pt'den 5,22 pt'ye (1,84 mm)
            # düşürüyordu. Bütün BOŞ FORMLAR bu yüzden yazılamaz
            # hâldeydi — Faz 4 çelişmeli incelemesinin R5 bulgusu
            # ("2 mm'lik saç teli satırlar") DÜZELMEMİŞTİ, çünkü
            # düzeltme `row_pt`'ye yazılmıştı ve bu çarpan onu da
            # aşağı çekiyordu (26 pt → 15,9 pt).
            # Regresyon: 07_TESTS/selftest.py § test_blank_form_rows_are_writable
            h = rowh + (max(max(len(c), 1) for c in cells) - 1) * size * 1.12
            tail = keep_after_pt if i == len(rows) - 1 else 0.0
            if not self._room(h + tail):
                self._flow_page()
            self.y -= h
            x = x0
            face = "sans-semibold" if i == 0 else "sans"
            for j, lines in enumerate(cells):
                self.c.setFont(font(face), size)
                for k, ln in enumerate(lines):
                    self.c.drawString(x, self.y + h - rowh + 3.0 - k * (size * 1.12), ln)
                x += widths[j] * tw
            self.c.setStrokeGray(0.0 if i == 0 else 0.45)
            self.c.setLineWidth(0.7 if i == 0 else 0.4)
            self.c.line(x0, self.y - 2.5, x0 + tw, self.y - 2.5)
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
    for _i, b in enumerate(blocks):
        k = b["type"]
        if k in ("h2", "h3"):
            ts.reserve_group(blocks, _i, meta_by_key)
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
            # Başlık tablodan AYRI bir bloktur; son satırla birlikte
            # kalması için yüksekliği tabloya bildirilir (s. 46 kusuru).
            cap = b.get("caption") or ""
            cap_h = 0.0
            if cap:
                cap_h = ts.lead * (len(ts._wrap(cap, ts.tw, "sans-italic", 8.5))
                                   + 1.05)
            ts.table(m["data"], b.get("widths") or m["col_ratio"],
                     row_pt=b.get("row_pt"), keep_after_pt=cap_h,
                     full=bool(b.get("row_pt")))
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
