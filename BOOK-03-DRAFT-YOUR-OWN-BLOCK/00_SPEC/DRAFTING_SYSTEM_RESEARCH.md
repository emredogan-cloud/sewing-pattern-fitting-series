# BOOK-03 — ÇİZİM SİSTEMİ ARAŞTIRMA MİMARİSİ (`A10`)

> ⚠ **BU KİTAP ÜRETİLMİYOR.** Kitap 3'ün kapısı `init`'tir ve bu turda
> ilerlemedi. Bu belge Faz 1 yürütmesinin **yalnızca araştırma
> mimarisini** kurar: hangi sistemler değerlendirilecek, hangi kanıt
> gerekecek, hangi kaynak edinilecek, hangi ölçü bağımlılıkları var.
>
> `OPEN_QUESTIONS A10` · `DECISIONS.md K27` (terminoloji: `A9` → `K26`)

---

## 0 · Bu turda ne KARARA BAĞLANDI, ne BAĞLANMADI

| Konu | Durum |
|---|---|
| Hangi çizim sistemi kullanılacak | **BAĞLANMADI** — teknik kanıt yok, bağlanamaz |
| Sistemin nasıl SEÇİLECEĞİ | **BAĞLANDI** — § 3'ün ölçütleri ve § 4'ün kanıt kapısı |
| Hangi kaynakların edinileceği | **BAĞLANDI** — `ACQUISITION_REQUEST_QUEUE A-01`, `A-04` |
| Görsel üretim mimarisi | **KAVRAMSAL OLARAK BAĞLANDI** — § 5 |
| Ölçü bağımlılıkları | **BAĞLANDI** — § 6 |
| Başlıkta `block` mu `sloper` mı | **BAĞLANDI** — § 7 (`A9`) |

**Sistem neden şimdi seçilemez:** bu depoda hiçbir kalıp çizim
referansı yoktur ve 12 blok bileşeninin (`BLK-01`–`BLK-12`) hiçbiri bir
kaynağa bağlı değildir. Kamu kaynağı taraması bu boşluğu **kapatamadı**
— eldeki altı kurumsal kaynağın hepsi *var olan bir kalıbın
düzeltilmesini* anlatır, *sıfırdan çizimi* değil
(`../../01_SOURCE/PUBLIC_SOURCE_SURVEY.md § 6`).

Sistemi kanıtsız seçmek, `SOURCING_STANDARD § 7`'nin doğrudan ihlali
olurdu: farklı çizim okulları aynı sonuca farklı geometrilerle ulaşır ve
**hiçbiri yanlış değildir** — birini sessizce tercih etmek yasaktır.

## 1 · Kitap 3'ün çözdüğü problem — sistemin hizmet edeceği şey

> "Her kalıpta aynı düzeltmeyi tekrarlamak istemiyorum."

Bu, sistem seçimini doğrudan kısıtlar. Kitap 3 bir **moda kalıpçılığı
ders kitabı değildir**; Kitap 1'in uyum profilini ve Kitap 2'nin tekrar
eden düzeltmelerini **kalıcı bir bloğa** çeviren bir üründür.

Bu yüzden değerlendirme ölçütlerinin başında "sistem ne kadar
kapsamlı" değil, **"sistem ev koşullarında tek kişi tarafından
uygulanabilir mi"** gelir.

## 2 · Değerlendirilecek sistem aileleri

| # | Aile | Karakteri | Kitap 3'e uygunluk hipotezi |
|---|---|---|---|
| **DS-1** | **Doğrudan ölçü (direct measurement) çizimi** — ölçüler doğrudan çizime girer | Kişiye özel; oran tablosu yok | **En güçlü aday** — ürünün vaadi tam olarak kişiye özeldir |
| **DS-2** | **Oransal (proportional) çizim** — birkaç ana ölçüden oranla türetme | Endüstriyel; beden serisi üretmeye uygun | Zayıf — kişiye özel bloğa gereksiz dolaylılık ekler |
| **DS-3** | **Karma** — ana ölçüler doğrudan, ara noktalar oranla | Yaygın uygulama | Orta — DS-1 yetersiz kalırsa yedek |
| **DS-4** | **Ölçüden türetme + kalıptan geri mühendislik** — mevcut, iyi oturan bir kalıptan blok çıkarma | Ev dikişçisinin gerçek başlangıç noktası | **İkinci güçlü aday** — Kitap 1–2 zincirinin doğal devamı |

**DS-4 neden özellikle ilginç:** okur Kitap 1'de teşhis etti, Kitap 2'de
düzeltti; elinde **düzeltilmiş ve doğrulanmış** bir kalıp var. Bunu bir
bloğa çevirmek, sıfırdan çizmekten hem daha kısa hem de kanıtı elinde
olan bir yoldur. Bu, serinin kendi mimarisinin ürettiği bir
farklılaşma adayıdır ve **hiçbir rakip bu yolu Kitap 1–2 zinciriyle
birlikte sunmuyor** `HYPOTHESIS`.

## 3 · Seçim ölçütleri — önceden yazılı, sonradan uydurulmaz

| # | Ölçüt | Ağırlık | Nasıl ölçülür |
|---|---|---|---|
| Ö1 | **Tek kişi uygulayabilir mi** — yardımcı gerektiren adım sayısı | **Yüksek** | Adım sayımı |
| Ö2 | **Kitap 1'in ölçü setiyle uyum** — kaç yeni ölçü ister | **Yüksek** | § 6 |
| Ö3 | **Fiziksel doğrulanabilirlik** — bloğun doğru olduğu nasıl anlaşılır | **Yüksek** | `BLK-12` doğrulama toile'i |
| Ö4 | **Deterministik çizilebilirlik** — adımlar kayıt verisinden figüre çevrilebilir mi | Orta–yüksek | § 5 |
| Ö5 | Öğretilebilirlik — adım sayısı ve geri dönüş noktaları | Orta | Adım sayımı |
| Ö6 | Kaynak erişilebilirliği | Orta | `ACQUISITION_REQUEST_QUEUE` |
| Ö7 | Telif güvenliği — yöntem serbest, **ifade değil** | **Sert kısıt** | `IP_AND_BRAND_POLICY § 2` |

**Ö7 bir ölçüt değil, bir kapıdır.** Bir çizim yöntemi telifle
korunmaz; bir kitabın anlatımı, tabloları ve çizimleri korunur. Kitap 3
bir sistemi **öğrenip sıfırdan anlatır**; hiçbir çizim izlenerek
çoğaltılmaz.

## 4 · Kanıt kapısı — sistem hangi koşulda seçilebilir

Bir sistem ancak **üçü birden** sağlandığında seçilebilir:

1. **En az iki bağımsız sistem** `fulltext` seviyesinde okunmuş olmalı
   (`ACQUISITION_REQUEST_QUEUE A-04`). Tek sistem okunursa seçim
   gerekçesiz olur — karşılaştırma yoksa tercih yoktur.
2. Seçilen sistemin **ölçü tanımları** `S-0014` (ISO 8559-1) veya eş
   otoriteyle hizalanmış olmalı (`A-01`). Farklı sistemler aynı adı
   farklı yerlerden ölçer; hizalama yapılmazsa Kitap 1'in ölçü kartı
   Kitap 3'te **yanlış sayı** verir.
3. Seçilen sistemle çizilmiş bir blok **fiziksel olarak sınanmış**
   olmalı — `BLK-12`'nin doğrulama toile'i, `VAL-xxxx` kaydıyla.

**Üçü de bugün eksiktir.** Bu yüzden `A10` **ERTELENDİ**, "açık"
bırakılmadı: ertelemenin koşulu, sahibi ve fazı yazılıdır.

## 5 · Görsel üretim mimarisi — kavramsal karar

Kitap 3'ün figürleri Kitap 1'inkinden **yapısal olarak farklıdır**:
Kitap 1 bir vücut/giysi üzerinde *gözlem* gösterir; Kitap 3 bir kâğıt
üzerinde *inşa adımı* gösterir.

| Üretim yolu | Uygunluk | Karar |
|---|---|---|
| **Deterministik CLI üretimi** — çizim adımları veriden figüre | **Çok yüksek** | **Birincil yol** |
| Dış görsel varlık (elle çizim, satın alınmış çizim) | Düşük | Yalnızca istisna |
| Karma | Orta | Yedek |

**Neden deterministik üretim Kitap 3'te Kitap 1'den DAHA uygun:**
bir blok çizimi zaten bir **algoritmadır** — "A noktasından B'ye X
kadar git, dik indir, eğri çiz". Bu, doğrudan koda çevrilebilir bir
tariftir. Kitap 1'in belirti figürleri (gerçek kumaşın davranışı) bu
kadar kolay türetilemez.

**Bu, serinin en büyük üretim kaldıracıdır** ve `REUSE_MAP`'in
mantığını doğrular: Kitap 1'in figür motoru Kitap 3'te **daha yüksek**
deterministik oran verebilir.

**Sert kısıt:** deterministik üretim, sistem seçilmeden yazılamaz —
motorun girdisi sistemin geometrisidir. Bu yüzden § 4'ün kanıt kapısı,
görsel mimarinin de ön koşuludur.

## 6 · Ölçü bağımlılıkları — Kitap 1'in setiyle ilişki

Kitap 1'in 32 ölçüsü **teşhis** için seçildi. Blok çizimi için
gerekecek olanlar `TOP-21`'de ayrı bir topik olarak zaten ayrılmıştır
(`K13`'ün topik bölmesi).

| Grup | Durum |
|---|---|
| **Kitap 1'de var ve doğrulanmış** — `M-001` `M-002` `M-005` `M-006` `M-014` `M-016` `M-020` `M-023` `M-024` `M-026` `M-027` `M-029` | Kitap 3 doğrudan kullanır |
| **Kitap 1'de var, doğrulanmamış** — `M-004` `M-015` `M-017` `M-018` `M-019` `M-021` `M-022` | **Kitap 3 için KRİTİK.** Bir blok bu noktalardan inşa edilir; tanım belirsizliği doğrudan yanlış geometriye dönüşür → `A-01`'i Kitap 3'te **zorunlu** yapan asıl neden |
| **Kitap 1'de YOK, blok için gerekebilecek** | Sistem seçilmeden listelenemez — seçim sonrası ilk iş |

> **Bulgu:** `A-01` (ISO 8559-1) Kitap 1 için *iyi olur*, Kitap 3 için
> *gereklidir*. Bu, edinim kuyruğundaki önceliklendirmenin gerekçesidir.

## 7 · `A9` — başlıkta `block` mu `sloper` mı

### 7.1 · Kanıt

| Bulgu | Durum |
|---|---|
| `sloper` **ABD** kullanımıdır; `block` Birleşik Krallık ve Avustralya kullanımıdır | `OBSERVED` 28 Ağu 2026 |
| ABD arama niyeti `sloper` ekseninde yoğunlaşıyor ("sloper drafting", "how to draft a sloper", "personal sloper") | `OBSERVED` — `SERIES_KEYWORD_ARCHITECTURE § 4` |
| **ABD dikiş dilinde `block` sözcüğü kapkaçlı bir ikinci anlam taşır: kapitone (quilt) bloğu** | `OBSERVED` — arama sonuçları bu anlamla dolu |
| Bazı kaynaklar ikisini teknik olarak ayırır (bloğun ease taşıdığı, sloper'ın taşımadığı) | `OBSERVED` — ama kullanım büyük ölçüde eşanlamlıdır |

### 7.2 · KARAR

> **Başlık yüzeyinde `SLOPER`. Depo içi kanonik terim `block` OLARAK
> KALIR.**

**Neden `sloper` başlıkta:**
1. Hedef pazar ABD'dir ve baskın terim odur.
2. `block` ABD dikiş kategorisinde **kapitone bloğuyla karışır** —
   keşfedilebilirlik açısından bu tek başına belirleyicidir.
3. Alt başlık her iki biçimi de taşır, böylece iki arama kümesi de
   yakalanır.

**Neden kanonik terim değişmiyor:** `terminology.json T-05` `block`'u
kanonik yapar ve `STYLE.md § 2` `sloper`'ı **tam eşdeğer** olarak
korur. `A9` zaten "hangisi *başlıkta* duracak" sorusuydu — kanonik
terim sorusu değil. İç dili değiştirmek 148 crosswalk kaydını ve üç
kitabın dilini gereksizce sarsardı.

**Sonuç — çalışma başlığı:**

| Yüzey | Metin |
|---|---|
| Başlık | *True Fit 3 — Draft Your Own Sloper* → **seri adı `A1`'e bağlıdır** |
| Alt başlık | `block` biçimini **de** taşır |
| Dizin adı (`BOOK-03-DRAFT-YOUR-OWN-BLOCK`) | **Değişmez** — yerel, yayımlanmaz |
| Kitap içi dil | `block` kanonik, `sloper` bir kez eşanlamlı olarak tanıtılır |

⚠ Nihai başlık `A1` (seri adı) kapanmadan **kesinleşemez**.

## 8 · Bu turda YAPILMAYAN

Kitap 3 içerik spesifikasyonu · bölüm mimarisi · blok çizim adımları ·
figür üretimi · kaynak edinimi · sistem seçimi.

**Kitap 3 kapısı `init`'te kalır.** Kitap 3'ün P0'ı bile
başlamamıştır ve Kitap 1'in P3 kill-gate'i PASS vermeden başlamaz
(`SERIES_ROADMAP § 4`).

---

*Vâliçe Press · TRUE FIT 3 · Drafting System Research Architecture · 28 Ağustos 2026*
