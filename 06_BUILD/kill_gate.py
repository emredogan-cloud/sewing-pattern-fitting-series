#!/usr/bin/env python3
"""
kill_gate.py — Kitap 1 Faz 3 kill-gate'inin MEKANİK yüzü.

⚠ BU SCRIPT KILL-GATE'İ ÖLÇMEZ. Ölçemez.

Bu projenin iki kill-gate'i de DIŞ DÜNYADA ölçülür:
  ① FARK TESTİ — üç gerçek ev dikişçisi (araştırma raporu § 35 madde 1).
     Hiçbir AI vekili bu ölçümün yerine geçmez (DECISIONS.md K6).
  ② FİZİKSEL DOĞRULAMA — her diyagramın gerçekten kalıba uygulanıp
     muslin dikilmesi (araştırma raporu § 35 madde 2).

Bu script yalnızca şunu yapar: kill-gate'in ÖLÇÜLEBİLİR OLMASI için
gereken ÖN KOŞULLAR hazır mı, ve ölçüm SONUCU usulüne uygun
kaydedilmiş mi. PASS yazdırması, kill-gate'in geçtiği ANLAMINA GELMEZ
— yalnızca ölçümün yapılabileceği/kaydedildiği anlamına gelir.

Kardeş emsal: Hangıl projesinin kill_gate.py'si de kendi notunda aynı
sınırı taşır ("bu YALNIZCA mekanik denetimleri ölçer"). Bu proje o notu
scriptin ADINDAN ve ÇIKTISINDAN itibaren görünür kılar.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

DECISIONS = {"HARD_STOP", "REVISE", "PASS"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))
    kg = cfg["killGates"]
    blockers, notes = [], []

    for name, spec in kg.items():
        if name.startswith("$"):
            continue
        if spec.get("book") != args.book:
            continue
        if spec.get("measured") is not True:
            blockers.append(f"{name}: HENÜZ ÖLÇÜLMEDİ (measured=false). "
                            f"Ölçüm modeli: {spec.get('model')}")
            continue
        d = spec.get("measuredDecision")
        if d not in DECISIONS:
            blockers.append(f"{name}: measured=true ama measuredDecision geçersiz ({d!r})")
        elif d != "PASS":
            blockers.append(f"{name}: ÖLÇÜLDÜ → {d}. Faz 4 (tam üretim) AÇILAMAZ.")
        if spec.get("aiProxyCountsAsHuman") is True:
            blockers.append(f"{name}: aiProxyCountsAsHuman=true — bu bayrak AÇILAMAZ. "
                            f"AI vekil testi insan testinin YERİNE GEÇMEZ (DECISIONS.md K6).")
        if spec.get("founderOverride"):
            notes.append(f"{name}: KURUCU GEÇERSİZ KILMASI kayıtlı → {spec['founderOverride']}. "
                         f"Kapıyı ilerleten ÖLÇÜM DEĞİL, KURUCU KARARIDIR.")

    # ── fiziksel sınama kayıtları ile killGates.measured TUTARLI mı ──
    # Faz 3'te eklendi: `measured: true` yazmak yetmez; 19 kaydın
    # gerçekten doldurulmuş olması gerekir. Bir bayrak, olmayan bir
    # ölçümü var edemez (VALIDATION_PROTOCOL § 5).
    val_file = paths.REPORTS_TRACKED / "VAL_RECORDS.json"
    if val_file.exists():
        vd = json.loads(val_file.read_text(encoding="utf-8"))
        recs = vd.get("records", [])
        done = [r for r in recs if r.get("performed") is True]
        notes.append(f"fiziksel sınama kaydı: {len(done)}/{len(recs)} yapıldı")
        pv = kg.get("physicalValidation", {})
        if pv.get("book") == args.book:
            if pv.get("measured") is True and len(done) < len(recs):
                blockers.append(
                    f"physicalValidation: measured=true ama {len(recs) - len(done)} "
                    f"VAL kaydı BOŞ — ölçüm bayrağı kayıtlarla ÇELİŞİYOR "
                    f"(08_REPORTS/tracked/VAL_RECORDS.json).")
            if done and pv.get("measured") is not True:
                notes.append("VAL kayıtları dolmaya başlamış ama measured hâlâ false — "
                             "bu DOĞRUDUR; kapı ancak 19'un tamamı ve bir karar ile açılır.")
        bad = [r["validation_id"] for r in done
               if r.get("match") is None or not any(r.get("conditions", {}).values())]
        if bad:
            blockers.append(f"performed=true ama sonucu/koşulları eksik VAL kayıtları: "
                            f"{', '.join(bad[:5])} — kanıtsız bir sınama sayılmaz.")
        if done:
            failed = [r for r in done if r.get("match") is False]
            rate = len(failed) / len(done)
            notes.append(f"gözlenen hata oranı: %{rate*100:.1f} "
                         f"({len(failed)}/{len(done)}) — eşik: >%0 REVİZE, >%5 RED")
    else:
        notes.append("VAL_RECORDS.json yok — `python3 06_BUILD/build_val_kit.py`")

    spec_dir = paths.book_spec(args.book)
    for req in ("DIFFERENTIATION_TEST.md", "VALIDATION_PROTOCOL.md"):
        if not (spec_dir / req).exists():
            blockers.append(f"ön koşul eksik: {args.book}/00_SPEC/{req} — "
                            f"protokol yazılmadan ölçüm YAPILAMAZ.")

    passed = not blockers
    print(f"▸ kill_gate.py — {args.book}")
    print("  ⚠ Bu script kill-gate'i ÖLÇMEZ; ölçümün ön koşullarını ve kaydını denetler.")
    for n in notes:
        print(f"  ⚑ {n}")
    if blockers:
        print(f"  ✗ {len(blockers)} engel:")
        for b in blockers:
            print(f"    - {b}")
        print("  → SONUÇ: Faz 4 AÇILAMAZ.")
    else:
        print("  ✓ Mekanik ön koşullar tamam ve ölçüm PASS olarak kaydedilmiş.")
    if args.json:
        out = Path(args.json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"book": args.book, "blockers": blockers,
                                   "notes": notes, "mechanically_clear": passed},
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
