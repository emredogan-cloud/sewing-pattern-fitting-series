# TRUE FIT 1 — Measure & Diagnose

**Rol: SORUNU GÖR.** Serinin edinme ürünü ve teşhis motoru.

> **Durum: FAZ 1 KURUCU ONAYI BEKLİYOR** · kapı `foundation`
> Rapor: [`08_REPORTS/PHASE_1_REPORT.md`](08_REPORTS/PHASE_1_REPORT.md)

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

## Bilinen sınır

Bu kitabın taksonomisi (43 belirti, 129 aday neden, 32 ölçü)
**hiçbir dış teknik otoriteye karşı doğrulanmadı** ve **hiçbiri fiziksel
olarak sınanmadı.** Tamamı `agent_drafted_unverified`. Kaynak edinim
bütçesi kurucu kararı bekliyor (`../OPEN_QUESTIONS.md → A3`) ve bu,
Faz 1'in **kapanış koşuludur**.
