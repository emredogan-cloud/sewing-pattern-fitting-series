#!/usr/bin/env python3
"""
figure_engine.py — figürleri KAYIT VERİSİNDEN üreten motor.

Faz 2 / G3–G4 (BOOK-01/00_SPEC/PHASE_2_ROADMAP.md).

İlke: bir figür elle çizilen bir resim değil, bir kaydın GÖRÜNTÜSÜDÜR.
`fit_signs.json` değişirse akış şeması değişir; `measurements.json`
değişirse ölçüm figürü değişir. Böylece taksonomi ile kitap arasında
sessiz bir kayma OLUŞAMAZ.

Üretilen her figür için bir `figures.json` kaydı yazılır ve o kaydın
`notation_tokens` listesi ÖLÇÜLÜR — çizim sırasında gerçekten kullanılan
token'lardan türetilir, elle beyan edilmez.

Çıktı: BOOK-xx/03_VISUAL/generated/*.pdf (gitignore) +
       BOOK-xx/03_VISUAL/figures.json (izlenir)

Kullanım:
  python3 06_BUILD/figure_engine.py --book book-01
  python3 06_BUILD/figure_engine.py --book book-01 --measure-only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from figure_tokens import FigureCanvas, ForbiddenDrawing  # noqa: E402
from croquis import Croquis, LEVEL, fit as croquis_fit  # noqa: E402

# ── ölçüm figürü tarifleri ────────────────────────────────────────────
# Her ölçü için: hangi görünüş, hangi yol türü, hangi iki işaret noktası.
# Bu tablo `measurements.json`'daki landmark_start/landmark_end
# METİNLERİNİN krokideki karşılığıdır — metin serbesttir, kroki değildir.
GIRTH = "girth"; VERT = "vertical"; HORZ = "horizontal"; DERIVED = "derived"
LIMB_LEVELS = {"bicep", "elbow", "wrist", "thigh", "knee", "calf", "ankle"}

MEASURE_PLAN = {
    "M-001": ("front", GIRTH, "high_bust", "high_bust"),
    "M-002": ("front", GIRTH, "bust_apex", "bust_apex"),
    "M-003": ("front", GIRTH, "underbust", "underbust"),
    "M-004": ("front", GIRTH, "waist", "waist"),
    "M-005": ("front", GIRTH, "high_hip", "high_hip"),
    "M-006": ("front", GIRTH, "full_hip", "full_hip"),
    "M-007": ("front", GIRTH, "bicep", None),
    "M-008": ("front", GIRTH, "wrist", None),
    "M-009": ("front", GIRTH, "thigh", "thigh"),
    "M-010": ("front", GIRTH, "knee", "knee"),
    "M-011": ("front", GIRTH, "calf", "calf"),
    "M-013": ("front", GIRTH, "neck_base", "neck_base"),
    "M-014": ("front", HORZ, "side_neck_point", "shoulder_point"),
    "M-015": ("front", VERT, "throat_hollow", "waist"),
    "M-016": ("back", VERT, "nape", "waist"),
    "M-017": ("front", VERT, "side_neck_point", "bust_apex"),
    "M-018": ("front", HORZ, "bust_apex", "bust_apex"),
    "M-019": ("front", VERT, "bust_apex", "waist"),
    "M-020": ("back", HORZ, "across_back", "across_back"),
    "M-021": ("front", HORZ, "across_chest", "across_chest"),
    "M-022": ("back", VERT, "nape", "underarm"),
    "M-023": ("front", VERT, "waist", "full_hip"),
    "M-024": ("side", VERT, "waist", "floor"),
    "M-025": ("front", VERT, "crotch", "floor"),
    "M-026": ("side", VERT, "waist", "seat_surface"),
    "M-027": ("side", VERT, "waist", "waist"),
    "M-028": ("front", VERT, "shoulder_point", "wrist"),
    "M-029": ("front", VERT, "shoulder_point", "elbow"),
    "M-030": ("front", VERT, "top_of_head", "floor"),
    "M-031": ("front", DERIVED, None, None),
    "M-032": ("front", DERIVED, None, None),
    "M-033": ("front", DERIVED, None, None),
}

# ── belirti figürü tarifleri: sınıf → token davranışı ─────────────────
SIGN_CLASS_PLAN = {
    "diagonal_drag_line":  ("TK-05", 38.0),
    "horizontal_fold":     ("TK-06", 0.0),
    "vertical_fold":       ("TK-06", 90.0),
    "strain_pull":         ("TK-07", None),
    "gape":                ("TK-06", 20.0),
    "pooling":             ("TK-06", 0.0),
    "seam_displacement":   ("TK-09", None),
    "grain_distortion":    ("TK-10", None),
    "hem_hike":            ("TK-09", None),
    "silhouette_deviation": ("TK-12", None),
}

# krokideki bölge çapaları — belirti figüründe işaretin NEREYE konacağı
ZONE_ANCHOR = {
    "neck":          ("neck_base", 0.0),
    "shoulder":      ("shoulder_point", 0.6),
    "upper_back":    ("across_back", 0.0),
    "bust_chest":    ("bust_apex", 0.45),
    "armhole":       ("underarm", 0.85),
    "sleeve_arm":    ("bicep", 1.35),
    "waist_torso":   ("waist", 0.0),
    "hip_seat":      ("full_hip", 0.5),
    "crotch_leg":    ("thigh", 0.4),
    "whole_garment": ("underbust", 0.0),
}

NODE = {
    "obs_w": 148.0, "obs_h": 30.0,
    "dec_w": 158.0, "dec_h": 40.0,
    "end_w": 128.0, "end_h": 32.0,
    "vgap": 17.0, "hgap": 20.0,
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def wrap_lines(text: str, max_w: float, size: float, face: str = "sans") -> list:
    """Metni verilen genişliğe sarar. ÇİZMEDEN ölçer — düğüm boyutları
    çizimden ÖNCE bilinmelidir, yoksa şema kendi kutusunu taşırır."""
    from figure_tokens import font, register_fonts
    from reportlab.pdfbase import pdfmetrics
    register_fonts()
    fname = font(face)
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(cand, fname, size) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def short(s: str, n: int = 92) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1].rstrip(" ,.;:") + "…"


# ══ AKIŞ ŞEMASI ═══════════════════════════════════════════════════════
class SignChart:
    """Tek bir belirtinin teşhis akışı.

    Yapı (VISUAL_SPEC § 2): gözlem → ikili karar zinciri → devir ya da
    eleme. BOŞTA BİTEN YOL YAPISAL OLARAK İMKÂNSIZDIR: son karar
    düğümünün 'hayır' dalı her zaman bir eleme düğümüne bağlanır.

    Düğüm yükseklikleri metinden ÖLÇÜLÜR. Bir eşkenar dörtgenin içine
    yazı sığdırmak dikdörtgeninkinden zordur: orta yükseklikte tam
    genişlik vardır, uçlarda sıfır. Bu yüzden karar düğümünün metin
    alanı genişliğin %54'ü ve yüksekliği metin bloğunun 1,9 katıdır.
    """

    TXT = 6.4          # düğüm içi punto
    LH = 1.24          # satır aralığı çarpanı
    DEC_TEXT_FRAC = 0.54
    DEC_HEIGHT_FACTOR = 1.9

    def __init__(self, sign: dict, label: dict, ui: dict):
        self.sign = sign
        self.label = label
        self.ui = ui
        # ⚠ Faz 5'te ÖLÇÜLEN kusur: metin girişi nedenleri
        # `atlas.sign_entry()` içinde YENİDEN SIRALIYOR — kalıp
        # değişikliği GEREKTİRMEYEN (bedava) nedenler öne alınıyor ve
        # başlık da bunu ilan ediyor: "Candidate causes, cheapest test
        # first". Akış şeması ise HAM taksonomi sırasını kullanıyordu.
        # İki sonuç: (a) şema, karşı sayfadaki başlığın vaat ettiği
        # sırayı çiğniyordu — bedava dal 17 girişin 17'sinde ikinci ya
        # da üçüncü sıradaydı; (b) metinde "1." olan neden ile şemanın
        # ilk dalı FARKLI nedenlerdi, yani "birinci neden" aynı
        # yayılımda iki ayrı şeye işaret ediyordu.
        # Sıralama artık TEK yerden gelir.
        # Regresyon: 07_TESTS/selftest.py § test_flowchart_and_entry_agree_on_cause_order
        pairs = list(zip(sign["candidate_causes"], label["causes"]))
        gates = [q for q in pairs if not q[0].get("adjustment_family_ref")]
        rest = [q for q in pairs if q[0].get("adjustment_family_ref")]
        ordered = gates + rest
        self.causes = [q[0] for q in ordered]
        self._labels = [q[1] for q in ordered]
        self._layout()

    # ── ölçüm ─────────────────────────────────────────────────────────
    def _box_h(self, text, width, frac=1.0, factor=1.0, minimum=26.0):
        lines = wrap_lines(text, width * frac - 8.0, self.TXT)
        h = len(lines) * self.TXT * self.LH + 10.0
        return max(minimum, h * factor), len(lines)

    def _layout(self):
        self.obs_text = short(self.label["observation"], 150)
        self.obs_h, _ = self._box_h(self.obs_text, NODE["dec_w"], minimum=NODE["obs_h"])
        self.rows = []
        for i, c in enumerate(self.causes):
            dtxt = short(self._labels[i]["evidence"], 160)
            dh, _ = self._box_h(dtxt, NODE["dec_w"], self.DEC_TEXT_FRAC,
                                self.DEC_HEIGHT_FACTOR, NODE["dec_h"])
            af = c.get("adjustment_family_ref")
            ttxt = None  # çizimde doldurulur
            th_min = NODE["end_h"]
            self.rows.append({"cause": c, "cause_en": self._labels[i]["cause"],
                              "dec_text": dtxt, "dec_h": dh,
                              "af": af, "term_text": ttxt, "term_h": th_min})
        self.tail_text = self.ui["not_this_sign"].replace(
            "{apx_c}", str(self.ui.get("_apx_c_page") or "")).replace(" (page )", "")
        self.tail_h, _ = self._box_h(self.tail_text, NODE["dec_w"], minimum=NODE["end_h"])

    def set_terminal_texts(self, af_names: dict):
        # ⚠ Faz 5 çizge denetimi: 43 belirtinin 8'inde İKİ neden AYNI
        # aileye çıkıyor. Metin bunu biliyor ve okura söylüyor —
        # "Another cause on this sign leads to the same family in the
        # OPPOSITE direction — record which one you confirmed, and in
        # which direction". Ama ŞEMA iki AYNI kutu basıyordu: okurun
        # gerçekte kullandığı gösterim, ayırt etmesi istenen şeyi
        # gösteremiyordu. Paylaşılan varış artık nedeniyle etiketlenir.
        # Regresyon: 07_TESTS/selftest.py § test_shared_family_terminals_are_distinguishable
        import collections as _c
        shared = {f for f, n in _c.Counter(
            r["af"] for r in self.rows if r["af"]).items() if n > 1}
        for r in self.rows:
            c = r["cause"]
            if r["af"]:
                name = af_names.get(r["af"], r["af"])
                if r["af"] in shared:
                    r["term_text"] = (short(name, 44) + " — via: "
                                      + short(r["cause_en"], 46))
                else:
                    r["term_text"] = short(name, 60)
                r["term_h"], _ = self._box_h(r["term_text"], NODE["end_w"],
                                             minimum=NODE["end_h"])
                r["term_h"] += 8.0   # AF-xx etiketi için ek şerit
            else:
                r["term_text"] = self.ui["not_a_pattern_problem"] + short(r["cause_en"], 60)
                r["term_h"], _ = self._box_h(r["term_text"], NODE["end_w"],
                                             minimum=NODE["end_h"])

    def size(self) -> tuple:
        h = self.obs_h + self.tail_h + NODE["vgap"] * (len(self.rows) + 1)
        for r in self.rows:
            h += max(r["dec_h"], r["term_h"])
        w = NODE["dec_w"] + NODE["hgap"] + NODE["end_w"]
        return (w, h)

    def terminals(self) -> list:
        out = []
        for r in self.rows:
            out.append(("handoff", r["af"]) if r["af"]
                       else ("eliminate", r["cause_en"]))
        out.append(("eliminate", self.tail_text))
        return out

    # ── çizim ─────────────────────────────────────────────────────────
    def draw(self, fc: FigureCanvas, x0: float, y_top: float, af_names: dict):
        self.set_terminal_texts(af_names)
        w, total_h = self.size()
        cx = x0 + NODE["dec_w"] / 2
        y = y_top - self.obs_h
        fc.tk17_observation_node(x0, y, NODE["dec_w"], self.obs_h,
                                 self.obs_text, size=self.TXT)
        prev_bottom = y
        for r in self.rows:
            row_h = max(r["dec_h"], r["term_h"])
            y -= NODE["vgap"] + row_h
            dy = y + (row_h - r["dec_h"]) / 2
            fc.connector(cx, prev_bottom, cx, dy + r["dec_h"])
            fc.tk16_decision_node(x0, dy, NODE["dec_w"], r["dec_h"],
                                  r["dec_text"], size=self.TXT)
            ex = x0 + NODE["dec_w"] + NODE["hgap"]
            ey = y + (row_h - r["term_h"]) / 2
            ymid = dy + r["dec_h"] / 2
            fc.connector(x0 + NODE["dec_w"], ymid, ex, ymid, elbow=False)
            fc.text((x0 + NODE["dec_w"] + ex) / 2, ymid + 2.6, self.ui["yes"],
                    face="sans-semibold", size=6.0, anchor="middle")
            if r["af"]:
                fc.tk18_handoff_node(ex, ey, NODE["end_w"], r["term_h"],
                                     r["term_text"], r["af"], size=self.TXT,
                                     reader_ref=r.get("reader_ref"))
            else:
                fc.tk17_observation_node(ex, ey, NODE["end_w"], r["term_h"],
                                         r["term_text"], size=self.TXT - 0.2)
            prev_bottom = dy
        y -= NODE["vgap"] + self.tail_h
        fc.connector(cx, prev_bottom, cx, y + self.tail_h)
        fc.text(cx + 3.0, y + self.tail_h + NODE["vgap"] / 2 - 1.0, self.ui["no"],
                face="sans-semibold", size=6.0)
        fc.tk17_observation_node(x0, y, NODE["dec_w"], self.tail_h,
                                 self.tail_text, size=self.TXT)
        return w, total_h


# ══ MOTOR ═════════════════════════════════════════════════════════════
class Engine:
    def __init__(self, book_id: str):
        self.book = book_id
        self.geom = load(paths.PAGE_GEOMETRY)
        self.signs = load(paths.FIT_SIGNS)["signs"]
        self.measures = load(paths.MEASUREMENTS)["measurements"]
        self.families = load(paths.ADJUSTMENT_FAMILIES)["families"]
        # ── okura dönük DİL katmanı ───────────────────────────────────
        # Kitabın dili series_config → series.language'dır. Taksonomi
        # PROJE BELGE dilindedir (documentLanguage). Figürler okurun
        # dilinde çizilir; ikisi karışırsa okura gösterilemeyecek bir
        # figür üretilir (DECISIONS.md K45).
        cfg = load(paths.SERIES_CONFIG)
        self.book_language = cfg["series"]["language"]
        self.labels = load(paths.LABELS_EN) if paths.LABELS_EN.exists() else None
        if self.book_language != "en" or self.labels is None:
            raise SystemExit(
                f"figür motoru okur dili {self.book_language!r} için etiket katmanı "
                f"bulamadı — 02_TAXONOMY/public/labels_en.json")
        self.ui = self.labels["ui"]
        self.zone_names = self.labels["zones"]
        # bölge → bölüm numarası: yönlendirici okura NEREYE
        # gideceğini söylemek zorunda (İnceleme C).
        self.zone_chapter = {
            "neck": 9, "shoulder": 9, "upper_back": 10, "armhole": 10,
            "bust_chest": 11, "waist_torso": 12, "hip_seat": 13,
            "sleeve_arm": 14, "crotch_leg": 15, "whole_garment": None}
        self.af_names = {f["adjustment_family_id"]: f["name"] for f in self.families}
        self.out_dir = paths.book_generated(book_id)
        self.figures: list[dict] = []
        self.notes: list[str] = []
        self.fa = self.geom["figure_area"]
        self.max_w = float(self.fa["max_width_pt"])
        self.max_h = float(self.fa["max_height_pt"])
        self._n = 0

    # ── canvas fabrikası ──────────────────────────────────────────────
    # `place()` ile bir hedef verilirse SONRAKİ figür o sayfaya çizilir.
    # Tek kullanımlıktır: bir yerleştirme yanlışlıkla sonraki figürleri
    # de yakalayamaz.
    _place: tuple | None = None

    def place(self, canvas, x: float, y: float):
        self._place = (canvas, x, y)
        return self

    def _fc(self, w: float, h: float, surface: str, filename: str):
        if self._place is not None:
            canvas, x, y = self._place
            self._place = None
            return FigureCanvas(w, h, surface=surface, canvas=canvas, origin=(x, y))
        return FigureCanvas(w, h, surface=surface, out_path=self.out_dir / filename)

    def _next_id(self) -> str:
        self._n += 1
        return f"FIG-B{self.book[-1]}-{self._n:03d}"

    _silent = False

    def _record(self, *, fig_type, shows, view, tokens, deterministic,
                manual_reason=None, claim_ref=None, photo_required=False,
                extra=None):
        if self._silent:
            return None
        rec = {
            "figure_id": self._next_id(),
            "book": self.book,
            "figure_type": fig_type,
            "shows": shows,
            "view": view,
            "notation_tokens": tokens,
            "deterministic": deterministic,
            "manual_reason": manual_reason,
            "photo_required": photo_required,
            "claim_ref": claim_ref,
            "physical_validation_ref": None,
            "reused_from": None,
            "verification_status": "drafted" if deterministic else "specified",
        }
        self.figures.append(rec)
        if extra:
            self._meta[rec["figure_id"]] = extra
        return rec

    _meta: dict = {}

    # ── ① akış şemaları ───────────────────────────────────────────────
    def gen_flowcharts(self):
        zones: dict[str, list] = {}
        for s in self.signs:
            zones.setdefault(s["zone"], []).append(s)

        # ÖLÇÜM: bölge düzeyinde tek şema tek sayfaya sığar mı?
        zone_fit = {}
        for z, ss in zones.items():
            charts = [SignChart(s, self.labels["signs"][s["symptom_id"]], self.ui)
                      for s in ss]
            for c in charts:
                c.set_terminal_texts(self.af_names)
            lane_w = max(c.size()[0] for c in charts) + NODE["hgap"]
            total_w = lane_w * len(charts)
            total_h = max(c.size()[1] for c in charts)
            zone_fit[z] = {
                "signs": len(ss),
                "width_pt": round(total_w, 1),
                "height_pt": round(total_h, 1),
                "fits_page": total_w <= self.max_w and total_h <= self.max_h,
            }
        self.zone_fit = zone_fit

        # bölge yönlendirici (ana şema)
        self._draw_zone_router(zones)
        # eleme şeması
        self._draw_elimination_chart()

        for z in sorted(zones):
            for s in zones[z]:
                self._draw_sign_chart(s)

    def _draw_sign_chart(self, sign: dict):
        chart = SignChart(sign, self.labels["signs"][sign["symptom_id"]], self.ui)
        chart.set_terminal_texts(self.af_names)
        w, h = chart.size()
        pad = 10.0
        fid_hint = sign["symptom_id"]
        fc = self._fc(w + pad * 2, h + pad * 2, "diagram", f"flow_{fid_hint}.pdf")
        chart.draw(fc, pad, h + pad, self.af_names)
        tokens = fc.finish()
        rec = self._record(
            fig_type="flowchart",
            shows=f"{sign['symptom_id']} teşhis akışı — "
                  f"{short(self.labels['signs'][sign['symptom_id']]['observation'], 80)}",
            view=None, tokens=tokens, deterministic=True,
            extra={"symptom_ref": sign["symptom_id"], "zone": sign["zone"],
                   "width_pt": round(w + pad * 2, 1), "height_pt": round(h + pad * 2, 1),
                   "terminals": chart.terminals(),
                   "source_file": f"flow_{fid_hint}.pdf"})
        return rec

    def _draw_zone_router(self, zones: dict):
        """Kitabın ANA yönlendiricisi — bir soru, on bölge.

        ⚠ İnceleme C ve D'nin ORTAK bir numaralı bulgusu: bu figür
        yanlış bir TOPOLOJİ çiziyordu. Bütün bağlayıcılar aynı noktadan
        başladığı için dikey parçaları ÜST ÜSTE binip tek bir sürekli
        çizgiye dönüşüyor, o çizgi de kutuların İÇİNDEN ve etiket
        metinlerinin ÜSTÜNDEN geçiyordu. Sonuç bir dallanma değil bir
        ZİNCİR gibi okunuyordu: "kol oyuntusundaysa → ağ ve bacağa git".
        Üstelik başlığı "hangi BÖLÜME gideceğini bu belirler" diyen
        figürde HİÇBİR bölüm numarası yoktu.

        Yeni yerleşim: kökten aşağı tek dikey, oradan yatay bir OMURGA,
        her sütunun DIŞ yanından inen bir dikey ve her düğüme kısa bir
        yatay dal. Hiçbir çizgi hiçbir kutunun içinden geçmez.
        """
        names = self.zone_names
        order = sorted(zones, key=lambda z: (self.zone_chapter.get(z) or 99, z))
        cols, rows = 2, (len(order) + 1) // 2
        gut = NODE["hgap"] * 1.6          # omurga için dış pay
        w = NODE["obs_w"] * cols + NODE["hgap"] * 3 + gut * 2
        h = NODE["obs_h"] * (rows + 1) + NODE["vgap"] * (rows + 3)
        fc = self._fc(w, h, "diagram", "flow_ZONE_ROUTER.pdf")

        root_y = h - NODE["vgap"] - NODE["obs_h"]
        fc.tk17_observation_node((w - NODE["obs_w"]) / 2, root_y,
                                 NODE["obs_w"], NODE["obs_h"],
                                 self.ui["router_question"], size=7.4)
        bus_y = root_y - NODE["vgap"] * 0.8
        # kökten omurgaya tek dikey
        fc.line(w / 2, root_y, w / 2, bus_y, role="callout_leader")
        col_x = [gut + NODE["hgap"] / 2,
                 w - gut - NODE["hgap"] / 2]          # sütun omurgaları
        fc.line(col_x[0], bus_y, col_x[1], bus_y, role="callout_leader")

        top = bus_y - NODE["vgap"] * 0.6
        node_x = [gut + NODE["hgap"], w / 2 + NODE["hgap"] / 2]
        last_y = [bus_y, bus_y]
        for i, z in enumerate(order):
            c, r = i % cols, i // cols
            x = node_x[c]
            y = top - (r + 1) * (NODE["obs_h"] + NODE["vgap"]) + NODE["vgap"] * 0.4
            ch = self.zone_chapter.get(z)
            label = f"{names[z]} · " + self.ui["sign_count"].format(n=len(zones[z]))
            if ch:
                label += f" · ch. {ch}"
            fc.tk17_observation_node(x, y, NODE["obs_w"], NODE["obs_h"],
                                     label, size=7.0)
            ymid = y + NODE["obs_h"] / 2
            # sütun omurgası: son bağlantıdan bu düğümün hizasına
            fc.line(col_x[c], last_y[c], col_x[c], ymid, role="callout_leader")
            last_y[c] = ymid
            # omurgadan düğüme kısa yatay dal
            ex = x if c == 0 else x + NODE["obs_w"]
            fc.connector(col_x[c], ymid, ex, ymid, elbow=False)
        tokens = fc.finish()
        self._record(fig_type="flowchart",
                     shows="Ana yönlendirici — belirtinin bölgesine göre bölüm seçimi",
                     view=None, tokens=tokens, deterministic=True,
                     extra={"zone": "ALL", "width_pt": round(w, 1), "height_pt": round(h, 1),
                            "source_file": "flow_ZONE_ROUTER.pdf"})

    def _draw_elimination_chart(self):
        """Eleme şeması. Sayfaya SIĞMAZSA bölünür — küçültülmez.

        VISUAL_SPEC § 2 kural 4: 'Bir şema tek yayılıma sığmalıdır.
        Sığmıyorsa KONU BÖLÜNÜR, şema küçültülmez.' Bu kural burada
        koda dönüşür: satır sayısı sayfa yüksekliğinden HESAPLANIR.
        """
        conf: list[str] = []
        for s in self.signs:
            for c in s.get("confounders_to_rule_out", []):
                head = c.split(":")[0].strip()
                head_en = self.labels["confounders"].get(head)
                if head_en is None:
                    self.notes.append(f"karıştırıcı sınıfı için İngilizce etiket YOK: {head!r}")
                    head_en = head
                if head_en not in conf:
                    conf.append(head_en)
        row_h = NODE["dec_h"] + NODE["vgap"]
        overhead = NODE["end_h"] + NODE["vgap"] * 2
        per_page = max(1, int((self.max_h - overhead) // row_h))
        pages = [conf[i:i + per_page] for i in range(0, len(conf), per_page)]
        self.notes.append(
            f"eleme şeması: {len(conf)} karıştırıcı sınıfı, sayfa başına "
            f"{per_page} satır sığıyor → {len(pages)} şemaya BÖLÜNDÜ "
            f"(VISUAL_SPEC § 2 kural 4).")
        for i, chunk in enumerate(pages, 1):
            self._draw_elimination_page(chunk, i, len(pages))

    def _draw_elimination_page(self, conf: list, page: int, total: int):
        rows = len(conf)
        w = NODE["dec_w"] + NODE["hgap"] + NODE["end_w"]
        h = (NODE["dec_h"] + NODE["vgap"]) * rows + NODE["end_h"] + NODE["vgap"] * 2
        name = f"flow_ELIMINATION_{page}.pdf"
        fc = self._fc(w, h, "diagram", name)
        y = h - NODE["vgap"]
        prev = None
        for c in conf:
            y -= NODE["dec_h"]
            fc.tk16_decision_node(0, y, NODE["dec_w"], NODE["dec_h"],
                                  self.ui["eliminated"].format(c=c), size=6.8)
            if prev is not None:
                fc.connector(NODE["dec_w"] / 2, prev, NODE["dec_w"] / 2, y + NODE["dec_h"])
                fc.text(NODE["dec_w"] / 2 + 3.0, prev - NODE["vgap"] / 2 - 1.0,
                        self.ui["yes"], face="sans-semibold", size=6.0)
            ex = NODE["dec_w"] + NODE["hgap"]
            ey = y + (NODE["dec_h"] - NODE["end_h"]) / 2
            fc.connector(NODE["dec_w"], y + NODE["dec_h"] / 2, ex, ey + NODE["end_h"] / 2,
                         elbow=False)
            fc.text((NODE["dec_w"] + ex) / 2, y + NODE["dec_h"] / 2 + 2.6, self.ui["no"],
                    face="sans-semibold", size=6.0, anchor="middle")
            fc.tk17_observation_node(ex, ey, NODE["end_w"], NODE["end_h"],
                                     self.ui["fix_first"], size=6.2)
            prev = y
            y -= NODE["vgap"]
        y -= NODE["end_h"]
        tail = (self.ui["all_clear"] if page == total
                else self.ui["next_list"].format(n=page + 1))
        fc.tk17_observation_node(0, y, NODE["dec_w"], NODE["end_h"], tail, size=6.8)
        fc.connector(NODE["dec_w"] / 2, prev, NODE["dec_w"] / 2, y + NODE["end_h"])
        fc.text(NODE["dec_w"] / 2 + 3.0, prev - NODE["vgap"] / 2 - 1.0, self.ui["yes"],
                face="sans-semibold", size=6.0)
        tokens = fc.finish()
        self._record(fig_type="flowchart",
                     shows=(f"Eleme şeması {page}/{total} — kalıba dokunmadan ÖNCE "
                            f"elenmesi gereken karıştırıcılar"),
                     view=None, tokens=tokens, deterministic=True,
                     extra={"zone": "ELIMINATION", "page": page, "of": total,
                            "width_pt": round(w, 1), "height_pt": round(h, 1),
                            "confounders": conf, "source_file": name})

    # ── ② ölçüm figürleri ─────────────────────────────────────────────
    def gen_measurement_figures(self):
        for m in self.measures:
            mid = m["measurement_id"]
            plan = MEASURE_PLAN.get(mid)
            if plan is None:
                self.notes.append(f"{mid}: MEASURE_PLAN girdisi yok — figür üretilmedi.")
                continue
            view, kind, l1, l2 = plan
            if kind == DERIVED:
                self._draw_derived_measure(m)
                continue
            self._draw_measure(m, view, kind, l1, l2)

    def _measure_caption(self, m: dict) -> str:
        """Ölçü figürünün altındaki uyarı etiketi.

        ⚠ Faz 5'te ÖLÇÜLEN kusur: etiket `verification_status`'tan
        TÜRETİLİYORDU — "doğrulanmamış AMA kaynağı var" ⇒ "Sources
        differ". Bu YEDİ ölçüye "see the note in Chapter 2" bastırdı;
        oysa kayıtlı tanım çelişkisi DÖRT tanedir ve Bölüm 2'de yalnızca
        dört not vardır. Üç okur (`M-015`, `M-017`, `M-028`) VAR OLMAYAN
        bir nota gönderiliyordu — üstelik Ek F "dört anlaşmazlık kaydeder"
        diye yazarken. Çelişki artık kayıttan OKUNUR.
        Regresyon: 07_TESTS/selftest.py § test_source_conflict_caption_matches_the_record
        """
        if m.get("source_conflict"):
            return self.ui["source_conflict"]
        if m["verification_status"] == "technical_reference_verified":
            return ""
        if m.get("source_refs"):
            return ""      # kaynağı var, çelişki YOK — uyarıya gerek yok
        return self.ui["no_source"]

    def _draw_measure(self, m: dict, view: str, kind: str, l1: str, l2: str | None):
        W, H = 214.0, 300.0
        fc = self._fc(W, H, "body", f"meas_{m['measurement_id']}.pdf")
        lows = [LEVEL[x] for x in (l1, l2) if x in LEVEL]
        lowest = min(lows) if lows else LEVEL["waist"]
        needs_arm = (l1 in ("bicep", "elbow", "wrist", "shoulder_point")
                     or l2 in ("bicep", "elbow", "wrist"))
        full = lowest < LEVEL["thigh"] - 1e-9 or l1 == "top_of_head"
        if view == "side":
            cro = croquis_fit(W, H, "floor" if full else "crotch", "top_of_head",
                              arms=True, view="side", pad_y=20.0)
            cro.draw(fc, arms=False, head=True, legs=full)
        elif full:
            cro = croquis_fit(W, H, "floor", "top_of_head", arms=True, view=view,
                              pad_y=20.0)
            cro.draw(fc, arms=True, head=True, legs=True)
        elif needs_arm:
            cro = croquis_fit(W, H, "wrist", "top_of_head", arms=True, view=view,
                              pad_y=18.0)
            cro.draw(fc, arms=True, head=True, legs=False)
        else:
            bottom = "high_hip" if lowest >= LEVEL["high_hip"] else "thigh"
            cro = croquis_fit(W, H, bottom, "top_of_head", arms=False, view=view,
                              pad_y=18.0)
            cro.draw_torso_only(fc, bottom=bottom)
        if kind == GIRTH:
            if l1 in LIMB_LEVELS:
                pts = cro.limb_girth_path(l1, l1, side=1)
            else:
                pts = cro.girth_path(l1, l1)
            fc.tk11_measure_path(pts, label=m["name"])
            fc.landmark_dot(*pts[0]); fc.landmark_dot(*pts[-1])
        elif kind == HORZ:
            hk = {"across_back": "across_back", "across_chest": "across_chest",
                  "bust_apex": "apex_offset",
                  "shoulder_point": "shoulder_point"}.get(l2 or l1, "waist")
            if l1 == "side_neck_point":
                a = cro.p("side_neck_point", "neck_base", 1)
                b = cro.p("shoulder_point", "shoulder_point", 1)
                pts = [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 1.2), b]
            else:
                a = cro.p(l1, hk, -1); b = cro.p(l1, hk, 1)
                pts = [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b]
            fc.tk11_measure_path(pts, label=m["name"], label_side="right")
            fc.landmark_dot(*pts[0]); fc.landmark_dot(*pts[-1])
        elif view == "side":
            if m["measurement_id"] == "M-027":     # ağ uzunluğu (rise)
                pts = [cro.profile_point("waist", True),
                       cro.profile_point("crotch", True),
                       (cro.cx, cro.y("crotch") - 0.004 * cro.H),
                       cro.profile_point("crotch", False),
                       cro.profile_point("waist", False)]
            else:                                   # M-024 dış dikiş, M-026 ağ derinliği
                a = cro.profile_point("waist", False)
                b = cro.profile_point(l2 if l2 in ("floor", "seat_surface") else "crotch",
                                      False)
                pts = [a, ((a[0] + b[0]) / 2 - 5.0, (a[1] + b[1]) / 2), b]
            fc.tk11_measure_path(pts, label=m["name"], label_side="left")
            fc.landmark_dot(*pts[0]); fc.landmark_dot(*pts[-1])
        else:  # VERT — önden/arkadan
            side = 0
            hk = None
            if l1 == "shoulder_point":
                side, hk = 1, "shoulder_point"
            a = cro.p(l1, hk, side)
            b = cro.p(l2, hk if l2 in ("shoulder_point",) else None,
                      side if l2 in ("wrist", "elbow") else 0)
            if l1 == "shoulder_point":
                b = (a[0] + 6.0, cro.y(l2))
            pts = [a, ((a[0] + b[0]) / 2 + 4.0, (a[1] + b[1]) / 2), b]
            fc.tk11_measure_path(pts, label=m["name"])
            fc.landmark_dot(*pts[0]); fc.landmark_dot(*pts[-1])
        if l1 in ("bust_apex",) or (l2 == "bust_apex"):
            fc.tk08_apex(*cro.apex(1))
            fc.tk08_apex(*cro.apex(-1))
        cap = self._measure_caption(m)
        if cap:
            fc.text(6.0, 6.0, cap, face="sans-italic", size=6.2, gray=0.45)
        tokens = fc.finish()
        self._record(
            fig_type="measurement_path",
            shows=f"{m['measurement_id']} {m['name']} — {short(m['path_rule'], 90)}",
            view=view, tokens=tokens, deterministic=True,
            extra={"measurement_ref": m["measurement_id"],
                   "verification_status_of_record": m["verification_status"],
                   "caption_class": ("verified" if not cap else
                                     ("source_conflict" if m.get("source_refs") else "no_source")),
                   "width_pt": W, "height_pt": H,
                   "source_file": f"meas_{m['measurement_id']}.pdf"})

    def _draw_derived_measure(self, m: dict):
        W, H = 300.0, 96.0
        fc = self._fc(W, H, "diagram", f"meas_{m['measurement_id']}.pdf")
        # Türetilmiş ölçünün "işaret noktaları" başka ÖLÇÜLERDİR ve
        # kayıtta kimlikleriyle durur. Okur bir kimliği okuyamaz —
        # figürde ölçünün ADI basılır (TYPOGRAPHY_STANDARD § 3.4).
        names = {x["measurement_id"]: x["name"] for x in self.measures}
        a = names.get(m["landmark_start"], m["landmark_start"])
        b = names.get(m["landmark_end"], m["landmark_end"])
        fc.tk17_observation_node(8, H - 40, 118, 30, a, size=7.0)
        fc.tk17_observation_node(174, H - 40, 118, 30, b, size=7.0)
        fc.text(W / 2, H - 27, "−", face="sans-bold", size=11.0, anchor="middle")
        fc.tk18_handoff_node(91, 12, 118, 30, short(m["name"], 46), "M-fark", size=6.8) \
            if False else fc.tk17_observation_node(91, 12, 118, 30, short(m["name"], 46), size=6.8)
        fc.connector(67, H - 40, 150, 42)
        fc.connector(233, H - 40, 150, 42)
        tokens = fc.finish()
        self._record(fig_type="table_graphic",
                     shows=f"{m['measurement_id']} {m['name']} — türetilmiş ölçünün hesabı",
                     view=None, tokens=tokens, deterministic=True,
                     extra={"measurement_ref": m["measurement_id"],
                            "width_pt": W, "height_pt": H,
                            "source_file": f"meas_{m['measurement_id']}.pdf"})

    # ── ③ belirti figürleri ───────────────────────────────────────────
    # Çelişmeli inceleme B-05: 43 belirti figürünün hepsi aynı silüetteydi.
    # Varyant ELLE ATANMAZ — belirtinin aday nedenlerinden TÜRETİLİR.
    # Kural: figür, o belirtinin nedeni olan vücut farkını gösterebilmeli.
    # Neden bir vücut farkı DEĞİLSE (yapım, kumaş, beden) varyant yoktur.
    _VARIANT_BY_FAMILY = (
        (("AF-01", "AF-02"), "fuller_bust"),      # göğüs hacmi / konumu
        (("AF-07",), "rounded_back"),             # yuvarlak / geniş sırt
        (("AF-14", "AF-11"), "straight_back"),    # lumbar / gövde dengesi
    )

    @classmethod
    def _body_variant(cls, sign: dict) -> str:
        refs = {c.get("adjustment_family_ref") for c in sign["candidate_causes"]}
        refs.discard(None)
        for families, variant in cls._VARIANT_BY_FAMILY:
            if refs & set(families):
                return variant
        return "standard"

    def gen_sign_figures(self):
        for s in self.signs:
            self._draw_sign_figure(s)

    BACK_WORDS = ("back", "nape", "seat", "shoulder blade", "shoulder-blade",
                  "centre back", "behind")
    FRONT_WORDS = ("front", "bust", "chest", "abdomen", "button band", "neckline")

    def _sign_view(self, s: dict, zone: str) -> str:
        """Belirti vücudun hangi yüzünde görülür — KAYITTAN okunur."""
        if zone == "upper_back":
            return "back"
        txt = (self.labels["signs"][s["symptom_id"]]["observation"]).lower()
        back = sum(txt.count(w) for w in self.BACK_WORDS)
        front = sum(txt.count(w) for w in self.FRONT_WORDS)
        return "back" if back > front else "front"

    def _draw_sign_figure(self, s: dict):
        W, H = 200.0, 268.0
        sid = s["symptom_id"]
        fc = self._fc(W, H, "garment", f"sign_{sid}.pdf")
        zone = s["zone"]
        anchor_level, side_mult = ZONE_ANCHOR[zone]
        bottom = "knee" if zone == "crotch_leg" else "thigh"
        variant = self._body_variant(s)
        # ⚠ İnceleme D-02/D-06: görünüm yalnızca `zone == "upper_back"`
        # ile belirleniyordu; oysa altı belirti daha vücudun ARKASINI
        # anlatıyor (oturak, arka ağ, arka bel). Bunlar ÖNDEN çiziliyor
        # ve önden çizilen benzerleriyle AYNI figüre düşüyordu — s. 205
        # (arka, yetersizlik) ile s. 208 (ön, fazlalık) aynı resimdi.
        # Görünüm artık belirtinin KENDİ gözlem metninden okunur.
        view = self._sign_view(s, zone)
        cro = croquis_fit(W, H, bottom, "top_of_head", arms=False, pad_y=16.0,
                          view=view, variant=variant)
        # ⚠ İnceleme D-13: 1-bit baskıda %45 gri SİYAHA düşer. Gövde
        # 1,2 pt, teşhis işareti 0,6 pt çiziliyordu — yani figürün
        # ÇERÇEVESİ, ÖZNESİNİN iki katı kalınlıkta basılıyordu.
        # Anlamı GRİYE emanet etmek siyah-mürekkep bir kitapta
        # çalışmaz; hiyerarşi KALINLIKLA kurulur.
        cro.draw_torso_only(fc, bottom=bottom, gray=0.45,
                            role="construction_line")
        hk = {"neck_base": "neck_base", "shoulder_point": "shoulder_point",
              "across_back": "across_back", "bust_apex": "bust_apex",
              "underarm": "underarm", "bicep": "underarm", "waist": "waist",
              "full_hip": "full_hip", "thigh": "thigh",
              "underbust": "underbust"}[anchor_level]
        ax = cro.cx + side_mult * cro.hw(hk) * 0.72
        ay = cro.y(anchor_level)
        # İşaret kutunun kenarına yapışamaz: TK-05/TK-06 uzunlukları
        # (≈26 pt) + ok başı için her kenarda 34 pt boşluk bırakılır.
        edge = 34.0
        ax = min(max(ax, edge), W - edge)
        ay = min(max(ay, edge), min(H - edge, cro.y("shoulder_point")))
        token, ang = SIGN_CLASS_PLAN[s["sign_class"]]
        if token == "TK-05":
            fc.tk05_drag_lines(ax, ay, ang, role="body_outline")
        elif token == "TK-06":
            fc.tk06_excess_fold(ax, ay, ang, role="body_outline")
        elif token == "TK-07":
            fc.tk07_strain_zone(ax, ay, 20.0, 13.0)
        elif token == "TK-09":
            # SAPMAYI çiz, sağlıklı durumu değil (D-04). Ayrıca sınıfa
            # göre AYIR (D-02): bir ETEK UCU yatay bir çizgidir ve
            # düzlüğünü kaybeder — eteğin hizasında çizilir. Bir DİKİŞ
            # KAYMASI dikey bir çizgidir ve düzlüğünü kaybeder — bel
            # hizasında dikey çizilir. İkisi aynı token'ı paylaşıyordu
            # ve aynı resmi üretiyordu.
            if s["sign_class"] == "hem_hike":
                hem_y = cro.y(bottom) + 6.0
                fc.tk09_balance_line(cro.cx - cro.hw("full_hip") * 1.05, hem_y,
                                     cro.cx + cro.hw("full_hip") * 1.05, hem_y,
                                     label="H", tilt=11.0 * (side_mult or 1))
            else:
                top_y, bot_y = cro.y("across_back"), cro.y("high_hip")
                fc.tk09_balance_line(cro.cx, top_y, cro.cx, bot_y,
                                     label="S", tilt=0.0)
                fc.tk05_drag_lines(cro.cx + 9.0, (top_y + bot_y) / 2, 90.0,
                                   length=14.0, count=1, role="body_outline")
        elif token == "TK-10":
            fc.tk10_grainline(ax, ay - 20.0, ax, ay + 20.0)
        elif token == "TK-12":
            fc.tk12_before([(ax - 18, ay - 22), (ax - 12, ay), (ax - 16, ay + 22)])
        tokens = fc.finish()
        self._record(
            fig_type="fit_sign_on_figure",
            shows=f"{sid} — {short(s['observation'], 96)}",
            view=view,
            tokens=tokens, deterministic=False,
            manual_reason=("Şablon deterministik üretildi (bölge çapası + sınıf token'ı), "
                           "ama kumaşın GERÇEK dökümü kayıttan türetilemez: kıvrımın uzunluğu, "
                           "sayısı ve yönü fiziksel sınamadan (VAL-xxxx) gelir. Bu figür "
                           "Faz 3'te toile üzerinden düzeltilecektir."),
            extra={"symptom_ref": sid, "zone": zone, "sign_class": s["sign_class"],
                   "template_token": token, "body_variant": variant,
                   "width_pt": W, "height_pt": H,
                   "source_file": f"sign_{sid}.pdf"})

    # ── ④ kalıp parçası figürleri ─────────────────────────────────────
    def gen_pattern_pieces(self):
        pieces = [
            ("front_bodice", "Ön beden — düz ölçüm noktaları", "bodice"),
            ("back_bodice", "Arka beden — düz ölçüm noktaları", "bodice"),
            ("sleeve", "Kol — kol oyuntusu ve kol uzunluğu", "sleeve"),
            ("front_skirt", "Ön etek — bel ve kalça hattı", "skirt"),
            ("back_skirt", "Arka etek — bel ve kalça hattı", "skirt"),
            ("front_trouser", "Ön pantolon — ağ eğrisi ve iç bacak", "trouser"),
            ("back_trouser", "Arka pantolon — ağ eğrisi ve oturuş", "trouser"),
            ("dart_anatomy", "Pens anatomisi — uç, taban, derinlik", "dart"),
        ]
        for key, shows, kind in pieces:
            self._draw_pattern_piece(key, shows, kind)

    def _draw_pattern_piece(self, key: str, shows: str, kind: str):
        W, H = 210.0, 250.0
        fc = self._fc(W, H, "pattern", f"patt_{key}.pdf")
        m = 20.0
        if kind == "bodice":
            pts = [(m, m), (W - m, m), (W - m, H - m - 46), (W - m - 30, H - m - 10),
                   (m + 34, H - m), (m, H - m - 14)]
        elif kind == "sleeve":
            pts = [(m + 22, m), (W - m - 22, m), (W - m - 8, H - m - 60),
                   (W / 2, H - m), (m + 8, H - m - 60)]
        elif kind == "skirt":
            pts = [(m - 6, m), (W - m + 6, m), (W - m - 14, H - m), (m + 14, H - m)]
        elif kind == "trouser":
            pts = [(m, m), (W - m - 24, m), (W - m, H / 2), (W - m - 18, H - m),
                   (m + 10, H - m), (m + 4, H / 2)]
        else:  # dart
            pts = [(m, m), (W - m, m), (W - m, H - m), (m, H - m)]
        fc.polyline(pts, role="pattern_edge_original", close=True)
        # dikiş çizgisi (⅝ inç = 45 pt ölçekte değil; şematik iç ofset)
        inset = 8.0
        cxp = sum(p[0] for p in pts) / len(pts)
        cyp = sum(p[1] for p in pts) / len(pts)
        seam = [(x + (cxp - x) * inset / max(abs(cxp - x), 1e-6) * 0.12 if False else
                 x + (cxp - x) * 0.055, y + (cyp - y) * 0.055) for (x, y) in pts]
        fc.polyline(seam, role="seam_line", close=True)
        fc.tk10_grainline(W / 2, m + 26, W / 2, H - m - 26)
        if kind == "dart":
            apex = (W / 2, H - m - 34)
            fc.polyline([(W / 2 - 24, m + 8), apex, (W / 2 + 24, m + 8)],
                        role="construction_line")
            fc.tk04_pivot_point(*apex)
            fc.tk08_apex(W / 2, H - m - 12)
            fc.tk03_overlap_arrow(W / 2 - 24, m + 8, W / 2 + 24, m + 8, self.ui["dart_depth"])
        if kind == "bodice":
            fc.tk08_apex(W / 2 + 6, H - m - 74)
            fc.tk09_balance_line(m + 4, H - m - 74, W - m - 4, H - m - 74)
        fc.declare_scale(self.ui["scale_note"])
        tokens = fc.finish()
        self._record(fig_type="pattern_piece", shows=shows, view="flat",
                     tokens=tokens, deterministic=True,
                     extra={"piece": key, "width_pt": W, "height_pt": H,
                            "source_file": f"patt_{key}.pdf"})

    # ── ⑤ tablo grafikleri ────────────────────────────────────────────
    #
    # İKİ SINIF vardır ve karıştırılamaz:
    #   · OKURA DÖNÜK tablo — kitaba basılır, iç kayıt kimliği TAŞIYAMAZ
    #   · İÇ tablo — üretim/denetim aracıdır, kitaba GİRMEZ
    # Ayrım `internal` bayrağıyla kayda geçer ve qa_visual ayrı sayar.
    def gen_tables(self):
        zn = self.zone_names
        reader = [
            ("zone_index", "Bölge → belirti sayısı dizini (okura dönük)",
             [["Region", "Signs"]] +
             [[zn[z], str(sum(1 for x in self.signs if x["zone"] == z))]
              for z in sorted({s["zone"] for s in self.signs})]),
            ("order_of_operations", "Düzeltme sırası — neden önce omuz",
             [["Step", "Region", "Why here"],
              ["1", "Shoulder and neck", "If it shifts, everything below it shifts"],
              ["2", "Bust", "Carries the neckline and armhole with it"],
              ["3", "Waist", "Cannot be read until the upper body sits"],
              ["4", "Hip and crotch", "Cannot be read until the waistline is fixed"],
              ["5", "Sleeve", "The armhole must stop changing first"]]),
            ("do_not_change_yet", "Henüz değiştirme — geri alınamaz kesimler",
             [["Do not", "Because"],
              ["Cut the neckline", "A cut neckline cannot be put back"],
              ["Deepen the armhole", "The sleeve cap measurement breaks with it"],
              ["Take in the side seam", "The grain of the pattern shifts"],
              ["Shorten the hem", "Level the waistline first"]]),
        ]
        internal = [
            ("af_index", "Düzeltme ailesi dizini — İÇ ARAÇ (kitaba girmez)",
             [["Family", "Name", "Zone"]] +
             [[f["adjustment_family_id"], short(f["name"], 40), f["zone"]]
              for f in self.families]),
            ("sign_class_index", "Belirti sınıfı sayımı — İÇ ARAÇ",
             [["Class", "How many"]] +
             [[c, str(sum(1 for s in self.signs if s["sign_class"] == c))]
              for c in sorted({s["sign_class"] for s in self.signs})]),
            ("measure_status", "Ölçü doğrulama durumu — İÇ ARAÇ",
             [["Status", "Measurements"]] +
             [[k, str(v)] for k, v in sorted(
                 {m["verification_status"]: sum(
                     1 for x in self.measures
                     if x["verification_status"] == m["verification_status"])
                  for m in self.measures}.items())]),
        ]
        for key, shows, rows in reader:
            self._draw_table(key, shows, rows, internal=False)
        for key, shows, rows in internal:
            self._draw_table(key, shows, rows, internal=True)

    # ── ⑤b MANÜSKRİPT FİGÜRLERİ — Faz 4'te ÖLÇÜLEREK eklendi ─────────
    #
    # Faz 2 figür sicilini TAKSONOMİ katmanından türetti: her belirtiye
    # bir figür, her ölçüye bir figür, her bölgeye bir şema. Doğruydu ve
    # EKSİKTİ. Manüskript dizilince yedi figürün var olmadığı ÖLÇÜLDÜ —
    # hepsi CHAPTER_SPECS'te yazılıydı ama hiçbiri taksonomi kaydından
    # türetilemezdi, çünkü karşılıkları bir kayıt değil bir BÖLÜMDÜR.
    #
    # Ders Faz 2'nin B-10'uyla aynı sınıftan: bir üretim hattı, sormadığı
    # soruyu üretemez. Kapı eklendi — qa_manuscript.py her bölümün spec'te
    # istenen figürünü arar.
    def gen_manuscript_figures(self):
        cls = self.labels["sign_classes"]
        self._draw_table("three_numbers",
                         "Üç sayı — vücut, kalıp, bitmiş giysi (okura dönük)",
                         [["", "What it measures", "Where it comes from"],
                          ["Body", "You", "A tape measure, on you"],
                          ["Pattern", "The paper pieces, flat",
                           "Measured off the pattern, allowances removed"],
                          ["Finished garment", "The sewn thing on a hanger",
                           "The pattern envelope, or measured off the pattern"]],
                         internal=False)
        self._draw_table("sign_classes",
                         "On belirti sınıfı ve ne anlattıkları (okura dönük)",
                         [["Class", "What it means"]] +
                         [[v[0], v[1]] for v in cls.values()],
                         internal=False)
        conf = []
        for sg in self.signs:
            for c in sg.get("confounders_to_rule_out", []):
                head = self.labels["confounders"].get(c.split(":")[0].strip())
                if head and head not in conf:
                    conf.append(head)
        self._draw_table("rule_out_checklist",
                         "Eleme kontrol listesi — okura dönük, fotokopi edilebilir",
                         [["", "Ruled out?"]] + [[c, "\u2610"] for c in conf],
                         internal=False)
        for key, (title, cols) in self.labels["forms"].items():
            rows = [cols] + [[""] * len(cols) for _ in range(10)]
            self._draw_table(f"form_{key}", f"Boş form — {title} (okura dönük)",
                             rows, internal=False)
        # ── Ek A ve Ek H: OKURA DÖNÜK dizinler ────────────────────────
        # Ek A önce Bölüm 2'ye işaret eden bir sayfaydı ve pratikte BOŞTU.
        # Bir başvuru eki, öğretim bölümünün kopyası olmamalıdır ama
        # ARAMA yapılabilir olmalıdır: ad, nereden, nereye, en sık hata.
        self._draw_table("measurement_index",
                         "Ölçü dizini — okura dönük başvuru (Ek A)",
                         [["Measurement", "Where it runs", "Helper?"]] +
                         # Kırpma burada YAPILMAZ: dizgi sarar, çizim
                         # katmanı kendi sınırını kendisi uygular.
                         [[m["name"],
                           ("a calculated difference" if m["category"] == "derived"
                            else f"{m['landmark_start']} → {m['landmark_end']}"),
                           "yes" if m.get("helper_required") else "no"]
                          for m in self.measures],
                         internal=False)
        # Ek H: Kitap 1'in vardığı 20 aile. İÇ KİMLİK TAŞIMAZ — okura
        # dönük bir dizinde AF-xx basmak K46'nın ihlalidir.
        self._draw_table("family_index",
                         "Düzeltme ailesi dizini — okura dönük (Ek H)",
                         [["Adjustment family", "Region"]] +
                         [[f["name"], self.zone_names.get(f["zone"], f["zone"])]
                          for f in self.families],
                         internal=False)
        self._draw_cycle_chart()

    def _draw_cycle_chart(self):
        """Yedi adımlı döngünün ana şeması — Bölüm 6'nın merkez figürü.

        DÖNGÜDÜR, liste değildir: son adımdan ikinci adıma dönen bağ
        çizilir. Çelişmeli inceleme B-01 tam olarak bu bağın metinde
        olmamasıydı; şemada da olmalıdır."""
        steps = [
            ("Set up", "Standardise the conditions before you look at anything"),
            ("Observe", "Look in a fixed order and record without interpreting"),
            ("Name", "Name what you see from the controlled vocabulary"),
            ("Locate", "Where a sign appears is not always where it comes from"),
            ("Measure", "Compare the three numbers at that point"),
            ("Test", "One hypothesis, the cheapest reversible test"),
            ("Record", "Name the adjustment family and write down the amount"),
        ]
        # Geri dönüş etiketi kutunun SAĞINA yazılıyor; kutu onu almalı.
        # İlk sürüm 74 pt ayırmıştı ve etiket figür kutusunun dışına
        # taşıyordu — sayfaya bakılarak görüldü.
        w = NODE["obs_w"] + 132.0
        h = (NODE["obs_h"] + NODE["vgap"]) * len(steps) + NODE["vgap"]
        fc = self._fc(w, h, "diagram", "flow_CYCLE.pdf")
        y = h - NODE["vgap"]
        ys = []
        for i, (name, why) in enumerate(steps, 1):
            y -= NODE["obs_h"]
            fc.tk14_step(14.0, y + NODE["obs_h"] / 2, i)
            fc.tk17_observation_node(28.0, y, NODE["obs_w"], NODE["obs_h"],
                                     f"{name} \u2014 {why}", size=6.4)
            if ys:
                fc.connector(28.0 + NODE["obs_w"] / 2, ys[-1],
                             28.0 + NODE["obs_w"] / 2, y + NODE["obs_h"])
            ys.append(y)
            y -= NODE["vgap"]
        # ── B-01: yeniden gözlem bağı — döngüyü KAPATAN çizgi ─────────
        x_r = 28.0 + NODE["obs_w"] + 12.0
        y_last = ys[-1] + NODE["obs_h"] / 2
        y_obs = ys[1] + NODE["obs_h"] / 2
        fc.polyline([(28.0 + NODE["obs_w"], y_last), (x_r, y_last), (x_r, y_obs)],
                    role="callout_leader")
        fc.connector(x_r, y_obs, 28.0 + NODE["obs_w"], y_obs, elbow=False)
        fc.text(x_r + 5.0, (y_last + y_obs) / 2, "sign reduced",
                face="sans-semibold", size=6.0)
        fc.text(x_r + 5.0, (y_last + y_obs) / 2 - 7.5, "but not gone",
                face="sans-semibold", size=6.0)
        tokens = fc.finish()
        self._record(fig_type="flowchart",
                     shows=("Yedi adımlı teşhis döngüsü — ana şema; yeniden gözlem "
                            "bağı döngüyü kapatır (çelişmeli inceleme B-01)"),
                     view=None, tokens=tokens, deterministic=True,
                     extra={"zone": "CYCLE", "width_pt": round(w, 1),
                            "height_pt": round(h, 1), "source_file": "flow_CYCLE.pdf"})

    def _draw_table(self, key: str, shows: str, rows: list, internal: bool = False):
        size = float(self.geom["typography_grid"]["table_size_pt"])
        pad, rowh = 6.0, size * 1.75
        ncol = max(len(r) for r in rows)
        colw = []
        for c in range(ncol):
            w = 0.0
            for r in rows:
                if c < len(r):
                    w = max(w, len(r[c]) * size * 0.52)
            colw.append(min(max(w + pad * 2, 42.0), 210.0))
        # ⚠ Sütun genişlikleri içerikten HESAPLANIR ve toplamı sayfanın
        # figür alanını AŞABİLİR. Ek A'nın dört sütunlu ölçü dizini tam
        # bunu yaptı (723 pt > 504 pt) ve qa_visual yakaladı.
        #
        # Kapı doğru davrandı; hatayı KAYNAĞINDA kapatmak gerekiyordu:
        # bir tablo figürü sayfadan geniş ÜRETİLEMEMELİ. Taşarsa sütunlar
        # ORANTILI daraltılır — kolon atılmaz, çünkü hangi kolonun
        # atılacağı bir İÇERİK kararıdır ve motor onu veremez.
        # İlk denemede sütunlar ORANTILI daraltıldı. Yanlıştı: daraltma
        # etiketleri üst üste bindirdi ve çakışma kapısı onu yakaladı.
        # Bir kapıyı başka bir kapıyı bozarak geçmek bir çözüm değildir.
        #
        # Motor artık REDDEDİYOR. Sayfadan geniş bir tablo bir çizim
        # sorunu değil bir İÇERİK sorunudur ve motorun veremeyeceği bir
        # karar ister: hangi sütun kısalacak.
        # ⚠ Sütun genişliği 210 pt'de KIRPILIYOR ama hücre metni tam
        # uzunlukta çiziliyordu; uzun bir hücre komşusunun üzerine
        # taşıyor ve çakışma kapısı haklı olarak reddediyordu.
        # Metin artık SÜTUNUNA sığdırılır — genişlik bir sınırdır, bir
        # temenni değil.
        # ⚠ KIRPMA YALNIZCA ÇİZİM İÇİNDİR. Sayfaya dizilen tablo
        # `extra["data"]`'dan gelir ve orada TAM metin durmalıdır:
        # dizgi motoru sütuna sığdırmayı SARARAK yapar, kırparak değil.
        # İlk sürüm kırpılmış satırları kaydetti ve Ek B'deki sınıf
        # tanımları kitapta "…" ile kesildi — çizim sınırı, İÇERİĞİ
        # budamıştı. İki katmanın kısıtı aynı değildir.
        full_rows = [list(r) for r in rows]
        fitted = []
        for r in rows:
            row = []
            for c in range(ncol):
                txt = str(r[c]) if c < len(r) else ""
                budget = max(1, int((colw[c] - pad * 2) / (size * 0.52)))
                row.append(txt if len(txt) <= budget else short(txt, budget))
            fitted.append(row)
        rows = fitted

        max_w = float(self.geom["text_block"]["total_measure_pt"])
        if sum(colw) > max_w:
            raise ValueError(
                f"tbl_{key}: tablo sayfadan GENİŞ ({sum(colw):.0f} > {max_w:.0f} pt). "
                f"Sütun sayısını ya da hücre metnini kısaltın; motor hangisinin "
                f"kısalacağına karar veremez.")
        W = sum(colw); H = rowh * len(rows) + 2
        fc = self._fc(W, H, "table", f"tbl_{key}.pdf")
        y = H - rowh
        for i, r in enumerate(rows):
            x = 0.0
            face = "sans-semibold" if i == 0 else "sans"
            for c in range(ncol):
                txt = r[c] if c < len(r) else ""
                fc.text(x + pad, y + rowh * 0.32, txt, face=face, size=size)
                x += colw[c]
            if i == 0:
                fc.line(0, y - 1.0, W, y - 1.0, role="balance_line")
            elif i < len(rows) - 1:
                fc.line(0, y - 1.0, W, y - 1.0, role="callout_leader", gray=0.45)
            y -= rowh
        tokens = fc.finish(internal_marks=internal) or ["TK-09"]
        self._record(fig_type="table_graphic", shows=shows, view=None,
                     tokens=tokens if tokens else ["TK-09"], deterministic=True,
                     extra={"table": key, "rows": len(rows), "internal": internal,
                            # Dizgi için SATIRIN KENDİSİ ve sütun oranları.
                            # Tablo sayfaya PDF olarak yapıştırılmaz, metin
                            # ızgarasında yeniden dizilir — ama veri TEK
                            # kaynaktan gelir: bu kayıt. İki kopya olsaydı
                            # PDF ile sayfa birbirinden ayrılabilirdi.
                            "data": full_rows,
                            "col_ratio": [round(c / W, 4) for c in colw],
                            "width_pt": round(W, 1), "height_pt": round(H, 1),
                            "source_file": f"tbl_{key}.pdf"})

    # ── ⑥ öncesi/sonrası — ölçüm hatası çiftleri ──────────────────────
    # ⚠ İnceleme D-19: `render()`'ın docstring'i "İkinci bir çizim yolu
    # YOKTUR… ikisi ayrışamaz" diyordu. AYRIŞMIŞLARDI: bağımsız figür
    # PDF'leri TÜRKÇE etiket basıyordu ("Kollar kaldırıldı"), kitap
    # İNGİLİZCE ("Arms raised"). İki ayrı spesifikasyon tablosu vardı.
    # Tablo artık TEKTİR ve okur dilindedir; iki yol da buradan okur.
    # Regresyon: 07_TESTS/selftest.py § test_figure_specs_have_one_copy
    COMPARISON_SPEC = [
        ("tape_slipped_back", "Tape slipped down at the back", "high_bust"),
        ("arms_raised", "Arms raised", "high_bust"),
        ("tape_too_tight", "Tape pulled too tight", "waist"),
        ("waist_guessed", "Waist measured without marking it", "waist"),
        ("hip_too_high", "Hip not measured at the fullest point", "full_hip"),
        ("posture_leaning", "Leaning forward", "waist"),
    ]

    def gen_comparisons(self):
        for key, label, level in self.COMPARISON_SPEC:
            self._draw_comparison(key, label, level)

    def _draw_comparison(self, key: str, label: str, level: str):
        W, H = 300.0, 210.0
        fc = self._fc(W, H, "body", f"cmp_{key}.pdf")
        hk = {"high_bust": "high_bust", "waist": "waist", "full_hip": "full_hip"}[level]
        for i, (dx, wrong) in enumerate(((0.0, True), (W / 2, False))):
            # Kesim seviyesi ÖLÇÜLEN seviyenin altında olmalıdır; yoksa
            # ölçü yolu krokinin dışına düşer.
            bottom = "thigh" if LEVEL[level] <= LEVEL["high_hip"] else "high_hip"
            cro = croquis_fit(W / 2, H, bottom, "top_of_head", arms=False, pad_y=22.0,
                              cx=dx + W / 4, view="front")
            cro.draw_torso_only(fc, bottom=bottom, gray=0.45 if wrong else 0.0)
            pts = cro.girth_path(level, hk)
            if wrong:
                pts = [(x, y + (6.0 if 0 < i2 < len(pts) - 1 else 0.0))
                       for i2, (x, y) in enumerate(pts)]
            fc.tk11_measure_path(pts)
            fc.landmark_dot(*pts[0]); fc.landmark_dot(*pts[-1])
            fc.text(dx + W / 4, 6.0, self.ui["wrong"] if wrong else self.ui["right"],
                    face="sans-bold", size=7.0, anchor="middle")
            del i
        fc.tk15_do_not_do(8.0, 24.0, W / 2 - 26.0, H - 58.0)
        fc.text(6.0, H - 9.0, label, face="sans-italic", size=6.6, gray=0.45)
        tokens = fc.finish()
        self._record(fig_type="comparison_before_after",
                     shows=f"Ölçüm hatası: {label} — yanlış ve doğru yan yana",
                     view="front", tokens=tokens, deterministic=True,
                     extra={"error": key, "width_pt": W, "height_pt": H,
                            "source_file": f"cmp_{key}.pdf"})

    # ── ⑦ bölge anatomi figürleri ─────────────────────────────────────
    def gen_body_landmarks(self):
        groups = [
            ("neck_shoulder", "front", ["side_neck_point", "shoulder_point", "throat_hollow", "neck_base"]),
            ("back_upper", "back", ["nape", "across_back", "underarm"]),
            ("bust", "front", ["high_bust", "bust_apex", "underbust"]),
            ("waist_hip", "front", ["waist", "high_hip", "full_hip"]),
            ("arm", "front", ["shoulder_point", "elbow", "wrist"]),
            ("leg", "front", ["crotch", "knee", "ankle"]),
            ("full_figure", "front", ["top_of_head", "waist", "floor"]),
        ]
        for key, view, marks in groups:
            self._draw_landmark_figure(key, view, marks)

    def _draw_landmark_figure(self, key: str, view: str, marks: list):
        """İşaret noktası figürü — etiketler ÇAKIŞMAZ.

        Etiketler çapa noktasına en yakın yere değil, kendi sütununda
        ÇAKIŞMAYAN bir yüksekliğe konur ve oraya bir bağlayıcı çizilir.
        Çakışan iki etiket yanlış okunur (RISK_REGISTER R-06) ve
        FigureCanvas.check_label_collisions bunu artık reddeder."""
        W, H = 232.0, 300.0
        size = 6.6
        lh = size * 1.62
        fc = self._fc(W, H, "body", f"lmk_{key}.pdf")
        cro = croquis_fit(W * 0.62, H, "floor", "top_of_head", arms=True,
                          pad_y=20.0, cx=W / 2, view=view)
        cro.draw(fc, arms=True, head=True, legs=True)
        hkmap = {"side_neck_point": ("neck_base", 1), "shoulder_point": ("shoulder_point", 1),
                 "throat_hollow": (None, 0), "neck_base": (None, 0), "nape": (None, 0),
                 "across_back": ("across_back", 1), "underarm": ("underarm", 1),
                 "high_bust": ("high_bust", 1), "bust_apex": ("apex_offset", 1),
                 "underbust": ("underbust", 1), "waist": ("waist", 1),
                 "high_hip": ("high_hip", 1), "full_hip": ("full_hip", 1),
                 "elbow": ("elbow", 1), "wrist": ("wrist", 1), "bicep": ("bicep", 1),
                 "crotch": (None, 0), "knee": ("knee", 1), "ankle": ("ankle", 1),
                 "top_of_head": (None, 0), "floor": (None, 0)}
        anchors = []
        ARM_MARKS = {"bicep", "elbow", "wrist"}
        for mk in marks:
            hk, side = hkmap[mk]
            # kol nirengileri KOLUN üstünde durur, gövdenin değil (D-16)
            if mk in ARM_MARKS:
                x, y = cro.arm_center(mk, 1)
            else:
                x, y = cro.p(mk, hk, side)
            fc.landmark_dot(x, y)
            anchors.append((mk, x, y))

        # etiket sütunu: figürün sağı. Çakışmayı önlemek için yukarıdan
        # aşağı yerleştirilir ve gerekirse AŞAĞI itilir.
        col_x = W - 6.0
        placed, last_y = [], None
        for mk, x, y in sorted(anchors, key=lambda a: -a[2]):
            ly = y if last_y is None else min(y, last_y - lh)
            ly = max(ly, 6.0 + lh)
            placed.append((mk, x, y, ly))
            last_y = ly
        for mk, x, y, ly in placed:
            label = mk.replace("_", " ")
            w = fc.text_width(label, "sans", size)
            lx = col_x - w
            fc.line(x, y, lx - 3.0, ly + size * 0.28, role="callout_leader")
            fc.text(lx, ly, label, size=size)
        tokens = fc.finish() or ["TK-11"]
        self._record(fig_type="body_landmark",
                     shows=f"İşaret noktaları — {key.replace('_', ' ')} ({len(marks)} nokta)",
                     view=view, tokens=tokens, deterministic=True,
                     extra={"group": key, "landmarks": marks, "width_pt": W, "height_pt": H,
                            "source_file": f"lmk_{key}.pdf"})

    # ── ⑧ toile durum figürleri ───────────────────────────────────────
    def gen_toile_states(self):
        states = [
            ("marking_cf_cb", "Toile üzerine ön ve arka orta hattın işaretlenmesi"),
            ("marking_balance", "Denge çizgilerinin işaretlenmesi — göğüs ve kalça hizası"),
            ("marking_waist", "Bel hattının lastikle bulunması ve işaretlenmesi"),
            ("pin_test", "İğne testi — fazlalığın toplanıp ölçülmesi"),
            ("slash_test", "Kesme testi — yetersizliğin açılıp ölçülmesi"),
            ("control_toile", "Kontrol toile — düzeltme öncesi referans"),
        ]
        for key, shows in states:
            self._draw_toile_state(key, shows)

    def _draw_toile_state(self, key: str, shows: str):
        W, H = 200.0, 262.0
        fc = self._fc(W, H, "garment", f"toile_{key}.pdf")
        cro = croquis_fit(W, H, "thigh", "top_of_head", arms=False, pad_y=16.0,
                          view="front")
        cro.draw_torso_only(fc, bottom="thigh", gray=0.45)
        if key == "marking_cf_cb":
            fc.tk09_balance_line(cro.cx, cro.y("neck_base"), cro.cx, cro.y("waist"), label="CF")
        elif key == "marking_balance":
            for lv, hk in (("bust_apex", "bust_apex"), ("full_hip", "full_hip")):
                fc.tk09_balance_line(cro.cx - cro.hw(hk), cro.y(lv),
                                     cro.cx + cro.hw(hk), cro.y(lv))
        elif key == "marking_waist":
            fc.tk09_balance_line(cro.cx - cro.hw("waist") * 1.1, cro.y("waist"),
                                 cro.cx + cro.hw("waist") * 1.1, cro.y("waist"), label="W")
            fc.tk14_step(cro.cx + cro.hw("waist") * 1.1 + 10, cro.y("waist"), 1)
        elif key == "pin_test":
            y = cro.y("underbust")
            fc.tk03_overlap_arrow(cro.cx - 22, y, cro.cx + 22, y, self.ui["excess_label"])
            fc.tk06_excess_fold(cro.cx, y + 22, 0.0)
        elif key == "slash_test":
            y = cro.y("bust_apex")
            fc.tk02_spread_arrow(cro.cx - 22, y, cro.cx + 22, y, self.ui["shortfall_label"])
            fc.tk05_drag_lines(cro.cx + cro.hw("bust_apex") * 0.7, y, 38.0)
        else:
            fc.tk09_balance_line(cro.cx - cro.hw("waist"), cro.y("waist"),
                                 cro.cx + cro.hw("waist"), cro.y("waist"))
            fc.tk08_apex(*cro.apex(1)); fc.tk08_apex(*cro.apex(-1))
        tokens = fc.finish()
        self._record(fig_type="toile_state", shows=shows, view="front",
                     tokens=tokens, deterministic=False,
                     manual_reason=("Toile'un GERÇEK dökümü ve iğne/kesme sonrası kumaş "
                                    "davranışı kayıttan türetilemez; şablon deterministiktir "
                                    "ama nihai çizim VAL-xxxx fiziksel sınamasından gelir."),
                     extra={"state": key, "width_pt": W, "height_pt": H,
                            "source_file": f"toile_{key}.pdf"})

    # ── tek figürü bir SAYFAYA çizmek ─────────────────────────────────
    def render(self, key: str, canvas, x: float, y: float):
        """Bir figürü verilen sayfaya, verilen noktadan itibaren çizer.

        Aynı üretici fonksiyonlar kullanılır — ikinci bir çizim yolu
        YOKTUR. Dizilmiş sayfadaki figür, tek başına üretilen PDF ile
        BİREBİR aynıdır; ikisi ayrışamaz."""
        self._silent = True
        self.place(canvas, x, y)
        try:
            if key.startswith("flow_SYM-"):
                sid = key[len("flow_"):]
                sign = next(s for s in self.signs if s["symptom_id"] == sid)
                self._draw_sign_chart(sign)
            elif key == "flow_ZONE_ROUTER":
                zones: dict = {}
                for s in self.signs:
                    zones.setdefault(s["zone"], []).append(s)
                self._draw_zone_router(zones)
            elif key.startswith("flow_ELIMINATION_"):
                page = int(key.rsplit("_", 1)[1])
                conf: list[str] = []
                for s in self.signs:
                    for c in s.get("confounders_to_rule_out", []):
                        h = self.labels["confounders"].get(c.split(":")[0].strip(),
                                                           c.split(":")[0].strip())
                        if h not in conf:
                            conf.append(h)
                row_h = NODE["dec_h"] + NODE["vgap"]
                per = max(1, int((self.max_h - NODE["end_h"] - NODE["vgap"] * 2) // row_h))
                pages = [conf[i:i + per] for i in range(0, len(conf), per)]
                self._draw_elimination_page(pages[page - 1], page, len(pages))
            elif key.startswith("meas_"):
                mid = key[len("meas_"):]
                m = next(x for x in self.measures if x["measurement_id"] == mid)
                plan = MEASURE_PLAN[mid]
                if plan[1] == DERIVED:
                    self._draw_derived_measure(m)
                else:
                    self._draw_measure(m, plan[0], plan[1], plan[2], plan[3])
            elif key.startswith("sign_SYM-"):
                sid = key[len("sign_"):]
                self._draw_sign_figure(next(s for s in self.signs
                                            if s["symptom_id"] == sid))
            elif key.startswith("lmk_"):
                grp = key[len("lmk_"):]
                spec = {g[0]: g for g in [
                    ("neck_shoulder", "front", ["side_neck_point", "shoulder_point",
                                                "throat_hollow", "neck_base"]),
                    ("back_upper", "back", ["nape", "across_back", "underarm"]),
                    ("bust", "front", ["high_bust", "bust_apex", "underbust"]),
                    ("waist_hip", "front", ["waist", "high_hip", "full_hip"]),
                    ("arm", "front", ["shoulder_point", "elbow", "wrist"]),
                    ("leg", "front", ["crotch", "knee", "ankle"]),
                    ("full_figure", "front", ["top_of_head", "waist", "floor"])]}[grp]
                self._draw_landmark_figure(*spec)
            elif key.startswith("toile_"):
                st = key[len("toile_"):]
                self._draw_toile_state(st, "")
            elif key.startswith("cmp_"):
                k = key[len("cmp_"):]
                spec = {e[0]: e for e in self.COMPARISON_SPEC}[k]
                self._draw_comparison(*spec)
            elif key.startswith("patt_"):
                k = key[len("patt_"):]
                spec = {q[0]: q for q in [
                    ("front_bodice", "", "bodice"), ("back_bodice", "", "bodice"),
                    ("sleeve", "", "sleeve"), ("front_skirt", "", "skirt"),
                    ("back_skirt", "", "skirt"), ("front_trouser", "", "trouser"),
                    ("back_trouser", "", "trouser"), ("dart_anatomy", "", "dart")]}[k]
                self._draw_pattern_piece(*spec)
            elif key == "flow_CYCLE":
                self._draw_cycle_chart()
            elif key.startswith("tbl_"):
                raise KeyError(f"{key}: tablo figürleri sayfaya doğrudan dizilir "
                               f"(build_pilot.py § table), render() ile değil.")
            else:
                raise KeyError(f"bilinmeyen figür anahtarı: {key}")
        finally:
            self._silent = False
            self._place = None

    # ── koşum ─────────────────────────────────────────────────────────
    def run(self):
        self.gen_flowcharts()
        self.gen_body_landmarks()
        self.gen_measurement_figures()
        self.gen_sign_figures()
        self.gen_pattern_pieces()
        self.gen_tables()
        self.gen_manuscript_figures()
        self.gen_comparisons()
        self.gen_toile_states()
        return self.figures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    eng = Engine(args.book)
    eng.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        figs = eng.run()
    except ForbiddenDrawing as e:
        print(f"✗ ÇİZİM YASAĞI: {e}")
        return 2

    det = sum(1 for f in figs if f["deterministic"])
    by_type: dict[str, int] = {}
    for f in figs:
        by_type[f["figure_type"]] = by_type.get(f["figure_type"], 0) + 1

    out = {
        "$comment": [
            "FIGURE REGISTER — 06_BUILD/figure_engine.py tarafından ÜRETİLDİ.",
            "Elle düzenlenmez. Kaynak: 02_TAXONOMY/public/*.json + 03_VISUAL/*.json",
            "",
            "notation_tokens listesi BEYAN DEĞİL ÖLÇÜMDÜR: figür çizilirken",
            "gerçekten çağrılan token'lardan türetilir (figure_tokens.FigureCanvas.use).",
            "",
            "verification_status='drafted' = motor üretti, geometrisi denetlendi;",
            "FİZİKSEL olarak doğrulanmadı. 'physically_validated' YALNIZCA bir",
            "VAL-xxxx kaydıyla yazılabilir (validate_spec.check_figure_tokens).",
        ],
        "generated_by": "06_BUILD/figure_engine.py",
        "book": args.book,
        "count": len(figs),
        "deterministic_count": det,
        "deterministic_ratio": round(det / len(figs), 4) if figs else 0.0,
        "by_type": dict(sorted(by_type.items())),
        "figures": figs,
        "figure_meta": Engine._meta,
        "zone_chart_fit": getattr(eng, "zone_fit", {}),
    }
    paths.book_figures(args.book).parent.mkdir(parents=True, exist_ok=True)
    paths.book_figures(args.book).write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ── ÖKSÜZ VARLIK TEMİZLİĞİ ────────────────────────────────────────
    # ⚠ İnceleme D-19: üretilen dizinde SİCİLDE OLMAYAN bir dosya
    # duruyordu — `flow_ELIMINATION.pdf`, şema ikiye bölünmeden önceki
    # koşumdan kalma, üstelik PROJE dilinde. Bir incelemeci ya da
    # matbaacı o klasöre baktığında kitapta olmayan bir figür görüyordu.
    # Üretilmiş varlık, sicilin TÜREVİDİR; sicilde yoksa durmaz.
    live = {m["source_file"] for m in Engine._meta.values() if m.get("source_file")}
    gen_dir = paths.book_generated(args.book)
    orphans = sorted(f.name for f in gen_dir.glob("*.pdf") if f.name not in live) \
        if gen_dir.exists() else []
    for name in orphans:
        (gen_dir / name).unlink()
    if orphans:
        eng.notes.append(f"öksüz üretilmiş varlık SİLİNDİ: {len(orphans)} "
                         f"({', '.join(orphans[:4])}{'…' if len(orphans) > 4 else ''})")

    print(f"▸ figure_engine.py — {args.book}")
    print(f"  {len(figs)} figür üretildi · deterministik {det} ({out['deterministic_ratio']:.1%})")
    for k, v in out["by_type"].items():
        print(f"    {k:<26} {v}")
    for n in eng.notes:
        print(f"  ⚑ {n}")
    if args.json:
        Path(args.json).write_text(json.dumps(out["by_type"], indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
