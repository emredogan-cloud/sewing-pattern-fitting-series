#!/usr/bin/env python3
"""
selftest.py — KAPILARIN KENDİ TESTİ.

Desen: kardeş projelerin `07_TESTS/selftest.py`'si.

Bu, hattın EN ÖNEMLİ testidir. İçerik yokken yeşil kalan bir
doğrulayıcı, kusur geldiğinde de yeşil kalabilir — bu test o riski
kapatır. Her kontrol, KASITLI OLARAK KUSURLU bir kurgu veri üretir ve
ilgili kapının onu GERÇEKTEN yakaladığını kanıtlar.

    "Yakalamayan bir kapı, kapı değildir."

Bu projeye özgü ek yük: seri mimarisi (tek-birincil kuralı, crosswalk
kapsaması, kitap sınırı) ve iddia disiplini (sahte uzman, korunan
"basılı avantaj" iddiası, Türkçe büyük 'İ' kusuru) da burada sınanır.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "06_BUILD"))
import paths            # noqa: E402
import schema_lite      # noqa: E402
import validate_spec    # noqa: E402
import validate_structure  # noqa: E402
import qa_boundary      # noqa: E402
import qa_claims        # noqa: E402
import qa_terminology   # noqa: E402
import build_crosswalk  # noqa: E402
import trfold           # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, condition: bool, detail: str = ""):
    global CHECKS
    CHECKS += 1
    print(f"  {'✓' if condition else '✗'} {name}")
    if not condition:
        FAILURES.append(f"{name} — {detail}")


# ─────────────────────────────────────────────────────────────────────
# ① schema_lite
# ─────────────────────────────────────────────────────────────────────
def test_schema_lite():
    s = {"type": "object", "additionalProperties": False,
         "required": ["a"], "properties": {"a": {"type": "string"}}}
    e = schema_lite.validate({"a": "x", "b": "yasak"}, s)
    check("schema_lite izin listesi dışı alanı yakalıyor",
          any("İZİN LİSTESİNDE" in x for x in e), f"errors={e}")
    e2 = schema_lite.validate({}, s)
    check("schema_lite eksik zorunlu alanı yakalıyor",
          any("zorunlu alan eksik" in x for x in e2), f"errors={e2}")
    e3 = schema_lite.validate({"a": "x"}, {"type": "object", "properties":
         {"a": {"type": ["string", "null"], "pattern": "^AF-[0-9]{2}$"}}})
    check("schema_lite nullable alanda pattern'i string'e uyguluyor",
          any("desenle eşleşmiyor" in x for x in e3), f"errors={e3}")
    e4 = schema_lite.validate({"a": None}, {"type": "object", "properties":
         {"a": {"type": ["string", "null"], "pattern": "^AF-[0-9]{2}$"}}})
    check("schema_lite null değeri pattern'den MUAF tutuyor", e4 == [], f"errors={e4}")


# ─────────────────────────────────────────────────────────────────────
# ② kaynak disiplini
# ─────────────────────────────────────────────────────────────────────
def test_source_authority_consistency():
    for t in ("commercial_competitor_structural", "marketplace_observation",
              "community_reference_non_authoritative"):
        e: list[str] = []
        validate_spec.check_source_type_authority_consistency(
            {"source_type": t, "technical_authority": True}, e, "S-0001")
        check(f"rakip/pazar/topluluk kaynağı otorite olarak İŞARETLENEMEZ ({t})",
              any("ASLA teknik otorite" in x for x in e), f"errors={e}")


def test_source_locator_discipline():
    e: list[str] = []
    validate_spec.check_source_locator_discipline(
        {"verification_level": "not_yet_acquired", "locator": "s. 142"}, e, "S-0002")
    check("görülmemiş kaynağın locator'ı YAKALANIYOR",
          any("UYDURULAMAZ" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_source_locator_discipline(
        {"verification_level": "fulltext", "locator": "s. 142"}, e2, "S-0003")
    check("görülmüş kaynağın locator'ı serbest", e2 == [], f"errors={e2}")


def test_source_authority_required():
    e: list[str] = []
    validate_spec.check_source_authority(
        {"source_refs": ["S-0001"]}, {"S-0001": False}, e, "SYM-001", "symptom")
    check("yalnızca otoritesiz kaynağa dayanan teknik iddia YAKALANIYOR",
          any("GEÇERSİZDİR" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_source_authority(
        {"source_refs": ["S-9999"]}, {"S-0001": True}, e2, "SYM-002", "symptom")
    check("kayıtsız kaynak referansı YAKALANIYOR",
          any("kayıtsız kaynak" in x for x in e2), f"errors={e2}")


def test_verification_evidence():
    e: list[str] = []
    validate_spec.check_verification_evidence(
        {"verification_status": "technical_reference_verified", "source_refs": ["S-0001"]},
        {"S-0001": "secondary_citation"}, e, "AF-01")
    check("'technical_reference_verified' kanıtsız İDDİA EDİLEMİYOR",
          any("kanıtsız iddia edilemez" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_verification_evidence(
        {"verification_status": "physically_validated", "source_refs": [],
         "validation_record_ref": None}, {}, e2, "SYM-016")
    check("'physically_validated' VAL kaydı olmadan İDDİA EDİLEMİYOR",
          any("validation_record_ref YOK" in x for x in e2), f"errors={e2}")
    e3: list[str] = []
    validate_spec.check_verification_evidence(
        {"verification_status": "agent_drafted_unverified", "source_refs": []}, {}, e3, "SYM-017")
    check("'agent_drafted_unverified' kanıt İSTEMİYOR (dürüst taban durumu)",
          e3 == [], f"errors={e3}")


# ─────────────────────────────────────────────────────────────────────
# ③ taksonomi bütünlüğü — bu ürünün çekirdek kuralları
# ─────────────────────────────────────────────────────────────────────
def test_cause_distinguishability():
    e0: list[str] = []
    validate_spec.check_cause_distinguishability({"symptom_id": "SYM-899", "candidate_causes": [
        {"cause": "A", "distinguishing_evidence": "Omuz ucunda kumaş GERGİNDİR."},
        {"cause": "B", "distinguishing_evidence": "omuz ucunda kumaş gergindir."},
    ]}, e0)
    check("Türkçe büyük İ farkı ayırt-edicilik denetimini ATLATAMIYOR (K16 regresyonu)",
          any("okur bunları ayıramaz" in x for x in e0), f"errors={e0}")

    e: list[str] = []
    validate_spec.check_cause_distinguishability({"symptom_id": "SYM-900", "candidate_causes": [
        {"cause": "A nedeni", "distinguishing_evidence": "Aynı kanıt metni."},
        {"cause": "B nedeni", "distinguishing_evidence": "  AYNI KANIT METNİ.  "},
    ]}, e)
    check("iki nedenin AYNI ayırt edici kanıtı YAKALANIYOR (boşluk/büyük harf farkı dâhil)",
          any("okur bunları ayıramaz" in x for x in e), f"errors={e}")


def test_cause_measurement_present():
    e: list[str] = []
    validate_spec.check_cause_measurement_present({"symptom_id": "SYM-901", "candidate_causes": [
        {"cause": "Kanıtsız neden",
         "confirming_measurement": "NO_MEASUREMENT_EXISTS — physical test only",
         "physical_test": None},
    ]}, e)
    check("ne ölçümü ne fiziksel testi olan neden YAKALANIYOR",
          any("kanıtsız neden yazılamaz" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_cause_measurement_present({"symptom_id": "SYM-902", "candidate_causes": [
        {"cause": "Testi olan neden",
         "confirming_measurement": "NO_MEASUREMENT_EXISTS — physical test only",
         "physical_test": "Çözgü çizgilerini kontrol et."},
    ]}, e2)
    check("fiziksel testi olan ölçümsüz neden SERBEST", e2 == [], f"errors={e2}")


def test_symptom_af_refs():
    e: list[str] = []
    validate_spec.check_symptom_af_refs(
        {"symptom_id": "SYM-903", "candidate_causes": [{"adjustment_family_ref": "AF-99"}]},
        {"AF-01"}, e)
    check("tanımsız düzeltme ailesi referansı YAKALANIYOR",
          any("tanımlı bir düzeltme ailesi DEĞİL" in x for x in e), f"errors={e}")


def test_measurement_derivation():
    e: list[str] = []
    validate_spec.check_measurement_derivation(
        {"measurement_id": "M-900", "category": "derived", "derived_from": []}, {"M-001"}, e)
    check("kaynaksız türetilmiş ölçü YAKALANIYOR",
          any("derived_from BOŞ" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_measurement_derivation(
        {"measurement_id": "M-901", "category": "derived", "derived_from": ["M-777"]}, {"M-001"}, e2)
    check("tanımsız ölçü referansı YAKALANIYOR",
          any("tanımlı bir ölçü DEĞİL" in x for x in e2), f"errors={e2}")


def test_crosswalk_integrity():
    e: list[str] = []
    validate_spec.check_crosswalk_integrity(
        {"crosswalk_id": "XW-900", "direction": "DIAGNOSIS_TO_ADJUSTMENT",
         "from_ref": "SYM-001", "to_ref": None, "exception": None},
        {"SYM-001"}, {"AF-01"}, {"BLK-01"}, e)
    check("gerekçesiz crosswalk istisnası YAKALANIYOR",
          any("AÇIKÇA yazılmalıdır" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_crosswalk_integrity(
        {"crosswalk_id": "XW-901", "direction": "DIAGNOSIS_TO_ADJUSTMENT",
         "from_ref": "SYM-777", "to_ref": "AF-77", "exception": None},
        {"SYM-001"}, {"AF-01"}, {"BLK-01"}, e2)
    check("crosswalk'ta tanımsız uç noktaları YAKALANIYOR", len(e2) >= 2, f"errors={e2}")
    e3: list[str] = []
    validate_spec.check_crosswalk_integrity(
        {"crosswalk_id": "XW-902", "direction": "ADJUSTMENT_TO_BLOCK",
         "from_ref": "AF-01", "to_ref": None, "exception": "Blokta dereceleme yoktur."},
        {"SYM-001"}, {"AF-01"}, {"BLK-01"}, e3)
    check("gerekçeli istisna SERBEST", e3 == [], f"errors={e3}")


def test_figure_tokens():
    e: list[str] = []
    validate_spec.check_figure_tokens(
        {"figure_id": "FIG-B1-001", "notation_tokens": ["TK-99"],
         "deterministic": True, "verification_status": "drafted"}, {"TK-01"}, e)
    check("tanımsız görsel token YAKALANIYOR",
          any("tanımlı DEĞİL" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_spec.check_figure_tokens(
        {"figure_id": "FIG-B1-002", "notation_tokens": ["TK-01"],
         "deterministic": False, "manual_reason": None, "verification_status": "drafted"}, {"TK-01"}, e2)
    check("gerekçesiz elle çizim YAKALANIYOR",
          any("gerekçesiz olamaz" in x for x in e2), f"errors={e2}")
    e3: list[str] = []
    validate_spec.check_figure_tokens(
        {"figure_id": "FIG-B1-003", "notation_tokens": ["TK-01"], "deterministic": True,
         "verification_status": "physically_validated", "physical_validation_ref": None}, {"TK-01"}, e3)
    check("kanıtsız 'physically_validated' figür YAKALANIYOR",
          any("physical_validation_ref YOK" in x for x in e3), f"errors={e3}")


# ─────────────────────────────────────────────────────────────────────
# ④ kitap sınırı — seriye özgü kapı
# ─────────────────────────────────────────────────────────────────────
def test_single_primary_rule():
    f: list[str] = []
    qa_boundary.check_single_primary({"topics": [
        {"topic_id": "TOP-900", "name": "Çakışan topik",
         "book-01": "primary", "book-02": "primary", "book-03": "excluded"}]}, f)
    check("TEK-BİRİNCİL ihlali YAKALANIYOR",
          any("TEK-BİRİNCİL İHLALİ" in x for x in f), f"findings={f}")
    f2: list[str] = []
    qa_boundary.check_single_primary({"topics": [
        {"topic_id": "TOP-901", "name": "Sahipsiz topik",
         "book-01": "support", "book-02": "reference_only", "book-03": "excluded"}]}, f2)
    check("sahipsiz topik YAKALANIYOR",
          any("SAHİPSİZ TOPİK" in x for x in f2), f"findings={f2}")
    f3: list[str] = []
    qa_boundary.check_single_primary({"topics": [
        {"topic_id": "TOP-902", "name": "Tamamen dışlanmış",
         "book-01": "excluded", "book-02": "excluded", "book-03": "excluded"}]}, f3)
    check("tamamen dışlanmış topik SERBEST (kapsam dışı meşrudur)", f3 == [], f"findings={f3}")


def test_role_values():
    f: list[str] = []
    qa_boundary.check_role_values({"role_order": ["primary", "excluded"], "topics": [
        {"topic_id": "TOP-903", "book-01": "sahte_rol", "book-02": "excluded", "book-03": "excluded"}]}, f)
    check("geçersiz rol değeri YAKALANIYOR",
          any("geçersiz rol" in x for x in f), f"findings={f}")


def test_symptom_path_coverage():
    f: list[str] = []
    qa_boundary.check_symptom_paths([{"symptom_id": "SYM-904"}], [], f)
    check("hiçbir yola bağlanmamış belirti YAKALANIYOR",
          any("YOLSUZ BELİRTİ" in x for x in f), f"findings={f}")


def test_family_reachability():
    f: list[str] = []
    qa_boundary.check_family_reachability(
        [{"adjustment_family_id": "AF-77", "name": "Ulaşılamayan aile", "book1_entry_point": True}],
        [], f)
    check("Kitap 1'den ulaşılamayan düzeltme ailesi YAKALANIYOR",
          any("ULAŞILAMAYAN AİLE" in x for x in f), f"findings={f}")
    f2: list[str] = []
    qa_boundary.check_family_reachability(
        [{"adjustment_family_id": "AF-78", "name": "Kitap 2'ye özel", "book1_entry_point": False}],
        [], f2)
    check("book1_entry_point=false olan aile ulaşılabilirlik İSTEMİYOR", f2 == [], f"findings={f2}")


# ─────────────────────────────────────────────────────────────────────
# ⑤ iddia disiplini
# ─────────────────────────────────────────────────────────────────────
def test_fake_expert_claim():
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/SAHTE.md",
                        "Bu kitabın her bölümü expert-verified içerik taşır.", set(), f)
    check("sahte uzman iddiası YAKALANIYOR",
          any("SAHTE UZMAN" in x for x in f), f"findings={f}")


def test_negation_is_exempt():
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/DURUST.md",
                        "Bu kitap uzman onaylı DEĞİLDİR.", set(), f)
    check("dürüst inkâr YAKALANMIYOR (yanlış pozitif yok)", f == [], f"findings={f}")


def test_turkish_capital_i_regression():
    """K12/K16: kardeş projede SONRADAN bulunan gerçek kusur — Türkçe büyük
    'İ' str.lower() ile 'i̇' (i + birleşen nokta) olur ve alt dizi eşleşmesini
    SESSİZCE bozar.

    Bu testin kendisi bu depoda ÜÇÜNCÜ bir açık noktayı buldu
    (validate_spec.check_cause_distinguishability); katlama artık tek
    kopyadır (trfold.py) ve üç doğrulayıcı da oradan alır."""
    check("trfold.fold() Türkçe büyük İ'yi doğru katlıyor",
          trfold.fold("UZMAN ONAYLI DEĞİLDİR") == "uzman onaylı değildir",
          f"got={trfold.fold('UZMAN ONAYLI DEĞİLDİR')!r}")
    for mod, name in ((qa_claims, "qa_claims"), (qa_terminology, "qa_terminology")):
        check(f"{name} TEK KOPYA katlamayı kullanıyor", mod._fold is trfold.fold)
    check("str.lower() bunu YAPAMAZDI (kusurun gerçekliğinin kanıtı)",
          "değildir" not in "UZMAN ONAYLI DEĞİLDİR".lower(),
          "beklenmedik: str.lower() doğru sonuç verdi, regresyon testi anlamsızlaşır")
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/BUYUK.md",
                        "BU KİTAP UZMAN ONAYLI DEĞİLDİR.", set(), f)
    check("BÜYÜK HARFLİ dürüst inkâr da YAKALANMIYOR", f == [], f"findings={f}")


def test_protected_print_advantage_claim():
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/IDDIA.md",
                        "Bu üründe basılı formatın kanıtlanmış avantajı vardır.", set(), f)
    check("korunan 'basılı avantaj' iddiası YAKALANIYOR",
          any("KORUNAN İDDİA" in x for x in f), f"findings={f}")


def test_unbacked_validation_claim():
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/DOG.md",
                        "Kitaptaki her diyagram test edildi.", set(), f)
    check("dayanaksız doğrulama iddiası YAKALANIYOR",
          any("DAYANAKSIZ DOĞRULAMA" in x for x in f), f"findings={f}")
    f2: list[str] = []
    qa_claims.scan_file("00_CONTEXT/DOG2.md",
                        "Kitaptaki her diyagram test edildi (VAL-0001).", set(), f2)
    check("VAL-xxxx atıflı doğrulama iddiası SERBEST", f2 == [], f"findings={f2}")


def test_policy_files_exempt():
    f: list[str] = []
    qa_claims.scan_file("00_CONTEXT/CLAIMS_STANDARD.md",
                        "expert-verified ifadesi yasaktır.", set(), f)
    check("politika belgesi yasağı TANIMLAYABİLİYOR (muaf)", f == [], f"findings={f}")


# ─────────────────────────────────────────────────────────────────────
# ⑥ terminoloji
# ─────────────────────────────────────────────────────────────────────
def test_terminology_exemptions_exist():
    check("sözlük belgeleri yasak-eşanlamlı taramasından muaf",
          "00_CONTEXT/STYLE.md" in qa_terminology.EXEMPT_FROM_BANNED_SYNONYMS)
    check("anahtar kelime belgeleri AYRI bir gerekçeyle muaf (K14)",
          "00_CONTEXT/SERIES_KEYWORD_ARCHITECTURE.md" in qa_terminology.KEYWORD_FILES
          and "00_CONTEXT/SERIES_KEYWORD_ARCHITECTURE.md" not in qa_terminology.GLOSSARY_FILES,
          "iki muafiyet AYNI kümede olamaz — gerekçeleri farklıdır")


def test_terminology_id_patterns_cover_all_kinds():
    for kind in ("AF", "SYM", "M", "T", "TOP", "BLK", "TK"):
        check(f"terminoloji taraması {kind}-kimliklerini tanıyor",
              kind in qa_terminology.ID_PATTERNS)


# ─────────────────────────────────────────────────────────────────────
# ⑦ depo koruma
# ─────────────────────────────────────────────────────────────────────
def test_photo_leak_detection():
    e: list[str] = []
    validate_structure.check_photo_leak(
        ["BOOK-01-MEASURE-AND-DIAGNOSE/08_REPORTS/validation_photos/a.jpg"], e)
    check("fiziksel doğrulama fotoğrafı sızıntısı YAKALANIYOR",
          any("FOTOĞRAFI TAKİP EDİLİYOR" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_structure.check_photo_leak(["docs/x_muslin_photo.png"], e2)
    check("adlandırma deseniyle fotoğraf sızıntısı YAKALANIYOR",
          any("FOTOĞRAFI TAKİP EDİLİYOR" in x for x in e2), f"errors={e2}")
    e3: list[str] = []
    validate_structure.check_photo_leak(["06_BUILD/paths.py", "README.md"], e3)
    check("normal dosyalar fotoğraf sanılmıyor", e3 == [], f"errors={e3}")


def test_protected_dir_leak_detection():
    e: list[str] = []
    validate_structure.check_protected_dirs(
        ["BOOK-01-MEASURE-AND-DIAGNOSE/02_CONTENT/protected/lesson.json"], e)
    check("korumalı dizinde izlenen dosya YAKALANIYOR",
          any("KORUMALI DİZİNDE" in x for x in e), f"errors={e}")
    e2: list[str] = []
    validate_structure.check_protected_dirs(
        ["BOOK-01-MEASURE-AND-DIAGNOSE/02_CONTENT/protected/.gitkeep"], e2)
    check(".gitkeep muaf", e2 == [], f"errors={e2}")
    e3: list[str] = []
    validate_structure.check_protected_dirs([], e3)
    check("git deposu yokken sızıntı denetimi SESSİZCE GEÇMİYOR",
          any("YAPILAMAZ" in x for x in e3), f"errors={e3}")


def test_brand_leak_detection():
    tmp = paths.TESTS_FIXTURES / "generated"
    tmp.mkdir(parents=True, exist_ok=True)
    bad = tmp / "fixture_metadata.json"
    bad.write_text('{"title": "Fitting for Simplicity patterns"}', encoding="utf-8")
    try:
        e: list[str] = []
        validate_structure.check_brand_leak(e)
        check("metadata'da ticari kalıp markası YAKALANIYOR",
              any("MARKA SIZINTISI" in x and "fixture_metadata.json" in x for x in e),
              f"errors={e}")
    finally:
        bad.unlink(missing_ok=True)
    e2: list[str] = []
    validate_structure.check_brand_leak(e2)
    check("gerçek depoda marka sızıntısı YOK", e2 == [], f"errors={e2}")


def test_sibling_dependency_detection():
    probe = paths.TESTS / "fixture_sibling_probe.py"
    probe.write_text(
        "# mimari atıf: KOREAN-HANGUL-HANDWRITING-WORKBOOK deseninden ilham alındı\n"
        "import os\n", encoding="utf-8")
    try:
        e: list[str] = []
        validate_structure.check_no_sibling_dependency(e)
        check("mimari ATIF yorumu izolasyon ihlali SAYILMIYOR",
              not any("fixture_sibling_probe" in x for x in e), f"errors={e}")
        # ⚠ Kardeş depo adı BURADA LİTERAL OLARAK YAZILAMAZ: bu dosya da
        # check_no_sibling_dependency tarafından taranır ve kendi
        # fixture'ımız yanlış pozitif üretirdi (kardeş projelerde
        # SONRADAN bulunan "doğrulayıcı kendi araç zincirini tarıyor"
        # kusurunun tam karşılığı). Ad, çalışma anında yapılandırmadan
        # okunur — böylece kapı ZAYIFLATILMADAN yanlış pozitif kalkar.
        sibling = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))[
            "series"]["isolatedFrom"][0]
        probe.write_text(
            'from pathlib import Path\n'
            'P = Path("../%s/06_BUILD")\n' % sibling, encoding="utf-8")
        e2: list[str] = []
        validate_structure.check_no_sibling_dependency(e2)
        check("gerçek kardeş-depo BAĞIMLILIĞI YAKALANIYOR",
              any("İZOLASYON İHLALİ" in x and "fixture_sibling_probe" in x for x in e2),
              f"errors={e2}")
    finally:
        probe.unlink(missing_ok=True)


# ─────────────────────────────────────────────────────────────────────
# ⑧ kapı katmanları ve türetilmiş veri
# ─────────────────────────────────────────────────────────────────────
def test_gate_layers_are_separate():
    check("seri ve kitap kapı sıraları FARKLI",
          paths.SERIES_GATE_ORDER != paths.BOOK_GATE_ORDER)
    ok = paths.gate_at_least("production", "series-architecture", paths.SERIES_GATE_ORDER)
    check("seri kapısı kendi sırasında karşılaştırılabiliyor", ok is True)
    try:
        paths.gate_at_least("phase1-spec", "series-architecture", paths.SERIES_GATE_ORDER)
        crossed = False
    except ValueError:
        crossed = True
    check("KİTAP kapısı SERİ sırasıyla karşılaştırılamıyor (katman karışması engelli)",
          crossed, "gate_at_least yanlış katmanı sessizce kabul etti")


def test_invalid_gate_value_rejected():
    gf = paths.book_gate_file("book-01")
    original = gf.read_text(encoding="utf-8")
    try:
        gf.write_text("bogus-gate", encoding="utf-8")
        try:
            paths.read_book_gate("book-01")
            caught = False
        except ValueError:
            caught = True
        check("geçersiz kapı değeri REDDEDİLİYOR", caught)
    finally:
        gf.write_text(original, encoding="utf-8")


def test_crosswalk_is_deterministic_and_staleness_detected():
    a = build_crosswalk.build()
    b = build_crosswalk.build()
    check("crosswalk üretimi DETERMİNİSTİK", a["crosswalks"] == b["crosswalks"])
    cur = json.loads(paths.CROSSWALK.read_text(encoding="utf-8"))
    check("diskteki crosswalk kaynak taksonomiyle GÜNCEL",
          cur.get("crosswalks") == a["crosswalks"],
          "build_crosswalk.py çalıştırılmalı")
    stale = [dict(r) for r in a["crosswalks"]]
    stale.pop()
    check("bayat crosswalk TESPİT EDİLEBİLİR", stale != a["crosswalks"])


def test_kill_gate_flag_cannot_be_flipped():
    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))
    kg = cfg["killGates"]["differentiationTest"]
    check("AI vekil bayrağı KAPALI (K6 — açılamaz)", kg["aiProxyCountsAsHuman"] is False)
    check("fark testi HENÜZ ÖLÇÜLMEDİ olarak kayıtlı", kg["measured"] is False)
    check("kurucu geçersiz kılması AYRI bir alan (ölçümle karışmıyor)",
          "founderOverride" in kg and kg["founderOverride"] is None)


def test_verification_status_is_honestly_recorded():
    """Faz 1'in en önemli dürüstlük kaydı: hiçbir taksonomi kaydı sessizce
    yükseltilmemiş olmalı."""
    for f, key in ((paths.FIT_SIGNS, "signs"), (paths.ADJUSTMENT_FAMILIES, "families"),
                   (paths.MEASUREMENTS, "measurements")):
        recs = json.loads(f.read_text(encoding="utf-8"))[key]
        upgraded = [r for r in recs
                    if r.get("verification_status") != "agent_drafted_unverified"]
        check(f"{f.name}: hiçbir kayıt kanıtsız yükseltilmemiş",
              not upgraded, f"yükseltilmiş: {[r for r in upgraded][:3]}")


def main():
    print("▸ selftest.py — kapıların kendi testi\n")
    for fn in (
        test_schema_lite,
        test_source_authority_consistency, test_source_locator_discipline,
        test_source_authority_required, test_verification_evidence,
        test_cause_distinguishability, test_cause_measurement_present,
        test_symptom_af_refs, test_measurement_derivation,
        test_crosswalk_integrity, test_figure_tokens,
        test_single_primary_rule, test_role_values,
        test_symptom_path_coverage, test_family_reachability,
        test_fake_expert_claim, test_negation_is_exempt,
        test_turkish_capital_i_regression, test_protected_print_advantage_claim,
        test_unbacked_validation_claim, test_policy_files_exempt,
        test_terminology_exemptions_exist, test_terminology_id_patterns_cover_all_kinds,
        test_photo_leak_detection, test_protected_dir_leak_detection,
        test_brand_leak_detection, test_sibling_dependency_detection,
        test_gate_layers_are_separate, test_invalid_gate_value_rejected,
        test_crosswalk_is_deterministic_and_staleness_detected,
        test_kill_gate_flag_cannot_be_flipped,
        test_verification_status_is_honestly_recorded,
    ):
        fn()

    print(f"\n{CHECKS} denetim çalıştı, {len(FAILURES)} başarısız.")
    if FAILURES:
        print("\n✗ BAŞARISIZ DENETİMLER:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("✓ Bütün kapılar kusurlu fixture'ları doğru yakaladı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
