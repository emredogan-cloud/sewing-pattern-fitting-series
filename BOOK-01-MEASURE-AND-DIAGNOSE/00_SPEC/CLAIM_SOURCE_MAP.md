# CLAIM SOURCE MAP — BEFORE YOU CUT, Book 1

> **ÜRETİLMİŞ BELGE — elle düzenlenmez.**
> Kaynak: `06_BUILD/build_claim_map.py` · sicil:
> `02_CONTENT/public/claims.public.json`
>
> Faz 4 talimatı § 15. Her teknik olarak maddi ifade buradan kaynağına
> ve doğrulama durumuna izlenir.
>
> **`evidence_level` BEYAN DEĞİL TÜREVDİR:** taksonomi kaydının
> `verification_status`'ünden ve atıf yaptığı kaynakların
> otoritesinden hesaplanır. Hiçbir iddia kendi seviyesini yazamaz.

---

## 1 · Toplam

**310 iddia.**

| Kanıt seviyesi | Sayı | Oran | Anlamı |
|---|---:|---:|---|
| `VERIFIED` | 51 | %16.5 | Kayıt doğrulanmış VE en az bir tam metin teknik otoritesine bağlı. |
| `VERIFIED_NARROWER` | 18 | %5.8 | Kaynak okundu ve İLKEYİ destekliyor, ama iddianın yazıldığı hâlinden DAHA DAR bir ifadeyi destekliyor. Kaydın `source_support_note` alanı kaynağın gerçekte ne dediğini yazar (görev talimatı § 9). |
| `CONTESTED` | 2 | %0.6 | Kaynaklar arasında KAYITLI tanım farkı var. Bir hata değildir — Bölüm 2'nin öğretim malzemesidir. |
| `INFERRED` | 203 | %65.5 | Kaynak bağlamı destekliyor; iddianın KENDİSİ ajan türevi. |
| `UNVERIFIED` | 36 | %11.6 | Hiçbir otoriter kaynağa bağlı değil. |

> ⚠ **`INFERRED` çoğunluktadır ve bu gizlenmemiştir.** Kitabın
> teşhis ilişkileri (belirti → aday neden) kamu kaynaklarında
> tek tek doğrulanamadı; Faz 1 bunu kaydetti, Faz 4 değiştirmedi.
> Bu yüzden her giriş bir CEVAP değil bir FİZİKSEL TEST verir.

## 2 · İddia türüne göre

| Tür | Sayı | Ne dayatır |
|---|---:|---|
| `sign_cause` | 129 | Bir nedenin AYIRT EDİCİ kanıtı — kitabın en riskli sınıfı. |
| `sign_observation` | 43 | Bir belirtinin gözlenebilir olduğu ve nerede durduğu. |
| `measurement_definition` | 33 | Bir ölçünün nereden nereye alındığı. |
| `measurement_path` | 33 | Şeridin serbest değil KISITLI olduğu. |
| `conceptual` | 32 | Yöntem katmanı — kitabın öğrettiği kuralın kendisi. |
| `adjustment_family` | 20 | Bir düzeltmenin kalıbın hangi alanına dokunduğu. |
| `adjustment_order` | 20 | Hangi düzeltmenin hangisinden önce geldiği. |

## 3 · Bölüme göre

| Bölüm | İddia | `VERIFIED` | `V_NARROWER` | `CONTESTED` | `INFERRED` | `UNVERIFIED` |
|---|---:|---:|---:|---:|---:|---:|
| 1 · Why the pattern did not fit | 2 | 0 | 0 | 0 | 2 | 0 |
| 2 · Measuring your body | 71 | 29 | 7 | 2 | 13 | 20 |
| 3 · Reading the pattern | 5 | 1 | 0 | 0 | 4 | 0 |
| 4 · The fitting garment | 3 | 0 | 0 | 0 | 1 | 2 |
| 5 · The fitting session | 3 | 0 | 1 | 0 | 2 | 0 |
| 6 · The seven-step cycle | 3 | 0 | 1 | 0 | 2 | 0 |
| 7 · Naming what you see | 4 | 1 | 1 | 0 | 0 | 2 |
| 8 · Ruling out false causes | 3 | 1 | 0 | 0 | 1 | 1 |
| 9 · Neck and shoulder | 32 | 0 | 0 | 0 | 32 | 0 |
| 10 · Upper back and armhole | 28 | 0 | 0 | 0 | 28 | 0 |
| 11 · Bust and chest | 24 | 0 | 0 | 0 | 24 | 0 |
| 12 · Waist and torso length | 20 | 0 | 0 | 0 | 20 | 0 |
| 13 · Hip and seat | 16 | 0 | 0 | 0 | 16 | 0 |
| 14 · Sleeve and arm | 16 | 0 | 0 | 0 | 16 | 0 |
| 15 · Trousers: crotch and leg | 20 | 0 | 0 | 0 | 20 | 0 |
| 16 · Order of work | 58 | 19 | 7 | 0 | 22 | 10 |
| 17 · Your fit profile | 1 | 0 | 1 | 0 | 0 | 0 |
| 18 · Carrying it forward | 1 | 0 | 0 | 0 | 0 | 1 |

## 4 · Kaynağa göre

| Kaynak | İddia | Otorite | Erişim | Başlık |
|---|---:|:---:|---|---|
| `S-0001` | 184 | ✓ | fulltext | Pattern Alteration — Guide C-228 |
| `S-0004` | 178 | ✓ | fulltext | Challenging Patterns — EM4582 |
| `S-0003` | 104 | ✓ | fulltext | Pattern Alteration: Principles of Pattern Alteration |
| `S-0002` | 66 | ✓ | fulltext | Making Perfect Pants — Guide C-227 |
| `S-0006` | 4 | ✓ | official_pdf | National Health and Nutrition Examination Survey (NH |
| `S-0005` | 4 | ✓ | fulltext | 2012 Anthropometric Survey of U.S. Army Personnel: M |
| `S-0007` | 1 | ✓ | official_web | Fit for Fashion: The "A-B-C's" — E-419 |

## 5 · İzlenebilirlik

Dizilen metinden izlenen maddi iddia: **205/205**

Ölçüm: `06_BUILD/qa_manuscript.py § ⑪`. Bir iddianın izlenebilir
sayılması için manüskript bloğunun `claims` alanında taksonomi
kimliğini TAŞIMASI gerekir; blok o kimliği taşımıyorsa kapı kırmızı yakar.

## 6 · Faz 4 bağımsız incelemesinde DEĞİŞEN iddialar

**23 kavramsal iddia** bağımsız inceleme sonucunda yeniden yazıldı.

| # | Karar | Gerekçe |
|---|---|---|
| `CC-01` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-06` | ACCEPTED | Önceki hâli 'ne kadar şekillendirme gerektiğini söyler' diyordu; kaynak yalnızca BEDEN SEÇİMİ eşiğini destekliyor. |
| `CC-09` | ACCEPTED | Deponun tek ease kaynağı (S-0001 Table 1) bel satırı taşımıyor ve kendi dipnotuyla çelişiyor; tek otorite olarak sunulamaz. |
| `CC-10` | ACCEPTED | Düz '2 inç' eşiği üç ayrı yayıncıda farklıdır ve tam 2 inçte doğru bedendeki okuru gereksiz bir düzeltmeye gönderiyordu. |
| `CC-11` | ACCEPTED | Bir kampın kuralı nedensel bir gerçek gibi yazılmıştı; okurun satın alacağı kalıpların bir kısmı bunun tersini basıyor. |
| `CC-13` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-14` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-15` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-16` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-17` | ACCEPTED | Kaynaklar bir SIRA vermiyor — 'aklında tut' diyorlar ve o listede denge DÖRDÜNCÜ sırada. Okuma sırası ile düzeltme sırası ayrıldı; birincisi kitabın kendi kuralı olarak beyan edildi. |
| `CC-18` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-19` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-20` | ACCEPTED | Kendi verisiyle ÇELİŞİYORDU: 129 testin 17'si ilk adım olarak kesiyordu ve üçü, SYM-001'in kendi uyarısının 'geri eklenemez' dediği yakayı kesiyordu. Ayrım netleştirildi: toile kesilir, KALIP ve KENAR kesilmez. |
| `CC-21` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-22` | ACCEPTED | Kural KAYNAKSIZDI: atıf yapılan belge (S-0004) tam metin okundu ve içinde kıvrım-ekseni kuralı YOK. Ayrıca tabloda GERGİN yatay kırışık için hücre yoktu ve deponun kendi verisi bunu kanıtlıyordu: horizontal_fold sınıfındaki beş kaydın üçü fazlalığı değil YETERSİZLİĞİ anlatıyor (SYM-027'nin kendi origin_rule'u bunu açıkça yazıyor). Okur dar bir giysiyi KISALTIRDI. |
| `CC-23` | ACCEPTED | 'o yönde' ibaresi SİLİNDİ: kaynak yön hakkında hiçbir şey söylemiyor ve o ek, CC-22'yi CC-23'ün içine sokarak kaynaksız bir iddiayı kaynaklı gösteriyordu. |
| `CC-24` | ACCEPTED | Atıf yapılan belgede çekme çizgisi HİÇ geçmiyor. Üç ayrı geometrik model var ve iddia en az ayırt edici olanını seçmişti. Adım 4 tek başına buna dayanıyor; daraltıldı ve fiziksel doğrulamaya bağlandı. |
| `CC-25` | ACCEPTED | Veri kendi kuralını TERS uyguluyordu: 20 kalıp-dışı nedenin hiçbiri ilk sırada değildi, 13'ü sonuncuydu. Sunum sırası kapı-önce olacak biçimde değiştirildi (atlas.py). |
| `CC-27` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-28` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-29` | ACCEPTED | S-0004'ten ÇIKARILDI — belge etek ucunun türev olduğunu söylemiyor. Kalibre hâliyle korunuyor ama artık kaynaksız olduğunu beyan ediyor. |
| `CC-30` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |
| `CC-31` | ACCEPTED | Faz 4 bağımsız teknik inceleme (PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md) uyarınca yeniden yazıldı. |

Tam gerekçeler ve kaynaklar:
[`../../08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md`](../../08_REPORTS/PHASE_4_INDEPENDENT_TECHNICAL_REVIEW.md).

---

*Vâliçe Press · BEFORE YOU CUT, Book 1 · Claim Source Map · ÜRETİLMİŞ*
