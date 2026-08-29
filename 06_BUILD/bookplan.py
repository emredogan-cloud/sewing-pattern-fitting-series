"""
bookplan.py — kitabın YAPISI. Tek kopya, üçüncü taraf bağımlılığı YOK.

`build_book.py` bu yapıyı DİZER, `qa_manuscript.py` DENETLER. İkisi de
buradan okur. Ayrı bir dosya olmasının sebebi bağımlılık katmanıdır:
build_book reportlab'a bağlıdır, kapı ise bağlı OLMAMALIDIR — yoksa
render katmanı kurulu değilken manüskript kapısı sessizce atlanır ve
"kapı yeşil, ürün bozuk" sınıfı bir kez daha açılır.
"""
import re

MANUSCRIPT_DIR = "02_CONTENT/protected/manuscript"

# Bölüm 2 ve bölge atlası ÜRETİLİR; gerisi yazılır.
GENERATED = {
    "ch02": "MEASUREMENTS",
    "ch09": "B1-CH09", "ch10": "B1-CH10", "ch11": "B1-CH11", "ch12": "B1-CH12",
    "ch13": "B1-CH13", "ch14": "B1-CH14", "ch15": "B1-CH15",
    "ch16_atlas": "B1-CH16-ATLAS",
}

PARTS = [
    (0, "How to use this book", ["part0"]),
    (1, "The language of numbers", ["ch01", "ch02", "ch03"]),
    (2, "The fitting garment", ["ch04", "ch05"]),
    (3, "The diagnostic method", ["ch06", "ch07", "ch08"]),
    (4, "The regional atlas",
     ["ch09", "ch10", "ch11", "ch12", "ch13", "ch14", "ch15"]),
    (5, "From decision to record", ["ch16", "ch16_atlas", "ch17", "ch18"]),
    (6, "Appendices", ["appendix"]),
]

# OKUR DİLİ (K45/K46): iç kimlikler dizilen metne GİREMEZ.
INTERNAL_ID = re.compile(r"\b(?:SYM-\d{3}|AF-\d{2}|M-\d{3}|TK-\d{2}|S-\d{4}|"
                         r"XW-\d{3}|VAL-\d{4}|CLM-\d{4}|BLK-\d{2}|T-\d{2}|"
                         r"TOP-\d{2}|B1-CH\d{2})\b")

# Okur-görünür bölüm adları. TOC, PDF ana hattı ve çapraz atıflar
# AYNI tablodan okur; ikinci bir kopya tutulsaydı içindekiler ile
# sayfa başlıkları sessizce ayrışabilirdi.
CHAPTER_TITLES = {
    "part0": "How to use this book",
    "ch01": "1 · Why the pattern did not fit",
    "ch02": "2 · Measuring your body",
    "ch03": "3 · Reading the pattern",
    "ch04": "4 · The diagnostic fitting garment",
    "ch05": "5 · The fitting session",
    "ch06": "6 · The seven-step cycle",
    "ch07": "7 · Naming what you see",
    "ch08": "8 · Ruling out the false causes",
    "ch09": "9 · The neck and shoulder",
    "ch10": "10 · The upper back and armhole",
    "ch11": "11 · The bust and chest",
    "ch12": "12 · The waist and torso length",
    "ch13": "13 · The hip and seat",
    "ch14": "14 · The sleeve and arm",
    "ch15": "15 · Trousers: the crotch and the leg",
    "ch16": "16 · The order of work",
    # ⚠ Faz 5'te ÖLÇÜLEN kusur: bu bölüm okura "16b" diye görünüyordu.
    # Bir başvuru kitabında "16" ve "16b" diye iki bölüm, numaralandırma
    # hatası olarak okunur. Bölüm gerçekten de bir BÖLGE değildir —
    # bütün giysiye ait dört belirtiyi taşır — ve kitapta zaten
    # numarasız bölümler vardır ("How to use this book", "Appendices").
    # Numara KALDIRILDI; yeri (düzeltme sırasından sonra) değişmedi,
    # çünkü bu belirtiler en son okunur.
    # Regresyon: 07_TESTS/selftest.py § test_no_duplicate_chapter_number
    "ch16_atlas": "Signs that belong to the whole garment",
    "ch17": "17 · Your fit profile",
    "ch18": "18 · Carrying the profile forward",
    "appendix": "Appendices",
}
# Çapraz atıf çözümü: "Chapter 8" → hangi bölüm anahtarı
CHAPTER_BY_NUMBER = {int(t.split(" · ")[0]): k
                     for k, t in CHAPTER_TITLES.items()
                     if t.split(" · ")[0].isdigit() and k != "ch16_atlas"}


def fill_index_slots(blocks: list, groups: dict) -> list:
    """`index_slot` işaretlerini üretilmiş ek bloklarıyla değiştirir.

    Birinci geçişte `groups` boştur (sayfa numaraları henüz ölçülmedi);
    işaretler o geçişte DÜŞÜRÜLÜR ve yakınsama döngüsü ikinci geçişte
    onları doldurur. `run_blocks` bilinmeyen blok türünde patladığı için
    işaretlerin dizgiye ULAŞMAMASI şarttır."""
    out: list = []
    for b in blocks:
        if b.get("type") == "index_slot":
            out.extend(groups.get(b["slot"], []))
        else:
            out.append(b)
    return out
