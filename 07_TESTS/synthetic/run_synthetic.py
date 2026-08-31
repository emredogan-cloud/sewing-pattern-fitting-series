#!/usr/bin/env python3
"""
run_synthetic.py — SENTETİK VÜCUT + DİFERANSİYEL TEŞHİS SİMÜLASYONU.

⚠ BU BİR FİZİKSEL TEST DEĞİLDİR ve onun yerine geçmez (K58).
Kumaş yok, drape yok, gerçek beden yok. Sınanan şey TEK BİR ŞEYDİR:

    teşhis sisteminin KENDİ KURALLARI, kenar durumlarda okuru
    tutarlı ve ulaşılabilir bir sonuca götürüyor mu.

İki koşu yapar:
  ① SENTETİK VÜCUT — 16 profil, her biri kalıptan sapmalar listesi.
     Profilin ürettiği beklenen belirtilerden yola çıkar ve sistemin
     beklenen düzeltme ailesine GERÇEKTEN ulaşıp ulaşmadığını ölçer.
  ② DİFERANSİYEL TEŞHİS — 28 kanıt çakışmasının her biri için, aynı
     görünür belirtiyi üreten iki senaryo kurar ve mevcut ayırt edici
     kanıtın onları AYIRIP AYIRMADIĞINI ölçer. Ayırmıyorsa kitabın
     bunu BEYAN ETTİĞİNİ doğrular — uydurulmuş bir ayrım aramaz.
"""
from __future__ import annotations
import json, sys, re, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "06_BUILD"))
import paths  # noqa: E402

T = paths.TAXONOMY_PUBLIC
SIGNS = {s["symptom_id"]: s for s in json.loads((T/"fit_signs.json").read_text(encoding="utf-8"))["signs"]}
FAMS  = {f["adjustment_family_id"]: f for f in json.loads((T/"adjustment_families.json").read_text(encoding="utf-8"))["families"]}
LAB   = json.loads((T/"labels_en.json").read_text(encoding="utf-8"))
COLL  = json.loads((T/"evidence_collisions.json").read_text(encoding="utf-8"))["collisions"]
PROF  = json.loads((ROOT/"07_TESTS/synthetic/synthetic_bodies.json").read_text(encoding="utf-8"))

FAIL, WARN = [], []


def reachable_families(sid):
    """Bu belirtiden okurun ULAŞABİLECEĞİ aileler.

    ⚠ İKİNCİ İÇERİK TURU: model yalnızca `adjustment_family_ref`e
    bakıyordu ve `cross_route`u GÖRMÜYORDU. Ama çapraz yönlendirme,
    kitabın okuru AÇIKÇA gönderdiği bir yoldur ve sayfada basılır —
    modelin görmemesi, modelin eksiğidir. SB-17 (tek taraflı yüksek
    omuz) bu yüzden 'ulaşılamaz' görünüyordu.
    """
    fams = set()
    for c in SIGNS[sid]["candidate_causes"]:
        if c.get("adjustment_family_ref"):
            fams.add(c["adjustment_family_ref"])
        cr = c.get("cross_route")
        if cr and cr.get("family_ref"):
            fams.add(cr["family_ref"])
    return fams


def run_bodies():
    print("═══ ① SENTETİK VÜCUT PROFİLİ SİMÜLASYONU ═══")
    print("    (kenar durum MANTIK sınaması — istatistiksel geçerliliği YOKTUR)\n")
    ok = 0
    for p in PROF["profiles"]:
        pid, name = p["id"], p["name"]
        # profilin beklenen belirtileri gerçekten tanımlı mı
        unknown = [s for s in p["expected_signs"] if s not in SIGNS]
        if unknown:
            FAIL.append(f"{pid}: tanımsız belirti {unknown}")
            print(f"  ✗ {pid} {name:22s} tanımsız belirti: {unknown}")
            continue
        # bu belirtilerden ulaşılabilen aileler
        reach = set()
        for s in p["expected_signs"]:
            reach |= reachable_families(s)
        want = set(p["expected_families"])
        missing = want - reach
        if missing:
            FAIL.append(f"{pid} ({name}): beklenen aile(ler) ULAŞILAMIYOR {sorted(missing)}")
            print(f"  ✗ {pid} {name:22s} ULAŞILAMAYAN: {sorted(missing)}")
            continue
        # her belirtinin bir çıkışı ve bir yeniden gözlem adımı var mı
        for s in p["expected_signs"]:
            if not reachable_families(s):
                FAIL.append(f"{pid}: {s} hiçbir aileye çıkmıyor")
            if not SIGNS[s].get("do_not_change_yet"):
                FAIL.append(f"{pid}: {s} 'henüz değiştirme' sınırı taşımıyor")
        ok += 1
        print(f"  ✓ {pid} {name:22s} {len(p['expected_signs'])} belirti → "
              f"{len(reach)} aile · beklenen {sorted(want)} ulaşılabilir")
    print(f"\n  {ok}/{len(PROF['profiles'])} profil tutarlı\n")


def run_differential():
    print("═══ ② DİFERANSİYEL TEŞHİS SİMÜLASYONU ═══")
    print("    28 kanıt çakışması — ayırt edici kanıt GERÇEKTEN ayırıyor mu\n")
    declared = {c["symptom_id"] for c in COLL}
    separated, disclosed, undisclosed = 0, 0, 0
    for sid, s in SIGNS.items():
        causes = s["candidate_causes"]
        if len(causes) < 2:
            continue
        ev = [(i + 1, (LAB["signs"][sid]["causes"][i]["evidence"] or "").strip())
              for i in range(len(causes))]
        # iki senaryo aynı görünür belirtiyi üretir; kanıt onları ayırır mı
        pairs = [(a, b) for i, a in enumerate(ev) for b in ev[i+1:]]
        for (ia, ea), (ib, eb) in pairs:
            na, nb = _norm(ea), _norm(eb)
            wa, wb = set(na.split()), set(nb.split())
            jac = len(wa & wb) / max(1, len(wa | wb))
            same = (na == nb) or jac > 0.80
            if same:
                if sid in declared:
                    disclosed += 1
                else:
                    undisclosed += 1
                    FAIL.append(f"{sid}.C{ia}/C{ib}: ayırt edici kanıt AYIRMIYOR ve "
                                f"kitap bunu BEYAN ETMİYOR")
            else:
                separated += 1
    print("  ⚠ SINIR: bu test METİNSEL örtüşmeyi ölçer. İki kanıt farklı")
    print("    KELİMELERLE aynı şeyi söylüyorsa burada AYRILMIŞ görünür.")
    print("    Projenin beyan ettiği 28 çakışma ANLAMSAL incelemeyle bulundu;")
    print("    bu koşum onların YENİSİNİN eklenmediğini gösterir, hepsinin")
    print("    gerçekten ayrıldığını DEĞİL.\n")
    print(f"  ayırt edici kanıtın METİNSEL olarak ayırdığı çift : {separated}")
    print(f"  metinsel olarak AYIRMAYAN, kitabın BEYAN ETTİĞİ  : {disclosed}")
    print(f"  metinsel olarak AYIRMAYAN, BEYAN EDİLMEYEN       : {undisclosed}")
    print(f"  beyan edilen çakışma taşıyan belirti          : {len(declared)}/43\n")
    # beyan edilen her çakışma gerçekten kitapta basılıyor mu (veri düzeyinde)
    for c in COLL:
        if c["symptom_id"] not in SIGNS:
            FAIL.append(f"çakışma kaydı tanımsız belirtiye işaret ediyor: {c['symptom_id']}")


def _norm(t):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (t or "").lower())).strip()


def main():
    print("▸ run_synthetic.py — İÇSEL SİMÜLASYON (fiziksel testin YERİNE GEÇMEZ)\n")
    run_bodies()
    run_differential()
    print("─" * 62)
    if FAIL:
        print(f"✗ {len(FAIL)} BULGU:")
        for f in FAIL:
            print(f"  - {f}")
        return 1
    print("✓ Sentetik profillerin ve diferansiyel senaryoların tamamı tutarlı.")
    print("⚠ Bu, sistemin KENDİ KURALLARINA göre tutarlı olduğunu gösterir.")
    print("  Gerçek kumaşta doğru olduğunu GÖSTERMEZ — o ölçüm yapılmadı (K58).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
