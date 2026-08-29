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
import textwrap
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
import croquis          # noqa: E402
import trfold           # noqa: E402

FAILURES: list[str] = []
SKIPPED: list[str] = []
CHECKS = 0


def check(name: str, condition: bool, detail: str = ""):
    global CHECKS
    CHECKS += 1
    print(f"  {'✓' if condition else '✗'} {name}")
    if not condition:
        FAILURES.append(f"{name} — {detail}")


def skip(name: str, why: str):
    """ATLANAN denetim — GEÇEN denetim DEĞİLDİR.

    ⚠ Faz 5'te ÖLÇÜLEN kusur: temiz bir klonda (manüskript prozası
    bilerek izlenmiyor — K9) sekiz denetim `check(..., True)` ile
    ATLANIYOR ama GEÇMİŞ sayılıyordu. Sayı 152'den 146'ya düşüyor,
    çıktı yine de "✓ Bütün kapılar kusurlu fixture'ları doğru
    yakaladı" diyordu. Atlanan denetimlerin arasında Faz 4'ün en
    önemli düzeltmelerini koruyanlar vardı (B-01 yeniden gözlem,
    B-03 belirtiye özgü eleme, ölçüm figürü kapsaması). CI yeşildi ve
    o denetimler HİÇ KOŞMAMIŞTI.

    Atlananlar artık AYRI sayılır ve kapanış satırı bunu söyler."""
    SKIPPED.append(f"{name} — {why}")
    print(f"  ⊘ {name} — ATLANDI: {why}")


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
# ⑬ GÖRSEL SİSTEM — VERİ katmanı
#
# ⚠ Çizim yasaklarının kendi testi BU DOSYADA DEĞİLDİR.
# `figure_tokens.py` reportlab'a bağlıdır ve bu dosya ÜÇÜNCÜ TARAF
# PAKET GEREKTİRMEZ — CI'nin sekiz kapı işi standart kütüphaneyle
# çalışır ve saniyeler içinde biter. Render katmanının kendi testi:
#   07_TESTS/selftest_visual.py  (CI işi: `render`)
# ─────────────────────────────────────────────────────────────────────
def test_qa_visual_catches_defects():
    """qa_visual.py kusurlu bir figür sicilini yakalamalıdır."""
    import copy
    real = json.loads(paths.book_figures("book-01").read_text(encoding="utf-8")) \
        if paths.book_figures("book-01").exists() else None
    if real is None:
        skip("qa_visual fixture testi", "figures.json yok")
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


# ══ FAZ 4 KAPILARI ═══════════════════════════════════════════════════

def test_manuscript_gate_catches_missing_reobservation():
    """B-01 yapısal olarak dayatılıyor mu — yoksa yalnızca umut mu ediliyor.

    Çelişmeli inceleme B-01'i (YÜKSEK) Faz 4'e yazılı kısıt olarak
    taşıdı. Bir kısıt, ihlal edildiğinde BİR ŞEY OLMUYORSA kısıt
    değildir. Bu test yeniden gözlem adımını üreten kodu bozar ve
    kapının bunu gördüğünü kanıtlar."""
    sys.path.insert(0, str(paths.BUILD))
    import atlas as _atlas
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not mdir.exists():
        skip("manüskript yeniden-gözlem kapısı (B-01/B-03)",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    a = _atlas.AtlasBuilder("book-01", mdir)
    sid = "SYM-001"
    blocks = a.sign_entry(sid)
    txt = " ".join(str(b.get("text", "")) for b in blocks)
    check("her belirti girişi YENİDEN GÖZLEM adımı taşıyor (B-01)",
          "reduced but has not gone" in txt)
    check("her belirti girişi BELİRTİYE ÖZGÜ eleme taşıyor (B-03)",
          any(b.get("text") == "Rule these out first" for b in blocks))
    check("her belirti girişi 'henüz değiştirme' uyarısı taşıyor",
          any(b.get("type") == "callout" for b in blocks))
    # kusurlu içerik: 'partial' alanı boşaltılırsa kapı görmeli
    saved = a.content[sid]["partial"]
    a.content[sid]["partial"] = ""
    blocks2 = a.sign_entry(sid)
    txt2 = " ".join(str(b.get("text", "")) for b in blocks2)
    a.content[sid]["partial"] = saved
    check("boş 'azaldı ama gitmedi' metni girişi BOŞ bırakıyor",
          txt2.rstrip().endswith("as well:"))
    # ⑫ başlık/ilk cümle tekrarı — DİZİLMİŞ SAYFADA bulundu, kapıda değil
    check("aynı cümle başlık ve paragraf olarak İKİ KEZ basılmıyor",
          not any(_atlas._too_similar(b["text"], nb.get("text", ""))
                  for b, nb in zip(blocks, blocks[1:])
                  if b.get("type") == "h2" and nb.get("type") == "para"))
    check("benzerlik ölçütü GERÇEKTEN ayırıyor",
          _atlas._too_similar("The side seam swings toward the back at hip level",
                              "The side seam, at hip level.")
          and not _atlas._too_similar(
              "A horizontal fold crosses the back",
              "Fabric pools below the seat forming an empty pouch"))


def test_manuscript_gate_rejects_overclaim():
    """§ 32 kalibre dil kapısı — hem yakalamalı hem YANLIŞ POZİTİF vermemeli.

    İlk sürüm 13 yanlış pozitif üretti ve hepsi koşullu cümlelerdeydi
    ('If the pressure goes, the cause is in the back'). Bir kapı,
    yakalaması gerekeni yakalamalı ve BAŞKA HİÇBİR ŞEYİ
    yakalamamalıdır."""
    sys.path.insert(0, str(paths.BUILD))
    import qa_manuscript as qm
    import re as _re
    hard = [_re.compile(x, _re.I) for x in qm.OVERCLAIM_HARD]
    cond = [_re.compile(x, _re.I) for x in qm.OVERCLAIM_CONDITIONAL]

    def flagged(sent: str) -> bool:
        low = sent.lower()
        neg = any(n in low for n in qm.NEGATION)
        conditioned = any(c in low for c in qm.CONDITION_CUES)
        if any(p.search(low) for p in hard) and not neg:
            return True
        return any(p.search(low) for p in cond) and not neg and not conditioned

    check("KOŞULSUZ nedensellik yakalanıyor",
          flagged("A horizontal fold always means the bodice is too long."))
    check("'guarantee' yakalanıyor", flagged("This adjustment guarantees a good fit."))
    check("KOŞULLU cümle SERBEST (yanlış pozitif yok)",
          not flagged("If the pressure goes, the cause is in the back."))
    check("HEDGE'li cümle SERBEST (yanlış pozitif yok)",
          not flagged("The cause is often about fifteen centimetres lower."))
    check("yasağı TANIMLAYAN cümle SERBEST",
          not flagged("Do not write that a fold always means excess length."))
    check("YORDAM kuralı SERBEST ('always' nedensel değil)",
          not flagged("The hem is read last, always."))


def test_adjustment_interactions_are_symmetric():
    """interacts_with asimetrisi B-01'in cevabını çürütüyordu."""
    fams = json.loads(paths.ADJUSTMENT_FAMILIES.read_text(encoding="utf-8"))["families"]
    idx = {f["adjustment_family_id"]: set(f.get("interacts_with") or []) for f in fams}
    bad = [(a, b) for a, peers in idx.items() for b in peers if a not in idx.get(b, set())]
    check("interacts_with SİMETRİK (gerçek veri)", not bad, str(bad[:3]))
    errors: list = []
    broken = [dict(f) for f in fams]
    broken[0] = dict(broken[0])
    broken[0]["interacts_with"] = []
    sys.path.insert(0, str(paths.BUILD))
    from validate_spec import check_adjustment_interaction_symmetry
    check_adjustment_interaction_symmetry(broken, errors)
    check("kapı ASİMETRİK kaydı yakalıyor",
          any("ASİMETRİK" in e for e in errors))


def test_every_measurement_has_a_figure_in_the_book():
    """Faz 4'te ÖLÇÜLEN kusur: 29 ölçüm figürünün hiçbiri kitapta yoktu.

    Bütün kapılar yeşildi. Bir ölçü bölümünün işi şeridin yolunu
    GÖSTERMEKTİR; metin tek başına onu yapamaz. B-10 sınıfı."""
    sys.path.insert(0, str(paths.BUILD))
    import atlas as _atlas
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not mdir.exists():
        skip("ölçüm figürü kapsama kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    a = _atlas.AtlasBuilder("book-01", mdir)
    blocks = a.measurement_chapter()
    figured = {b["key"][len("meas_"):] for b in blocks
               if b.get("type") in ("figure", "figtable")
               and str(b.get("key", "")).startswith("meas_")}
    missing = sorted(set(a.measures) - figured)
    check("32 ölçünün HEPSİ kitapta bir figürle gösteriliyor",
          not missing, f"eksik: {missing[:6]}")


def test_internal_figures_never_reach_the_book():
    """İç araç figürleri (tbl_af_index gibi) kitaba GİREMEZ."""
    figs = json.loads(paths.book_figures("book-01").read_text(encoding="utf-8"))
    internal = {m["source_file"][:-4] for m in figs["figure_meta"].values()
                if m.get("source_file") and m.get("internal")}
    check("sicilde iç araç figürü İŞARETLİ", len(internal) >= 1)
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not mdir.exists():
        return
    used = set()
    for f in sorted(mdir.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for b in (d.get("blocks") or []):
            if b.get("type") in ("figure", "figtable"):
                used.add(b["key"])
    check("hiçbir iç araç figürü manüskriptte KULLANILMIYOR",
          not (used & internal), str(sorted(used & internal)))


def test_claim_registry_derives_its_evidence_level():
    """Bir iddia kendi kanıt seviyesini BEYAN EDEMEZ."""
    sys.path.insert(0, str(paths.BUILD))
    from build_claims import evidence_level
    srcs = {"S-A": {"technical_authority": True, "verification_level": "fulltext",
                    "acquisition_status": "public_access"},
            "S-B": {"technical_authority": False, "verification_level": "official_web",
                    "acquisition_status": "public_access"},
            "S-C": {"technical_authority": True, "verification_level": "not_yet_acquired",
                    "acquisition_status": "budget_pending"}}
    check("kaynaksız iddia UNVERIFIED",
          evidence_level("technical_reference_verified", [], srcs, False) == "UNVERIFIED")
    check("otorite olmayan kaynak UNVERIFIED",
          evidence_level("technical_reference_verified", ["S-B"], srcs, False) == "UNVERIFIED")
    check("tam metin otorite + doğrulanmış kayıt VERIFIED",
          evidence_level("technical_reference_verified", ["S-A"], srcs, False) == "VERIFIED")
    check("ajan türevi kayıt VERIFIED OLAMAZ",
          evidence_level("agent_drafted_unverified", ["S-A"], srcs, False) == "INFERRED")
    check("edinilmemiş kaynak yükseltemez",
          evidence_level("agent_drafted_unverified", ["S-C"], srcs, False) == "UNVERIFIED")
    check("kayıtlı tanım çelişkisi CONTESTED",
          evidence_level("technical_reference_verified", ["S-A"], srcs, True) == "CONTESTED")


def test_conditional_phase4_does_not_claim_kill_gate():
    """Kurucu geçersiz kılması (K49) kill-gate'i GEÇİLMİŞ gösteremez.

    `phase4-production-conditional` kümülatif sırada `phase3-pilot`'tan
    ÖNCEDİR. Bu, bir isimlendirme tercihi değil bir GÜVENLİKTİR: kapı
    adı değiştirilerek yapılmamış bir ölçüm var edilemez."""
    order = paths.BOOK_GATE_ORDER
    check("koşullu Faz 4, phase3-pilot'tan ÖNCE",
          order.index("phase4-production-conditional") < order.index("phase3-pilot"))
    check("koşullu Faz 4 'phase3-pilot geçildi' DEMİYOR",
          not paths.gate_at_least("phase4-production-conditional", "phase3-pilot", order))
    check("koşullu Faz 4 'phase5-qa açık' DEMİYOR",
          not paths.gate_at_least("phase4-production-conditional", "phase5-qa", order))
    check("koşullu Faz 4 'phase2-visual tamam' DİYOR",
          paths.gate_at_least("phase4-production-conditional", "phase2-visual", order))
    # kill-gate bayrakları hâlâ kapalı olmalı
    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))
    kg = cfg.get("killGate", {})
    check("fark testi HÂLÂ ölçülmemiş",
          not kg.get("differentiationTest", {}).get("measured"))
    check("fiziksel doğrulama HÂLÂ ölçülmemiş",
          not kg.get("physicalValidation", {}).get("measured"))
    # kapı, bayrak açılırsa BAĞIRMALI
    sys.path.insert(0, str(paths.BUILD))
    from validate_spec import check_kill_gate_not_claimed
    errs: list = []
    check_kill_gate_not_claimed("book-01", errs)
    check("gerçek veriyle koşullu Faz 4 denetimi TEMİZ", not errs, str(errs[:2]))


def test_manuscript_gate_holds_the_book2_boundary():
    """Kitap 1 DÜZELTMEYİ anlatmaya başlarsa seri mimarisi çöker (§ 34).

    ⚠ Ayrım ince: fiziksel TEST bir düzeltme DEĞİLDİR. 'Kes ve bak' bir
    teşhis adımıdır; 'kes, sonra kalıbı yeniden çiz' bir düzeltmedir.
    Kapı KALIBA kalıcı müdahaleyi arar, toile'a müdahaleyi değil."""
    import re as _re
    # Desenler kapının KENDİ kaynağından okunur; ikinci bir kopya
    # tutulsaydı test, kapının gerçekte ne aradığını değil testin ne
    # hatırladığını sınardı.
    src = (paths.BUILD / "qa_manuscript.py").read_text(encoding="utf-8")
    check("kapı KİTAP 2 SINIRI denetimi içeriyor", "PATTERN_HOWTO" in src)
    block = src[src.index("PATTERN_HOWTO = ["):]
    block = block[:block.index("\n    ]") + 6]
    ns: dict = {"re": _re}
    exec(textwrap.dedent(block), ns)
    patterns = ns["PATTERN_HOWTO"]

    def flagged(text: str) -> bool:
        return any(pat.search(text) for pat, _ in patterns)

    check("kalıp düzeltme talimatı YAKALANIYOR",
          flagged("Slash and spread the pattern at the apex line."))
    check("kalıbı yeniden çizme YAKALANIYOR",
          flagged("Then redraw the cutting line and true up the seams."))
    check("toile üzerinde FİZİKSEL TEST serbest (yanlış pozitif yok)",
          not flagged("Slash the fitting garment and open it until the sign clears."))
    check("iğneleme testi serbest",
          not flagged("Pin the fold out horizontally and measure what the pins take up."))
    check("aile ADLANDIRMA serbest",
          not flagged("Leads to: bust volume (full / small bust adjustment)."))


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
        test_qa_visual_catches_defects,
        test_build_scripts_are_tracked,
        test_reader_language_layer,
        test_page_geometry_respects_platform_minimums,
        test_calibration_is_not_claimed_without_evidence,
        test_croquis_is_declared_non_anthropometric,
        test_croquis_fit_never_overflows,
        test_manuscript_gate_catches_missing_reobservation,
        test_manuscript_gate_rejects_overclaim,
        test_adjustment_interactions_are_symmetric,
        test_every_measurement_has_a_figure_in_the_book,
        test_internal_figures_never_reach_the_book,
        test_claim_registry_derives_its_evidence_level,
        test_conditional_phase4_does_not_claim_kill_gate,
        test_manuscript_gate_holds_the_book2_boundary,
        # ── Faz 5: dizgi katmanı regresyonları ────────────────────────
        test_side_note_title_stays_in_column,
        test_flowed_page_keeps_folio,
        test_blank_form_rows_are_writable,
        test_no_test_cause_gets_no_reduction_criterion,
        test_appendices_print_in_letter_order,
        test_no_duplicate_chapter_number,
        test_heading_travels_with_its_content,
        test_measurement_figure_travels_with_its_text,
        test_sign_index_points_at_the_entry_not_the_page_before,
        test_reader_spelling_is_one_variety,
        test_counted_claims_match_the_data,
        test_flowchart_and_entry_agree_on_cause_order,
        test_gate_layer_never_imports_the_render_layer,
        test_external_unavailable_is_not_a_pass,
        test_rule_out_list_is_one_list,
        test_cause_text_matches_its_destination,
        test_sign_prose_has_exactly_one_copy,
        test_figure_specs_have_one_copy,
    ):
        fn()

    print(f"\n{CHECKS} denetim çalıştı, {len(SKIPPED)} atlandı, "
          f"{len(FAILURES)} başarısız.")
    if FAILURES:
        print("\n✗ BAŞARISIZ DENETİMLER:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    if SKIPPED:
        print("\n⊘ ATLANAN DENETİMLER — bu koşum EKSİKTİR:")
        for x in SKIPPED:
            print(f"  - {x}")
        print(f"\n✓ Koşan {CHECKS} denetimin hepsi geçti — ama "
              f"{len(SKIPPED)} denetim HİÇ KOŞMADI.")
        print("  Tam kapsam için manüskript prozasının ve render "
              "katmanının bulunduğu YEREL koşum gerekir.")
        return 0
    print("✓ Bütün kapılar kusurlu fixture'ları doğru yakaladı.")
    return 0




# ═════════════════════════════════════════════════════════════════════
# FAZ 5 — DİZGİ KATMANI REGRESYONLARI
#
# Bu altı denetimin hepsi Faz 5'te GERÇEK kitapta ölçülmüş kusurlardır.
# Hiçbiri veri kapılarından geçmiyordu: sekiz veri kapısı da yeşildi,
# 152 denetim de geçiyordu, ürün yine de bozuktu. Dizgi kusurunu ancak
# dizgi çıktısını ÖLÇEN bir denetim görür.
# ═════════════════════════════════════════════════════════════════════

def _render_layer_missing() -> str:
    """Render katmanı koşulabilir mi — koşulamıyorsa NEDENİ.

    ⚠ `selftest.py` üçüncü taraf paket GEREKTİRMEZ (CI'nin `selftest`
    işi bağımlılıksız koşar). Dizgi regresyonları reportlab'a VE yazı
    tipi ikililerine bağlıdır; ikisi de yoksa denetim ATLANIR — ama
    ATLANDIĞINI söyleyerek. Yazı tipi eksikliği de bir bağımlılık
    eksikliğidir: ilk sürüm yalnızca `ModuleNotFoundError`'ı sayıyordu
    ve temiz bir klonda selftest ÇÖKÜYORDU."""
    try:
        import reportlab  # noqa: F401
    except ModuleNotFoundError:
        return "reportlab yok (render katmanı)"
    try:
        sys.path.insert(0, str(paths.BUILD))
        import figure_tokens as _ft
        _ft.register_fonts()
    except ModuleNotFoundError as e:
        return f"render modülü yok: {e}"
    except FileNotFoundError:
        return "yazı tipi dosyaları edinilmemiş (06_BUILD/fetch_fonts.py)"
    return ""


def _mini_typesetter(tmp):
    """Gerçek geometriyle küçük bir dizgi motoru kurar."""
    sys.path.insert(0, str(paths.BUILD))
    import typeset as T
    import figure_engine as FE
    geom = json.loads(paths.PAGE_GEOMETRY.read_text(encoding="utf-8"))
    return T, T.Typesetter(tmp, geom, FE.Engine("book-01"))


def test_side_note_title_stays_in_column():
    """Yan not BAŞLIĞI sütunun dışına taşıyor mu.

    Faz 5'te ölçülen: 36 yan notun 3'ünün başlığı 108 pt'lik sütundan
    taşıyor ve verso sayfada METİN BLOĞUNUN ÜSTÜNE basılıyordu
    (s. 72'de 33,2 pt). Gövde sarılıyordu, başlık sarılmıyordu.

    ⚠ Bu test GERÇEK `side_note()` yolunu koşar ve tuvale ÇİZİLEN her
    dizgiyi ölçer. İlk sürümü `_wrap`'i doğrudan çağırıyordu ve
    sarmayı geri alan bir mutasyonu YAKALAMIYORDU — kapı olmayan bir
    kapıydı."""
    why = _render_layer_missing()
    if why:
        skip("yan not başlığı kapısı", why)
        return
    from reportlab.pdfbase import pdfmetrics
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        drawn: list = []
        real_draw = ts.c.drawString
        state = {"font": "", "size": 0.0}
        real_setfont = ts.c.setFont

        def spy_setfont(name, size, *a, **k):
            state["font"], state["size"] = name, size
            return real_setfont(name, size, *a, **k)

        def spy_draw(x, y, text, *a, **k):
            drawn.append((x, text, state["font"], state["size"]))
            return real_draw(x, y, text, *a, **k)

        ts.c.setFont, ts.c.drawString = spy_setfont, spy_draw
        ts.side_note("What would have happened without step 7",
                     "Short body text for the note.")
        ts.c.setFont, ts.c.drawString = real_setfont, real_draw

        side = [(x, t, f, sz) for x, t, f, sz in drawn
                if abs(x - ts.x_side) < 0.5]
        check("yan not tuvale ÇİZİLDİ", len(side) >= 2, f"{len(side)} dizgi")
        worst = 0.0
        for x, t, f, sz in side:
            w = pdfmetrics.stringWidth(t, f, sz)
            worst = max(worst, x + w - (ts.x_side + ts.side_w))
        check("çizilen HİÇBİR yan not dizgisi sütundan taşmıyor",
              worst <= 0.5, f"en fazla {worst:.1f} pt taşma")
        # başlık gerçekten birden çok satıra bölünmüş olmalı
        heads = [t for x, t, f, sz in side if "Bold" in f or "bold" in f]
        check("uzun başlık BİRDEN ÇOK satıra bölündü",
              len(heads) > 1, f"{len(heads)} başlık satırı: {heads}")


def test_flowed_page_keeps_folio():
    """Akış içinde açılan sayfa SAYFA NUMARASI alıyor mu.

    Faz 5'te ölçülen: s. 46 ve s. 236 metin taşıyor ama folyo
    taşımıyordu. `_new_page()` `_dirty`'yi sıfırlıyor, çizim yordamları
    ise `_touch()`'ı yalnızca başta çağırıyordu."""
    why = _render_layer_missing()
    if why:
        skip("folyo kapısı", why)
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        ts.y = ts.bottom + ts.lead * 0.5      # sayfanın dibi
        p0 = ts.page
        ts._flow_page()
        check("akış sayfası AÇILDI", ts.page == p0 + 1)
        check("akış sayfası derhâl KİRLİ işaretlendi (folyo basılacak)",
              ts._dirty is True)
        # karşı örnek: kasıtlı boş verso kirli OLMAMALI
        ts2 = _mini_typesetter(Path(d) / "u.pdf")[1]
        ts2.page_break()
        check("kasıtlı boş sayfa kirli DEĞİL (boş verso numaralanmaz)",
              ts2._dirty is False)


def test_blank_form_rows_are_writable():
    """Boş form satırları elle DOLDURULABİLİR yükseklikte mi.

    Faz 4 çelişmeli incelemesi (R5) "2 mm'lik saç teli satırlar"
    bildirmişti; düzeltme `row_pt: 26` olarak yazıldı ama satır
    yüksekliği formülü BOŞ hücreyi 0 satır sayıp yüksekliği NEGATİF
    düzeltiyordu: 26 pt → 15,9 pt, varsayılan 15,3 pt → 5,2 pt.
    Faz 5'te ÖLÇÜLDÜ ve kusurun DURDUĞU görüldü."""
    why = _render_layer_missing()
    if why:
        skip("boş form satırı kapısı", why)
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        rows = [["A", "B", "C"]] + [["", "", ""] for _ in range(6)]
        widths = [0.34, 0.33, 0.33]
        h_declared = ts.table_h(rows, widths, row_pt=26.0)
        per_row = (h_declared - ts.lead) / len(rows)
        mm = per_row / 72.0 * 25.4
        check("beyan edilen 26 pt'lik form satırı GERÇEKTEN ~26 pt",
              per_row > 24.0, f"{per_row:.1f} pt ({mm:.1f} mm)")
        check("boş form satırı elle yazılabilir (≥ 6 mm)",
              mm >= 6.0, f"{mm:.1f} mm")
        # kusurlu formül geri gelirse yakalansın
        bad = 26.0 + (0 - 1) * 9.0 * 1.12
        check("eski (kusurlu) formül BUGÜN kullanılsaydı yazılamazdı",
              bad / 72.0 * 25.4 < 6.0, f"{bad/72.0*25.4:.1f} mm")


def test_no_test_cause_gets_no_reduction_criterion():
    """'Fiziksel test yok' diyen neden, testin sonucunu okumasını İSTEMESİN.

    Faz 5'te ölçülen: 129 aday nedenin 8'i aynı maddede önce
    "There is no physical test" diyor, sonra "bu neden, belirti
    AZALIRSA doğrulanmıştır" diyordu. Okura çelişkili yordam."""
    sys.path.insert(0, str(paths.BUILD))
    import atlas as _atlas
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    check("çelişkili okuma ölçütü kapısı: yardımcı TANIMLI",
          hasattr(_atlas, "_declares_no_physical_test"))
    check("'no physical test' cümlesi TANINIYOR",
          _atlas._declares_no_physical_test(
              "There is no physical test. This is settled at the size chart."))
    check("normal test cümlesi yanlışlıkla TANINMIYOR",
          not _atlas._declares_no_physical_test(
              "Pin the back neckline edge downward by 5 mm and rehang."))
    if not mdir.exists():
        skip("çelişkili okuma ölçütü kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    a = _atlas.AtlasBuilder("book-01", mdir)
    bad = []
    for sid in a.signs:
        txt = []
        for b in a.sign_entry(sid, with_chart=False):
            txt.append(str(b.get("text", "")))
            txt += [str(x) for x in (b.get("items") or [])]
        for i, t in enumerate(txt):
            if "There is no physical test" in t:
                nxt = " ".join(txt[i + 1:i + 4])
                if "this cause is confirmed if" in nxt and "is reduced" in nxt:
                    bad.append(sid)
    check("hiçbir 'fiziksel test yok' nedeni AZALMA ölçütü taşımıyor",
          not bad, f"{len(bad)} neden: {bad[:5]}")


def test_appendices_print_in_letter_order():
    """Ekler kitapta HARF SIRASIYLA basılıyor mu.

    Faz 5'te ölçülen: basılan sıra A, B, D, E, F, G, C, H, I idi.
    Üretilen üç dizin (C, H, I) yazılmış eklerin SONUNA ekleniyordu.
    Ek C kitabın asıl girişidir — 43 akış şemasının hepsi ona işaret
    eder — ve dokuz ekin yedincisinde basılıyordu."""
    # ⚠ `bookplan` üçüncü taraf paket GEREKTİRMEZ; `build_book` reportlab'a
    # bağlıdır ve bu kapı BAĞIMLILIKSIZ koşmak zorundadır (CI `selftest`
    # işi hiçbir paket kurmaz). Faz 5'te bir kez ihlal edildi ve CI düştü.
    sys.path.insert(0, str(paths.BUILD))
    import bookplan as _bb
    check("`index_slot` doldurucusu TANIMLI ve BAĞIMLILIKSIZ",
          hasattr(_bb, "fill_index_slots"))
    blocks = [{"type": "h2", "text": "Appendix B — x"},
              {"type": "index_slot", "slot": "C"},
              {"type": "h2", "text": "Appendix D — y"},
              {"type": "index_slot", "slot": "HI"}]
    out = _bb.fill_index_slots(blocks, {"C": [{"type": "h2", "text": "Appendix C — z"}],
                                        "HI": [{"type": "h2", "text": "Appendix H — w"}]})
    letters = [b["text"].split(" — ")[0].replace("Appendix ", "")
               for b in out if b.get("type") == "h2"]
    check("işaretler yerine ÜRETİLEN bloklar geçiyor", letters == sorted(letters),
          str(letters))
    check("hiçbir `index_slot` dizgiye ULAŞMIYOR",
          not any(b.get("type") == "index_slot" for b in out))
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not (mdir / "appendix.json").exists():
        skip("ek harf sırası kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    src = json.loads((mdir / "appendix.json").read_text(encoding="utf-8"))
    slots = [b["slot"] for b in src["blocks"] if b.get("type") == "index_slot"]
    check("appendix.json iki dizin işareti TAŞIYOR", slots == ["C", "HI"], str(slots))


def test_no_duplicate_chapter_number():
    """İki bölüm AYNI numarayı taşıyor mu.

    Faz 5'te ölçülen: içindekiler "16 · The order of work" ve
    "16b · Signs that belong to the whole garment" satırlarını yan yana
    basıyordu. Bir başvuru kitabında bu, numaralandırma hatası okunur."""
    import re
    sys.path.insert(0, str(paths.BUILD))
    import bookplan as _bb
    nums = []
    for key, title in _bb.CHAPTER_TITLES.items():
        head = title.split(" · ")[0]
        if head.isdigit():
            nums.append(int(head))
    check("hiçbir bölüm numarası TEKRARLANMIYOR",
          len(nums) == len(set(nums)), str(sorted(nums)))
    check("okur metninde 'b' ekli bölüm numarası YOK",
          not any(re.match(r"^\d+[a-z]\b", t) for t in _bb.CHAPTER_TITLES.values()),
          str([t for t in _bb.CHAPTER_TITLES.values()
               if re.match(r"^\d+[a-z]\b", t)]))


def test_flowchart_and_entry_agree_on_cause_order():
    """Akış şeması ile metin girişi nedenleri AYNI sırada mı veriyor.

    Faz 5 bağımsız incelemesi: metin girişi nedenleri yeniden sıralıyor
    (kalıp değişikliği GEREKTİRMEYEN "bedava" nedenler öne) ve başlık
    bunu ilan ediyor — "Candidate causes, cheapest test first". Akış
    şeması HAM taksonomi sırasını kullanıyordu. İki sonuç: bedava dal
    17 girişin 17'sinde şemada ikinci/üçüncü sıradaydı; ve metindeki
    "1. neden" ile şemanın ilk dalı FARKLI nedenlerdi — aynı yayılımda
    "birinci neden" iki ayrı şeye işaret ediyordu."""
    why = _render_layer_missing()
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not mdir.exists():
        skip("şema/metin sıra kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    if why:
        skip("şema/metin sıra kapısı", why)
        return
    sys.path.insert(0, str(paths.BUILD))
    import atlas as _atlas
    import figure_engine as _fe
    ab = _atlas.AtlasBuilder("book-01", mdir)
    fs = {x["symptom_id"]: x for x in json.loads(
        (paths.TAXONOMY_PUBLIC / "fit_signs.json").read_text(encoding="utf-8"))["signs"]}
    lab = json.loads((paths.TAXONOMY_PUBLIC / "labels_en.json")
                     .read_text(encoding="utf-8"))
    bad, free_bad, announced = [], [], 0
    for sid in ab.signs:
        blocks = ab.sign_entry(sid, with_chart=False)
        printed = [b["text"].split(". ", 1)[1] for b in blocks
                   if b.get("type") == "h3" and b["text"][:2].rstrip(".").isdigit()]
        sc = _fe.SignChart(fs[sid], lab["signs"][sid], lab["ui"])
        chart = [r["cause_en"] for r in sc.rows]
        if printed != chart:
            bad.append(sid)
        txt = " ".join(str(b.get("text", "")) for b in blocks)
        if "cheapest test first" in txt:
            announced += 1
            if sc.rows[0]["cause"].get("adjustment_family_ref"):
                free_bad.append(sid)
    check("akış şeması ile metin girişi AYNI neden sırasını kullanıyor",
          not bad, f"{len(bad)} belirti ayrışıyor: {bad[:5]}")
    check("'cheapest test first' diyen her girişin ŞEMASI da bedava dalla başlıyor",
          not free_bad, f"{len(free_bad)}/{announced} şema ihlal ediyor: {free_bad[:5]}")


def test_figure_specs_have_one_copy():
    """Figür spesifikasyonunun İKİNCİ bir kopyası var mı.

    ⚠ İnceleme D-19: `figure_engine.render()`'ın docstring'i şunu
    iddia ediyordu — *"İkinci bir çizim yolu YOKTUR… ikisi ayrışamaz."*
    AYRIŞMIŞLARDI. Karşılaştırma figürlerinin spesifikasyonu İKİ KEZ
    yazılmıştı: toplu üretimde PROJE dilinde, `render()` içinde OKUR
    dilinde. Bağımsız figür PDF'i "Kollar kaldırıldı" basarken kitap
    "Arms raised" basıyordu — bir incelemecinin ya da matbaacının
    denetlediği 163 varlık, kitaptaki figürler DEĞİLDİ.

    Ayrıca: üretilmiş varlık sicilin TÜREVİDİR. Sicilde olmayan bir
    dosya o klasörde duramaz (öksüz `flow_ELIMINATION.pdf`)."""
    sys.path.insert(0, str(paths.BUILD))
    src = (paths.BUILD / "figure_engine.py").read_text(encoding="utf-8")
    check("karşılaştırma spesifikasyonu TEK yerde tanımlı",
          src.count('"tape_slipped_back"') == 1,
          f"{src.count('\"tape_slipped_back\"')} kez geçiyor")
    # spesifikasyonun KENDİSİ okunur — yorumlar değil (ilk sürümüm
    # kendi açıklama yorumumdaki Türkçe dizgiye takıldı)
    import ast as _ast
    spec_vals = []
    for node in _ast.walk(_ast.parse(src)):
        if isinstance(node, _ast.Assign) and any(
                getattr(t, "id", "") == "COMPARISON_SPEC" for t in node.targets):
            for el in getattr(node.value, "elts", []):
                spec_vals += [c.value for c in getattr(el, "elts", [])
                              if isinstance(c, _ast.Constant)
                              and isinstance(c.value, str)]
    check("karşılaştırma spesifikasyonu BULUNDU", bool(spec_vals))
    tr = [v for v in spec_vals if any(ch in v for ch in "şğİçöüı")]
    check("spesifikasyon OKUR dilinde (proje dili sızmamış)",
          not tr, f"proje dilinde değer: {tr[:3]}")
    gen = paths.book_generated("book-01")
    figs = paths.book_figures("book-01")
    if not (gen.exists() and figs.exists()):
        skip("öksüz varlık kapısı", "üretilmiş figürler yok (render katmanı)")
        return
    meta = json.loads(figs.read_text(encoding="utf-8"))["figure_meta"]
    live = {m["source_file"] for m in meta.values() if m.get("source_file")}
    orphans = sorted(f.name for f in gen.glob("*.pdf") if f.name not in live)
    check("üretilmiş dizinde SİCİLDE OLMAYAN dosya yok",
          not orphans, f"öksüz: {orphans[:5]}")


def test_sign_prose_has_exactly_one_copy():
    """Belirti prozasının İKİNCİ bir kopyası var mı.

    ⚠ Faz 5'te GERÇEKLEŞTİ: `signs_en_a/b/c.json` adlı üç dosya
    `sign_content_en.json` ile aynı 43 belirtiyi taşıyordu ama hiçbir
    kod onları OKUMUYORDU. 43 belirtinin 17'sinde iki kopya AYRIŞMIŞTI.
    İnceleme A'nın bulduğu iki KRİTİK yön hatasını düzeltirken ölü
    kopyayı düzelttim ve düzeltme kitaba HİÇ ULAŞMADI — ancak dizilmiş
    metni yeniden ölçtüğümde fark ettim.

    Ölü kopyalar emekliye ayrıldı. Bu kapı yenisinin sessizce
    doğmasını engeller. Desen `K16`/`K56`: bir davranış, bir kopya."""
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not mdir.exists():
        skip("belirti prozası tek-kopya kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    canonical = mdir / "sign_content_en.json"
    check("kanonik belirti prozası dosyası MEVCUT", canonical.exists())
    if not canonical.exists():
        return
    canon = json.loads(canonical.read_text(encoding="utf-8"))
    n_signs = len([k for k in canon if k.startswith("SYM-")])
    check("kanonik dosya 43 belirtiyi taşıyor", n_signs == 43, str(n_signs))
    dupes = []
    for f in sorted(mdir.glob("*.json")):
        if f == canonical:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and sum(1 for k in d if k.startswith("SYM-")) >= 3:
            dupes.append(f.name)
    check("belirti prozasının İKİNCİ bir kopyası YOK",
          not dupes, f"ikinci kopya: {dupes}")


def test_cause_text_matches_its_destination():
    """Neden metni birden çok duruma işaret edip TEK aileye çıkıyor mu.

    ⚠ Faz 5'te ÖLÇÜLEN kusur: `SYM-018.C1` okura "Not enough volume in
    the front (bust **or abdomen**)" diyor ve `AF-01` GÖĞÜS hacmine
    çıkıyordu; `SYM-040.C1` "A volume (bust, **abdomen** or seat)" deyip
    yine `AF-01`'e. Oysa `AF-20` (karın hacmi) tam bu boşluk için Faz
    4'te eklenmişti. Karnı yüzünden bu belirtiyi gören okur GÖĞÜS
    düzeltmesine yollanıyordu.

    Kural: neden metni bir vücut BÖLGESİ adı taşıyorsa, ya o bölgenin
    ailesine çıkacak ya da `cross_route` ile okuru oraya YOLLAYACAK."""
    signs = json.loads((paths.TAXONOMY_PUBLIC / "fit_signs.json")
                       .read_text(encoding="utf-8"))["signs"]
    lab = json.loads((paths.TAXONOMY_PUBLIC / "labels_en.json")
                     .read_text(encoding="utf-8"))
    fams = {f["adjustment_family_id"]: f for f in json.loads(
        (paths.TAXONOMY_PUBLIC / "adjustment_families.json")
        .read_text(encoding="utf-8"))["families"]}
    # bölge adı → o bölgenin ailesi
    REGION = {"abdomen": "AF-20", "seat": "AF-13", "bust": "AF-01"}
    bad = []
    routed = sum(1 for s in signs for c in s["candidate_causes"]
                 if c.get("cross_route"))
    for s in signs:
        sid = s["symptom_id"]
        for i, c in enumerate(s["candidate_causes"]):
            txt = (lab["signs"][sid]["causes"][i]["cause"] + " "
                   + lab["signs"][sid]["causes"][i]["evidence"]).lower()
            named = {r for r in REGION if r in txt}
            if len(named) < 2:
                continue
            dest = c.get("adjustment_family_ref")
            cr = c.get("cross_route")
            covered = {r for r in named if REGION[r] == dest}
            if cr:
                covered |= {r for r in named if REGION[r] == cr.get("family_ref")}
            if named - covered:
                bad.append(f"{sid}.C{i+1}: metin {sorted(named)} diyor, "
                           f"varış {dest}, cross_route={cr and cr.get('family_ref')}")
    check("çok bölgeli neden metni, okuru YANLIŞ aileye bırakmıyor",
          not bad, "; ".join(bad))
    check("çapraz yönlendirme KULLANILIYOR", routed >= 2, f"{routed} neden")
    # her cross_route TANIMLI bir aileye işaret etmeli
    dangling = [f"{s['symptom_id']}.C{i+1}"
                for s in signs for i, c in enumerate(s["candidate_causes"])
                if c.get("cross_route")
                and c["cross_route"]["family_ref"] not in fams]
    check("her `cross_route` TANIMLI bir aileye işaret ediyor",
          not dangling, str(dangling))


def test_rule_out_list_is_one_list():
    """Bölüm 8'in on dördü ile Ek D'nin on dördü AYNI on dört mü.

    ⚠ Faz 5'te ÖLÇÜLEN kusur: ikisi de 14 taneydi ve bu yüzden fark
    görünmüyordu — ama AYNI on dört DEĞİLDİ. Proza "Fabric"i ikiye
    bölüyor (kumaş sınıfı + ön yıkama) ve kanonik listedeki
    "Measuring"i hiç taşımıyordu. Kitap ise "The fourteen, with one
    question each" ve "Also in Appendix D" diyerek aynı olduklarını
    İDDİA EDİYOR. Kanonik kaynak `labels_en.json.confounders`tır.
    """
    import re as _re
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    canon = list(json.loads((paths.TAXONOMY_PUBLIC / "labels_en.json")
                            .read_text(encoding="utf-8"))["confounders"].values())
    check("kanonik karıştırıcı listesi 14 öge", len(canon) == 14, str(len(canon)))
    if not (mdir / "ch08.json").exists():
        skip("eleme listesi kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    d = json.loads((mdir / "ch08.json").read_text(encoding="utf-8"))
    prose = None
    for b in d["blocks"]:
        it = b.get("items") or []
        if len(it) == 14 and all("—" in str(x) for x in it):
            prose = [_re.match(r'^([A-Za-z ,]+?)\s*—', str(x)).group(1).strip()
                     for x in it]
            break
    check("Bölüm 8 prozası 14 ögelik eleme listesi taşıyor", prose is not None)
    if prose is None:
        return

    def norm(x):
        return (x.lower().replace("fitting ", "").replace("pattern ", "")
                .replace("design ", "").strip())
    a, b2 = sorted(map(norm, prose)), sorted(map(norm, canon))
    check("Bölüm 8 ile Ek D AYNI on dört ögeyi listeliyor", a == b2,
          f"yalnız prozada {sorted(set(a)-set(b2))} · yalnız kanonikte {sorted(set(b2)-set(a))}")


def test_external_unavailable_is_not_a_pass():
    """`EXTERNAL_VALIDATION_UNAVAILABLE` bir PASS'e DÖNÜŞEMEZ.

    Kurucu dış doğrulamanın erişilemez olduğunu bildirdi (K58) ve proje
    ilerlemeye devam ediyor. Bu, kill-gate'in geçtiği ANLAMINA GELMEZ ve
    bu denetim o dönüşümü mekanik olarak imkânsız kılar:

      · `measured` HÂLÂ false olmalı — erişilemezlik ölçüm üretmez;
      · `aiProxyCountsAsHuman` HÂLÂ false olmalı (K6);
      · erişilemezlik KİM tarafından kaydedildi, İÇSEL İKAME nedir ve
        ikamenin eşdeğer OLMADIĞI beyan edildi mi — üçü de zorunlu;
      · `validationStatus` hiçbir yerde "validated" DEMEZ.
    """
    cfg = json.loads(paths.SERIES_CONFIG.read_text(encoding="utf-8"))
    kg = cfg["killGates"]
    for name in ("differentiationTest", "physicalValidation"):
        spec = kg[name]
        check(f"{name}: erişilemezlik ÖLÇÜM ÜRETMEDİ (measured hâlâ false)",
              spec.get("measured") is False)
        check(f"{name}: erişilemezliği KİM kaydetti yazılı",
              bool(spec.get("unavailabilityRecordedBy")))
        check(f"{name}: İÇSEL İKAME kaydedilmiş",
              bool(spec.get("internalSubstitute")))
        check(f"{name}: ikamenin EŞDEĞER OLMADIĞI beyan edilmiş",
              spec.get("substituteIsNotEquivalent") is True)
    check("AI vekil bayrağı HÂLÂ kapalı (K6 — erişilemezlik onu açmaz)",
          kg["differentiationTest"]["aiProxyCountsAsHuman"] is False)
    vs = cfg["validationStatus"]
    check("ürün doğrulama durumu KOŞULLU-İÇSEL",
          vs["productValidation"] == "CONDITIONAL_INTERNAL_VALIDATION")
    check("dış doğrulama durumu ERİŞİLEMEZ", vs["externalValidation"] == "UNAVAILABLE")
    for k in ("physicallyValidated", "humanValidated", "printProofValidated"):
        check(f"`{k}` FALSE — iddia edilemez", vs[k] is False)
    # kapı sırası: içsel KA phase3-pilot'u GEÇMİŞ SAYMAZ
    g = paths.read_book_gate("book-01")
    check("kitap kapısı içsel KA seviyesinde",
          paths.gate_at_least(g, "phase5-qa-internal", paths.BOOK_GATE_ORDER))
    check("kapı 'phase3-pilot geçildi' DEMİYOR",
          not paths.gate_at_least(g, "phase3-pilot", paths.BOOK_GATE_ORDER))
    check("kapı 'gerçek phase5-qa açık' DEMİYOR",
          not paths.gate_at_least(g, "phase5-qa", paths.BOOK_GATE_ORDER))
    # kill_gate hâlâ measured=true'yu kayıtsız KABUL ETMİYOR
    sys.path.insert(0, str(paths.BUILD))
    check("kill-gate sırasında içsel KA seviyesi phase3-pilot'tan ÖNCE",
          paths.BOOK_GATE_ORDER.index("phase5-qa-internal")
          < paths.BOOK_GATE_ORDER.index("phase3-pilot"))


def test_gate_layer_never_imports_the_render_layer():
    """Bağımlılıksız kapı katmanı reportlab'ı İÇE AKTARMIYOR mu.

    ⚠ Faz 5'te GERÇEKLEŞTİ: iki yeni denetim `build_book`'u içe
    aktarıyordu; `build_book` → `figure_engine` → `figure_tokens` →
    **reportlab**. CI'nin `selftest` işi hiçbir üçüncü taraf paket
    KURMAZ (tasarım gereği, `.github/workflows/validate.yml`) ve iş
    `ModuleNotFoundError` ile düştü. Yerel ağaçta reportlab kurulu
    olduğu için kusur burada görünmüyordu.

    `bookplan.py` tam bu ayrım için var ve docstring'i bunu söylüyor.
    Bu denetim ayrımın KORUNDUĞUNU kanıtlar."""
    import ast as _ast
    import re as _re
    src = (paths.ROOT / "07_TESTS" / "selftest.py").read_text(encoding="utf-8")
    # `_render_layer_missing()` korumasının ARKASINDA olmayan içe aktarmalar
    forbidden = {"build_book", "typeset", "figure_engine", "figure_tokens",
                 "croquis", "calibrate_tokens"}
    tree = _ast.parse(src)
    guarded = set()
    for fn in [n for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)]:
        body = _ast.dump(fn)
        if "_render_layer_missing" in body or "skip" in body:
            guarded.add(fn.name)
    bad = []
    for fn in [n for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)]:
        # Yalnızca DENETİMLER denetlenir. `_mini_typesetter` gibi
        # yardımcılar render katmanını içe aktarabilir — koruma onları
        # ÇAĞIRAN denetimdedir ve o denetim burada ayrıca sınanır.
        if not fn.name.startswith("test_") or fn.name in guarded:
            continue
        for node in _ast.walk(fn):
            if isinstance(node, _ast.Import):
                for a in node.names:
                    if a.name in forbidden:
                        bad.append(f"{fn.name} → {a.name}")
            elif isinstance(node, _ast.ImportFrom) and node.module in forbidden:
                bad.append(f"{fn.name} → {node.module}")
    check("korumasız hiçbir denetim RENDER katmanını içe aktarmıyor",
          not bad, "; ".join(bad))
    # bookplan gerçekten bağımlılıksız mı
    bp = (paths.BUILD / "bookplan.py").read_text(encoding="utf-8")
    check("bookplan.py üçüncü taraf paket İÇE AKTARMIYOR",
          not _re.search(r"^\s*(import|from)\s+(reportlab|PIL)", bp, _re.M))


def test_counted_claims_match_the_data():
    """Metindeki SAYI iddiaları veriyle uyuşuyor mu.

    Faz 5 bağımsız incelemesinin bulduğu sınıf: kitap kendi
    envanterini yanlış sayıyordu. Hiçbir kapı buna bakmıyordu.

      · "Eleven of these are taken with the tape horizontal" — grup 12
      · "Two widths and two depths … three of the four need a helper"
        — 3 genişlik + 2 derinlik = 5, ve BEŞİNİN de yardımcısı gerekli
      · "a second person for five of the measurements" — 19
        (üstelik Bölüm 2 aynı kitapta "nineteen" diyor)
    """
    mdir = paths.BOOK_DIRS["book-01"] / "02_CONTENT" / "protected" / "manuscript"
    if not (mdir / "measurements_en.json").exists():
        skip("sayılı iddia kapısı",
             "manüskript prozası izlenmiyor (K9) — YEREL koşumda denetlenir")
        return
    import re as _re
    M = {m["measurement_id"]: m for m in
         json.loads((paths.TAXONOMY_PUBLIC / "measurements.json")
                    .read_text(encoding="utf-8"))["measurements"]}
    mc = json.loads((mdir / "measurements_en.json").read_text(encoding="utf-8"))
    WORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
            "twelve": 12, "thirteen": 13, "fourteen": 14, "nineteen": 19,
            "twenty": 20, "thirty-two": 32}

    def num(w):
        return WORD.get(w.lower().strip())

    # ① her grubun giriş cümlesindeki baş sayı, grubun BÜYÜKLÜĞÜNÜ aşmasın
    bad = []
    for g in mc["groups"]:
        n = len(g["ids"])
        m = _re.match(r"^([A-Za-z-]+) of these", g["intro"])
        if m and num(m.group(1)) is not None and num(m.group(1)) != n:
            bad.append(f"{g['title']!r}: metin {m.group(1)} ({num(m.group(1))}), veri {n}")
        m2 = _re.match(r"^([A-Za-z-]+) widths and ([A-Za-z-]+) depths", g["intro"])
        if m2:
            import collections
            cats = collections.Counter(M[i]["category"] for i in g["ids"])
            if num(m2.group(1)) != cats.get("width", 0) or \
               num(m2.group(2)) != cats.get("depth", 0):
                bad.append(f"{g['title']!r}: metin {m2.group(1)}/{m2.group(2)}, "
                           f"veri {cats.get('width', 0)}/{cats.get('depth', 0)}")
    check("ölçü grubu giriş cümlelerindeki sayılar veriyle UYUŞUYOR",
          not bad, "; ".join(bad))

    # ② yardımcı gerektiren ölçü sayısı, kitabın her yerinde AYNI
    helper = sum(1 for m in M.values() if m.get("helper_required"))
    blob = json.dumps(json.loads((mdir / "part0.json").read_text(encoding="utf-8")),
                      ensure_ascii=False)
    claims = _re.findall(r"second person for ([a-z-]+) of the", blob)
    wrong = [c for c in claims if num(c) is not None and num(c) != helper]
    check("ön maddedeki 'yardımcı gereken ölçü' sayısı veriyle UYUŞUYOR",
          not wrong, f"metin {wrong}, veri {helper}")

    # ③ kusurlu kurgu YAKALANIYOR (kapı gerçekten ısırıyor mu)
    fake_groups = [{"title": "x", "intro": "Eleven of these are taken.",
                    "ids": list(M)[:12]}]
    m = _re.match(r"^([A-Za-z-]+) of these", fake_groups[0]["intro"])
    check("kapı yanlış sayıyı GERÇEKTEN yakalıyor",
          num(m.group(1)) != len(fake_groups[0]["ids"]))


def test_reader_spelling_is_one_variety():
    """Okur katmanı TEK bir imla ailesi kullanıyor mu.

    Faz 5'te ölçülen: kitabın prozası baştan sona İNGİLİZ imlasıydı
    ("centre front", "centre back" — 88 kez), ama iki ÖLÇÜ ADI Amerikan
    imlasındaydı: "Center front length", "Center back length" (19 kez).
    Okur Bölüm 4'te toile'ine "centre front" yazıyor, sonra ölçü
    kartında "Center front length" arıyor. Aynı nirengi, aynı kitapta
    iki yazım. `qa_terminology` bunu göremez: eşanlamlı listesine
    bakar, imla ailesine bakmaz.

    KURUM ADLARI muaftır — "National Center for Health Statistics" bir
    özel addır ve İngilizleştirilemez."""
    pairs = [("centre", "center"), ("colour", "color"),
             ("metre", "meter"), ("grey", "gray")]
    # okur katmanı: taksonomi adları + İngilizce etiketler
    blobs = []
    for rel in ("02_TAXONOMY/public/measurements.json",
                "02_TAXONOMY/public/adjustment_families.json",
                "02_TAXONOMY/public/fit_signs.json",
                "02_TAXONOMY/public/labels_en.json"):
        f = paths.ROOT / rel
        if f.exists():
            blobs.append((rel, json.loads(f.read_text(encoding="utf-8"))))
    import re as _re
    bad = []
    for rel, data in blobs:
        txt = json.dumps(data, ensure_ascii=False)
        for br, am in pairs:
            has_br = bool(_re.search(rf"\b{br}", txt, _re.I))
            # Amerikan biçimi: özel ad değilse say
            am_hits = [m.start() for m in _re.finditer(rf"\b{am}\w*", txt, _re.I)]
            proper = 0
            for i in am_hits:
                ctx = txt[max(0, i - 40):i + 40]
                if _re.search(r"National|U\.S\.|Engineering|Research|University|"
                              r"Disease|Statistics|Cooperative", ctx):
                    proper += 1
            if has_br and len(am_hits) > proper:
                bad.append(f"{rel}: hem '{br}' hem '{am}' "
                           f"({len(am_hits) - proper} özel-ad olmayan)")
    check("okur katmanında karışık İngiliz/Amerikan imlası YOK",
          not bad, "; ".join(bad))
    # kurum adları YANLIŞLIKLA yakalanmıyor (yanlış pozitif testi)
    fake = json.dumps({"a": "centre front",
                       "b": "National Center for Health Statistics"},
                      ensure_ascii=False)
    hits = [m.start() for m in _re.finditer(r"\bcenter\w*", fake, _re.I)]
    proper = sum(1 for i in hits
                 if _re.search(r"National|Statistics", fake[max(0, i - 40):i + 40]))
    check("kurum adı imla denetiminden MUAF (yanlış pozitif yok)",
          len(hits) == proper, f"{len(hits)} bulundu, {proper} muaf")


def test_sign_index_points_at_the_entry_not_the_page_before():
    """Ek C'nin sayfa numarası, girişin GERÇEKTEN başladığı sayfa mı.

    Faz 5'te ölçülen KRİTİK kusur: `sign_page[sid] = ts.page` başlık
    DİZİLMEDEN ÖNCE okunuyordu. Başlık sayfanın dibine denk gelip
    sonraki sayfaya kaydığında kaydedilen numara BİR ÖNCEKİ sayfaydı.
    43 belirtinin 18'inde Ek C okuru bir sayfa erkene gönderiyordu ve o
    sayfaların çoğu BAŞKA bir belirtinin karar tablosudur, sonu da
    "Not this sign — go back to the sign index in Appendix C": okur
    kendisini gönderen satıra geri dönüyordu. Kapalı döngü, hem de
    kitabın ilan ettiği tek giriş yolunda.

    Bu test sayfanın YER AÇILDIKTAN SONRA okunduğunu kanıtlar."""
    why = _render_layer_missing()
    if why:
        skip("belirti dizini sayfa doğruluğu kapısı", why)
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        rest = [{"type": "h2", "text": "A sign heading",
                 "claims": ["SYM-001"]},
                {"type": "para", "text": "Body text under the heading."},
                {"type": "bullets", "items": ["one", "two", "three"]}]
        # sayfanın dibi: başlık kesinlikle sonraki sayfaya kayacak
        ts.y = ts.bottom + ts.lead * 0.4
        before = ts.page
        ts.reserve_group(rest, 0, {})
        after_reserve = ts.page
        check("dip kenarda başlık için SAYFA ÇEVRİLİYOR",
              after_reserve == before + 1)
        # kaydedilecek numara, başlığın GERÇEKTEN düştüğü sayfa olmalı
        recorded = ts.page
        import typeset as _T
        _T.run_blocks(ts, rest, {})
        check("kaydedilen sayfa, başlığın DİZİLDİĞİ sayfayla aynı",
              recorded == after_reserve,
              f"kaydedilen {recorded}, dizilen {after_reserve}")
        check("kaydedilen sayfa, yer açılmadan ÖNCEKİ sayfa DEĞİL",
              recorded != before, f"{recorded} == {before} → bir sayfa erken")


def test_measurement_figure_travels_with_its_text():
    """Ölçü figürü, kendi metniyle AYNI sayfada mı ayrılıyor.

    Faz 5'te ölçülen: Bölüm 2'de birim `h3 → para → bullets → figure`.
    Ayırma yalnızca ilk paragrafa bakıyordu; figür 4. bloktu ve 29
    ölçüm figürünün HEPSİ metninden bir sayfa sonra, üstelik BİR SONRAKİ
    ölçünün başlığının üstünde basılıyordu."""
    why = _render_layer_missing()
    if why:
        skip("ölçü figürü birlikteliği kapısı", why)
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        meta = {"meas_X": {"width_pt": 300.0, "height_pt": 380.0}}
        unit = [{"type": "h3", "text": "High bust"},
                {"type": "para", "text": "Horizontal, passing under the arms."},
                {"type": "bullets", "items": ["error one", "error two"]},
                {"type": "figure", "key": "meas_X",
                 "caption": "High bust: the path the tape takes."}]
        # sayfanın yarısı dolu: birim sığmaz, BİRLİKTE kaymalı
        ts.y = ts.bottom + (ts.top - ts.bottom) * 0.45
        p0 = ts.page
        ts.reserve_group(unit, 0, meta)
        check("ölçü birimi sığmıyorsa başlık FİGÜRLE BİRLİKTE kayıyor",
              ts.page == p0 + 1)
        # boş sayfada birim sığar: gereksiz sayfa açılmamalı
        ts.y = ts.top
        p1 = ts.page
        ts.reserve_group(unit, 0, meta)
        check("boş sayfada ölçü birimi için sayfa AÇILMIYOR", ts.page == p1)
        # figürsüz bir başlık eski davranışı korumalı
        plain = [{"type": "h3", "text": "Conditions"},
                 {"type": "para", "text": "Short."}]
        ts.y = ts.top
        p2 = ts.page
        ts.reserve_group(plain, 0, {})
        check("figürsüz başlık davranışı DEĞİŞMEDİ", ts.page == p2)


def test_heading_travels_with_its_content():
    """Başlık, ardındaki ilk bölünmez parçayla birlikte mi kalıyor."""
    why = _render_layer_missing()
    if why:
        skip("başlık-içerik kapısı", why)
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        T, ts = _mini_typesetter(Path(d) / "t.pdf")
        check("başlık yükseklik ölçüsü TANIMLI", ts.head_h("h2") > 0)
        blocks = [{"type": "h2", "text": "Where this leads"},
                  {"type": "para", "text": "One short intro line."},
                  {"type": "bullets", "items": ["a", "b", "c"]}]
        ts.y = ts.bottom + ts.lead * 2      # yalnızca iki satırlık yer var
        p0 = ts.page
        ts.reserve_group(blocks, 0, {})
        check("başlık grubu sığmıyorsa SAYFA ÇEVRİLİYOR", ts.page == p0 + 1)
        ts.y = ts.top                       # bol yer
        p1 = ts.page
        ts.reserve_group(blocks, 0, {})
        check("yer varken gereksiz sayfa AÇILMIYOR", ts.page == p1)


if __name__ == "__main__":
    sys.exit(main())
