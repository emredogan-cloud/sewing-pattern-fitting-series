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

# FAZ 1 YÜRÜTMESİ — K18…K33

**28 Ağustos 2026.** Kurucu, `A1`–`A14` açık sorularının kapatılabilir
olanlarının kapatılmasını ve Kitap 1 Faz 1'in tam olarak yürütülmesini
talimatlandırdı. Aşağıdaki on altı karar o turun ürünüdür.

Her karar şu beş alanı taşır: **karar · gerekçe · kanıt · değerlendirilen
alternatifler · sonuç · faz.**

## K18 · `A1` — "TRUE FIT" YAYIMLANAN ad olarak kilitlenmez

**Karar.** Ad, depo içi çalışma adı olarak korunur; kapak, metadata,
alan adı ve dijital tamamlayıcı yüzeyinde **kullanılmaz.** Önerilen
yerine geçen: **`BEFORE YOU CUT`**. Nihai seçim ve profesyonel marka
temizliği **kurucu kararıdır**.

**Kanıt.** `TRUE FIT`, True Fit Corporation adına **yürürlükte ve
tescilli** bir ABD markasıdır (reg. 4280126, 22 Oca 2013) ve kapsamı
"kullanıcıları **vücut ölçülerine göre** giysiyle eşleştirme"dir —
yani bu serinin **tam konusu**. `TRUE FIT RECOMMENDATION ENGINE`
(reg. 4851499) ve Sınıf 42 yazılım tescili aynı sahibindir. Alan ayrıca
kalabalıktır (`TRU FIT`, `TRU-FIT`, `TRUE FIT APPAREL`).
`OBSERVED` 28 Ağu 2026 — tam kayıt:
`08_REPORTS/PHASE_1_BRAND_SCREENING.md`.

**Neden "düşük sınıf riski" demek yetmedi.** ① Sektör aynı. ② Ad bir
ŞEMSİYE marka olacak (üç kapak + metadata). ③ `A4`'ün dijital
tamamlayıcısı, marka sahibinin Sınıf 42 tescilinin yaşadığı yüzeydir.
④ Sonucu sert: bir listeleme kaldırma bildirimi üç kitabı aynı anda
sıfırlar (`R-12`). ⑤ Kalabalık alanda ad bize de ayırt edicilik
kazandırmıyor.

**Alternatifler.** `FIT LOGIC` **elendi** — giyim sınıfında tescilli
(Mbrio, L.L.C.), `TRUE FIT`'ten daha kötü. `FIT SIGNS` ve
`THE FIT DIAGNOSIS` ikinci ve üçüncü sırada; ikisi de kalabalık
"FIT ___" alanının içinde.

**Sonuç.** Kapak/metadata üretimi `A1` kapanmadan **başlayamaz**.
GitHub deposu marka-nötr adla açıldı (`K32`).

**Faz.** Kitap 1 `phase2-visual` başlangıcı.

## K19 · `A3` — kamu kaynağı ÖNCE; Faz 1 için sıfır satın alma

**Karar.** Faz 1, **hiçbir ücretli kaynak satın alınmadan** kapatıldı.
15 kaynak kaydı açıldı; altısı teknik otorite taşıyan ve **tam metni
okunmuş** kamu kaynağıdır.

**Kanıt.** `01_SOURCE/PUBLIC_SOURCE_SURVEY.md` — yedi eksende tarama.
Bulunanlar: NMSU C-228 ve C-227, Texas AgriLife E-372, WSU EM4582
(dört üniversite yayım kaynağı), ANSUR II ve NHANES 2021 (iki kamu
malı devlet teknik raporu).

**Sonuç — ölçülebilir.** 32 ölçünün **16'sı** ve 19 düzeltme ailesinin
**13'ü** `technical_reference_verified`'e yükseltildi. Faz 1 başında
bu sayılar 0 ve 0'dı.

**Alternatifler.** (a) bütçe onayı isteyip beklemek — gereksiz oldu;
(b) yalnızca açık kaynakla sınırlı kalıp kapsamı daraltmak — kapsam
daralmadı; (c) fiziksel doğrulamayı tek katman saymak — reddedildi,
`C-A` sınıfı deneyle doğrulanamaz.

**Ne satın alınMADI ve neden.** Dört kalem kuyruğa alındı
(`01_SOURCE/ACQUISITION_REQUEST_QUEUE.md`) ve **hiçbiri Faz 1 için
gerekli değildir**: ISO 8559-1 (≈$230) ve ASTM D5219 (≈$76–90)
**Kitap 3**'te zorunlu; *Fitting and Pattern Alteration* ($135 veya
**kütüphane ödünç: $0**) **Kitap 2**'de; bir kalıp çizim referansı
($45–60) **Kitap 3**'te.

**Faz.** Kitap 1 `phase1-spec` — KAPANDI.

## K20 · Kapı kendi kusurunu buldu — "yükseltilmemiş" ≠ "kanıtsız yükseltilmemiş"

**Bulgu.** `selftest.test_verification_status_is_honestly_recorded`'ın
docstring'i "hiçbir kayıt **sessizce** yükseltilmemiş olmalı" diyordu;
gövdesi ise "hiçbir kayıt yükseltilmemiş olmalı" diye yazılmıştı.

Kaynak sayısı sıfırken ikisi aynı görünüyordu. `K19` gerçek kanıt
üretince test, **doğru davranışı hata olarak** raporladı.

**Karar.** Test, adının söylediği şeyi ölçecek biçimde yeniden yazıldı:
yükseltilmiş **her** kaydın gerçekten `fulltext`/`official_pdf` ve
`technical_authority=true` bir kaynağı var mı. Ayrıca yeni bir kapı
eklendi: `test_verification_summary_matches_records` — `fit_signs.json`'un
ilan ettiği doğrulama özeti gerçek kayıtlarla uyuşmalıdır.

**Neden ikinci kapı.** "43 kaydın tamamı doğrulanmamıştır" cümlesi on
belgede alıntılanıyor. Özet bloğun veriden sessizce sapması, projenin
**en çok tekrarlanan dürüstlük iddiasını** yalana çevirirdi.

**Kanıt.** Kasıtlı bir kusur enjekte edildi (`M-010` kanıtsız
yükseltildi) ve kapı yakaladı.

Bu, kapının gerçekten çalıştığının **altıncı** kanıtıdır
(`K13`, `K15`, `K16`, `K17` zincirinin devamı).

## K21 · `C-G` ease — "yazılamaz"dan "adı konmuş konvansiyonla yazılabilir"e

**Karar.** Bölüm 3.5–3.6 yazılabilir — **üç sert koşulla**: ① sayısal
bant kaynağı **adıyla** anılır; ② bandın **tek bir kurumun
konvansiyonu** olduğu ve kalıp şirketleri arasında değiştiği okura
açıkça söylenir; ③ bölümün **yöntemi** (bitmiş ölçü − vücut ölçüsü =
ease) sayısal banttan **bağımsız** kalır.

**Kanıt.** `S-0001` Table 1, adlandırılmış bir kurumsal ease bandı
tablosu taşır ve tablonun kendisi "ease miktarları kalıba, kumaşa ve
tercihe göre değişir" uyarısıyla gelir.

**Neden bu bir sektör standardı DEĞİL.** Tek bir üniversite yayımının
bandıdır. Bir sektör standardı (`S-0014`/`S-0015`) hâlâ edinilmemiştir.
③ numaralı koşul, bant sonradan değişse bile bölümün ayakta kalmasını
garanti eder.

**Faz.** Kitap 1 `phase4-production`.

## K22 · `A5` — format

**Karar.** Kitap 1 birincil SKU: **8,5×11 ciltsiz, beyaz kâğıt.**
Ciltli (8,25×11) ikinci SKU **adayı**, P6'da karara bağlanır.
Kindle **ertelendi**. Spiral **KDP'de yok**.

**Kanıt.** `S-0009`…`S-0013` (KDP yardım sayfaları, 28 Ağu 2026):
KDP yalnızca yapıştırma ciltsiz ve ciltli sunar — **spiral/tel sarmal
YOKTUR**. 8,5×11 ciltsiz 24–590 sayfa; ciltli listesinde 8,5×11 yok,
en yakını **8,25×11**.

**Sonuç — sayılarla.** 236 sayfada siyah mürekkep baskı maliyeti
**$5,01**; $26,99'da birim telif **$11,18**. Ciltli 8,25×11: maliyet
$9,66, $34,99'da telif **$11,33** — ciltli ekonomik olarak anlamlıdır
ama **ayrı bir iç dosya** ister.

**Groundwood kâğıt reddedildi:** sayfa başına ≈%5 ucuz ama 0,4–0,6 pt
yardımcı çizgiler ve tramlar o kâğıtta kaybolur. Kazanç ≈$0,20/kopya.

**Kitap 2 sonucu.** Kitap 2'nin düz açık durma gereksinimi KDP dışı bir
üretim yolu ister → **Kitap 2 `phase1-spec` görevi** (`R-09` güncellendi).

**Faz.** Kesinleşme: `phase6-format` doğrulama kapısı.

## K23 · `A6` — renk: siyah mürekkep, ölçülebilir bir yeniden açılma eşiğiyle

**Karar.** **Siyah mürekkep, beyaz kâğıt.** Premium renk **aritmetik
olarak dışarıda**; standart renk mümkün ama seçilmedi.

**Kanıt.** 236 sayfa, 8,5×11 (large trim): premium renk baskı maliyeti
**$19,88** → asgari liste fiyatı **$33,14**, gözlemlenen pazar
medyanının ($21–23) ve fiyat bandımızın üst ucunun ($28,99)
**üstünde**. Standart renk $10,49 → $26,99'da telif $11,18'den
**$5,71'e** düşer (**−%49**).

**Ayrıca: "seçmeli renk" bir seçenek DEĞİLDİR.** Mürekkep türü kitabın
tamamı için seçilir; on sayfası renkli bir kitap tüm sayfaları için
renkli ücret öder.

**Karar neden ucuzluk kararı değil.** `VISUAL_STANDARD § 3–4` anlamı
**çizgi kalınlığı ve tonla** taşır, renkle değil — bu, renk kararından
ÖNCE verilmiş bir tasarım kararıdır. Renk bu üründe ikinci bir anlam
kanalı değil, bir **cila**dır.

**Yeniden açılma eşiği — bir zevk tartışması değil.** Faz 2'de
`color_required` gerekçesiyle işaretlenen figürlerin oranı **%10'u
aşarsa** `A6` otomatik olarak yeniden açılır ve **standart renk**
(premium değil) yeniden değerlendirilir.

**Karşı argüman kaydedildi:** rakiplerin bir kısmı renkli fotoğraf
kullanıyor ve alıcı bunu bekliyor olabilir (`R-05` **azalmadı**).

## K24 · `A7` — tipografi: $0, yalnızca açık lisans

**Karar.** Metin **Source Serif 4**, başlık/tablo/figür etiketi
**Source Sans 3**, ikisi de SIL OFL 1.1. Figür etiketi yedeği
**Atkinson Hyperlegible**. **Ticari yazı tipi satın alınmayacaktır.**

**Kanıt.** SIL OFL 1.1 altındaki bir yazı tipi ticari olarak satılan
bir belgeye **gömülebilir**; gömme lisans anlamında dağıtım sayılmaz ve
belgenin kendi lisansını değiştirmez `OBSERVED` 28 Ağu 2026.
Source Serif 4 `frac`/`numr` OpenType özelliklerini taşır `OBSERVED`.

**Ürünün gerçek gereksinimi.** ABD ev dikişinin dili kesirdir ve
standart dikiş payı **⅝ inç**tir. Kesir yanlış dizilirse ölçüm zinciri
kayar. Ayrıca figür etiketindeki bir rakamın yanlış okunması okurun
kumaşını götürür — bu, tipografinin bu üründeki **tek gerçek risk
noktasıdır**.

**Alternatifler.** Charis SIL **elenmedi, yedek olarak adlandırıldı**
(düşük kaliteli baskı için tasarlanmıştır; POD tam olarak o koşuldur).
EB Garamond ve Libre Baskerville elendi — küçük puntoda ve POD'da fazla
ince.

**Sonuç.** `TYPOGRAPHY_STANDARD.md` altı test tanımladı (`T1`–`T6`) ve
hepsi Faz 2'nin çıkış koşullarına eklendi.

## K25 · `A4` — ortam: basılı kitap + TEK ADRESLİ dijital tamamlayıcı

**Karar.** Basılı kitap **kendi başına eksiksizdir**. Tek bir kalıcı
adres taşıyan bir dijital tamamlayıcı vardır ve içeriği **üç kalemle**
sınırlıdır: yazdırılabilir boş formlar · akış şemalarının renkli
sürümü · düzeltme (errata) sayfası. **Sayfa başına QR REDDEDİLDİ.
Video kapsam dışı.**

**Gerekçe — en önemli bulgu.** Hareketli gösterim gerektiren beş içerik
türü adlandırıldığında **üçünün Kitap 2'ye ait olduğu** görüldü.
Kitap 1'in içeriği (teşhis) yapısal olarak durağandır; Kitap 2'nin
içeriği (işlem) yapısal olarak hareketlidir.

> QR/video sorusu aslında bir Kitap 1 sorusu değil, bir **Kitap 2**
> sorusudur.

**Sayfa başına QR neden reddedildi.** Onlarca hedef taşıyan bir kitap,
her hedef için ayrı bir bağlantı ölümü riski taşır. Tek adres, tek
risk, tek çözüm. Kazanılan sayfa alanı "bir yayılım, bir kavram"
kuralına harcandı.

**Bağımsızlık testi: GEÇTİ — tasarım gereği.** Üç kalemin ikisinin
basılı karşılığı vardır (Ek E, Ek G); üçüncüsünün yokluğu kitabı
çalışmaz kılmaz.

**Video neden kapsam dışı.** Kanıt eksikliğinden **değil**, üretim
kapasitesi yokluğundan. İkisi karıştırılmaz. `R-01` bu yüzden
**azalmadı**.

**Açık kalan:** S3 (okur gerçekten istiyor mu) → Faz 3 pilot sorusu,
kill-gate'in **dışında**.

## K26 · `A9` — Kitap 3 başlığında `sloper`, kanonik terim `block`

**Karar.** Başlık yüzeyinde **`SLOPER`**; depo içi kanonik terim
**`block` olarak KALIR**; alt başlık her iki biçimi de taşır.

**Kanıt.** `sloper` ABD, `block` Birleşik Krallık/Avustralya
kullanımıdır `OBSERVED`. **Belirleyici bulgu:** ABD dikiş dilinde
`block` sözcüğü **kapitone bloğu** anlamını taşır ve arama sonuçları bu
anlamla doludur — keşfedilebilirlik açısından tek başına yeterli
gerekçe.

**Neden kanonik terim değişmiyor.** `A9` zaten "hangisi *başlıkta*
duracak" sorusuydu. İç dili değiştirmek 148 crosswalk kaydını ve üç
kitabın dilini gereksizce sarsardı. `terminology.json T-05` ve
`STYLE.md § 2` değişmedi.

## K27 · `A10` — Kitap 3 çizim sistemi SEÇİLEMEZ; kanıt kapısı kuruldu

**Karar.** Sistem **seçilmedi** ve kanıtsız seçilemez. Bunun yerine
seçimin **nasıl yapılacağı** kilitlendi: dört sistem ailesi (`DS-1`…`DS-4`),
yedi seçim ölçütü ve **üç maddelik kanıt kapısı**
(`BOOK-03/00_SPEC/DRAFTING_SYSTEM_RESEARCH.md`).

**Kanıt kapısı.** ① En az **iki bağımsız sistem** tam metin okunmuş
olmalı — karşılaştırma yoksa tercih yoktur. ② Ölçü tanımları
`S-0014` veya eş otoriteyle hizalanmış olmalı. ③ Seçilen sistemle
çizilmiş bir blok **fiziksel olarak sınanmış** olmalı.

**Neden kanıtsız seçilemez.** `SOURCING_STANDARD § 7`: farklı çizim
okulları aynı sonuca farklı geometrilerle ulaşır ve hiçbiri yanlış
değildir. Birini sessizce tercih etmek yasaktır.

**Görsel mimari — kavramsal karar.** Kitap 3 için **deterministik CLI
üretimi birincil yoldur**; bir blok çizimi zaten bir algoritmadır. Bu,
Kitap 1'den **daha yüksek** deterministik oran verebilir ve serinin en
büyük üretim kaldıracıdır.

**Ölçü bağımlılığı bulgusu.** Kitap 1'in doğrulanMAMIŞ yedi ölçüsü
(`M-004` `M-015` `M-017` `M-018` `M-019` `M-021` `M-022`) Kitap 3 için
**kritiktir** — bir blok tam olarak o noktalardan inşa edilir. Bu,
`A-01`'i Kitap 3'te zorunlu yapan asıl nedendir.

## K28 · `A12` — reklam: çerçeve kuruldu, bütçe verilmedi

**Karar.** Hiçbir kampanya yürütülmedi. Bunun yerine **eşiklerin
telifin üzerine kurulduğu** bir karar çerçevesi yazıldı
(`00_CONTEXT/ADS_FRAMEWORK.md`).

**Neden bu tur bir şey ekleyebildi.** Telif artık **ölçülmüş** bir
sayıdır ($11,18 — `K22`). Bu, tolere edilebilir CPC'yi bir tahmin
olmaktan çıkarıp bir **fonksiyon** hâline getirir:
`başabaş CPC = birim telif × dönüşüm oranı`. Başabaş ACoS **%41,4**.

**Bütçe tıklamayla tanımlandı, dolarla değil.** CPC bilinmiyorken dolar
bütçesi anlamsızdır: **300 tıklama**, üç kampanya, 14–30 gün.
Kampanya A **satış için değil, CPC'yi ÖLÇMEK için** vardır — CPC'yi
uydurmamanın tek dürüst yolu onu ölçmektir.

**Altı durma koşulu** önceden yazıldı. Aralarında `D6`: ürün sayfasında
hiç yorum yokken düşük dönüşüm bir **reklam** sorunu değildir; `D1`
uygulanmaz.

**Ön koşul.** Fark testi **PASS** vermeden harcama yapılmaz — hipotez
çürükse reklam metninin dayanacağı iddia yoktur.

## K29 · `A13` — asgari uygulanabilir sınama seti: iki toile, 19 kayıt

**Karar.** **2 toile + 3 yedek parça**, tek vücut (kurucu), **19 adet
`VAL-xxxx` kaydı**, ≈4 m prova kumaşı (≈$15–30), ≈20–25 saat.

**Tasarımın çekirdek fikri.** Bir sapmayı **taşıyan** vücut aramak
yerine, **bilinen** bir sapmayı tek vücutta **üret** (`Y-1`). Sınanan
şey vücut değil, **yöntemin sapmayı bulup bulmadığıdır** — ve doğru
cevap önceden bilinir.

**Maliyeti düşüren asıl teknik.** Sapmaların çoğu kalıbı değiştirmeden
ve yeni toile dikmeden, **geri dönülebilir** biçimde üretilebilir
(dikiş sökme, pili iğneleme, şerit ekleme). Yalnızca üç eleme kalemi
geri dönülemez ve ayrı parça ister. Bu, "kaç toile" sorusunun cevabını
**20'den 2'ye** indirdi.

**Kontrol toile'i (`T-1c`) setin en önemli kalemidir:** kontrol
olmadan üretilen belirti ile zaten var olan belirti ayırt edilemez.

**Yeni sınır kaydedildi.** Kasten üretilmiş bir sapma, o sapmayı doğal
olarak taşıyan bir vücudun **tam eşdeğeri değildir** → `R-06`
güncellendi.

**Eşik gevşetilmedi.** 19 kayıtlık sette tek bir FAIL, hata oranını
%5,3 yapar — üretim yöntemi reddi eşiğinin üstüne. Doğru tepki eşiği
değiştirmek değil, kök nedeni düzeltip **seti yeniden koşmaktır**.

## K30 · `A14` — protokol tamamlandı; ölçüm DIŞ BEKLEMEDE; `INCONCLUSIVE` tanımlandı

**Karar.** Fark testinin **tüm** uygulanabilir parçaları yazıldı:
eleme ölçütleri ve üç soruluk ön eleme · beş bulma kanalı · teşvik
politikası · taraf tutmayı azaltan dört kural · **oturum betiği**
(söylenecek ve söylenMEYECEK cümleler) · kayıt formu · pilot
karşılaştırma malzemesinin spesifikasyonu.

**Katılımcı bulunmadı; ölçüm yapılmadı; PASS uydurulmadı.**

**Yeni sonuç durumu: `INCONCLUSIVE`.** Kurucu, üç katılımcı hemen
bulunamadı diye projenin durmasını istemiyor. Bu, ölçütü
**değiştirmez**; üçüncü bir durum tanımlar:

| Katılımcı | Durum | `measured` | Kapı |
|---|---|---|---|
| 3, ≥2'si farkı söyledi | PASS | `true` | Açılır |
| 3, ≤1'i söyledi | FAIL | `true` | Proje durur |
| **1 veya 2** | **INCONCLUSIVE** | **`false`** | **Kapalı kalır** |

`INCONCLUSIVE` bir PASS değildir. Faz 2 üretimi, fiziksel sınama ve
pilot malzemesi **devam eder**; yalnızca kapı ilerlemez.

**`aiProxyCountsAsHuman` `false` KALDI ve açılmadı.** Çelişmeli AI
incelemesinin izinli kullanımı ayrıca listelendi (protokol eleştirisi,
yönlendirici dil taraması, başarısızlık senaryosu üretme) — ve yasak
kullanımı da (katılımcı yerine geçmek, `measured` alanına yazmak).

## K31 · Yeni kapı: `qa_crosswalk.py` — dokuz ilişki denetimi

**Karar.** Devir haritası için ayrı bir bütünlük kapısı yazıldı ve
`qa_all.sh`, CI ve `selftest.py`'ye bağlandı.

**Neden gerekti.** `build_crosswalk.py --check` yalnızca **tazeliği**
ölçer: diskteki dosya yeniden üretilenle aynı mı. **Üretici kodun
kendisi yanlışsa hiçbir şey yakalamaz** — bayat olmayan ama yanlış bir
crosswalk sessizce geçerdi. `validate_spec.check_crosswalk_integrity`
ise tek bir kaydın referanslarına bakar, kayıtlar ARASINDAKİ ilişkilere
bakmaz.

**Dokuz denetim.** Uç noktalar · devir cümlesi ↔ aday neden · istisna
mantığı (**iki yönlü**) · taksonomiyle birebirlik (kaybolmuş VE
uydurulmuş yol) · kitap sahipliği · kanonik ad · ulaşılabilirlik ·
yolu olmayan belirti.

**Sonuç.** 148 kaydın tamamı denetlendi: **0 bulgu.** 129 teşhis→düzeltme
yolu, 21 açık istisna, 19/19 aileye ulaşılıyor, 43/43 belirtinin yolu
var. `selftest.py` sekiz kusurlu kurguyla kapının gerçekten yakaladığını
kanıtlar.

**Denetim sayısı 77 → 91.**

## K32 · `A2` — GitHub: public, ama marka-nötr adla

**Karar.** Depo **public** olarak yayımlandı ve CI etkinleştirildi.
Depo adı **marka-nötrdür**: `sewing-pattern-fitting-series`.

**Neden marka-nötr ad.** `A1` henüz kapanmadı; public bir depo adı,
adın **kamuya açık kullanımıdır**. Maliyeti sıfır olan bir azaltma
(`K18` § 5).

**Public kalan.** Kod · CI · şema · doğrulayıcı · politika ve
spesifikasyon belgeleri · **taksonomi metadatası** · **kaynak
KAYITLARI (künye)** · görsel notasyon sözlüğü · faz raporları.

**Bilerek DIŞARIDA bırakılan.** Yayın-öncesi tam proza ve pilot metni ·
**fiziksel sınama fotoğrafları** (gerçek insan bedeni — gizlilik) ·
telif korumalı referans malzeme ve satın alınmış ticari kalıplar ·
üretilmiş nihai diyagram varlıkları ve yayın dosyaları · sırlar ve
yerel ortam · yerel önbellek ve indirilmiş kaynak PDF'leri.

**`.gitignore` genişletildi:** indirilmiş kaynak belgeleri
(`01_SOURCE/downloads/`), kişisel arşiv desenleri ve ek sır desenleri
eklendi. Kaynak KAYDI public kalır; kaynağın METNİ asla.

## K33 · `ROADMAP_PROGRESS.md`'nin ölçüm hatası düzeltildi

**Bulgu.** İlerleme belgesi kill-gate satırında **"✗ 4 engel"**
yazıyordu. `kill_gate.py` hem şimdi hem de o günkü commit'te
**2 engel** raporluyor.

**Karar.** Sayı düzeltildi ve bu kayıt açıldı.

**Ders — kaydedilir.** Bu proje "ölçülen / geçersiz kılınan /
ölçülmemiş" ayrımı üzerine kurulu. Bir ilerleme tablosundaki
doğrulanmamış bir sayı, tam olarak o ayrımı aşındırır.
**İlerleme belgesindeki her sayı, onu üreten komutun çıktısından
alınmalıdır** — hatırlanan bir değerden değil.

## K34 · `A8` — birim: inç birincil, figürlerde tek birim

**Karar.** **Figürlerde yalnızca inç.** Gövde metninde inç birincil.
**Karar eşiklerinde** (ör. `M-031` ≥ 2 inç → küçük beden) ve ölçü
tablolarında/boş formlarda **inç + cm**.

**Kanıt.** Hedef pazar ABD'dir. ABD ev dikişinin standart dikiş payı
**⅝ inç**tir ve büyük kalıp yayıncılarının ortak konvansiyonudur
`OBSERVED`. Doğrulanmış üç kaynağın (`S-0001` `S-0002` `S-0003`)
**tamamı** inç kullanır — ease bantları, "belin 3 inç altı", "7–9 inç
altı", "≥ 2 inç fark". İnç sistemi kesirle, metrik sistem ondalıkla
yazılır; ikisi aynı etikete karıştırılamaz.

**Neden figürlerde tek birim.** İkinci birim etiket yoğunluğunu iki
katına çıkarır ve doğrudan "bir yayılım, bir kavram" kuralıyla —
yani `Complexity(58)` şikâyetine verilen cevapla — çatışır.
`VISUAL_STANDARD § 7`'nin kuralı korunur.

**Neden karar eşiklerinde iki birim.** Bir eşik, kitabın okura verdiği
**sayısal bir karar kuralıdır**. ABD dışındaki bir okur o kuralı
uygulayamıyorsa kitabın yöntemi ona kapanır — ve maliyeti yalnızca
birkaç parantezdir.

**Alternatifler.** "Yalnızca inç" — karar eşiklerini gereksizce
kapatırdı. "Her yerde inç + cm" — figür etiketlerini iki katına
çıkarırdı.

**Sonuç.** `TYPOGRAPHY_STANDARD § 5`: inç işareti daktilo tırnağı
değildir; kesirler tek glif veya `frac` ile dizilir. ⅝ glifinin gerçek
baskıda okunması Faz 2'nin `T1` testidir.

## K35 · `A11` — fotoğraf: çizimler yeterli, fotoğraf bağımlılığı KURULMAZ

**Karar.** Kitap 1 fotoğraf kullanmaz ve fotoğraf bağımlılığı kurmaz.
Koşullu bir kapı açık bırakıldı: yalnızca **belirti tanıma** için, en
fazla **altı** figür, **beş koşulun hepsi** sağlanırsa.

**Gerekçe — figür türü bazında değerlendirme.** Yedi figür türünden
**dördünde fotoğraf çizimden KÖTÜDÜR**, birinde imkânsızdır, yalnızca
ikisinde faydalıdır:

- Ölçüm yolu: el ve şerit, işaret noktasının **kendisini örter**;
  çizim ikisini birden gösterebilir.
- Öncesi/sonrası: fotoğraf değişikliği **izole edemez** — iki kare
  arasında ışık, duruş ve kumaşın oturuşu da değişir.
- Kalıp parçası: kâğıdın fotoğrafı çiziminden kötüdür.
- Akış şeması: fotoğrafı **olamaz**.

Bu, "rakipler fotoğraf kullanıyor" gözleminin bir ürün gerekçesine
dönüşmesini engelleyen asıl argümandır.

**Beş koşul.** ① Kaynak, `A13`'ün fiziksel sınama programının kendisi
olmalıdır — `Y-1` testleri zaten *bilinen bir sapmayı taşıyan gerçek
kumaş* üretir; **ayrı çekim yapılmaz**. ② Model izni yazılı olmalı;
kurucu kendi görüntüsü için de bu kararı **açıkça** vermelidir — bu bir
mühendislik kararı değildir. ③ Fotoğraf **depoya girmez**
(`CONTENT_PROTECTION § 2` değişmedi). ④ Hiçbir fotoğraf tek başına
durmaz; yanında aynı belirtinin notasyonlu çizimi bulunur — fotoğraf
*gösterir*, çizim *adlandırır*. ⑤ İnternetten alınmış görsel, stok
fotoğraf ve marka görünen görsel **yasak**.

**Maliyet kaydedildi, yok sayılmadı.** `R-05` değişmedi: alıcı fotoğraf
bekliyorsa bu bir dezavantajdır. Karşılayan iki şey: kapak tam
renklidir; dijital tamamlayıcı görsel taşıyabilir.

**Yeniden açılma eşiği.** `photo_required` işaretli figür sayısı
**altıyı aşarsa** `A11` yeniden açılır.

---

*Vâliçe Press · TRUE FIT · Decisions · 28 Ağustos 2026*

## K36 · `A15` — seri adı: **BEFORE YOU CUT** (kurucu kararı)

**28 Ağustos 2026 · Kitap 1 Faz 2**

**Karar.** Serinin kamuya dönük adı **`BEFORE YOU CUT`**'tır.
`TRUE FIT` yayımlanan ad olarak **kullanılmaz** (`K18`).

**Kimin kararı.** **Kurucunun.** Bu bir mühendislik kararı değildir ve
ajan tarafından verilemezdi; `A15` bu yüzden `EXTERNAL PENDING`
tutuluyordu. Kurucu 28 Ağustos 2026'da adı onayladı ve serinin bu adla
ilerlemesini talimatlandırdı.

**Gerekçe — ajanın Faz 1'de kaydettiği üç bulgu.**

1. Üç eksende **sıfır çakışma bulgusu** (`08_REPORTS/PHASE_1_BRAND_SCREENING.md`).
2. Kalabalık "FIT ___" adlandırma alanının **tamamen dışında** — o alan
   `TRUE FIT`'in reddedilme nedeniydi.
3. Ad, serinin **tezini** ve **kapsam sınırını** birlikte taşıyor:
   kesmeden önce teşhis. `DIAGNOSE → ADJUST → CREATE` ilerlemesinin
   birinci adımı adın kendisindedir.

**Ne KADAR temizlendiği — abartılmaz.**

`brandClearanceStatus = "founder-approved-working-name"`.

Bu **hukuki bir temizlik DEĞİLDİR.** Bu depoda yapılan tarama bir marka
vekilinin temizlik araştırmasının yerine geçmez ve federal sicilin arama
arayüzü otomatik sorguya kapalıydı. Profesyonel temizlik **kapak ve
metadata üretiminden önce** zorunludur — `OPEN_QUESTIONS.md A16`,
`EXTERNAL_DEPENDENCIES.md D-03`.

**Mekanik dayanak.** `validate_structure.py`'ye iki denetim eklendi:

- `check_public_name_is_declared` — `brandClearanceStatus`
  `"professionally-cleared"` değerini **kanıtsız** alamaz.
- `check_retired_name_leak` — `TRUE FIT` kamuya dönük hiçbir yüzeyde
  (`metadata.json`, `TITLE.md`, `KEYWORDS.md`, `BLURB.md`,
  `DESCRIPTION.md`, `COVER_BRIEF.md`) geçemez.

**Alternatifler.** `FIT SIGNS` — ikinci sıradaydı; tezi taşıyor ama
kapsam sınırını taşımıyor. `FIT LOGIC` — **elendi** (giyim sınıfında
tescilli).

## K37 · Dizin adları DEĞİŞTİRİLMEDİ — yol dizesi kimlik beyanı değildir

**28 Ağustos 2026 · Kitap 1 Faz 2**

**Karar.** `TRUE-FIT-SEWING-PATTERN-FITTING-SERIES` ve
`BOOK-03-DRAFT-YOUR-OWN-BLOCK` dizin adları **korundu**.

**Gerekçe.** Yeniden adlandırma git geçmişini, CI yollarını,
`paths.py`'yi ve on beşten fazla belgedeki bağlantıyı **aynı anda**
kırar. Kazanç **sıfırdır**: hiçbir dizin adı okura görünmez.

Kimlik, dosya sisteminde değil `series_config.json → series.publicName`
alanında yaşar ve kamuya dönük her yüzey oradan okur.

**Tarihsel kayıt SİLİNMEDİ.** `series_config.json → series.nameHistory`
iki kaydı da taşır: `TRUE FIT` (reddedildi, gerekçesiyle) ve
`BEFORE YOU CUT` (benimsendi). Bir kararın gerekçesi, reddettiği adı
anmadan yazılamaz — bu yüzden `DECISIONS.md`, `OPEN_QUESTIONS.md`,
`RISK_REGISTER.md`, `CHANGELOG.md` ve `series_config.json`
`check_retired_name_leak`'ten **muaftır**.

## K38 · `A7` yedeği DEĞİŞTİ — Atkinson Hyperlegible ÖLÇÜLEREK elendi

**28 Ağustos 2026 · Kitap 1 Faz 2 · `G1`**

**Bulgu.** `TYPOGRAPHY_STANDARD § 3.3` figür etiketleri için yedek
yazı tipi olarak **Atkinson Hyperlegible**'ı adlandırmıştı. Faz 2'nin
glif taraması bu yedeğin ürünün **kendi gereksinimini** karşılamadığını
ölçtü:

| Yazı tipi | ⅛ ¼ ⅜ ½ ⅝ ¾ ⅞ | ″ (inç) | `Y1` |
|---|---|---|---|
| Source Serif 4 | tamamı var | var | ✓ |
| Source Sans 3 | tamamı var | var | ✓ |
| **Atkinson Hyperlegible** | **⅛ ⅜ ⅝ ⅞ YOK** | **YOK** | ✗ |
| **Atkinson Hyperlegible Next** | **⅛ ⅜ ⅝ ⅞ YOK** | **YOK** | ✗ |

`Y1` bu ürünün **birinci** tipografik gereksinimidir: ABD ev dikişinin
standart dikiş payı **⅝ inç**tir. Bir ölçü kitabının figür etiketi
`⅝` yazamıyorsa o yazı tipi yedek **olamaz**.

**Karar.** Yedek figür etiketi yazı tipi **`IBM Plex Sans`**
(SIL OFL 1.1) oldu. `Atkinson Hyperlegible` ve `Atkinson Hyperlegible
Next` **elendi**.

**Nasıl seçildi — tercihle değil, ölçümle.**
`06_BUILD/font_legibility_scan.py` beş adayı iki eksende ölçtü:
`Y1` (eleyici) ve karıştırılabilir karakter çiftlerinin 6,5 pt'de
600 dpi'deki **piksel farkı** (sıralayıcı).

| Sıra | Yazı tipi | `Y1` | En kötü çift | Ortalama |
|---:|---|---|---|---|
| 1 | **Source Sans 3** (birincil) | ✓ | `3/8` = 0,391 | 0,539 |
| 2 | **IBM Plex Sans** (yeni yedek) | ✓ | `3/8` = 0,347 | **0,608** |
| 3 | Lexend | ✓ | `1/I` = 0,333 | 0,495 |
| 4 | **Inter — ELENDİ** | ✓ | **`l/I` = 0,000** | 0,533 |
| — | Atkinson Hyperlegible | ✗ | — | — |
| — | Atkinson Hyperlegible Next | ✗ | — | — |

**`Inter` ayrıca elendi:** küçük `l` ile büyük `I` **piksel piksel
aynıdır**. Bir ölçü etiketinde bu, `Y3`'ün tam olarak tanımladığı
başarısızlıktır.

**Yan bulgu — birincil seçim de doğrulandı.** `Source Sans 3` en kötü
çift ölçütünde **birinci** çıktı. `K24` bu ölçümle **güçlendi**,
değişmedi.

**Ölçümün sınırı — açıkça yazılır.** Piksel farkı okunabilirliği
**ölçmez**. Bir okurun 6,5 pt'de basılmış bir `1` ile `l`'yi ayırt
edebildiğini **kanıtlamaz**. `T3` üç insan okuyucu gerektirir ve gerçek
kâğıtta yapılır — `EXTERNAL_DEPENDENCIES.md D-05`. Bu ölçüm yalnızca
**açıkça kötü adayları eledi** ve bir sıralama üretti.

**Kanıt.** `03_VISUAL/font_legibility_scan.json` · `S-0018`

## K39 · Sayfa geometrisi ÖLÇÜMLE değişti — asimetrik iki sütun

**28 Ağustos 2026 · Kitap 1 Faz 2 · `G2`**

**Bulgu.** İlk sayfa geometrisi profili metin bloğunu tam ölçüye
(7,0 in) yayıyordu. `06_BUILD/calibrate_tokens.py` bunun 10,5 pt'de
satır başına **107,1 karakter** ettiğini ölçtü. Rahat okuma bandı
**72–88** karakterdir; 107 karakter bir referans kitabı için satır
sonunda göz kaybı üretir.

**Karar.** Metin bloğu **bölündü**: 387,0 pt dar metin sütunu +
9,0 pt boşluk + 108,0 pt yan sütun = 504,0 pt tam ölçü.
Ölçülen yeni değer: **83,0 karakter** — hedef bandın içinde.

**Yan sütunun işlevi.** Figür başlıkları, ölçü etiketleri ve
"HENÜZ DEĞİŞTİRME" uyarıları. Bu, `Complexity(58)` şikâyetine verilen
cevabı **ucuzlatır**: bir uyarı artık gövde metninin akışını kesmez.

**Figürler değişmedi.** İki genişlik sınıfı vardır ve aradaki bir
genişlik **yoktur**: `387,0 pt` (metin sütunu) veya `504,0 pt` (tam
ölçü). `qa_visual.py § ⑤` bunu denetler.

**Neden iki eşit sütun DEĞİL.** 8,5×11 sayfada iki eşit sütun 3,3 in
verir; bu, asgari figür genişliğinin (2,6 in) hemen üstündedir ve
etiketli bir ölçüm figürü sığmaz.

**Aritmetik hatası — testin bulduğu.** Profilin ilk sürümü tam ölçüyü
**499,5 pt** yazıyordu; doğrusu `612 − 63 − 45 = 504,0` pt'dir. Hatayı
`selftest.py`'nin sayfa aritmetiği denetimi yakaladı — **bir belge
değil, bir test buldu**. Bu, `K33`'ün dersinin tekrarıdır: bir
belgedeki her sayı, onu üreten hesabın çıktısı olmalıdır.

**KDP asgarileri.** Bütün kenar boşlukları platform asgarilerinin
üstündedir ve `qa_visual.py § ⑨` her koşuda denetler (`S-0016`).
Sayfa hedefi 300'ü aşarsa cilt payı bandı değişir ve kapı **kırmızı
yanar**.

## K40 · Token sözlüğü kalibre edildi — ama `CALIBRATED_DIGITAL_RENDER`

**28 Ağustos 2026 · Kitap 1 Faz 2 · `G1`**

**Karar.** `visual_language_tokens.json` durumu
`DESIGN_TARGET_NOT_CALIBRATED` → **`CALIBRATED_DIGITAL_RENDER`**.

**Neden düz `CALIBRATED` değil.** Ölçüm bir **dijital rasterdır**
(300 ve 600 dpi, 1-bit). Talep-üzerine baskının **mürekkep yayılması**
ölçüme **girmez**: 0,4 pt bir çizgi gerçek baskıda kalınlaşır, 6 pt bir
tırnak dolar. Düz `CALIBRATED` yazmak, yapılmamış bir baskı testini
yapılmış göstermek olurdu. Durum adının kendisi sınırı taşır.

`selftest.py § test_calibration_is_not_claimed_without_evidence` bu
ayrımı her koşuda denetler.

**Ölçülenler.**

| Ne | Sonuç |
|---|---|
| Dokuz çizgi kalınlığı, 300 dpi 1-bit | **hepsi hayatta**; en ince (0,4 pt) **2 piksel** |
| Beş kesik deseni | hepsi düzden ayrık |
| Üç gri tonu | hedeften sapma ≤ 1 luma |
| **`TK-05` ↔ `TK-06`** | **AYRIK — eğrilik oranı 3,49** (eşik 2,0) |
| `T1` kesir glifleri | Source Serif 4 ve Source Sans 3'te **tam** |
| `G2` satır ölçüsü | 83,0 karakter (hedef 72–88) |

**`TK-06` yay yüksekliği ÖLÇÜMLE değişti.** İlk değer 3,2 pt idi ve
eğrilik oranını **2,4**'te bırakıyordu — eşiğin (2,0) hemen üstünde,
dar bir marj. **4,6 pt**'de oran **3,49** oldu. Değer bir tercihle
değil, bir ölçümle değişti.

**Metrik de düzeltildi — `K20`'nin tekrarı.** Ayırt edicilik ölçümünün
ilk sürümü mürekkep oranı ve bileşen sayısına bakıyordu ve `RİSKLİ`
veriyordu. Ama iki işaret de üç parçadan oluşur ve neredeyse aynı
mürekkebi kullanır: metrik, **ayırt eden şeyi ölçmüyordu**. Eğrilik
ekseni eklendi ve ölçüm parça bazına indirildi. **Bir testin ADI ile
ÖLÇTÜĞÜ ŞEY aynı olmalıdır.**

`TK-05` ↔ `TK-06` ayrımı bir stil tercihi değil bir **teknik
gerekliliktir** (`S-0004`, WSU EM4582: kumaşı *çeken* kırışıklık az
ease, *kıvrım hâlinde duran* kırışıklık çok ease gösterir). İki token
karışırsa kitabın en çok kullanılan kuralı çöker.

**Kanıt.** `03_VISUAL/calibration_report.json`

## K41 · Akış şeması mimarisi ÖLÇÜMLE değişti — 9 değil 46

**28 Ağustos 2026 · Kitap 1 Faz 2 · `G3`/`G6`**

**Bulgu.** `VISUAL_SPEC § 1` dokuz akış şeması öngörüyordu:
"7 bölge + 1 ana şema + 1 eleme". Motor **bölge düzeyinde** şemaları
kurup ölçtü:

| Bölge | Belirti | Gereken genişlik | Sayfaya sığar mı |
|---|---:|---:|---|
| bust_chest | 6 | 1956 pt | **hayır** |
| shoulder · waist_torso · crotch_leg | 5 | 1630 pt | **hayır** |
| upper_back · hip_seat · sleeve_arm · whole_garment | 4 | 1304 pt | **hayır** |
| neck · armhole | 3 | 978 pt | **hayır** |

Sayfanın figür alanı **504 × 612 pt**'dir. **On bölgenin onu da
sığmıyor** — en küçüğü bile iki katından fazla yer istiyor.

**Karar.** Akış şemasının birimi **bölge değil, BELİRTİDİR.**
43 belirti şeması + 1 bölge yönlendirici + 2 eleme şeması = **46**.

**Kural ihlal edilmedi, UYGULANDI.** `VISUAL_SPEC § 2` kural 4:
*"Bir şema tek yayılıma sığmalıdır. Sığmıyorsa **konu bölünür**, şema
küçültülmez."* Ölçüm konunun bölünmesi gerektiğini gösterdi. Kural 1
(*"her şema tek bir bölgeye aittir"*) de korunur: bir belirti tam olarak
bir bölgeye aittir.

**Eleme şeması da bölündü.** 11 karıştırıcı sınıfı 693 pt istiyordu
(azami 612). Sayfa başına 9 satır sığıyor → **2 şema**. Bölme sayısı
elle yazılmadı, **sayfa yüksekliğinden hesaplandı**.

**Sonucu — `R-05` için gerçek sayı.** Faz 1 tahmini ~123 figürdü.
**Ölçülen: 154.** Fark neredeyse tamamen akış şemalarından geliyor
(9 → 46). Bu, görsel üretim hacmi riskinin ilk **ölçülmüş** değeridir.

**Bunun maliyeti sayfa sayısıdır.** 46 şema, "bir yayılım bir kavram"
kuralıyla birlikte, Kitap 1'in sayfa hedefini (220–260) zorlayabilir.
`qa_visual.py § ⑨` sayfa sayısı 300'ü aşarsa cilt payı bandının
değiştiğini ve geometrinin yeniden hesaplanması gerektiğini **kırmızı
yakarak** söyler. Bu, Faz 3 sonrası kapsam kararının girdisidir.

## K42 · Figür token'ları BEYAN değil ÖLÇÜM — ve yasaklar çalıştırılabilir

**28 Ağustos 2026 · Kitap 1 Faz 2 · `G4`/`G5`**

**Karar.** `figures.json`'daki `notation_tokens` listesi elle
yazılmaz; figür çizilirken **gerçekten çağrılan** token'lardan
türetilir (`figure_tokens.FigureCanvas.use`).

**Gerekçe.** Bir kaydın alanı ile o alanın anlattığı gerçeklik arasında
sessiz bir kayma olabilir — `K20`'nin ve `K33`'ün dersi. Ölçülen bir
alan kayamaz.

**İkinci karar — `VISUAL_STANDARD § 5`'in yasakları KODA döndü.**
Bir yasak artık bir belge cümlesi değil, çizimi **durduran** bir
istisnadır (`ForbiddenDrawing`):

| Yasak | Tetikleyen |
|---|---|
| Sayısal etiketsiz spread/overlap oku | `tk02`/`tk03` boş etiketle çağrılırsa |
| Vücut figüründe slash line | `surface="body"` + `TK-01` |
| Ölçek beyanı olmayan kalıp parçası | `surface="pattern"` + `declare_scale` yok |
| Anlam taşımayan gri | izin listesi dışı ton |
| Baskı asgarisi altında çizgi | < 0,4 pt |
| Asgari punto altında etiket | < 6,0 pt |
| Figür kutusundan taşma | her çizim çağrısı |
| Tanımsız token | `use()` |

`selftest.py`'ye **14 regresyon** eklendi ve her biri yasağın
**gerçekten kırmızı yaktığını** kanıtlar — yanlış pozitif testleriyle
birlikte. Toplam selftest: **91 → 125 denetim** (sonra render katmanı ayrıldı — `K48`).

## K43 · Kroki bir çizim konvansiyonudur, antropometrik bir iddia DEĞİLDİR

**28 Ağustos 2026 · Kitap 1 Faz 2**

**Karar.** `06_BUILD/croquis.py`'deki oranlar hiçbir kaynağa
dayandırılmaz ve hiçbir kaynak olarak **gösterilmez**.

**Gerekçe.** Kroki, "şerit metre nereden nereye gider" sorusunu
yanıtlamak için vardır. Hiçbir okur bu figürden **kendi ölçüsünü
okumaz**; kendi ölçüsünü kendi vücudundan alır. Ölçünün tanımı
`measurements.json → path_rule` alanındadır; kroki yalnızca o kuralın
resmidir.

Krokiyi bir antropometrik kaynağa (`S-0006` ANSUR II, `S-0007` NHANES)
dayandırmak, **taşımadığı bir kesinliği** ima ederdi: bir çizim
figürünün omuz genişliği bir popülasyon istatistiği değildir.

**Mekanik dayanak.** `selftest.py § test_croquis_is_declared_non_
anthropometric` iki şeyi denetler: dosya sınırı **açıkça** yazıyor mu,
ve dosya hiçbir `S-xxxx` kaydına atıf yapıyor mu.

## K44 · Faz 2 kapandı, Faz 3'ün kill-gate'i AÇILMADI

**28 Ağustos 2026 · Kitap 1 Faz 2 → Faz 3**

**Karar.** `BOOK-01/.gate` → `phase2-visual`. Seri kapısı `.gate` →
`series-architecture`.

**Karar — ikinci yarısı, daha önemlisi.** `phase3-pilot` kapısı
**AÇILMADI** ve bu turda açılamaz.

Faz 3'ün iki kill-gate'i de dış dünyada ölçülür ve ikisi de
**ölçülmemiştir**:

| Kill-gate | Durum | `measured` |
|---|---|---|
| Fark testi (üç ev dikişçisi) | `EXTERNAL VALIDATION REQUIRED` | `false` |
| Fiziksel doğrulama (19 `VAL` kaydı) | `EXTERNAL VALIDATION REQUIRED` | `false` |

`06_BUILD/kill_gate.py --book book-01` **2 engel** raporluyor ve
raporlamaya devam edecek. Bu **beklenen** ve **doğru** davranıştır.

**Faz 3'ün içeriden yapılabilen kısmı YAPILDI:** pilot kesit üretildi,
fark testi karşılaştırma paketi hazırlandı, fiziksel sınama kiti
(19 `VAL` kayıt formu) üretildi, çelişmeli inceleme koşturuldu.
**Ölçümlerin kendisi yapılmadı ve yapılmış gibi kaydedilmedi.**

> Bir kapıyı ilerleten şey ölçümdür. Hazırlık, ölçümün yerine geçmez.

## K45 · Figürler OKURUN dilinde çizilir — belge dilinde değil

**28 Ağustos 2026 · Kitap 1 Faz 3 hazırlığı**

**Bulgu.** Faz 2'nin figür motoru düğüm metinlerini doğrudan
`fit_signs.json`'dan okuyordu. O dosya **proje belge dilindedir**
(`series_config → documentLanguage = "tr"`). Kitabın kendisi
**İngilizcedir** (`series.language = "en"`, hedef pazar ABD).

Sonuç: 46 akış şeması, 43 belirti figürü ve bütün karşılaştırma
figürleri **Türkçe** üretiliyordu. Faz 2'nin kapıları bunu yakalamadı —
çünkü hiçbiri **dil** sormuyordu.

**Bulgunun ortaya çıktığı yer.** Faz 3'ün fark testi malzemesi
hazırlanırken. `DIFFERENTIATION_TEST § 6.1` malzeme A için
*"Faz 2'nin gerçek figürleri — taslak/eskiz kullanılmaz"* diyor. Üç
ABD ev dikişçisine Türkçe akış şeması gösterilemez: **fark testi bu
hâliyle YAPILAMAZDI** ve testin sonucu ölçtüğü şeyle ilgisiz olurdu.

**Karar.** Okura dönük bir **etiket katmanı** eklendi:
`02_TAXONOMY/public/labels_en.json` — 43 belirti gözlemi, 129 aday
nedenin ayırt edici kanıtı ve neden adı, 10 bölge adı, 11 karıştırıcı
sınıfı ve figür arayüz dizeleri.

Motor artık `series.language`'ı okur ve etiket katmanı yoksa
**çalışmayı reddeder** — sessizce belge dilinde üretmez.

**Neden ayrı bir dosya, taksonominin içine gömülü alanlar değil.**
Taksonomi bir **kanıt kaydıdır**; `verification_status` alanları
oradaki iddialara bağlıdır. Okura dönük ifade bir **sunum
katmanıdır**. İkisini aynı kayda koymak, bir ifade değişikliğinin
doğrulama durumunu gölgede etkilemesine kapı açardı.

**Sınır — açıkça yazılır.** Bu katman bir **doğrulama değildir**.
43 belirti hâlâ `agent_drafted_unverified`'dır ve birincil doğrulaması
**fizikseldir** (Faz 3). Dosya bunu `does_not_change_verification_status:
true` alanıyla beyan eder ve `selftest.py` beyanın varlığını denetler.

**Mekanik dayanak.** `qa_visual.py § ⑩`: kitap dili ile belge dili
farklıysa her belirti ve her aday neden için okura dönük karşılık
aranır; eksik bir etiket kapıyı **kırmızı yakar**. `selftest.py` kusurlu
bir fixture'la kapının gerçekten yakaladığını kanıtlar.

**Ders — `K20`'nin üçüncü tekrarı.** Faz 2'nin bütün kapıları yeşildi
ve üretilen figürlerin **hiçbiri kullanılamazdı**. Bir kapı kümesi,
**sormadığı soruyu** yakalayamaz. Bu yüzden kapı eklendi, figürler
düzeltilmekle yetinilmedi.

## K46 · Okura dönük figür iki yeni kapı kazandı — iç kimlik ve etiket çakışması

**28 Ağustos 2026 · Kitap 1 Faz 3 hazırlığı**

**Bulgu 1 — iç kayıt kimlikleri okura basılıyordu.**
`TYPOGRAPHY_STANDARD § 3.4`: *"Kayıt kimlikleri (`SYM-016`, `AF-01`,
`M-031`) iç veri kimlikleridir ve okura gösterilmez."*

Ama üretilen figürler tam olarak bunu yapıyordu:

| Nerede | Ne basılıyordu |
|---|---|
| Belirti figürü alt yazısı | `SYM-016 · diagonal_drag_line` |
| Devir düğümü (`TK-18`) | `AF-01` |
| Türetilmiş ölçü figürü | `M-002 − M-001` |
| Düzeltme ailesi dizini tablosu | `AF-01` … `AF-19` |

**İkinci çelişki — iki Faz 1 belgesi birbiriyle uyuşmuyordu.**
`visual_language_tokens.json`'daki `TK-18` spec'i *"kalın kenarlı
dikdörtgen + **AF-xx etiketi**"* diyordu. Bu, tipografi standardının
§ 3.4'ünün doğrudan ihlalidir. İki belge Faz 1'de birbirinden habersiz
yazılmış ve çelişki **hiçbir kapı tarafından görülmemişti**.

**Karar.**

1. `TK-18` düğümü ailenin **ADINI** taşır. `AF-xx` veri bağı olarak
   figürün **kaydında** durur; okura basılmaz. Okura dönük çapraz
   gönderme (`reader_ref`) Kitap 2'nin bölüm numaraları var olduğunda
   eklenir — bugün `null`'dur ve **uydurulmaz**.
2. Tablolar **ikiye ayrıldı**: okura dönük (3) ve iç araç (3). İç
   araçlar `internal: true` taşır, kimlik basabilir ve **kitap figürü
   sayılmaz**.
3. Yeni kapı: `figure_tokens.check_internal_id_leak` — okura dönük bir
   figürde `SYM-`/`AF-`/`M-`/`BLK-`/`TOP-`/`XW-`/`VAL-`/`FIG-`/`TK-`
   deseni geçerse çizim **durur**.

**Bulgu 2 — işaret noktası etiketleri üst üste biniyordu.**
`lmk_*` figürlerinde etiketler çapa noktasının yanına konuyordu ve
yakın noktalarda (boyun tabanı / omuz ucu / boğaz çukuru) **okunamaz
biçimde çakışıyordu**.

**Neden bu bir hata, bir estetik kusur değil.** Bu bir **ölçü
kitabıdır**. Yanlış okunan bir ölçü etiketi okurun kumaşını götürür
(`RISK_REGISTER R-06`). `VISUAL_SPEC § 3` zaten *"'nereden nereye'
sorusu figürden cevaplanabilir olmalıdır"* diyor.

**Karar.** Yeni kapı: `figure_tokens.check_label_collisions` — iki
etiket kutusu kesişirse çizim **durur**. Yerleşim algoritması yeniden
yazıldı: etiketler kendi sütununda, çakışmayan yüksekliklere konur ve
oraya bir bağlayıcı çizilir.

**Her iki kapı için selftest regresyonu eklendi** — yanlış pozitif
testleriyle birlikte (`internal_marks=True` muafiyeti ve ayrık
etiketler serbest kalmalıdır). Toplam selftest: **125 → 143 denetim** (116 veri + 27 render).

**Ders — `K45`'in tekrarı.** Üç bulgunun üçü de "kapı yeşil, ürün
bozuk" sınıfındandır ve üçü de **üretilen sayfaya gözle bakılarak**
bulundu. Faz 4'ün her turunda üretilen sayfalardan bir örneklem gözle
incelenecektir; otomatik kapılar bunun yerine **geçmez**.
`08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md § 6`.

## K47 · `.gitignore` sır deseni iki kaynak dosyayı YUTUYORDU

**28 Ağustos 2026 · Kitap 1 Faz 3 · commit öncesi**

**Bulgu.** `.gitignore § ⑦` (sırlar) çıplak `*_token*` ve `*_secret*`
arıyordu. Bu desen iki **kaynak dosyayı** yakalıyordu:

- `06_BUILD/figure_tokens.py` — on sekiz token'ın çalışan karşılığı
- `06_BUILD/calibrate_tokens.py` — kalibrasyon ölçüm scripti

**Sonucu.** Depo yerelde tamamen yeşildi (`qa_all.sh` sıfır hata,
selftest **o anda** 137/137) ama **temiz bir klonda görsel sistem hiç
çalışmayacaktı**: `figure_engine.py` `figure_tokens`'ı import ediyor ve
o dosya depoda **yoktu**. CI de bunu görmezdi — CI görsel motoru
çalıştırmıyordu, yalnızca kapıları çalıştırıyordu.

**Karar.** Desen daraltıldı: `*.token`, `access_token*`, `api_token*`,
`auth_token*`, `*.secret`, `client_secret*`. Gerçek sır dosyalarını
hedefler, kaynak kodunu değil.

**Regresyon eklendi** — `selftest.py § test_build_scripts_are_tracked`:
`06_BUILD/` ve `07_TESTS/` altındaki her `.py`/`.sh` dosyası için
`git check-ignore` çalıştırır ve yoksayılan bir script bulursa
**kırmızı yakar**.

**Ders — `R-19`'un dördüncü örneği.** Bir kapı kümesi, sormadığı soruyu
yakalayamaz. Bu turda dört kez oldu: figür dili (`K45`), iç kayıt
kimliği ve etiket çakışması (`K46`), ve şimdi izlenmeyen kaynak dosya.
Dördü de "kapılar yeşil, ürün bozuk" sınıfındandır.

**Bu kusurun özel yanı:** öbür üçü **ürüne bakılarak** bulundu, bu
**commit'e bakılarak** bulundu. Faz 4'ün yazılı kuralına bir madde
daha eklenir: *her commit'ten önce `git status --untracked-files=all`
çıktısı gözle okunur.*

## K48 · KA hattı ikiye ayrıldı — veri kapıları bağımlılıksız kalır

**28 Ağustos 2026 · Kitap 1 Faz 3 · CI kırmızı yandıktan sonra**

**Bulgu.** İlk commit'ten sonra **CI kırmızı yandı**:

```
ModuleNotFoundError: No module named 'reportlab'
  07_TESTS/selftest.py:35  →  import figure_tokens
```

`selftest.py`'ye eklenen çizim yasağı testleri `figure_tokens.py`'yi
import ediyordu, o da reportlab'ı. Ama CI iş akışının kendi tasarım
kuralı şudur (`validate.yml` başlığı): *"bu iş akışı ÜÇÜNCÜ TARAF PAKET
KURMAZ. Bütün kalite kapıları Python standart kütüphanesiyle yazıldı."*

**Yerelde görülmedi** çünkü reportlab yerelde kuruluydu.

**Karar — bağımlılığı GİZLEME, AYIR.**

| Katman | Dosya | Bağımlılık | CI işi |
|---|---|---|---|
| **Veri kapıları** | `selftest.py` + sekiz kapı | **YOK — stdlib** | `gates` `spec` `structure` `crosswalk` `boundary` `claims` `visual` `selftest` |
| **Render katmanı** | `selftest_visual.py` · `figure_tokens.py` · `figure_engine.py` · `calibrate_tokens.py` | reportlab · Pillow · `pdftoppm` | **`render`** *(yeni)* |

`qa_visual.py` **veri katmanında kaldı** — yalnızca JSON okur, hiçbir
şey çizmez. Bu doğrudur: bir figür **kaydını** denetlemek için figürü
**çizmek** gerekmez.

**Bağımlılık açıkça beyan edildi:** `07_TESTS/requirements-render.txt`.

**Yerel `qa_all.sh` ikisini de çalıştırır** ama render katmanının
bağımlılığı yoksa **uyarı** verir, başarısızlık değil (çıkış kodu 2).
Veri kapıları temiz bir Python kurulumunda çalışmaya devam eder —
`selftest.py` reportlab ve Pillow **gizlenerek** de sınandı ve 116/116
geçti.

**`render` işi iki şeyi ayrıca denetliyor:**

1. **`figures.json` bayat mı** — motor çalıştırılır ve `git diff
   --exit-code` ile karşılaştırılır. Taksonomi değişip figür sicili
   güncellenmezse CI **kırmızı yanar**.
2. **Yazı tipleri gerçekten edinilebiliyor mu** — `fetch_fonts.py`
   arşivden indirir ve SHA-256 doğrular. Manifest bozulursa CI yakalar.

**Ders — `R-19`'un beşinci örneği.** Bu kez kusuru **CI buldu** ve bu
CI'nin ne için var olduğudur. Ama bulmasının nedeni şanstır: eğer CI de
reportlab kurmuş olsaydı, "veri kapıları bağımlılıksızdır" iddiası
sessizce **yalan** hâline gelirdi ve kimse fark etmezdi. Bir mimari
ilke, onu **sınayan bir mekanizma** olmadan bir dilektir.

---

## K49 — Faz 4 kurucu geçersiz kılması: koşullu üretim kapısı

**Tarih:** 29 Ağustos 2026 · **Faz:** 4 · **Durum:** UYGULANDI

Yol haritası P4'ü P3'ün **PASS**'ine bağlar. Kurucu, P3'ün iki dış
ölçümünü (`D-01` fark testi, `D-02` fiziksel doğrulama) beklemeden tam
içerik üretiminin sürmesine izin verdi ve aynı talimatta **ölçümlerin
PASS yazılmasını AÇIKÇA yasakladı**: *"DO NOT FAKE THE MISSING P3
RESULTS."*

Bu iki şey aynı anda kaydedilmek zorundaydı. Seçenekler:

| Seçenek | Neden reddedildi |
|---|---|
| `.gate` → `phase4-production` | Kümülatif sırada `phase3-pilot`'ı da geçilmiş gösterirdi. **Tarih yeniden yazılırdı.** |
| `.gate` = `phase2-visual` bırakılsın | Yapılan iş kaydedilmezdi; bir sonraki tur nereden devam edeceğini bilemezdi. |
| `book_config.json`'a serbest bir alan | Kapı mekanizmasının dışında kalırdı — hiçbir kapı onu denetlemezdi. |

**Karar: `BOOK_GATE_ORDER`'a `phase4-production-conditional` eklendi ve
kümülatif sırada `phase3-pilot`'tan ÖNCEYE konuldu.**

Sonuç, mekanik olarak doğru olan tam da şudur:

- `gate_at_least(g, "phase2-visual")` → **doğru** (Faz 2 bitti)
- `gate_at_least(g, "phase3-pilot")` → **YANLIŞ** (kill-gate ölçülmedi)
- `gate_at_least(g, "phase5-qa")` → **YANLIŞ** (P5 bu yoldan açılamaz)

`kill_gate.py` hâlâ **iki engel** raporluyor ve "Faz 4 AÇILAMAZ" diyor.
Bu **çelişki değil, tam olarak istenen durumdur**: üretim ilerledi,
doğrulama kapısı ilerlemedi. İkisi ayrı eksenlerdir ve ayrı kalmalıdır.

İki yeni denetim bunu korur: `check_book_phase4_requirements` (Faz 4
çıktıları BEYAN değil DOSYA olarak aranır) ve `check_kill_gate_not_claimed`
(kapı sırası bozulursa ya da bir kill-gate bayrağı açılırsa hata).
Regresyon: `selftest.py § test_conditional_phase4_does_not_claim_kill_gate`.

---

## K50 — Manüskript üretilir, prozа yazılır

**Tarih:** 29 Ağustos 2026 · **Faz:** 4 · **Durum:** UYGULANDI

Bölüm 2 (32 ölçü) ve bölge atlası (43 belirti girişi) **üretilir**;
Bölüm 1, 3–8 ve 16–18 **yazılır**.

**Gerekçe:** o iki bölümün iç yapısı bir spesifikasyondur, bir yazarlık
tercihi değil. 43 giriş elle yazılsaydı, er geç biri "henüz değiştirme"
uyarısını ya da yeniden gözlem adımını taşımazdı ve **hiçbir kapı bunu
göremezdi** — çünkü kapı, metinde olmayan bir bölümü arayamaz. Üretilen
bir yapıda eksik alan **derlenmez**.

Yazılan proza `sign_content_en.json`, `zones_en.json`,
`measurements_en.json` dosyalarında durur; `06_BUILD/atlas.py` sırayı,
başlık hiyerarşisini, figür yerleşimini ve **üç yapısal zorunluluğu**
(`B-01` yeniden gözlem · `B-02` beden kapısı · `B-03` belirtiye özgü
eleme) üretir.

---

## K51 — İki dizgi yolu YOK: `typeset.py`

**Tarih:** 29 Ağustos 2026 · **Faz:** 4 · **Durum:** UYGULANDI

Faz 3'te dizgi kodu `build_pilot.py`'nin içindeydi. Faz 4 tam kitabı
dizmek zorundaydı ve o kodu **kopyalamak** iki dizgi yolu yaratırdı.

Figür sisteminde bu hatadan bilinçle kaçınılmıştı (`figure_engine.render()`
tek yoldur). Aynı disiplin dizgiye uygulandı: `06_BUILD/typeset.py`
çıkarıldı, `build_pilot.py` ondan okuyor. **Pilot çıktısı değişmedi:
8 sayfa, 7 figür** — refactor'ın doğruluk kanıtı budur.

Neden önemli: iki yol olsaydı pilotun 8 sayfası ile kitabın aynı bölümü
**farklı** dizilebilirdi ve fark testi (`D-01`) karşılaştırılamaz hâle
gelirdi.

---

## K52 — Ayırt edici kanıt çakışmaları UYDURMA bir ayrımla kapatılmadı

**Tarih:** 29 Ağustos 2026 · **Faz:** 4 · **Durum:** UYGULANDI

Bağımsız inceleme, 43 belirtinin **28'inde** iki aday nedenin aynı
gözlemi ürettiğini ve `distinguishing_evidence` alanlarının onları
**gerçekten ayırmadığını** ölçtü. Şema alanın DOLU olmasını dayatıyordu;
alanın **işini yapmasını** hiçbir şey dayatmıyordu.

İki yol vardı:

1. Her çakışma için yeni bir ayırt edici kanıt **yazmak.** Kolaydı ve
   **uydurma** olurdu: elde o ayrımı destekleyen kanıt yok.
2. Çakışmayı **kaydetmek ve okura söylemek.**

**İkincisi seçildi.** `02_TAXONOMY/public/evidence_collisions.json`
28 çakışmayı taşır; `atlas.py` ilgili girişe şu kutuyu basar:
*"bu iki neden aynı görünebilir, ikisini de en ucuz testten başlayarak
sına — bu senin kaçırdığın bir şey değil, yayımlanmış kanıtın bilinen
sınırı."*

**Bir teşhis kitabının en az yapabileceği şey, nerede teşhis
koyamadığını bilmektir.** Ayrımların kendisi `D-02`'ye bağlıdır.

---

## K53 — Kalıp-dışı nedenler ÖNCE sunulur

**Tarih:** 29 Ağustos 2026 · **Faz:** 4 · **Durum:** UYGULANDI

Taksonomi aday nedenleri **olasılık** sırasına diziyordu. Adım 6 ise
"en ucuz testi önce uygula" diyor ve en ucuz nedenler kalıba
dokunmayanlardır (yapım, kesim, prova koşulu, tasarım).

Bağımsız inceleme ölçtü: **20 kalıp-dışı nedenin hiçbiri ilk sırada
değildi; 13'ü sonuncuydu.** Kitap kendi kuralının tersini yaptırıyordu.

`atlas.py` sunum sırasını **kapı-önce** yaptı. Taksonominin olasılık
sırası korunur; değişen yalnızca okura gösterilme sırasıdır ve gerekçe
`h3` başlığında yazılıdır: *"Check these before the pattern."*

---

## K54 — Kapı, kapsamını SESSİZCE küçültemez

**Tarih:** 29 Ağustos 2026 · **Faz:** 5 · **Durum:** UYGULANDI

Faz 5 temiz klon denetiminde ölçüldü: `selftest.py` yerel ağaçta 152,
temiz klonda **146** denetim koşuyordu. Fark, prozanın bilerek
izlenmemesinden (`K9`) doğuyor ve bu **meşru**. Meşru olmayan, kapının
bunu nasıl raporladığıydı:

* atlanan denetimler `check(..., True)` ile **GEÇMİŞ** sayılıyordu;
* kapanış satırı yine de *"✓ Bütün kapılar kusurlu fixture'ları doğru
  yakaladı"* diyordu.

Atlananlar arasında **Faz 4'ün en pahalı düzeltmelerini koruyanlar**
vardı: `B-01` yeniden gözlem, `B-03` belirtiye özgü eleme, ölçüm figürü
kapsaması. CI yeşildi ve o denetimler **hiç koşmamıştı.**

**Karar:** atlanan bir denetim GEÇEN bir denetim DEĞİLDİR. `skip()`
ayrı sayar, adıyla listeler, kapanış satırı *"Koşan N denetimin hepsi
geçti — ama M denetim HİÇ KOŞMADI"* der.

Aynı ilke iki yerde daha uygulandı: `qa_manuscript.py` artık atlama
gerekçesini DOĞRU yazıyor (eskiden *"Faz 4 öncesi kitaplar için"*
diyordu; Kitap 1 Faz 4 öncesi değildir), ve `selftest_visual.py` eksik
YAZI TİPİNİ de kayıp bağımlılık sayıyor (eskiden 11 çizim yasağını
yanlışlıkla `✗` basıyordu).

**Bir kapının en tehlikeli hâli, sormadığı soruyu sormuş gibi
görünmesidir.**

---

## K55 — Dizgi çıktısı ÖLÇÜLÜR, varsayılmaz

**Tarih:** 29 Ağustos 2026 · **Faz:** 5 · **Durum:** UYGULANDI

Faz 4 sonunda sekiz veri kapısı yeşildi ve **ürün bozuktu.** Faz 5'te
bulunan kusurların hiçbiri veri katmanında değildi:

* yan not başlığı metin bloğunun ÜSTÜNE basıyordu (s. 72'de 33,2 pt);
* akışta açılan sayfa folyo ALMIYORDU (s. 46, s. 236);
* boş form satırları **1,84 mm** idi — `_wrap("") == []` yüzünden satır
  yüksekliği formülü NEGATİF düzeltme uyguluyordu;
* Ek C — kitabın ilan ettiği tek giriş yolu — 43 belirtinin 18'inde
  okuru bir sayfa erkene, çoğu kez BAŞKA bir belirtinin karar tablosuna
  gönderiyordu (kapalı döngü);
* ölçü figürü 32/32 kendi metninden bir sayfa sonra basılıyordu.

**Karar:** dizgi katmanı da ölçülür. Yöntem: `pdftotext -bbox-layout`
ile her kelimenin kutusu çıkarılır; dikdörtgen kesişimi (harf çakışması),
kenar boşluğu ihlali ve folyo bütünlüğü **255 sayfanın tamamında**
taranır. 300 dpi 1-bit rasterleştirme baskı hayatta kalmasını ölçer.

Bu ölçümlerin **on üçü kalıcı kapıya** dönüştürüldü (152 → 187 denetim).
Dördü **mutasyonla** sınandı: düzeltme geri alındığında kapının gerçekten
düştüğü gösterildi. Biri ilk yazılışında mutasyonu YAKALAYAMADI (gerçek
çizim yolunu değil yardımcı işlevi sınıyordu) ve yeniden yazıldı —
**kapının kendisi de bir kapıdan geçti.**

---

## K56 — Sunum sırası TEK yerden gelir

**Tarih:** 29 Ağustos 2026 · **Faz:** 5 · **Durum:** UYGULANDI

`K53` aday nedenleri kapı-önce sıraya dizdi — ama yalnızca `atlas.py`
içinde. `figure_engine.py` akış şemasını **ham taksonomi sırasından**
çiziyordu.

İki sonuç ölçüldü: *"cheapest test first"* diyen **17 girişin 17'sinde**
bedava dal şemada ikinci ya da üçüncü sıradaydı; ve metindeki **"1.
neden"** ile şemanın **ilk dalı FARKLI nedenlerdi** — aynı yayılımda
"birinci neden" iki ayrı şeye işaret ediyordu.

**Karar:** sıralama tek bir kuraldan gelir ve iki sunum da onu kullanır.
Kapı: `test_flowchart_and_entry_agree_on_cause_order` 43/43 denetler.

Desen `K16` (`trfold.py`) ile aynıdır: **bir davranış, bir kopya.**

---

## K57 — Kapsam okura BEYAN EDİLİR

**Tarih:** 29 Ağustos 2026 · **Faz:** 5 · **Durum:** UYGULANDI

`SCOPE.md` örme/esnek kumaş dikişçisini *"farklı fizik — seri dışı"*
diye kapsam DIŞINDA tutuyor. Fark testi katılımcıları *"dokuma kumaşla"*
dikenlerden seçiliyor. Doğrulama protokolü dokuma prova kumaşı istiyor.

**Kitapta "woven" kelimesi 252 sayfada SIFIR kez geçiyordu.**

*"Who this is not for"* listesi üç okuru dışlıyordu ve hiçbiri bu
değildi. Üstelik Bölüm 1 *"The third is **always** larger than the
first"* diyordu — negatif payda YANLIŞ olan koşulsuz bir genelleme.

**Karar:** bir kitabın dışladığı okur, o kitabı satın almadan ÖNCE
bunu bilmelidir. Dışlama listeye eklendi, prova kumaşı satırı "woven"
dedi, ve mutlak cümle kapsamla sınırlandırıldı.

**Beyan edilmemiş bir kapsam, kapsam değildir.**

---

## K59 — İÇERİK TURU TAMAMLANMADI; FAZ 6 AÇILMADI

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu · **Durum:** UYGULANDI

L-2 ve L-3 kapatıldı. Bütün kapılar yeşil, kitap 273 sayfada kuruluyor,
309 iddianın hepsi izlenebilir.

**Ve içerik turu TAMAMLANMADI.**

Görev talimatı § 23'ün zorunlu kıldığı bağımsız inceleme — üç ayrı geçiş,
hiçbiri birincil üretimin sonuçlarını görmedi — L-2/L-3'ün **altında
ikinci bir kusur katmanı** buldu. En ağırı:

> 43 belirti girişinin doğrulama ölçütü **YANLIŞLANAMAZDI.** "Read it"
> satırı nedenin değil BELİRTİNİN azalmasını istiyordu. Bir girişin üç
> nedeni aynı koridora yer açar; üçünün de testi belirtiyi azaltır.
> Ölçüt, okurun **hangi nedeni önce denediyse onu** onaylıyordu.

Bu kusur Faz 5'in bir DÜZELTMESİNDEN doğmuştu ve beş kapıdan, iki
çelişmeli incelemeden ve bir sentetik koşumdan geçmişti.

**Karar:** çıkış ölçütlerinin 6., 11. ve 12. maddesi karşılanmadığı için
içerik turu COMPLETE işaretlenmez ve Faz 6 açılmaz. 24 kusur açık
kaydedildi ve hiçbiri gizlenmedi.

**Gerekçe:** görev talimatı § 26 bunu açıkça yasaklıyor — *"Do not use
successful build, zero automated errors, visual completeness, page count
as a substitute for content completeness."* Yeşil kapı bir ürün iddiası
değildir; kapının sorduğu soruların cevabıdır.

---

## K60 — SAYFA BÜTÇESİNİN ÜST SINIRI 260'TAN 275'E ÇIKARILDI

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu · **Durum:** UYGULANDI

İçerik turu L-2'yi kapatmak için Bölüm 3'e kalıp okuma kesitlerini,
Bölüm 5'e dört prova okumasını ve Ek J'yi ekledi; F-01'in düzeltmesi
doğrulama ölçütünü 129 nedenin hepsine yaydı. Aynı turda 43 girişte
tekrarlanan iki metin bloğu KALDIRILDI.

Net: 255 → 273.

**Karar:** sınır 275'e çıkarıldı, sayfa kırpılmadı.

**Gerekçe ÖLÇÜLDÜ:** gerçek kısıt 260 değil **300**'dür — KDP'nin iç
kenar (gutter) bandı 151–300 sayfada sabittir ve 301'de değişir. 273 o
bandın içindedir. 260'ın altına inmek ancak L-2'yi yeniden AÇARAK
mümkündü. Görev talimatı § 21: *"Do not optimize for page count at the
expense of content clarity."*

---

## K61 — KAYNAĞIN DESTEKLEDİĞİNDEN GENİŞ İDDİA İÇİN YENİ SEVİYE

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu · **Durum:** UYGULANDI

Sicilde `VERIFIED` ile `INFERRED` arasında bir şey yoktu. Ama okunan bir
kaynak bir iddianın İLKESİNİ destekleyip YAZILDIĞI HÂLİNİ
desteklemeyebilir — `M-007` bicep bunun tam örneği: kaynak "koltuk
altında" der, kitap "en dolgun noktada" ölçer.

**Karar:** `VERIFIED_NARROWER` eklendi (görev talimatı § 9). Kayıt
`source_support: narrower` beyan eder ve `source_support_note` kaynağın
GERÇEKTE ne dediğini yazmak ZORUNDADIR. Seviye yine TÜRETİLİR.

**Gerekçe:** bir güven skoru değildir. `VERIFIED`in anlamı *"kaynak
iddiayı YAZILDIĞI GİBİ destekliyor"*tur; desteklemediğinde iddiayı
`VERIFIED` bırakmak, sicilin tek işini yapmamaktır.

---

## K62 — DOĞRULAMA ÖLÇÜTÜ HAM FARKA DEĞİL EASE'E BAKAR

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu II · **Durum:** UYGULANDI

Otuz yedi doğrulama ölçütü vücut ölçüsünü kalıp okumasıyla DOĞRUDAN
karşılaştırıyordu: *"senin sayın kalıptan büyük"*. Ama kitabın kendi 3.
bölümü bu çıkarmayı **ease** olarak tanımlar ve Ek J bantları basar.
Doğru çizilmiş bir kalıpta kalıp her zaman bedenden bant kadar
büyüktür.

**Ölçülen sonuç tek yönlüydü:** dolgun oturak, çıkık karın ve sığ ağ
derinliği YAPISAL OLARAK doğrulanamıyor; *"ağ çok derin"*, *"arka ağ
çok uzun"* ve *"bel çok geniş"* ise HER kalıpta doğrulanıyordu.

**Karar:** bir bandı olan her ölçüde ölçüt EASE karşılaştırmasıdır ve
bandı ADIYLA söyler. `qa_verification` ⑭ bunu dayatır ve ham
karşılaştırmayı REDDEDER. Ease'in sadeleştiği ölçütler
(`comparison_kind`: ratio / position / size_chart) bundan MUAFTIR ve
muafiyet VERİDEDİR, kapının tahmini değildir.

**İkinci yarısı:** kitap sekiz ölçüyü kaynaktan FARKLI nirengiden alır;
o bantlar başka bir ölçüyü tarif eder ve EŞİK OLAMAZ. Bu, izlenen
veride durur (`applies_to_this_books_measurement`) — izlenmeyen prozada
değil, ki kapı temiz klonda da görsün.

---

## K63 — BASILAN NEDEN SIRASI: KLİNİK ÖNCELİK MALİYETTEN ÖNCE GELİR

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu II · **Durum:** UYGULANDI

Sıra yalnızca `test_cost`tan geliyordu. Ama bazı girişler bir KLİNİK
öncelik de ilan ediyor (*"önce sırtı ele, sonra omuz konumunu"*) ve
ikisi çeliştiğinde basılan sıra maliyeti izliyordu. Dört girişte sıra
TERSTİ — ikisinde tam da girişin *"yanlış olanı düzeltmek ötekini
kötüleştirir"* diye uyardığı çiftte.

**Karar:** öncelik VERİDEDİR (`order_before`) ve sıra dört katmandır:
① kalıp değişikliği gerektirmeyen nedenler ② klinik öncelik ③ test
maliyeti ④ geri alınamaz aileler. Hesap TEK yerdedir
(`06_BUILD/cause_order.py`); atlas girişi ve akış şeması aynı
fonksiyonu çağırır. `graph_audit` ⑭ önceliğin GERÇEKTEN sağlandığını
ölçer — geri alınamaz bir aile onu bastırıyorsa bu SESSİZ kalmaz.

**Sınır:** "koltuk altı kol kapağından önce" bir DÜZELTME sırası
kuralıdır, test sırası değil. İkisi aynı cümlede karışıyordu; ayrıldı.

---

## K64 — YİRMİ BİRİNCİ DÜZELTME AİLESİ: ÖN GÖĞÜS GENİŞLİĞİ

**Tarih:** 31 Ağustos 2026 · **Faz:** İçerik turu II · **Durum:** UYGULANDI

Kitap göğüs üstü genişliğini *"bir GENİŞLİK sorununu bir HACİM
sorunundan ayıran ölçü"* diye satıyor ve yardımcı gerektiren bir ölçü
olarak öğretiyor. O ölçüyü kullanan İKİ nedenin ikisi de **koltuk altı
DERİNLİĞİ** ailesine çıkıyordu. Sırtın genişlik ailesi vardı (`AF-07`),
önün YOKTU: okur farkı ölçüp koltuk altını değiştirmeye yollanıyordu.

**Karar:** `AF-21 — Chest width (narrow / broad chest)` eklendi ve iki
neden oraya taşındı. Aile sayısı artık her yerde KAYITTAN türetilir;
"twenty" yazılı iki cümle bu yüzden sessizce yanlış olacaktı.

**Bedeli kaydediliyor:** yalnızca "fazla genişlik" yönünde nedeni var.
DAR göğüs bu kitapta bir GİRİŞ değildir ve bu, bilinen bir boşluktur.
