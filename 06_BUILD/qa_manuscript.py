#!/usr/bin/env python3
"""
qa_manuscript.py — manüskript katmanının kalite kapısı.

Faz 4'te eklendi. Var olan sekiz kapı VERİ katmanını denetliyordu ve
Faz 2'nin `B-10` dersi tam olarak şuydu: **bir kapı kümesi, sormadığı
soruyu yakalayamaz.** Bütün kapılar yeşilken üretilen 154 figürün
hiçbiri kitaba konulamıyordu.

Aynı kusur Faz 4'te BİR KEZ DAHA çıktı: ilk tam dizgide 29 ölçüm
figürünün hiçbiri kitapta yer almıyordu — bir ölçü bölümü, ölçüm
figürü olmadan. Kapılar yine yeşildi. Bu dosya o sınıfı kapatır.

Denetimler:
  ①  Bölüm mimarisinin TAMAMI dizildi mi (5 parça + 18 bölüm + ekler)
  ②  43 belirtinin HEPSİ bir bölüme yerleşti mi
  ③  Her belirti girişi YENİDEN GÖZLEM adımını taşıyor mu   (B-01)
  ④  Her belirti girişi BELİRTİYE ÖZGÜ eleme taşıyor mu      (B-03)
  ⑤  Her belirti girişi 'henüz değiştirme' uyarısını taşıyor mu
  ⑥  32 ölçünün HEPSİ bir figürle gösterildi mi
  ⑦  Kalibre edilmemiş kesinlik dili                        (§ 32)
  ⑧  İç kayıt kimliği okur metnine sızdı mı                 (K45/K46)
  ⑨  İç araç figürü kitaba kondu mu
  ⑩  Sayfa bütçesi bandın içinde mi                         (B-08)
  ⑪  İddia sicilindeki her maddi iddia metinden İZLENEBİLİR mi (§ 15)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from atlas import AtlasBuilder  # noqa: E402
import bookplan  # noqa: E402

# § 32 — kalibre edilmemiş kesinlik. Uyum belirleyici DEĞİLDİR.
#
# ⚠ İLK SÜRÜM 13 YANLIŞ POZİTİF ÜRETTİ ve hepsi aynı iki kalıptandı:
#   · "If the pressure goes, THE CAUSE IS in the back" — bu bir KOŞULDUR
#     ve tam olarak kitabın istediği kalibre dildir: bir test, sonra o
#     testin sonucu. Yasaklanacak şey koşulsuz nedensellik iddiasıdır.
#   · "The hem is ALWAYS read last" — bu bir YORDAM kuralıdır, nedensel
#     bir kesinlik değil.
# Bir denetim yakalaması gerekeni yakalamalı ve BAŞKA HİÇBİR ŞEYİ
# yakalamamalıdır; yanlış pozitif kapıyı işe yaramaz hâle getirir
# (build_pilot.py'de aynı ders 'press'/'pressure' ile öğrenilmişti).
#
# KOŞULSUZ nedensellik — her bağlamda yanlış:
OVERCLAIM_HARD = [
    r"\balways means\b", r"\balways indicates\b", r"\bnever means\b",
    r"\bguarantee[sd]?\b", r"\bwill fix\b", r"\bproven to\b",
    r"\bscientifically\b", r"\bdefinitely means\b",
    r"\bmust be caused by\b", r"\bcan only be\b", r"\bthe only cause\b",
]
# Bağlama bağlı — yalnızca KOŞUL YOKSA yanlış:
OVERCLAIM_CONDITIONAL = [r"\bthe cause is\b", r"\bthis means\b"]
CONDITION_CUES = ["if ", "when ", "unless ", "where ", "provided ",
                  # HEDGE de bir koşuldur: "the cause is OFTEN lower" kalibre
                  # bir cümledir ve yasaklanacak şey değildir.
                  "often", "usually", "commonly", "frequently", "may ",
                  "can be", "tends to", "in most", "almost always"]
# Yasağın KENDİSİNİ yazan cümleler muaftır: bir kitap "asla şöyle deme"
# diyebilmek için o ifadeyi ADLANDIRMAK zorundadır.
NEGATION = ["not ", "never ", "cannot", "does not", "do not", "rarely",
            "no single", "is not", "seldom"]


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def reader_strings(b: dict):
    for f in ("text", "caption", "title"):
        v = b.get(f)
        if isinstance(v, str):
            yield v
    for it in (b.get("items") or []):
        yield str(it)
    for r in (b.get("rows") or []):
        for c in r:
            yield str(c)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    findings: list = []
    bdir = paths.BOOK_DIRS[args.book]
    mdir = bdir / bookplan.MANUSCRIPT_DIR
    if not mdir.exists():
        print(f"▸ qa_manuscript.py — manüskript YOK ({mdir.relative_to(paths.ROOT)}); "
              f"bu kapı Faz 4 öncesi kitaplar için ATLANIR.")
        return 0

    atlas = AtlasBuilder(args.book, mdir)
    signs = atlas.signs
    measures = atlas.measures

    # ── bölümleri topla ──────────────────────────────────────────────
    chapters: dict = {}
    for _, _, keys in bookplan.PARTS:
        for key in keys:
            if key == "ch02":
                chapters[key] = atlas.measurement_chapter()
            elif key in bookplan.GENERATED:
                chapters[key] = atlas.chapter(bookplan.GENERATED[key])[0]
            else:
                f = mdir / f"{key}.json"
                if f.exists():
                    chapters[key] = load(f)["blocks"]
                else:
                    findings.append(f"① BÖLÜM YAZILMADI: {key}")

    # ② her belirti bir bölümde
    charted = set()
    for key in bookplan.GENERATED:
        if key == "ch02":
            continue
        charted |= set(atlas.chapter(bookplan.GENERATED[key])[1])
    missing = sorted(set(signs) - charted)
    if missing:
        findings.append(f"② {len(missing)} belirti hiçbir bölüme yerleşmedi: "
                        f"{', '.join(missing[:8])}")

    # ③④⑤ her belirti girişinin ZORUNLU üç parçası
    for sid in signs:
        blocks = atlas.sign_entry(sid)
        text = " ".join(s for b in blocks for s in reader_strings(b))
        if "Look again" not in text:
            findings.append(f"③ {sid}: YENİDEN GÖZLEM adımı yok (B-01).")
        if "reduced but has not gone" not in text:
            findings.append(f"③ {sid}: 'azaldı ama gitmedi' dalı yok (B-01).")
        if "Rule these out first" not in text:
            findings.append(f"④ {sid}: belirtiye özgü eleme yok (B-03).")
        if not any(b.get("type") == "callout" for b in blocks):
            findings.append(f"⑤ {sid}: 'henüz değiştirme' uyarısı yok.")

    # ⑥ her ölçü bir figürle
    ch02 = chapters.get("ch02", [])
    figured = {b["key"][len("meas_"):] for b in ch02
               if b.get("type") in ("figure", "figtable")
               and str(b.get("key", "")).startswith("meas_")}
    nofig = sorted(set(measures) - figured)
    if nofig:
        findings.append(f"⑥ {len(nofig)} ölçünün figürü kitapta YOK: "
                        f"{', '.join(nofig[:8])} — bir ölçü bölümünün işi şeridin "
                        f"yolunu GÖSTERMEKTİR.")

    # ⑦⑧⑨ metin taraması
    figs = load(paths.book_figures(args.book))
    internal = {m["source_file"][:-4] for m in figs["figure_meta"].values()
                if m.get("source_file") and m.get("internal")}
    hard = [(p, re.compile(p, re.I)) for p in OVERCLAIM_HARD]
    cond = [(p, re.compile(p, re.I)) for p in OVERCLAIM_CONDITIONAL]
    for key, blocks in chapters.items():
        for b in blocks:
            if b.get("type") in ("figure", "figtable") and b.get("key") in internal:
                findings.append(f"⑨ {key}: İÇ ARAÇ figürü kitapta — {b['key']}")
            for v in reader_strings(b):
                low = v.lower()
                for sent in re.split(r"(?<=[.!?])\s+", low):
                    negated = any(n in sent for n in NEGATION)
                    conditioned = any(c in sent for c in CONDITION_CUES)
                    for _, pat in hard:
                        m = pat.search(sent)
                        if m and not negated:
                            findings.append(f"⑦ {key}: KALİBRE EDİLMEMİŞ KESİNLİK "
                                            f"{m.group(0)!r} — «{sent[:80]}»")
                    for _, pat in cond:
                        m = pat.search(sent)
                        if m and not negated and not conditioned:
                            findings.append(f"⑦ {key}: KOŞULSUZ NEDENSELLİK "
                                            f"{m.group(0)!r} — «{sent[:80]}»")
                idm = bookplan.INTERNAL_ID.search(v)
                if idm:
                    findings.append(f"⑧ {key}: iç kimlik {idm.group(0)!r} okur "
                                    f"metninde — «{v[:70]}»")

    # ⑩⑪ ölçüm dosyasından
    idx_path = bdir / "02_CONTENT" / "public" / "manuscript_index.public.json"
    stats: dict = {}
    if idx_path.exists():
        idx = load(idx_path)
        stats = {"pages": idx["pages_total"], "figures": idx["figures_distinct"],
                 "chapters": idx["chapters_built"]}
        band = idx.get("page_target")
        if band and not (band[0] <= idx["pages_total"] <= band[1]):
            findings.append(f"⑩ SAYFA BÜTÇESİ: {idx['pages_total']}, hedef "
                            f"{band[0]}–{band[1]} (B-08).")
        claims_file = bdir / "02_CONTENT" / "public" / "claims.public.json"
        if claims_file.exists():
            reg = load(claims_file)
            # Her MADDİ iddia sınıfı metinden izlenebilir olmalıdır.
            # sign_observation ve sign_cause iddiaları taksonomi kimliğine
            # bağlıdır; girişler o kimlikleri claims alanında taşır.
            need = {c["taxonomy_ref"] for c in reg["claims"]
                    if c["kind"] in ("sign_observation", "sign_cause",
                                     "measurement_definition")}
            seen = set(idx.get("claims_referenced") or [])
            gap = sorted(need - seen)
            if gap:
                findings.append(f"⑪ {len(gap)} maddi iddia dizilen metinden "
                                f"İZLENEMİYOR: {', '.join(gap[:8])}")
            stats["claims_traced"] = len(need & seen)
            stats["claims_material"] = len(need)
    else:
        findings.append("⑩ ölçüm dosyası YOK — 06_BUILD/build_book.py çalıştırılmadı.")

    print("▸ qa_manuscript.py — manüskript kapısı")
    if stats:
        print(f"  {stats.get('chapters')} bölüm · {stats.get('pages')} sayfa · "
              f"{stats.get('figures')} figür · izlenen maddi iddia "
              f"{stats.get('claims_traced')}/{stats.get('claims_material')}")
    if findings:
        print(f"  ✗ {len(findings)} bulgu:")
        for f in findings[:40]:
            print(f"    - {f}")
        if len(findings) > 40:
            print(f"    … ve {len(findings)-40} bulgu daha")
    else:
        print("  ✓ 0 bulgu (on bir denetim)")
    if args.json:
        out = Path(args.json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"findings": findings, "stats": stats,
                                   "passed": not findings}, indent=2,
                                  ensure_ascii=False), encoding="utf-8")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
