# REUSE MAP — üç kitapta ne paylaşılır

> Görev talimatı § 24. Hedef: **tekrar eden kitaplar üretmeden
> yeniden kullanım ekonomisi.**
>
> Araştırma raporu § 31: *"Diyagram kütüphanesi amortize olur — bir kez
> üretilen, doğrulanmış, tutarlı ölçekli çizim sistemi üç kitapta
> yeniden kullanılır. Bu, kazananın en somut üretim avantajıdır."*

---

## 1 · Paylaşılan varlıklar

| Varlık | Nerede | Kim kurar | Kim yeniden kullanır |
|---|---|---|---|
| Ölçü çerçevesi (32 ölçü) | `02_TAXONOMY/public/measurements.json` | Kitap 1 | Kitap 2 (destek), Kitap 3 (birincil kullanıcı + kendi eklerini yapar) |
| Terminoloji (20 terim) | `02_TAXONOMY/terminology.json` | Kitap 1 | 2 ve 3 — **değiştiremez** |
| Görsel notasyon (18 token) | `03_VISUAL/visual_language_tokens.json` | Kitap 1 | 2 ve 3 — **değiştiremez** |
| Figür şeması | `03_VISUAL/figure_schema.json` | seri | üçü de |
| Düzeltme aile taksonomisi (19 aile) | `02_TAXONOMY/public/adjustment_families.json` | Kitap 2 sahiplenir, Kitap 1 adlandırır | 3 (seçici) |
| Belirti taksonomisi (43 belirti) | `02_TAXONOMY/public/fit_signs.json` | Kitap 1 | 2 (atıf), 3 (atıf) |
| Crosswalk (148 kayıt) | `02_TAXONOMY/public/crosswalk.json` | türetilmiş | üçü de |
| Kaynak sicili | `01_SOURCE/records/` | seri | üçü de |
| Fiziksel doğrulama protokolü | `00_CONTEXT/VALIDATION_PROTOCOL.md` | seri | üçü de |
| Araç zinciri (8 script) | `06_BUILD/`, `07_TESTS/` | seri | üçü de |

## 2 · Neden tek araç zinciri

Kardeş projelerin "ortak kütüphane YOK" kuralı **depolar arasında**
geçerlidir ve aynen yürürlüktedir. **Depo içinde** üç kitap tek zincir
paylaşır (`DECISIONS.md K2`).

Gerekçe: üç ayrı doğrulayıcı kopyası zamanla sapardı ve raporun
işaretlediği amortisman avantajını doğrudan yok ederdi.

## 3 · Neyin paylaşılMAdığı — tekrarı önleyen sınır

| Paylaşılmaz | Neden |
|---|---|
| Bölüm prozası | Her kitap kendi okur bağlamında yazar |
| Alıştırmalar | Teşhis alıştırması ≠ uygulama alıştırması ≠ çizim alıştırması |
| Figürlerin KENDİSİ (çoğu) | Aynı notasyon, farklı içerik. Bir figür yeniden kullanılırsa `figure_schema § reused_from` alanı ZORUNLU — sessiz kopya yok |
| Kapak sistemi | Seri kimliği paylaşılır, tasarım değil |
| Toile protokolleri | Üç farklı toile türü (`TOP-07/26/27`) |

## 4 · Yeniden kullanım fazlar arası nasıl birikir

```
KİTAP 1 phase2-visual   → notasyonu KURAR, figür motorunu YAZAR
        ↓ (miras)
KİTAP 2 phase2-visual   → notasyonu KULLANIR, yalnızca EKSİK token'ları ekler
        ↓ (miras)
KİTAP 3 phase2-visual   → aynı — en ucuz görsel faz
```

**Ölçülebilir hedef:** Kitap 2 ve 3'ün görsel fazı, Kitap 1'inkinden
belirgin biçimde kısa olmalıdır. Değilse yeniden kullanım gerçekleşmemiş
demektir ve bu, `ROADMAP_PROGRESS.md`'de izlenen bir ölçüdür.

## 5 · Yeniden kullanımın riski — tekrarlayan kitap

Ekonomiyi paylaşmak, İÇERİĞİ paylaşmak değildir. Koruma:
`SERIES_CONTENT_ARCHITECTURE.md`'nin tek-birincil kuralı ve
`qa_boundary.py`. Bir okur üç kitabı da alıp aynı sayfayı üç kez
okuduğunu hissederse seri başarısızdır — bu risk
`RISK_REGISTER R-07`'de izlenir.

---

*Vâliçe Press · TRUE FIT · Reuse Map · 28 Ağustos 2026*
