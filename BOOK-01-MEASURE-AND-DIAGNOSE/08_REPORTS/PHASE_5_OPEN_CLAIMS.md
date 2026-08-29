# BOOK 1 — PHASE 5 — OPEN CLAIMS

> Ölçüm: `python3 06_BUILD/build_claims.py --check` · 2026-08-29
> Kaynak: `BOOK-01-MEASURE-AND-DIAGNOSE/02_CONTENT/public/claims.public.json`
>
> **Bu belgedeki her sayı iddia sicilinden OKUNUR.** Sicil taksonomiden
> üretilir; elle yazılmış ikinci bir kopya yoktur (`DECISIONS.md K33`).

---

## 0 · Tek cümlelik durum

> **307 izlenen maddi iddianın 56'sı `VERIFIED`, 251'i AÇIK.**
> Açık iddiaların ezici çoğunluğu (`INFERRED`, 214) kitabın TEZİNİ
> oluşturan belirti→neden ilişkileridir. Bunları kapatacak şey daha iyi
> bir kaynak değil, **fiziksel testtir** (`D-02`) — ve o test HENÜZ
> YAPILMADI.

## 1 · Sayım

| Kanıt düzeyi | Sayı | Ne demek |
|---|---:|---|
| `VERIFIED` | 56 | Tam metni okunmuş teknik otorite kaydı destekliyor |
| `INFERRED` | 214 | Yerleşik uygulamadan türetildi; İÇ tutarlılığı denetlendi, DIŞ doğrulaması yok |
| `UNVERIFIED` | 29 | Kayıtlı kaynağı YOK; sicil bunu beyan etmek ZORUNDA |
| `CONTESTED` | 8 | Kaynaklar birbiriyle ÇELİŞİYOR; kitap çelişkiyi yazıyor, taraf tutmuyor |
| **Toplam** | **307** | |

### Açık iddialar, türüne göre

| Kanıt düzeyi | Tür | Sayı |
|---|---|---:|
| `CONTESTED` | `measurement_definition` | 4 |
| `CONTESTED` | `measurement_path` | 4 |
| `INFERRED` | `adjustment_family` | 6 |
| `INFERRED` | `adjustment_order` | 6 |
| `INFERRED` | `conceptual` | 24 |
| `INFERRED` | `measurement_definition` | 3 |
| `INFERRED` | `measurement_path` | 3 |
| `INFERRED` | `sign_cause` | 129 |
| `INFERRED` | `sign_observation` | 43 |
| `UNVERIFIED` | `adjustment_family` | 2 |
| `UNVERIFIED` | `adjustment_order` | 2 |
| `UNVERIFIED` | `conceptual` | 7 |
| `UNVERIFIED` | `measurement_definition` | 9 |
| `UNVERIFIED` | `measurement_path` | 9 |

---

## 2 · `CONTESTED` — 8 iddia, dört ölçü

Kitabın **taraf tutmayı reddettiği** yerler. Her ölçü iki kayıt sayılır:
ölçünün TANIMI ve şeridin YOLU.

| İddia | Ölçü | Kaynaklar |
|---|---|---|
| `CLM-0038` | `M-004` — Natural waist is measured from narrowest point of the to | `S-0002`, `S-0003` |
| `CLM-0039` | `M-004` — Natural waist: the tape path is constrained, not free (s | `S-0002`, `S-0003` |
| `CLM-0046` | `M-008` — Wrist is measured from wrist bone to around the wrist ba | `S-0001` |
| `CLM-0047` | `M-008` — Wrist: the tape path is constrained, not free (see the r | `S-0001` |
| `CLM-0054` | `M-013` — Neck base is measured from base of the neck to around th | `S-0001` |
| `CLM-0055` | `M-013` — Neck base: the tape path is constrained, not free (see t | `S-0001` |
| `CLM-0078` | `M-025` — Inseam is measured from crotch level to floor. | `S-0001` |
| `CLM-0079` | `M-025` — Inseam: the tape path is constrained, not free (see the  | `S-0001` |

**Dördü de okura BEYAN EDİLİYOR.** Ek F ("Where the evidence stands")
anlaşmazlıkları adıyla sayar: belin nerede olduğu, bileğin nereden
ölçüldüğü, boyun tabanının nerede olduğu, iç dikişin nerede bittiği.
Bu dört ölçünün figürü metinde **"Sources differ — see the note in
Chapter 2"** notuyla basılır (Faz 5'te dört sayfada da doğrulandı).

| Soru | Yanıt |
|---|---|
| Yayını engelliyor mu | **HAYIR** — çelişki gizlenmiyor, yazılıyor. |
| Fiziksel test çözer mi | **HAYIR** — bu bir TANIM anlaşmazlığı, ölçüm hatası değil. |
| İnsan testi çözer mi | **KISMEN** — `D-01` iki tanımın okuru farklı sonuca götürüp götürmediğini ölçebilir. |
| Daha iyi kaynak çözer mi | **EVET** — `S-0014` (ISO 8559-1) ve `S-0015` (ASTM D5219) EDİNİLMEDİ ve tam olarak bu tanımları yönetir. → `D-07` |

---

## 3 · `UNVERIFIED` — 29 iddia, kaynağı olmayan

| Tür | Sayı | Neden kaynaksız |
|---|---:|---|
| `conceptual` | 7 | Kitabın KENDİ yöntem kuralları (kıvrımın yönünün ne anlattığı, hemin en son okunması, ev baskısının doğrulanması). Kamu kaynağı bunları bu biçimde yazmıyor. |
| `measurement_definition` + `measurement_path` | 18 | Dokuz ölçünün kaydında kaynak yok: `M-010` diz · `M-011` baldır · `M-018` apeks arası · `M-019` apeks–bel · `M-021` ön genişlik · `M-022` kol oyuntusu derinliği · `M-030` boy · `M-032` ön/arka fark · `M-033` bel–kalça farkı |
| `adjustment_family` + `adjustment_order` | 4 | İki ailenin kaynak kaydı yok |

| Soru | Yanıt |
|---|---|
| Yayını engelliyor mu | **HAYIR** — ama sicil bunları `UNVERIFIED` taşımak ZORUNDA; `selftest.py` "kaynaksız iddia UNVERIFIED" denetimiyle bunu dayatıyor. |
| Fiziksel test çözer mi | Ölçüler için **KISMEN**: TEKRARLANABİLİRLİK ölçülebilir, DOĞRULUK ölçülemez. |
| İnsan testi çözer mi | Kavramsal kurallar için **EVET** (`D-01` / `D-05`). |
| Daha iyi kaynak çözer mi | **EVET** → `D-07`. |

---

## 4 · `INFERRED` — 214 iddia, kitabın TEZİ

Bu grup kitabın kendisidir: **43 belirti gözlemi · 129 aday neden ·
20 aile · 20 sıra kuralı · 24 kavramsal kural · 6 ölçü kaydı.**

Hiçbiri uydurulmadı; yerleşik uyum uygulamasından türetildi ve iç
tutarlılığı dokuz crosswalk denetimi, on dört manüskript denetimi ve
**182 kapı testiyle** sınandı. Ama:

> **Bir belirtinin bir nedene bağlanmasının İÇ tutarlılığı, o bağın
> gerçek bir bedende gerçek bir kumaşla TUTACAĞI anlamına gelmez.**
> Bunu yalnızca `D-02` gösterebilir.

| Soru | Yanıt |
|---|---|
| Yayını engelliyor mu | **`D-02` yapılana kadar EVET.** Kill-gate bu yüzden kapalı. |
| Fiziksel test çözer mi | **EVET — birincil yol budur.** 19 `VAL` kaydı HAZIR; **0'ı yapıldı**. |
| İnsan testi çözer mi | **KISMEN**: `D-01` okurun AYIRT EDEBİLDİĞİNİ ölçer, ilişkinin DOĞRU olduğunu değil. |
| Daha iyi kaynak çözer mi | **HAYIR.** Faz 4 bağımsız incelemesi 68 kaynağa danıştı; 149 bulgunun 56'sı `CONTRADICTED` çıktı. Kaynak katmanı TÜKETİLDİ. |

### İçindeki en sert alt küme: 28 kanıt çakışması

43 belirtinin **28'inde** iki aday neden okura AYNI görünür ve
kitabın sunduğu ayırt edici kanıt onları **güvenilir biçimde ayırMAZ**.

Bu, uydurulmuş bir ayrımla kapatılMADI. Okura SÖYLENDİ: her birinde
**"THESE TWO CAN LOOK THE SAME"** kutusu basılır — Faz 5'te dizilmiş
kitapta **28 kez** sayıldı, Ek F'nin beyan ettiği sayıyla birebir —
ve okur ikisini de test etmeye yönlendirilir.

| Ağırlık | Sayı |
|---|---:|
| `high` | 9 |
| `medium` | 17 |
| `low` | 2 |

Bunları kapatacak tek şey **fiziksel testtir**. Kitap bunu bir kusur
olarak değil, **yöntemin ölçülmüş sınırı** olarak sunar.

---

## 5 · Faz 5'te ne değişti

| | |
|---|---:|
| Faz 5'te KAPANAN iddia | **0** |
| Faz 5'te AÇILAN iddia | **0** |
| Kanıt düzeyi DEĞİŞEN iddia | **0** |
| Toplam iddia (Faz 4 → Faz 5) | **307 → 307** |

Faz 5 bir **kalite güvence** fazıdır. Görev talimatı § 6 epistemik
durumun sessizce yeniden yazılmasını açıkça yasaklıyor ve
**yazılmadı**. Faz 5'te düzeltilen kusurların tamamı **dizgi, navigasyon
ve sunum** katmanındaydı; iddia katmanı Faz 4'ten olduğu gibi devralındı.

**İki kalibrasyon düzeltmesi** yapıldı ve ikisi de iddia sicilinde
izlenen bir kayda karşılık GELMİYOR — okur diline aittirler (§ 7):

1. "The third is **always** larger than the first" → koşulsuz bir
   genellemeydi ve negatif payda (negative ease) YANLIŞTIR. Kitabın
   kapsamıyla sınırlandırıldı: *"In the woven garments this book is
   about, the third is larger than the first…"*
2. Kitap dokuma kumaş VARSAYIYOR ama okura hiç söylemiyordu —
   252 sayfada "woven" kelimesi **sıfır** kez geçiyordu. `SCOPE.md`
   örme/esnek kumaş dikişçisini "farklı fizik" gerekçesiyle kapsam
   dışında tutuyor. Bu dışlama artık "Who this is not for" listesinde.

---

## 6 · Yayını engelleyen açık iddia var mı

| Kategori | Engelliyor mu |
|---|---|
| `CONTESTED` (8) | HAYIR — beyan ediliyor |
| `UNVERIFIED` (29) | HAYIR — beyan ediliyor |
| `INFERRED` (214) | **EVET — `D-02` yapılana kadar** |
| 28 kanıt çakışması | **EVET — `D-02` yapılana kadar** |

> **Desteklenmeyen KRİTİK bir iddia KALMADI** — çünkü kitap
> desteklenmeyen hiçbir şeyi desteklenmiş gibi SUNMUYOR. Kalan risk,
> iddiaların YANLIŞ olması değil; **DOĞRULANMAMIŞ** olmasıdır. Bu ikisi
> aynı şey değildir ve kitap hangisinde olduğunu okura söylüyor.

---

*Vâliçe Press · BEFORE YOU CUT · Kitap 1 · Faz 5 Açık İddialar · 29 Ağustos 2026*
