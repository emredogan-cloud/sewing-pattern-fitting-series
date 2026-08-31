#!/usr/bin/env python3
"""
build_claims.py — iddia sicilini ÜRETİR (yazmaz).

Faz 4 talimatı § 15: her teknik olarak maddi ifade izlenebilir olmalıdır.
Bu script o izlenebilirliği bir BEYAN olarak değil bir TÜREVE olarak
kurar: kanıt seviyesi (`evidence_level`) taksonomi kaydının
`verification_status`'ünden ve atıf yaptığı kaynakların OTORİTESİNDEN
hesaplanır. Hiçbir iddia kendi kanıt seviyesini yazamaz.

Kanıt seviyesi vokabüleri (Faz 4 talimatı § 5):

  VERIFIED             kayıt technical_reference_verified VE en az bir
                       technical_authority kaynağı tam metin/resmî PDF
                       VE kayıt `source_support: narrower` TAŞIMIYOR
  VERIFIED_NARROWER    yukarıdakinin hepsi sağlanıyor AMA kaydın kendisi
                       kaynağın DAHA DAR bir ifadeyi desteklediğini beyan
                       ediyor (`source_support: narrower`). Görev talimatı
                       § 9: ilke destekleniyor, ifade fazla geniş.
  PARTIALLY_VERIFIED   kayıt doğrulanmış ama kaynak tam metin değil,
                       ya da yalnızca kısmi kapsama var
  INFERRED             kaynak bağlamı destekliyor, iddianın KENDİSİ
                       ajan türevi (agent_drafted_unverified)
  CONTESTED            kaynaklar arasında kayıtlı tanım farkı var
                       (SOURCE_MAP § 7)
  UNVERIFIED           hiçbir kaynağa bağlı değil

⚠ CONTESTED bir HATA DEĞİLDİR. Dört ölçü tanımı kaynaklar arasında
gerçekten farklıdır ve bu fark Bölüm 2'nin öğretim malzemesidir.

Çıktı: BOOK-xx/02_CONTENT/public/claims.public.json  (.gitignore izin
listesi: BOOK-*/02_CONTENT/public/*.public.json — proza değil, SİCİL).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

# SOURCE_MAP § 7 — kaynaklar arası kayıtlı tanım farkları.
#
# ⚠ İÇERİK TURU: bu küme burada ELLE YAZILIYORDU ve ölçü kaydının kendi
# `source_conflict` alanıyla İKİ AYRI doğruluk kaynağı oluşturuyordu.
# Faz 5 tam da bu sınıftan bir kusur ölçmüştü (figür başlığı çelişkiyi
# TÜRETİYOR, kayıt BEYAN EDİYORDU). Küme artık KAYITTAN okunur.

ZONE_TO_CHAPTER = {
    "neck": "B1-CH09", "shoulder": "B1-CH09",
    "upper_back": "B1-CH10", "armhole": "B1-CH10",
    "bust_chest": "B1-CH11",
    "waist_torso": "B1-CH12",
    "hip_seat": "B1-CH13",
    "sleeve_arm": "B1-CH14",
    "crotch_leg": "B1-CH15",
    "whole_garment": "B1-CH16",
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def source_index() -> dict:
    idx = {}
    for f in sorted(paths.SOURCE_RECORDS.glob("S-*.json")):
        rec = load(f)
        idx[rec["source_id"]] = rec
    return idx


def evidence_level(status: str, refs: list, srcs: dict, contested: bool,
                   narrower: bool = False) -> str:
    """Kanıt seviyesi TÜRETİLİR — beyan edilmez.

    ⚠ İÇERİK TURU: `narrower` bir GÜVEN SKORU değildir. Kaydın kendisi,
    okunmuş kaynağın iddiadan DAHA DAR bir ifadeyi desteklediğini
    BEYAN ettiğinde doğrudur ve o beyan `source_support_note` alanında
    kaynağın ne dediğini yazmak zorundadır. Beyan yoksa alan da yoktur.
    """
    if contested:
        return "CONTESTED"
    if not refs:
        return "UNVERIFIED"
    authoritative = [srcs[r] for r in refs if r in srcs and srcs[r].get("technical_authority")]
    if not authoritative:
        return "UNVERIFIED"
    fulltext = [s for s in authoritative
                if s.get("verification_level") in ("fulltext", "official_pdf")]
    acquired = [s for s in authoritative
                if s.get("acquisition_status") in ("public_access", "acquired")]
    if status == "technical_reference_verified":
        if not fulltext:
            return "PARTIALLY_VERIFIED"
        return "VERIFIED_NARROWER" if narrower else "VERIFIED"
    if not acquired:
        return "UNVERIFIED"
    return "INFERRED"


def build(book_id: str) -> dict:
    srcs = source_index()
    claims: list = []
    n = 0

    def add(kind, chapter, text, refs, status, taxonomy_ref, contested=False, risk=None,
            narrower=False, support_note=None):
        nonlocal n
        n += 1
        claims.append({
            "claim_id": f"CLM-{n:04d}",
            "kind": kind,
            "chapter": chapter,
            "claim": text,
            "taxonomy_ref": taxonomy_ref,
            "source_refs": refs,
            "record_verification_status": status,
            "evidence_level": evidence_level(status, refs, srcs, contested, narrower),
            "source_support_note": support_note,
            # ⚠ KAYNAK ADLİ İNCELEMESİ (H-2): bu alan 309 kaydın
            # 309'unda "pending" idi ve Ek G okura bağımsız incelemenin
            # TAMAMLANDIĞINI söylüyordu. İkisi aynı anda doğru olamaz.
            # Alan artık gerçeği söyler: incelemeler KOŞTU ve KAYIT
            # DÜZEYİNDE imzalanmadı — bir inceleme kitabı okur, sicili
            # satır satır imzalamaz. Sicilin işi bunu GİZLEMEMEKTİR.
            "reviewer_status": "not_signed_off_at_record_level",
            "risk_note": risk,
        })

    # ① kavramsal iddialar — YÖNTEM katmanı
    cc = load(paths.book_spec(book_id).parent / "00_SPEC" / "CONCEPTUAL_CLAIMS.json")
    for c in cc["claims"]:
        # ⚠ KAYNAK ADLİ İNCELEMESİ (M-1): burada durum SABİT yazılıydı ve
        # sicil, kaynağında KELİMESİ KELİMESİNE bulunan bir yöntem
        # iddiasını VERIFIED gösteremiyordu. Bir sicil kanıtı olduğundan
        # ZAYIF göstermemelidir; bu da bir ölçüm hatasıdır.
        add("conceptual", c["chapter"], c["claim"], c["source_refs"],
            c.get("verification_status", "agent_drafted_unverified"), c["id"],
            risk=c["risk_note"],
            narrower=c.get("source_support") == "narrower",
            support_note=c.get("source_support_note"))

    # ② ölçü tanımları — her ölçü İKİ iddia taşır: TANIM ve YOL
    for m in load(paths.MEASUREMENTS)["measurements"]:
        mid = m["measurement_id"]
        contested = bool(m.get("source_conflict"))
        narrow = m.get("source_support") == "narrower"
        note = m.get("source_support_note")
        derived = m["category"] == "derived"
        add("measurement_definition", "B1-CH02",
            (f"{m['name']} is calculated from {m['landmark_start']} and "
             f"{m['landmark_end']}." if derived else
             f"{m['name']} is measured from {m['landmark_start']} to {m['landmark_end']}."),
            m.get("source_refs") or [], m["verification_status"], mid, contested,
            risk="A measurement taken from the wrong landmark is not a smaller error than "
                 "no measurement; it is a confident wrong number.",
            narrower=narrow, support_note=note)
        if m.get("path_rule"):
            # ⚠ İÇERİK TURU · L-3: TÜRETİLMİŞ ölçünün ŞERİT YOLU YOKTUR.
            # Sicil üç türetilmiş ölçü için "the tape path is constrained"
            # iddiası üretiyordu ve biri (M-031) VERIFIED sayılıyordu.
            # Bir iddia, tanımı gereği var olmayan bir şey hakkında
            # doğrulanmış olamaz. Türetilmiş ölçüler artık TÜRETME
            # iddiası taşır.
            add("measurement_path", "B1-CH02",
                (f"{m['name']}: the two inputs are fixed and the subtraction order "
                 f"is fixed (see the record's path_rule)." if derived else
                 f"{m['name']}: the tape path is constrained, not free "
                 f"(see the record's path_rule)."),
                m.get("source_refs") or [], m["verification_status"], mid, contested,
                risk=("A difference computed the other way round changes sign and "
                      "sends the reader to the opposite adjustment." if derived else
                      "Two readers following the same name but different paths get "
                      "different numbers and blame the pattern."),
                narrower=narrow, support_note=note)

    # ③ düzeltme ailesi kapsamı + sıra kısıtı
    for a in load(paths.ADJUSTMENT_FAMILIES)["families"]:
        aid = a["adjustment_family_id"]
        add("adjustment_family", "B1-CH16",
            f"{a['name']} acts on: {a['pattern_area']}.",
            a.get("source_refs") or [], a["verification_status"], aid,
            risk="Naming the wrong pattern area sends the reader to Book 2 with the "
                 "wrong family and the adjustment fails there, not here.",
            narrower=a.get("source_support") == "narrower",
            support_note=a.get("source_support_note"))
        if a.get("order_constraint"):
            # ⚠ İÇERİK TURU · L-3: sıra iddiası AİLENİN kaydından seviye
            # alıyordu. Bir aileyi TANIMLAYAN kaynak, o ailenin NE ZAMAN
            # yapılacağını söylemek zorunda değildir — ve altısında
            # söylemiyordu. Sıra iddiası artık `order_source_refs`ten
            # türer; o boşsa iddia UNVERIFIED'dır.
            oref = a.get("order_source_refs", a.get("source_refs") or [])
            # ⚠ KAYNAK ADLİ İNCELEMESİ (H-4): yirmi sıra iddiasının METNİ
            # BİRBİRİNİN AYNISIYDI ("bir sıra kısıtı taşır") ve dört ayrı
            # kanıt düzeyi taşıyordu. Bir incelemeci iddiayı OKUYUP
            # doğrulayamıyordu, çünkü iddia kısıtın NE OLDUĞUNU
            # söylemiyordu. Metin artık kısıtı taşır.
            add("adjustment_order", "B1-CH16",
                f"{a['name']} — ordering constraint: {a['order_constraint']}",
                oref,
                # sıra iddiasının kayıt durumu SIRA kanıtından gelir;
                # ailenin kendi durumu ondan bağımsızdır
                ("technical_reference_verified" if oref
                 else "agent_drafted_unverified"),
                aid,
                risk="Out-of-order adjustment invalidates work already done.",
                narrower=a.get("order_support") == "narrower",
                support_note=a.get("order_support_note"))

    # ④ belirti gözlemi + her aday nedenin AYIRT EDİCİ KANITI
    #    Bu, kitabın EN RİSKLİ iddia sınıfıdır: 129 nedensel ilişki,
    #    hiçbiri fiziksel olarak sınanmadı.
    for s in load(paths.FIT_SIGNS)["signs"]:
        sid = s["symptom_id"]
        ch = ZONE_TO_CHAPTER[s["zone"]]
        add("sign_observation", ch,
            f"{sid} ({s['sign_class']}) is observable as described and appears at: "
            f"{s['where_it_appears']}.",
            s.get("source_refs") or [], s["verification_status"], sid,
            risk="If the sign is not reliably observable, the reader cannot enter the "
                 "diagnostic path at all.")
        for i, c in enumerate(s["candidate_causes"], 1):
            add("sign_cause", ch,
                f"{sid} may be caused by: {c['cause']} — distinguished by: "
                f"{c['distinguishing_evidence']}",
                s.get("source_refs") or [], s["verification_status"], f"{sid}.C{i}",
                risk="A cause whose distinguishing evidence does not actually "
                     "discriminate sends the reader to the wrong adjustment family.")

    by_level: dict = {}
    by_kind: dict = {}
    for c in claims:
        by_level[c["evidence_level"]] = by_level.get(c["evidence_level"], 0) + 1
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1

    return {
        "$comment": [
            "ÜRETİLMİŞ DOSYA — elle düzenlenmez. Kaynak: 06_BUILD/build_claims.py",
            "evidence_level TÜRETİLMİŞTİR; hiçbir iddia kendi seviyesini beyan etmez.",
            "reviewer_status: bağımsız incelemeler KİTABI okur ve bulgularını "
            "raporlara yazar; sicili SATIR SATIR imzalamazlar. Alan bu yüzden "
            "'not_signed_off_at_record_level' der ve 'pending' DEMEZ — bekleyen bir "
            "şey yok, yapılmayan bir şey var ve fark söylenmelidir.",
        ],
        "generated_by": "06_BUILD/build_claims.py",
        "book": book_id,
        "count": len(claims),
        "by_evidence_level": dict(sorted(by_level.items())),
        "by_kind": dict(sorted(by_kind.items())),
        "claims": claims,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--check", action="store_true",
                    help="diskteki sicil güncel mi — YAZMAZ")
    args = ap.parse_args()

    data = build(args.book)
    out = paths.BOOK_DIRS[args.book] / "02_CONTENT" / "public" / "claims.public.json"
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not out.exists():
            print(f"✗ iddia sicili YOK: {out.relative_to(paths.ROOT)}")
            return 1
        if out.read_text(encoding="utf-8") != text:
            print("✗ iddia sicili BAYAT — 06_BUILD/build_claims.py yeniden çalıştırılmalı")
            return 1
        print(f"▸ build_claims.py --check — güncel ({data['count']} iddia)")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"▸ build_claims.py — {out.relative_to(paths.ROOT)}")
    print(f"  {data['count']} iddia · " +
          " · ".join(f"{k}:{v}" for k, v in data["by_evidence_level"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
