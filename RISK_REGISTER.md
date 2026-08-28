# RISK REGISTER — TRUE FIT

> Görev talimatı § 44. Araştırma raporu § 32'den devralınan riskler +
> bu depoda ortaya çıkan üretim riskleri.
>
> Her risk şunları taşır: nasıl gerçekleşir · ciddiyet · erken uyarı
> göstergesi · azaltma · sahip.

---

## R-01 · ORTAM RİSKİ — serinin en büyük riski

| | |
|---|---|
| **Nasıl gerçekleşir** | Lider ürün hibrit (QR→video). Saf basılı ürün yapısal olarak dezavantajlı olabilir. Araştırma raporu § 27'de "basılı format avantajı" iddiası **ZAYIF** çıktı. |
| **Ciddiyet** | **YÜKSEK** |
| **Erken uyarı** | Faz 3 pilot testinde okurların "video var mı?" diye sorması |
| **Azaltma** | `MEDIUM_DECISION_FRAMEWORK.md` — karar dört alt soruya bölündü; sayfa düzeni QR'a yer bırakacak biçimde tasarlanır (geri dönülebilir) |
| **Mekanik koruma** | `qa_claims.py § ②` — basılı üstünlük iddiası bir gerçek gibi yazılamaz |
| **Sahip** | Kurucu (`A4`) |

## R-02 · TALEP TAVANI RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Mutlak alıcı havuzu ölçülemedi; yalnızca açığa vurulmuş tercih (yorum sayıları) var. Yıllık havuz on binlerse üç kitaplık seri için tavan düşük olabilir. |
| **Ciddiyet** | **YÜKSEK** |
| **Erken uyarı** | Kitap 1 lansmanının ilk 90 günlük organik performansı |
| **Azaltma** | Üç kitabın da **bağımsız** arama trafiği var; seri tezi çökse bile harmanlanmış telif tek kitabın üzerinde kalıyor (araştırma raporu § 31) |
| **Sahip** | Kurucu — araştırma raporu § 35 madde 5 bunu açık bir kanıt boşluğu olarak bıraktı |

## R-03 · FARKLILAŞMA RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | "Teşhis-önce" konumlandırması kanıtlanmamış bir hipotezdir. Alıcı `Complexity(58)` şikâyetini bizim çözdüğümüzü **satın alma anında** fark etmeyebilir. |
| **Ciddiyet** | **YÜKSEK** |
| **Erken uyarı** | Faz 3 fark testi |
| **Azaltma** | Kill-gate'e bağlandı: üç okurdan en az ikisi farkı kendiliğinden söylemezse **proje durur** |
| **Sahip** | Kurucu (`A14`) |

## R-04 · TEKNİK DOĞRULUK RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | 43 belirti, 19 düzeltme ailesi, 32 ölçü — **tamamı** `agent_drafted_unverified`. Sıfır kaynak kaydı var. Teknik olarak yanlış bir bağ, okuru yanlış düzeltmeye yönlendirir. |
| **Ciddiyet** | **YÜKSEK** |
| **Erken uyarı** | Kaynak edinildiğinde ilk çapraz kontrolde çıkan çelişki sayısı |
| **Azaltma** | `verification_status` alanları mekanik olarak dayatılıyor; hiçbir kayıt kanıtsız yükseltilemiyor. Fiziksel doğrulama ikinci katman. |
| **Sahip** | Kurucu (`A3` — kaynak bütçesi) |

## R-05 · GÖRSEL ÜRETİM RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Rakipler gerçek vücut fotoğrafı kullanıyor. Saf çizgi grafiği daha ucuz ve tutarlıdır ama alıcı fotoğraf bekliyorsa dezavantajdır. Ayrıca diyagram hacmi tahminden büyük çıkabilir. |
| **Ciddiyet** | ORTA–YÜKSEK |
| **Erken uyarı** | Faz 2 sonunda deterministik üretilebilen figür oranı; Faz 3'te okur geri bildirimi |
| **Azaltma** | `figure_schema § deterministic` + `photo_required` alanları; `manual_reason` zorunlu — elle çizim yükü **ölçülüyor** |
| **Sahip** | Kurucu (`A11`) |

## R-06 · FİZİKSEL DOĞRULAMA RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Doğrulama **tek bir vücut** üzerinde ve **ürünün sahibi** tarafından yapılıyor. Bir düzeltmenin farklı vücutlarda da doğru çalıştığı bu protokolle kanıtlanamaz. |
| **Ciddiyet** | ORTA |
| **Erken uyarı** | Okur yorumlarında "bende işe yaramadı" deseni |
| **Azaltma** | Sınır `VALIDATION_PROTOCOL.md § 7`'de AÇIKÇA yazılı; hiçbir yerde bağımsız doğrulama iddia edilmiyor |
| **Sahip** | Kurucu (`A13` — kapsam) |

## R-07 · İÇERİK KAPSAMI / SERİ YEME RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Kitap 1 düzeltme adımı verirse Kitap 2 gereksizleşir; Kitap 2 blok çizimine girerse Kitap 3 gereksizleşir. Okur üç kitapta aynı sayfayı okuduğunu hissederse seri başarısızdır. |
| **Ciddiyet** | ORTA–YÜKSEK |
| **Erken uyarı** | `qa_boundary.py` sızıntı bulguları |
| **Azaltma** | Tek-birincil kuralı + topik bölme + adım dili taraması — **mekanik** |
| **Sahip** | Ajan (mekanik olarak yönetiliyor) |

## R-08 · REKABET RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Haz–Ağu 2026'da 13 yeni başlık girdi; içlerinde doğrudan uyum odaklı olanlar var. Hiçbiri traksiyon kazanmadı — ama bir sonraki kazanabilir. |
| **Ciddiyet** | ORTA–YÜKSEK |
| **Erken uyarı** | Araştırma raporu § 35 madde 6: 13 başlığın 90 günlük yorum/BSR takibi. **Bu takip BAŞLATILMADI.** |
| **Azaltma** | Takibin başlatılması Kitap 1 `phase2-visual` görevi |
| **Sahip** | Kurucu |

## R-09 · FORMAT RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Kitap 2 bir referans atlasıdır ve düz açık durmalıdır. Spiral cilt KDP'de mevcut olmayabilir veya ekonomik olmayabilir. |
| **Ciddiyet** | ORTA |
| **Erken uyarı** | Kitap 2 `phase1-spec`'te yapılacak spiral fizibilite araştırması |
| **Azaltma** | `phase6-format` doğrulama kapısı — hiçbir fiyat/telif kararı ölçüm öncesi kesinleşmez |
| **Sahip** | Kurucu (`A5`) |

## R-10 · FİYAT RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Gözlemlenen medyan $21–23. Model $26,99'da tutuldu ama garanti değil; $64,50 spiral **tek bir rakibin** başarısıdır, kural değil. |
| **Ciddiyet** | ORTA |
| **Erken uyarı** | İlk 90 günlük dönüşüm oranı |
| **Azaltma** | Fiyat bandı aralık olarak tutuluyor; tek nokta olarak kilitlenmiyor |
| **Sahip** | Kurucu |

## R-11 · REKLAM RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Dönüşüm %5'in altında kalırsa tolere edilebilir CPC $0,33–$0,53'e iner. Niş dar; ücretsiz YouTube içeriği güçlü. |
| **Ciddiyet** | ORTA |
| **Erken uyarı** | Küçük bütçeli test kampanyası |
| **Azaltma** | Yazılı iptal eşiği (`A12`): dönüşüm %5 altındaysa ücretli edinme iptal, ürün organiğe bırakılır |
| **Sahip** | Kurucu |

## R-12 · IP / MARKA RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Ticari kalıp markasının metadata'ya sızması → listeleme kaldırılabilir. Seri adı çakışması → yeniden markalama. |
| **Ciddiyet** | **DÜŞÜK ama sonucu SERT** |
| **Erken uyarı** | `validate_structure.py § check_brand_leak` |
| **Azaltma** | Mekanik tarama + `A1` marka taraması |
| **Sahip** | Kurucu (`A1`) |

## R-13 · AI İKAME RİSKİ

| | |
|---|---|
| **Nasıl gerçekleşir** | Bir dil modeli bu içeriği üretebilir hâle gelirse ürünün savunması zayıflar. |
| **Ciddiyet** | DÜŞÜK–ORTA |
| **Azaltma** | Araştırma raporu § 19: geometrik olarak doğru düzeltme diyagramı üretmek AI için zordur ve hata dikilen giyside anında görünür. Bu projenin **fiziksel doğrulama katmanı**, taklit edilmesi en zor kısımdır. |
| **Sahip** | — (yapısal) |

## R-14 · KAPI EROZYONU RİSKİ *(bu depoya özgü)*

| | |
|---|---|
| **Nasıl gerçekleşir** | Kill-gate FAIL verdiğinde kapının gevşetilmesi veya AI vekil testinin insan testi yerine sayılması. |
| **Ciddiyet** | ORTA |
| **Azaltma** | `aiProxyCountsAsHuman: false` bayrağı `kill_gate.py` tarafından ayrı bir engel olarak yakalanır; `founderOverride` ayrı bir alandır ve "geçti" diye DEĞİL, "kapıyı ilerleten ölçüm değil kurucu kararıdır" diye raporlanır (Hangıl K20 dersi) |
| **Sahip** | Ajan + Kurucu |

---

## Terk etme koşulları — ölçülebilir

Araştırma raporu § 32'den devralındı:

1. Fark testi: üç okurdan hiçbiri farkı kendiliğinden fark etmezse → **dur**
2. Fiziksel doğrulama: diyagram hata oranı **>%5** → üretim yöntemi reddedilir, **dur**
3. 13 rakip başlıktan biri 6 ayda 200+ yoruma ulaşırsa → niş kapanmış
4. Liderin `Complexity(58)` etiketi 12 ayda kaybolursa → kalite açığı kapanmış
5. Reklam testinde dönüşüm %5 altındaysa → ücretli edinme iptal
6. Kitap 3'ün bağımsız talep kanıtı zayıflarsa → seri **ikiye** indirilir

---

*Vâliçe Press · TRUE FIT · Risk Register · 28 Ağustos 2026*
