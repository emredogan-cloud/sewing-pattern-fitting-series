# ROADMAP PROGRESS — TRUE FIT

> Son ölçüm: **2026-08-28** · dal `master` · etiket — yok
> · depo: `emredogan-cloud/sewing-pattern-fitting-series` (**public**)
>
> Kaynak: [`SERIES_ROADMAP.md`](SERIES_ROADMAP.md) ve
> `BOOK-0x/ROADMAP.md`
>
> **Kural (`DECISIONS.md K33`): bu belgedeki her sayı, onu üreten
> komutun çıktısından alınır — hatırlanan bir değerden değil.**

## Seri fazları

| Faz | Başlık | İlerleme | Ölçüt | Kapı |
|---:|---|---|---|---|
| **S0** | Seri Bootstrap | `████████████████` tamamlandı | Tüm kapılar yeşil, git commit var | `bootstrap` ✓ |
| **S1** | Seri Mimarisi | `████████████████` **çıktılar üretildi ve YÜRÜTÜLDÜ — KURUCU ONAYI BEKLİYOR** | 12/12 çıktı mevcut + Faz 1 yürütmesi tamamlandı; DoD madde 3 (kurucu onayı) KARŞILANMADI | `bootstrap` — **ilerlemedi** |
| **S2** | Kitap 1 yaşam döngüsü | `████░░░░░░░░░░░░` P0 ✓ · P1 yürütüldü, onay bekliyor | — | — |
| **S3** | Kitap 2 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı | — | — |
| **S4** | Kitap 3 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı | Yalnızca `A10` araştırma mimarisi yazıldı | `init` |
| **S5** | Seri KA / Katalog | `░░░░░░░░░░░░░░░░` başlamadı | — | — |

## Kitap fazları

| Kitap | Kapı | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|
| **1 — Measure & Diagnose** | `foundation` | ✓ | **yürütüldü — onay bekliyor** | — | — | — | — | — | — |
| **2 — The Adjustment Atlas** | `init` | roadmap var | — | — | — | — | — | — | — |
| **3 — Draft Your Own Block** | `init` | roadmap + `A10` araştırma mimarisi | — | — | — | — | — | — | — |

> **Hiçbir kapı bu turda ilerlemedi.** Kitap 1 Faz 1'in DoD'si dört
> maddedir ve dördüncüsü (kurucu onayı) karşılanmamıştır.

## Kalite kapıları — son ölçüm

Komut: `bash 06_BUILD/qa_all.sh` · 2026-08-28

| Kapı | Komut | Sonuç |
|---|---|---|
| Şema · bütünlük · kaynak otoritesi | `validate_spec.py` | ✓ 0 hata (**15 kaynak** · 43 belirti · 19 aile · 32 ölçü · 148 crosswalk · 12 blok) |
| Depo · koruma · marka · izolasyon | `validate_structure.py` | ✓ 0 hata (**139 izlenen dosya**) |
| Crosswalk tazeliği | `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| **Crosswalk bütünlüğü** *(yeni)* | `qa_crosswalk.py` | ✓ **0 bulgu** — dokuz denetim · 129 teşhis→düzeltme · 21 istisna · **19/19 aileye ulaşılıyor** |
| Kitap sınırı | `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| İddia disiplini | `qa_claims.py` | ✓ 0 bulgu (35 belge) |
| Terminoloji | `qa_terminology.py` | ✓ 0 bulgu (30 belge · 20 terim) |
| Kill-gate ön koşulu | `kill_gate.py --book book-01` | ✗ **2 engel — BEKLENEN.** İki ölçüm de dış dünyada yapılır |
| **Kapıların kendi testi** | `selftest.py` | ✓ **91/91** denetim geçti *(önceki tur: 77)* |
| **GitHub Actions CI** | `.github/workflows/validate.yml` | ✓ **YEŞİL** — koşu `33193615969`, 22 sn, 7/7 iş geçti; `kill-gate` işi tasarım gereği başarısız (`continue-on-error`) |

> ⚠ **Düzeltme (`K33`).** Bu satırda önceki turda "4 engel" yazıyordu.
> `kill_gate.py` hem şimdi hem de o günkü commit'te **2 engel**
> raporluyor. Sayı doğrulandı ve düzeltildi.

## İçerik envanteri

| Varlık | Sayı | Doğrulama durumu |
|---|---|---|
| Uyum belirtisi (`SYM-xxx`) | 43 | **0 doğrulandı · 43 kaynağa bağlı ama YÜKSELTİLMEDİ** — bilinçli, `SOURCE_MAP § 6` |
| Aday neden | 129 | **0 doğrulandı** — `C-C` sınıfı, Faz 3'e ait |
| Düzeltme ailesi (`AF-xx`) | 19 | **13 doğrulandı** · 4 kısmi · 2 kaynaksız |
| Ölçü (`M-xxx`) | 32 | **16 doğrulandı** · 7 kısmi · 9 kaynaksız |
| Blok bileşeni (`BLK-xx`) | 12 | 0 — kamu kaynağı **çizim** anlatmıyor (`A10`) |
| Crosswalk (`XW-xxx`) | 148 | türetilmiş · **iç bütünlük denetlendi, 0 bulgu** · dış doğrulama yok |
| Terim (`T-xx`) | 20 | taslak |
| Görsel token (`TK-xx`) | 18 | `DESIGN_TARGET_NOT_CALIBRATED` |
| Sınır topiği (`TOP-xx`) | 35 | — |
| **Kaynak kaydı (`S-xxxx`)** | **15** | 6 teknik otorite + tam metin · 2 taranmış (okunamadı) · 5 platform · 2 edinilmemiş |
| Fiziksel sınama (`VAL-xxxx`) | **0** | plan hazır: 19 kayıt, `A13` |
| Figür (`FIG-xxx`) | 0 | Faz 2'de üretilir |

## Kaynak doğrulama durumu

| Durum | Ölçü | Düzeltme ailesi | Belirti | Blok |
|---|---|---|---|---|
| **VERIFIED** | **16** / 32 | **13** / 19 | 0 / 43 | 0 / 12 |
| PARTIALLY VERIFIED | 7 | 4 | 43 | 0 |
| EXTERNAL-SOURCE REQUIRED | 9 | 2 | — | 12 |
| UNVERIFIED | — | — | **43** | — |

**Faz 1 için satın alınan ücretli kaynak: 0.**
Kuyruğa alınan: 4 kalem, hiçbiri Kitap 1 için gerekli değil
(`01_SOURCE/ACQUISITION_REQUEST_QUEUE.md`).

## `A14` durumu — kill-gate ①

| | |
|---|---|
| Protokol | ✓ **TAMAMLANDI** — eleme ölçütleri, ön eleme soruları, beş bulma kanalı, teşvik politikası, taraf tutma kuralları, oturum betiği, kayıt formu, malzeme spesifikasyonu |
| Katılımcı | ✗ **0 / 3** |
| Ölçüm | ✗ **YAPILMADI** — `measured: false` |
| AI vekil | ✗ `aiProxyCountsAsHuman: false` — **açılmadı** |
| Sonuç | **EXTERNAL PENDING** — kurucu bağımsız uygulayabilir |
| 1–2 katılımcı bulunursa | **`INCONCLUSIVE`** — PASS değil, FAIL değil; kapı **kapalı kalır** |

## Dış doğrulama durumu

| # | Bekleyen | Kim | En geç |
|---|---|---|---|
| 1 | **Kitap 1 Faz 1 onayı** | Kurucu | — |
| 2 | `A15` yerine geçen seri adı + **profesyonel marka temizliği** | Kurucu + marka vekili | `phase2-visual` başlangıcı / kapak öncesi |
| 3 | `A14` üç ev dikişçisi | Kurucu | `phase3-pilot` |
| 4 | Fiziksel sınama — 19 `VAL` kaydı | Kurucu | `phase3-pilot` |
| 5 | Rakip akış takibinin başlatılması | Kurucu | `phase2-visual` |

## Git / CI durumu

| | |
|---|---|
| Depo | `github.com/emredogan-cloud/sewing-pattern-fitting-series` |
| Görünürlük | **public** |
| Depo adı | **marka-nötr** — `A1` kapanmadan hiçbir ad kamuya taahhüt edilmedi (`K32`) |
| Dal | `master` |
| İzlenen dosya | **139** |
| CI | ✓ **yeşil** — 7/7 iş; `kill-gate` işi tasarım gereği başarısız |
| Korumalı dizinler | ✓ hepsi yalnızca `.gitkeep` içeriyor — doğrulandı |
| Hassas içerik taraması | ✓ temiz (e-posta, mutlak yerel yol, token/anahtar, telefon) |

**Bilerek yayımlanMAYAN:** yayın-öncesi proza ve pilot metni · fiziksel
sınama fotoğrafları · **fark testi katılımcı verisi** · telif korumalı
referans malzeme ve ticari kalıplar · **indirilmiş kaynak PDF'leri** ·
üretilmiş diyagram varlıkları ve yayın dosyaları · sırlar ve yerel
önbellek.

## Açık kararlar

**12 kapandı · 1 ertelendi · 2 dış beklemede.** Hiçbiri "hâlâ açık"
değil. Tam liste: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

## Alınmış kararlar

**35 karar kayıtlı (`K1`–`K35`).** Bu turda 18 yeni kayıt.

Altısı, kapıların **gerçekten çalıştığının kanıtı** olarak doğdu:
`K13` (sınır matrisi), `K14` (anahtar kelime muafiyeti), `K15`
(`SYM-043`), `K16` (Türkçe katlama), `K17` (selftest fixture'ı) ve
**`K20`** (testin adı ile ölçtüğü şeyin farklı olması).
Tam liste: [`DECISIONS.md`](DECISIONS.md).

## Riskler

**18 risk** — 4'ü YÜKSEK (`R-01` ortam, `R-02` talep tavanı, `R-03`
farklılaşma, `R-04` teknik doğruluk). Bu turda `R-12`'nin olasılığı
**DÜŞÜK → ORTA–YÜKSEK**'e çıktı (somut marka çakışması bulundu) ve
dört yeni risk eklendi (`R-15`…`R-18`). **Hiçbir risk silinmedi.**
Tam liste: [`RISK_REGISTER.md`](RISK_REGISTER.md).

---

*Vâliçe Press · TRUE FIT · Roadmap Progress · 28 Ağustos 2026 (Faz 1 yürütmesi)*
