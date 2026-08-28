#!/usr/bin/env python3
"""
figure_tokens.py — on sekiz token'ın ÇALIŞAN karşılığı.

Bu dosya VISUAL_STANDARD.md § 3–5'i bir belgeden bir ARAÇ hâline
getirir. İki şey yapar:

  ① Her token'ı `visual_language_tokens.json`'daki spec'ine göre çizer.
     Çizgi kalınlıkları ve kesik desenleri dosyadan OKUNUR; burada
     yeniden yazılmaz. Token dosyası değişirse çizim değişir.

  ② VISUAL_STANDARD § 5'in YASAKLARINI ÇALIŞTIRILABİLİR hâle getirir.
     Bir yasak artık "belgede yazan bir kural" değil, çizimi
     DURDURAN bir istisnadır:

       · sayısal etiketsiz spread/overlap oku      → ForbiddenDrawing
       · vücut figüründe slash line (TK-01)        → ForbiddenDrawing
       · ölçek beyanı olmayan kalıp parçası        → ForbiddenDrawing
       · güvenli alanın dışına taşan çizim         → ForbiddenDrawing
       · üçten fazla gri tonu                      → ForbiddenDrawing

Ayrıca her `use()` çağrısı kaydedilir; bu sayede `figures.json`
kaydındaki `notation_tokens` listesi BEYAN EDİLMEZ, ÖLÇÜLÜR — figürün
gerçekten çizdiği token'lardan türetilir (DECISIONS.md K20 disiplini:
bir alanın adı ile ölçtüğü şey aynı olmalıdır).
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402


class ForbiddenDrawing(Exception):
    """VISUAL_STANDARD § 5 ihlali. Çizim DURUR — sessizce düzeltilmez."""


# ── yazı tipleri ──────────────────────────────────────────────────────
FONT_FACES = {
    "serif": ("SourceSerif4", "ttf/SourceSerif4-Regular.ttf"),
    "serif-bold": ("SourceSerif4-Bold", "ttf/SourceSerif4-Bold.ttf"),
    "serif-italic": ("SourceSerif4-It", "ttf/SourceSerif4-It.ttf"),
    "sans": ("SourceSans3", "ttf/SourceSans3-Regular.ttf"),
    "sans-semibold": ("SourceSans3-Semibold", "ttf/SourceSans3-Semibold.ttf"),
    "sans-bold": ("SourceSans3-Bold", "ttf/SourceSans3-Bold.ttf"),
    "sans-italic": ("SourceSans3-It", "ttf/SourceSans3-It.ttf"),
    "atkinson": ("AtkinsonHyperlegible", "ttf/AtkinsonHyperlegible-Regular.ttf"),
    "atkinson-bold": ("AtkinsonHyperlegible-Bold", "ttf/AtkinsonHyperlegible-Bold.ttf"),
}
_registered: set[str] = set()


def register_fonts() -> list[str]:
    """TTF'leri reportlab'a kaydeder. Eksik dosya SESSİZCE atlanmaz."""
    missing = []
    for key, (name, rel) in FONT_FACES.items():
        if name in _registered:
            continue
        p = paths.VISUAL_FONTS / rel
        if not p.exists():
            missing.append(rel)
            continue
        pdfmetrics.registerFont(TTFont(name, str(p)))
        _registered.add(name)
    if missing:
        raise FileNotFoundError(
            "yazı tipi dosyaları eksik: " + ", ".join(missing)
            + " — `python3 06_BUILD/fetch_fonts.py` çalıştırın "
            "(03_VISUAL/fonts/fonts_manifest.json)."
        )
    return sorted(_registered)


def font(key: str) -> str:
    return FONT_FACES[key][0]


# ── token sözlüğü ve sayfa geometrisi ─────────────────────────────────
def load_tokens() -> dict:
    return json.loads(paths.VISUAL_TOKENS.read_text(encoding="utf-8"))


def load_geometry() -> dict:
    return json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))


DASH = {
    "solid": None,
    "solid_heavier": None,
    "dash 2-2": (2, 2),
    "dash 4-2": (4, 2),
    "dash-dot 6-2-1-2": (6, 2, 1, 2),
    "dash 1-1": (1, 1),
}


class FigureCanvas:
    """Bir figürün çizim yüzeyi.

    Koordinatlar PUNTO cinsindendir ve figürün SOL ALT köşesinden başlar
    (0, 0). Sayfa yerleşimi figürün işi değildir; figür kendi kutusunu
    doldurur, yerleşimi dizgi yapar.
    """

    def __init__(self, width_pt: float, height_pt: float, *, surface: str = "garment",
                 scale_declared: str | None = None, out_path: Path | None = None,
                 canvas=None, origin: tuple = (0.0, 0.0)):
        """`canvas` verilirse figür KENDİ dosyasına değil, verilen sayfaya
        `origin` noktasından itibaren çizilir. Koordinatlar yine figürün
        kendi (0,0)'ından başlar — bir figür nereye yerleştirildiğini
        BİLMEZ. Bu, aynı motorun hem tek figür PDF'i hem de dizilmiş
        sayfa üretmesini sağlar; ikinci bir çizim yolu YOKTUR."""
        if surface not in {"body", "garment", "pattern", "diagram", "table"}:
            raise ValueError(f"bilinmeyen yüzey: {surface}")
        self.tokens = load_tokens()
        self.geom = load_geometry()
        self.w, self.h = float(width_pt), float(height_pt)
        self.surface = surface
        self.scale_declared = scale_declared
        self.used: list[str] = []
        self.warnings: list[str] = []
        self.labels: list[tuple] = []   # (x0, y0, x1, y1, metin)
        self._grays: set[float] = set()
        self.out_path = out_path
        self._lw = {k: v for k, v in self.tokens["line_weights_pt"].items() if not k.startswith("$")}
        self._inset = float(self.geom["figure_area"]["safe_zone_pt"]["inset"])
        self._allowed_grays = set(self.geom["print_safety"]["gray_levels"])
        self._max_grays = int(self.geom["print_safety"]["max_gray_levels"])
        self._min_stroke = float(self.geom["print_safety"]["min_stroke_pt"])
        self._min_text = float(self.geom["print_safety"]["min_text_size_pt"])
        register_fonts()
        self.bound = canvas is not None
        if self.bound:
            self.c = canvas
            self.c.saveState()
            self.c.translate(origin[0], origin[1])
        else:
            self.c = rl_canvas.Canvas(str(out_path) if out_path else "/dev/null",
                                      pagesize=(self.w, self.h))
        self.c.setLineCap(1)
        self.c.setLineJoin(1)

    # ── disiplin ──────────────────────────────────────────────────────
    def use(self, token_id: str):
        if token_id not in {t["token_id"] for t in self.tokens["tokens"]}:
            raise ForbiddenDrawing(f"{token_id} visual_language_tokens.json'da tanımlı DEĞİL.")
        if token_id == "TK-01" and self.surface == "body":
            raise ForbiddenDrawing(
                "TK-01 (slash line) vücut figüründe ASLA kullanılmaz — "
                "visual_language_tokens.json TK-01.rule.")
        if token_id not in self.used:
            self.used.append(token_id)

    def _guard(self, *pts):
        for (x, y) in pts:
            if x < -0.01 or y < -0.01 or x > self.w + 0.01 or y > self.h + 0.01:
                raise ForbiddenDrawing(
                    f"çizim figür kutusunun DIŞINA taşıyor: ({x:.1f}, {y:.1f}) "
                    f"kutu {self.w:.1f}×{self.h:.1f} pt")

    def _stroke(self, role: str, override_pt: float | None = None):
        w = override_pt if override_pt is not None else self._lw[role]
        if w < self._min_stroke - 1e-9:
            raise ForbiddenDrawing(
                f"{role}: {w} pt, baskı asgarisi {self._min_stroke} pt'nin ALTINDA "
                f"(page_geometry.print_safety.min_stroke_pt).")
        self.c.setLineWidth(w)
        return w

    def _gray(self, g: float):
        if g not in self._allowed_grays:
            raise ForbiddenDrawing(
                f"gri tonu {g} izin listesinde yok {sorted(self._allowed_grays)} — "
                f"VISUAL_SPEC § 6: en fazla üç ton.")
        self._grays.add(g)
        if len(self._grays) > self._max_grays:
            raise ForbiddenDrawing(
                f"{len(self._grays)} gri tonu kullanıldı, azami {self._max_grays}.")
        self.c.setFillGray(g)
        self.c.setStrokeGray(g)

    def _dash(self, pattern_key: str):
        d = DASH.get(pattern_key, "?")
        if d == "?":
            raise ForbiddenDrawing(f"tanımsız kesik deseni: {pattern_key}")
        self.c.setDash(list(d), 0) if d else self.c.setDash([], 0)

    # ── temel çizim ───────────────────────────────────────────────────
    def line(self, x1, y1, x2, y2, role="construction_line", gray=0.0,
             dash="solid", width=None):
        self._guard((x1, y1), (x2, y2))
        self._gray(gray); self._dash(dash); self._stroke(role, width)
        self.c.line(x1, y1, x2, y2)
        self.c.setDash([], 0)

    def polyline(self, pts, role="garment_outline", gray=0.0, dash="solid",
                 close=False, width=None):
        self._guard(*pts)
        self._gray(gray); self._dash(dash); self._stroke(role, width)
        p = self.c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if close:
            p.close()
        self.c.drawPath(p, stroke=1, fill=0)
        self.c.setDash([], 0)

    def curve(self, pts, role="body_outline", gray=0.0, dash="solid", width=None):
        """Catmull-Rom → bezier. Deterministik: aynı nokta listesi aynı eğri."""
        self._guard(*pts)
        self._gray(gray); self._dash(dash); self._stroke(role, width)
        p = self.c.beginPath(); p.moveTo(*pts[0])
        n = len(pts)
        for i in range(n - 1):
            p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, n - 1)]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
            p.curveTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
        self.c.drawPath(p, stroke=1, fill=0)
        self.c.setDash([], 0)

    def text(self, x, y, s, *, face="sans", size=None, anchor="start", gray=0.0):
        size = size or float(self.geom["typography_grid"]["figure_label_size_pt"])
        if size < self._min_text - 1e-9:
            raise ForbiddenDrawing(
                f"etiket {size} pt, asgari {self._min_text} pt'nin ALTINDA.")
        if s.isupper() and len(s) > 24:
            raise ForbiddenDrawing(
                "figür içinde BÜYÜK HARFLİ uzun metin yasak "
                "(TYPOGRAPHY_STANDARD § 5 madde 6).")
        self._guard((x, y))
        w = pdfmetrics.stringWidth(s, font(face), size)
        x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        self.labels.append((x0, y - size * 0.22, x0 + w, y + size * 0.78, s))
        self._gray(gray)
        self.c.setFont(font(face), size)
        if anchor == "start":
            self.c.drawString(x, y, s)
        elif anchor == "middle":
            self.c.drawCentredString(x, y, s)
        elif anchor == "end":
            self.c.drawRightString(x, y, s)
        else:
            raise ValueError(anchor)

    def text_width(self, s, face="sans", size=None):
        size = size or float(self.geom["typography_grid"]["figure_label_size_pt"])
        return pdfmetrics.stringWidth(s, font(face), size)

    # ── TK-01 · slash line ────────────────────────────────────────────
    def tk01_slash_line(self, x1, y1, x2, y2):
        self.use("TK-01")
        self.line(x1, y1, x2, y2, role="pattern_edge_modified",
                  dash="dash 4-2", width=self._lw["pattern_edge_original"])
        ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
        for (x, y) in ((x1, y1), (x2, y2)):
            dx, dy = 2.5 * math.cos(ang), 2.5 * math.sin(ang)
            self.line(x - dx, y - dy, x + dx, y + dy, role="construction_line")

    # ── TK-02 / TK-03 · spread & overlap arrows ───────────────────────
    def _arrow_head(self, x, y, ang, size=4.2, filled=True):
        a1 = ang + math.radians(160); a2 = ang - math.radians(160)
        p = self.c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x + size * math.cos(a1), y + size * math.sin(a1))
        p.lineTo(x + size * math.cos(a2), y + size * math.sin(a2))
        p.close()
        self.c.drawPath(p, stroke=1, fill=1 if filled else 0)

    def tk02_spread_arrow(self, x1, y1, x2, y2, label: str):
        """Açma oku. `label` ZORUNLUDUR — VISUAL_STANDARD § 5."""
        if not label or not label.strip():
            raise ForbiddenDrawing(
                "TK-02 spread arrow SAYISAL ETİKETSİZ çizilemez "
                "(visual_language_tokens.json TK-02.rule).")
        self.use("TK-02")
        ang = math.atan2(y2 - y1, x2 - x1)
        off = 0.9
        dx, dy = off * math.sin(ang), -off * math.cos(ang)
        self.line(x1 + dx, y1 + dy, x2 + dx, y2 + dy, role="balance_line")
        self.line(x1 - dx, y1 - dy, x2 - dx, y2 - dy, role="balance_line")
        self._gray(0.0); self._stroke("balance_line")
        self._arrow_head(x2, y2, ang, filled=False)
        self._arrow_head(x1, y1, ang + math.pi, filled=False)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        self.text(mx, my + 3.0, label, anchor="middle")

    def tk03_overlap_arrow(self, x1, y1, x2, y2, label: str):
        if not label or not label.strip():
            raise ForbiddenDrawing(
                "TK-03 overlap arrow SAYISAL ETİKETSİZ çizilemez.")
        self.use("TK-03")
        ang = math.atan2(y2 - y1, x2 - x1)
        self.line(x1, y1, x2, y2, role="balance_line")
        self._gray(0.0); self._stroke("balance_line")
        self._arrow_head(x2, y2, ang, filled=True)
        self._arrow_head(x1, y1, ang + math.pi, filled=True)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        self.text(mx, my + 3.0, label, anchor="middle")

    # ── TK-04 · pivot point ───────────────────────────────────────────
    def tk04_pivot_point(self, x, y, r=2.6):
        self.use("TK-04")
        self._guard((x - r, y - r), (x + r, y + r))
        self._gray(0.0); self._stroke("seam_line")
        self.c.circle(x, y, r, stroke=1, fill=0)
        self.c.circle(x, y, 0.55, stroke=1, fill=1)

    # ── TK-05 · drag line indicator ───────────────────────────────────
    def tk05_drag_lines(self, x, y, ang_deg: float, length=22.0, count=3, spacing=3.4):
        """Yönlü çekme. Ok KAYNAĞA bakar: (x, y) kaynaktır."""
        self.use("TK-05")
        ang = math.radians(ang_deg)
        nx, ny = -math.sin(ang), math.cos(ang)
        for i in range(count):
            o = (i - (count - 1) / 2.0) * spacing
            sx, sy = x + nx * o, y + ny * o
            ex, ey = sx + length * math.cos(ang + math.pi), sy + length * math.sin(ang + math.pi)
            self.line(ex, ey, sx, sy, role="seam_line")
            self._gray(0.0); self._stroke("seam_line")
            self._arrow_head(sx, sy, ang, size=3.0, filled=False)

    # ── TK-06 · excess fabric fold ────────────────────────────────────
    def tk06_excess_fold(self, x, y, ang_deg: float, length=26.0, count=3, spacing=4.6,
                         bow=4.6):
        """Fazlalık kıvrımı — PARALEL YAY kümesi. TK-05'ten görsel olarak AYRI."""
        self.use("TK-06")
        ang = math.radians(ang_deg)
        nx, ny = -math.sin(ang), math.cos(ang)
        for i in range(count):
            o = (i - (count - 1) / 2.0) * spacing
            cx, cy = x + nx * o, y + ny * o
            pts = []
            for t in (-0.5, -0.25, 0.0, 0.25, 0.5):
                px = cx + length * t * math.cos(ang)
                py = cy + length * t * math.sin(ang)
                b = bow * (1 - (2 * t) ** 2)
                pts.append((px + nx * b, py + ny * b))
            self.curve(pts, role="seam_line")

    # ── TK-07 · strain / pull zone ────────────────────────────────────
    def tk07_strain_zone(self, x, y, rx, ry, step=3.6):
        """Seyrek nokta tramı. Gölge/dolgu olarak ASLA kullanılmaz."""
        self.use("TK-07")
        self._gray(0.45)
        n = 0
        i = -int(rx / step) - 1
        while i * step <= rx:
            j = -int(ry / step) - 1
            while j * step <= ry:
                px, py = x + i * step, y + j * step
                if ((px - x) / rx) ** 2 + ((py - y) / ry) ** 2 <= 1.0:
                    self._guard((px, py))
                    self.c.circle(px, py, 0.42, stroke=0, fill=1)
                    n += 1
                j += 1
            i += 1
        if n == 0:
            raise ForbiddenDrawing("TK-07 alanı boş çıktı — yarıçap tram adımından küçük.")

    # ── TK-08 · apex marker ───────────────────────────────────────────
    def tk08_apex(self, x, y, r=3.0):
        self.use("TK-08")
        self._guard((x - r, y - r), (x + r, y + r))
        self._gray(0.0); self._stroke("seam_line")
        self.c.circle(x, y, r, stroke=1, fill=0)
        self.line(x - r * 0.72, y, x + r * 0.72, y, role="construction_line")
        self.line(x, y - r * 0.72, x, y + r * 0.72, role="construction_line")

    # ── TK-09 · balance line ──────────────────────────────────────────
    def tk09_balance_line(self, x1, y1, x2, y2, label="B"):
        self.use("TK-09")
        self.line(x1, y1, x2, y2, role="balance_line")
        self.text(x2 + 2.4, y2 - 2.0, label, face="sans-semibold", size=6.5)

    # ── TK-10 · grainline ─────────────────────────────────────────────
    def tk10_grainline(self, x1, y1, x2, y2):
        self.use("TK-10")
        self.line(x1, y1, x2, y2, role="grainline")
        ang = math.atan2(y2 - y1, x2 - x1)
        self._gray(0.0); self._stroke("grainline")
        self._arrow_head(x2, y2, ang, size=4.0, filled=False)
        self._arrow_head(x1, y1, ang + math.pi, size=4.0, filled=False)

    # ── TK-11 · measurement caliper ───────────────────────────────────
    def tk11_measure_path(self, pts, label: str | None = None, label_side="right",
                          label_offset=5.0):
        """Ölçü yolu. dash 1-1 + iki uçta dik bitiş."""
        self.use("TK-11")
        self.curve(pts, role="construction_line", dash="dash 1-1",
                   width=self._lw["construction_line"])
        for (a, b) in ((pts[0], pts[1]), (pts[-1], pts[-2])):
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
            dx, dy = 2.8 * math.cos(ang), 2.8 * math.sin(ang)
            self.line(a[0] - dx, a[1] - dy, a[0] + dx, a[1] + dy, role="construction_line")
        if label:
            mid = pts[len(pts) // 2]
            dx = label_offset if label_side == "right" else -label_offset
            self.text(mid[0] + dx, mid[1] - 2.2, label,
                      anchor="start" if label_side == "right" else "end")

    def landmark_dot(self, x, y, r=1.5):
        """İşaret noktası — ölçü figürünün ZORUNLU unsuru (VISUAL_SPEC § 3)."""
        self._guard((x - r, y - r), (x + r, y + r))
        self._gray(0.0); self._stroke("seam_line")
        self.c.circle(x, y, r, stroke=1, fill=1)

    # ── TK-12 / TK-13 · before / after ────────────────────────────────
    def tk12_before(self, pts, close=False):
        self.use("TK-12")
        self.polyline(pts, role="pattern_edge_original", gray=0.45, close=close)

    def tk13_after(self, pts, close=False):
        self.use("TK-13")
        self.polyline(pts, role="pattern_edge_modified", gray=0.0, close=close)

    # ── TK-14 · step number ───────────────────────────────────────────
    def tk14_step(self, x, y, n: int, r=5.0):
        if n < 1:
            raise ForbiddenDrawing("TK-14: adım numaraları 1'den başlar.")
        self.use("TK-14")
        self._guard((x - r, y - r), (x + r, y + r))
        self._gray(0.0)
        self.c.circle(x, y, r, stroke=0, fill=1)
        self.c.setFillGray(1.0)
        self.c.setFont(font("sans-bold"), 7.0)
        self.c.drawCentredString(x, y - 2.4, str(n))
        self._gray(0.0)

    # ── TK-15 · do-not-do marker ──────────────────────────────────────
    def tk15_do_not_do(self, x, y, w, h, box=9.0):
        self.use("TK-15")
        self.line(x, y, x + w, y + h, role="garment_outline")
        bx, by = x + w - box, y + h
        self._guard((bx, by), (bx + box, by + box))
        self._gray(0.0); self._stroke("garment_outline")
        self.c.rect(bx, by, box, box, stroke=1, fill=0)
        self.line(bx + 2.0, by + 2.0, bx + box - 2.0, by + box - 2.0, role="garment_outline")
        self.line(bx + 2.0, by + box - 2.0, bx + box - 2.0, by + 2.0, role="garment_outline")

    # ── TK-16 / TK-17 / TK-18 · akış şeması düğümleri ─────────────────
    def _wrap(self, s, max_w, face="sans", size=7.0):
        words, lines, cur = s.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if self.text_width(t, face, size) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        return lines

    def tk17_observation_node(self, x, y, w, h, label, size=7.0):
        self.use("TK-17")
        self._guard((x, y), (x + w, y + h))
        self._gray(0.0); self._stroke("garment_outline"); self._dash("solid")
        self.c.roundRect(x, y, w, h, min(6.0, h / 2 - 0.5), stroke=1, fill=0)
        self._center_text(x, y, w, h, label, size=size)
        return (x, y, w, h)

    def tk16_decision_node(self, x, y, w, h, label, size=7.0):
        self.use("TK-16")
        self._guard((x, y), (x + w, y + h))
        self._gray(0.0); self._stroke("garment_outline"); self._dash("solid")
        p = self.c.beginPath()
        p.moveTo(x + w / 2, y + h); p.lineTo(x + w, y + h / 2)
        p.lineTo(x + w / 2, y); p.lineTo(x, y + h / 2); p.close()
        self.c.drawPath(p, stroke=1, fill=0)
        self._center_text(x + w * 0.16, y, w * 0.68, h, label, size=size)
        return (x, y, w, h)

    def tk18_handoff_node(self, x, y, w, h, label, af_id: str, size=7.0,
                          reader_ref: str | None = None):
        """Devir düğümü.

        `af_id` VERİ BAĞIDIR ve figürün kaydına girer; OKURA BASILMAZ.
        Okur "AF-01"i okuyamaz — o bir iç kimliktir
        (TYPOGRAPHY_STANDARD § 3.4). Okura basılan şey ailenin ADIDIR
        ve varsa okura dönük çapraz göndermedir (`reader_ref`).
        """
        if not af_id:
            raise ForbiddenDrawing("TK-18 devir düğümü bir AF veri bağı olmadan çizilemez.")
        self.use("TK-18")
        self._guard((x, y), (x + w, y + h))
        self._gray(0.0); self._stroke("pattern_edge_modified"); self._dash("solid")
        self.c.rect(x, y, w, h, stroke=1, fill=0)
        if reader_ref:
            self._center_text(x, y + 4.0, w, h - 4.0, label, size=size)
            self.text(x + w / 2, y + 3.0, reader_ref, face="sans-bold", size=6.5,
                      anchor="middle")
        else:
            self._center_text(x, y, w, h, label, size=size)
        return (x, y, w, h)

    def _center_text(self, x, y, w, h, label, face="sans", size=7.0):
        lines = self._wrap(label, w - 8.0, face, size)
        lh = size * 1.22
        top = y + h / 2 + (len(lines) - 1) * lh / 2 - size * 0.36
        for i, ln in enumerate(lines):
            self.text(x + w / 2, top - i * lh, ln, face=face, size=size, anchor="middle")

    def connector(self, x1, y1, x2, y2, label: str | None = None, elbow=True):
        """Düğümler arası bağlantı — dik açılı, ok başlı."""
        pts = [(x1, y1)]
        if elbow and abs(x1 - x2) > 0.5 and abs(y1 - y2) > 0.5:
            pts.append((x1, y2 + 0.0)) if False else pts.append((x1, (y1 + y2) / 2))
            pts.append((x2, (y1 + y2) / 2))
        pts.append((x2, y2))
        self.polyline(pts, role="callout_leader")
        ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        self._gray(0.0); self._stroke("callout_leader")
        self._arrow_head(x2, y2, ang, size=3.4, filled=True)
        if label:
            lx, ly = (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2
            self.text(lx + 2.4, ly, label, face="sans-semibold", size=6.5)

    # ── kalıp parçası ölçek beyanı ────────────────────────────────────
    def declare_scale(self, s: str):
        self.scale_declared = s
        self.text(2.0, 2.0, s, face="sans-italic", size=6.5, gray=0.45)

    # ── kapanış ───────────────────────────────────────────────────────
    # İç kayıt kimlikleri okura BASILMAZ (TYPOGRAPHY_STANDARD § 3.4).
    INTERNAL_ID = re.compile(r"\b(SYM|AF|M|BLK|TOP|XW|VAL|FIG|TK|S|C)-\d{2,4}\b")

    def check_internal_id_leak(self) -> list:
        return [s for (_x0, _y0, _x1, _y1, s) in self.labels
                if self.INTERNAL_ID.search(s)]

    def check_label_collisions(self, pad: float = 0.5) -> list:
        """Üst üste binen etiketleri bulur.

        Bir ölçüm kitabında çakışan iki etiket yanlış OKUNUR ve yanlış
        okunan bir ölçü okurun kumaşını götürür (RISK_REGISTER R-06).
        Bu yüzden çakışma bir estetik kusur değil, bir HATA'dır."""
        bad = []
        for i in range(len(self.labels)):
            ax0, ay0, ax1, ay1, at = self.labels[i]
            for j in range(i + 1, len(self.labels)):
                bx0, by0, bx1, by1, bt = self.labels[j]
                if ax0 < bx1 - pad and bx0 < ax1 - pad \
                        and ay0 < by1 - pad and by0 < ay1 - pad:
                    bad.append((at, bt))
        return bad

    def finish(self, *, allow_label_overlap: bool = False,
               internal_marks: bool = False) -> list[str]:
        if not internal_marks:
            leaked = self.check_internal_id_leak()
            if leaked:
                raise ForbiddenDrawing(
                    "İÇ KAYIT KİMLİĞİ OKURA BASILIYOR: " + ", ".join(repr(s) for s in leaked[:3])
                    + " — kayıt kimlikleri iç veri kimlikleridir ve okura gösterilmez "
                      "(TYPOGRAPHY_STANDARD § 3.4).")
        if self.surface == "pattern" and not self.scale_declared:
            raise ForbiddenDrawing(
                "ölçek belirtilmemiş kalıp parçası — VISUAL_STANDARD § 5.")
        if not allow_label_overlap:
            bad = self.check_label_collisions()
            if bad:
                raise ForbiddenDrawing(
                    "ÇAKIŞAN ETİKET: " + " · ".join(f"{a!r}↔{b!r}" for a, b in bad[:3])
                    + " — çakışan bir ölçü etiketi yanlış okunur.")
        if self.bound:
            self.c.restoreState()
        elif self.out_path:
            self.out_path.parent.mkdir(parents=True, exist_ok=True)
            self.c.showPage()
            self.c.save()
        return list(self.used)
