#!/usr/bin/env python3
"""
validate_structure.py — depo, belge ve içerik-koruma denetimi.

Desen: KOREAN-HANGUL-HANDWRITING-WORKBOOK validate_structure.py.

⚠ FARKLAR (bilinçli — DECISIONS.md K9 / CONTENT_PROTECTION.md):
  ① Bu bir SERİ deposudur: üç kitabın da kendi zorunlu belgeleri
     ayrıca denetlenir.
  ② "Cevap alanı" koruması YOKTUR (kalıp geometrisi sır değildir);
     yerine ÜÇ hat vardır: yayın-öncesi içerik, fiziksel doğrulama
     FOTOĞRAFLARI (gerçek insan bedeni — gizlilik), telif korumalı
     referans malzeme.
  ③ Kardeş projelerde OLMAYAN dördüncü hat: MARKA SIZINTISI. Ticari
     kalıp markaları başlık/metadata dosyalarında geçemez (KDP
     Metadata Guidelines — IP_AND_BRAND_POLICY.md § 1).
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

PROTECTED_DIR_PATTERNS = [
    "02_TAXONOMY/protected",
    "01_SOURCE/reference_material",
]
PROTECTED_BOOK_SUBDIRS = ["02_CONTENT/protected", "04_EDITORIAL/pilot"]
EXEMPT_BASENAMES = {".gitkeep", "README.md"}

PHOTO_LEAK_PATTERNS = [
    re.compile(r"(^|/)validation_photos/"),
    re.compile(r"_fitting_photo\.", re.I),
    re.compile(r"_muslin_photo\.", re.I),
]

# IP_AND_BRAND_POLICY.md § 1 — ticari kalıp markaları.
BRAND_TOKENS = [
    "mccall", "mccall's", "simplicity", "vogue patterns", "butterick",
    "burda", "burdastyle", "new look pattern", "kwik sew",
]
# Marka adının MEŞRU geçebileceği yerler (politika/karar belgeleri):
BRAND_ALLOWED_FILES = {
    "00_CONTEXT/IP_AND_BRAND_POLICY.md",
    "00_CONTEXT/SERIES_KEYWORD_ARCHITECTURE.md",
    "DECISIONS.md", "RISK_REGISTER.md", "OPEN_QUESTIONS.md",
    "06_BUILD/validate_structure.py", "07_TESTS/selftest.py",
}
# Marka taraması YALNIZCA bu tür dosyalarda yapılır (başlık/metadata yüzeyi):
BRAND_SCANNED_SUFFIXES = ("metadata.json", "TITLE.md", "KEYWORDS.md", "BLURB.md")

REQUIRED_SERIES_DOCS = [
    "README.md", "PROJECT_CONTEXT.md", "SERIES_ROADMAP.md", "ROADMAP_PROGRESS.md",
    "DECISIONS.md", "CHANGELOG.md", "OPEN_QUESTIONS.md", "RISK_REGISTER.md",
    ".gate", "series_config.json",
    "00_CONTEXT/BRIEF.md",
    "00_CONTEXT/REFERENCE_SYNTHESIS.md",
    "00_CONTEXT/SERIES_POSITIONING.md",
    "00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md",
    "00_CONTEXT/SERIES_KEYWORD_ARCHITECTURE.md",
    "00_CONTEXT/SERIES_CROSSSELL_ARCHITECTURE.md",
    "00_CONTEXT/VISUAL_STANDARD.md",
    "00_CONTEXT/SOURCING_STANDARD.md",
    "00_CONTEXT/QA_STANDARD.md",
    "00_CONTEXT/VALIDATION_PROTOCOL.md",
    "00_CONTEXT/CLAIMS_STANDARD.md",
    "00_CONTEXT/IP_AND_BRAND_POLICY.md",
    "00_CONTEXT/CONTENT_PROTECTION.md",
    "00_CONTEXT/STYLE.md",
    "00_CONTEXT/MEDIUM_DECISION_FRAMEWORK.md",
    "00_CONTEXT/FORMAT_STRATEGY.md",
    "00_CONTEXT/REUSE_MAP.md",
    # Faz 1 yürütmesinde eklendi (DECISIONS.md K24, K28, K19):
    "00_CONTEXT/TYPOGRAPHY_STANDARD.md",
    "00_CONTEXT/ADS_FRAMEWORK.md",
    "01_SOURCE/PUBLIC_SOURCE_SURVEY.md",
    "01_SOURCE/ACQUISITION_REQUEST_QUEUE.md",
]
REQUIRED_BOOK_DOCS = ["ROADMAP.md", "book_config.json", ".gate", "README.md"]


def git_ls_files() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=paths.ROOT,
                             capture_output=True, text=True, check=True)
        return [l for l in out.stdout.splitlines() if l.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def check_required_docs(errors: list):
    for rel in REQUIRED_SERIES_DOCS:
        if not (paths.ROOT / rel).exists():
            errors.append(f"gerekli seri belgesi eksik: {rel}")
    for book_id, bdir in paths.BOOK_DIRS.items():
        if not bdir.exists():
            errors.append(f"kitap dizini eksik: {bdir.name}")
            continue
        for rel in REQUIRED_BOOK_DOCS:
            if not (bdir / rel).exists():
                errors.append(f"gerekli kitap belgesi eksik: {bdir.name}/{rel}")


def check_book_gate_validity(errors: list):
    for book_id in paths.BOOK_DIRS:
        try:
            paths.read_book_gate(book_id)
        except ValueError as e:
            errors.append(str(e))


def check_protected_dirs(tracked: list, errors: list):
    if not tracked:
        errors.append("git ls-files boş döndü — çalışan bir git deposu yok; "
                      "sızıntı denetimi bu koşulda YAPILAMAZ.")
        return
    dirs = list(PROTECTED_DIR_PATTERNS)
    for bdir in paths.BOOK_DIRS.values():
        dirs += [f"{bdir.name}/{s}" for s in PROTECTED_BOOK_SUBDIRS]
    for d in dirs:
        for t in tracked:
            if t.startswith(d + "/") and t.rsplit("/", 1)[-1] not in EXEMPT_BASENAMES:
                errors.append(f"KORUMALI DİZİNDE TAKİP EDİLEN DOSYA: {t} — "
                              f"{d} hiçbir gerçek dosya taşıyamaz (CONTENT_PROTECTION.md § 2).")


def check_photo_leak(tracked: list, errors: list):
    """Hat 3: gerçek insan bedeninin fotoğrafı ASLA depoya girmez."""
    for t in tracked:
        for pat in PHOTO_LEAK_PATTERNS:
            if pat.search(t):
                errors.append(f"FİZİKSEL DOĞRULAMA FOTOĞRAFI TAKİP EDİLİYOR: {t} — "
                              f"gerçek bir kişinin vücut görüntüsü depoya giremez "
                              f"(CONTENT_PROTECTION.md § 3).")
                break


def check_brand_leak(errors: list):
    """Hat 4: ticari kalıp markaları başlık/metadata yüzeyinde geçemez."""
    for f in sorted(paths.ROOT.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(paths.ROOT).as_posix()
        if rel.startswith((".git/", "06_BUILD/__pycache__/")):
            continue
        if rel in BRAND_ALLOWED_FILES:
            continue
        if not rel.endswith(BRAND_SCANNED_SUFFIXES):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        for b in BRAND_TOKENS:
            if b in text:
                errors.append(f"MARKA SIZINTISI: {rel} içinde ticari kalıp markası {b!r} — "
                              f"KDP Metadata Guidelines başlıkta/metadata'da izinsiz marka "
                              f"kullanımını yasaklar (IP_AND_BRAND_POLICY.md § 1).")


# Bir kardeş depo adının GERÇEK bir bağımlılığa dönüştüğü sözdizimsel
# bağlamlar. Salt ATIF (docstring'de "desen: X projesinden devralındı")
# bir ihlal DEĞİLDİR ve kardeş projelerin kendi kongvansiyonudur —
# bu yüzden çıplak metin araması yapılmaz, yalnızca bu bağlamlar aranır.
DEPENDENCY_CONTEXT = ("import ", "sys.path", "Path(", "open(", "../", "..\\", "subprocess")


def check_no_sibling_dependency(errors: list):
    """K2: hiçbir kardeş depo bu deponun build'i için GEREKLİ olamaz.

    Yalnızca gerçek bağımlılık bağlamları taranır (bkz. DEPENDENCY_CONTEXT);
    mimari atıf yorumları serbesttir."""
    siblings = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))["series"]["isolatedFrom"]
    for f in sorted(paths.BUILD.glob("*.py")) + sorted(paths.TESTS.glob("*.py")):
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if not any(ctx in line for ctx in DEPENDENCY_CONTEXT):
                continue
            for s in siblings:
                if s in line:
                    errors.append(
                        f"İZOLASYON İHLALİ: {f.name}:{lineno} kardeş depoya ({s}) BAĞIMLILIK "
                        f"bağlamında atıf yapıyor — hiçbir kardeş depo build için gerekli "
                        f"olamaz (DECISIONS.md K2)."
                    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    errors: list[str] = []
    tracked = git_ls_files()
    check_required_docs(errors)
    check_book_gate_validity(errors)
    check_protected_dirs(tracked, errors)
    check_photo_leak(tracked, errors)
    check_brand_leak(errors)
    check_no_sibling_dependency(errors)

    result = {"tracked_file_count": len(tracked), "errors": errors, "passed": not errors}
    print(f"▸ validate_structure.py — {len(tracked)} izlenen dosya")
    if errors:
        print(f"  ✗ {len(errors)} hata:")
        for e in errors:
            print(f"    - {e}")
    else:
        print("  ✓ 0 hata")
    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
