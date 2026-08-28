#!/usr/bin/env python3
"""
qa_boundary.py — kitap sınırı denetimi.

Bu, SERİNİN KENDİNE ÖZGÜ kapısıdır; hiçbir kardeş projede karşılığı
yoktur çünkü hiçbiri çok kitaplı değildir (DECISIONS.md K11).

Neyi korur (RISK_REGISTER R-07 "içerik kapsamı riski"):
  ① TEK-BİRİNCİL kuralı — bir topik iki kitapta birden 'primary' olamaz.
     İki kitap da öğretirse okur ikincisini almaz.
  ② KAPSAM DIŞI topikler gerçekten dışarıda mı.
  ③ Her belirtinin Kitap 2'ye bir yolu VEYA açık bir istisnası var mı.
  ④ Her düzeltme ailesine Kitap 1'den ulaşılabiliyor mu (ulaşılamıyorsa
     ya Kitap 1 eksik ya aile gereksiz — ikisi de bilinmeli).
  ⑤ 'excluded'/'introduce_only' bir topik, kitabın spesifikasyon
     belgelerinde prosedür diliyle geçiyor mu (sızıntı taraması).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

# ⑤ için: bir topik 'excluded' ya da 'introduce_only' ise, o kitabın
# spesifikasyonunda ADIM DİLİ ile geçmesi bir sızıntı işaretidir.
PROCEDURE_LANGUAGE = [
    re.compile(r"\bad[ıi]m\s*\d", re.I),
    re.compile(r"\bstep\s*\d", re.I),
    re.compile(r"\bşöyle\s+yap", re.I),
    re.compile(r"\bnas[ıi]l\s+yap[ıi]l[ıi]r\b", re.I),
]
LEAK_TOPIC_KEYWORDS = {
    "TOP-14": ["slash and spread", "kes ve aç", "kes ve bindir"],
    "TOP-16": ["dart rotation", "pens döndür"],
    "TOP-22": ["drafting sequence", "çizim sırası"],
}


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def check_single_primary(matrix, findings):
    for t in matrix["topics"]:
        prim = [b for b in ("book-01", "book-02", "book-03") if t[b] == "primary"]
        if len(prim) > 1:
            findings.append(f"TEK-BİRİNCİL İHLALİ: {t['topic_id']} ({t['name']}) "
                            f"{', '.join(prim)} kitaplarının HEPSİNDE 'primary' — "
                            f"iki kitap aynı konuyu öğretirse okur ikincisini almaz. "
                            f"Çözüm kopyalama değil TOPİK BÖLME'dir.")
        if not prim and not all(t[b] == "excluded" for b in ("book-01", "book-02", "book-03")):
            findings.append(f"SAHİPSİZ TOPİK: {t['topic_id']} hiçbir kitapta 'primary' değil "
                            f"ama tamamen dışlanmış da değil — kanonik tanımı kim yazacak?")


def check_role_values(matrix, findings):
    allowed = set(matrix["role_order"])
    for t in matrix["topics"]:
        for b in ("book-01", "book-02", "book-03"):
            if t[b] not in allowed:
                findings.append(f"{t['topic_id']}: {b} için geçersiz rol {t[b]!r}")


def check_symptom_paths(signs, xws, findings):
    have = {}
    for x in xws:
        if x["direction"] != "DIAGNOSIS_TO_ADJUSTMENT":
            continue
        have.setdefault(x["from_ref"], []).append(x)
    for s in signs:
        rows = have.get(s["symptom_id"], [])
        if not rows:
            findings.append(f"YOLSUZ BELİRTİ: {s['symptom_id']} için hiçbir crosswalk kaydı yok.")
            continue
        if not any(r["to_ref"] for r in rows) and not all(r.get("exception") for r in rows):
            findings.append(f"{s['symptom_id']}: hiçbir Kitap 2 yolu yok ve istisna gerekçesi eksik.")


def check_family_reachability(fams, xws, findings):
    reachable = {x["to_ref"] for x in xws
                 if x["direction"] == "DIAGNOSIS_TO_ADJUSTMENT" and x["to_ref"]}
    for f in fams:
        fid = f["adjustment_family_id"]
        if f.get("book1_entry_point") and fid not in reachable:
            findings.append(
                f"ULAŞILAMAYAN AİLE: {fid} ({f['name']}) book1_entry_point=true olarak "
                f"işaretli ama hiçbir Kitap 1 belirtisi oraya varmıyor — ya Kitap 1'de bir "
                f"belirti eksik, ya bu bayrak yanlış. İkisi de sessizce bırakılamaz."
            )


def check_excluded_leak(matrix, findings):
    books = {"book-01": paths.book_spec("book-01"),
             "book-02": paths.book_spec("book-02"),
             "book-03": paths.book_spec("book-03")}
    for t in matrix["topics"]:
        kws = LEAK_TOPIC_KEYWORDS.get(t["topic_id"])
        if not kws:
            continue
        for book, spec in books.items():
            if t[book] not in ("excluded", "introduce_only") or not spec.exists():
                continue
            for f in sorted(spec.glob("*.md")):
                text = f.read_text(encoding="utf-8", errors="ignore").lower()
                for kw in kws:
                    if kw not in text:
                        continue
                    for line in text.splitlines():
                        if kw in line and any(p.search(line) for p in PROCEDURE_LANGUAGE):
                            findings.append(
                                f"SINIR SIZINTISI: {book}/00_SPEC/{f.name} — {t['topic_id']} bu "
                                f"kitapta '{t[book]}' ama {kw!r} ADIM DİLİYLE geçiyor. "
                                f"Prosedür başka kitaba aittir."
                            )
                            break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    findings: list[str] = []
    matrix = load(paths.BOUNDARY_MATRIX)
    check_role_values(matrix, findings)
    check_single_primary(matrix, findings)

    signs = load(paths.FIT_SIGNS)["signs"] if paths.FIT_SIGNS.exists() else []
    fams = load(paths.ADJUSTMENT_FAMILIES)["families"] if paths.ADJUSTMENT_FAMILIES.exists() else []
    xws = load(paths.CROSSWALK)["crosswalks"] if paths.CROSSWALK.exists() else []
    check_symptom_paths(signs, xws, findings)
    check_family_reachability(fams, xws, findings)
    check_excluded_leak(matrix, findings)

    result = {"topics": len(matrix["topics"]), "signs": len(signs),
              "families": len(fams), "crosswalks": len(xws),
              "findings": findings, "passed": not findings}
    print(f"▸ qa_boundary.py — {len(matrix['topics'])} topik · {len(signs)} belirti · "
          f"{len(fams)} aile · {len(xws)} crosswalk")
    if findings:
        print(f"  ✗ {len(findings)} bulgu:")
        for f in findings:
            print(f"    - {f}")
    else:
        print("  ✓ 0 bulgu")
    if args.json:
        out = Path(args.json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
