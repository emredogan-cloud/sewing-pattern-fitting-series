# BOOK-01-DIFFERENTIATION-TEST — **KİLL-GATE PROTOKOLÜ**

> Faz 1 çıktısı 9/10. Görev talimatı § 36.12.
> Kaynak: araştırma raporu § 35 madde 1 — **KİLİT KAPI**.
>
> `OPEN_QUESTIONS A14` — **protokol Faz 1 yürütmesinde TAMAMLANDI;
> ölçüm DIŞ DÜNYADA BEKLİYOR** (`DECISIONS.md K30`).
>
> ⚠ **Bu test HENÜZ YAPILMADI.** `series_config.json →
> killGates.differentiationTest.measured` = `false`.

---

## 1 · Neden bu test var

Bu projenin **tek kanıtlanmamış temel hipotezi** şudur:

> **D1:** Teşhis-önce mimari (akış şeması), rakiplerin katalog
> mimarisinden okur için ölçülebilir biçimde daha anlaşılırdır.

**Dayanağı:** kategori liderinde (n=1.797) Amazon'un kendi
sayısallaştırılmış olumsuz etiketi `Complexity(58)` ve özet metni
"some find it too complicated for their understanding" `OBSERVED`
27 Ağu 2026.

**Kanıtlanmayan kısım:** alıcının bu farkı **fark ettiği**. Bir kalite
açığını çözmek, alıcının çözüldüğünü görmesiyle aynı şey değildir.

Bu hipotez çürükse **üç kitap da aynı hipoteze dayanıyordu.**

## 2 · Test tasarımı

| | |
|---|---|
| **Katılımcı** | **Üç gerçek ev dikişçisi** — § 5'in eleme ölçütlerine uyan |
| **Malzeme A** | Kitap 1'in pilot bölümünden **tek bir teşhis bölümü** (tam akış şemasıyla) — § 6 |
| **Malzeme B** | Kategori liderinin **aynı konudaki** bölümü — § 6.2 |
| **Sunum** | Yan yana, **markasız** (kapak, logo, yazar adı görünmez) |
| **Sıra** | Katılımcılar arasında **değiştirilir** (sıra etkisi kontrolü) |
| **Görev** | Okuyun ve kendi giysinizdeki bir uyum sorununu teşhis etmeye çalışın |
| **Soru** | Yönlendirmesiz açık uçlu: *"Bu iki metin arasında fark var mı? Varsa nedir?"* |
| **Süre** | 30–40 dakika |

## 3 · GEÇME KRİTERİ — tek ve değiştirilemez

> **Üç okurdan en az İKİSİ, farkı KENDİLİĞİNDEN söyler.**

**"Kendiliğinden" ne demek:** araştırmacı farkı ima etmeden, seçenek
sunmadan, "hangisi daha anlaşılır" diye sormadan. Katılımcı farkı
**kendi cümleleriyle** dile getirmelidir.

**Kabul edilen ifadeler:** teşhis yönteminin varlığına, adım adım
ilerlemeye, "hangisinin benim sorunum olduğunu buldum" duygusuna veya
belirtiden nedene giden yola işaret eden herhangi bir ifade.

**Kabul EDİLMEYEN ifadeler:** "bu daha güzel", "yazısı daha net",
"resimleri daha iyi" — bunlar tasarım tercihidir, mimari fark değil.

### 3.1 · n < 3 olursa ne olur — açıkça tanımlı

Kurucu, üç katılımcı hemen bulunamadı diye projenin durmasını
istemiyor. Bu, ölçütü **değiştirmez**; üçüncü bir sonuç durumu
tanımlar:

| Katılımcı | Sonuç durumu | `measured` | Kapı |
|---|---|---|---|
| 3 · en az 2'si farkı söyledi | **PASS** | `true` | Açılır |
| 3 · en fazla 1'i söyledi | **FAIL** | `true` | **Proje durur** |
| **1 veya 2** | **INCONCLUSIVE** | **`false`** | **Kapalı kalır** |
| 0 | **NOT MEASURED** | `false` | Kapalı kalır |

**`INCONCLUSIVE` bir PASS değildir ve bir FAIL de değildir.** Bulgular
raporlanır, protokol iyileştirilir, işe yarayan her şey (Faz 2 üretimi,
fiziksel sınama, pilot malzemesi) **devam eder** — yalnızca kapı
ilerlemez.

**`measured: false` kalır.** `kill_gate.py` bunu bir engel olarak
raporlamaya devam eder ve **bu doğrudur**.

## 4 · FAIL sonucu — pazarlık yok

> **Farklılaşma hipotezi çürüktür ve proje DURUR.**

FAIL şu anlama gelir: `Complexity(58)` bir kalite açığıdır ama **bizim
çözümümüz o açığı alıcının göreceği biçimde kapatmıyor.**

FAIL sonrası seçenekler (hepsi **kurucu kararı**):
(a) proje durur; (b) mimari yeniden tasarlanır ve test tekrarlanır;
(c) konumlandırma değiştirilir ve seri yeniden gerekçelendirilir.

**Ajan bu seçeneklerden hiçbirini tek başına seçemez.**

---

## 5 · `A14` — KATILIMCI BULMA PROSEDÜRÜ

Bu bölüm Faz 1 yürütmesinde eklendi. Kurucu bunu **bağımsız olarak**
uygulayabilir.

### 5.1 · Eleme ölçütleri — katılımcı kimdir

| Zorunlu | Ölçüt |
|---|---|
| ✔ | Dikiş makinesi kullanabiliyor |
| ✔ | **Dokuma kumaşla** en az **iki** ticari kalıp uygulamış |
| ✔ | En az bir kez sonuçtan memnun kalmamış (uyum nedeniyle) |
| ✔ | Yetişkin kadın giyimi dikiyor |
| ✘ | **Profesyonel terzi/kalıpçı/eğitmen DEĞİL** — hedef okur değil |
| ✘ | Yalnızca örme/esnek kumaş dikmiyor — farklı fizik, kapsam dışı |
| ✘ | Ürünün varlığından haberdar değil |

**Üç soruluk ön eleme (metin/telefon):**
1. "Son bir yılda dokuma kumaştan kaç giysi diktiniz ve kaçında hazır
   kalıp kullandınız?"
2. "Diktiğiniz bir giysinin oturmadığı oldu mu? Ne yaptınız?"
3. "Dikişle geçiminizi sağlıyor musunuz veya dikiş dersi veriyor
   musunuz?" *(evet → elenir)*

### 5.2 · Nereden bulunur — en ucuzdan pahalıya

| # | Kanal | Maliyet | Not |
|---|---|---|---|
| 1 | **Yerel kumaş/dikiş dükkânının ders panosu** | ilan çıktısı | En yüksek isabet: oradakiler tanımı gereği hedef okur |
| 2 | **Halk kütüphanesi / üretim atölyesi dikiş grubu** | 0 | Genellikle düzenli toplanır |
| 3 | Dikiş kursu eğitmeninden **öğrenci** yönlendirmesi | 0 | Eğitmenin kendisi katılımcı OLAMAZ (§ 5.1) |
| 4 | **Çevrimiçi dikiş toplulukları** | 0 | Ön eleme **zorunlu**; görüntülü görüşme ister |
| 5 | Kişisel çevre (ikinci derece tanıdık) | 0 | ⚠ En yüksek **taraf tutma** riski — § 5.4 |

**Hedef: 4 kişi kabul et, 3'ünün geleceğini varsay.**

### 5.3 · Teşvik

Küçük ve nötr: **$15–25 bandında bir kumaş hediye çeki** veya
yayımlandığında kitabın bir nüshası.

⚠ Büyük bir teşvik, katılımcıyı "işe yarar bir şey söyleme" baskısı
altına sokar ve testi bozar. Teşvik, **soru sorulmadan önce ve
koşulsuz** verilir.

### 5.4 · Taraf tutmayı azaltan dört kural

1. Katılımcı, araştırmacının **hangi metni yazdığını bilmez**.
2. Materyaller **markasızdır**; yazar adı, kapak, logo yoktur.
3. Araştırmacı **hiçbir aşamada** "akış şeması", "teşhis", "adım adım"
   gibi hedef kelimeleri **söylemez**.
4. Kişisel çevreden bir katılımcı varsa, oturumu **başka biri**
   yürütür veya o katılımcının verisi ayrı işaretlenir.

### 5.5 · Oturum betiği — araştırmacının söyleyeceği ve söyleMEYECEĞİ

**Söylenir:**
> "Size iki kısa metin vereceğim. İkisi de dikişte uyum konusunda.
> Sırayla okuyun, acele etmeyin. Okurken kendi diktiğiniz bir giyside
> yaşadığınız bir uyum sorununu düşünün ve bu metinlerle onu anlamaya
> çalışın. Bittiğinde birkaç şey soracağım."

**Okuma bitince, tam olarak bu sırayla:**
1. "Bu iki metin arasında fark var mı? Varsa nedir?" ← **ölçüm budur**
2. *(Katılımcı kendiliğinden farkı söylediyse:)* "Biraz daha
   anlatabilir misiniz?"
3. "Kendi sorununuzu bu metinlerden biriyle teşhis edebildiniz mi?"
4. "Değiştirmek isteyeceğiniz bir şey var mı?"
5. *(En son, `A4` için:)* "Bunun internette bir tamamlayıcı sayfası
   olsaydı orada ne bulmak isterdiniz?"

**SÖYLENMEZ:** "hangisi daha anlaşılır" · "hangisi daha kolay" ·
"hangisini tercih ederdiniz" · "akış şeması" · "teşhis" · "adım adım"
· "A metni bizim".

**5. soru neden en sonda:** `A4`'ün girdisidir ve ölçümü kirletmemesi
için fark sorusu **yanıtlandıktan sonra** sorulur
(`MEDIUM_DECISION_FRAMEWORK § 6`).

### 5.6 · Kayıt formu — oturum başına

| Alan | Not |
|---|---|
| Katılımcı kodu (P1/P2/P3) | **Kimlik bilgisi kaydedilmez** |
| Eleme yanıtları | § 5.1'in üç sorusu |
| Sunum sırası | A→B veya B→A |
| **Soru 1'e verilen yanıtın DOĞRUDAN ALINTISI** | **Özetlenmez, düzeltilmez, yumuşatılmaz** |
| Farkı kendiliğinden söyledi mi | `evet` / `hayır` / **`belirsiz`** |
| Soru 2–5 yanıtları | Alıntı |
| Araştırmacı notu | Ayrı alan — yanıtla karıştırılmaz |

**`belirsiz` bir PASS değildir.** Belirsiz bir ifade **belirsiz**
olarak kaydedilir.

## 6 · Pilot karşılaştırma malzemesi — spesifikasyon

Malzemenin kendisi Faz 3'te üretilir; **neyin üretileceği burada
kilitlenir.**

### 6.1 · Malzeme A — bizim kesitimiz

| Ölçüt | Değer |
|---|---|
| Kaynak | Bölüm 11 (Göğüs) — pilot bölüm |
| Kapsam | Bölge anatomisi + bu bölgede okunan ölçüler + **en az 3 belirti girişi** + **tam bölge akış şeması** + "bu bölgede neyi henüz değiştirmeyin" |
| Uzunluk | **6–8 sayfa** — B ile karşılaştırılabilir olmalı |
| Biçim | Nihai sayfa geometrisinde basılmış, **markasız** |
| Görsel | Faz 2'nin gerçek figürleri — taslak/eskiz **kullanılmaz** |
| Yasak | Seri adı, yazar adı, kapak, "Kitap 2'yi alın" ifadesi |

**Neden en az 3 belirti girişi:** tek bir giriş, mimariyi göstermez.
Fark, **girişler arasındaki tekrar eden yapıdadır** — okur ancak
üçüncüde deseni görür.

### 6.2 · Malzeme B — rakip kesiti

| Kural | |
|---|---|
| Konu | **Aynı bölge** (göğüs) — farklı konu karşılaştırmayı geçersiz kılar |
| Uzunluk | A ile ±%20 içinde |
| Edinim | Kitabın **meşru bir nüshasından** (satın alınmış veya kütüphaneden ödünç) |
| Kullanım | **Yalnızca test oturumunda**; çoğaltılmaz, depoya girmez, dağıtılmaz (`IP_AND_BRAND_POLICY § 2`, `.gitignore § ③`) |
| Markasızlaştırma | Kapak, yazar adı, yayıncı, sayfa altı bilgileri kapatılır |
| Kayıt | Rapor, hangi kitabın hangi bölümünün kullanıldığını **iç bilgi olarak** taşır; ürün metnine geçmez |

### 6.3 · Hazırlık kontrol listesi

- [ ] Malzeme A basıldı (Faz 3)
- [ ] Malzeme B'nin meşru nüshası edinildi
- [ ] İkisi de markasızlaştırıldı
- [ ] Sıra planı yazıldı (P1: A→B · P2: B→A · P3: A→B)
- [ ] Kayıt formu × 3 çıktı alındı
- [ ] Betik (§ 5.5) yazıcıdan çıktı olarak yanda duruyor
- [ ] Teşvik hazır

## 7 · AI VEKİL TESTİ SAYILMAZ — sertleştirilmiş kural

> Bir AI ajanının "okur gibi davranarak" bu testi yapması **geçerli bir
> ölçüm DEĞİLDİR.**

`series_config.json → killGates.differentiationTest.aiProxyCountsAsHuman`
= **`false`** ve bu bayrak **açılamaz** — `kill_gate.py` açılmasını ayrı
bir engel olarak yakalar.

**Bu kural neden bu kadar sert:** kardeş Hangıl projesinde Faz 4
kill-gate'i tam olarak bu nedenle **REVISE** ölçtü ve kapı ancak açık
bir **kurucu geçersiz kılmasıyla** ilerledi — ölçüm değiştirilmeden,
geçersiz kılma ayrı bir alan olarak kaydedilerek (`DECISIONS.md K6`).

### 7.1 · Çelişmeli AI incelemesinin İZİNLİ kullanımı

Bir AI incelemesi şunlar için **kullanılabilir ve kullanılmalıdır**:

| İzinli | Örnek |
|---|---|
| **Test öncesi protokol eleştirisi** | "5. soru 1. soruyu kirletir mi?" |
| **Yönlendirici dil taraması** | Betikte hedef kelime kaçağı arama |
| **Başarısızlık senaryosu üretme** | "Bu test hangi biçimde yanlış PASS verebilir?" |
| Malzeme A'nın iç tutarlılık denetimi | Akış şemasında boşta biten yol |

| **YASAK** | |
|---|---|
| Katılımcı yerine geçmek | Sonucu `measured` alanına yazmak |
| "Yapay okur farkı gördü" biçiminde raporlamak | Herhangi bir yerde insan testi gibi sunmak |

Çıktı ayrı bir dosyaya yazılır:
`08_REPORTS/PHASE_3_ADVERSARIAL_REVIEW.md` — fark testi raporuyla
**karıştırılmaz**.

## 8 · Ön koşullar — güncel durum

| # | Ön koşul | Durum |
|---|---|---|
| 1 | Pilot bölüm üretilmiş | ✗ — Faz 3 |
| 2 | Rakip bölümün meşru nüshası edinilmiş | ✗ — Faz 3 |
| 3 | Katılımcılar bulunmuş | ✗ — **`A14` DIŞ BEKLEMEDE**; prosedür § 5'te hazır |
| 4 | Bu protokol yazılı | ✓ |
| 5 | Kayıt formu tanımlı | ✓ — § 5.6 |
| 6 | Oturum betiği yazılı | ✓ — § 5.5 |
| 7 | Malzeme spesifikasyonu kilitli | ✓ — § 6 |

`kill_gate.py` 4. maddeyi mekanik olarak denetler; 1–3 Faz 3'ün işidir.

## 9 · Kayıt ve raporlama

Sonuç `08_REPORTS/PHASE_3_DIFFERENTIATION_TEST.md`'ye yazılır ve
şunları **tam olarak** içerir: katılımcı profilleri (kimlik olmadan) ·
sunum sırası · **doğrudan alıntılar** · kaç katılımcının farkı
kendiliğinden söylediği · PASS / FAIL / INCONCLUSIVE kararı ·
kararın `series_config.json`'a işlenmesi.

**Sert kural:** katılımcı ifadeleri yeniden yazılmaz, yumuşatılmaz,
lehte yorumlanmaz.

## 10 · Bu testin ölçMEDİĞİ şey

Bu test yalnızca **algılanan mimari farkı** ölçer. Şunları ölçmez:
teknik doğruluk (→ `VALIDATION_PROTOCOL.md`) · satın alma niyeti
(→ `ADS_FRAMEWORK.md`) · kitabın tamamının kullanılabilirliği
(→ Faz 5 KA) · ürünün ticari başarısı.

Bu sınırların bulanıklaştırılması, kapının erozyona uğramasının en
olası yoludur (`RISK_REGISTER R-14`).

---

*Vâliçe Press · TRUE FIT 1 · Differentiation Test · 28 Ağustos 2026 (Faz 1 yürütmesi)*
