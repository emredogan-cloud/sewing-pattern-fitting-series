# EXTERNAL DEPENDENCIES — depo dışında yapılması gereken işler

> **Bu belgenin varlık nedeni tek bir cümledir:**
>
> # Yapılmamış bir dış ölçüm, yapılmış gibi kaydedilemez.
>
> Ajan bu depodan bir toile dikemez, bir insana soru soramaz, bir
> matbaadan prova alamaz, bir KDP hesabına giremez ve bir marka
> vekiline danışamaz. Bu belge o işleri **hazırlar**, sahibini
> **adlandırır** ve hangi kapıyı **kilitlediklerini** yazar.
>
> Durum sözlüğü `ROADMAP_PROGRESS.md` ile aynıdır:
> `NOT STARTED` · `IN PROGRESS` · `READY FOR REVIEW` ·
> `EXTERNAL VALIDATION REQUIRED` · `PASS` · `FAIL` · `REVISE` · `BLOCKED`

---

## 0 · Özet

| # | Bağımlılık | Sahip | Durum | Engellediği kapı | Engelleyici mi |
|---|---|---|---|---|---|
| **D-01** | Fark testi — üç gerçek ev dikişçisi | Kurucu | `EXTERNAL VALIDATION REQUIRED` | `book-01 phase3-pilot` | **EVET — HARD STOP** |
| **D-02** | Fiziksel doğrulama — 2 toile + 19 `VAL` kaydı | Kurucu | `EXTERNAL VALIDATION REQUIRED` | `book-01 phase3-pilot` | **EVET — HARD STOP** |
| **D-03** | `BEFORE YOU CUT` profesyonel marka temizliği | Kurucu + marka vekili | `NOT STARTED` | `book-01 phase7 / kapak + metadata` | EVET (yayın öncesi) |
| **D-04** | Rakip akış takibi — 13 yeni başlık, 90 gün | Kurucu | `NOT STARTED` | hiçbiri — karar besler | hayır |
| **D-05** | `T3` rakam okunabilirliği — üç insan okuyucu, gerçek kâğıt | Kurucu | `EXTERNAL VALIDATION REQUIRED` | `book-01 phase6-format` | hayır (Faz 2 kapanabilir) |
| **D-06** | `T4`/`T6` + KDP Previewer + fiziksel prova baskı | Kurucu | `NOT STARTED` | `book-01 phase6-format` | EVET (P6) |
| **D-07** | Ücretsiz kaynak edinimi — TAMU/USDA/MSU | Kurucu veya ajan | `NOT STARTED` | hiçbiri | hayır |
| **D-08** | Kitap 3 çizim sistemi kaynakları | Kurucu | `NOT STARTED` | `book-03 phase1-spec` | EVET (Kitap 3) |
| **D-09** | Kitap 2 spiral/wire-o üretim fizibilitesi | Kurucu | `NOT STARTED` | `book-02 phase1-spec` | hayır (Kitap 1'i etkilemez) |

**Kitap 1'i şu anda durduran iki kalem: `D-01` ve `D-02`.**
İkisi de `phase3-pilot` kill-gate'idir ve ikisi de bu depodan
ölçülemez. Faz 4 (tam içerik üretimi) bu ikisi PASS olmadan
**AÇILAMAZ** — `06_BUILD/kill_gate.py` mekanik olarak engeller.

---

## D-01 · Fark testi — üç gerçek ev dikişçisi

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | Üç ev dikişçisine, aynı uyum sorunu hakkında iki metin yan yana gösterilir: bizim pilot teşhis bölümümüz ve bir rakibin aynı konudaki bölümü. Okurdan hangisini tercih ettiği **SORULMAZ**; ne fark ettiği açık uçlu sorulur. |
| **Sahip** | **Kurucu** |
| **Neden ajan yapamaz** | Gerçek insan gerekir. **AI vekil SAYILMAZ** ve `series_config.json → aiProxyCountsAsHuman` bayrağı `false`'tur; `selftest.py` bu bayrağın açılamayacağını her koşuda kanıtlar (`DECISIONS.md K6`). |
| **PASS koşulu** | Üç okurdan **en az ikisi** farkı **kendiliğinden** söyler |
| **1–2 katılımcı bulunursa** | Sonuç **`INCONCLUSIVE`** — PASS değil, FAIL değil. `measured` `false` kalır, kapı **kapalı kalır** (`K30`) |
| **FAIL sonucu** | Farklılaşma hipotezi çürük → **SERİ DURUR** |
| **Hazır olan** | Eleme ölçütleri · üç soruluk ön eleme · beş bulma kanalı · teşvik politikası · taraf tutma kuralları · oturum betiği · kayıt formu · malzeme spesifikasyonu — `BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/DIFFERENTIATION_TEST.md § 5–6` |
| **Faz 2'de eklenen** | Pilot kesitin **figürleri** artık üretilebiliyor (`06_BUILD/figure_engine.py`). Test malzemesinin görsel yarısı hazır. |
| **Hâlâ eksik** | ① katılımcılar ② pilot bölümün nihai metni (Faz 3 çıktısı) |
| **Gereken kanıt** | Üç katılımcının kayıtlı yanıtı; `series_config.json → killGates.differentiationTest.measured = true` ve `measuredDecision` |
| **Gizlilik** | Kayıt formu **kimlik bilgisi taşımaz**. Ham not, iletişim bilgisi, ses/görüntü kaydı depoya **GİRMEZ** (`.gitignore` — `**/participants/`, `**/*_PII.*`, `*.wav`, `*.m4a`) |

---

## D-02 · Fiziksel doğrulama — 2 toile + 19 `VAL` kaydı

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | `A13` kapsamı (`DECISIONS.md K29`): 2 toile + 3 yedek parça, tek vücut, 19 `VAL-xxxx` kaydı, ≈$15–30 malzeme, ≈20–25 saat. Pilotun **her diyagramı** kalıba uygulanır, muslin dikilir, beklenen sonuç ölçülür. |
| **Sahip** | **Kurucu** |
| **Neden ajan yapamaz** | Kumaş, iğne, dikiş makinesi ve bir vücut gerekir. |
| **PASS koşulu** | Diyagram hata oranı **%0** |
| **FAIL sonucu** | >%0 → pilot durur, kök nedenden düzeltilir. **>%5 → üretim yöntemi REDDEDİLİR, proje durur** |
| **Hazır olan** | `BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/VALIDATION_PROTOCOL.md` · `00_CONTEXT/VALIDATION_PROTOCOL.md` |
| **Faz 2'de eklenen** | Sınanacak figürler artık **var**: 154 figür üretildi ve altı `toile_state` figürü doğrudan sınama talimatıdır (`toile_marking_*`, `toile_pin_test`, `toile_slash_test`, `toile_control_toile`). Fiziksel sınama artık "bir gün çizilecek diyagramları" değil, **elde duran PDF'leri** sınayacaktır. |
| **Gereken kanıt** | 19 `VAL-xxxx` kaydı; her figürün `physical_validation_ref` alanı doldurulur ve `verification_status` → `physically_validated`. `validate_spec.py § check_figure_tokens` bu yükseltmeyi **kanıtsız kabul etmez**. |
| **Gizlilik** | Prova **fotoğrafları depoya GİRMEZ** — gerçek bir kişinin vücut görüntüsüdür (`CONTENT_PROTECTION.md § 3`; `validate_structure.py § check_photo_leak` mekanik olarak engeller). Yalnızca **ölçüm kaydı** girer. |

---

## D-03 · `BEFORE YOU CUT` profesyonel marka temizliği

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | Seçilen ad için bir marka vekilinden **temizlik araştırması** (clearance search): federal sicil, eyalet sicilleri, ortak hukuk kullanımı, alan adı ve sınıf 16 (basılı yayın) / sınıf 41 (eğitim) çakışması. |
| **Sahip** | **Kurucu** (talep) + **marka vekili** (yürütme) |
| **Neden ajan yapamaz** | ① Marka temizliği bir **hukuki hizmettir**; bu depoda yapılan tarama onun yerine geçmez. ② Federal sicilin arama arayüzü otomatik sorguya kapalıydı. |
| **Şu anki durum** | `series_config.json → brandClearanceStatus = "founder-approved-working-name"` — **hukuki temizlik DEĞİLDİR** ve öyle sunulamaz. `validate_structure.py § check_public_name_is_declared` `"professionally-cleared"` değerinin **kanıtsız** yazılmasını engeller. |
| **Ne zaman gerekir** | **Kapak ve metadata üretiminden ÖNCE** (`book-01 phase7`). Faz 2 ve Faz 3 bu bağımlılıkla engellenmez — çünkü ne pilot metni ne de figürler seri adını taşır. |
| **Yanlış giderse** | Bir listeleme kaldırma bildirimi üç kitabın kapağını, metadata'sını ve kurulmuş arama görünürlüğünü **aynı anda** sıfırlar (`RISK_REGISTER R-12`) |
| **Ara azaltma — yapıldı** | GitHub deposu marka-nötr adla açıldı (`K32`); hiçbir ad kamuya taahhüt edilmedi; `check_retired_name_leak` reddedilmiş adın kamuya dönük yüzeye sızmasını engelliyor. |

---

## D-04 · Rakip akış takibi — 13 yeni başlık, 90 gün

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | Araştırma raporu § 35 madde 6: Haz–Ağu 2026'da pazara giren 13 yeni başlığın **yorum sayısı ve BSR gelişimi** 90 gün izlenir. Ayda bir gözlem yeterlidir. |
| **Sahip** | **Kurucu** |
| **Neden ajan yapamaz** | Gözlem **zamana yayılmış** olmalıdır; tek seferlik bir sorgu bir eğilim üretmez. Ayrıca pazar yeri gözlemi `marketplace_observation`'dır ve **asla teknik otorite değildir** (`SOURCING_STANDARD § 1`). |
| **Terk koşulu — önceden yazılı** | Biri **6 ayda 200+ yoruma** ulaşırsa niş bizim girişimizden önce kapanmış demektir. |
| **Hazır olan** | `08_REPORTS/tracked/COMPETITOR_TRACKING_SHEET.md` — boş kayıt formu, alanları ve ölçüm kuralları yazılı |
| **Engellediği kapı** | Hiçbiri. Bu bir **karar besleyicisidir**, bir kapı değil. |

---

## D-05 · `T3` rakam okunabilirliği — üç insan okuyucu, gerçek kâğıt

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | 6–7 pt'de basılmış `1 l I 0 O 6 8 9 3 5` dizisi gerçek kâğıda basılır ve **üç kişiye okutulur**. Geçme ölçütü: **sıfır yanlış okuma** (`TYPOGRAPHY_STANDARD § 4`). |
| **Sahip** | **Kurucu** |
| **Neden ajan yapamaz** | Okunabilirlik bir **insan algısı** ölçümüdür. Faz 2'nin piksel farkı ölçümü (`03_VISUAL/font_legibility_scan.json`) bunun **yerine geçmez** ve öyle sunulmaz. |
| **Faz 2'de yapılan** | Piksel düzeyinde ön eleme: `Inter` **elendi** (`l`/`I` piksel farkı **0,0** — iki karakter aynı). `Atkinson Hyperlegible` ve `Atkinson Hyperlegible Next` `Y1` gereksiniminde **elendi**. Kalan sıralama: `Source Sans 3` (en kötü çift 0,391) > `IBM Plex Sans` (0,347) > `Lexend` (0,333). |
| **Hazır olan** | Basılacak test sayfası `06_BUILD/calibrate_tokens.py --keep <yol>` ile üretilir |
| **Başarısız olursa** | Figür içi etiketler `IBM Plex Sans`'a geçer; gövde metni ve başlıklar **değişmez** (`TYPOGRAPHY_STANDARD § 3.3` geçiş koşulu, `DECISIONS.md K38` ile güncellendi) |

---

## D-06 · `T4` · `T6` · KDP Previewer · fiziksel prova baskı

| Alan | |
|---|---|
| **Tam olarak ne yapılacak** | ① Gerçek KDP maliyet hesaplayıcısıyla baskı maliyeti ölçülür. ② Seçilen trim/cilt seçeneğinin **mevcut olduğu** doğrulanır. ③ **KDP Previewer'ın kendisi** çalıştırılır. ④ Fiziksel prova baskı alınır; **düz açık durma** ve figür okunabilirliği elle test edilir. |
| **Sahip** | **Kurucu** (KDP hesabı gerekir) |
| **Neden ajan yapamaz** | KDP hesap işlemi ve fiziksel baskı. |
| **Faz 2'de yapılan** | Sayfa geometrisi KDP'nin **yayımlanmış asgarilerine** göre kuruldu ve `qa_visual.py § ⑨` her koşuda denetliyor (`S-0016`). Çizgi kalınlıkları 300/600 dpi'de 1-bit rasterda **ölçüldü**. |
| **Faz 2'nin ÖLÇMEDİĞİ** | **Mürekkep yayılması (dot gain).** Talep-üzerine baskıda 0,4 pt bir çizgi kalınlaşır ve 6 pt bir tırnak dolar. Dijital raster bunu **göstermez**. `visual_language_tokens.status` bu yüzden `CALIBRATED_DIGITAL_RENDER`'dır, düz `CALIBRATED` değil. |
| **Engellediği kapı** | `book-01 phase6-format` — dört maddenin dördü de yapılmadan bu kapı geçilemez |

---

## D-07 · Ücretsiz kaynak edinimi

| Alan | |
|---|---|
| **Ne** | TAMU uzatma serisinin elle indirilmesi · USDA 1945 bültenleri · MSU taramalarının **gözle** okunması |
| **Maliyet** | **Sıfır** — hiçbiri ücretli değildir |
| **Sahip** | Kurucu veya ajan (erişim engeli varsa kurucu) |
| **Neden bekliyor** | Faz 1 için gerekli değildi (`K19`); iki tanesi tarayıcı-arkası PDF ve otomatik indirmeye kapalıydı |
| **Engellediği kapı** | Hiçbiri. 43 belirtinin doğrulama durumunu **iyileştirebilir** ama fiziksel doğrulamanın (`D-02`) yerine geçmez — belirtilerin birincil doğrulaması **fizikseldir**. |

---

## D-08 · Kitap 3 çizim sistemi kaynakları

| Alan | |
|---|---|
| **Ne** | En az **iki bağımsız çizim sistemi**nin tam metni; ölçü tanımlarının `S-0014` (ISO 8559-1) veya eş otoriteyle hizalanması |
| **Sahip** | **Kurucu** (edinim bütçesi kararı) |
| **Neden gerekli** | Bu depoda hiçbir kalıp çizim referansı yoktur ve 12 blok bileşeninin **hiçbiri** kaynağa bağlı değildir. Eldeki altı kurumsal kaynağın hepsi *var olan bir kalıbın düzeltilmesini* anlatır, *sıfırdan çizimi* değil. |
| **Hazır olan** | `BOOK-03-DRAFT-YOUR-OWN-BLOCK/00_SPEC/DRAFTING_SYSTEM_RESEARCH.md` — dört sistem ailesi, yedi ölçüt, kanıt kapısı · `01_SOURCE/ACQUISITION_REQUEST_QUEUE.md` |
| **Engellediği kapı** | `book-03 phase1-spec` — `A10` bu kanıt olmadan kapanamaz (`K27`) |

---

## D-09 · Kitap 2 spiral / wire-o üretim fizibilitesi

| Alan | |
|---|---|
| **Ne** | KDP **spiral cilt sunmuyor** (`K22`). Kitap 2 bir referans atlasıdır ve düz açık durmazsa ürün gereksinimini karşılamaz (`R-09`). KDP dışı bir üretim yolunun maliyeti ve fizibilitesi araştırılmalıdır. |
| **Sahip** | **Kurucu** |
| **Engellediği kapı** | `book-02 phase1-spec`. **Kitap 1'i engellemez** — Kitap 1 ciltsiz bir teşhis kitabıdır ve düz açık durma gereksinimi Kitap 2 kadar sert değildir. |

---

## 1 · Bu belgenin kuralı

Bir satırın durumu **yalnızca gerçekleşmiş bir dış olayla** değişir.
Ajan hiçbir satırı `PASS`'e çeviremez. `D-01` ve `D-02` için ayrıca
mekanik bir kilit vardır: `series_config.json → killGates.*.measured`
alanları ve `06_BUILD/kill_gate.py`.

> Bir kapıyı ilerleten şey **ÖLÇÜM**, ya da açıkça kaydedilmiş bir
> **KURUCU GEÇERSİZ KILMASIDIR**. İkisi ayrı alanlardır ve
> birbirinin yerine geçmez.

---

*Vâliçe Press · BEFORE YOU CUT · External Dependencies · 28 Ağustos 2026 (Faz 2 yürütmesi)*

---

## D-10 · WSU E.M. 2246 "Garment Fitting" (1962) — edinim

| Alan | |
|---|---|
| **Ne** | Washington State University Agricultural Extension Service, E.M. 2246, *Garment Fitting*, Hazel L. Roberts, Aralık 1962. |
| **Neden gerekli** | Faz 4 bağımsız incelemesi, deponun `S-0004` olarak kaydettiği WSU belgesinin (EM4582) uyum içeriğinin **tek sayfa, beş madde** olduğunu ve kitabın dört çekirdek kuralından ikisini **içermediğini** tam metin okuyarak ölçtü (`R-23`). İncelemeci, WSU'nun bu konuda yayımladığı **asıl** belgeyi buldu: E.M. 2246 tam bir uyum yayınıdır ve **belirti→neden listesi taşır** — yani `CC-22` ve `CC-24`'ün, ayrıca `SYM-004`'ün ayrım probleminin gerçek kaynağı olabilir. |
| **Nerede** | `content.libraries.wsu.edu` dijital koleksiyonu (incelemeci erişti ve iki girdisini birebir alıntıladı) |
| **Engelleyici mi** | **Hayır** — kitap onsuz üretildi ve ilgili iddialar *kaynaksız olduklarını beyan ederek* duruyor. Ama Faz 5'te edinilirse üç iddia `INFERRED`'dan yükselebilir. |
| **Kim** | Ajan (erişilebilir görünüyor) |
| **Durum** | **AÇIK** — Faz 5 |

## D-11 · Faz 4 iddialarının ikinci tur kaynak denetimi

| Alan | |
|---|---|
| **Ne** | 18 kaynak kaydının **tam metin** okunarak, atıf yapılan her iddiayı gerçekten içerip içermediğinin denetlenmesi. |
| **Neden gerekli** | Faz 4'te dört atıfın kaynağında karşılığı olmadığı ölçüldü (`R-23`). Denetlenen kaynaklar yalnızca incelemenin dört hattının değdiği kısımdır; **kalan 18 kayıt tam metin okunmadı.** |
| **Engelleyici mi** | Hayır — ama `CLAIM_SOURCE_MAP.md`'deki `VERIFIED` sayısının (56) gerçek olduğu ancak bundan sonra söylenebilir. |
| **Kim** | Ajan |
| **Durum** | **AÇIK** — Faz 5 |

---

## Faz 5 sonrası durum — 29 Ağustos 2026

Faz 5 **hiçbir dış bağımlılığı kapatmadı ve kapatamazdı.** Faz 5 içsel
bir kalite güvence fazıdır; `D-01` ve `D-02` gerçek insanların gerçek
kumaşla yapacağı ölçümlerdir.

| # | Bekleyen | Faz 5 girişi | **Faz 5 çıkışı** | Engelleyici |
|---|---|---|---|---|
| `D-01` | Fark testi — 3 ev dikişçisi | 0/3 · `measured: false` | **0/3 · `measured: false`** | **EVET — HARD STOP** |
| `D-02` | Fiziksel doğrulama — 19 `VAL` | 0/19 · `measured: false` | **0/19 · `measured: false`** | **EVET — HARD STOP** |
| `D-03` | Marka temizliği | yapılmadı | yapılmadı | EVET (yayın öncesi) |
| `D-06` | KDP Previewer + prova baskı | yapılmadı | yapılmadı | EVET (Faz 6) |
| `D-07` | Ücretsiz kaynak edinimi | yapılmadı | yapılmadı | hayır |

### Faz 5'in `D-06` için ürettiği girdi

Faz 5 **dijital** bir baskı simülasyonu koştu (300 dpi, 1-bit, 23
temsilci sayfa) ve şunu ölçtü: yapısal çizgiler ≥ 2 px ile hayatta,
etiketler okunur, akış şeması hiyerarşisi korunuyor.

> **Bu bir FİZİKSEL PROVA DEĞİLDİR.** Kâğıt, mürekkep yayılması, cilt
> kıvrımı ve gerçek okuma mesafesi ölçülmedi. `D-06` açıktır.

Faz 5 ayrıca `D-06`'ya iki karar taşıdı:
* **`R-27`** — belirti figüründe teşhis işareti gövdeden hafif çiziliyor
  (0,6 pt / 1,2 pt). Düzeltmesi token ağırlığı değişikliğidir ve baskı
  kalibrasyonunun yeniden koşulmasını ister.
* **`A-04`** — iki figür alanı inç etiketli, kitabın geri kalanı metrik.
  Birim politikası kararı gerekiyor.

### Faz 5'in `D-07` için ürettiği girdi

Dört `CONTESTED` ölçü (`M-004` bel · `M-008` bilek · `M-013` boyun
tabanı · `M-025` iç dikiş) **yalnızca daha iyi kaynakla** kapanır.
`S-0014` (ISO 8559-1:2017) ve `S-0015` (ASTM D5219) tam olarak bu
tanımları yönetir ve **ikisi de edinilmedi**. Bunlar edinilirse sekiz
`CONTESTED` iddia çözülebilir.

---

*Vâliçe Press · BEFORE YOU CUT · External Dependencies · 29 Ağustos 2026 (Faz 5 yürütmesi)*
