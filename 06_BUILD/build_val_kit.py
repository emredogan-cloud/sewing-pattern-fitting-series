#!/usr/bin/env python3
"""
build_val_kit.py — fiziksel sınama kitini KAYIT VERİSİNDEN üretir.

`BOOK-01/00_SPEC/VALIDATION_PROTOCOL.md § 4.5`: 19 `VAL` kaydı,
`A13` kapsamı (`DECISIONS.md K29`).

Bu script sınamayı YAPMAZ — yapamaz. Kumaş, iğne, dikiş makinesi ve bir
vücut gerekir. Yaptığı şey, kurucunun sınamayı **bağımsız olarak**
uygulayabilmesi için gereken her şeyi taksonomiden üretmektir:

  · hangi sapma, hangi belirtiyi üretmeli
  · kitabın o belirtiden çıkaracağı teşhis (crosswalk'tan)
  · beklenen sonuç ve kabul ölçütü
  · boş kayıt formu (`VALIDATION_PROTOCOL § 5` alanları)

Çıktı iki dosyadır:
  · `09_OUTPUT/VALIDATION_KIT.md` — yazdırılıp yanına konacak kit
  · `08_REPORTS/tracked/VAL_RECORDS.json` — BOŞ kayıt iskeleti

⚠ `VAL_RECORDS.json`'daki her kaydın `performed` alanı `false`'tur ve
  bu script onu ASLA `true` yapmaz. Bir kaydı dolduran şey bir dış
  olaydır (`EXTERNAL_DEPENDENCIES.md D-02`).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

ZONE = "bust_chest"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def build(book_id: str):
    signs = [s for s in load(paths.FIT_SIGNS)["signs"] if s["zone"] == ZONE]
    labels = load(paths.LABELS_EN)
    families = {f["adjustment_family_id"]: f["name"]
                for f in load(paths.ADJUSTMENT_FAMILIES)["families"]}
    measures = {m["measurement_id"]: m for m in load(paths.MEASUREMENTS)["measurements"]}
    confounders: list[str] = []
    for s in load(paths.FIT_SIGNS)["signs"]:
        for c in s.get("confounders_to_rule_out", []):
            h = c.split(":")[0].strip()
            if h not in confounders:
                confounders.append(h)

    records, rows = [], []
    n = 0

    def add(method, target, deviation, expected_sign, expected_dx, accept, note=None):
        nonlocal n
        n += 1
        vid = f"VAL-{n:04d}"
        records.append({
            "validation_id": vid, "book": book_id, "method": method,
            "target": target,
            "induced_deviation": deviation,
            "expected_sign": expected_sign,
            "expected_book_diagnosis": expected_dx,
            "acceptance": accept,
            "note": note,
            # ── ölçüm alanları: DIŞ OLAY doldurur ──
            "performed": False,
            "performed_on": None,
            "observed_sign": None,
            "book_diagnosis": None,
            "match": None,
            "discriminating_evidence_worked": None,
            "new_signs_appeared": None,
            "reverted_and_verified": None,
            "conditions": {"fabric": None, "underwear": None, "posture": None,
                           "seam_allowance": None, "marking": None,
                           "observer": None, "movement_test": None},
        })
        rows.append((vid, method, target, deviation, expected_sign, expected_dx, accept))
        return vid

    # ── Y-1 · belirti üretme (4 kayıt) ────────────────────────────────
    y1 = [s for s in signs if len(s["candidate_causes"]) >= 3][:4]
    for s in y1:
        sid = s["symptom_id"]
        lab = labels["signs"][sid]
        c0 = s["candidate_causes"][0]
        af = c0.get("adjustment_family_ref")
        add("Y-1 · belirti üretme",
            sid,
            f"Kontrol toile'a bilinen bir sapma uygula: {c0['cause']}. "
            f"Miktar KAYDEDİLİR (geri dönülebilir teknikle — VALIDATION_PROTOCOL § 4.3).",
            lab["observation"],
            f"{af} — {families.get(af, af)}" if af else "eleme kalemi",
            "Uygulanan sapma, kayıtta yazan belirtiyi ÜRETMELİ ve kitabın o "
            "belirtiden çıkardığı teşhis, uygulanan sapmayla EŞLEŞMELİ.")

    # ── Y-2 · ayırt edicilik (3 kayıt) ────────────────────────────────
    for s in [x for x in signs if len(x["candidate_causes"]) >= 3][:3]:
        sid = s["symptom_id"]
        lab = labels["signs"][sid]
        add("Y-2 · ayırt edicilik",
            sid,
            "Aynı belirtiyi İKİ FARKLI nedenden üret (sırayla, her seferinde "
            "kontrol durumuna dönerek).",
            lab["observation"],
            "ayırt edici kanıt iki durumu AYIRMALI",
            "Kayıttaki `distinguishing_evidence` metni, iki durumu gözle "
            "ayırmaya YETMELİ. Yetmiyorsa kayıt REVİZE edilir.",
            note="Bu, teşhis sisteminin çekirdek iddiasıdır (C-C sınıfı).")

    # ── Y-4 · eleme kalemi (9 kayıt) ──────────────────────────────────
    for c in confounders[:9]:
        add("Y-4 · eleme kalemi",
            c,
            f"'{c}' karıştırıcısını KASTEN üret (ör. dikiş payını değiştir, "
            f"kenarı gerdir, çözgüye eğri kes).",
            "kalıp sorunuyla KARIŞABİLEN bir belirti",
            "eleme — kalıba dokunulmaz",
            "Eleme şemasının o adımı, karıştırıcıyı kalıp sorunundan AYIRMALI.")

    # ── Y-5 · sıra kısıtı (2 kayıt) ───────────────────────────────────
    for a, b, why in (
        ("AF-03/AF-04 omuz", "AF-01 göğüs",
         "Omuz düzeltmesi göğüs teşhisini değiştirir mi"),
        ("AF-01 göğüs", "AF-08 kol oyuntusu",
         "Göğüs düzeltmesi kol oyuntusu belirtisini ortadan kaldırır mı")):
        add("Y-5 · sıra kısıtı",
            f"{a} → {b}",
            "İki sapmayı BİRLİKTE uygula; önce yanlış sırada düzelt, sonra "
            "kontrol durumuna dön ve doğru sırada düzelt.",
            "iki belirti aynı anda",
            "sıra kuralı",
            f"{why}. Yanlış sıra İKİNCİ bir sorun üretmeli; doğru sıra "
            f"ikisini de çözmeli. Üretmiyorsa sıra kuralı KANITSIZDIR.")

    # ── Y-3 · ölçüm tekrarlanabilirliği (1 kayıt) ─────────────────────
    ch11_measures = ["M-001", "M-002", "M-003", "M-017", "M-018", "M-019", "M-031"]
    add("Y-3 · ölçüm tekrarı",
        "Bölüm 11'in yedi ölçüsü",
        "Aynı vücutta, aynı koşullarda, ÜÇ kez ölç: "
        + ", ".join(f"{measures[m]['name']}" for m in ch11_measures if m in measures),
        "—",
        "—",
        "Üç ölçümün yayılımı ⅛ inç'i AŞMAMALI. Aşıyorsa ölçünün "
        "`path_rule` metni yetersizdir ve YENİDEN YAZILIR.")
    return records, rows, ch11_measures, measures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    args = ap.parse_args()
    records, rows, ch11, measures = build(args.book)

    out_json = paths.REPORTS_TRACKED / "VAL_RECORDS.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({
        "$comment": [
            "VAL KAYIT İSKELETİ — 06_BUILD/build_val_kit.py üretti.",
            "Her kaydın `performed` alanı FALSE'tur ve bu script onu asla",
            "TRUE yapmaz. Bir kaydı dolduran şey bir DIŞ OLAYDIR:",
            "EXTERNAL_DEPENDENCIES.md D-02.",
            "",
            "⚠ FOTOĞRAF BU DOSYAYA GİRMEZ ve depoya girmez",
            "  (CONTENT_PROTECTION.md § 3). Yalnızca sayı, koşul ve sonuç.",
        ],
        "book": args.book,
        "scope": "A13 asgari uygulanabilir set — DECISIONS.md K29",
        "count": len(records),
        "performed_count": 0,
        "error_rate": None,
        "error_rate_note": "Ölçüm yapılmadan hata oranı HESAPLANAMAZ.",
        "records": records,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    kit = paths.BOOK_DIRS[args.book] / "09_OUTPUT" / "VALIDATION_KIT.md"
    kit.parent.mkdir(parents=True, exist_ok=True)
    L = []
    L.append("# FİZİKSEL SINAMA KİTİ — Kitap 1, Bölüm 11 (Göğüs)\n")
    L.append("> Üretici: `06_BUILD/build_val_kit.py` · kapsam: `A13` / `DECISIONS.md K29`")
    L.append("> · protokol: `BOOK-01/00_SPEC/VALIDATION_PROTOCOL.md`\n")
    L.append("> **Bu kiti AJAN UYGULAYAMAZ.** Kumaş, iğne, dikiş makinesi ve bir")
    L.append("> vücut gerekir. Kurucu bunu bağımsız olarak uygulayabilir.")
    L.append("> Sonuçlar `08_REPORTS/tracked/VAL_RECORDS.json`'a yazılır.\n")
    L.append("> **Hata oranı eşiği:** herhangi bir FAIL → pilot durur, kök nedenden")
    L.append("> düzeltilir. **>%5 → üretim yöntemi REDDEDİLİR.** 19 kayıtlık sette")
    L.append("> tek bir FAIL hata oranını **%5,3** yapar.\n")
    L.append("---\n")
    L.append("## Malzeme listesi\n")
    L.append("| Kalem | Miktar | Not |")
    L.append("|---|---|---|")
    L.append("| Muslin / prova bezi, orta ağırlık dokuma | ≈3 m | Kontrol toile + iki yedek parça |")
    L.append("| Şerit kumaş (sapma eklemek için) | artık parçalar | Geri dönülebilir hacim ekleme |")
    L.append("| Toplu iğne | bol | Geri dönülebilir sapma tekniği |")
    L.append("| İşaretleme kalemi / terzi tebeşiri | 1 | Denge çizgileri ve orta hatlar |")
    L.append("| Şerit metre | 1 | `Y-3` için |")
    L.append("| Lastik (bel bulmak için) | 1 | Doğal bel işaretleme |")
    L.append("| Fotoğraf makinesi / telefon | 1 | **Görüntüler DEPOYA GİRMEZ** |")
    L.append("\n**Tahmini maliyet:** ≈$15–30 · **tahmini süre:** ≈20–25 saat\n")
    L.append("---\n")
    L.append("## Yedi standart koşul — her kayıtta doldurulur\n")
    L.append("Kumaş · iç giyim · duruş · dikiş payı · işaretleme · gözlemci · hareket testi.")
    L.append("Koşullar arasında bir fark, sonuçlar arasındaki farkı AÇIKLAYABİLİR;")
    L.append("kaydedilmeyen bir koşul, açıklanamayan bir sonuç demektir.\n")
    L.append("---\n")
    L.append("## 19 kayıt\n")
    for (vid, method, target, dev, sign, dx, acc) in rows:
        L.append(f"### {vid} · {method}\n")
        L.append(f"**Hedef:** `{target}`\n")
        L.append(f"**Uygulanacak sapma:** {dev}\n")
        L.append(f"**Beklenen belirti:** {sign}\n")
        L.append(f"**Kitabın vermesi gereken teşhis:** {dx}\n")
        L.append(f"**Kabul ölçütü:** {acc}\n")
        L.append("| Alan | Değer |")
        L.append("|---|---|")
        for f in ("tarih", "kumaş", "iç giyim", "duruş", "dikiş payı", "işaretleme",
                  "gözlemci", "hareket testi", "uygulanan sapma MİKTARI",
                  "gözlenen belirti", "kitabın teşhisi", "EŞLEŞTİ mi (evet/hayır)",
                  "yeni belirti çıktı mı", "kontrol durumuna DÖNÜLDÜ mü"):
            L.append(f"| {f} | |")
        L.append("")
    L.append("---\n")
    L.append("## Sonuç sayfası\n")
    L.append("| | |")
    L.append("|---|---|")
    L.append("| Yapılan sınama sayısı | ___ / 19 |")
    L.append("| Beklenen sonucu ÜRETMEYEN sınama | ___ |")
    L.append("| **Hata oranı** | ___ % |")
    L.append("| Karar (PASS / REVISE / HARD STOP) | ___ |")
    L.append("\n**Hata oranı > %0 ise pilot durur ve kök nedenden düzeltilir.**")
    L.append("**Hata oranı > %5 ise üretim yöntemi reddedilir ve proje durur.**\n")
    L.append("*Vâliçe Press · Validation Kit · 28 Ağustos 2026*")
    kit.write_text("\n".join(L) + "\n", encoding="utf-8")

    print("▸ build_val_kit.py")
    print(f"  {len(records)} VAL kaydı üretildi · performed=false (hepsi)")
    print(f"  kit : {kit.relative_to(paths.ROOT)}")
    print(f"  kayıt: {out_json.relative_to(paths.ROOT)}")
    print("  ⚠ Sınamanın KENDİSİ yapılmadı — EXTERNAL_DEPENDENCIES.md D-02")
    return 0


if __name__ == "__main__":
    sys.exit(main())
