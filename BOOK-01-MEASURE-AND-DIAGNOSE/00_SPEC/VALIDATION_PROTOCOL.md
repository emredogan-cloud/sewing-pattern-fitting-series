# BOOK-01-VALIDATION-PROTOCOL

> Faz 1 çıktısı 8/10. Görev talimatı § 26, § 36.11.
> Seri protokolü: [`../../00_CONTEXT/VALIDATION_PROTOCOL.md`](../../00_CONTEXT/VALIDATION_PROTOCOL.md)
>
> Bu belge Kitap 1'in **hangi iddialarının fiziksel olarak sınanması
> gerektiğini** ve nasıl sınanacağını tanımlar.
>
> ⚠ **Hiçbir doğrulama henüz yapılMADI.** `VAL-xxxx` kayıt sayısı: **0**.

---

## 1 · Neden Kitap 1 için fiziksel doğrulama zorunlu

Araştırma raporu § 28: bu pazarın en güçlü yanlarından biri **uzman
kapısının olmaması ve doğrulamanın fiziksel olmasıdır**. Bunun bedeli
şudur: doğrulama bizim üzerimizdedir.

Kitap 1 bir düzeltme diyagramı vermez — ama **bir teşhis verir.**
Yanlış bir teşhis, okurun yanlış düzeltmeyi yapmasına ve kumaşını
mahvetmesine yol açar. Kitap 1'in hatası Kitap 2'nin hatası kadar
pahalıdır; yalnızca bir adım daha erken meydana gelir.

## 2 · Neyin doğrulanması ZORUNLU, neyin değil

| İddia sınıfı | Fiziksel doğrulama | Gerekçe |
|---|---|---|
| **C-C** Ayırt edici kanıt (129) | **ZORUNLU** | "Bu kanıt bu iki nedeni gerçekten ayırıyor mu" ancak deneyle bilinir |
| **C-D** Ölçüm–hipotez ilişkisi (129) | **ZORUNLU** | Ölçümün hipotezi gerçekten doğrulayıp doğrulamadığı |
| **C-H** Eleme kalemi (9) | **ZORUNLU** | Kalıp dışı bir nedenin gerçekten aynı belirtiyi ürettiği |
| **C-F** Sıra kısıtı (5 kural) | **ZORUNLU** | Yanlış sıranın gerçekten yeni belirti ürettiği |
| **C-B** Belirti–neden bağı (129) | Kısmi (örneklem) | Tümü tek vücutta üretilemez |
| **C-A** Ölçü tanımı (32) | **Hayır** | Bir tanım deneyle doğrulanamaz — kaynak işi |
| **C-G** Ease konvansiyonu | **Hayır** | Sektör konvansiyonu — kaynak işi |

## 3 · Doğrulama yöntemleri

### Y-1 · Belirti üretme testi *(C-B, C-C için)*

Bir belirtiyi **kasten üretmek** ve kitabın onu doğru teşhis edip
etmediğini görmek.

```
BİLİNEN BİR SAPMA UYGULA        (ör. omuz dikişini kasten 1 cm alçalt)
      ↓
TOILE DİK
      ↓
KİTABIN YÖNTEMİNİ UYGULA        yedi adım, kitaba bakarak
      ↓
KARŞILAŞTIR                     kitap uyguladığım sapmayı buldu mu
```

**PASS:** kitabın vardığı düzeltme ailesi, uygulanan sapmayla eşleşir.
**FAIL:** eşleşmezse ya belirti kaydı ya ayırt edici kanıt yanlıştır.

Bu, Kitap 1'in **en güçlü doğrulama yöntemidir**: doğru cevap önceden
bilinir.

### Y-2 · Ayırt edicilik testi *(C-C için)*

Aynı belirtiyi **iki farklı nedenden** üret ve ayırt edici kanıtın
ikisini gerçekten ayırıp ayırmadığına bak.

Örnek: `SYM-004` (boyun noktasından koltuk altına çapraz çekme) hem dik
omuz hem dar omuz genişliğinden doğabilir. İkisi ayrı ayrı üretilir;
kanıt ("omuz ucunda kumaş gergin mi toplanıyor mu") ikisini ayırıyor mu.

**PASS:** kanıt iki durumda **farklı** sonuç veriyor.
**FAIL:** aynı sonuç veriyorsa kanıt ayırt edici DEĞİLDİR ve kayıt
düzeltilmelidir.

### Y-3 · Ölçüm tekrarlanabilirliği *(C-A destek)*

Aynı ölçü, aynı kişide, farklı zamanlarda, farklı kişilerce alınır;
sapma ölçülür. Çıktı: Bölüm 2'nin "kabul edilebilir sapma" eşiği —
şu anda **belirlenmemiş**, ampirik olarak bulunacak.

### Y-4 · Eleme kalemi testi *(C-H için)*

Dokuz eleme kaleminin her biri **kasten** uygulanır (eğri kesim, yanlış
dikiş payı, yanlış iç giyim, yanlış ölçekte basılmış kalıp…) ve ürettiği
belirti kaydedilir. Bölüm 8'in doğrudan kanıt tabanıdır.

### Y-5 · Sıra kısıtı testi *(C-F için)*

İki düzeltme **yanlış sırada** uygulanır; ikincinin birinciyi bozup
bozmadığı ölçülür. Beş sıra kuralının her biri için ayrı test.

## 4 · Faz 3 pilot doğrulama planı

Pilot, **bir tam bölge bölümüdür** (Bölüm 11 · Göğüs önerilir).

**Neden Bölüm 11:** hedef okurun en sık karşılaştığı bölge; en çok
yanlış teşhis edilen bölge (göğüs kaynaklı belirtiler yaka, kol
oyuntusu ve etek ucunda görünür); ve rakiplerin en çok yazdığı konu —
fark testi için en anlamlı karşılaştırma zemini.

| # | Test | Yöntem | Kapsam |
|---|---|---|---|
| 1 | Belirti üretme | Y-1 | Bölüm 11'in 6 belirtisinin en az 4'ü |
| 2 | Ayırt edicilik | Y-2 | En az 3 belirtinin çoklu nedenleri |
| 3 | Eleme kalemi | Y-4 | 9 kalemin tamamı |
| 4 | Sıra kısıtı | Y-5 | Göğüs–omuz ve göğüs–kol oyuntusu etkileşimleri |
| 5 | Ölçüm tekrarı | Y-3 | Bölüm 11'in 7 ölçüsü |

**Kill-gate eşiği:** hata oranı **%0**. Bir tek yanlış teşhis bile
pilotu durdurur ve kök nedenden düzeltilir. **>%5 → üretim yöntemi
reddedilir, proje durur.**

## 5 · `VAL-xxxx` kaydı — Kitap 1 alanları

Seri protokolünün yedi standart koşuluna ek olarak Kitap 1 kayıtları
şunları taşır:

| Alan | Neden |
|---|---|
| `induced_deviation` | Y-1'de kasten uygulanan sapma ve miktarı |
| `book_diagnosis` | Kitabın vardığı `AF-xx` + miktar |
| `match` | Eşleşti mi (`true`/`false`) |
| `discriminating_evidence_worked` | Y-2 sonucu |
| `new_signs_appeared` | Yan etki taraması sonucu |

## 6 · Kapsam sınırı — dürüst kayıt

| Sınır | Sonucu |
|---|---|
| Doğrulama **tek bir vücut** üzerinde yapılır | Bir teşhisin farklı vücutlarda da doğru çalıştığı **kanıtlanamaz** |
| Doğrulamayı **ürünün sahibi** yapar | Bu **bağımsız bir doğrulama değildir** ve hiçbir yerde öyle sunulamaz |
| Örneklem: 129 bağın tümü değil | Örneklem seçimi ve kapsam oranı kayda geçirilir |

Bu sınırlar `RISK_REGISTER R-06`'da izlenir ve ürün metninde gizlenmez.

## 7 · Kim, ne zaman, hangi kaynakla

| Soru | Durum |
|---|---|
| Kim doğrular | Kurucu (`DECISIONS.md K6` — dış uzman işe alınmayacak) |
| Kaç toile | **KARAR VERİLMEDİ** — `../../OPEN_QUESTIONS.md → A13` |
| Hangi vücut(lar) | **KARAR VERİLMEDİ** — `A13` |
| Ne zaman | Faz 3 (`phase3-pilot`), Faz 2 tamamlandıktan sonra |
| Ön koşul | Bu belge + `DIFFERENTIATION_TEST.md` yazılı olmalı (`kill_gate.py` denetler) |

---

*Vâliçe Press · TRUE FIT 1 · Validation Protocol · 28 Ağustos 2026*
