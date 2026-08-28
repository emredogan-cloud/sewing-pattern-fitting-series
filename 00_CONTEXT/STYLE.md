# STYLE — yazım ve terim disiplini

> Kanonik terim sözlüğü makine-okunur: `02_TAXONOMY/terminology.json`
> (20 terim). Mekanik denetim: `06_BUILD/qa_terminology.py`.
>
> ⚠ Bu belge terimleri TANIMLADIĞI için yasak-eşanlamlı taramasından
> muaftır (`GLOSSARY_FILES`).

---

## 1 · Serinin en önemli terim ayrımı

| Terim | Ne demek | Bu seri öğretir mi |
|---|---|---|
| **pattern adjustment** | Kâğıt kalıp üzerinde, kumaş kesilmeden ÖNCE yapılan değişiklik | ✅ Evet — serinin konusu budur |
| garment alteration | Dikilmiş, bitmiş giysi üzerinde yapılan değişiklik | ❌ Hayır — kapsam dışı |
| **toile correction** | Prova giysisinde iğneyle yapılan, kalıba GERİ AKTARILAN geçici düzeltme | ✅ Evet — bir ölçüm aracıdır |

Kitap 2'nin adı (*The Adjustment Atlas*) bu ayrımı taşır. Okurun bunu
ilk bölümde öğrenmesi, tüm serinin dilini kurar.

## 2 · Kanonik biçimler ve kabul edilen varyantlar

| Kanonik | Kabul edilen varyant | Kural |
|---|---|---|
| **toile** | muslin (ABD kullanımı), test garment | Kanonik biçim `toile`; `muslin` metinde BİR KEZ eşanlamlı olarak tanıtılır ve anahtar kelime hedeflemesinde tam eşdeğer kullanılır |
| **block** | sloper (ABD kullanımı), foundation pattern | Kanonik biçim `block` (Kitap 3 başlığı); `sloper` dizinde, sözlükte ve anahtar kelimede TAM EŞDEĞER korunur. Başlıkta hangisinin duracağı `OPEN_QUESTIONS A9` |
| **fit sign** | — | Okurun GÖRDÜĞÜ, yorumlanmamış olgu. Yorum içeren adlandırmalar (bir belirtiyi "problem" diye adlandırmak) YASAK — gözlem ile teşhis karışır |
| **drag line** | — | Yönlü çekme çizgisi. Belirsiz genel kırışıklık sözcüğü yerine kullanılır |

## 3 · Sayı ve birim

- **Birim kararı VERİLDİ** (`DECISIONS.md K34`): **inç birincil**;
  figürlerde **yalnızca inç**; karar eşiklerinde ve tablolarda
  **inç + cm**.
- **Bir figürde birim karışık kullanılamaz.**
- Kesirler tek glif veya `frac` ile dizilir; inç işareti daktilo
  tırnağı değildir (`TYPOGRAPHY_STANDARD.md § 5`).
- Ölçü değeri her zaman birimiyle birlikte yazılır.
- Spread/overlap oku **sayısal etiketsiz** çizilemez.

## 4 · Kesinlik dili

| Kanıt durumu | İzinli dil | Yasak dil |
|---|---|---|
| `OBSERVED` / `FACT` | "…dır", kesin ifade | — |
| `INFERENCE` | "…gösterir", "…işaret eder" | "kanıtlanmıştır" |
| `HYPOTHESIS` | "…olabilir", "…muhtemeldir" | "…dır", "her zaman" |
| `UNVERIFIED` | Metinde KULLANILMAZ | Her şey |

`CLAIMS_STANDARD.md` bu tabloyu yasak ifadeler düzeyinde sertleştirir.

## 5 · Bölüm mimarisi kuralları

- **Bir yayılım, bir kavram.** Rakip liderin `Complexity(58)` etiketine
  verilen doğrudan cevap: okur bir sayfada tek bir şey öğrenir.
- **Ön koşul zinciri açık olur.** Her bölüm neyi varsaydığını başında
  söyler.
- **Her belirti kaydı üç şeyi birlikte verir:** ne görüyorsun · nasıl
  ayırt ediyorsun · **neyi henüz değiştirmiyorsun.**
- **Dolgu yok.** Dikiş tarihi, genel zanaat anlatısı, "sevgili okur"
  girişleri yok (`TOP-33` kapsam dışı).

## 6 · Sayı vaadi kilidi

Alt başlıkta veya kapakta bir sayı vaat edilirse ("40+ fitting
problems"), o sayı **taksonomideki gerçek kayıt sayısına** bağlanır ve
kapak/metadata kesinleşmeden önce yeniden ölçülür. Kardeş projelerden
devralınan kural — bir pazarlama sayısı içerikten kopamaz.

---

*Vâliçe Press · TRUE FIT · Style · 28 Ağustos 2026*
