# FAZ 3 — PİLOT PAKETİ VE KILL-GATE DURUMU

> Kitap 1 · kapı `phase3-pilot` · **AÇILMADI** · 28 Ağustos 2026
>
> # BU FAZ TAMAMLANMADI VE TAMAMLANAMAZ.
>
> Faz 3'ün iki kill-gate'i de **dış dünyada** ölçülür. Bu belge, o iki
> ölçümün yapılabilmesi için gereken **her şeyin hazır olduğunu**
> kaydeder ve ölçümlerin **YAPILMADIĞINI** aynı netlikte kaydeder.

---

## 0 · Kapı durumu

```
   P2 Görsel sistem ✓ TAMAM
    │
    ▼
   P3 Pilot + KILL-GATE
    │
    ├── İçeriden yapılabilen: ✓ TAMAM        ◄── BU TURDA YAPILDI
    │     · pilot kesit üretildi (8 sayfa, markasız, İngilizce)
    │     · fiziksel sınama kiti üretildi (19 VAL kaydı)
    │     · çelişmeli inceleme koşturuldu (11 bulgu)
    │
    └── DIŞARIDA ölçülmesi gereken: ✗ YAPILMADI
          ① fark testi — üç gerçek ev dikişçisi      D-01
          ② fiziksel doğrulama — 19 VAL kaydı        D-02
                       │
                       ▼
              ═══ HARD STOP ═══
   P4 Tam içerik üretimi — AÇILAMAZ
```

`06_BUILD/kill_gate.py --book book-01` → **2 engel · çıkış kodu 1.**
Bu **beklenen ve doğru** davranıştır.

## 1 · Malzeme A — pilot kesit · **ÜRETİLDİ**

| Ölçüt (`DIFFERENTIATION_TEST § 6.1`) | Gereken | **Üretilen** |
|---|---|---|
| Kaynak | Bölüm 11 (Göğüs) | ✓ `B1-CH11`, `bust_chest` |
| Belirti girişi | en az 3 | ✓ **3** (`SYM-016`, `SYM-017`, `SYM-020`) |
| Bölge anatomisi | var | ✓ işaret noktası figürü |
| Bu bölgede okunan ölçüler | var | ✓ üç ölçü + tablo + ölçüm figürü |
| Akış şeması | var | ✓ **belirti başına bir şema + eleme şeması** |
| "Neyi henüz değiştirmeyin" | var | ✓ giriş başına + bölge kapanışı |
| Uzunluk | **6–8 sayfa** | ✓ **8 sayfa** |
| Biçim | nihai sayfa geometrisi | ✓ `PG-B1-8.5x11` |
| **Markasız** | zorunlu | ✓ **mekanik olarak denetleniyor** |
| Görsel | Faz 2'nin **gerçek** figürleri | ✓ **7 figür, aynı motordan** |

**Dosya:** `BOOK-01/09_OUTPUT/PILOT_MATERIAL_A.pdf` (`.gitignore § ⑥`)
**Kaynak:** `BOOK-01/04_EDITORIAL/pilot/PILOT_MATERIAL_A.json` (`§ ①`)
**Üretici:** `06_BUILD/build_pilot.py`

**Markasızlık bir dilek değil bir denetimdir.** `check_unbranded` seri
adını, yayıncı adını ve kitap göndermelerini arar; bulursa **çıktı
üretilmez**. Uzunluk da denetlenir: 6–8 penceresi dışında **hata
verir**.

### 1.1 · Spec'ten iki sapma — kayıtlı

**Sapma 1 — "tam bölge akış şeması" yerine belirti başına şema.**
`§ 6.1` bölge düzeyinde tek bir şema istiyordu. Faz 2 ölçümü bölge
düzeyinde tek şemanın **hiçbir sayfaya sığmadığını** gösterdi
(`DECISIONS.md K41`): en küçük bölge bile 978 pt genişlik istiyor,
sayfada 504 pt var. Şemanın birimi belirti oldu. Malzeme A bu yüzden
üç belirti şeması + bir eleme şeması taşır.

**Sapma 2 — uzunluk iki kez düzeltildi.**
İlk sürüm beş belirti girişi ve 11 figürle **13 sayfa** çıktı;
`build_pilot.py`'nin uzunluk denetimi yakaladı. Kapsam spec
asgarisine indirildi (üç giriş) → 10 sayfa. Zorunlu sayfa sonları
kaldırıldı → **8 sayfa**. Çıkarılanlar: `SYM-018` girişi,
`sign_SYM-020`, `toile_slash_test`, `meas_M-001`.

## 2 · Malzeme B — rakip kesiti · **EDİNİLMEDİ**

| Alan | Durum |
|---|---|
| Konu | aynı bölge (göğüs) — kilitli |
| Uzunluk | A ile ±%20 → **6,4–9,6 sayfa** (A = 8) |
| Edinim | ✗ **YAPILMADI** — kitabın meşru bir nüshası gerekir |
| Kullanım | yalnızca test oturumunda; **çoğaltılmaz, depoya girmez** |

**Bu bir `D-01` alt bağımlılığıdır** ve çelişmeli inceleme `B-07`
olarak işaretledi: Malzeme B edinilemezse test **yapılamaz**.
Ajan bir kitabı satın alamaz veya kütüphaneden ödünç alamaz.

## 3 · Fark testi — `D-01` · **ÖLÇÜLMEDİ**

| | |
|---|---|
| Protokol | ✓ **TAMAMLANDI** (Faz 1) — eleme ölçütleri, ön eleme, beş kanal, teşvik, taraf tutma kuralları, oturum betiği, kayıt formu |
| Malzeme A | ✓ **HAZIR** |
| Malzeme B | ✗ edinilmedi |
| Katılımcı | ✗ **0 / 3** |
| Ölçüm | ✗ **YAPILMADI** — `measured: false` |
| AI vekil | ✗ `aiProxyCountsAsHuman: false` — **açılamaz** |
| Sonuç | **EXTERNAL VALIDATION REQUIRED** |

**1–2 katılımcı bulunursa:** sonuç **`INCONCLUSIVE`** — PASS değil,
FAIL değil. `measured` `false` kalır, kapı **kapalı kalır** (`K30`).

### 3.1 · Çelişmeli incelemeden gelen protokol eklentisi

`PHASE_3_ADVERSARIAL_REVIEW § 3` (`B-03`) eleme şemasının uzunluğunu
YÜKSEK bir risk olarak işaretledi ve iki çözüm önerdi. Hangisinin daha
iyi olduğu bir **okuma** sorusudur. **Öneri:** oturum betiğinin 4.
sorusundan ("Değiştirmek isteyeceğiniz bir şey var mı?") sonra, eleme
sayfasına özel bir gözlem notu tutulsun — katılımcı o sayfayı atladı
mı, okudu mu, geri döndü mü. **Soru sorulmaz**, yalnızca gözlenir;
yönlendirici bir soru testi kirletir.

## 4 · Fiziksel doğrulama — `D-02` · **ÖLÇÜLMEDİ**

| | |
|---|---|
| Kapsam | `A13` / `K29` — 2 toile + 3 yedek parça, tek vücut |
| Kayıt | **19** (`VAL-0001` – `VAL-0019`) |
| **Kit** | ✓ **ÜRETİLDİ** — `BOOK-01/09_OUTPUT/VALIDATION_KIT.md` |
| **Kayıt iskeleti** | ✓ **ÜRETİLDİ** — `08_REPORTS/tracked/VAL_RECORDS.json` |
| Yapılan sınama | **0 / 19** — hepsinin `performed` alanı `false` |
| Hata oranı | **HESAPLANAMAZ** — ölçüm yok |
| Sonuç | **EXTERNAL VALIDATION REQUIRED** |

**Dağılım:**

| Kayıt | Yöntem | Ne sınanıyor |
|---|---|---|
| `VAL-0001`–`0004` | `Y-1` belirti üretme | Bilinen bir sapma, kayıttaki belirtiyi ÜRETİYOR mu |
| `VAL-0005`–`0007` | `Y-2` ayırt edicilik | Ayırt edici kanıt iki nedeni AYIRIYOR mu |
| `VAL-0008`–`0016` | `Y-4` eleme kalemi | Karıştırıcı, kalıp sorunundan AYRILIYOR mu |
| `VAL-0017`–`0018` | `Y-5` sıra kısıtı | Yanlış sıra ikinci bir sorun ÜRETİYOR mu |
| `VAL-0019` | `Y-3` ölçüm tekrarı | Üç ölçümün yayılımı ⅛ inç'i aşıyor mu |

**Faz 2 bu kiti gerçek yaptı.** Sınanacak figürler artık "bir gün
çizilecek diyagramlar" değil, **elde duran PDF'lerdir**. Altı
`toile_state` figürü doğrudan sınama talimatıdır.

**Mekanik kilit — Faz 3'te eklendi.** `kill_gate.py` artık
`VAL_RECORDS.json`'ı okuyor: `physicalValidation.measured = true`
yazılmış ama kayıtlar boşsa **ayrı bir engel** raporlanır. Bir bayrak,
olmayan bir ölçümü var edemez.

## 5 · Çelişmeli inceleme · **YAPILDI**

`08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md` — **11 bulgu**, **ikisi
KRİTİK**, üçü YÜKSEK. **HARD_STOP bulgusu yok.**

| Bulgu | Durum |
|---|---|
| `B-10` figürler kullanılamıyordu (dil) | **KAPATILDI** — `K45` + yeni kapı |
| `B-11` `.gitignore` iki kaynak dosyayı yutuyordu | **KAPATILDI** — `K47` + regresyon |
| `B-01` "ilk evet kazanır" yanlış dal | Faz 4'e yazılı kısıt |
| `B-03` eleme şeması çok uzun | Faz 4 + `D-01` gözlem notu |
| `B-05` tek kroki, "her vücut" vaadi | Faz 4 kısıtı — üç oran varyantı |
| `B-08` sayfa bütçesi | **ÖLÇÜLDÜ** — bölge atlası ≈80–110 sayfa |

⚠ Bu **bir insan uzman incelemesi değildir** (`CLAIMS_STANDARD § 1`).

## 6 · Bu turda ÜRETİLMEYEN — ve neden

| Ne | Neden |
|---|---|
| Kalan 15 bölümün prozası | **Faz 4'tür ve kill-gate kapalıdır.** Kanıtlanmamış bir mimariyi 18 bölüme ölçeklemek, bu projenin kaçınmak için kurulduğu hatanın ta kendisidir |
| Kapak | `A16` marka temizliği kapanmadan kapak taslaklanmaz (`D-03`) |
| KDP iç dosyası | P6'dır ve P5'e, P5 P4'e, P4 bu kapıya bağlıdır |
| Reklam kampanyası | P7'dir; altı girdinin hiçbiri yok (`K28`) |
| Kitap 2 / Kitap 3 içeriği | Seri kapısı `production`'a ulaşmadı |

## 7 · Kurucunun yapması gerekenler — sırayla

1. **Malzeme B'yi edin** — kategori liderinin meşru bir nüshası;
   göğüs bölümü, 6,4–9,6 sayfa.
2. **`PILOT_MATERIAL_A.pdf`'i bas** — 8 sayfa, markasız.
3. **Üç katılımcı bul** — `DIFFERENTIATION_TEST § 5.2`'nin beş kanalı.
   *Hedef: 4 kabul, 3 katılım.*
4. **Oturumları yürüt** — betik `§ 5.5`, kayıt formu `§ 5.6`.
   **Betikteki yasak kelimeler söylenmez.**
5. **Sonucu kaydet** — `series_config.json →
   killGates.differentiationTest.measured` + `measuredDecision`.
6. **Fiziksel sınamayı yürüt** — `VALIDATION_KIT.md`, 19 kayıt.
7. **Sonuçları kaydet** — `08_REPORTS/tracked/VAL_RECORDS.json`.
8. `python3 06_BUILD/kill_gate.py --book book-01` → **0 engel** olmalı.

**Adım 5 ve 7 arasında bir sıra yoktur** — ikisi bağımsızdır ve ikisi
de PASS olmadan Faz 4 açılmaz.

---

*Vâliçe Press · BEFORE YOU CUT · Phase 3 Pilot Package · 28 Ağustos 2026*
