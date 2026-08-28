# SERIES CROSS-SELL ARCHITECTURE

> Görev talimatı § 9, § 20–23. Kitaplar arası geçiş, bağımsız kullanım
> senaryoları ve sıralı satın alma gerekçeleri.
>
> Makine-okunur devir haritası: `02_TAXONOMY/public/crosswalk.json`
> (148 kayıt) — `06_BUILD/build_crosswalk.py` tarafından türetilir.

---

## 1 · Neden bu sıra: 1 → 2 → 3

| Karar | Gerekçe | Alternatif neden reddedildi |
|---|---|---|
| **Kitap 1 neden teşhis?** | En düşük giriş bariyeri (ön koşul bilgi gerektirmez) ve en geniş huni ağzı ("why doesn't my pattern fit"). Okur problemi hissediyor, adını bilmiyor. | Katalogla başlamak, okurun zaten teşhis koyabildiğini varsayar — bu varsayım tam olarak rakiplerin `Complexity(58)` şikâyetini üreten şeydir. |
| **Kitap 2 neden ikinci?** | Teşhisin doğrudan ve kaçınılmaz devamı: "artık ne olduğunu biliyorum, nasıl yapılır?" Ayrıca serinin en yüksek birim telifi burada (spiral SKU adayı). | Blok çizimini ikinci sıraya koymak, okuru henüz çözemediği somut bir sorunla baş başa bırakır. |
| **Kitap 3 neden son?** | En yüksek beceri eşiği ve en yüksek fiyat noktası. Önce gelirse okuru korkutur; sonra gelirse Kitap 1–2'nin kurduğu güvenle satılır. | — |
| **Neden dördüncü kitap yok?** | Doğal genişleme yönleri var (örme kumaş, erkek giyim, terzilik) ama bu turun kapsamı üçtür. `TOP-31`/`TOP-34` bilerek kapsam dışı. | — |

**Bağımlılık zinciri doğrulaması:** Kitap 2 ve Kitap 3, Kitap 1'in
**yayımlanmasına** bağımlı DEĞİLDİR; yalnızca Kitap 1'in **ortak
mimarisine** (terminoloji, ölçü çerçevesi, görsel notasyon) bağımlıdır.
Bu ayrım seri yol haritasının paralelleşme kuralını mümkün kılar —
`SERIES_ROADMAP.md § 4`.

## 2 · Kitap 1 → Kitap 2 — TEŞHİS → DÜZELTME devri

Devir noktası **her belirti kaydının içine gömülüdür**: her aday neden
bir `adjustment_family_ref` (AF-xx) taşır veya taşımadığının gerekçesini
yazar.

**Kapsam ölçümü (Faz 1 sonu):**

| Metrik | Değer |
|---|---|
| Kitap 1 belirtisi | 43 |
| Aday neden | 129 |
| Kitap 2'ye giden yol | 108 |
| Açık istisna (Kitap 2 karşılığı YOK) | 21 |
| Kitap 1'den ulaşılabilen düzeltme ailesi | 19 / 19 |

**İstisnalar neden değerlidir:** 21 nedenin Kitap 2'de karşılığı
YOKTUR — çünkü bunlar kalıp sorunu değildir: yapım hatası, eğri kesim,
prova koşulu hatası veya bir TASARIM tercihi. Kitap 1'in bunları
ayırabilmesi, okuru **gereksiz bir düzeltmeden** korur. Bu, satılan
değerin bir parçasıdır ve rakip mimarilerinde sistematik karşılığı
görülmedi (`SERIES_POSITIONING.md § D2`).

**Devir cümlesinin biçimi** (Kitap 1'in akış şemalarının bitiş formu,
görsel token `TK-18`):

> Belirti `SYM-016` + ayırt edici kanıt → **AF-01 · Bust volume**
> → *Bu düzeltmenin adım adım uygulaması: TRUE FIT 2, Bölüm «Bust».*

## 3 · Kitap 2 → Kitap 3 — DÜZELTME → BLOK devri

Devir tetikleyicisi bir **tekrar farkındalığıdır**:

> "Aldığım her kalıpta aynı üç düzeltmeyi yapıyorum."

19 düzeltme ailesinin 18'i bir blok bileşenine karşılık gelir; biri
(`AF-18` beden dereceleme) **bilerek karşılıksızdır** — blok tek
bedendir, dereceleme kavramı orada yoktur. Bu bir eksik değil, Kitap
3'ün tanımıdır ve en güçlü satış argümanlarından biridir.

## 4 · Kitap 1 → Kitap 3 (atlamalı yol)

Nadir ama gerçek: teşhisini koymuş, ticari kalıpları düzeltmekle
uğraşmak istemeyen okur doğrudan bloğa geçebilir. Kitap 3 bunu
destekler — Kitap 2'yi **ön koşul saymaz**; yalnızca Kitap 1'in ölçü
çerçevesini ve terminolojisini varsayar (`TOP-01`, `TOP-28` üzerinden
`reference_only`).

Bu yol reklam hedeflemede **kullanılmaz** (dönüşümü düşük olması
beklenir, `HYPOTHESIS`), ama içerik mimarisinde **engellenmez**.

## 5 · Bağımsız giriş kapıları

Her kitap kendi başına bir giriş kapısıdır — seri sırasına girmeden:

| Kitap | Bağımsız giriş senaryosu |
|---|---|
| 1 | Okur ilk kez "neden oturmuyor" diye arıyor |
| 2 | Okur teşhisini bir kurstan/videodan öğrenmiş, referans arıyor |
| 3 | Okur doğrudan kalıp çizimi öğrenmek istiyor (bağımsız pazar, `OBSERVED` $45,50 / 992 yorum) |

**Kural:** hiçbir kitap, diğerini okumamış birine "önce diğerini oku"
demez. Ön koşul bilgisi **kitabın içinde** kısaca verilir veya bir
çapraz referansla işaretlenir — asla bir satın alma engeli olarak
kurulmaz.

## 6 · Bağlanma oranı — ÖLÇÜLMEDİ

Araştırma raporu § 31 dört senaryo modelledi (%5/%2 … %35/%20) ve
hepsini **`ESTIMATE`** olarak etiketledi. Bu depoda hiçbir bağlanma
oranı gerçek sayılmaz. Ölçüm ancak Kitap 2 yayımlandıktan sonra
mümkündür ve `SERIES_ROADMAP.md`'nin `catalog` kapısının girdisidir.

Raporun kritik gözlemi devralındı: seri tezi neredeyse tamamen yanlış
çıksa bile harmanlanmış telif tek kitabın üzerinde kalır — çünkü Kitap
2 ve 3'ün **bağımsız** arama trafiği vardır.

---

*Vâliçe Press · TRUE FIT · Series Cross-sell Architecture · 28 Ağustos 2026*
