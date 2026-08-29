#!/usr/bin/env python3
"""
qa_visual.py — görsel sistem kapısı (Faz 2 / G5).

Bu kapının varlık nedeni: bir figür kaydı "doğru göründüğü" için doğru
sayılamaz. `validate_spec.py` figürün ŞEMASINI denetler; bu script
figürün SİSTEMLE tutarlılığını denetler.

Dokuz denetim:

  ① Token bütünlüğü — tanımsız token; kalibrasyon durumu kapıyla uyumlu mu
  ② Figür ↔ kayıt bağı — var olmayan SYM/M/AF'ye referans
  ③ Gerekçesiz elle çizim — deterministic=false ise manual_reason zorunlu
  ④ Akış şeması kapsaması — her belirtinin şeması var mı, boşta biten yol
     var mı, her `book1_entry_point` ailesine bir şemadan ulaşılıyor mu
  ⑤ Yayılım taşması — figür kutusu sayfa geometrisine sığıyor mu ve
     genişlik iki sınıftan birine oturuyor mu
  ⑥ Ölçek beyanı — kalıp parçası figürü ölçeğini beyan ediyor mu
  ⑦ `A11` eşiği — photo_required işaretli figür sayısı ≤ 6
  ⑧ `A6` eşiği — color_required oranı ≤ %10
  ⑩ OKUR DİLİ — kitabın dili (series.language) ile figürlerin dili aynı mı;
     her belirti ve her aday neden için okura dönük etiket var mı
  ⑨ Sayfa geometrisinin KENDİ tutarlılığı — KDP asgarileri ihlal edilmiş mi,
     sayfa sayısı bandı hâlâ geçerli mi, yazı tipi manifesti doğrulanıyor mu
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
import croquis  # noqa: E402

PHOTO_CAP = 6                # VISUAL_SPEC § 5.4 / DECISIONS K35
COLOR_RATIO_CAP = 0.10       # FORMAT_STRATEGY § 5.3 / DECISIONS K23
CALIBRATED_STATES = {"CALIBRATED", "CALIBRATED_DIGITAL_RENDER"}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def check(book_id: str, findings: list, stats: dict):
    ffile = paths.book_figures(book_id)
    if not ffile.exists():
        gate = paths.read_book_gate(book_id)
        if paths.gate_at_least(gate, "phase2-visual", paths.BOOK_GATE_ORDER):
            findings.append(f"{book_id}: kapı {gate} ama 03_VISUAL/figures.json YOK — "
                            f"Faz 2 çıktısı olmadan bu kapı geçilemez.")
        return

    data = load(ffile)
    figs = data.get("figures", [])
    meta = data.get("figure_meta", {})
    tokens = load(paths.VISUAL_TOKENS)
    geom = load(paths.PAGE_GEOMETRY)
    signs = load(paths.FIT_SIGNS)["signs"]
    measures = load(paths.MEASUREMENTS)["measurements"]
    families = load(paths.ADJUSTMENT_FAMILIES)["families"]

    token_ids = {t["token_id"] for t in tokens["tokens"]}
    sym_ids = {s["symptom_id"] for s in signs}
    m_ids = {m["measurement_id"] for m in measures}
    af_ids = {f["adjustment_family_id"] for f in families}
    entry_afs = {f["adjustment_family_id"] for f in families if f.get("book1_entry_point")}

    # ① token bütünlüğü + kalibrasyon durumu
    gate = paths.read_book_gate(book_id)
    if paths.gate_at_least(gate, "phase2-visual", paths.BOOK_GATE_ORDER):
        if tokens.get("status") not in CALIBRATED_STATES:
            findings.append(
                f"{book_id}: kapı {gate} ama visual_language_tokens.status="
                f"{tokens.get('status')!r} — Faz 2'nin DoD'si kalibrasyondur.")
        if not paths.CALIBRATION_REPORT.exists():
            findings.append("kalibrasyon raporu YOK — 03_VISUAL/calibration_report.json")
    for f in figs:
        for tk in f.get("notation_tokens", []):
            if tk not in token_ids:
                findings.append(f"{f['figure_id']}: tanımsız token {tk}")
        if not f.get("notation_tokens"):
            findings.append(f"{f['figure_id']}: notation_tokens BOŞ — "
                            f"hiçbir token kullanmayan bir figür bir iddia taşıyamaz.")

    # ② figür ↔ kayıt bağı
    for fid, mx in meta.items():
        if "symptom_ref" in mx and mx["symptom_ref"] not in sym_ids:
            findings.append(f"{fid}: symptom_ref={mx['symptom_ref']} tanımlı bir belirti DEĞİL.")
        if "measurement_ref" in mx and mx["measurement_ref"] not in m_ids:
            findings.append(f"{fid}: measurement_ref={mx['measurement_ref']} tanımlı bir ölçü DEĞİL.")

    # ③ gerekçesiz elle çizim
    for f in figs:
        if f.get("deterministic") is False and not f.get("manual_reason"):
            findings.append(f"{f['figure_id']}: deterministic=false ama manual_reason YOK.")

    # ④ akış şeması kapsaması
    charted = {meta[f["figure_id"]].get("symptom_ref")
               for f in figs if f["figure_type"] == "flowchart"
               and f["figure_id"] in meta}
    missing = sorted(sym_ids - charted)
    if missing:
        findings.append(f"{book_id}: {len(missing)} belirtinin akış şeması YOK — "
                        f"örn. {', '.join(missing[:5])}")
    reached: set = set()
    for f in figs:
        if f["figure_type"] != "flowchart":
            continue
        mx = meta.get(f["figure_id"], {})
        for kind, ref in mx.get("terminals", []):
            if kind == "handoff":
                if ref not in af_ids:
                    findings.append(f"{f['figure_id']}: devir düğümü {ref} tanımlı bir aile DEĞİL.")
                reached.add(ref)
            elif not ref:
                findings.append(f"{f['figure_id']}: BOŞTA BİTEN YOL — "
                                f"eleme kalemi metinsiz.")
    unreached = sorted(entry_afs - reached)
    if unreached:
        findings.append(f"{book_id}: Kitap 1 giriş noktası olan {len(unreached)} düzeltme "
                        f"ailesine hiçbir akış şemasından ULAŞILAMIYOR: {', '.join(unreached)}")

    # ⑤ yayılım taşması + genişlik sınıfı
    fa = geom["figure_area"]
    max_w, max_h = float(fa["max_width_pt"]), float(fa["max_height_pt"])
    min_w = float(fa["min_width_pt"])
    classes = fa["width_class"]
    over = []
    for fid, mx in meta.items():
        w, h = mx.get("width_pt"), mx.get("height_pt")
        if w is None or h is None:
            continue
        if w > max_w + 0.01 or h > max_h + 0.01:
            over.append(f"{fid} ({w}×{h} pt > {max_w}×{max_h})")
        if w < min_w - 0.01 and mx.get("width_pt"):
            stats.setdefault("below_min_width", []).append(fid)
    if over:
        findings.append(f"{book_id}: {len(over)} figür sayfa figür alanına SIĞMIYOR — "
                        f"{'; '.join(over[:4])}")
    stats["width_classes"] = {
        "text_column_or_less": sum(1 for mx in meta.values()
                                   if mx.get("width_pt", 0) <= classes["text_column_pt"] + 0.01),
        "full_measure": sum(1 for mx in meta.values()
                            if classes["text_column_pt"] + 0.01 < mx.get("width_pt", 0)
                            <= classes["full_measure_pt"] + 0.01),
    }

    # ⑥ ölçek beyanı
    for f in figs:
        if f["figure_type"] == "pattern_piece":
            mx = meta.get(f["figure_id"], {})
            if not mx.get("piece"):
                findings.append(f"{f['figure_id']}: kalıp parçası figürü kayıtta "
                                f"tanımlanmamış.")

    # ⑦b okura dönük / iç figür ayrımı — iç araçlar kitap sayısına girmez
    internal_ids = {fid for fid, mx in meta.items() if mx.get("internal")}
    stats["internal_figures"] = len(internal_ids)
    stats["reader_figures"] = len(figs) - len(internal_ids)

    # ⑦ A11 eşiği
    photos = [f["figure_id"] for f in figs if f.get("photo_required")]
    stats["photo_required"] = len(photos)
    if len(photos) > PHOTO_CAP:
        findings.append(f"{book_id}: photo_required işaretli {len(photos)} figür — "
                        f"azami {PHOTO_CAP} (A11 / DECISIONS K35). Aşım A11'i YENİDEN AÇAR.")

    # ⑧ A6 eşiği
    colored = [f["figure_id"] for f in figs if f.get("color_required")]
    ratio = len(colored) / len(figs) if figs else 0.0
    stats["color_required"] = len(colored)
    stats["color_ratio"] = round(ratio, 4)
    if ratio > COLOR_RATIO_CAP:
        findings.append(f"{book_id}: color_required oranı %{ratio*100:.1f} — "
                        f"eşik %{COLOR_RATIO_CAP*100:.0f} (A6 / DECISIONS K23). "
                        f"Aşım RENK KARARINI YENİDEN AÇAR.")

    # ⑩ okur dili — figürler okurun dilinde mi
    cfg0 = load(paths.SERIES_CONFIG)
    lang = cfg0["series"]["language"]
    doc_lang = cfg0["series"].get("documentLanguage")
    if lang != doc_lang:
        if not paths.LABELS_EN.exists():
            findings.append(
                f"OKUR DİLİ: kitap dili {lang!r}, belge dili {doc_lang!r} ve okura "
                f"dönük etiket katmanı YOK — figürler proje belge dilinde üretilir "
                f"ve okura gösterilemez (02_TAXONOMY/public/labels_en.json).")
        else:
            lab = load(paths.LABELS_EN)
            if lab.get("language") != lang:
                findings.append(f"OKUR DİLİ: labels_en.json dili {lab.get('language')!r}, "
                                f"kitap dili {lang!r} — uyuşmuyor.")
            miss_sign, miss_cause = [], []
            for s in signs:
                sid = s["symptom_id"]
                e = lab["signs"].get(sid)
                if not e or not e.get("observation"):
                    miss_sign.append(sid); continue
                if len(e.get("causes", [])) != len(s["candidate_causes"]):
                    miss_cause.append(f"{sid} ({len(e.get('causes', []))}/"
                                      f"{len(s['candidate_causes'])})")
                    continue
                for i, c in enumerate(e["causes"]):
                    if not c.get("evidence") or not c.get("cause"):
                        miss_cause.append(f"{sid}#{i+1}")
            if miss_sign:
                findings.append(f"OKUR DİLİ: {len(miss_sign)} belirtinin okura dönük "
                                f"etiketi YOK — {', '.join(miss_sign[:5])}")
            if miss_cause:
                findings.append(f"OKUR DİLİ: {len(miss_cause)} aday nedenin okura dönük "
                                f"etiketi eksik — {', '.join(miss_cause[:5])}")
            for z in {s["zone"] for s in signs}:
                if z not in lab.get("zones", {}):
                    findings.append(f"OKUR DİLİ: '{z}' bölgesinin okura dönük adı YOK.")
            if lab.get("does_not_change_verification_status") is not True:
                findings.append("OKUR DİLİ: labels_en.json, doğrulama durumunu "
                                "DEĞİŞTİRMEDİĞİNİ açıkça beyan etmiyor — bir çeviri "
                                "katmanı bir doğrulama değildir.")
        stats["reader_language"] = lang

    # ⑨ sayfa geometrisi tutarlılığı
    pm = geom["platform_minimums"]
    band = pm["page_count_band_used"]
    gutter_min = pm["gutter_by_page_count_in"][band]
    if geom["margins"]["gutter_in"] < gutter_min:
        findings.append(f"SAYFA GEOMETRİSİ: cilt payı {geom['margins']['gutter_in']} in, "
                        f"KDP asgarisi {gutter_min} in ({band} sayfa) — DOSYA REDDEDİLİR.")
    outside_min = pm["outside_margin_with_bleed_in"] if geom["trim"]["bleed"] \
        else pm["outside_margin_no_bleed_in"]
    for edge in ("outside_in", "top_in", "bottom_in"):
        if geom["margins"][edge] < outside_min:
            findings.append(f"SAYFA GEOMETRİSİ: {edge}={geom['margins'][edge]} in, "
                            f"KDP asgarisi {outside_min} in — DOSYA REDDEDİLİR.")
    cfg = load(paths.SERIES_CONFIG)
    target = next((b["pageTargetProvisional"] for b in cfg["books"] if b["id"] == book_id), None)
    if target:
        lo, hi = band.split("-")
        if target[1] > int(hi):
            findings.append(f"SAYFA GEOMETRİSİ: {book_id} sayfa hedefi {target} bandın "
                            f"({band}) DIŞINA taşıyor — cilt payı yeniden hesaplanmalı.")
        del lo

    # yazı tipi manifesti
    if paths.FONTS_MANIFEST.exists():
        man = load(paths.FONTS_MANIFEST)
        missing_lic = [f["license_file"] for f in man["families"].values()
                       if not (paths.VISUAL_FONTS / f["license_file"]).exists()]
        if missing_lic:
            findings.append(f"YAZI TİPİ LİSANSI eksik: {', '.join(missing_lic)} — "
                            f"TYPOGRAPHY_STANDARD § 1.1 madde 3.")

    # ⑪ VÜCUT VARYANTI — çelişmeli inceleme B-05
    #
    # Kitap uyum sorunlarının vücut çeşitliliğinden doğduğunu söyler.
    # Bunu TEK bir silüetle anlatmak, kitabın kendi tezini görsel olarak
    # yalanlar. Bu denetim iki şeyi ayrı ayrı arar:
    #   (a) belirti figürleri varyant kaydı TAŞIYOR mu — kayıtsız bir
    #       varyant ölçülemez;
    #   (b) en az iki farklı varyant GERÇEKTEN kullanılıyor mu.
    # (b) olmadan (a) bir alan doldurma egzersizidir.
    sign_meta = [m for fid, m in meta.items() if "body_variant" in m]
    sign_figs = [f for f in figs if f["figure_type"] == "fit_sign_on_figure"]
    if sign_figs:
        if len(sign_meta) != len(sign_figs):
            findings.append(f"{book_id}: {len(sign_figs) - len(sign_meta)} belirti figürü "
                            f"body_variant KAYDI taşımıyor — B-05 ölçülemez hâle gelir.")
        used = {m["body_variant"] for m in sign_meta}
        unknown = used - set(croquis.VARIANTS)
        if unknown:
            findings.append(f"{book_id}: tanımsız kroki varyantı: {sorted(unknown)}")
        if len(used) < 2:
            findings.append(f"{book_id}: belirti figürlerinin TAMAMI tek bir vücut "
                            f"varyantında ({sorted(used)}) — çelişmeli inceleme B-05 "
                            f"(YÜKSEK) yeniden açılır.")
        stats["body_variants"] = {v: sum(1 for m in sign_meta if m["body_variant"] == v)
                                  for v in sorted(used)}

    stats["figures"] = len(figs)
    stats["deterministic"] = sum(1 for f in figs if f.get("deterministic"))
    stats["deterministic_ratio"] = round(stats["deterministic"] / len(figs), 4) if figs else 0.0
    stats["flowcharts"] = sum(1 for f in figs if f["figure_type"] == "flowchart")
    stats["af_reached_from_flowcharts"] = len(reached)
    stats["af_entry_points"] = len(entry_afs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None)
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    findings: list[str] = []
    stats: dict = {}
    books = [args.book] if args.book else list(paths.BOOK_DIRS)
    per_book = {}
    for b in books:
        s: dict = {}
        check(b, findings, s)
        if s:
            per_book[b] = s

    print("▸ qa_visual.py — görsel sistem kapısı")
    for b, s in per_book.items():
        print(f"  {b}: {s.get('figures', 0)} figür · deterministik "
              f"{s.get('deterministic', 0)} (%{s.get('deterministic_ratio', 0)*100:.1f}) · "
              f"akış şeması {s.get('flowcharts', 0)} · "
              f"ulaşılan giriş ailesi {s.get('af_reached_from_flowcharts', 0)}/"
              f"{s.get('af_entry_points', 0)} · foto {s.get('photo_required', 0)}/{PHOTO_CAP} · "
              f"renk %{s.get('color_ratio', 0)*100:.1f}/%{COLOR_RATIO_CAP*100:.0f}")
    if findings:
        print(f"  ✗ {len(findings)} bulgu:")
        for f in findings:
            print(f"    - {f}")
    else:
        print("  ✓ 0 bulgu")
    if args.json:
        out = Path(args.json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"findings": findings, "stats": per_book,
                                   "passed": not findings}, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
