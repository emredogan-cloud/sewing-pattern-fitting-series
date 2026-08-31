# FAZ 5 — NİHAİ KALİTE RAPORU (Kitap 1)

**Tarih:** 31 Ağustos 2026 · **git:** `a67298c` · **dal:** `faz/4-production`

---

## 1 · Kapı katmanı

| Kapı | Ne ölçer | Durum |
|---|---|---|
| `validate_spec` | şema · bütünlük · kaynak otoritesi | ✅ 0 hata |
| `validate_structure` | depo · koruma · marka · izolasyon | ✅ 208 izlenen dosya |
| `build_crosswalk --check` | crosswalk tazeliği | ✅ 148 kayıt |
| `qa_crosswalk` | dokuz ilişki bütünlüğü | ✅ 21/21 aileye ulaşılıyor |
| `qa_boundary` | kitap sınırı (DIAGNOSE ≠ ADJUST) | ✅ |
| `qa_claims` | iddia disiplini · destek notları | ✅ |
| `qa_terminology` | 20 terim tutarlılığı | ✅ |
| `qa_visual` | figür sicili · token · sayfa geometrisi | ✅ |
| `build_claims --check` | sicil tazeliği | ✅ 312 iddia |
| `build_claim_map --check` | iddia→kaynak haritası | ✅ |
| `qa_verification` | 14 denetim · doğrulama adımı | ✅ 129/129 adım |
| `qa_manuscript` | bölüm yapısı · yeniden gözlem · dil | ✅ |
| `selftest` | KAPILARIN kendi testi | ✅ **225** denetim, 0 atlandı |
| `graph_audit` | 14 denetim · nedensel çizge | ✅ |
| `run_synthetic` | 24 sentetik profil + diferansiyel | ✅ 24/24 |
| `fetch_fonts` | 10 dosya · SHA-256 | ✅ |
| `build_book` | kitabın kendisi | ✅ 259 sayfa |
| `qa_format` | 12 denetim · YAYIN VARLIĞI | ✅ |
| `print_sim` | 6 denetim · 259/259 sayfa · 300 dpi | ✅ |
| `selftest_visual` | çizim yasaklarının kendi testi | ✅ 29 denetim |

`qa_all.sh` çıkış kodu **0**. CI (GitHub Actions) **YEŞİL** —
`33420497199` ve sonrası.

---

## 2 · Bu turda EKLENEN kapılar ve KANITLARI

Talimat: "bir kusuru 'bilinen' diye işaretleyerek kapatma." Her kusurla
birlikte SINIFINI yakalayan bir kapı yazıldı ve her biri kusurun
**özgün metniyle sınandı** — yeşil bir kapı, yakaladığı kanıtlanmadan
kabul edilmedi.

| Kapı | Yakaladığı sınıf | Sınama |
|---|---|---|
| `qa_verification` ⑭ | Bandı olan bir ölçüde ölçüt HAM FARKA bakamaz; bandı söylemeli ve YÖNÜNÜ vermeli | İki ağ ölçütünün özgün hâli kondu → **çıkış 1**, ikisi de yakalandı |
| `graph_audit` ⑬ | Ailesi olmayan neden, NEDEN olmadığını beyan etmeli | Beyan silindi → **çıkış 1** |
| `graph_audit` ⑭ | Klinik öncelik basılan sırada GERÇEKTEN sağlanıyor mu | Geri alınamaz ailenin bastırdığı öncelik kondu → **çıkış 1** |
| `qa_format` ⑫ | Basılı sayfada iç kayıt kimliği / yer tutucu / geçici yol | Sızıntı fixture'ı: `AF-13`, `M-006`, `TODO` yakalandı; Ek I'deki `NATICK/TR-15/007` doğru şekilde YOK SAYILDI |
| `print_sim` ④ | Kenar boşluğuna giren mürekkep — DERİNLİĞİYLE | 20 sayfalık gerçek taşmayı buldu; eşik iki ölçülmüş nüfustan türetildi |
| `selftest` (yeni ×2) | AYRILMA ≠ ÇELİŞKİ · yardımcı sayısı kayıtla uyuşuyor | 225 denetim, 0 atlandı |
| `figure_tokens.text()` | Etiket KUTUDAN taşarsa sessizce kırpılamaz | Açılır açılmaz üçüncü bir kusuru buldu (panel altyazısı) |
| `Engine.render()` | Çizim tuval durumunu DENGESİZ bırakamaz | Bayat dönüşümün bütün sayfayı kaydırdığı kusuru kapatır |

---

## 3 · Tek kaynak hâline getirilenler

Bu turun kusurlarının çoğu **aynı olgunun iki kaydı** olmasından
doğdu. Ayrışan her çift birleştirildi:

| Olgu | Önce | Sonra |
|---|---|---|
| Ek J ease bantları | figure_engine içinde Python listesi + `expected` metinlerinde ELLE | `02_TAXONOMY/public/ease_bands.json` — figür de kapı da BURAYI okur |
| Bandın bu kitabın ölçüsünü tarif edip etmediği | hiçbir yerde | `applies_to_this_books_measurement` (izlenen veri) |
| Aday neden sırası | atlas ve figure_engine'de AYRI hesap | `06_BUILD/cause_order.py` — ikisi aynı fonksiyonu çağırır |
| Geri alınamaz aileler | `cause_order` içinde sabit | kayıttan (`defer_in_diagnosis`) |
| "Yardımcı gerekir" | taksonomide `helper_required` (20) + prozada `helper` (14), atlas VEYA'lıyordu | yalnız taksonomi · **19/33** |
| Ek G'nin kanıt sayıları | prozada ELLE | kayıttan TÜRETİLİR |
| Çakışma kutusu sayıları | prozada ELLE | kayıttan TÜRETİLİR |
| "Kaç giriş ease hesaplar" | "yedi" (elle) | kayıttan — **otuz iki** |
| Düzeltme ailesi sayısı | "twenty" (elle) | kayıttan — **21** |

---

## 4 · Ölçülen nihai durum

259 sayfa · 71.208 kelime · 0,73 MB · 166 ayrı figür (183 yerleşim) ·
43 belirti · 129 neden · **21** düzeltme ailesi · 33 ölçü (19'u yardımcı
ister) · 33 kalıp + 4 prova okuması · 148 crosswalk · 312 iddia
(VERIFIED 52 · VERIFIED_NARROWER 19 · CONTESTED 2 · INFERRED 203 ·
UNVERIFIED 36) · 100 nedende yazılı `expected` ölçütü · 11 çapraz rota ·
2 klinik öncelik kısıtı · 24 sentetik profil.

Test basamağı dağılımı: 18 okuma · 1 koşul · 67 iğne · 23 kumaş şeridi ·
8 sök-ve-yeniden-dik · 12 provayı keser.

---

## 5 · Temiz klon doğrulaması

Depo `f18e89d`'de temiz klonlandı ve SIFIRDAN koşuldu:

* yazı tipleri indirildi ve **SHA-256 ile doğrulandı** ✅
* figür sicili **BAYT BAYT AYNI** üretildi (determinizm kanıtı) ✅
* sekiz veri kapısı, `graph_audit`, `run_synthetic`, `selftest_visual` ✅
* `selftest`: **200/224 koştu, 9 ATLANDI** — ve bunu SÖYLEDİ:
  "Koşan 200 denetimin hepsi geçti — ama 9 denetim HİÇ KOŞMADI."
* `build_book`: **BAŞARISIZ, TASARIM GEREĞİ** — "manüskript dizini yok".
  Yayın öncesi proza bilerek izlenmiyor (K9); temiz klon veriyi, kodu ve
  figürleri yeniden üretir ama KİTABI kuramaz.

Bu, dürüst bir sonuçtur ve gizlenmemiştir.

---

## 6 · Görsel regresyon

Temel: `4f0bcaa` (BOOK 1 — INTERNAL RELEASE CANDIDATE). 163 figür → 170.

* **0 figür KAYBOLMADI**
* 34 figür piksel piksel AYNI
* 114 figür yeniden boyutlandı (akış şemaları 326 → 458 pt; düğümler
  ayırt edici metnin TAMAMINI taşıyor ve şemalar KISALDI)
* 15 figürün içeriği değişti (karşılaştırma figürlerinin yeniden
  çizimi, ölçüm etiketlerinin gövdeden çıkarılması)
* 7 yeni figür

Her değişiklik bilinen ve amaçlanan bir işe bağlanabiliyor.

---

## 7 · Kapanmayanlar — DÜRÜST LİSTE

1. **Fiziksel doğrulama YOK.** Hiçbir teşhis gerçek kumaşta sınanmadı.
   `measured = false`, kill-gate ÖLÇÜLMEDİ (K58).
2. **İnsan okur doğrulaması YOK.** Üç ev dikişçisiyle pilot yapılmadı.
3. **203 iddia INFERRED.** Teşhis mantığının çoğu yayımlanmış bir
   kaynaktan değil, kayıtlı geometriden ve yerleşik uygulamadan gelir.
4. **İki standart hiç edinilemedi** (ISO 8559-1, ASTM D5219).
5. **"Read it" satırları tekrar taşıyor.** Bağımsız inceleme bunu LOW
   verdi; kaldırılmadı çünkü o satır Faz 4'ün en ağır mantık kusurunun
   (yanlışlanamayan ölçüt) düzeltmesidir. Tercih, gerekçesiyle açık.
6. **Bölüm önsözleri ve şema geri dönüşleri tekrarlı.** 43 girişte aynı
   kalıp basılıyor. Bir BAŞVURU kitabında bu bilinçli bir seçimdir
   (okur tek bir girişe dalar), ama uçtan uca okuyan birine üretilmiş
   gibi gelir. Değiştirilmedi; kaydedildi.
