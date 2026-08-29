# PHASE 4 — YÜRÜTME RAPORU

> Kitap 1 · *Measure & Diagnose* · 29 Ağustos 2026
>
> **Bu raporun her sayısı, onu üreten komutun çıktısından alınmıştır**
> (`DECISIONS.md K33`). Hatırlanan hiçbir değer yoktur.

---

## 1 · Faz 4 özeti

Kitap 1'in **tam manüskripti üretildi**: 252 sayfa, 21 bölüm, 42 224
kelime, 160 figür. Aynı turda dört hatlı bir **bağımsız teknik inceleme**
yürütüldü ve **149 bulgu** üretti; bulguların **132'si revizyon gerektirdi**
ve revizyonlar uygulandı.

Fazın en önemli tek cümlesi şudur: **incelenen 149 iddiadan yalnızca
biri — `CC-02`, "belirti ≠ neden" — değişmeden ayakta kaldı.** Kitabın
tezi doğrulandı; ayrıntılarının çoğu doğrulanmadı ve düzeltildi.

## 2 · Kurucu geçersiz kılması

Yol haritası P4'ü P3'ün **PASS**'ine bağlar. Kurucu, P3'ün iki dış
ölçümünü beklemeden üretimin sürmesine izin verdi ve aynı talimatta
eksik sonuçların PASS yazılmasını **açıkça yasakladı**.

İkisi birlikte kaydedildi (`DECISIONS.md K49`). `BOOK_GATE_ORDER`'a
`phase4-production-conditional` eklendi ve kümülatif sırada
`phase3-pilot`'ın **ÖNÜNE** konuldu:

| Sorgu | Sonuç |
|---|---|
| `gate_at_least(g, "phase2-visual")` | **doğru** — Faz 2 bitti |
| `gate_at_least(g, "phase3-pilot")` | **YANLIŞ** — kill-gate ölçülmedi |
| `gate_at_least(g, "phase5-qa")` | **YANLIŞ** — P5 bu yoldan açılamaz |

`kill_gate.py --book book-01` hâlâ **iki engel** raporluyor ve
"Faz 4 AÇILAMAZ" diyor. Bu bir çelişki değil, istenen durumdur: üretim
ekseni ilerledi, doğrulama ekseni ilerlemedi.

Regresyon: `selftest.py § test_conditional_phase4_does_not_claim_kill_gate`
— kapı sırası bozulursa ya da bir kill-gate bayrağı açılırsa test kırılır.

## 3 · Üretilen içerik

| Ölçüt | Değer |
|---|---:|
| Sayfa | **252** (hedef bandı 220–260) |
| Bölüm (Parça 0 + 18 bölüm + ekler + atlas ayrımı) | **21** |
| Kelime | **42 224** |
| Bölge atlası | **176 sayfa** (kitabın %76'sı) |
| Belirti girişi | **43 / 43** |
| Kullanılan ayrı figür | **159 / 159** yerleştirilebilir figürün tamamı |
| Figür yerleşimi | **175** |
| Bölüm açılışı boş versosu | 13 — hiçbiri numara taşımıyor |

**Mimari karar (`K50`):** Bölüm 2 (32 ölçü) ve bölge atlası (43 giriş)
**üretilir**; Bölüm 1, 3–8, 16–18, Parça 0 ve ekler **yazılır**.

Gerekçe: o iki bölümün iç yapısı bir spesifikasyondur. 43 giriş elle
yazılsaydı er geç biri "henüz değiştirme" uyarısını ya da yeniden
gözlem adımını taşımazdı ve **hiçbir kapı bunu göremezdi** — bir kapı,
metinde hiç olmayan bir bölümü arayamaz. Üretilen bir yapıda eksik alan
**derlenmez**.

**Dizgi (`K51`):** Faz 3'te dizgi kodu `build_pilot.py`'nin içindeydi.
Kopyalamak iki dizgi yolu yaratırdı ve pilotun 8 sayfası ile kitabın
aynı bölümü farklı dizilebilirdi — fark testi (`D-01`) karşılaştırılamaz
hâle gelirdi. Kod `06_BUILD/typeset.py`'ye çıkarıldı. **Kanıt: pilot
çıktısı değişmedi — 8 sayfa, 7 figür.**

## 4 · Teknik doğrulama

`06_BUILD/build_claims.py` **307 iddia** üretti. Kanıt seviyesi
**beyan değil türevdir**: taksonomi kaydının `verification_status`'ünden
ve atıf yaptığı kaynakların otoritesinden hesaplanır.

| Seviye | Sayı | Oran |
|---|---:|---:|
| `VERIFIED` | 56 | %18,2 |
| `CONTESTED` | 8 | %2,6 |
| `INFERRED` | 214 | %69,7 |
| `UNVERIFIED` | 29 | %9,4 |

`INFERRED`'ın çoğunluk olması **gizlenmedi ve düzeltilmedi**. Kitabın
129 nedensel ilişkisi kamu kaynaklarında tek tek doğrulanamaz; Faz 1
bunu kaydetti, Faz 4 değiştirmedi. Kitabın buna verdiği cevap her
girişte bir **cevap değil bir fiziksel test** sunmaktır.

İzlenebilirlik: `00_SPEC/CLAIM_SOURCE_MAP.md` (üretilen) ·
**204/204 maddi iddia** dizilen metinden izleniyor
(`qa_manuscript § ⑪`).

## 5 · Bağımsız inceleme bulguları

Dört hat, birincil üretimden ayrı çalıştırıldı. Hiçbirine kendini
onaylama yetkisi verilmedi.

| Hat | Bulgu | Kaynak |
|---|---:|---:|
| Ölçü tanımları ve işaret noktaları | 37 | 18 |
| Ease, beden seçimi, düzeltme aileleri | 32 | 17 |
| Teşhis mantığı ve belirti→neden | 66 | 22 |
| Prova protokolü, karıştırıcılar, sıra | 14 | 23 |
| **Toplam** | **149** | **68** |

| Sonuç | Sayı |
|---|---:|
| `CONTRADICTED` | **56** |
| `CONTESTED` | 14 |
| `UNSUPPORTED` | 10 |
| `SUPPORTED_NARROWER` | 40 |
| `SUPPORTED` | 29 |

**En ciddi altı bulgu:**

1. **`AF-20` karın hacmi ailesi YOKTU.** 19 ailede karın yoktu ve
   crosswalk beş kaydı karın nedenlerini ya `AF-13`'e (giysinin ARKASI)
   ya da `AF-01`'e (**göğüs pensi ailesi**) yönlendiriyordu. Karnı
   çıkık bir okur göğüs düzeltmesine gönderiliyordu. Aile eklendi,
   yollar düzeltildi, 20/20 aileye ulaşılıyor.

2. **`CC-21` bir mantık hatasıydı.** "Belirti azaldı ama gitmediyse
   ikinci bir neden vardır" iddiasının hiçbir kaynağı yoktu ve yanlıştı:
   kısmi iyileşme en az o kadar sık **doğru nedenin yetersiz
   düzeltilmesidir**. Yanlış hâliyle okuru olmayan bir ikinci nedenin
   peşine gönderirdi. 43 girişin tamamında **yapısal** olarak düzeltildi.

3. **`M-015` iki ayrı ölçünün birleştirilmesiydi** ve kaynağın kendi
   yöntemi "sık yapılan hata" diye listelenmişti. Sonuç `M-032`'yi —
   kitabın denge sayısını — bozuyordu: aynı duruşta farklı göğüs
   hacmine sahip iki okur farklı "denge" okuyordu.

4. **`T-10` / `M-001` üst göğüs yolu yanlıştı.** "Kolların ÜSTÜNDEN"
   yazıyordu; doğrusu **kolların ALTINDAN**. Şerit deltoidlerin üzerinden
   geçerse üst göğüs büyük okunur, göğüs−üst göğüs farkı küçülür ve
   **beden seçimi kararı yanlış dala gider**.

5. **`CC-20` kendi verisiyle çelişiyordu.** Kural kesmeyi yasaklıyor,
   129 fiziksel testin **17'si ilk adımda kesiyordu** — üçü, `SYM-001`'in
   kendi uyarısının "geri eklenemez" dediği yakayı. Ayrım netleştirildi:
   **toile kesilir, KALIP ve KENAR kesilmez.**

6. **`S-0004` iki çekirdek kuralı içermiyordu.** Belge 43 belirtinin
   tamamında kaynak olarak duruyordu. Tam metin (8 sayfa) okundu: uyum
   içeriği tek sayfada beş maddedir. `CC-23` ve `CC-26` birebir vardır;
   `CC-22` (kıvrım ekseni), `CC-24` (çekme çizgisi) ve `CC-29` (etek ucu
   türevdir) **yoktur**. Atıflar kaldırıldı.

**Ayrıca:** `interacts_with`'te altı tek yönlü kenar (Faz 3'ün `B-01`
cevabı buna dayanıyordu) · karıştırıcı sayısında 9-11 çelişkisi
(üç spesifikasyon belgesi dokuz, veri on bir diyordu) · `AF-19` dosyanın
en yüksek notunu metninde geçmeyen bir atıfla taşıyor · `CC-25`'in
kendi kuralı veride ters uygulanmış.

## 6 · Web kanıtı

**68 tekil kaynak** danışıldı. Kullanılan kaynak sınıfları: standart
kuruluşları (`ISO 8559-1:2017`, `ASTM D5219`), devlet antropometri
araştırmaları (`ANSUR II`, `NHANES`), üniversite eğitim yayınları
(NMSU, Texas A&M AgriLife, WSU), kalıp yayıncılarının kendi resmî uyum
kılavuzları ve tanınmış uygulayıcı kaynakları.

İncelemeciler **ulaşamadıklarını da kaydetti**: bir standart ders
kitabı, birkaç dergi makalesi ve bir eğitim yayını erişim engeline
takıldı. Bu kayıtlar rapor § 6'da durur.

**Bir incelemeci kendi hatasını düzeltti ve bu kayıtlıdır:** `S-0004`'ü
önce "edinilemez" diye raporladı, sonra edindi ve *"düzeltiyorum;
gerçek bulgu daha kötü, çünkü denetlenebilir"* diye yazdı.

## 7 · Değişen iddialar

**23 kavramsal iddia** (31'den) bağımsız inceleme sonucunda yeniden
yazıldı. Hepsi `CONCEPTUAL_CLAIMS.json`'da `phase4_review` alanı taşır
ve `CLAIM_SOURCE_MAP.md § 6`'da listelenir.

Taksonomi düzeyinde değişenler: `AF-13` (kapsam), `AF-15`/`AF-16`
(sınır), `AF-18` (ad + sıra kısıtı), `AF-19` (not düşürüldü), `AF-05`,
`AF-07` (sıra notu), `M-001`, `M-004`, `M-008`, `M-013`, `M-015`
(tanım), `T-05`, `T-10` (terim), 32 ölçüde `helper_required`, dört
karıştırıcı sınıfı eklendi.

## 8 · Kaldırılan iddialar

Hiçbir iddia **sessizce** kaldırılmadı. Kaldırılan **atıflardır**:

- `S-0004` → `CC-22`, `CC-24`, `CC-29` (belge içermiyor)
- `S-0003` → sekiz ölçünün işaret noktası tanımı (belge tanım içermiyor;
  atıf **bağlam** olarak yeniden etiketlendi)
- `S-0001` → `AF-19` (metinde ilgili terimler geçmiyor)

İlgili iddialar **korundu ama kaynaksız olduklarını beyan ederek**.
Bölüm 7 artık açıkça şunu yazıyor: *"bu bir geometrik türetmedir; bu
kitap onu kurumsal bir kaynakta bulmadı."*

## 9 · Görsel üretim özeti

| Ölçüt | Faz 2 | **Faz 4** |
|---|---:|---:|
| Toplam figür | 154 | **163** |
| Deterministik | 105 (%68,2) | **114 (%69,9)** |
| Akış şeması | 46 | **47** |
| Tablo grafiği | 9 | **15** |
| Kitapta kullanılan | — | **159 / 159** |

**Dokuz figür Faz 4'te eklendi** ve hepsi `CHAPTER_SPECS`'te yazılıydı
ama hiçbiri taksonomi kaydından türetilemezdi — karşılıkları bir kayıt
değil bir **bölümdü**: üç sayı tablosu, yedi adımlı döngü şeması, on
belirti sınıfı tablosu, eleme kontrol listesi ve üç boş form.

**Vücut varyantları (`B-05` kapatıldı):** `croquis.py` üç varyant taşıyor
(düz sırt, yuvarlak sırt, dolgun göğüs). Varyant **elle atanmaz,
veriden türetilir**: bir belirtinin nedeni bir vücut farkıysa o varyant
kullanılır. Ölçüm: 43 belirti figürünün **26'sı** standart-dışı bir
gövde kullanıyor (dolgun göğüs 11 · yuvarlak sırt 9 · düz sırt 6);
kalan 17'nin nedeni bir vücut farkı değildir (yapım, kumaş, beden).
`qa_visual § ⑪` en az iki varyantın gerçekten kullanıldığını denetler.

## 10 · Kod ve dış görsel kararı

**Karar: 163 figürün 161'i KOD ile üretildi. Dış görsel aracı
KULLANILMADI.**

Kurucu talimatı § 17–21 dış üretimi *"profesyonel kaliteyi maddi olarak
artırdığı yerde"* yetkilendirdi. Karar çerçevesi (§ 18) uygulandı:

| Figür sınıfı | Sınıf | Gerekçe |
|---|---|---|
| Ölçüm yolu (29) | **A — KOD** | § 19 doğrudan kapsıyor: ölçü, etiket, geometri. Dış üretim burada **yasak**. |
| Kalıp parçası (8) | **A — KOD** | § 19: kalıp konturu, dikiş çizgisi, ölçek beyanı. |
| Akış şeması (47) | **A — KOD** | Kayıt verisinden türetiliyor; elle çizim taksonomi ile ayrışırdı. |
| Tablo (15) | **A — KOD** | Veri tek kaynaktan; dizgi metin ızgarasında. |
| İşaret noktası (7) | **A — KOD** | § 19. |
| Belirti figürü (43) | **B adayı — KOD kaldı** | Aşağıya bakınız. |
| Toile durumu (6) | **B adayı — KOD kaldı** | Aşağıya bakınız. |

**Belirti ve toile figürleri neden dışarı verilmedi.** Bunlar tam da
§ 20'nin izin verdiği sınıftır: kumaş dökümü, kırışık görünümü. Ve
çelişmeli inceleme `B-04` bu figürlerin zayıflığını zaten kaydetmişti —
43'ü de aynı şablondan geliyor ve gerçek kumaş dökümü yok.

Yine de dış üretim **reddedildi**, üç ölçülebilir sebeple:

1. **Doğrulanacak bir referans yok.** Bir kırışığın nasıl düştüğü
   `D-02`'de ölçülecek. Bugün üretilecek "gerçekçi" bir görsel,
   doğrulanmamış bir geometriyi **inandırıcı** kılardı — `RISK_REGISTER
   R-06`'nın tam tanımı. Kaba bir şematik yanlış olduğunda yanlış
   görünür; gerçekçi bir görsel yanlış olduğunda **doğru görünür**.
2. **Uzman elle doğrulama yok.** § 19 dış sonucun bir uzmanca
   doğrulanmasını şart koşuyor. Bu projede dış uzman **işe alınmayacak**
   (`K6`). Şart karşılanamaz.
3. **Deterministiklik kaybı ölçülür.** Bugün %69,6 olan deterministik
   oran, 49 figür dışarı verilirse **%39,1'e** düşerdi ve `figures.json`
   sicili ile sayfa arasındaki bağ kopardı.

**Karar `D-02`'den SONRA yeniden değerlendirilecektir** ve o noktada
doğru sınıf muhtemelen **B (kod + elle rötuş)** olacaktır: fiziksel
sınama gerçek kıvrımın nerede ve ne kadar olduğunu ölçtükten sonra,
şablon o ölçüme göre düzeltilebilir.

## 11 · Görsel kalite bulguları

Otomatik kapılar yeşilken **gözle bakılarak** iki kusur bulundu — bu,
`R-19`'un Faz 4'teki tekrarıdır ve kaydedilmesi gerekir:

1. **Boş sayfalar folyo taşıyordu.** Bölüm açılışları tek sayfada
   başlar ve 13 boş verso üretir. Yayıncılık konvansiyonu: boş sayfa
   **sayılır ama numaralanmaz**. Dizgi motoru sayfa mobilyasını
   **açılışta** yazıyordu; **kapanışa** taşındı ve sayfa "kirli" değilse
   yazılmıyor.
2. **Bölüm kicker'ı başlıkla çakışıyordu.** 9 pt "CHAPTER 6" ile 20 pt
   başlık arasındaki boşluk 12,3 pt idi — 20 pt harf yüksekliğinin
   **altında**. Hiçbir otomatik kapı iki metin bloğunun çakıştığını
   görmüyor.

Ayrıca `flow_CYCLE` şemasının geri dönüş etiketi figür kutusunun dışına
taşıyordu; kutu genişletildi.

**Ders değişmedi:** kapılar sormadıkları soruyu yakalayamaz. Faz 5'te
sayfa örneklemi yine **gözle** incelenmelidir.

## 12 · Sayfa sayısı

**252 sayfa** · hedef bandı **220–260** · `build_book.py` her koşumda
denetliyor ve bant dışında **çıkış kodu 1** veriyor.

Çelişmeli inceleme `B-08` bölge atlası için **100 sayfa** kısıtı
yazmıştı. Atlas **176 sayfa** çıktı ve kısıt **aşıldı**.

Önce kapsam daraltıldı: 43 girişte tekrar eden dört blok ölçülerek
kesildi ve atlas **127 → 115 sayfa**ya indi. Bu, `B-09`'un (işlevsel
tekrar) ölçülmüş maliyetidir: **12 sayfa**.

Sonra kapsam **bilinçli olarak büyüdü**, çünkü aynı incelemenin diğer
kısıtları yer tutuyor: `B-01` yeniden gözlem (43 × 2 paragraf), `B-03`
belirtiye özgü eleme (43 × 3 satır), `CC-25` kapı-önce sunum, **28 kanıt
çakışması beyanı** ve ilk dizgide **hiç yer almadığı ölçülen 29 ölçüm
figürü** (+25 sayfa).

`B-08`'in 100 sayfalık rakamı, bu eklerin zorunlu olacağı bilinmeden
yapılmış doğrusal bir tahmindi. **Kısıtın koruduğu gerçek şey** 300
sayfada değişen cilt payıdır; 252 o bandın rahatça içindedir.

## 13 · Figür sayısı

**163 figür** · kitapta **159**'i kullanıldı · **3'ü iç araçtır ve
kitaba giremez** (`build_book` ve `qa_manuscript` bunu denetler).

Faz 2'nin 154'ü **final değildi** ve talimat § 25 bunu doğru öngörmüştü.
Dokuz figür eklendi. Kullanım oranı **%100**: yerleştirilebilir hiçbir
figür kitap dışında kalmadı.

## 14 · KA sonuçları

`bash 06_BUILD/qa_all.sh` → **BÜTÜN KAPILAR GEÇTİ**

| Kapı | Sonuç |
|---|---|
| `validate_spec.py` | ✓ 0 hata — 18 kaynak · 43 belirti · **20 aile** · 32 ölçü · 148 crosswalk · **163 figür** |
| `validate_structure.py` | ✓ 0 hata — **193 izlenen dosya** |
| `build_crosswalk.py --check` | ✓ güncel (148) |
| `qa_crosswalk.py` | ✓ 0 bulgu — **20/20** aileye ulaşılıyor |
| `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| `qa_claims.py` | ✓ 0 bulgu (42 belge) |
| `qa_terminology.py` | ✓ 0 bulgu (31 belge) |
| `qa_visual.py` | ✓ 0 bulgu — **on dört denetim** |
| `build_claims.py --check` | ✓ güncel (**307 iddia**) |
| `build_claim_map.py --check` | ✓ güncel |
| **`qa_manuscript.py`** *(yeni)* | ✓ **0 bulgu — on bir denetim** |
| `selftest.py` | ✓ **152/152** *(önceki tur 116)* |
| `fetch_fonts.py --verify` | ✓ 10 dosya SHA-256 |
| **`build_book.py`** *(yeni)* | ✓ **252 sayfa**, bütçe içinde |
| `selftest_visual.py` | ✓ 27/27 |
| `kill_gate.py` | ✗ **2 engel — BEKLENEN VE DOĞRU** |

**Temiz klon doğrulaması yapıldı** ve bir kusur buldu:
`CLAIM_SOURCE_MAP.md` bayattı ve `qa_all.sh` bunu denetlemiyordu.
Denetim eklendi.

## 15 · İkinci çelişmeli inceleme

Bitmiş manüskript üzerinde, **34 sayfa görüntü olarak incelenerek** ve
üç okur yolculuğu uçtan uca yürünerek yapıldı. Birinci turdan ve içerik
üretiminden AYRI bir incelemedir.

| | |
|---|---:|
| Bulgu | **36** |
| `CRITICAL` | 5 |
| `HIGH` | 16 |
| `MEDIUM` | 13 |
| `LOW` | 2 |
| Kırılamayan saldırı | 12 |
| Okur yolculuğu | 3 — **1 başarılı · 1 çıkmaz · 1 takıldı** |

**İncelemenin hükmü, kendi cümlesiyle:** *"Bu, şu hâliyle profesyonel
bir yayın gibi okunmuyor — altındaki yöntem tür normundan iyi, ama
ürünün görünmez sayfaları var, içeri girecek kapısı yok ve pantolon
okurunu yanlış düzeltme ailesine yolluyor."*

### Doğrulanan ve düzeltilenler

| Bulgu | Ne yapıldı |
|---|---|
| **`A-04` ağ UZUNLUĞU nedenleri ağ DERİNLİĞİ ailesine gidiyor** | **DOĞRULANDI — ve bu turun kendi regresyonuydu.** `AF-15`/`AF-16` sınırı ayrıldığında aileler yeniden adlandırılmış, nedenler yeniden yönlendirilmemişti. Kitabın 4. sıra kuralı bu karışıklığı "en sık yapılan pantolon hatası" diye adlandırıyor ve veri onu ÜRETİYORDU. Dördü de düzeltildi + `validate_spec` kapısı eklendi (kapı ilk yazımda SESSİZCE ÇALIŞMIYORDU; kusurlu fixture yakaladı) |
| **`A-02` 43 şema kitapta olmayan bir "zone chart"a çıkıyor** | **DOĞRULANDI.** "zone" kelimesi kitabın başka hiçbir yerinde geçmiyordu. Çıkış artık Ek C'deki belirti dizinini adlandırıyor |
| **`A-03` Ek H hiçbir şey basmıyor** | **DOĞRULANDI.** 20 aile, her birine hangi sayfalardan ulaşıldığıyla birlikte ÜRETİLİYOR |
| **`A-05` içindekiler, dizin, sayfa numarası, PDF ana hattı yok** | **DOĞRULANDI.** İki geçişli dizgi kuruldu: içindekiler + PDF ana hattı + ~45 çapraz atıfa sayfa numarası + Ek C belirti dizini. Sayfa numaraları YAKINSAYANA kadar tekrarlanıyor |
| **129 testin 105'i sonucu okuma ölçütü taşımıyor** | **DOĞRULANDI ve ölçüldü.** Ölçüt uydurulmadı — belirtinin KENDİ gözlem cümlesinden türetiliyor ve her nedene bağlanıyor |
| **`A-07`/`A-33` profil formu kendi zorunlu alan listesiyle uyuşmuyor** | **DOĞRULANDI.** Yön ve tarih sütunları eklendi; iki karşıt nedeni tek aileye yollayan **8 belirtiye** açık uyarı eklendi |
| **`A-15` Ek G kendi kitabı hakkında yanlış** | **DOĞRULANDI.** İki yanlış iddia düzeltildi |
| **`A-21` kaynak listesi yok** | **DOĞRULANDI.** Ek I eklendi, kaynak KAYITLARINDAN üretiliyor |
| Boş form satırları yazılamayacak kadar dar | **DOĞRULANDI.** 15,3 → 26 pt |
| Yan not taşması | **LATENT KUSUR DOĞRULANDI.** Aynı sayfadaki ikinci not birincinin üzerine yazabiliyordu; notlar artık yığılıyor |
| Okur yolculuğu (b) çıkmaz — yan dikiş çelişkisi | **DOĞRULANDI.** Aynı sayfada "yan dikişi açma" ve "yan dikişleri aç" vardı; ayrım metne yazıldı |
| Okur yolculuğu (c) — üç hacim, tek aile | **DOĞRULANDI.** Önce hacmi ADLANDIR adımı eklendi |

### Doğrulanmayan bulgu

**`A-01` — "iki sayfa metin taşıyor ama hiç mürekkep basmıyor" (CRITICAL).**

Denetlendi ve **o hâliyle doğru değil**. 252 sayfanın tamamı 40 dpi'de
rasterleştirildi ve metin katmanıyla karşılaştırıldı: **metni olup
mürekkebi olmayan sayfa YOK.** Mürekkepsiz 15 sayfanın hepsi bölüm
açılışı versosudur, metinleri de yoktur ve numara taşımazlar — yayıncılık
konvansiyonu. İncelemeci muhtemelen bu turda birkaç kez yeniden derlenen
kitabın FARKLI sürümlerine baktı.

**Ama denetim kaldı.** `build_book.py` artık her sayfayı rasterleştiriyor
ve metni olup basılmayan bir sayfa bulursa çıkış kodu 1 veriyor. *İddia
yanlış çıktı; sorduğu soru doğruydu.*

### Bulgu tablosu

| # | Şiddet | Alan | Gözlem |
|---|---|---|---|
| `A-01` | CRITICAL | typography | Pages 128 and 200 render as pure white — not one non-white pixel anywhere on the sheet, not even the folio number — yet both pages carry real, extract |
| `A-02` | CRITICAL | reader_journey | Every one of the 43 diagnostic flowcharts ends its failure branch with the terminal box 'Not this sign — go back to the zone chart'. The string 'zone  |
| `A-03` | CRITICAL | boundary | Page 230, the last page of the book, prints: 'Appendix H — Where each region leads. Every diagnosis in this book ends by naming an adjustment family.  |
| `A-04` | CRITICAL | contradiction | Four candidate causes that are explicitly about crotch LENGTH are routed to the crotch DEPTH family: SYM-027.C2 'Not enough crotch length (in trousers |
| `A-05` | CRITICAL | missing | The book has no table of contents, no index, no title page, no copyright page, no ISBN, no bibliography and no glossary. Page 1 is 'BEFORE YOU START / |
| `A-06` | HIGH | certainty | Of the 129 'Test:' instructions in the atlas, 112 (87%) give an action with no criterion for reading the result. Examples in full: 'Test: Lower the sh |
| `A-07` | HIGH | boundary | The fit profile — the book's deliverable — has no direction field. Page 221 lists 'What each entry needs': the adjustment family by name, the amount a |
| `A-08` | HIGH | typography | The six 'shown wrong and right side by side' figures on pages 41-43 show identical drawings on both sides. I cropped and inspected the 'Tape slipped d |
| `A-09` | HIGH | contradiction | Two different chapters are both numbered 16. Page 203 opens 'CHAPTER 16 / The order of work'. Page 207 opens 'CHAPTER 16 / Signs that belong to the wh |
| `A-10` | HIGH | typography | All three blank forms have collapsed rows. On page 43 the measurement card prints a header row (Measurement / First reading / Second reading / Differe |
| `A-11` | HIGH | typography | Side-note titles overflow the margin column and print on top of the body text. Page 70: the title 'What would have happened without step 7' overprints |
| `A-12` | HIGH | certainty | The 'THESE TWO CAN LOOK THE SAME' box directly contradicts the 'Tells it apart' fields printed immediately above it, in all 28 instances. On page 131  |
| `A-13` | HIGH | contradiction | For size-choice causes the prose and the flowchart give opposite answers. In the prose, five causes carry the exit line 'This is not an adjustment. It |
| `A-14` | HIGH | contradiction | On page 166 the book instructs and then forbids the same action within six lines. Cause 3 of SYM-027 ends '— Test: Let both side seams out.' Immediate |
| `A-15` | HIGH | certainty | Appendix G, the appendix whose job is to state where the evidence stands, makes two false claims about the book. (1) 'The four disagreements it record |
| `A-16` | HIGH | typography | Throughout Chapter 2 (pages 10-39) every measurement's figure lands on the page AFTER its text, at the top of the page, directly above the NEXT measur |
| `A-17` | HIGH | boundary | Twelve 'Test' instructions are pattern-alteration operations, not diagnostic tests on a toile: 'Shorten or lengthen the bodice at the lengthen/shorten |
| `A-18` | HIGH | contradiction | Chapter 8's list of the fourteen rule-out items does not match the checklist it is a commentary on. The flowchart (pages 80-81) and Appendix D (page 2 |
| `A-19` | HIGH | typography | The 'Where it comes from' side note routinely lands at the top of a page beside the PREVIOUS entry's flowchart, hundreds of points above the entry it  |
| `A-20` | HIGH | typography | Page 44 contains one line of text — the italic caption 'The measurement card. Two readings, and the difference between them.' — and nothing else. The  |
| `A-21` | HIGH | missing | The book has no source list. Appendix G rests the book's credibility on 'published institutional sources' and says 'where those sources disagree with  |
| `A-22` | MEDIUM | repetition | 27.1% of the atlas is verbatim boilerplate. Measuring pages 85-219 (30,402 words) against 23 exact repeated strings: 8,246 words, or roughly 192 of th |
| `A-23` | MEDIUM | contradiction | Three figures carry a 'Sources differ' flag for measurements the book records no disagreement about. The annotation 'Sources differ — see the note in  |
| `A-24` | MEDIUM | typography | The measurement croquis has no arms, so the arm measurements cannot be drawn, and the caption on each claims the opposite. On page 17 the Bicep figure |
| `A-25` | MEDIUM | typography | Headings that wrap to two lines are set with near-zero leading and leave one-word runt lines. Page 110: 'A horizontal fold of excess fabric crosses th |
| `A-26` | MEDIUM | typography | Whitespace discipline is poor across the whole book. Measured over all 230 pages with the folio band excluded, 48 pages (21%) have their last mark of  |
| `A-27` | MEDIUM | reader_journey | Flowchart outcome text is truncated. On page 218 the third terminal box reads 'NOT a pattern problem — The hem allowance was turned differently than t |
| `A-28` | MEDIUM | typography | Several pattern-schematic figures show none of what their captions describe. Page 205: 'The skirt back. Waist shaping and seat volume are read on this |
| `A-29` | MEDIUM | contradiction | Appendix A and Appendix C do not deliver what their headings promise. Appendix A is headed 'Measurement reference' and says 'This appendix gives the i |
| `A-30` | MEDIUM | contradiction | Two near-identical entries live in different chapters with no cross-reference between them. SYM-027 'Horizontal drag lines cross the seat' is in Chapt |
| `A-31` | MEDIUM | repetition | The same 14-item rule-out checklist is printed three times in full: as a two-page flowchart on pages 80-81 in which all fourteen 'No' branches point a |
| `A-32` | MEDIUM | contradiction | The default working order on page 204 has five rows — Shoulder and neck, Bust, Waist, Hip and crotch, Sleeve — and omits the armhole entirely, along w |
| `A-33` | MEDIUM | contradiction | Page 221 lists five things every profile entry needs, ending with 'The date' and 'Which pattern it was confirmed on, and which company made it'. The b |
| `A-34` | MEDIUM | contradiction | Spelling of the same term is inconsistent, split along a chapter boundary. 'centre back' appears 47 times and 'centre front' 18 times, but Chapter 2's |
| `A-35` | LOW | contradiction | Page 203 heads a section 'Four rules that are settled' and lists four, then heads the next 'One rule that is contested' and describes the top-down heu |
| `A-36` | LOW | missing | PDF production hygiene. Document metadata reads Title 'untitled', Subject 'unspecified', Author 'anonymous', Creator 'anonymous'; Producer is 'ReportL |

## 16 · Kalan dış doğrulama

**HİÇBİRİ YAPILMADI. HİÇBİRİ PASS YAZILMADI.**

| # | Bekleyen | Durum | Engelleyici mi |
|---|---|---|---|
| `D-01` | Fark testi — üç ev dikişçisi | `measured: false` · 0/3 katılımcı | **EVET** |
| `D-02` | Fiziksel doğrulama — **28** `VAL` kaydı | `measured: false` · 0/28 | **EVET** |
| `D-03` | Marka temizliği | açık | yayın öncesi |
| `D-06` | KDP Previewer + prova baskı | açık | P6 |
| **`D-10`** | **WSU E.M. 2246 edinimi** *(yeni)* | açık | hayır |
| **`D-11`** | **18 kaynağın tam metin denetimi** *(yeni)* | açık | hayır |

`physical_validation_status = external_pending`
`differentiation_test_status = external_pending`

**AI incelemesi insan testinin yerine SAYILMAZ** (`K6`;
`aiProxyCountsAsHuman: false`, açılamaz). Bu turda dört bağımsız
inceleme hattı çalıştı ve 149 bulgu üretti — **hiçbiri `D-01`'in
yerine geçmez.**

## 17 · Riskler

**24 risk** — bu turda **üç yeni**:

- **`R-22` Ayırt edici kanıtın gerçekten ayırmaması.** 43 belirtinin
  **28'inde** iki neden aynı gözlemi üretiyor. Şema alanın **dolu**
  olmasını dayatıyordu; **işini yapmasını** hiçbir şey dayatmıyordu.
  Uydurma ayrım yazılmadı (`K52`); çakışmalar okura beyan ediliyor.
  Gerçek çözüm `D-02`'dedir.
- **`R-23` Kaynağın söylemediği şeyin ona atfedilmesi.** Dört atıfta
  gerçekleşti. **Kaynaklı görünen kaynaksız bir iddia, kaynaksız bir
  iddiadan daha tehlikelidir: denetimden geçer.**
- **`R-24` Manüskript kapılarının CI'da çalışamaması.** Proza bilerek
  izlenmiyor; temiz klonda `qa_manuscript` kendini atlar. Yapısal ve
  kabul edilmiş; iki türev (iddia sicili + iddia haritası) CI'da
  denetleniyor.

**Hiçbir risk silinmedi.**

## 18 · Git / CI

| | |
|---|---|
| Dal | `faz/4-production` — **itildi** (CI `faz/**` dallarını kapsıyor) |
| Commit | 4 |
| İzlenen dosya | **193** (önceki tur 139) |
| CI | **11 iş · 10 başarılı · 1 tasarım gereği başarısız** |
| Temiz klon | ✓ doğrulandı — veri kapıları bağımlılıksız çalışıyor |

**CI iş listesi (koşum `33230267042`):**

| Sonuç | İş |
|---|---|
| ✓ | kapı seviyelerini oku |
| ✓ | şema · bütünlük · kaynak otoritesi |
| ✓ | depo · koruma · marka · izolasyon |
| ✓ | crosswalk tazeliği + bütünlüğü |
| ✓ | kitap sınırı |
| ✓ | iddia disiplini · terminoloji |
| ✓ | görsel sistem |
| ✓ | **iddia sicili · izlenebilirlik · manüskript kapısı** *(yeni)* |
| ✓ | KAPILARIN KENDİ TESTİ |
| ✓ | RENDER KATMANI |
| ✗ | **kill-gate ön koşulu — TASARIM GEREĞİ BAŞARISIZ** (`continue-on-error`) |

Kill-gate işinin başarısız olması bir kusur değil, **kayıttır**: Faz 3
ölçülene kadar bu iş her koşumda kırmızı yanacaktır ve yanmalıdır.

⚠ **Master'a birleştirilmedi.** Faz 4 kurucu geçersiz kılmasıyla
yürütüldü; birleştirme kararı kurucunundur. PR bağlantısı depoda hazır.

**Bilerek yayımlanMAYAN:** manüskript prozası (`02_CONTENT/protected/`)
· dizilmiş kitap PDF'i · pilot prozası · fiziksel sınama fotoğrafları ·
katılımcı verisi · telif korumalı referans malzeme · yazı tipi ikili
dosyaları · üretilmiş figür PDF'leri.

**Yayımlanan:** kod · şema · taksonomi · kaynak kayıtları · **iddia
sicili** · **iddia→kaynak haritası** · **manüskript ÖLÇÜMÜ** · raporlar
· **bağımsız incelemenin ham çıktısı** (428 KB).

Ham inceleme çıktısının yayımlanması bilinçlidir: rapor ondan
**üretilir** ve bu, raporun incelemenin söylediğini taşıdığının tek
kanıtıdır.

## 19 · Faz 5 hazırlığı

**Faz 5'e mekanik olarak GEÇİLEMEZ** ve bu doğrudur: `phase5-qa`,
`phase3-pilot`'ın arkasındadır ve kill-gate ölçülmedi.

Faz 5 için hazır olan: tam manüskript · 307 iddialık sicil ·
izlenebilirlik haritası · **14 denetimli** manüskript kapısı ·
**152 öz-test** · `D-10` ve `D-11` yazılı · **28 kayıtlık fiziksel
sınama kiti** (`D-02` yapıldığında dokuz `Y-6` kaydı, 43 belirtinin
28'indeki kanıt çakışmasının yüksek şiddetli olanlarını **çözmek**
üzere hazır).

Faz 5'in ilk işi, Faz 4'ün **kapatamadıklarıdır**: 28 kanıt çakışması
(`D-02`) · 18 kaynağın tam metin denetimi (`D-11`) · sayfa örnekleminin
gözle incelenmesi (`R-19`).

---

## Faz 4 "TAM DOĞRULANDI" DEMEZ

Bu faz **üretim tamamlandı** der ve **başka hiçbir şey demez.**

**Yapılmayanlar, açıkça:** insan doğrulaması yapılmadı · fiziksel
doğrulama yapılmadı · profesyonel hukuki temizlik yapılmadı · gerçek
baskı doğrulaması yapılmadı · 129 nedensel ilişkinin hiçbiri kumaşta
sınanmadı · 28 kanıt çakışması çözülmedi, yalnızca **beyan edildi**.

Kitap **ÜRETİM TAMAMLANMIŞ** durumdadır ve aynı anda
**DIŞ DOĞRULAMA BEKLEMEDEDİR**.

---

*Vâliçe Press · BEFORE YOU CUT · Phase 4 Execution Report · 29 Ağustos 2026*
