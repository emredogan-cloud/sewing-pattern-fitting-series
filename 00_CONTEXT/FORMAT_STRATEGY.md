# FORMAT STRATEGY — trim, cilt, kâğıt, renk, kullanılabilirlik

> Görev talimatı § 28. Kararlar: `OPEN_QUESTIONS A5` (format) ve
> `A6` (renk) — **Faz 1 yürütmesinde KARARA BAĞLANDI**
> (`DECISIONS.md K22`, `K23`).
>
> Kanıt: `S-0009`…`S-0013` (Amazon KDP yardım sayfaları, 28 Ağu 2026).
> ⚠ Bu kayıtlar `marketplace_observation`'dır — **teknik otorite
> değildir** ve fiyatlar değişir. Hiçbiri `phase6-format` doğrulama
> kapısının yerine geçmez.

---

## 1 · Kullanılabilirlik gereksinimi — üründen türer, tercihten değil

Bu kitaplar **kesim masasında açık durur.** Okur kitabı bir yana koyar,
kalıp kâğıdını serer, ölçer, işaretler.

| # | Gereksinim | Neden | Kitap 1 | Kitap 2 |
|---|---|---|---|---|
| G1 | **Düz açık durabilme** | İki elin serbest olması gerekir | Orta | **KRİTİK** |
| G2 | **Geniş figür alanı** | Kalıp parçası diyagramı okunabilir ölçekte olmalı | **KRİTİK** | **KRİTİK** |
| G3 | **Hızlı erişim** | Bir referans atlası baştan okunmaz, aranır | Orta | **KRİTİK** |

**Kitap 1 ile Kitap 2'nin farkı budur:** Kitap 1 baştan sona okunan bir
**yöntem** kitabıdır; Kitap 2 masada açılan bir **atlastır**. G1 ve G3,
Kitap 2 için karar belirleyicidir, Kitap 1 için değildir.

## 2 · Platformun GERÇEKTEN sunduğu — doğrulandı

| Soru | Cevap | Kaynak |
|---|---|---|
| Spiral / tel sarmal cilt | **YOK.** Yalnızca yapıştırma ciltsiz ve ciltli. | `S-0013` |
| Ciltsiz trim listesi | 5×8 … 8,5×11 · 8,27×11,69 | `S-0013` |
| 8,5×11 ciltsiz sayfa aralığı | **24–590** | `S-0013` |
| Ciltli trim listesi | 5,5×8,5 · 6×9 · 6,14×9,21 · 7×10 · **8,25×11** | `S-0013` |
| Ciltli sayfa aralığı | 75–550 | `S-0013` |
| "Large trim" tanımı | genişlik > 6,12 inç **veya** yükseklik > 9 inç | `S-0009` |
| Mürekkep seçimi | **Kitap başına tek seçim** — sayfa bazlı seçmeli renk YOKTUR | `S-0009` (maliyet modeli sayfa sayısıyla çarpar) |
| Telif oranı | liste ≤ $9,98 → %50 · ≥ $9,99 → **%60** | `S-0011`, `S-0012` |
| Asgari liste fiyatı | baskı maliyeti ÷ telif oranı | `S-0011` |
| E-kitap %70 telif bandı | **$2,99 – $12,99** | `eBook List Price Requirements`, 28 Ağu 2026 |
| E-kitap teslim maliyeti (%70 seçeneği) | **$0,15/MB** (Amazon.com) | KDP dijital fiyatlandırma sayfası |

> ⚠ **Çelişki, çözülmedi:** ciltli baskı maliyeti sayfası (`S-0010`)
> premium renk ciltli oranı listeliyor; trim/kâğıt sayfası (`S-0013`)
> ciltli için yalnızca siyah mürekkep listeliyor. **P6 format kapısında
> KDP arayüzünden doğrulanacaktır.** Bu belge hiçbir yerde premium renk
> ciltlinin var olduğunu VARSAYMAZ.

### 2.1 · "Seçmeli renk" bir seçenek DEĞİLDİR

Maliyet modeli `sabit + (sayfa sayısı × sayfa başı)` biçimindedir ve
mürekkep türü **kitabın tamamı** için seçilir. On sayfası renkli bir
kitap, **tüm sayfaları** için renkli sayfa başı ücreti öder.

Bu, `A6`'nın seçenek kümesini üçe indirir: **siyah mürekkep** ·
**standart renk** · **premium renk**. "Seçici renk" stratejisi bu
platformda mevcut değildir.

## 3 · Kitap 1 ekonomisi — 8,5×11, 236 sayfa (model)

Baskı maliyeti = `sabit + sayfa × sayfa başı` · 8,5×11 **large trim**'dir.

| Mürekkep | Sayfa başı | 220 s. | **236 s.** | 260 s. | Asgari liste (%60) | **$26,99'da telif** |
|---|---|---|---|---|---|---|
| Siyah / beyaz kâğıt | $0,017 | $4,74 | **$5,01** | $5,42 | **$8,35** | **$11,18** |
| Siyah / groundwood | ≈ $0,0162 | $4,55 | $4,81 | $5,20 | $8,02 | $11,38 |
| **Standart renk** | $0,0402 | $9,84 | **$10,49** | $11,45 | **$17,48** | **$5,71** |
| **Premium renk** | $0,080 | $18,60 | **$19,88** | $21,80 | **$33,14** | **−$3,69** |

**Ciltli (8,25×11, siyah mürekkep, 236 s.):**
maliyet $5,65 + $4,01 = **$9,66** · asgari liste **$16,10** ·
$34,99'da telif **$11,33** · $39,99'da **$14,33**.

### 3.1 · Üç sonuç

**① Premium renk aritmetik olarak DIŞARIDA.**
Asgari liste fiyatı **$33,14**, gözlemlenen pazar medyanının ($21–23)
ve bu kitabın fiyat bandının üst ucunun ($28,99) **üstünde**. Bu bir
tercih değil, bir kısıttır.

**② Standart renk mümkün ama telifi YARIYA indiriyor.**
$26,99'da $11,18 → $5,71 (**−%49**). Siyah mürekkebin telifini geri
kazanmak için liste fiyatı ≈ **$36** olmalıdır — gözlemlenen bandın
çok üstünde.

**③ Ciltli sürüm ekonomik olarak ANLAMLI.**
$34,99'da ciltli telif ($11,33), $26,99'da ciltsiz telifle ($11,18)
neredeyse aynıdır. Ciltli bir **ikinci SKU** olarak gerçek bir
adaydır — ama **ayrı bir iç dosya** ister (8,25×11 ≠ 8,5×11).

## 4 · `A5` KARARI — format

| Ürün | Karar | Gerekçe |
|---|---|---|
| **Kitap 1 birincil SKU** | **8,5×11 ciltsiz · beyaz kâğıt** | G2 (geniş figür alanı) belirleyici; 236 sayfa 590 sınırının çok altında; ABD standart trim'i; rakiplerin rafıyla aynı boy |
| Kâğıt | **Beyaz** — groundwood REDDEDİLDİ | Groundwood sayfa başı ≈ %5 ucuz ama gazete kâğıdı sınıfıdır; 0,4–0,6 pt yardımcı çizgiler ve tramlar bu kâğıtta kaybolur. Kazanç kopya başına ≈ $0,20; kayıp figür okunabilirliği. |
| **Kitap 1 ikinci SKU** | **Ciltli 8,25×11 — ADAY, P6'da karara bağlanır** | Ekonomi olumlu (§ 3.1 ③); maliyeti ayrı bir iç dosyadır. Talep kanıtı yok → **ERTELENDİ** |
| **Kindle** | **ERTELENDİ — lansman sonrası** | Karar Faz 2'nin ÖLÇTÜĞÜ figür sayısına ve dosya boyutuna bağlıdır (§ 4.1) |
| **Spiral** | **KDP'de YOK — doğrulandı** | Kitap 2'nin G1/G3 gereksinimi KDP dışı bir üretim yolu ister → **Kitap 2 `phase1-spec` görevi** |
| Kitap 2 trim | 8,5×11 ciltsiz **varsayılan**, spiral fizibilitesi ayrı | R-09 |
| Kitap 3 trim | 8,5×11 ciltsiz | Uzun çizim dizileri için geniş sayfa |

### 4.1 · Kindle neden ERTELENDİ — sayılarla

Diyagram yoğun bir kitapta e-kitap ekonomisi dosya boyutuna bağlıdır:

| Senaryo | Dosya | %70 telif ($12,99) | %35 telif ($12,99) |
|---|---|---|---|
| Sabit düzen, sıkıştırılmamış | ~40 MB | $9,09 − $6,00 = **$3,09** | **$4,55** |
| Sabit düzen, optimize | ~12 MB | $9,09 − $1,80 = **$7,29** | $4,55 |
| Akışkan, optimize | ~8 MB | $9,09 − $1,20 = **$7,89** | $4,55 |

`ESTIMATE` — dosya boyutları varsayımdır; **gerçek boyut Faz 2'nin
figür motoru çalışmadan bilinemez.**

İki gerçek kısıt:
1. **Akışkan (reflowable) düzen, "bir yayılım bir kavram" kuralını
   bozar** (`STYLE.md § 5`) — kitabın `Complexity(58)` cevabının
   temelini.
2. **Sabit düzen küçük ekranda okunmaz** — 8,5×11 bir yayılım telefonda
   çalışmaz.

Bu yüzden Kindle bir **format kararı değil, bir ürün tasarımı
kararıdır** ve girdisi Faz 2'nin ölçümüdür. Ertelenmesi bir gecikme
değil, doğru sıralamadır.

## 5 · `A6` KARARI — renk

# SİYAH MÜREKKEP, BEYAZ KÂĞIT — Kitap 1 basılı sürüm

### 5.1 · Karar neden ucuzluk kararı DEĞİL

Ucuz olduğu için değil, **anlamın renge bağlı olmaması tasarlandığı
için** seçildi:

`VISUAL_STANDARD § 4` öncesi/sonrası ayrımını (`TK-12`/`TK-13`)
**renkle değil, ton ve kalınlıkla** kurar ve § 3 çizgi kalınlığını
anlam taşıyıcısı yapar (dokuz rol, 0,4–1,6 pt). Bu, renk kararından
**önce** verilmiş bir tasarım kararıdır. Sonucu şudur:

> Renk bu üründe **ikinci bir anlam kanalı değil, bir cila**dır.
> Cila için telifin %49'u verilmez.

Buna karşılık, renk **gerçekten** ikinci bir anlam kanalı olsaydı karar
tersine dönerdi — ve § 5.3'ün ölçüm kapısı tam olarak bunu sınar.

### 5.2 · Karşı argüman — kaydedilir, yok sayılmaz

Rakiplerin bir kısmı **renkli fotoğraf** kullanıyor ve alıcı bunu
bekliyor olabilir (`RISK_REGISTER R-05`). Bu karar o riski **ortadan
kaldırmaz**; iki yerde karşılar:

- **Dijital tamamlayıcı renkli olabilir** — orada marjinal maliyet
  sıfırdır (`A4`, `MEDIUM_DECISION_FRAMEWORK`).
- **Kapak tam renklidir** — kapak baskı maliyetine dâhildir; rafta
  görünen yüzey renk kaybetmez.

### 5.3 · Kararı YENİDEN AÇAN ölçüm — bir zevk tartışması değil

`A6` Faz 2'de otomatik olarak yeniden değerlendirilir, **eğer**:

> Figür sicilinde (`figures.json`) **ikinci bir anlam kanalı olmadan
> okunamayan** figürlerin oranı **%10'u aşarsa.**

Mekanik: bu figürler `manual_reason` alanında `color_required`
gerekçesiyle işaretlenir; `qa_visual.py` oranı sayar. Eşik aşılırsa
`A6` yeniden açılır ve standart renk (premium DEĞİL — § 3.1 ①) tekrar
değerlendirilir.

**Eşik neden %10:** altındaki bir oran, ilgili figürleri bölerek veya
tram/kalınlık ile yeniden tasarlayarak kapatılabilir; üstündeki bir
oran sistematik bir tasarım açığıdır.

### 5.4 · Gri tonlama — siyah mürekkebin içinde

"Siyah mürekkep" gri tonlamayı dışlamaz; talep-üzerine baskıda gri
alanlar **tram (halftone)** ile üretilir ve ince tramlar ezilebilir.
Bu yüzden `VISUAL_STANDARD § 5`'in "anlam taşımayan gri dolgu yasak"
kuralı **aynı zamanda bir baskı güvenliği kuralıdır**. Kullanılan gri
sayısı Faz 2'de **üç tonla sınırlanır** ve gerçek baskı provasında
sınanır (P6, madde 4).

## 6 · FORMAT DOĞRULAMA KAPISI — `phase6-format`, değişmedi

Bu belgedeki hiçbir sayı bir taahhüt değildir. Her kitabın
`phase6-format` fazında **zorunlu** dört adım vardır:

1. Gerçek KDP maliyet hesaplayıcısıyla baskı maliyeti **ölçülür**.
2. Seçilen trim/cilt/mürekkep seçeneğinin **mevcut olduğu** doğrulanır
   (§ 2'deki ciltli-renk çelişkisi burada çözülür).
3. **KDP Previewer'ın kendisi** çalıştırılır — yerel render başarısı
   YETERLİ DEĞİLDİR.
4. Fiziksel prova baskı alınır; G1–G3 **elle** test edilir; gri tonlar
   ve 0,4 pt çizgiler gerçek kâğıtta okunuyor mu bakılır.

**Hiçbir fiyat, telif veya format kararı bu kapıdan önce
kesinleştirilemez.**

---

*Vâliçe Press · TRUE FIT · Format Strategy · 28 Ağustos 2026 (Faz 1 yürütmesi)*
