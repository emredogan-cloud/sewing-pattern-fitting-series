# TRUE FIT 1 — Measure & Diagnose

**Rol: SORUNU GÖR.** Serinin edinme ürünü ve teşhis motoru.

> **Durum: FAZ 1 YÜRÜTÜLDÜ — KURUCU ONAYI BEKLİYOR** · kapı `foundation`
> Raporlar: [`08_REPORTS/PHASE_1_REPORT.md`](08_REPORTS/PHASE_1_REPORT.md)
> (spesifikasyon) ·
> [`../08_REPORTS/PHASE_1_EXECUTION_REPORT.md`](../08_REPORTS/PHASE_1_EXECUTION_REPORT.md)
> (**yürütme — 20 bölüm**)

## Çözdüğü problem

> "Kalıbı doğru uyguladım. Giysi yine oturmuyor. **Neden?**"

Piyasadaki kitaplar bir düzeltme **kataloğudur** ve okurun teşhisi
zaten koyabildiğini varsayar. Alıcının gerçek sorunu tam olarak
teşhisin kendisidir.

## Ne öğretir, ne öğretmez

| Öğretir | Öğretmez |
|---|---|
| Doğru ölçü almayı ve en sık yapılan hataları | Dikiş yapmayı (ön koşul) |
| Kalıp bedeni ≠ hazır giyim bedeni ayrımını | Düzeltmenin ADIM ADIM nasıl yapılacağını (**Kitap 2**) |
| Teşhis toile'i dikmeyi ve prova protokolünü | Blok çizmeyi (**Kitap 3**) |
| 43 uyum belirtisini ADLANDIRMAYI | Örme kumaş uyumunu (seri dışı) |
| Belirtiyi nedenden ayırmayı | Erkek giyim / terzilik (seri dışı) |
| Kalıp DIŞI nedenleri elemeyi (kumaş, kesim, yapım, basım) | |
| Hangi düzeltmenin ÖNCE geldiğini | |
| Kişisel uyum profilini kaydetmeyi | |

Sınır kuralı: [`../00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md`](../00_CONTEXT/SERIES_CONTENT_ARCHITECTURE.md)
· mekanik denetim `qa_boundary.py`.

## Faz 1'in on çıktısı

| Belge | Ne |
|---|---|
| [`00_SPEC/SCOPE.md`](00_SPEC/SCOPE.md) | Kapsam ve dışlama |
| [`00_SPEC/CONTENT_ARCHITECTURE.md`](00_SPEC/CONTENT_ARCHITECTURE.md) | Tam hiyerarşik içerik yapısı |
| [`00_SPEC/CHAPTER_SPECS.md`](00_SPEC/CHAPTER_SPECS.md) | 18 bölümün tek tek spesifikasyonu |
| [`00_SPEC/DIAGNOSTIC_SYSTEM.md`](00_SPEC/DIAGNOSTIC_SYSTEM.md) | Yedi adımlı teşhis döngüsü |
| [`00_SPEC/DIAGNOSIS_TO_ADJUSTMENT_MAP.md`](00_SPEC/DIAGNOSIS_TO_ADJUSTMENT_MAP.md) | Kitap 1 → Kitap 2 crosswalk |
| [`00_SPEC/VISUAL_SPEC.md`](00_SPEC/VISUAL_SPEC.md) | Diyagram gereksinimleri |
| [`00_SPEC/SOURCE_MAP.md`](00_SPEC/SOURCE_MAP.md) | Teknik iddia → kaynak matrisi |
| [`00_SPEC/VALIDATION_PROTOCOL.md`](00_SPEC/VALIDATION_PROTOCOL.md) | Fiziksel doğrulama planı |
| [`00_SPEC/DIFFERENTIATION_TEST.md`](00_SPEC/DIFFERENTIATION_TEST.md) | **KİLL-GATE** test protokolü |
| [`00_SPEC/PHASE_2_ROADMAP.md`](00_SPEC/PHASE_2_ROADMAP.md) | Faz 2 planı (YÜRÜTÜLMEDİ) |

## Bilinen sınır — Faz 1 yürütmesi sonrası

| Katman | Durum |
|---|---|
| Ölçü (`M-xxx`) | **16 / 32 doğrulandı** · 7 kısmi · 9 kaynaksız |
| Düzeltme ailesi (`AF-xx`) | **13 / 19 doğrulandı** · 4 kısmi · 2 kaynaksız |
| **Belirti (`SYM-xxx`)** | **0 / 43** — ve bu **bilinçlidir** |
| Aday neden / ayırt edici kanıt | **0 / 129** |
| Fiziksel sınama | **0 kayıt** — plan hazır (19 kayıt) |

**Belirtiler neden sıfırda:** bir belirti kaydının çekirdek iddiası aynı
belirtinin iki nedenini ayıran kanıttır ve **hiçbir kamu kaynağı bu
ayrımı yapmaz.** Bu sınıfın birincil doğrulaması **fizikseldir** ve
Faz 3'e aittir (`00_SPEC/VALIDATION_PROTOCOL.md`).

Faz 1 **hiçbir ücretli kaynak satın alınmadan** kapandı — 15 kaynak
kaydı, 6'sı tam metni okunmuş kurumsal otorite
(`../01_SOURCE/PUBLIC_SOURCE_SURVEY.md`).
