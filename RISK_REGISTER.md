# RISK REGISTER — TRUE FIT

> Görev talimatı § 19, § 44. Araştırma raporu § 32'den devralınan
> riskler + bu depoda ortaya çıkan üretim riskleri.
>
> **Faz 1 yürütmesinde yeniden değerlendirildi (28 Ağustos 2026).**
> Her risk altı alan taşır: **olasılık · etki · azaltma · tespit
> yöntemi · sahip · faz.**
>
> **Kural: hiçbir risk elverişsiz olduğu için kaldırılmaz.** Bu turda
> hiçbir risk silinmedi; ikisinin değerlendirmesi değişti, dördü eklendi.

---

## 0 · Faz 1 yürütmesinin risk tablosuna etkisi

| Risk | Önce | **Sonra** | Neden |
|---|---|---|---|
| `R-01` ortam | YÜKSEK | **YÜKSEK — değişmedi** | Video kanıt eksikliğinden değil, **üretim kapasitesi yokluğundan** kapsam dışı. İkisi karıştırılmaz. |
| `R-02` talep tavanı | YÜKSEK | **YÜKSEK — değişmedi** | Yeni kanıt yok. Birim telif doğrulandı ama **hacim** ölçülmedi. |
| `R-03` farklılaşma | YÜKSEK | **YÜKSEK — değişmedi** | Dolaylı ve zayıf bir destek gözlemi eklendi; fark testinin **yerine geçmez**. |
| `R-04` teknik doğruluk | YÜKSEK | **YÜKSEK — ama ARTIK YERİ BELLİ** | Ölçü ve aile katmanı kısmen kapandı; risk `C-C`/`C-D`/`C-H` sınıflarına **daraldı**. Şiddeti düşmedi. |
| `R-12` IP / marka | DÜŞÜK olasılık | **ORTA–YÜKSEK olasılık** | Somut bir çakışma **bulundu** (`K18`). Bu, en büyük tek değerlendirme değişikliğidir. |
| `R-05` görsel üretim | ORTA–YÜKSEK | ORTA–YÜKSEK | `A11` fotoğraf bağımlılığını kaldırdı ama alıcı beklentisi riski durdu |
| `R-06` fiziksel sınama | ORTA | ORTA — **yeni bir sınır eklendi** | Üretilmiş sapma ≠ doğal sapma (`K29`) |
| `R-09` format | ORTA | ORTA — **doğrulandı** | Spiralin KDP'de **olmadığı** kesinleşti; risk artık bir varsayım değil, bir olgu |

---

## R-01 · ORTAM RİSKİ — serinin en büyük riski

| | |
|---|---|
| **Nasıl gerçekleşir** | Lider ürün hibrit (QR→video). Saf basılı ürün yapısal olarak dezavantajlı olabilir. Araştırma raporu § 27'de "basılı format avantajı" iddiası **ZAYIF** çıktı. |
| **Olasılık** | **ORTA–YÜKSEK** — ölçülmedi |
| **Etki** | **YÜKSEK** — ürünün rekabet konumu |
| **Azaltma** | `A4` kararı (`K25`): basılı kitap **kendi başına eksiksiz**; tek adresli tamamlayıcı; bağımsızlık testi **tasarım gereği geçiyor**. Hareketli gösterim gerektiren beş içerik türü adlandırıldı; üçü Kitap 2'ye ait |
| **Tespit** | Faz 3 pilot testinin **son sorusu**: "internette bir tamamlayıcı sayfa olsaydı orada ne bulmak isterdiniz?" — yönlendirmesiz. Üç okurdan ikisi kendiliğinden hareketli gösterim isterse `A4` Kitap 2 için yeniden açılır |
| **Mekanik koruma** | `qa_claims.py § ②` — basılı üstünlük iddiası bir gerçek gibi yazılamaz |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase3-pilot` (ölçüm) · Kitap 2 `phase1-spec` (karar) |

## R-02 · TALEP TAVANI RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Mutlak alıcı havuzu ölçülemedi; yalnızca açığa vurulmuş tercih (yorum sayıları) var. Yıllık havuz on binlerse üç kitaplık seri için tavan düşük olabilir. |
| **Olasılık** | **ORTA** — ölçülmedi |
| **Etki** | **YÜKSEK** — seri tezinin tamamı |
| **Azaltma** | Üç kitabın da **bağımsız** arama trafiği var; seri tezi çökse bile harmanlanmış telif tek kitabın üzerinde kalıyor. **Faz 1 katkısı:** birim telif **doğrulandı** ($11,18) ve başabaş ACoS %41,4 çıktı — dar bir nişte yüksek fiyatlı ürünün yapısal avantajı sayıyla gösterildi |
| **Tespit** | Kitap 1 lansmanının ilk 90 günlük organik performansı |
| **Sahip** | Kurucu — araştırma raporu § 35 madde 5 bunu açık bir kanıt boşluğu olarak bıraktı |
| **Faz** | Kitap 1 `release` (P7) |

## R-03 · FARKLILAŞMA RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | "Teşhis-önce" konumlandırması kanıtlanmamış bir hipotezdir. Alıcı `Complexity(58)` şikâyetini bizim çözdüğümüzü **satın alma anında** fark etmeyebilir. |
| **Olasılık** | **ORTA** — ölçülmedi |
| **Etki** | **KRİTİK** — üç kitap da aynı hipoteze dayanıyor |
| **Azaltma** | Kill-gate'e bağlandı: üç okurdan en az ikisi farkı kendiliğinden söylemezse **proje durur**. Protokol Faz 1'de **tamamlandı** (betik, form, eleme ölçütleri, malzeme spesifikasyonu) |
| **Tespit** | Faz 3 fark testi. **Zayıf ve dolaylı bir ön işaret:** gönüllü içerikte fazlalık ↔ yetersizlik ayrımının sistematik olarak karıştırıldığı gözlendi (`01_SOURCE/PUBLIC_SOURCE_SURVEY.md § 5.1`) `OBSERVED`. **Bu, testin yerine GEÇMEZ** |
| **Sahip** | Kurucu (`A14`) |
| **Faz** | Kitap 1 `phase3-pilot` |

## R-04 · TEKNİK DOĞRULUK RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Teknik olarak yanlış bir belirti–neden bağı, okuru yanlış düzeltmeye yönlendirir ve kumaşını mahveder. |
| **Olasılık** | **ORTA–YÜKSEK** |
| **Etki** | **YÜKSEK** — ürünün tek gerçek savunması doğruluktur |
| **Faz 1'de ne değişti** | Risk **daralmadı, YERİ BELLİ OLDU.** 32 ölçünün 16'sı ve 19 ailenin 13'ü otoriter kamu kaynağına bağlandı. Ama **43 belirtinin ve 129 ayırt edici kanıtın hiçbiri** doğrulanmadı — çünkü hiçbir kamu kaynağı aynı belirtinin iki nedenini ayırmıyor |
| **Azaltma** | `verification_status` mekanik olarak dayatılıyor; hiçbir kayıt kanıtsız yükseltilemiyor (`validate_spec` + **`selftest` gerçek korpus üzerinde**, `K20`). İkinci katman: fiziksel sınama (`A13`, 19 kayıt) |
| **Tespit** | ① `Y-1` belirti üretme testinde eşleşmeyen teşhis sayısı; ② `Y-2` ayırt edicilik testinde ayırmayan kanıt sayısı; ③ ileride bir kaynak edinilirse ilk çapraz kontroldeki çelişki sayısı |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase3-pilot` (birincil) · Kitap 2 `phase1-spec` (`A-03` ile ikincil) |

## R-05 · GÖRSEL ÜRETİM RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Rakipler gerçek vücut fotoğrafı kullanıyor; alıcı fotoğraf bekliyorsa saf çizgi grafiği dezavantajdır. Ayrıca diyagram hacmi tahminden büyük çıkabilir. |
| **Olasılık** | ORTA |
| **Etki** | ORTA–YÜKSEK |
| **Azaltma** | `A11` (`K35`): yedi figür türünün **dördünde fotoğraf çizimden kötüdür** — karar bir bütçe kısıtı değil, bir işlev analizidir. Kapak tam renkli; tamamlayıcı görsel taşıyabilir. Hacim tarafında: `figure_schema § deterministic` + zorunlu `manual_reason` |
| **Tespit** | Faz 2 çıkış ölçütleri: deterministik figür oranı · `photo_required` sayısı (eşik **6**) · `color_required` oranı (eşik **%10**) |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase2-visual` |

## R-06 · FİZİKSEL SINAMA RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Sınama **tek bir vücut** üzerinde ve **ürünün sahibi** tarafından yapılıyor. |
| **Olasılık** | **KESİN** — bu bir belirsizlik değil, bir tasarım sınırıdır |
| **Etki** | ORTA |
| **Faz 1'de eklenen YENİ sınır** | **Kasten üretilmiş bir sapma, o sapmayı doğal olarak taşıyan bir vücudun tam eşdeğeri değildir** (`K29`). `A13`'ün maliyeti düşüren tasarımı bu sınırı satın aldı |
| **Azaltma** | Sınır `VALIDATION_PROTOCOL.md § 7`'de dört madde hâlinde **açıkça** yazılı; hiçbir yerde bağımsız sınama iddia edilmiyor. `T-1c` kontrol toile'i, üretilen belirtiyi baştan var olandan ayırır |
| **Tespit** | Okur yorumlarında "bende işe yaramadı" deseni |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase3-pilot` · sürekli izleme P7 sonrası |

## R-07 · İÇERİK KAPSAMI / SERİ YEME RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Kitap 1 düzeltme adımı verirse Kitap 2 gereksizleşir; Kitap 2 blok çizimine girerse Kitap 3 gereksizleşir. |
| **Olasılık** | DÜŞÜK — mekanik olarak yönetiliyor |
| **Etki** | ORTA–YÜKSEK |
| **Azaltma** | Tek-birincil kuralı + topik bölme + adım dili taraması |
| **Tespit** | `qa_boundary.py` sızıntı bulguları · **`qa_crosswalk.py § ⑥`** kitap sahipliği çelişkisi (Faz 1'de eklendi) |
| **Sahip** | Ajan (mekanik) |
| **Faz** | Sürekli |

## R-08 · REKABET RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Haz–Ağu 2026'da 13 yeni başlık girdi. Hiçbiri traksiyon kazanmadı — ama bir sonraki kazanabilir. |
| **Olasılık** | ORTA |
| **Etki** | ORTA–YÜKSEK |
| **Azaltma** | 90 günlük yorum/BSR takibinin başlatılması — **Faz 2 görevi (`G7`)** |
| **Tespit** | **Takip HÂLÂ BAŞLATILMADI.** Terk koşulu: biri 6 ayda 200+ yoruma ulaşırsa niş kapanmış demektir |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase2-visual` |

## R-09 · FORMAT RİSKİ — **DOĞRULANDI**

| | |
|---|---|
| **Nasıl gerçekleşir** | Kitap 2 bir referans atlasıdır ve düz açık durmalıdır. |
| **Olasılık** | **KESİN** — artık bir varsayım değil |
| **Etki** | ORTA |
| **Faz 1 bulgusu** | **KDP spiral / tel sarmal cilt SUNMUYOR** — yalnızca yapıştırma ciltsiz ve ciltli (`S-0013`). Rakibin gözlemlenen spiral SKU'su KDP dışı bir yolla üretilmiş olmalıdır |
| **Azaltma** | Kitap 1 için düz açık durma **kritik değil** (baştan sona okunan bir yöntem kitabıdır). Kitap 2 için KDP dışı bir üretim yolu araştırılacak |
| **Tespit** | Kitap 2 `phase1-spec` fizibilite araştırması: vendor, maliyet, Amazon'da listeleme yolu |
| **Sahip** | Kurucu |
| **Faz** | **Kitap 2 `phase1-spec`** |

## R-10 · FİYAT RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Gözlemlenen medyan $21–23. Model $26,99'da tutuldu ama garanti değil. |
| **Olasılık** | ORTA |
| **Etki** | ORTA |
| **Faz 1 katkısı** | Asgari liste fiyatları **hesaplandı**: siyah mürekkep $8,36 · standart renk $17,48 · premium renk **$33,14**. Premium rengin fiyat bandını aşması, bir fiyat riskini bir **format kısıtına** çevirdi |
| **Azaltma** | Fiyat bandı aralık olarak tutuluyor; tek nokta olarak kilitlenmiyor |
| **Tespit** | İlk 90 günlük dönüşüm oranı |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `phase6-format` |

## R-11 · REKLAM RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Dönüşüm %5'in altında kalırsa tolere edilebilir CPC $0,56'ya iner. Niş dar; ücretsiz video içeriği güçlü. |
| **Olasılık** | ORTA |
| **Etki** | ORTA |
| **Azaltma** | Yazılı iptal eşiği (`D1`) + beş ek durma koşulu. **`D6`:** yorumsuz bir sayfada düşük dönüşüm bir reklam sorunu **değildir**; `D1` o durumda uygulanmaz |
| **Tespit** | 300 tıklamalık keşif testi; Kampanya A **CPC'yi ölçmek için** |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `release` (P7) |

## R-12 · IP / MARKA RİSKİ — **OLASILIK YÜKSELDİ**

| | |
|---|---|
| **Nasıl gerçekleşir** | Seri adı çakışması → yeniden markalama veya listeleme kaldırma. Ticari kalıp markasının metadata'ya sızması → listeleme kaldırılabilir. |
| **Olasılık** | **ORTA–YÜKSEK** *(önce: DÜŞÜK)* — somut bir çakışma **bulundu** |
| **Etki** | **YÜKSEK** — üç kitabı aynı anda etkiler |
| **Faz 1 bulgusu** | `TRUE FIT`, True Fit Corporation adına yürürlükte ve tescilli bir ABD markasıdır ve kapsamı "kullanıcıları **vücut ölçülerine göre** giysiyle eşleştirme"dir — bu serinin tam konusu `OBSERVED` |
| **Azaltma** | `K18`: ad yayımlanan marka olarak **kilitlenmedi**. `K32`: GitHub deposu **marka-nötr** adla açıldı. Ticari kalıp markası tarafında mekanik koruma sürüyor |
| **Tespit** | `validate_structure.py § check_brand_leak` (kalıp markaları) · profesyonel marka temizliği (`A15`) |
| **Sahip** | Kurucu (`A15`) + marka vekili |
| **Faz** | Seçim: `phase2-visual` başlangıcı · temizlik: kapak öncesi |

## R-13 · AI İKAME RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Bir dil modeli bu içeriği üretebilir hâle gelirse ürünün savunması zayıflar. |
| **Olasılık** | DÜŞÜK–ORTA |
| **Etki** | ORTA |
| **Azaltma** | Geometrik olarak doğru düzeltme diyagramı üretmek zordur ve hata dikilen giyside anında görünür. Bu projenin **fiziksel sınama katmanı**, taklit edilmesi en zor kısımdır |
| **Tespit** | — (yapısal) |
| **Sahip** | — |
| **Faz** | Sürekli |

## R-14 · KAPI EROZYONU RİSKİ *(bu depoya özgü)*

| | |
|---|---|
| **Nasıl gerçekleşir** | Kill-gate FAIL verdiğinde kapının gevşetilmesi veya AI vekil testinin insan testi yerine sayılması. |
| **Olasılık** | ORTA |
| **Etki** | **KRİTİK** — kapı erozyonu bütün diğer korumaları geçersizleştirir |
| **Faz 1'de eklenen YENİ erozyon yüzeyi** | **`INCONCLUSIVE` durumu** (`K30`). 1–2 katılımcıyla yapılan bir testin "neredeyse PASS" diye sunulması en olası erozyon biçimidir |
| **Azaltma** | `aiProxyCountsAsHuman: false`, açılamaz. `founderOverride` ayrı bir alandır ve "geçti" diye DEĞİL, "kapıyı ilerleten ölçüm değil kurucu kararıdır" diye raporlanır. **`INCONCLUSIVE` → `measured` `false` KALIR** ve `kill_gate.py` engel raporlamaya devam eder |
| **Tespit** | `kill_gate.py` bayrak denetimi · `selftest.test_kill_gate_flag_cannot_be_flipped` |
| **Sahip** | Ajan + Kurucu |
| **Faz** | Sürekli |

---

# FAZ 1 YÜRÜTMESİNDE KEŞFEDİLEN YENİ RİSKLER

## R-15 · TEK KAYNAK BAĞIMLILIĞI *(yeni)*

| | |
|---|---|
| **Nasıl gerçekleşir** | Bölüm 3'ün ease bantları **tek bir kaynağa** dayanıyor (`S-0001` Table 1). O bandın atipik veya hatalı olması, Bölüm 3'ün bütün sayısal örneklerini bozar. Aynı yapı `M-031`'in ≥2 inç eşiği için de geçerlidir (`S-0003`). |
| **Olasılık** | ORTA |
| **Etki** | ORTA — bölüm çöker, kitap çökmez |
| **Azaltma** | `K21`'in üçüncü koşulu: bölümün **yöntemi** sayısal banttan bağımsız kalır. Bant düşse bile "bitmiş ölçü − vücut ölçüsü = ease" ayakta kalır. Ayrıca bant **kaynağı adıyla** anılır — anonim bir "standart" gibi sunulmaz |
| **Tespit** | İkinci bir kaynak edinildiğinde (`A-01` veya TAMU E-373) ilk çapraz kontrol. Çelişki çıkarsa `SOURCING_STANDARD § 7` uyarınca `DECISIONS.md`'ye açık bulgu olarak yazılır |
| **Sahip** | Ajan |
| **Faz** | Kitap 1 `phase2-visual` (ücretsiz edinimler) · Kitap 3 `phase1-spec` (`A-01`) |

## R-16 · KAYNAK BAĞLANTISI ÖLÜMÜ *(yeni)*

| | |
|---|---|
| **Nasıl gerçekleşir** | Altı kamu kaynağının hepsi web'de barındırılan PDF'lerdir. Üniversite yayım siteleri yeniden düzenlenir; devlet arşivleri taşınır. Politika gereği kaynağın **metni depoya girmez** — yalnızca künye ve locator girer. Bağlantı ölürse doğrulama zinciri kopabilir. |
| **Olasılık** | **ORTA–YÜKSEK** — çok yıllık bir projede neredeyse kaçınılmaz |
| **Etki** | DÜŞÜK–ORTA — yeniden edinilebilir, ama zaman kaybettirir |
| **Azaltma** | Her kayıt **tam künye + locator + erişim tarihi** taşıyor; bu, kaynağı başka bir yerden (kütüphane, arşiv) yeniden bulmaya yeter. İndirilen PDF'ler kurucunun **yerel** arşivinde tutulur ve depoya **girmez** (`.gitignore`) |
| **Tespit** | Faz 2 ve Faz 5 KA'sında kaynak URL'lerinin toplu kontrolü |
| **Sahip** | Ajan |
| **Faz** | Kitap 1 `phase2-visual`, sonra her fazda |

## R-17 · KÜÇÜK SINAMA SETİNİN EŞİĞİ TETİKLEMESİ *(yeni)*

| | |
|---|---|
| **Nasıl gerçekleşir** | `A13` seti 19 kayıttır. **Tek bir FAIL, hata oranını %5,3 yapar** — yani "üretim yöntemi reddedilir" eşiğinin (>%5) üstüne. Doğal ve yanlış tepki: eşiği gevşetmek veya seti büyütüp oranı seyreltmek. |
| **Olasılık** | ORTA |
| **Etki** | **YÜKSEK** — `R-14`'ün (kapı erozyonu) somut bir biçimidir |
| **Azaltma** | `K29`'da **yazılı**: eşik gevşetilmez. Bir FAIL çıkarsa doğru tepki kök nedeni düzeltip **seti yeniden koşmaktır** — oranı seyreltmek değil |
| **Tespit** | Faz 3 raporunda hata oranının paydası: set büyütülerek mi düşürüldü |
| **Sahip** | Ajan + Kurucu |
| **Faz** | Kitap 1 `phase3-pilot` |

## R-18 · DİJİTAL TAMAMLAYICININ TERK EDİLMESİ *(yeni)*

| | |
|---|---|
| **Nasıl gerçekleşir** | Basılı kitaptaki QR ve adres **güncellenemez**. Alan adı yenilenmezse veya barındırma durursa, basılı kitaplarda ölü bir adres kalır. |
| **Olasılık** | ORTA — çok yıllık ürün ömründe |
| **Etki** | **DÜŞÜK** — tasarım gereği |
| **Azaltma** | `K25`'in bağımsızlık testi: üç tamamlayıcı kalemin ikisinin basılı karşılığı var (Ek E, Ek G), üçüncüsünün yokluğu kitabı çalışmaz kılmaz. **Tek adres, tek risk** — sayfa başına QR reddedilmesinin asıl gerekçesi budur. Adres kitapta **metin olarak da** yazar |
| **Tespit** | Yıllık alan adı yenileme takvimi |
| **Sahip** | Kurucu |
| **Faz** | Kitap 1 `release` sonrası, sürekli |

---

## Terk etme koşulları — ölçülebilir

Araştırma raporu § 32'den devralındı; Faz 1'de sayılar doğrulandı.

1. Fark testi: üç okurdan hiçbiri farkı kendiliğinden fark etmezse → **dur**
2. Fiziksel sınama: hata oranı **>%5** → üretim yöntemi reddedilir, **dur**
3. 13 rakip başlıktan biri 6 ayda 200+ yoruma ulaşırsa → niş kapanmış
4. Liderin `Complexity(58)` etiketi 12 ayda kaybolursa → kalite açığı kapanmış
5. Reklam testinde dönüşüm %5 altındaysa → ücretli edinme iptal
   *(başabaş CPC $0,56; başabaş ACoS %41,4 — `ADS_FRAMEWORK § 1`)*
6. Kitap 3'ün bağımsız talep kanıtı zayıflarsa → seri **ikiye** indirilir

---

*Vâliçe Press · TRUE FIT · Risk Register · 28 Ağustos 2026 (Faz 1 yürütmesi)*
