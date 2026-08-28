# MEDIUM DECISION FRAMEWORK — ortam ve dijital tamamlayıcı

> Görev talimatı § 27. **Faz 1 yürütmesinde ÜRÜN MİMARİSİ KARARA
> BAĞLANDI** — `OPEN_QUESTIONS A4`, `DECISIONS.md K25`.
>
> ⚠ Bu belge korunan iddiayı TARTIŞTIĞI için `qa_claims.py`'den muaftır.

---

## 0 · KARAR

# BASILI KİTAP + TEK ADRESLİ DİJİTAL TAMAMLAYICI

# VİDEO ÜRETİMİ KAPSAM DIŞI · SAYFA BAŞINA QR REDDEDİLDİ

| Karar | İçerik |
|---|---|
| **A4-1** | Basılı kitap **kendi başına eksiksizdir.** Okurun ihtiyaç duyduğu hiçbir şey kitabın dışında değildir. |
| **A4-2** | Kitap 1, **tek bir kalıcı adrese** sahip bir dijital tamamlayıcıyla çıkar. İçeriği üç kalemle sınırlıdır (§ 3). |
| **A4-3** | Hareketli gösterim gerektiren beş içerik türü **adlandırıldı ve ERTELENDİ**; yeri ayrıldı, üretimi yapılmadı. |
| **A4-4** | Terk stratejisi **karardan önce** yazıldı (§ 5) — çerçevenin kendi koşulu. |

## 1 · Neden bu proje "video ekleyelim" diyemez ve "eklemeyelim" de diyemez

**Ekleme yönünde kanıt:** Lider ürün (n=958) hibrittir. Müşteri
etiketlerinde `Video content` bir GÜÇ olarak anılıyor ve "neredeyse her
sayfada QR kodu" öne çıkarılıyor `OBSERVED` 27 Ağu 2026. Araştırma
raporu § 32 ortam riskini **serinin en büyük riski (Yüksek)** olarak
işaretledi.

**Eklememe yönünde kanıt:** Yok. Araştırma raporunun § 27 girdi
geçerliliği testinde "basılı formatın gerçek bir avantajı var" iddiası
sınandı ve **ZAYIF** çıktı. Bu iddia bu projede bir gerekçe olarak
kullanılamaz (`CLAIMS_STANDARD.md § 2`).

**Faz 1 yürütmesinde eklenen üçüncü kısıt:** kurucu, bu aşamada
**fiziksel video çekimi yapılamayacağını** bildirdi. Bu, "hangi ortam
daha iyi" sorusunu ortadan kaldırmaz ama **bugün verilebilecek kararı**
netleştirir: video, kanıt eksikliğinden değil, **üretim kapasitesi
yokluğundan** kapsam dışıdır. İkisi karıştırılmaz.

## 2 · Karar dört ayrı soruya bölünür — ve üçü yanıtlandı

| # | Soru | Durum |
|---|---|---|
| S1 | Hangi içerik basılı sayfada **daha iyi** çalışır? | **YANITLANDI** — § 2.1 |
| S2 | Hangi içerik hareketli gösterim **gerektirir**? | **YANITLANDI** — § 2.2 |
| S3 | QR okur için **gerçekten** kullanışlı mı, yoksa rakip taklidi mi? | **AÇIK** — Faz 3 pilot testinde okura sorulur |
| S4 | Bakım yükü ve bağlantı ölümü riski kabul edilebilir mi? | **YANITLANDI** — § 5 |

### 2.1 · S1 — basılı sayfanın taşıdığı içerik

| İçerik türü | Karar |
|---|---|
| Teşhis akış şeması (7 bölge + 1 ana + 1 eleme) | **Basılı** — kitabın imza formu; okur şemada *gezinir*, izlemez |
| Ölçü alma yolu (`M-xxx` figürleri) | **Basılı** — durağan geometri |
| Belirti tanıma figürleri | **Basılı** |
| Tablolar, kontrol listeleri, boş formlar | **Basılı** — ayrıca fotokopi edilebilir olmalı |
| Kalıptan düz ölçü alma | **Basılı** |

### 2.2 · S2 — hareketli gösterim GEREKTİREN beş içerik türü

Bunlar **adlandırıldı ve sayıldı**; üretilmedi.

| # | İçerik | Neden hareketli | Kitap |
|---|---|---|---|
| H1 | Ölçüm **hatası** — şeridin kayması, duruşun bozulması | Hata bir **harekettir**; durağan görüntüde görünmez | 1 (Bölüm 2.6, 6 hata) |
| H2 | Belirtinin **hareketle ortaya çıkması** — kol öne uzatınca sırtta çekme | Tanımı gereği hareketli | 1 (Bölüm 5.3, 4 hareket testi) |
| H3 | Toile üzerinde iğneleme | El becerisi | 1 (Bölüm 4.4) · **2 (asıl yeri)** |
| H4 | Kalıpta kes-ve-aç sırası | Sıralama hatası hareketle daha görünür | **2** |
| H5 | Blok çizim sırası | Uzun ve tekrarlı | 3 (basılı referans muhtemelen üstün) |

**Kritik gözlem:** beş türden **üçü Kitap 2'ye aittir**, Kitap 1'e
değil. Kitap 1'in içeriği (teşhis) yapısal olarak durağandır; Kitap 2'nin
içeriği (işlem) yapısal olarak hareketlidir.

> **Sonuç: QR/video sorusu aslında bir KİTAP 1 sorusu değil, bir
> KİTAP 2 sorusudur.** Kitap 1'de sayfa başına QR koymak, çözdüğü bir
> sorun olmadan bakım yükü satın almaktır.

## 3 · Dijital tamamlayıcı — Kitap 1'de tam olarak ne var

**Tek bir kalıcı adres.** Kitapta iki yerde geçer: Parça 0'daki
"gerekli malzeme" sayfasında ve arka sayfalarda. Metin olarak **ve**
tek bir QR olarak. **Sayfa başına QR YOKTUR.**

| # | Kalem | Neden dijitalde daha iyi | Basılı karşılığı |
|---|---|---|---|
| **D1** | **Yazdırılabilir boş formlar** — ölçü kartı, prova kaydı, uyum profili | Okurun bunları **defalarca** yazdırması gerekir; kitap sayfası yeniden basılamaz | Ek E (aynı formlar basılı) |
| **D2** | **Bölge akış şemalarının renkli ve büyük sürümü** | Renk dijitalde **bedava** (`FORMAT_STRATEGY § 5`); ekranda büyütülebilir | Ek G (siyah-beyaz, basılı) |
| **D3** | **Düzeltme/errata sayfası** | 43 belirti ve 129 bağ taşıyan teknik bir kitapta hata **olacaktır**; kalıcı bir düzeltme adresi bir kalite taahhüdüdür | Yok — ama yokluğu kitabı çalışmaz kılmaz |

### 3.1 · Lansmanda AÇIKÇA OLMAYANLAR

video · sesli anlatım · etkileşimli araç · topluluk/forum · üyelik ·
e-posta yakalama zorunluluğu · sayfa başına QR

**Sesli anlatım neden değerlendirildi ve elendi:** bu kitabın öğrettiği
şey **görmektir**. Bir kırışıklık deseninin sesli tarifi, figürün
yerini tutmaz; erişilebilirlik katkısı da sınırlıdır çünkü içeriğin
kendisi görseldir. Erişilebilirlik yatırımı bunun yerine **etiketli
(tagged) PDF formlarına** yapılır (D1).

## 4 · Bağımsızlık testi — çerçevenin sert kuralı

> **Kitap, dijital tamamlayıcıya HİÇ erişilmeden tam değerini
> vermelidir.** Vermiyorsa ürün bir kitap değil, bir kursun broşürüdür.

| Kalem | İnternet yoksa ne olur |
|---|---|
| D1 formlar | Ek E'deki basılı formlar kullanılır — **kayıp yok** |
| D2 renkli şemalar | Ek G'deki basılı şemalar kullanılır — **kayıp yok** |
| D3 errata | Erişilemez — ama kitabın çalışmasını engellemez |

**Test SONUCU: GEÇTİ — tasarım gereği.** Üç kalemin hiçbiri kitabın
işleyişi için gerekli değildir. Bu, kararın en önemli özelliğidir ve
`A4` yeniden açılsa bile korunur.

## 5 · Terk stratejisi — `A4-4`, karardan ÖNCE yazıldı

### 5.1 · Bağlantı ölümü planı

Basılı bir QR **güncellenemez**. Bu yüzden:

1. QR **tek bir alan adına** işaret eder; alan adı kurucunun
   kontrolündedir ve barındırma sağlayıcısından bağımsızdır.
2. Barındırma değişirse alan adı yeni hedefe yönlendirilir — **basılı
   kitap değişmez**.
3. Alan adı bir gün düşerse: § 4'ün testi gereği okur **hiçbir şey
   kaybetmez**.
4. Kitapta QR'ın yanında **her zaman metin olarak da adres yazar** —
   QR okunamazsa adres elle yazılabilir.

**Sayfa başına QR'ın reddedilmesinin asıl gerekçesi budur:** onlarca
farklı hedefi taşıyan bir kitap, hedeflerin her biri için ayrı bir
ölüm riski taşır. Tek adres, tek risk, tek çözüm.

### 5.2 · Bakım bütçesi

Bir durağan sayfa + üç PDF + yedi görsel. Yıllık bakım: alan adı
yenileme + statik barındırma. **Video yok → kodlama, altyazı, güncelleme
yükü de yok.**

### 5.3 · Platform kısıtı

Basılı kitaba dış bağlantı koymak platform kurallarına tabidir; en
bilinen kısıtlar **yorum/inceleme talep etmemek** ve **başka
satıcılara yönlendirmemektir**. Tamamlayıcı sayfanın içeriği bu iki
şeyi **yapmaz**.

⚠ Bu kısıtların yürürlükteki tam metni bu turda **doğrulanmadı**;
doğrulama `phase6-format` kapısının maddesidir.

## 6 · S3 nasıl kapanır — Faz 3 pilot sorusu

Fark testi katılımcılarına, testin **sonunda** (fark sorusu sorulup
yanıtlandıktan sonra, sonucu kirletmemek için) tek bir ek soru
sorulur:

> "Bu kitabın internette bir tamamlayıcı sayfası olsaydı, orada ne
> bulmak isterdiniz?"

Yönlendirmesizdir; video kelimesi **araştırmacı tarafından
söylenmez**. Üç katılımcıdan ikisi kendiliğinden hareketli gösterim
isterse, `A4` Kitap 2 için yeniden açılır ve H3/H4 üretimi
değerlendirilir.

**Kayıt:** `08_REPORTS/PHASE_3_DIFFERENTIATION_TEST.md` § ek gözlemler.
Bu soru **kill-gate'in parçası DEĞİLDİR** ve sonucu PASS/FAIL kararını
etkilemez.

## 7 · Sayfa düzeni sonucu

`K8`'in geri dönülebilir varsayılanı **daraltıldı**: sayfa düzeni artık
her sayfada QR alanı bırakmaz. Bunun yerine **bölüm sonlarında** bir
kaynak bandı yeri korunur. Kitap 2 hareketli içerik eklemeye karar
verirse, o bant bölüm düzeyinde QR taşıyabilir.

Kazanç: sayfa başına ayrılan boşluk geri kazanıldı ve "bir yayılım, bir
kavram" kuralına harcandı.

## 8 · Karar sahipliği

| | |
|---|---|
| Karar sahibi | Kurucu |
| Bu turda verilen | **Ürün mimarisi** (A4-1 … A4-4) |
| Hâlâ açık | S3 (okur gerçekten istiyor mu) → Faz 3 |
| Yeniden açılma koşulu | § 6'nın ölçümü **veya** Kitap 2 `phase1-spec` |
| En geç ne zaman kesinleşir | Kitap 2 `phase1-spec` — çünkü H3/H4 oraya aittir |

**Sert kural değişmedi:** hangi karar verilirse verilsin, basılı kitap
dijital tamamlayıcıya erişilmeden **tam işlevli** olmalıdır.

---

*Vâliçe Press · TRUE FIT · Medium Decision Framework · 28 Ağustos 2026 (Faz 1 yürütmesi)*
