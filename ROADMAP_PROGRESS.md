# ROADMAP PROGRESS — BEFORE YOU CUT

> Son ölçüm: **2026-08-28** · dal `master`
> · depo: `emredogan-cloud/sewing-pattern-fitting-series` (**public**,
> marka-nötr ad)
>
> Kaynak: [`SERIES_ROADMAP.md`](SERIES_ROADMAP.md) ve `BOOK-0x/ROADMAP.md`
>
> **Kural (`DECISIONS.md K33`): bu belgedeki her sayı, onu üreten
> komutun çıktısından alınır — hatırlanan bir değerden değil.**

---

## 0 · Tek cümlelik durum

> **Kitap 1 Faz 2 tamamlandı. Faz 3, kill-gate'inde DURDU.**
> İki ölçüm de dış dünyada yapılır ve **yapılmadı**.
> `kill_gate.py` → **2 engel** · Faz 4 **AÇILAMAZ**.

## Seri fazları

| Faz | Başlık | İlerleme | Kapı |
|---:|---|---|---|
| **S0** | Seri Bootstrap | `████████████████` tamamlandı | `bootstrap` ✓ |
| **S1** | Seri Mimarisi | `████████████████` **TAMAMLANDI** — kurucu onayı alındı, ortak mimari donduruldu | `series-architecture` ✓ **İLERLEDİ** |
| **S2** | Kitap 1 yaşam döngüsü | `██████░░░░░░░░░░` P0 ✓ · P1 ✓ · **P2 ✓** · P3 **KILL-GATE'TE DURDU** | — |
| **S3** | Kitap 2 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı — seri kapısı `production` değil | `init` |
| **S4** | Kitap 3 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı · yalnızca `A10` araştırma mimarisi | `init` |
| **S5** | Seri KA / Katalog | `░░░░░░░░░░░░░░░░` başlamadı — gerçek çok-kitap verisi yok | — |

## Kitap fazları

| Kitap | Kapı | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|
| **1 — Measure & Diagnose** | **`phase2-visual`** | ✓ | ✓ | **✓** | **DIŞ BEKLEMEDE** | — | — | — | — |
| **2 — The Adjustment Atlas** | `init` | roadmap var | — | — | — | — | — | — | — |
| **3 — Draft Your Own Sloper** | `init` | roadmap + `A10` araştırma mimarisi | — | — | — | — | — | — | — |

> **Bu turda iki kapı ilerledi:** seri `bootstrap` → `series-architecture`,
> Kitap 1 `foundation` → `phase2-visual`.
> **Üçüncü kapı (`phase3-pilot`) İLERLEMEDİ** ve bu turda ilerleyemez.

## Kalite kapıları — son ölçüm

Komut: `bash 06_BUILD/qa_all.sh` · 2026-08-28

| Kapı | Komut | Sonuç |
|---|---|---|
| Şema · bütünlük · kaynak otoritesi | `validate_spec.py` | ✓ 0 hata (**18 kaynak** · 43 belirti · 19 aile · 32 ölçü · 148 crosswalk · 12 blok · **154 figür**) |
| Depo · koruma · marka · izolasyon | `validate_structure.py` | ✓ 0 hata (**139 izlenen dosya** · **altı denetim hattı**) |
| Crosswalk tazeliği | `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| Crosswalk bütünlüğü | `qa_crosswalk.py` | ✓ 0 bulgu — 19/19 aileye ulaşılıyor |
| Kitap sınırı | `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| İddia disiplini | `qa_claims.py` | ✓ 0 bulgu (40 belge) |
| Terminoloji | `qa_terminology.py` | ✓ 0 bulgu (30 belge · 20 terim) |
| **Görsel sistem** *(yeni)* | `qa_visual.py` | ✓ **0 bulgu** — **on denetim** |
| **Yazı tipi bütünlüğü** *(yeni)* | `fetch_fonts.py --verify` | ✓ 10 dosya SHA-256 ile doğrulandı |
| **Kapıların kendi testi** | `selftest.py` | ✓ **138/138** *(önceki tur: 91)* |
| Kill-gate ön koşulu | `kill_gate.py --book book-01` | ✗ **2 engel — BEKLENEN VE DOĞRU** |

## Görsel sistem — Faz 2 ÖLÇÜMLERİ

| Ölçüt | Faz 1 tahmini | **ÖLÇÜLEN** |
|---|---:|---:|
| Toplam figür | ~123 | **154** |
| Akış şeması | 9 | **46** |
| Deterministik üretilebilen | — | **105 · %68,2** |
| `manual_reason` taşıyan | — | **49** (43 belirti + 6 toile) |
| İç araç figürü (kitaba girmez) | — | **3** |
| Bir yayılıma sığmayan şema | — | **0** (bölme öncesi 11) |
| `photo_required` | — | **0** / eşik 6 |
| `color_required` | — | **%0,0** / eşik %10 |
| Satır başına karakter | — | **83,0** (hedef 72–88) |
| `TK-05` ↔ `TK-06` eğrilik oranı | — | **3,49** (eşik 2,0) |
| En ince çizgi, 300 dpi 1-bit | — | **2 px** — hayatta |

### Figür türlerine göre

| Tür | Sayı |
|---|---:|
| `flowchart` | 46 |
| `fit_sign_on_figure` | 43 |
| `measurement_path` | 29 |
| `table_graphic` | 9 |
| `pattern_piece` | 8 |
| `body_landmark` | 7 |
| `comparison_before_after` | 6 |
| `toile_state` | 6 |
| **Toplam** | **154** |

## İçerik envanteri

| Varlık | Sayı | Doğrulama durumu |
|---|---|---|
| Uyum belirtisi (`SYM-xxx`) | 43 | **0 doğrulandı · 43 kaynağa bağlı ama YÜKSELTİLMEDİ** — bilinçli |
| Aday neden | 129 | **0 doğrulandı** — `C-C` sınıfı, birincil doğrulama FİZİKSEL |
| Düzeltme ailesi (`AF-xx`) | 19 | **13 doğrulandı** · 4 kısmi · 2 kaynaksız |
| Ölçü (`M-xxx`) | 32 | **16 doğrulandı** · 7 kısmi · 9 kaynaksız |
| Blok bileşeni (`BLK-xx`) | 12 | 0 — kamu kaynağı **çizim** anlatmıyor (`A10`) |
| Crosswalk (`XW-xxx`) | 148 | iç bütünlük denetlendi · dış doğrulama yok |
| Terim (`T-xx`) | 20 | taslak |
| Görsel token (`TK-xx`) | 18 | **`CALIBRATED_DIGITAL_RENDER`** |
| **Figür (`FIG-B1-xxx`)** | **154** | **105 `drafted` · 49 `specified` · 0 `physically_validated`** |
| **Okur etiketi (İngilizce)** | **43 belirti · 129 neden** | sunum katmanı — doğrulama durumunu **değiştirmez** |
| **Kaynak kaydı (`S-xxxx`)** | **18** | 6 teknik otorite + tam metin · 2 taranmış · **8 platform/lisans** · 2 edinilmemiş |
| **Fiziksel sınama (`VAL-xxxx`)** | **19 kayıt üretildi · 0 YAPILDI** | kit hazır: `BOOK-01/09_OUTPUT/VALIDATION_KIT.md` |
| **Pilot kesit** | **1 · 8 sayfa · 7 figür** | markasız · İngilizce · nihai sayfa geometrisinde |

**Faz 2 için satın alınan ücretli kaynak: 0.**
Yazı tipi maliyeti: **$0** (üç aile de SIL OFL 1.1).

## KILL-GATE durumu — Kitap 1 Faz 3

| | Fark testi (`D-01`) | Fiziksel doğrulama (`D-02`) |
|---|---|---|
| Protokol | ✓ TAMAM | ✓ TAMAM |
| **Malzeme** | ✓ **Malzeme A üretildi (8 sayfa)** · ✗ Malzeme B edinilmedi | ✓ **19 kayıtlık kit üretildi** |
| Katılımcı / uygulama | ✗ **0 / 3** | ✗ **0 / 19** |
| Ölçüm | ✗ `measured: false` | ✗ `measured: false` |
| AI vekil | ✗ `false` — **açılamaz** | — |
| Sonuç | **EXTERNAL VALIDATION REQUIRED** | **EXTERNAL VALIDATION REQUIRED** |

**`kill_gate.py` mekanik kilidi Faz 3'te güçlendirildi:**
`physicalValidation.measured = true` yazılmış ama `VAL_RECORDS.json`
kayıtları boşsa **ayrı bir engel** raporlanır. Bir bayrak, olmayan bir
ölçümü var edemez.

## Dış doğrulama durumu

Tam kayıt: [`EXTERNAL_DEPENDENCIES.md`](EXTERNAL_DEPENDENCIES.md)

| # | Bekleyen | Kim | Engelleyici mi |
|---|---|---|---|
| `D-01` | Fark testi — 3 ev dikişçisi | Kurucu | **EVET — HARD STOP** |
| `D-02` | Fiziksel doğrulama — 19 `VAL` | Kurucu | **EVET — HARD STOP** |
| `D-03` | `BEFORE YOU CUT` marka temizliği | Kurucu + vekil | EVET (yayın öncesi) |
| `D-04` | Rakip akış takibi (90 gün) | Kurucu | hayır |
| `D-05` | `T3` — üç insan okuyucu | Kurucu | hayır |
| `D-06` | KDP Previewer + prova baskı | Kurucu | EVET (P6) |
| `D-07` | Ücretsiz kaynak edinimi | Kurucu/ajan | hayır |
| `D-08` | Kitap 3 çizim sistemi kaynakları | Kurucu | EVET (Kitap 3) |
| `D-09` | Kitap 2 spiral fizibilitesi | Kurucu | hayır |

## Git / CI durumu

| | |
|---|---|
| Depo | `github.com/emredogan-cloud/sewing-pattern-fitting-series` (**public**) |
| Depo adı | **marka-nötr** (`K32`) — `BEFORE YOU CUT` de kamuya taahhüt edilmedi |
| Dal | `master` |
| İzlenen dosya | **139** |
| CI işi | **8** — `gates` · `spec` · `structure` · `crosswalk` · `boundary` · `claims` · **`visual`** *(yeni)* · `selftest` · `killgate` (tasarım gereği başarısız) |

**Bilerek yayımlanMAYAN:** pilot prozası ve derlenmiş pilot PDF'i ·
fiziksel sınama fotoğrafları · fark testi katılımcı verisi · telif
korumalı referans malzeme · indirilmiş kaynak PDF'leri · **yazı tipi
ikili dosyaları** (manifestle yeniden edinilir) · üretilmiş 154 figür
PDF'i · sırlar ve yerel önbellek.

## Açık kararlar

**13 kapandı · 1 ertelendi · 2 dış beklemede.**
Tam liste: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

`A15` (seri adı) **kapandı** — `BEFORE YOU CUT` (`K36`).
`A16` (profesyonel marka temizliği) **açıldı** ve dış beklemededir.

## Alınmış kararlar

**47 karar kayıtlı (`K1`–`K47`).** Bu turda **12 yeni kayıt**
(`K36`–`K47`).

Dördü, Faz 1 tahminlerinin **ölçümle yanlışlanmasıdır**: `K38` (yedek
yazı tipi), `K39` (sayfa ölçüsü), `K40` (token kalibrasyonu),
`K41` (akış şeması sayısı).
**Üçü, kapılar yeşilken ürünün kullanılamaz olmasıdır**: `K45` (figür
dili), `K46` (iç kimlik + etiket çakışması) ve `K47` (`.gitignore` iki
kaynak dosyayı yutuyordu — temiz bir klonda görsel sistem
çalışmazdı). `RISK_REGISTER R-19`.

## Riskler

**21 risk** — 4'ü YÜKSEK (`R-01` ortam, `R-02` talep tavanı,
`R-03` farklılaşma, `R-04` teknik doğruluk). Bu turda **üç yeni risk**
(`R-19` kapılar yeşilken ürün bozuk · `R-20` sayfa bütçesi ·
`R-21` tek kroki) ve **üç yeniden değerlendirme** (`R-05`, `R-06`,
`R-12`). **Hiçbir risk silinmedi.**
Tam liste: [`RISK_REGISTER.md`](RISK_REGISTER.md).

---

*Vâliçe Press · BEFORE YOU CUT · Roadmap Progress · 28 Ağustos 2026 (Faz 2 + Faz 3 hazırlığı)*
