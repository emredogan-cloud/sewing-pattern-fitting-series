# BOOK-01-SOURCE-MAP

> Faz 1 çıktısı 7/10. Görev talimatı § 29–30, § 36.10.
> Politika: [`../../00_CONTEXT/SOURCING_STANDARD.md`](../../00_CONTEXT/SOURCING_STANDARD.md)
>
> Tarama kaydı: [`../../01_SOURCE/PUBLIC_SOURCE_SURVEY.md`](../../01_SOURCE/PUBLIC_SOURCE_SURVEY.md)
> · İstek kuyruğu: [`../../01_SOURCE/ACQUISITION_REQUEST_QUEUE.md`](../../01_SOURCE/ACQUISITION_REQUEST_QUEUE.md)

---

## 0 · DURUM — 28 Ağustos 2026, Faz 1 yürütmesi sonrası

Bu belgenin ilk sürümü şöyle başlıyordu: *"Bu depoda SIFIR kaynak
kaydı vardır."* O cümle artık doğru değildir.

| | Faz 1 başlangıcı | **Faz 1 sonu** |
|---|---|---|
| Kaynak kaydı | 0 | **15** |
| Teknik otorite + tam metin okunmuş | 0 | **6** |
| Doğrulanmış ölçü | 0 / 32 | **16 / 32** |
| Doğrulanmış düzeltme ailesi | 0 / 19 | **13 / 19** |
| Doğrulanmış belirti | 0 / 43 | **0 / 43** — *bilinçli* |
| Ücretli kaynak satın alındı | — | **0** |

**Belirti kayıtlarının sıfırda kalması bir eksiklik değil, taramanın
en net bulgusudur** ve § 6'da gerekçelendirilir.

## 1 · İddia sınıfları — hangi iddia hangi kanıtı ister

| Sınıf | Ne | Gereken kanıt | Kitap 1'deki sayı | **Faz 1 sonu durumu** |
|---|---|---|---|---|
| **C-A** Ölçü tanımı | Bir ölçünün nereden nereye, hangi yolla alındığı | Antropometrik standart VEYA ≥2 bağımsız otoriter referansın uyuşması | 32 | **KAMU KAYNAĞIYLA DOĞRULANDI (16) · KISMİ (7) · DIŞ KAYNAK GEREKLİ (9)** |
| **C-B** Belirti–neden bağı | Bir belirtinin hangi nedenlerden doğabileceği | Otoriter uyum referansı + fiziksel doğrulama | 43 belirti / 129 bağ | **KISMİ** — bağlam kaynağa bağlandı, bağın kendisi bağlanmadı |
| **C-C** Ayırt edici kanıt | İki nedeni birbirinden ayıran gözlem | **Fiziksel doğrulama** (birincil) + referans (destek) | 129 | **DOĞRULANMADI** — Faz 3'e ait |
| **C-D** Ölçüm–hipotez ilişkisi | Hangi ölçümün hangi hipotezi doğruladığı | Geometrik türetme + fiziksel doğrulama | 129 | **DOĞRULANMADI** — Faz 3'e ait |
| **C-E** Düzeltme ailesi kapsamı | Bir ailenin hangi kalıp bölgesini nasıl değiştirdiği | Otoriter kalıp düzeltme referansı | 19 | **KAMU KAYNAĞIYLA DOĞRULANDI (13) · KISMİ (4) · YOK (2)** |
| **C-F** Sıra kısıtı | Hangi düzeltmenin hangisinden önce geldiği | Geometrik türetme + fiziksel doğrulama | 5 kural + aile bazlı | **2/5 KAMU KAYNAĞIYLA DOĞRULANDI** (`S-0003`) |
| **C-G** Ease konvansiyonu | Tipik hareket payı değerleri | Sektör beden/ease standardı | Bölüm 3 | **TEK KURUMSAL KONVANSİYONLA YAZILABİLİR** (`S-0001`) — bkz. § 5 |
| **C-H** Eleme kalemi | Kalıp dışı bir nedenin aynı belirtiyi üretmesi | Fiziksel doğrulama | 9 | **DOĞRULANMADI** — Faz 3'e ait |

## 2 · Elde tutulan kaynaklar

| Kayıt | Kaynak | Tür | Seviye | Otorite |
|---|---|---|---|---|
| `S-0001` | NMSU Guide C-228 *Pattern Alteration* | `educational_institution` | `fulltext` | ✅ |
| `S-0002` | NMSU Guide C-227 *Making Perfect Pants* | `educational_institution` | `fulltext` | ✅ |
| `S-0003` | Texas AgriLife E-372 *Principles of Pattern Alteration* | `educational_institution` | `fulltext` | ✅ |
| `S-0004` | WSU Extension EM4582 *Challenging Patterns* | `educational_institution` | `fulltext` | ✅ |
| `S-0005` | ANSUR II — NATICK/TR-15/007 | `anthropometric_standard` | `fulltext` | ✅ |
| `S-0006` | NHANES 2021 Anthropometry Procedures Manual | `anthropometric_standard` | `official_pdf` | ✅ |
| `S-0007` · `S-0008` | MSU Extension E-419 / E-421 | `educational_institution` | `official_web` | ✅ ama **kanıt değil** (§ 4) |
| `S-0009`…`S-0013` | Amazon KDP yardım sayfaları | `marketplace_observation` | `official_web` | ❌ **asla teknik otorite değil** |
| `S-0014` · `S-0015` | ISO 8559-1 · ASTM D5219 | `industry_sizing_standard` | `not_yet_acquired` | ✅ ama **edinilmedi** |

## 3 · C-A — ölçü bazlı doğrulama tablosu

### Doğrulandı — `technical_reference_verified` (16)

| Ölçü | Kaynak | Ne eşleşti |
|---|---|---|
| `M-001` üst göğüs | `S-0001`, `S-0003` | Kolların hemen altından, göğsün üzerinden, sırtta en dolgun noktadan |
| `M-002` göğüs | `S-0001`, `S-0003` | En dolgun noktadan |
| `M-003` göğüs altı | `S-0001` | Göğsün hemen altından |
| `M-005` üst kalça | `S-0002`, `S-0003` | Belin 3 inç altı (bu depodaki 7–10 cm bandıyla uyumlu) |
| `M-006` kalça | `S-0001`, `S-0002` | En dolgun nokta, belin 7–9 inç altı |
| `M-007` pazu | `S-0001` | Koltuk altı hizasında üst kol çevresi |
| `M-009` uyluk | `S-0001`, `S-0003` | Belin 9 inç altı, tek bacağın en dolgun yeri |
| `M-014` omuz uzunluğu | `S-0001`, `S-0003`, `S-0005` | ANSUR (70): trapezius → acromion |
| `M-016` arka boy | `S-0001`, `S-0003` | Ense çıkıntısı → bel |
| `M-020` sırt genişliği | `S-0003`, `S-0005` | ANSUR (54) INTERSCYE I: arka koltuk altı kıvrımları arası |
| `M-023` bel–kalça | `S-0002` | Yandan, bel → kalçanın en dolgun yeri |
| `M-024` bel–yer | `S-0002`, `S-0003` | Bel → yer |
| `M-026` ağ derinliği | `S-0002`, `S-0003` | Otururken, yandan bel → oturma yüzeyi |
| `M-027` ağ uzunluğu | `S-0002`, `S-0003` | Ön bel → ağ → arka bel |
| `M-029` omuz–dirsek | `S-0001`, `S-0003` | Omuz üstü → dirseğin dış ortası |
| `M-031` göğüs–üst göğüs farkı | `S-0003` | **≥ 2 inç ise küçük beden seçilir** — sayısal karar kuralı |

### Kaynağa bağlı ama YÜKSELTİLMEDİ (7)

| Ölçü | Kaynak | Neden yükseltilmedi |
|---|---|---|
| `M-004` doğal bel | `S-0002`, `S-0003` | Hiçbir kaynak "en dar nokta" yol kuralını yazmıyor. `S-0005`/`S-0006` **farklı bir bel** tanımlıyor. |
| `M-008` bilek | `S-0001` | Kaynak bileği *elin en geniş yeri* olarak ölçüyor — farklı amaç, farklı sayı |
| `M-013` boyun tabanı | `S-0001` | Kaynak *tabanın 1 inç üstünü* ölçüyor |
| `M-015` ön orta boy | `S-0003` | Kaynağın "shoulder to waist"i bizim boğaz çukuru → bel ölçümüz değil |
| `M-017` omuz–apeks | `S-0003` | Kaynağın başlangıcı omuz, bizimki yan boyun noktası |
| `M-025` iç bacak | `S-0001` | Kaynak ayak bileğinde bitiriyor, bizimki yerde |
| `M-028` kol boyu | `S-0001`, `S-0003` | Yol kuralı (bükük dirsek üzerinden) hiçbir kaynakta yok |

### Kaynağı YOK (9)

`M-010` diz · `M-011` baldır · `M-018` apeks arası · `M-019` apeks–bel ·
`M-021` ön genişlik · `M-022` kol oyuntusu derinliği · `M-030` boy ·
`M-032` ön/arka boy farkı · `M-033` bel–kalça düşüşü

*(son ikisi türetilmiştir; kaynakları yükselmeden yükselemezler)*

**Kapanma yolu:** `A-01` (ISO 8559-1) veya Faz 2'de elle indirilecek
TAMU E-373 *Personal Measurement Chart*. İkisi de bugün gerekli değildir.

## 4 · C-E — düzeltme ailesi doğrulama tablosu

| Doğrulandı (13) | Kaynak | Kaynakta karşılığı |
|---|---|---|
| `AF-01` | `S-0001` | Full Bust / Small Bust |
| `AF-02` | `S-0001` | High Bust / Low Bust (pens hizası) |
| `AF-03` | `S-0001`, `S-0003` | Sloping / Square Shoulders |
| `AF-04` | `S-0001` | Broad / Narrow Shoulders |
| `AF-06` | `S-0001` | Small Neck / Large Neck / Gaping Neckline |
| `AF-07` | `S-0001`, `S-0003` | Round Shoulders / Broad Back / Narrow Back |
| `AF-09` | `S-0001` | Sleeve Cap Too Narrow; kol başı yüksekliğinin geri kazanılması |
| `AF-10` | `S-0001` | Small Arm / Large Arm / Large Upper Arm |
| `AF-13` | `S-0001`, `S-0002` | Protruding / Flat Derriere; Wide Hips; Flat Side Hip |
| `AF-14` | `S-0001`, `S-0003` | Sway Back (beden + etek + pantolon) |
| `AF-15` | `S-0001`, `S-0002` | Ağ dikişi ve iç bacak boyunun yeniden çizilmesi |
| `AF-17` | `S-0001`, `S-0002` | Bulging Thighs |
| `AF-19` | `S-0001`, `S-0003` | Kalıptaki hazır uzatma/kısaltma çizgilerinin kullanılması |

| Kısmi (4) | Neden yükseltilmedi |
|---|---|
| `AF-08` kol oyuntusu | Kaynaklar kol oyuntusunu *başka* düzeltmelerin yan etkisi olarak yeniden çiziyor; bağımsız derinlik/şekil girişi yok |
| `AF-11` gövde boyu ve denge | Ön/arka denge ayrı bir aile olarak tanımlı değil |
| `AF-16` ağ eğrisi şekli | `AF-15`'ten ayrı izole edilmiyor |
| `AF-18` beden dereceleme | `S-0003` beden **seçimi** veriyor, dereceleme değil |

| Kaynağı yok (2) | Not |
|---|---|
| `AF-05` öne kaymış omuz | Hiçbir kamu kaynağında yok — `A-03` adayı |
| `AF-12` bel çevresi | Aynı |

## 5 · C-G — ease: "yazılamaz"dan "adı konmuş konvansiyonla yazılabilir"e

Bu belgenin ilk sürümü `C-G`'yi **kaynak olmadan yazılamaz** diye
işaretlemiş ve bunu Bölüm 3.5–3.6'nın kapsam sonucu saymıştı.

`S-0001` Table 1 bir kurumsal ease bandı tablosu taşır ve tablonun
kendisi şu uyarıyla gelir: *ease miktarları kalıp talimatına, kumaşa
ve kişisel tercihe göre değişir.*

**Karar (`DECISIONS.md K21`):** Bölüm 3.5–3.6 yazılabilir, **üç sert
koşulla**:

1. Sayısal bant verildiğinde kaynağı **adıyla** anılır; anonim bir
   "standart" gibi sunulmaz.
2. Bandın **tek bir kurumun konvansiyonu** olduğu ve kalıp şirketleri
   arasında değiştiği okura **açıkça** söylenir.
3. Kitabın ease üzerine kurduğu **yöntem** (bitmiş ölçü − vücut ölçüsü =
   ease; ease tasarımın kendisi olabilir) sayısal banttan **bağımsız**
   kalır — bant düşse bile bölüm ayakta kalır.

Bu üç koşul, ISO/ASTM edinilirse bandın **değiştirilebilir** olmasını
da garanti eder.

## 6 · Belirti kayıtları neden yükseltilMEDİ — taramanın en önemli bulgusu

Elde tutulan altı kaynağın hepsi **figür tipinden düzeltmeye** gider:
"kaykık omzunuz varsa şunu yapın." Hiçbiri **belirtiden nedene**
gitmez ve — daha kritik olarak — **hiçbiri aynı belirtinin iki
nedenini birbirinden ayırmaz.**

Bir belirti kaydının çekirdek iddiası tam olarak budur (`C-C`).
Kayıt bağlamı (gözlem, bölge, sınıf) kaynağa bağlanabilir; **ayırt
edicilik bağlanamaz.**

Bu yüzden 43 kaydın hepsi `agent_drafted_unverified` kaldı ve her birine
kural tabanlı `source_refs` eklendi:

| Kural | Eklenen kaynak |
|---|---|
| `sign_class` ∈ {yatay kıvrım, dikey kıvrım, çapraz çekme, gerginlik, açıklık, havuzlanma} | `S-0004` (fazlalık ↔ yetersizlik ayrımı) |
| `sign_class` ∈ {dikiş kayması, çözgü bozulması, etek ucu yükselmesi, siluet sapması} | `S-0003` + `S-0004` (uyum kontrol listesi) |
| `zone` = kalça/oturak veya ağ/bacak | `S-0002` |
| diğer bölgeler | `S-0001` |

**Bu, kanıt zincirinin izlenebilir olması içindir** (`SOURCING_STANDARD § 8`)
— yükseltme kanıtı değildir. Mekanik ayrım: `selftest.py §
test_verification_status_is_honestly_recorded` yükseltilmiş her kaydın
gerçekten `fulltext`/`official_pdf` bir kaynağı olduğunu denetler.

`S-0007` ve `S-0008` (taranmış MSU arşivleri) bilerek `official_web`
seviyesinde tutuldu: okunmamış bir belge yükseltme kanıtı olamaz.

## 7 · Kaynaklar arası tanım farkları — sessizce ezilmedi

`SOURCING_STANDARD § 7` gereği. Dördü de `PUBLIC_SOURCE_SURVEY § 7`'de
tam olarak kayıtlıdır: `M-004` (bel: doğal ↔ göbek ↔ iliak),
`M-008` (bilek ↔ el), `M-013` (boyun tabanı ↔ 1 inç üstü),
`M-025` (yer ↔ ayak bileği).

**Hiçbiri "düzeltilmedi".** Dördü de Bölüm 2'nin öğretim malzemesine
dönüştü: *bir ölçünün adı yetmez; nereden nereye ölçüldüğü ölçünün
kendisidir.*

## 8 · Kaynak olmadan yazılamayacak bölümler — güncellenmiş

| Bölüm | İlk durum | **Şimdi** |
|---|---|---|
| **3.5–3.6** ease | Yazılamaz | **Yazılabilir** — § 5'in üç koşuluyla |
| **3.1–3.2** beden tabloları | Yazılamaz | **Kısmen** — beden *seçim kuralı* `S-0003`'ten doğrulandı; beden *tabloları* hâlâ kalıp şirketine aittir ve kitapta çoğaltılmaz |
| **2** ölçü tanımları | Yazılamaz | **16 ölçü tam · 7 kısmi · 9 açık** — açık olanlar Bölüm 2'de "bu ölçüyü kalıp şirketinizin tanımına göre alın" biçiminde işaretlenir |

## 9 · İzlenebilirlik hedefi

```
KAYNAK → ÖLÇÜ / BELİRTİ KAYDI → BÖLÜM → FİGÜR → SAYFA
                 ↓
        FİZİKSEL DOĞRULAMA (VAL-xxxx)
```

Faz 5 KA'sının bir kapısı: **"bu sayfa neden bu düzeltmeyi öneriyor?"**
sorusunun her sayfa için bir kanıt yolu olmalıdır.

Faz 1 sonunda bu zincirin **ilk iki halkası** kuruldu (kaynak → kayıt).
Üçüncü halka (kayıt → bölüm) `CHAPTER_SPECS.md`'nin kaynak satırlarıyla
kuruldu. Dördüncü ve beşinci halka Faz 2'nin işidir.

---

*Vâliçe Press · TRUE FIT 1 · Source Map · 28 Ağustos 2026 (Faz 1 yürütmesi)*
