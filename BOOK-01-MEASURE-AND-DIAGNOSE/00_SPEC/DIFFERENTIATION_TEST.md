# BOOK-01-DIFFERENTIATION-TEST — **KİLL-GATE PROTOKOLÜ**

> Faz 1 çıktısı 9/10. Görev talimatı § 36.12.
> Kaynak: araştırma raporu § 35 madde 1 — **KİLİT KAPI**.
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
| **Katılımcı** | **Üç gerçek ev dikişçisi** — hedef okur profiline uyan (dikmeyi bilen, orta seviye, dokuma kumaşla giysi diken) |
| **Malzeme A** | Kitap 1'in pilot bölümünden **tek bir teşhis bölümü** (tam akış şemasıyla) |
| **Malzeme B** | Kategori liderinin **aynı konudaki** bölümü |
| **Sunum** | Yan yana, **markasız** (kapak, logo, yazar adı görünmez) |
| **Sıra** | Katılımcılar arasında **değiştirilir** (sıra etkisi kontrolü) |
| **Görev** | Okuyun ve kendi giysinizdeki bir uyum sorununu teşhis etmeye çalışın |
| **Soru** | Yönlendirmesiz açık uçlu: *"Bu iki metin arasında fark var mı? Varsa nedir?"* |

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

## 4 · FAIL sonucu — pazarlık yok

> **Farklılaşma hipotezi çürüktür ve proje DURUR.**

Bu, araştırma raporunun § 32'de yazdığı terk koşuludur. FAIL şu anlama
gelir: `Complexity(58)` bir kalite açığıdır ama **bizim çözümümüz o
açığı alıcının göreceği biçimde kapatmıyor.**

FAIL sonrası seçenekler (hepsi **kurucu kararı**):
(a) proje durur; (b) mimari yeniden tasarlanır ve test tekrarlanır;
(c) konumlandırma değiştirilir ve seri yeniden gerekçelendirilir.

**Ajan bu seçeneklerden hiçbirini tek başına seçemez.**

## 5 · AI VEKİL TESTİ SAYILMAZ — sertleştirilmiş kural

> Bir AI ajanının "okur gibi davranarak" bu testi yapması **geçerli bir
> ölçüm DEĞİLDİR.**

`series_config.json → killGates.differentiationTest.aiProxyCountsAsHuman`
= **`false`** ve bu bayrak **açılamaz** — `kill_gate.py` açılmasını ayrı
bir engel olarak yakalar.

**Bu kural neden bu kadar sert:** kardeş Hangıl projesinde Faz 4
kill-gate'i tam olarak bu nedenle **REVISE** ölçtü (vekil AI testi insan
testi yerine sayılmadı) ve kapı ancak açık bir **kurucu geçersiz
kılmasıyla** ilerledi — ölçüm değiştirilmeden, geçersiz kılma ayrı bir
alan olarak kaydedilerek (`DECISIONS.md K6`, Hangıl K20 dersi).

Bir vekil test **yapılabilir** ve bulguları değerlidir; ama sonucu
`differentiationTest.measured` alanına **yazılamaz** ve raporda
"insan testi" olarak **sunulamaz**.

## 6 · Ön koşullar — test başlamadan önce hazır olmalı

| # | Ön koşul | Durum |
|---|---|---|
| 1 | Pilot bölüm üretilmiş (Faz 3 çıktısı) | ✗ |
| 2 | Rakip bölümün karşılaştırılabilir bir kopyası edinilmiş (**yalnızca test için, çoğaltılmaz** — `IP_AND_BRAND_POLICY.md § 2`) | ✗ |
| 3 | Üç katılımcı bulunmuş | ✗ — `../../OPEN_QUESTIONS.md → A14` |
| 4 | Bu protokol yazılı | ✓ |
| 5 | Kayıt formu hazır | Faz 3'te |

`kill_gate.py` 4. maddeyi mekanik olarak denetler; 1–3 Faz 3'ün işidir.

## 7 · Kayıt ve raporlama

Test sonucu `08_REPORTS/PHASE_3_DIFFERENTIATION_TEST.md`'ye yazılır ve
şunları **tam olarak** içerir:

- Katılımcı profilleri (kimlik bilgisi olmadan)
- Sunum sırası ve hangi katılımcıya hangi sırayla verildiği
- **Katılımcı ifadelerinin doğrudan alıntısı** — özetlenmiş değil
- Kaç katılımcının farkı kendiliğinden söylediği
- PASS / FAIL kararı
- Kararın `series_config.json`'a işlenmesi

**Sert kural:** katılımcı ifadeleri yeniden yazılmaz, yumuşatılmaz,
lehte yorumlanmaz. Belirsiz bir ifade **belirsiz** olarak kaydedilir ve
PASS sayılmaz.

## 8 · Bu testin ölçMEDİĞİ şey

Bu test yalnızca **algılanan mimari farkı** ölçer. Şunları ölçmez:

- teknik doğruluk (→ `VALIDATION_PROTOCOL.md`)
- satın alma niyeti (→ reklam testi, `A12`)
- kitabın tamamının kullanılabilirliği (→ Faz 5 KA)
- ürünün ticari başarısı

Bu sınırların bulanıklaştırılması, kapının erozyona uğramasının en
olası yoludur (`RISK_REGISTER R-14`).

---

*Vâliçe Press · TRUE FIT 1 · Differentiation Test · 28 Ağustos 2026*
