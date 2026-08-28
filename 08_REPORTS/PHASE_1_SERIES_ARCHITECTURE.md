# FAZ S1 RAPORU — SERİ MİMARİSİ + KİTAP 1 FAZ 1 SPESİFİKASYONU

> **Faz durumu: READY_FOR_DECISION**
>
> Araştırma/mimari işi tamamlandı. **Bir kurucu kararı kapı
> ilerletmesinden önce gerekiyor** (§ 8).
>
> Tarih: 28 Ağustos 2026 · Seri kapısı: `bootstrap` (**ilerlemedi**)

---

## 1 · Yönetici özeti

Kabul edilmiş pazar kararı (dikiş kalıp uyumu, 7,02/10) ürün mimarisine
çevrildi. Üç kitaplık seri için ortak mimari kuruldu ve **Kitap 1'in
Faz 1'i tam olarak spesifiye edildi**.

Üretilen çekirdek entelektüel varlık: **43 uyum belirtisi, 129 aday
neden**, her aday nedenin kendi **ayırt edici kanıtı** ve **doğrulayıcı
ölçümü** ile birlikte; 19 düzeltme ailesi; 32 ölçü noktası; 148
crosswalk kaydı; 35 topikli sınır matrisi; 20 terimlik sözlük; 18
token'lık çizim dili.

**Faz 1'in en önemli çıktısı bir sayı değil, bir mimaridir:** belirti
ile nedenin şema düzeyinde ayrılması. `symptom_schema.json`, ayırt edici
kanıtı olmayan bir nedenin **yazılmasını mekanik olarak engeller.**

## 2 · Üretilen çıktılar

### Seri düzeyi (12/12)

| # | Çıktı | Yol |
|---|---|---|
| 1 | Konumlandırma | `00_CONTEXT/SERIES_POSITIONING.md` |
| 2 | Sınır matrisi (35 topik) | `SERIES_CONTENT_ARCHITECTURE.md` + `boundary_matrix.json` |
| 3 | Anahtar kelime mimarisi | `SERIES_KEYWORD_ARCHITECTURE.md` |
| 4 | Çapraz satış mimarisi | `SERIES_CROSSSELL_ARCHITECTURE.md` |
| 5 | Görsel dil (18 token) | `VISUAL_STANDARD.md` + `visual_language_tokens.json` |
| 6 | Kaynak politikası (9 katman) | `SOURCING_STANDARD.md` |
| 7 | KA standardı | `QA_STANDARD.md` |
| 8 | Fiziksel doğrulama protokolü | `VALIDATION_PROTOCOL.md` |
| 9 | Terminoloji (20 terim) | `terminology.json` |
| 10 | Taksonomiler | `02_TAXONOMY/public/*.json` |
| 11 | **Kitap 1 Faz 1 spesifikasyonu (10 belge)** | `BOOK-01/00_SPEC/` |
| 12 | Kitap 2 ve 3 yol haritaları | `BOOK-0x/ROADMAP.md` |

### Kitap 1 Faz 1 — on zorunlu çıktı

`SCOPE` · `CONTENT_ARCHITECTURE` · `CHAPTER_SPECS` · `DIAGNOSTIC_SYSTEM`
· `DIAGNOSIS_TO_ADJUSTMENT_MAP` · `VISUAL_SPEC` · `SOURCE_MAP` ·
`VALIDATION_PROTOCOL` · `DIFFERENTIATION_TEST` · `PHASE_2_ROADMAP`

Mekanik denetim: `validate_spec.py § check_book_phase1_requirements`.

## 3 · Ana mimari kararlar

| # | Karar | Neden |
|---|---|---|
| **K3** | İki katmanlı kapı | Üç kitap kısmen paralel ilerler |
| **K5** | Kill-gate: ikili DIŞ ölçüm | Bu projenin kapısı depo içinden ölçülemez |
| **K6** | AI vekil insan yerine SAYILMAZ, bayrak açılamaz | Hangıl K20 dersinin sertleştirilmesi |
| **K7** | "Basılı avantaj" iddiası kalıcı korumada | Araştırma raporu § 27: ZAYIF |
| **K13** | Sınır matrisi TOPİK BÖLME ile düzeltildi | Kopyalama yerine bölme |
| **K16** | Türkçe katlama TEK KOPYA (`trfold.py`) | Koruma üç yerde tekrarlanırsa dördüncüde unutulur |

## 4 · Kapıların gerçekten çalıştığının kanıtları

Bir kapı, kendi kusurunu yakalamadıkça kapı değildir. Bu turda **dört**
gerçek yakalama oldu:

| # | Kapı | Ne buldu | Sonuç |
|---|---|---|---|
| 1 | `validate_spec.py` | `M-011.path_rule` şema minimum uzunluğunun altında | İçerik düzeltildi |
| 2 | `qa_boundary.py` | `AF-19`'a hiçbir Kitap 1 belirtisinden ulaşılamıyor | **`SYM-043` eklendi** (K15) |
| 3 | `qa_terminology.py` | Anahtar kelime belgesinde yasak eşanlamlı | Kural doğru, KAPSAM yanlıştı → ayrı `KEYWORD_FILES` muafiyeti (K14) |
| 4 | **`selftest.py`** | Türkçe büyük "İ" kusuru **ÜÇÜNCÜ** bir doğrulayıcıda hâlâ açık | Katlama tek kopyaya çıkarıldı (K16) + regresyon testi |

Dördüncüsü özellikle değerlidir: kardeş projede *sonradan* bulunmuş bir
kusurun bu depoda **üçüncü** bir yerde hâlâ açık olduğunu, kapının kendi
testi buldu.

## 5 · Ölçümler

| Ölçüt | Değer |
|---|---|
| Uyum belirtisi | 43 |
| Aday neden | 129 |
| Bölge kapsaması | 10/10 |
| Belirti sınıfı kapsaması | 10/10 |
| Düzeltme ailesi | 19 |
| Kitap 1'den ulaşılabilen aile | **19/19** |
| Ölçü noktası | 32 |
| Crosswalk kaydı | 148 (129 + 19) |
| Açık istisna | 21 |
| Sınır topiği | 35 (30 sahipli + 5 tamamen dışlanmış) |
| Terim | 20 |
| Görsel token | 18 |
| Belge | 44 |
| Doğrulayıcı script | 10 |
| `selftest` denetimi | **77/77** |
| **Kaynak kaydı** | **0** |
| **Fiziksel doğrulama** | **0** |

## 6 · SINIRLAMALAR — bu raporun en önemli bölümü

### ① Sıfır kaynak, doğrulanmamış taksonomi

106 taksonomi kaydının (43 belirti + 19 aile + 32 ölçü + 12 blok)
**tamamı `agent_drafted_unverified`.** Kaynak sicili **boştur**.

Bu bir ihmal değil, bir **kısıt**tır: otoriter kalıp/uyum referansları
satın alınması gereken basılı kitaplardır; ajan künye uyduramaz.

**Sonuç:** görev talimatı § 37 "validated diagnostic system" istiyor.
Teslim edilen şey *tanımlanmış ve içsel olarak tutarlı* bir sistemdir.
**Dış doğrulama yapılmadı** ve bu ayrım hiçbir belgede
bulanıklaştırılmadı (`DIAGNOSTIC_SYSTEM.md § 0`).

Karar: `OPEN_QUESTIONS A3` — **Faz 1'in kapanış koşulu.**

### ② Okur tanımı devralındı, doğrulanmadı

Hedef okur profili araştırma raporundan alındı; bu depoda bağımsız
olarak sınanmadı. Doğrulama Faz 3 fark testindedir.

### ③ Farklılaşma hipotezi kanıtlanmadı

D1 ("teşhis-önce daha anlaşılır") bir `HYPOTHESIS`'tir. Kill-gate'e
bağlandı; FAIL → **seri durur**.

### ④ D2 hipotezi de sınanmadı

"Rakiplerde sahte neden eleme sisteminin sistematik karşılığı yok"
iddiası bir `HYPOTHESIS`'tir; rakip yapı incelemesiyle sınanmalıdır.

### ⑤ Görsel yük tahmin edildi, ölçülmedi

~123 figür bir **tahmindir**. Gerçek sayı Faz 2'de ölçülür.

### ⑥ Sayfa ve fiyat hedefleri `PROVISIONAL`

Araştırma raporunun tüm ekonomi modeli `ESTIMATE` etiketlidir.
`phase6-format` doğrulama kapısından önce kesinleşemez.

### ⑦ Bu turda yapılMAYAN dış işler

Marka taraması (`A1`) · kaynak edinimi (`A3`) · spiral fizibilitesi
(`A5`) · rakip akış takibi (13 başlık, 90 gün) · reklam testi.
Hiçbiri "yapıldı" gibi kaydedilmedi.

## 7 · Riskler

14 risk kayıtlı; 4'ü **YÜKSEK**: ortam (`R-01`), talep tavanı (`R-02`),
farklılaşma (`R-03`), teknik doğruluk (`R-04`).
Tam liste: `RISK_REGISTER.md`.

## 8 · KURUCU KARARI GEREKİYOR

Bu faz **kendi başına kapanamaz.**

| Karar | Soru |
|---|---|
| **Onay** | Kitap 1 Faz 1 spesifikasyonu kabul ediliyor mu? |
| **`A3`** | Kaynak edinim bütçesi — üç seçenekten hangisi? (`SOURCE_MAP.md § 2`) |

**Onay verilirse:** `.gate` → `series-architecture`,
`BOOK-01/.gate` → `phase1-spec`, Faz 2 açılır.

**Onay verilmezse:** düzeltme turu planlanır; hiçbir üretim başlamaz.

---

## FAZ DURUMU: **READY_FOR_DECISION**

## KİTAP 1 — FAZ 1 KURUCU ONAYINA HAZIR

---

*Vâliçe Press · TRUE FIT · Faz S1 Raporu · 28 Ağustos 2026*
