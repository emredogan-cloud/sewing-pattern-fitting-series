# BOOK-01-VISUAL-SPEC

> Faz 1 çıktısı 6/10. Görev talimatı § 25, § 36.9.
> Seri çizim dili: [`../../00_CONTEXT/VISUAL_STANDARD.md`](../../00_CONTEXT/VISUAL_STANDARD.md)
> · token sözlüğü: `03_VISUAL/visual_language_tokens.json` (18 token)
> · tipografi: [`../../00_CONTEXT/TYPOGRAPHY_STANDARD.md`](../../00_CONTEXT/TYPOGRAPHY_STANDARD.md)
>
> **Bu belge Kitap 1'in görsel İHTİYACINI tanımlar. Hiçbir figür
> üretilmedi** — üretim Faz 2'nin (`phase2-visual`) işidir.
>
> Faz 1 yürütmesinde kapanan kararlar: `A6` (renk), `A7` (yazı tipi),
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

⚠ Bu sayılar **tahmindir**. Gerçek sayı Faz 2'de ölçülür ve
`RISK_REGISTER R-05`'in (görsel üretim hacmi) ana girdisidir.

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
düzeyindeki karşılığı artık iki kapıda birden denetleniyor —
`qa_boundary.py` (kapsama) ve **`qa_crosswalk.py § ⑨`** (yolu olmayan
belirti). Şemanın kendisi Faz 2'de `qa_visual.py` ile denetlenecek.

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

| Ölçüt | Neden |
|---|---|
| Deterministik üretilebilen figür **oranı** | Yeniden kullanım ekonomisinin temeli |
| Ortalama figür üretim süresi | `RISK_REGISTER R-05`'in gerçek büyüklüğü |
| `manual_reason` taşıyan figür sayısı | Elle çizim yükü |
| **`color_required` işaretli figür oranı** | `A6`'nın yeniden açılma eşiği (%10) |
| **`photo_required` işaretli figür sayısı** | `A11`'in yeniden açılma eşiği (6) |
| Bir yayılıma sığmayan şema sayısı | Konu bölme ihtiyacı |
| **`TK-05` ↔ `TK-06` ayırt edicilik testi** | § 4'ün teknik gerekliliği — gerçek baskıda sınanır |
| **Tipografi `T1`–`T6`** | `TYPOGRAPHY_STANDARD § 4` |

---

*Vâliçe Press · TRUE FIT 1 · Visual Spec · 28 Ağustos 2026 (Faz 1 yürütmesi)*
