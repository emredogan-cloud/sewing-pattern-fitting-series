# DECISIONS — karar kaydı

> Kural (kardeş projelerden devralındı): bir varsayım sessizce proje
> gerekliliğine dönüşemez. Açık kararlar `OPEN_QUESTIONS.md`'de;
> **alınmış** kararlar burada.

---

## K1 · Proje mimarisi kardeş projelerden devralındı, içerik değil

**28 Ağustos 2026 · Faz S0**

Tam gerekçe: `00_CONTEXT/REFERENCE_SYNTHESIS.md`. Özet: `paths.py`/
`schema_lite.py` deseni, `.gate` mekanizması, K#/A# kaydı, `selftest.py`
felsefesi, faz raporu durum sözlüğü ve "ölçülen / geçersiz kılınan /
ölçülmemiş" üç durumunun ayrılığı BİREBİR devralındı. Kill-gate modeli,
içerik koruma modeli ve kapı katmanlaması bilinçli olarak DEĞİŞTİRİLDİ.

## K2 · Ortak kütüphane: depolar arası YOK, depo içi VAR

**28 Ağustos 2026 · Faz S0**

Kardeş projelerin "ortak kütüphane YOK" kuralı **depolar arasında**
aynen yürürlüktedir — hiçbir kardeş depo bu deponun build'i için
gerekli değildir (`validate_structure.py § check_no_sibling_dependency`
mekanik olarak denetler; mimari ATIF yorumları serbesttir, yalnızca
gerçek bağımlılık bağlamları hata verir).

**Depo içinde** ise üç kitap TEK araç zinciri paylaşır. Gerekçe:
araştırma raporu § 31 diyagram kütüphanesinin amortismanını kazananın
**en somut üretim avantajı** olarak işaretledi; üç ayrı doğrulayıcı
kopyası bu avantajı doğrudan yok eder ve zamanla birbirinden sapardı.

## K3 · İki katmanlı kapı sistemi

**28 Ağustos 2026 · Faz S0**

Kardeş projelerin hepsi tek kitaplıktır ve tek düz bir `.gate` taşır.
Bu depo üç kitap taşır ve kitaplar kısmen paralel ilerler — tek düz bir
kapı bunu ifade edemez.

Çözüm: seri kapısı (`.gate`, kökte) + kitap kapısı (`BOOK-xx/.gate`).
`paths.gate_at_least()` sırayı AÇIKÇA parametre alır; iki katman
yanlışlıkla karşılaştırılamaz.

## K4 · Kitap dizinleri kardeş numaralandırmasının ALT KÜMESİDİR

**28 Ağustos 2026 · Faz S0**

Kitap klasörleri `00_SPEC` · `02_CONTENT` · `03_VISUAL` ·
`04_EDITORIAL` · `05_APLUS_COVER` · `08_REPORTS` · `09_OUTPUT` taşır.
`01_SOURCE`, `06_BUILD`, `07_TESTS`, `10_ARCHIVE` **seri düzeyindedir**
(K2). Numaralandırma kardeş projelerle aynı anlamı korur; yalnızca
seri düzeyine taşınanlar kitapta tekrarlanmaz.

Kardeş projelerdeki `00_CONTEXT` yerine kitapta `00_SPEC` kullanılır:
politika belgeleri seri düzeyinde tektir, kitap düzeyinde olan şey
politika değil **spesifikasyondur**.

## K5 · Kill-gate: ikili DIŞ ÖLÇÜM modeli

**28 Ağustos 2026 · Faz S0**

| Proje | Model |
|---|---|
| Sigorta | Oran eşiği (SME onay oranı ≥%90) |
| Hangıl | Kusur şiddeti (HARD_STOP / REVISE / PASS) |
| **TRUE FIT** | **İki bağımsız DIŞ ölçüm** |

① **Fark testi** — üç gerçek ev dikişçisi; en az ikisi farkı
kendiliğinden söylemeli (araştırma raporu § 35 madde 1).
② **Fiziksel doğrulama** — her diyagram gerçekten kalıba uygulanır,
toile dikilir; hata oranı >%0 pilotu durdurur, >%5 üretim yöntemini
reddeder (§ 35 madde 2).

Kritik fark: bu kill-gate **depo içinden ölçülemez**. `kill_gate.py`
bu sınırı adından ve çıktısının ilk satırından itibaren duyurur.

## K6 · Dış uzman İŞE ALINMAYACAK — ve AI vekil onun yerine SAYILMAZ

**28 Ağustos 2026 · Faz S0**

Sigorta projesinin K9'u ve Hangıl projesinin K5'i ile aynı kurucu
kısıtı. Bağımsız çelişmeli AI incelemesi kullanılacak, ama asla insan
uzman yerine sayılmayacak.

`series_config.json → killGates.differentiationTest.aiProxyCountsAsHuman`
`false`'tur ve **açılamaz** — `kill_gate.py` bunu ayrı bir engel olarak
yakalar. Bu, Hangıl projesinin K20 kaydından (28 Ağustos 2026: kurucu
insan-kullanılabilirlik kriterini geçersiz kıldı, ölçüm değişmedi)
doğrudan öğrenilen bir sertleştirmedir.

Yasak etiketler ve mekanik koruma: `00_CONTEXT/CLAIMS_STANDARD.md § 1`,
`qa_claims.py § ①`.

## K7 · "Basılı format avantajı" iddiası KALICI OLARAK korumaya alındı

**28 Ağustos 2026 · Faz S1**

Araştırma raporunun § 27 girdi geçerliliği testinde altı iddiadan
beşi doğrulandı; düşen tek iddia "basılı formatın gerçek bir avantajı
var" oldu (**ZAYIF**). Rapor bunu puanı yükseltmek için kullanmadı.

Bu proje de kullanamaz: hiçbir konumlandırma, bölüm metni, kapak
kopyası veya reklam metni bu iddiaya dayanamaz. Mekanik koruma:
`qa_claims.py § ②`. Bu, Hangıl projesindeki A6 hafıza-iddiası
korumasının bu projedeki karşılığıdır.

## K8 · Ortam kararı VERİLMEDİ — çerçeveye bağlandı

**28 Ağustos 2026 · Faz S1**

"Video ekleyelim mi" sorusu tek bir soru olarak sorulamaz; dört alt
soruya bölündü (`MEDIUM_DECISION_FRAMEWORK.md § 2`). Karar
`OPEN_QUESTIONS A4`. Kararsızlık hâlinde varsayılan: **karar ertelenir,
varsayılmaz** — sayfa düzeni QR alanına yer bırakacak biçimde
tasarlanır (geri dönülebilir seçenek).

Bir sert kural karardan bağımsız yürürlüktedir: **basılı kitap
videolara erişilmeden tam işlevli olmalıdır.**

## K9 · İçerik koruma modeli yeniden tasarlandı — üç hat

**28 Ağustos 2026 · Faz S0**

"Cevap anahtarı" modeli uygulanmaz (kalıp geometrisi sır değildir,
araştırma raporu § 21). Yerine üç hat: ① yayın-öncesi içerik,
② **fiziksel doğrulama fotoğrafları** (gerçek insan bedeni — kardeş
projelerin hiçbirinde olmayan gizlilik kısıtı), ③ telif korumalı
referans malzeme. Gerekçe: `00_CONTEXT/CONTENT_PROTECTION.md`.

## K10 · Doğrulama durumu ücretsiz verilmez — dört basamak

**28 Ağustos 2026 · Faz S1**

`agent_drafted_unverified` → `agent_reviewed` →
`technical_reference_verified` (≥1 `fulltext`/`official_pdf` kaynak
GEREKİR) → `physically_validated` (bir `VAL-xxxx` kaydı GEREKİR).

`validate_spec.py § check_verification_evidence` mekanik olarak
dayatır. **Faz 1 sonunda 106 taksonomi kaydının tamamı en alt
basamaktadır** ve bu, açıkça kaydedilmiş bir sınırdır.

## K11 · Kardeş projelerde olmayan iki yeni kapı yazıldı

**28 Ağustos 2026 · Faz S1**

`qa_boundary.py` — çok kitaplı bir seride en büyük içerik riski
kitapların birbirini yemesidir; tek kitaplı kardeşlerde karşılığı yok.
`qa_claims.py` — iki gerçek dış kısıt (KDP marka yasağı + zayıf çıkan
"basılı avantaj" iddiası).

## K12 · Türkçe büyük "İ" kusuru BAŞTAN kapatıldı

**28 Ağustos 2026 · Faz S1**

Sigorta projesinde `qa_legal_language.py`'nin dürüst inkârları
("X DEĞİLDİR") Türkçe büyük "İ" Unicode kusuru yüzünden yanlış
yakaladığı SONRADAN bulunmuştu. Bu projede `qa_claims.py` ve
`qa_terminology.py` ilk sürümden itibaren `_fold()` ile Unicode-doğru
katlama yapar ve inkâr farkındalığı **cümle** düzeyindedir, pencere
düzeyinde değil. Regresyon testi: `07_TESTS/selftest.py`.

## K13 · Sınır matrisi düzeltildi — TOPİK BÖLME ile

**28 Ağustos 2026 · Faz S1**

Görev talimatının § 11 başlangıç çerçevesi iki yerde tek-birincil
kuralına aykırıydı (*Measurements*: Kitap 1 ve 3 "Core"; *Muslin*: üçü
de "Core"). Bu bir çelişki değil, bir **çözünürlük eksikliğiydi**.

Çözüm kopyalama değil bölme oldu: `TOP-21` (`TOP-01`'den), `TOP-24`
(`TOP-23`'ten), `TOP-26`/`TOP-27` (`TOP-07`'den). `qa_boundary.py`
kuralı mekanik olarak dayatır.

## K14 · Anahtar kelime belgeleri yasak-eşanlamlı taramasından muaf

**28 Ağustos 2026 · Faz S1**

`qa_terminology.py` ilk çalıştırmasında `SERIES_KEYWORD_ARCHITECTURE.md`
içindeki "wrinkles in bodice sewing" ifadesini yakaladı. Bu **doğru bir
yakalamaydı ama yanlış bir kural uygulamasıydı**: anahtar kelime
belgeleri BİZİM dilimizi değil, ALICININ arama kutusuna yazdığı dili
taşır. İkisini aynı kurala tabi tutmak, hedeflememiz gereken kelimeleri
yasaklamak olurdu.

Ayrı bir `KEYWORD_FILES` muafiyeti eklendi — `GLOSSARY_FILES`'tan
FARKLI bir gerekçeyle ve kodda açıkça ayrı belgelenerek.

## K15 · SYM-043 eklendi — kapsam denetiminin bulduğu boşluk

**28 Ağustos 2026 · Faz S1**

`qa_boundary.py § check_family_reachability` ilk çalıştırmada `AF-19`
(genel boy düzeltmesi) ailesine hiçbir Kitap 1 belirtisinden
ulaşılamadığını buldu. Boşluk `SYM-043` ("başka hiçbir belirti yokken
yalnızca boy yanlış") ile kapatıldı.

**Bu, kapının gerçekten çalıştığının ilk kanıtıdır** ve kayda geçirilir.


## K16 · Türkçe katlama TEK KOPYAYA çıkarıldı — `selftest.py`'nin bulduğu kusur

**28 Ağustos 2026 · Faz S1**

`qa_claims.py` ve `qa_terminology.py` K12 uyarınca Türkçe-güvenli
katlamayla **baştan** yazılmıştı. Ama `07_TESTS/selftest.py`, aynı
kusurun **ÜÇÜNCÜ** bir yerde hâlâ açık olduğunu buldu:
`validate_spec.check_cause_distinguishability` düz `str.lower()`
kullanıyordu ve iki AYNI ayırt edici kanıt metni, biri büyük harfli
olduğunda farklı görünüyordu.

Ders: **koruma üç yerde tekrarlanırsa dördüncü yerde unutulur.**

Katlama `06_BUILD/trfold.py`'de tek kopya hâline getirildi; üç
doğrulayıcı da oradan alır. `selftest.py` iki şeyi ayrıca dayatır:
(a) üç modülün de AYNI fonksiyon nesnesini kullandığı,
(b) büyük harfli bir çift kanıtın ayırt-edicilik denetimini
**atlatamadığı** (regresyon testi).

Bu kayıt, kapının gerçekten çalıştığının **dördüncü** kanıtıdır.


## K17 · Test fixture'ları kardeş depo adını LİTERAL olarak taşıyamaz

**28 Ağustos 2026 · Faz S1**

`validate_structure.check_no_sibling_dependency`, `selftest.py`'nin
KENDİ fixture'ını yakaladı: test, "gerçek bir kardeş-depo bağımlılığı
yakalanıyor mu" diye sınamak için bir sonda dosyasına kardeş depo yolu
yazıyordu — ve o yol satırı `selftest.py`'nin kendi kaynağında literal
olarak duruyordu.

Bu, kardeş sigorta projesinde SONRADAN bulunan **"doğrulayıcı kendi
araç zincirini tarıyor"** kusurunun tam karşılığıdır (`K12` ailesinden).

**İki çözüm vardı:**
(a) `selftest.py`'yi taramadan muaf tutmak — kapıyı ZAYIFLATIR;
(b) fixture dizesini çalışma anında `series_config.json`'dan üretmek.

**(b) seçildi.** Kapı hiçbir muafiyet almadı; yanlış pozitif kaynağında
ortadan kalktı. Test hâlâ ikisini de kanıtlıyor: mimari ATIF yorumu
ihlal sayılmıyor, gerçek BAĞIMLILIK yakalanıyor.

Bu kayıt, kapının gerçekten çalıştığının **beşinci** kanıtıdır.

---

*Vâliçe Press · TRUE FIT · Decisions · 28 Ağustos 2026*
