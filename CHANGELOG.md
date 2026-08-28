# CHANGELOG

Faz kapanışlarını ve önemli mimari kararları kronolojik sırayla
kaydeder. Gerekçelerin tam metni `DECISIONS.md`'dedir; burada yalnızca
**ne zaman ne olduğu** durur.

## [S0 + S1] — 2026-08-28 (proje kuruldu, seri mimarisi ve Kitap 1 Faz 1 spesifikasyonu üretildi)

> Durum: **READY_FOR_DECISION** — `.gate` BİLEREK `bootstrap`'ta kaldı.
> `series-architecture`'a yükseltme kurucu onayına bağlıdır.

### Oluşturuldu
- Seri deposu: 11 seri dizini + 3 kitap projesi (`BOOK-01`…`BOOK-03`).
- `series_config.json` + 3× `book_config.json`; 4 ayrı `.gate` dosyası.
- 17 politika belgesi (`00_CONTEXT/`), 8 kök belgesi.
- 6 JSON şeması: kaynak, belirti, düzeltme, ölçü, crosswalk, figür.
- Taksonomi taslakları: **43 belirti** (129 aday neden), **19 düzeltme
  ailesi**, **32 ölçü**, **12 blok bileşeni**, **20 terim**,
  **18 görsel token**, **35 sınır topiği**.
- Türetilmiş **148 crosswalk** kaydı (129 teşhis→düzeltme,
  19 düzeltme→blok, 21 açık istisna).
- Araç zinciri: `paths.py`, `schema_lite.py`, `build_crosswalk.py`,
  `validate_spec.py`, `validate_structure.py`, `qa_boundary.py`,
  `qa_claims.py`, `qa_terminology.py`, `kill_gate.py`, `qa_all.sh`,
  `selftest.py` (77 denetim).
- CI iş akışı; git deposu ve ilk commit.
- Kitap 1 Faz 1'in **on zorunlu çıktısı** (`BOOK-01/00_SPEC/`).
- Kitap 2 ve Kitap 3 yol haritaları (yürütülMEDİ).

### Kararlar
- **K2** — ortak kütüphane: depolar arası YOK, depo içi VAR.
- **K3** — iki katmanlı kapı sistemi (kardeş projelerde yok).
- **K5** — kill-gate: ikili DIŞ ölçüm modeli.
- **K6** — dış uzman işe alınmayacak; **AI vekil insan yerine SAYILMAZ**
  (`aiProxyCountsAsHuman: false`, açılamaz).
- **K7** — "basılı format avantajı" iddiası kalıcı olarak korumaya
  alındı (araştırma raporu § 27: ZAYIF).
- **K13** — sınır matrisi tek-birincil kuralına göre düzeltildi;
  çözüm kopyalama değil **topik bölme**.

### Kapıların gerçekten çalıştığının kanıtları
- `validate_spec.py` bir şema ihlali yakaladı (`M-011.path_rule` çok
  kısa) — düzeltildi.
- `qa_boundary.py` bir kapsam boşluğu buldu: `AF-19`'a hiçbir Kitap 1
  belirtisinden ulaşılamıyordu — `SYM-043` eklendi (**K15**).
- `qa_terminology.py` anahtar kelime belgesinde bir yasak eşanlamlı
  yakaladı; **kural doğru, kapsam yanlıştı** — ayrı bir `KEYWORD_FILES`
  muafiyeti eklendi ve gerekçesi kodda belgelendi (**K14**).
- `selftest.py`, Türkçe büyük "İ" kusurunun **ÜÇÜNCÜ** bir doğrulayıcıda
  (`validate_spec`) hâlâ açık olduğunu buldu — katlama tek kopyaya
  çıkarıldı (**K16**) ve regresyon testi eklendi.
- `validate_structure.py`, `selftest.py`'nin KENDİ fixture'ının izolasyon
  ihlali ürettiğini yakaladı — fixture yeniden yazıldı, **kapı muafiyet
  almadı** (**K17**).

### YAPILMAYAN (bilinçli)
Manüskript · diyagram · kapak · KDP dosyası · reklam kampanyası ·
Kitap 2/3 üretimi · kaynak edinimi · marka taraması · spiral
fizibilitesi · rakip akış takibi.

### Bilinen sınır
106 taksonomi kaydının **tamamı** `agent_drafted_unverified`; kaynak
sicili **boş**. Bu, Faz 1'in açıkça kaydedilmiş en büyük sınırıdır ve
`OPEN_QUESTIONS A3`'ün konusudur.

---

*Vâliçe Press · TRUE FIT · Changelog*
