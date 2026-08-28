#!/usr/bin/env python3
"""
qa_crosswalk.py — devir haritası bütünlük kapısı.

NEDEN AYRI BİR KAPI (DECISIONS.md K31):

`build_crosswalk.py --check` yalnızca **tazeliği** ölçer: diskteki
dosya kaynak taksonomiden yeniden üretilenle aynı mı. Bu, üretici
kodun kendisi yanlışsa **hiçbir şey yakalamaz** — bayat olmayan ama
yanlış bir crosswalk sessizce geçer.

`validate_spec.check_crosswalk_integrity` ise tek bir kaydın
referanslarına bakar; kayıtlar ARASINDAKİ ve kayıtlarla taksonomi
ARASINDAKİ ilişkilere bakmaz.

Bu kapı o boşluğu doldurur ve dokuz ilişkiyi ayrı ayrı sınar:

  ① kaynak uç noktası tanımlı mı
  ② devir cümlesi gerçekten o belirtinin bir aday nedenini taşıyor mu
  ③ hedef uç noktası tanımlı mı
  ④ istisna mantığı tutarlı mı (null ⇔ exception)
  ⑤ belirti→aile çiftleri taksonomiyle BİREBİR mi (fazla/eksik yol yok)
  ⑥ kitap sahipliği tutarlı mı (book1_entry_point)
  ⑦ devir cümlesi ailenin KANONİK adını taşıyor mu (terminoloji)
  ⑧ her giriş noktası ailesine Kitap 1'den ulaşılabiliyor mu
  ⑨ her belirtinin en az bir yolu var mı

Üçüncü taraf paket GEREKTİRMEZ.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def audit(signs: list, families: dict, blocks: dict, crosswalks: list) -> list[str]:
    """Dokuz denetimi çalıştırır. Hataları liste olarak döndürür."""
    findings: list[str] = []
    sym = {s["symptom_id"]: s for s in signs}

    d2a = [x for x in crosswalks if x.get("direction") == "DIAGNOSIS_TO_ADJUSTMENT"]
    a2b = [x for x in crosswalks if x.get("direction") != "DIAGNOSIS_TO_ADJUSTMENT"]

    # ① kaynak uç noktası
    for x in d2a:
        if x.get("from_ref") not in sym:
            findings.append(f"① {x.get('crosswalk_id')}: from_ref={x.get('from_ref')} tanımlı bir belirti DEĞİL.")
    for x in a2b:
        if x.get("from_ref") not in families:
            findings.append(f"① {x.get('crosswalk_id')}: from_ref={x.get('from_ref')} tanımlı bir düzeltme ailesi DEĞİL.")

    # ② devir cümlesi ↔ aday neden
    for x in d2a:
        s = sym.get(x.get("from_ref"))
        if not s:
            continue
        hs = x.get("handoff_sentence") or ""
        causes = [c.get("cause", "") for c in s.get("candidate_causes", [])]
        if not any(c[:40] and c[:40] in hs for c in causes):
            findings.append(
                f"② {x.get('crosswalk_id')}: devir cümlesi {x.get('from_ref')}'in HİÇBİR aday nedenini "
                f"taşımıyor — okur cümleden hangi nedene vardığını anlayamaz."
            )

    # ③ hedef uç noktası
    for x in d2a:
        if x.get("to_ref") is not None and x["to_ref"] not in families:
            findings.append(f"③ {x.get('crosswalk_id')}: to_ref={x['to_ref']} tanımlı bir düzeltme ailesi DEĞİL.")
    for x in a2b:
        if x.get("to_ref") is not None and x["to_ref"] not in blocks:
            findings.append(f"③ {x.get('crosswalk_id')}: to_ref={x['to_ref']} tanımlı bir blok bileşeni DEĞİL.")

    # ④ istisna mantığı — İKİ YÖNLÜ
    for x in crosswalks:
        if x.get("to_ref") is None and not x.get("exception"):
            findings.append(f"④ {x.get('crosswalk_id')}: to_ref=null ama 'exception' BOŞ.")
        if x.get("to_ref") is not None and x.get("exception"):
            findings.append(
                f"④ {x.get('crosswalk_id')}: to_ref DOLU ama 'exception' da dolu — "
                f"bir yol hem varış noktası olup hem istisna OLAMAZ."
            )

    # ⑤ taksonomi ↔ crosswalk birebir
    pairs_tax = {(s["symptom_id"], c.get("adjustment_family_ref"))
                 for s in signs for c in s.get("candidate_causes", [])}
    pairs_xw = {(x.get("from_ref"), x.get("to_ref")) for x in d2a}
    for p in sorted(pairs_tax - pairs_xw, key=str):
        findings.append(f"⑤ taksonomide var, crosswalk'ta YOK: {p[0]} → {p[1]} — Kitap 1'in bir yolu KAYBOLMUŞ.")
    for p in sorted(pairs_xw - pairs_tax, key=str):
        findings.append(f"⑤ crosswalk'ta var, taksonomide YOK: {p[0]} → {p[1]} — UYDURULMUŞ yol.")

    # ⑥ kitap sahipliği
    for x in d2a:
        t = x.get("to_ref")
        if t and t in families and not families[t].get("book1_entry_point"):
            findings.append(
                f"⑥ {x.get('crosswalk_id')}: {t} book1_entry_point=false ama Kitap 1'den bir yol var — "
                f"kitap sahipliği çelişkisi."
            )

    # ⑦ terminoloji — kanonik ad
    for x in d2a:
        t = x.get("to_ref")
        if not t or t not in families:
            continue
        if families[t]["name"] not in (x.get("handoff_sentence") or ""):
            findings.append(
                f"⑦ {x.get('crosswalk_id')}: devir cümlesi {t}'in KANONİK adını taşımıyor — "
                f"okur Kitap 2'de aradığı girişi bulamaz."
            )

    # ⑧ ulaşılabilirlik
    reached = {x.get("to_ref") for x in d2a if x.get("to_ref")}
    for fid, f in families.items():
        if f.get("book1_entry_point") and fid not in reached:
            findings.append(f"⑧ {fid}: book1_entry_point=true ama Kitap 1'den ULAŞILAMIYOR.")

    # ⑨ her belirtinin yolu
    with_path = {x.get("from_ref") for x in d2a}
    for s in signs:
        if s["symptom_id"] not in with_path:
            findings.append(f"⑨ {s['symptom_id']}: hiçbir crosswalk yolu YOK — teşhis boşta bitiyor.")

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    signs = load(paths.FIT_SIGNS)["signs"]
    families = {f["adjustment_family_id"]: f
                for f in load(paths.ADJUSTMENT_FAMILIES)["families"]}
    blocks = {b["block_id"]: b for b in load(paths.BLOCK_COMPONENTS)["blocks"]}
    crosswalks = load(paths.CROSSWALK)["crosswalks"]

    findings = audit(signs, families, blocks, crosswalks)

    d2a = sum(1 for x in crosswalks if x.get("direction") == "DIAGNOSIS_TO_ADJUSTMENT")
    exc = sum(1 for x in crosswalks if x.get("to_ref") is None)
    reached = len({x.get("to_ref") for x in crosswalks
                   if x.get("direction") == "DIAGNOSIS_TO_ADJUSTMENT" and x.get("to_ref")})

    print(f"▸ qa_crosswalk.py — {len(crosswalks)} kayıt · {d2a} teşhis→düzeltme · "
          f"{exc} istisna · {reached}/{len(families)} aileye ulaşılıyor")
    if findings:
        print(f"  ✗ {len(findings)} bulgu:")
        for x in findings:
            print(f"    - {x}")
    else:
        print("  ✓ 0 bulgu (dokuz denetim)")

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"records": len(crosswalks), "diagnosis_to_adjustment": d2a,
                                   "exceptions": exc, "families_reached": reached,
                                   "findings": findings, "passed": not findings},
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
