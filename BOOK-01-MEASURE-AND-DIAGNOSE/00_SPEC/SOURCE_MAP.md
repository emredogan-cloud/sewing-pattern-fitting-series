# BOOK-01-SOURCE-MAP

> Faz 1 çıktısı 7/10. Görev talimatı § 29–30, § 36.10.
> Politika: [`../../00_CONTEXT/SOURCING_STANDARD.md`](../../00_CONTEXT/SOURCING_STANDARD.md)

---

## 0 · DÜRÜST BAŞLANGIÇ

> **Bu depoda SIFIR kaynak kaydı vardır.**
>
> Kitap 1'in 43 belirtisi, 129 aday nedeni, 32 ölçüsü ve 148 crosswalk
> kaydının **tamamı** `agent_drafted_unverified` durumundadır.
>
> Bu bir ihmal değil, bir **kayıt**tır: otoriter kalıp çizimi ve uyum
> referansları büyük ölçüde satın alınması gereken basılı kitaplardır.
> Ajan bir künye uyduramaz, hatırladığı bir ISBN'i yazamaz
> (`SOURCING_STANDARD.md § 3`).
>
> Kaynak edinim bütçesi `../../OPEN_QUESTIONS.md → A3`'te kurucu
> kararı beklemektedir ve **Faz 1'in kapanış koşuludur.**

## 1 · İddia sınıfları — hangi iddia hangi kanıtı ister

| Sınıf | Ne | Gereken kanıt | Kitap 1'deki sayı |
|---|---|---|---|
| **C-A** Ölçü tanımı | Bir ölçünün nereden nereye, hangi yolla alındığı | Antropometrik standart VEYA ≥2 bağımsız otoriter referansın uyuşması | 32 |
| **C-B** Belirti–neden bağı | Bir belirtinin hangi nedenlerden doğabileceği | Otoriter uyum referansı **+ fiziksel doğrulama** | 43 belirti / 129 bağ |
| **C-C** Ayırt edici kanıt | İki nedeni birbirinden ayıran gözlem | **Fiziksel doğrulama** (birincil) + referans (destek) | 129 |
| **C-D** Ölçüm–hipotez ilişkisi | Hangi ölçümün hangi hipotezi doğruladığı | Geometrik türetme + fiziksel doğrulama | 129 |
| **C-E** Düzeltme ailesi kapsamı | Bir ailenin hangi kalıp bölgesini nasıl değiştirdiği | Otoriter kalıp çizimi/düzeltme referansı | 19 |
| **C-F** Sıra kısıtı | Hangi düzeltmenin hangisinden önce geldiği | Geometrik türetme + fiziksel doğrulama | 5 kural + aile bazlı |
| **C-G** Ease konvansiyonu | Tipik hareket payı değerleri | **Sektör beden/ease standardı** — en kırılgan sınıf | Bölüm 3 |
| **C-H** Eleme kalemi | Kalıp dışı bir nedenin aynı belirtiyi üretmesi | Fiziksel doğrulama | 9 |

## 2 · Sınıf bazlı doğrulama stratejisi

| Sınıf | Birincil doğrulama | İkincil | Fiziksel doğrulama YETERLİ Mİ |
|---|---|---|---|
| C-A | Antropometrik/sektör standardı | Uyum referansı | **Hayır** — tanım bir konvansiyondur, deneyle bulunamaz |
| C-B | Uyum referansı | Fiziksel | Kısmen |
| C-C | **Fiziksel** | Referans | **Evet** — ayırt edicilik deneysel bir özelliktir |
| C-D | Geometrik türetme | Fiziksel | **Evet** |
| C-E | Kalıp çizimi referansı | Fiziksel | Hayır |
| C-F | Geometrik + fiziksel | Referans | **Evet** |
| C-G | **Sektör standardı** | — | **HAYIR — bu sınıf kaynak olmadan yazılamaz** |
| C-H | **Fiziksel** | — | **Evet** |

**Kritik okuma:** C-C, C-D, C-F ve C-H sınıfları (toplam iddiaların
büyük çoğunluğu) **fiziksel doğrulamayla** desteklenebilir. C-A, C-E ve
özellikle **C-G kaynak gerektirir** ve kaynak olmadan yazılamaz.

Bu, `A3` kararının üç seçeneğinden (c)'yi — "fiziksel doğrulama tek
katman olsun" — **kısmen** mümkün kılar: kapsam C-G'yi (ease
konvansiyonları) dışarıda bırakacak şekilde daraltılırsa. Bu bir
kurucu kararıdır; ajan tek başına veremez.

## 3 · Aranacak kaynak türleri

| `source_type` | Ne için | Erişim | Kitap 1'de kritik mi |
|---|---|---|---|
| `anthropometric_standard` | C-A ölçü tanımları, işaret noktaları | Kısmen açık | **Evet** |
| `industry_sizing_standard` | C-G ease ve beden konvansiyonları | Genellikle ücretli | **EVET — en kritik** |
| `fitting_reference` | C-B, C-C | Satın alma | **Evet** |
| `patternmaking_reference` | C-E, C-F | Satın alma | Evet |
| `educational_institution` | C-A, C-E destek | Kısmen açık | Destek |
| `physical_self_validation` | C-C, C-D, C-F, C-H | Kendi üretimimiz | **Evet** |
| `commercial_competitor_structural` | Yalnızca yapı analizi | Açık | **ASLA teknik kanıt değil** |

## 4 · Kaynak edinim planı — `A3` onaylanırsa

| Adım | Ne | Çıktı |
|---|---|---|
| 1 | Açık erişimli antropometrik ve kurumsal eğitim kaynaklarının taranması | `S-0001`… kayıtları, `verification_level: official_web/official_pdf` |
| 2 | Sektör beden/ease standardının erişilebilirliğinin araştırılması | C-G'nin yazılabilir olup olmadığı — **kapsam kararı** |
| 3 | Otoriter uyum ve kalıp çizimi referanslarının **kurucu-teslim istek kuyruğuna** yazılması (kardeş projelerin deseni) | Satın alma listesi + maliyet |
| 4 | Edinilen her kaynak için künye kaydı (metin DEĞİL) | `01_SOURCE/records/S-xxxx.json` |
| 5 | 129 bağın kaynağa karşı çapraz kontrolü | Çelişki listesi → `DECISIONS.md` |
| 6 | Doğrulama durumlarının yükseltilmesi | `agent_drafted_unverified` → `technical_reference_verified` |

**Adım 5 çelişki üretirse:** `SOURCING_STANDARD.md § 7` — iki otoriter
kaynak çelişirse sessizce biri seçilemez; çelişki `DECISIONS.md`'ye
açık bir bulgu olarak yazılır.

## 5 · Kaynak olmadan yazılamayacak bölümler

| Bölüm | Neden |
|---|---|
| **3.5–3.6** Ease | C-G kaynak gerektirir; tipik ease değerleri bir konvansiyondur |
| **3.1–3.2** Beden tabloları | Sektör konvansiyonu |
| **2** Ölçü tanımları | C-A; fiziksel doğrulama bir tanımı **doğrulayamaz** |

**Bu üç alan, `A3` kararının doğrudan kapsam sonucudur.** Kaynak
edinilmezse ya bu bölümler daraltılır ya kitap bir kapsam sınırı ilan
eder — ve bu, ürün metninde **açıkça** belirtilir.

## 6 · İzlenebilirlik hedefi

```
KAYNAK → ÖLÇÜ / BELİRTİ KAYDI → BÖLÜM → FİGÜR → SAYFA
                 ↓
        FİZİKSEL DOĞRULAMA (VAL-xxxx)
```

Faz 5 KA'sının bir kapısı: **"bu sayfa neden bu düzeltmeyi öneriyor?"**
sorusunun her sayfa için bir kanıt yolu olmalıdır.

---

*Vâliçe Press · TRUE FIT 1 · Source Map · 28 Ağustos 2026*
