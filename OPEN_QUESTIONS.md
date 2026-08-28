# OPEN QUESTIONS — kurucudan yanıt bekleyen kararlar

> Görev talimatı § 43. Kural (kardeş projelerden devralındı): **bir
> varsayım sessizce proje gerekliliğine dönüşemez.** Araştırma
> raporunun vermediği her şey önce buraya yazılır.
>
> Her soru şunları taşır: sahip · bağımlılık · en geç hangi fazda
> kapanmalı · gerekli kanıt · yanlış karar verilirse ne olur.

Durum tablosu · **28 Ağustos 2026** (Kitap 1 Faz 1 sonu)

---

| # | Soru | Sahip | Aciliyet | En geç | Ajan çözebilir mi | Durum |
|---|---|---|---|---|---|---|
| **A1** | "TRUE FIT" seri adı kullanılabilir mi — marka/kategori çakışması var mı | Kurucu | **YÜKSEK** | Kitap 1 `phase2-visual` öncesi | Kısmen (tarama yapar, karar veremez) | **AÇIK** |
| **A2** | Depo GitHub'a itilsin mi, public mi private mı | Kurucu | ORTA | Kitap 1 `phase2-visual` öncesi | Kısmen | **AÇIK** — bilerek yerel |
| **A3** | Teknik kaynak edinim bütçesi — otoriter kalıp/uyum referansları satın alınacak mı | Kurucu | **YÜKSEK** | Kitap 1 `phase1-spec` KAPANIŞI | **HAYIR** | **AÇIK — EN KRİTİK** |
| **A4** | Ortam kararı: QR→video eklenecek mi | Kurucu | **YÜKSEK** | Kitap 1 `phase2-visual` sonu | Kısmen (çerçeve sunar) | **AÇIK** |
| **A5** | Format: trim, cilt, spiral SKU, kâğıt, Kindle | Kurucu | ORTA | Kitap 1 `phase6-format`; spiral için Kitap 2 `phase1-spec` | Kısmen | **AÇIK** |
| **A6** | Renk stratejisi (S/B · gri tonlama · renk) | Kurucu | ORTA | Kitap 1 `phase2-visual` | Kısmen | **AÇIK** |
| **A7** | Font seçimi ve lisansı (gömme hakları) | Ajan → Kurucu (ücretliyse) | DÜŞÜK | Kitap 1 `phase2-visual` | Evet, açık kaynaksa | **AÇIK** |
| **A8** | Birim sunumu: yalnızca inç mi, inç+cm mi | Kurucu | ORTA | Kitap 1 `phase2-visual` | Kısmen | **AÇIK** |
| **A9** | Kitap 3 başlığında `block` mu `sloper` mı | Kurucu | DÜŞÜK | Kitap 3 `phase1-spec` | Kısmen | **AÇIK** |
| **A10** | Kitap 3 hangi kalıp çizim sistemini kullanacak | Kurucu (kaynak edinimine bağlı) | ORTA | Kitap 3 `phase1-spec` | **HAYIR** — A3'e bağlı | **AÇIK** |
| **A11** | Gerçek vücut fotoğrafı kullanılacak mı | Kurucu | ORTA | Kitap 1 `phase2-visual` | Kısmen | **AÇIK** |
| **A12** | Reklam testi: bütçe, kelime kümesi, iptal eşiği | Kurucu | DÜŞÜK | Kitap 1 `phase7` öncesi | Kısmen | **AÇIK** |
| **A13** | Fiziksel doğrulama kapsamı: kaç toile, hangi vücut(lar) | Kurucu | **YÜKSEK** | Kitap 1 `phase3-pilot` öncesi | **HAYIR** | **AÇIK** |
| **A14** | Fark testi katılımcıları: üç gerçek ev dikişçisi nereden bulunacak | Kurucu | **YÜKSEK** | Kitap 1 `phase3-pilot` öncesi | **HAYIR** | **AÇIK** |

---

## Ayrıntılar

### A1 · Seri adı — marka taraması

**Kanıt gereken:** kitap kategorisinde marka çakışması taraması, Amazon
seri adı taraması, yayıncılık kategorisi kontrolü.
**Yanlış karar verilirse:** seri adı üç kitabı bağlar; sonradan
değiştirmek her üçünün kapağını, metadata'sını ve kurulmuş arama
görünürlüğünü sıfırlar.
**Not:** araştırma raporu § 35 madde 7 bunu zorunlu kontrol maddesi
olarak işaretledi. **Bu turda YAPILMADI.**

### A3 · Kaynak edinim bütçesi — EN KRİTİK AÇIK SORU

**Neden kritik:** bu depoda **sıfır** kaynak kaydı vardır. 43 belirti,
19 düzeltme ailesi, 32 ölçü ve 12 blok bileşeninin **tamamı**
`agent_drafted_unverified` durumundadır.

**Ajan neden çözemez:** otoriter kalıp çizimi ve uyum referansları
büyük ölçüde satın alınması gereken basılı kitaplardır. Ajan künye
uyduramaz, hatırladığı ISBN'i yazamaz (`SOURCING_STANDARD.md § 3`).

**Yanlış karar verilirse:** teknik olarak yanlış bir düzeltme diyagramı
okurun kumaşını mahveder ve ürünün tek gerçek moat'ını (doğruluk) yok
eder — araştırma raporu § 32'nin "doğruluk riski" maddesi.

**Seçenekler:** (a) bütçe onaylanır, referanslar edinilir;
(b) yalnızca açık erişim/kurumsal kaynaklarla sınırlı kalınır ve kapsam
buna göre daraltılır; (c) fiziksel doğrulama tek doğrulama katmanı
kabul edilir ve bu ürün metninde AÇIKÇA belirtilir.
**Ajan (c)'yi tek başına seçemez.**

### A4 · Ortam kararı

Çerçeve: `00_CONTEXT/MEDIUM_DECISION_FRAMEWORK.md`. Kararsızlık hâlinde
varsayılan: **karar ERTELENİR, varsayılmaz** — sayfa düzeni QR alanına
yer bırakacak biçimde tasarlanır.

### A13 / A14 · Kill-gate lojistiği

Kitap 1'in P3 kill-gate'i **depo içinden ölçülemez**: üç gerçek ev
dikişçisi ve gerçek dikilmiş toile'ler gerekir. Bu iki soru
çözülmeden P3 **başlayamaz** — `kill_gate.py` ön koşul eksikliğini
engel olarak raporlar.

**AI vekil testi bu ölçümlerin yerine SAYILMAZ** (`DECISIONS.md K6`).
`series_config.json → killGates.differentiationTest.aiProxyCountsAsHuman`
bayrağı `false`'tur ve **açılamaz**.

---

## Kapanmış sorular

*(Henüz yok — bu, Faz 1'in ilk turudur.)*

---

*Vâliçe Press · TRUE FIT · Open Questions · 28 Ağustos 2026*
