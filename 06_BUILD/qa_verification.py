#!/usr/bin/env python3
"""
qa_verification.py — DOĞRULAMA ADIMI KAPISI (İçerik turu · L-2).

⚠ NEDEN VAR: Faz 5'te sekiz kapı da yeşildi ve 129 doğrulama adımının
26'sı okurun kitapta HİÇ ÖĞRENMEDİĞİ bir niceliğe başvuruyordu. Hiçbir
kapı bunu göremiyordu, çünkü `confirming_measurement` SERBEST METİNDİ:
bir kapı dolu bir dizeyi doğrulanmış sayar. Kusur yalnızca DİZİLMİŞ
sayfada, okur gibi okununca görünüyordu.

Bu kapı o soruyu MAKİNEYE sorar:

  ① her adımın `confirming_refs` alanı var mı ve şema uyumlu mu
  ② başvurduğu her VÜCUT ölçüsü measurements.json'da var mı
  ③ başvurduğu her KALIP okuması pattern_readings.json'da var mı
  ④ başvurduğu her PROVA okuması pattern_readings.json'da var mı
  ⑤ her kalıp/prova okumasının bir ÖĞRETİM ÇAPASI (bölüm + kesit) var mı
  ⑥ kind='none' diyen adımın okur metni gerçekten "ölçüm yok" diyor mu
     ve kind≠'none' diyen adımın metni bunu DEMİYOR mu
  ⑦ okur metni, başvurduğu vücut ölçüsünü ADIYLA anıyor mu
  ⑧ ÖLÇÜLEBİLİR bir adım en az bir nicelik taşıyor mu (boş referans yok)
  ⑨ sicildeki her kalıp/prova okuması EN AZ BİR adımda kullanılıyor mu
     (kullanılmayan okuma, kitaba gereksiz karmaşıklık ekler — § 7)
  ⑩ ease KARŞILAŞTIRMASI döngüsel mi: "kalıbın öngördüğü ease" gibi
     bir ifade, okurun ZATEN bilmesi gereken bir sayıya gönderir
  ⑬ ölçülebilir bir adım, farkın NE ANLAMA GELDİĞİNİ söylüyor mu
     (metinde yön sözcüğü ya da kayıtta `expected`)

  ⑫ kind='compare' diyen bir adım GERÇEKTEN iki taraflı mı: hem bir
     vücut ölçüsü hem bir kalıp/prova okuması taşıyor mu, ve okur metni
     KALIP tarafını da anıyor mu. Sentetik okur incelemesi altı adımda
     "kendi ön/arka farkını OKU" yazdığını ve karşılaştıracak ikinci
     sayının HİÇ istenmediğini ölçtü — bir sayı bir karşılaştırma
     değildir ve Bölüm 6 Adım 5 ile çelişiyordu

  ⑪ bir doğrulama adımında KULLANILAN her ölçü, en az bir bölge
     bölümünün "The measurements you read here" tablosunda görünüyor mu.

     ⚠ KURALIN SINIRI BİLEREK GEVŞEKTİR: bir bölgenin girişi başka bir
     bölgenin ölçüsünü İSTEYEBİLİR ve bu kitabın çekirdek fikridir —
     yakadaki belirtinin nedeni göğüstedir. Bu yüzden kapı "bu bölümün
     tablosu" değil "HERHANGİ bir bölümün tablosu" diye sorar. Kapıyı
     sıkılaştırmak, kitabın kendi tezini ihlal eden bir tablo üretirdi.
     Ölçülen kusur şuydu: üç ölçü (diz, ön göğüs genişliği, omuz eğimi)
     HİÇBİR bölge tablosunda yokken doğrulama adımlarında isteniyordu

Çıkış: 0 temiz · 1 en az bir kusur.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

PATTERN_READINGS = paths.TAXONOMY_PUBLIC / "pattern_readings.json"

# Okur metninde bir ölçünün ADI hangi biçimlerde geçebilir. Bu tablo
# ÖLÇÜ KAYDININ adından türetilemez: "Bust–high bust difference" okur
# metninde "bust minus high bust difference" diye geçer. Eşleşme
# ELLE kurulur ve kapı onu DENETLER — tersi değil.
SURFACE = {
    "M-001": [r"high bust"],
    "M-002": [r"full bust", r"\bbust\b"],
    "M-003": [r"underbust", r"under[- ]bust"],
    "M-004": [r"natural waist", r"waist measurement", r"marked waist", r"waist mark"],
    "M-005": [r"high hip"],
    "M-006": [r"full hip"],
    "M-007": [r"bicep"],
    "M-008": [r"wrist"],
    "M-009": [r"thigh"],
    "M-010": [r"\bknee\b"],
    "M-011": [r"\bcalf\b"],
    "M-013": [r"neck base", r"neck[- ]base"],
    "M-014": [r"shoulder length"],
    "M-015": [r"centre front length"],
    "M-016": [r"centre back length"],
    "M-017": [r"shoulder[- ]to[- ]apex"],
    "M-018": [r"apex to apex"],
    "M-019": [r"apex to waist"],
    "M-020": [r"across back"],
    "M-021": [r"across chest"],
    "M-022": [r"armhole depth"],
    "M-023": [r"waist to hip"],
    "M-024": [r"waist to floor", r"outseam", r"waist mark to the floor"],
    "M-025": [r"inseam"],
    "M-026": [r"crotch depth"],
    "M-027": [r"crotch length"],
    "M-028": [r"sleeve length"],
    "M-029": [r"shoulder[- ]to[- ]elbow"],
    "M-030": [r"total height", r"\bheight\b"],
    "M-031": [r"bust minus high bust", r"bust[-–−] ?high bust",
              r"bust[- ]to[- ]chest difference"],
    "M-032": [r"front[- ]to[- ]back (length )?difference"],
    "M-033": [r"hip minus waist", r"waist[- ]to[- ]hip"],
    "M-034": [r"shoulder slope"],
}

NO_MEASUREMENT = re.compile(r"there is no measurement for this", re.I)

# ⑬ Farkın YÖNÜNÜ bildiren sözcükler.
DIRECTION = re.compile(
    r"\b(larger|smaller|bigger|longer|shorter|more than|less than|exceeds?|"
    r"below|above|deeper|shallower|wider|narrower|adequate|"
    r"too (much|little|deep|shallow|wide|narrow|long|short))\b"
    r"|no published|there is no measurement|Appendix J|band", re.I)

# ⑩ Döngüsel ease: okurdan, ancak KARŞILAŞTIRMAYI YAPARAK
# öğrenebileceği bir sayıyı karşılaştırmaya GİRDİ olarak vermesi
# istenirse adım uygulanamaz. Faz 5 bunu göremiyordu.
CIRCULAR_EASE = re.compile(
    r"plus (?:the )?(?:necessary |wearing |required )?ease"
    r"|plus the ease the pattern"
    r"|ease the pattern (?:intends|allows|assumes)", re.I)


def load(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    errs: list = []
    warns: list = []

    signs = load(paths.FIT_SIGNS)["signs"]
    meas = {m["measurement_id"] for m in load(paths.MEASUREMENTS)["measurements"]}
    pr_doc = load(PATTERN_READINGS)
    pr = {r["reading_id"]: r for r in pr_doc["readings"]}
    tr = {r["reading_id"]: r for r in pr_doc["toile_readings"]}
    mdir = (paths.BOOK_DIRS[args.book] / "02_CONTENT" / "protected" / "manuscript")
    # ⚠ DÜRÜST SINIR: manüskript prozası BİLEREK izlenmiyor (.gitignore
    # § ①, DECISIONS.md K9). Temiz bir klonda OKUR METNİ yoktur ve bu
    # kapının yedi denetimi (⑥⑦⑩⑫⑬ ve okuma yöntemi uzunluğu) prozayı
    # okur. Kapı o durumda ÇÖKMEZ ve SESSİZCE GEÇMEZ: yapısal
    # denetimleri koşar ve neyi ATLADIĞINI yazar.
    en_path = mdir / "sign_content_en.json"
    prose = en_path.exists()
    en = load(en_path) if prose else {}

    used_pr: set = set()
    used_tr: set = set()
    n_steps = n_none = n_body = n_pattern = n_toile = 0

    # ⑤ öğretim çapası
    for rid, r in list(pr.items()) + list(tr.items()):
        if not r.get("taught_in") or not r.get("taught_section"):
            errs.append(f"{rid}: ÖĞRETİM ÇAPASI yok (taught_in/taught_section)")
        if not r.get("how") or len(r["how"]) < 40:
            errs.append(f"{rid}: okuma yöntemi yok ya da çok kısa")

    for s in signs:
        sid = s["symptom_id"]
        auth = en.get(sid)
        if not auth and prose:
            errs.append(f"{sid}: okur içeriği YOK")
            continue
        for i, c in enumerate(s["candidate_causes"], 1):
            k = f"{sid}.C{i}"
            n_steps += 1
            refs = c.get("confirming_refs")
            if not refs:                                             # ①
                errs.append(f"{k}: confirming_refs YOK")
                continue
            body = refs.get("body") or []
            pat = refs.get("pattern") or []
            toi = refs.get("toile") or []
            kind = refs.get("kind")
            text = auth["causes"][i - 1]["measure"] if auth else None

            for m in body:                                           # ②
                if m not in meas:
                    errs.append(f"{k}: kayıtta OLMAYAN ölçü {m}")
            for p in pat:                                            # ③
                if p not in pr:
                    errs.append(f"{k}: sicilde OLMAYAN kalıp okuması {p}")
                else:
                    used_pr.add(p)
            for t in toi:                                            # ④
                if t not in tr:
                    errs.append(f"{k}: sicilde OLMAYAN prova okuması {t}")
                else:
                    used_tr.add(t)

            if text is None:
                n_body += len(body); n_pattern += len(pat); n_toile += len(toi)
                if kind == "none":
                    n_none += 1
                continue
            declares_none = bool(NO_MEASUREMENT.search(text))
            if kind == "none":                                       # ⑥
                n_none += 1
                if not declares_none:
                    errs.append(f"{k}: kind='none' ama okur metni bunu SÖYLEMİYOR")
                if body or pat or toi:
                    errs.append(f"{k}: kind='none' ama referans taşıyor")
            else:
                if declares_none:
                    errs.append(f"{k}: metin 'ölçüm yok' diyor ama kind='{kind}'")
                if not (body or pat or toi):                         # ⑧
                    errs.append(f"{k}: ölçülebilir adım ama HİÇ nicelik taşımıyor")

            for m in body:                                           # ⑦
                pats = SURFACE.get(m)
                if not pats:
                    errs.append(f"{k}: {m} için okur karşılığı TANIMSIZ (SURFACE)")
                elif not any(re.search(x, text, re.I) for x in pats):
                    errs.append(f"{k}: okur metni {m} ölçüsünü ADIYLA anmıyor "
                                f"— \"{text[:70]}…\"")

            if kind == "compare":                                    # ⑫
                if body and not (pat or toi):
                    errs.append(f"{k}: kind='compare' ama YALNIZCA vücut tarafı var "
                                f"— karşılaştırılacak ikinci sayı yok")
                if (pat or toi) and not re.search(
                        r"pattern|toile|sewn|garment|size chart|printed", text, re.I):
                    errs.append(f"{k}: kalıp/prova okumasına başvuruyor ama okur metni "
                                f"o tarafı ANMIYOR — \"{text[:70]}…\"")

            # ⑬ ölçülebilir bir adım, farkın NE ANLAMA GELDİĞİNİ
            # söylüyor mu — ya metninde bir yön sözcüğü vardır, ya da
            # kayıtta `expected` alanı. Yoksa okur iki sayı tutar ve
            # hiçbir karar veremez (bağımsız inceleme M-15).
            if kind in ("compare", "read") and not c.get("expected"):
                if not DIRECTION.search(text):
                    errs.append(f"{k}: karşılaştırma YÖNSÜZ — hangi sonuç hipotezi "
                                f"destekler, söylenmiyor ve `expected` alanı yok")

            if CIRCULAR_EASE.search(text):                           # ⑩
                errs.append(f"{k}: DÖNGÜSEL ease ifadesi — okurdan, ancak "
                            f"karşılaştırmayı yaparak öğrenebileceği bir sayı "
                            f"isteniyor: \"{text[:70]}…\"")

            n_body += len(body)
            n_pattern += len(pat)
            n_toile += len(toi)

    # ⑪ kullanılan her ölçü EN AZ BİR bölge tablosunda görünüyor mu
    #    (bölge tabloları da manüskript prozasındadır — K9)
    zpath = mdir / "zones_en.json"
    if zpath.exists():
        zones = load(zpath)
        listed_anywhere: set = set()
        for z in zones.values():
            if isinstance(z, dict) and "measures" in z:
                listed_anywhere |= set(z["measures"])
        used_body: set = set()
        for s in signs:
            for c in s["candidate_causes"]:
                used_body |= set((c.get("confirming_refs") or {}).get("body") or [])
        for m in sorted(used_body - listed_anywhere):
            errs.append(f"{m}: doğrulama adımlarında KULLANILIYOR ama hiçbir bölge "
                        f"bölümünün ölçü tablosunda görünmüyor — okur onu atlastan "
                        f"bulamaz")

    for rid in pr:                                                   # ⑨
        if rid not in used_pr:
            warns.append(f"{rid} ({pr[rid]['name']}): hiçbir doğrulama adımı "
                         f"kullanmıyor")
    for rid in tr:
        if rid not in used_tr:
            warns.append(f"{rid} ({tr[rid]['name']}): hiçbir doğrulama adımı "
                         f"kullanmıyor")

    print("▸ qa_verification.py — doğrulama adımı kapısı")
    if not prose:
        print("  ⚠ OKUR METNİ İZLENMİYOR (K9) — yedi denetim ATLANDI: metin/kayıt "
              "uyumu, 'ölçüm yok' beyanı, ölçü adının anılması, döngüsel ease, "
              "karşılaştırmanın iki taraflılığı ve yön ölçütü. Yapısal denetimler "
              "koştu. TAM KAPSAM YEREL KOŞUMDADIR.")
    print(f"  {n_steps} adım · ölçüm yok diyen {n_none} · "
          f"vücut atfı {n_body} · kalıp atfı {n_pattern} · prova atfı {n_toile}")
    print(f"  kalıp okuması {len(pr)} ({len(used_pr)} kullanılıyor) · "
          f"prova okuması {len(tr)} ({len(used_tr)} kullanılıyor)")
    if args.verbose and warns:
        for w in warns:
            print(f"  ⚠ {w}")
    if errs:
        print(f"  ✗ {len(errs)} kusur")
        for e in errs[:60]:
            print(f"    - {e}")
        if len(errs) > 60:
            print(f"    … ve {len(errs) - 60} tane daha")
        return 1
    print("  ✓ hiçbir doğrulama adımı öğretilmemiş bir niceliğe başvurmuyor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
