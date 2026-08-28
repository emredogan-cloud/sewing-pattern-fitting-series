# BOOK-01-VISUAL-SPEC

> Faz 1 çıktısı 6/10. Görev talimatı § 25, § 36.9.
> Seri çizim dili: [`../../00_CONTEXT/VISUAL_STANDARD.md`](../../00_CONTEXT/VISUAL_STANDARD.md)
> · token sözlüğü: `03_VISUAL/visual_language_tokens.json` (18 token)
> · tipografi: [`../../00_CONTEXT/TYPOGRAPHY_STANDARD.md`](../../00_CONTEXT/TYPOGRAPHY_STANDARD.md)
>
> **FAZ 2 YÜRÜTÜLDÜ.** Bu belge artık yalnızca ihtiyacı değil, ihtiyacın
> **ÖLÇÜLMÜŞ** karşılığını da taşır. **154 figür üretildi**
> (`06_BUILD/figure_engine.py`), sicili
> `03_VISUAL/figures.json`'dadır.
>
> ⚠ **Aşağıdaki § 1 ve § 2 tahminlerinin ikisi de ÖLÇÜMLE
> DEĞİŞTİ** — `DECISIONS.md K41`. Tahminler tarihsel kayıt olarak
> korunmuş, ölçüm sonuçları yanına yazılmıştır.
>
> Faz 1'de kapanan kararlar: `A6` (renk), `A7` (yazı tipi),
> `A8` (birim), `A11` (fotoğraf).

---

## 1 · Kitap 1'in görsel yükü — türlere göre

| Tür (`figure_type`) | Tahmini sayı | Deterministik üretilebilir mi | Not |
|---|---|---|---|
| `measurement_path` | ≥32 | **Evet** — ölçü kaydından | Her `M-xxx` için en az bir |
| `body_landmark` | 7 | Kısmen | Bölge anatomi figürleri |
| `fit_sign_on_figure` | ≥43 | Kısmen | Her `SYM-xxx` için en az bir |
| `flowchart` | 9 | **Evet** — taksonomi verisinden | 7 bölge + 1 ana şema + 1 eleme |
| `toile_state` | ~6 | Kısmen | İşaretleme, kontrol noktaları |
| `pattern_piece` | ~8 | **Evet** | Kalıptan düz ölçüm alma |
| `table_graphic` | ≥12 | **Evet** | Karşılaştırma, ease, sıra |
| `comparison_before_after` | ~6 | Kısmen | Ölçüm hatası çiftleri |
| **Toplam (tahmin)** | **~123** | | |

⚠ Bu sayılar **tahmindi**. **ÖLÇÜLDÜ — Faz 2:**

| Tür | Tahmin | **ÖLÇÜLEN** | Fark |
|---|---:|---:|---|
| `flowchart` | 9 | **46** | +37 — bölge şeması sayfaya sığmıyor (§ 2) |
| `measurement_path` | ≥32 | **29** | üç türetilmiş ölçü (`M-031`–`M-033`) yol değil **hesap** figürüdür ve `table_graphic` sayıldı |
| `fit_sign_on_figure` | ≥43 | **43** | tam isabet |
| `body_landmark` | 7 | **7** | tam isabet |
| `table_graphic` | ≥12 | **9** | 6 tablo + 3 türetilmiş ölçü hesabı |
| `pattern_piece` | ~8 | **8** | tam isabet |
| `comparison_before_after` | ~6 | **6** | tam isabet |
| `toile_state` | ~6 | **6** | tam isabet |
| **Toplam** | **~123** | **154** | **+31** |

**Deterministik üretilebilen oran: %68,2** (105/154). Elle çizim
gerektiren 49 figürün tamamı `manual_reason` taşıyor ve hepsinin
gerekçesi aynı: **kumaşın gerçek dökümü kayıttan türetilemez** —
43 belirti figürü + 6 toile figürü, hepsi Faz 3'ün fiziksel
sınamasından düzeltilecek.

`RISK_REGISTER R-05`'in ilk **ölçülmüş** değeri budur.

## 2 · Kitap 1'in imza formu: AKIŞ ŞEMASI

Dokuz akış şeması bu kitabın farklılaşmasını taşıyan görsel biçimdir —
rakip mimarisi katalog, bu kitabınki akıştır.

**Yapı:**

```
  ⬭ GÖZLEM DÜĞÜMÜ (TK-17)      "Yatay kıvrım, kürek hizasında"
        │
  ◇ KARAR DÜĞÜMÜ (TK-16)       "Kol kaldırılınca kayboluyor mu?"
       ╱ ╲
   evet   hayır
     │      │
  ▭ DEVİR DÜĞÜMÜ (TK-18)       "AF-08 · Kol oyuntusu"
```

**Kurallar:**

1. Her şema **tek bir bölgeye** aittir; bölgeler arası atlama yoktur.
2. Her karar düğümü **ikili** olur — üçlü dallanma yasak.
3. Her yol ya bir **devir düğümünde** (`AF-xx`) ya bir **eleme
   kaleminde** biter. **Boşta biten yol yasak.**
4. Bir şema tek yayılıma sığmalıdır. Sığmıyorsa **konu bölünür**, şema
   küçültülmez.

**Faz 1 yürütmesinde eklenen mekanik dayanak:** kural 3'ün veri
düzeyindeki karşılığı iki kapıda denetleniyor — `qa_boundary.py`
(kapsama) ve `qa_crosswalk.py § ⑨` (yolu olmayan belirti).

### 2.1 · FAZ 2 ÖLÇÜMÜ — kural 4 uygulandı, şemanın BİRİMİ değişti

Motor önce **bölge düzeyinde** şemaları kurdu ve ölçtü. Sayfanın figür
alanı **504 × 612 pt**'dir:

| Bölge | Belirti | Gereken genişlik | Sığar mı |
|---|---:|---:|---|
| `bust_chest` | 6 | 1956 pt | **hayır** |
| `shoulder` · `waist_torso` · `crotch_leg` | 5 | 1630 pt | **hayır** |
| `upper_back` · `hip_seat` · `sleeve_arm` · `whole_garment` | 4 | 1304 pt | **hayır** |
| `neck` · `armhole` | 3 | 978 pt | **hayır** |

**On bölgenin onu da sığmıyor.** En küçüğü bile iki katından fazla yer
istiyor.

Kural 4 (*"sığmıyorsa konu bölünür, şema küçültülmez"*) uygulandı:
**akış şemasının birimi bölge değil, BELİRTİ oldu.**

**46 şema** = 43 belirti şeması + 1 bölge yönlendirici + 2 eleme
şeması. Eleme şeması da bölündü: 11 karıştırıcı sınıfı 693 pt
istiyordu; sayfa başına 9 satır sığıyor. Bölme sayısı elle yazılmadı,
**sayfa yüksekliğinden hesaplandı**.

Kural 1 korunur: bir belirti tam olarak bir bölgeye aittir.

**Boşta biten yol YAPISAL OLARAK İMKÂNSIZ.** Motor her belirti şemasını
şöyle kurar: gözlem → her aday neden için bir ikili karar → `evet`
dalı devir düğümüne (`AF-xx`) ya da eleme kalemine; **son kararın
`hayır` dalı her zaman** "Bu belirti değil — bölge şemasına dön"
düğümüne bağlanır. `qa_visual.py § ④` ayrıca denetler ve
`selftest.py` kusurlu bir fixture'la kapının **gerçekten kırmızı
yaktığını** kanıtlar.

**19/19 giriş noktası ailesine ulaşılıyor** — ölçüldü.

## 3 · Ölçüm figürleri

Her `M-xxx` için: vücut konturu (`body_outline` 1,2 pt) + iki işaret
noktası + `TK-11` ölçüm yolu + sayısal etiket alanı.

**Zorunlu:** başlangıç ve bitiş işaret noktaları **görünür** olmalı.
"Nereden nereye" sorusu figürden cevaplanabilir olmalıdır.

**Faz 1 yürütmesinin getirdiği kısıt — üç sınıf ölçü figürü:**

| Sınıf | Ölçü sayısı | Figürde ne gösterilir |
|---|---|---|
| Kaynakla doğrulanmış | **16** | Yalnızca yol ve işaret noktaları |
| Kaynağa bağlı, doğrulanmamış | 7 | Yol + **kaynak farkı notu** (ör. `M-013`: bu depo boyun tabanını, bazı konvansiyonlar tabanın 1 inç üstünü ölçer) |
| Kaynağı yok | 9 | Yol + "kalıp şirketinizin tanımını izleyin" uyarısı |

Bu üçlü ayrım, `SOURCE_MAP.md § 3`'ün doğrudan görsel sonucudur ve
Bölüm 2'nin dürüstlük taahhüdüdür: bir ölçüyü kesin diye sunmak,
kesin olmadığı yerde okuru yanıltır.

**Altı hata figürü** (Bölüm 2.6) `TK-15` do-not-do işareti taşır ve
doğru versiyonuyla **yan yana** durur (`comparison_before_after`).

## 4 · Belirti figürleri

Her `SYM-xxx` için giysi üzerinde belirtinin gösterimi:

| Belirti sınıfı | Token |
|---|---|
| Çapraz çekme çizgisi | `TK-05` — ok KAYNAĞA bakar |
| Yatay / dikey kıvrım | `TK-06` — paralel yay kümesi |
| Gerginlik / açıklık | `TK-07` — seyrek nokta tramı |
| Dikiş kayması | `TK-09` referans + kayma oku |
| Çözgü bozulması | `TK-10` + `TK-09` |

**Kritik ayrım:** `TK-05` (çekme çizgisi) ile `TK-06` (kıvrım) görsel
olarak **açıkça** farklı olmalıdır.

**Faz 1 yürütmesinin kanıtı:** bu ayrım artık bir kaynağa bağlıdır —
`S-0004` (WSU EM4582), uyumun beş temel noktasını sayarken kumaşı
**çeken** kırışıklığın *az* ease'i, **kıvrım hâlinde duran**
kırışıklığın *çok* ease'i gösterdiğini yazar. Ayrım bizim icadımız
değildir; ama gönüllü içerikte sistematik olarak karıştırılmaktadır
(`../../01_SOURCE/PUBLIC_SOURCE_SURVEY.md § 5.1`).

> Bu, `TK-05`/`TK-06` ayrımını bir **stil tercihi** olmaktan çıkarıp bir
> **teknik gereklilik** hâline getirir. İki token görsel olarak
> karışırsa kitabın en çok kullanılan kuralı çöker.

## 5 · `A11` KARARI — fotoğraf

# ÇİZGİ GRAFİĞİ YETERLİDİR. KİTAP 1 FOTOĞRAF BAĞIMLILIĞI KURMAZ.

### 5.1 · Figür türü bazında değerlendirme

| Figür türü | Fotoğrafın katkısı | Karar |
|---|---|---|
| Akış şeması | **Yok** — fotoğrafı olamaz | Çizgi grafiği |
| Ölçüm yolu | **Negatif** — el ve şerit, işaret noktasının kendisini ÖRTER; çizim ikisini birden gösterebilir | Çizgi grafiği |
| Kalıp parçası | Negatif — kâğıdın fotoğrafı çiziminden kötüdür | Çizgi grafiği |
| Öncesi/sonrası | **Negatif** — fotoğraf değişikliği İZOLE EDEMEZ; iki fotoğraf arasında ışık, duruş ve kırışıklık da değişir | Çizgi grafiği |
| Tablo, form | Yok | Çizgi grafiği |
| **Belirti tanıma** | **Yüksek** — gerçek kumaş idealize çizimden farklı görünür | **Tek gerçek aday** — § 5.3 |
| **Ölçüm hatası** | **Yüksek** — hata bir duruş/hareket meselesidir | Aday — ama `A4` bunu hareketli içerik olarak zaten işaretledi (`H1`) |

**Bulgu:** yedi türden **dördünde fotoğraf çizimden KÖTÜDÜR**, birinde
imkânsızdır, ikisinde faydalıdır. Bu, "rakipler fotoğraf kullanıyor"
gözleminin ürün gerekçesine dönüşmesini engelleyen asıl argümandır.

### 5.2 · Fotoğraf kullanılmamasının GERÇEK maliyeti — kaydedilir

`RISK_REGISTER R-05` değişmedi: rakipler gerçek vücut fotoğrafı
kullanıyor ve **alıcı fotoğraf bekliyorsa** bu bir dezavantajdır.
Bu karar o riski ortadan kaldırmaz, üstlenir.

Riski karşılayan iki şey: kapak tam renklidir; dijital tamamlayıcı
görsel taşıyabilir (`MEDIUM_DECISION_FRAMEWORK § 3`).

### 5.3 · Fotoğraf kullanılırsa — koşullar önceden yazılı

Yalnızca **belirti tanıma** için, en fazla **altı** figür, ve **beş
koşulun hepsi** sağlanırsa:

1. **Kaynak: fiziksel sınama programının kendisi.** `A13`'ün
   `Y-1` testleri zaten *bilinen bir sapmayı taşıyan gerçek kumaş*
   üretir — tam olarak ihtiyaç duyulan görüntü. **Ayrı bir çekim
   yapılmaz.**
2. **Model izni yazılı olmalı.** Tanınabilir bir kişi görünüyorsa
   yazılı izin zorunludur. Kurucu kendi görüntüsü için de bu kararı
   **açıkça** vermelidir — bu bir mühendislik kararı değildir.
3. **Fotoğraf depoya GİRMEZ.** `CONTENT_PROTECTION.md § 2` ve
   `.gitignore § ②` değişmez; görüntü yalnızca dizgi aşamasında
   yayın dosyasına girer.
4. **Hiçbir zaman tek başına durmaz.** Her fotoğrafın yanında aynı
   belirtinin `TK-05`/`TK-06` notasyonlu çizimi bulunur — fotoğraf
   *gösterir*, çizim *adlandırır*.
5. **Yasak:** internetten alınmış görsel, stok fotoğraf, izinsiz
   görüntü, marka görünen kalıp zarfı (`IP_AND_BRAND_POLICY § 1`).

### 5.4 · Sonuç

`figure_schema.json`'daki `photo_required` alanı korunur ve Faz 2'de
**en fazla altı** figürde `true` olabilir. Altıyı aşan bir talep,
`A11`'i yeniden açar.

**Karar durumu:** `A11` **KAPANDI — çizimler yeterli.** Fotoğraf
üretimi Kitap 1 için **planlanmamıştır**; koşullu bir kapı olarak
açık bırakılmıştır.

## 6 · `A6` renk kararının görsel sonuçları

Karar: **siyah mürekkep, beyaz kâğıt** (`FORMAT_STRATEGY § 5`).

| Sonuç | Ne demek |
|---|---|
| Anlam **renkle taşınmaz** | Zaten böyleydi — `VISUAL_STANDARD § 4`, `TK-12`/`TK-13` ayrımını ton+kalınlıkla kurar |
| **En fazla üç gri tonu** | Talep-üzerine baskıda ince tramlar ezilir; ton sayısı sınırlanır ve gerçek provada sınanır |
| Dijital tamamlayıcıdaki şemalar **renkli olabilir** | Marjinal maliyet sıfır (`MEDIUM_DECISION_FRAMEWORK § 3`, `D2`) |
| Yeniden açılma eşiği | `color_required` işaretli figür oranı **%10'u aşarsa** (`FORMAT_STRATEGY § 5.3`) |

## 7 · `A8` KARARI — birim sunumu

# İNÇ BİRİNCİL. FİGÜRLERDE YALNIZCA İNÇ. KARAR EŞİKLERİNDE İNÇ + CM.

### 7.1 · Kanıt

| Bulgu | Durum |
|---|---|
| Hedef pazar ABD'dir (`series_config → language: en`, rakiplerin tamamı ABD pazarı) | `FACT` |
| ABD ev dikişinin standart dikiş payı **⅝ inç**tir ve büyük kalıp yayıncılarının ortak konvansiyonudur | `OBSERVED` 28 Ağu 2026 |
| İnç sistemi **kesirle**, metrik sistem **ondalıkla** yazılır — ikisi aynı satıra karıştırılamaz | `OBSERVED` |
| Doğrulanmış kaynakların (`S-0001`, `S-0002`, `S-0003`) tamamı inç kullanıyor — ease bantları, "3 inç altı", "7–9 inç altı" | `FACT` |
| Bazı okurlar iki birimi birden istiyor | `OBSERVED` — zayıf, karışık kanıt |

### 7.2 · Karar ve sınırı

| Yüzey | Birim |
|---|---|
| **Figürler** | **Yalnızca inç.** İkinci birim eklemek etiket yoğunluğunu iki katına çıkarır ve "bir yayılım, bir kavram" kuralıyla doğrudan çatışır |
| Gövde metni | İnç birincil |
| **Karar eşikleri** (ör. `M-031` ≥ 2 inç → küçük beden) | **İnç + cm**, parantez içinde |
| Ölçü tabloları ve boş formlar | **İki sütun** — okur hangisini kullanacağına kendi karar verir |
| Ek A ölçü referansı | Çevirme tablosu |

**Neden karar eşiklerinde iki birim:** bir eşik, kitabın okura verdiği
**sayısal bir karar kuralıdır**. ABD dışındaki bir okur o kuralı
uygulayamıyorsa kitabın yöntemi ona kapanır — ve maliyeti yalnızca
birkaç parantezdir.

**Neden figürlerde tek birim:** `VISUAL_STANDARD § 7`'nin kuralı
(bir figürde birim asla karışık kullanılmaz) korunur ve etiket
yoğunluğu artmaz.

### 7.3 · Dizgi kuralı

Kesirler tek glif veya `frac` özelliğiyle dizilir; inç işareti daktilo
tırnağı **değildir** (`TYPOGRAPHY_STANDARD § 5`). ⅝ glifinin gerçek
baskıda okunması Faz 2'nin `T1` testidir.

## 8 · Sayfa yerleşimi kuralı — bir yayılım, bir kavram

Bu kural doğrudan `Complexity(58)` etiketine verilen cevaptır:

- Bir yayılımda **tek** bir kavram öğretilir.
- Belirti girişi ve figürü **aynı yayılımda** durur.
- Akış şeması **bölünmez**.
- Ölçüm figürü ve ölçüm talimatı **aynı yayılımda**.

Bu kural sayfa sayısını artırır ve bu **kabul edilmiş bir maliyettir**.

**Faz 1 yürütmesinde kazanılan alan:** `A4` sayfa başına QR alanını
kaldırdı (`MEDIUM_DECISION_FRAMEWORK § 7`); o boşluk bu kurala
harcanır.

## 9 · Faz 2'de ölçülecekler — çıkış ölçütleri

| Ölçüt | **SONUÇ** | Not |
|---|---|---|
| Deterministik üretilebilen figür **oranı** | **%68,2** (105/154) | Yeniden kullanım ekonomisinin temeli |
| Toplam figür sayısı | **154** (tahmin ~123) | `R-05`'in ilk ölçülmüş değeri |
| `manual_reason` taşıyan figür sayısı | **49** | 43 belirti + 6 toile; hepsi Faz 3'e bağlı |
| **`color_required` oranı** | **%0,0** (eşik %10) | `A6` yeniden açılmadı |
| **`photo_required` sayısı** | **0** (eşik 6) | `A11` yeniden açılmadı |
| Bir yayılıma sığmayan şema | **0** (bölmeden sonra) | Bölme öncesi: 11 |
| **`TK-05` ↔ `TK-06`** | **AYRIK** — eğrilik oranı **3,49** (eşik 2,0) | § 4'ün teknik gerekliliği; dijital ölçüm |
| **Tipografi `T1`** | ✓ ölçüldü | Kesir glifleri tam; **yedek yazı tipi elendi** (`K38`) |
| **Tipografi `T2`** | ✓ sabit sütun | Tablo motoru hizalıyor |
| **Tipografi `T3` · `T4` · `T5` · `T6`** | ⏳ **DIŞ** | `D-05`, `D-06` |
| **`G2` satır ölçüsü** | **83,0 karakter** (hedef 72–88) | Sayfa geometrisi ölçümle değişti (`K39`) |

---

*Vâliçe Press · TRUE FIT 1 · Visual Spec · 28 Ağustos 2026 (Faz 1 yürütmesi)*
