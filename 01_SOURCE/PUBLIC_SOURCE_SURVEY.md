# PUBLIC SOURCE SURVEY — kamu kaynağı taraması

> `OPEN_QUESTIONS A3`'ün birinci ayağı: **satın almadan önce kamu
> kaynaklarını tüket.** Bu belge taramanın kendisidir — ne arandı, ne
> bulundu, ne reddedildi ve **neden**.
>
> Tarih: **28 Ağustos 2026** · Politika:
> [`../00_CONTEXT/SOURCING_STANDARD.md`](../00_CONTEXT/SOURCING_STANDARD.md)
>
> Makine-okunur çıktı: `records/S-*.json` (15 kayıt).

---

## 0 · Sonuç — tek paragrafta

Faz 1 başlarken bu depoda **sıfır** kaynak kaydı vardı. Tarama sonunda
**15 kaynak kaydı** oluştu *(Faz 2 üç platform/lisans kaydı daha ekledi;
güncel toplam **18** — `S-0016` KDP baskı gereksinimleri, `S-0017` Adobe
Source yazı tipleri, `S-0018` yedek yazı tipi adayları. Üçü de
`technical_authority: false`'tur ve aşağıdaki teknik otorite sayısını
DEĞİŞTİRMEZ)*; bunların **altısı** teknik otorite taşıyan
ve **tam metni okunmuş** kamu kaynağıdır. Bu altı kaynak, 32 ölçünün
**16'sını** ve 19 düzeltme ailesinin **13'ünü** doğrulamaya yetti.

**Faz 1'i tamamlamak için hiçbir ücretli kaynak satın alınması gerekmedi.**
İki ücretli standart *tespit edildi ve gerekçelendirildi* ama ikisi de
Faz 1 için zorunlu değildir — bkz.
[`ACQUISITION_REQUEST_QUEUE.md`](ACQUISITION_REQUEST_QUEUE.md).

Doğrulanamayan şey de nettir: **43 belirti kaydının hiçbiri
yükseltilmedi**, çünkü bir belirti kaydının çekirdek iddiası aynı
belirtinin iki nedenini birbirinden ayıran kanıttır ve **hiçbir kamu
kaynağı bu ayrımı yapmaz.**

---

## 1 · Ne arandı — tarama eksenleri

| # | Eksen | Arama biçimi |
|---|---|---|
| 1 | ABD üniversite yayım (Cooperative Extension) uyum/kalıp düzeltme bültenleri | kurum + yayın numarası + PDF |
| 2 | Devlet antropometri teknik raporları (kamu malı) | DTIC · CDC/NCHS · NIST |
| 3 | Uluslararası/sektör beden ve ölçü standartları | ISO · ASTM · ANSI |
| 4 | Açık ders kaynağı / açık ders kitabı (OER) | OER Commons · BCcampus · OpenStax |
| 5 | Kamu malı tarihsel devlet yayınları | USDA Farmers' Bulletins · UNT · HathiTrust |
| 6 | Kurumsal arşiv taramaları | MSU Extension Publication Archive · TAMU OAKTrust |
| 7 | Platform dokümantasyonu (format/renk ekonomisi) | Amazon KDP yardım sayfaları |

## 2 · Ne bulundu — ALINDI ve OKUNDU

| Kayıt | Kaynak | Kurum | Seviye | Ne doğruladı |
|---|---|---|---|---|
| `S-0001` | Guide C-228 *Pattern Alteration* | New Mexico State Univ. Extension | `fulltext` | 11 ölçü tanımı · **ease bantları** · 13 düzeltme ailesi |
| `S-0002` | Guide C-227 *Making Perfect Pants* | New Mexico State Univ. Extension | `fulltext` | 7 ölçü tanımı (ağ dahil) · kalça tipleri · pantolon uyum listesi |
| `S-0003` | E-372 *Principles of Pattern Alteration* | Texas AgriLife Extension (Texas A&M) | `fulltext` | **Sıra kısıtı** · beden seçim eşiği · çözgü standardı · 13 maddelik uyum kontrol listesi |
| `S-0004` | EM4582 *Challenging Patterns* | Washington State Univ. Extension | `fulltext` | **Fazlalık ↔ yetersizlik ayrımı** · uyumun beş temel noktası |
| `S-0005` | ANSUR II — NATICK/TR-15/007 | U.S. Army Natick (kamu malı) | `fulltext` | İşaret noktası disiplini · omuz uzunluğu · sırt genişliği |
| `S-0006` | NHANES 2021 Anthropometry Procedures Manual | CDC / NCHS (kamu malı) | `official_pdf` | Ölçüm koşulu · tekrar-ölçüm (replicate) yöntemi |

### 2.1 · En değerli üç bulgu

**① Fazlalık ile yetersizliğin ayrımı — `S-0004`**

Washington State Üniversitesi yayımı, uyumun beş temel noktasını
sayarken şunu yazar: kumaşı **çeken ve geren** kırışıklıklar *çok az*
ease'i, **kıvrım hâlinde duran** kırışıklıklar ise *çok fazla* ease'i
gösterir.

Bu, bu kitabın en çok kullanılan kuralının (`TK-05` çekme çizgisi ↔
`TK-06` kıvrım ayrımı, Bölüm 7.4, teşhis Adım ③) doğrudan kurumsal
karşılığıdır. Ayrım *bizim icadımız değildir* — ama piyasadaki
gönüllü içerikte **sistematik olarak karıştırılmaktadır** (§ 5).

**② Sıra kısıtı — `S-0003`**

Texas AgriLife yayımı düzeltme sırasını açıkça yazar: bir seferde tek
düzeltme; önce **boy** düzeltmeleri, omuz/boyundan başlayıp aşağı
doğru; sonra **genişlik** düzeltmeleri, yine boyundan başlayıp aşağı.

Bu, Bölüm 16'nın ① (boy → genişlik) ve ② (yukarıdan aşağı) kurallarının
kaynak karşılığıdır — projenin `C-F` sınıfının ilk dış doğrulaması.

Aynı belge ayrıca şunu söyler: düzeltmeyi **sorunun kaynağında** yap —
göğüs ölçüsü kalıptan büyükse yan dikişte değil, göğsün en dolgun
yerinde büyüt. Bu, teşhis Adım ④'ün (belirtinin göründüğü yer ≠
kaynaklandığı yer) kurumsal karşılığıdır.

**③ Ease bantları — `S-0001`**

`SOURCE_MAP.md`'nin ilk sürümü `C-G` sınıfını (ease konvansiyonları)
"**kaynak olmadan yazılamaz**" diye işaretlemişti ve bunu `A3`
kararının kapsam sonucu saymıştı. NMSU Guide C-228 Table 1, adlandırılmış
bir kurumsal ease bandı tablosu verir (göğüs 3–4 inç, boyun 0,5–1 inç,
sırt 1–1,5 inç, üst kol çevresi 0,5–2 inç, kalça 2–4 inç, arka boy 1–2
inç, uyluk 1–3 inç…).

**Bu, `C-G`'yi "yazılamaz"dan "adı konmuş tek bir konvansiyonla
yazılabilir"e taşır** — ama bir sektör standardına dönüştürmez.
Sonucu ve kapsam sınırı: `DECISIONS.md K21`.

## 3 · Ne bulundu — ALINDI ama KULLANILAMADI

| Kayıt | Kaynak | Neden kullanılamadı |
|---|---|---|
| `S-0007` | MSU Extension E-419 *Fit for Fashion: The "A-B-C's"* (1963) | PDF taranmış **görüntüdür**, metin katmanı yok. Yalnızca arşiv kapağı okunabildi. Ayrıca arşivin kendi uyarısı: "do not use for current recommendations". |
| `S-0008` | MSU Extension E-421 *Fit for Fashion: Refitting and Altering* (1967) | Aynı. |

İkisi de `official_web` seviyesinde tutuldu — **bilerek**. `official_pdf`
yazmak, okunmamış bir belgeyi yükseltme kanıtı hâline getirirdi
(`SOURCING_STANDARD § 4`).

## 4 · Ne bulundu — TESPİT EDİLDİ ama İNDİRİLEMEDİ

Bunlar var oldukları **doğrulanan** ama bu turda metnine erişilemeyen
kaynaklardır. Kayıt açılmadı; künye uydurulmadı.

| Kaynak | Engel | Faz |
|---|---|---|
| Texas A&M OAKTrust *Pattern Alteration* serisinin tamamı — E-373 *Personal Measurement Chart* (17 ölçü), *Shoulder Slope*, *Hollow Chest*, *Location of Bust Fullness*, *Bodice Back Width* | Depo otomatik indirmeye kapalı (Cloudflare, HTTP 403). Serinin varlığı arama sonuçlarından ve `S-0003`'ün kendi iç atfından doğrulandı. | **Faz 2 — elle indirilebilir** |
| USDA Farmers' Bulletin *Pattern alteration* (Nisan 1945) ve *Fitting dresses* (Ocak 1945), UNT Digital Library | Katalog kaydı görüldü, tam metin bu turda alınamadı. **Kamu malı** (ABD hükümeti eseri). | **Faz 2** |
| ERIC ED355335 *Fashion Production and Management Program Guide* (Georgia) | İndirildi (234 s.) ama uyum teşhisi değil **müfredat** belgesidir; teknik iddia taşımıyor. | Reddedildi |

**Bu tablo `A3`'ün en önemli çıktılarından biridir:** Faz 2'de yapılacak
iş bir *satın alma* değil, bir *elle indirme* işidir. Maliyeti sıfırdır.

## 5 · Ne REDDEDİLDİ — ve neden

| Kaynak sınıfı | Örnek | Ret gerekçesi |
|---|---|---|
| Dikiş blogları, kalıp şirketi blogları, dergi web içeriği | çeşitli | `community_reference_non_authoritative` — `technical_authority` taşıyamaz (`SOURCING_STANDARD § 1`, mekanik: `check_source_type_authority_consistency`) |
| Rakip kitapların pazaryeri sayfaları | çeşitli | `commercial_competitor_structural` — **asla** teknik kanıt değildir |
| Korsan PDF barındıran siteler (vdoc.pub, dokumen.pub, scribd) — telifli uyum/kalıp kitaplarının tam kopyalarını sunuyorlardı | *Fitting & Pattern Alteration: A Multi-method Approach* | **Kullanılmadı.** Telifli eserin izinsiz kopyası bir kaynak değildir; `IP_AND_BRAND_POLICY § 2`. Kitabın kendisi meşru yoldan edinilebilir — bkz. `ACQUISITION_REQUEST_QUEUE A-03`. |
| Yapay zekâ hatırası | — | `SOURCING_STANDARD § 3`: hatırlanan künye yazılamaz |

### 5.1 · Reddedilen kaynaklarda gözlemlenen ÇELİŞKİ — ve neden önemli

Yatay/dikey kırışıklık kuralı için yapılan tarama, gönüllü içerikte
**birbiriyle doğrudan çelişen** üç ifade buldu:

> "Gevşek yatay kırışıklıklar giysinin çok **uzun** olduğunu, gevşek
> dikey kırışıklıklar çok **geniş** olduğunu gösterir."
>
> "Yatay kırışıklık varsa o bölge çok **küçüktür**; dikey kırışıklık
> varsa çok **büyüktür**."
>
> "Yatay çekmeler daha çok **genişlik** ister; dikey kırışıklıklar
> fazla **boy** işaretidir."

Bunlar `UNVERIFIED` ve **kanıt olarak kullanılmadı.** Ama gözlemin
kendisi kayda değer: üç ifade de aynı hatayı yapıyor — **kıvrımı
(fazlalık) çekme çizgisinden (yetersizlik) ayırmıyor.** `S-0004` bu
ayrımı yapar; gönüllü içerik yapmaz.

Bu, farklılaşma hipotezinin (`D1`) **dolaylı ve zayıf** bir destek
gözlemidir `OBSERVED` 28 Ağu 2026. Kill-gate'in yerine **geçmez**;
`DIFFERENTIATION_TEST.md`'nin ölçtüğü şey ayrıdır ve hâlâ ölçülmemiştir.

## 6 · Kapatılamayan boşluklar

| Boşluk | Neden kapanmadı | Nasıl kapanır |
|---|---|---|
| `C-C` ayırt edici kanıt (129 bağ) | Hiçbir kamu kaynağı aynı belirtinin iki nedenini ayırmıyor | **Fiziksel doğrulama** — Faz 3, `VALIDATION_PROTOCOL.md` |
| `M-004` doğal bel "en dar nokta" tanımı | ANSUR II beli yalnızca göbek hizasında tanımlar; NHANES sağlık ölçüsü verir; Extension kaynakları yol kuralı vermez | `S-0014` (ISO 8559-1) **veya** fiziksel tekrar-ölçüm çalışması |
| `M-018`, `M-019`, `M-021`, `M-022` (apeks/ön genişlik/kol oyuntusu derinliği) | Kamu kaynaklarında tanımlı değil | `S-0014` **veya** Faz 2'de indirilecek TAMU E-373 |
| `AF-05` (öne kaymış omuz), `AF-12` (bel çevresi) | Hiçbir kamu kaynağında ayrı giriş yok | `A-03` (uyum referansı) veya fiziksel doğrulama |
| Blok bileşenleri (12 kayıt) | Kamu kaynakları **düzeltme** anlatıyor, **çizim** anlatmıyor | Kitap 3 — `A10`, `BOOK-03/00_SPEC/DRAFTING_SYSTEM_RESEARCH.md` |

## 7 · Kaynaklar arası tanım FARKLARI — sessizce ezilmedi

`SOURCING_STANDARD § 7` gereği kaydedilir. Bunlar "hata" değil,
**farklı amaçlar için farklı tanımlardır** — ve üçü de Bölüm 2'nin
öğretim malzemesidir.

| Ölçü | Bu depo | Kaynak | Fark |
|---|---|---|---|
| `M-008` bilek | Bilek kemiği çevresi | `S-0001`: **elin en geniş yeri** | Kaynak, kolun içinden geçmesi gereken ölçüyü verir — farklı amaç |
| `M-013` boyun tabanı | Boyun tabanı çevresi | `S-0001`: boyun tabanının **1 inç üstü** | Yaka pervazı payı içeren bir konvansiyon |
| `M-025` iç bacak | Ağ hizası → **yer** | `S-0001`: ağ → **ayak bileği kemiği** | Farklı bitiş; paça payı ayrı hesaplanır |
| `M-004` bel | **En dar nokta** (işaretlenmiş) | `S-0005`: **göbek hizası**; `S-0006`: iliak kanat üstü | Antropometri ile ev dikişi FARKLI bel kullanır |

**Karar:** dört ölçünün hiçbiri yükseltilmedi. Bölüm 2, farkın kendisini
öğretir — "bel tek bir yer değildir; kalıbın kastettiği bel,
işaretlediğiniz beldir." Bu, kaynak çatışmasının **ürün değerine
çevrildiği** bir yerdir.

---

*Vâliçe Press · TRUE FIT · Public Source Survey · 28 Ağustos 2026*
