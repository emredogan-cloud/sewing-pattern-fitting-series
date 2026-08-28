#!/usr/bin/env python3
"""
calibrate_tokens.py — token değerlerini GERÇEK RENDER ile ölçer.

Faz 2 / G1 (BOOK-01/00_SPEC/PHASE_2_ROADMAP.md).

`visual_language_tokens.json` bugüne kadar `DESIGN_TARGET_NOT_CALIBRATED`
durumundaydı: içindeki her sayı bir HEDEFTİ. Bu script o hedefleri
ÖLÇÜLMÜŞ değerlere çevirir.

Yöntem — üç adım, hiçbiri tahmin değil:
  ① reportlab ile gerçek trim ölçüsünde (8,5×11 in) bir kalibrasyon
     sayfası basılır;
  ② pdftoppm ile 300 ve 600 dpi'de rasterlanır ve 1-bit'e indirilir;
  ③ Pillow ile piksel piksel ÖLÇÜLÜR: çizgi kalınlığı, kesik deseninin
     ayrık kalıp kalması, gri tonlarının gerçek mürekkep yoğunluğu,
     TK-05 ↔ TK-06 ayırt ediciliği, kesir gliflerinin varlığı, rakam
     ayırt ediciliği ve satır başına karakter.

⚠ ÖLÇÜMÜN SINIRI — bu script bir DİJİTAL RENDER ölçer, BASILI KÂĞIT
  DEĞİL. Talep-üzerine baskıda mürekkep yayılması (dot gain) bu ölçüme
  GİRMEZ. `TYPOGRAPHY_STANDARD § 4`'ün T3 ve T4 testleri gerçek prova
  baskısı ve ÜÇ İNSAN OKUYUCU gerektirir; ikisi de bu depodan
  yapılamaz (EXTERNAL_DEPENDENCIES.md D-05, D-06). Bu script onların
  YERİNE GEÇMEZ; onlardan ÖNCE elenebilecekleri eler.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from figure_tokens import FigureCanvas, font, register_fonts  # noqa: E402

from PIL import Image  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402

FRACTIONS = "⅛ ¼ ⅜ ½ ⅝ ¾ ⅞"
DIGIT_PAIRS = [("1", "l"), ("1", "I"), ("l", "I"), ("0", "O"), ("6", "8"),
               ("8", "9"), ("6", "9"), ("5", "6"), ("3", "8")]
PRIME = "″"


# ── ① kalibrasyon sayfası ─────────────────────────────────────────────
def build_sheet(out_pdf: Path, geom: dict, tokens: dict) -> dict:
    """Ölçülecek her şeyi BİLİNEN koordinatlara yerleştirir."""
    W = geom["trim"]["width_pt"]; H = geom["trim"]["height_pt"]
    fc = FigureCanvas(W, H, surface="diagram", out_path=out_pdf)
    idx: dict = {"strokes": [], "dashes": [], "grays": [], "text": {}}

    y = H - 54.0
    fc.text(45.0, y, "Kalibrasyon sayfasi — cizgi kalinlik hiyerarsisi",
            face="sans-semibold", size=11.0)
    y -= 22.0
    weights = {k: v for k, v in tokens["line_weights_pt"].items() if not k.startswith("$")}
    for role, w in sorted(weights.items(), key=lambda kv: -kv[1]):
        fc.line(160.0, y, 470.0, y, role=role)
        fc.text(45.0, y - 2.4, f"{role}  {w} pt", face="sans", size=8.0)
        idx["strokes"].append({"role": role, "pt": w, "y_pt": y, "x0": 160.0, "x1": 470.0})
        y -= 15.0

    y -= 10.0
    fc.text(45.0, y, "Kesik desenleri", face="sans-semibold", size=11.0)
    y -= 20.0
    for name, key in [("original_state", "solid"), ("hidden_or_underneath", "dash 2-2"),
                      ("cut_line_slash", "dash 4-2"), ("fold_line", "dash-dot 6-2-1-2"),
                      ("measurement_path", "dash 1-1")]:
        fc.line(160.0, y, 470.0, y, role="construction_line", dash=key)
        fc.text(45.0, y - 2.4, f"{name}  [{key}]", face="sans", size=8.0)
        idx["dashes"].append({"name": name, "pattern": key, "y_pt": y,
                              "x0": 160.0, "x1": 470.0})
        y -= 15.0

    y -= 10.0
    fc.text(45.0, y, "Gri tonlari — talep-uzerine baskida ezilme sinavi",
            face="sans-semibold", size=11.0)
    y -= 18.0
    for g in geom["print_safety"]["gray_levels"]:
        fc._gray(g)
        fc.c.rect(160.0, y - 12.0, 90.0, 14.0, stroke=0, fill=1)
        fc.text(45.0, y - 8.0, f"gray {g}", face="sans", size=8.0)
        idx["grays"].append({"gray": g, "rect": [160.0, y - 12.0, 90.0, 14.0]})
        y -= 20.0

    y -= 14.0
    fc.text(45.0, y, "TK-05 (cekme) ile TK-06 (kivrim) ayirt ediciligi",
            face="sans-semibold", size=11.0)
    y -= 60.0
    fc.tk05_drag_lines(200.0, y, 38.0)
    fc.tk06_excess_fold(360.0, y, 0.0)
    fc.text(140.0, y - 34.0, "TK-05", face="sans", size=8.0)
    fc.text(330.0, y - 34.0, "TK-06", face="sans", size=8.0)
    idx["tk05_box"] = [168.0, y - 26.0, 64.0, 52.0]
    idx["tk06_box"] = [328.0, y - 26.0, 64.0, 52.0]

    y -= 66.0
    fc.text(45.0, y, "Y1 — bayagi kesir glifleri", face="sans-semibold", size=11.0)
    y -= 18.0
    for size, face in ((10.5, "serif"), (9.0, "sans"), (7.0, "sans")):
        fc.text(60.0, y, FRACTIONS + "   " + f"5⁄8 in = {PRIME}", face=face, size=size)
        fc.text(400.0, y, f"{face} {size} pt", face="sans", size=7.0)
        idx["text"][f"frac_{face}_{size}"] = {"y_pt": y, "size": size, "face": face}
        y -= size * 1.9

    y -= 12.0
    fc.text(45.0, y, "Y3 — rakam ayirt ediciligi (6-7 pt figur etiketi bandi)",
            face="sans-semibold", size=11.0)
    y -= 16.0
    seq = "1 l I 0 O 6 8 9 3 5"
    for face in ("sans", "atkinson"):
        for size in (7.0, 6.5, 6.0):
            fc.text(60.0, y, seq, face=face, size=size)
            fc.text(220.0, y, f"{face} {size} pt", face="sans", size=7.0)
            idx["text"][f"digits_{face}_{size}"] = {"y_pt": y, "size": size, "face": face}
            y -= 13.0
        y -= 4.0

    y -= 6.0
    fc.text(45.0, y, "Metin olcusu — 499,5 pt sutunda satir basina karakter",
            face="sans-semibold", size=11.0)
    y -= 16.0
    sample = ("Bir kalip parcasini kesmeden once neyi degistirdiginizi bilmeniz gerekir; "
              "olcum once, teshis sonra, duzeltme en son gelir. ")
    body = float(geom["typography_grid"]["body_size_pt"])
    fc.text(45.0, y, sample[:110], face="serif", size=body)
    idx["text"]["measure_sample"] = {"y_pt": y, "size": body, "face": "serif",
                                     "string": sample}
    # Kalibrasyon sayfası bir İÇ ARAÇTIR ve okura basılmaz: token
    # kimliklerini (TK-05, TK-06) etiket olarak taşımak zorundadır,
    # çünkü ölçülen şey tam olarak o token'lardır. Etiket çakışması da
    # muaftır — sayfa yoğunluk sınırlarını sınamak için sıkıştırılmıştır.
    fc.finish(internal_marks=True, allow_label_overlap=True)
    return idx


# ── ② rasterle ────────────────────────────────────────────────────────
def rasterize(pdf: Path, dpi: int, out_prefix: Path) -> Image.Image:
    subprocess.run(["pdftoppm", "-r", str(dpi), "-gray", "-png", "-singlefile",
                    str(pdf), str(out_prefix)], check=True,
                   capture_output=True)
    return Image.open(str(out_prefix) + ".png").convert("L")


# ── ③ ölç ─────────────────────────────────────────────────────────────
def pt_to_px(v: float, dpi: int) -> float:
    return v * dpi / 72.0


def measure_stroke(img: Image.Image, dpi: int, sheet_h_pt: float,
                   rec: dict, threshold=128) -> dict:
    """Bir yatay çizginin GERÇEK piksel kalınlığı."""
    px = img.load()
    x = int(pt_to_px((rec["x0"] + rec["x1"]) / 2, dpi))
    y_center = int(pt_to_px(sheet_h_pt - rec["y_pt"], dpi))
    span = int(pt_to_px(6.0, dpi))
    dark = [yy for yy in range(y_center - span, y_center + span + 1)
            if 0 <= yy < img.height and px[x, yy] < threshold]
    if not dark:
        return {"role": rec["role"], "target_pt": rec["pt"], "measured_px": 0,
                "measured_pt": 0.0, "survives": False}
    runs, cur = [], [dark[0]]
    for a, b in zip(dark, dark[1:]):
        if b - a == 1:
            cur.append(b)
        else:
            runs.append(cur); cur = [b]
    runs.append(cur)
    thickest = max(runs, key=len)
    n = len(thickest)
    return {"role": rec["role"], "target_pt": rec["pt"], "measured_px": n,
            "measured_pt": round(n * 72.0 / dpi, 3),
            "expected_px": round(pt_to_px(rec["pt"], dpi), 2),
            "survives": n >= 1}


def measure_dash(img: Image.Image, dpi: int, sheet_h_pt: float, rec: dict,
                 threshold=128) -> dict:
    px = img.load()
    y = int(pt_to_px(sheet_h_pt - rec["y_pt"], dpi))
    x0, x1 = int(pt_to_px(rec["x0"], dpi)) + 2, int(pt_to_px(rec["x1"], dpi)) - 2
    band = []
    for x in range(x0, x1):
        col = any(px[x, yy] < threshold
                  for yy in range(y - 3, y + 4) if 0 <= yy < img.height)
        band.append(col)
    transitions = sum(1 for a, b in zip(band, band[1:]) if a != b)
    ink = sum(band) / max(len(band), 1)
    return {"name": rec["name"], "pattern": rec["pattern"],
            "transitions": transitions, "ink_ratio": round(ink, 3),
            "distinct_from_solid": transitions >= 2 or rec["pattern"] == "solid"}


def measure_gray(img: Image.Image, dpi: int, sheet_h_pt: float, rec: dict) -> dict:
    x, y, w, h = rec["rect"]
    x0 = int(pt_to_px(x + 4, dpi)); x1 = int(pt_to_px(x + w - 4, dpi))
    y0 = int(pt_to_px(sheet_h_pt - (y + h) + 3, dpi))
    y1 = int(pt_to_px(sheet_h_pt - y - 3, dpi))
    crop = img.crop((x0, y0, x1, y1))
    vals = list(crop.getdata())
    mean = sum(vals) / len(vals)
    return {"gray": rec["gray"], "target_luma": round((1 - rec["gray"]) * 255, 1),
            "measured_luma": round(mean, 1),
            "delta": round(abs(mean - (1 - rec["gray"]) * 255), 1)}


def crop_signature(img: Image.Image, dpi: int, sheet_h_pt: float, box: list) -> dict:
    """Bir işaretin yapısal imzası: mürekkep oranı, satır profili, bileşen sayısı."""
    x, y, w, h = box
    x0 = int(pt_to_px(x, dpi)); x1 = int(pt_to_px(x + w, dpi))
    y0 = int(pt_to_px(sheet_h_pt - (y + h), dpi)); y1 = int(pt_to_px(sheet_h_pt - y, dpi))
    crop = img.crop((x0, y0, x1, y1))
    px = crop.load()
    W, H = crop.size
    ink = 0
    row_profile = []
    for j in range(H):
        r = sum(1 for i in range(W) if px[i, j] < 128)
        row_profile.append(r); ink += r
    col_profile = [sum(1 for j in range(H) if px[i, j] < 128) for i in range(W)]
    # bağlı bileşenler (8-komşuluk) — piksel listeleriyle birlikte
    seen = [[False] * H for _ in range(W)]
    comp_pixels: list[list] = []
    for i in range(W):
        for j in range(H):
            if px[i, j] < 128 and not seen[i][j]:
                stack = [(i, j)]; seen[i][j] = True; blob = []
                while stack:
                    a, b = stack.pop(); blob.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < W and 0 <= nb < H and not seen[na][nb] \
                                    and px[na, nb] < 128:
                                seen[na][nb] = True; stack.append((na, nb))
                comp_pixels.append(blob)
    comps = len(comp_pixels)
    big = [b for b in comp_pixels if len(b) >= 20]
    curv = [_curvature_index(b) for b in big]
    return {"ink_ratio": round(ink / (W * H), 4), "components": comps,
            "significant_components": len(big),
            "row_profile_peaks": _peaks(row_profile),
            "col_profile_peaks": _peaks(col_profile),
            "curvature_index": round(sum(curv) / len(curv), 5) if curv else 0.0,
            "curvature_per_component": [round(c, 5) for c in curv],
            "size_px": [W, H]}


def _curvature_index(blob: list) -> float:
    """Bir işaret parçasının EĞRİLİK ENDEKSİ.

    TK-05 ile TK-06 arasındaki GERÇEK fark eğriliktir: biri düz çizgi
    kümesi, diğeri yay kümesidir. Mürekkep oranı ve bileşen sayısı bu
    farkı GÖRMEZ — iki işaret de üç parçadan oluşur ve neredeyse aynı
    mürekkebi kullanır. Bir testin ADI ile ÖLÇTÜĞÜ ŞEY aynı olmalıdır
    (DECISIONS.md K20); ilk sürüm bütün mürekkep bulutuna tek bir doğru
    uyduruyordu ve PARALEL DÜZ ÇİZGİLERİ de "eğri" sayıyordu.

    Yöntem: parçanın kendi ana eksenine (PCA) dik sapmanın karekök
    ortalaması, parçanın eksen boyunca uzunluğuna bölünür.
    Düz bir çizgide sonuç yalnızca çizgi kalınlığından gelir (≈0,01);
    yayda yay yüksekliğinden gelir (≈0,04+).
    """
    n = len(blob)
    mx = sum(p[0] for p in blob) / n
    my = sum(p[1] for p in blob) / n
    sxx = sum((p[0] - mx) ** 2 for p in blob)
    syy = sum((p[1] - my) ** 2 for p in blob)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in blob)
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ax, ay = math.cos(theta), math.sin(theta)
    nx, ny = -ay, ax
    along = [(p[0] - mx) * ax + (p[1] - my) * ay for p in blob]
    perp = [(p[0] - mx) * nx + (p[1] - my) * ny for p in blob]
    extent = max(along) - min(along)
    if extent < 1e-6:
        return 0.0
    rms = math.sqrt(sum(d * d for d in perp) / n)
    return rms / extent


def _peaks(profile: list) -> int:
    thr = max(profile) * 0.4 if profile else 0
    above = [p > thr for p in profile]
    return sum(1 for a, b in zip(above, above[1:]) if not a and b)


def glyph_coverage() -> dict:
    """Y1/T1: kesir glifleri ve inç işareti GERÇEKTEN var mı."""
    from reportlab.pdfbase.ttfonts import TTFontFile
    out = {}
    for key in ("serif", "sans", "atkinson"):
        rel = {"serif": "ttf/SourceSerif4-Regular.ttf",
               "sans": "ttf/SourceSans3-Regular.ttf",
               "atkinson": "ttf/AtkinsonHyperlegible-Regular.ttf"}[key]
        f = TTFontFile(str(paths.VISUAL_FONTS / rel))
        cmap = f.charToGlyph
        missing = [ch for ch in (FRACTIONS.replace(" ", "") + PRIME)
                   if ord(ch) not in cmap]
        out[key] = {"glyph_count": len(cmap), "missing": missing,
                    "y1_pass": not missing}
    return out


def digit_distinguishability(size: float) -> dict:
    """Y3'ün ÖLÇÜLEBİLİR yarısı: karıştırılabilir çiftlerin genişlik farkı.

    ⚠ Bu bir OKUNABİLİRLİK ölçümü DEĞİLDİR — genişlik farkı okurun
    ayırt edebildiğini KANITLAMAZ. T3'ün gerçek testi üç insan
    okuyucudur (TYPOGRAPHY_STANDARD § 4). Bu ölçüm yalnızca AÇIKÇA
    aynı genişlikte olan çiftleri işaretler."""
    register_fonts()
    out = {}
    for key in ("sans", "atkinson"):
        fname = font(key)
        pairs = {}
        for a, b in DIGIT_PAIRS:
            wa = pdfmetrics.stringWidth(a, fname, size)
            wb = pdfmetrics.stringWidth(b, fname, size)
            pairs[f"{a}/{b}"] = round(abs(wa - wb) / max(wa, wb, 1e-6), 4)
        out[key] = {"size_pt": size, "pair_width_delta_ratio": pairs,
                    "identical_width_pairs": [k for k, v in pairs.items() if v < 1e-6]}
    return out


def chars_per_line(geom: dict) -> dict:
    register_fonts()
    body = float(geom["typography_grid"]["body_size_pt"])
    width = float(geom["text_block"]["width_pt"])
    sample = ("Bir kalip parcasini kesmeden once neyi degistirdiginizi bilmeniz "
              "gerekir; olcum once, teshis sonra, duzeltme en son gelir.")
    per_char = pdfmetrics.stringWidth(sample, font("serif"), body) / len(sample)
    n = width / per_char
    lo, hi = geom["text_block"]["measure_target_chars"]
    return {"body_size_pt": body, "text_width_pt": width,
            "avg_char_width_pt": round(per_char, 3),
            "chars_per_line": round(n, 1), "target": [lo, hi],
            "in_target": lo <= n <= hi}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, nargs="*", default=[300, 600])
    ap.add_argument("--keep", default=None, help="kalibrasyon PDF'ini buraya kopyala")
    args = ap.parse_args()

    geom = json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))
    tokens = json.loads(paths.VISUAL_TOKENS.read_text(encoding="utf-8"))
    H = geom["trim"]["height_pt"]

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        pdf = tdp / "calibration_sheet.pdf"
        idx = build_sheet(pdf, geom, tokens)
        if args.keep:
            Path(args.keep).parent.mkdir(parents=True, exist_ok=True)
            Path(args.keep).write_bytes(pdf.read_bytes())

        per_dpi = {}
        for dpi in args.dpi:
            img = rasterize(pdf, dpi, tdp / f"cal_{dpi}")
            strokes = [measure_stroke(img, dpi, H, r) for r in idx["strokes"]]
            dashes = [measure_dash(img, dpi, H, r) for r in idx["dashes"]]
            grays = [measure_gray(img, dpi, H, r) for r in idx["grays"]]
            bw = img.point(lambda v: 0 if v < 128 else 255, mode="L")
            s5 = crop_signature(bw, dpi, H, idx["tk05_box"])
            s6 = crop_signature(bw, dpi, H, idx["tk06_box"])
            per_dpi[str(dpi)] = {
                "strokes": strokes,
                "dashes": dashes,
                "grays": grays,
                "tk05_signature": s5,
                "tk06_signature": s6,
                "tk05_tk06_distinguishable": _distinguishable(s5, s6),
                "all_strokes_survive_1bit": all(s["survives"] for s in strokes),
                "thinnest_stroke_px": min(s["measured_px"] for s in strokes),
            }

    report = {
        "$comment": [
            "CALIBRATION REPORT — 06_BUILD/calibrate_tokens.py çıktısı.",
            "Faz 2 / G1. Her sayı bir RENDER ölçümüdür.",
            "",
            "⚠ SINIR: bu ölçüm DİJİTAL rasterdır. Talep-üzerine baskının",
            "  mürekkep yayılması ölçüme GİRMEZ. T3 (üç insan okuyucu) ve",
            "  T4 (gerçek prova baskısı) DIŞ BAĞIMLILIKTIR —",
            "  EXTERNAL_DEPENDENCIES.md D-05, D-06.",
        ],
        "measured_on": "2026-08-28",
        "tool_chain": {
            "renderer": "reportlab " + __import__("reportlab").Version,
            "rasterizer": "pdftoppm (poppler)",
            "analyzer": "Pillow " + __import__("PIL").__version__,
        },
        "page_geometry_profile": geom["profile_id"],
        "per_dpi": per_dpi,
        "glyph_coverage_T1": glyph_coverage(),
        "digit_width_Y3_partial": {str(s): digit_distinguishability(s)
                                   for s in (7.0, 6.5, 6.0)},
        "text_measure_G2": chars_per_line(geom),
    }
    paths.CALIBRATION_REPORT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("▸ calibrate_tokens.py")
    for dpi, r in per_dpi.items():
        print(f"  {dpi} dpi · en ince çizgi {r['thinnest_stroke_px']} px · "
              f"hepsi 1-bit'te hayatta: {r['all_strokes_survive_1bit']} · "
              f"TK-05↔TK-06 ayrık: {r['tk05_tk06_distinguishable']['verdict']}")
    gc = report["glyph_coverage_T1"]
    for k, v in gc.items():
        print(f"  T1 {k:<9} kesir+inç glifleri: "
              f"{'TAM' if v['y1_pass'] else 'EKSİK ' + ''.join(v['missing'])}")
    tm = report["text_measure_G2"]
    print(f"  G2 satır başına karakter: {tm['chars_per_line']} "
          f"(hedef {tm['target'][0]}–{tm['target'][1]}) → "
          f"{'HEDEFTE' if tm['in_target'] else 'HEDEF DIŞI'}")
    return 0


def _distinguishable(s5: dict, s6: dict) -> dict:
    """TK-05 ile TK-06 aynı sayfada karışır mı — VISUAL_SPEC § 4'ün
    teknik gerekliliği. Üç bağımsız eksende karşılaştırılır."""
    ink = abs(s5["ink_ratio"] - s6["ink_ratio"]) / max(s5["ink_ratio"], s6["ink_ratio"], 1e-9)
    comp = s5["components"] != s6["components"]
    prof = abs(s5["col_profile_peaks"] - s6["col_profile_peaks"])
    c5, c6 = s5["curvature_index"], s6["curvature_index"]
    ratio = c6 / c5 if c5 > 1e-9 else float("inf")
    axes = sum([ink > 0.15, comp, prof >= 1, ratio >= 2.0])
    return {"ink_delta_ratio": round(ink, 3),
            "component_counts": [s5["components"], s6["components"]],
            "col_peak_delta": prof,
            "curvature_index": {"TK-05": c5, "TK-06": c6},
            "curvature_ratio": round(ratio, 2) if ratio != float("inf") else None,
            "curvature_threshold": 2.0,
            "axes_differing": axes,
            "primary_axis": "curvature",
            "verdict": ("AYRIK — eğrilik ekseni" if ratio >= 2.0 else
                        ("ZAYIF — yalnızca ikincil eksenlerde ayrışıyor" if axes >= 2
                         else "RİSKLİ — ELLE İNCELE"))}


if __name__ == "__main__":
    sys.exit(main())
