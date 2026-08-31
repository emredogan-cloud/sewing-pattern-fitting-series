#!/usr/bin/env python3
"""
qa_claims.py — iddia disiplini denetimi.

Desen: KOREAN-HANGUL-HANDWRITING-WORKBOOK qa_language.py'nin sahte-uzman
ve korunan-iddia taramaları; bu ürünün kendi riskleriyle yeniden
tasarlandı (DECISIONS.md K12).

Üç hat:
  ① SAHTE UZMAN İDDİASI — gerçek bir insan uzman kullanılmadıkça
     "expert-verified", "tested by a professional", "SME approved" gibi
     ifadeler yazılamaz. Kurucu kararı: bu seride de dış uzman İŞE
     ALINMAYACAK (DECISIONS.md K6, sigorta K9 / Hangıl K5 zincirinin
     devamı). AI incelemesi uzman DEĞİLDİR.
  ② KORUNAN İDDİA — "basılı formatın avantajı" iddiası araştırma
     raporunun § 27 girdi geçerliliği testinde ZAYIF çıktı. Bu iddia
     bir GERÇEK gibi kullanılamaz. (Hangıl projesindeki A6 hafıza-iddiası
     korumasının bu projedeki karşılığı.)
  ③ DOĞRULANMAMIŞ FİZİKSEL İDDİA — "tested", "validated", "proven"
     gibi kelimeler bir VAL-xxxx kaydına bağlı olmadan kullanılamaz.

Türkçe büyük 'İ' kusuru (kardeş projelerde SONRADAN bulunan gerçek bir
hata) burada BAŞTAN kapatıldı: _fold() Unicode-doğru katlama yapar ve
inkâr farkındalığı CÜMLE düzeyindedir, pencere düzeyinde değil.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

from trfold import fold as _fold  # noqa: E402  (TEK KOPYA — trfold.py, K16)


FAKE_EXPERT = [
    "expert-verified", "expert verified", "verified by an expert",
    "reviewed by a professional", "professional tailor verified",
    "sme approved", "sme onaylı", "uzman onaylı", "uzman tarafından doğrulandı",
    "terzi onaylı", "pattern maker verified", "kalıpçı onaylı",
]
PRINT_ADVANTAGE = [
    "print is better than video", "basılı format üstündür",
    "printed format has a proven advantage", "basılı formatın kanıtlanmış avantajı",
    "video gerekmez", "video is unnecessary",
]
UNBACKED_VALIDATION = [
    "physically validated", "fiziksel olarak doğrulandı",
    "every diagram was tested", "her diyagram test edildi",
    "proven to fit", "oturduğu kanıtlandı",
]
NEGATION_CUES = [
    "değil", "yoktur", "yok.", "asla", "yasak", "kullanılamaz", "kullanılmaz",
    "yazılamaz", "iddia edilemez", "not ", "never", "cannot", "must not",
    "olmadıkça", "olmadan", "zayıf", "doğrulanmadı", "unverified", "kanıtlanmadı",
]

SCAN_GLOBS = [
    "00_CONTEXT/*.md", "BOOK-*/00_SPEC/*.md", "BOOK-*/02_CONTENT/public/*.md",
    "08_REPORTS/PHASE_*.md", "BOOK-*/08_REPORTS/PHASE_*.md", "03_VISUAL/**/*.md",
]
# Bu belgeler yasağın KENDİSİNİ tanımlar; içlerinde ifade GEÇMEK ZORUNDA.
POLICY_FILES = {
    "00_CONTEXT/CLAIMS_STANDARD.md",
    "00_CONTEXT/QA_STANDARD.md",
    "00_CONTEXT/MEDIUM_DECISION_FRAMEWORK.md",
}


def _sentences(text: str):
    for raw in re.split(r"(?<=[.!?…])\s+|\n", text):
        s = raw.strip()
        if s:
            yield s


def scan_file(rel: str, text: str, validation_ids: set, findings: list):
    if rel in POLICY_FILES:
        return
    for sent in _sentences(text):
        f = _fold(sent)
        negated = any(c in f for c in NEGATION_CUES)
        for phrase in FAKE_EXPERT:
            if phrase in f and not negated:
                findings.append(f"{rel}: SAHTE UZMAN İDDİASI — {phrase!r} · «{sent[:120]}»"
                                f" (CLAIMS_STANDARD.md § 1: gerçek insan uzman kullanılmadı)")
        for phrase in PRINT_ADVANTAGE:
            if phrase in f and not negated:
                findings.append(f"{rel}: KORUNAN İDDİA — {phrase!r} · «{sent[:120]}»"
                                f" (araştırma raporu § 27: bu iddia ZAYIF çıktı, gerçek gibi kullanılamaz)")
        for phrase in UNBACKED_VALIDATION:
            if phrase in f and not negated and not re.search(r"VAL-\d{4}", sent):
                findings.append(f"{rel}: DAYANAKSIZ DOĞRULAMA İDDİASI — {phrase!r} · «{sent[:120]}»"
                                f" (bir VAL-xxxx kaydına atıf ZORUNLU — VALIDATION_PROTOCOL.md § 5)")


def check_support_notes(findings: list):
    """VERIFIED_NARROWER ve CONTESTED, GEREKÇESİZ olamaz.

    ⚠ KAYNAK ADLİ İNCELEMESİ (H-9): sicilin kendi kuralı "kaydın
    `source_support_note` alanı kaynağın GERÇEKTE ne dediğini yazar"
    diyordu ve on CONTESTED kaydın ONUNDA da alan BOŞTU. Bir 'daha dar'
    ya da 'çelişiyor' etiketi, NEYİN dar olduğunu söylemedikçe bir
    etiket değil bir bahanedir.
    """
    import json as _j
    from pathlib import Path as _P
    reg = (paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "public"
           / "claims.public.json")
    if not reg.exists():
        return
    for c in _j.loads(reg.read_text(encoding="utf-8"))["claims"]:
        if c["evidence_level"] in ("VERIFIED_NARROWER", "CONTESTED") \
                and not c.get("source_support_note"):
            findings.append(
                f"{c['claim_id']} ({c['taxonomy_ref']}): {c['evidence_level']} "
                f"ama `source_support_note` BOŞ — kaynağın ne dediği yazılmamış")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    findings: list[str] = []
    validation_ids: set = set()
    valfile = paths.REPORTS_TRACKED / "validation_records.json"
    if valfile.exists():
        validation_ids = {r["validation_id"]
                          for r in json.loads(valfile.read_text(encoding="utf-8")).get("records", [])}

    scanned = 0
    seen = set()
    for g in SCAN_GLOBS:
        for f in sorted(paths.ROOT.glob(g)):
            rel = f.relative_to(paths.ROOT).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            scanned += 1
            scan_file(rel, f.read_text(encoding="utf-8", errors="ignore"), validation_ids, findings)

    check_support_notes(findings)

    result = {"scanned": scanned, "validation_records": len(validation_ids),
              "findings": findings, "passed": not findings}
    print(f"▸ qa_claims.py — {scanned} belge tarandı, {len(validation_ids)} doğrulama kaydı")
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
