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
run 06_BUILD/fetch_fonts.py --verify
run 07_TESTS/selftest.py
echo "──────────────────────────────────────────────────────────────"
if [ "$FAIL" -eq 0 ]; then echo "✓ BÜTÜN KAPILAR GEÇTİ"; else echo "✗ EN AZ BİR KAPI BAŞARISIZ"; fi
exit "$FAIL"
