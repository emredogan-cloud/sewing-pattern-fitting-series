#!/usr/bin/env python3
"""
graph_audit.py — TAKSONOMİ BİR ÇİZGEDİR; çizge olarak denetlenir.

Görev talimatı § 20. Belirti → aday neden → düzeltme ailesi → blok
zinciri bir yönlü çizgedir ve bir teşhis kitabının doğruluğu, o
çizgenin ÖZELLİKLERİDİR:

  ① ÖKSÜZ            hiçbir nedenin varmadığı aile
  ② ULAŞILAMAZ       hiçbir belirtiden erişilemeyen aile
  ③ ÇIKIŞSIZ         hiçbir aileye çıkmayan belirti
  ④ DÖNGÜ            sıra kısıtlarında çevrim
  ⑤ ASİMETRİK        A, B ile etkileşir der ama B demez
  ⑥ ÇİFT VARIŞ       aynı belirtide iki neden aynı aileye çıkıyor
  ⑦ GEÇERSİZ         tanımsız aileye / belirtiye atıf
  ⑧ İMKÂNSIZ         aynı belirtide iki neden AYNI yönde ZITLIK iddia ediyor
  ⑨ KOPUK            crosswalk ile taksonomi arasında sapma
  ⑩ TEK ÇIKIŞLI      bir belirtinin bütün nedenleri tek aileye çıkıyor
                     (o belirti bir TEŞHİS değil, bir ETİKETTİR)
  ⑪ ERİŞİLMEZ OKUMA  hiçbir adımda kullanılmayan kalıp/prova okuması
  ⑫ SAĞIR AİLE       bir aileye çıkan hiçbir neden bir ÖLÇÜ taşımıyor
                     (okur oraya varır ve miktarı ölçemez)
  ⑭ SIRA ÇELİŞKİSİ   `order_before` klinik önceliği, basılan sırada
                     GERÇEKTEN sağlanıyor mu (çevrim ya da geri
                     alınamaz aile yüzünden sağlanamıyorsa kusurdur)
  ⑬ SESSİZ ÇIKIŞ     ailesi olmayan bir neden, NEDEN olmadığını
                     söylemiyor — okur "kalıpta hiçbir şey yok"
                     cümlesini kesim hatası ile kalıp parametresi
                     için AYNI biçimde okur (bağımsız inceleme M-3/M-4)

Çıkış: 0 temiz · 1 en az bir kusur.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "06_BUILD"))
import paths  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main() -> int:
    signs = load(paths.FIT_SIGNS)["signs"]
    fams = {f["adjustment_family_id"]: f
            for f in load(paths.ADJUSTMENT_FAMILIES)["families"]}
    meas = {m["measurement_id"] for m in load(paths.MEASUREMENTS)["measurements"]}
    pr = load(paths.TAXONOMY_PUBLIC / "pattern_readings.json")
    prs = {r["reading_id"] for r in pr["readings"]}
    trs = {r["reading_id"] for r in pr["toile_readings"]}
    cw = load(paths.CROSSWALK)

    errs: list = []
    warns: list = []

    # ── kenarlar ──────────────────────────────────────────────────────
    edges: list = []          # (sid.Ci, family)
    for s in signs:
        sid = s["symptom_id"]
        for i, c in enumerate(s["candidate_causes"], 1):
            f = c.get("adjustment_family_ref")
            if f:
                edges.append((f"{sid}.C{i}", f))
            for cr in (c.get("cross_routes") or []):
                if cr.get("family_ref"):
                    edges.append((f"{sid}.C{i}", cr["family_ref"]))

    reached = {f for _, f in edges}

    # ⑦ geçersiz atıf
    for src, f in edges:
        if f not in fams:
            errs.append(f"⑦ {src}: TANIMSIZ aileye atıf {f}")

    # ①② öksüz / ulaşılamaz aile
    for fid in fams:
        if fid not in reached:
            errs.append(f"② {fid} ({fams[fid]['name']}): hiçbir belirtiden ULAŞILAMIYOR")

    # ③ çıkışsız belirti · ⑩ tek çıkışlı belirti
    for s in signs:
        sid = s["symptom_id"]
        outs = {c.get("adjustment_family_ref") for c in s["candidate_causes"]
                if c.get("adjustment_family_ref")}
        if not outs:
            errs.append(f"③ {sid}: hiçbir düzeltme ailesine ÇIKMIYOR")
        elif len(outs) == 1 and len(s["candidate_causes"]) > 1:
            warns.append(f"⑩ {sid}: {len(s['candidate_causes'])} nedenin hepsi tek "
                         f"aileye ({outs.pop()}) çıkıyor — teşhis mi, etiket mi?")

    # ⑥ aynı belirtide çift varış — BEYAN EDİLMİŞ olmalı
    for s in signs:
        sid = s["symptom_id"]
        seen: dict = {}
        for i, c in enumerate(s["candidate_causes"], 1):
            f = c.get("adjustment_family_ref")
            if not f:
                continue
            if f in seen:
                a, b = seen[f], i
                opp = (s["candidate_causes"][a - 1].get("opposite_of")
                       or s["candidate_causes"][b - 1].get("opposite_of"))
                if not opp:
                    warns.append(f"⑥ {sid}: C{a} ve C{b} AYNI aileye ({f}) çıkıyor ve "
                                 f"`opposite_of` BEYAN EDİLMEMİŞ")
            seen[f] = i

    # ⑤ asimetrik etkileşim
    for fid, f in fams.items():
        for other in f.get("interacts_with", []):
            if other not in fams:
                errs.append(f"⑦ {fid}: TANIMSIZ aile ile etkileşim {other}")
            elif fid not in fams[other].get("interacts_with", []):
                errs.append(f"⑤ {fid} → {other} etkileşimi TEK YÖNLÜ")

    # ④ sıra kısıtı döngüsü — `order_source_refs` + interacts değil,
    #    BEYAN EDİLEN önceliklerden kurulur
    prec: dict = {}
    for fid, f in fams.items():
        prec[fid] = set()
    # "defer_in_diagnosis" bir kısmi sıradır: ertelenen aile, ertelenmeyen
    # her aileden SONRA gelir. Bu ilişkide döngü OLAMAZ; yine de denetlenir.
    deferred = {fid for fid, f in fams.items() if f.get("defer_in_diagnosis")}
    for a in deferred:
        for b in fams:
            if b not in deferred:
                prec[a].add(b)
    colour: dict = {}

    def dfs(n):
        colour[n] = 1
        for m in prec.get(n, ()):
            if colour.get(m) == 1:
                errs.append(f"④ sıra kısıtında DÖNGÜ: {n} ↔ {m}")
                return
            if colour.get(m) is None:
                dfs(m)
        colour[n] = 2

    for n in fams:
        if colour.get(n) is None:
            dfs(n)

    # ⑧ imkânsız durum — aynı belirtide iki neden ZIT beyan ediyor ama
    #    ikisi de aynı yöne gidiyor
    for s in signs:
        sid = s["symptom_id"]
        for i, c in enumerate(s["candidate_causes"], 1):
            op = c.get("opposite_of")
            if not op:
                continue
            j = int(op.rsplit(".C", 1)[1])
            other = s["candidate_causes"][j - 1]
            if other.get("opposite_of") != f"{sid}.C{i}":
                errs.append(f"⑧ {sid}.C{i} → {op} zıtlığı KARŞILIKLI DEĞİL")

    # ⑨ crosswalk ↔ taksonomi
    # Aile YOKLUĞU da bir kayıttır: "bu neden kalıpta bir yere çıkmaz"
    # crosswalk'ta to_ref=None olarak durur ve taksonomide de öyle.
    tax_pairs = {(src.split(".C")[0], f) for src, f in edges}
    for s_ in signs:
        for c_ in s_["candidate_causes"]:
            if not c_.get("adjustment_family_ref"):
                tax_pairs.add((s_["symptom_id"], None))
    # crosswalk kaydı belirtiyi SYM-xxx düzeyinde tutar, neden düzeyinde
    # değil; karşılaştırma o düzeyde yapılır.
    cw_pairs = {(r["from_ref"], r["to_ref"]) for r in cw["crosswalks"]
                if r.get("direction") == "DIAGNOSIS_TO_ADJUSTMENT"}
    only_tax = {p for p in tax_pairs if p not in cw_pairs}
    only_cw = cw_pairs - tax_pairs
    # cross_route kenarları crosswalk'a girmez — bu BEKLENEN bir farktır
    cross_edges = set()
    for s in signs:
        for c in s["candidate_causes"]:
            for cr in (c.get("cross_routes") or []):
                if cr.get("family_ref"):
                    cross_edges.add((s["symptom_id"], cr["family_ref"]))
    only_tax -= cross_edges
    for p in sorted(only_tax):
        errs.append(f"⑨ taksonomide VAR, crosswalk'ta YOK: {p[0]} → {p[1]}")
    for p in sorted(only_cw):
        errs.append(f"⑨ crosswalk'ta VAR, taksonomide YOK: {p[0]} → {p[1]}")

    # ⑪ erişilmez okuma
    used_pr, used_tr, used_m = set(), set(), set()
    for s in signs:
        for c in s["candidate_causes"]:
            r = c.get("confirming_refs") or {}
            used_m |= set(r.get("body") or [])
            used_pr |= set(r.get("pattern") or [])
            used_tr |= set(r.get("toile") or [])
    for rid in sorted(prs - used_pr):
        warns.append(f"⑪ {rid}: hiçbir doğrulama adımı kullanmıyor")
    for rid in sorted(trs - used_tr):
        warns.append(f"⑪ {rid}: hiçbir doğrulama adımı kullanmıyor")
    for mid in sorted(meas - used_m):
        warns.append(f"⑪ {mid}: hiçbir doğrulama adımında kullanılmıyor "
                     f"(kitap bunu okura BEYAN etmeli)")

    # ⑫ sağır aile — oraya çıkan hiçbir neden ÖLÇÜ taşımıyor
    fam_has_measure: dict = {}
    for s in signs:
        for c in s["candidate_causes"]:
            f = c.get("adjustment_family_ref")
            if not f:
                continue
            r = c.get("confirming_refs") or {}
            has = bool((r.get("body") or []) or (r.get("pattern") or [])
                       or (r.get("toile") or []))
            fam_has_measure[f] = fam_has_measure.get(f, False) or has
    for fid, has in sorted(fam_has_measure.items()):
        if not has:
            errs.append(f"⑫ {fid} ({fams[fid]['name']}): bu aileye çıkan HİÇBİR neden "
                        f"bir ölçü taşımıyor — okur oraya varır ve miktarı ölçemez")

    # ⑬ sessiz çıkış — ailesi yoksa GEREKÇESİ yazılmalı
    for s in signs:
        for i, c in enumerate(s["candidate_causes"], 1):
            if not c.get("adjustment_family_ref") and not c.get("no_family_reason"):
                errs.append(f"⑬ {s['symptom_id']}.C{i}: ailesi YOK ve NEDEN olmadığı "
                            f"BEYAN EDİLMEMİŞ — kesim hatası mı, kalıp parametresi mi?")

    # ⑭ klinik öncelik BASILAN sırada sağlanıyor mu
    #
    # ⚠ OKUR SİMÜLASYONU (KRİTİK-3): bir girişin "Order:" satırı bir
    # sıra ilan edip basılan sıranın TERSİNİ üretebiliyordu. Öncelik
    # artık veridedir; bu kapı onun GERÇEKTEN uygulandığını ölçer.
    # Geri alınamaz bir aile önceliği bastırırsa bu SESSİZ kalmamalı:
    # iki kural çelişiyorsa metin bunu okura söylemek zorundadır.
    sys.path.insert(0, str(paths.ROOT / "06_BUILD"))
    import cause_order
    for s in signs:
        pairs = [tuple(x) for x in (s.get("order_before") or [])]
        if not pairs:
            continue
        seq = [i for i, _ in cause_order.ordered_causes(s)]
        pos = {i: n for n, i in enumerate(seq)}
        for a, b in pairs:
            if pos.get(a, 0) > pos.get(b, 0):
                errs.append(f"⑭ {s['symptom_id']}: C{a} klinik olarak C{b}'den ÖNCE "
                            f"gelmeli ama basılan sıra C{b}'yi öne alıyor — "
                            f"öncelik SAĞLANMIYOR")

    print("▸ graph_audit.py — nedensel çizge denetimi")
    print(f"  {len(signs)} belirti · {sum(len(s['candidate_causes']) for s in signs)} neden "
          f"· {len(fams)} aile · {len(edges)} kenar · {len(cw['crosswalks'])} crosswalk")
    print(f"  ulaşılan aile {len(reached)}/{len(fams)} · "
          f"kullanılan ölçü {len(used_m)}/{len(meas)} · "
          f"kalıp okuması {len(used_pr)}/{len(prs)} · prova okuması {len(used_tr)}/{len(trs)}")
    for w in warns:
        print(f"  ⚠ {w}")
    if errs:
        print(f"  ✗ {len(errs)} kusur")
        for e in errs[:40]:
            print(f"    - {e}")
        return 1
    print("  ✓ çizgede öksüz, ulaşılamaz, çıkışsız, döngü, asimetri, "
          "geçersiz atıf ve sağır aile YOK")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.parse_args()
    sys.exit(main())
