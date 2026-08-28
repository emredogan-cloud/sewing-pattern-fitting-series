#!/usr/bin/env python3
"""
qa_terminology.py — seri sözlüğü tutarlılık denetimi.

Kural (SERIES_CONTENT_ARCHITECTURE.md TOP-28): bir terim BİR kitapta
kurulur; diğer ikisi tanımı değiştiremez. Yasak eşanlamlıların kullanımı
serinin ortak dilini bozar ve okurun üç kitap arasında taşıdığı bilgiyi
geçersiz kılar.

İki hat:
  ① YASAK EŞANLAMLI — terminology.json'daki banned_synonyms geçiyor mu.
  ② TANIMSIZ ANAHTAR TERİM — bir spesifikasyon belgesi AF-xx/SYM-xxx/
     M-xxx/T-xx kimliği kullanıyorsa o kimlik gerçekten tanımlı mı.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

from trfold import fold as _fold  # noqa: E402  (TEK KOPYA — trfold.py, K16)

SCAN_GLOBS = ["00_CONTEXT/*.md", "BOOK-*/00_SPEC/*.md", "BOOK-*/02_CONTENT/public/*.md"]
# Terimleri TANIMLAYAN belgeler yasak-eşanlamlı taramasından muaftır:
# yasağı yazabilmek için yasaklı ifadeyi ADLANDIRMAK zorundadırlar.
GLOSSARY_FILES = {"00_CONTEXT/STYLE.md", "00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md"}

# Anahtar kelime belgeleri de muaftır — ama BAŞKA bir gerekçeyle:
# oradaki ifadeler BİZİM dilimiz değil, ALICININ arama kutusuna yazdığı
# dildir. Alıcı "wrinkles in bodice" yazar; biz kitapta "drag line"
# yazarız. İkisini aynı kurala tabi tutmak, hedeflememiz GEREKEN
# kelimeleri yasaklamak olurdu.
KEYWORD_FILES = {"00_CONTEXT/SERIES_KEYWORD_ARCHITECTURE.md"}
EXEMPT_FROM_BANNED_SYNONYMS = GLOSSARY_FILES | KEYWORD_FILES

ID_PATTERNS = {
    "AF": re.compile(r"\bAF-\d{2}\b"),
    "SYM": re.compile(r"\bSYM-\d{3}\b"),
    "M": re.compile(r"\bM-\d{3}\b"),
    "T": re.compile(r"\bT-\d{2}\b"),
    "TOP": re.compile(r"\bTOP-\d{2}\b"),
    "BLK": re.compile(r"\bBLK-\d{2}\b"),
    "TK": re.compile(r"\bTK-\d{2}\b"),
}


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    findings: list[str] = []
    terms = load(paths.TERMINOLOGY)["terms"]
    banned = {}
    for t in terms:
        for b in t.get("banned_synonyms", []):
            # "garment alteration (bu ayrı bir şeydir)" → yalnızca terim kısmı
            core = b.split("(")[0].strip()
            if core:
                banned[_fold(core)] = t["term"]

    known = {
        "AF": {f["adjustment_family_id"] for f in load(paths.ADJUSTMENT_FAMILIES)["families"]},
        "SYM": {s["symptom_id"] for s in load(paths.FIT_SIGNS)["signs"]},
        "M": {m["measurement_id"] for m in load(paths.MEASUREMENTS)["measurements"]},
        "T": {t["term_id"] for t in terms},
        "TOP": {t["topic_id"] for t in load(paths.BOUNDARY_MATRIX)["topics"]},
        "BLK": {b["block_id"] for b in load(paths.BLOCK_COMPONENTS)["blocks"]},
        "TK": {t["token_id"] for t in load(paths.VISUAL_TOKENS)["tokens"]},
    }

    scanned = 0
    for g in SCAN_GLOBS:
        for f in sorted(paths.ROOT.glob(g)):
            rel = f.relative_to(paths.ROOT).as_posix()
            scanned += 1
            text = f.read_text(encoding="utf-8", errors="ignore")
            folded = _fold(text)
            if rel not in EXEMPT_FROM_BANNED_SYNONYMS:
                for bad, canonical in banned.items():
                    if bad in folded:
                        findings.append(
                            f"{rel}: YASAK EŞANLAMLI {bad!r} — kanonik terim {canonical!r} "
                            f"(02_TAXONOMY/terminology.json)"
                        )
            for kind, pat in ID_PATTERNS.items():
                for m in set(pat.findall(text)):
                    if m not in known[kind]:
                        findings.append(f"{rel}: TANIMSIZ KİMLİK {m} — taksonomide karşılığı yok.")

    result = {"scanned": scanned, "terms": len(terms), "findings": findings, "passed": not findings}
    print(f"▸ qa_terminology.py — {scanned} belge · {len(terms)} terim")
    if findings:
        print(f"  ✗ {len(findings)} bulgu:")
        for x in findings:
            print(f"    - {x}")
    else:
        print("  ✓ 0 bulgu")
    if args.json:
        out = Path(args.json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
