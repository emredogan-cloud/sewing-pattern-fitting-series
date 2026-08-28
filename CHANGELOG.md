# CHANGELOG

Faz kapanışlarını ve önemli mimari kararları kronolojik sırayla
kaydeder. Gerekçelerin tam metni `DECISIONS.md`'dedir; burada yalnızca
**ne zaman ne olduğu** durur.

## [S1 YÜRÜTME] — 2026-08-28 (14 açık kararın 12'si kapatıldı, kaynak katmanı kuruldu, depo yayımlandı)

> Durum: **READY_FOR_DECISION** — kapılar BİLEREK ilerlemedi.
> Seri `.gate` = `bootstrap` · Kitap 1 `.gate` = `foundation`.
> Rapor: `08_REPORTS/PHASE_1_EXECUTION_REPORT.md` (20 bölüm).

### Kaynak katmanı — sıfırdan on beşe
- **15 kaynak kaydı** (`01_SOURCE/records/S-0001`…`S-0015`); altısı
  teknik otorite taşıyan ve **tam metni okunmuş** kamu kaynağı:
  NMSU C-228 · NMSU C-227 · Texas AgriLife E-372 · WSU EM4582 ·
  ANSUR II (NATICK/TR-15/007) · NHANES 2021 APM.
- **Faz 1 hiçbir ücretli kaynak satın alınmadan kapandı.**
- `01_SOURCE/PUBLIC_SOURCE_SURVEY.md` — yedi eksende tarama kaydı:
  ne bulundu, ne kullanılamadı, ne reddedildi ve **neden**.
- `01_SOURCE/ACQUISITION_REQUEST_QUEUE.md` — dört ücretli kalem, her
  biri dokuz alanla; hiçbiri Kitap 1 için gerekli değil.

### Taksonomi doğrulama
- **16/32 ölçü** ve **13/19 düzeltme ailesi**
  `technical_reference_verified`'e yükseltildi.
- **43 belirtinin hiçbiri yükseltilmedi** — bilinçli: hiçbir kamu
  kaynağı aynı belirtinin iki nedenini ayırmıyor (`C-C` sınıfı).
- Dört kaynak-arası tanım farkı çelişki olarak kaydedildi, sessizce
  ezilmedi (`M-004` `M-008` `M-013` `M-025`).

### Yeni kapılar ve düzeltmeler
- **`06_BUILD/qa_crosswalk.py`** — 148 kaydın dokuz ilişki üzerinden
  denetimi; `qa_all.sh` + CI + `selftest`'e bağlandı. **0 bulgu.**
- `selftest.test_verification_status_is_honestly_recorded` **yeniden
  yazıldı** — adı ne diyorsa onu ölçüyor (`K20`).
- `test_verification_summary_matches_records` **eklendi**.
- Selftest **77 → 91** denetim.
- `REQUIRED_SERIES_DOCS` dört belge genişledi.
- CI eylem sürümleri yükseltildi (Node.js 20 kullanımdan kaldırma).

### Yeni belgeler
- `00_CONTEXT/TYPOGRAPHY_STANDARD.md` (`A7`)
- `00_CONTEXT/ADS_FRAMEWORK.md` (`A12`)
- `01_SOURCE/PUBLIC_SOURCE_SURVEY.md` · `ACQUISITION_REQUEST_QUEUE.md`
- `08_REPORTS/PHASE_1_EXECUTION_REPORT.md` · `PHASE_1_BRAND_SCREENING.md`
- `BOOK-03/00_SPEC/DRAFTING_SYSTEM_RESEARCH.md` (`A10`)

### Kararlar — `K18`…`K35` (18 yeni kayıt)
- **K18** — `TRUE FIT` **yayımlanan ad olarak KULLANILAMAZ**; aynı
  sektörde tescilli marka bulundu. Öneri: `BEFORE YOU CUT`.
- **K19** — kamu kaynağı önce; Faz 1 için sıfır satın alma.
- **K20** — kapı kendi kusurunu buldu: "yükseltilmemiş" ≠ "kanıtsız
  yükseltilmemiş". *(Kapının çalıştığının ALTINCI kanıtı.)*
- **K21** — `C-G` ease üç koşulla yazılabilir hâle geldi.
- **K22**–**K25** — format · renk · tipografi · ortam.
- **K26**–**K28** — Kitap 3 terminolojisi · çizim sistemi kanıt kapısı
  · reklam çerçevesi.
- **K29**–**K30** — asgari sınama seti · fark testi protokolü ve yeni
  `INCONCLUSIVE` durumu.
- **K31**–**K33** — yeni crosswalk kapısı · GitHub yayımı ·
  `ROADMAP_PROGRESS` ölçüm hatasının düzeltilmesi.
- **K34**–**K35** — birim · fotoğraf.

### Riskler
- `R-12` (IP/marka) olasılığı **DÜŞÜK → ORTA–YÜKSEK**.
- `R-09` (format) bir varsayımdan bir **olguya** dönüştü: KDP spiral
  cilt **sunmuyor**.
- Dört yeni risk: `R-15` tek kaynak bağımlılığı · `R-16` kaynak
  bağlantısı ölümü · `R-17` küçük sınama setinin eşiği tetiklemesi ·
  `R-18` dijital tamamlayıcının terk edilmesi.
- **Hiçbir risk silinmedi.**

### Yayım
- GitHub: `emredogan-cloud/sewing-pattern-fitting-series` — **public**,
  **marka-nötr ad**, CI **yeşil** (7/7 iş).
- `.gitignore` genişletildi: indirilmiş kaynak belgeleri, katılımcı
  verisi, ek sır ve önbellek desenleri.

### YAPILMAYAN
Manüskript · figür · kapak · KDP dosyası · reklam kampanyası ·
fiziksel sınama · fark testi · Faz 2.

---

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
