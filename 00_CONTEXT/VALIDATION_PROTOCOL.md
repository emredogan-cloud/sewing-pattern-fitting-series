# VALIDATION PROTOCOL — fiziksel doğrulama sistemi

> Görev talimatı § 26. Araştırma raporu § 28 bu pazarın en güçlü
> yanlarından birini şöyle kaydetti: **uzman kapısı YOK ve doğrulama
> FİZİKSEL — kalıbı uygula, giysiyi dik, oturuyor mu bak.**
>
> Bunun bedeli şudur: **doğrulama bizim üzerimizdedir.**

---

## 1 · Kapsam

Bu protokol üç şeyi doğrular:

| Ne | Neden |
|---|---|
| **Ölçü tanımları** (`M-xxx`) | Yanlış tanımlanmış bir ölçü, aşağı akıştaki her teşhisi bozar |
| **Belirti→neden bağları** (`SYM-xxx`) | Ayırt edici kanıt gerçekten ayırt ediyor mu |
| **Düzeltme diyagramları** (`FIG-xxx`) | Geometrik olarak yanlış bir diyagram okurun kumaşını mahveder |

## 2 · Üç toile türü — karıştırılmaz

`SERIES_CONTENT_ARCHITECTURE.md`'de üç ayrı topik olmalarının nedeni:

| Tür | Kitap | Amaç | Ayırt edici özelliği |
|---|---|---|---|
| **Teşhis toile'i** (`TOP-07`) | 1 | Belirtiyi görünür kılmak | Hızlı, işaretli (denge çizgileri, ön/arka orta, apeks), **düzeltilmemiş** |
| **Doğrulama toile'i** (`TOP-26`) | 2 | Düzeltmenin işe yaradığını göstermek | Düzeltilmiş kalıptan; öncesiyle KARŞILAŞTIRILIR |
| **Blok sınama toile'i** (`TOP-27`) | 3 | Bloğun bedene oturduğunu göstermek | Referans yalnızca bedenin kendisi; ticari kalıp YOK |

## 3 · Standart koşullar — ölçüm koşulu ölçümün parçasıdır

Bir provanın koşulları kaydedilmemişse **o prova bir kanıt değildir**.
Her `VAL-xxxx` kaydı şunları taşır:

1. **Kumaş** — cinsi, gramajı, yıkanmış mı, dokuma yönü
2. **İç giyim** — hangi sutyen/iç çamaşırı (göğüs teşhisinde belirleyici)
3. **Duruş** — ayakta, ağırlık iki ayağa eşit, kollar yanda
4. **Dikiş payı** — kalıbın varsaydığı payla mı dikildi
5. **İşaretleme** — denge çizgileri, ön/arka orta, apeks işaretli mi
6. **Gözlemci** — kim baktı, aynayla mı, fotoğrafla mı
7. **Hareket testi** — kol öne, kol yukarı, oturma, adım atma

Bu liste Kitap 1 Bölüm 5'in (prova protokolü) doğrudan kaynağıdır.

## 4 · Diyagram doğrulama döngüsü

```
FİGÜR KAYDI (FIG-xxx)
      ↓
KALIBA UYGULA — diyagram tam olarak ne diyorsa
      ↓
TOILE DİK
      ↓
ÖLÇ — beklenen değişim gerçekleşti mi (sayıyla)
      ↓
GÖZLE — hedef belirti kayboldu mu
      ↓
YAN ETKİ TARA — YENİ bir belirti doğdu mu
      ↓
KAYDET → VAL-xxxx
```

**Kritik adım "yan etki tarama"dır.** Bir düzeltme hedef belirtiyi
çözüp başka bir yerde yenisini yaratabilir; bu, düzeltme etkileşim
haritasının (`AF-xx.interacts_with`) fiziksel karşılığıdır.

## 5 · `VAL-xxxx` kaydı — ne saklanır, ne saklanmaz

**Saklanır (public):** koşullar, ölçüm sayıları (öncesi/sonrası),
gözlem notu, sonuç (`PASS`/`FAIL`), hangi figüre/kayda ait, tarih.

**SAKLANMAZ (depoya girmez):** prova fotoğrafları. Bir toile fotoğrafı
gerçek bir insanın vücut görüntüsüdür.

Mekanik koruma: `.gitignore § ②` ve
`validate_structure.py § check_photo_leak`. Fotoğraflar depo dışında,
kurucunun yerel arşivinde tutulur; `VAL-xxxx` kaydı yalnızca
**referans** taşır.

## 6 · Hata oranı ve eşikler

```
hata oranı = (beklenen sonucu ÜRETMEYEN figür sayısı) / (test edilen figür sayısı)
```

| Sonuç | Karar |
|---|---|
| %0 | Pilot geçer |
| > %0 | Pilot durur; her hata **kök nedenden** düzeltilir (tek figür yamanmaz) |
| > %5 | **Üretim yöntemi reddedilir** — proje durur (araştırma raporu § 32 terk koşulu) |

## 7 · Kim yapar — dürüst kayıt

Fiziksel doğrulamayı **kurucu** yapar (kaynak: kurucu kararı, dış uzman
işe alınmayacak — `DECISIONS.md K6`). Bu bir sınırdır ve şöyle
kaydedilir:

> Doğrulayan kişi ürünün sahibidir. Bu, bağımsız bir doğrulama
> **değildir** ve hiçbir yerde öyle sunulamaz. Değeri, hatanın
> yayımlanmadan önce yakalanmasıdır — bağımsızlık iddiası değil.

Kapsam sınırı: doğrulama **tek bir vücut** üzerinde yapılır. Bir
düzeltmenin farklı vücutlarda da doğru çalıştığı bu protokolle
kanıtlanamaz — bu, ürünün bilinen ve `RISK_REGISTER R-06`'da izlenen
sınırıdır.

---

*Vâliçe Press · TRUE FIT · Validation Protocol · 28 Ağustos 2026*
