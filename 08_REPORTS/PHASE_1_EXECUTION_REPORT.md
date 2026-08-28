# PHASE 1 EXECUTION REPORT — Kitap 1

> **Durum: `READY_FOR_DECISION`** — Kitap 1 Faz 1 içsel olarak
> tamamlandı; iki dış bağımlılık açık.
>
> Tarih: **28 Ağustos 2026** · Seri kapısı `bootstrap` (ilerlemedi) ·
> Kitap 1 kapısı `foundation` (ilerlemedi)
>
> Durum sözlüğü: `00_CONTEXT/QA_STANDARD.md § 6`

---

## 1 · Executive Summary

Bu tur, Kitap 1 Faz 1'i **onay bekleyen bir spesifikasyondan**
**yürütülmüş bir faza** çevirdi. Üç şey yapıldı:

**① On dört açık kurucu kararının on ikisi kapatıldı.** Kalan ikisi
(`A10` çizim sistemi, `A12` bütçesi) ertelendi ve iki tanesi
(`A14` katılımcılar, yeni `A15` seri adı) dış beklemeye alındı —
**hiçbiri "hâlâ açık" olarak bırakılmadı.**

**② Depo sıfır kaynaktan 15 kaynağa geçti — hiçbir şey satın
alınmadan.** Yedi eksende yapılan kamu taraması altı tam metin teknik
otorite kaynağı buldu. Sonuç: 32 ölçünün **16'sı** ve 19 düzeltme
ailesinin **13'ü** kanıta bağlandı.

**③ En önemli bulgu bir olumsuzluktur.** 43 belirti kaydının **hiçbiri**
yükseltilmedi ve bu bilinçlidir: bir belirti kaydının çekirdek iddiası
aynı belirtinin iki nedenini ayıran kanıttır (`C-C` sınıfı) ve **hiçbir
kamu kaynağı bu ayrımı yapmaz.** Bu, `A13` fiziksel sınama planını bir
"iyi olur" kaleminden **tek doğrulama yoluna** çevirdi.

Ayrıca iki uyarı üretildi: seri adı `TRUE FIT` **yayımlanamaz**
(tescilli, aynı sektörde) ve KDP **spiral cilt sunmuyor** (Kitap 2'nin
ürün gereksinimi doğrudan etkileniyor).

**Kapılar ilerlemedi.** Ne seri kapısı ne kitap kapısı yükseltildi;
kill-gate iki engelle bloklu kaldı. Bu, bir eksiklik değil, tasarımın
kendisidir.

## 2 · Founder Decisions Resolved

| # | Soru | Durum | Karar |
|---|---|---|---|
| `A1` | Seri adı | **CLOSED — DECIDED** | `TRUE FIT` **yayımlanan ad olarak kullanılamaz** (`K18`) |
| `A2` | GitHub | **CLOSED — FOUNDER POLICY** | Public + CI, **marka-nötr depo adıyla** (`K32`) |
| `A3` | Kaynak bütçesi | **CLOSED — DECIDED** | Faz 1 **satın almasız** kapandı (`K19`) |
| `A4` | Ortam | **CLOSED — DECIDED** | Basılı + tek adresli tamamlayıcı; video kapsam dışı (`K25`) |
| `A5` | Format | **CLOSED — DECIDED** | 8,5×11 ciltsiz, beyaz kâğıt (`K22`) |
| `A6` | Renk | **CLOSED — DECIDED** | Siyah mürekkep + %10 yeniden açılma eşiği (`K23`) |
| `A7` | Yazı tipi | **CLOSED — DECIDED** | Source Serif 4 + Source Sans 3, OFL, **$0** (`K24`) |
| `A8` | Birim | **CLOSED — DECIDED** | İnç birincil; figürlerde tek birim (`K34`) |
| `A9` | Kitap 3 terminolojisi | **CLOSED — DECIDED** | Başlıkta `sloper`, kanonik `block` (`K26`) |
| `A10` | Çizim sistemi | **DEFERRED** | Kanıt kapısı kuruldu; sistem seçilemez (`K27`) |
| `A11` | Fotoğraf | **CLOSED — DECIDED** | Kullanılmaz; koşullu en fazla 6 (`K35`) |
| `A12` | Reklam | **CLOSED — DECIDED** (çerçeve) · bütçe **DEFERRED** | Başabaş CPC ve ACoS hesaplandı (`K28`) |
| `A13` | Sınama kapsamı | **CLOSED — DECIDED** | 2 toile + 3 parça, 19 kayıt (`K29`) |
| `A14` | Test katılımcıları | **EXTERNAL PENDING** | Protokol tam; katılımcı yok (`K30`) |
| `A15` | *(yeni)* Yerine geçen ad + temizlik | **EXTERNAL PENDING** | `A1`'in doğurduğu soru |

**Sayım: 12 kapandı · 1 ertelendi · 2 dış beklemede.**
Yeni karar kayıtları: `DECISIONS.md K18`–`K35` (18 kayıt).

## 3 · Source Research

### 3.1 · Ne bulundu

| Kayıt | Kaynak | Kurum | Seviye |
|---|---|---|---|
| `S-0001` | Guide C-228 *Pattern Alteration* | New Mexico State Univ. Extension | `fulltext` |
| `S-0002` | Guide C-227 *Making Perfect Pants* | New Mexico State Univ. Extension | `fulltext` |
| `S-0003` | E-372 *Principles of Pattern Alteration* | Texas AgriLife Extension | `fulltext` |
| `S-0004` | EM4582 *Challenging Patterns* | Washington State Univ. Extension | `fulltext` |
| `S-0005` | ANSUR II — NATICK/TR-15/007 | U.S. Army Natick (kamu malı) | `fulltext` |
| `S-0006` | NHANES 2021 Anthropometry Procedures Manual | CDC / NCHS (kamu malı) | `official_pdf` |
| `S-0007` `S-0008` | MSU Extension E-419 / E-421 | Michigan State Univ. | `official_web` — **taranmış, okunamadı** |
| `S-0009`…`S-0013` | Amazon KDP yardım sayfaları | platform | `official_web` — **teknik otorite DEĞİL** |
| `S-0014` `S-0015` | ISO 8559-1 · ASTM D5219 | ISO · ASTM | `not_yet_acquired` |

### 3.2 · Üç en değerli bulgu

**① Fazlalık ↔ yetersizlik ayrımı (`S-0004`).** Kumaşı **çeken**
kırışıklık *az* ease'i, **kıvrım hâlindeki** kırışıklık *çok* ease'i
gösterir. Bu, kitabın en çok kullanılan kuralının (`TK-05` ↔ `TK-06`,
Bölüm 7.4, teşhis Adım ③) kurumsal karşılığıdır — ve gönüllü içerikte
**sistematik olarak karıştırılan** ayrımdır.

**② Sıra kuralı (`S-0003`).** Bir seferde tek düzeltme; önce **boy**,
omuz/boyundan aşağı; sonra **genişlik**, yine yukarıdan aşağı. Bölüm
16'nın ① ve ② kurallarını doğrular — `C-F` sınıfının ilk dış
doğrulaması.

**③ Ease bantları (`S-0001` Table 1).** `C-G` sınıfını
"**yazılamaz**"dan "adı konmuş tek bir konvansiyonla yazılabilir"e
taşıdı (`K21`, üç koşulla).

### 3.3 · Ne satın alınması gerekiyor — ve NE ZAMAN

| Kalem | Gerçekten gerekli olduğu faz | Maliyet | Alternatif |
|---|---|---|---|
| ISO 8559-1:2017 | **Kitap 3 P1** | ≈$230 | Kısmen TAMU E-373 + fiziksel tekrar-ölçüm |
| ASTM D5219 (yürürlükteki) | Kitap 3 P1 — **isteğe bağlı** | ≈$76–90 | ISO büyük ölçüde kapsar |
| *Fitting and Pattern Alteration* 4. baskı | **Kitap 2 P1** | $135 veya **$0** | **Kütüphane ödünç — ÖNERİLEN** |
| Bir kalıp çizim referansı (Aldrich / Joseph-Armstrong) | **Kitap 3 P1** | $45–60 | Yok |

**Kitap 1 Faz 1 için gereken: $0.** Ayrıca **ücretsiz ama yapılması
gereken** üç edinim Faz 2'ye yazıldı (TAMU serisinin elle indirilmesi,
USDA 1945 bültenleri, MSU taramalarının gözle okunması).

### 3.4 · Ne reddedildi

Telifli uyum kitaplarının izinsiz tam kopyalarını sunan siteler
**kullanılmadı**. Dikiş blogları ve rakip ürün sayfaları
`technical_authority` taşıyamaz (mekanik: `check_source_type_authority_consistency`).

## 4 · Technical Validation Status

| Kayıt türü | Toplam | VERIFIED | PARTIALLY VERIFIED | EXTERNAL-SOURCE REQUIRED | UNVERIFIED |
|---|---|---|---|---|---|
| Ölçü (`M-xxx`) | 32 | **16** | 7 | 9 | — |
| Düzeltme ailesi (`AF-xx`) | 19 | **13** | 4 | 2 | — |
| Belirti (`SYM-xxx`) | 43 | 0 | — | — | **43** |
| Aday neden / ayırt edici kanıt | 129 | 0 | — | — | **129** |
| Blok bileşeni (`BLK-xx`) | 12 | 0 | — | 12 | — |
| Crosswalk (`XW-xxx`) | 148 | iç bütünlük ✓ | — | — | dış doğrulama yok |

**Terim tanımları.** *VERIFIED* = elde tutulan bir `fulltext`/`official_pdf`
otorite kaydın çekirdek iddiasını tanımlıyor. *PARTIALLY VERIFIED* =
kaynak kaydın bağlamını destekliyor ama çekirdek iddiasını tanımlamıyor
(`source_refs` var, durum yükseltilmedi). *EXTERNAL-SOURCE REQUIRED* =
hiçbir kamu kaynağında karşılığı yok; hangi kalemin kapatacağı yazılı.
*UNVERIFIED* = dış otorite yok **ve** fiziksel sınama yapılmadı.

**Belirtiler neden sıfırda kaldı.** Elde tutulan altı kaynağın hepsi
*figür tipinden düzeltmeye* gider. Hiçbiri *belirtiden nedene* gitmez
ve — kritik olan — hiçbiri **aynı belirtinin iki nedenini ayırmaz.**
Bir belirti kaydının çekirdek iddiası tam olarak budur.

**Mekanik koruma iki katmanlı.** `validate_spec.check_verification_evidence`
tek kaydı denetler; `selftest.test_verification_status_is_honestly_recorded`
**gerçek korpusun tamamını** denetler. İkincisi bu turda yazıldı ve
kasıtlı bir kusurla sınandı (`K20`).

## 5 · Medium Decision

**Basılı kitap + tek adresli dijital tamamlayıcı. Video kapsam dışı.
Sayfa başına QR reddedildi.**

Tamamlayıcının üç kalemi: yazdırılabilir boş formlar · akış şemalarının
renkli sürümü · düzeltme (errata) sayfası. Üçünün de basılı karşılığı
var veya yokluğu kitabı çalışmaz kılmıyor — **bağımsızlık testi tasarım
gereği geçiyor.**

**Kararın omurgası olan bulgu:** hareketli gösterim gerektiren beş
içerik türü adlandırıldığında **üçünün Kitap 2'ye ait olduğu** görüldü.
Kitap 1'in içeriği (teşhis) yapısal olarak durağan, Kitap 2'nin içeriği
(işlem) yapısal olarak hareketlidir.

⚠ Video, kanıt eksikliğinden değil **üretim kapasitesi yokluğundan**
kapsam dışıdır. `R-01` bu yüzden **azalmadı**.

## 6 · Format Decision

| Konu | Karar |
|---|---|
| Trim / cilt | **8,5×11 ciltsiz** (large trim) |
| Kâğıt | **Beyaz** — groundwood reddedildi (ince çizgiler kaybolur) |
| Ciltli SKU | 8,25×11 **aday**, P6'da karara bağlanır |
| Kindle | **Ertelendi** — Faz 2'nin ölçtüğü dosya boyutuna bağlı |
| Spiral | **KDP'de YOK** — doğrulandı |

**Ekonomi (236 sayfa, doğrulanmış oranlar):** baskı maliyeti **$5,01**,
$26,99'da birim telif **$11,18**, başabaş ACoS **%41,4**.
Ciltli 8,25×11: maliyet $9,66, $34,99'da telif **$11,33**.

**Kitap 2 sonucu:** düz açık durma gereksinimi KDP dışı bir üretim yolu
ister → **Kitap 2 `phase1-spec` görevi** (`R-09` artık bir varsayım
değil, bir olgu).

## 7 · Visual Decision

**Renk:** siyah mürekkep, beyaz kâğıt. Premium renk **aritmetik olarak
dışarıda** (asgari liste $33,14 > fiyat bandının üstü). Standart renk
mümkün ama telifi %49 düşürüyor. **Seçmeli renk platformda mevcut
değil.** Yeniden açılma eşiği: `color_required` oranı %10.

**Fotoğraf:** kullanılmaz. Yedi figür türünden **dördünde fotoğraf
çizimden kötüdür**, birinde imkânsızdır. Koşullu kapı: en fazla 6 figür,
beş koşulla, kaynağı `A13`'ün sınama programı.

**Tipografi:** Source Serif 4 + Source Sans 3 (SIL OFL 1.1, **$0**).
Yedek: Charis SIL (metin), Atkinson Hyperlegible (figür etiketi).
Altı test (`T1`–`T6`) Faz 2'ye eklendi — aralarında **⅝ glifinin gerçek
baskıda okunması** ve 6 pt'de rakam ayırt edicilik testi.

**Notasyonun teknik gerekliliği:** `TK-05` ↔ `TK-06` ayrımı artık bir
stil tercihi değil; `S-0004` ile kaynağa bağlı bir gerekliliktir.

## 8 · Unit Decision

**İnç birincil.** Figürlerde **yalnızca inç** (etiket yoğunluğu ve
"bir yayılım, bir kavram" kuralı). **Karar eşiklerinde ve tablolarda
inç + cm** — bir eşik okura verilen sayısal bir kuraldır; ABD dışındaki
okur onu uygulayamıyorsa yöntem ona kapanır.

Dayanak: ABD standart dikiş payı **⅝ inç**; doğrulanmış üç kaynağın
**tamamı** inç kullanıyor.

## 9 · Terminology Decision

Kitap 3 başlığında **`sloper`**; depo içi kanonik terim **`block`**
kalır; alt başlık her ikisini de taşır.

Belirleyici bulgu: ABD dikiş dilinde `block` **kapitone bloğu** anlamını
taşır ve arama sonuçları bu anlamla doludur. Kanonik terim
değiştirilmedi — `A9` zaten "hangisi *başlıkta* duracak" sorusuydu.

## 10 · Book 1 Scope

Kapsamdan **çıkarılan hiçbir şey yok, eklenen hiçbir şey yok.**
Değişen tek şey üç bölümün hangi dille yazılabileceğidir:

| Bölüm | Önce | Sonra |
|---|---|---|
| 3.5–3.6 ease | Yazılamaz | **Yazılabilir** — `K21`'in üç koşuluyla |
| 3.1–3.2 beden tabloları | Yazılamaz | **Kısmen** — seçim kuralı doğrulandı, tablolar çoğaltılmaz |
| 2 ölçü tanımları | Yazılamaz | **16 tam · 7 kısmi · 9 açık** |

Sabit kalan: 5 parça · 18 bölüm · ekler · 220–260 sayfa hedefi ·
10 alıştırma · 43 belirti.

## 11 · Book 1 Content Architecture

Mimari korundu ve **iki yeni satırla derinleştirildi**: her bölüm artık
bir **kaynak kanıtı** satırı (hangi `S-xxxx` kaydına dayanıyor ve
**nereye dayanmıyor**) ve bir **karar noktaları** bloğu (okurun o
bölümde verdiği ikili kararlar) taşıyor — 18 bölümün hepsinde.

Karar noktaları Faz 2 akış şemalarının **doğrudan girdisidir**: bir
akış şemasının karar düğümleri, bölümün karar noktalarıdır.

Üç bölümün kaynak satırı bilerek "Yok" der (Bölüm 1, 17, 18) — bu
bölümler teknik iddia taşımaz veya projenin kendi yapısıdır.

## 12 · Diagnostic System

Yedi adımlı döngü korundu. **Dört adım artık bir kamu kaynağına
bağlıdır:**

| Adım | Kaynak |
|---|---|
| ② GÖZLE — sabit sıra, önce denge/çözgü | `S-0003` (13 maddelik kontrol listesi) · `S-0004` (beş temel nokta) |
| ③ SINIFLA — fazlalık ↔ yetersizlik | **`S-0004`** |
| ④ YERİNİ BUL — kaynağında düzelt | **`S-0003`** |
| ⑤ ÖLÇ — beden seçim eşiği | `S-0003` (≥ 2 inç kuralı) |

**Doğrulanmayan:** adım ⑥'nın üzerinde çalıştığı **129 ayırt edici
kanıtın hiçbiri.** Bu, çerçevenin en büyük açık noktası olarak § 6'ya
eklendi.

`SYMPTOM ≠ CAUSE` ve `HENÜZ DEĞİŞTİRME` ilkeleri değişmedi.

## 13 · Crosswalk

**148 kaydın tamamı denetlendi — dokuz ayrı ilişki üzerinden. Bulgu: 0.**

| Denetim | Sonuç |
|---|---|
| ① Kaynak uç noktası tanımlı | 148/148 |
| ② Devir cümlesi aday nedeni taşıyor | 129/129 |
| ③ Hedef uç noktası tanımlı | 148/148 |
| ④ İstisna mantığı **iki yönlü** tutarlı | 148/148 |
| ⑤ Taksonomiyle **birebir** (kayıp/uydurma yol yok) | 129/129 |
| ⑥ Kitap sahipliği tutarlı | 129/129 |
| ⑦ Devir cümlesi **kanonik adı** taşıyor | 108/108 |
| ⑧ Her giriş noktası ailesine ulaşılıyor | **19/19** |
| ⑨ Her belirtinin yolu var | **43/43** |

**Denetim kalıcı bir kapıya dönüştürüldü:** `06_BUILD/qa_crosswalk.py`
(`K31`), `qa_all.sh` + CI + `selftest.py`'ye bağlandı. Sekiz kusurlu
kurgu ile kapının gerçekten yakaladığı kanıtlandı.

**Neden ayrı bir kapı gerekti:** `build_crosswalk --check` yalnızca
**tazeliği** ölçer; üretici kod yanlışsa hiçbir şey yakalamaz.

## 14 · Validation Plan

**Asgari uygulanabilir set:** 2 toile (`T-1` + **kontrol** `T-1c`) +
3 yedek parça · tek vücut (kurucu) · **19 `VAL-xxxx` kaydı** · ≈4 m
prova kumaşı (**≈$15–30**) · **≈20–25 saat**.

| Kayıt | Yöntem | Kapsam |
|---|---|---|
| `VAL-0001`–`0004` | `Y-1` belirti üretme | Bölüm 11'in 6 belirtisinden ≥4'ü |
| `VAL-0005`–`0007` | `Y-2` ayırt edicilik | Çok nedenli ≥3 belirti |
| `VAL-0008`–`0016` | `Y-4` eleme kalemi | 9 kalemin tamamı |
| `VAL-0017`–`0018` | `Y-5` sıra kısıtı | 2 etkileşim |
| `VAL-0019` | `Y-3` ölçüm tekrarı | 7 ölçü × 3 tekrar |

**Maliyeti düşüren fikir:** sapmayı **taşıyan** vücut aramak yerine
**bilinen** bir sapmayı tek vücutta **üret** — ve çoğunu geri
dönülebilir biçimde (dikiş sökme, pili iğneleme, şerit ekleme). Bu,
"kaç toile" cevabını **20'den 2'ye** indirdi.

**Yeni sınır kaydedildi:** üretilmiş sapma ≠ doğal sapma (`R-06`).
**Eşik gevşetilmedi:** 19 kayıtta tek FAIL = %5,3 > %5 (`R-17`).

⚠ **Hiçbir sınama yapılmadı.** `VAL` kayıt sayısı: **0**.

## 15 · Differentiation Test

Protokolün **uygulanabilir olan her parçası** yazıldı: eleme ölçütleri ·
üç soruluk ön eleme · beş bulma kanalı · teşvik politikası · taraf
tutmayı azaltan dört kural · **oturum betiği** (söylenecek ve
söylenMEYECEK cümleler) · kayıt formu · pilot karşılaştırma
malzemesinin spesifikasyonu (Malzeme A: **≥3 belirti girişi**, 6–8
sayfa, markasız; Malzeme B: meşru nüsha, çoğaltılmaz).

**Yeni sonuç durumu: `INCONCLUSIVE`** (1–2 katılımcı). PASS değildir,
FAIL değildir; `measured` `false` kalır ve **kapı kapalı kalır**.
Faz 2 üretimi ve fiziksel sınama devam eder.

`aiProxyCountsAsHuman` **`false` kaldı**. Çelişmeli AI incelemesinin
izinli kullanımı (protokol eleştirisi, yönlendirici dil taraması,
başarısızlık senaryosu üretme) ve yasak kullanımı ayrı ayrı listelendi.

⚠ **Test yapılmadı. Katılımcı yok. Sahte bir PASS üretilmedi.**

## 16 · Risk Changes

| Risk | Değişiklik |
|---|---|
| `R-12` IP/marka | **Olasılık DÜŞÜK → ORTA–YÜKSEK** — somut çakışma bulundu |
| `R-04` teknik doğruluk | Şiddet aynı, **yeri belli oldu**: `C-C`/`C-D`/`C-H` |
| `R-09` format | Varsayım → **olgu**: KDP spiral sunmuyor |
| `R-06` fiziksel sınama | **Yeni sınır**: üretilmiş sapma ≠ doğal sapma |
| `R-14` kapı erozyonu | **Yeni erozyon yüzeyi**: `INCONCLUSIVE`'in "neredeyse PASS" gibi sunulması |
| `R-01` `R-02` `R-03` | **Değişmedi** — yeni kanıt yok |

**Eklenen dört risk:** `R-15` tek kaynak bağımlılığı (ease bandı tek
kaynağa dayanıyor) · `R-16` kaynak bağlantısı ölümü · `R-17` küçük
sınama setinin eşiği tetiklemesi · `R-18` dijital tamamlayıcının terk
edilmesi.

**Hiçbir risk silinmedi.**

## 17 · Remaining External Dependencies

| # | Bağımlılık | Kim | En geç | Engellediği |
|---|---|---|---|---|
| 1 | **Kitap 1 Faz 1 onayı** | Kurucu | — | Seri kapısı `series-architecture`; Kitap 1 kapısı `phase1-spec`; Faz 2'nin açılması |
| 2 | **`A15` — yerine geçen seri adı + profesyonel marka temizliği** | Kurucu + marka vekili | `phase2-visual` başlangıcı / kapak öncesi | Kapak, metadata, alan adı, tamamlayıcı |
| 3 | **`A14` — üç ev dikişçisi** | Kurucu | `phase3-pilot` | **Kill-gate ①** |
| 4 | **Fiziksel sınama (19 kayıt)** | Kurucu | `phase3-pilot` | **Kill-gate ②** |
| 5 | Rakip akış takibinin başlatılması | Kurucu | `phase2-visual` | `R-08` erken uyarısı |

**3 ve 4 depo içinden ölçülemez** ve ölçülmüş gibi kaydedilemez.

## 18 · QA Results

```
$ bash 06_BUILD/qa_all.sh
▸ validate_spec.py       ✓ 0 hata   (15 kaynak · 43 belirti · 19 aile · 32 ölçü · 148 crosswalk · 12 blok)
▸ validate_structure.py  ✓ 0 hata   (116 izlenen dosya)
▸ build_crosswalk --check ✓ güncel  (148 kayıt)
▸ qa_crosswalk.py        ✓ 0 bulgu  (dokuz denetim · 19/19 aile · 21 istisna)
▸ qa_boundary.py         ✓ 0 bulgu  (35 topik)
▸ qa_claims.py           ✓ 0 bulgu  (34 belge)
▸ qa_terminology.py      ✓ 0 bulgu  (30 belge · 20 terim)
▸ selftest.py            ✓ 91/91 denetim
✓ BÜTÜN KAPILAR GEÇTİ
```

**Kill-gate — BEKLENEN biçimde bloklu:**

```
$ python3 06_BUILD/kill_gate.py --book book-01
  ✗ 2 engel:
    - differentiationTest: HENÜZ ÖLÇÜLMEDİ (measured=false)
    - physicalValidation:  HENÜZ ÖLÇÜLMEDİ (measured=false)
  → SONUÇ: Faz 4 AÇILAMAZ.
```

**Kapı sisteminde bu turda değişen:** yeni kapı `qa_crosswalk.py`;
selftest 77 → **91** denetim; `test_verification_status_is_honestly_recorded`
yeniden yazıldı; `test_verification_summary_matches_records` eklendi;
`REQUIRED_SERIES_DOCS` dört belge genişledi.

⚠ **Düzeltme:** `ROADMAP_PROGRESS.md` kill-gate satırında "4 engel"
yazıyordu; `kill_gate.py` hem şimdi hem de o günkü commit'te **2 engel**
raporluyor. Sayı düzeltildi ve `K33` olarak kaydedildi.

## 19 · Git / CI Status

| | |
|---|---|
| Depo | `github.com/emredogan-cloud/sewing-pattern-fitting-series` |
| Görünürlük | **public** |
| Depo adı | **marka-nötr** — `A1` kapanmadan hiçbir ad kamuya taahhüt edilmedi (`K32`) |
| Dal | `master` |
| İzlenen dosya | **139** |
| CI koşusu | `33193615969` — **başarılı**, 22 sn |
| CI işleri | **7/7 geçti**: kapı seviyeleri · şema/bütünlük/kaynak · depo/koruma/marka · crosswalk tazeliği + bütünlüğü · kitap sınırı · iddia + terminoloji · **kapıların kendi testi** |
| `kill-gate` işi | ✗ **tasarım gereği başarısız** (`continue-on-error: true`) — iş akışı bunu kendi notunda ilan eder |
| Düzeltilen CI sorunu | İlk koşuda "Node.js 20 kullanımdan kaldırıldı" anotasyonu çıktı; eylem sürümleri yükseltildi (checkout v4→v5, setup-python v5→v6, upload-artifact v4→v5) ve ikinci koşu **anotasyonsuz** yeşil döndü |

**Korumalı dizin denetimi — GitHub üzerinde doğrulandı:**
`01_SOURCE/reference_material`, `02_TAXONOMY/protected`,
`BOOK-01/02_CONTENT/protected`, `BOOK-01/04_EDITORIAL/pilot` ve
`09_OUTPUT` dizinlerinin **hepsi yalnızca `.gitkeep` içeriyor.**

**Bilerek dışarıda bırakılan:** yayın-öncesi tam proza ve pilot metni ·
fiziksel sınama fotoğrafları (gerçek insan bedeni) · **fark testi
katılımcı verisi** (yeni) · telif korumalı referans malzeme ve satın
alınmış ticari kalıplar · **indirilmiş kaynak PDF'leri** (yeni) ·
üretilmiş nihai diyagram varlıkları ve yayın dosyaları · sırlar,
anahtarlar, yerel önbellek.

**Yayımlanan:** kod · CI · şema · doğrulayıcı · politika ve
spesifikasyon belgeleri · taksonomi **metadatası** · kaynak
**KAYITLARI (künye)** · görsel notasyon sözlüğü · faz raporları.

Hassas içerik taraması (e-posta, mutlak yerel yol, token/anahtar
deseni, telefon) **temiz** döndü.

## 20 · Phase 2 Readiness

**Faz 2 AÇILMADI ve bu turda açılmayacaktır.** Kurucu onayı olmadan
`phase2-visual` başlamaz.

Faz 2'ye hazır olan girdiler:

| Girdi | Durum |
|---|---|
| Altı kurucu kararı (`A1` `A4` `A6` `A7` `A8` `A11`) | **Beşi kapandı**; `A1` yerine `A15` dış beklemede |
| Renk kararı → token kalibrasyonu girdisi | ✓ |
| Yazı tipi kararı → sayfa geometrisi girdisi | ✓ + altı test tanımlı |
| Birim kararı → her ölçüm figürünün etiketi | ✓ |
| Bölüm bazlı **karar noktaları** → akış şemalarının düğümleri | ✓ (18 bölüm) |
| Ölçü doğrulama sınıfları → figür uyarı katmanı | ✓ (16/7/9) |
| Yeni ölçüm eşikleri (`color_required` %10, `photo_required` 6) | ✓ |
| Ücretsiz kaynak edinimi (TAMU serisi, USDA 1945, MSU) | ✓ görev listesinde |
| Rakip akış takibi (`G7`) | ✓ görev listesinde |

**Faz 2'nin yapmayacağı:** manüskript · pilot · fiziksel sınama · fark
testi · kapak · KDP dosyası · reklam.

---

## Sınırlamalar — bu raporun iddia ETMEDİĞİ

1. **Hiçbir teknik iddia fiziksel olarak sınanmadı.** `VAL` kayıt
   sayısı 0.
2. **43 belirti ve 129 ayırt edici kanıt doğrulanmadı.**
3. **Fark testi yapılmadı.** Hipotez `D1` hâlâ hipotezdir.
4. **Marka taraması bir temizlik araştırması değildir.** Bulunanlar
   `OBSERVED`; bulunmayanlar yokluk kanıtı değildir.
5. **KDP rakamları `marketplace_observation`'dır**, teknik otorite
   değildir ve `phase6-format` kapısının yerine geçmez.
6. **Okur tanımı hâlâ araştırma raporundan devralınmıştır**; bu depoda
   bağımsız olarak doğrulanmadı.
7. **Bu turda hiçbir bağımsız çelişmeli inceleme turu yapılmadı** —
   `PHASE_2_ADVERSARIAL_REVIEW.md` Faz 2'nin çıktısıdır.

---

*Vâliçe Press · TRUE FIT · Phase 1 Execution Report · 28 Ağustos 2026*
