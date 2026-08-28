# PROJECT CONTEXT — TRUE FIT

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk
> belgedir.**
>
> Son güncelleme: **28 Ağustos 2026** · Seri kapısı: **`bootstrap`** ·
> Kitap kapıları: **book-01 = `foundation`**, book-02/03 = `init`
>
> **Durum: KİTAP 1 — FAZ 1 KURUCU ONAYI BEKLİYOR.**

---

## ⚠ Bu depo henüz içerik ÜRETMEDİ

| | |
|---|---|
| Yazılmış manüskript sayfası | **0** |
| Üretilmiş diyagram | **0** |
| Tasarlanmış kapak | **0** |
| KDP dosyası | **0** |
| Kaynak kaydı | **0** — bilinçli, `OPEN_QUESTIONS A3` |
| Taksonomi kaydı (belirti/aile/ölçü/blok) | **106** — tamamı `agent_drafted_unverified` |
| Crosswalk kaydı | **148** (129 teşhis→düzeltme, 19 düzeltme→blok, 21 açık istisna) |
| Görsel notasyon token'ı | **18** — `DESIGN_TARGET_NOT_CALIBRATED` |
| Fiziksel doğrulama kaydı | **0** |
| Kill-gate | **ÖLÇÜLMEDİ** — ölçüm depo dışında yapılır |

Bu belge ve bu depo, **kitapların kendisi değil, kitapları üretecek
proje işletim sistemidir.**

## 1 · Proje kimliği

| | |
|---|---|
| Seri | TRUE FIT (**ÇALIŞMA ADI** — marka taraması YAPILMADI, `A1`) |
| Kitaplar | 1 Measure & Diagnose · 2 The Adjustment Atlas · 3 Draft Your Own Block |
| Depo | yerel, GitHub'a itilmedi (`A2`) |
| Kaynak | `../KDP_2_3_BOOK_SERIES_OPPORTUNITY_RESEARCH_2026_CYCLE_2.html` § 28–32, 35–36 |
| Skor | 7,02/10 — çelişmeli inceleme sonrası birinci, dört stres testinin dördünde de birinci |
| Portföy yeri | Vâliçe Press'in **dördüncü** üretim dalı |

## 2 · Bu proje neden var

Araştırma raporunun ikinci turu 20 yeni aday taradı, 5 finalisti aynı
12 ölçütlü modelle inceledi ve çıpasız bir çelişmeli inceleme birinci
sıradakini (IEP/özel eğitim) olgusal hatalar nedeniyle yıktı. Dikiş
kalıp uyumu kazandı — yalnızca rakibi düştüğü için değil, üç ölçütte
kendi puanı da yükseldiği için.

**Pazar tartışması KAPALIDIR** (kurucu kararı). Bu depo yalnızca ürün
mimarisi ve üretimdir.

## 3 · Serinin tek cümlesi

> Bedeninde ne olduğunu **gör**, kalıpta ne yapacağını **bil**, sonunda
> kalıbı kendin **üret**.

## 4 · Mimari özet

| Katman | Ne |
|---|---|
| **İki kapı** | Seri kapısı (`.gate`) + kitap kapısı (`BOOK-xx/.gate`) — biri diğerini otomatik ilerletmez |
| **Tek araç zinciri** | Üç kitap tek doğrulayıcı seti paylaşır (depo İÇİ); hiçbir kardeş depoya bağımlılık YOK |
| **Tek-birincil kuralı** | Bir topik en fazla bir kitapta `primary` — çakışma kopyalamayla değil **topik bölmeyle** çözülür |
| **Dört basamaklı doğrulama** | `agent_drafted_unverified` → `agent_reviewed` → `technical_reference_verified` → `physically_validated`; her basamak kanıt ister |
| **İkili dış kill-gate** | Üç gerçek okurun fark testi + %0 diyagram hata oranı. **Depo içinden ölçülemez.** |

## 5 · Bu projenin üç bilinen zayıflığı — sessizce unutulmasın

### ① Sıfır kaynak, doğrulanmamış taksonomi
106 kaydın tamamı ajan taslağıdır. Teknik doğruluk **henüz hiçbir dış
otoriteye karşı sınanmadı.** `OPEN_QUESTIONS A3` bunun kurucu kararı
olduğunu ve Faz 1'in kapanış koşulu olduğunu kaydeder.

### ② Farklılaşma hipotezi kanıtlanmadı
"Teşhis-önce mimari daha anlaşılırdır" bir `HYPOTHESIS`'tir. Dayanağı
lider üründeki `Complexity(58)` etiketidir; alıcının bunu satın alma
anında fark edeceği **kanıtlanmadı.**

### ③ Ortam riski çözülmedi
Lider ürün hibrit (QR→video). "Basılı formatın avantajı" iddiası
araştırma raporunun § 27 testinde **ZAYIF** çıktı ve bu projede bir
gerçek gibi kullanılamaz (`qa_claims.py` mekanik olarak korur).

## 6 · Kapı geçmişi

| Tarih | Olay | Seri kapısı |
|---|---|---|
| 2026-08-28 | S0 Bootstrap tamamlandı | `bootstrap` |
| 2026-08-28 | S1 Seri mimarisi + Kitap 1 Faz 1 spesifikasyonu üretildi | `bootstrap` — **kurucu onayı bekliyor** |

`.gate` bilerek `bootstrap`'ta bırakılmıştır: `series-architecture`'a
yükseltme **kurucu onayına** bağlıdır (`SERIES_ROADMAP.md § S1 DoD 3`).
Kardeş projelerde de aynı disiplin uygulandı — Hangıl Faz 1 raporu
`READY_FOR_DECISION` durumunda kapıyı ilerletmemişti.

## 7 · Bir sonraki adım

**Kurucu Kitap 1 Faz 1'i onaylarsa:**
`.gate` → `series-architecture`, `BOOK-01/.gate` → `phase1-spec`,
Kitap 1 Faz 2 (`phase2-visual`) açılır.

**Onaylamazsa:** `BOOK-01/00_SPEC/PHASE_2_ROADMAP.md` yerine düzeltme
turu planlanır. Hiçbir üretim başlamaz.

---

*Vâliçe Press · TRUE FIT · Project Context · 28 Ağustos 2026*
