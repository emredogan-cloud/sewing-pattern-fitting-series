#!/usr/bin/env python3
"""
validate_spec.py — şema + bütünlük + kaynak-otoritesi + kapı doğrulayıcı.

Desen: KOREAN-HANGUL-HANDWRITING-WORKBOOK validate_spec.py.

Kritik ilke (DECISIONS.md K10): bu script bir KARARI EZMEZ ve bir
İDDİAYI ÜCRETSİZ VERMEZ. Hiçbir kayıt kanıt olmadan
'technical_reference_verified' veya 'physically_validated' olamaz —
check_verification_evidence bunu mekanik olarak dayatır.

İçerik yokken 0 hatayla biter; bu yüzden 07_TESTS/selftest.py var:
kusurlu fixture'larla bu scriptin GERÇEKTEN kırmızı yaktığını kanıtlar.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from schema_lite import validate as schema_validate  # noqa: E402
from trfold import fold  # noqa: E402

NEVER_AUTHORITATIVE = {
    "commercial_competitor_structural",
    "marketplace_observation",
    "community_reference_non_authoritative",
}
STRONG_VERIFICATION = {"fulltext", "official_pdf"}


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


# ── kaynak katmanı ────────────────────────────────────────────────────
def check_source_type_authority_consistency(rec: dict, errors: list, sid: str):
    """SOURCING_STANDARD.md § 1: rakip/pazar/topluluk kaynağı ASLA teknik otorite değildir."""
    if rec.get("source_type") in NEVER_AUTHORITATIVE and rec.get("technical_authority") is True:
        errors.append(
            f"{sid}: source_type={rec['source_type']} ama technical_authority=true — "
            f"bu tür kaynaklar ASLA teknik otorite sayılamaz (SOURCING_STANDARD.md § 1)."
        )


def check_source_locator_discipline(rec: dict, errors: list, sid: str):
    """SOURCING_STANDARD.md § 3: görülmemiş kaynağın locator'ı olamaz."""
    if rec.get("verification_level") in {"not_yet_acquired", "unverifiable"} and rec.get("locator"):
        errors.append(
            f"{sid}: verification_level={rec['verification_level']} ama locator dolu "
            f"({rec['locator']!r}) — görülmemiş bir kaynağın sayfa/bölüm bilgisi UYDURULAMAZ."
        )


def check_source_authority(record: dict, authority: dict, errors: list, rid: str, kind: str):
    """Teknik bir iddia en az bir technical_authority=true kaynağa dayanmalıdır."""
    refs = record.get("source_refs", [])
    unknown = [r for r in refs if r not in authority]
    for r in unknown:
        errors.append(f"{rid}: source_refs içindeki {r} 01_SOURCE/records/'de bulunamadı — kayıtsız kaynak.")
    if not refs:
        return
    if not any(authority.get(r) is True for r in refs):
        errors.append(
            f"{rid} ({kind}): source_refs içinde technical_authority=true taşıyan hiçbir kaynak yok — "
            f"yalnızca rakip/pazar gözlemine dayanan bir teknik iddia GEÇERSİZDİR (SOURCING_STANDARD.md § 1)."
        )


def check_verification_evidence(record: dict, verification: dict, errors: list, rid: str):
    """DECISIONS.md K10: doğrulama durumu kanıt gerektirir."""
    st = record.get("verification_status")
    refs = record.get("source_refs", [])
    if st == "technical_reference_verified":
        if not any(verification.get(r) in STRONG_VERIFICATION for r in refs):
            errors.append(
                f"{rid}: verification_status='technical_reference_verified' ama hiçbir kaynağı "
                f"fulltext/official_pdf seviyesinde DEĞİL — bu durum kanıtsız iddia edilemez."
            )
    if st == "physically_validated" and not record.get("validation_record_ref"):
        errors.append(
            f"{rid}: verification_status='physically_validated' ama validation_record_ref YOK — "
            f"fiziksel doğrulama bir KAYIT gerektirir (VALIDATION_PROTOCOL.md § 5)."
        )


# ── taksonomi bütünlüğü ───────────────────────────────────────────────
def check_cause_distinguishability(sign: dict, errors: list):
    """Aynı belirtinin iki nedeni AYNI ayırt edici kanıtı taşıyamaz —
    taşırsa okur onları ayıramaz ve teşhis sistemi çöker."""
    sid = sign.get("symptom_id", "?")
    seen = {}
    for c in sign.get("candidate_causes", []):
        # Türkçe-güvenli katlama ZORUNLU — str.lower() büyük "İ"yi bozar
        # ve iki AYNI kanıt metni farklı görünür (trfold.py, DECISIONS.md K16).
        ev = fold((c.get("distinguishing_evidence") or "").strip())
        if ev in seen:
            errors.append(
                f"{sid}: iki aday neden AYNI ayırt edici kanıtı taşıyor "
                f"({seen[ev]!r} ve {c.get('cause')!r}) — okur bunları ayıramaz."
            )
        seen[ev] = c.get("cause")


def check_cause_measurement_present(sign: dict, errors: list):
    """Ölçüm yoksa fiziksel test ZORUNLU — bir neden kanıtsız bırakılamaz."""
    sid = sign.get("symptom_id", "?")
    for c in sign.get("candidate_causes", []):
        m = (c.get("confirming_measurement") or "")
        if m.startswith("NO_MEASUREMENT_EXISTS") and not c.get("physical_test"):
            errors.append(
                f"{sid}: '{c.get('cause')}' nedeni için ne ölçüm ne fiziksel test var — "
                f"kanıtsız neden yazılamaz (symptom_schema.json § candidate_causes)."
            )


def check_symptom_af_refs(sign: dict, af_ids: set, errors: list):
    sid = sign.get("symptom_id", "?")
    for c in sign.get("candidate_causes", []):
        af = c.get("adjustment_family_ref")
        if af and af not in af_ids:
            errors.append(f"{sid}: adjustment_family_ref={af} tanımlı bir düzeltme ailesi DEĞİL.")


def check_measurement_derivation(rec: dict, m_ids: set, errors: list):
    mid = rec.get("measurement_id", "?")
    for d in rec.get("derived_from", []):
        if d not in m_ids:
            errors.append(f"{mid}: derived_from={d} tanımlı bir ölçü DEĞİL.")
    if rec.get("category") == "derived" and not rec.get("derived_from"):
        errors.append(f"{mid}: category='derived' ama derived_from BOŞ — türetilmiş ölçü kaynaksız olamaz.")


def check_crosswalk_integrity(xw: dict, sym_ids: set, af_ids: set, blk_ids: set, errors: list):
    xid = xw.get("crosswalk_id", "?")
    src, dst = xw.get("from_ref"), xw.get("to_ref")
    if xw.get("direction") == "DIAGNOSIS_TO_ADJUSTMENT":
        if src not in sym_ids:
            errors.append(f"{xid}: from_ref={src} tanımlı bir belirti DEĞİL.")
        if dst is not None and dst not in af_ids:
            errors.append(f"{xid}: to_ref={dst} tanımlı bir düzeltme ailesi DEĞİL.")
    else:
        if src not in af_ids:
            errors.append(f"{xid}: from_ref={src} tanımlı bir düzeltme ailesi DEĞİL.")
        if dst is not None and dst not in blk_ids:
            errors.append(f"{xid}: to_ref={dst} tanımlı bir blok bileşeni DEĞİL.")
    if dst is None and not xw.get("exception"):
        errors.append(
            f"{xid}: to_ref=null ama 'exception' BOŞ — bir teşhis yolunun karşılığı yoksa "
            f"NEDEN olmadığı AÇIKÇA yazılmalıdır (görev talimatı § 22)."
        )


def check_figure_tokens(fig: dict, token_ids: set, errors: list):
    fid = fig.get("figure_id", "?")
    for tk in fig.get("notation_tokens", []):
        if tk not in token_ids:
            errors.append(f"{fid}: notation_tokens içindeki {tk} visual_language_tokens.json'da tanımlı DEĞİL.")
    if fig.get("deterministic") is False and not fig.get("manual_reason"):
        errors.append(f"{fid}: deterministic=false ama manual_reason YOK — elle çizim gerekçesiz olamaz.")
    if fig.get("verification_status") == "physically_validated" and not fig.get("physical_validation_ref"):
        errors.append(f"{fid}: 'physically_validated' ama physical_validation_ref YOK.")


# ── kapı gereksinimleri ───────────────────────────────────────────────
def check_book_phase1_requirements(book_id: str, errors: list):
    """Bir kitabın kapısı phase1-spec'e ulaşmışsa on zorunlu belgesi olmalıdır."""
    required = [
        "SCOPE.md", "CONTENT_ARCHITECTURE.md", "CHAPTER_SPECS.md",
        "DIAGNOSTIC_SYSTEM.md", "DIAGNOSIS_TO_ADJUSTMENT_MAP.md", "VISUAL_SPEC.md",
        "SOURCE_MAP.md", "VALIDATION_PROTOCOL.md", "DIFFERENTIATION_TEST.md",
        "PHASE_2_ROADMAP.md",
    ]
    spec = paths.book_spec(book_id)
    for r in required:
        if not (spec / r).exists():
            errors.append(f"kapı phase1-spec ({book_id}): zorunlu Faz 1 çıktısı eksik — 00_SPEC/{r}")


def check_series_architecture_requirements(errors: list):
    required = [
        "SERIES_POSITIONING.md", "SERIES_CONTENT_ARCHITECTURE.md",
        "SERIES_KEYWORD_ARCHITECTURE.md", "SERIES_CROSSSELL_ARCHITECTURE.md",
        "VISUAL_STANDARD.md", "SOURCING_STANDARD.md", "QA_STANDARD.md",
        "VALIDATION_PROTOCOL.md", "IP_AND_BRAND_POLICY.md",
    ]
    for r in required:
        if not (paths.CONTEXT / r).exists():
            errors.append(f"kapı series-architecture: zorunlu belge eksik — 00_CONTEXT/{r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default=None, help="seri kapısı (varsayılan: .gate)")
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    errors: list[str] = []
    gate = args.gate or paths.read_series_gate()
    if gate not in paths.SERIES_GATE_ORDER:
        print(f"✗ geçersiz seri kapısı: {gate}")
        return 2

    counts = {"sources": 0, "signs": 0, "adjustments": 0, "measurements": 0,
              "crosswalks": 0, "blocks": 0, "figures": 0}

    # ── kaynaklar ──
    authority, verification = {}, {}
    if paths.SOURCE_SCHEMA.exists():
        sschema = load(paths.SOURCE_SCHEMA)
        for f in sorted(paths.SOURCE_RECORDS.glob("S-*.json")):
            counts["sources"] += 1
            try:
                rec = load(f)
            except json.JSONDecodeError as e:
                errors.append(f"{f.name}: geçersiz JSON — {e}")
                continue
            errors.extend(schema_validate(rec, sschema, path=f.name))
            sid = rec.get("source_id", f.name)
            check_source_type_authority_consistency(rec, errors, sid)
            check_source_locator_discipline(rec, errors, sid)
            authority[sid] = rec.get("technical_authority")
            verification[sid] = rec.get("verification_level")

    # ── düzeltme aileleri ──
    af_ids: set = set()
    if paths.ADJUSTMENT_FAMILIES.exists():
        aschema = load(paths.ADJUSTMENT_SCHEMA)
        for rec in load(paths.ADJUSTMENT_FAMILIES)["families"]:
            counts["adjustments"] += 1
            rid = rec.get("adjustment_family_id", "?")
            errors.extend(schema_validate(rec, aschema, path=rid))
            af_ids.add(rid)
            check_verification_evidence(rec, verification, errors, rid)
            if rec.get("verification_status") != "agent_drafted_unverified":
                check_source_authority(rec, authority, errors, rid, "adjustment")
        for rec in load(paths.ADJUSTMENT_FAMILIES)["families"]:
            for other in rec.get("interacts_with", []):
                if other not in af_ids:
                    errors.append(f"{rec['adjustment_family_id']}: interacts_with={other} tanımlı DEĞİL.")

    # ── bloklar ──
    blk_ids: set = set()
    if paths.BLOCK_COMPONENTS.exists():
        for rec in load(paths.BLOCK_COMPONENTS)["blocks"]:
            counts["blocks"] += 1
            blk_ids.add(rec["block_id"])

    # ── belirtiler ──
    sym_ids: set = set()
    if paths.FIT_SIGNS.exists():
        yschema = load(paths.SYMPTOM_SCHEMA)
        for rec in load(paths.FIT_SIGNS)["signs"]:
            counts["signs"] += 1
            rid = rec.get("symptom_id", "?")
            errors.extend(schema_validate(rec, yschema, path=rid))
            sym_ids.add(rid)
            check_cause_distinguishability(rec, errors)
            check_cause_measurement_present(rec, errors)
            check_symptom_af_refs(rec, af_ids, errors)
            check_verification_evidence(rec, verification, errors, rid)
            if rec.get("verification_status") != "agent_drafted_unverified":
                check_source_authority(rec, authority, errors, rid, "symptom")

    # ── ölçüler ──
    if paths.MEASUREMENTS.exists():
        mschema = load(paths.MEASUREMENT_SCHEMA)
        recs = load(paths.MEASUREMENTS)["measurements"]
        m_ids = {r.get("measurement_id") for r in recs}
        for rec in recs:
            counts["measurements"] += 1
            rid = rec.get("measurement_id", "?")
            errors.extend(schema_validate(rec, mschema, path=rid))
            check_measurement_derivation(rec, m_ids, errors)
            check_verification_evidence(rec, verification, errors, rid)

    # ── crosswalk ──
    if paths.CROSSWALK.exists():
        xschema = load(paths.CROSSWALK_SCHEMA)
        for rec in load(paths.CROSSWALK)["crosswalks"]:
            counts["crosswalks"] += 1
            rid = rec.get("crosswalk_id", "?")
            errors.extend(schema_validate(rec, xschema, path=rid))
            check_crosswalk_integrity(rec, sym_ids, af_ids, blk_ids, errors)

    # ── figürler ──
    token_ids = set()
    if paths.VISUAL_TOKENS.exists():
        token_ids = {t["token_id"] for t in load(paths.VISUAL_TOKENS)["tokens"]}
    fschema = load(paths.FIGURE_SCHEMA) if paths.FIGURE_SCHEMA.exists() else None
    for book_id, bdir in paths.BOOK_DIRS.items():
        ffile = bdir / "03_VISUAL" / "figures.json"
        if not ffile.exists() or fschema is None:
            continue
        for rec in load(ffile).get("figures", []):
            counts["figures"] += 1
            rid = rec.get("figure_id", "?")
            errors.extend(schema_validate(rec, fschema, path=rid))
            check_figure_tokens(rec, token_ids, errors)

    # ── kapı gereksinimleri ──
    if paths.gate_at_least(gate, "series-architecture", paths.SERIES_GATE_ORDER):
        check_series_architecture_requirements(errors)
    for book_id in paths.BOOK_DIRS:
        bgate = paths.read_book_gate(book_id)
        if paths.gate_at_least(bgate, "phase1-spec", paths.BOOK_GATE_ORDER):
            check_book_phase1_requirements(book_id, errors)

    result = {"series_gate": gate,
              "book_gates": {b: paths.read_book_gate(b) for b in paths.BOOK_DIRS},
              "counts": counts, "errors": errors, "passed": not errors}

    print(f"▸ validate_spec.py — seri kapısı: {gate} · kitap kapıları: "
          + " · ".join(f"{b}={g}" for b, g in result["book_gates"].items()))
    print(f"  kaynak: {counts['sources']} · belirti: {counts['signs']} · düzeltme ailesi: "
          f"{counts['adjustments']} · ölçü: {counts['measurements']} · crosswalk: "
          f"{counts['crosswalks']} · blok: {counts['blocks']} · figür: {counts['figures']}")
    if errors:
        print(f"  ✗ {len(errors)} hata:")
        for e in errors:
            print(f"    - {e}")
    else:
        print("  ✓ 0 hata")

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
