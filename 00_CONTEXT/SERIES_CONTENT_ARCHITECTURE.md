# SERIES CONTENT ARCHITECTURE — kitap sınır matrisi

> Görev talimatı § 9 ve § 11. Hangi konu HANGİ kitaba ait, ve **neden**.
> Makine-okunur kaynak: `02_TAXONOMY/boundary_matrix.json`.
> Mekanik denetim: `06_BUILD/qa_boundary.py`.

---

## 1 · Neden bu belge var

Üç kitaplık bir seride en büyük **içerik** riski pazarın küçüklüğü
değil, **kitapların birbirini yemesidir** (`RISK_REGISTER.md → R-07`).
Kitap 1 düzeltme adımı verirse Kitap 2 gereksizleşir. Kitap 2 blok
çizimine girerse Kitap 3 gereksizleşir. Bu belge o sınırı **kural
hâline** getirir.

## 2 · Rol sözlüğü

| Rol | Anlamı |
|---|---|
| `primary` | Bu kitap konuyu ÖĞRETİR ve sahiplenir. Kanonik tanım buradadır. |
| `support` | Bu kitap konuyu KULLANIR ve kendi bağlamında derinleştirir, kanonik tanımı yeniden yazmaz. |
| `introduce_only` | Konunun VARLIĞINI en fazla bir kavram/bir sayfa düzeyinde tanıtır. **Prosedür VERMEZ.** |
| `reference_only` | Yalnızca ATIF (bir cümle + çapraz referans). |
| `excluded` | Bu kitapta YOKTUR. |

## 3 · TEK-BİRİNCİL KURALI

> **Bir topik için EN FAZLA BİR kitap `primary` olabilir.**

Görev talimatının başlangıç çerçevesi iki yerde bu kurala aykırıydı:

- *Measurements*: Kitap 1 **ve** Kitap 3 "Core"
- *Muslin / toile*: üç kitap da "Core"

Bu bir çelişki değil, bir **çözünürlük eksikliğiydi**: iki kitap gerçekten
de o alanı sahiplenir, ama **aynı şeyi değil**. Çözüm kopyalama değil,
**TOPİK BÖLME** oldu:

| Bölünen topik | Kaynağı | Gerekçe |
|---|---|---|
| `TOP-21` Drafting measurement set (block-specific) | `TOP-01` | TOP-01'den BİLEREK ayrıldı: teşhis için gerekmeyen ölçüler Kitap 1'i şişirirdi. |
| `TOP-24` Balance & grain — construction in the draft | `TOP-23` | TOP-23'ten BİLEREK ayrıldı: görmek ile kurmak farklı becerilerdir. |
| `TOP-26` Verification toile (after adjustment) | `TOP-07` | TOP-07'den ayrı bir giysidir — farklı amaç, farklı protokol. |
| `TOP-27` Block-proving toile | `TOP-07` | TOP-07/TOP-26'dan ayrı: hiçbir ticari kalıp yok, referans yalnızca bedenin kendisi. |

`qa_boundary.py § check_single_primary` bu kuralı mekanik olarak dayatır
ve bir sahipsiz topik bırakılmasını da yakalar.

## 4 · Matris (35 topik)

| ID | Topik | Kitap 1 | Kitap 2 | Kitap 3 | Birincil amaç |
|---|---|---|---|---|---|
| `TOP-01` | Body measurement — taking | primary | reference_only | reference_only | Ölçüyü DOĞRU almak |
| `TOP-02` | Body measurement — interpretation vs size charts | primary | reference_only | support | Kalıp bedeni ≠ hazır giyim bedeni |
| `TOP-03` | Pattern flat measurement + finished garment measurement | primary | support | reference_only | Kalıbın gerçekte ne vaat ettiğini okumak |
| `TOP-04` | Ease theory — wearing ease vs design ease | primary | support | support | Fark ölçüsünü yorumlamak |
| `TOP-05` | Pattern size selection | primary | reference_only | excluded | Yanlış bedeni düzeltmeye çalışmayı önlemek |
| `TOP-06` | Body shape / posture / asymmetry analysis | primary | reference_only | support | Nedeni bedende bulmak |
| `TOP-07` | Diagnostic toile — construction | primary | support | support | Teşhis için dikilen prova giysisi |
| `TOP-08` | Fitting session protocol | primary | reference_only | reference_only | Ölçüm koşullarını standartlaştırmak |
| `TOP-09` | Fit sign controlled vocabulary | primary | reference_only | reference_only | Belirtiyi ADLANDIRMAK |
| `TOP-10` | The diagnostic loop (7 steps) | primary | reference_only | reference_only | Tekrarlanabilir teşhis yöntemi |
| `TOP-11` | Confounder elimination — fabric / construction / printing | primary | support | reference_only | Kalıpla İLGİSİ OLMAYAN nedenleri elemek |
| `TOP-12` | Symptom → cause taxonomy | primary | reference_only | excluded | Belirtiden olası nedene |
| `TOP-13` | Adjustment family naming + scope | introduce_only | primary | reference_only | Teşhisin varış noktasını adlandırmak |
| `TOP-14` | Alteration procedures — step by step | excluded | primary | support | Düzeltmeyi UYGULAMAK |
| `TOP-15` | Slash-and-spread / pivot-and-slide mechanics | introduce_only | primary | support | Kalıp geometrisini değiştirme mekaniği |
| `TOP-16` | Dart manipulation / rotation | excluded | primary | support | Şekillendirmeyi taşımak |
| `TOP-17` | Adjustment interaction map | introduce_only | primary | reference_only | Bir düzeltmenin diğerini bozması |
| `TOP-18` | Adjustment order / priority | primary | support | reference_only | HANGİSİ ÖNCE |
| `TOP-19` | Verification after alteration | excluded | primary | support | Düzeltme İŞE YARADI MI |
| `TOP-20` | Block / sloper drafting theory | excluded | introduce_only | primary | Sıfırdan üretim mantığı |
| `TOP-21` | Drafting measurement set (block-specific) | excluded | excluded | primary | Blok çizimi için EK ölçüler |
| `TOP-22` | Drafting sequence | excluded | excluded | primary | Çizim adım sırası |
| `TOP-23` | Balance & grain — diagnosis | primary | support | support | Dengesizliği GÖRMEK |
| `TOP-24` | Balance & grain — construction in the draft | excluded | excluded | primary | Dengeyi ÇİZİMDE kurmak |
| `TOP-25` | Personal fit profile (record system) | primary | support | support | Teşhisi TAŞINABİLİR kılmak |
| `TOP-26` | Verification toile (after adjustment) | excluded | primary | reference_only | Düzeltilmiş kalıbı sınamak |
| `TOP-27` | Block-proving toile | excluded | reference_only | primary | Bloğu sınamak ve rafine etmek |
| `TOP-28` | Series terminology glossary | primary | reference_only | reference_only | Tek terim, tek tanım |
| `TOP-29` | Visual notation system | primary | reference_only | reference_only | Tek çizim dili |
| `TOP-30` | Grading between sizes | introduce_only | primary | reference_only | İki beden arasında geçiş |
| `TOP-31` | Knit / stretch fabric fitting | excluded | excluded | excluded | SERİ DIŞI |
| `TOP-32` | Sewing construction technique | excluded | excluded | excluded | ÖN KOŞUL, ÜRÜN DEĞİL |
| `TOP-33` | Sewing history / general craft narrative | excluded | excluded | excluded | DOLGU |
| `TOP-34` | Menswear / tailoring | excluded | excluded | excluded | SERİ DIŞI |
| `TOP-35` | Commercial pattern brand-specific instructions | excluded | excluded | excluded | IP SINIRI |

## 5 · Kapsam DIŞI beş topik ve gerekçeleri

| Topik | Neden dışarıda |
|---|---|
| `TOP-31` Örme/esnek kumaş uyumu | Dokuma uyumundan farklı fizik. Araştırma raporu § 29 bunu **gelecek katalog yönü** olarak işaretledi; bu seride yok. |
| `TOP-32` Dikiş yapım tekniği | ÖN KOŞUL, ürün değil. Hedef okur zaten dikebiliyor; dikiş öğretmek ürünü genel bir dikiş kitabına dönüştürür. |
| `TOP-33` Dikiş tarihi / genel zanaat anlatısı | Dolgu. Kalite standardı: her bölüm yerini hak eder. |
| `TOP-34` Erkek giyim / terzilik | Gelecek katalog yönü (araştırma raporu § 29). |
| `TOP-35` Ticari yayıncıya özgü kalıp talimatı | IP sınırı — `IP_AND_BRAND_POLICY.md § 1-2`. |

## 6 · En yüksek riskli sınır: `TOP-13` ↔ `TOP-14`

Kitap 1 `TOP-13`'te (düzeltme ailesini ADLANDIRMA) `introduce_only`,
Kitap 2 `TOP-14`'te (adım adım prosedür) `primary`'dir. **Aradaki çizgi
bir cümledir:**

> Kitap 1 şunu yazabilir: *"Bu bir göğüs hacmi düzeltmesidir (AF-01);
> kalıbın ön bedenine apeks hizasından hacim eklenir."*
>
> Kitap 1 şunu YAZAMAZ: *"Önce apeksten dikey bir çizgi çiz, sonra
> pens ucuna kadar kes, sonra 2 cm aç, sonra…"*

`qa_boundary.py § check_excluded_leak` bir `excluded`/`introduce_only`
topiğin ADIM DİLİYLE ("Adım 1", "Step 2", "şöyle yapılır") geçmesini
tarar.

## 7 · Ortak sözlük kuralı

`TOP-28` uyarınca terimler Kitap 1'de kurulur; Kitap 2 ve 3
**değiştiremez**. Kanonik sözlük: `02_TAXONOMY/terminology.json`
(20 terim). Mekanik denetim: `qa_terminology.py`.

En kritik ayrım — **pattern adjustment** (kâğıt kalıp, kesimden ÖNCE)
ile bitmiş giysi üzerinde yapılan değişiklik AYNI ŞEY DEĞİLDİR. Seri
birincisini öğretir, ikincisini öğretmez. Kitap 2'nin adı bu ayrımı taşır.

---

*Vâliçe Press · TRUE FIT · Series Content Architecture · 28 Ağustos 2026*
