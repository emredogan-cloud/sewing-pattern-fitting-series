# BOOK-01-DIAGNOSTIC-SYSTEM

> Faz 1 çıktısı 4/10. Görev talimatı § 14, § 36.3.
>
> ⚠ **DOĞRULAMA DURUMU — dürüst kayıt.** Bu çerçeve **iç tutarlılık**
> açısından denetlendi (mantıksal tutarlılık, öğretilebilirlik,
> tekrarlanabilirlik, görsel anlatılabilirlik, fiziksel sınanabilirlik)
> ve `qa_boundary.py`/`validate_spec.py` kapılarından geçti.
>
> **Hiçbir dış teknik otoriteye karşı doğrulanmadı ve hiçbir adımı
> fiziksel olarak sınanmadı.** Görev talimatı § 37 "validated
> diagnostic framework" istiyor; teslim edilen şey *tanımlanmış ve
> içsel olarak tutarlı* bir çerçevedir. Dış doğrulama `A3` (kaynak
> bütçesi) ve Faz 3 (fiziksel doğrulama) görevidir. Bu ayrım
> bulanıklaştırılamaz.

---

## 1 · Neden bir döngü, neden bir katalog değil

Rakip mimarisi bir **kataloğdur**: "işte düzeltmeler, hangisine
ihtiyacınız olduğunu bulun." Bu, okurun teşhisi zaten koyabildiğini
varsayar.

Kategori liderinde Amazon'un kendi sayısallaştırılmış olumsuz etiketi
`Complexity(58)` (n=1.797) `OBSERVED` — okurun bir kısmı bu varsayımın
altında kalıyor.

Bu kitabın cevabı bir **yöntemdir**: okur her seferinde aynı yedi adımı
uygular ve her adımda tek bir karar verir.

## 2 · Yedi adım

```text
  ① KUR         Ölçüm koşulunu standartlaştır
       │        (yanlış koşul, bedeni değil kurulumu teşhis eder)
       ▼
  ② GÖZLE       Sabit sırayla bak, yorumlamadan kaydet
       │        denge → siluet → kıvrım alanı → gerginlik/açıklık → hareket
       ▼
  ③ SINIFLA     Gördüğünü kontrollü sözlükten ADLANDIR
       │        (10 belirti sınıfı — yorum değil, ad)
       ▼
  ④ YERİNİ BUL  Belirtinin GÖRÜLDÜĞÜ yer ≠ KAYNAKLANDIĞI yer
       │
       ▼
  ⑤ ÖLÇ         Üç sayıyı karşılaştır:
       │        vücut · kalıp (düz, payı çıkarılmış) · dikilmiş giysi
       ▼
  ⑥ SINA        TEK bir hipotez kur, EN UCUZ tersine çevrilebilir
       │        fiziksel testi uygula
       │        ├── belirti kayboldu VE yeni belirti doğmadı → ⑦
       │        ├── belirti kaldı → başka hipotez, ③'e dön
       │        └── yeni belirti doğdu → hipotez YANLIŞ, ④'e dön
       ▼
  ⑦ ADLANDIR    Düzeltme ailesini (AF-xx) ve MİKTARI kaydet
     ve KAYDET  → uyum profiline yaz → Kitap 2'ye devir noktası
```

## 3 · Adımların gerekçeleri

### ① KUR — neden ilk adım eleme adımıdır

Yanlış iç giyimle, yanlış duruşta, denge çizgisi çizilmemiş bir toile
üzerinde yapılan her gözlem **geçersizdir**. Bu adım
`confounders_to_rule_out` listesinin (dokuz kalem) uygulandığı yerdir.

Bu, kitabın en somut farklılaşma iddialarından biridir: rakip
mimarilerinde bu adımın sistematik bir karşılığı **görülmedi**
`HYPOTHESIS`.

### ② GÖZLE — neden sıra sabittir

Denge önce okunur, çünkü **denge bozuksa aşağıdaki her okuma
yanlıştır.** Ön/arka boy dengesizliği, göğüs bölgesinde göğüs hacmi
sorunu gibi görünen belirtiler üretir.

Sabit sıra ayrıca okurun "en dikkat çekici" belirtiye atlamasını
engeller — en dikkat çekici belirti genellikle en **sonuç** olandır
(etek ucu).

### ③ SINIFLA — neden yorum değil ad

"Burada bir sorun var" bir yorumdur. "Burada yatay bir kıvrım var" bir
gözlemdir. Sözlük on sınıf taşır ve her sınıfın **görsel bir işareti**
vardır (`TK-05`…`TK-07`).

**Kitabın en sık kullanılan kuralı:**

| Görülen | Ne anlatır |
|---|---|
| **Yatay** kıvrım | O yönde **BOY** fazlası |
| **Dikey** kıvrım | O yönde **GENİŞLİK** fazlası |
| **Çapraz** çekme çizgisi | Bir yerde **YETERSİZLİK**; çizgiler kaynağa doğru işaret eder |

### ④ YERİNİ BUL — belirtinin göründüğü yer nadiren nedenin yeridir

Üç yerleştirme kuralı:

1. **Çekme çizgileri kaynağa işaret eder.** Işınsal desenin merkezi
   gerginlik noktasıdır.
2. **Kıvrım en kısa kenarında sabitlenir.** Kumaşın toplandığı yer,
   fazlalığın olduğu yerdir.
3. **Etek ucu bir aynadır.** Etek ucundaki her sapmanın nedeni
   yukarıdadır — bu yüzden etek ucu **en son** okunur ve **asla ilk
   düzeltilmez**.

### ⑤ ÖLÇ — üç sayı, iki fark

| Sayı | Kaynağı |
|---|---|
| Vücut ölçüsü | `M-xxx` |
| Kalıbın vaat ettiği bitmiş ölçü | Beden tablosu veya kalıptan düz ölçü |
| Dikilmiş giysinin gerçek ölçüsü | Toile'den ölçülür |

İki fark okunur:

- **Kalıp − vücut = ease.** Bu fark tasarımın kendisi olabilir; o zaman
  ortada bir sorun **yoktur** (Bölüm 3).
- **Giysi − kalıp = yapım sapması.** Bu fark sıfır değilse neden
  kalıpta değil, dikişte veya kesimdedir → ① adımına geri dönülür.

Bu ikinci fark, `TOP-11`'in (eleme) sayısal karşılığıdır ve teşhisin
kalıba geçmeden önceki son güvenlik kapısıdır.

### ⑥ SINA — üç kural

1. **Tek değişken.** Bir seferde bir hipotez. İki değişiklik aynı anda
   denenirse hangisinin işe yaradığı bilinemez.
2. **En ucuz tersine çevrilebilir test.** İğnele, katla, şerit kumaş
   ekle — **kesme**. Kesilen kumaş geri gelmez.
3. **Yan etki taraması zorunlu.** Belirti kayboldu ama başka bir yerde
   yenisi doğduysa hipotez **yanlıştır** — düzeltmelerin birbirini
   etkilemesinin (`AF-xx.interacts_with`) fiziksel karşılığıdır.

### ⑦ ADLANDIR ve KAYDET

Çıktı üç parçadır: **düzeltme ailesi adı** (`AF-xx`) + **miktar** (sayı,
"biraz" değil) + **kanıt** (hangi ölçüm, hangi test).

Bu, Kitap 2'ye devir noktasıdır (`TK-18` handoff düğümü) ve okurun
elinde kalan kalıcı çıktıdır (uyum profili).

## 4 · Döngünün durma koşulları

| Durum | Ne yapılır |
|---|---|
| Belirti kayboldu, yeni belirti yok | Kaydet, sonraki belirtiye geç |
| İki hipotez de reddedildi | Bölge atlasında **başka** aday neden ara |
| Atlasta aday kalmadı | Eleme listesini (Bölüm 8) **baştan** uygula |
| Eleme de sonuç vermedi | Kaydet ve **açık bırak** — çözülmemiş bir gözlem, uydurulmuş bir nedenden iyidir |

**Son satır bir tasarım kararıdır:** kitap her belirtiye bir cevap
vermeye çalışmaz. Cevabı olmayan gözlemi cevapsız bırakmak,
doğrulanmamış bir neden atamaktan daha dürüsttür.

## 5 · Öğretilebilirlik kontrolü

| Ölçüt | Nasıl karşılanıyor |
|---|---|
| Mantıksal tutarlılık | Her adımın çıktısı bir sonrakinin girdisidir; geri dönüş yolları açık |
| Öğretilebilirlik | Yedi adım, her biri tek karar; Bölüm 6'da uçtan uca tek örnek |
| Tekrarlanabilirlik | Sabit gözlem sırası + sabit sözlük + sabit ölçüm üçlüsü |
| Görsel anlatılabilirlik | `TK-16`/`TK-17`/`TK-18` düğümleriyle akış şeması; yedi bölge şeması |
| Fiziksel sınanabilirlik | Adım ⑥ tanımı gereği fiziksel bir testtir |

## 6 · Bu çerçevenin bilinen zayıflıkları

1. **Çoklu belirti.** Gerçek bir toile'de aynı anda birkaç belirti
   bulunur. Döngü tek belirti üzerinde çalışır; sıralama kuralı
   (Bölüm 16) bu boşluğu kapatmaya çalışır ama **Faz 3'te gerçek
   okurlarla sınanmalıdır.**
2. **Ölçüm hassasiyeti.** Ev koşullarında ölçüm hatası, aranan farkla
   aynı büyüklükte olabilir. Kitap bunu "tek ölçüm değil, tekrar
   ölçüm" kuralıyla azaltır — ama ortadan kaldıramaz.
3. **Asimetri.** Tek taraflı belirtiler ayrı bir sınıf olarak
   işaretlendi, ama asimetrik düzeltmenin kendisi Kitap 2'nin işidir.
4. **Dış doğrulama yok.** § 0'daki uyarı burada tekrarlanır.

---

*Vâliçe Press · TRUE FIT 1 · Diagnostic System · 28 Ağustos 2026*
