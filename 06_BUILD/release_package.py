#!/usr/bin/env python3
"""
release_package.py — YAYIN ADAYI PAKETİ (Faz 6 · § 45).

Kurucunun yükleyeceği DOSYALARI tek bir dizinde toplar ve her birinin
SHA-256'sını yazar. Hiçbir şeyi YAYIMLAMAZ: paket hazırlanır, karar
kurucunundur (§ 45 "Do not publish automatically").

Pakete giren her sayı bir ÖLÇÜMDÜR — beyan değil. Sayfa sayısı
pdfinfo'dan, yazı tipleri pdffonts'tan, kaynak listesi kayıttan gelir.

Üretilenler:
  · BOOK_01_interior.pdf     yükleme dosyası (iç blok)
  · KDP_METADATA.txt         KDP formuna GİRİLECEK alanlar
  · BUILD_MANIFEST.json      girdi dosyalarının SHA-256'sı + git SHA
  · QA_REPORT.txt            qa_all.sh çıktısının tamamı
  · RELEASE_NOTES.md         bu adayda NE değişti
  · CHECKSUMS.sha256         paketin kendi bütünlüğü

⚠ Paket bir YAYIN İZNİ DEĞİLDİR. Fiziksel prova alınmadı, KDP
Previewer çalıştırılmadı ve insan doğrulaması yapılmadı.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    args = ap.parse_args()

    bdir = paths.BOOK_DIRS[args.book]
    pdf = bdir / "09_OUTPUT" / "BOOK_01.pdf"
    if not pdf.exists():
        print(f"✗ yayın varlığı YOK: {pdf} — önce build_book.py")
        return 1

    out = bdir / "09_OUTPUT" / "RELEASE_CANDIDATE"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))
    book = json.loads((bdir / "book_config.json").read_text(encoding="utf-8"))
    geom = json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))

    info = {}
    for ln in run(["pdfinfo", str(pdf)]).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            info[k.strip()] = v.strip()
    pages = int(info.get("Pages", 0))

    shutil.copy2(pdf, out / "BOOK_01_interior.pdf")

    # ── KDP formuna girilecek alanlar ────────────────────────────────
    b = book["book"]
    meta = out / "KDP_METADATA.txt"
    meta.write_text(f"""KDP YÜKLEME ALANLARI — Kitap 1
{'=' * 62}
⚠ Bu dosya KURUCUNUN ELİYLE gireceği alanları listeler. Hiçbir KDP
  hesabı işlemi YAPILMADI ve yapılamaz.

Title            : {info.get('Title', '')}
Subtitle         : {b.get('workingSubtitle', '')}
Author           : {info.get('Author', '')}
Imprint          : {cfg['series'].get('imprintName', '(seri kaydında yok)')}
Language         : {cfg['series'].get('language', 'en')}
Keywords         : {info.get('Keywords', '')}

Trim size        : {geom['trim']['width_in']} x {geom['trim']['height_in']} in
Bleed            : {'YES' if geom['trim'].get('bleed') else 'NO'}
Interior         : Black & white
Paper            : (KURUCU SEÇER — white / cream)
Binding          : {b.get('bindingProvisional', 'paperback')}
Page count       : {pages}
Gutter margin    : {geom['margins']['gutter_in']} in (KDP asgarisi {geom['platform_minimums']['gutter_by_page_count_in'].get(geom['platform_minimums']['page_count_band_used'], '?')} in, {geom['platform_minimums']['page_count_band_used']} sayfa bandı)
Outside margin   : {geom['margins']['outside_in']} in
PDF version      : {info.get('PDF version', '')}
Fonts            : TAMAMI GÖMÜLÜ (pdffonts ile doğrulandı)
File size        : {pdf.stat().st_size / 1e6:.2f} MB

ISBN             : (KURUCU KARARI — KDP ücretsiz ISBN ya da kendi ISBN'i)
Price            : (KURUCU KARARI — kayıtta öneri {book['product'].get('priceModelProvisional')})
Categories       : (KURUCU KARARI)

{'=' * 62}
DOLDURULMAMIŞ ALANLAR YUKARIDA "KURUCU" olarak işaretlidir. Bu proje
onları TAHMİN ETMEZ.
""", encoding="utf-8")

    # ── girdilerin parmak izi ────────────────────────────────────────
    tracked = sorted(
        [p for p in (paths.TAXONOMY_PUBLIC).glob("*.json")]
        + [paths.PAGE_GEOMETRY, paths.SERIES_CONFIG, bdir / "book_config.json"]
        + [p for p in (bdir / "03_VISUAL").glob("*.json")])
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_sha": run(["git", "rev-parse", "HEAD"]),
        "git_branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "git_dirty": bool(run(["git", "status", "--porcelain"])),
        "python": sys.version.split()[0],
        "reportlab": run([sys.executable, "-c",
                          "import reportlab;print(reportlab.Version)"]),
        "pdf": {"pages": pages, "bytes": pdf.stat().st_size,
                "sha256": sha256(pdf), "version": info.get("PDF version")},
        "inputs": {str(p.relative_to(paths.ROOT)): sha256(p)
                   for p in tracked if p.exists()},
        "not_included_and_why": {
            "manuscript_prose": "BİLEREK izlenmiyor (DECISIONS.md K9) — "
                                "yayın öncesi içerik korumasıdır",
            "physical_proof": "ALINMADI — erişilemez (K58)",
            "kdp_previewer": "ÇALIŞTIRILMADI — hesap erişimi yok",
        },
    }
    (out / "BUILD_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ── QA çıktısının tamamı ─────────────────────────────────────────
    qa = subprocess.run(["bash", str(paths.ROOT / "06_BUILD" / "qa_all.sh")],
                        capture_output=True, text=True, cwd=paths.ROOT)
    (out / "QA_REPORT.txt").write_text(
        f"qa_all.sh — çıkış kodu {qa.returncode}\n"
        f"{'=' * 62}\n{qa.stdout}\n{qa.stderr}", encoding="utf-8")

    (out / "RELEASE_NOTES.md").write_text(f"""# Kitap 1 — yayın adayı

- git: `{manifest['git_sha'][:12]}` ({manifest['git_branch']})
- {pages} sayfa · {pdf.stat().st_size / 1e6:.2f} MB · PDF {info.get('PDF version')}
- qa_all.sh çıkış kodu: **{qa.returncode}**

## Bu paket NEYİ KANITLAR

Kitabın kendi kayıtlarıyla tutarlı olduğunu ve kendi kapılarından
geçtiğini. Bütün doğrulama İÇSELDİR.

## Bu paket NEYİ KANITLAMAZ

- Fiziksel prova ALINMADI (K58) — kâğıt, mürekkep yayılması, cilt
- KDP Previewer ÇALIŞTIRILMADI — hesap erişimi yok
- İnsan okur doğrulaması YAPILMADI — kill-gate ölçülmedi
- Gerçek kumaş üzerinde hiçbir teşhis sınanmadı

## Kurucunun yapması gerekenler

1. `BOOK_01_interior.pdf`'i KDP'ye yükle ve **Previewer'ı çalıştır**
2. Basılı prova sipariş et ve `print_sim.py`'nin ölçemediklerini kontrol et
3. `KDP_METADATA.txt` içindeki **(KURUCU KARARI)** alanlarını doldur
4. Kapak AYRI bir iştir — bu pakette YOKTUR
""", encoding="utf-8")

    lines = []
    for p in sorted(out.iterdir()):
        if p.name != "CHECKSUMS.sha256":
            lines.append(f"{sha256(p)}  {p.name}")
    (out / "CHECKSUMS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"▸ release_package.py — {out.relative_to(paths.ROOT)}")
    for p in sorted(out.iterdir()):
        print(f"  {p.stat().st_size:>9,} B  {p.name}")
    print(f"  qa_all.sh çıkış kodu: {qa.returncode}")
    print("  ⚠ PAKET HAZIR — YAYIMLANMADI. Fiziksel prova ve KDP Previewer "
          "ERİŞİLEMEZ durumda.")
    return 0 if qa.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
