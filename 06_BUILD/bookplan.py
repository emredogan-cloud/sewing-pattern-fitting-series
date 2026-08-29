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
