# OPEN QUESTIONS — karar durum tablosu

> Kural (kardeş projelerden devralındı): **bir varsayım sessizce proje
> gerekliliğine dönüşemez.** Araştırma raporunun vermediği her şey önce
> buraya yazılır.
>
> Durum tablosu · **28 Ağustos 2026** — Kitap 1 Faz 1 **yürütmesi**
> sonrası. Alınan kararlar: [`DECISIONS.md`](DECISIONS.md) `K18`–`K35`.

---

## 0 · Dört durumdan biri — "hâlâ açık" diye bir durum yoktur

| Durum | Anlamı |
|---|---|
| **CLOSED — DECIDED** | Kanıt yeterliydi; ajan güvenle karar verdi ve kaydetti |
| **CLOSED — FOUNDER POLICY** | Kurucu kararı açıkça verdi; ajan yürüttü |
| **EXTERNAL PENDING** | Depo içinden tamamlanamaz; dış bir aktör gerekir |
| **DEFERRED** | Bugün karar verilirse kanıtsız olur; hangi fazda, hangi kanıtla kapanacağı yazılı |

## 1 · Özet tablo

| # | Soru | **Durum** | Karar / bekleyen |
|---|---|---|---|
| **A1** | "TRUE FIT" seri adı kullanılabilir mi | **CLOSED — DECIDED** | **Hayır** — yayımlanan ad olarak kilitlenmez (`K18`) |
| **A2** | Depo GitHub'a itilsin mi, public mi | **CLOSED — FOUNDER POLICY** | Public + CI, **marka-nötr adla** (`K32`) |
| **A3** | Teknik kaynak edinim bütçesi | **CLOSED — DECIDED** | Faz 1 için **satın alma GEREKMEDİ**; 15 kayıt, 6 tam metin (`K19`) |
| **A4** | Ortam: QR → video | **CLOSED — DECIDED** | Basılı kitap + **tek adresli** tamamlayıcı; video kapsam dışı (`K25`) |
| **A5** | Format: trim, cilt, spiral, kâğıt, Kindle | **CLOSED — DECIDED** | 8,5×11 ciltsiz beyaz kâğıt; spiral KDP'de **yok** (`K22`) |
| **A6** | Renk stratejisi | **CLOSED — DECIDED** | **Siyah mürekkep** + ölçülebilir yeniden açılma eşiği (`K23`) |
| **A7** | Font seçimi ve lisansı | **CLOSED — DECIDED** | Source Serif 4 + Source Sans 3, OFL, **$0** (`K24`) |
| **A8** | Birim sunumu | **CLOSED — DECIDED** | **İnç birincil**; figürlerde yalnızca inç, eşiklerde inç+cm (`K34`) |
| **A9** | Kitap 3 başlığında `block` mu `sloper` mı | **CLOSED — DECIDED** | Başlıkta **`sloper`**, kanonik terim `block` (`K26`) |
| **A10** | Kitap 3 hangi çizim sistemini kullanacak | **DEFERRED** | Kanıt kapısı kuruldu; sistem seçilemez (`K27`) — § 2.1 |
| **A11** | Gerçek vücut fotoğrafı | **CLOSED — DECIDED** | **Kullanılmaz**; koşullu, en fazla 6 (`K35`) |
| **A12** | Reklam: bütçe, kelime kümesi, iptal eşiği | **CLOSED — DECIDED** | Çerçeve kuruldu; **bütçe P7'ye ertelendi** (`K28`) — § 2.2 |
| **A13** | Fiziksel sınama kapsamı | **CLOSED — DECIDED** | **2 toile + 3 parça, 19 kayıt, tek vücut** (`K29`) |
| **A14** | Fark testi katılımcıları | **EXTERNAL PENDING** | Protokol tam; katılımcı yok (`K30`) — § 3.1 |
| **A15** | *(yeni)* Yerine geçecek seri adı + marka temizliği | **EXTERNAL PENDING** | `A1`'in doğurduğu soru — § 3.2 |

**Sayım:** 12 kapandı · 1 ertelendi · 2 dış beklemede.

---

## 2 · ERTELENEN kalemler — beş alan zorunlu

### 2.1 · `A10` · Kitap 3 çizim sistemi

| Alan | |
|---|---|
| **Neden bugün karar verilemez** | Bu depoda hiçbir kalıp çizim referansı yoktur ve 12 blok bileşeninin hiçbiri kaynağa bağlı değildir. Kamu kaynağı taraması bu boşluğu kapatamadı: eldeki altı kurumsal kaynağın hepsi *var olan bir kalıbın düzeltilmesini* anlatır, *sıfırdan çizimi* değil. Kanıtsız seçim `SOURCING_STANDARD § 7`'nin doğrudan ihlali olur. |
| **Kim / ne karar verir** | Ajan — **ama ancak § kanıt kapısı sağlandıktan sonra**. Kaynak edinimi kurucu kararıdır. |
| **En geç hangi faz** | **Kitap 3 `phase1-spec`** |
| **Gereken kanıt** | ① En az **iki bağımsız sistem** tam metin okunmuş; ② ölçü tanımları `S-0014` (ISO 8559-1) veya eş otoriteyle hizalanmış; ③ seçilen sistemle çizilmiş bir blok fiziksel olarak sınanmış (`BLK-12`, bir `VAL-xxxx` kaydı) |
| **Yanlış karar verilirse** | Blok geometrisi yanlış olur; okur ölçüsünü doğru alsa bile oturmayan bir blok çizer. Kitap 3'ün tek vaadi budur. |
| **Hazırlık** | `BOOK-03-DRAFT-YOUR-OWN-BLOCK/00_SPEC/DRAFTING_SYSTEM_RESEARCH.md` — dört sistem ailesi, yedi ölçüt, kanıt kapısı, görsel mimari, ölçü bağımlılıkları |

### 2.2 · `A12` alt kalemi · reklam BÜTÇESİ

| Alan | |
|---|---|
| **Neden bugün karar verilemez** | Altı girdinin **hiçbiri** mevcut değil: doğrulanmış birim telif (P6), nihai liste fiyatı (P6), 30 günlük organik taban (P7), yorum tabanı (P7), gözlemlenen CPC (Kampanya A), fark testi PASS (P3) |
| **Kim karar verir** | **Kurucu** |
| **En geç hangi faz** | Kitap 1 `release` (P7) öncesi |
| **Gereken kanıt** | `ADS_FRAMEWORK.md § 5`'in altı maddesi |
| **Yanlış karar verilirse** | Dar bir nişte, yorumsuz bir sayfaya reklam vermek bütçeyi yakar ve **yanlış** sonuç üretir (`D6`) |

### 2.3 · `A5` alt kalemleri · ciltli SKU · Kindle · Kitap 2 spirali

| Kalem | En geç | Gereken kanıt | Sonucu |
|---|---|---|---|
| Ciltli 8,25×11 ikinci SKU | Kitap 1 `phase6-format` | Gerçek KDP maliyeti + talep işareti; **ayrı iç dosya** maliyeti | Ekonomi olumlu ama kanıtsız SKU üretim yükü ekler |
| Kindle sürümü | Kitap 1 `phase6-format` | Faz 2'nin **ÖLÇTÜĞÜ** figür sayısı ve dosya boyutu | Akışkan düzen "bir yayılım bir kavram" kuralını bozar; sabit düzen telefonda okunmaz |
| Kitap 2 spiral/düz açık durma | **Kitap 2 `phase1-spec`** | KDP dışı üretim yolu fizibilitesi ve maliyeti | Kitap 2 bir referans atlasıdır; düz açık durmazsa ürün gereksinimini karşılamaz (`R-09`) |

### 2.4 · `A3` alt kalemi · ücretli kaynak edinimi

**Faz 1 için gerekli DEĞİL.** Dört kalem kuyrukta ve her birinin
gerçekten gerekli olduğu faz yazılı:
`01_SOURCE/ACQUISITION_REQUEST_QUEUE.md`.

Ayrıca **ücretsiz ama yapılması gereken** üç edinim Faz 2'ye
yazıldı (TAMU serisinin elle indirilmesi, USDA 1945 bültenleri,
MSU taramalarının gözle okunması) — maliyeti **sıfır**.

---

## 3 · DIŞ BEKLEMEDEKİ kalemler

### 3.1 · `A14` · Fark testi katılımcıları — **KILL-GATE ENGELİ**

| Alan | |
|---|---|
| **Neden depo içinden çözülemez** | Üç gerçek ev dikişçisi gerekir. **AI vekil SAYILMAZ** ve `aiProxyCountsAsHuman` bayrağı `false`'tur, açılamaz (`K6`) |
| **Kim yapar** | **Kurucu** — protokol bağımsız uygulanabilir biçimde yazıldı |
| **En geç hangi faz** | Kitap 1 `phase3-pilot` — **kapı budur** |
| **Gereken kanıt** | Üç katılımcının kayıtlı yanıtı; en az ikisinin farkı **kendiliğinden** söylemesi |
| **Yanlış/eksik ölçüm sonucu** | Farklılaşma hipotezi **üç kitabın da temelidir**. Sahte bir PASS, çürük bir hipotezin üzerine üç kitap inşa eder. |
| **Şu an hazır olan** | Eleme ölçütleri · üç soruluk ön eleme · beş bulma kanalı · teşvik politikası · taraf tutma kuralları · **oturum betiği** · kayıt formu · malzeme spesifikasyonu — `BOOK-01/00_SPEC/DIFFERENTIATION_TEST.md § 5–6` |
| **Şu an eksik olan** | **Yalnızca katılımcılar.** Ve pilot bölüm (Faz 3 çıktısı). |
| **1–2 katılımcı bulunursa** | Sonuç **`INCONCLUSIVE`** olarak kaydedilir. PASS **değildir**, FAIL **değildir**; `measured` `false` kalır ve kapı **kapalı kalır**. Faz 2 üretimi ve fiziksel sınama devam eder (`K30`). |

### 3.2 · `A15` · Yerine geçecek seri adı + profesyonel marka temizliği *(yeni)*

| Alan | |
|---|---|
| **Nereden doğdu** | `A1`'in kapanışından (`K18`): `TRUE FIT` yayımlanan ad olarak kilitlenemez |
| **Neden depo içinden çözülemez** | ① Marka temizliği bir hukuki hizmettir; yapılan tarama onun yerine geçmez (federal sicilin arama arayüzü otomatik sorguya kapalıydı). ② Marka seçimi bir ticari kimlik kararıdır. |
| **Kim karar verir** | **Kurucu** (seçim) + **marka vekili** (temizlik) |
| **En geç hangi faz** | Seçim: Kitap 1 `phase2-visual` **başlangıcı** · temizlik: kapak/metadata üretiminden **önce** |
| **Gereken kanıt** | Seçilen ad için profesyonel temizlik araştırması |
| **Ajanın önerisi** | **`BEFORE YOU CUT`** — üç eksende sıfır çakışma bulgusu; kalabalık "FIT ___" alanının tamamen dışında; serinin tezini ve kapsam sınırını adın kendisi taşıyor. İkinci sıra: `FIT SIGNS`. **Elenen:** `FIT LOGIC` (giyim sınıfında tescilli) |
| **Yanlış karar verilirse** | Bir listeleme kaldırma bildirimi üç kitabın kapağını, metadata'sını ve kurulmuş arama görünürlüğünü **aynı anda** sıfırlar (`R-12`) |
| **Ara azaltma — yapıldı** | GitHub deposu marka-nötr adla açıldı; hiçbir ad kamuya taahhüt edilmedi (`K32`) |
| **Kanıt dosyası** | `08_REPORTS/PHASE_1_BRAND_SCREENING.md` |

---

## 4 · Kapanmış sorular — kararların özeti

| # | Karar | Nerede |
|---|---|---|
| `A1` | `TRUE FIT` yayımlanan ad olarak **kullanılamaz**; çalışma adı olarak korunur | `K18` · `08_REPORTS/PHASE_1_BRAND_SCREENING.md` |
| `A2` | Public depo + CI, **marka-nötr ad** | `K32` |
| `A3` | Faz 1 **satın almasız** kapandı; 15 kaynak, 16/32 ölçü ve 13/19 aile doğrulandı | `K19` · `01_SOURCE/PUBLIC_SOURCE_SURVEY.md` |
| `A4` | Basılı kitap + **tek adresli** tamamlayıcı (formlar, renkli şemalar, errata); sayfa başına QR **reddedildi**; video kapsam dışı | `K25` |
| `A5` | 8,5×11 ciltsiz, beyaz kâğıt; **spiral KDP'de yok** | `K22` |
| `A6` | **Siyah mürekkep**; premium renk aritmetik olarak dışarıda; %10 eşiğiyle yeniden açılır | `K23` |
| `A7` | Source Serif 4 + Source Sans 3 (OFL, **$0**); yedek Atkinson Hyperlegible | `K24` |
| `A8` | **İnç birincil**; figürlerde yalnızca inç, karar eşiklerinde inç + cm | `K34` · `VISUAL_SPEC § 7` |
| `A9` | Başlıkta **`sloper`**; kanonik terim `block` kalır | `K26` |
| `A11` | Fotoğraf **kullanılmaz**; yedi figür türünün dördünde fotoğraf çizimden **kötüdür** | `K35` · `VISUAL_SPEC § 5` |
| `A12` | Çerçeve kuruldu: başabaş CPC = telif × dönüşüm; başabaş ACoS %41,4; **300 tıklamalık** test; altı durma koşulu | `K28` · `00_CONTEXT/ADS_FRAMEWORK.md` |
| `A13` | **2 toile + 3 parça, 19 `VAL` kaydı**, tek vücut, ≈$15–30, ≈20–25 saat | `K29` |

---

*Vâliçe Press · TRUE FIT · Open Questions · 28 Ağustos 2026 (Faz 1 yürütmesi)*
