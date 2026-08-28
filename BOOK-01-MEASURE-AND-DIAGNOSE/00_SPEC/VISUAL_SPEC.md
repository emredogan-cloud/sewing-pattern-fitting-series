# BOOK-01-VISUAL-SPEC

> Faz 1 çıktısı 6/10. Görev talimatı § 25, § 36.9.
> Seri çizim dili: [`../../00_CONTEXT/VISUAL_STANDARD.md`](../../00_CONTEXT/VISUAL_STANDARD.md)
> · token sözlüğü: `03_VISUAL/visual_language_tokens.json` (18 token).
>
> **Bu belge Kitap 1'in görsel İHTİYACINI tanımlar. Hiçbir figür
> üretilmedi** — üretim Faz 2'nin (`phase2-visual`) işidir.

---

## 1 · Kitap 1'in görsel yükü — türlere göre

| Tür (`figure_type`) | Tahmini sayı | Deterministik üretilebilir mi | Not |
|---|---|---|---|
| `measurement_path` | ≥32 | **Evet** — ölçü kaydından | Her `M-xxx` için en az bir |
| `body_landmark` | 7 | Kısmen | Bölge anatomi figürleri |
| `fit_sign_on_figure` | ≥43 | Kısmen | Her `SYM-xxx` için en az bir |
| `flowchart` | 9 | **Evet** — taksonomi verisinden | 7 bölge + 1 ana şema + 1 eleme |
| `toile_state` | ~6 | Kısmen | İşaretleme, kontrol noktaları |
| `pattern_piece` | ~8 | **Evet** | Kalıptan düz ölçüm alma |
| `table_graphic` | ≥12 | **Evet** | Karşılaştırma, ease, sıra |
| `comparison_before_after` | ~6 | Kısmen | Ölçüm hatası çiftleri |
| **Toplam (tahmin)** | **~123** | | |

⚠ Bu sayılar **tahmindir**. Gerçek sayı Faz 2'de ölçülür ve
`RISK_REGISTER R-05`'in (görsel üretim hacmi) ana girdisidir.

## 2 · Kitap 1'in imza formu: AKIŞ ŞEMASI

Dokuz akış şeması bu kitabın farklılaşmasını taşıyan görsel biçimdir —
rakip mimarisi katalog, bu kitabınki akıştır.

**Yapı:**

```
  ⬭ GÖZLEM DÜĞÜMÜ (TK-17)      "Yatay kıvrım, kürek hizasında"
        │
  ◇ KARAR DÜĞÜMÜ (TK-16)       "Kol kaldırılınca kayboluyor mu?"
       ╱ ╲
   evet   hayır
     │      │
  ▭ DEVİR DÜĞÜMÜ (TK-18)       "AF-08 · Kol oyuntusu"
```

**Kurallar:**

1. Her şema **tek bir bölgeye** aittir; bölgeler arası atlama yoktur
   (atlama gerekiyorsa şema yanlış bölünmüştür).
2. Her karar düğümü **ikili** olur — üçlü dallanma yasak, iki ardışık
   ikiliye bölünür.
3. Her yol ya bir **devir düğümünde** (`AF-xx`) ya bir **eleme
   kaleminde** biter. **Boşta biten yol yasak** — `qa_boundary.py`
   kapsama denetimi bunun veri düzeyindeki karşılığıdır.
4. Bir şema tek yayılıma sığmalıdır. Sığmıyorsa **konu bölünür**, şema
   küçültülmez — doğrudan `Complexity(58)` şikâyetine verilen cevap.

## 3 · Ölçüm figürleri

Her `M-xxx` için: vücut konturu (`body_outline` 1,2 pt) + iki işaret
noktası + `TK-11` ölçüm yolu + sayısal etiket alanı.

**Zorunlu:** başlangıç ve bitiş işaret noktaları **görünür** olmalı.
Ölçüm yolu bir çizgi olarak gösterilip uçları belirsiz bırakılamaz —
"nereden nereye" sorusu figürden cevaplanabilir olmalıdır.

**Altı hata figürü** (Bölüm 2.6) `TK-15` do-not-do işareti taşır ve
doğru versiyonuyla **yan yana** durur (`comparison_before_after`).

## 4 · Belirti figürleri

Her `SYM-xxx` için giysi üzerinde belirtinin gösterimi:

| Belirti sınıfı | Token |
|---|---|
| Çapraz çekme çizgisi | `TK-05` — ok KAYNAĞA bakar |
| Yatay / dikey kıvrım | `TK-06` — paralel yay kümesi |
| Gerginlik / açıklık | `TK-07` — seyrek nokta tramı |
| Dikiş kayması | `TK-09` referans + kayma oku |
| Çözgü bozulması | `TK-10` + `TK-09` |

**Kritik ayrım:** `TK-05` (çekme çizgisi) ile `TK-06` (kıvrım) görsel
olarak **açıkça** farklı olmalıdır. Bu ayrım Bölüm 7'nin çekirdeğidir;
figürler onu bulanıklaştırırsa bölüm çalışmaz.

## 5 · Fotoğraf sorusu — Kitap 1'e özgü

| Figür türü | Fotoğraf faydası | Karar |
|---|---|---|
| Ölçüm yolu | Düşük — geometri yeterli | Çizgi grafiği |
| Ölçüm **hatası** | **Yüksek** — hata bir duruş/hareket meselesi | `photo_required` adayı |
| Belirti tanıma | **Yüksek** — gerçek kumaşta farklı görünür | `photo_required` adayı |
| Kalıp parçası | Yok | Çizgi grafiği |
| Akış şeması | Yok | Çizgi grafiği |

**Karar VERİLMEDİ** — `../../OPEN_QUESTIONS.md → A11`. Rakipler gerçek
vücut fotoğrafı kullanıyor; saf çizgi grafiği daha ucuz ve tutarlıdır
ama alıcı fotoğraf bekliyorsa dezavantajdır (`RISK_REGISTER R-05`).

Fotoğraf kullanılırsa: dosyalar depoya **girmez**
(`CONTENT_PROTECTION.md § 2`), yalnızca figür kaydı public kalır.

## 6 · Sayfa yerleşimi kuralı — bir yayılım, bir kavram

Bu kural doğrudan `Complexity(58)` etiketine verilen cevaptır:

- Bir yayılımda **tek** bir kavram öğretilir.
- Belirti girişi ve figürü **aynı yayılımda** durur; okur sayfa
  çevirerek karşılaştırmaz.
- Akış şeması **bölünmez**.
- Ölçüm figürü ve ölçüm talimatı **aynı yayılımda**.

Bu kural sayfa sayısını artırır ve bu **kabul edilmiş bir maliyettir**.

## 7 · Faz 2'de ölçülecekler — çıkış ölçütleri

| Ölçüt | Neden |
|---|---|
| Deterministik üretilebilen figür **oranı** | Yeniden kullanım ekonomisinin temeli |
| Ortalama figür üretim süresi | `RISK_REGISTER R-05`'in gerçek büyüklüğü |
| `manual_reason` taşıyan figür sayısı | Elle çizim yükü |
| Bir yayılıma sığmayan şema sayısı | Konu bölme ihtiyacı |
| `photo_required` işaretli figür sayısı | `A11` kararının maliyeti |

---

*Vâliçe Press · TRUE FIT 1 · Visual Spec · 28 Ağustos 2026*
