# ROADMAP — TRUE FIT 2: The Adjustment Atlas

> **Bu yol haritası YÜRÜTÜLMEDİ.** Görev talimatı § 39 uyarınca
> planlandı ve burada durur.
>
> **Açılma koşulu:** Kitap 1'in P3 kill-gate'i **PASS**. Farklılaşma
> hipotezi çürükse üç kitap da aynı hipoteze dayanıyordu.
>
> **Kitap 1'in YAYIMLANMASINA bağımlı DEĞİLDİR** — yalnızca Kitap 1'in
> kurduğu ortak mimariye (terminoloji, ölçü çerçevesi, görsel notasyon,
> belirti taksonomisi) bağımlıdır.

---

## Faz akışı

```text
   P0 Temel  →  P1 Teknik Araştırma + Atlas Mimarisi
       │           ╞═ KURUCU ONAY ═╡
       ▼
   P2 Görsel Sistem (MİRAS — en ucuz faz)
       │
       ▼
   P3 Pilot + Prosedür Doğrulama ──[FAIL]──HARD STOP
       │  [PASS]
       ▼
   P4 Tam Atlas Üretimi  →  P5 KA  →  P6 Format (SPİRAL KAPISI)  →  P7 Lansman
```

---

## P0 — TEMEL · `foundation`

Dizin, `book_config.json`, `.gate`, kayıt defterleri. Seri
politikaları devralınır (kopya değil, atıf).

**Bağımlılık:** Kitap 1 P3 PASS · **Kurucu bağımlılığı:** DÜŞÜK

---

## P1 — TEKNİK ARAŞTIRMA + ATLAS MİMARİSİ · `phase1-spec`

**Kurucu bağımlılığı:** **YÜKSEK (onay kapısı)** · `A3`, `A5`

### Görevler

1. **Düzeltme taksonomisinin teknik doğrulaması.** 19 ailenin tamamı şu
   anda `agent_drafted_unverified`. Her aile için: yöntem ailesi doğru
   mu, sıra kısıtı doğru mu, etkileşim haritası eksiksiz mi.
2. **Aile → giriş ayrıştırması.** Her aile birden çok ATLAS GİRİŞİ
   üretir (ör. `AF-01` göğüs hacmi → FBA, SBA, pens tipine göre
   varyantlar). Kaç giriş olduğu ÖLÇÜLÜR — sayfa hedefi buradan gelir.
3. **Standart giriş şablonunun kilitlenmesi** (aşağıda).
4. **Prosedür doğrulama planı.** Her prosedür fiziksel olarak sınanır;
   hangi kalıp, hangi kumaş, hangi ölçü.
5. **Zorluk derecelendirmesi** ve önkoşul zinciri.
6. **Etkileşim haritası.** Bir düzeltmenin diğerini bozması —
   `AF-xx.interacts_with` ve `order_constraint` alanlarının
   genişletilmesi.
7. **Kitap 1 crosswalk doğrulaması.** 129 teşhis yolunun her biri gerçek
   bir atlas girişine varıyor mu.
8. **Kitap 3 köprüsü** (`TOP-20` `introduce_only`): kapanış bölümünün
   spesifikasyonu.
9. **SPİRAL FİZİBİLİTESİ** — `A5`. KDP'de spiral/wire-o seçeneği var mı,
   maliyeti ne, hangi trim'de. **Yazılı cevap zorunlu.**
10. **Erişilebilirlik testi.** Bir referans atlası ARANIR, okunmaz:
    dizin, sekme, üst bilgi ve çapraz referans sistemi tasarlanır.

### Standart giriş şablonu (Faz 1'de kilitlenir)

```text
BAŞLIK          düzeltmenin adı + AF-xx + zorluk
GÖRÜNEN BELİRTİ Kitap 1'in SYM-xxx sözlüğünden — YENİ ad ÜRETİLMEZ
OLASI NEDEN     tek cümle
KALIP BÖLGESİ   hangi parça, hangi hat
ÖN KOŞUL        önce hangi düzeltme yapılmış olmalı
YÖNTEM          slash_and_spread / pivot_and_slide / dart_manipulation / …
ADIM 1..n       her adım bir figür + bir cümle
DOĞRULA         hangi ölçü hangi değeri göstermeli + hangi belirti kaybolmalı
YAN ETKİ        bu düzeltme neyi bozar (AF-xx.interacts_with)
SIK YAPILAN HATA en az iki tanesi, TK-15 do-not-do figürüyle
```

**Sert kural:** Belirti adları Kitap 1'in kontrollü sözlüğünden alınır.
Kitap 2 **yeni belirti adı üretemez** — `qa_terminology.py` tanımsız
kimlikleri yakalar.

### Definition of Done

On görev tamamlandı · atlas giriş sayısı ÖLÇÜLDÜ · şablon kilitlendi ·
spiral fizibilitesi **yazılı** · kurucu onayı · `.gate` → `phase1-spec`.

---

## P2 — GÖRSEL SİSTEM (MİRAS) · `phase2-visual`

**Bu, serinin en ucuz görsel fazı olmalıdır.** Kitap 1'in kurduğu 18
token ve figür motoru **olduğu gibi** devralınır; yalnızca eksik
token'lar eklenir.

**Ölçülebilir hedef:** bu fazın süresi Kitap 1'in P2'sinden belirgin
biçimde kısa olmalıdır. Değilse yeniden kullanım gerçekleşmemiştir
(`REUSE_MAP.md § 4`).

Yeni ihtiyaç beklentisi: adım adım kalıp modifikasyon figürleri
(`figure_type: pattern_modification`) ve öncesi/sonrası karşılaştırma
(`comparison_before_after`) — ikisi de mevcut token'larla ifade
edilebilir olmalıdır.

---

## P3 — PİLOT + PROSEDÜR DOĞRULAMA · `phase3-pilot` · **HARD STOP**

**Kill-gate (Kitap 1'inkinden FARKLI):**

| Ölçüm | PASS koşulu | FAIL sonucu |
|---|---|---|
| **Prosedür doğruluğu** — pilot girişlerin HER adımı kalıba uygulanır, toile dikilir | Hata oranı **%0** | >%0 kök nedenden düzeltilir; **>%5 üretim yöntemi reddedilir** |
| **Uygulanabilirlik** — üç gerçek dikişçi pilot girişi **yardımsız** uygular | En az **2/3** doğru sonuca ulaşır | Şablon veya figür dili yeniden tasarlanır |

Kitap 1'in fark testi burada **tekrarlanmaz** — o hipotez zaten
sınanmıştır. Buradaki soru farklılaşma değil, **uygulanabilirliktir.**

---

## P4 — TAM ATLAS ÜRETİMİ · P5 — KA · P6 — FORMAT · P7 — LANSMAN

| Faz | Ayırt edici görev |
|---|---|
| P4 | 19 ailenin tüm girişleri; her giriş AYNI şablonda |
| P5 | Dört hat + **çapraz referans bütünlüğü** (atlas bir ağdır: her "bkz." gerçek bir girişe gitmeli) |
| P6 | **SPİRAL KAPISI** — ciltsiz + spiral iki SKU'nun maliyeti, fiyatı ve KDP mevcudiyeti ÖLÇÜLÜR; Previewer'ın kendisi çalıştırılır |
| P7 | Lansman + **Kitap 1 ile karşılıklı reklam hedeflemesi** açılır |

---

## Kitap 1'e bağımlılıklar — özet

| Ne | Ne zaman gerekir |
|---|---|
| Terminoloji (20 terim) | P1 |
| Belirti taksonomisi (43 `SYM-xxx`) | P1 |
| Ölçü çerçevesi (32 `M-xxx`) | P1 |
| Görsel notasyon (18 `TK-xx`) + figür motoru | P2 |
| Kill-gate PASS | **P0 açılışı** |
| Kitap 1'in **yayımlanması** | **GEREKMEZ** |

---

*Vâliçe Press · TRUE FIT 2 · Roadmap (planlandı, yürütülmedi) · 28 Ağustos 2026*
