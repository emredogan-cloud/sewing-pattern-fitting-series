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

## 4 · Seri adı — "TRUE FIT" ÇALIŞMA ADIDIR

Araştırma raporu § 29 ve § 35 madde 7 bunu açıkça bir **zorunlu kontrol
maddesi** olarak işaretledi.

**Kapak veya metadata kesinleşmeden ÖNCE yapılması zorunlu:**

1. Kitap kategorisinde marka çakışması taraması
2. Amazon'da aynı/benzer seri adı taraması
3. Yayıncılık kategorisi çakışma kontrolü
4. Adın hedef pazarda uygunluğu

Karar: `OPEN_QUESTIONS A1`. **Bu tarama bu turda YAPILMADI.**

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
