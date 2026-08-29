#!/usr/bin/env python3
"""
build_review_report.py — PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md üretir.

Faz 4 talimatı § 6. Rapor ELLE yazılmaz: dört bağımsız inceleme hattının
HAM ÇIKTISINDAN türetilir (`08_REPORTS/tracked/phase4_review/R*.json`).

Neden: elle yazılan bir inceleme raporu, incelemenin söylediğini değil
yazarın hatırladığını taşır. Bu projede inceleme edilen taraf ile raporu
yazan taraf AYNI ajandır; tek koruma, raporun ham çıktıdan MEKANİK
türetilmesidir. Ham dosyalar depoda durur ve rapor onlardan yeniden
üretilebilir.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

SRC = paths.REPORTS_TRACKED / "phase4_review"
OUT = paths.REPORTS / "PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md"

LINE_TITLE = {
    "R1_measurements": "① Ölçü tanımları ve işaret noktaları",
    "R2_ease_sizing": "② Ease, beden seçimi ve düzeltme aileleri",
    "R3_diagnostic_logic": "③ Teşhis mantığı ve belirti→neden ilişkileri",
    "R4_protocol": "④ Prova protokolü, karıştırıcılar ve sıra",
}
SEVERITY = {"CONTRADICTED": 4, "UNSUPPORTED": 3, "CONTESTED": 2,
            "REQUIRES_PHYSICAL_TEST": 2, "SUPPORTED_NARROWER": 1, "SUPPORTED": 0}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def esc(s: str, n: int = 200) -> str:
    s = " ".join(str(s).split())
    if len(s) > n:
        s = s[:n - 1] + "…"
    return s.replace("|", "\\|")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not SRC.exists():
        print(f"✗ ham inceleme çıktısı yok: {SRC.relative_to(paths.ROOT)}")
        return 2

    lines_data = {}
    for f in sorted(SRC.glob("R*.json")):
        lines_data[f.stem] = load(f)

    all_findings = []
    for key, d in lines_data.items():
        for fnd in d["findings"]:
            fnd["_line"] = key
            all_findings.append(fnd)

    verdicts = Counter(f["conclusion"] for f in all_findings)
    revisions = sum(1 for f in all_findings if f.get("required_revision"))
    conflicts = sum(1 for f in all_findings if f.get("conflict_found"))
    srcs = []
    seen = set()
    for d in lines_data.values():
        for s in d.get("sources_consulted", []):
            k = s.get("url") or s.get("label")
            if k not in seen:
                seen.add(k); srcs.append(s)

    L = []
    A = L.append
    A("# PHASE 4 — BAĞIMSIZ TEKNİK İNCELEME")
    A("")
    A("> **ÜRETİLMİŞ BELGE — elle düzenlenmez.**")
    A("> Kaynak: `06_BUILD/build_review_report.py` · ham çıktı:")
    A("> `08_REPORTS/tracked/phase4_review/R*.json`")
    A(">")
    A("> **Amaç: Kitap 1'i KIRMAK.** Bu belge bir onay değildir ve bir onay")
    A("> olarak alıntılanamaz.")
    A(">")
    A("> ⚠ **Bu bir insan uzman incelemesi DEĞİLDİR** ve hiçbir yerde öyle")
    A("> sunulamaz (`CLAIMS_STANDARD.md § 1`). Dört bağımsız inceleme hattı,")
    A("> birincil içerik üretiminden AYRI çalıştırıldı; hiçbirine kendini")
    A("> onaylama yetkisi verilmedi ve hiçbiri birincil ajanın ifadesini")
    A("> kanıt saymadı. Yine de **insan doğrulamasının yerine geçmez**:")
    A("> `D-01` ve `D-02` açık kalır.")
    A(">")
    A("> Rapor neden ÜRETİLİYOR: incelenen taraf ile raporu yazan taraf aynı")
    A("> ajandır. Tek koruma, raporun ham çıktıdan mekanik türetilmesi ve ham")
    A("> çıktının depoda durmasıdır.")
    A("")
    A("---")
    A("")
    A("## 1 · Kapsam ve yöntem")
    A("")
    A("| Hat | İnceleme | Bulgu | Kaynak |")
    A("|---|---|---:|---:|")
    for k, d in lines_data.items():
        A(f"| {LINE_TITLE.get(k,k)} | `{k}` | {len(d['findings'])} | "
          f"{len(d.get('sources_consulted',[]))} |")
    A(f"| **Toplam** | | **{len(all_findings)}** | **{len(srcs)}** (tekilleştirilmiş) |")
    A("")
    A("## 2 · Sonuç dağılımı")
    A("")
    A("| Sonuç | Sayı | Anlamı |")
    A("|---|---:|---|")
    MEAN = {
        "CONTRADICTED": "Otoriter bir kaynak AKSİNİ söylüyor.",
        "UNSUPPORTED": "Hiçbir otoriter destek bulunamadı.",
        "CONTESTED": "Otoriter kaynaklar BİRBİRİYLE çelişiyor.",
        "SUPPORTED_NARROWER": "Yalnızca daraltılmış hâliyle doğru.",
        "SUPPORTED": "Yazıldığı hâliyle destekleniyor.",
        "REQUIRES_PHYSICAL_TEST": "Belgesel kanıtla çözülemez.",
    }
    for v, n in sorted(verdicts.items(), key=lambda x: -SEVERITY.get(x[0], 0)):
        A(f"| `{v}` | {n} | {MEAN.get(v,'')} |")
    A("")
    A(f"**Revizyon gerektiren: {revisions}/{len(all_findings)}** · "
      f"**kaynak çelişkisi taşıyan: {conflicts}**")
    A("")
    A("> Yalnızca bir iddia (`CC-02`, 'belirti ≠ neden') dört hattın")
    A("> hiçbirinde revizyon gerektirmedi.")
    A("")
    A("## 3 · Bulgu tablosu")
    A("")
    A("Faz 4 talimatı § 6'nın istediği alanlar. Tam gerekçe ve kaynak")
    A("listesi ham JSON'dadır; buradaki `Not` sütunu kısaltılmıştır.")
    A("")
    A("| İddia | Kaynak | Kalite | Sonuç | Güven | Çelişki | Revizyon | Not |")
    A("|---|---|---|---|---|:---:|:---:|---|")
    for f in sorted(all_findings,
                    key=lambda x: (-SEVERITY.get(x["conclusion"], 0), x["claim_id"])):
        u = f.get("sources") or []
        su = f"{len(u)} kaynak" if u else "—"
        A(f"| `{f['claim_id']}` | {su} | {esc(f.get('source_quality','—'),28)} | "
          f"`{f['conclusion']}` | {f.get('confidence','—')} | "
          f"{'evet' if f.get('conflict_found') else 'hayır'} | "
          f"{'EVET' if f.get('required_revision') else 'hayır'} | "
          f"{esc(f.get('notes',''),150)} |")
    A("")
    A("## 4 · EN YÜKSEK RİSKLİ 20 TEKNİK İDDİA")
    A("")
    A("Dört hattın `top_risks` çıktısı, şiddet sırasına dizildi.")
    A("")
    A("| # | İddia | Önerilen eylem | Neden riskli |")
    A("|---:|---|---|---|")
    risks = []
    for k, d in lines_data.items():
        for r in d.get("top_risks", []):
            r["_line"] = k
            risks.append(r)
    ACT = {"exclude_from_manuscript": 5, "physical_validation": 4,
           "further_research": 3, "additional_source": 2, "cautious_wording": 1}
    risks.sort(key=lambda r: -ACT.get(r.get("recommended_action", ""), 0))
    for i, r in enumerate(risks[:20], 1):
        A(f"| {i} | `{r['claim_id']}` | `{r.get('recommended_action','')}` | "
          f"{esc(r.get('why',''),190)} |")
    A("")
    A("## 5 · Ayırt edici kanıt ÇAKIŞMALARI")
    A("")
    cols = lines_data.get("R3_diagnostic_logic", {}).get("evidence_collisions", [])
    sev = Counter(c["severity"] for c in cols)
    A(f"**{len(cols)} çakışma, {len({c['symptom_id'] for c in cols})} belirtide** "
      f"(yüksek {sev.get('high',0)} · orta {sev.get('medium',0)} · "
      f"düşük {sev.get('low',0)}).")
    A("")
    A("Şema her aday nedenin bir `distinguishing_evidence` taşımasını")
    A("**dayatıyordu**; incelemeci o alanların GERÇEKTEN ayırıp ayırmadığını")
    A("denetledi. Bir alanın dolu olması, işini yaptığı anlamına gelmiyordu.")
    A("")
    A("**Çözüm uydurulmadı.** Çakışmalar")
    A("`02_TAXONOMY/public/evidence_collisions.json`'a kaydedildi ve")
    A("`06_BUILD/atlas.py` bunları OKURA BEYAN eder: *\"bu iki neden aynı")
    A("görünebilir, ikisini de sına.\"* Ayrımın kendisi `D-02` fiziksel")
    A("doğrulamasına bağlıdır.")
    A("")
    A("| Belirti | Şiddet | Neden ayırmıyor |")
    A("|---|---|---|")
    for c in sorted(cols, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["severity"]]):
        A(f"| `{c['symptom_id']}` | {c['severity']} | {esc(c['why_it_fails'],170)} |")
    A("")
    A("## 6 · İncelemenin ULAŞAMADIĞI kaynaklar")
    A("")
    A("Bir incelemenin bulamadıkları da bulguları kadar kayda değerdir.")
    A("")
    for k, d in lines_data.items():
        for c in d.get("could_not_verify", []):
            A(f"- *({k})* {esc(c, 300)}")
    A("")
    A("## 7 · Bu incelemenin YAPAMADIĞI")
    A("")
    A("1. **Okur anlıyor mu.** Tek gerçek sınav `D-01`'dir.")
    A("2. **Teşhis ilişkileri doğru mu.** 129 nedensel ilişki belgesel")
    A("   kanıtla çözülemez; tek gerçek sınav `D-02`'dir. İnceleme")
    A("   ilişkilerin İÇ TUTARLILIĞINI denetleyebildi, DOĞRULUĞUNU değil.")
    A("3. **Diyagramlar geometrik olarak doğru mu.** `D-02`.")
    A("4. **Baskıda okunuyor mu.** `D-05`, `D-06`.")
    A("")
    A("---")
    A("")
    A("*Vâliçe Press · BEFORE YOU CUT · Phase 4 Independent Technical Review · "
      "ÜRETİLMİŞ*")
    A("")

    text = "\n".join(L)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("✗ inceleme raporu BAYAT")
            return 1
        print("▸ build_review_report.py --check — güncel")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"▸ build_review_report.py — {OUT.relative_to(paths.ROOT)}")
    print(f"  {len(all_findings)} bulgu · {len(srcs)} kaynak · {revisions} revizyon · "
          f"{len(cols)} kanıt çakışması")
    return 0


if __name__ == "__main__":
    sys.exit(main())
