# QA STANDARD — üç kitabın ortak kalite kapıları

> Görev talimatı § 9, § 45. Bu belge SERİ genelinde geçerli kuralları
> tanımlar; kitaba özgü ek kapılar o kitabın `ROADMAP.md`'sindedir.

---

## 1 · Temel ilke

> **"Kendi kusurunu yakalamayan bir kapı, kapı değildir."**

Kardeş projelerden birebir devralınan ilke. İçerik yokken yeşil yanan
bir doğrulayıcı, kusur geldiğinde de yeşil yanabilir. Bu riski kapatan
şey `07_TESTS/selftest.py`'dir: her doğrulayıcı için **kasıtlı olarak
bozuk** bir fixture üretir ve kapının onu GERÇEKTEN yakaladığını
kanıtlar.

## 2 · Kapı envanteri

| Kapı | Komut | Ne denetler |
|---|---|---|
| Şema + bütünlük + kaynak otoritesi | `06_BUILD/validate_spec.py` | Taksonomi şemaları, referans bütünlüğü, kaynak otoritesi, doğrulama kanıtı, kapı gereksinimleri |
| Depo + koruma + marka | `06_BUILD/validate_structure.py` | Zorunlu belgeler, korumalı dizin sızıntısı, **fotoğraf sızıntısı**, **marka sızıntısı**, kardeş-depo izolasyonu |
| Crosswalk tazeliği | `06_BUILD/build_crosswalk.py --check` | Devir haritası kaynak taksonomiyle güncel mi |
| **Kitap sınırı** | `06_BUILD/qa_boundary.py` | Tek-birincil kuralı, belirti→yol kapsaması, aile ulaşılabilirliği, sınır sızıntısı |
| **İddia disiplini** | `06_BUILD/qa_claims.py` | Sahte uzman iddiası, korunan "basılı avantaj" iddiası, dayanaksız doğrulama iddiası |
| **Terminoloji** | `06_BUILD/qa_terminology.py` | Yasak eşanlamlı, tanımsız kimlik referansı |
| Kill-gate ön koşulu | `06_BUILD/kill_gate.py` | Ölçümün ön koşulları hazır mı, sonuç usulüne uygun kaydedilmiş mi |
| **Kapıların kendi testi** | `07_TESTS/selftest.py` | Her kapının kusurlu fixture'ı yakalayıp yakalamadığı |
| Hepsi | `bash 06_BUILD/qa_all.sh` | Sırayla tümü |

Üçüncü taraf paket **gerekmez** — tüm kapılar Python standart
kütüphanesiyle yazılmıştır.

## 3 · Üç kitapta da geçerli içerik kuralları

### K-1 · Belirti ≠ neden
Bir belirti kaydı yorumsuz gözlemdir. Her aday neden kendi **ayırt
edici kanıtını** ve **doğrulayıcı ölçümünü** taşımak zorundadır. İki
neden aynı ayırt edici kanıtı taşıyamaz — taşırsa okur onları ayıramaz
(`check_cause_distinguishability`).

### K-2 · Ölçüm yoksa fiziksel test zorunlu
`confirming_measurement: "NO_MEASUREMENT_EXISTS…"` yazan her neden bir
`physical_test` tanımlamak ZORUNDADIR. Kanıtsız neden yazılamaz.

### K-3 · Doğrulama durumu ücretsiz verilmez
`technical_reference_verified` ≥1 `fulltext`/`official_pdf` kaynak
gerektirir. `physically_validated` bir `VAL-xxxx` kaydı gerektirir.

### K-4 · Sınır ihlali bir KUSURDUR
Bir kitabın `excluded`/`introduce_only` topiği adım diliyle geçemez.

### K-5 · Sahte uzman etiketi yasaktır
Kurucu kararı (`DECISIONS.md K6`): bu seride de dış uzman İŞE
ALINMAYACAK. Bağımsız çelişmeli AI incelemesi **kullanılacak**, ama
asla insan uzman yerine **sayılmayacak**. "expert-verified",
"professional tailor verified", "uzman onaylı" gibi ifadeler gerçek bir
insan kullanılmadıkça yazılamaz.

### K-6 · Marka yasağı
Ticari kalıp markaları başlık/metadata yüzeyinde geçemez.

### K-7 · Korunan iddia
Basılı formatın videoya üstünlüğü bir GERÇEK gibi kullanılamaz —
araştırma raporu § 27'de bu iddia **ZAYIF** çıktı.

## 4 · Fiziksel KA — kâğıt üstünde bitmez

Bu ürünün ayırt edici KA gereği: **her düzeltme diyagramı gerçekten
kalıba uygulanır, toile dikilir, sonuç ölçülür.** Protokol:
`VALIDATION_PROTOCOL.md`. Bu, kardeş projelerin hiçbirinde olmayan bir
kapıdır ve araştırma raporunun § 32 "doğruluk riski" maddesinin
doğrudan karşılığıdır.

**Eşikler (araştırma raporu § 35 madde 2'den):**

| Ölçüm | Sonuç |
|---|---|
| Diyagram hata oranı **%0** | Pilot geçer |
| Hata oranı **> %0** | Pilot durur, hatalı diyagramlar kök nedenden düzeltilir |
| Hata oranı **> %5** | **ÜRETİM YÖNTEMİ reddedilir** — proje durur |

## 5 · Bağımsız çelişmeli inceleme

Her fazın kapanışında, o fazın işini yapmamış bağımsız bir inceleyici
fazın çıktısını **çürütmeye çalışır**. Bulgular
`08_REPORTS/PHASE_x_ADVERSARIAL_REVIEW.md`'ye yazılır ve HARD_STOP
bulguları kapıyı bloke eder.

⚠ **Bu bir insan uzman incelemesi DEĞİLDİR** ve hiçbir yerde öyle
sunulamaz (K-5).

## 6 · Faz raporu durum sözlüğü

Kardeş projelerden devralındı — bir faz raporu şu durumlardan **tam
olarak birini** taşır:

`COMPLETE` · `PARTIAL` · `BLOCKED` · `FOUNDER-DEPENDENT` ·
`READY_FOR_DECISION` · `COMPLETE — FOUNDER OVERRIDE`

**Kural:** "ölçüldü ve geçti", "ölçüldü ve geçmedi ama kurucu geçersiz
kıldı" ve "henüz ölçülmedi" ASLA birbirinin yerine geçmez.

---

*Vâliçe Press · TRUE FIT · QA Standard · 28 Ağustos 2026*
