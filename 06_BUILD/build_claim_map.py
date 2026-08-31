#!/usr/bin/env python3
"""
build_claim_map.py — CLAIM_SOURCE_MAP.md'yi ÜRETİR.

Faz 4 talimatı § 15. Belge elle yazılmaz: elle yazılan bir izlenebilirlik
haritası, sicille ilk düzenlemede ayrışır ve ayrıştığı an bir izlenebilirlik
haritası olmaktan çıkar — daha kötüsü, öyle görünmeye devam eder.

Girdi:  02_CONTENT/public/claims.public.json  (iddia sicili)
        02_CONTENT/public/manuscript_index.public.json (dizgi ölçümü)
        01_SOURCE/records/*.json
Çıktı:  00_SPEC/CLAIM_SOURCE_MAP.md
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

LEVEL_ORDER = ["VERIFIED", "VERIFIED_NARROWER", "PARTIALLY_VERIFIED",
               "CONTESTED", "INFERRED", "UNVERIFIED"]
LEVEL_MEANING = {
    "VERIFIED": "Kayıt doğrulanmış VE en az bir tam metin teknik otoritesine bağlı.",
    "VERIFIED_NARROWER": "Kaynak okundu ve İLKEYİ destekliyor, ama iddianın "
                         "yazıldığı hâlinden DAHA DAR bir ifadeyi destekliyor. "
                         "Kaydın `source_support_note` alanı kaynağın gerçekte "
                         "ne dediğini yazar (görev talimatı § 9).",
    "PARTIALLY_VERIFIED": "Kayıt doğrulanmış ama kaynak tam metin değil.",
    "CONTESTED": "Kaynaklar arasında KAYITLI tanım farkı var. Bir hata değildir — "
                 "Bölüm 2'nin öğretim malzemesidir.",
    "INFERRED": "Kaynak bağlamı destekliyor; iddianın KENDİSİ ajan türevi.",
    "UNVERIFIED": "Hiçbir otoriter kaynağa bağlı değil.",
}
CH_TITLE = {
    "B1-CH01": "1 · Why the pattern did not fit", "B1-CH02": "2 · Measuring your body",
    "B1-CH03": "3 · Reading the pattern", "B1-CH04": "4 · The fitting garment",
    "B1-CH05": "5 · The fitting session", "B1-CH06": "6 · The seven-step cycle",
    "B1-CH07": "7 · Naming what you see", "B1-CH08": "8 · Ruling out false causes",
    "B1-CH09": "9 · Neck and shoulder", "B1-CH10": "10 · Upper back and armhole",
    "B1-CH11": "11 · Bust and chest", "B1-CH12": "12 · Waist and torso length",
    "B1-CH13": "13 · Hip and seat", "B1-CH14": "14 · Sleeve and arm",
    "B1-CH15": "15 · Trousers: crotch and leg", "B1-CH16": "16 · Order of work",
    "B1-CH17": "17 · Your fit profile", "B1-CH18": "18 · Carrying it forward",
}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    bdir = paths.BOOK_DIRS[args.book]
    reg = load(bdir / "02_CONTENT" / "public" / "claims.public.json")
    idx_p = bdir / "02_CONTENT" / "public" / "manuscript_index.public.json"
    idx = load(idx_p) if idx_p.exists() else {}
    srcs = {}
    for f in sorted(paths.SOURCE_RECORDS.glob("S-*.json")):
        r = load(f)
        srcs[r["source_id"]] = r
    traced = set(idx.get("claims_referenced") or [])

    by_level = Counter(c["evidence_level"] for c in reg["claims"])
    by_ch = defaultdict(Counter)
    by_src = Counter()
    for c in reg["claims"]:
        by_ch[c["chapter"]][c["evidence_level"]] += 1
        for s in c["source_refs"]:
            by_src[s] += 1

    L = []
    A = L.append
    A("# CLAIM SOURCE MAP — BEFORE YOU CUT, Book 1")
    A("")
    A("> **ÜRETİLMİŞ BELGE — elle düzenlenmez.**")
    A("> Kaynak: `06_BUILD/build_claim_map.py` · sicil:")
    A("> `02_CONTENT/public/claims.public.json`")
    A(">")
    A("> Faz 4 talimatı § 15. Her teknik olarak maddi ifade buradan kaynağına")
    A("> ve doğrulama durumuna izlenir.")
    A(">")
    A("> **`evidence_level` BEYAN DEĞİL TÜREVDİR:** taksonomi kaydının")
    A("> `verification_status`'ünden ve atıf yaptığı kaynakların")
    A("> otoritesinden hesaplanır. Hiçbir iddia kendi seviyesini yazamaz.")
    A("")
    A("---")
    A("")
    A("## 1 · Toplam")
    A("")
    A(f"**{reg['count']} iddia.**")
    A("")
    A("| Kanıt seviyesi | Sayı | Oran | Anlamı |")
    A("|---|---:|---:|---|")
    for lv in LEVEL_ORDER:
        n = by_level.get(lv, 0)
        if n:
            A(f"| `{lv}` | {n} | %{n*100/reg['count']:.1f} | {LEVEL_MEANING[lv]} |")
    A("")
    A("> ⚠ **`INFERRED` çoğunluktadır ve bu gizlenmemiştir.** Kitabın")
    A("> teşhis ilişkileri (belirti → aday neden) kamu kaynaklarında")
    A("> tek tek doğrulanamadı; Faz 1 bunu kaydetti, Faz 4 değiştirmedi.")
    A("> Bu yüzden her giriş bir CEVAP değil bir FİZİKSEL TEST verir.")
    A("")
    A("## 2 · İddia türüne göre")
    A("")
    A("| Tür | Sayı | Ne dayatır |")
    A("|---|---:|---|")
    KIND_NOTE = {
        "conceptual": "Yöntem katmanı — kitabın öğrettiği kuralın kendisi.",
        "measurement_definition": "Bir ölçünün nereden nereye alındığı.",
        "measurement_path": "Şeridin serbest değil KISITLI olduğu.",
        "adjustment_family": "Bir düzeltmenin kalıbın hangi alanına dokunduğu.",
        "adjustment_order": "Hangi düzeltmenin hangisinden önce geldiği.",
        "sign_observation": "Bir belirtinin gözlenebilir olduğu ve nerede durduğu.",
        "sign_cause": "Bir nedenin AYIRT EDİCİ kanıtı — kitabın en riskli sınıfı.",
    }
    for k, n in sorted(Counter(c["kind"] for c in reg["claims"]).items(),
                       key=lambda x: -x[1]):
        A(f"| `{k}` | {n} | {KIND_NOTE.get(k, '')} |")
    A("")
    A("## 3 · Bölüme göre")
    A("")
    A("| Bölüm | İddia | `VERIFIED` | `V_NARROWER` | `CONTESTED` | `INFERRED` "
      "| `UNVERIFIED` |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for ch in sorted(by_ch):
        c = by_ch[ch]
        A(f"| {CH_TITLE.get(ch, ch)} | {sum(c.values())} | {c.get('VERIFIED',0)} | "
          f"{c.get('VERIFIED_NARROWER',0)} | "
          f"{c.get('CONTESTED',0)} | {c.get('INFERRED',0)} | {c.get('UNVERIFIED',0)} |")
    A("")
    A("## 4 · Kaynağa göre")
    A("")
    A("| Kaynak | İddia | Otorite | Erişim | Başlık |")
    A("|---|---:|:---:|---|---|")
    for sid, n in by_src.most_common():
        s = srcs.get(sid, {})
        auth = "✓" if s.get("technical_authority") else "—"
        A(f"| `{sid}` | {n} | {auth} | {s.get('verification_level','?')} | "
          f"{str(s.get('title',''))[:52]} |")
    A("")
    A("## 5 · İzlenebilirlik")
    A("")
    material = [c for c in reg["claims"]
                if c["kind"] in ("sign_observation", "sign_cause",
                                 "measurement_definition")]
    hit = [c for c in material if c["taxonomy_ref"] in traced]
    A(f"Dizilen metinden izlenen maddi iddia: **{len(hit)}/{len(material)}**")
    A("")
    A("Ölçüm: `06_BUILD/qa_manuscript.py § ⑪`. Bir iddianın izlenebilir")
    A("sayılması için manüskript bloğunun `claims` alanında taksonomi")
    A("kimliğini TAŞIMASI gerekir; blok o kimliği taşımıyorsa kapı kırmızı yakar.")
    A("")
    A("## 6 · Faz 4 bağımsız incelemesinde DEĞİŞEN iddialar")
    A("")
    cc = load(bdir / "00_SPEC" / "CONCEPTUAL_CLAIMS.json")
    changed = [c for c in cc["claims"] if c.get("phase4_review")]
    A(f"**{len(changed)} kavramsal iddia** bağımsız inceleme sonucunda yeniden yazıldı.")
    A("")
    A("| # | Karar | Gerekçe |")
    A("|---|---|---|")
    for c in changed:
        r = c["phase4_review"]
        A(f"| `{c['id']}` | {r['resolution']} | {r['note']} |")
    A("")
    A("Tam gerekçeler ve kaynaklar:")
    A("[`../../08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md`]"
      "(../../08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md).")
    A("")
    A("---")
    A("")
    A("*Vâliçe Press · BEFORE YOU CUT, Book 1 · Claim Source Map · ÜRETİLMİŞ*")
    A("")

    text = "\n".join(L)
    out = bdir / "00_SPEC" / "CLAIM_SOURCE_MAP.md"
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            print("✗ CLAIM_SOURCE_MAP.md BAYAT — build_claim_map.py yeniden çalıştırılmalı")
            return 1
        print("▸ build_claim_map.py --check — güncel")
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"▸ build_claim_map.py — {out.relative_to(paths.ROOT)}")
    print(f"  {reg['count']} iddia · izlenen maddi iddia {len(hit)}/{len(material)} · "
          f"{len(changed)} kavramsal iddia Faz 4'te değişti")
    return 0


if __name__ == "__main__":
    sys.exit(main())
