# TRUE FIT — Sewing Pattern Fitting Series

Üç kitaplık dikiş kalıp uyumu serisi. Ev dikişçisinin en tekrarlayan
sorununu çözer: **kalıbı doğru uyguluyorum, giysi yine oturmuyor.**

> ⚠ **Bu depo bir kitap DEĞİL, üç kitabı üretecek proje işletim
> sistemidir.** Hiçbir manüskript yazılmadı, hiçbir diyagram üretilmedi,
> hiçbir kapak tasarlanmadı.
>
> **Şu anki durum: KİTAP 1 — FAZ 1 YÜRÜTÜLDÜ, KURUCU ONAYI BEKLİYOR.**
> Bkz. [`08_REPORTS/PHASE_1_EXECUTION_REPORT.md`](08_REPORTS/PHASE_1_EXECUTION_REPORT.md)
> (yürütme, 20 bölüm) ve
> [`08_REPORTS/PHASE_1_SERIES_ARCHITECTURE.md`](08_REPORTS/PHASE_1_SERIES_ARCHITECTURE.md)
> (mimari).
>
> ⚠ **`TRUE FIT` bir ÇALIŞMA ADIDIR ve YAYIMLANAMAZ** — aynı sektörde
> tescilli bir marka bulundu (`DECISIONS.md K18`,
> [`08_REPORTS/PHASE_1_BRAND_SCREENING.md`](08_REPORTS/PHASE_1_BRAND_SCREENING.md)).
> Bu deponun GitHub adı bu yüzden marka-nötrdür.

## Ne bu

`KDP_2_3_BOOK_SERIES_OPPORTUNITY_RESEARCH_2026_CYCLE_2.html`'in beş
finalist arasından **7,02/10** ile seçtiği fırsat. Kazanma gerekçesi:
bağımsız yayıncının bu pazarda kazandığı kanıtlı, lider üründe
sayısallaştırılmış bir kalite açığı var (`Complexity(58)`, n=1.797),
uzman kapısı yok ve doğrulama fiziksel.

```
KİTAP 1  Measure & Diagnose      SORUNU GÖR
KİTAP 2  The Adjustment Atlas    SORUNU ÇÖZ
KİTAP 3  Draft Your Own Block    ÇÖZÜMÜ ÜRET
```

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

15 kaynak kaydı vardır (6'sı tam metni okunmuş kurumsal otorite) ve
Faz 1 **hiçbir ücretli kaynak satın alınmadan** kapandı —
[`01_SOURCE/PUBLIC_SOURCE_SURVEY.md`](01_SOURCE/PUBLIC_SOURCE_SURVEY.md).

## Lisans

Kod MIT (`LICENSE`). Kitap içeriği ve taksonomi tüm hakları saklıdır.
