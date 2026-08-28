# BOOK-01-VALIDATION-PROTOCOL

> Faz 1 çıktısı 8/10. Görev talimatı § 26, § 36.11.
> Seri protokolü: [`../../00_CONTEXT/VALIDATION_PROTOCOL.md`](../../00_CONTEXT/VALIDATION_PROTOCOL.md)
>
> `OPEN_QUESTIONS A13` — **kapsam Faz 1 yürütmesinde KARARA BAĞLANDI**
> (`DECISIONS.md K29`).
>
> ⚠ **Hiçbir doğrulama henüz YAPILMADI.** `VAL-xxxx` kayıt sayısı: **0**.
> Bu belge planın kendisidir; sonucun değil.

---

## 1 · Neden Kitap 1 için fiziksel sınama zorunlu

Araştırma raporu § 28: bu pazarın en güçlü yanlarından biri **uzman
kapısının olmaması ve sınamanın fiziksel olmasıdır**. Bunun bedeli
şudur: sınama bizim üzerimizdedir.

Kitap 1 bir düzeltme diyagramı vermez — ama **bir teşhis verir.**
Yanlış bir teşhis, okurun yanlış düzeltmeyi yapmasına ve kumaşını
mahvetmesine yol açar. Kitap 1'in hatası Kitap 2'nin hatası kadar
pahalıdır; yalnızca bir adım daha erken meydana gelir.

**Faz 1 yürütmesinde bu gerekçe güçlendi:** kamu kaynağı taraması,
belirti kayıtlarının çekirdek iddiasını (`C-C` ayırt edici kanıt)
**hiçbir kamu kaynağının doğrulamadığını** gösterdi
(`SOURCE_MAP.md § 6`). Fiziksel sınama, o boşluğun **tek** doldurma
yoludur — ikinci bir seçenek yoktur.

## 2 · Neyin sınanması ZORUNLU, neyin değil

| İddia sınıfı | Fiziksel sınama | Gerekçe | Faz 1 sonrası durum |
|---|---|---|---|
| **C-C** Ayırt edici kanıt (129) | **ZORUNLU** | "Bu kanıt bu iki nedeni gerçekten ayırıyor mu" ancak deneyle bilinir | Kaynak yok → **tek yol bu** |
| **C-D** Ölçüm–hipotez ilişkisi (129) | **ZORUNLU** | Ölçümün hipotezi gerçekten doğrulayıp doğrulamadığı | Aynı |
| **C-H** Eleme kalemi (9) | **ZORUNLU** | Kalıp dışı bir nedenin gerçekten aynı belirtiyi ürettiği | Aynı |
| **C-F** Sıra kısıtı (5 kural) | **ZORUNLU** | Yanlış sıranın gerçekten yeni belirti ürettiği | **2/5 kaynakla desteklendi** (`S-0003`) → sınama yükü hafifledi ama kalktı sayılmaz |
| **C-B** Belirti–neden bağı (129) | Kısmi (örneklem) | Tümü tek vücutta üretilemez | Değişmedi |
| **C-A** Ölçü tanımı (32) | **Hayır** | Bir tanım deneyle doğrulanamaz — kaynak işi | **16'sı kaynakla kapandı** |
| **C-G** Ease konvansiyonu | **Hayır** | Sektör konvansiyonu — kaynak işi | `S-0001` ile yazılabilir hâle geldi |

## 3 · Sınama yöntemleri

### Y-1 · Belirti üretme testi *(C-B, C-C için)* — en güçlü yöntem

Bir belirtiyi **kasten üretmek** ve kitabın onu doğru teşhis edip
etmediğini görmek.

```
BİLİNEN BİR SAPMA UYGULA        (ör. omuz dikişini kasten 1 cm alçalt)
      ↓
TOILE'İ O SAPMAYLA DİK / DEĞİŞTİR
      ↓
KİTABIN YÖNTEMİNİ UYGULA        yedi adım, kitaba bakarak
      ↓
KARŞILAŞTIR                     kitap uyguladığım sapmayı buldu mu
```

**PASS:** kitabın vardığı düzeltme ailesi, uygulanan sapmayla eşleşir.
**FAIL:** eşleşmezse ya belirti kaydı ya ayırt edici kanıt yanlıştır.

**Neden en güçlü:** doğru cevap **önceden bilinir**. Değerlendirme
yorum değil, karşılaştırmadır.

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

Aynı ölçü, aynı kişide, farklı zamanlarda alınır; sapma ölçülür.
Yöntem dayanağı: `S-0006` (NHANES) tekrar-ölçüm (replicate) deseni.

Çıktı: Bölüm 2'nin "kabul edilebilir sapma" eşiği — şu anda
**belirlenmemiş**, ampirik olarak bulunacak.

### Y-4 · Eleme kalemi testi *(C-H için)*

Dokuz eleme kaleminin her biri **kasten** uygulanır (eğri kesim, yanlış
dikiş payı, yanlış iç giyim, yanlış ölçekte basılmış kalıp…) ve ürettiği
belirti kaydedilir. Bölüm 8'in doğrudan kanıt tabanıdır.

### Y-5 · Sıra kısıtı testi *(C-F için)*

İki düzeltme **yanlış sırada** uygulanır; ikincinin birinciyi bozup
bozmadığı ölçülür.

---

## 4 · `A13` KARARI — ASGARİ UYGULANABİLİR SINAMA SETİ

Kurucu, ajana **en basit uygulanabilir ve düşük maliyetli** tasarımı
seçme yetkisi verdi. Seçilen tasarım:

### 4.1 · Temel fikir — sapmayı ARA değil, ÜRET

Örneklem çeşitliliğini artırmanın pahalı yolu **çok sayıda vücut
bulmaktır.** Ucuz yolu şudur:

> Bir sapmayı **taşıyan** bir vücut aramak yerine, **bilinen** bir
> sapmayı tek bir vücutta **üret**.

`Y-1` bunu yapar. Sonuç: **tek bir vücutla onlarca farklı sapma
sınanabilir** — çünkü sınanan şey vücut değil, **yöntemin sapmayı
bulup bulmadığıdır**.

⚠ **Bunun sınırı da açıktır:** bu tasarım *yöntemin* doğruluğunu
sınar, *bir düzeltmenin farklı vücutlarda çalıştığını* **kanıtlamaz**.
O sınır `RISK_REGISTER R-06`'da izlenmeye devam eder ve **azalmadı**.

### 4.2 · Kaç prova giysisi — üç parça, iki adet toile

| ID | Ne | Neden | Tahmini kumaş |
|---|---|---|---|
| **T-1** | Temel beden (bodice) toile'i — dokuma prova kumaşı, işaretli (denge çizgileri, ön/arka orta, apeks, bel) | Bütün `Y-1`/`Y-2` sapmaları bunun üzerinde **geri dönülebilir** biçimde üretilir | ~1,5 m |
| **T-1c** | **Kontrol** — T-1'in değiştirilmemiş ikizi | Kontrol olmadan, üretilen belirti ile zaten var olan belirti ayırt edilemez. **Bu setin en önemli kalemi budur.** | ~1,5 m |
| **P-1…P-3** | Üç yedek ön parça (eğri kesilmiş · yanlış dikiş payıyla dikilmiş · yanlış ölçekte basılmış kalıptan kesilmiş) | Üç eleme kalemi geri dönülemez; ayrı parça ister | ~1 m |

**Toplam: iki toile + üç parça, ≈ 4 m prova kumaşı.**
Malzeme maliyeti bandı: **≈ $15–30** `ESTIMATE`.

### 4.3 · Geri dönülebilir sapma üretimi — maliyeti düşüren asıl teknik

Sapmaların çoğu **kalıbı değiştirmeden ve yeni toile dikmeden**
üretilebilir:

| Sapma | Nasıl üretilir | Geri alınabilir mi |
|---|---|---|
| Omuz eğimi | Omuz dikişini sök, 1 cm alçak dik | ✔ sökülür |
| Omuz genişliği | Omuz dikişini içeri al | ✔ |
| Göğüs hacmi fazlası/eksiği | Şerit kumaş ekle / pens al | ✔ |
| Sırt genişliği | Dikey pili iğnele | ✔ |
| Gövde boyu | Bel hizasında yatay pili iğnele | ✔ |
| Ön/arka denge | Omuz dikişini önden/arkadan farklı al | ✔ |
| Eğri kesim · yanlış pay · yanlış ölçek | **Yeni parça gerekir** | ✘ → `P-1…P-3` |

Bu tablo, "kaç toile" sorusunun cevabını **20'den 2'ye** indiren şeydir.

### 4.4 · Hangi vücut

**Tek vücut: kurucu.** Dış uzman işe alınmayacaktır (`DECISIONS.md K6`)
ve bu protokol bunu değiştirmez.

Kayda geçirilen sonuç: bu **bağımsız bir sınama DEĞİLDİR** ve hiçbir
yerde öyle sunulamaz. Değeri, hatanın yayımlanmadan önce yakalanmasıdır.

### 4.5 · Asgari set — Faz 3 pilotu için (Bölüm 11 · Göğüs)

Pilot bölüm gerekçesi: hedef okurun en sık karşılaştığı bölge; en çok
yanlış teşhis edilen bölge (göğüs kaynaklı belirtiler yakada, kol
oyuntusunda ve etek ucunda görünür); rakiplerin en çok yazdığı konu.

| Kayıt | Yöntem | Kapsam | Adet |
|---|---|---|---|
| `VAL-0001` – `VAL-0004` | **Y-1** belirti üretme | Bölüm 11'in 6 belirtisinden **en az 4'ü** | 4 |
| `VAL-0005` – `VAL-0007` | **Y-2** ayırt edicilik | Çok nedenli **en az 3** belirti | 3 |
| `VAL-0008` – `VAL-0016` | **Y-4** eleme kalemi | **9 kalemin tamamı** | 9 |
| `VAL-0017` – `VAL-0018` | **Y-5** sıra kısıtı | Göğüs–omuz ve göğüs–kol oyuntusu etkileşimi | 2 |
| `VAL-0019` | **Y-3** ölçüm tekrarı | Bölüm 11'in 7 ölçüsü × 3 tekrar | 1 |
| | | **TOPLAM** | **19 kayıt** |

**Tahmini süre:** temel toile ≈ 3 sa · her `Y-1`/`Y-2` çalışması
30–45 dk · eleme kalemleri çoğunlukla 15 dk · toplam **≈ 20–25 saat**
`ESTIMATE`.

**Bu, bir araştırma çalışması değildir.** Bir hafta sonu ile bir hafta
arasında bitirilebilecek, ama büyük teknik hataları yakalayabilecek en
küçük settir.

### 4.6 · Bir toile birden çok kaydı NE ZAMAN doğrulayabilir

`T-1` üzerinde ardışık sapmalar sınanabilir — **iki koşulla**:

1. Her sapmadan sonra toile **kontrol durumuna geri döndürülür** ve
   `T-1c` ile karşılaştırılarak geri döndüğü **doğrulanır**.
2. İki sapma **aynı anda** uygulanmaz — tek değişken kuralı
   (`DIAGNOSTIC_SYSTEM § 3` adım ⑥), sınama tarafında da geçerlidir.

Koşullardan biri sağlanmazsa **yeni toile dikilir**. Bu, maliyetten
tasarrufun kaliteyi yemesini engelleyen kuraldır.

### 4.7 · Faz 5'e ERTELENEN

| Ne | Neden ertelendi |
|---|---|
| Pantolon toile'i (`T-2`) ve `crotch_leg` bölgesi | Pilot bölüm göğüstür; pantolon sınaması tam kitap KA'sına aittir |
| Kalan 5 bölgenin `Y-1` sınaması | Aynı |
| 129 bağın tamamı | Örneklem tasarımı gereği; kapsam oranı kayda geçirilir |

---

## 5 · `VAL-xxxx` kaydı — Kitap 1 alanları

Seri protokolünün yedi standart koşuluna (kumaş · iç giyim · duruş ·
dikiş payı · işaretleme · gözlemci · hareket testi) ek olarak:

| Alan | Neden |
|---|---|
| `induced_deviation` | `Y-1`'de kasten uygulanan sapma ve **miktarı** |
| `book_diagnosis` | Kitabın vardığı `AF-xx` + miktar |
| `match` | Eşleşti mi (`true`/`false`) |
| `discriminating_evidence_worked` | `Y-2` sonucu |
| `new_signs_appeared` | Yan etki taraması sonucu |
| `reverted_and_verified` | § 4.6 koşulu 1 sağlandı mı |

**Fotoğraf depoya GİRMEZ.** Bir prova fotoğrafı gerçek bir insanın
vücut görüntüsüdür (`CONTENT_PROTECTION.md § 2`; mekanik:
`validate_structure.py § check_photo_leak`). Kayıt yalnızca sayıları,
koşulları ve sonucu taşır.

## 6 · Hata oranı ve eşikler — değişmedi

```
hata oranı = (beklenen sonucu ÜRETMEYEN sınama sayısı) / (yapılan sınama sayısı)
```

| Sonuç | Karar |
|---|---|
| **%0** | Pilot geçer |
| **> %0** | Pilot durur; her hata **kök nedenden** düzeltilir (tek kayıt yamanmaz) |
| **> %5** | **Üretim yöntemi reddedilir** — proje durur |

19 kayıtlık sette **tek bir FAIL**, hata oranını %5,3 yapar — yani
**üretim yöntemi reddi eşiğinin üstüne**. Bu, setin küçüklüğünün
bilinçli bir sonucudur: küçük set, tek hatayı bile ciddiye almayı
zorunlu kılar.

⚠ Bu aritmetik, eşiği kolayca tetiklenebilir hâle getirir. **Eşik
gevşetilmez.** Bir FAIL çıkarsa doğru tepki, eşiği değiştirmek değil,
kök nedeni düzeltip **seti yeniden koşmaktır**.

## 7 · Kapsam sınırı — dürüst kayıt

| Sınır | Sonucu |
|---|---|
| Sınama **tek bir vücut** üzerinde yapılır | Bir teşhisin farklı vücutlarda da doğru çalıştığı **kanıtlanamaz** |
| Sınamayı **ürünün sahibi** yapar | Bu **bağımsız bir sınama değildir** ve hiçbir yerde öyle sunulamaz |
| Örneklem: 129 bağın tümü değil | Örneklem seçimi ve kapsam oranı kayda geçirilir |
| Üretilen sapma ≠ doğal sapma | Kasten üretilmiş bir sapma, o sapmayı doğal olarak taşıyan bir vücudun **tam eşdeğeri değildir** |

Son satır `A13` kararının **yeni** sınırıdır ve `RISK_REGISTER R-06`'ya
eklendi.

## 8 · Kim, ne zaman, hangi kaynakla

| Soru | Durum |
|---|---|
| Kim | Kurucu (`DECISIONS.md K6`) |
| Kaç toile | **2 toile + 3 yedek parça** — `A13` KAPANDI |
| Hangi vücut | **Tek vücut: kurucu** — `A13` KAPANDI |
| Kaç kayıt | **19** (`VAL-0001` – `VAL-0019`) |
| Ne zaman | Faz 3 (`phase3-pilot`), Faz 2 tamamlandıktan sonra |
| Ön koşul | Bu belge + `DIFFERENTIATION_TEST.md` yazılı olmalı (`kill_gate.py` denetler) ✓ |
| Malzeme | ≈ 4 m prova kumaşı + kurucunun bedenine uygun bir ticari beden kalıbı |

---

*Vâliçe Press · TRUE FIT 1 · Validation Protocol · 28 Ağustos 2026 (Faz 1 yürütmesi)*
