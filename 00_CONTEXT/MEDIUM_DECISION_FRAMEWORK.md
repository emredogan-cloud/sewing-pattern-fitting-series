# MEDIUM DECISION FRAMEWORK — QR / video kararı

> Görev talimatı § 27. **Bu belge kararı VERMEZ.** Karar çerçevesini,
> kanıt gereksinimini ve karar sahibini tanımlar. Karar:
> `OPEN_QUESTIONS A4`.
>
> ⚠ Bu belge korunan iddiayı TARTIŞTIĞI için `qa_claims.py`'den muaftır.

---

## 1 · Neden bu proje "video ekleyelim" diyemez ve "eklemeyelim" de diyemez

**Ekleme yönünde kanıt:** Lider ürün (n=958) hibrit. Müşteri
etiketlerinde `Video content` bir GÜÇ olarak anılıyor ve "neredeyse her
sayfada QR kodu" öne çıkarılıyor `OBSERVED` 27 Ağu 2026. Araştırma
raporu § 32 ortam riskini **serinin en büyük riski (Yüksek)** olarak
işaretledi.

**Eklememe yönünde kanıt:** Yok. Araştırma raporunun § 27 girdi
geçerliliği testinde "basılı formatın gerçek bir avantajı var" iddiası
sınandı ve **ZAYIF** çıktı. Bu iddia bu projede bir gerekçe olarak
kullanılamaz (`CLAIMS_STANDARD.md § 2`).

**Yani:** karar kanıtla verilemez durumda. Bu belge o boşluğu
kapatmanın YOLUNU tanımlar.

## 2 · Karar dört ayrı soruya bölünür

Bunları tek bir "video ekleyelim mi" sorusu olarak sormak hatadır.

| # | Soru | Nasıl cevaplanır |
|---|---|---|
| S1 | Hangi içerik basılı sayfada **daha iyi** çalışır? | İçerik türü analizi (§ 3) |
| S2 | Hangi içerik hareketli gösterim **gerektirir**? | Aynı analiz |
| S3 | QR bağlantısı okur için **gerçekten** kullanışlı mı, yoksa rakip taklidi mi? | Faz 3 pilot testi — okura sorulur |
| S4 | Bakım yükü ve bağlantı ölümü riski kabul edilebilir mi? | Maliyet tahmini + terk stratejisi |

## 3 · İçerik türü analizi — ilk taslak

| İçerik türü | Basılı | Hareketli | Gerekçe |
|---|---|---|---|
| Ölçü alma yolu (şerit metrenin izlediği yol) | ✅ | ○ | Statik geometri; diyagram yeterli |
| Ölçü alma HATASI (şeridin kayması, duruş bozulması) | ○ | ✅ | Hata bir **hareket**tir; durağan görüntüde görünmez |
| Belirti tanıma (kırışıklık deseni) | ✅ | ○ | Durağan; ama gerçek kumaşta farklı görünebilir |
| Belirtinin hareketle ORTAYA ÇIKMASI (kol öne uzatınca sırt çekmesi) | ○ | ✅ | Tanımı gereği hareketli |
| Teşhis akış şeması | ✅ | ✕ | Kitap 1'in imza formu; video buna hizmet edemez |
| Kalıp üzerinde kes-ve-aç (Kitap 2) | ✅ | ○ | Adım adım durağan; ama sıralama hatası videoda daha görünür |
| Toile üzerinde iğneleme | ○ | ✅ | El becerisi; hareketli gösterim belirgin avantaj |
| Blok çizim sırası (Kitap 3) | ✅ | ○ | Uzun ve tekrarlı; basılı referans daha kullanışlı |

`✅` açık üstünlük · `○` çalışır ama üstün değil · `✕` uygun değil

**Bu tablo bir TASLAKTIR** ve Faz 3 pilotunda gerçek okurlarla test
edilir.

## 4 · Terk stratejisi zorunludur

Karar "evet" olursa, şu üç şey **karardan önce** yazılı olmalıdır:

1. **Bağlantı ölümü planı** — barındırma durursa QR'ı olan basılı
   kitaplar ne olur? (Kalıcı yönlendirme alan adı? Kitap videosuz da
   tam işlevli mi?)
2. **Bakım bütçesi** — video güncelleme, barındırma, alt yazı.
3. **Bağımsızlık testi** — kitap, videolara HİÇ erişilmeden tam
   değerini veriyor mu? Vermiyorsa ürün bir kitap değil, bir kursun
   broşürüdür.

**Sert kural:** hangi karar verilirse verilsin, basılı kitap videolara
erişilmeden **tam işlevli** olmalıdır. Bu, ortam kararından bağımsız,
ürünün kendisi hakkında bir karardır.

## 5 · Karar kapısı

| | |
|---|---|
| Karar sahibi | Kurucu |
| Kayıt | `OPEN_QUESTIONS A4` |
| En geç ne zaman | Kitap 1 `phase2-visual` sonu — çünkü ortam kararı sayfa düzenini ve figür sayısını etkiler |
| Gerekli kanıt | § 3 tablosunun pilot testiyle doğrulanması + § 4'ün üç maddesinin yazılı olması + maliyet tahmini |
| Kararsızlık hâlinde varsayılan | **Karar ERTELENİR, varsayılmaz.** Sayfa düzeni QR alanı için yer BIRAKACAK biçimde tasarlanır (geri dönülebilir seçenek) |

---

*Vâliçe Press · TRUE FIT · Medium Decision Framework · 28 Ağustos 2026*
