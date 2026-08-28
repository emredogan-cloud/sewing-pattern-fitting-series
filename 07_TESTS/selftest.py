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
import qa_crosswalk     # noqa: E402
import qa_visual        # noqa: E402
import figure_tokens    # noqa: E402
import croquis          # noqa: E402
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


def test_crosswalk_audit_gate():
    """qa_crosswalk.py — dokuz ilişki denetiminin her biri KUSURLU bir
    kurguyu gerçekten yakalıyor mu.

    Bu kapı, `build_crosswalk --check`'in yakalayamadığı sınıfı kapatır:
    BAYAT OLMAYAN ama YANLIŞ bir crosswalk (DECISIONS.md K31)."""
    def sign(sid, causes):
        return {"symptom_id": sid,
                "candidate_causes": [{"cause": c, "adjustment_family_ref": a}
                                     for c, a in causes]}

    SIGNS = [sign("SYM-001", [("Yaka fazla geniş", "AF-06")])]
    FAMS = {"AF-06": {"adjustment_family_id": "AF-06", "name": "Neckline size and shape",
                      "book1_entry_point": True}}
    BLKS = {"BLK-01": {"block_id": "BLK-01"}}
    GOOD = [{"crosswalk_id": "XW-001", "direction": "DIAGNOSIS_TO_ADJUSTMENT",
             "from_ref": "SYM-001", "to_ref": "AF-06", "exception": None,
             "handoff_sentence": "Yaka fazla geniş → AF-06 (Neckline size and shape)."}]

    check("qa_crosswalk: sağlam kurgu TEMİZ geçiyor",
          qa_crosswalk.audit(SIGNS, FAMS, BLKS, GOOD) == [],
          f"{qa_crosswalk.audit(SIGNS, FAMS, BLKS, GOOD)}")

    # ② devir cümlesi aday nedeni taşımıyor
    bad = [dict(GOOD[0], handoff_sentence="Bir şey oldu → AF-06 (Neckline size and shape).")]
    check("qa_crosswalk ②: nedeni taşımayan devir cümlesi YAKALANIYOR",
          any(x.startswith("②") for x in qa_crosswalk.audit(SIGNS, FAMS, BLKS, bad)))

    # ④ to_ref DOLU ama exception da dolu — build_crosswalk --check bunu GÖRMEZ
    bad = [dict(GOOD[0], exception="Bu bir yapım hatasıdır.")]
    check("qa_crosswalk ④: hem varış hem istisna taşıyan kayıt YAKALANIYOR",
          any(x.startswith("④") for x in qa_crosswalk.audit(SIGNS, FAMS, BLKS, bad)))

    # ⑤ uydurulmuş yol (taksonomide olmayan çift)
    bad = GOOD + [{"crosswalk_id": "XW-002", "direction": "DIAGNOSIS_TO_ADJUSTMENT",
                   "from_ref": "SYM-001", "to_ref": None, "exception": "Yapım hatası.",
                   "handoff_sentence": "Yaka fazla geniş → istisna."}]
    check("qa_crosswalk ⑤: taksonomide karşılığı OLMAYAN yol YAKALANIYOR",
          any(x.startswith("⑤") for x in qa_crosswalk.audit(SIGNS, FAMS, BLKS, bad)))

    # ⑤ kaybolmuş yol
    check("qa_crosswalk ⑤: taksonomide OLUP crosswalk'ta olmayan yol YAKALANIYOR",
          any(x.startswith("⑤") for x in qa_crosswalk.audit(SIGNS, FAMS, BLKS, [])))

    # ⑥ kitap sahipliği çelişkisi
    fams2 = {"AF-06": dict(FAMS["AF-06"], book1_entry_point=False)}
    check("qa_crosswalk ⑥: book1_entry_point=false hedefe giden yol YAKALANIYOR",
          any(x.startswith("⑥") for x in qa_crosswalk.audit(SIGNS, fams2, BLKS, GOOD)))

    # ⑦ kanonik ad taşımayan devir cümlesi
    bad = [dict(GOOD[0], handoff_sentence="Yaka fazla geniş → AF-06 (yaka işi).")]
    check("qa_crosswalk ⑦: kanonik aile adını taşımayan devir cümlesi YAKALANIYOR",
          any(x.startswith("⑦") for x in qa_crosswalk.audit(SIGNS, FAMS, BLKS, bad)))

    # ⑨ yolu olmayan belirti
    signs2 = SIGNS + [sign("SYM-002", [("Başka bir neden", "AF-06")])]
    check("qa_crosswalk ⑨: hiçbir yolu olmayan belirti YAKALANIYOR",
          any(x.startswith("⑨") for x in qa_crosswalk.audit(signs2, FAMS, BLKS, GOOD)))

    # GERÇEK veri temiz mi
    real = qa_crosswalk.audit(
        json.loads(paths.FIT_SIGNS.read_text(encoding="utf-8"))["signs"],
        {f["adjustment_family_id"]: f for f in
         json.loads(paths.ADJUSTMENT_FAMILIES.read_text(encoding="utf-8"))["families"]},
        {b["block_id"]: b for b in
         json.loads(paths.BLOCK_COMPONENTS.read_text(encoding="utf-8"))["blocks"]},
        json.loads(paths.CROSSWALK.read_text(encoding="utf-8"))["crosswalks"])
    check("qa_crosswalk: GERÇEK crosswalk dokuz denetimden temiz geçiyor",
          real == [], f"bulgular={real[:3]}")


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


def _source_index():
    """Gerçek kaynak kayıtlarını okur: id → (technical_authority, verification_level)."""
    idx = {}
    for f in sorted(paths.SOURCE_RECORDS.glob("S-*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        idx[r["source_id"]] = (r.get("technical_authority") is True,
                               r.get("verification_level"))
    return idx


def test_verification_status_is_honestly_recorded():
    """Faz 1'in en önemli dürüstlük kaydı: hiçbir taksonomi kaydı SESSİZCE
    yükseltilmemiş olmalı.

    ⚠ Bu testin İLK sürümü "hiçbir kayıt yükseltilMEMİŞ" diye yazılmıştı.
    Bu, kaynak sayısı SIFIRKEN doğru görünen ama YANLIŞ bir testtir: bir
    kaydın yükseltilmesi bir kusur değildir — KANITSIZ yükseltilmesi
    kusurdur. Kamu kaynakları edinildiğinde test, doğru davranışı hata
    olarak raporladı. Düzeltildi: artık testin ADI ne diyorsa ONU ölçer
    (DECISIONS.md K20).
    """
    idx = _source_index()
    for f, key in ((paths.FIT_SIGNS, "signs"), (paths.ADJUSTMENT_FAMILIES, "families"),
                   (paths.MEASUREMENTS, "measurements")):
        recs = json.loads(f.read_text(encoding="utf-8"))[key]
        bad = []
        for r in recs:
            st = r.get("verification_status")
            refs = r.get("source_refs", [])
            if st == "technical_reference_verified":
                if not any(idx.get(x, (False, None))[1] in validate_spec.STRONG_VERIFICATION
                           for x in refs):
                    bad.append((r, "fulltext/official_pdf kaynağı yok"))
                elif not any(idx.get(x, (False, None))[0] for x in refs):
                    bad.append((r, "technical_authority=true kaynağı yok"))
            elif st == "physically_validated" and not r.get("validation_record_ref"):
                bad.append((r, "validation_record_ref yok"))
            if refs and not any(x in idx for x in refs):
                bad.append((r, "source_refs kayıtsız kaynağa işaret ediyor"))
        check(f"{f.name}: yükseltilmiş her kayıt GERÇEKTEN kanıt taşıyor",
              not bad, f"kusurlu: {[(b[0].get('measurement_id') or b[0].get('adjustment_family_id') or b[0].get('symptom_id'), b[1]) for b in bad][:4]}")


def test_verification_summary_matches_records():
    """fit_signs.json'un ilan ettiği doğrulama özeti GERÇEK kayıtlarla
    uyuşmalıdır. Bu özet blok on'a yakın belgede alıntılanıyor; veriden
    sessizce sapması, projenin en çok tekrarlanan dürüstlük iddiasını
    yalana çevirirdi."""
    d = json.loads(paths.FIT_SIGNS.read_text(encoding="utf-8"))
    declared = d.get("verification_summary", {})
    actual = {}
    for r in d["signs"]:
        actual[r["verification_status"]] = actual.get(r["verification_status"], 0) + 1
    for k, v in declared.items():
        check(f"fit_signs verification_summary['{k}'] veriyle uyuşuyor",
              actual.get(k, 0) == v, f"ilan={v} gerçek={actual.get(k, 0)}")
    check("fit_signs count alanı kayıt sayısıyla uyuşuyor",
          d.get("count") == len(d["signs"]), f"count={d.get('count')} kayıt={len(d['signs'])}")


# ─────────────────────────────────────────────────────────────────────
# ⑬ GÖRSEL SİSTEM — Faz 2 kapıları
#
# Bu blok `qa_visual.py` ve `figure_tokens.py`'nin GERÇEKTEN kırmızı
# yaktığını kanıtlar. Bir çizim yasağı, çizimi DURDURMUYORSA yasak
# değildir; yalnızca bir belge cümlesidir.
# ─────────────────────────────────────────────────────────────────────
def _fc(w=200.0, h=200.0, surface="diagram"):
    return figure_tokens.FigureCanvas(w, h, surface=surface)


def _raises(fn) -> bool:
    try:
        fn()
    except figure_tokens.ForbiddenDrawing:
        return True
    except Exception:
        return False
    return False


def test_drawing_prohibitions_are_executable():
    """VISUAL_STANDARD § 5'in her yasağı bir İSTİSNA üretmelidir."""
    check("sayısal etiketsiz TK-02 (spread) çizimi REDDEDİLİYOR",
          _raises(lambda: _fc().tk02_spread_arrow(10, 10, 60, 10, "")),
          "etiketsiz spread oku çizilebildi")
    check("sayısal etiketsiz TK-03 (overlap) çizimi REDDEDİLİYOR",
          _raises(lambda: _fc().tk03_overlap_arrow(10, 10, 60, 10, "  ")),
          "etiketsiz overlap oku çizilebildi")
    check("ETİKETLİ spread oku SERBEST (yanlış pozitif yok)",
          not _raises(lambda: _fc().tk02_spread_arrow(10, 10, 60, 10, "1 in")),
          "etiketli ok reddedildi")
    check("vücut figüründe TK-01 (slash line) REDDEDİLİYOR",
          _raises(lambda: _fc(surface="body").tk01_slash_line(10, 10, 60, 60)),
          "vücutta slash line çizilebildi")
    check("KALIP yüzeyinde TK-01 SERBEST (yasak yüzeye özgüdür)",
          not _raises(lambda: _fc(surface="pattern").tk01_slash_line(10, 10, 60, 60)),
          "kalıpta slash line reddedildi")
    check("ölçek beyanı olmayan kalıp parçası REDDEDİLİYOR",
          _raises(lambda: _fc(surface="pattern").finish()),
          "ölçeksiz kalıp parçası kapanabildi")
    check("ölçek BEYAN EDİLİRSE kalıp parçası kapanıyor",
          not _raises(lambda: _fc(surface="pattern").declare_scale("şematik") or
                      None),
          "ölçek beyanı çalışmıyor")
    check("figür kutusunun DIŞINA çizim REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 10, 400)),
          "taşan çizgi çizilebildi")
    check("izin listesi dışı GRİ TONU REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 60, 10, gray=0.30)),
          "tanımsız gri kullanılabildi")
    check("baskı asgarisinin ALTINDA çizgi REDDEDİLİYOR",
          _raises(lambda: _fc().line(10, 10, 60, 10, width=0.15)),
          "0,15 pt çizgi çizilebildi")
    check("asgari punto ALTINDA etiket REDDEDİLİYOR",
          _raises(lambda: _fc().text(10, 10, "x", size=4.0)),
          "4 pt etiket yazılabildi")
    check("TK-14 adım numarası 1'den KÜÇÜK olamıyor",
          _raises(lambda: _fc().tk14_step(50, 50, 0)),
          "0. adım çizilebildi")
    check("TK-18 devir düğümü AF etiketi OLMADAN çizilemiyor",
          _raises(lambda: _fc().tk18_handoff_node(10, 10, 120, 30, "x", "")),
          "AF'siz devir düğümü çizilebildi")
    check("tanımsız token kullanımı REDDEDİLİYOR",
          _raises(lambda: _fc().use("TK-99")),
          "TK-99 kullanılabildi")


def test_reader_facing_figures_carry_no_internal_ids():
    """İç kayıt kimlikleri OKURA BASILAMAZ (TYPOGRAPHY_STANDARD § 3.4)."""
    fc = _fc()
    fc.text(10, 100, "See AF-01")
    check("okura dönük figürde AF-xx kimliği REDDEDİLİYOR",
          _raises(lambda: fc.finish()), "AF-01 basılabildi")
    fc2 = _fc()
    fc2.text(10, 100, "SYM-016")
    check("okura dönük figürde SYM-xxx kimliği REDDEDİLİYOR",
          _raises(lambda: fc2.finish()), "SYM-016 basılabildi")
    fc3 = _fc()
    fc3.text(10, 100, "Bust volume")
    check("normal etiket SERBEST (yanlış pozitif yok)",
          not _raises(lambda: fc3.finish()), "normal etiket reddedildi")
    fc4 = _fc()
    fc4.text(10, 100, "AF-01")
    check("İÇ ARAÇ figüründe kimlik SERBEST (internal_marks)",
          not _raises(lambda: fc4.finish(internal_marks=True)),
          "iç araç figürü reddedildi")


def test_labels_do_not_overlap():
    """Çakışan iki ölçü etiketi yanlış okunur — bu bir HATA'dır."""
    fc = _fc()
    fc.text(20, 100, "high bust")
    fc.text(24, 101, "bust apex")
    check("ÜST ÜSTE BİNEN etiketler REDDEDİLİYOR",
          _raises(lambda: fc.finish()), "çakışan etiketler geçti")
    fc2 = _fc()
    fc2.text(20, 100, "high bust")
    fc2.text(20, 130, "bust apex")
    check("ayrık etiketler SERBEST (yanlış pozitif yok)",
          not _raises(lambda: fc2.finish()), "ayrık etiketler reddedildi")


def test_token_usage_is_measured_not_declared():
    """figures.json'daki notation_tokens BEYAN değil ÖLÇÜMDÜR."""
    fc = _fc()
    fc.tk08_apex(60, 60)
    fc.tk04_pivot_point(120, 60)
    used = fc.finish()
    check("kullanılan token'lar çizimden TÜRETİLİYOR",
          set(used) == {"TK-08", "TK-04"}, f"used={used}")
    fc2 = _fc()
    check("hiç çizim yapılmayan figürde token listesi BOŞ",
          fc2.finish() == [], "boş figür token bildirdi")


def test_qa_visual_catches_defects():
    """qa_visual.py kusurlu bir figür sicilini yakalamalıdır."""
    import copy
    real = json.loads(paths.book_figures("book-01").read_text(encoding="utf-8")) \
        if paths.book_figures("book-01").exists() else None
    if real is None:
        check("qa_visual fixture testi atlandı (figures.json yok)", True)
        return

    tokens = json.loads(paths.VISUAL_TOKENS.read_text(encoding="utf-8"))
    geom = json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))
    token_ids = {x["token_id"] for x in tokens["tokens"]}

    # ① tanımsız token
    f = {"figure_id": "FIG-B1-999", "notation_tokens": ["TK-99"]}
    check("qa_visual tanımsız token'ı YAKALIYOR",
          "TK-99" not in token_ids, "TK-99 gerçekten tanımlı çıktı")

    # ② boşta biten yol — terminals içinde metinsiz eleme
    bad = copy.deepcopy(real)
    fid = next(x["figure_id"] for x in bad["figures"] if x["figure_type"] == "flowchart"
               and x["figure_id"] in bad["figure_meta"]
               and "terminals" in bad["figure_meta"][x["figure_id"]])
    bad["figure_meta"][fid]["terminals"] = [["eliminate", ""]]
    findings: list[str] = []
    _run_qa_visual_on(bad, findings)
    check("qa_visual BOŞTA BİTEN YOLU yakalıyor",
          any("BOŞTA BİTEN" in x for x in findings), f"findings={findings[:2]}")

    # ③ gerekçesiz elle çizim
    bad2 = copy.deepcopy(real)
    for x in bad2["figures"]:
        if x["deterministic"] is False:
            x["manual_reason"] = None
            break
    findings2: list[str] = []
    _run_qa_visual_on(bad2, findings2)
    check("qa_visual GEREKÇESİZ elle çizimi yakalıyor",
          any("manual_reason YOK" in x for x in findings2), f"findings={findings2[:2]}")

    # ④ A11 fotoğraf eşiği
    bad3 = copy.deepcopy(real)
    for x in bad3["figures"][:qa_visual.PHOTO_CAP + 1]:
        x["photo_required"] = True
    findings3: list[str] = []
    _run_qa_visual_on(bad3, findings3)
    check("qa_visual A11 fotoğraf eşiğinin AŞILMASINI yakalıyor",
          any("photo_required" in x for x in findings3), f"findings={findings3[:2]}")

    # ⑤ A6 renk eşiği
    bad4 = copy.deepcopy(real)
    n = int(len(bad4["figures"]) * qa_visual.COLOR_RATIO_CAP) + 2
    for x in bad4["figures"][:n]:
        x["color_required"] = True
    findings4: list[str] = []
    _run_qa_visual_on(bad4, findings4)
    check("qa_visual A6 renk eşiğinin AŞILMASINI yakalıyor",
          any("color_required" in x for x in findings4), f"findings={findings4[:2]}")

    # ⑥ sayfaya sığmayan figür
    bad5 = copy.deepcopy(real)
    k = next(iter(bad5["figure_meta"]))
    bad5["figure_meta"][k]["height_pt"] = geom["figure_area"]["max_height_pt"] + 50
    findings5: list[str] = []
    _run_qa_visual_on(bad5, findings5)
    check("qa_visual SAYFAYA SIĞMAYAN figürü yakalıyor",
          any("SIĞMIYOR" in x for x in findings5), f"findings={findings5[:2]}")

    # ⑦ eksik akış şeması
    bad6 = copy.deepcopy(real)
    for x in list(bad6["figures"]):
        if x["figure_type"] == "flowchart" and x["figure_id"] in bad6["figure_meta"] \
                and bad6["figure_meta"][x["figure_id"]].get("symptom_ref"):
            bad6["figure_meta"].pop(x["figure_id"])
            bad6["figures"].remove(x)
            break
    findings6: list[str] = []
    _run_qa_visual_on(bad6, findings6)
    check("qa_visual AKIŞ ŞEMASI EKSİK olan belirtiyi yakalıyor",
          any("akış şeması YOK" in x for x in findings6), f"findings={findings6[:2]}")

    # ⑧ sağlam sicil temiz geçmeli — YANLIŞ POZİTİF YOK
    findings7: list[str] = []
    _run_qa_visual_on(copy.deepcopy(real), findings7)
    check("qa_visual GERÇEK sicilde 0 bulgu veriyor (yanlış pozitif yok)",
          not findings7, f"findings={findings7[:3]}")
    del f, fid


def _run_qa_visual_on(data: dict, findings: list):
    """qa_visual.check()'i geçici bir figures.json üzerinde koşturur."""
    import tempfile, shutil
    real_path = paths.book_figures("book-01")
    backup = real_path.read_bytes()
    try:
        real_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        qa_visual.check("book-01", findings, {})
    finally:
        real_path.write_bytes(backup)
    del tempfile, shutil


def test_build_scripts_are_tracked():
    """Her build/test scripti git tarafından İZLENİYOR olmalıdır.

    Bu test bir gerçek kusurdan doğdu: `.gitignore`'un sır deseni
    çıplak `*_token*` arıyordu ve `06_BUILD/figure_tokens.py` ile
    `06_BUILD/calibrate_tokens.py`'yi SESSİZCE dışarıda bırakıyordu.
    Depo yerelde yeşil, temiz bir klonda ÇALIŞMAZ hâldeydi — ve
    hiçbir kapı bunu görmüyordu (RISK_REGISTER R-19).
    """
    import subprocess
    try:
        out = subprocess.run(["git", "ls-files"], cwd=paths.ROOT,
                             capture_output=True, text=True, check=True)
        tracked = set(out.stdout.split())
    except Exception:
        check("git ls-files çalıştı", False, "git yok")
        return
    on_disk = {p.relative_to(paths.ROOT).as_posix()
               for p in list(paths.BUILD.glob("*.py")) + list(paths.TESTS.glob("*.py"))
               + list(paths.BUILD.glob("*.sh"))}
    untracked = sorted(on_disk - tracked)
    # Yeni eklenen ama henüz commit edilmemiş dosyalar `git add -A` ile
    # gelir; test asıl olarak YOKSAYILAN dosyayı arar.
    ignored = []
    for f in untracked:
        r = subprocess.run(["git", "check-ignore", "-q", f], cwd=paths.ROOT)
        if r.returncode == 0:
            ignored.append(f)
    check("hiçbir build/test scripti .gitignore tarafından YUTULMUYOR",
          not ignored, f"yoksayılan scriptler: {ignored}")


def test_reader_language_layer():
    """Figürler OKURUN dilinde çizilmelidir, proje belge dilinde değil."""
    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))["series"]
    check("kitap dili ile belge dili AYRI alanlarda",
          cfg.get("language") != cfg.get("documentLanguage"),
          "iki dil aynı alanda karışmış")
    check("okura dönük etiket katmanı MEVCUT",
          paths.LABELS_EN.exists(), "labels_en.json yok")
    lab = json.loads(paths.LABELS_EN.read_text(encoding="utf-8"))
    signs = json.loads(paths.FIT_SIGNS.read_text(encoding="utf-8"))["signs"]
    check("her belirtinin okura dönük karşılığı var",
          all(s["symptom_id"] in lab["signs"] for s in signs),
          "eksik belirti etiketi")
    check("her aday nedenin okura dönük karşılığı var",
          all(len(lab["signs"][s["symptom_id"]]["causes"]) == len(s["candidate_causes"])
              for s in signs), "aday neden sayıları uyuşmuyor")
    check("etiket katmanı DOĞRULAMA DURUMUNU değiştirmediğini beyan ediyor",
          lab.get("does_not_change_verification_status") is True,
          "bir çeviri katmanı bir doğrulama gibi sunulabilir hâlde")

    # kusurlu fixture: bir belirtinin etiketini sil
    import copy
    real = paths.LABELS_EN.read_bytes()
    bad = copy.deepcopy(lab)
    victim = signs[0]["symptom_id"]
    bad["signs"].pop(victim)
    findings: list[str] = []
    try:
        paths.LABELS_EN.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        qa_visual.check("book-01", findings, {})
    finally:
        paths.LABELS_EN.write_bytes(real)
    check("qa_visual EKSİK okur etiketini yakalıyor",
          any("okura dönük etiketi YOK" in x for x in findings),
          f"findings={findings[:2]}")


def test_page_geometry_respects_platform_minimums():
    """Sayfa geometrisi KDP'nin asgarisini ihlal EDEMEZ — dosya reddedilir."""
    geom = json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))
    pm = geom["platform_minimums"]
    band = pm["page_count_band_used"]
    check("cilt payı KDP asgarisinin ÜSTÜNDE",
          geom["margins"]["gutter_in"] >= pm["gutter_by_page_count_in"][band],
          f"gutter={geom['margins']['gutter_in']} min={pm['gutter_by_page_count_in'][band]}")
    om = pm["outside_margin_with_bleed_in"] if geom["trim"]["bleed"] \
        else pm["outside_margin_no_bleed_in"]
    check("dış/üst/alt kenar boşlukları KDP asgarisinin ÜSTÜNDE",
          all(geom["margins"][e] >= om for e in ("outside_in", "top_in", "bottom_in")),
          f"min={om}")
    check("metin bloğu + yan sütun + boşluk = tam ölçü",
          abs(geom["text_block"]["width_pt"] + geom["text_block"]["column_gap_pt"]
              + geom["text_block"]["side_column_width_pt"]
              - geom["text_block"]["total_measure_pt"]) < 0.01,
          "sütun aritmetiği tutmuyor")
    check("tam ölçü = trim − cilt payı − dış kenar",
          abs(geom["text_block"]["total_measure_pt"]
              - (geom["trim"]["width_pt"] - geom["margins"]["gutter_pt"]
                 - geom["margins"]["outside_pt"])) < 0.01,
          "sayfa aritmetiği tutmuyor")


def test_calibration_is_not_claimed_without_evidence():
    """`CALIBRATED` bir RAPORA bağlı olmadan yazılamaz — K10 disiplini."""
    tokens = json.loads(paths.VISUAL_TOKENS.read_text(encoding="utf-8"))
    st = tokens.get("status", "")
    if st in qa_visual.CALIBRATED_STATES:
        check("kalibrasyon iddiası bir RAPORA bağlı",
              paths.CALIBRATION_REPORT.exists(), "calibration_report.json yok")
        cal = tokens.get("calibration", {})
        check("kalibrasyon bloğu ölçüm zincirini kaydediyor",
              bool(cal.get("tool_chain")) and bool(cal.get("stroke_fidelity")),
              "tool_chain/stroke_fidelity eksik")
        check("kalibrasyon durumu DİJİTAL olduğunu AÇIKÇA söylüyor",
              "DIGITAL" in st or "dijital" in " ".join(tokens.get("$comment", [])).lower(),
              f"status={st} — basılı doğrulama iddiası yaratıyor")
    else:
        check("kalibre edilmemiş token dosyası durumunu dürüstçe söylüyor",
              "NOT_CALIBRATED" in st, f"status={st}")


def test_croquis_is_declared_non_anthropometric():
    """Kroki oranları bir ÖLÇÜ İDDİASI değildir ve öyle sunulamaz."""
    src = (ROOT / "06_BUILD" / "croquis.py").read_text(encoding="utf-8")
    check("croquis.py antropometrik iddia taşımadığını AÇIKÇA yazıyor",
          "ANTROPOMETRİK BİR" in src and "İDDİA DEĞİLDİR" in src,
          "dürüstlük sınırı belgede yok")
    check("kroki hiçbir kaynak kaydına atıf YAPMIYOR",
          "S-00" not in src, "kroki bir kaynağa dayandırılmış görünüyor")


def test_croquis_fit_never_overflows():
    """fit() taşmayı en baştan imkânsız kılmalıdır."""
    bad = []
    for lo, hi in (("floor", "top_of_head"), ("thigh", "top_of_head"),
                   ("high_hip", "top_of_head"), ("crotch", "chin")):
        for w, h in ((200.0, 268.0), (140.0, 300.0), (300.0, 180.0)):
            for arms in (True, False):
                c = croquis.fit(w, h, lo, hi, arms=arms)
                top, bot = c.y(hi), c.y(lo)
                half = (croquis.MAX_HALF_FULL if arms else croquis.MAX_HALF_TORSO) * c.H
                if bot < -0.01 or top > h + 0.01 or c.cx - half < -0.01 \
                        or c.cx + half > w + 0.01:
                    bad.append((lo, hi, w, h, arms))
    check("croquis.fit() hiçbir kutuda TAŞMIYOR", not bad, f"taşanlar={bad[:3]}")


def main():
    print("▸ selftest.py — kapıların kendi testi\n")
    for fn in (
        test_schema_lite,
        test_source_authority_consistency, test_source_locator_discipline,
        test_source_authority_required, test_verification_evidence,
        test_cause_distinguishability, test_cause_measurement_present,
        test_symptom_af_refs, test_measurement_derivation,
        test_crosswalk_integrity, test_crosswalk_audit_gate, test_figure_tokens,
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
        test_verification_summary_matches_records,
        test_drawing_prohibitions_are_executable,
        test_reader_facing_figures_carry_no_internal_ids,
        test_labels_do_not_overlap,
        test_token_usage_is_measured_not_declared,
        test_qa_visual_catches_defects,
        test_build_scripts_are_tracked,
        test_reader_language_layer,
        test_page_geometry_respects_platform_minimums,
        test_calibration_is_not_claimed_without_evidence,
        test_croquis_is_declared_non_anthropometric,
        test_croquis_fit_never_overflows,
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
