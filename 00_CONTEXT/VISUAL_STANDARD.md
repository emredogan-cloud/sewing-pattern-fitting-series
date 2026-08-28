# VISUAL STANDARD — TRUE FIT çizim dili

> Görev talimatı § 9 ve § 25. Makine-okunur kaynak:
> `03_VISUAL/visual_language_tokens.json` (18 token) ve
> `03_VISUAL/figure_schema.json`.
>
> ⚠ **DURUM: `DESIGN_TARGET_NOT_CALIBRATED`.** Bu belgedeki her sayısal
> değer (çizgi kalınlığı, kesik desen, etiket boyutu) bir TASARIM
> HEDEFİDİR, ölçülmüş sonuç değil. Kalibrasyon Kitap 1 Faz 2
> (`phase2-visual`) içinde gerçek render testiyle yapılır.

---

## 1 · Neden bu belge en önemli üretim varlığıdır

Araştırma raporu § 31, diyagram kütüphanesinin üç kitapta amortize
olmasını **kazananın en somut üretim avantajı** olarak işaretledi. Bu
avantaj yalnızca tek bir koşulda gerçekleşir: **çizim dili bir kez
kurulur ve üç kitapta değişmez.**

`TOP-29` uyarınca notasyonu Kitap 1 kurar; Kitap 2 ve 3 yeniden
kullanır ve **değiştiremez**.

## 2 · Temel ilke: bir figür bir İDDİADIR

Her figür bir kayıttır (`figure_schema.json`) ve şu alanları taşır:
ne gösterdiği, hangi token'ları kullandığı, deterministik olarak
üretilebilir mi, hangi teknik iddiaya bağlı, fiziksel olarak
doğrulandı mı.

**Geometrik olarak yanlış bir düzeltme diyagramı okurun kumaşını
mahveder** (`RISK_REGISTER R-06`). Bu yüzden:

> Bir figür "doğru göründüğü için" doğru sayılamaz.
> `verification_status: physically_validated` bir `VAL-xxxx` kaydına
> bağlı olmadan yazılamaz — `validate_spec.py § check_figure_tokens`
> mekanik olarak dayatır.

## 3 · Çizgi hiyerarşisi — kalınlık ANLAMDIR

| Rol | Hedef (pt) | Anlamı |
|---|---|---|
| `body_outline` | 1,2 | Vücut konturu |
| `pattern_edge_original` | 1,0 | Değişiklik ÖNCESİ kalıp kenarı |
| `pattern_edge_modified` | 1,6 | Değişiklik SONRASI kalıp kenarı |
| `garment_outline` | 1,0 | Giysi konturu |
| `balance_line` | 0,7 | Denge çizgisi |
| `grainline` | 0,9 | Çözgü çizgisi |
| `seam_line` | 0,6 | Dikiş çizgisi |
| `construction_line` | 0,5 | Yardımcı çizgi |
| `callout_leader` | 0,4 | Etiket bağlayıcısı |

**Kural:** kalınlık dekoratif amaçla DEĞİŞTİRİLEMEZ. Aynı kalınlık
üç kitapta aynı anlamı taşır.

## 4 · On sekiz token — özet

Tam tanımlar `visual_language_tokens.json`'dadır. Kritik olanlar:

| Token | Ne | Neden ayrı |
|---|---|---|
| `TK-01` slash line | Kesilecek çizgi | Yalnızca kalıpta; vücut figüründe ASLA |
| `TK-02` / `TK-03` spread/overlap arrow | Açma / daraltma | **Sayısal etiketsiz çizilemez** |
| `TK-04` pivot point | Döndürme merkezi | `TK-08` apeks işaretinden GÖRSEL OLARAK ayrıdır |
| `TK-05` drag line | Yönlü çekme | Ok, kırışıklığın işaret ettiği KAYNAĞA bakar |
| `TK-06` excess fold | Kıvrım/fazlalık | `TK-05`'ten ayrı — teşhiste farklı anlam |
| `TK-09` balance line | Yer düzlemine göre referans | `TK-10` grainline DEĞİLDİR |
| `TK-12` / `TK-13` before/after | Değişiklik durumu | Renk değil TON/kalınlık farkı (1-bit baskı güvenliği) |
| `TK-15` do-not-do marker | Yanlış uygulama | Okur yanlışı doğru sanmamalı — ZORUNLU |
| `TK-16` / `TK-17` / `TK-18` | Karar / gözlem / devir düğümü | Kitap 1'in imza formu: akış şeması |

## 5 · Yasaklar

- Dekoratif çerçeve, süsleme, arka plan deseni
- Anlam taşımayan gri dolgu
- Aynı sayfada iki farklı ok stilinin aynı anlamı taşıması
- Ölçek belirtilmemiş kalıp parçası
- Sayısal etiketi olmayan spread/overlap oku
- Gerçek marka adı taşıyan kalıp zarfı/talimat görseli
  (`IP_AND_BRAND_POLICY § 1`)

## 6 · Fotoğraf sorusu — AÇIK KARAR

Araştırma raporu § 22 ve § 32 bunu bir **risk** olarak kaydetti:
rakipler gerçek vücut fotoğrafı kullanıyor; saf çizgi grafiği daha ucuz
ve daha tutarlıdır ama **alıcı fotoğraf bekliyorsa dezavantajdır**.

Bu proje kararı VERMEZ; `OPEN_QUESTIONS A11`'e bağlar ve `figure_schema.json`
her figürde bir `photo_required` alanı taşır. Fotoğraf gerektiren
figürler **ayrı bir üretim ve gizlilik hattıdır** — fotoğraflar depoya
girmez (`CONTENT_PROTECTION.md § 3`).

## 7 · Birim kararı — AÇIK

Hedef pazar ABD'dir. İki birimli (inç + cm) sunum kararı **verilmedi**
(`OPEN_QUESTIONS A8`). Kural, karar hangisi olursa olsun geçerlidir:

> Bir figürde birim ASLA karışık kullanılmaz. İkili sunumda ikincil
> birim parantez içindedir ve figür boyunca tutarlıdır.

## 8 · Determinizm hedefi

Araştırma raporu § 22, kalıp düzeltme diyagramlarını "saf çizgi
grafiği — deterministik render için ideal" diye işaretledi. Hedef:
figürlerin **kayıt verisinden otomatik üretilmesi**.

`figure_schema.json § deterministic: false` olan her figür bir
`manual_reason` taşımak ZORUNDADIR — elle çizim gerekçesiz olamaz.
Deterministik oranının ölçülmesi Faz 2'nin çıkış ölçütlerinden biridir.

---

*Vâliçe Press · TRUE FIT · Visual Standard · 28 Ağustos 2026*
