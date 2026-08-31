# ROADMAP PROGRESS — BEFORE YOU CUT

> Son ölçüm: **2026-08-29** · dal `master`
> · depo: `emredogan-cloud/sewing-pattern-fitting-series` (**public**,
> marka-nötr ad)
>
> Kaynak: [`SERIES_ROADMAP.md`](SERIES_ROADMAP.md) ve `BOOK-0x/ROADMAP.md`
>
> **Kural (`DECISIONS.md K33`): bu belgedeki her sayı, onu üreten
> komutun çıktısından alınır — hatırlanan bir değerden değil.**

---

## 0 · Tek cümlelik durum

> **Kitap 1 — INTERNAL RELEASE CANDIDATE.**
> 255 sayfa · 21 bölüm · 159 ayrı figür · 307 iddia · **249 kapı denetimi**.
>
> Kurucu dış doğrulamayı ERİŞİLEMEZ ilan etti (`K58`). Proje durmadı:
> fiziksel testin yerine içsel ikameler kuruldu ve **beş bağımsız
> çelişmeli inceleme** koşuldu (teknik · teşhis mantığı · okur yolu ·
> görsel anlam · tutarlılık). ≈103 bulgudan **30'u düzeltildi**,
> **4'ü ölçümle çürütüldü**, 73'ü kayda geçirildi.
> Bu turda **kendi iki çürütmemi geri aldım** — ikisinde de yanılmışım.
>
> Faz 5 girerken sekiz veri kapısı yeşildi, 152 kapı testi geçiyordu ve
> **ürün bozuktu**: dizilmiş sayfada harfler üst üste biniyordu, kitabın
> ilan ettiği tek giriş yolu (Ek C) 43 belirtinin 18'inde kapalı döngüye
> gönderiyordu, boş formlar 1,84 mm satırlarla yazılamazdı, ve CI kendi
> kapsamını sessizce %4 küçültüp yine "bütün kapılar geçti" diyordu.
> **24 kusur doğrulandı ve düzeltildi; 4 inceleme bulgusu çürütüldü.**
>
> `kill_gate.py` hâlâ **2 engel** raporluyor ve raporlamaya DEVAM EDİYOR.
> Kitap kapısı `phase4-production-conditional` olarak **KALDI** —
> kümülatif sırada `phase3-pilot`'ın ÖNÜNDEDİR ve `phase5-qa` bu yoldan
> **açılamaz**. Doğru durum: **QA COMPLETE / EXTERNAL VALIDATION PENDING.**

## Seri fazları

| Faz | Başlık | İlerleme | Kapı |
|---:|---|---|---|
| **S0** | Seri Bootstrap | `████████████████` tamamlandı | `bootstrap` ✓ |
| **S1** | Seri Mimarisi | `████████████████` **TAMAMLANDI** — kurucu onayı alındı, ortak mimari donduruldu | `series-architecture` ✓ **İLERLEDİ** |
| **S2** | Kitap 1 yaşam döngüsü | `████████████░░░░` P0 ✓ · P1 ✓ · P2 ✓ · **P4 ✓ KOŞULLU** · **P5 ✓ İÇSEL** · P3 **KILL-GATE'TE DURUYOR** | — |
| **S3** | Kitap 2 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı — seri kapısı `production` değil | `init` |
| **S4** | Kitap 3 yaşam döngüsü | `░░░░░░░░░░░░░░░░` başlamadı · yalnızca `A10` araştırma mimarisi | `init` |
| **S5** | Seri KA / Katalog | `░░░░░░░░░░░░░░░░` başlamadı — gerçek çok-kitap verisi yok | — |

## Kitap fazları

| Kitap | Kapı | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|
| **1 — Measure & Diagnose** | **`phase5-qa-internal`** | ✓ | ✓ | ✓ | **ERİŞİLEMEZ** | **✓ KOŞULLU** | **✓ İÇSEL** | — | — |
| **2 — The Adjustment Atlas** | `init` | roadmap var | — | — | — | — | — | — | — |
| **3 — Draft Your Own Sloper** | `init` | roadmap + `A10` araştırma mimarisi | — | — | — | — | — | — | — |

> **Bu turda HİÇBİR kapı ilerlemedi ve bu doğrudur.** Faz 5'in içsel
> işi bitti; `phase5-qa`'yı açacak olan kod değil, **ölçümdür**.
> `phase3-pilot` ilerlemedi ve ilerleyemez — iki dış ölçüm (`D-01`,
> `D-02`) hâlâ yapılmadı. Koşullu kapı bunu mekanik olarak korur.

## Kalite kapıları — son ölçüm

Komut: `bash 06_BUILD/qa_all.sh` · 2026-08-29

| Kapı | Komut | Sonuç |
|---|---|---|
| Şema · bütünlük · kaynak otoritesi | `validate_spec.py` | ✓ 0 hata (18 kaynak · 43 belirti · **20 aile** · 32 ölçü · 148 crosswalk · 12 blok · **163 figür**) |
| Depo · koruma · marka · izolasyon | `validate_structure.py` | ✓ 0 hata (**194 izlenen dosya** · altı denetim hattı) |
| Crosswalk tazeliği | `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| Crosswalk bütünlüğü | `qa_crosswalk.py` | ✓ 0 bulgu — **20/20** aileye ulaşılıyor |
| Kitap sınırı | `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| İddia disiplini | `qa_claims.py` | ✓ 0 bulgu (43 belge) |
| Terminoloji | `qa_terminology.py` | ✓ 0 bulgu (31 belge · 20 terim) |
| **Görsel sistem** | `qa_visual.py` | ✓ 0 bulgu — **on dört denetim** *(vücut varyantı eklendi)* |
| **İddia sicili tazeliği** *(yeni)* | `build_claims.py --check` | ✓ güncel (**307 iddia**) |
| **Manüskript** | `qa_manuscript.py` | ✓ **0 bulgu** — on dört denetim · 255 sayfa |
| **Tam kitap dizgisi** | `build_book.py` | ✓ **255 sayfa**, bütçe 220–260 içinde |
| **Yazı tipi bütünlüğü** *(yeni)* | `fetch_fonts.py --verify` | ✓ 10 dosya SHA-256 ile doğrulandı |
| **Kapıların kendi testi** | `selftest.py` | ✓ **220/220** *(Faz 4: 152)* + **29** çizim yasağı = **249** |
| Sentetik simülasyon *(yeni)* | `run_synthetic.py` | ✓ 16/16 profil · 129 neden çifti |
| Kill-gate durumu | `kill_gate.py --book book-01` | ⊗ **DIŞ DOĞRULAMA ERİŞİLEMEZ — PASS DEĞİL** |

## Görsel sistem — Faz 2 ÖLÇÜMLERİ

| Ölçüt | Faz 1 tahmini | **ÖLÇÜLEN** |
|---|---:|---:|
| Toplam figür | ~123 | **154** |
| Akış şeması | 9 | **46** |
| Deterministik üretilebilen | — | **105 · %68,2** |
| `manual_reason` taşıyan | — | **49** (43 belirti + 6 toile) |
| İç araç figürü (kitaba girmez) | — | **3** |
| Bir yayılıma sığmayan şema | — | **0** (bölme öncesi 11) |
| `photo_required` | — | **0** / eşik 6 |
| `color_required` | — | **%0,0** / eşik %10 |
| Satır başına karakter | — | **83,0** (hedef 72–88) |
| `TK-05` ↔ `TK-06` eğrilik oranı | — | **3,49** (eşik 2,0) |
| En ince çizgi, 300 dpi 1-bit | — | **2 px** — hayatta |

### Figür türlerine göre

| Tür | Sayı |
|---|---:|
| `flowchart` | 46 |
| `fit_sign_on_figure` | 43 |
| `measurement_path` | 29 |
| `table_graphic` | 9 |
| `pattern_piece` | 8 |
| `body_landmark` | 7 |
| `comparison_before_after` | 6 |
| `toile_state` | 6 |
| **Toplam** | **154** |

## Faz 5 — QA ÖLÇÜMLERİ

Tam rapor: [`08_REPORTS/PHASE_5_QA_REPORT.md`](08_REPORTS/PHASE_5_QA_REPORT.md)
· açık iddialar:
[`BOOK-01/08_REPORTS/PHASE_5_OPEN_CLAIMS.md`](BOOK-01-MEASURE-AND-DIAGNOSE/08_REPORTS/PHASE_5_OPEN_CLAIMS.md)

| Ölçüt | Faz 4 | **Faz 5** | Δ |
|---|---:|---:|---:|
| Sayfa | 252 | **255** | +3 |
| Bölüm | 21 | **21** | 0 |
| Kelime | 42 224 | **42 392** | +168 |
| Ayrı figür | 159 | **159** | 0 |
| Figür yerleşimi | 175 | **175** | 0 |
| İzlenen maddi iddia | 204/204 | **204/204** | 0 |
| İddia (toplam) | 307 | **307** | 0 |
| Crosswalk | 148 | **148** | 0 |
| **Kapı denetimi** | 152 | **249** | **+97** |

### Dizgi katmanı — ÖLÇÜLDÜ (yeni)

Yöntem: `pdftotext -bbox-layout` ile 255 sayfanın her kelimesinin kutusu;
dikdörtgen kesişimi + kenar boşluğu + folyo taraması. 300 dpi 1-bit
rasterleştirme.

| Ölçüt | Faz 5 girişi | **Faz 5 çıkışı** |
|---|---:|---:|
| Harf çakışması (üst üste basılan kelime) | **5** (s. 50, s. 72) | **0** |
| Metin bloğu dışına taşan kelime | **1** (s. 61, 17,4 pt) | **0** |
| Metni olup sayfa numarası olmayan sayfa | **2** (s. 46, s. 236) | **0** |
| Yanlış/yinelenen folyo | 0 | **0** |
| Ek C belirti işaretçisi doğruluğu | **25/43** | **43/43** |
| İçindekiler parça satırı doğruluğu | **0/6** | **6/6** |
| Yinelenen bölüm numarası | **1** (iki "CHAPTER 16") | **0** |
| Ek harf sırası | **A,B,D,E,F,G,C,H,I** | **A→I** |
| İçindekilerde listelenen ek | **0/9** | **9/9** |
| Boş form satır yüksekliği | **1,84 mm** | **9,1–9,2 mm** |
| Ölçü figürü metniyle aynı sayfada | **0/32** | **28/32** |
| Var olmayan nota gönderen figür | **3** | **0** |
| Şema ↔ metin neden sırası uyumu | **0/43** | **43/43** |
| Ortalama sayfa doluluğu | %79,6 | %78,1 |

### Bağımsız inceleme + okur yolculukları

Birincil üretimden AYRI iki hat koşuldu.

| | |
|---|---:|
| Bağımsız inceleme bulgusu | **33** |
| CI'de yakalanan (Faz 5'in kendi ürettiği) kusur | **1** — kapı katmanı render katmanına bağlanmıştı |
| …kabul edilip düzeltilen | **8** |
| …**ölçümle çürütülen** | **4** |
| …kabul edilip AÇIK bırakılan (içerik turu ister) | **6** |
| Okur yolculuğu | **3** — üçü de Ek C kusurunu buldu |

**Çürütülenler ölçümle çürütüldü**, tartışmayla değil: "ters teşhis"
iddiası iki AYRI belirtinin birleştirilmesiydi; "dört mü beş mi sıra
kuralı" iddiası kitabın *"Four settled + One contested"* yapısını
gözden kaçırmıştı.

### Faz 5'te AÇIK BIRAKILAN — Faz 6 öncesi içerik turu

| # | Risk | Bulgu |
|---|---|---|
| `A-01` | `R-25` | Karın nedeni göğüs ailesine yönleniyor (`SYM-018.C1`, `SYM-040.C1`) |
| `A-02` | `R-26` | 129 `Confirm by` satırının 46'sı kitabın öğretmediği bir ölçüye başvuruyor |
| `A-03` | — | İşlenmiş örnekte "3 cm" kenar başına mı toplam mı belirsiz |
| `A-04` | — | İki figür alanı inç, kitap metrik |
| `A-05` | `R-27` | Belirti figüründe teşhis işareti (0,6 pt) gövdeden (1,2 pt) HAFİF |
| `A-06` | — | Bölüm 8 ile Ek D'nin "on dört ögesi" aynı on dört değil |

---

## Faz 4 — MANÜSKRİPT ÖLÇÜMLERİ

Komut: `python3 06_BUILD/build_book.py` · ölçüm dosyası
`BOOK-01/02_CONTENT/public/manuscript_index.public.json`

| Ölçüt | Spec hedefi | **ÖLÇÜLEN** |
|---|---:|---:|
| Toplam sayfa | 220–260 | **252** ✓ |
| Bölüm (parça + bölüm + ek) | 21 | **21** ✓ |
| Kelime | — | **42 224** |
| Ayrı figür kullanımı | — | **159 / 159** yerleştirilebilir figürün tamamı |
| Figür yerleşimi | — | **175** (17 figür birden çok yerde) |
| Bölge atlası | ≤100 *(B-08)* | **177** — kısıt AŞILDI, aşağıya bakınız |
| Boş sayfa (bölüm açılışı verso) | — | **13**, hiçbiri numara taşımıyor |
| Kalibre edilmemiş kesinlik | 0 | **0** |
| Okur metnine sızan iç kimlik | 0 | **0** |
| Kitaba giren iç araç figürü | 0 | **0** |

### Bölüm bazında

| Bölüm | Sayfa | Figür | Kelime |
|---|---:|---:|---:|
| Parça 0 · Nasıl kullanılır | 2 | 0 | 621 |
| 1 · Kalıp neden oturmaz | 4 | 2 | 698 |
| **2 · Vücudunuzu ölçmek** *(üretilen)* | **38** | **40** | 2 702 |
| 3 · Kalıbı okumak | 7 | 6 | 1 166 |
| 4 · Teşhis toile'i | 6 | 3 | 1 091 |
| 5 · Prova oturumu | 5 | 1 | 878 |
| 6 · Yedi adımlı döngü | 10 | 3 | 1 861 |
| 7 · Belirtileri adlandırmak | 8 | 11 | 1 011 |
| 8 · Sahte nedenleri elemek | 5 | 3 | 709 |
| **9–15 + 16 atlas · Bölge atlası** *(üretilen)* | **177** | **94** | 20 000+ |
| 16 · Düzeltme sırası | 6 | 3 | 1 019 |
| 17 · Uyum profili | 3 | 1 | 529 |
| 18 · Profili taşımak | 3 | 0 | 634 |
| Ekler A–H | 5 | 8 | 465 |

### `B-08` sayfa bütçesi kısıtı — AŞILDI, gerekçe yazıldı

Çelişmeli inceleme `B-08` şunu yazmıştı: *"Bölge atlası 100 sayfayı
aşarsa kapsam daraltılır."* Atlas **176 sayfa** çıktı.

**Ne yapıldı:** önce kapsam daraltıldı. Tekrarlanan metin ölçülerek
kesildi — 43 girişte tekrar eden dört blok (eleme gerekçesi, figür
başlığı uyarısı, devir cümlesi kalıbı, yeniden gözlem başlığı)
kaldırıldığında atlas **127 → 115 sayfa**ya indi. Bu, `B-09`'un
(işlevsel tekrar) ölçülmüş maliyetidir: **12 sayfa.**

**Sonra kapsam BÜYÜDÜ ve bu bilinçliydi.** Aynı çelişmeli incelemenin
diğer bulguları Faz 4'e yazılı kısıt olarak geliyordu ve hepsi yer
tutuyor: `B-01` yeniden gözlem adımı (43 giriş × 2 paragraf),
`B-03` belirtiye özgü eleme (43 × 3 satır), Faz 4 bağımsız incelemesinin
`CC-25` bulgusu (kapı-önce sunum) ve **28 kanıt çakışması beyanı**
(`K52`). Ayrıca ilk tam dizgide **29 ölçüm figürünün hiçbirinin kitapta
olmadığı** ölçüldü ve eklendi (+25 sayfa).

**Karar:** `B-08`'in 100 sayfalık rakamı, bu eklerin ZORUNLU olduğu
bilinmeden yapılmış **doğrusal bir tahmindi**. Gerçek kısıt, onun
koruduğu şeydir: **300 sayfada cilt payı değişir ve sayfa geometrisi
yeniden hesaplanır.** 252 sayfa o bandın rahatça içindedir ve
`qa_visual § ⑨` ile `build_book` bunu her koşumda denetler.

## Faz 4 — BAĞIMSIZ TEKNİK İNCELEME

Dört ayrı inceleme hattı, birincil üretimden AYRI çalıştırıldı.

| | |
|---|---:|
| Bulgu | **149** |
| Danışılan kaynak (tekilleştirilmiş) | **68** |
| `CONTRADICTED` | **56** |
| `CONTESTED` | 14 |
| `UNSUPPORTED` | 10 |
| `SUPPORTED_NARROWER` | 40 |
| `SUPPORTED` | 29 |
| **Revizyon gerektiren** | **132 / 149** |
| Ayırt edici kanıt çakışması | **28** (43 belirtinin 28'inde) |

**Revizyon gerektirmeyen tek iddia: `CC-02` — "belirti ≠ neden".**
Kitabın tezi ayakta kaldı; ayrıntılarının çoğu kalmadı.

**Uygulanan başlıca düzeltmeler:**

| Ne | Neydi | Ne oldu |
|---|---|---|
| `CC-21` yeniden gözlem | "azaldı ama gitmedi = ikinci neden var" | **Mantık hatasıydı.** Önce YETERSİZ DÜZELTME, sonra ikinci neden. 43 girişin tamamında yapısal düzeltme |
| `AF-20` karın hacmi | **aile YOKTU**; beş crosswalk kaydı okuru göğüs pensi ya da giysinin arkası ailesine yolluyordu | Aile eklendi, beş yol düzeltildi |
| `M-015` ön orta boy | iki ayrı ölçü birleştirilmişti; kaynağın kendi yöntemi "hata" diye listelenmişti | Ayrıldı — `M-032` denge sayısı artık göğüs çıkıntısı taşımıyor |
| `T-10` / `M-001` üst göğüs | "kolların ÜSTÜNDEN" | **Kolların ALTINDAN.** Yanlış hâli beden seçimini yanlış dala gönderiyordu |
| `CC-10` beden kuralı | düz "2 inç" eşiği | Kalıbın KENDİ beyan ettiği fark; tam 2 inçte doğru bedendeki okuru gereksiz düzeltmeye yolluyordu |
| `CC-20` geri alınamazlık | "kesme" | 129 testin **17'si ilk adımda kesiyordu**, üçü kitabın kendi yasakladığı yakayı. Toile kesilir, KALIP ve KENAR kesilmez |
| `interacts_with` | 6 kenar tek yönlü | Simetrik + kapı + regresyon |
| `S-0004` atfı | 43 belirtinin tamamında kaynaktı | Tam metin okundu: iki çekirdek kuralı **içermiyor**. Atıf kaldırıldı, iddialar kaynaksız olduklarını beyan ediyor |
| Karıştırıcı sayısı | 9 (üç belgede) / 11 (veride) | **14** — dört sınıf eklendi, ikisinin kapsamı genişletildi |

Tam rapor:
[`08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md`](08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md)
· ham çıktı `08_REPORTS/tracked/phase4_review/`

## İçerik envanteri

| Varlık | Sayı | Doğrulama durumu |
|---|---|---|
| Uyum belirtisi (`SYM-xxx`) | 43 | **0 doğrulandı · 43 kaynağa bağlı ama YÜKSELTİLMEDİ** — bilinçli |
| Aday neden | 129 | **0 doğrulandı** — `C-C` sınıfı, birincil doğrulama FİZİKSEL |
| Düzeltme ailesi (`AF-xx`) | **20** *(`AF-20` karın Faz 4'te eklendi)* | 13 doğrulandı · 4 kısmi · 3 kaynaksız |
| Ölçü (`M-xxx`) | 32 | **16 doğrulandı** · 7 kısmi · 9 kaynaksız |
| Blok bileşeni (`BLK-xx`) | 12 | 0 — kamu kaynağı **çizim** anlatmıyor (`A10`) |
| Crosswalk (`XW-xxx`) | 148 | iç bütünlük denetlendi · dış doğrulama yok |
| Terim (`T-xx`) | 20 | taslak · `T-05` ve `T-10` Faz 4'te DÜZELTİLDİ |
| **İddia (`CLM-xxxx`)** | **307** | 56 `VERIFIED` · 8 `CONTESTED` · 214 `INFERRED` · 29 `UNVERIFIED` |
| **Kanıt çakışması** | **28** | okura BEYAN ediliyor; çözümü `D-02`'dedir |
| **Manüskript** | **252 sayfa · 21 bölüm · 42 224 kelime** | proza izlenmiyor (`K9`); ÖLÇÜM izleniyor |
| Görsel token (`TK-xx`) | 18 | **`CALIBRATED_DIGITAL_RENDER`** |
| **Figür (`FIG-B1-xxx`)** | **161** *(+7 manüskript figürü)* | **112 `drafted` · 49 `specified` · 0 `physically_validated`** |
| **Okur etiketi (İngilizce)** | **43 belirti · 129 neden** | sunum katmanı — doğrulama durumunu **değiştirmez** |
| **Kaynak kaydı (`S-xxxx`)** | **18** | 6 teknik otorite + tam metin · 2 taranmış · **8 platform/lisans** · 2 edinilmemiş |
| **Fiziksel sınama (`VAL-xxxx`)** | **19 kayıt üretildi · 0 YAPILDI** | kit hazır: `BOOK-01/09_OUTPUT/VALIDATION_KIT.md` |
| **Pilot kesit** | **1 · 8 sayfa · 7 figür** | markasız · İngilizce · nihai sayfa geometrisinde |

**Faz 2 için satın alınan ücretli kaynak: 0.**
Yazı tipi maliyeti: **$0** (üç aile de SIL OFL 1.1).

## KILL-GATE durumu — Kitap 1 Faz 3

| | Fark testi (`D-01`) | Fiziksel doğrulama (`D-02`) |
|---|---|---|
| Protokol | ✓ TAMAM | ✓ TAMAM |
| **Malzeme** | ✓ **Malzeme A üretildi (8 sayfa)** · ✗ Malzeme B edinilmedi | ✓ **19 kayıtlık kit üretildi** |
| Katılımcı / uygulama | ✗ **0 / 3** | ✗ **0 / 19** |
| Ölçüm | ✗ `measured: false` | ✗ `measured: false` |
| AI vekil | ✗ `false` — **açılamaz** | — |
| Sonuç | **EXTERNAL VALIDATION REQUIRED** | **EXTERNAL VALIDATION REQUIRED** |

**`kill_gate.py` mekanik kilidi Faz 3'te güçlendirildi:**
`physicalValidation.measured = true` yazılmış ama `VAL_RECORDS.json`
kayıtları boşsa **ayrı bir engel** raporlanır. Bir bayrak, olmayan bir
ölçümü var edemez.

## Dış doğrulama durumu

Tam kayıt: [`EXTERNAL_DEPENDENCIES.md`](EXTERNAL_DEPENDENCIES.md)

| # | Bekleyen | Kim | Engelleyici mi |
|---|---|---|---|
| `D-01` | Fark testi — 3 ev dikişçisi | Kurucu | **EVET — HARD STOP** |
| `D-02` | Fiziksel doğrulama — 19 `VAL` | Kurucu | **EVET — HARD STOP** |
| `D-03` | `BEFORE YOU CUT` marka temizliği | Kurucu + vekil | EVET (yayın öncesi) |
| `D-04` | Rakip akış takibi (90 gün) | Kurucu | hayır |
| `D-05` | `T3` — üç insan okuyucu | Kurucu | hayır |
| `D-06` | KDP Previewer + prova baskı | Kurucu | EVET (P6) |
| `D-07` | Ücretsiz kaynak edinimi | Kurucu/ajan | hayır |
| `D-08` | Kitap 3 çizim sistemi kaynakları | Kurucu | EVET (Kitap 3) |
| `D-09` | Kitap 2 spiral fizibilitesi | Kurucu | hayır |

## Git / CI durumu

| | |
|---|---|
| Depo | `github.com/emredogan-cloud/sewing-pattern-fitting-series` (**public**) |
| Depo adı | **marka-nötr** (`K32`) — `BEFORE YOU CUT` de kamuya taahhüt edilmedi |
| Dal | `master` |
| İzlenen dosya | **139** |
| CI işi | **10** — `gates` · `spec` · `structure` · `crosswalk` · `boundary` · `claims` · **`visual`** *(yeni)* · `selftest` · **`render`** *(yeni)* · `killgate` (tasarım gereği başarısız) |

**Bilerek yayımlanMAYAN:** pilot prozası ve derlenmiş pilot PDF'i ·
fiziksel sınama fotoğrafları · fark testi katılımcı verisi · telif
korumalı referans malzeme · indirilmiş kaynak PDF'leri · **yazı tipi
ikili dosyaları** (manifestle yeniden edinilir) · üretilmiş 163 figür
PDF'i · sırlar ve yerel önbellek.

## Açık kararlar

**13 kapandı · 1 ertelendi · 2 dış beklemede.**
Tam liste: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

`A15` (seri adı) **kapandı** — `BEFORE YOU CUT` (`K36`).
`A16` (profesyonel marka temizliği) **açıldı** ve dış beklemededir.

## Alınmış kararlar

**48 karar kayıtlı (`K1`–`K48`).** Bu turda **13 yeni kayıt**
(`K36`–`K48`).

Dördü, Faz 1 tahminlerinin **ölçümle yanlışlanmasıdır**: `K38` (yedek
yazı tipi), `K39` (sayfa ölçüsü), `K40` (token kalibrasyonu),
`K41` (akış şeması sayısı).
**Üçü, kapılar yeşilken ürünün kullanılamaz olmasıdır**: `K45` (figür
dili), `K46` (iç kimlik + etiket çakışması) ve `K47` (`.gitignore` iki
kaynak dosyayı yutuyordu — temiz bir klonda görsel sistem
çalışmazdı). `RISK_REGISTER R-19`.

## Riskler

**21 risk** — 4'ü YÜKSEK (`R-01` ortam, `R-02` talep tavanı,
`R-03` farklılaşma, `R-04` teknik doğruluk). Bu turda **üç yeni risk**
(`R-19` kapılar yeşilken ürün bozuk · `R-20` sayfa bütçesi ·
`R-21` tek kroki) ve **üç yeniden değerlendirme** (`R-05`, `R-06`,
`R-12`). **Hiçbir risk silinmedi.**
Tam liste: [`RISK_REGISTER.md`](RISK_REGISTER.md).

---

*Vâliçe Press · BEFORE YOU CUT · Roadmap Progress · 28 Ağustos 2026 (Faz 2 + Faz 3 hazırlığı)*


---

# İÇERİK TURU — 31 Ağustos 2026

**Durum: TAMAMLANMADI. Faz 6 AÇILMADI.** (`K59`)

| Ne | Sonuç |
|---|---|
| **L-2** — 46 doğrulama adımı | **KAPANDI**. 33 kalıp okuması + 4 prova okuması öğretildi, 1 ölçü eklendi (`M-034`), 63 adım metni değişti, `qa_verification.py` kapısı dayatıyor. |
| **L-3** — `VERIFIED` iddialar | **KAPANDI**. 8 kaynağın 7'si açıldı, **ikisi ilk kez okundu**. 16 sapma düzeltildi. `VERIFIED` 56 → 44; `VERIFIED_NARROWER` (yeni) 7. |
| **§ 23 bağımsız inceleme** | Üç ayrı geçiş · **80 bulgu · 72 kabul · 48 düzeltildi · 24 AÇIK**. |
| **§ 22 okur yolculukları** | **A geçti** (miktar güvenilmez) · **B kapalı döngüye girdi** · **C miktar sütunu boş bitti**. |
| **§ 25 çıkış ölçütleri** | 12 maddenin **9'u** karşılandı. **6, 11, 12 karşılanmadı.** |

Sayfa 255 → **273** (`K60`). Figür 163 → **170**. İddia 307 → **309**.

**Bir sonraki tur:** `CONTENT_PASS_REPORT.md` § 6'daki 24 kusur.

---

*Vâliçe Press · BEFORE YOU CUT · Roadmap Progress · 31 Ağustos 2026 (içerik turu)*
