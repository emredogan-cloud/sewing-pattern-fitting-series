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
