#!/usr/bin/env bash
# qa_all.sh — bütün kalite kapılarını sırayla çalıştırır.
# Desen: kardeş projelerin qa_all.sh'i. Üçüncü taraf paket GEREKTİRMEZ.
set -u
cd "$(dirname "$0")/.."
PY=python3
FAIL=0
run() {
  echo "──────────────────────────────────────────────────────────────"
  "$PY" "$@" || FAIL=1
}
run 06_BUILD/validate_spec.py --verbose
run 06_BUILD/validate_structure.py --verbose
run 06_BUILD/build_crosswalk.py --check
run 06_BUILD/qa_crosswalk.py --verbose
run 06_BUILD/qa_boundary.py --verbose
run 06_BUILD/qa_claims.py --verbose
run 06_BUILD/qa_terminology.py --verbose
run 06_BUILD/qa_visual.py --verbose
run 06_BUILD/build_claims.py --check
run 06_BUILD/build_claim_map.py --check
run 06_BUILD/qa_verification.py --verbose
run 06_BUILD/qa_manuscript.py --verbose
run 07_TESTS/selftest.py
# ── İÇSEL SİMÜLASYON (K58) ────────────────────────────────────────────
# Dış doğrulama ERİŞİLEMEZ olduğu için fiziksel testin yerine geçen
# İKAME buradadır. Fiziksel testin EŞDEĞERİ DEĞİLDİR ve çıktısı bunu
# her koşumda söyler. Bağımlılıksızdır.
run 07_TESTS/synthetic/graph_audit.py --verbose
run 07_TESTS/synthetic/run_synthetic.py

# ── RENDER KATMANI ────────────────────────────────────────────────────
# Bu iki kapı reportlab/Pillow'a bağlıdır. Sekiz veri kapısı DEĞİL —
# bağımlılık gizlenmedi, AYRILDI (07_TESTS/requirements-render.txt).
# Bağımlılık yoksa çıkış kodu 2'dir ve UYARI sayılır, başarısızlık değil.
echo "──────────────────────────────────────────────────────────────"
"$PY" 06_BUILD/fetch_fonts.py --verify
RC=$?
if [ "$RC" -eq 1 ]; then FAIL=1; fi
echo "──────────────────────────────────────────────────────────────"
"$PY" 06_BUILD/build_book.py
RC=$?
if [ "$RC" -eq 1 ]; then FAIL=1; fi
echo "──────────────────────────────────────────────────────────────"
# ── FAZ 6 · YAYIN VARLIĞI ─────────────────────────────────────────────
# Bu kapı ÜRETİLEN PDF'i ölçer, veriyi değil. build_book.py'den SONRA
# koşmak zorundadır. poppler yoksa çıkış kodu 2'dir ve UYARI sayılır.
"$PY" 06_BUILD/qa_format.py --verbose
RC=$?
if [ "$RC" -eq 1 ]; then FAIL=1; fi
if [ "$RC" -eq 2 ]; then echo "⚠ BASKI KAPISI ATLANDI — poppler-utils yok."; fi
echo "──────────────────────────────────────────────────────────────"
"$PY" 07_TESTS/selftest_visual.py
RC=$?
if [ "$RC" -eq 2 ]; then
  echo "⚠ RENDER KATMANI ATLANDI — bağımlılık yok."
  echo "  pip install -r 07_TESTS/requirements-render.txt"
elif [ "$RC" -ne 0 ]; then
  FAIL=1
fi
echo "──────────────────────────────────────────────────────────────"
if [ "$FAIL" -eq 0 ]; then echo "✓ BÜTÜN KAPILAR GEÇTİ"; else echo "✗ EN AZ BİR KAPI BAŞARISIZ"; fi
exit "$FAIL"
