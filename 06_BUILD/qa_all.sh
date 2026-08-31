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
# ── FAZ 6 · § 42 · FİZİKSEL PROVANIN İÇSEL İKAMESİ ────────────────────
# HER sayfayı 300 dpi'de basar, 1-bit eşikler ve kenar boşluğuna giren
# mürekkebi DERİNLİĞİYLE ölçer. Fiziksel prova değildir ve öyle
# olduğunu iddia etmez; provanın yakalayacağı kusurların hesapla
# yakalanabilen kısmını ölçer. 20 sayfada cilt payına giren figür
# taşmasını ve bütün bir sayfayı kaydıran bayat dönüşümü BU buldu.
"$PY" 06_BUILD/print_sim.py --verbose
RC=$?
if [ "$RC" -eq 1 ]; then FAIL=1; fi
if [ "$RC" -eq 2 ]; then echo "⚠ BASKI SİMÜLASYONU ATLANDI — pdftoppm/Pillow yok."; fi
echo "──────────────────────────────────────────────────────────────"
# ── SİCİL TAZELİĞİ ────────────────────────────────────────────────────
# ⚠ CI'da VARDI, BURADA YOKTU ve bu boşluk ÖLÇÜLDÜ: bir ölçünün
# "yardımcı gerekir" bayrağı değişti, figures.json güncellenmedi,
# qa_all.sh YEŞİL verdi ve CI kırmızı yandı. Yerel takım ile CI aynı
# soruyu sormuyorsa yerel yeşil bir şey KANITLAMAZ.
#
# Soru git'e DEĞİL dosyaya sorulur: diskteki sicil, motorun ÜRETTİĞİ
# şeyle aynı mı. (git'e sorulsaydı, commit edilmemiş DOĞRU bir
# değişiklik de "bayat" görünürdü.)
REG=BOOK-01-MEASURE-AND-DIAGNOSE/03_VISUAL/figures.json
BEFORE=$(sha256sum "$REG" | cut -d' ' -f1)
"$PY" 06_BUILD/figure_engine.py --book book-01 >/dev/null
AFTER=$(sha256sum "$REG" | cut -d' ' -f1)
if [ "$BEFORE" != "$AFTER" ]; then
  echo "✗ figür sicili BAYATTI — motor onu DEĞİŞTİRDİ. Yeniden üretildi;"
  echo "  commit edin ve qa_all.sh'i tekrar koşun."
  FAIL=1
else
  echo "▸ figür sicili GÜNCEL (motor yeniden koştu, dosya DEĞİŞMEDİ)"
fi
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
