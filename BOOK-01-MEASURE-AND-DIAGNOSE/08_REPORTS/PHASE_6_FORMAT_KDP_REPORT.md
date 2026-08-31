# FAZ 6 — BİÇİM VE KDP DOĞRULAMA RAPORU (Kitap 1)

**Tarih:** 31 Ağustos 2026 · **git:** `f18e89d` · **dal:** `faz/4-production`

Faz 6, içerik turu KAPANDIKTAN sonra açıldı (kurucunun sırası:
"Phase 6 must remain CLOSED until CONTENT PASS = COMPLETE").

---

## 1 · Yayın varlığının ölçülen özellikleri

`06_BUILD/qa_format.py` — bütün sayılar DOSYADAN okunur:

| Ölçüt | Değer | KDP kaydı | Durum |
|---|---|---|---|
| Kesim | 8,5 × 11,0 in | 8,5 × 11,0 | ✅ |
| Sayfa | **257** | 24–828 | ✅ |
| Cilt payı | 0,875 in | 0,5 in asgari (151–300 bandı) | ✅ |
| Dış kenar | 0,625 in | 0,25 in asgari (taşmasız) | ✅ |
| Üst / alt | 0,75 in | 0,25 in asgari | ✅ |
| Taşma | YOK, beyanla uyumlu | — | ✅ |
| Yazı tipi | 6 / 6 **gömülü** | tamamı gömülü olmalı | ✅ |
| PDF sürümü | 1.3 | 1.3–1.7 | ✅ |
| Dosya | 0,72 MB | 650 MB sınırı | ✅ |
| Künye | başlık/yazar/konu/anahtar dolu | yer tutucu olamaz | ✅ |
| Ana hat | var, bölümleri taşıyor | — | ✅ |

**İlk koşumda İKİ kusur bulundu ve düzeltildi:** gömülmemiş `Helvetica`
(KDP yüklemede işaretler) ve künyede `untitled` / `anonymous`.

---

## 2 · § 43 · Biçim kalitesi incelemesi

Basılı sayfanın METİN KATMANI tarandı: yer tutucu metin, iç kayıt
kimliği (`SYM-xxx`, `AF-xx`, `M-xxx`, `PR-xx`, `TR-xx`, `S-xxxx`),
geçici dosya adı, mutlak yol, hata ayıklama artığı, proje dili sızıntısı.

**Sonuç: temiz.**

Kapının ilk sürümü DESEN arıyordu ve YANLIŞ POZİTİF verdi: Ek I'deki
ANSUR II rapor numarası `NATICK/TR-15/007` bir prova okuması kimliği
sanıldı. Deseni gevşetmek kapıyı körleştirirdi; kapı bunun yerine
KAYITTAKİ GERÇEK kimlikleri arar. Sızıntı fixture'ıyla sınandı:
`AF-13`, `M-006` ve `TODO` yakalandı, rapor numarası yok sayıldı.

---

## 3 · § 42 · Fiziksel provanın içsel ikamesi

`06_BUILD/print_sim.py` — **257 sayfanın 257'si** 300 dpi'de
rasterleştirildi.

| Denetim | Sonuç |
|---|---|
| ① 300 dpi rasterleştirme | 257/257 başarılı |
| ② 1-bit eşikleme (POD yarım ton kullanmaz) | çizgi kaybı yok |
| ③ ince çizgi hayatta kalma | asgari çizgi 0,4 pt = 1,7 piksel |
| ④ kenar boşluğuna mürekkep | **temiz** (eşik 2,0 pt) |
| ⑤ mürekkep yoğunluğu | en yoğun sayfa %5,2 |
| ⑥ başparmak okunabilirliği | 1/8 ölçekte yapı korunuyor |

**Bu araç iki sessiz kusur buldu ve ikisini de hiçbir veri kapısı
göremezdi:**

1. **46 akış şeması metin sütunundan 71 pt genişti.** Dizgi, farkı
   sıfıra kırpıp figürü sağa taşırıyordu: 20 ÇİFT sayfada mürekkep cilt
   payına giriyor, kesime **1,3 pt** kalana kadar uzanıyordu — ciltte
   kaybolurdu. Örneklem bunu bulamazdı: 29 sayfalık ilk örneklem
   4 sayfa gördü, TAM tarama 20 gördü. Kapı artık her sayfayı okur.
2. **Bir sayfanın tamamı 122,5 pt kaymıştı.** Bir figür çizici tuval
   açıp `finish()` çağırmıyordu; karşılıksız `saveState()`, sonraki bir
   figürün `restoreState()`'i tarafından çekilip o sayfanın gövdesini,
   yan notunu ve folyosunu kaydırdı — yan notun metni sayfadan taşıp
   KESİLDİ. Aynı hata figürün kitaba HİÇ BASILMAMASINA da yol açıyordu.

Eşik (2,0 pt) bir ÖLÇÜMDEN gelir: tam tarama iki nüfus buldu —
0,24–1,20 pt tipografik (ortalanmış cetvel kalemi, italik harfin
negatif yan boşluğu) ve 45–62 pt içerik taşması. Eşik birinciyi kapsar,
ikincisinin yirmide biridir.

### ÖLÇÜLEMEYENLER — bu araç fiziksel provanın YERİNE GEÇMEZ

kâğıdın gerçek beyazlığı · mürekkep yayılması (dot gain) · cildin düz
durup durmadığı · sayfanın arkasından görünme · gerçek kesim toleransı.

**Fiziksel prova durumu: `UNAVAILABLE`.** Prova baskı sipariş
EDİLMEDİ ve sonucu UYDURULMADI.

---

## 4 · KDP dış doğrulama

**`KDP_EXTERNAL_VALIDATION_UNAVAILABLE`**

KDP hesabı erişimi YOKTUR. Bu nedenle:

* KDP Previewer **çalıştırılmadı**;
* yükleme **yapılmadı**;
* baskı maliyeti / telif **hesaplanmadı** (kayıtlı S-0009…S-0012
  değerleri Faz 1'de okunmuştur, bu fazda YENİDEN doğrulanmadı);
* hiçbir KDP hesap işlemi yapılmadı ve yapılmış gibi gösterilmedi.

Kurucunun yükleyeceği paket hazırlandı:
`09_OUTPUT/RELEASE_CANDIDATE/` — iç blok PDF'i, KDP form alanları,
yapı manifestosu (girdi SHA-256'ları + git SHA), tam QA çıktısı,
yayın notları ve paketin kendi sağlamaları.

**Kapak bu pakette YOKTUR** ve bu fazın kapsamı değildir.

---

## 5 · Faz 6 kabul ölçütleri

| Ölçüt | Durum |
|---|---|
| Kesim / kenar / cilt payı KDP kaydına uyuyor | ✅ ölçüldü |
| Yazı tipleri gömülü | ✅ 6/6 |
| PDF sürümü ve boyutu kabul aralığında | ✅ |
| Künyede yer tutucu yok | ✅ |
| Ana hat (bookmark) var | ✅ |
| Basılı sayfada iç kimlik / hata ayıklama artığı yok | ✅ § 43 |
| Kenar boşluğuna içerik taşmıyor | ✅ 257/257 sayfa ölçüldü |
| Sayfa sayısı cilt payı bandını değiştirmiyor | ✅ 257 ∈ 151–300 |
| KDP Previewer | ❌ **ERİŞİLEMEZ** |
| Fiziksel prova | ❌ **ERİŞİLEMEZ** |

**Faz 6 durumu: İÇSEL OLARAK TAMAM · DIŞ DOĞRULAMA BEKLİYOR.**
