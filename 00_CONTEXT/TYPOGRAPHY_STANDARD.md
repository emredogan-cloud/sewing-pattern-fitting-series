# TYPOGRAPHY STANDARD — yazı tipi sistemi ve lisansı

> `OPEN_QUESTIONS A7` — **Faz 1 yürütmesinde KARARA BAĞLANDI**
> (`DECISIONS.md K24`). Kalibrasyon Faz 2'nin işidir
> (`BOOK-01/00_SPEC/PHASE_2_ROADMAP.md § G1`, `G2`).
>
> ⚠ **DURUM: `DESIGN_TARGET_NOT_CALIBRATED`.** Bu belgedeki her punto
> değeri bir tasarım hedefidir, ölçülmüş sonuç değil — `VISUAL_STANDARD.md`
> ile aynı disiplin.

---

## 0 · Karar özeti

| | |
|---|---|
| **Maliyet** | **$0** — ticari yazı tipi satın alınmaz |
| **Lisans** | **SIL Open Font License 1.1** (yalnızca) |
| Metin | **Source Serif 4** |
| Başlık · tablo · figür etiketi | **Source Sans 3** |
| Figür etiketi yedeği | **Atkinson Hyperlegible** — Faz 2 testi başarısız olursa |
| Tek yazı boyu | **Yok** — hiçbir yerde tek başına punto anlam taşımaz |

## 1 · Neden lisans önce, estetik sonra

Bir kitap PDF'i yazı tipini **gömer**. KDP gömülmemiş yazı tipiyle
gönderilen bir iç dosyayı reddeder. Bu, yazı tipi seçimini bir zevk
sorusu olmaktan çıkarıp bir **hak sorusu** hâline getirir.

**Doğrulanan olgu** `OBSERVED` 28 Ağu 2026: SIL Open Font License 1.1
altındaki bir yazı tipi **ticari olarak satılan** bir belgeye
gömülebilir; gömme, lisans anlamında "dağıtım" sayılmaz ve belgenin
kendi lisansını **değiştirmez**.

Bu tek olgu, ticari yazı tipi satın alma ihtiyacını ortadan kaldırır.
`A7` bu yüzden bir bütçe kalemi **değildir**.

### 1.1 · Uyulacak üç lisans kuralı

1. **Ayrılmış Yazı Adı (Reserved Font Name)** — yazı tipi
   *değiştirilirse* adı değiştirilmelidir. Bu proje yazı tiplerini
   **değiştirmez**; kural yalnızca kayda geçirilir.
2. Yazı tiplerinin **kendisi tek başına satılamaz**. Bu proje yalnızca
   gömer.
3. Lisans metinleri `03_VISUAL/notation/` altında saklanır ve künye
   sayfasında yazı tipleri **adıyla anılır**.

## 2 · Ürünün yazı tipinden İSTEDİĞİ — dört işlevsel gereksinim

Bu gereksinimler estetik değil, **ürünün kendisinden** türer.

| # | Gereksinim | Neden bu üründe kritik |
|---|---|---|
| **Y1** | **Bayağı kesir glifleri** — ⅛ ¼ ⅜ ½ ⅝ ¾ ⅞ | ABD ev dikişinin dili kesirdir; standart dikiş payı **⅝ inç**tir. Kesir yanlış dizilirse okur yanlış payla diker ve **tüm ölçüm zinciri kayar**. |
| **Y2** | **Tablo rakamları** (sabit genişlik) | Ölçü kartı, ease tablosu ve karşılaştırma tabloları sütun hâlinde okunur |
| **Y3** | **Ayırt edilebilir rakam ve harfler** — 1/l/I, 0/O, 6/8/9 | Figür içindeki bir ölçü etiketi yanlış okunursa okurun kumaşı gider. Bu, tipografinin bu üründeki **tek gerçek risk noktasıdır**. |
| **Y4** | **Küçük puntoda ve talep-üzerine baskıda dayanıklılık** | Figür etiketleri 6–7 pt bandındadır; POD baskıda mürekkep yayılması ince tırnakları doldurur |

## 3 · Seçim ve gerekçesi

### 3.1 · Metin — **Source Serif 4**

| Ölçüt | Değerlendirme |
|---|---|
| Lisans | SIL OFL 1.1 ✓ |
| Uzun metin | Ekran ve baskı için tasarlanmış, geniş x-yüksekliği |
| **Y1 kesir** | `frac` ve `numr` OpenType özellikleri **mevcut** `OBSERVED` |
| **Y2 tablo rakamı** | ⚠ **Faz 2'de DOĞRULANACAK** — orantılı ve eski-biçim rakam desteği belgelenmiş; sabit genişlikli (`tnum`) desteği bu turda doğrulanamadı |
| Ağırlık | 8 ağırlık + değişken sürüm — başlık hiyerarşisi için fazlasıyla yeterli |
| Türkçe | Noktalı/noktasız İ-i ayrımı tam (proje belgeleri için) |

**Değerlendirilen ve elenmeyen alternatif — Charis SIL.**
SIL tarafından *düşük kaliteli baskıda okunabilirlik* için tasarlanmış
bir Charter türevidir; talep-üzerine baskı tam olarak o koşuldur.
Elenmedi, **yedek olarak adlandırıldı**: Faz 2'nin gerçek prova
baskısında Source Serif 4'ün ince tırnakları dolarsa Charis SIL'e
geçilir. Bedeli: Charis dört stil taşır (değişken sürüm yok), bu yüzden
başlık hiyerarşisi tamamen sans'a yüklenir.

**Elenen:** EB Garamond (küçük puntoda ve POD'da fazla ince),
Libre Baskerville (yüksek kontrast — aynı sorun), Literata (iyi aday,
ama Source Serif 4'ün rakam özellik seti daha eksiksiz belgelenmiş).

### 3.2 · Başlık, tablo ve figür etiketi — **Source Sans 3**

| Ölçüt | Değerlendirme |
|---|---|
| Lisans | SIL OFL 1.1 ✓ |
| Metinle ilişki | Source Serif 4 ile **aynı tasarım ailesinden** — genişlik ve x-yüksekliği uyumlu |
| **Y3 ayırt edilebilirlik** | ⚠ **Faz 2'de ÖLÇÜLECEK** — § 4 |
| **Y4 dayanıklılık** | Düşük kontrast, açık iç boşluklar |

### 3.3 · Figür etiketi yedeği — **Atkinson Hyperlegible**

Braille Institute tarafından **karakterleri birbirinden ayırmak** için
tasarlanmıştır: 1/l/I, 0/O ve 6/8/9 çiftleri kasıtlı olarak
farklılaştırılmıştır. Lisans: SIL OFL 1.1.

**Neden birinci tercih değil:** iki ailelik bir sistem, üç ailelik bir
sistemden daha tutarlıdır ve Source Sans 3 muhtemelen yeterlidir.
**Neden yedek olarak adlandırıldı:** `Y3` bu ürünün tek gerçek
tipografik riskidir ve riskin cevabı önceden yazılı olmalıdır.

**Geçiş koşulu — ölçülebilir:** § 4'ün rakam ayırt edicilik testi
başarısız olursa, **yalnızca figür içi etiketler** Atkinson
Hyperlegible'a geçer. Gövde metni ve başlıklar değişmez.

### 3.4 · Tek aralıklı (monospace) — basılı kitapta YOK

Kayıt kimlikleri (`SYM-016`, `AF-01`, `M-031`) **iç veri
kimlikleridir** ve okura gösterilmez. Basılı kitapta tek aralıklı bir
yazı tipine ihtiyaç yoktur. Dijital tamamlayıcı gerekirse
JetBrains Mono (Apache 2.0) veya IBM Plex Mono (OFL) kullanılır.

## 4 · Faz 2 doğrulama listesi — bu belge kendini SINAR

Aşağıdakiler `phase2-visual` çıkış koşullarına eklenir. Hiçbiri bu
turda yapılmadı.

| # | Test | Geçme ölçütü |
|---|---|---|
| **T1** | ⅛ ¼ ⅜ ½ ⅝ ¾ ⅞ gliflerinin gerçek render'ı | Yedisi de doğru çizilir; **⅝ ayrıca gerçek baskı provasında** okunur |
| **T2** | Ölçü tablosunda sütun hizalaması | Rakamlar hizalı; değilse `tnum` yoksa alternatif seçilir |
| **T3** | **Rakam ayırt edicilik** — 6 pt'de basılmış 1/l/I · 0/O · 6/8/9 dizisi, gerçek kâğıtta, üç kişiye okutulur | **Sıfır yanlış okuma.** Başarısızsa § 3.3 devreye girer |
| **T4** | En ince çizgi (0,4 pt `callout_leader`) + en küçük etiket, gerçek POD provasında | Çizgi kaybolmuyor, tırnak dolmuyor |
| **T5** | İnç işareti disiplini | Daktilo tırnağı `"` **hiçbir yerde** geçmiyor — § 5 |
| **T6** | PDF gömme | Bütün yazı tipleri gömülü; ön izleyici reddetmiyor |

## 5 · Sert dizgi kuralları

1. **İnç işareti daktilo tırnağı değildir.** Ya çift üvey işareti (″)
   ya `in.` yazılır. Bir ölçü kitabında `5/8"` ile `5/8″` farkı bir
   ayrıntı değil, bir kalite göstergesidir.
2. **Kesirler tek glif veya `frac` ile dizilir**, elle üst/alt simge
   kurgusuyla değil.
3. **Bir figürde tek birim** (`VISUAL_STANDARD § 7`) ve bir tabloda
   tek rakam biçimi.
4. Punto **tek başına anlam taşımaz**. Anlam çizgi kalınlığında ve
   token'dadır (`VISUAL_STANDARD § 3`). Bir etiketi büyütmek onu
   "daha önemli" yapmaz.
5. **Vurgu için ALT ÇİZGİ yok, italik var.** Alt çizgi ölçüm çizgisiyle
   karışır.
6. Figür içinde **büyük harfli uzun metin yok** — küçük puntoda
   okunabilirliği düşürür.

## 6 · Punto hedefleri — `DESIGN_TARGET_NOT_CALIBRATED`

| Rol | Hedef | Not |
|---|---|---|
| Gövde metni | 10,5 / 14,5 pt | 8,5×11 sayfada tek sütun geniş kalır; sütun kararı Faz 2 (`G2`) |
| Bölüm başlığı | 20 pt | Source Sans 3 |
| Alt başlık | 13 pt | |
| Tablo metni | 9 pt | Source Sans 3 |
| **Figür etiketi** | **7 pt** | `T3` ve `T4`'ün asıl konusu |
| Figür içi sayısal etiket | 7 pt, tablo rakamı | `TK-02`/`TK-03` okları etiketsiz çizilemez |
| Dipnot | 8,5 pt | |

**Bu tablodaki hiçbir sayı ölçülmemiştir.** Faz 2 gerçek render ve
gerçek prova baskısıyla kalibre eder.

## 7 · Ticari yazı tipi ne zaman gündeme gelir

Yalnızca `T1`–`T4`'ün **hepsi** açık lisanslı alternatiflerle
başarısız olursa. O durumda talep, `01_SOURCE/ACQUISITION_REQUEST_QUEUE.md`
biçiminde yazılır: yazı tipi · lisans türü (gömme hakkı **açıkça**) ·
maliyet · hangi testin neden başarısız olduğu · denenmiş açık
alternatifler.

**Bugün böyle bir talep YOKTUR.**

---

*Vâliçe Press · TRUE FIT · Typography Standard · 28 Ağustos 2026*
