# REFERENCE SYNTHESIS — kardeş projelerden ne devralındı, ne değişti

> Görev talimatı § 3–5'in doğrudan çıktısı. Hangi mimari desenler
> İNCELENDİ, hangileri DEVRALINDI, hangileri BİLİNÇLİ OLARAK
> DEĞİŞTİRİLDİ. Hiçbir kardeş projeden **içerik** devralınmadı —
> yalnızca **yöntem**.

---

## 1 · İncelenen depolar

| Depo | Ne için incelendi |
|---|---|
| `KOREAN-HANGUL-HANDWRITING-WORKBOOK` | **En yakın mimari emsal.** `paths.py`/`schema_lite.py`, `.gate`, K#/A# kaydı, `selftest.py` felsefesi, `ROADMAP_PROGRESS.md` ölçüm tablosu, "ölçülen / kurucu tarafından geçersiz kılınan / henüz ölçülmemiş" üç durumunun ASLA birbirinin yerine geçmemesi |
| `LICENSE-AND-LAUNCH-CALIFORNIA-LIFE-HEALTH` | Faz raporu durum sözlüğü (COMPLETE / PARTIAL / BLOCKED / FOUNDER-DEPENDENT / READY_FOR_DECISION), iki katmanlı içerik koruma iskeleti, kill-gate'in ayrı bir dosya olması |
| `CODEX-ENIGMATICA` | Kill-gate'in GERÇEKTEN başarısız olabilme ilkesi (A12 emsali) |
| `THE-GREAT-BOOK-OF-WORLD-GAMES` | Ortak kütüphane reddi, açık karar kapanış izleme, kurucu-teslim istek kuyruğu |
| `CODEX_BESTIARIUM` / `CODEX_MYTHOLOGICA` / `THE-GREAT-BOOK-OF-WORLD-MYTHS` / `THE-MYTH-HUNTERS-FIELD-BOOK` | Dizin numaralandırma felsefesi, kaynak katmanlama, editoryal geçiş modeli |

Ayrıca `KDP_2_3_BOOK_SERIES_OPPORTUNITY_RESEARCH_2026_CYCLE_2.html`
(27 Ağustos 2026) bu projenin ticari başlangıç noktası olarak
tamamen okundu — bkz. `BRIEF.md`.

## 2 · BİREBİR devralınan mimari

- `paths.py` tek-yol-tablosu — hiçbir script kendi yolunu kurmaz.
- `schema_lite.py` — bağımlılıksız JSON-Schema-lite doğrulayıcı
  (içerikten bağımsız genel altyapı).
- `.gate` kümülatif kapı dosyası + `gate_at_least()` mantığı.
- K#/A# karar-kaydı kongvansiyonu (`DECISIONS.md` + `OPEN_QUESTIONS.md`).
- `selftest.py` felsefesi: **"kendi kusurunu yakalamayan bir kapı, kapı
  değildir."**
- Faz raporu durum sözlüğü.
- İki-katmanlı public/protected `.gitignore` mimarisi (izin-listesi >
  yasak-listesi ilkesi).
- "Ölçülen / geçersiz kılınan / ölçülmemiş" ayrımının ASLA
  bulanıklaştırılmaması.
- Kanıt etiketleri: `FACT` `OBSERVED` `ESTIMATE` `INFERENCE`
  `HYPOTHESIS` `UNVERIFIED`.

## 3 · BİLİNÇLİ OLARAK DEĞİŞTİRİLEN mimari

### ① Tek kitap deposundan SERİ deposuna — iki katmanlı kapı

Kardeş projelerin hepsi **tek kitaplıktır** ve tek düz bir `.gate`
taşır. Bu depo üç kitap taşır ve kitaplar KISMEN PARALEL ilerler
(Kitap 2'nin araştırması, Kitap 1'in üretimi sürerken başlayabilir).
Tek düz bir kapı bunu ifade EDEMEZ.

Çözüm: **iki katman** (`DECISIONS.md K3`).

| Katman | Dosya | Neyi ölçer |
|---|---|---|
| Seri kapısı | `.gate` (kökte) | Ortak mimarinin donma derecesi |
| Kitap kapısı | `BOOK-xx/.gate` | O kitabın kendi faz ilerlemesi |

Biri diğerini **otomatik ilerletmez**. `paths.gate_at_least()` sırayı
AÇIKÇA parametre alır — iki katman yanlışlıkla karşılaştırılamasın diye.

### ② Ortak araç zinciri — ama yalnızca DEPO İÇİNDE

Kardeş projelerin K1/K2 kararı "ortak kütüphane YOK"tur ve **bu karar
aynen yürürlüktedir**: hiçbir kardeş depo bu deponun build'i için
gerekli değildir (`validate_structure.py § check_no_sibling_dependency`
bunu mekanik olarak denetler).

Ama **depo içinde** üç kitap TEK araç zinciri paylaşır
(`DECISIONS.md K2`). Gerekçe: araştırma raporu § 31 diyagram
kütüphanesinin amortismanını kazananın **en somut üretim avantajı**
olarak işaretledi. Üç ayrı doğrulayıcı kopyası bu avantajı doğrudan
yok ederdi ve zamanla birbirinden sapardı.

### ③ "Cevap alanı" korumasından ÜÇ HATLI korumaya

Sigorta/Enigmatica'da korunan şey gerçek, tekil bir GİZLİ ALANDIR
(`correct_answer`). Kalıp düzeltmede böyle bir alan **yoktur** — kalıp
geometrisi ve düzeltme yöntemleri telifle korunmaz (araştırma raporu
§ 21). Bu yüzden korunan şey yeniden tanımlandı:

1. yayın-öncesi tam proza/akış şeması metni (sıradan yayın gizliliği),
2. **fiziksel doğrulama fotoğrafları** — gerçek bir insanın vücut
   görüntüsü (hiçbir kardeş projede olmayan, bu ürüne özgü gizlilik
   kısıtı),
3. telif korumalı referans malzeme (taranmış kitap sayfası, satın
   alınmış ticari kalıp).

### ④ Kardeş projelerde OLMAYAN iki yeni kapı

| Kapı | Neden var |
|---|---|
| `qa_boundary.py` | Üç kitaplık bir seride en büyük içerik riski **kitapların birbirini yemesi**dir. Tek-birincil kuralı, crosswalk bütünlüğü ve sınır sızıntısı mekanik olarak denetlenir. Tek kitaplı kardeşlerde karşılığı yok. |
| `qa_claims.py § MARKA/ORTAM` | İki gerçek dış kısıt: (a) KDP metadata'da izinsiz marka kullanımı yasağı, (b) araştırma raporunun ZAYIF çıkan "basılı avantaj" iddiası. |

### ⑤ Kill-gate: oran ve kusur-şiddeti modellerinden **ikili DIŞ ÖLÇÜM** modeline

| Proje | Model |
|---|---|
| Sigorta | Oran eşiği (SME onay oranı ≥ %90) |
| Hangıl | Kusur şiddeti (HARD_STOP / REVISE / PASS) |
| **TRUE FIT** | **İki bağımsız DIŞ ölçüm** — ① üç gerçek okurun fark testi, ② her diyagramın fiziksel dikim testi |

Fark: bu projenin kill-gate'i **depo içinden ölçülemez**. `kill_gate.py`
bu sınırı adından ve çıktısının ilk satırından itibaren duyurur —
Hangıl projesinde aynı sınır scriptin içine gömülü bir nota kalmıştı ve
bu, ölçümün yanlış okunmasına zemin hazırlamıştı.

## 4 · Hangıl projesinin K20 dersi — bu projeye taşınan kural

28 Ağustos 2026'da Hangıl projesinin Faz 4 kill-gate'i **REVISE** ölçtü
ve kurucu, insan-kullanılabilirlik kriterini açıkça **geçersiz kıldı**.
O kayıt örnek bir dürüstlük belgesidir: ölçüm değiştirilmedi, geçersiz
kılma ayrı bir alan olarak yazıldı.

Bu proje aynı disiplini **baştan** taşır: `series_config.json →
killGates` içinde `measured`, `measuredDecision` ve `founderOverride`
**ayrı alanlardır** ve `kill_gate.py` bir override'ı "geçti" diye
DEĞİL, "kapıyı ilerleten ölçüm değil kurucu kararıdır" diye raporlar.
Ayrıca `aiProxyCountsAsHuman: false` bayrağı **açılamaz** — script bunu
ayrı bir engel olarak yakalar.

## 5 · İzolasyon beyanı

Bu proje hiçbir kardeş depodan dosya, diyagram, kaynak kaydı veya
manüskript metni devralmaz. `series_config.json → isolatedFrom` bunu
makine-okunur biçimde sabitler ve `validate_structure.py` bir kardeş
depoya BAĞIMLILIK bağlamında yapılan her atfı hata olarak raporlar
(mimari ATIF yorumları serbesttir — kardeş projelerin kendi
kongvansiyonudur).

---

*Vâliçe Press · TRUE FIT · Reference Synthesis · 28 Ağustos 2026*
