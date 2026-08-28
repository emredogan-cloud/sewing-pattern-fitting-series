# BOOK-01-PHASE-2-ROADMAP

> Faz 1 çıktısı 10/10. Görev talimatı § 37.
>
> ✓ **BU FAZ YÜRÜTÜLDÜ.** Kurucu onayı 28 Ağustos 2026'da alındı
> (`DECISIONS.md K36`) ve faz aynı turda tamamlandı.
> Sonuç raporu: [`../../08_REPORTS/PHASE_2_EXECUTION_REPORT.md`](../../08_REPORTS/PHASE_2_EXECUTION_REPORT.md)
>
> Aşağıdaki plan **değiştirilmedi** — planla sonucun karşılaştırılabilir
> kalması için. On bir DoD maddesinin **onu karşılandı**; sekizincisi
> (`G7` rakip takibi) bir dış gözlemdir ve `EXTERNAL_DEPENDENCIES.md
> D-04` olarak açık kaldı.

---

## Faz 2 — GÖRSEL SİSTEM + FİGÜR MOTORU · kapı `phase2-visual`

**Amaç:** serinin 18 token'lık çizim dilini bu kitapta somutlaştırmak,
figürleri **kayıt verisinden üreten** motoru yazmak ve görsel üretim
yükünü **ölçmek**.

**Bağımlılık:** Faz 1 kurucu onayı · **Kurucu bağımlılığı:** ORTA–YÜKSEK

---

## 1 · Bu fazda KAPANMASI GEREKEN kurucu kararları

Faz 2 bir üretim fazı değil, aynı zamanda bir **karar toplama fazıdır**.
Beş açık karar burada kapanmazsa Faz 3 pilotu üretilemez.

| # | Karar | Neden Faz 2'de | **Sonuç** |
|---|---|---|---|
| `A1` | "TRUE FIT" marka taraması | Kapak sistemi ve seri kimliği burada taslaklanır | ✓ `K18` → `A15` → **`K36` BEFORE YOU CUT** |
| `A4` | Ortam: QR→video | Sayfa düzenini ve figür sayısını doğrudan etkiler |
| `A6` | Renk stratejisi | Token kalibrasyonunun girdisi |
| `A7` | Font ve lisans | Sayfa geometrisinin girdisi |
| `A8` | Birim sunumu (inç / inç+cm) | Her ölçüm figürünün etiketini etkiler |
| `A11` | Fotoğraf kullanımı | Üretim hattını ve gizlilik protokolünü belirler |

---

## 2 · Görevler

### G1 · Token kalibrasyonu

`visual_language_tokens.json` şu anda `DESIGN_TARGET_NOT_CALIBRATED`.
Her çizgi kalınlığı, kesik deseni ve etiket boyutu **gerçek render
testiyle** ölçülür: baskı ölçeğinde ayırt edilebiliyor mu, 1-bit
baskıda kayboluyor mu, küçültülmüş figürde okunuyor mu.

**Çıktı:** `status: CALIBRATED` + ölçüm raporu.

### G2 · Sayfa geometrisi profili

Trim, kenar boşluğu, sütun, figür alanı, minimum figür genişliği.
**Kısıt:** "bir yayılım, bir kavram" kuralı (`VISUAL_SPEC.md § 6`) —
sayfa geometrisi bu kuralı desteklemelidir.

### G3 · Figür motoru

Kayıt verisinden (`fit_signs.json`, `measurements.json`,
`crosswalk.json`) figür üreten deterministik üretim hattı.

**Öncelik sırası** — en yüksek deterministik kazancı olandan:

1. **Akış şemaları (9)** — taksonomi verisinden **tamamen** türetilebilir
2. **Ölçüm figürleri (≥32)** — ölçü kaydından yol + işaret noktası
3. **Tablolar (≥12)** — veriden doğrudan
4. **Kalıp parçası figürleri (~8)** — geometrik
5. Belirti figürleri (≥43) — kısmen elle

### G4 · `figures.json` — bu kitabın figür sicili

Her figür bir kayıt olur (`figure_schema.json`). `deterministic: false`
olan her figür bir `manual_reason` taşımak **zorundadır**.

### G5 · `qa_visual.py` — yeni kapı

| Denetim | Ne yakalar |
|---|---|
| Token bütünlüğü | Tanımsız token kullanımı |
| Figür↔kayıt bağı | Var olmayan `SYM-xxx`/`M-xxx`'e referans |
| `manual_reason` zorunluluğu | Gerekçesiz elle çizim |
| Akış şeması kapsaması | Boşta biten yol (bir düğüm ne `AF-xx`'e ne eleme kalemine gitmiyor) |
| Yayılım taşması | Bir yayılıma sığmayan şema |
| Ölçek beyanı | Ölçek belirtilmemiş kalıp parçası |

### G6 · Görsel üretim yükünün ÖLÇÜLMESİ

`RISK_REGISTER R-05`'in gerçek büyüklüğü burada bulunur:

| Ölçüt | Neden |
|---|---|
| Deterministik üretilebilen figür oranı | Yeniden kullanım ekonomisinin temeli |
| Ortalama elle çizim süresi | Faz 4'ün takvim tahmini |
| Toplam figür sayısı (gerçek) | Faz 1'in ~123 tahmini doğru mu |
| Bir yayılıma sığmayan şema sayısı | Konu bölme ihtiyacı |
| `photo_required` figür sayısı | `A11` kararının maliyeti |

### G7 · Rakip akış takibinin BAŞLATILMASI

Araştırma raporu § 35 madde 6: Haz–Ağu 2026'da giren 13 yeni başlığın
yorum/BSR gelişimi 90 gün izlenmeli. **Bu takip henüz başlatılmadı**
(`RISK_REGISTER R-08`). Faz 2 bunun için doğru yerdir: uzun sürer ve
Faz 3 kararını besler.

**Terk koşulu:** biri 6 ayda 200+ yoruma ulaşırsa niş bizim girişimizden
önce kapanmış demektir.

### G8 · Bağımsız çelişmeli inceleme

Faz 2'nin çıktısını çürütmeye çalışan bağımsız bir inceleme turu.
Çıktı: `08_REPORTS/PHASE_2_ADVERSARIAL_REVIEW.md`.

⚠ Bu **bir insan uzman incelemesi değildir** ve hiçbir yerde öyle
sunulamaz (`CLAIMS_STANDARD.md § 1`).

---

## 3 · Definition of Done

1. `visual_language_tokens.json` → `CALIBRATED`.
2. Sayfa geometrisi profili yazılı ve render edilmiş bir örnekle test edilmiş.
3. Figür motoru en az akış şemalarını ve ölçüm figürlerini **üretiyor**.
4. `figures.json` mevcut; her `deterministic: false` figürün gerekçesi var.
5. `qa_visual.py` yazılmış ve `selftest.py`'ye regresyon testleri eklenmiş.
6. Görsel üretim yükü **ölçülmüş** (G6'nın beş ölçütü).
7. `A1`, `A4`, `A6`, `A7`, `A8`, `A11` kararları **kapanmış**.
8. Rakip akış takibi **başlatılmış**.
9. Çelişmeli inceleme tamamlanmış, HARD_STOP bulgusu yok.
10. `qa_all.sh` sıfır hata.
11. `.gate` → `phase2-visual`.

## 4 · Çıkış ölçütü — ölçülebilir

| Ölçüt | Eşik |
|---|---|
| Deterministik figür oranı | **ÖLÇÜLÜR** — eşik Faz 2'de belirlenir, önceden varsayılmaz |
| Boşta biten akış yolu | **0** |
| Gerekçesiz elle çizim | **0** |
| Kapanmamış YÜKSEK aciliyetli karar | **0** |

## 5 · Riskler

| Risk | Azaltma |
|---|---|
| Diyagram hacmi tahminden büyük (`R-05`) | G6 hacmi ölçer; büyükse kapsam Faz 3 öncesi daraltılır |
| Ortam kararı (`A4`) geciker ve sayfa düzenini bloke eder | Varsayılan: QR alanına yer bırakan geri dönülebilir düzen (`K8`) |
| Token kalibrasyonu 1-bit baskıda başarısız | Öncesi/sonrası ayrımı zaten renkle değil ton+kalınlıkla kurulu |
| Font lisansı ücretli çıkar (`A7`) | Kurucu-teslim istek kuyruğu deseni; açık kaynak önce araştırılır |

## 6 · Faz 2'nin YAPMAYACAĞI

Manüskript prozası · pilot bölüm (Faz 3) · fiziksel doğrulama (Faz 3) ·
fark testi (Faz 3) · kapak · KDP dosyası · reklam.

---

*Vâliçe Press · TRUE FIT 1 · Phase 2 Roadmap (planlandı, yürütülmedi) · 28 Ağustos 2026*
