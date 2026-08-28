#!/usr/bin/env python3
"""
build_crosswalk.py — teşhis→düzeltme ve düzeltme→blok haritasını
kaynak taksonomilerden TÜRETİR.

Görev talimatı § 22-23. Crosswalk ELLE yazılmaz: fit_signs.json ve
adjustment_families.json değişince yeniden üretilir. Böylece "Kitap 1
bir belirti ekledi ama Kitap 2 karşılığını unuttu" durumu sessizce
oluşamaz.

--check : dosyayı YAZMAZ, mevcut dosyayla karşılaştırır (CI için).
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

# Kitap 2 → Kitap 3 eşlemesi. None = blok bileşenine dönüşmez (istisna
# ZORUNLU olarak yazılır — sessiz boşluk bırakılamaz).
AF_TO_BLOCK = {
    "AF-01": "BLK-03", "AF-02": "BLK-03", "AF-03": "BLK-04", "AF-04": "BLK-04",
    "AF-05": "BLK-04", "AF-06": "BLK-04", "AF-07": "BLK-02", "AF-08": "BLK-05",
    "AF-09": "BLK-06", "AF-10": "BLK-06", "AF-11": "BLK-11", "AF-12": "BLK-10",
    "AF-13": "BLK-07", "AF-14": "BLK-10", "AF-15": "BLK-08", "AF-16": "BLK-08",
    "AF-17": "BLK-09", "AF-18": None,     "AF-19": "BLK-11",
}
NO_BLOCK_REASON = (
    "Beden dereceleme kavramı blok çiziminde YOKTUR — blok tek bedendir. "
    "Bu, Kitap 3'ün bir eksiği değil, TANIMIDIR ve Kitap 3'ün en güçlü "
    "satış argümanlarından biridir."
)
NO_ADJUSTMENT_REASON = (
    "Bu neden bir kalıp/vücut uyumsuzluğu değildir (yapım, kesim, prova "
    "koşulu veya tasarım tercihi); Kitap 2'de karşılığı YOKTUR ve OLMAMALIDIR."
)


def build() -> dict:
    signs = json.loads(paths.FIT_SIGNS.read_text(encoding="utf-8"))["signs"]
    fams = {f["adjustment_family_id"]: f
            for f in json.loads(paths.ADJUSTMENT_FAMILIES.read_text(encoding="utf-8"))["families"]}
    rows, n = [], 0
    for s in signs:
        for c in s["candidate_causes"]:
            af = c["adjustment_family_ref"]
            n += 1
            if af:
                hand = ("Belirti %s ve ayırt edici kanıt doğrulandığında teşhis şudur: %s → %s (%s)."
                        % (s["symptom_id"], c["cause"], af, fams[af]["name"]))
                exc = None
            else:
                hand = ("Belirti %s bu nedene bağlandığında SONUÇ BİR KALIP DÜZELTMESİ DEĞİLDİR: %s."
                        % (s["symptom_id"], c["cause"]))
                exc = c.get("likelihood_note") or NO_ADJUSTMENT_REASON
            rows.append({"crosswalk_id": "XW-%03d" % n, "direction": "DIAGNOSIS_TO_ADJUSTMENT",
                         "from_ref": s["symptom_id"], "to_ref": af, "handoff_sentence": hand,
                         "exception": exc, "verification_status": "agent_drafted_unverified"})
    for af in sorted(AF_TO_BLOCK):
        blk = AF_TO_BLOCK[af]
        n += 1
        f = fams[af]
        if blk:
            hand = ("Okur %s ailesini HER kalıpta yeniden uyguluyorsa, bu tekrar bir blok kararına dönüşür: %s"
                    % (af, f["book3_relevance"]))
            exc = None
        else:
            hand = "%s (%s) bir blok bileşenine dönüşmez." % (af, f["name"])
            exc = NO_BLOCK_REASON
        rows.append({"crosswalk_id": "XW-%03d" % n, "direction": "ADJUSTMENT_TO_BLOCK",
                     "from_ref": af, "to_ref": blk, "handoff_sentence": hand,
                     "exception": exc, "verification_status": "agent_drafted_unverified"})
    return {
        "$comment": [
            "CROSSWALK — kitaplar arası devir haritası (görev talimatı § 22-23).",
            "OTOMATİK TÜRETİLMİŞTİR (06_BUILD/build_crosswalk.py).",
            "ELLE DÜZENLENMEZ — kaynak dosyalar değişince yeniden üretilir.",
            "qa_boundary.py her belirtinin en az bir yola VEYA açık bir istisnaya sahip olduğunu dayatır.",
        ],
        "generated_by": "06_BUILD/build_crosswalk.py",
        "count": len(rows),
        "by_direction": {
            "DIAGNOSIS_TO_ADJUSTMENT": sum(1 for r in rows if r["direction"] == "DIAGNOSIS_TO_ADJUSTMENT"),
            "ADJUSTMENT_TO_BLOCK": sum(1 for r in rows if r["direction"] == "ADJUSTMENT_TO_BLOCK"),
        },
        "exception_count": sum(1 for r in rows if r["to_ref"] is None),
        "crosswalks": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="yazma, mevcut dosyayla karşılaştır")
    args = ap.parse_args()
    doc = build()
    if args.check:
        if not paths.CROSSWALK.exists():
            print("✗ crosswalk.json yok — build_crosswalk.py çalıştırılmalı")
            return 1
        cur = json.loads(paths.CROSSWALK.read_text(encoding="utf-8"))
        if cur.get("crosswalks") != doc["crosswalks"]:
            print("✗ crosswalk.json BAYAT — kaynak taksonomi değişmiş, yeniden üretilmeli")
            return 1
        print(f"▸ build_crosswalk.py --check — ✓ güncel ({doc['count']} kayıt)")
        return 0
    paths.CROSSWALK.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"▸ build_crosswalk.py — {doc['count']} kayıt yazıldı "
          f"({doc['by_direction']['DIAGNOSIS_TO_ADJUSTMENT']} teşhis→düzeltme, "
          f"{doc['by_direction']['ADJUSTMENT_TO_BLOCK']} düzeltme→blok, "
          f"{doc['exception_count']} istisna)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
