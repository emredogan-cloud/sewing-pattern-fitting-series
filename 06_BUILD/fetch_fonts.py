#!/usr/bin/env python3
"""
fetch_fonts.py — yazı tiplerini YENİDEN EDİNİR ve manifestle DOĞRULAR.

Neden bu script var: TTF dosyaları ikili dosyadır ve depoya girmez
(.gitignore § ⑧). Ama Faz 2 kalibrasyonu onlarsız çalışmaz. Bu script
`03_VISUAL/fonts/fonts_manifest.json`'daki arşiv URL'lerinden aynı
dosyaları indirir ve SHA-256 ile doğrular — kalibrasyonun BAŞKA BİR
MAKİNEDE de aynı sonucu vermesi için.

Lisans: her üç aile de SIL Open Font License 1.1'dir ve lisans METİNLERİ
depoda İZLENİR (TYPOGRAPHY_STANDARD.md § 1.1 madde 3).

Kullanım:
  python3 06_BUILD/fetch_fonts.py --verify   # sadece doğrula (ağ yok)
  python3 06_BUILD/fetch_fonts.py            # eksikse indir + doğrula
"""
from __future__ import annotations
import argparse, hashlib, io, json, sys, urllib.request, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

FONTS = paths.VISUAL / "fonts"
MANIFEST = FONTS / "fonts_manifest.json"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="indirme yapma, yalnızca doğrula")
    args = ap.parse_args()

    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing, bad, ok = [], [], 0

    for fam_key, fam in man["families"].items():
        wanted = {Path(f["file"]).name: f for f in fam["files"]}
        for name, rec in wanted.items():
            dst = FONTS / rec["file"]
            if dst.exists() and sha256(dst) == rec["sha256"]:
                ok += 1
                continue
            if dst.exists():
                bad.append(rec["file"])
                continue
            missing.append((fam_key, fam, rec))

    if missing and not args.verify:
        by_fam: dict[str, list] = {}
        for fam_key, fam, rec in missing:
            by_fam.setdefault(fam_key, []).append((fam, rec))
        for fam_key, items in by_fam.items():
            fam = items[0][0]
            print(f"▸ indiriliyor: {fam['family']} — {fam['archive_url']}")
            with urllib.request.urlopen(fam["archive_url"], timeout=180) as r:
                blob = r.read()
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                for _, rec in items:
                    member = fam["archive_member_prefix"] + Path(rec["file"]).name
                    dst = FONTS / rec["file"]
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(z.read(member))
                    got = sha256(dst)
                    if got != rec["sha256"]:
                        bad.append(f"{rec['file']} (SHA-256 uyuşmadı)")
                    else:
                        ok += 1
        missing = []

    print(f"▸ fetch_fonts.py — {ok} dosya doğrulandı")
    for b in bad:
        print(f"  ✗ SHA-256 UYUŞMUYOR: {b}")
    for fam_key, _fam, rec in missing:
        print(f"  ✗ EKSİK: {rec['file']} — `python3 06_BUILD/fetch_fonts.py` çalıştırın")
    if bad or missing:
        return 1
    print("  ✓ bütün yazı tipi dosyaları manifestle uyuşuyor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
