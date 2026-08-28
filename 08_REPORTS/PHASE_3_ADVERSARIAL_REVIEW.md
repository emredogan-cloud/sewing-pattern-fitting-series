# PHASE 3 — ÇELİŞMELİ İNCELEME

> **Amaç: Kitap 1'i KIRMAK.** Bu belge bir onay değildir ve bir onay
> olarak alıntılanamaz.
>
> ⚠ **Bu bir insan uzman incelemesi DEĞİLDİR** ve hiçbir yerde öyle
> sunulamaz (`CLAIMS_STANDARD.md § 1`). Bir AI incelemesinin
> `DIFFERENTIATION_TEST § 7.1` uyarınca **izinli** kullanımıdır:
> protokol eleştirisi, iç tutarlılık denetimi ve başarısızlık senaryosu
> üretimi. **Katılımcı yerine geçemez.**
>
> Kapsam: Faz 2 görsel sistemi + Faz 3 pilot paketi.
> Tarih: 28 Ağustos 2026.

---

## 0 · Bulgu özeti

| # | Bulgu | Şiddet | Durum |
|---|---|---|---|
| **B-01** | Akış şeması "ilk evet kazanır" mantığı, aynı anda iki nedeni olan okuru yanlış dala götürür | **YÜKSEK** | **AÇIK — Faz 4'e taşındı** |
| **B-02** | `SYM-016` C2 dalı (beden seçimi) bir teşhis değil, bir çıkış kapısı | ORTA | **KABUL EDİLDİ, gerekçe yazıldı** |
| **B-03** | Eleme şeması 11 adım uzunluğunda; okur onu her belirtide tekrar yürütmez | **YÜKSEK** | **AÇIK — Faz 4 tasarım kısıtı** |
| **B-04** | Belirti figürlerinin 43'ü de aynı şablondan üretildi; gerçek kumaş dökümü yok | ORTA | **BİLİNEN — `manual_reason` kayıtlı, `D-02`'ye bağlı** |
| **B-05** | Kroki tek bir vücut tipini gösteriyor; kitap her vücut için yazıldığını ima ediyor | **YÜKSEK** | **AÇIK — Faz 4 metin kısıtı** |
| **B-06** | "⅝ inç dikiş payı" varsayımı kaynakta `OBSERVED`, kalıba göre değişir | DÜŞÜK | **KABUL — pilotta geçmiyor** |
| **B-07** | Fark testi Malzeme B'nin edinimi kurucuya bağlı; edinilemezse test yapılamaz | ORTA | **AÇIK — `D-01` alt bağımlılığı** |
| **B-08** | Pilot 8 sayfa; tam bölüm ölçeklenirse Kitap 1 sayfa hedefini aşar | **YÜKSEK** | **ÖLÇÜLDÜ — § 5** |
| **B-09** | `flow_ELIMINATION` sayfası dokuz kez aynı çıkış metnini tekrarlıyor | DÜŞÜK | **KABUL — işlevsel tekrar** |
| **B-10** | Faz 2'nin bütün kapıları yeşilken figürlerin hiçbiri kullanılamıyordu | **KRİTİK** | **KAPATILDI — `K45`, yeni kapı eklendi** |
| **B-11** | `.gitignore` sır deseni iki kaynak dosyayı yutuyordu; temiz klonda görsel sistem çalışmazdı | **KRİTİK** | **KAPATILDI — `K47`, regresyon eklendi** |

**Üç YÜKSEK ve İKİ KRİTİK bulgu.** Biri kapatıldı, üçü Faz 4'e
yazılı kısıt olarak taşındı. **HARD_STOP bulgusu yok** — ama `B-01`,
`B-03` ve `B-05` fark testinin (`D-01`) sonucunu doğrudan etkileyebilir
ve testten ÖNCE değil, testin SONUCUYLA birlikte ele alınmalıdır.

---

## 1 · `B-01` — "ilk evet kazanır" yanlış dal üretebilir

**İddia.** Motor her belirti şemasını sıralı bir ikili karar zinciri
olarak kurar ve okur ilk "evet"te durur. Ama `SYM-016`'nın üç nedeni
**birbirini dışlamaz**: bir okurda hem fazla göğüs hacmi hem de yanlış
konumlanmış bir pens ucu olabilir.

**Kırma senaryosu.** Okur ilk karara "evet" der (`AF-01` göğüs hacmi),
düzeltmeyi uygular, çekme çizgileri **azalır ama kaybolmaz**. Kitap
ona ne yapacağını söylemez: şema bitmiştir.

**Neden ciddi.** Bu, kitabın vaadinin (`SEE THE PROBLEM`) tam olarak
başarısız olduğu yerdir. Okur bir teşhis aldı, uyguladı, sorun kısmen
sürüyor ve elinde bir sonraki adım yok.

**Neden bu turda kapatılmadı.** Çözüm bir **metin** çözümüdür, bir
veri çözümü değil: her şemanın sonuna "düzeltmeden sonra yeniden
gözlemle" döngüsü ve "belirti azaldı ama gitmedi" dalı gerekir. O metin
Faz 4'ün işidir ve Faz 3 kill-gate'i geçmeden yazılamaz.

**Faz 4 için yazılı kısıt.** Her belirti girişi bir **yeniden gözlem
adımı** ile bitecektir. Şema verisi bunu destekliyor: her `AF-xx`
kaydında `interacts_with` alanı zaten var ve `SYM-016 → AF-01`
kaydının `order_constraint`'i "omuz ve boyun düzeltmelerinden SONRA"
diyor.

**Karşı argüman — kaydedildi.** Rakip mimari (katalog) bu sorunu
**hiç** ele almaz; okur orada da yarı çözülmüş bir sorunla kalır. Bu,
bulguyu geçersiz kılmaz ama şiddetini bağlamına oturtur.

## 2 · `B-02` — beden seçimi bir teşhis değil

**İddia.** `SYM-016`'nın ikinci dalı "her yerde aynı gerginlik var" →
`AF-18` (bedenler arası derecelendirme). Bu bir düzeltme ailesi değil,
"yanlış kitaptasınız" demenin kibar hâli.

**Kabul edildi.** Ve **doğru olan budur.** Bir teşhis sisteminin en
değerli çıktılarından biri "bu bir kalıp düzeltme sorunu değil"
demektir. `SYM-016 C2`'nin `likelihood_note`'u zaten bunu yazıyor:
*"BEDEN sorunudur, düzeltme sorunu değil."*

**Ama pilot metni bunu söylemiyor.** Akış şeması okuru `AF-18`'e
gönderiyor ve düğüm "Grading between sizes" yazıyor — okur bunu bir
düzeltme sanabilir. **Faz 4 kısıtı:** `AF-18`'e giden düğümler
metinde açıkça "bu bir beden seçimi kararıdır" ile karşılanacaktır.

## 3 · `B-03` — eleme şeması çok uzun

**İddia.** 11 karıştırıcı sınıfı, iki sayfaya bölünmüş bir şema. Hiçbir
okur bunu 43 belirtinin her birinde yürütmez. İkinci kez atlanır.

**Ölçüm.** Eleme şeması pilotun **8 sayfasının 1'ini** tek başına
kaplıyor — %12,5.

**Neden ciddi.** Eleme adımı kitabın en özgün parçasıdır (rakip
mimaride yoktur) ve **atlanırsa bütün teşhisler kirlenir.**

**Faz 4 kısıtı — iki seçenek, ikisi de test edilecek:**

1. **Kısa liste + tam liste ayrımı:** her belirti girişinde üç satırlık
   bir "bu belirtide en sık karışan üç şey" kutusu; tam 11'lik liste
   yalnızca bir kez, Bölüm 3'te.
2. **Belirtiye özgü eleme:** `confounders_to_rule_out` alanı zaten
   belirti başına kayıtlı — şema genel değil, belirtiye özgü üretilir.

**Veri seçenek 2'yi destekliyor** ve motor bunu bugün üretebilir.
Ama hangisinin daha iyi olduğu bir **okuma** sorusudur ve `D-01`'in
5. sorusuna eklenmelidir.

## 4 · `B-05` — tek kroki, "her vücut" vaadi

**İddia.** 154 figürün tamamı **tek bir kroki oranından** üretiliyor.
Kitap uyum sorunlarının vücut çeşitliliğinden doğduğunu söylüyor ama
her figürde aynı vücudu gösteriyor.

**Neden ciddi.** Hedef okur "kalıbı doğru uyguladım, giysi yine
oturmuyor" diyen kişidir — yani kalıbın **varsaydığı vücudun dışında**
olan kişi. Ona her sayfada kalıbın varsaydığı vücudu göstermek,
kitabın kendi tezini görsel olarak yalanlar.

**Karşı argüman.** Kroki bir **çizim konvansiyonudur** ve `K43` bunu
açıkça antropometrik iddiadan ayırır. Bir ölçüm figürünün işi "şerit
nereden nereye gider"i göstermektir, vücut çeşitliliğini değil.

**Ama bu argüman belirti figürleri için GEÇERLİ DEĞİL.** Bir belirti
figürü tam olarak *bu vücutta bu kumaş ne yapıyor* sorusunun resmidir.
43 belirti figürünün hepsinin aynı silüette olması, `B-04` ile
birleşince ciddi bir zayıflıktır.

**Faz 4 kısıtı.** `croquis.py` oranları **parametreleştirilebilir**
(tek bir tabloda duruyorlar). En az üç varyant — düz sırt, yuvarlak
sırt, dolgun göğüs — belirti figürlerinde kullanılmalıdır. Maliyet:
motor değişikliği **yok**, yalnızca üç oran tablosu.

## 5 · `B-08` — sayfa bütçesi ÖLÇÜLDÜ ve hedefi aşıyor

**Bu turun en somut bulgusu.**

| Ölçüm | Değer |
|---|---|
| Pilot: bir bölgenin **üç** belirtisi + anatomi + eleme | **8 sayfa** |
| Aynı içerik **beş** belirtiyle (ilk sürüm) | **13 sayfa** |
| Bölge başına ortalama belirti | 4,3 |
| **10 bölge için doğrusal tahmin** | **≈ 80–110 sayfa** |
| Kitap 1 sayfa hedefi | 220–260 |

İlk bakışta hedef **rahat** görünüyor. Ama pilot yalnızca **bölge
atlasını** içeriyor. Bölüm mimarisi 5 parça ve 18 bölümdür; bölge
atlası bunun bir parçasıdır. Ölçüm bölge atlasının hedefin
**yaklaşık %40'ını** yiyeceğini söylüyor.

**Asıl risk sayfa sayısı değil, CİLT PAYI.** `page_geometry.json`
151–300 sayfa bandını varsayıyor ve cilt payını 0,875 inç seçti.
**300 sayfa aşılırsa** KDP asgarisi 0,625 inç'e çıkar ve metin bloğu
daralır — bütün sayfa geometrisi yeniden hesaplanır. `qa_visual § ⑨`
bunu denetliyor ve sayfa hedefi banttan taşarsa **kırmızı yakıyor.**

**Faz 4 kısıtı.** Bölge atlası **100 sayfayı aşarsa** kapsam
daraltılır (belirti sayısı değil, belirti başına sayfa).

## 6 · `B-10` — kapılar yeşilken ürün kullanılamıyordu

**En ciddi bulgu ve tek KRİTİK olan.**

Faz 2 sonunda: `qa_all.sh` sıfır hata, `selftest.py` **o anda** 131/131,
CI yeşil,
`figures.json` 154 kayıt, deterministik oran %68,2 — **ve üretilen
figürlerin hiçbiri kitaba konulamazdı**, çünkü hepsi proje belge
dilinde (Türkçe) yazılmıştı.

**Bir kapı kümesi, sormadığı soruyu yakalayamaz.**

**Kapatıldı** (`DECISIONS.md K45`): okura dönük etiket katmanı
(`labels_en.json`) + `qa_visual § ⑩` + selftest regresyonu. Motor artık
etiket katmanı yoksa **çalışmayı reddediyor**.

**Aynı sınıftan ÜÇ bulgu daha aynı turda çıktı ve kapatıldı:**

- İç kayıt kimlikleri (`SYM-016`, `AF-01`) okura dönük figürlere
  basılıyordu — `TYPOGRAPHY_STANDARD § 3.4` ile çelişki. Kapı eklendi
  (`check_internal_id_leak`), `TK-18` spec'i düzeltildi.
- İşaret noktası etiketleri **üst üste biniyordu** — bir ölçü kitabında
  çakışan etiket yanlış okunur. Kapı eklendi
  (`check_label_collisions`), yerleşim algoritması yeniden yazıldı.
- **`B-11`:** `.gitignore`'un sır deseni (`*_token*`)
  `06_BUILD/figure_tokens.py` ve `06_BUILD/calibrate_tokens.py`'yi
  **yutuyordu**. Depo yerelde yeşil, temiz bir klonda **çalışmaz**
  hâldeydi ve CI bunu görmüyordu — CI görsel motoru çalıştırmıyor,
  yalnızca kapıları çalıştırıyor. Desen daraltıldı, regresyon eklendi
  (`K47`).

**Ders.** Dört bulgunun dördü de "kapı yeşil, ürün bozuk"
sınıfındandır ve dördü de **elle bakarak** bulundu — kapılar bulmadı.
Üçü ürüne bakılarak, biri commit'e bakılarak. Faz 4'ün her turunda
(a) üretilen sayfalardan bir örneklem ve (b) `git status
--untracked-files=all` çıktısı **gözle** incelenmelidir; otomatik
kapılar bunun yerine geçmez.

## 7 · Kırılmayan şeyler — denendi, dayandı

Bir çelişmeli inceleme yalnızca bulduklarını değil, **bulamadıklarını**
da kaydetmelidir.

| Saldırı | Sonuç |
|---|---|
| "Bir akış yolu boşta bitiyor olabilir" | **Yapısal olarak imkânsız** — son karar düğümünün `hayır` dalı her zaman bir eleme düğümüne bağlanıyor; `qa_visual § ④` ayrıca denetliyor |
| "Bir düzeltme ailesine ulaşılamıyor olabilir" | **19/19 ulaşılıyor** — ölçüldü |
| "Doğrulanmamış bir kayıt sessizce yükseltilmiş olabilir" | `validate_spec § check_verification_evidence` engelliyor; selftest kusurlu fixture'la kanıtlıyor |
| "`TK-05` ile `TK-06` baskıda karışabilir" | Eğrilik oranı **3,49** (eşik 2,0) — ölçüldü. *Ama dijital ölçüm; gerçek baskı `D-06`* |
| "Figür token listesi gerçeği yansıtmıyor olabilir" | Liste **beyan değil ölçüm** — çizim çağrılarından türetiliyor |
| "Sayfa geometrisi KDP'yi ihlal ediyor olabilir" | Platform asgarileri `qa_visual § ⑨`'da denetleniyor (`S-0016`) |
| "Kill-gate bayrağı elle açılabilir" | `aiProxyCountsAsHuman` açılamıyor; `measured=true` artık VAL kayıtlarıyla **çapraz denetleniyor** |

## 8 · Bu incelemenin YAPAMADIĞI

1. **Okur anlıyor mu.** Tek gerçek sınav `D-01`'dir. Bu belge
   protokolü eleştirebilir, okurun yerine geçemez.
2. **Diyagramlar geometrik olarak doğru mu.** Tek gerçek sınav
   `D-02`'dir. Bir figürün "doğru görünmesi" bir doğrulama değildir.
3. **Baskıda okunuyor mu.** `D-05` ve `D-06`.

---

*Vâliçe Press · BEFORE YOU CUT · Phase 3 Adversarial Review · 28 Ağustos 2026*
