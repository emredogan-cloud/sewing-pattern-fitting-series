# IP AND BRAND POLICY

> Görev talimatı § 31–32. Araştırma raporu § 21 bu pazarın IP riskini
> **DÜŞÜK (8/10)** olarak değerlendirdi — ama düşük risk, kuralsızlık
> demek değildir.

---

## 1 · Ticari kalıp markaları — başlık ve metadata yasağı

Şu markalar **başlık, alt başlık, anahtar kelime alanı, kategori
açıklaması veya herhangi bir metadata dosyasında kullanılamaz**:

`McCall's` · `Simplicity` · `Vogue Patterns` · `Butterick` · `Burda` /
`BurdaStyle` · `New Look` · `Kwik Sew` — ve benzeri ticari kalıp
yayıncıları.

**Gerekçe:** KDP Metadata Guidelines, başlıkta ve metadata'da izinsiz
marka kullanımını açıkça yasaklar. Bu bir stil tercihi değil, bir
platform kuralıdır ve ihlali listelemenin kaldırılmasına yol açabilir.

**Mekanik koruma:** `validate_structure.py § check_brand_leak` —
`*metadata.json`, `TITLE.md`, `KEYWORDS.md`, `BLURB.md` dosyalarını
tarar. Politika/karar belgeleri (bu dosya dâhil) muaftır, çünkü yasağı
tanımlamak için markayı ADLANDIRMAK zorundadırlar.

## 2 · Yöntem telifle korunmaz, İFADE korunur

Kalıp geometrisi ve düzeltme yöntemleri **telifle korunmaz** — bunlar
teknik yöntemlerdir. Ama bir kitabın **metni, çizimleri, tabloları ve
sayfa düzeni** korunur.

| İzinli (OLGU) | Yasak (İFADE) |
|---|---|
| Bir düzeltme yönteminin geometrik mantığını öğrenmek ve **sıfırdan** anlatmak | Bir kitabın anlatım cümlelerini kopyalamak veya "kendi sözcüklerimizle" yeniden yazmak |
| Bir ölçü noktasının nerede olduğunu doğrulamak | Bir kitabın ölçü tablosunu çoğaltmak |
| Bir yöntemin var olduğunu ve adını kaydetmek | Bir kitabın diyagramını yeniden çizmek (türev eser) |
| Kendi ölçülerimizden kendi çizimimizi üretmek | Bir ticari kalıbın parçalarını dijitalleştirip yayımlamak |

**Kural:** her diyagram bu projenin kendi geometri kayıtlarından
üretilir. Hiçbir figür bir kaynaktan **izlenerek** çizilmez.

## 3 · Ticari kalıpların kullanımı

Fiziksel doğrulama için ticari kalıplar **satın alınabilir ve
kullanılabilir** — bu normal bir kullanımdır. Ama:

- Kalıbın kendisi (kâğıt veya PDF) depoya **girmez**
  (`.gitignore § ③`).
- Kalıbın talimat sayfası **çoğaltılmaz**.
- Marka adı, doğrulama kaydında bir **iç not** olarak geçebilir; ürün
  metnine veya metadata'ya **geçemez**.

## 4 · Seri adı — "TRUE FIT" YAYIMLANAMAZ

**Tarama YAPILDI** (28 Ağu 2026). Tam kanıt:
`08_REPORTS/PHASE_1_BRAND_SCREENING.md`. Karar: `DECISIONS.md K18`.

### 4.1 · Bulgu

`TRUE FIT`, **True Fit Corporation** adına yürürlükte ve **tescilli**
bir ABD markasıdır (reg. 4280126, 22 Oca 2013) ve kapsamı
"kullanıcıları **vücut ölçülerine göre** giysiyle eşleştirme"dir —
yani bu serinin **tam konusu**. Aynı sahibin `TRUE FIT RECOMMENDATION
ENGINE` (reg. 4851499) ve Sınıf 42 yazılım tescilleri de vardır.
Alan ayrıca kalabalıktır. `OBSERVED`

Kitap kategorisinde (Sınıf 16) bir tescil **bulunamadı** — ama tarama
otomatik sorguya kapalı arayüzler nedeniyle **eksiktir** ve bu,
yokluk kanıtı **değildir**.

### 4.2 · Karar

> **Ad, depo içi çalışma adı olarak korunur; kapak, metadata, alan adı
> ve dijital tamamlayıcı yüzeyinde KULLANILMAZ.**

Önerilen yerine geçen: **`BEFORE YOU CUT`** — üç eksende sıfır çakışma
bulgusu; kalabalık "FIT ___" alanının dışında; serinin kapsam sınırını
(kâğıt kalıpta, **kesmeden önce** yapılan değişiklik — § 2, `STYLE § 1`)
adın kendisi taşıyor.

### 4.3 · Hâlâ yapılması gereken

| # | İş | Kim | Ne zaman |
|---|---|---|---|
| 1 | Yerine geçen adın seçilmesi | **Kurucu** | `phase2-visual` başlangıcı |
| 2 | Seçilen ad için **profesyonel marka temizlik araştırması** | **Marka vekili** | Kapak/metadata üretiminden **önce** |

Kayıt: `OPEN_QUESTIONS A15` (**EXTERNAL PENDING**).

⚠ **Bu belgedeki değerlendirme bir hukuki görüş DEĞİLDİR.** Bir
mühendislik risk değerlendirmesidir ve profesyonel temizliğin yerine
geçmez.

### 4.4 · Ara azaltma — yapıldı

GitHub deposu **marka-nötr** bir adla açıldı; `A1` kapanmadan hiçbir ad
kamuya taahhüt edilmedi (`DECISIONS.md K32`).

## 5 · Sorumluluk sınırı

Araştırma raporu § 21: bu üründe sorumluluk riski **yok** (tıbbi/hukuki
tavsiye değil). Ama bir düzeltme diyagramının geometrik hatası okurun
kumaşını mahveder — bu bir **ürün kalitesi** meselesidir ve
`VALIDATION_PROTOCOL.md` ile yönetilir, bir hukuki risk olarak değil.

## 6 · Kaynak malzeme deposu

Telif korumalı referans malzeme (taranmış sayfa, satın alınmış kalıp,
kurs materyali) `01_SOURCE/reference_material/` altında **git'e
izlenmeden** tutulur. Kaynak KAYDI (künye) public kalır; malzemenin
KENDİSİ asla.

---

*Vâliçe Press · TRUE FIT · IP and Brand Policy · 28 Ağustos 2026*
