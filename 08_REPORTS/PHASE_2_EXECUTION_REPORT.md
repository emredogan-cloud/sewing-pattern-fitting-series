# FAZ 2 YÜRÜTME RAPORU — GÖRSEL SİSTEM + FİGÜR MOTORU

> Kitap 1 · kapı `phase2-visual` · 28 Ağustos 2026
> · yol haritası: [`../BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/PHASE_2_ROADMAP.md`](../BOOK-01-MEASURE-AND-DIAGNOSE/00_SPEC/PHASE_2_ROADMAP.md)
>
> **Kural (`DECISIONS.md K33`): bu belgedeki her sayı, onu üreten
> komutun çıktısından alınmıştır.**

---

## 0 · Bu fazın tek cümlelik özeti

> Faz 1'in **dört tahmininin dördü de yanlıştı** ve dördü de ölçümle
> düzeltildi.

| Ne | Faz 1 tahmini | **ÖLÇÜLEN** | Kayıt |
|---|---|---|---|
| Akış şeması sayısı | 9 | **46** | `K41` |
| Toplam figür | ~123 | **154** | `K41` |
| Figür etiketi yedek yazı tipi | Atkinson Hyperlegible | **IBM Plex Sans** (Atkinson `Y1`'de elendi) | `K38` |
| Satır başına karakter | (belirtilmemiş) | **107,1 → düzen değişti → 83,0** | `K39` |

Faz 2 bir üretim fazı olduğu kadar bir **yanlışlama** fazı oldu.

## 1 · Definition of Done — madde madde

`PHASE_2_ROADMAP § 3`'ün on bir maddesi:

| # | Madde | Durum | Kanıt |
|---|---|---|---|
| 1 | `visual_language_tokens.json` → `CALIBRATED` | ✓ **`CALIBRATED_DIGITAL_RENDER`** | `03_VISUAL/calibration_report.json` |
| 2 | Sayfa geometrisi profili yazılı ve render edilmiş örnekle test edilmiş | ✓ | `03_VISUAL/page_geometry.json` · `PILOT_MATERIAL_A.pdf` |
| 3 | Motor en az akış şemalarını ve ölçüm figürlerini üretiyor | ✓ **sekiz türün hepsini üretiyor** | `06_BUILD/figure_engine.py` |
| 4 | `figures.json` mevcut; her `deterministic:false` figürün gerekçesi var | ✓ **154 kayıt · 49 gerekçe** | `BOOK-01/03_VISUAL/figures.json` |
| 5 | `qa_visual.py` yazılmış + selftest regresyonları | ✓ **on denetim · 12 regresyon** | `06_BUILD/qa_visual.py` |
| 6 | Görsel üretim yükü ölçülmüş (`G6`'nın beş ölçütü) | ✓ | § 4 |
| 7 | `A1` `A4` `A6` `A7` `A8` `A11` kapanmış | ✓ **hepsi kapalı** (`A1`→`A15`→`K36`) | `OPEN_QUESTIONS.md` |
| 8 | Rakip akış takibi başlatılmış | ⏳ **ARAÇ HAZIR, GÖZLEM DIŞ** | `D-04` |
| 9 | Çelişmeli inceleme, `HARD_STOP` bulgusu yok | ✓ | `PHASE_3_ADVERSARIAL_REVIEW.md` |
| 10 | `qa_all.sh` sıfır hata | ✓ | § 6 |
| 11 | `.gate` → `phase2-visual` | ✓ | `BOOK-01/.gate` |

**On bir maddenin onu tamam. Sekizinci madde (`G7` rakip takibi) bir
dış gözlemdir** ve ajan tarafından yapılamaz: bir eğilim ölçümü zamana
yayılmış olmalıdır. Ölçüm **aleti** üretildi
(`08_REPORTS/tracked/COMPETITOR_TRACKING_SHEET.md`), ölçüm **yapılmadı**
ve yapılmış gibi kaydedilmedi.

**Bu madde `phase2-visual` kapısını engellemez** (`PHASE_2_ROADMAP § 2 G7`
kendi metninde *"terk koşulu"* olarak tanımlanmıştır, çıkış ölçütü
olarak değil) ama `EXTERNAL_DEPENDENCIES.md D-04` olarak açık kalır.

## 2 · Token kalibrasyonu — `G1`

**Yöntem:** reportlab ile gerçek trim ölçüsünde (8,5 × 11 inç)
kalibrasyon sayfası → `pdftoppm` ile 300 ve 600 dpi raster → 1-bit'e
indirme → Pillow ile piksel ölçümü.

### 2.1 · Çizgi kalınlığı — dokuzunun dokuzu da hayatta

| Rol | Hedef (pt) | 300 dpi (px) | 600 dpi (px) | 1-bit'te |
|---|---:|---:|---:|---|
| `pattern_edge_modified` | 1,6 | 7 | 14 | ✓ |
| `body_outline` | 1,2 | 5 | 10 | ✓ |
| `garment_outline` · `pattern_edge_original` | 1,0 | 4 | 9 | ✓ |
| `grainline` | 0,9 | 4 | 8 | ✓ |
| `balance_line` | 0,7 | 3 | 6 | ✓ |
| `seam_line` | 0,6 | 3 | 5 | ✓ |
| `construction_line` | 0,5 | 2 | 4 | ✓ |
| **`callout_leader`** | **0,4** | **2** | **3** | ✓ |

En ince çizgi 300 dpi'de **2 piksel** kalıyor ve 1-bit'te kayboluyor
değil. **Ama bu bir DİJİTAL sonuçtur.** Talep-üzerine baskının mürekkep
yayılması ölçüme girmez — `D-06`.

### 2.2 · `TK-05` ↔ `TK-06` — kitabın en önemli ayrımı

`S-0004` (WSU EM4582) kumaşı **çeken** kırışıklığın *az* ease,
**kıvrım hâlinde duran** kırışıklığın *çok* ease gösterdiğini yazar.
İki token karışırsa kitabın en çok kullanılan kuralı çöker.

| Ölçüm | Değer |
|---|---|
| `TK-05` eğrilik endeksi | 0,016 |
| `TK-06` eğrilik endeksi | 0,056 |
| **Oran** | **3,49** (eşik 2,0) |
| Karar | **AYRIK** |

**Metrik iki kez yazıldı.** İlk sürüm mürekkep oranı ve bileşen
sayısına bakıyordu ve `RİSKLİ` veriyordu — çünkü iki işaret de üç
parçadan oluşur ve neredeyse aynı mürekkebi kullanır. **Metrik, ayırt
eden şeyi ölçmüyordu.** Eğrilik ekseni eklendi ve ölçüm parça bazına
indirildi (`K40`).

`TK-06`'nın yay yüksekliği ölçümle 3,2 → 4,6 pt'ye çıkarıldı: 3,2'de
oran 2,4'tü (eşiğin hemen üstünde, dar marj).

### 2.3 · Tipografi

| Test | Sonuç |
|---|---|
| `T1` kesir glifleri | ✓ Source Serif 4 ve Source Sans 3'te **yedisi de** var; ″ (U+2033) var |
| `T1` yan bulgu | **reportlab OpenType `frac` özelliğini UYGULAMAZ** — kesirler ÖNCEDEN BİRLEŞTİRİLMİŞ gliflerle dizilir. Yedi glif (⅛ ¼ ⅜ ½ ⅝ ¾ ⅞) ABD ev dikişinin bütün kesirlerini karşılar |
| `T2` tablo hizalaması | ✓ Motor sabit sütun genişliğiyle diziyor; `tnum` desteğine bırakılmadı |
| `T3` rakam ayırt ediciliği | ⏳ **DIŞ** (`D-05`) — piksel ön elemesi yapıldı |
| `T4` · `T5` · `T6` | ⏳ **DIŞ** (`D-06`) |

**`T3` ön elemesinin bulduğu:** `Inter`'de küçük `l` ile büyük `I`
**piksel piksel aynıdır** (fark 0,000) — bir ölçü etiketinde `Y3`'ün
tam olarak tanımladığı başarısızlık. Elendi.

## 3 · Sayfa geometrisi — `G2`

**Ölçüm düzeni değiştirdi.** İlk profil metin bloğunu tam ölçüye
yaydı; 10,5 pt'de **107,1 karakter/satır** çıktı (rahat okuma bandı
72–88).

**Çözüm:** dar metin sütunu (387,0 pt) + boşluk (9,0 pt) + yan sütun
(108,0 pt) = tam ölçü (504,0 pt). **Ölçülen yeni değer: 83,0 karakter.**

Yan sütun figür başlıklarını, ölçü etiketlerini ve "HENÜZ DEĞİŞTİRME"
uyarılarını taşır; bir uyarı artık gövde metninin akışını **kesmez**.

**Aritmetik hatası — testin bulduğu.** Profilin ilk sürümü tam ölçüyü
499,5 pt yazıyordu; doğrusu `612 − 63 − 45 = 504,0` pt'dir. Hatayı
`selftest.py`'nin sayfa aritmetiği denetimi yakaladı — **bir belge
değil, bir test buldu.**

**KDP asgarileri** (`S-0016`) `qa_visual § ⑨`'da her koşuda
denetleniyor: cilt payı 0,875 in (asgari 0,5), dış/üst/alt 0,625–0,75 in
(asgari 0,25). Sayfa hedefi 300'ü aşarsa bant değişir ve kapı kırmızı
yanar.

## 4 · Görsel üretim yükü — `G6`, beş ölçüt

| Ölçüt | **DEĞER** |
|---|---|
| Toplam figür | **154** (tahmin ~123) |
| Deterministik üretilebilen | **105 · %68,2** |
| `manual_reason` taşıyan | **49** — 43 belirti + 6 toile figürü |
| Bir yayılıma sığmayan şema | **0** (bölmeden sonra; bölme öncesi 11) |
| `photo_required` | **0** / eşik 6 → `A11` yeniden açılmadı |
| `color_required` | **%0,0** / eşik %10 → `A6` yeniden açılmadı |

**49 elle çizim gerektiren figürün hepsinin gerekçesi aynıdır:**
kumaşın gerçek dökümü kayıttan türetilemez. Kıvrımın uzunluğu, sayısı
ve yönü **fiziksel sınamadan** gelir (`D-02`). Bu, `R-05`'in gerçek
büyüklüğüdür: görsel üretim yükünün üçte biri Faz 3'e bağlıdır.

### 4.1 · Akış şeması mimarisi ölçümle değişti

Motor bölge düzeyinde şemaları kurup ölçtü. Sayfanın figür alanı
**504 × 612 pt**'dir:

| Bölge | Belirti | Gereken genişlik | Sığar mı |
|---|---:|---:|---|
| `bust_chest` | 6 | 1956 pt | **hayır** |
| `shoulder` · `waist_torso` · `crotch_leg` | 5 | 1630 pt | **hayır** |
| dört bölge | 4 | 1304 pt | **hayır** |
| `neck` · `armhole` | 3 | 978 pt | **hayır** |

**On bölgenin onu da sığmıyor.** `VISUAL_SPEC § 2` kural 4 uygulandı
(*"sığmıyorsa konu bölünür, şema küçültülmez"*): şemanın birimi
**belirti** oldu → **46 şema**.

## 5 · Yeni kapı: `qa_visual.py`

| # | Denetim | Yakaladığı |
|---|---|---|
| ① | Token bütünlüğü + kalibrasyon durumu | Tanımsız token; kalibre edilmemiş sözlükle kapı geçme |
| ② | Figür ↔ kayıt bağı | Var olmayan `SYM`/`M` referansı |
| ③ | `manual_reason` zorunluluğu | Gerekçesiz elle çizim |
| ④ | Akış şeması kapsaması | Şemasız belirti · boşta biten yol · ulaşılamayan aile |
| ⑤ | Yayılım taşması + genişlik sınıfı | Sayfaya sığmayan figür |
| ⑥ | Ölçek beyanı | Kayıtsız kalıp parçası |
| ⑦ | `A11` eşiği | 6'dan fazla `photo_required` |
| ⑧ | `A6` eşiği | %10'dan fazla `color_required` |
| ⑨ | Sayfa geometrisi | KDP asgarisi ihlali · sayfa bandı taşması |
| ⑩ | **Okur dili** | Figürün proje belge dilinde üretilmesi (`K45`) |

**`figure_tokens.py` ayrıca `VISUAL_STANDARD § 5`'in yasaklarını
çalıştırılabilir hâle getirdi** (`K42`): sayısal etiketsiz ok, vücutta
slash line, ölçeksiz kalıp parçası, izin dışı gri, baskı asgarisinin
altında çizgi, kutudan taşma, tanımsız token, **iç kayıt kimliği**
(`K46`), **çakışan etiket** (`K46`). Her biri çizimi **durduran** bir
istisnadır.

## 6 · Kalite kapıları — son ölçüm

Komut: `bash 06_BUILD/qa_all.sh` · 28 Ağustos 2026

| Kapı | Sonuç |
|---|---|
| `validate_spec.py` | ✓ 0 hata — **18 kaynak** · 43 belirti · 19 aile · 32 ölçü · 148 crosswalk · 12 blok · **154 figür** |
| `validate_structure.py` | ✓ 0 hata (**altı denetim hattı**) |
| `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| `qa_crosswalk.py` | ✓ 0 bulgu — 19/19 aileye ulaşılıyor |
| `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| `qa_claims.py` | ✓ 0 bulgu |
| `qa_terminology.py` | ✓ 0 bulgu |
| **`qa_visual.py`** *(yeni)* | ✓ **0 bulgu** — on denetim |
| **`fetch_fonts.py --verify`** *(yeni)* | ✓ 10 dosya SHA-256 ile doğrulandı |
| **`selftest.py`** | ✓ **116/116** — veri katmanı *(önceki tur: 91)* |
| `kill_gate.py --book book-01` | ✗ **2 engel — BEKLENEN VE DOĞRU** |

## 7 · Bu fazın YAPMADIĞI

Manüskript prozası (pilot hariç) · fiziksel doğrulama · fark testi ·
kapak · KDP dosyası · reklam. Hiçbiri Faz 2'nin işi değildi ve
hiçbirine dokunulmadı.

**Ve yapılamayan üç ölçüm:** gerçek prova baskısı (dot gain), KDP
Previewer, üç insan okuyucu. Üçü de `EXTERNAL_DEPENDENCIES.md`'de
kayıtlıdır ve hiçbiri "yapıldı" diye işaretlenmemiştir.

---

*Vâliçe Press · BEFORE YOU CUT · Phase 2 Execution Report · 28 Ağustos 2026*
