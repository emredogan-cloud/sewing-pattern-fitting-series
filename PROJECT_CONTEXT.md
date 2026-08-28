# PROJECT CONTEXT — TRUE FIT

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk
> belgedir.**
>
> Son güncelleme: **28 Ağustos 2026** · Seri kapısı: **`bootstrap`** ·
> Kitap kapıları: **book-01 = `foundation`**, book-02/03 = `init`
>
> **Durum: KİTAP 1 — FAZ 1 YÜRÜTÜLDÜ, KURUCU ONAYI BEKLİYOR.**
>
> Yürütme turunun tam kaydı (20 bölüm):
> [`08_REPORTS/PHASE_1_EXECUTION_REPORT.md`](08_REPORTS/PHASE_1_EXECUTION_REPORT.md)
>
> ⚠ **Yeni ajanın önce bilmesi gereken üç şey:**
> ① `TRUE FIT` bir **çalışma adıdır ve yayımlanamaz** — aynı sektörde
> tescilli marka bulundu (`DECISIONS.md K18`).
> ② 43 belirti kaydının **hiçbiri doğrulanmadı** ve bu bilinçlidir;
> 16/32 ölçü ve 13/19 düzeltme ailesi doğrulandı (`SOURCE_MAP.md`).
> ③ Depo **public** olarak yayımlandı; adı marka-nötrdür (`K32`).

---

## ⚠ Bu depo henüz içerik ÜRETMEDİ

| | |
|---|---|
| Yazılmış manüskript sayfası | **0** |
| Üretilmiş diyagram | **0** |
| Tasarlanmış kapak | **0** |
| KDP dosyası | **0** |
| Kaynak kaydı | **15** — 6'sı teknik otorite + tam metin okunmuş; **0 satın alma** |
| Taksonomi kaydı (belirti/aile/ölçü/blok) | **106** — **29'u** `technical_reference_verified` (16 ölçü + 13 aile); **43 belirtinin hiçbiri değil** |
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

### ① Belirti–neden bağlarının hiçbiri doğrulanmadı
Ölçü ve düzeltme ailesi katmanı kısmen kapandı (16/32 ve 13/19), ama
**43 belirtinin ve 129 ayırt edici kanıtın hiçbiri** doğrulanmadı ve
**hiçbiri fiziksel olarak sınanmadı**. Hiçbir kamu kaynağı aynı
belirtinin iki nedenini ayırmıyor; bu sınıfın tek doğrulama yolu
**fiziksel sınamadır** (Faz 3, 19 kayıtlık plan hazır).

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
| 2026-08-28 | **S1 YÜRÜTME:** 14 açık kararın 12'si kapatıldı · kaynak katmanı kuruldu (15 kayıt, 0 satın alma) · taksonomi kanıta bağlandı · yeni crosswalk kapısı · depo public yayımlandı | `bootstrap` — **kurucu onayı bekliyor** |

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
