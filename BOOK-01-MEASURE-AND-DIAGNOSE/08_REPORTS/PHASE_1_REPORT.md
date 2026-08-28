# FAZ 1 RAPORU — TRUE FIT 1: Measure & Diagnose

> **Faz durumu: READY_FOR_DECISION**
> Tarih: 28 Ağustos 2026 · Kitap kapısı: `foundation` (**ilerlemedi**)
>
> Seri bağlamı: [`../../08_REPORTS/PHASE_1_SERIES_ARCHITECTURE.md`](../../08_REPORTS/PHASE_1_SERIES_ARCHITECTURE.md)
>
> ⚠ **Bu rapor SPESİFİKASYON turunu anlatır.** Sonraki **YÜRÜTME**
> turunun tam kaydı ayrı bir belgededir:
> [`../../08_REPORTS/PHASE_1_EXECUTION_REPORT.md`](../../08_REPORTS/PHASE_1_EXECUTION_REPORT.md)
> — 14 açık kararın 12'sinin kapatılması, kaynak katmanının kurulması
> ve taksonominin kanıta bağlanması orada anlatılır.

---

## 1 · Ne üretildi

On zorunlu Faz 1 çıktısının tamamı (`00_SPEC/`), artı Kitap 1'in
çekirdek veri seti (`../../02_TAXONOMY/public/`).

| Çıktı | Ölçü |
|---|---|
| Kapsam ve dışlama | 19 kapsam-içi + 12 kapsam-dışı konu, gerekçeli |
| İçerik mimarisi | 5 parça · 18 bölüm · 7 ek · 10 alıştırma |
| Bölüm spesifikasyonları | 18 bölüm × 11 alan |
| Teşhis sistemi | 7 adım, 3 yerleştirme kuralı, 4 durma koşulu |
| Belirti taksonomisi | **43 belirti · 129 aday neden · 10 bölge · 10 sınıf** |
| Ölçü çerçevesi | 32 ölçü, her biri sık-hata listesiyle |
| Kitap 2 crosswalk | 129 yol + 21 açık istisna · **19/19 aile ulaşılabilir** |
| Görsel spesifikasyon | ~123 figür tahmini, 8 türde |
| Kaynak haritası | 8 iddia sınıfı, sınıf bazlı doğrulama stratejisi |
| Fiziksel doğrulama planı | 5 yöntem (Y-1…Y-5), pilot planı |
| Fark testi protokolü | Kill-gate, geçme kriteri, FAIL sonucu |
| Faz 2 yol haritası | 8 görev, 11 DoD maddesi |

## 2 · Faz 1'in üç mimari kararı

### ① Belirti ile neden ŞEMA DÜZEYİNDE ayrıldı

`symptom_schema.json`, her aday nedenin bir `distinguishing_evidence` ve
bir `confirming_measurement` taşımasını **zorunlu** kılar. Ayırt edici
kanıtı olmayan bir neden **yazılamaz**; iki neden aynı kanıtı taşıyamaz
(`check_cause_distinguishability`).

Bu, "teşhis-önce" konumlandırmasının pazarlama değil **veri modeli**
düzeyinde uygulanmasıdır.

### ② `do_not_change_yet` bir birinci sınıf alan yapıldı

43 belirtinin her birinde. Bir katalog kitabı okura ne yapacağını
söyler; bu kitap ayrıca **neyi henüz yapmayacağını** söyler — çünkü
kesilen kumaş geri gelmez.

### ③ Sahte neden eleme (`TOP-11`) bir BÖLÜM oldu

Dokuz eleme kalemi ve 21 crosswalk istisnası. Okurun kalıba dokunmadan
önce geçmesi gereken son güvenlik kapısı.

## 3 · Ölçülebilir çıkış ölçütleri

| Ölçüt | Eşik | Sonuç |
|---|---|---|
| Bölge kapsaması | 10/10 | ✓ |
| Belirti sınıfı kapsaması | 10/10 | ✓ |
| Her aday nedenin ayırt edici kanıtı | %100 | ✓ (şema dayatır) |
| Ölçümü olmayan nedenin fiziksel testi | %100 | ✓ |
| Kitap 1'den ulaşılabilen düzeltme ailesi | 19/19 | ✓ |
| Yolsuz belirti | 0 | ✓ |
| Gerekçesiz crosswalk istisnası | 0 | ✓ |
| Sınır sızıntısı | 0 | ✓ |
| **Kaynak kaydı** | ≥1 otoriter | ✗ **0** |

Son satır **karşılanmadı** ve bu, fazın kapanmama nedenidir.

## 4 · Bu fazda BULUNAN ve DÜZELTİLEN

| Bulgu | Bulan | Düzeltme |
|---|---|---|
| `AF-19`'a Kitap 1'den ulaşılamıyor | `qa_boundary.py` | `SYM-043` eklendi |
| `M-011` şema ihlali | `validate_spec.py` | İçerik düzeltildi |
| Türkçe "İ" kusuru üçüncü doğrulayıcıda açık | `selftest.py` | `trfold.py` tek kopya + regresyon testi |
| `selftest.py` fixture'ı izolasyon ihlali üretiyordu | `validate_structure.py` | Fixture çalışma anında üretiliyor; kapı muafiyet almadı |

## 5 · SINIRLAMALAR

1. ~~43 belirti, 129 neden, 32 ölçü — tamamı `agent_drafted_unverified`.
   Sıfır kaynak kaydı.~~ → **YÜRÜTME TURUNDA KISMEN KAPANDI:**
   15 kaynak kaydı açıldı; **16/32 ölçü** ve **13/19 düzeltme ailesi**
   `technical_reference_verified`'e yükseltildi. **43 belirtinin hiçbiri
   yükseltilMEDİ** — hiçbir kamu kaynağı aynı belirtinin iki nedenini
   ayırmıyor (`00_SPEC/SOURCE_MAP.md § 6`). Faz 1 **hiçbir ücretli
   kaynak satın alınmadan** kapandı (`DECISIONS.md K19`).
2. **Sıfır fiziksel sınama.** `VAL-xxxx` kaydı yok — ama **plan
   tamamlandı**: 2 toile + 3 parça, 19 kayıt, ≈$15–30, ≈20–25 saat
   (`DECISIONS.md K29`).
3. **Okur tanımı devralındı**, bu depoda doğrulanmadı.
4. **Figür sayısı tahmin.** Faz 2'de ölçülür.
5. **Sayfa/fiyat `PROVISIONAL`.**
6. Çoklu belirti işleme, ölçüm hassasiyeti ve asimetri — teşhis
   sisteminin kendi kaydettiği üç zayıflık (`DIAGNOSTIC_SYSTEM.md § 6`).

## 6 · Faz 2'ye giden yol

`00_SPEC/PHASE_2_ROADMAP.md` — 8 görev, 11 DoD maddesi.

**Yürütme turunun katkısı:** Faz 2'de kapanması beklenen altı kurucu
kararından **beşi önceden kapatıldı** (`A4` `A6` `A7` `A8` `A11`).
`A1`'in yerini `A15` aldı ve dış beklemededir. Faz 2 artık bir
**karar toplama** fazı değil, saf bir **üretim ve ölçüm** fazıdır.

**Faz 2 kurucu onayı olmadan AÇILMAZ.**

---

## FAZ DURUMU: **READY_FOR_DECISION**

## KİTAP 1 — FAZ 1 KURUCU ONAYINA HAZIR

---

*Vâliçe Press · TRUE FIT 1 · Faz 1 Raporu · 28 Ağustos 2026*
