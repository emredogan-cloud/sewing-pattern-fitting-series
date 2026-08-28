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
BLOCK_COMPONENTS = TAXONOMY_PUBLIC / "block_components.json"
BOUNDARY_MATRIX = TAXONOMY / "boundary_matrix.json"
TERMINOLOGY = TAXONOMY / "terminology.json"
VISUAL_TOKENS = VISUAL / "visual_language_tokens.json"

BOOK_DIRS = {
    "book-01": ROOT / "BOOK-01-MEASURE-AND-DIAGNOSE",
    "book-02": ROOT / "BOOK-02-THE-ADJUSTMENT-ATLAS",
    "book-03": ROOT / "BOOK-03-DRAFT-YOUR-OWN-BLOCK",
}

def book_spec(book_id):
    return BOOK_DIRS[book_id] / "00_SPEC"

def book_gate_file(book_id):
    return BOOK_DIRS[book_id] / ".gate"

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
    "phase3-pilot",      # P3 — pilot + KILL-GATE (fark testi + fiziksel doğrulama)
    "phase4-production", # P4 — tam içerik üretimi
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
