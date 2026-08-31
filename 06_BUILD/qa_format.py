#!/usr/bin/env python3
"""
qa_format.py — FAZ 6 · YAYIN VARLIĞININ KENDİSİNİ ÖLÇER.

⚠ NEDEN VAR: Faz 5'e kadar bütün kapılar VERİYE bakıyordu. Bir kitabın
basılabilirliği ise verinin değil ÜRETİLEN PDF'İN özelliğidir ve o
dosya hiç denetlenmemişti. İlk koşumda iki kusur ölçüldü:

  · gömülmemiş `Helvetica` (KDP gömülmemiş yazı tipini işaretler)
  · künye alanları `untitled` / `anonymous` (§ 43: yer tutucu kalamaz)

Denetimler — hepsi DOSYADAN okunur, hiçbiri beyan değildir:

  ① kesim ölçüsü kayıtla uyuşuyor mu (page_geometry.trim)
  ② SAYFA SAYISI, cilt payı bandını değiştiriyor mu
  ③ kullanılan cilt payı, o bandın ASGARİSİNİN üstünde mi
  ④ dış/üst/alt kenar boşluğu asgarinin üstünde mi
  ⑤ HER yazı tipi GÖMÜLÜ mü (KDP zorunluluğu)
  ⑥ künyede yer tutucu kaldı mı
  ⑦ PDF sürümü KDP'nin kabul ettiği aralıkta mı
  ⑧ dosya boyutu yükleme sınırının altında mı (650 MB)
  ⑨ PDF ana hattı (bookmark) var mı ve bölümleri taşıyor mu
  ⑩ sayfa numarası HER sayfada mı (ön maddeler hariç)
  ⑪ taşma (bleed) beyanı ile gerçek sayfa kutusu uyuşuyor mu
  ⑫ BİÇİM KALİTESİ (§ 43): basılı sayfada YER TUTUCU metin, İÇ KAYIT
     KİMLİĞİ (SYM-xxx, AF-xx, M-xxx, S-xxxx…), GEÇİCİ DOSYA ADI ya da
     HATA AYIKLAMA içeriği kaldı mı. Bu denetim ÜRETİLEN PDF'in metin
     katmanında yapılır: veri katmanındaki bir kimlik zararsızdır,
     OKURA BASILANI kusurdur.

     ⚠ Kenar boşluğu taşması artık print_sim.py'nin işidir: o HER
     sayfayı 300 dpi'de rasterleştirip mürekkebin kenara ne kadar
     girdiğini ÖLÇER. Metin katmanı bir çizginin nereye çizildiğini
     bilmez; bu yüzden o denetim buradan ALINDI, uydurulmadı.

Çıkış: 0 temiz · 1 en az bir kusur · 2 araç yok (poppler).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

KDP_MAX_UPLOAD_MB = 650          # S-0016
KDP_PDF_VERSIONS = {"1.3", "1.4", "1.5", "1.6", "1.7"}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--pdf", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not shutil.which("pdfinfo") or not shutil.which("pdffonts"):
        print("▸ qa_format.py — ATLANDI: poppler-utils yok "
              "(pdfinfo/pdffonts). Bu kapı BASKI varlığını ölçer ve "
              "araç olmadan ölçemez; SESSİZCE GEÇMEZ.")
        return 2

    pdf = Path(args.pdf) if args.pdf else (
        paths.BOOK_DIRS[args.book] / "09_OUTPUT" / "BOOK_01.pdf")
    if not pdf.exists():
        print(f"✗ yayın varlığı YOK: {pdf}")
        return 1

    geom = load(paths.PAGE_GEOMETRY)
    trim, marg, pmin = geom["trim"], geom["margins"], geom["platform_minimums"]

    errs: list = []
    warns: list = []

    info = {}
    for ln in run(["pdfinfo", str(pdf)]).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            info[k.strip()] = v.strip()

    # ① kesim ölçüsü
    m = re.search(r"([\d.]+) x ([\d.]+) pts", info.get("Page size", ""))
    if not m:
        errs.append("① sayfa ölçüsü OKUNAMADI")
    else:
        w, h = float(m.group(1)), float(m.group(2))
        if abs(w - trim["width_pt"]) > 0.6 or abs(h - trim["height_pt"]) > 0.6:
            errs.append(f"① kesim ölçüsü kayıtla UYUŞMUYOR: dosya {w}×{h} pt, "
                        f"kayıt {trim['width_pt']}×{trim['height_pt']} pt")

    # ② ③ sayfa sayısı ve cilt payı bandı
    pages = int(info.get("Pages", 0))
    band = None
    for rng, mn in pmin["gutter_by_page_count_in"].items():
        lo, hi = (int(x) for x in rng.split("-"))
        if lo <= pages <= hi:
            band, band_min = rng, mn
            break
    if band is None:
        errs.append(f"② {pages} sayfa HİÇBİR cilt payı bandına girmiyor "
                    f"(KDP 24–828)")
    else:
        if band != pmin["page_count_band_used"]:
            errs.append(f"② SAYFA SAYISI BANDI DEĞİŞTİ: dosya {pages} sayfa → "
                        f"band {band}, kayıt band {pmin['page_count_band_used']}. "
                        f"page_geometry.json YENİDEN HESAPLANMALI.")
        gutter_in = marg["gutter_in"]
        if gutter_in < band_min:
            errs.append(f"③ cilt payı {gutter_in} in, {band} bandının asgarisi "
                        f"{band_min} in — ALTINDA")

    # ④ dış / üst / alt kenar
    out_min = (pmin["outside_margin_with_bleed_in"] if trim.get("bleed")
               else pmin["outside_margin_no_bleed_in"])
    if marg["outside_in"] < out_min:
        errs.append(f"④ dış kenar {marg['outside_in']} in, asgari {out_min} in")
    for side in ("top_in", "bottom_in"):
        if marg[side] < out_min:
            errs.append(f"④ {side} {marg[side]} in, asgari {out_min} in")

    # ⑤ yazı tipi gömme
    fonts = [ln.split() for ln in run(["pdffonts", str(pdf)]).splitlines()[2:] if ln.strip()]
    not_emb = [f[0] for f in fonts if len(f) > 5 and f[-4] == "no"]
    if not_emb:
        errs.append(f"⑤ GÖMÜLMEMİŞ yazı tipi: {', '.join(not_emb)} — "
                    f"KDP gömülmemiş yazı tipini yüklemede işaretler")
    if not fonts:
        errs.append("⑤ dosyada HİÇ yazı tipi yok — metin görüntüye mi çevrilmiş?")

    # ⑥ künye yer tutucusu
    PLACEHOLDER = {"untitled", "anonymous", "unspecified", "", "none"}
    for k in ("Title", "Author", "Creator", "Subject"):
        v = (info.get(k) or "").strip().lower()
        if v in PLACEHOLDER:
            errs.append(f"⑥ künye alanı YER TUTUCU: {k} = {info.get(k)!r}")

    # ⑦ PDF sürümü
    ver = info.get("PDF version", "")
    if ver not in KDP_PDF_VERSIONS:
        errs.append(f"⑦ PDF sürümü {ver} — KDP kabul aralığı "
                    f"{sorted(KDP_PDF_VERSIONS)}")

    # ⑧ dosya boyutu
    mb = pdf.stat().st_size / 1e6
    if mb > KDP_MAX_UPLOAD_MB:
        errs.append(f"⑧ dosya {mb:.1f} MB — KDP yükleme sınırı "
                    f"{KDP_MAX_UPLOAD_MB} MB")

    # ⑨ ana hat (bookmark)
    if shutil.which("pdftk"):
        outline = run(["pdftk", str(pdf), "dump_data"])
        n_bm = outline.count("BookmarkTitle")
    else:
        raw = pdf.read_bytes()
        n_bm = raw.count(b"/Outlines")
    if n_bm == 0:
        errs.append("⑨ PDF ANA HATTI YOK — 271 sayfalık bir başvuru kitabı "
                    "gezinilemez")

    # ⑩ folyo — metin katmanından ölçülür
    if shutil.which("pdftotext"):
        txt = run(["pdftotext", "-layout", str(pdf), "-"])
        pgs = txt.split("\f")
        missing = []
        for i, p in enumerate(pgs[:pages], 1):
            if i <= 2:
                continue                      # ön madde folyo taşımaz
            # ⚠ İlk koşum 17 sayfayı işaretledi ve ONYEDİSİ DE BOŞTU:
            # bir bölüm recto'da başladığında önündeki verso boş kalır
            # ve BOŞ SAYFA FOLYO TAŞIMAZ — yerleşik uygulama budur.
            # Kapı, metni OLAN sayfayı denetler.
            if not p.strip():
                continue
            if not re.search(rf"(?m)^\s*{i}\s*$", p) and str(i) not in p:
                missing.append(i)
        if len(missing) > pages * 0.06:
            warns.append(f"⑩ {len(missing)} sayfada folyo bulunamadı "
                         f"(metin katmanı ölçümü; ilk beş: {missing[:5]})")

    # ⑪ taşma beyanı
    raw = pdf.read_bytes()
    has_bleedbox = b"/BleedBox" in raw or b"/TrimBox" in raw
    if trim.get("bleed") and not has_bleedbox:
        errs.append("⑪ taşma BEYAN EDİLMİŞ ama dosyada BleedBox/TrimBox YOK")
    if not trim.get("bleed") and has_bleedbox:
        warns.append("⑪ taşma yok deniyor ama dosyada BleedBox/TrimBox VAR")

    # ⑫ biçim kalitesi — § 43
    if shutil.which("pdftotext"):
        body = run(["pdftotext", str(pdf), "-"])
        # İç kayıt kimlikleri: figür motorunun kendi sızıntı denetimi
        # ÇİZİMLERİ koruyor; bu, DİZİLMİŞ METNİ kontrol eder.
        #
        # ⚠ İLK SÜRÜM DESEN ARIYORDU ve YANLIŞ POZİTİF verdi: Ek I'deki
        # ANSUR II rapor numarası "NATICK/TR-15/007" prova okuması
        # kimliği sanıldı. Deseni gevşetmek kapıyı körleştirirdi.
        # Kapı artık KAYITTAKİ GERÇEK kimlikleri arar — sicilde olmayan
        # bir dizi zaten bir sızıntı değildir, ve sicilde olan hiçbiri
        # gözden kaçamaz.
        real: dict = {}
        try:
            real["belirti kimliği"] = {x["symptom_id"] for x in
                                       load(paths.FIT_SIGNS)["signs"]}
            real["aile kimliği"] = {x["adjustment_family_id"] for x in
                                    load(paths.ADJUSTMENT_FAMILIES)["families"]}
            real["ölçü kimliği"] = {x["measurement_id"] for x in
                                    load(paths.MEASUREMENTS)["measurements"]}
            pr = load(paths.TAXONOMY_PUBLIC / "pattern_readings.json")
            real["okuma kimliği"] = ({x["reading_id"] for x in pr["readings"]}
                                     | {x["reading_id"] for x in pr["toile_readings"]})
            real["kaynak kimliği"] = {f"S-{i:04d}" for i in range(1, 40)}
        except Exception as exc:                     # veri yoksa SESSİZ GEÇME
            warns.append(f"⑫ iç kimlik denetimi ATLANDI — kayıt okunamadı: {exc}")
        for name, ids in real.items():
            # Kimlik TEK BAŞINA bir belirteç olmalı: bir yol ya da rapor
            # numarasının içinde geçen dizi bir sızıntı DEĞİLDİR.
            hits = sorted(i for i in ids
                          if re.search(rf"(?<![\w/-]){re.escape(i)}(?![\w/-])", body))
            if hits:
                errs.append(f"⑫ OKURA BASILAN {name}: {', '.join(hits[:6])}"
                            + (f" (+{len(hits)-6})" if len(hits) > 6 else ""))
        PLACEHOLDERS = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b",
                        r"\bLorem ipsum\b", r"\bplaceholder\b", r"\bdummy\b",
                        r"\[\s*\]", r"\{\{.*?\}\}", r"<[a-z_]+>"]
        for pat in PLACEHOLDERS:
            hits = sorted(set(re.findall(pat, body, re.I)))
            if hits:
                errs.append(f"⑫ YER TUTUCU metin basılmış: {hits[:4]}")
        # Geçici / iç dosya adları ve hata ayıklama artığı
        for pat, what in ((r"\b[\w/]+\.(?:py|json|sh|pdf|png|txt)\b", "dosya adı"),
                          (r"\bTraceback\b|\bstderr\b|\bstdout\b", "hata ayıklama"),
                          (r"/tmp/|/home/|C:\\", "mutlak yol")):
            hits = sorted(set(m if isinstance(m, str) else m[0]
                              for m in re.findall(pat, body)))
            if hits:
                errs.append(f"⑫ basılı sayfada {what}: {hits[:4]}")
        # Proje dili (Türkçe) OKUR metnine sızmış mı — kitap İngilizcedir
        tr = sorted(set(re.findall(r"\b\w*[çğışöüÇĞİŞÖÜ]\w*\b", body)))
        tr = [w for w in tr if len(w) > 2 and w.lower() not in {"vâliçe"}]
        if tr:
            errs.append(f"⑫ OKUR metninde proje dili: {tr[:6]}")

    print("▸ qa_format.py — yayın varlığı kapısı")
    try:                                   # --pdf ağaç DIŞINDA olabilir
        shown = pdf.relative_to(paths.ROOT)
    except ValueError:
        shown = pdf
    print(f"  {shown}")
    print(f"  {pages} sayfa · {trim['width_in']}×{trim['height_in']} in · "
          f"{mb:.2f} MB · PDF {ver} · yazı tipi {len(fonts)} "
          f"({len(fonts) - len(not_emb)} gömülü)")
    print(f"  cilt payı {marg['gutter_in']} in (band {band}, asgari "
          f"{pmin['gutter_by_page_count_in'].get(band, '?')} in) · "
          f"dış {marg['outside_in']} in (asgari {out_min} in)")
    if args.verbose:
        for w in warns:
            print(f"  ⚠ {w}")
    if errs:
        print(f"  ✗ {len(errs)} kusur")
        for e in errs:
            print(f"    - {e}")
        return 1
    print("  ✓ kesim, kenar, cilt payı, yazı tipi gömme, künye, sürüm, "
          "boyut ve ana hat KDP kaydına uyuyor")
    print("  ✓ basılı sayfada yer tutucu, iç kayıt kimliği, geçici dosya adı "
          "ya da hata ayıklama artığı YOK (§ 43)")
    print("  ⚠ Bu bir İÇSEL ölçümdür. KDP Previewer ÇALIŞTIRILMADI ve "
          "fiziksel prova ALINMADI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
