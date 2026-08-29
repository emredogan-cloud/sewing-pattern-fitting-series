# BOOK 1 — PHASE 5 — FULL QA REPORT

> Ölçüm tarihi: **2026-08-29** · dal `faz/4-production`
> Kitap kapısı: **`phase4-production-conditional`** (İLERLEMEDİ — § 20)
>
> **Kural (`DECISIONS.md K33`): bu belgedeki her sayı, onu üreten komutun
> çıktısından alınır.** Hatırlanan hiçbir değer yoktur.

---

## 1 · Faz Özeti

Faz 5 bir **kalite güvence** fazıydı, içerik genişletme fazı değil.

Başlangıç durumu: sekiz veri kapısı yeşil, 152 kapı testi geçiyor,
`qa_all.sh` çıkış kodu 0. **Ve ürün bozuktu.**

Faz 5'in bulduğu kusurların **hiçbirini** mevcut kapılar göremezdi —
çünkü hepsi kapıların BAKMADIĞI katmanlarda yaşıyordu: dizgi çıktısı,
sayfa geometrisi, navigasyon işaretçileri, ve metnin kendi verisiyle
tutarlılığı.

| | |
|---|---:|
| Doğrulanmış kusur | **24** |
| Düzeltilmiş kusur | **24** |
| Çürütülen inceleme bulgusu | **4** |
| Yeni regresyon kapısı | **37 denetim** (152 → 189) |
| Sayfa | 252 → **255** |
| Taksonomi değişikliği | **0 kayıt eklendi/silindi** |
| İddia kanıt düzeyi değişikliği | **0** |

**Yöntem:** 255 sayfanın her kelimesinin kutusu `pdftotext -bbox-layout`
ile çıkarıldı; dikdörtgen kesişimi, kenar boşluğu ve folyo taraması
yapıldı. Sayfalar 300 dpi'de rasterleştirilip 1-bit'e indirgendi. Her
iddia komut çıktısıdır.

---

## 2 · Otomatik QA

Komut: `bash 06_BUILD/qa_all.sh` → **çıkış kodu 0**

| Kapı | Komut | Sonuç |
|---|---|---|
| Şema · bütünlük · kaynak otoritesi | `validate_spec.py` | ✓ 0 hata (18 kaynak · 43 belirti · 20 aile · 32 ölçü · 148 crosswalk · 12 blok · 163 figür) |
| Depo · koruma · marka · izolasyon | `validate_structure.py` | ✓ 0 hata (194 izlenen dosya) |
| Crosswalk tazeliği | `build_crosswalk.py --check` | ✓ güncel (148 kayıt) |
| Crosswalk bütünlüğü | `qa_crosswalk.py` | ✓ 0 bulgu · 20/20 aileye ulaşılıyor |
| Kitap sınırı | `qa_boundary.py` | ✓ 0 bulgu (35 topik) |
| İddia disiplini | `qa_claims.py` | ✓ 0 bulgu (43 belge) |
| Terminoloji | `qa_terminology.py` | ✓ 0 bulgu (31 belge · 20 terim) |
| Görsel sistem | `qa_visual.py` | ✓ 0 bulgu (on dört denetim) |
| İddia sicili tazeliği | `build_claims.py --check` | ✓ güncel (307 iddia) |
| İddia→kaynak haritası | `build_claim_map.py --check` | ✓ güncel |
| Manüskript | `qa_manuscript.py` | ✓ 0 bulgu (on dört denetim) · 21 bölüm · 255 sayfa |
| Yazı tipi bütünlüğü | `fetch_fonts.py --verify` | ✓ 10 dosya SHA-256 ile doğrulandı |
| **Kapıların kendi testi** | `selftest.py` | ✓ **189/189** *(Faz 4: 152)* |
| **Çizim yasakları** | `selftest_visual.py` | ✓ **27/27** |
| Kill-gate ön koşulu | `kill_gate.py` | ✗ **2 engel — BEKLENEN VE DOĞRU** |

### Faz 5'te eklenen kapılar (37 denetim)

Her biri Faz 5'te **gerçek kitapta ölçülmüş** bir kusuru korur:

| Kapı | Neyi koruyor |
|---|---|
| `test_side_note_title_stays_in_column` | Yan not başlığının metin bloğuna taşması |
| `test_flowed_page_keeps_folio` | Akışta açılan sayfanın numarasız kalması |
| `test_blank_form_rows_are_writable` | Boş form satırlarının yazılamaz hâle gelmesi |
| `test_no_test_cause_gets_no_reduction_criterion` | "Test yok" diyen nedene test sonucu okutulması |
| `test_appendices_print_in_letter_order` | Eklerin harf sırası dışında basılması |
| `test_no_duplicate_chapter_number` | İki bölümün aynı numarayı taşıması |
| `test_heading_travels_with_its_content` | Başlığın içeriğinden ayrılması |
| `test_measurement_figure_travels_with_its_text` | Ölçü figürünün metninden kopması |
| `test_sign_index_points_at_the_entry_not_the_page_before` | Ek C'nin bir sayfa erkeni göstermesi |
| `test_reader_spelling_is_one_variety` | Karışık İngiliz/Amerikan imlası |
| `test_counted_claims_match_the_data` | Metnin kendi envanterini yanlış sayması |
| `test_flowchart_and_entry_agree_on_cause_order` | Şema ile metnin farklı neden sırası vermesi |
| `test_source_conflict_caption_matches_the_record` | Var olmayan bir nota gönderme |
| `test_gate_layer_never_imports_the_render_layer` | Kapı katmanının render katmanına bağlanması |

**Dört yeni kapı MUTASYONLA sınandı:** düzeltme geri alındığında kapının
gerçekten düştüğü ayrı ayrı gösterildi. Bir denetim ilk yazıldığında
mutasyonu YAKALAMAMIŞTI (gerçek çizim yolunu değil, yardımcı işlevi
sınıyordu) ve **yeniden yazıldı** — kapının kendisi de bir kapıdan geçti.

---

## 3 · Temiz Klon Doğrulaması

Gerçek `git clone` yapıldı (çalışma dizinine GÜVENİLMEDİ).

| Denetim | Sonuç |
|---|---|
| İzlenen dosya | **194** — yerel ağaçla birebir |
| On veri kapısı | ✓ hepsi geçti, **sayılar birebir aynı** |
| Yazı tipi çözümü | ✓ manifest + SHA-256 ile **ağdan edinildi**, 10/10 doğrulandı |
| Figür motoru | ✓ 163 figür yeniden üretildi — **sicil sapması SIFIR** (deterministik) |
| Çizim yasakları | ✓ 27/27 |
| Kapı testi | ✓ 167 geçti, **4 ATLANDI ve adlarıyla raporlandı** |
| Kitap dizgisi | ✗ **doğru biçimde reddetti** — proza bilerek izlenmiyor (`K9`) |

### Temiz klonda bulunan ÜÇ dürüstlük kusuru — düzeltildi

Bunlar Faz 5'in en önemli bulguları arasında, çünkü **CI'yi yalancı
yapıyorlardı**:

1. **`selftest.py` sessizce küçülüyordu.** Temiz klonda 152 → 146
   denetime düşüyor, atlananları `check(..., True)` ile **GEÇMİŞ**
   sayıyor ve kapanışta yine de *"✓ Bütün kapılar kusurlu fixture'ları
   doğru yakaladı"* diyordu. Atlananlar arasında **Faz 4'ün en önemli
   düzeltmelerini koruyanlar** vardı: `B-01` yeniden gözlem, `B-03`
   belirtiye özgü eleme, ölçüm figürü kapsaması. CI yeşildi ve o
   denetimler **hiç koşmamıştı.**
   → Atlananlar artık AYRI sayılır, adlarıyla listelenir, kapanış satırı
   *"Koşan N denetimin hepsi geçti — ama M denetim HİÇ KOŞMADI"* der.

2. **`qa_manuscript.py` yanlış gerekçe yazıyordu:** *"bu kapı Faz 4
   ÖNCESİ kitaplar için ATLANIR."* Kitap 1'in kapısı
   `phase4-production-conditional`'dır — Faz 4 öncesi **değildir**. Kapı
   kitabın fazı yüzünden değil, prozanın bilerek izlenmemesi (`K9`)
   yüzünden atlanıyor. CI çıktısını okuyan birine kitabın Faz 4'ü
   geçmediği söyleniyordu.

3. **`selftest_visual.py` yanlış kusuru gösteriyordu.** Yalnızca
   `ModuleNotFoundError`'ı "bağımlılık yok" sayıyordu; temiz klonda
   **yazı tipi ikilileri de yok** (`.gitignore § ⑧`) ve her çizim
   `FileNotFoundError` fırlatıyordu. `_raises()` bunu `ForbiddenDrawing`
   saymadığı için **11 çizim yasağı `✗` basıyordu**. Operatöre "çizim
   yasakları başarısız" deniyordu; oysa hiçbiri koşmamıştı.
   → Eksik yazı tipi artık eksik modülle aynı sözleşmeye uyar: çıkış
   kodu 2 ve edinme komutu. Beklenmeyen istisnalar ayrıca raporlanır.

---

## 4 · İddia Denetimi

Tam rapor: [`BOOK-01/08_REPORTS/PHASE_5_OPEN_CLAIMS.md`](../BOOK-01-MEASURE-AND-DIAGNOSE/08_REPORTS/PHASE_5_OPEN_CLAIMS.md)

| Kanıt düzeyi | Faz 4 | Faz 5 |
|---|---:|---:|
| `VERIFIED` | 56 | **56** |
| `INFERRED` | 214 | **214** |
| `UNVERIFIED` | 29 | **29** |
| `CONTESTED` | 8 | **8** |
| **Toplam** | 307 | **307** |

**Hiçbir iddianın epistemik durumu değişmedi.** Görev talimatı § 6 bunu
açıkça yasaklıyor ve yasağa uyuldu. Faz 5'te düzeltilen kusurların
tamamı dizgi, navigasyon ve sunum katmanındaydı.

İzlenebilirlik: **204/204** maddi iddia manüskriptte bir bloğa bağlı.

---

## 5 · Teknik Tutarlılık

### 5.1 Kalibre dil (§ 7)

Mutlakçı dil taraması yapıldı. Bulunanların **büyük çoğunluğu doğru
kalibre edilmiş** çıktı: `proves`, `definitely`, `only cause`,
`without exception` — dördü de epistemik İNKÂR ya da yordam kuralı
(*"the value of the list is that it removes a category of error, not
that it proves anything"*). `always` kullanımlarının 16'sı sıra kuralı;
`the cause is` kullanımlarının 17'si koşul cümlesi (*"If the lines
disappear, the cause is slope"*) — teşhis için DOĞRU biçim.

**İki gerçek kusur bulundu:**

| Kusur | Düzeltme |
|---|---|
| *"The third is **always** larger than the first"* — negatif payda (negative ease) YANLIŞ olan koşulsuz bir genelleme | Kapsamla sınırlandırıldı: *"In the woven garments this book is about…"* |
| Kitap **dokuma kumaş varsayıyor ama okura hiç söylemiyordu** — 252 sayfada "woven" kelimesi **sıfır** kez geçiyordu, oysa `SCOPE.md` örme/esnek dikişçisini "farklı fizik" diye kapsam dışı tutuyor, fark testi katılımcıları dokuma dikenlerden seçiliyor | *"Who this is not for"* listesine eklendi; prova kumaşı satırı da "woven" diyor |

### 5.2 Formül ve aritmetik (§ 14)

Bağımsız hesapla denetlendi: `104−94=10` ✓ · `106−104=2` ✓ ·
`102−92=10` ✓ · `2 in = 5,08 cm` ✓ · hem ekstrapolasyonu
`(2,0−0,5)/3,0 = 0,5` → 3 cm'den 4 cm'e ✓.
**Aritmetik hatası bulunmadı.**

Açık kalan: s. 72'deki tek tam işlenmiş örnekte *"unpick the side
seam**s**"* (çoğul) ile *"**a** strip … measures 3 cm"* (tekil) arasında
**birim başına mı toplam mı** belirsizliği var. Kitabın kendi vurgusuyla
bu sayı *"her gelecek kalıba"* taşınır. **§ 19 · AÇIK BULGU olarak
kaydedildi** — düzeltmesi işlenmiş örneğin yeniden yazımını gerektirir.

---

## 6 · Belirti / Neden Denetimi

| Denetim | Sonuç |
|---|---|
| 43 belirtinin altı zorunlu ögesi | ✓ 0 eksik |
| 129 aday nedenin ayırt edici kanıtı + doğrulama adımı | ✓ 0 eksik |
| BEYAN EDİLMEMİŞ neredeyse-aynı ayırt edici kanıt | ✓ **0** |
| Beyan edilen kanıt çakışması | **28** — kitapta 28 kez basıldığı ölçüldü |
| Çakışmalı belirti | 28/43 · geri kalan **15**'te kitap ayrımı İDDİA EDİYOR |

### Düzeltilen çelişki

**8 aday neden aynı maddede önce** *"There is no physical test"* **diyor,
hemen ardından** *"bu neden, belirti AZALIRSA doğrulanmıştır"* **diyordu.**
Okura önce yapacak bir test olmadığı, sonra testin sonucunu okuması
söyleniyordu. Bu nedenler kalıp/beden BELGESİYLE kapanır ve zaten bir
`Confirm by:` satırı taşırlar. Genel okuma ölçütü artık eklenmiyor.

### Düzeltilen atıf

28 çakışma kutusunun hepsi *"a known limit of **the published
evidence**"* diyordu. Kayıt aynı fikirde değil: **25'i** gerçekten kaynak
boşluğu, **3'ü** bu kitabın kendi ayırt edici kanıt taslağının kusuru
(kayıtta *"INVERTED"*, *"presupposes the conclusion"*, *"is the sign,
not a discriminator"*). Cümle 28'i için de doğru olacak biçimde
düzeltildi: *"a known limit of the method as this book states it."*

---

## 7 · Crosswalk Denetimi

| | |
|---|---:|
| Kayıt | **148** (129 teşhis→düzeltme + 19 istisna) |
| Ulaşılan aile | **20/20** |
| Dokuz bütünlük denetimi | ✓ 0 bulgu |
| Sahipsiz kaynak / varış | 0 |
| Tanımsız uç nokta | 0 |

`AF-20` (karın hacmi) dâhil tüm aileler Kitap 1'den ulaşılabilir.

---

## 8 · Terminoloji Denetimi

`qa_terminology.py` ✓ 0 bulgu (31 belge · 20 terim).

**Ama kapının sormadığı bir soru vardı ve cevabı kusurluydu:**

Kitabın prozası baştan sona **İngiliz** imlası kullanıyor
(*"centre front"*, *"centre back"* — 88 kez). İki **ölçü adı** ise
Amerikan imlasındaydı: *"Center front length"*, *"Center back length"*
(19 kez), taksonomiden geliyordu. Okur Bölüm 4'te toile'ine *"centre
front"* işaretliyor, sonra ölçü kartında ve Ek A'da *"Center front
length"* arıyor. **Aynı nirengi, aynı kitapta iki yazım.**

Düzeltildi (`M-015`, `M-016`, `M-010`, `AF-07`, `AF-14`). Kaynak
listesindeki üç *"Center"* **özel addır** (Engineering Center · U.S.
Centers for Disease Control · National Center for Health Statistics) ve
dokunulmadı; kapı bunları bağlamdan tanıyıp muaf tutuyor.

Yeni kapı yazıldığı anda **elle bulunamayan iki kaydı daha yakaladı.**

---

## 9 · Ölçü Denetimi

32 ölçünün tamamı denetlendi.

| Denetim | Sonuç |
|---|---|
| Okur adı kitapta geçiyor | **32/32** |
| Kitapta bir figürle gösteriliyor | **32/32** *(kapı ile dayatılıyor)* |
| Kayıtlı tanım çelişkisi | **4** — `M-004` bel · `M-008` bilek · `M-013` boyun tabanı · `M-025` iç dikiş |
| Çelişkinin okura beyanı | **4/4** · Ek F'nin ilan ettiği sayıyla birebir |

### İki kusur bulundu ve düzeltildi

**① Ölçü figürü metninden bir sayfa sonra basılıyordu — 32/32.**
Bölüm 2'de her birim `h3 → para → bullets → figure` sırasındadır. Sayfa
ayırma yalnızca ilk paragrafa bakıyordu; figür 4. bloktu ve **asla** aynı
sayfaya sığmıyordu. Sonuç: her figür, kendi metninden bir sayfa sonra ve
**BİR SONRAKİ ölçünün başlığının hemen ÜSTÜNDE** basılıyordu —
s. 13'te *"High bust"* figürünün altında *"Full bust"* başlığı duruyordu.
Şeridin yolunu yanlış ölçüye atfetmek için fazlasıyla yeterli.
→ **0/32 → 28/32 aynı sayfada.** Kalan 4'ü kaynak-çelişkisi notu
taşıdığı için bir sayfaya sığmıyor; figür başlıkları kendi adlarını
taşıdığından atıf belirsiz kalmıyor. **Sayfa sayısı değişmedi.**

**② Yedi figür var olmayan bir nota gönderiyordu.** *"Sources differ —
see the note in Chapter 2"* etiketi `verification_status`'tan
TÜRETİLİYORDU ("doğrulanmamış ama kaynaklı" ⇒ "sources differ"). Bölüm
2'de **dört** not var ve Ek F **"dört anlaşmazlık kaydeder"** diyor.
Üç ölçü (`M-015`, `M-017`, `M-028`) okuru olmayan bir nota yolluyordu.
→ Çelişki artık türetilmiyor, **beyan ediliyor**: public taksonomiye
`source_conflict` alanı eklendi. **7 → 4.**

---

## 10 · Görsel Denetim — Otomatik

`qa_visual.py` ✓ 0 bulgu · `selftest_visual.py` ✓ 27/27.

163 figür · deterministik 114 (%69,9) · akış şeması 47 · foto 0/6 ·
renk %0,0/%10 · ulaşılan giriş ailesi 20/20.

**Figür motoru deterministiktir:** temiz klonda yeniden üretildiğinde
sicil sapması **sıfır**.

---

## 11 · İnsan Görsel İncelemesi

Sayfalar 150 dpi'de rasterleştirilip **gerçek okuma ölçeğinde** incelendi
(küçük resim DEĞİL). Örneklem: içindekiler · ön madde · bölüm açılışı ·
metin yoğun · figür yoğun · tablo · akış şeması · belirti · ölçü · form ·
ek · çapraz atıf · son sayfa · her figür sınıfından en az bir örnek.

### Otomatik denetimin GÖREMEDİĞİ, gözle bulunan kusur

**Yan not başlığı metin bloğunun ÜSTÜNE basılıyordu.** `side_note()`
gövdeyi sütun genişliğine sarıyor, **başlığı sarmıyordu**; `drawString`
hiçbir sınır tanımaz. 36 yan notun 3'ünde başlık taşıyordu.

Gözle görüldü, sonra **255 sayfanın tamamında ölçüldü**: her kelimenin
kutusu çıkarılıp dikdörtgen kesişimi arandı.

| Sayfa | Taşma | Sonuç |
|---|---|---|
| s. 72 (verso) | metin bloğuna **33,2 pt** | harfler üst üste — *"what a turn of the cycle…"* okunamıyor |
| s. 50 (verso) | metin bloğuna **4,3 pt** | *"before"* kelimesinin "b"si üzerine basılmış |
| s. 61 (recto) | dış kenar boşluğuna **17,4 pt** | kitabın kendi geometri sözleşmesi ihlali |

**Ölçülen çakışma: 5 · şimdi 0.**

---

## 12 · Navigasyon Denetimi

### Ek C — kitabın TEK giriş yolu — 43 belirtinin 18'inde KIRIKTI

`build_book.run_pass` belirti başlığının sayfasını **başlık dizilmeden
önce** okuyordu. Başlık sayfanın dibine denk gelip sonraki sayfaya
kaydığında kaydedilen numara **bir önceki sayfa** oluyordu.

Bu, kitabın ilan ettiği tek giriş yolunda oluyordu: Ek C kendini
*"This is the way in"* diye tanıtır ve **43 akış şemasının hepsi**
*"go back to the sign index in Appendix C"* ile biter. Yanlış sayfaların
çoğu **başka bir belirtinin** karar tablosudur ve o tablo da aynı cümleyle
biter — okur kendisini gönderen satıra geri döner. **Kapalı döngü.**
Ek H de aynı sayfa modelini kullandığı için aynı sapmayı devralıyordu.

| Denetim | Önce | Sonra |
|---|---:|---:|
| Ek C belirti işaretçisi | 18 yanlış | **43/43 doğru** |
| `Chapter N (page P)` atfı | — | **11/11 doğru** |
| Ek H sayfa atıfları | sapmalı | **hepsi bir giriş başlangıcına düşüyor** |
| İçindekilerdeki parça satırı | 6/6 kendi ayracını atlıyor | **6/6 doğru** |
| Yinelenen bölüm numarası | s. 221 ve s. 225 ikisi de "CHAPTER 16" | **yok** |

### Diğer navigasyon kusurları

* **Ekler harf sırası DIŞINDA basılıyordu:** A, B, D, E, F, G, **C**, H, I.
  Üretilen üç dizin (C, H, I) yazılmış eklerin sonuna ekleniyordu. Ek C —
  43 şemanın işaret ettiği giriş — dokuz ekin **yedincisindeydi**.
  Sırayla çeviren okur onu B ile D arasında arar ve bulamaz.
  → `index_slot` işaretçileriyle alfabetik konuma yerleştirildi.
* **İçindekiler "Part 6 — Appendices" satırında bitiyordu.** Dokuz ekin
  hiçbiri listelenmiyordu. → Dokuzu da sayfa numarasıyla listelendi.
* **Yanlış bölüme yönlendirme:** *"…is a plain length cause. That is the
  entry in **Chapter 12**."* O giriş (`SYM-043`) Bölüm 12'de değil,
  **bütün-giysi bölümündedir**. Okur koca bir Parça öteye gönderiliyordu.

---

## 13 · Okur Yolculukları

Üç uçtan uca simülasyon koşuldu (birincil üretimden AYRI).

| Yolculuk | Senaryo | Sonuç |
|---|---|---|
| **A** | Sırtta yatay kıvrım | Ek C'de **kapalı döngüye** düştü |
| **B** | Yan dikiş öne kayıyor + ön etek ucu yüksek | Yanlış bölüme yönlendirildi |
| **C** | Ağ altında çekme + bacak dönüyor | Ek C'de **kapalı döngüye** düştü |

**Yolculukların bulduğu ve düzeltilen:** Ek C sapması (§ 12), Bölüm 12
yönlendirmesi, yinelenen bölüm numarası.

**Yolculukların DOĞRULADIĞI (kırılmayan):**

* **Yedi adımlı döngü** — geri dönülebilirliğe göre sıralı tırmanma
  merdiveni açık ve sınırlı.
* **43/43 girişte yetersiz düzeltme, ikinci nedenden ÖNCE geliyor** —
  Faz 4'ün `CC-21` düzeltmesi ayakta.
* **129/129 nedenin bir doğrulama adımı var.**
* **43 akış şemasının hepsi açık bir çıkışla bitiyor**, hiçbiri havada
  kalmıyor.
* **Çok belirtili durum yanıtlanıyor:** s. 71 → Bölüm 16 → bağımlılık
  modeli.
* Bölüm 5 prova protokolü tam uygulanabilir; Bölüm 8 eleme listesi doğru
  bağlanmış.

---

## 14 · Baskı Simülasyonu (1-bit)

23 temsilci sayfa 300 dpi'de rasterleştirilip 1-bit'e indirgendi.

| Denetim | Sonuç |
|---|---|
| Yapısal çizgiler (gövde, tablo, akış şeması) | **≥ 2 px — hayatta** |
| Etiketler ve figür başlıkları | okunur |
| Oklar ve karar düğümleri | hiyerarşi korunuyor |
| Tek piksellik koşular | %0,7–4,4 — hepsi harf ucu, yapısal çizgi değil |
| En ince beyan edilen çizgi | 0,4 pt (`callout_leader`) |

**⚠ FİZİKSEL BASKI PROVASI YAPILMADI.** Bu bir **dijital** simülasyondur.
Gerçek kâğıt provası `D-06` altında **DIŞ BEKLEMEDEDİR**.

---

## 15 · Sayfa Sayısı

| | |
|---|---:|
| Ölçülen sayfa | **255** |
| Hedef bant | 220–260 ✓ |
| Cilt payı | 0,875 in (KDP asgarisi 0,5 in) |
| Dış / üst / alt kenar | 0,625 / 0,75 / 0,75 in (asgari 0,25 in) |
| 300 sayfa eşiği | **aşılmadı** — cilt payı yeniden hesaplanmıyor |
| Metin bloğu dışına taşan kelime | **0** |

Faz 4'ten değişim: **252 → 255 (+3)**. Tamamı düzeltmelerin ölçülmüş
maliyetidir; hiçbiri içerik eklemesi değildir.

---

## 16 · Bağımsız Son İnceleme

Birincil üretimden AYRI, çelişmeli bir inceleme koşuldu. **33 bulgu**
bildirdi. Her biri MEVCUT yapıya karşı yeniden ölçüldü.

| Sınıflandırma | Sayı |
|---|---:|
| **KABUL + DÜZELTİLDİ** | **8** |
| **ÇÜRÜTÜLDÜ** (ölçümle) | **4** |
| **KABUL — AÇIK** (içerik turu gerektiriyor) | **6** |
| Daha önce düzeltilmişti (bayat yapıdan okunmuş) | 3 |
| Alt-şiddet / kayda geçirildi | 12 |

### Çürütülenler — ölçümle

| Bulgu | Neden çürütüldü |
|---|---|
| **"Ters teşhis"** (omuz eğimi) | İncelemeci İKİ AYRI belirtiyi birleştirmiş. `SYM-004` boyun noktasından çapraz çizgiler (omuz UCUNDA toplanma); `SYM-005` omuz dikişinin ALTINDA yatay kıvrım. Dört yön de tutarlı: vücut kalıptan KARE ise omuz ucu kaldırılır, daha EĞİK ise alçaltılır. |
| **"Dört mü beş mi sıra kuralı"** | Kitap *"Four rules that are settled"* + *"One rule that is contested"* = **beş** diyor. Her iki sayı da doğru. |
| **"Şema, karşı sayfanın sıra kuralını çiğniyor"** | Kitap bu ayrımı AÇIKÇA yapıyor: s. 61 *"Reading order, not correcting order · This is the order you LOOK in. The order you CORRECT in is different."* Şema teşhis sırası, `Order:` satırı düzeltme sırasıdır. |
| **"Centre/Center kopukluğu gelecek"** | Zaten düzeltilmişti; inceleme bayat bir PDF'ten okumuş. |

### Kabul edilip düzeltilenler

Ek C sapması · şema/metin neden sırası uyuşmazlığı · içindekiler parça
satırları · kaynak-çelişkisi etiketi · üç sayım hatası ("eleven"→12,
"two widths and two depths"→üç ve iki, "five"→19) · çakışma kutusu atfı.

### Kabul edilen ama AÇIK bırakılanlar — § 19

### Faz 5'in KENDİ ürettiği kusur — ve nasıl yakalandı

Dürüstlük gereği kaydedilir: Faz 5'te **yazdığım iki denetim CI'yi
düşürdü.**

`test_appendices_print_in_letter_order` ve `test_no_duplicate_chapter_number`
`build_book`'u içe aktarıyordu; zincir `build_book → figure_engine →
figure_tokens → reportlab`'a iniyor. CI'nin `selftest` işi **tasarım
gereği** hiçbir üçüncü taraf paket kurmaz ve iş `ModuleNotFoundError`
ile düştü.

**Neden yerel denetimlerim yakalamadı:** bu makinede reportlab kurulu.
Temiz klon denetimim de aynı sebeple yakalayamadı — klon *yeni* ama
*ortam* aynı. Kusuru gösteren tek şey **gerçek CI koşusu** oldu.

`bookplan.py` tam bu ayrım için var ve docstring'i bunu 2024'ten beri
söylüyor: *"build_book reportlab'a bağlıdır, kapı ise bağlı
OLMAMALIDIR."* Üç saf yapı (`CHAPTER_TITLES`, `CHAPTER_BY_NUMBER`,
`fill_index_slots`) oraya taşındı.

**Kalıcı önlem:** `test_gate_layer_never_imports_the_render_layer`,
`selftest.py`'nin KENDİ kaynağını AST ile tarar ve korumasız bir
`test_*` işlevinin render katmanını içe aktarmasını yakalar.

**Ve ortam artık taklit ediliyor:** CI koşulları (proza YOK + reportlab
`meta_path` ile ENGELLENDİ + gerçek git deposu) yerelde yeniden üretildi
ve doğrulandı — çıkış kodu 0, 156 denetim koştu, 12 atlandı ve on ikisi
de adıyla raporlandı.

> **Ders `R-19`'un ta kendisi:** bir kapının yeşil olması, o kapının
> koşacağı ORTAMDA yeşil olacağı anlamına gelmez. Faz 5 bunu bir kez
> daha, bu kez kendi eliyle öğrendi.

---

## 17 · Regresyonlar

| Ölçüt | Faz 4 | Faz 5 | Δ | Açıklama |
|---|---:|---:|---:|---|
| Sayfa | 252 | **255** | +3 | düzeltmelerin ölçülmüş maliyeti |
| Figür yerleşimi | 175 | **175** | 0 | — |
| Ayrı figür | 159 | **159** | 0 | — |
| Bölüm | 21 | **21** | 0 | — |
| Kelime | 42 224 | **41 995** | −229 | +75 kapsam beyanı, −8×53 çelişkili okuma ölçütü |
| İzlenen iddia | 204 | **204** | 0 | — |
| Kapsanan belirti | 43 | **43** | 0 | — |
| Crosswalk | 148 | **148** | 0 | — |
| Terim | 20 | **20** | 0 | — |
| Çözülmemiş iddia | 251 | **251** | 0 | — |
| **Kapı denetimi** | 152 | **189** | **+37** | Faz 5 regresyonları |

**Hiçbir düzeltme başka bir alt sistemi sessizce bozmadı.** Kelime
farkının tamamı kalem kalem açıklanmıştır.

### Görsel regresyon

Sayfa sayısı bilinçli olarak değiştiği için sayfa-sayfa özdeşlik
karşılaştırması anlamlı değildir. Bunun yerine **kitap geneli
değişmezler** yeniden ölçüldü:

| Değişmez | Sonuç |
|---|---:|
| Harf çakışması | **0** |
| Kenar boşluğu ihlali | **0** |
| Metni olup numarası olmayan sayfa | **0** |
| Yanlış/yinelenen folyo | **0** |
| Ek C işaretçisi | **43/43** |
| Ortalama sayfa doluluğu | %78,1 |

---

## 18 · Kalan Dış Doğrulama

**Faz 5 `D-01` ve `D-02`'yi PASS'e ÇEVİRMEZ ve çevirmedi.**

| # | Bekleyen | Durum | Engelleyici |
|---|---|---|---|
| `D-01` | Fark testi — 3 ev dikişçisi | **0/3 katılımcı · `measured: false`** | **EVET — HARD STOP** |
| `D-02` | Fiziksel doğrulama — 19 `VAL` kaydı | **0/19 uygulandı · `measured: false`** | **EVET — HARD STOP** |
| `D-06` | KDP Previewer + prova baskı | yapılmadı | EVET (Faz 6) |
| `D-03` | Marka temizliği | yapılmadı | EVET (yayın öncesi) |
| `D-07` | ISO 8559-1 / ASTM D5219 edinimi | edinilmedi | hayır (4 `CONTESTED` iddiayı kapatırdı) |

`kill_gate.py` **2 engel** raporlamaya devam ediyor ve bu **doğrudur**.

> **İNSAN DOĞRULAMASI YAPILMADI. FİZİKSEL DOĞRULAMA YAPILMADI.
> FİZİKSEL BASKI PROVASI YAPILMADI.** Bu rapor hiçbirini iddia etmiyor.

---

## 19 · Riskler ve AÇIK BULGULAR

Doğrulandı ama Faz 5'te **düzeltilmedi** — çünkü düzeltmeleri **içerik
turu** gerektiriyor (kaynak doğrulaması + taksonomi değişikliği), ve
Faz 5 bir içerik genişletme fazı değildir.

| # | Bulgu | Ölçüm | Neden açık |
|---|---|---|---|
| **A-01** *(`R-25`)* | **Karın nedeni göğüs ailesine yönleniyor** | `SYM-018.C1` *"Not enough volume in the front (bust **or abdomen**)"* → `AF-01` göğüs hacmi. `SYM-040.C1` *"A volume (bust, **abdomen** or seat)"* → `AF-01`. Oysa `AF-20` karın ailesi Faz 4'te tam bunun için eklendi ve `SYM-017.C3` doğru yönlendiriyor | Doğru düzeltme nedeni BÖLMEK ya da yeni neden EKLEMEKtir → crosswalk, şema, iddia sicili zinciri. Kaynak doğrulaması ister |
| **A-02** *(`R-26`)* | **46 `Confirm by` satırı kitabın öğretmediği bir ölçüye atıfta bulunuyor** | 129 satırın 12'si dürüstçe *"There is no measurement for this"* diyor; 71'i öğretilen bir ölçüyü adlandırıyor; **46'sı** *"the height of the shoulder tip"*, *"your own profile"* gibi öğretilmeyen bir şeye başvuruyor. Bir kısmı KALIP ölçüsüdür (Bölüm 3 öğretiyor), bir kısmı öğretilen ölçünün BAŞKA ADIdır (*"front-to-back length difference"* = `M-032`) | Üçe ayrılıp her biri ayrı ele alınmalı: takma ad → adlandırma birliği; kalıp ölçüsü → Bölüm 3'e atıf; gerçekten öğretilmeyen → ya öğret ya *"no measurement"* de |
| **A-03** | **İşlenmiş örnekte birim belirsizliği** | s. 72: *"unpick the side seam**s**"* (çoğul) + *"**a** strip … 3 cm"* (tekil). "3 cm" kenar başına mı toplam mı belli değil; kitabın kendi vurgusuyla bu sayı *"her gelecek kalıba"* taşınır | Örneğin yeniden yazımını gerektirir |
| **A-04** | **İki figür alanı inç, kitap metrik** | *"excess: ___ in"*, *"shortfall: ___ in"* — kitabın tek birim etiketleri, oysa işlenmiş örnek ve Bölüm 2 metrik. Ek E'nin kartında birim sütunu YOK | Birim politikası kararı gerektirir (`D-06` ile birlikte) |
| **A-05** *(`R-27`)* | **Belirti figürü, teşhis işaretini gövdeden HAFİF çiziyor** | Gövde dış hattı **1,2 pt**, çekme çizgisi işareti **0,6 pt** — figürün ÖZNESİ, çerçevesinin **yarısı** kalınlıkta. 43 `fit_sign_on_figure` figürünü etkiler | Token ağırlığı değişikliği **baskı kalibrasyonunun** yeniden koşulmasını ister → **Faz 6** girdisi |
| **A-06** | **Bölüm 8 eleme listesi ile Ek D listesi aynı 14 öge DEĞİL** | Prozada *"Fabric, preshrinking"* var, *"Measuring"* yok; şema ve Ek D'de tersi. İkisi de 14 | İçerik kararı: hangi 14 |

Üçü `RISK_REGISTER.md`'ye **`R-25` · `R-26` · `R-27`** olarak kaydedildi.

Ayrıca: **`R-19` (kapılar yeşilken
ürün bozuk) Faz 5'te BİR KEZ DAHA gerçekleşti** ve bu sefer üç ayrı
biçimde (dizgi çakışması · navigasyon sapması · CI'nin kendi kapsamını
sessizce küçültmesi). Risk **kapanmadı; güçlendirildi.**

---

## 20 · Faz 6 Hazırlığı

### Faz 5 kapısı — İÇSEL OLARAK GEÇTİ

| Kapı ölçütü | Durum |
|---|---|
| Otomatik QA sıfır hata | ✓ |
| Yapısal QA sıfır çözülmemiş hata | ✓ |
| Desteklenmeyen kritik iddia | ✓ yok |
| Kritik görsel kusur | ✓ yok |
| Kritik navigasyon yolu | ✓ hepsi çalışıyor |
| Okur yolculuğunda kritik çıkmaz | ✓ yok |
| Regresyon denetimleri | ✓ hepsi geçti |

### KİTAP KAPISI İLERLEMEDİ — ve bu doğrudur

`.gate` **`phase4-production-conditional`** olarak KALDI.

Kümülatif sırada bu değer `phase3-pilot`'un **ÖNÜNDEDİR** ve
`kill_gate.py` iki engeli raporlamaya devam etmektedir. `phase5-qa`
bu yoldan **açılamaz** — mekanik kilit tasarım gereği çalışıyor.
Faz 5'in içsel işi bitti; kapıyı açacak olan şey kod değil, **ölçüm**.

### Doğru durum beyanı

> # QA COMPLETE / EXTERNAL VALIDATION PENDING

**"HUMAN VALIDATED" DEĞİL. "PHYSICALLY VALIDATED" DEĞİL.
"READY FOR PUBLICATION" DEĞİL.**

### CI durumu

| İş | Sonuç |
|---|---|
| `gates` · `spec` · `structure` · `crosswalk` · `boundary` · `claims` · `visual` · `selftest` · `render` · `manuscript` | ✓ **onu da geçti** |
| `killgate` | ✗ **tasarım gereği başarısız** (`continue-on-error`) |

Genel sonuç: **success.**

### Faz 6'ya devredilenler

1. `D-06` — KDP Previewer, gerçek sayfa geometrisi, **fiziksel prova baskı**
2. **A-05** — figür hiyerarşisi (token ağırlığı ⇒ baskı kalibrasyonu)
3. **A-04** — birim politikası
4. `D-03` — marka temizliği

### Faz 6 ÖNCESİ kapatılması gerekenler

**A-01** (karın yönlendirmesi) ve **A-02** (öğretilmeyen ölçüye atıf)
teşhis doğruluğunu etkiler ve bir **içerik turunda** kapatılmalıdır.
Faz 6 biçim doğrulamasıdır; bu ikisi biçim değil, içeriktir.

---

*Vâliçe Press · BEFORE YOU CUT · Kitap 1 · Faz 5 QA Raporu · 29 Ağustos 2026*
