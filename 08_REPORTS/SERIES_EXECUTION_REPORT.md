# BEFORE YOU CUT — YÜRÜTME RAPORU

> 28 Ağustos 2026 · uçtan uca yürütme turu
> · seri kapısı `series-architecture` · Kitap 1 kapısı `phase2-visual`
>
> **Bu rapordaki her sayı, onu üreten komutun çıktısındandır (`K33`).**
> Yapılmamış hiçbir dış ölçüm yapılmış gibi kaydedilmemiştir.

---

## 1 · Uygulanan kararlar

| Konu | Karar | Kayıt |
|---|---|---|
| Seri adı | **`BEFORE YOU CUT`** — kurucu onayı | `K36` |
| `TRUE FIT` | Yayımlanan ad olarak **reddedildi**; tarihsel kayıt korundu | `K18` · `K36` |
| Dizin adları | **Değiştirilmedi** — yol dizesi kimlik beyanı değildir | `K37` |
| Yazı tipi yedeği | Atkinson Hyperlegible **elendi** → **IBM Plex Sans** | `K38` |
| Sayfa geometrisi | Asimetrik iki sütun — 83,0 karakter/satır | `K39` |
| Token kalibrasyonu | `CALIBRATED_DIGITAL_RENDER` | `K40` |
| Akış şeması mimarisi | Birim **bölge değil belirti** — 46 şema | `K41` |
| Figür token'ları | **Beyan değil ölçüm**; yasaklar çalıştırılabilir | `K42` |
| Kroki | Çizim konvansiyonu, antropometrik iddia **değil** | `K43` |
| Faz kapıları | P2 ✓ · **P3 kill-gate'i AÇILMADI** | `K44` |
| Figür dili | Okurun dilinde — etiket katmanı + yeni kapı | `K45` |
| Okura dönük figür | İç kimlik basılmaz · etiket çakışamaz | `K46` |
| `.gitignore` sır deseni | Daraltıldı — iki kaynak dosyayı yutuyordu | `K47` |

Toplam **47 karar** (`K1`–`K47`); bu turda **12 yeni**.

## 2 · Marka durumu

| | |
|---|---|
| Kamuya dönük ad | **`BEFORE YOU CUT`** |
| `brandClearanceStatus` | **`founder-approved-working-name`** |
| Ne DEMEK | Kurucu adı onayladı ve seri bu adla ilerliyor |
| Ne DEMEK DEĞİL | **Hukuki temizlik yapıldı** — yapılmadı |
| Neden yapılmadı | Marka temizliği bir hukuki hizmettir; federal sicilin arama arayüzü otomatik sorguya kapalıydı |
| Ne zaman gerekir | **Kapak ve metadata üretiminden ÖNCE** |
| Kayıt | `OPEN_QUESTIONS A16` · `EXTERNAL_DEPENDENCIES D-03` |
| Mekanik koruma | `check_public_name_is_declared` `"professionally-cleared"` değerini **kanıtsız** almaz · `check_retired_name_leak` `TRUE FIT`'i kamuya dönük yüzeyde **yakalar** |

## 3 · Kaynak durumu

| | |
|---|---|
| Kayıt | **18** (`S-0001`–`S-0018`) — bu turda **3 yeni** |
| Teknik otorite + tam metin | **6** — değişmedi |
| Yeni kayıtlar | `S-0016` KDP baskı gereksinimleri · `S-0017` Adobe Source yazı tipleri (OFL) · `S-0018` yedek yazı tipi adayları |
| **Bu turda satın alınan ücretli kaynak** | **0** |
| Yazı tipi maliyeti | **$0** — üç aile de SIL OFL 1.1 |
| Kuyrukta bekleyen | 4 kalem, hiçbiri Kitap 1 için gerekli değil |

**Üç yeni kaynağın üçü de `technical_authority: false`'tur** ve öyle
olmak zorundadır: platform dokümantasyonu ve yazı tipi künyesi teknik
otorite **değildir** (`SOURCING_STANDARD § 1`).

## 4 · Kitap 1 · Faz 2 durumu — **TAMAM**

DoD'nin **11 maddesinin 10'u** karşılandı; sekizinci (`G7` rakip
takibi) bir dış gözlemdir — araç hazır, gözlem yapılmadı.

| Ölçüt | Faz 1 tahmini | **ÖLÇÜLEN** |
|---|---:|---:|
| Toplam figür | ~123 | **154** |
| Akış şeması | 9 | **46** |
| Deterministik oran | — | **%68,2** |
| `photo_required` | — | **0** / eşik 6 |
| `color_required` | — | **%0,0** / eşik %10 |
| `TK-05` ↔ `TK-06` | — | **AYRIK**, eğrilik oranı 3,49 |
| Satır ölçüsü | — | **83,0** karakter |

Tam rapor: [`PHASE_2_EXECUTION_REPORT.md`](PHASE_2_EXECUTION_REPORT.md)

## 5 · Kitap 1 · Faz 3 durumu — **KILL-GATE'TE DURDU**

| Parça | Durum |
|---|---|
| Pilot kesit (Malzeme A) | ✓ **8 sayfa · 7 gerçek figür · markasız · İngilizce** |
| Rakip kesiti (Malzeme B) | ✗ **edinilmedi** — kurucu |
| Fark testi | ✗ **0/3 katılımcı · `measured: false`** |
| Fiziksel sınama kiti | ✓ **19 `VAL` kaydı üretildi** |
| Fiziksel sınama | ✗ **0/19 yapıldı · `measured: false`** |
| Çelişmeli inceleme | ✓ **11 bulgu · HARD_STOP yok** |

`kill_gate.py --book book-01` → **2 engel · çıkış kodu 1.**

Tam rapor: [`PHASE_3_PILOT_PACKAGE.md`](PHASE_3_PILOT_PACKAGE.md)

## 6 · Kitap 1 · Faz 4 (tam içerik üretimi) — **AÇILAMADI**

**NOT STARTED — BLOCKED.**

`BOOK-01/ROADMAP.md § P4` bağımlılığı: **P3 PASS.** P3 ölçülmedi.

Kanıtlanmamış bir mimariyi 18 bölüme ölçeklemek, bu projenin kaçınmak
için kurulduğu hatanın ta kendisidir. Faz 4 için **yazılı kısıtlar**
hazırlandı (çelişmeli incelemeden): yeniden gözlem döngüsü (`B-01`),
belirtiye özgü eleme (`B-03`), üç kroki varyantı (`B-05`), bölge atlası
sayfa tavanı (`B-08`), üretilen sayfaların **gözle** örneklenmesi
(`R-19`).

## 7 · Kitap 1 · Faz 5 (KA) — **NOT STARTED**

P4'e bağlıdır. Ancak KA **altyapısı** bu turda genişledi: `qa_visual.py`
(on denetim), `fetch_fonts.py --verify`, selftest **91 → 138**.

## 8 · Kitap 1 · Faz 6 (format + KDP) — **NOT STARTED · dış engelli**

P5'e bağlıdır **ve ayrıca `D-06`**: KDP Previewer, gerçek maliyet
hesaplayıcısı ve fiziksel prova baskı bu depodan yapılamaz.

**Bu turda P6 için hazırlanan:** sayfa geometrisi KDP'nin
**yayımlanmış asgarilerine** göre kuruldu (`S-0016`) ve `qa_visual § ⑨`
her koşuda denetliyor. **Ölçülmeyen:** mürekkep yayılması. Token durumu
bu yüzden `CALIBRATED_DIGITAL_RENDER`'dır, düz `CALIBRATED` değil.

## 9 · Kitap 1 · Faz 7 (lansman) — **NOT STARTED · dış engelli**

P6'ya **ve `D-03`'e** (marka temizliği) bağlıdır. Reklam bütçesi
`K28`'in altı girdisi olmadan kararlaştırılamaz; hiçbiri yok.

## 10 · Kitap 2 durumu — **`init`**

Seri kapısı `production` değil. Kitap 2 mimarisi (`PROBLEM → VISIBLE
SIGN → … → COMMON MISTAKES`) ve 19 düzeltme ailesi hazır; `qa_boundary`
Kitap 1'in bir düzeltme kılavuzuna dönüşmesini **engelliyor**.

Kendi `phase1-spec`'i ayrıca `D-09`'a bağlıdır (spiral cilt fizibilitesi
— KDP spiral **sunmuyor**, `K22`).

## 11 · Kitap 3 durumu — **`init`**

`A10` (çizim sistemi) **DEFERRED** ve `D-08`'e bağlıdır: bu depoda
hiçbir kalıp çizim referansı yoktur ve 12 blok bileşeninin hiçbiri
kaynağa bağlı değildir. Kanıt kapısı yazılı; sistem **seçilemez**.

## 12 · Dış bağımlılıklar

Dokuz kalem: [`../EXTERNAL_DEPENDENCIES.md`](../EXTERNAL_DEPENDENCIES.md)

**Kitap 1'i şu anda durduran ikisi:** `D-01` (fark testi) ve
`D-02` (fiziksel doğrulama).

## 13 · KA sonuçları

`bash 06_BUILD/qa_all.sh` → **BÜTÜN KAPILAR GEÇTİ**

| Kapı | Sonuç |
|---|---|
| `validate_spec.py` | ✓ 0 hata · 18 kaynak · 154 figür |
| `validate_structure.py` | ✓ 0 hata · 139 izlenen dosya · altı hat |
| `build_crosswalk.py --check` | ✓ güncel (148) |
| `qa_crosswalk.py` | ✓ 0 bulgu · 19/19 aile |
| `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| `qa_claims.py` | ✓ 0 bulgu (40 belge) |
| `qa_terminology.py` | ✓ 0 bulgu |
| **`qa_visual.py`** | ✓ **0 bulgu · on denetim** |
| **`fetch_fonts.py --verify`** | ✓ 10 dosya SHA-256 |
| **`selftest.py`** | ✓ **138/138** |
| `kill_gate.py` | ✗ **2 engel — DOĞRU** |

## 14 · Git / CI durumu

| | |
|---|---|
| Depo | `emredogan-cloud/sewing-pattern-fitting-series` — **public** |
| Dal | `master` |
| CI işleri | **9** — `visual` bu turda eklendi |
| `killgate` işi | Tasarım gereği başarısız (`continue-on-error`) |

## 15 · Riskler

**21 risk.** Bu turda **3 yeni** (`R-19` kapılar yeşilken ürün bozuk ·
`R-20` sayfa bütçesi · `R-21` tek kroki) ve **3 yeniden değerlendirme**
(`R-05`, `R-06`, `R-12`). Hiçbiri silinmedi.

**En önemli yeni risk `R-19`'dur** ve bu turda **üç kez gerçekleşti:**
bütün kapılar yeşilken üretilen figürlerin hiçbiri kullanılamıyordu;
dördüncü kez, temiz bir klonda görsel sistem hiç çalışmayacaktı
(`K47`). Kapılar sormadıkları soruyu yakalayamaz.

## 16 · Kalan engeller

| Engel | Tür | Neyi durduruyor |
|---|---|---|
| `D-01` fark testi | **DIŞ · HARD STOP** | Faz 4 ve sonrası |
| `D-02` fiziksel doğrulama | **DIŞ · HARD STOP** | Faz 4 ve sonrası |
| `D-03` marka temizliği | DIŞ | Kapak + metadata (Faz 7) |
| `D-06` KDP Previewer + prova | DIŞ | Faz 6 |
| `D-08` çizim sistemi kaynakları | DIŞ | Kitap 3 `phase1-spec` |

**İç engel yoktur.** Yapılabilecek her iç iş yapıldı.

## 17 · TAM OLARAK BİR SONRAKİ EYLEM

> ### Kurucu, Malzeme B'yi edinir ve üç katılımcı bulur.
>
> `BOOK-01/09_OUTPUT/PILOT_MATERIAL_A.pdf` **hazır ve basılabilir.**
> `DIFFERENTIATION_TEST § 5.2`'nin beş kanalı yazılı. Hedef: **4 kabul,
> 3 katılım.**
>
> Paralel olarak `BOOK-01/09_OUTPUT/VALIDATION_KIT.md` uygulanabilir —
> ikisi arasında bir sıra yoktur.
>
> İki ölçüm de PASS olmadan `kill_gate.py` **0 engel** vermez ve
> **Faz 4 açılmaz.**

---

*Vâliçe Press · BEFORE YOU CUT · Execution Report · 28 Ağustos 2026*
