"""
paths.py — tek yol tablosu.

Desen: KOREAN-HANGUL-HANDWRITING-WORKBOOK / LICENSE-AND-LAUNCH-
CALIFORNIA-LIFE-HEALTH paths.py. Hiçbir script kendi yol dizesini
kurmaz; hepsi buradan okur.

⚠ KARDEŞ PROJELERDEN YAPISAL FARK (DECISIONS.md K2/K3): bu depo ÜÇ
kitaplık bir SERİ taşır. Bu yüzden iki kapı katmanı vardır:
  · seri kapısı  (.gate, kökte)              → ortak mimarinin donması
  · kitap kapısı (BOOK-xx/.gate)             → o kitabın faz ilerlemesi
Biri diğerinin yerine GEÇMEZ ve biri diğerini otomatik İLERLETMEZ.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONTEXT = ROOT / "00_CONTEXT"
SOURCE = ROOT / "01_SOURCE"
SOURCE_RECORDS = SOURCE / "records"
SOURCE_REFERENCE_MATERIAL = SOURCE / "reference_material"
TAXONOMY = ROOT / "02_TAXONOMY"
TAXONOMY_PUBLIC = TAXONOMY / "public"
TAXONOMY_PROTECTED = TAXONOMY / "protected"
VISUAL = ROOT / "03_VISUAL"
VISUAL_NOTATION = VISUAL / "notation"
VISUAL_TEMPLATES = VISUAL / "templates"
VISUAL_GENERATED = VISUAL / "generated"
VISUAL_FONTS = VISUAL / "fonts"
VISUAL_FONTS_TTF = VISUAL_FONTS / "ttf"
FONTS_MANIFEST = VISUAL_FONTS / "fonts_manifest.json"
BUILD = ROOT / "06_BUILD"
TESTS = ROOT / "07_TESTS"
TESTS_FIXTURES = TESTS / "fixtures"
REPORTS = ROOT / "08_REPORTS"
REPORTS_TRACKED = REPORTS / "tracked"
OUTPUT = ROOT / "09_OUTPUT"
ARCHIVE = ROOT / "10_ARCHIVE"

GATE_FILE = ROOT / ".gate"
SERIES_CONFIG = ROOT / "series_config.json"

SOURCE_SCHEMA = SOURCE / "source_schema.json"
SYMPTOM_SCHEMA = TAXONOMY / "symptom_schema.json"
ADJUSTMENT_SCHEMA = TAXONOMY / "adjustment_schema.json"
CROSSWALK_SCHEMA = TAXONOMY / "crosswalk_schema.json"
MEASUREMENT_SCHEMA = TAXONOMY / "measurement_schema.json"
FIGURE_SCHEMA = VISUAL / "figure_schema.json"

FIT_SIGNS = TAXONOMY_PUBLIC / "fit_signs.json"
ADJUSTMENT_FAMILIES = TAXONOMY_PUBLIC / "adjustment_families.json"
MEASUREMENTS = TAXONOMY_PUBLIC / "measurements.json"
CROSSWALK = TAXONOMY_PUBLIC / "crosswalk.json"
LABELS_EN = TAXONOMY_PUBLIC / "labels_en.json"
BLOCK_COMPONENTS = TAXONOMY_PUBLIC / "block_components.json"
EASE_BANDS = TAXONOMY_PUBLIC / "ease_bands.json"
BOUNDARY_MATRIX = TAXONOMY / "boundary_matrix.json"
TERMINOLOGY = TAXONOMY / "terminology.json"
VISUAL_TOKENS = VISUAL / "visual_language_tokens.json"
PAGE_GEOMETRY = VISUAL / "page_geometry.json"
CALIBRATION_REPORT = VISUAL / "calibration_report.json"
EXTERNAL_DEPENDENCIES = ROOT / "EXTERNAL_DEPENDENCIES.md"

BOOK_DIRS = {
    "book-01": ROOT / "BOOK-01-MEASURE-AND-DIAGNOSE",
    "book-02": ROOT / "BOOK-02-THE-ADJUSTMENT-ATLAS",
    "book-03": ROOT / "BOOK-03-DRAFT-YOUR-OWN-BLOCK",
}

def book_spec(book_id):
    return BOOK_DIRS[book_id] / "00_SPEC"

def book_gate_file(book_id):
    return BOOK_DIRS[book_id] / ".gate"

def book_figures(book_id):
    return BOOK_DIRS[book_id] / "03_VISUAL" / "figures.json"

def book_generated(book_id):
    return BOOK_DIRS[book_id] / "03_VISUAL" / "generated"

# ── Kapı sıraları — ROADMAP belgeleriyle BİREBİR eşleşir ──────────────
SERIES_GATE_ORDER = [
    "bootstrap",            # proje makinesi kuruldu
    "series-architecture",  # ortak mimari donduruldu + Kitap 1 Faz 1 ONAYLANDI
    "production",           # en az bir kitap kill-gate'i geçti, tam üretim açık
    "catalog",              # ≥2 kitap yayında, çapraz satış mimarisi canlı
    "release",              # seri tamamlandı
]

BOOK_GATE_ORDER = [
    "init",              # klasör + roadmap var, kendi P0'ı çalışmadı
    "foundation",        # P0 — proje temeli
    "phase1-spec",       # P1 — araştırma + içerik spesifikasyonu
    "phase2-visual",     # P2 — görsel sistem + diyagram motoru
    # ── KURUCU GEÇERSİZ KILMA (K49) ─────────────────────────────────
    # P4, yol haritasında P3'ün PASS'ine bağlıdır. Kurucu, P3'ün İKİ
    # DIŞ ÖLÇÜMÜNÜ beklemeden üretimin sürmesine izin verdi ama
    # ölçümlerin PASS yazılmasını AÇIKÇA yasakladı.
    #
    # Bu seviye o iki şeyi aynı anda kaydeder. Kümülatif sırada
    # phase3-pilot'tan ÖNCEDİR: yani "P4 üretimi yapıldı" DOĞRU olur,
    # "P3 geçildi" ise gate_at_least(bgate, 'phase3-pilot') altında
    # HÂLÂ YANLIŞ kalır. Bir bayrak, olmayan bir ölçümü var edemez.
    #
    # Sonuç: P5 (phase5-qa) ve sonrası bu yoldan AÇILAMAZ. Kill-gate
    # ölçüldüğünde kapı phase3-pilot'a ilerler ve zincir devam eder.
    "phase4-production-conditional",
    # ── DIŞ DOĞRULAMA ERİŞİLEMEZ (K58) ──────────────────────────────
    # Kurucu, D-01 (üç ev dikişçisi) ve D-02 (fiziksel toile) için
    # pratik erişimin OLMADIĞINI açıkça bildirdi. İki ölçüm de
    # YAPILMADI ve YAPILAMAYACAK. Proje bunu bir PASS'e çevirmez;
    # yerine İÇSEL doğrulama ikamesi koyar ve sınırı beyan eder.
    #
    # Bu seviye de kümülatif sırada phase3-pilot'tan ÖNCEDİR:
    #   gate_at_least(g, "phase5-qa-internal") → True   (içsel KA bitti)
    #   gate_at_least(g, "phase3-pilot")       → FALSE  (P3 OLMADI)
    #   gate_at_least(g, "phase5-qa")          → FALSE  (gerçek P5 P3 ister)
    # Yani "içsel KA tamamlandı" DOĞRU olur, "kill-gate geçildi" ise
    # HÂLÂ YANLIŞ kalır. Tarih yeniden yazılmaz.
    "phase5-qa-internal",
    "phase3-pilot",      # P3 — pilot + KILL-GATE (fark testi + fiziksel doğrulama)
    "phase4-production", # P4 — tam içerik üretimi (kill-gate GEÇİLMİŞ hâli)
    "phase5-qa",         # P5 — teknik/editoryal/görsel/fiziksel KA
    "phase6-format",     # P6 — format + render + KDP
    "release",           # P7 — lansman
]


def _read(path, order, default):
    if not path.exists():
        return default
    level = path.read_text(encoding="utf-8").strip()
    if level not in order:
        raise ValueError(f"{path} geçersiz bir kapı seviyesi taşıyor: {level!r}")
    return level


def read_series_gate() -> str:
    return _read(GATE_FILE, SERIES_GATE_ORDER, "bootstrap")


def read_book_gate(book_id: str) -> str:
    return _read(book_gate_file(book_id), BOOK_GATE_ORDER, "init")


def gate_at_least(current: str, required: str, order: list) -> bool:
    """Kümülatif kapı karşılaştırması. order AÇIKÇA verilir — iki katman
    yanlışlıkla birbiriyle karşılaştırılamasın diye."""
    return order.index(current) >= order.index(required)
