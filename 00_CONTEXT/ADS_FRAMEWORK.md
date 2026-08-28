# ADS FRAMEWORK — gelecekteki reklam testinin çerçevesi

> `OPEN_QUESTIONS A12` — **çerçeve Faz 1 yürütmesinde KURULDU**
> (`DECISIONS.md K28`). **Bütçe kurucu kararıdır ve verilmedi.**
>
> ⚠ **HİÇBİR KAMPANYA YÜRÜTÜLMEDİ VE YÜRÜTÜLMEYECEKTİR** (görev
> talimatı § 16, § 29). Bu belge bir plan değil, bir **karar
> çerçevesidir**: hangi veri toplanınca hangi eşikle hangi karar
> verilir.
>
> Anahtar kelime NİYET yapısı ve gerçek sorgu dizeleri:
> [`SERIES_KEYWORD_ARCHITECTURE.md`](SERIES_KEYWORD_ARCHITECTURE.md)
> — **burada tekrarlanmaz** (tek kaynak kuralı).

---

## 0 · Uydurulmayan şeyler

Bu belgede **hiçbir CPC, hiçbir dönüşüm oranı ve hiçbir gösterim
tahmini uydurulmamıştır.** Araştırma raporu § 30 ve § 36 bunları
ölçmediğini açıkça kaydetti; bu tur da ölçmedi.

Uydurulan yerine yapılan şey: **telifi doğrulamak** ve eşikleri
telifin üzerine kurmaktır. Telif artık ölçülmüş bir sayıdır
(`FORMAT_STRATEGY § 3`), bu yüzden tolere edilebilir CPC de **bir
tahmin değil, bir fonksiyondur**.

## 1 · Tek denklem

```
başabaş CPC  =  birim telif  ×  dönüşüm oranı
başabaş ACoS =  birim telif  ÷  liste fiyatı
```

Kitap 1 için birim telif **$11,18** (8,5×11, 236 s., siyah mürekkep,
$26,99 — `FORMAT_STRATEGY § 3`, kaynak `S-0009`/`S-0011`).

| Dönüşüm | Başabaş CPC | Yorum |
|---|---|---|
| %15 | **$1,68** | İyi bir ürün sayfası + yorum birikmiş |
| %10 | **$1,12** | Kitap kategorisinde iyi kabul edilen bant |
| %7 | $0,78 | |
| **%5** | **$0,56** | **Terk eşiği** — araştırma raporunun yazılı sınırı |
| %3 | $0,34 | Ücretli edinme anlamsız |

**Başabaş ACoS = 11,18 ÷ 26,99 = %41,4.**

Bu, kategorinin gözlemlenen "iyi" bandının (≈%30 altı) **üstündedir** —
yani bu üründe %30'luk bir ACoS **kârlıdır**, sadece kabul edilebilir
değil. Bu, dar bir nişte yüksek fiyatlı bir ürünün yapısal avantajıdır
ve reklam testini yapmaya değer kılan tek şeydir.

⚠ Gözlemlenen ACoS/CTR bantları `community_reference_non_authoritative`
sınıfındadır — yön verir, karar vermez.

## 2 · Hedefleme aileleri

Sorgu dizeleri `SERIES_KEYWORD_ARCHITECTURE.md § 2–4`'tedir.

### 2.1 · Birincil anahtar kelime ailesi — Kitap 1

| Aile | Niyet | Beklenen dönüşüm | Not |
|---|---|---|---|
| **Problem tarifi** | Okur sorunu hissediyor, adını bilmiyor | Düşük–orta | Huninin en geniş ağzı; en ucuz tıklama, en zayıf niyet |
| **Belirti tarifi** | Okur gördüğünü tarif ediyor | **Orta–yüksek** | **Bu ürünün en özgün eşleşmesi** — kitabın kontrollü sözlüğü tam olarak bu sorguların cevabıdır |
| **Ölçüm** | Yöntem arıyor | Orta | Bölüm 2–3 |
| **Prova** | Yöntem arıyor | Orta | Bölüm 4–5 |
| **Ürün** | Kategori arıyor | **Yüksek** | En pahalı, en rekabetçi |

### 2.2 · İkincil aileler

Kitap 2'nin **işlem niyetli** kelimeleri (adlandırılmış düzeltmeler).
Kitap 1 buraya **teşhis bağlamıyla** girer, işlem vaadiyle değil —
reklam metni "bu düzeltmeye ihtiyacınız olup olmadığını nasıl
anlarsınız" der, "bu düzeltmeyi nasıl yaparsınız" **demez**.
Sınır ihlali burada da geçerlidir (`SERIES_CONTENT_ARCHITECTURE`).

### 2.3 · Ürün hedefleme

| Öncelik | Hedef | Gerekçe |
|---|---|---|
| 1 | **Rakip uyum rehberlerinin ürün sayfaları** | Alıcı zaten kategoriyi arıyor; en yüksek niyet |
| 2 | Genel dikiş tekniği kitapları | Komşu ilgi |
| 3 | Kalıp çizim referansları | Kitap 3 için; Kitap 1'de zayıf |
| **Yasak** | Ticari kalıp markası taşıyan hiçbir alan | `IP_AND_BRAND_POLICY § 1` |

**Özellikle hedeflenecek rakip profili:** kategori liderinin ürün
sayfası. Gerekçe: bu ürünün tüm farklılaşma hipotezi, o ürünün
`Complexity(58)` etiketine verilen cevaptır. Reklamın işe yarayıp
yaramadığı **tam olarak orada** ölçülür.

### 2.4 · Kategori hedefleme

Sewing (Books) · Fashion / Craft. İki kategori, ayrı kampanya —
karıştırılırsa hangisinin çalıştığı bilinemez.

### 2.5 · Defansif hedefleme

**Kendi ASIN'imizi hedefleme.** Amacı satış değil, kendi ürün
sayfamızda rakip reklamının görünmesini pahalılaştırmaktır.

⚠ Bu, **yalnızca** organik satış tabanı kurulduktan sonra anlamlıdır —
ziyaretçisi olmayan bir sayfayı savunmak boş harcamadır. Kitap 2
yayımlanana kadar **kapalı**.

### 2.6 · Çapraz tanıtım mantığı

```
Kitap 1 satın alındı → Kitap 2 hedeflenir  (teşhis edildi, işlem lazım)
Kitap 2 satın alındı → Kitap 3 hedeflenir  (tekrardan kurtulmak)
Kitap 2 veya 3 arayan → Kitap 1 gösterilir (ön koşul konumlandırması)
```

**Kural:** çapraz tanıtım ancak **ikinci kitap yayında** anlam kazanır.
Tek kitaplık bir katalogda çapraz tanıtım kampanyası yoktur.
Bağlanma oranı ölçümü serinin `catalog` kapısına aittir
(`SERIES_ROADMAP § S5`).

## 3 · Asgari uygulanabilir lansman testi

**Bütçe dolarla DEĞİL, TIKLAMAYLA tanımlanır.** CPC bilinmiyorken
dolar bütçesi anlamsızdır; tıklama bütçesi anlamlıdır çünkü istatistiki
güç tıklama sayısına bağlıdır.

| | |
|---|---|
| **Hedef** | **300 tıklama**, üç kampanyaya bölünmüş |
| Kampanya A | Otomatik hedefleme — **CPC ve arama terimlerini KEŞFETMEK için**, satış için değil |
| Kampanya B | Belirti tarifi ailesi (§ 2.1) — bu ürünün en özgün iddiası |
| Kampanya C | Rakip ürün hedefleme (§ 2.3) — farklılaşmanın pazar testi |
| Süre | En az 14 gün, en çok 30 gün |
| **Dolar karşılığı** | CPC $0,30–$1,00 senaryo bandında **$90–$300** `ESTIMATE` |

**Neden 300 tıklama:** %5 dönüşümde beklenen sipariş ≈ 15. Bu, sıfırdan
ayırt edilebilen en küçük sayıdır. 100 tıklamada %5 ile %0 arasındaki
fark gürültüdür ve yanlış karar üretir.

**Kampanya A neden satış için değil:** CPC'yi uydurmamanın tek dürüst
yolu, onu **ölçmektir**. Otomatik kampanya bu ölçümü yapar; sonucu §1
tablosuna girdi olur.

## 4 · Durma koşulları — önceden yazılı

| # | Koşul | Karar |
|---|---|---|
| **D1** | 300 tıklama tamamlandı, dönüşüm **< %5** | **Ücretli edinme İPTAL.** Ürün organiğe bırakılır. Araştırma raporunun yazılı terk koşulu. |
| **D2** | Tek bir hedefte **100 tıklama, 0 sipariş** | O hedef kapatılır (kampanya değil, hedef) |
| **D3** | ACoS **> %41,4** ve düşüş eğilimi yok | O kampanya durdurulur — başabaşın üstünde |
| **D4** | Dönüşüm %5–%10 arası | **Devam**, ama teklif başabaş CPC'nin **%70'ini** aşamaz |
| **D5** | Dönüşüm **> %10** | Ölçekle; bütçeyi ikiye katla, tekrar ölç |
| **D6** | Ürün sayfasında **hiç yorum yokken** dönüşüm düşük | **D1'i uygulama** — önce yorum tabanı bekle; bu bir reklam sorunu değildir |

**D6 neden var:** yorumsuz bir sayfada düşük dönüşüm, reklamın değil
sayfanın ölçümüdür. D1'i o durumda uygulamak, yanlış şeyi iptal etmek
olur.

## 5 · Kurucunun harcamayı yetkilendirmesi için GEREKEN veri

Hiçbiri bugün mevcut değildir.

| # | Veri | Nereden | Faz |
|---|---|---|---|
| 1 | **Doğrulanmış birim telif** — gerçek KDP hesaplayıcısından | `phase6-format` madde 1 | P6 |
| 2 | **Nihai liste fiyatı** | P6 | P6 |
| 3 | **30 günlük organik taban** — reklamsız satış | Lansman sonrası | P7 |
| 4 | **En az birkaç yorum** | Lansman sonrası | P7 |
| 5 | **Gözlemlenen CPC** — Kampanya A'dan | § 3 | P7 |
| 6 | Fark testi **PASS** | Faz 3 kill-gate | P3 |

**6. madde bir ön koşuldur, bir tercih değil:** farklılaşma hipotezi
çürükse (kill-gate FAIL) reklam metninin dayanacağı iddia yoktur ve
harcama yapılmaz.

## 6 · Reklam metninin uyacağı kısıtlar

`CLAIMS_STANDARD.md` reklam metninde de aynen geçerlidir:

- **Sahte uzman iddiası yasak** (§ 1) — "uzman onaylı" yazılamaz.
- **Basılı üstünlük iddiası yasak** (§ 2) — bu iddia sınandı ve
  ZAYIF çıktı; reklam metni ona dayanamaz.
- **Pazar rakamları ürün metnine giremez** (§ 4) — yorum sayısı, BSR,
  "en çok satan" ifadeleri.
- **Sonuç garantisi yok** (§ 5) — "her kalıp size oturacak" yazılamaz.
- **Ticari kalıp markası hiçbir metadata yüzeyinde geçemez**
  (`IP_AND_BRAND_POLICY § 1`, mekanik: `check_brand_leak`).
- **Seri adı** — `A1` kapanmadan hiçbir marka adı reklam metnine
  yazılmaz (`08_REPORTS/PHASE_1_BRAND_SCREENING.md`).

## 7 · Bu çerçevenin ölçMEDİĞİ

Reklam testi **satın alma niyetini** ölçer. Şunları ölçmez:
farklılaşmanın algılanması (→ Faz 3 fark testi) · teknik doğruluk
(→ fiziksel doğrulama) · seri bağlanma oranı (→ `catalog` kapısı).

Bu sınırların karıştırılması, ticari bir sayının teknik bir kanıt gibi
kullanılmasına yol açar — `SOURCING_STANDARD § 1`'in
`marketplace_observation` yasağının tam olarak engellediği şey.

---

*Vâliçe Press · TRUE FIT · Ads Framework · 28 Ağustos 2026*
