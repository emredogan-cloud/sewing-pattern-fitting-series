# ROADMAP PROGRESS — TRUE FIT

> Son ölçüm: **2026-08-28** · dal `master` · etiket — yok
>
> Kaynak: [`SERIES_ROADMAP.md`](SERIES_ROADMAP.md) ve
> `BOOK-0x/ROADMAP.md`

## Seri fazları

| Faz | Başlık | İlerleme | Ölçüt | Kapı |
|---:|---|---|---|---|
| **S0** | Seri Bootstrap | `████████████████` tamamlandı | Tüm kapılar yeşil, git commit var | `bootstrap` ✓ |
| **S1** | Seri Mimarisi | `████████████████` **çıktılar üretildi — KURUCU ONAYI BEKLİYOR** | 12/12 çıktı mevcut; DoD madde 3 (kurucu onayı) KARŞILANMADI | `bootstrap` — **ilerlemedi** |
| **S2** | Kitap 1 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı | — | — |
| **S3** | Kitap 2 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı | — | — |
| **S4** | Kitap 3 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı | — | — |
| **S5** | Seri KA / Katalog | `░░░░░░░░░░░░░░░░` başlamadı | — | — |

## Kitap fazları

| Kitap | Kapı | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|
| **1 — Measure & Diagnose** | `foundation` | ✓ | **onay bekliyor** | — | — | — | — | — | — |
| **2 — The Adjustment Atlas** | `init` | roadmap var | — | — | — | — | — | — | — |
| **3 — Draft Your Own Block** | `init` | roadmap var | — | — | — | — | — | — | — |

## Kalite kapıları — son ölçüm

| Kapı | Komut | Sonuç |
|---|---|---|
| Şema · bütünlük · kaynak otoritesi | `validate_spec.py` | ✓ 0 hata (43 belirti · 19 aile · 32 ölçü · 148 crosswalk · 12 blok) |
| Depo · koruma · marka · izolasyon | `validate_structure.py` | ✓ 0 hata |
| Crosswalk tazeliği | `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| **Kitap sınırı** | `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| **İddia disiplini** | `qa_claims.py` | ✓ 0 bulgu |
| **Terminoloji** | `qa_terminology.py` | ✓ 0 bulgu (20 terim) |
| Kill-gate ön koşulu | `kill_gate.py --book book-01` | ✗ **4 engel — BEKLENEN.** İki ölçüm henüz yapılmadı (dış dünyada yapılır) |
| **Kapıların kendi testi** | `selftest.py` | ✓ tüm denetimler geçti |
| GitHub Actions CI | `.github/workflows/validate.yml` | yerel eşdeğeri yeşil; GitHub'da hiç TETİKLENMEDİ (push yok, `A2`) |

## İçerik envanteri

| Varlık | Sayı | Doğrulama durumu |
|---|---|---|
| Uyum belirtisi (`SYM-xxx`) | 43 | **43 × `agent_drafted_unverified`** |
| Aday neden | 129 | — |
| Düzeltme ailesi (`AF-xx`) | 19 | **19 × `agent_drafted_unverified`** |
| Ölçü (`M-xxx`) | 32 | **32 × `agent_drafted_unverified`** |
| Blok bileşeni (`BLK-xx`) | 12 | **12 × `agent_drafted_unverified`** |
| Crosswalk (`XW-xxx`) | 148 | türetilmiş |
| Terim (`T-xx`) | 20 | taslak |
| Görsel token (`TK-xx`) | 18 | `DESIGN_TARGET_NOT_CALIBRATED` |
| Sınır topiği (`TOP-xx`) | 35 | — |
| **Kaynak kaydı (`S-xxxx`)** | **0** | **`OPEN_QUESTIONS A3`** |
| Fiziksel doğrulama (`VAL-xxxx`) | 0 | — |
| Figür (`FIG-xxx`) | 0 | Faz 2'de üretilir |

## Açık kararlar

14 açık soru — 5'i **YÜKSEK** aciliyette (`A1` marka, `A3` kaynak
bütçesi, `A4` ortam, `A13` doğrulama kapsamı, `A14` test katılımcıları).
Tam liste: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

## Riskler

14 risk — 4'ü **YÜKSEK** (`R-01` ortam, `R-02` talep tavanı,
`R-03` farklılaşma, `R-04` teknik doğruluk).
Tam liste: [`RISK_REGISTER.md`](RISK_REGISTER.md).

---

*Vâliçe Press · TRUE FIT · Roadmap Progress · 28 Ağustos 2026*
