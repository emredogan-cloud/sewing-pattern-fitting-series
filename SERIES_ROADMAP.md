# SERIES ROADMAP — TRUE FIT

> Görev talimatı § 34. Üç kitaplık serinin tam yaşam döngüsü.
>
> Kitap bazlı yol haritaları: `BOOK-0x/ROADMAP.md`.
> İlerleme ölçümü: `ROADMAP_PROGRESS.md`.

---

## 1 · İki katmanlı kapı sistemi

Kardeş projeler tek kitaplıktır ve tek düz bir `.gate` taşır. Bu depo
üç kitap taşır ve kitaplar **kısmen paralel** ilerler — tek bir düz
kapı bunu ifade edemez (`DECISIONS.md K3`).

| Katman | Dosya | Ölçtüğü |
|---|---|---|
| **Seri kapısı** | `.gate` | Ortak mimarinin donma derecesi |
| **Kitap kapısı** | `BOOK-0x/.gate` | O kitabın kendi faz ilerlemesi |

Biri diğerini **otomatik ilerletmez.**

### Seri kapı sırası

```
bootstrap → series-architecture → production → catalog → release
```

| Kapı | Anlamı |
|---|---|
| `bootstrap` | Proje makinesi kuruldu (dizin, şema, doğrulayıcı, CI, belgeler) |
| `series-architecture` | Ortak mimari donduruldu **ve Kitap 1 Faz 1 kurucu tarafından ONAYLANDI** |
| `production` | En az bir kitap kill-gate'ini geçti; tam üretim açık |
| `catalog` | ≥2 kitap yayında; çapraz satış ve reklam mimarisi canlı |
| `release` | Seri tamamlandı |

### Kitap kapı sırası (üç kitapta aynı)

```
init → foundation → phase1-spec → phase2-visual → phase3-pilot
     → phase4-production → phase5-qa → phase6-format → release
```

## 2 · Seri akışı

```text
  S0  SERİ BOOTSTRAP                       [.gate = bootstrap]
       │  dizin · şema · doğrulayıcı · CI · politika belgeleri
       ▼
  S1  SERİ MİMARİSİ                        ◄── BU TURDA BURADAYIZ
       │  konumlandırma · sınır matrisi · görsel dil · terminoloji
       │  kaynak politikası · KA standardı · doğrulama protokolü
       │  + KİTAP 1 FAZ 1 SPESİFİKASYONU
       │
       ╞═══ KURUCU ONAY KAPISI ═══════════════════════════════╡
       │    Onaysız .gate → series-architecture YÜKSELMEZ
       ▼
  S2  KİTAP 1 YAŞAM DÖNGÜSÜ (P0→P7)
       │      └─ P3 KILL-GATE ──[FAIL]──► SERİ DURUR
       │                                  (farklılaşma hipotezi çürük)
       │  [PASS]
       ├──────────────► KİTAP 2 P0-P1 BAŞLAYABİLİR (paralel)
       ▼
  S3  KİTAP 2 YAŞAM DÖNGÜSÜ
       │
       ├──────────────► KİTAP 3 P0-P1 BAŞLAYABİLİR (paralel)
       ▼
  S4  KİTAP 3 YAŞAM DÖNGÜSÜ
       ▼
  S5  SERİ KA / KATALOG SİSTEMİ            [.gate = catalog → release]
          çapraz satış ölçümü · bağlanma oranı · reklam testi
```

## 3 · Faz tanımları

### S0 — SERİ BOOTSTRAP · `bootstrap`

**Amaç:** kitabı değil, kitapları üretecek **makineyi** kurmak.

| # | Çıktı | Yol |
|---|---|---|
| 1 | Dizin iskeleti (seri + 3 kitap) | depo kökü |
| 2 | `series_config.json`, 3× `book_config.json` | kök + kitaplar |
| 3 | `.gate` × 4, `.gitignore`, `LICENSE` | kök + kitaplar |
| 4 | Kök belgeleri (8 dosya) | depo kökü |
| 5 | Politika belgeleri (17 dosya) | `00_CONTEXT/` |
| 6 | Şemalar (6 dosya) | `01_SOURCE/`, `02_TAXONOMY/`, `03_VISUAL/` |
| 7 | Araç zinciri (9 script) | `06_BUILD/`, `07_TESTS/` |
| 8 | CI iş akışı | `.github/workflows/` |
| 9 | Git deposu, ilk commit | depo kökü |

**Definition of Done:** `bash 06_BUILD/qa_all.sh` sıfır hata · `.gate` = `bootstrap`

**Kurucu bağımlılığı:** DÜŞÜK

---

### S1 — SERİ MİMARİSİ · `series-architecture`

**Amaç:** üç kitabın da uyacağı ortak mimariyi kurmak ve Kitap 1'in
Faz 1'ini tam olarak spesifiye etmek.

| # | Çıktı | Yol |
|---|---|---|
| 1 | Konumlandırma | `00_CONTEXT/SERIES_POSITIONING.md` |
| 2 | Sınır matrisi (35 topik) | `SERIES_CONTENT_ARCHITECTURE.md` + `boundary_matrix.json` |
| 3 | Anahtar kelime mimarisi | `SERIES_KEYWORD_ARCHITECTURE.md` |
| 4 | Çapraz satış mimarisi | `SERIES_CROSSSELL_ARCHITECTURE.md` |
| 5 | Görsel dil (18 token) | `VISUAL_STANDARD.md` + `visual_language_tokens.json` |
| 6 | Kaynak politikası | `SOURCING_STANDARD.md` |
| 7 | KA standardı | `QA_STANDARD.md` |
| 8 | Fiziksel doğrulama protokolü | `VALIDATION_PROTOCOL.md` |
| 9 | Terminoloji (20 terim) | `terminology.json` |
| 10 | Taksonomi taslakları | `02_TAXONOMY/public/*.json` |
| 11 | **Kitap 1 Faz 1 spesifikasyonu (10 belge)** | `BOOK-01/00_SPEC/` |
| 12 | Kitap 2 ve Kitap 3 yol haritaları | `BOOK-0x/ROADMAP.md` |

**Definition of Done:**
1. Yukarıdaki 12 çıktı mevcut.
2. `qa_all.sh` sıfır hata.
3. **Kurucu Kitap 1 Faz 1'i ONAYLADI.**
4. `.gate` → `series-architecture`.

**Kurucu bağımlılığı:** **YÜKSEK — onay kapısı.**

**Risk:** Bu fazın en büyük riski, taksonominin dış otoriteye karşı
doğrulanmamış olmasının sessizce unutulmasıdır. Mekanik koruma:
`verification_status` alanları + `check_verification_evidence`.

---

### S2/S3/S4 — KİTAP YAŞAM DÖNGÜLERİ

Her kitap sekiz fazdan geçer. Ayrıntı: `BOOK-0x/ROADMAP.md`.

| Faz | Kapı | Özet |
|---|---|---|
| P0 | `foundation` | Kitap temeli: yapı, config, kayıt defterleri |
| P1 | `phase1-spec` | Araştırma + içerik spesifikasyonu (10 belge) |
| P2 | `phase2-visual` | Görsel sistem instantiasyonu + figür motoru |
| P3 | `phase3-pilot` | **KILL-GATE** — pilot bölüm + fark testi + fiziksel doğrulama |
| P4 | `phase4-production` | Tam içerik üretimi |
| P5 | `phase5-qa` | Teknik/editoryal/görsel/fiziksel KA |
| P6 | `phase6-format` | **FORMAT DOĞRULAMA KAPISI** + render + KDP |
| P7 | `release` | Lansman + katalog aktivasyonu |

---

### S5 — SERİ KA / KATALOG SİSTEMİ · `catalog` → `release`

**Amaç:** üç kitabın bir katalog gibi çalışmasını ölçmek.

| Görev | Neden |
|---|---|
| Bağlanma oranı ölçümü | Araştırma raporunun tüm seri ekonomisi `ESTIMATE`; ilk gerçek sayı burada üretilir |
| Çapraz satış doğrulaması | "Birlikte alınanlar" ilişkisi ancak ikinci ürünle kurulur |
| Reklam testi | Yazılı eşik: dönüşüm %5 altındaysa ücretli edinme İPTAL |
| Terminoloji/notasyon regresyonu | Üç kitapta tutarlılık — `qa_terminology.py` tam katalog üzerinde |
| Bir sonraki ürün önerisi | Kitap 1–3'ün GERÇEK verisiyle; tüm genişlemelere önceden taahhüt YOK |

## 4 · Paralelleşme kuralı

**Kitap 2 ve 3, Kitap 1'in YAYIMLANMASINA bağımlı DEĞİLDİR.** Yalnızca
Kitap 1'in kurduğu **ortak mimariye** bağımlıdır.

| Bağımlılık | Ne zaman karşılanır |
|---|---|
| Terminoloji, ölçü çerçevesi, görsel notasyon | Kitap 1 `phase2-visual` sonu |
| **Farklılaşma hipotezinin doğrulanması** | Kitap 1 `phase3-pilot` — **bu bir SERİ kapısıdır** |
| Düzeltme aile taksonomisi | S1 (bu turda taslak üretildi) |

**Sert kural:** Kitap 1'in P3 kill-gate'i FAIL verirse **Kitap 2 ve 3
başlamaz.** Farklılaşma hipotezi çürükse üç kitap da aynı hipoteze
dayanıyordu.

## 5 · Onay kapıları — özet

| Kapı | Kim | Ne olmadan geçilmez |
|---|---|---|
| S1 → S2 | **Kurucu** | Kitap 1 Faz 1 onayı |
| P1 → P2 (her kitap) | Kurucu | Kapsam + mimari onayı |
| P3 kill-gate | **Dış ölçüm** | 3 okurun fark testi + %0 diyagram hata oranı. **AI vekil SAYILMAZ.** |
| P6 format kapısı | Ölçüm | Gerçek KDP maliyet + Previewer testi + fiziksel prova |
| `catalog` | Ölçüm | ≥2 kitap yayında + ilk bağlanma verisi |

## 6 · Bu turda YAPILMAYAN

Manüskript prozası · nihai diyagram · kapak · KDP dosyası · reklam
kampanyası · Kitap 2 ve 3 üretimi · kaynak edinimi · marka taraması ·
spiral fizibilitesi. Bkz. `08_REPORTS/PHASE_1_SERIES_ARCHITECTURE.md § Sınırlamalar`.

---

*Vâliçe Press · TRUE FIT · Series Roadmap · 28 Ağustos 2026*
