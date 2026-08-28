"""
trfold.py — Türkçe-güvenli metin katlama. TEK KOPYA.

Neden ayrı bir modül (DECISIONS.md K16):

Python'un `str.lower()`'ı Türkçe büyük 'İ' (U+0130) için 'i' + BİRLEŞEN
NOKTA (U+0307) üretir. Sonuç görünürde 'i'dir ama iki kod noktasıdır ve
alt dizi karşılaştırması SESSİZCE başarısız olur:

    "DEĞİLDİR".lower()  →  "deği̇ldi̇r"     ("değildir" ile eşleşmez)

Kardeş sigorta projesinde bu kusur bir KA scriptinde SONRADAN bulunmuştu
(dürüst inkârlar yanlış yakalanıyordu). Bu projede qa_claims.py ve
qa_terminology.py ilk sürümden itibaren korumalı yazıldı — ama
07_TESTS/selftest.py, aynı kusurun ÜÇÜNCÜ bir yerde
(validate_spec.check_cause_distinguishability) hâlâ açık olduğunu
yakaladı.

Ders: koruma üç yerde tekrarlanırsa dördüncü yerde unutulur. Katlama
artık TEK bir yerde tanımlıdır ve her tüketici buradan alır.
"""

_TR_MAP = str.maketrans({
    "İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç",
})


def fold(s: str) -> str:
    """Karşılaştırma için Türkçe-güvenli küçültme."""
    return s.translate(_TR_MAP).lower()
