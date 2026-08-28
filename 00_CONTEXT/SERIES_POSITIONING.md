# SERIES POSITIONING — TRUE FIT

> Görev talimatı § 9. Hedef okur · çekirdek problem · seri vaadi ·
> farklılaşma · ürün felsefesi · üç kitabın ilişkisi.

---

## 1 · Çekirdek müşteri problemi

> **"Kalıbı doğru uyguladım. Giysi yine oturmuyor. Neden?"**

Bu bir BİLGİ problemi değildir — bilgi ücretsiz ve boldur (YouTube,
bloglar, rakip kitaplar). Bu bir **TEŞHİS** problemidir: okur ne
yapacağını değil, **NEYİ yapacağını** bilmiyor.

Piyasadaki kitaplar bir **düzeltme kataloğudur** ve okurun teşhisi
zaten koyduğunu varsayar. Alıcının gerçek sorunu ise tam olarak
teşhisin kendisidir.

## 2 · Hedef okur

**Birincil — "Doğru dikip yanlış oturtan dikişçi":**
orta seviye, dokuma kumaşla giysi diken, kalıp talimatını harfiyen
uygulayan, sonuçtan memnun olmayan ev dikişçisi. Zaten kumaşa ve kalıba
para harcamış; fiyat duyarlılığı orta.

**Bilerek optimize EDİLMEYEN:**

| Okur | Neden değil |
|---|---|
| Tam başlangıç | Dikiş öğretmiyoruz (`TOP-32` kapsam dışı). Kitap onu kaybeder ve ürün genel bir dikiş kitabına dönüşür. |
| Profesyonel terzi/kalıpçı | Akademik referanslar bu kitleye zaten hizmet ediyor ve fiyat/derinlik beklentisi farklı. |
| Örme kumaş dikişçisi | Örme uyumu farklı fizik taşır (`TOP-31` kapsam dışı, gelecek katalog yönü). |
| Erkek giyim / terzilik | `TOP-34` kapsam dışı, gelecek katalog yönü. |

⚠ Bu tanım araştırma raporundan **devralındı**; bu depoda bağımsız
olarak doğrulanmadı. Doğrulama Kitap 1 Faz 3 pilotunda yapılır.

## 3 · Seri vaadi

> Bedeninde ne olduğunu **gör**, kalıpta ne yapacağını **bil**,
> sonunda kalıbı kendin **üret**.

Üç kitap, tek bir yolculuğun üç durağıdır — ama **her durak tek başına
bir varış noktasıdır** (§ 6).

## 4 · Farklılaşma — üç iddia, üç farklı kanıt durumu

| # | İddia | Dayanak | Durum |
|---|---|---|---|
| D1 | **Teşhis-önce mimari** — rakipler katalog, biz akış şeması | Lider üründe `Complexity(58)` etiketi, n=1.797 `OBSERVED` | `HYPOTHESIS` — Faz 3 kill-gate'inde sınanır |
| D2 | **Sahte nedenleri eleme sistemi** — kumaş/kesim/yapım/basım kaynaklı belirtiler kalıp sorunu sanılmadan önce elenir (`TOP-11`, 43 belirtinin her birinde `confounders_to_rule_out`) | Rakip mimarilerinde sistematik karşılığı GÖRÜLMEDİ | `HYPOTHESIS` — rakip incelemesiyle Faz 1 kapanışında sınanacak |
| D3 | **Tek, tutarlı, deterministik çizim dili** üç kitapta | `visual_language_tokens.json` (18 token) + `figure_schema.json` | `INFERENCE` — üretim avantajı; okur tarafından fark edilmesi ayrı bir mesele |

**Farklılaşma İDDİASI OLMAYAN şey:** basılı formatın videoya üstünlüğü.
Bu iddia araştırma raporunun § 27 testinde **ZAYIF** çıktı ve bu projede
hiçbir yerde konumlandırma dayanağı olarak kullanılmaz
(`qa_claims.py § ②` mekanik olarak korur).

## 5 · Ürün felsefesi — dört kural

1. **Belirti ile nedeni asla karıştırma.** Kitap 1'in tüm veri modeli
   bu ayrımın üzerine kurulur; şema, ayırt edici kanıtı olmayan bir
   nedenin yazılmasını mekanik olarak engeller.
2. **Okura neyi HENÜZ yapmayacağını da söyle.** 43 belirtinin her
   birinde `do_not_change_yet` alanı vardır. Bir katalog kitabı okura
   ne yapacağını söyler; bu kitap ayrıca onu geri alınamaz hatalardan
   korur (kesilen kumaş geri gelmez).
3. **Her sayfa yerini hak eder.** Dikiş tarihi yok, genel zanaat
   anlatısı yok, dolgu yok (`TOP-33` kapsam dışı).
4. **Diyagram bir iddiadır, dekorasyon değil.** Her figür bir kayıttır
   ve geometrik olarak yanlış bir diyagram okurun kumaşını mahveder —
   bu yüzden fiziksel doğrulama bir KAPIDIR, bir temenni değil.

## 6 · Üç kitabın ilişkisi — bağımsız değer testi

| | Kitap 1 | Kitap 2 | Kitap 3 |
|---|---|---|---|
| Rol | GÖR | ÇÖZ | ÜRET |
| Tek başına neden alınır? | Okur ne yapacağını değil, **neyi** yapacağını bilmiyor. Teşhis olmadan katalog işe yaramaz. | Okur teşhisini **başka bir yerden** (kurs, video, deneyim) koymuş; uygulama referansı arıyor. | Kalıp/blok çizimi **kendi başına bir pazardır** — akademik bir referans $45,50'de 992 yorum taşıyor `OBSERVED`. |
| "Cilt 1/2/3 olduğu için" gerekçesi kullanıldı mı | Hayır | Hayır | Hayır |
| Bağımsız talep kanıtı | Huninin en geniş ağzı: "why doesn't my pattern fit" | İşlem niyetli aramalar: "full bust adjustment", "sway back adjustment" | `OBSERVED` Aldrich, $45,50 / 992 yorum |

**Sıra gerekçesi:** `SERIES_CROSSSELL_ARCHITECTURE.md § 1`.

## 7 · Konumlandırmanın ölçülebilir çürütme koşulları

Bu konumlandırma **yanlışlanabilir** olmak zorundadır. Çürütme koşulları
(araştırma raporu § 32'den devralındı ve `RISK_REGISTER.md`'de izlenir):

- Üç okurdan hiçbiri fark testinde farkı kendiliğinden söylemezse → D1 çürük.
- Haz–Ağu 2026'da giren 13 başlıktan biri 6 ayda 200+ yoruma ulaşırsa →
  niş bizim girişimizden önce kapanmış.
- Liderin `Complexity(58)` etiketi 12 ay içinde kaybolursa → tek
  doğrulanmış kalite açığımız kapanmış.
- Kitap 3'ün bağımsız talep kanıtı zayıflarsa → üç kitaplık yapı ikiye indirilir.

---

*Vâliçe Press · TRUE FIT · Series Positioning · 28 Ağustos 2026*
