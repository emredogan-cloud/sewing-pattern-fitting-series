# SOURCING STANDARD — teknik kaynak disiplini

> Görev talimatı § 9, § 29–30. Makine-okunur şema:
> `01_SOURCE/source_schema.json`. Mekanik denetim:
> `validate_spec.py § check_source_*`.

---

## 1 · Dokuz katmanlı kaynak modeli

| `source_type` | Ne için | Teknik otorite mi |
|---|---|---|
| `patternmaking_reference` | Blok/kalıp çizim yöntemi, geometri | ✅ |
| `fitting_reference` | Uyum teşhisi, düzeltme yöntemi | ✅ |
| `anthropometric_standard` | Vücut ölçü tanımları, işaret noktaları | ✅ |
| `industry_sizing_standard` | Beden tabloları, ease konvansiyonları | ✅ |
| `educational_institution` | Ders materyali, kurumsal eğitim kaynağı | ✅ |
| `physical_self_validation` | Bu projenin KENDİ fiziksel testi (`VAL-xxxx`) | ✅ (kendi kapsamında) |
| `commercial_competitor_structural` | Rakip ürün yapısı, müşteri şikâyeti | ❌ **asla** |
| `marketplace_observation` | Amazon listeleme/BSR/yorum sayısı | ❌ **asla** |
| `community_reference_non_authoritative` | Forum, blog, gönüllü içerik | ❌ **asla** |

**Mekanik kural:** son üç tür `technical_authority: true` taşıyamaz —
`check_source_type_authority_consistency` bunu her kayıtta denetler.

Bu, görev talimatının uyarısının doğrudan uygulamasıdır: rakip ürün
metni veya pazar gözlemi **teknik kanıt değildir**.

## 2 · Kayıt KÜNYEDİR, metin DEĞİL

Bir kaynak kaydı yalnızca künye taşır (yazar, başlık, yayıncı, baskı,
locator). Kaynağın **metni, tabloları, çizimleri veya kalıpları** bu
depoya ASLA girmez. Telif korumalı malzeme
`01_SOURCE/reference_material/` altında **git'e izlenmeden** tutulur
(`.gitignore § ③`).

## 3 · Locator disiplini

`locator` alanı yalnızca kaynak **gerçekten görüldüyse** doldurulur.
Sayfa numarası, bölüm adı veya ISBN **uydurulmaz** ve **hatırlanan bir
değerle doldurulmaz** — görülmediyse `null` kalır.

Mekanik koruma: `check_source_locator_discipline` —
`verification_level` `not_yet_acquired`/`unverifiable` iken dolu bir
`locator` bir HATADIR.

## 4 · Doğrulama seviyeleri

```
fulltext  >  official_pdf  >  official_web  >
marketplace_listing_observed  >  secondary_citation  >
not_yet_acquired  >  unverifiable
```

Bir taksonomi kaydının `technical_reference_verified` olabilmesi için
en az bir kaynağının `fulltext` veya `official_pdf` seviyesinde olması
GEREKİR (`check_verification_evidence`).

## 5 · Kayıt doğrulama durumları — dört basamak

| Durum | Anlamı | Gerektirdiği kanıt |
|---|---|---|
| `agent_drafted_unverified` | Ajan yazdı, hiçbir dış doğrulama yok | — |
| `agent_reviewed` | Bağımsız çelişmeli inceleme geçti | İnceleme raporu |
| `technical_reference_verified` | Otoriter bir kaynağa bağlandı | ≥1 `fulltext`/`official_pdf` kaynak |
| `physically_validated` | Gerçekten dikildi ve sınandı | `VAL-xxxx` kaydı |

**Faz 1 YÜRÜTMESİ sonundaki gerçek durum (28 Ağu 2026):**

| Kayıt türü | Toplam | `technical_reference_verified` | Kaynağa bağlı, yükseltilmemiş | Kaynağı yok |
|---|---|---|---|---|
| Ölçü (`M-xxx`) | 32 | **16** | 7 | 9 |
| Düzeltme ailesi (`AF-xx`) | 19 | **13** | 4 | 2 |
| Belirti (`SYM-xxx`) | 43 | **0** | 43 | 0 |
| Blok bileşeni (`BLK-xx`) | 12 | 0 | 0 | 12 |

**Belirti kayıtlarının sıfırda kalması bilinçlidir.** Bir belirti
kaydının çekirdek iddiası aynı belirtinin iki nedenini ayıran
kanıttır ve **hiçbir kamu kaynağı bu ayrımı yapmaz** — bu sınıfın
birincil doğrulaması FİZİKSELDİR (Faz 3).

**Kaynağa bağlı ama yükseltilmemiş** bir kayıt, kaynağın kaydın
BAĞLAMINI desteklediğini ama ÇEKİRDEK İDDİASINI tanımlamadığını
gösterir. Mekanik ayrım:
`selftest.test_verification_status_is_honestly_recorded` (`K20`).

## 6 · Kaynak EDİNİMİ bir kurucu kararıdır

**Sıralama kuralı: KAMU KAYNAĞI ÖNCE.** Bir kalem ancak kamu
taraması tükendikten sonra satın alma kuyruğuna girebilir.

Faz 1 yürütmesi bu kuralın işe yaradığını gösterdi: yedi eksende
yapılan tarama **15 kaynak kaydı** üretti (altısı teknik otorite +
tam metin) ve Faz 1 **hiçbir ücretli kaynak satın alınmadan**
kapandı (`DECISIONS.md K19`).

Faz 2 üç kayıt daha ekledi (**güncel toplam 18**): `S-0016` KDP baskı
gereksinimleri, `S-0017` Adobe Source yazı tipleri, `S-0018` yedek yazı
tipi adayları. **Üçü de `technical_authority: false`'tur** ve öyle olmak
zorundadır: platform dokümantasyonu ve yazı tipi künyesi teknik otorite
DEĞİLDİR. Teknik otorite sayısı **altı** olarak kaldı.

| Belge | Ne |
|---|---|
| `01_SOURCE/PUBLIC_SOURCE_SURVEY.md` | Ne arandı, ne bulundu, ne reddedildi ve **neden** |
| `01_SOURCE/ACQUISITION_REQUEST_QUEUE.md` | Ücretli kalemler — her biri dokuz alan taşır ve **hangi fazda gerçekten gerekli olduğu** yazılıdır |

Bir kalem kuyruğa girmeden önce: ① bir kayıt doğrulanamıyor olarak
işaretlenmeli, ② o boşluk için yapılmış bir kamu taraması kayıtlı
olmalı, ③ dokuz alan doldurulmalı, ④ `not_yet_acquired` bir kayıt
açılmalı (`locator` **null**).

## 7 · İkincil kaynak birincili SESSİZCE EZEMEZ

İki otoriter kaynak çelişirse, çelişki `DECISIONS.md`'ye açık bir bulgu
olarak yazılır. Hiçbir ajan sessizce birini tercih edip devam edemez.

Bu, kalıp çiziminde **özellikle** önemlidir: farklı çizim sistemleri
(farklı okullar, farklı ülkeler) aynı sonuca farklı geometrilerle
ulaşır ve bunlardan biri "yanlış" değildir. Kitap 3'ün hangi sistemi
kullanacağı `OPEN_QUESTIONS A10`'da AÇIK tutulur.

## 8 · İzlenebilirlik zinciri

```
KAYNAK → ÖLÇÜ / BELİRTİ / DÜZELTME KAYDI → BÖLÜM → FİGÜR → SAYFA
                        ↓
              FİZİKSEL DOĞRULAMA (VAL-xxxx)
```

"Bu sayfa neden bu düzeltmeyi öneriyor?" sorusunun her zaman bir kanıt
yolu olmalıdır. Beş alan HER ZAMAN birlikte okunur ve biri diğerinin
yerine geçmez: `claim` → `source_id` → `locator` → `authority class`
(`source_type` + `technical_authority`) → `verification_status`.

---

*Vâliçe Press · TRUE FIT · Sourcing Standard · 28 Ağustos 2026*
