# BOOK-01-DIAGNOSIS-TO-ADJUSTMENT-MAP

> Faz 1 çıktısı 5/10. Görev talimatı § 22, § 36.8.
>
> Makine-okunur kaynak: [`../../02_TAXONOMY/public/crosswalk.json`](../../02_TAXONOMY/public/crosswalk.json)
> — `06_BUILD/build_crosswalk.py` tarafından TÜRETİLİR, elle düzenlenmez.
> Mekanik denetim: `qa_boundary.py`, `validate_spec.py`.

---

## 1 · Kapsam ölçümü

| Metrik | Değer |
|---|---|
| Kitap 1 belirtisi | **43** |
| Aday neden | **129** |
| Kitap 2'ye giden yol | **108** |
| **Açık istisna** (Kitap 2 karşılığı YOK) | **21** |
| Kitap 1'den ulaşılabilen düzeltme ailesi | **19 / 19** |
| Ulaşılamayan aile | **0** |

## 2 · İstisnalar neden bir eksik değil, bir ÜRÜN ÖZELLİĞİDİR

21 aday nedenin Kitap 2'de karşılığı **yoktur** — çünkü bunlar kalıp
sorunu değildir:

- **yapım hatası** (kenar gerdirilmiş, pens ucu düz bitirilmemiş,
  kol çentikleri hizalanmamış)
- **kesim hatası** (parça çözgüye eğri kesilmiş)
- **prova koşulu hatası** (ağırlık tek ayakta)
- **tasarım tercihi** (düşük omuz, bol kol, düşük ağ — bunlar SORUN
  DEĞİLDİR)
- **kalıp/tasarım parametresi** (kapama payı, düğme aralığı)

Kitap 1'in bunları ayırabilmesi okuru **gereksiz ve geri alınamaz bir
düzeltmeden** korur. Bu, satılan değerin bir parçasıdır.

## 3 · Devir cümlesinin biçimi

Kitap 1'in akış şemalarının bitiş formu (`TK-18` handoff düğümü):

> Belirti **SYM-016** + ayırt edici kanıt → **AF-01 · Bust volume**
> → *Bu düzeltmenin adım adım uygulaması: TRUE FIT 2.*

**Kitap 1 bir aile ADI ve bir MİKTAR verir. Adım vermez.**
Sınır: `SERIES_CONTENT_ARCHITECTURE.md § 6` · denetim:
`qa_boundary.py § check_excluded_leak`.

---

## 4 · Bölge bölge crosswalk


### Boyun — Bölüm 9 *(3 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-001` | Ön yaka, göğüs kemiğinin üzerinde vücuda değmeden duruyor; okur öne eğildiğinde açıklık büyüyor. | Yaka eğrisi vücut için fazla geniş/derin | Açıklık okur DİK dururken de var ve simetrik. | Kalıp yaka eğrisi uzunluğu vs. M-013 boyun tabanı çevresi | **AF-06** Neckline size and shape |
|  |  | Göğüs hacmi yakayı öne çekiyor | Açıklık ASİMETRİK biçimde göğse doğru yönleniyor ve göğüs pensi de yerinde değil; okur öne eğilince BELİRGİN artıyor. | M-031 (göğüs − üst göğüs farkı) kalıbın varsaydığı farktan büyük mü | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Yaka kenarı dikiş sırasında gerilmiş | Açıklık dalgalı/gevşek görünüyor, düz bir açıklık değil. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-002` | Yaka boynun tabanına baskı yapıyor, kırmızı iz bırakıyor veya yutkunmayı zorlaştırıyor. | Yaka eğrisi vücut için fazla dar | Baskı çevre boyunca eşit dağılmış. | Kalıp yaka çevresi vs. M-013 | **AF-06** Neckline size and shape |
|  |  | Yuvarlak sırt boyunu öne itiyor | Baskı ARKA yakada belirgin, ön yakada yok; arka yaka ayrıca yukarı tırmanıyor. | M-016 (arka orta boy) kalıbın arka orta boyundan uzun mu | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Omuz dikişi öne kaymış, yakayı boyna bindiriyor | Omuz dikişi omuz üstü orta çizgisinin ÖNÜNDE duruyor. | Omuz dikişinin konumu vs. omuz üstü orta çizgisi | **AF-05** Shoulder position (forward shoulder) |
| `SYM-003` | Arka yaka yukarı tırmanıyor ve boynu sıyırıyor; aynı anda arka etek ucu da yükseliyor. | Arka beden boyu yetersiz (yuvarlak sırt / dik duruş) | Ön etek ucu yerde düzgün, YALNIZCA arka yükseliyor. | M-016 vs. kalıp arka orta boyu; M-032 (ön/arka fark) | **AF-11** Torso length and front/back balance |
|  |  | Kürek kemiği genişliği yetersiz, kumaşı yukarı çekiyor | Yükselme ile birlikte kürek hizasında yatay gerginlik var. | M-020 (sırt genişliği) vs. kalıp arka beden genişliği | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Yaka arkada fazla dar, giysiyi yukarı asıyor | Yükselme SADECE yaka çevresinde, kürek hizasında gerginlik YOK. | Kalıp arka yaka çevresi vs. M-013 | **AF-06** Neckline size and shape |

### Omuz — Bölüm 9 *(5 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-004` | Boyun noktasından koltuk altına doğru uzanan çapraz çekme çizgileri. | Omuz eğimi kalıbın varsaydığından DİK (square shoulder) | Çizgiler boyun noktasından DIŞA-AŞAĞI iniyor; omuz ucunda kumaş gergin, omuz dikişi omza yapışık. | Omuz ucu ile koltuk altı arası dikey mesafe vs. kalıptaki karşılığı | **AF-03** Shoulder slope (square / sloping shoulder) |
|  |  | Omuz eğimi kalıbın varsaydığından EĞİK (sloping shoulder) | Çizgiler ters yönde — omuz ucundan boyuna doğru; omuz ucunda kumaş TOPLANIYOR. | Aynı ölçüm, ters yön | **AF-03** Shoulder slope (square / sloping shoulder) |
|  |  | Omuz genişliği yetersiz | Çizgiler var ama omuz eğimi doğru; kol oyuntusu dikişi omuz ucunun İÇİNDE kalıyor. | M-014 vs. kalıp omuz dikişi uzunluğu | **AF-04** Shoulder width (narrow / broad shoulder) |
| `SYM-005` | Omuz dikişinin hemen altında, kol oyuntusuna yakın yerde kumaş yatay bir kıvrım hâlinde toplanıyor. | Omuz eğimi fazla eğik çizilmiş (dik omuzlu okur için) | Kıvrım omuz UCUNA yakın; boyun tarafında yok. | Omuz ucu yüksekliği vs. kalıp | **AF-03** Shoulder slope (square / sloping shoulder) |
|  |  | Kol oyuntusu fazla derin, kol başı fazla yüksek | Kıvrım kol oyuntusu çevresini takip ediyor ve kol kaldırıldığında kayboluyor. | M-022 vs. kalıp kol oyuntusu derinliği | **AF-08** Armhole depth and shape |
|  |  | Omuz genişliği fazla | Kıvrımla birlikte kol başı omuz ucunun DIŞINA sarkıyor. | M-014 vs. kalıp omuz dikişi uzunluğu | **AF-04** Shoulder width (narrow / broad shoulder) |
| `SYM-006` | Omuz dikişi omuz üstü orta çizgisinin ARKASINDA duruyor; öne doğru kaymaya çalışıyor. | Öne düşük omuz duruşu (forward shoulder) | Dikiş HER İKİ omuzda da arkada; okur rahat dururken de böyle. | Omuz dikişi konumu vs. omuz üstü orta çizgisi (fotoğrafla ölç) | **AF-05** Shoulder position (forward shoulder) |
|  |  | Yuvarlak sırt kumaşı arkaya çekiyor | Dikiş kayması var AMA kürek hizasında yatay gerginlik de var. | M-016 ve M-020 vs. kalıp karşılıkları | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Ön beden arka bedene göre kısa | Ön etek ucu da yükseliyor. | M-032 (ön/arka boy farkı) | **AF-11** Torso length and front/back balance |
| `SYM-007` | Omuz dikişi omuz ucunu geçip kola sarkıyor; kol başı omuzdan aşağı düşüyor. | Omuz genişliği fazla (kalıp daha geniş omuz için) | Sarkma her iki omuzda simetrik; kol oyuntusu dikişi kol kemiği ucunun DIŞINDA. | M-014 vs. kalıp omuz dikişi uzunluğu | **AF-04** Shoulder width (narrow / broad shoulder) |
|  |  | Tasarım bilerek düşük omuzlu (drop shoulder) | Kalıp zarfı/teknik çizim düşük omuz gösteriyor; kol oyuntusu da derin. | Kalıbın bitmiş giysi ölçüsü tablosu — tasarım ease'i (T-07) mi | — *istisna* |
|  |  | Omuz eğimi fazla dik çizilmiş | Sarkmayla birlikte omuz ucunda kumaş toplanması var. | Omuz ucu yüksekliği vs. kalıp | **AF-03** Shoulder slope (square / sloping shoulder) |
| `SYM-008` | Kol öne uzatıldığında sırt boyunca sert bir çekme oluyor; giysi hareketi kısıtlıyor. | Sırt genişliği yetersiz | Kol yanda dururken belirti YOK; yalnızca kol öne gelince çıkıyor. | M-020 vs. kalıp arka beden genişliği (kol oyuntusu kıvrımları arası) | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Kol oyuntusu fazla dar/öne kaymış | Çekme kol oyuntusu kenarında yoğunlaşıyor, kürek ortasında yok. | Kalıp kol oyuntusu çevresi vs. M-007 + gerekli ease | **AF-08** Armhole depth and shape |
|  |  | Kol başı ease'i yetersiz veya kol dar | Çekme kolun kendisinde de hissediliyor. | M-007 vs. kalıp bicep hattı | **AF-10** Sleeve girth and length (bicep, forearm, length) |

### Üst sırt — Bölüm 10 *(4 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-009` | Kürek kemikleri hizasında sırt boyunca yatay bir kıvrım/fazlalık duruyor. | Arka beden boyu fazla | Kıvrım kol kaldırılınca da kalıyor; yaka ve omuz yerinde. | M-016 vs. kalıp arka orta boyu | **AF-11** Torso length and front/back balance |
|  |  | Kürek çıkıntısı için ayrılmış şekillendirme kullanılmıyor (düz sırt) | Kıvrım kürek hizasında YOĞUN, aşağı doğru kayboluyor; kalıpta omuz pensi/ease var ama vücut onu doldurmuyor. | Kalıp omuz dikişi uzunluğu (pens dâhil) vs. M-014 | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Arka yaka fazla yüksek, kumaşı aşağı itiyor | Kıvrım yakanın hemen altında ve yaka boyunu sıkıyor. | Kalıp arka yaka çevresi vs. M-013 | **AF-06** Neckline size and shape |
| `SYM-010` | Kol oyuntularının arasında, sırt boyunca dikey duran gevşek kıvrımlar var. | Sırt genişliği fazla | Kıvrımlar dikey ve simetrik; kol öne uzatıldığında da kayboluyor değil, AZALIYOR. | M-020 vs. kalıp arka beden genişliği | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Bir beden büyük seçilmiş | Aynı fazlalık ön bedende, kolda ve belde de var. | M-001/M-002 vs. kalıbın beden tablosu | **AF-18** Grading between sizes |
|  |  | Kol oyuntusu fazla geniş | Fazlalık yalnızca kol oyuntusuna yakın; sırt ortasında yok. | Kalıp kol oyuntusu çevresi vs. M-007 + ease | **AF-08** Armhole depth and shape |
| `SYM-011` | Arka etek ucu belirgin biçimde yükseliyor; giysi arkadan yukarı tırmanıyor. | Arka beden boyu yetersiz (yuvarlak sırt) | Kürek hizasında AYRICA yatay gerginlik var; arka yaka da yukarı çekiliyor. | M-016 vs. kalıp arka orta boyu | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Kalça/oturak hacmi kumaşı yukarı çekiyor | Yükselme bel hizasının ALTINDA başlıyor; kürek hizası temiz. | M-006 vs. kalıp kalça çevresi | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Ön/arka denge bozuk (öne eğik duruş) | Ön etek ucu ise AŞAĞI sarkıyor — ikisi birlikte. | M-032 (ön/arka boy farkı) | **AF-11** Torso length and front/back balance |
| `SYM-012` | Arka orta dikiş/fermuar düz durmuyor, dışa doğru yay çiziyor. | Bel oyuğu (sway back) — arka orta bel hizasında fazlalık | Yay bel hizasında en belirgin; hemen üstünde yatay kıvrımlar da var. | M-016 ve M-032; ayrıca bel hizasında kalıp/vücut boy farkı | **AF-14** Sway back / lumbar hollow |
|  |  | Yuvarlak sırt — arka orta üst kısımda boy yetersiz | Yay kürek hizasında; bel temiz. | M-016 vs. kalıp | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Fermuar dikilirken gerdirilmiş | Yay düzensiz, dalgalı; kumaş fermuar boyunca büzülmüş. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |

### Kol oyuntusu — Bölüm 10 *(3 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-013` | Kol aşağı indirildiğinde koltuk altı sıkıyor; giysi omuzdan yukarı çekiliyor. | Kol oyuntusu fazla sığ (koltuk altı çok yüksek) | Kol yukarıdayken rahat, aşağıdayken sıkıyor; koltuk altında kırmızı iz var. | M-022 vs. kalıp kol oyuntusu derinliği | **AF-08** Armhole depth and shape |
|  |  | Kol bicep hattı dar | Sıkışma kol içinde de hissediliyor; kol oyuntusu kendisi rahat. | M-007 + gerekli ease vs. kalıp bicep hattı | **AF-10** Sleeve girth and length (bicep, forearm, length) |
|  |  | Göğüs hacmi ön kol oyuntusunu yukarı çekiyor | Sıkışma ÖN koltuk altında; göğüsten kol oyuntusuna doğru çekme çizgileri de var. | M-031 (göğüs − üst göğüs) | **AF-01** Bust volume (full / small bust adjustment) |
| `SYM-014` | Kol oyuntusunun ÖN kenarı vücuda değmiyor, göğsün üstünde açık duruyor. | Ön beden genişliği fazla | Açıklık kol yanda dururken de var; ön göğüs üstünde gevşeklik hissediliyor. | M-021 (ön göğüs genişliği) vs. kalıp ön beden genişliği | **AF-08** Armhole depth and shape |
|  |  | Göğüs pensi apeksi doğru yerde değil, üstte fazlalık bırakıyor | Açıklıkla birlikte göğsün ÜSTÜNDE boş bir alan var. | M-017 (omuz–apeks) vs. kalıp pens konumu | **AF-02** Bust position (apex height / width, dart angle) |
|  |  | Omuz genişliği fazla | Kol başı da omuz ucundan sarkıyor. | M-014 vs. kalıp omuz dikişi | **AF-04** Shoulder width (narrow / broad shoulder) |
| `SYM-015` | Kol oyuntusunun ARKA kenarı vücuda değmiyor. | Arka beden genişliği fazla | Sırtta dikey gevşek kıvrımlar da var. | M-020 vs. kalıp arka beden genişliği | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Omuz eğimi fazla dik çizilmiş | Omuz ucunda kumaş toplanması da var. | Omuz ucu yüksekliği vs. kalıp | **AF-03** Shoulder slope (square / sloping shoulder) |
|  |  | Kol oyuntusu fazla geniş çizilmiş | Açıklık kol oyuntusu çevresi boyunca eşit. | Kalıp kol oyuntusu çevresi vs. M-007 + ease | **AF-08** Armhole depth and shape |

### Göğüs — Bölüm 11 *(6 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-016` | Göğüs ucundan yan dikişe (ve/veya kol oyuntusuna) doğru uzanan çekme çizgileri; kumaş göğsün üzerinde geriliyor. | Göğüs hacmi kalıbın varsaydığından fazla | Çizgiler apeksten IŞINSAL olarak yayılıyor; ön etek ucu da yukarı tırmanıyor; ön yaka açılıyor. | M-031 (göğüs − üst göğüs farkı) kalıbın varsaydığı farktan büyük | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Ön beden genel olarak dar (beden seçimi) | Aynı gerginlik göğüs dışında — bel, kalça, kol — her yerde var. | M-002 vs. kalıp beden tablosu | **AF-18** Grading between sizes |
|  |  | Pens ucu apeksin uzağında, hacmi yanlış yere dağıtıyor | Gerginlik VAR ama toplam ön genişlik yeterli; pens ucu apeksten belirgin uzakta bitiyor. | M-017 ve M-018 vs. kalıp pens ucu konumu | **AF-02** Bust position (apex height / width, dart angle) |
| `SYM-017` | Ön etek ucu arka etek ucundan belirgin biçimde yukarıda; giysi önden kısa görünüyor. | Göğüs hacmi ön kumaşı yukarı çekiyor | Göğüsten yayılan çekme çizgileri de var; yan dikiş öne kayıyor. | M-031; M-032 (ön/arka boy farkı) | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Ön beden boyu yetersiz | Çekme çizgisi YOK, yalnızca boy kısa; göğüs bölgesi rahat. | M-015 vs. kalıp ön orta boyu | **AF-11** Torso length and front/back balance |
|  |  | Karın hacmi kumaşı yukarı çekiyor | Yükselme bel hizasının altında başlıyor; göğüs temiz. | M-005 (yüksek kalça) vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |
| `SYM-018` | Yan dikişler düşey durmuyor, öne doğru kayıyor. | Ön beden hacmi yetersiz (göğüs veya karın) | Kayma ile birlikte göğüs veya karın hizasında gerginlik var. | M-031 veya M-005 vs. kalıp | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Arka beden genişliği fazla | Kayma var ama ön tarafta gerginlik YOK; arkada dikey gevşek kıvrımlar var. | M-020 vs. kalıp arka beden genişliği | **AF-07** Upper back (round back / broad back / narrow back) |
|  |  | Kumaş çözgüye eğri kesilmiş | Kayma tek tarafta; simetrik değil. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-019` | Göğüs pensi ucunda kumaş büzüşüyor veya küçük bir çıkıntı/kabarcık oluşuyor. | Pens ucu apeksin üzerinde bitiyor (çok uzun) | Kabarcık tam pens ucunda; apeksin kendisi düz. | M-017/M-018 vs. kalıp pens ucu | **AF-02** Bust position (apex height / width, dart angle) |
|  |  | Pens hacmi vücuda göre fazla | Pens çevresinde genel gevşeklik de var. | M-031 kalıbın varsaydığı farktan küçük | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Pens dikilirken ucu düz bitirilmemiş | Büzüşme düzensiz; dikiş ucunda düğüm/geri dikiş var. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-020` | Göğsün ÜSTÜNDE, köprücük kemiği ile göğüs arasında boş, çöken bir alan var. | Göğüs pensi apeksten yukarıda konumlanmış | Boşluk pensin hemen üstünde; pens ucu apeksin üzerinde. | M-017 vs. kalıp pens konumu | **AF-02** Bust position (apex height / width, dart angle) |
|  |  | Ön üst genişlik fazla | Boşluk geniş bir alana yayılmış; kol oyuntusu ön kenarı da açılıyor. | M-021 vs. kalıp ön beden genişliği | **AF-08** Armhole depth and shape |
|  |  | Kalıp daha dolgun bir üst göğüs için çizilmiş | Boşluk üst göğüs çevresinde; M-001 kalıbın varsaydığından küçük. | M-001 vs. kalıp üst göğüs karşılığı | **AF-01** Bust volume (full / small bust adjustment) |
| `SYM-021` | Düğme sırası göğüs hizasında yatay olarak açılıyor; düğmeler arasında boşluk oluşuyor. | Göğüs hacmi yetersiz | Açılma göğüs hizasında YOĞUN; üstte ve altta kapama düzgün. | M-031 | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Ön kapama payı (extension) dar | Açılma kapama boyunca EŞİT dağılmış. | Kalıp kapama payı genişliği | — *istisna* |
|  |  | Düğme aralığı göğüs hizasına düğme koymuyor | Açıklık iki düğme arasında ve apeks hizasında düğme YOK. | Düğme konumları vs. M-017 apeks yüksekliği | — *istisna* |

### Bel / gövde — Bölüm 12 *(5 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-022` | Bel dikişi/bel hattı doğal belin üstünde veya altında oturuyor. | Beden boyu kalıbın varsaydığından farklı | Kayma çevre boyunca EŞİT; ön ve arkada aynı miktarda. | M-015 ve M-016 vs. kalıp ön/arka orta boyları | **AF-11** Torso length and front/back balance |
|  |  | Ön/arka denge bozuk | Kayma ön ve arkada FARKLI miktarda. | M-032 (ön/arka boy farkı) | **AF-11** Torso length and front/back balance |
|  |  | Tasarım bilerek yüksek/düşük belli | Kalıp teknik çizimi ve bitmiş giysi ölçüsü bunu gösteriyor. | Kalıbın bitmiş giysi ölçü tablosu | — *istisna* |
| `SYM-023` | Bel hizasının hemen ÜSTÜNDE, arkada, kumaş yatay kıvrımlar hâlinde havuzlanıyor. | Bel oyuğu (sway back) — arka orta bel hizasında kumaş fazlası | Fazlalık YALNIZCA arka ortada yoğun, yan dikişlere doğru azalıyor; ön taraf temiz. | Arka orta bel hizasında kalıp boyu vs. M-016'nın bel hizasına düşen kısmı | **AF-14** Sway back / lumbar hollow |
|  |  | Arka beden boyu genel olarak fazla | Fazlalık arka genişliğe EŞİT dağılmış, yan dikişlerde de var. | M-016 vs. kalıp arka orta boyu | **AF-11** Torso length and front/back balance |
|  |  | Oturak hacmi kumaşı yukarı itiyor | Havuzlanma ile birlikte oturak üzerinde yatay çekme çizgileri de var. | M-006 vs. kalıp kalça çevresi | **AF-13** Hip and seat volume (full / flat seat, high hip) |
| `SYM-024` | Bel bandı arkada vücuttan uzaklaşıyor, aralık kalıyor. | Bel oyuğu (sway back) | Aralık arka ortada en geniş; yanlarda kapanıyor. Belin hemen üstünde havuzlanma da var. | Bel/kalça oranı ve M-016 | **AF-14** Sway back / lumbar hollow |
|  |  | Bel/kalça oranı kalıbın varsaydığından farklı | Bel bandı bel çevresine oturuyor ama kalça bölgesi dar/geniş. | M-033 (kalça − bel) vs. kalıbın beden tablosu | **AF-18** Grading between sizes |
|  |  | Bel bandı fazla uzun kesilmiş | Aralık çevre boyunca eşit. | Bel bandı uzunluğu vs. M-004 | **AF-12** Waist girth |
| `SYM-025` | Bel hizasında, yan dikişlerin yakınında dikey gevşek kıvrımlar var. | Bel çevresi fazla | Kıvrımlar dikey ve simetrik; göğüs ve kalça oturuyor. | M-004 vs. kalıp bel çevresi (dikiş payları çıkarılmış) | **AF-12** Waist girth |
|  |  | Bel şekillendirmesi (pens) yetersiz | Fazlalık var ama yan dikişten alınca kalça sıkışıyor. | M-033 (kalça − bel farkı) büyük | **AF-12** Waist girth |
|  |  | Bir beden büyük seçilmiş | Aynı fazlalık göğüs ve kalçada da var. | M-002/M-004/M-006 vs. beden tablosu | **AF-18** Grading between sizes |
| `SYM-026` | Bel dikişi/bandı sıkıyor; oturunca rahatsız ediyor, iz bırakıyor. | Bel çevresi yetersiz | Sıkışma çevre boyunca eşit; oturunca artıyor. | M-004 + wearing ease vs. kalıp bel çevresi | **AF-12** Waist girth |
|  |  | Bel hattı yanlış hizada oturuyor (doğal belin altında) | Sıkışma bel altında, karın hizasında. | M-015/M-016 vs. kalıp; M-005 | **AF-11** Torso length and front/back balance |
|  |  | Karın hacmi | Sıkışma yalnızca ÖNDE; arkada rahat. | M-005 (yüksek kalça) vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |

### Kalça / oturak — Bölüm 13 *(4 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-027` | Oturak üzerinde yatay çekme çizgileri var; kumaş oturağın üzerinde geriliyor. | Oturak hacmi kalıbın varsaydığından fazla | Çizgiler oturak üzerinde YOĞUN; yan dikiş arkaya kayıyor; arka etek ucu yükseliyor. | M-006 vs. kalıp kalça çevresi; ayrıca arka/ön kalça dağılımı | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Ağ uzunluğu yetersiz (pantolonda) | Çizgilerle birlikte ağ yukarı çekiliyor ve oturmak zor. | M-027 (ağ uzunluğu) vs. kalıp arka ağ uzunluğu | **AF-15** Crotch depth and length |
|  |  | Genel kalça çevresi yetersiz | Aynı gerginlik ÖNDE de var. | M-006 vs. kalıp toplam kalça çevresi | **AF-18** Grading between sizes |
| `SYM-028` | Oturağın hemen ALTINDA kumaş sarkıyor, boş bir torba oluşturuyor. | Oturak hacmi kalıbın varsaydığından az (flat seat) | Sarkma oturak altında; oturak üzerinde gerginlik YOK. | M-006 ve arka/ön kalça dağılımı vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Ağ uzunluğu fazla | Sarkma ağ bölgesine kadar iniyor; ağ vücuda değmiyor. | M-027 vs. kalıp arka ağ uzunluğu | **AF-15** Crotch depth and length |
|  |  | Arka beden/etek boyu fazla | Sarkma yatay kıvrım hâlinde ve bel hizasına kadar çıkıyor. | M-016 / bel-kalça mesafesi M-023 | **AF-11** Torso length and front/back balance |
| `SYM-029` | Etek/pantolon bir kalçada yukarı tırmanıyor; etek ucu yere paralel değil. | Vücut asimetrisi (bir kalça daha yüksek/dolgun) | Yükselme TEK TARAFTA ve okur ağırlığını eşit dağıttığında da sürüyor. | Bel işaretinden yere iki taraf ayrı ayrı ölçülür (M-024, sağ ve sol) | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Duruş: ağırlık tek ayakta | Yükselme okur ağırlığını eşitleyince KAYBOLUYOR. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
|  |  | Kumaş eğri kesilmiş | Yükselme ile birlikte yan dikiş de spiralleniyor. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-030` | Yan dikiş kalça hizasında arkaya doğru kayıyor. | Arka hacim yetersiz | Kayma ile birlikte oturak üzerinde yatay çekme var. | Arka/ön kalça dağılımı vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Ön hacim fazla | Kayma var ama arkada gerginlik YOK; önde gevşeklik var. | M-005 ve ön kalça karşılığı | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Kumaş eğri kesilmiş | Kayma tek tarafta. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |

### Kol — Bölüm 14 *(4 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-031` | Kol başından pazuya doğru çapraz çekme çizgileri; kol kaldırıldığında artıyor. | Kol bicep genişliği yetersiz | Çizgiler bicep hattında yoğun; kol kaldırılınca belirgin artıyor. | M-007 + wearing ease vs. kalıp bicep hattı | **AF-10** Sleeve girth and length (bicep, forearm, length) |
|  |  | Kol başı yüksekliği fazla | Çizgiler kol başı çevresinde; bicep rahat. | Kalıp kol başı yüksekliği vs. bitmiş kol oyuntusu çevresi | **AF-09** Sleeve cap (height, shape, ease) |
|  |  | Kol oyuntusu dar, kolu sıkıştırıyor | Çizgiler kol oyuntusu dikişinde başlıyor; kol tek başına rahat. | M-022 ve kalıp kol oyuntusu çevresi | **AF-08** Armhole depth and shape |
| `SYM-032` | Üst kolda dikey gevşek kıvrımlar var; kol torba gibi duruyor. | Kol genişliği fazla | Kıvrımlar dikey; kol hareketi tamamen serbest. | M-007 vs. kalıp bicep hattı | **AF-10** Sleeve girth and length (bicep, forearm, length) |
|  |  | Tasarım bilerek bol kollu | Kalıp teknik çizimi ve bitmiş ölçü tablosu bol kol gösteriyor. | Kalıbın bitmiş giysi ölçü tablosu | — *istisna* |
|  |  | Kol başı ease'i fazla, kol başında toplanma yaratıyor | Fazlalık kol başında yoğun, aşağı doğru azalıyor. | Kalıp kol başı çevresi − kol oyuntusu çevresi (ease miktarı) | **AF-09** Sleeve cap (height, shape, ease) |
| `SYM-033` | Kol, kol üzerinde dönüyor; alt kol dikişi düz inmiyor, spiral çiziyor. | Kol başı çentikleri yanlış hizalanmış (öne/arkaya kaymış) | Dönme her iki kolda AYNI yönde; kol başı çentikleri omuz dikişiyle örtüşmüyor. | Kol başı çentik konumları vs. kol oyuntusu çentikleri | **AF-09** Sleeve cap (height, shape, ease) |
|  |  | Kol dirsek eğrisi vücuda uymuyor (öne dönük kol duruşu) | Dönme kol rahat sarkarken belirgin; dirsek hizasında çekme var. | M-029 (omuz–dirsek) ve dirsek şekillendirme konumu | **AF-09** Sleeve cap (height, shape, ease) |
|  |  | Kol eğri kesilmiş | Dönme TEK kolda. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-034` | Kol başı, kol oyuntusuna birleştiği yerde büzüşüyor/kırışıyor. | Kol başı ease'i kumaş için fazla | Büzüşme kol başı üst yayında; kumaş sert/dokusuz. | Kalıp kol başı çevresi − kol oyuntusu çevresi | **AF-09** Sleeve cap (height, shape, ease) |
|  |  | Kol başı ease'i doğru ama dağıtım/pot alma yapılmamış | Büzüşme düzensiz ve toplu; belirli noktalarda kat oluşmuş. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
|  |  | Kol oyuntusu çevresi kalıptan farklı dikilmiş | Kol oyuntusu ölçüsü kalıpla uyuşmuyor. | Dikilmiş kol oyuntusu çevresi vs. kalıp kol oyuntusu çevresi | **AF-08** Armhole depth and shape |

### Ağ / bacak — Bölüm 15 *(5 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-035` | Oturağın altında yatay çekme çizgileri; ağ yukarı çekiliyor ve rahatsız ediyor. | Ağ derinliği yetersiz | Oturunca belirgin artıyor; ayakta azalıyor. | M-026 (oturarak ağ derinliği) vs. kalıp ağ derinliği | **AF-15** Crotch depth and length |
|  |  | Arka ağ uzunluğu yetersiz | Ayakta da var; oturak üzerinde de gerginlik var. | M-027 (ağ uzunluğu) vs. kalıp arka ağ uzunluğu | **AF-15** Crotch depth and length |
|  |  | Arka ağ eğrisi vücut için fazla düz | Çekme yalnızca ağ eğrisinin kıvrımında; derinlik ve uzunluk sayısal olarak yeterli. | Kalıp arka ağ eğrisi şekli vs. vücut profili | **AF-16** Crotch curve shape (front / back hook) |
| `SYM-036` | Ön ağ bölgesinde kumaş 'U' biçiminde toplanıyor. | Ön ağ uzunluğu fazla | Toplanma ön ağda; arka temiz. | M-027'nin ön kısmı vs. kalıp ön ağ uzunluğu | **AF-15** Crotch depth and length |
|  |  | Ağ derinliği fazla | Toplanma hem ön hem arkada; ağ vücuda değmiyor. | M-026 vs. kalıp ağ derinliği | **AF-15** Crotch depth and length |
|  |  | Ön ağ eğrisi vücut için fazla kavisli | Sayılar doğru ama eğri fazla derin. | Kalıp ön ağ eğrisi şekli | **AF-16** Crotch curve shape (front / back hook) |
| `SYM-037` | Ağ noktasından kalçaya doğru çapraz çekme çizgileri. | Uyluk çevresi yetersiz | Çizgiler uyluk hizasında yoğun; oturunca artıyor. | M-009 (uyluk) + ease vs. kalıp uyluk hattı | **AF-17** Leg girth and shape (thigh, knee, calf) |
|  |  | Ağ eğrisi vücuda uymuyor | Çizgiler doğrudan ağ noktasından çıkıyor; uyluk çevresi yeterli. | M-027 ve kalıp ağ eğrisi | **AF-16** Crotch curve shape (front / back hook) |
|  |  | Karın/oturak hacmi kumaşı ağa doğru çekiyor | Çizgiler yukarıdan aşağı, karın veya oturak hizasında başlıyor. | M-005 / M-006 vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |
| `SYM-038` | Pantolon paçası dönüyor; iç bacak dikişi düz inmiyor. | Bacak duruşu (içe/dışa dönük diz) kumaşı çeviriyor | Dönme her iki bacakta simetrik ve ayakta belirgin. | Diz hizasında ön/arka bacak genişliği dağılımı | **AF-17** Leg girth and shape (thigh, knee, calf) |
|  |  | Ağ eğrisi dengesiz (ön/arka) | Dönme ağ hizasından başlıyor. | M-027 ön/arka dağılımı | **AF-16** Crotch curve shape (front / back hook) |
|  |  | Bacak eğri kesilmiş | Dönme TEK bacakta. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-039` | Ağ vücuttan uzakta, aşağıda duruyor; adım atmayı zorlaştırıyor. | Ağ derinliği fazla | Ağ ile vücut arası boşluk ayakta da var; oturunca rahat. | M-026 vs. kalıp ağ derinliği | **AF-15** Crotch depth and length |
|  |  | Tasarım bilerek düşük ağlı | Kalıp teknik çizimi düşük ağ gösteriyor. | Kalıbın bitmiş giysi ölçü tablosu | — *istisna* |
|  |  | Bel hattı doğal belin altında oturuyor | Bel bandı aşağıda; ağ da onunla birlikte inmiş. | M-004 işaretinden bel bandına mesafe | **AF-11** Torso length and front/back balance |

### Tüm giysi — Bölüm 16 *(4 belirti)*

| Belirti | Görünen | Aday neden | Ayırt edici kanıt | Doğrulayıcı ölçüm | → Kitap 2 |
|---|---|---|---|---|---|
| `SYM-040` | Etek ucu yere paralel değil; bir bölgede yükseliyor veya alçalıyor. | Bir hacim (göğüs, karın, oturak) kumaşı yukarı çekiyor | Yükselme o hacmin bulunduğu tarafta; aynı bölgede çekme çizgileri de var. | İlgili çevre ölçüsü vs. kalıp karşılığı | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Ön/arka denge bozuk | Bir taraf yükselirken diğeri alçalıyor; simetrik. | M-032 (ön/arka boy farkı) | **AF-11** Torso length and front/back balance |
|  |  | Vücut asimetrisi | Yükselme tek tarafta ve ağırlık eşitlendiğinde de sürüyor. | M-024 sağ ve sol ayrı ayrı | **AF-13** Hip and seat volume (full / flat seat, high hip) |
| `SYM-041` | Giysi vücut üzerinde dönüyor; yan dikişler zamanla öne/arkaya kayıyor. | Ön/arka hacim dağılımı vücuda uymuyor | Dönme tutarlı bir yönde ve her giyişte aynı. | Ön/arka çevre dağılımı vs. kalıp | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Vücut asimetrisi | Dönme tek yönde ve tek taraflı belirtilerle birlikte. | Sağ/sol ayrı ölçümler | **AF-13** Hip and seat volume (full / flat seat, high hip) |
|  |  | Parçalar eğri kesilmiş | Dönme düzensiz; çözgü çizgileri kumaş kenarına paralel değil. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-042` | Ön orta veya arka orta çizgisi yere dik durmuyor; denge çizgileri yatay değil. | Duruş (öne/arkaya eğik) dengeyi bozuyor | Sapma simetrik ve okurun doğal duruşunda sürüyor. | M-032 (ön/arka boy farkı) | **AF-11** Torso length and front/back balance |
|  |  | Bir hacim (göğüs/oturak) kumaşı çekiyor | Sapma o hacmin hizasından başlıyor. | İlgili çevre ölçüsü | **AF-01** Bust volume (full / small bust adjustment) |
|  |  | Parça eğri kesilmiş | Sapma tek parçada ve düzensiz. | NO_MEASUREMENT_EXISTS — physical test only | — *istisna* |
| `SYM-043` | Bir parçanın BOYU yanlış (kol, paça, etek ucu, beden) ama başka hiçbir belirti yok: kırışıklık, çekme, kayma, boşluk YOK. | Kalıbın boyu okurun boy ölçüsüne uymuyor | Giysi her yerde düzgün oturuyor, denge çizgileri doğru, hiçbir çekme/kıvrım yok — YALNIZCA uzunluk farklı. | İlgili boy ölçüsü (M-028 kol, M-024/M-025 bacak, M-015/M-016 beden) vs. kalıbın bitmiş giysi boyu | **AF-19** Overall length (lengthen / shorten lines) |
|  |  | Tasarım bilerek kısa/uzun | Kalıp teknik çizimi ve bitmiş giysi ölçü tablosu bu boyu gösteriyor. | Kalıbın bitmiş giysi ölçü tablosu | — *istisna* |
|  |  | Etek ucu/paça payı kalıbın varsaydığından farklı katlanmış | Fark, kalıbın etek ucu payı kadar; giysinin geri kalanı kalıpla birebir uyuyor. | Katlanmış etek ucu payı vs. kalıp etek ucu payı | — *istisna* |

---

## 5 · Düzeltme ailesi kapsama tablosu

| Aile | Ad | Bölge | Kitap 1'den kaç yol | Kitap 1 bölümü |
|---|---|---|---|---|
| `AF-01` | Bust volume (full / small bust adjustment) | Göğüs | 10 | B9, B10, B11, B16 |
| `AF-02` | Bust position (apex height / width, dart angle) | Göğüs | 4 | B10, B11 |
| `AF-03` | Shoulder slope (square / sloping shoulder) | Omuz | 5 | B9, B10 |
| `AF-04` | Shoulder width (narrow / broad shoulder) | Omuz | 4 | B9, B10 |
| `AF-05` | Shoulder position (forward shoulder) | Omuz | 2 | B9 |
| `AF-06` | Neckline size and shape | Boyun | 4 | B9, B10 |
| `AF-07` | Upper back (round back / broad back / narrow back) | Üst sırt | 10 | B9, B10, B11 |
| `AF-08` | Armhole depth and shape | Kol oyuntusu | 9 | B9, B10, B11, B14 |
| `AF-09` | Sleeve cap (height, shape, ease) | Kol | 5 | B14 |
| `AF-10` | Sleeve girth and length (bicep, forearm, length) | Kol | 4 | B9, B10, B14 |
| `AF-11` | Torso length and front/back balance | Bel / gövde | 13 | B9, B10, B11, B12, B13, B15, B16 |
| `AF-12` | Waist girth | Bel / gövde | 4 | B12 |
| `AF-13` | Hip and seat volume (full / flat seat, high hip) | Kalça / oturak | 13 | B10, B11, B12, B13, B15, B16 |
| `AF-14` | Sway back / lumbar hollow | Bel / gövde | 3 | B10, B12 |
| `AF-15` | Crotch depth and length | Ağ / bacak | 7 | B13, B15 |
| `AF-16` | Crotch curve shape (front / back hook) | Ağ / bacak | 4 | B15 |
| `AF-17` | Leg girth and shape (thigh, knee, calf) | Ağ / bacak | 2 | B15 |
| `AF-18` | Grading between sizes | Tüm giysi | 5 | B10, B11, B12, B13 |
| `AF-19` | Overall length (lengthen / shorten lines) | Tüm giysi | 1 | B16 |

---

## 6 · Sıra kısıtları — Kitap 2'ye taşınan kural

Kitap 1 Bölüm 16 **hangi düzeltmenin önce geldiğini** belirler; Kitap 2
her girişte bu kısıtı tekrarlar.

| # | Kural | Neden |
|---|---|---|
| 1 | **Boy → genişlik** | Boy değişince çevre ölçüleri farklı hizalara kayar |
| 2 | **Yukarıdan aşağı** | Omuz gövdenin askı noktasıdır; kayarsa altındaki her şey kayar |
| 3 | **Gövde → kol** | Kol, kol oyuntusunun türevidir |
| 4 | **`AF-08` kesinleşmeden `AF-09` yok** | Kol başı, bitmiş kol oyuntusundan hesaplanır — serinin en katı kısıtı |
| 5 | **`AF-15` → `AF-16`** | Ağ derinliği/uzunluğu (sayı) önce, ağ eğrisi (şekil) sonra |

## 7 · İÇ BÜTÜNLÜK DENETİMİ — Faz 1 yürütmesinde YAPILDI

Görev talimatı § 24 crosswalk'ın **var olduğunu bildirmenin
yetmeyeceğini** söyler. Bu yüzden 148 kaydın tamamı, `06_BUILD/qa_crosswalk.py`
ile **dokuz ayrı ilişki** üzerinden denetlendi.

| # | Denetlenen ilişki | Sonuç |
|---|---|---|
| ① | Kaynak uç noktası (belirti / aile) tanımlı mı | ✓ 148/148 |
| ② | Devir cümlesi gerçekten o belirtinin bir **aday nedenini** taşıyor mu | ✓ 129/129 |
| ③ | Hedef uç noktası (aile / blok) tanımlı mı | ✓ 148/148 |
| ④ | **İstisna mantığı iki yönlü tutarlı mı** — `to_ref=null` ⇔ `exception` dolu | ✓ 148/148 |
| ⑤ | Belirti→aile çiftleri taksonomiyle **birebir** mi (kaybolmuş veya uydurulmuş yol yok) | ✓ 129/129 |
| ⑥ | **Kitap sahipliği** tutarlı mı (`book1_entry_point`) | ✓ 129/129 |
| ⑦ | Devir cümlesi ailenin **kanonik adını** taşıyor mu (terminoloji) | ✓ 108/108 |
| ⑧ | Her giriş noktası ailesine Kitap 1'den ulaşılıyor mu | ✓ **19/19** |
| ⑨ | Her belirtinin en az bir yolu var mı | ✓ **43/43** |

**Bulgu: 0.** Hiçbir Kitap 1 yolu var olmayan bir Kitap 2 varış
noktasına işaret etmiyor; hiçbir yol boşta bitmiyor; hiçbir kayıt hem
varış noktası hem istisna taşımıyor.

### 7.1 · Bu denetimin neden AYRI bir kapı olması gerekti

`build_crosswalk.py --check` yalnızca **tazeliği** ölçer: diskteki
dosya, kaynak taksonomiden yeniden üretilenle aynı mı. Üretici kodun
kendisi yanlışsa bu denetim **hiçbir şey yakalamaz** — bayat olmayan
ama yanlış bir crosswalk sessizce geçerdi.

`qa_crosswalk.py` o boşluğu kapatır ve `07_TESTS/selftest.py` sekiz
kusurlu kurguyla kapının **gerçekten yakaladığını** kanıtlar
(`DECISIONS.md K31`).

## 8 · Doğrulama durumu — dış otorite ve fizik

İç bütünlük (§ 7) ile dış doğrulama **farklı şeylerdir** ve
karıştırılmaz.

**148 crosswalk kaydının tamamı `agent_drafted_unverified`.**
Bir crosswalk kaydının geçerliliği, kaynak belirtinin **ayırt edici
kanıtının** geçerliliğine bağlıdır; o kanıt sınıfı (`C-C`) hiçbir kamu
kaynağında bulunamadı ve fiziksel olarak sınanmadı
(`SOURCE_MAP.md § 6`).

| Katman | Durum |
|---|---|
| İç bütünlük | ✓ **DENETLENDİ — 0 bulgu** (§ 7) |
| Dış teknik otorite | ✗ **YOK** — `C-C` sınıfı için kamu kaynağı bulunamadı |
| Fiziksel sınama | ✗ **YAPILMADI** — Faz 3, `VALIDATION_PROTOCOL.md § 4.5` |

Bu, Faz 1'in açıkça kaydedilmiş sınırıdır.

---

*Vâliçe Press · TRUE FIT 1 · Diagnosis → Adjustment Map · 28 Ağustos 2026*
