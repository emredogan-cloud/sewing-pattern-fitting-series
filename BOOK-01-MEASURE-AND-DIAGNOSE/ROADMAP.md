# ROADMAP — BEFORE YOU CUT, Book 1: Measure & Diagnose

> Seri bağlamı: [`../SERIES_ROADMAP.md`](../SERIES_ROADMAP.md).
> Kitap kapısı: `.gate` (bu dizinde). Seri kapısı: `../.gate`.
>
> **Sekiz faz.** Bu sayı kardeş projelerin faz sayısıyla aynı olduğu
> için DEĞİL, bu ürünün kendi mühendislik aşamalarının (temel → spec →
> görsel → pilot/kill-gate → üretim → KA → format → lansman) doğal
> olarak sekiz geçiş noktası gerektirdiği için seçildi.

---

## Faz akışı

```text
   P0 Temel                              [.gate = foundation]
    │
    ▼
   P1 Araştırma + İçerik Spesifikasyonu  ✓ TAMAM (kurucu onayı alındı)
    │
    ▼
   P2 Görsel Sistem + Figür Motoru       ✓ TAMAM [phase2-visual]
    │
    ▼
   P3 Pilot + KILL-GATE ──[FAIL]──HARD STOP──► SERİ DURUR
    │  ◄── HÂLÂ BURADA DURUYOR · iki DIŞ ölçüm YAPILMADI (D-01, D-02)
    │  [PASS]
    ▼
   P4 Tam İçerik Üretimi                 [phase4-production]

   ┌─ KURUCU GEÇERSİZ KILMASI (K49) ────────────────────────────┐
   │  P4 üretimi P3 BEKLENMEDEN yürütüldü ve TAMAMLANDI.        │
   │  Kapı: phase4-production-conditional                       │
   │  · "P2 bitti"        → DOĞRU                               │
   │  · "P3 geçildi"      → HÂLÂ YANLIŞ                         │
   │  · "P5 açılabilir"   → HÂLÂ YANLIŞ                         │
   │  ◄── ŞU AN BURADA                                          │
   └────────────────────────────────────────────────────────────┘
    │
    ▼
   P5 KA (teknik · editoryal · görsel · fiziksel)
    │
    ▼
   P6 Format + Render + KDP              [FORMAT DOĞRULAMA KAPISI]
    │
    ▼
   P7 Lansman
```

---

## P0 — PROJE TEMELİ · kapı `foundation`

**Bağımlılık:** seri S0 · **Kurucu bağımlılığı:** DÜŞÜK

**Amaç:** kitabı değil, kitabın yaşayacağı yapıyı kurmak.

| # | Çıktı | Yol |
|---|---|---|
| 1 | Kitap dizin iskeleti (7 dizin) | bu dizin |
| 2 | `book_config.json` | bu dizin |
| 3 | `.gate`, `README.md`, bu belge | bu dizin |
| 4 | Seri politikalarının devralınması (kopya DEĞİL, atıf) | `../00_CONTEXT/` |

**Definition of Done:** `validate_structure.py` bu kitabın zorunlu
belgelerini bulur · `.gate` = `foundation`.

---

## P1 — ARAŞTIRMA + İÇERİK SPESİFİKASYONU · kapı `phase1-spec`

**Bağımlılık:** P0 + seri S1 · **Kurucu bağımlılığı:** **YÜKSEK (onay kapısı)**

**Amaç:** manüskript üretimi başlamadan ÖNCE Kitap 1'in ne olduğunu tam
olarak belirlemek.

### Görevler

- [x] Teknik kapsam tanımı (ne öğretilir, ne bilerek dışlanır)
- [x] Okur tanımı (başlangıç/orta sınırı, ön koşullar, senaryolar)
- [x] Teşhis çerçevesinin tanımlanması (yedi adımlı döngü)
- [x] Konu taksonomisi (43 belirti, 129 aday neden, 10 bölge, 10 belirti sınıfı)
- [x] Her belirti için: ayırt edici kanıt · doğrulayıcı ölçüm · düzeltme ailesi
- [x] Bölüm mimarisi (5 parça, 18 bölüm, ekler)
- [x] Bölüm bazlı spesifikasyonlar
- [x] Kitap 1 → Kitap 2 crosswalk (129 kayıt + 21 açık istisna)
- [x] Görsel spesifikasyon
- [x] Kaynak haritası (teknik iddia → kaynak gereksinimi)
- [x] Fiziksel doğrulama planı
- [x] Farklılaşma testi protokolü
- [x] Ortam kararı çerçevesi (karar VERİLMEDİ — `A4`)
- [x] **Kamu kaynağı taraması ve kaynak katmanının kurulması** — 15
      kayıt, 6 tam metin otorite; **ücretli kaynak satın alınmadı**
      (`A3` KAPANDI, `DECISIONS.md K19`)
- [x] Taksonominin kanıta bağlanması — 16/32 ölçü, 13/19 düzeltme
      ailesi yükseltildi; 43 belirti **bilinçli olarak** yükseltilmedi
- [x] Crosswalk'ın dokuz ilişki üzerinden denetlenmesi — 0 bulgu
      (yeni kapı `qa_crosswalk.py`)
- [x] Kurucu kararlarının kapatılması — 12 kapandı, 1 ertelendi,
      2 dış beklemeye alındı (`OPEN_QUESTIONS.md`)
- [x] Marka çakışma taraması (`A1`) — `08_REPORTS/PHASE_1_BRAND_SCREENING.md`
- [x] GitHub deposu + CI (`A2`) — public, marka-nötr ad, CI yeşil
- [x] **Kurucu onayı** — 28 Ağu 2026 (`DECISIONS.md K36`)

### Definition of Done

1. On zorunlu çıktı `00_SPEC/` altında mevcut (`validate_spec.py §
   check_book_phase1_requirements` denetler).
2. `qa_all.sh` sıfır hata.
3. Taksonominin doğrulama durumu **dürüstçe** kaydedilmiş (sessizce
   yükseltilmemiş).
4. **Kurucu onayı alındı.** ✓ 28 Ağu 2026
5. `.gate` → `phase1-spec`. ✓ *(aynı turda `phase2-visual`'a ilerledi)*

### Çıkış ölçütü — ölçülebilir

| Ölçüt | Eşik | Ölçüldü mü |
|---|---|---|
| Belirti kapsaması: her bölge temsil edildi | 10/10 bölge | ✓ |
| Belirti sınıfı kapsaması | 10/10 sınıf | ✓ |
| Her aday nedenin ayırt edici kanıtı var | %100 | ✓ (şema dayatır) |
| Her düzeltme ailesine Kitap 1'den ulaşılabiliyor | 19/19 | ✓ |
| **Kaynak kaydı** | ≥1 otoriter kaynak | ✓ **15 kayıt · 6 tam metin otorite** |
| **Crosswalk iç bütünlüğü** | 0 bulgu | ✓ **dokuz denetim, 0 bulgu** |
| **Kapanmış kurucu kararı** | mümkün olanların tamamı | ✓ **12/14 + 2 yeni durum** |

### Risk

**YÜKSEK — teknik doğruluk.** Bu faz tüm sonraki fazların dayandığı
veri katmanını kurar. Hata burada yapılırsa aşağı akışta katlanarak
çoğalır. Mekanik koruma: `verification_status` alanları kanıtsız
yükseltilemiyor.

---

## P2 — GÖRSEL SİSTEM + FİGÜR MOTORU · kapı `phase2-visual`

**Bağımlılık:** P1 onayı · **Kurucu bağımlılığı:** ORTA (`A4`, `A6`, `A7`, `A8`, `A11`)

**Amaç:** seri çizim dilini (18 token) bu kitapta **instantiate** etmek
ve figürleri kayıt verisinden üretecek motoru yazmak.

| # | Çıktı |
|---|---|
| 1 | Kalibre edilmiş `visual_language_tokens.json` (gerçek render testiyle) |
| 2 | Figür üretim motoru (`06_BUILD/`) |
| 3 | `03_VISUAL/figures.json` — bu kitabın figür kayıtları |
| 4 | Font kararı + lisans kaydı (`A7`) |
| 5 | Sayfa geometrisi profili (trim, kenar boşluğu, figür alanı) |
| 6 | `qa_visual.py` — figür/token/geometri tutarlılık kapısı |

**Kurucu kararları — Faz 1 yürütmesinde ÖNCEDEN kapatıldı:**
`A4` (ortam) · `A6` (renk) · `A7` (font) · `A8` (birim) ·
`A11` (fotoğraf). `A1`'in yerini **`A15`** aldı (yerine geçen seri adı
+ profesyonel marka temizliği) ve **dış beklemededir** — kapak
sisteminin taslaklanması ondan önce başlayamaz.

Faz 2 bu yüzden artık bir **karar toplama** fazı değil, saf bir
**üretim ve ölçüm** fazıdır.

**Definition of Done: ✓ KARŞILANDI.** Deterministik oran **ölçüldü:
%68,2** (105/154) · `deterministic: false` olan **49 figürün hepsinin**
`manual_reason`'ı var · `.gate` → `phase2-visual` ✓

**Ölçümün Faz 1 tahminlerini yanlışladığı dört nokta:** akış şeması
9 → **46** · toplam figür ~123 → **154** · yedek yazı tipi Atkinson →
**IBM Plex Sans** · satır ölçüsü 107,1 → **83,0** karakter.
Rapor: [`../08_REPORTS/PHASE_2_EXECUTION_REPORT.md`](../08_REPORTS/PHASE_2_EXECUTION_REPORT.md)

**Risk:** ORTA–YÜKSEK. Diyagram hacmi tahminden büyük çıkabilir
(`RISK_REGISTER R-05`). Bu fazın çıktısı o hacmi **ölçer**.

---

## P3 — PİLOT + KİLL-GATE · kapı `phase3-pilot` · **HARD STOP**

**Bağımlılık:** P2 · **Kurucu bağımlılığı:** **KRİTİK** (`A13`, `A14`)

**Amaç:** ürünü doğrulamak değil, **yanlışlamak.**

| # | Çıktı |
|---|---|
| 1 | Pilot kesit: bir tam teşhis bölümü + akış şeması + figürler (`04_EDITORIAL/pilot/`) |
| 2 | **Fark testi** sonucu — `08_REPORTS/PHASE_3_DIFFERENTIATION_TEST.md` |
| 3 | **Fiziksel doğrulama** kayıtları — `VAL-xxxx` |
| 4 | Bağımsız çelişmeli inceleme — `08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md` |

### İki kill-gate

| # | Ölçüm | PASS koşulu | FAIL sonucu |
|---|---|---|---|
| ① | **Fark testi** — pilot bölüm, liderin aynı konudaki bölümüyle yan yana, üç gerçek ev dikişçisine | En az **2/3** okur farkı **kendiliğinden** söyler | Farklılaşma hipotezi çürük → **SERİ DURUR** |
| ② | **Fiziksel doğrulama** — pilotun her diyagramı kalıba uygulanır, toile dikilir | Hata oranı **%0** | >%0 → pilot durur, kök nedenden düzeltilir. **>%5 → üretim yöntemi reddedilir, proje durur** |

**Bu kapı depo içinden ölçülemez.** `kill_gate.py` yalnızca ön koşulları
ve kaydı denetler. **AI vekil testi insan testinin yerine SAYILMAZ**
(`DECISIONS.md K6`; `aiProxyCountsAsHuman: false`, açılamaz).

**Definition of Done:** iki ölçüm de yapıldı ve `series_config.json`'a
kaydedildi · ikisi de PASS · `.gate` → `phase3-pilot`.

**DURUM: içeriden yapılabilen KISIM TAMAM, ölçümler YAPILMADI.**

| Çıktı | Durum |
|---|---|
| Pilot kesit (Malzeme A) | ✓ **8 sayfa, markasız, 7 gerçek figür** |
| Fark testi sonucu | ✗ **0/3 katılımcı** — `D-01` |
| Fiziksel doğrulama kayıtları | ✗ **0/19 yapıldı** (kit üretildi) — `D-02` |
| Çelişmeli inceleme | ✓ **11 bulgu, HARD_STOP yok** |

Rapor: [`../08_REPORTS/PHASE_3_PILOT_PACKAGE.md`](../08_REPORTS/PHASE_3_PILOT_PACKAGE.md)

**Risk:** **KRİTİK — bu projenin tek gerçek durma noktası.** Kardeş
projelerin kill-gate'lerinin gerçekten başarısız olabildiği kanıtlandı
(Enigmatica A12, Hangıl Faz 4 REVISE). Bu kapı da gerçekten HARD STOP
verebilmelidir.

---

## P4 — TAM İÇERİK ÜRETİMİ · kapı `phase4-production-conditional`

**Bağımlılık:** ~~P3 PASS~~ → **KURUCU GEÇERSİZ KILMASI** (`DECISIONS.md K49`)
· **Kurucu bağımlılığı:** DÜŞÜK

**Amaç:** pilot mimarisini tam kitaba ölçeklemek.

> ⚠ **Bu faz, bağımlılığı KARŞILANMADAN yürütüldü.** Kurucu 29 Ağustos
> 2026'da üretimin sürmesine izin verdi ve aynı talimatta eksik P3
> sonuçlarının PASS yazılmasını **açıkça yasakladı**. Kapı bu yüzden
> `phase4-production` DEĞİL, `phase4-production-conditional`'dır ve
> kümülatif sırada `phase3-pilot`'ın **önündedir**: yapılan iş kayıtlı,
> yapılmayan ölçüm hâlâ yapılmamış.

### Yürütüldü

| # | Çıktı | Ölçüm |
|---|---|---|
| 1 | Tam manüskript | **231 sayfa · 21 bölüm · 35 472 kelime** |
| 2 | 43 belirti girişi | tamamı bölge atlasında · her biri yeniden gözlem adımı + belirtiye özgü eleme + "henüz değiştirme" taşıyor |
| 3 | Figür entegrasyonu | **160/160** yerleştirilebilir figür kullanıldı · 175 yerleşim |
| 4 | İddia sicili | **307 iddia**, kanıt seviyesi TÜREVdir |
| 5 | İddia→kaynak haritası | `00_SPEC/CLAIM_SOURCE_MAP.md` (üretilen) |
| 6 | Bağımsız teknik inceleme | dört hat · **149 bulgu** · 68 kaynak · **132 revizyon** |
| 7 | Yeni kapı | `qa_manuscript.py` — on bir denetim |
| 8 | Yeni dizgi katmanı | `typeset.py` (TEK yol) + `build_book.py` |
| 9 | Vücut varyantları | `B-05` kapatıldı — 26/43 belirti figürü artık standart-dışı bir gövde kullanıyor |

### Çelişmeli inceleme kısıtları — durum

| Bulgu | Faz 4'te ne oldu |
|---|---|
| `B-01` yeniden gözlem döngüsü | **KAPATILDI** — yapısal, 43/43 girişte; ayrıca `flow_CYCLE` şemasında döngüyü kapatan çizgi |
| `B-02` `AF-18` bir çıkış kapısıdır | **KAPATILDI** — o düğüme giden her yol "bu bir beden kararıdır" ile karşılanıyor |
| `B-03` eleme listesi çok uzun | **KAPATILDI** — belirtiye özgü üç kalem + tam liste Bölüm 8'de bir kez |
| `B-05` tek kroki | **KAPATILDI** — üç varyant, veriden türetilerek atanıyor, `qa_visual § ⑪` koruyor |
| `B-08` sayfa bütçesi | **AŞILDI ve GEREKÇELENDİ** — atlas 177 s.; toplam 232 s. bandın içinde |
| `B-04` figürlerde gerçek kumaş dökümü yok | **AÇIK** — `D-02`'ye bağlı |
| `B-06` ⅝ inç dikiş payı | **KAPATILDI** — Bölüm 3 ve 4 payı varsaymıyor, kalıbın beyanına yönlendiriyor |

**Definition of Done — karşılanan:** 18 bölümün tamamı + Parça 0 +
ekler yazıldı · 43 belirtinin tamamı yerleşti · manüskript kapısı 0
bulgu · sayfa bütçesi içinde · bağımsız inceleme tamamlandı ·
`.gate` → `phase4-production-conditional`.

**Karşılanmayan:** `.gate` → `phase4-production` (P3'ün PASS'ini ister
ve P3 ölçülmedi).

Rapor: [`../08_REPORTS/PHASE_4_EXECUTION_REPORT.md`](../08_REPORTS/PHASE_4_EXECUTION_REPORT.md)

---

## P5 — KA · kapı `phase5-qa`

**Bağımlılık:** P4 · **Kurucu bağımlılığı:** DÜŞÜK

Dört hat: **teknik** (taksonomi ↔ metin tutarlılığı, kaynak
izlenebilirliği) · **editoryal** (dil, terim, tekrar) · **görsel**
(token tutarlılığı, ölçek, okunabilirlik) · **fiziksel** (tam kitabın
diyagram örneklemi yeniden dikilir).

**Definition of Done:** `qa_all.sh` tam kitap üzerinde sıfır hata ·
ikinci bağımsız çelişmeli inceleme turu tamamlandı · fiziksel örneklem
hata oranı %0 · `.gate` → `phase5-qa`.

---

## P6 — FORMAT + RENDER + KDP · kapı `phase6-format`

**Bağımlılık:** P5 · **Kurucu bağımlılığı:** ORTA (`A5`)

### FORMAT DOĞRULAMA KAPISI

1. Gerçek KDP maliyet hesaplayıcısıyla baskı maliyeti **ölçülür**.
2. Seçilen trim/cilt seçeneğinin KDP'de **mevcut olduğu** doğrulanır.
3. **KDP Previewer'ın kendisi** çalıştırılır — yerel render başarısı
   YETERLİ DEĞİLDİR.
4. Fiziksel prova baskı alınır; düz açık durma ve figür okunabilirliği
   **elle** test edilir.

**Hiçbir fiyat/telif kararı bu kapıdan önce kesinleşemez.**

**Definition of Done:** dört madde de yapıldı · `.gate` → `phase6-format`.

---

## P7 — LANSMAN · kapı `release`

**Bağımlılık:** P6 · **Kurucu bağımlılığı:** YÜKSEK

Kapak (`A1` marka taraması KAPANMIŞ olmalı) · metadata (marka taraması
`validate_structure.py`'den geçmeli) · fiyat · reklam testi planı
(`A12` yazılı eşikle) · Kitap 2'nin P0-P1'inin açılması.

**Definition of Done:** yayında · `.gate` → `release` · Kitap 1'in
GERÇEK verisine dayanan Kitap 2 girdi notu yazıldı.

---

## Kurucu kararları — bu yol haritasının varsaydığı ama kesinleştirmediği

| # | Konu | Hangi fazda kapanmalı |
|---|---|---|
| A1 | "TRUE FIT" marka taraması | ✓ KAPANDI (`K18`) — yerine `A15`/`A16` |
| A3 | **Kaynak edinim bütçesi** | **P1 kapanışı** |
| A4 | Ortam (QR/video) | P2 sonu |
| A6 | Renk stratejisi | P2 |
| A7 | Font lisansı | P2 |
| A8 | Birim sunumu | P2 |
| A11 | Fotoğraf kullanımı | P2 |
| A13 | Fiziksel doğrulama kapsamı | P3 öncesi |
| A14 | Fark testi katılımcıları | P3 öncesi |
| A5 | Format/fiyat | P6 |

Tam liste ve gerekçeler: [`../OPEN_QUESTIONS.md`](../OPEN_QUESTIONS.md).

---

*Vâliçe Press · BEFORE YOU CUT, Book 1 · Roadmap · 28 Ağustos 2026 (Faz 2 sonrası)*
