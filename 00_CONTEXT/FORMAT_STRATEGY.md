# FORMAT STRATEGY — trim, cilt, kâğıt, kullanılabilirlik

> Görev talimatı § 28. **Bu belge kararı VERMEZ.** Format seçenekleri,
> kullanılabilirlik gereksinimleri ve doğrulama kapısını tanımlar.
> Kararlar: `OPEN_QUESTIONS A5`, `A6`.

---

## 1 · Kullanılabilirlik gereksinimi — üründen türer, tercihten değil

Bu kitaplar **kesim masasında açık durur.** Okur kitabı bir yana koyar,
kalıp kâğıdını serer, ölçer, işaretler. Bu, üç somut gereksinim üretir:

| # | Gereksinim | Neden |
|---|---|---|
| G1 | **Düz açık durabilme** | İki elin serbest olması gerekir |
| G2 | **Geniş figür alanı** | Kalıp parçası diyagramı okunabilir ölçekte olmalı (`visual_language_tokens.json § min_figure_width_in`) |
| G3 | **Hızlı erişim** | Özellikle Kitap 2 bir REFERANS ATLASIDIR — okur bir girişi arar, baştan okumaz |

G1 ve G3 en güçlü şekilde **Kitap 2** için geçerlidir.

## 2 · Gözlemlenen pazar kanıtı

| Gözlem | Durum |
|---|---|
| Kendi kendine yayımlayan bir yazar aynı anda $28,95 ciltsiz **ve $64,50 spiral** SKU sürdürüyor | `OBSERVED` 27 Ağu 2026 |
| Bir seri (Palmer/Pletsch) spiral ciltli çalışıyor | `OBSERVED` |
| Fiyat bandı $18,55–$45,50, medyan ~$21–23 | `OBSERVED` |

Araştırma raporu § 31 spiral SKU'nun Kitap 2'nin birim telifini
$11,97 → $21,57'ye çıkarabileceğini modelledi — **serinin ekonomisini
tek başına değiştirebilecek bir kalem.**

⚠ **Ama:** raporun § 36 sınırlamalar bölümü açıkça kaydediyor —
**KDP'de spiral üretim seçeneğinin varlığı ve maliyeti DOĞRULANMADI.**
Rakibin $64,50 spirali gözlemlendi; bunun KDP üzerinden mi başka bir
baskı yoluyla mı üretildiği bilinmiyor.

## 3 · Karar bekleyen sorular

| Soru | Kayıt | En geç |
|---|---|---|
| Trim boyutu (8,5×11 varsayımı doğrulanacak) | `A5` | Kitap 1 `phase2-visual` |
| Renk stratejisi (S/B mi, gri tonlama mı, renk mi) | `A6` | Kitap 1 `phase2-visual` |
| Spiral SKU gerçekten mümkün mü, maliyeti ne | `A5` | Kitap 2 `phase1-spec` |
| Kâğıt cinsi (beyaz/krem, gramaj) | `A5` | Kitap 1 `phase6-format` |
| Kindle/e-kitap sürümü var mı | `A5` | Kitap 1 `phase6-format` |

## 4 · FORMAT DOĞRULAMA KAPISI

Her kitabın `phase6-format` fazında **zorunlu** bir kapı vardır:

1. Gerçek KDP maliyet hesaplayıcısıyla baskı maliyeti **ölçülür**
   (varsayılmaz).
2. Seçilen trim/cilt seçeneğinin KDP'de **mevcut olduğu** doğrulanır.
3. KDP Previewer'ın **kendisi** çalıştırılır — yerel render başarısı
   YETERLİ DEĞİLDİR (kardeş projelerden devralınan kural).
4. Fiziksel prova baskı alınır ve G1–G3 gereksinimleri **elle** test
   edilir.

**Hiçbir fiyat, telif veya format kararı bu kapıdan önce
kesinleştirilemez.** Araştırma raporunun tüm ekonomi tablosu
`ESTIMATE` etiketlidir.

## 5 · Renk kararının gizli maliyeti

Renkli baskı KDP'de belirgin biçimde daha pahalıdır ve fiyat bandı
medyanı $21–23'tür. Bu ürünün diyagramları **saf çizgi grafiğidir**
(araştırma raporu § 22) — renk **teknik olarak gerekli değildir**.

Ama `TK-12`/`TK-13` (öncesi/sonrası durumu) renk olmadan da ayırt
edilebilir olmalıdır: bu yüzden görsel standart öncesi/sonrası ayrımını
**renkle değil, ton ve kalınlıkla** kurar. Bu, renk kararı hangi yöne
giderse gitsin geçerli kalan bir tasarım seçimidir.

---

*Vâliçe Press · TRUE FIT · Format Strategy · 28 Ağustos 2026*
