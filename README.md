# BEFORE YOU CUT — Sewing Pattern Fitting Series

Üç kitaplık dikiş kalıp uyumu serisi. Ev dikişçisinin en tekrarlayan
sorununu çözer: **kalıbı doğru uyguluyorum, giysi yine oturmuyor.**

> ⚠ **Bu depo bir kitap DEĞİL, üç kitabı üretecek proje işletim
> sistemidir.** Kitap 1'in manüskripti **üretildi** (232 sayfa, 21 bölüm,
> 161 figür) ama **prozası bu depoda YAYIMLANMAZ** — yayın-öncesi içerik
> izlenmez (`.gitignore § ①`, `DECISIONS.md K9`). Depoya **ölçüm** girer,
> **metin** girmez. Kapak tasarlanmadı.
>
> ## Şu anki durum: KİTAP 1 — FAZ 4 ÜRETİMİ TAMAM (KOŞULLU) · KILL-GATE HÂLÂ AÇIK
>
> Faz 4, kurucu geçersiz kılmasıyla (`DECISIONS.md K49`) P3'ün kill-gate'i
> **beklenmeden** yürütüldü. Eksik ölçümler **PASS yazılmadı ve
> yazılamaz**: kitap kapısı `phase4-production-conditional`'dır ve
> kümülatif sırada `phase3-pilot`'ın **ÖNÜNDEDİR**.
>
> `06_BUILD/kill_gate.py` hâlâ **2 engel** raporluyor. İki ölçüm de dış
> dünyada yapılır ve **yapılmadı**: üç ev dikişçisiyle fark testi, ve
> 19 kayıtlık fiziksel doğrulama. **`phase5-qa` bu yoldan açılamaz.**
>
> Bu turda dört hatlı bir **bağımsız teknik inceleme** yürütüldü:
> **149 bulgu**, 68 kaynak, **132 revizyon** — ve incelenen iddialardan
> **yalnızca biri** değişmeden ayakta kaldı. AI incelemesidir;
> **insan doğrulamasının yerine geçmez** (`K6`).
>
> Raporlar: [`08_REPORTS/PHASE_4_EXECUTION_REPORT.md`](08_REPORTS/PHASE_4_EXECUTION_REPORT.md)
> · [`08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md`](08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md)
> · [`08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md`](08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md)
> · dış bağımlılıklar: [`EXTERNAL_DEPENDENCIES.md`](EXTERNAL_DEPENDENCIES.md)
>
> ⚠ **Seri adı `BEFORE YOU CUT`** — kurucu kararı (`DECISIONS.md K36`).
> İlk çalışma adı `TRUE FIT` idi ve **reddedildi**: aynı sektörde
> tescilli bir marka bulundu (`K18`,
> [`08_REPORTS/PHASE_1_BRAND_SCREENING.md`](08_REPORTS/PHASE_1_BRAND_SCREENING.md)).
> Dizin ve depo adları **değiştirilmedi** — bir yol dizesi bir kimlik
> beyanı değildir (`K37`).
>
> ⚠ **`BEFORE YOU CUT` henüz PROFESYONEL OLARAK TEMİZLENMEDİ.**
> `brandClearanceStatus = founder-approved-working-name`. Kapak ve
> metadata üretiminden önce bir marka vekili gerekir
> (`OPEN_QUESTIONS A16`, `EXTERNAL_DEPENDENCIES D-03`).

## Ne bu

`KDP_2_3_BOOK_SERIES_OPPORTUNITY_RESEARCH_2026_CYCLE_2.html`'in beş
finalist arasından **7,02/10** ile seçtiği fırsat. Kazanma gerekçesi:
bağımsız yayıncının bu pazarda kazandığı kanıtlı, lider üründe
sayısallaştırılmış bir kalite açığı var (`Complexity(58)`, n=1.797),
uzman kapısı yok ve doğrulama fiziksel.

```
KİTAP 1  Measure & Diagnose      SORUNU GÖR      ◄ Faz 3'te durdu
KİTAP 2  The Adjustment Atlas    SORUNU ÇÖZ
KİTAP 3  Draft Your Own Sloper   ÇÖZÜMÜ ÜRET
```

*Kitap 3'ün dizin adı `BOOK-03-DRAFT-YOUR-OWN-BLOCK`'tur; başlıkta
`sloper`, kanonik terim `block` kalır (`K26`).*

Vâliçe Press'in mitoloji/oyun kataloğundan, duraklatılmış "License &
Launch" hattından ve Hangıl çalışma kitabından ayrı, **dördüncü üretim
dalı**.

## Hızlı başlangıç

```bash
cd TRUE-FIT-SEWING-PATTERN-FITTING-SERIES
bash 06_BUILD/qa_all.sh
```

Yeşilse proje makinesi çalışıyor demektir. Üçüncü taraf paket
gerekmez — tüm kapılar Python standart kütüphanesiyle yazılmıştır.

Tek tek:

```bash
python3 06_BUILD/validate_spec.py --verbose        # şema + bütünlük + kaynak otoritesi
python3 06_BUILD/validate_structure.py --verbose   # belge + koruma + marka + izolasyon
python3 06_BUILD/build_crosswalk.py --check        # devir haritası güncel mi
python3 06_BUILD/qa_crosswalk.py --verbose         # devir haritası bütünlüğü (dokuz ilişki)
python3 06_BUILD/qa_boundary.py --verbose          # kitap sınırı (seriye özgü)
python3 06_BUILD/qa_claims.py --verbose            # iddia disiplini
python3 06_BUILD/qa_terminology.py --verbose       # terim tutarlılığı
python3 06_BUILD/kill_gate.py --book book-01       # kill-gate ön koşulu
python3 07_TESTS/selftest.py                       # KAPILARIN KENDİ TESTİ
```

## Okuma sırası

1. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — genel harita
2. [`SERIES_ROADMAP.md`](SERIES_ROADMAP.md) — seri yaşam döngüsü
3. [`00_CONTEXT/SERIES_POSITIONING.md`](00_CONTEXT/SERIES_POSITIONING.md) — kim için, neden
4. [`00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md`](00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md) — kitap sınırları
5. [`BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/`](BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/) — Faz 1'in on çıktısı
6. [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — kurucudan yanıt bekleyen 14 karar
7. [`RISK_REGISTER.md`](RISK_REGISTER.md) — 14 risk
8. [`DECISIONS.md`](DECISIONS.md) — alınmış 17 karar

## Depo haritası

```
00_CONTEXT/     seri politikaları (17 belge)
01_SOURCE/      kaynak sicili — künye, metin DEĞİL
02_TAXONOMY/    43 belirti · 19 düzeltme ailesi · 32 ölçü · 148 crosswalk
03_VISUAL/      18 token'lık çizim dili + figür şeması
06_BUILD/       araç zinciri (8 script)
07_TESTS/       kapıların kendi testi
08_REPORTS/     faz raporları
BOOK-01…03/     üç kitap projesi (kendi roadmap · spec · gate)
```

## Bir not — doğrulanmamış içerik hakkında

Faz 1 yürütmesi sonrası **gerçek** durum:

| Katman | Doğrulandı | Toplam |
|---|---|---|
| Ölçü (`M-xxx`) | **16** | 32 |
| Düzeltme ailesi (`AF-xx`) | **13** | 19 |
| **Belirti (`SYM-xxx`)** | **0** | 43 |
| Aday neden / ayırt edici kanıt | **0** | 129 |
| Blok bileşeni (`BLK-xx`) | 0 | 12 |
| Fiziksel sınama (`VAL-xxxx`) | — | **0 kayıt** |

**Belirtilerin sıfırda kalması bir eksiklik değil, taramanın bulgusudur:**
bir belirti kaydının çekirdek iddiası aynı belirtinin iki nedenini ayıran
kanıttır ve **hiçbir kamu kaynağı bu ayrımı yapmaz.** Bu sınıfın birincil
doğrulaması fizikseldir ve Faz 3'e aittir.

**18 kaynak kaydı** vardır (6'sı tam metni okunmuş kurumsal otorite;
Faz 1 onbeşle kapandı, Faz 2 üç platform/lisans kaydı ekledi) ve
Faz 1 ile Faz 2 **hiçbir ücretli kaynak satın alınmadan** kapandı —
[`01_SOURCE/PUBLIC_SOURCE_SURVEY.md`](01_SOURCE/PUBLIC_SOURCE_SURVEY.md).

## Lisans

Kod MIT (`LICENSE`). Kitap içeriği ve taksonomi tüm hakları saklıdır.
