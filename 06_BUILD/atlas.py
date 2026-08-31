#!/usr/bin/env python3
"""
atlas.py — bölge atlası bölümlerini (Bölüm 9–15 + 16'nın atlas kısmı)
taksonomiden ve yazılmış İngilizce içerikten ÜRETİR.

⚠ NEDEN ÜRETİLİR, ELLE YAZILMAZ: 43 belirti girişinin iç yapısı
aynıdır ve o yapı bir SPESİFİKASYONDUR (CONTENT_ARCHITECTURE § PARÇA
IV). Elle yazılsaydı 43 girişten biri er geç 'henüz değiştirme'
uyarısını ya da yeniden gözlem adımını taşımazdı ve hiçbir kapı bunu
göremezdi. Üretilen bir yapıda eksik alan DERLENMEZ.

Yazılmış olan: proza (sign_content_en.json, zones_en.json).
Üretilen: sıra, başlık hiyerarşisi, figür yerleşimi, devir cümlesi ve
üç YAPISAL ZORUNLULUK:

  B-01  her giriş bir YENİDEN GÖZLEM adımıyla ve 'azaldı ama gitmedi'
        dalıyla biter — çelişmeli inceleme YÜKSEK bulgusu
  B-02  AF-18'e giden yol açıkça 'bu bir beden kararıdır' diye
        karşılanır
  B-03  eleme listesi BELİRTİYE ÖZGÜDÜR; 11 kalemlik tam liste yalnızca
        Bölüm 8'de bir kez yürünür

⚠ OKUR DİLİ: hiçbir iç kimlik (SYM-xxx, AF-xx, M-xxx) okura dönük
metne girmez (K45/K46). Kimlikler yalnızca izlenebilirlik alanlarında
(claims) durur ve dizilmez.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

# 12 karıştırıcı dizesinin okur karşılığı. Kaynak: fit_signs.json
# confounders_to_rule_out (Türkçe proje dili) → İngilizce okur dili.
CONFOUNDER_EN = {
 "Kumaş: kalıbın önerdiğinden farklı ağırlık/dökümlülük/esneklik":
   "Fabric — heavier, lighter, stiffer or stretchier than the pattern asks for.",
 "Beden: kalıp bedeni yanlış seçilmiş — bu bir SEÇİM sorunudur, düzeltme sorunu değil":
   "Size — the wrong pattern size was chosen. That is a choice, not an adjustment.",
 "Prova duruşu: okur prova sırasında doğal duruşunda değil":
   "Posture — you are not standing the way you normally stand.",
 "Yapım: dikiş payı eşit değil, kenar gerdirilmiş, tela/pekiştirme atlanmış":
   "Construction — uneven seam allowances, a stretched edge, or interfacing left out.",
 "Kesim: parça çözgüye eğri kesilmiş (off-grain)":
   "Cutting — the piece was cut off grain.",
 "Ütü: dikişler açılıp ütülenmemiş":
   "Pressing — the seams were not pressed open.",
 "İç giyim: prova sırasında farklı/uygunsuz sutyen veya iç çamaşırı":
   "Underwear — different from what will be worn with the finished garment.",
 "Kalıp basımı: PDF kalıp yanlış ölçekte basılmış (test karesi ölçülmemiş)":
   "Printing — a home-printed pattern whose test square was never measured.",
 "Dikiş payı: kalıbın varsaydığından farklı payla dikilmiş":
   "Seam allowance — sewn at a different width from the one the pattern assumes.",
 "Ease: gözlenen fazlalık aslında TASARIM ease'idir (T-07) — kalıbın bitmiş giysi ölçüsü tablosuyla karşılaştırılmadı":
   "Design ease — the excess may be intended. It was never checked against the finished garment measurements.",
 "Kumaş: yıkama/ütü sonrası çekme":
   "Fabric — shrinkage after washing or pressing.",
 "Ölçüm: boy ölçüsü ayakkabıyla veya yanlış duruşta alınmış":
   "Measuring — a length taken wearing shoes, or in the wrong posture.",
 # ── FAZ 4 BAĞIMSIZ İNCELEME: eksik bulunan sınıflar ──────────────────
 "Prova desteği: giysi bel hizasından desteklenmedi veya kapaması iliklenmedi — desteklenmeyen bir prova yanlış hizadan asılır":
   "Support — the garment was not held at the waist or its opening was not fastened.",
 "Ayakkabı: ölçüm ya da prova, giyilecek olandan farklı topuk yüksekliğinde yapıldı":
   "Footwear — a different heel height from the one that will be worn.",
 "Kumaş: ön çekmesi yapılmadı ya da parça asılıp dinlenmeden okundu (verev, gevşek dokuma, ağır kumaş)":
   "Fabric — not preshrunk, or read before it had hung and settled.",
 "Ölçüm yaşı: vücut ölçüleri güncel değil — beden değişti, kayıt değişmedi":
   "Measurement age — the numbers on the card are older than the body.",
 "Kalıp basımı: PDF kalıp yanlış ölçekte basılmış, test karesi tek yönde ölçülmüş, ya da sayfa birleştirmede kayma birikmiş":
   "Printing — wrong scale, a test square measured on one axis only, or drift accumulated across taped pages.",
 "Prova duruşu: okur prova sırasında doğal duruşunda değil — kendi bedenine bakmak için eğilmek ve dönmek de bu sınıfa girer":
   "Posture — not standing as you normally stand. Looking down at yourself counts.",
}

SIZE_FAMILY = "AF-18"   # B-02: bir teşhis değil, bir ÇIKIŞ kapısı

# Başlık ile gözlem cümlesi aynı şeyi söylüyorsa ikisini birden basmak
# tekrardır. Eşik ölçülerek seçildi: 43 girişin benzerlik dağılımında
# 0,55 altındaki tek çift gerçekten farklı bilgi taşıyor.
TITLE_OBS_SIMILARITY = 0.55


def _declares_no_physical_test(test: str) -> bool:
    """Yazılmış test "fiziksel test YOK" diyor mu.

    ⚠ Faz 5'te ÖLÇÜLEN kusur: 129 aday nedenin 8'i "There is no physical
    test" diyordu, ama hemen ardına genel okuma ölçütü ekleniyordu:
    "bu neden, belirti AZALIRSA doğrulanmıştır". Okur aynı maddede önce
    yapacak bir test olmadığını, sonra testin sonucunu okumasını
    söyleniyordu. Bu nedenler kalıp/beden BELGESİYLE kapanır ve zaten
    bir "Confirm by:" satırı taşırlar.
    Regresyon: 07_TESTS/selftest.py § test_no_test_cause_gets_no_reduction_criterion
    """
    import re
    return bool(re.search(r"\bno physical test\b", test, re.I))


def _has_read_criterion(test: str) -> bool:
    """Yazılmış test sonucun nasıl okunacağını zaten söylüyor mu."""
    import re
    return bool(re.search(
        r"\b(if|when|unless)\b.{0,90}?\b(is|are|goes|clears?|disappears?|remains?|"
        r"stays?|settles?|closes?|drops?|persists?|returns?|improves?)\b",
        test, re.I))


def _evidence_clause(evidence: str) -> str:
    """Ayırt edici kanıtı bir yan cümleye çevirir.

    ⚠ F-01'in düzeltmesi bu işlevde durur: doğrulama ölçütü artık
    NEDENİN kendi kanıtına bağlıdır. Kanıt kaydın alanıdır; burada
    yalnızca cümle biçimine sokulur.
    """
    t = evidence.strip()
    return t if t.endswith((".", "!", "?")) else t + "."


def _sign_clause(observation: str) -> str:
    """Gözlem cümlesini bir yan cümleye çevirir."""
    t = observation.strip().rstrip(".")
    return t[0].lower() + t[1:] if t else t


def _too_similar(a: str, b: str) -> bool:
    import difflib
    return difflib.SequenceMatcher(
        None, a.lower().rstrip("."), b.lower().rstrip(".")
    ).ratio() > TITLE_OBS_SIMILARITY


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


class AtlasBuilder:
    def __init__(self, book_id: str, mdir: Path):
        self.signs = {s["symptom_id"]: s for s in load(paths.FIT_SIGNS)["signs"]}
        self.labels = load(paths.LABELS_EN)
        self.families = {f["adjustment_family_id"]: f
                         for f in load(paths.ADJUSTMENT_FAMILIES)["families"]}
        self.measures = {m["measurement_id"]: m
                         for m in load(paths.MEASUREMENTS)["measurements"]}
        self.content = load(mdir / "sign_content_en.json")
        self.mcontent = load(mdir / "measurements_en.json")
        # Faz 4 bağımsız incelemesinin ÇAKIŞMA bulguları. Uydurma bir
        # ayrımla kapatılmadı; okura BEYAN edilir.
        cpath = paths.TAXONOMY_PUBLIC / "evidence_collisions.json"
        self.collisions = {}
        if cpath.exists():
            for c in load(cpath)["collisions"]:
                self.collisions.setdefault(c["symptom_id"], []).append(c)
        self.zones = load(mdir / "zones_en.json")
        self.claims: dict = {}          # blok sırası → iddia kimlikleri
        self.figure_plan: dict = {}     # belirti → kullanılan figürler

    def _landmarks(self, mid: str) -> tuple:
        """Okur karşılığı. TÜRETİLMİŞ ölçülerin işaret noktaları başka
        ölçülerin KİMLİĞİDİR (M-031 = M-002 − M-001) ve o kimlik okura
        dönük bir tabloya basılamaz (K46). Kimlik yerine AD yazılır.

        Bu kusuru build_book.py'nin okur dili kapısı yakaladı; tablo
        elle yazılsaydı da aynı kusur oluşurdu ve kapı yine yakalardı."""
        m = self.measures[mid]
        a, b = m["landmark_start"], m["landmark_end"]
        if m["category"] == "derived":
            return (f"{self.measures[a]['name']} minus {self.measures[b]['name']}",
                    "a calculated difference, not a tape reading")
        return (a, b)

    # ── bir belirti girişi ────────────────────────────────────────────
    def sign_entry(self, sid: str, *, with_chart: bool = True) -> list:
        s = self.signs[sid]
        c = self.content[sid]
        lab = self.labels["signs"][sid]
        out: list = []

        out.append({"type": "h2", "text": c["title"], "claims": [sid]})
        # ⚠ SAYFAYA BAKILARAK BULUNDU. İlk sürüm başlığın hemen ardına
        # gözlem cümlesini basıyordu ve 43 girişin 41'inde ikisi AYNI
        # ŞEYİ söylüyordu — sekizi kelimesi kelimesine. Okur her girişe
        # aynı cümleyi iki kez okuyarak başlıyordu.
        #
        # Hiçbir otomatik kapı bunu görmüyordu: iki alan da doluydu,
        # ikisi de geçerliydi, ikisi de doğruydu. Yalnızca DİZİLMİŞ
        # sayfada görünüyordu. (R-19'un bu turdaki üçüncü örneği.)
        # Paragraf, başlığın SÖYLEMEDİĞİ parçalardan kurulur. Hiçbir
        # parça yeni bilgi taşımıyorsa paragraf HİÇ BASILMAZ — başlık
        # zaten her şeyi söylemiştir ve bir kez söylemek yeter.
        obs_text = lab["observation"].rstrip()
        parts = [x for x in (obs_text, c["where"])
                 if not _too_similar(c["title"], x)]
        if parts:
            out.append({"type": "para", "text": " ".join(parts)})
        if c.get("origin"):
            out.append({"type": "side", "title": "Where it comes from",
                        "text": c["origin"]})
        out.append({"type": "figure", "key": f"sign_{sid}",
                    "caption": c["title"] + "."})

        # ── B-03: BELİRTİYE ÖZGÜ eleme ────────────────────────────────
        conf = [CONFOUNDER_EN[x] for x in s["confounders_to_rule_out"]
                if x in CONFOUNDER_EN][:3]
        if conf:
            out.append({"type": "h3", "text": "Rule these out first"})
            out.append({"type": "bullets", "items": conf})

        # ── aday nedenler ─────────────────────────────────────────────
        #
        # ⚠ FAZ 4 BAĞIMSIZ İNCELEME · CC-25 · KABUL EDİLDİ
        # Taksonomi nedenleri OLASILIK sırasına diziyordu. Ama Adım 6
        # "en ucuz testi önce uygula" diyor ve en ucuz nedenler tam da
        # kalıba dokunmayanlardır (yapım, kesim, prova koşulu, tasarım).
        # İncelemeci ölçtü: 20 kalıp-dışı nedenin HİÇBİRİ ilk sırada
        # değildi; 13'ü SONUNCUYDU. Yani kitap kendi kuralının tersini
        # yaptırıyordu.
        #
        # Sunum sırası bu yüzden KAPI ÖNCE olacak biçimde değiştirildi.
        # Taksonominin olasılık sırası KORUNUR — yalnızca okura önce
        # bedava ve geri alınabilir olanlar gösterilir.
        pairs = list(zip(s["candidate_causes"], c["causes"], lab["causes"]))
        # ── İKİNCİ ÇELİŞMELİ İNCELEME (A-07) ─────────────────────────
        # Bu belirtide iki KARŞIT neden aynı aileye gidiyorsa, aile adı
        # tek başına ne yapılacağını söylemez: omuz eğimi ailesine
        # "daha kare" için de "daha eğik" için de gidilir. Profil YÖNÜ
        # taşımazsa bir sonraki kalıpta ters uygulanır.
        fam_count: dict = {}
        for cz, _, _ in pairs:
            f = cz.get("adjustment_family_ref")
            if f:
                fam_count[f] = fam_count.get(f, 0) + 1
        shared = {f for f, n in fam_count.items() if n > 1}
        # ⚠ BAĞIMSIZ İNCELEME (F-02/F-05): okur ilk "evet"te DURUR. Üç
        # ailenin kendi kaydı "en son" dediği hâlde bazı girişlerde ilk
        # sıradaydı — ve o üçü kitabın GERİ ALINAMAZ dediği işlemler.
        # Sıra artık üç katmandır ve üçü de VERİDEN gelir.
        gates = [p for p in pairs if not p[0].get("adjustment_family_ref")]
        rest = [p for p in pairs if p[0].get("adjustment_family_ref")]
        defer = [p for p in rest
                 if self.families.get(p[0]["adjustment_family_ref"], {})
                 .get("defer_in_diagnosis")]
        rest = [p for p in rest if p not in defer]
        # ⚠ BAĞIMSIZ İNCELEME (F-09): 16 çakışma kutusu "en ucuzu önce"
        # diyordu ve nedenler maliyete göre SIRALANMAMIŞTI — çünkü
        # maliyet hiçbir yerde KAYITLI DEĞİLDİ. Artık kayıtlı
        # (`test_cost`, Bölüm 6 merdiveni) ve sıra ONDAN gelir. Böylece
        # cümle bir iddia olmaktan çıkıp bir OLGU olur.
        rest.sort(key=lambda p: p[0].get("test_cost", 9))
        ordered = gates + rest + defer
        if gates:
            out.append({"type": "h3", "text": "Check these before the pattern"})
            out.append({"type": "para",
                        "text": "These need no pattern change and are the cheapest "
                                "things here to test. If one of them is the cause, "
                                "nothing is cut."})
        # ⚠ Başlık, sıranın GERÇEKTE ne olduğunu söylemek zorundadır.
        # Sıra ÜÇ kuraldan gelir ve ikisi birbirini keser: maliyet
        # ucuzu öne alır, güvenlik geri alınamaz aileyi sona atar. Bir
        # entry'de ikisi çeliştiğinde "en ucuzu önce" YANLIŞ bir vaat
        # olur. Başlık nötr kalır; kural bölüm açılışında BİR KEZ
        # yazılır.
        # ⚠⚠ İKİNCİ İÇERİK TURU · KRİTİK: `c["hold"]` — her belirtinin
        # KENDİ "henüz değiştirme" listesi — HİÇBİR ZAMAN BASILMIYORDU.
        # 43 girişin 43'ünde veri vardı, kitapta sıfır tanesi vardı.
        # `fit_signs.json`'un kendi başlığı bu alan için "bu ürünün
        # rakiplerden en somut ayrıldığı yer" diyor.
        #
        # Kapı ⑤ bunu göremiyordu çünkü "girişte HERHANGİ bir callout
        # var mı" diye soruyordu ve ÇAKIŞMA kutusu bir callout'tu. 28
        # girişte çakışma kutusu vardı, 15'inde yoktu — ve kapı yine de
        # yeşildi, çünkü o 15'i de başka bir callout taşıyordu. Kusur
        # ancak çakışma kutuları KALDIRILINCA ortaya çıktı.
        #
        # Uyarı, NEDENLERDEN ÖNCE basılır: okur neyi yapmayacağını
        # test etmeye BAŞLAMADAN önce bilmelidir.
        if c.get("hold"):
            out.append({"type": "callout", "title": "Do not change yet",
                        "items": c["hold"]})
        if c.get("order"):
            out.append({"type": "para", "text": "Order: " + c["order"]})
        out.append({"type": "h3", "text": "Candidate causes, in testing order"})
        for i, (cause, authored, el) in enumerate(ordered, 1):
            fam = cause.get("adjustment_family_ref")
            out.append({"type": "h3", "text": f"{i}. {el['cause']}",
                        "claims": [f"{sid}.C{i}"]})
            # ⚠ F-09/F-13: okur bir testin NEYE MAL OLDUĞUNU görmeden
            # "en ucuzu önce" talimatını uygulayamaz. Basamak adıyla
            # yazılır ve Bölüm 6'nın merdiveniyle aynı sözcükleri
            # kullanır.
            # ⚠ BAĞIMSIZ İNCELEME · M-6/M-7: yedi test "iğne yeter"
            # diye etiketlenmişti ama metinleri kolu SÖKÜP YENİDEN
            # DİKMEYİ istiyordu. Merdivende o basamağın karşılığı
            # yoktu ve etiket TEST SIRASINI belirlediği için okuru en
            # pahalı işi en öne alıyordu. Basamak eklendi.
            _COST = {0: "costs nothing — a reading",
                     1: "costs nothing — change the fitting condition",
                     2: "reversible — pins only",
                     3: "costs a scrap of calico",
                     4: "reversible — unpick and set again",
                     5: "consumes the fitting garment"}
            _c = cause.get("test_cost")
            _tag = f" ({_COST[_c]})" if _c in _COST else ""
            # ⚠ M-15: iki sayıyı karşılaştırmak bir doğrulama DEĞİLDİR.
            # Farkın hangi yöne çıkarsa hipotezi desteklediği yazılmak
            # zorundadır ve o cümle KAYITTA durur.
            _mline = authored["measure"]
            if cause.get("expected"):
                _mline = _mline.rstrip() + " " + cause["expected"]
            items = [f"Tells it apart: {el['evidence']}",
                     f"Confirm by: {_mline}",
                     f"Test{_tag}: {authored['test']}"]
            # ── İKİNCİ ÇELİŞMELİ İNCELEME · KABUL EDİLDİ ──────────────
            # 129 fiziksel testin 105'i bir EYLEM veriyordu ve sonucun
            # NASIL OKUNACAĞINI söylemiyordu — kitabın bütün bilgi
            # kuramı "testi kumaş çözer" üzerine kuruluyken.
            #
            # Ölçüt UYDURULMADI; zaten belirtinin kendisidir ve Adım
            # 6'da yazılıdır. Burada o ölçüt her nedene BAĞLANIR ve
            # belirtinin KENDİ gözlem cümlesinden türetilir.
            #
            # Yazılmış test zaten bir koşul cümlesi taşıyorsa
            # TEKRARLANMAZ.
            # ⚠ İÇERİK TURU · A-22 SINIFI, İKİNCİ ÖRNEK. Faz 5'in
            # düzeltmesi doğruydu ve UYGULAMASI 34 kelimelik bir kuyruğu
            # 104 kez bastırıyordu — kitabın en çok tekrarlanan metni,
            # yaklaşık 3.500 kelime. Kuyruk üstelik Bölüm 6 Adım 6'nın
            # KELİMESİ KELİMESİNE kopyasıdır: "üç olası sonuç" orada
            # zaten yazılıdır.
            #
            # Girişte kalan şey GİRİŞE ÖZGÜ olandır: bu nedenin hangi
            # gözlemin azalmasıyla doğrulandığı. Genel kural bir kez,
            # ait olduğu yerde durur ve bölüm açılışından bir kez
            # işaret edilir.
            # ⚠ BAĞIMSIZ İNCELEME · F-01 (KRİTİK) — kitabın en ağır
            # mantık kusuru buradaydı. Ölçüt BELİRTİYİ tekrarlıyordu:
            # "şu belirti azaldıysa bu neden doğrulanmıştır". Ama bir
            # girişin üç nedeni AYNI koridora yer açar; üçünün de testi
            # belirtiyi azaltır. Yani ölçüt HANGİ nedeni test ettiyseniz
            # onu onaylıyordu — yanlışlanamayan bir ölçüt, Bölüm 6'nın
            # "onu ÇÜRÜTEBİLECEK en ucuz test" kuralının tam tersi.
            #
            # Ölçüt artık NEDENE ÖZGÜDÜR: belirti azalmalı VE O NEDENİN
            # kendi ayırt edici kanıtı onunla birlikte gitmelidir.
            # Kanıt UYDURULMADI — kaydın kendi alanıdır.
            #
            # Ayrıca ARTIK HER NEDENDE basılır: 129 nedenin 24'ünde
            # yoktu ve eksik olanlar sistematik biçimde BİRİNCİ neden,
            # yani okurun ilk test ettiğiydi.
            if not _declares_no_physical_test(authored["test"]):
                # İki koşul AYRI CÜMLE olarak kurulur: ayırt edici kanıt
                # kayıtta TAM CÜMLEDİR ve bir yan cümleye zorlanırsa
                # dilbilgisi bozulur.
                # Belirtiyi BURADA tekrarlamaz: başlık ve gözlem cümlesi
                # zaten aynı sayfada, birkaç santim yukarıda. Tekrar
                # eden şey ayırt etmiyordu; ayırt eden şey NEDENİN
                # kendi kanıtıdır ve ölçüt onu ister.
                # ⚠ İLK YAZIMDA bu satırın kuyruğu 24 kelimeydi ve 118
                # kez basılıyordu (≈12 sayfa) — düzelttiğim kusurun
                # kendisiyle aynı sınıf. Kuyruk GENEL bir ilkedir ve
                # bölüm açılışında BİR KEZ durur; girişte yalnızca O
                # NEDENE ÖZGÜ ölçüt kalır.
                items.append(
                    "Read it: the sign must reduce, and this must go with it — "
                    + _evidence_clause(el["evidence"]))
            # ⚠ Faz 5: bir neden metni BİRDEN ÇOK duruma işaret edip TEK
            # aileye çıkıyorsa, öteki durumu yaşayan okur YANLIŞ aileye
            # gider. `cross_route` o okuru kendi ailesine yollar.
            # ⚠ M-13: alan LİSTE oldu — bir nedenin üç varışı varsa
            # üçü de yazılır; ikisi birinin içine katlanmaz.
            for cr in (cause.get("cross_routes") or []):
                cf = self.families.get(cr["family_ref"], {}).get("name",
                                                                 cr["family_ref"])
                items.append(self.labels["ui"]["cross_route"]
                             .format(cond=cr["condition_en"], fam=cf.lower()))
            if fam == SIZE_FAMILY:
                # B-02 — bir düzeltme değil, bir çıkış kapısı
                items.append("This is not an adjustment. It is a size decision, and the "
                             "answer is in Chapter 3, not in a pattern change.")
            elif fam:
                line = f"Leads to: {self.families[fam]['name'].lower()}."
                # ⚠ BAĞIMSIZ İNCELEME (F-15): bu not AYNI aileye çıkan
                # HER çifte basılıyordu ve sekiz çiftin YEDİSİNDE
                # yanlıştı — iki neden aynı aileye çıkıp aynı yöne
                # gidebilir (ikisi de bel alır, ikisi de ağ uzatır).
                # Yön iddiası artık KAYITTAN gelir: yalnızca
                # `opposite_of` beyan edilmiş nedenlerde basılır.
                if cause.get("opposite_of"):
                    line += (" Another cause on this sign leads to the same family in "
                             "the OPPOSITE direction — record which one you confirmed, "
                             "and in which direction, not just the family name.")
                elif fam in shared:
                    line += (" Another cause on this sign leads to the same family. "
                             "Record which one you confirmed, not just the family name: "
                             "they act at different places within it.")
                items.append(line)
            else:
                # ⚠ BAĞIMSIZ İNCELEME · M-3/M-4: tek bir cümle İKİ AYRI
                # durumu birleştiriyordu. Kesim, dikiş ve tasarım
                # nedenleri gerçekten kalıp hatası değildir. Ama ön
                # bindirme genişliği ve kap çentikleri KALIP
                # PARAMETRESİDİR: metin "kalıpta hiçbir şey yok" derken
                # testin kendisi kalıp parçasını değiştiriyordu ve okur
                # hiçbir şey kaydetmeyip aynı dar bandı bir dahaki sefer
                # yine kesiyordu. Sınıf artık KAYITTA durur.
                if cause.get("no_family_reason") == "pattern_parameter_no_family":
                    items.append(
                        "Leads to: no adjustment family — this is a pattern "
                        "parameter, not a shape correction. Write the number you "
                        "measured on your profile: the change is made on the pattern "
                        "before the next cut, and Book 2 has no separate entry for it "
                        "because there is no shape to move.")
                else:
                    items.append("Leads to: nothing on the pattern. "
                                 "This is not a pattern fault.")
            if authored.get("note"):
                items.append(authored["note"])
            out.append({"type": "bullets", "items": items})

        # ── ÇAKIŞAN KANIT — bağımsız inceleme bulgusu, okura BEYAN ────
        #
        # Şema her nedenin bir ayırt edici kanıt taşımasını dayatıyordu;
        # incelemeci o kanıtların 28 belirtide GERÇEKTEN ayırmadığını
        # ölçtü. Sahte bir ayrım yazmak kolaydı ve yanlış olurdu. Kitap
        # bunun yerine okura durumu SÖYLER — bir teşhis kitabının en az
        # yapabileceği şey, nerede teşhis koyamadığını bilmektir.
        for col in self.collisions.get(sid, []):
            status = col.get("collision_status", "requires_physical_test")
            # ⚠ İKİNCİ İÇERİK TURU · F-10: 13 çakışma ARTIK muayeneyle
            # ayrılıyor. Okura "bu ikisi ayırt edilemez" demek, ayırt
            # eden gözlemi yapmaktan VAZGEÇİRİR — kutu basılmaz.
            if status == "separable_by_inspection":
                continue
            names = []
            for ref in col["causes"]:
                try:
                    k = int(ref.rsplit(".C", 1)[1]) - 1
                    names.append(lab["causes"][k]["cause"].lower())
                except (ValueError, IndexError):
                    continue
            if len(names) < 2:
                continue
            n = len(names)
            joined = ", ".join(names[:-1]) + " and " + names[-1]
            if status == "superset":
                # Bir KAPSAMA ilişkisidir: ikincisi birincinin gördüğü
                # her şeyi görür ve ÜSTÜNE bir işaret ekler. Okura ne
                # ARAYACAĞI söylenir.
                out.append({"type": "callout",
                            "title": "ONE OF THESE IS THE OTHER PLUS ONE MORE THING",
                            "items": [
                                "On this sign, " + joined + " look alike because the "
                                "second shows everything the first shows.",
                                "What separates them is " +
                                col.get("superset_en", "the extra sign named above") +
                                ". Look for that before you choose.",
                                "If it is there, take the second. If it is genuinely "
                                "absent, take the first and test it."]})
                continue
            # ⚠ BAĞIMSIZ İNCELEME (LOW): kutu "sonuç karar versin" diyor
            # ama ayrılamayan nedenler FARKLI Kitap 2 ailelerine
            # çıktığında okurun HANGİSİNİ yazacağını söylemiyordu.
            # Ayrım yapamayan bir kutu, hiç değilse ne kaydedileceğini
            # söylemek zorundadır. Aile adları KAYITTAN gelir.
            dests = []
            for ref in col["causes"]:
                try:
                    k = int(ref.rsplit(".C", 1)[1]) - 1
                    f_ = s["candidate_causes"][k].get("adjustment_family_ref")
                except (ValueError, IndexError):
                    continue
                if f_ and f_ not in dests:
                    dests.append(f_)
            tail = ["This is a known limit of the method as this book states "
                    "it, not something you have missed."]
            if len(dests) > 1:
                fam_names = " and ".join(
                    self.families[f_]["name"].lower() for f_ in dests)
                tail.insert(0,
                            "They do not lead to the same correction: " + fam_names +
                            " are separate entries in Book 2. Record the one whose "
                            "test worked — not both, and not the pair.")
            out.append({"type": "callout",
                        "title": ("THESE TWO CAN LOOK THE SAME" if n == 2
                                  else f"THESE {n} CAN LOOK THE SAME"),
                        "items": [
                            "On this sign, " + joined +
                            " can produce the same appearance, and the evidence above "
                            "does not reliably separate them.",
                            "Test " + ("both" if n == 2 else f"all {n}") +
                            " in the order they are printed above — that order is set "
                            "by what each test costs you — and let the result decide, "
                            "not the eye."] + tail})

        # ⚠ Her girişin KARAR ŞEMASI — F-10 düzenlemesinde yanlışlıkla
        # silinmişti ve 43 figür kitaptan düştü. Sayfa sayısındaki 38
        # sayfalık düşüş yakaladı; kapı değil, ÖLÇÜM yakaladı.
        out.append({"type": "figure", "key": f"flow_{sid}",
                    "caption": "The decision path for this sign."})

        # ── B-01: YENİDEN GÖZLEM — her girişin ZORUNLU son adımı ──────
        out.append({"type": "h3", "text": "Look again"})
        out.append({"type": "para", "text": c["reobserve"]})
        # ── FAZ 4 BAĞIMSIZ İNCELEME · CC-21 · KABUL EDİLDİ ────────────
        # İlk sürüm "azaldı ama gitmedi = ikinci bir neden var" diyordu.
        # İnceleme bunun MANTIK HATASI olduğunu ve hiçbir kaynağı
        # bulunmadığını gösterdi: kısmi iyileşme en az o kadar sık DOĞRU
        # nedenin YETERSİZ düzeltilmesidir — yerleşik uygulama zaten
        # "küçük başla, teyelle, tekrar dene" der. Yanlış hâliyle okuru
        # olmayan bir ikinci nedenin peşine gönderirdi.
        #
        # Düzeltme YAPISALDIR, 43 metnin tek tek elden geçirilmesi
        # değil: iki dal her girişte AYNI sırayla çıkar ve yazılmış
        # metin yalnızca İKİNCİ dalın içeriğini verir.
        # ── İÇERİK TURU · A-22 (Faz 4 incelemesi, o turda KAPATILMADI)
        # Bu paragraf 43 girişte KELİMESİ KELİMESİNE aynıydı: 2.000
        # kelime, yaklaşık yedi sayfa. Okur onu üçüncü girişte atlamayı
        # öğreniyor ve atladığı anda SONUNDAKİ tek girişe özgü cümleyi
        # de atlıyordu — kitabın o girişteki tek özgün cevabını.
        #
        # Kural bir kez, ait olduğu yerde (Bölüm 6, döngünün 7. adımı)
        # yazılır. Girişte yalnızca AYAKTA DURAN bir başlık ve GİRİŞE
        # ÖZGÜ olan kısım basılır. Bilgi kaybı YOKTUR; tekrar kaybolur.
        out.append({"type": "para",
                    "text": "Reduced but not gone? The two branches are in Chapter 6. "
                            "On this sign, the second cause to suspect is this: "
                            + c["partial"]})
        return out

    # ── Bölüm 2 — ölçü bölümü de ÜRETİLİR ─────────────────────────────
    # Aynı gerekçe: 32 ölçü girişinin yapısı bir spesifikasyondur. Elle
    # yazılsaydı bir ölçü er geç 'sık yapılan hata' satırını taşımazdı.
    def measurement_chapter(self) -> list:
        mc = self.mcontent
        blocks: list = [
            {"type": "recto"},
            {"type": "h1", "text": "Measuring your body", "kicker": "Chapter 2"},
            {"type": "lead", "text": "A measurement that cannot be repeated is not a "
                                     "measurement. This chapter is about repeatability "
                                     "more than it is about numbers."},
            {"type": "h2", "text": "Conditions"},
            {"type": "para", # ⚠ Faz 5 (İnceleme A-06): burası ÖLÇÜM bölümüdür ve kitabın kendi
            # M-024/M-030 kayıtları "without shoes" diyor, hatta "measured
            # wearing shoes" hatasını listeliyor. Bu cümle PROVA kuralını
            # (Bölüm 5) tekrarlayıp ölçü kayıtlarıyla çelişiyordu.
            "text": "Measure in the underwear you will wear with the "
                                     "garment, and barefoot — two of these measurements "
                                     "run to the floor and shoes change them. Note the "
                                     "heel height you intend to wear instead: the "
                                     "fitting session is done in those shoes, and the "
                                     "hem is judged there, not here. Stand as you "
                                     "normally stand, not at "
                                     "attention. Have someone else hold the tape wherever "
                                     "you can — twenty of the measurements in this "
                                     "chapter cannot be taken reliably on yourself."},
            {"type": "para", "text": "The tape lies flat, level with the floor for "
                                     "anything horizontal, and it does not press in. A "
                                     "tape pulled tight records a body smaller than the "
                                     "one that will wear the garment, and every garment "
                                     "made from those numbers will be tight everywhere "
                                     "at once — which reads like a size problem and is "
                                     "not one."},
            {"type": "h2", "text": "Mark the waist first"},
            {"type": "para", "text": "Before anything else, tie a narrow elastic or a "
                                     "length of cord around your waist and let it settle "
                                     "where it wants to sit. Leave it there for the whole "
                                     "session."},
            {"type": "figure", "key": "toile_marking_waist",
             "caption": "Finding the waist with an elastic and marking it. Every vertical "
                        "measurement in this book is read from this line."},
            # ⚠ İÇERİK TURU · L-3: bu cümle bir tanımı "the clothing size
            # standard"a atfediyordu. O standart (ISO 8559-1) DEPOYA
            # EDİNİLMEMİŞTİR ve ilgili maddesine ULAŞILAMAMIŞTIR —
            # kitabın kendi kaydı bunu yazıyor. Bir kitap, okuyamadığı
            # bir belgenin ne dediğini okura SÖYLEYEMEZ. Atıf, tam
            # metni bu turda okunan kaynağa taşındı.
            {"type": "para", "text": "This matters more than it looks. Sources do not "
                                     "agree on where a natural waist is. The public "
                                     "health survey manual behind many published body "
                                     "measurements defines it by bone — a horizontal "
                                     "line just above the top edge of the hip bone, "
                                     "found by feeling for it at the side. The sewing "
                                     "guides define it by shape or by habit instead: the "
                                     "narrowest point of the torso, the level of the "
                                     "navel, or simply where a belt sits. On one body "
                                     "those can be several centimetres apart."},
            {"type": "para", "text": "This book does not settle that argument, because it "
                                     "does not need to. What it needs is that your waist "
                                     "is in the same place every time you measure. A "
                                     "waist defined by a mark is repeatable; a waist "
                                     "defined by a word is not."},
            {"type": "side", "title": "The rule underneath",
             "text": "Where a measurement starts and ends IS the measurement. Its name "
                     "is not enough."},
            {"type": "h2", "text": "Mark the bust apex"},
            {"type": "para", "text": "Four measurements in this chapter run to or from "
                                     "the bust apex — the fullest point of the bust, "
                                     "wearing the bra you will wear with the garment. It "
                                     "moves with the bra, which is why the bra is part of "
                                     "the measuring conditions rather than an afterthought. "
                                     "Find it in a mirror, mark it, and take all four "
                                     "from the same mark."},
            {"type": "h2", "text": "Mark the four points you will measure from"},
            {"type": "para", "text": "Four points on the upper body anchor nine of the "
                                     "measurements in this chapter and every shoulder "
                                     "diagnosis in Part Four. Two of them you can feel. "
                                     "Two of them you have to agree with yourself and "
                                     "then mark — and marking them is not a lesser kind "
                                     "of accuracy, it is the only kind available."},
            {"type": "numbered", "items": [
                "The NAPE. Bend your head forward and run a finger down the back of your "
                "neck. The bone that stands out furthest is it. Mark it. This one is "
                "found, not agreed.",
                "The SHOULDER POINT. Run your fingers out along the top of your shoulder "
                "until you feel the bone end and the arm begin. That corner is it. Raise "
                "your arm halfway and you will feel it move; drop the arm before you "
                "mark. This one is found too.",
                "The SIDE NECK POINT, where the neck meets the shoulder. There is no bone "
                "here and no source settles it. Put a narrow cord around the base of your "
                "neck and let it fall where it wants to sit — the published guide this "
                "book follows ties a string at the neck base for exactly this — and mark "
                "where the cord crosses the top of your shoulder.",
                "The THROAT HOLLOW, the dip at the centre front between the collarbones. "
                "Feel for the notch in the bone and mark the bottom of it."]},
            {"type": "para", "text": "Two of these four are agreed rather than found, and "
                                     "that has a consequence worth saying plainly: your "
                                     "numbers are repeatable for YOU, and not "
                                     "necessarily comparable with anyone else's. That is "
                                     "enough for everything this book asks of them, "
                                     "because every comparison it asks for is between "
                                     "your body and your pattern. It is not enough for "
                                     "quoting a shoulder length to another sewer as "
                                     "though it were a standard figure."},
            {"type": "callout", "title": "Do not change yet", "items": [
                "Do not measure from a point you have not marked. Half of the "
                "measurements in this chapter start at one of these four, and a point "
                "chosen fresh each time is not a landmark.",
                "Do not wash the marks off between the measuring session and the fitting "
                "session. Chapter 5 reads the shoulder seam against the same marks."]},
            {"type": "figure", "key": "lmk_neck_shoulder",
             "caption": "The four points. Two are bone and can be found; two are agreed "
                        "and must be marked."},
            {"type": "h2", "text": "Measure everything twice"},
            {"type": "para", "text": "Take each measurement, write it down, take the tape "
                                     "off, and take it again. If the two readings differ "
                                     "by more than a few millimetres, your method varied "
                                     "and neither number is trustworthy yet. Repeat until "
                                     "two readings agree, and record the agreed number."},
            {"type": "para", "text": "This is not perfectionism. It is the only way to "
                                     "tell later whether a difference between you and a "
                                     "pattern is real or is measurement noise — and every "
                                     "diagnosis in Part Four rests on that distinction."},
        ]
        for g in mc["groups"]:
            blocks.append({"type": "h2", "text": g["title"]})
            blocks.append({"type": "para", "text": g["intro"]})
            for mid in g["ids"]:
                m = self.measures[mid]
                a = mc["m"][mid]
                blocks.append({"type": "h3", "text": m["name"], "claims": [mid]})
                blocks.append({"type": "para", "text": a["how"] + " " + a["why"]})
                items = ["Most common errors: " + " ".join(a["errors"])]
                if a.get("helper") or m.get("helper_required"):
                    items.append("Needs a second person, or a photograph taken from the "
                                 "side or the back.")
                if mid in mc["conflicts"]:
                    items.append("Sources differ here — see the note below.")
                if mid in mc.get("divergences", {}):
                    items.append("This book departs from its source here — see the note "
                                 "below.")
                blocks.append({"type": "bullets", "items": items})
                if mid in mc["conflicts"]:
                    blocks.append({"type": "side", "title": "Sources differ",
                                   "text": mc["conflicts"][mid]})
                # ⚠ İÇERİK TURU: "kaynaklar çelişiyor" ile "bu kitap
                # kaynağından ayrılıyor" AYNI ŞEY DEĞİLDİR. Birincisi
                # alanın çözmediği bir sorudur ve okur onu bilmelidir;
                # ikincisi bu kitabın verdiği bir karardır ve okur ONU
                # da bilmelidir — ama ikisini tek kutuda göstermek,
                # kitabın kendi kararını alanın anlaşmazlığı gibi
                # sunmaktır.
                if mid in mc.get("divergences", {}):
                    blocks.append({"type": "side",
                                   "title": "Where this book differs from its source",
                                   "text": mc["divergences"][mid]})
                # ⚠ FAZ 4 ÖLÇÜMÜ: ilk tam dizgide 29 ölçüm figürünün
                # HİÇBİRİ kitapta yer almıyordu. Bir ölçü bölümünün işi
                # "şerit nereden nereye gider"i göstermektir; metin tek
                # başına onu yapamaz. Kapılar yeşildi ve ürün eksikti —
                # B-10 sınıfı bir kusur. qa_manuscript.py artık her
                # ölçünün figürünü ARIYOR.
                # ⚠ M-13: başlık NİRENGİ TÜRÜNDEN türer. 30 figürün
                # hepsine "her iki nirengi de görünür" basmak, bir
                # düzininde YANLIŞTI ve kitabın kendi tekrarlanabilirlik
                # ölçütüyle çelişiyordu.
                # Başlıklar KISA tutulur: uzun başlık figürü sayfadan
                # taşırır ve nirenginin türü zaten tek cümlede söylenir.
                _K = {
                  "bone": f"{m['name']} — both ends are bone, findable by feel.",
                  "marked": f"{m['name']} — runs between marks you made.",
                  "fullest": f"{m['name']} — one end is a fullest point, not a bone.",
                  "level": f"{m['name']} — the level is measured down from your waist mark.",
                  "derived": f"{m['name']} — how the number is arrived at.",
                }
                cap = _K.get(m.get("landmark_kind"),
                             f"{m['name']}: the path the tape takes.")
                blocks.append({"type": "figure", "key": f"meas_{mid}", "caption": cap})
        blocks.append({"type": "h2", "text": "The six errors worth seeing"})
        blocks.append({"type": "para",
                       "text": "Six mistakes account for most unrepeatable measurements. "
                               "Each is shown wrong and right side by side."})
        for key, cap in (
            ("cmp_tape_slipped_back", "The tape has dropped at the back. Everything "
                                      "horizontal reads small."),
            ("cmp_arms_raised", "Arms raised. The high bust reads large and the size "
                                "decision goes the wrong way."),
            ("cmp_tape_too_tight", "The tape is pulled tight. The body it records is not "
                                   "the body that will wear the garment."),
            ("cmp_waist_guessed", "The waist was not marked. The next reading will be "
                                  "taken somewhere else."),
            ("cmp_hip_too_high", "The hip was not taken at the fullest point."),
            ("cmp_posture_leaning", "Leaning forward to see the tape. The measurement is "
                                    "of a posture you will not wear."),
        ):
            blocks.append({"type": "figure", "key": key, "caption": cap})
        blocks.append({"type": "h2", "text": "Exercise 2A — your measurement card"})
        blocks.append({"type": "para",
                       "text": "Fill in the measurement card below. Take five of the "
                               "decision-bearing measurements twice — high bust, full "
                               "bust, waist, full hip and centre back length — and record "
                               "both readings and the difference. Date it. You will "
                               "compare against this card every time you use this book, "
                               "and you will retake it when the numbers stop matching "
                               "your body."})
        # Diğer üç boş form 26 pt satır yüksekliği beyan eder; bu form
        # etmiyordu ve varsayılan 15,3 pt'ye (aslında 5,2 pt'ye) düşüyordu.
        blocks.append({"type": "figtable", "key": "tbl_form_measurement_card",
                       "row_pt": 26.0,
                       "caption": "The measurement card. Two readings, and the difference "
                                  "between them."})
        return blocks

    # ── bir bölge bölümü ──────────────────────────────────────────────
    def chapter(self, key: str, *, with_charts: bool = True) -> tuple:
        z = self.zones[key]
        # ⚠ Faz 5: bütün-giysi bölümü (`B1-CH16-ATLAS`) verisinde
        # `number: 16` taşır ve Bölüm 16 ("The order of work") da 16'dır.
        # İçindekilerden "16b" kaldırıldı ama SAYFA ÜSTÜNDEKİ kicker
        # kalmıştı: s. 221 ve s. 225 ikisi de "CHAPTER 16" basıyordu.
        # Bu bölüm bir BÖLGE değildir; numarasız basılır — tıpkı
        # "How to use this book" ve "Appendices" gibi.
        kicker = None if key == "B1-CH16-ATLAS" else f"Chapter {z['number']}"
        blocks: list = [{"type": "recto"},
                        {"type": "h1", "text": z["title"], "kicker": kicker},
                        {"type": "lead", "text": z["lead"]}]
        blocks.append({"type": "h2", "text": "What this region is"})
        for p in z["anatomy"]:
            blocks.append({"type": "para", "text": p})
        blocks.append({"type": "figure", "key": z["landmark_figure"],
                       "caption": "The landmarks this chapter is written from. Find them "
                                  "on your own body before you read further."})

        blocks.append({"type": "h2", "text": "The measurements you read here"})
        blocks.append({"type": "para", "text": z["measure_intro"]})
        rows = [["Measurement", "Read from", "To"]]
        for mid in z["measures"]:
            rows.append([self.measures[mid]["name"], *self._landmarks(mid)])
        blocks.append({"type": "table", "rows": rows, "widths": [0.26, 0.40, 0.34]})

        blocks.append({"type": "h2", "text": "Before you change anything in this region"})
        blocks.append({"type": "callout", "title": "Do not change yet", "items": z["hold"]})

        blocks.append({"type": "h2", "text": "The signs"})
        blocks.append({"type": "para",
                       "text": "Each entry below opens with three things most often "
                               "mistaken for that particular sign. They are drawn from "
                               "the full rule-out list in Chapter 8, which you walk once "
                               "at the start of a fitting rather than once per sign. The "
                               "drawings are schematic: they show where a sign sits, not "
                               "how much fabric is involved."})
        # ⚠ İÇERİK TURU: sonucun NASIL OKUNACAĞI kuralı Bölüm 6 Adım
        # 6'da yazılıdır ve girişlerde 104 kez TEKRARLANIYORDU. Bölüm
        # başına BİR KEZ işaret edilir; girişler yalnızca o girişe özgü
        # ölçütü taşır.
        blocks.append({"type": "para",
                       "text": "The causes under each sign are printed in the order to "
                               "test them, and that order is set by three things in "
                               "turn. Anything that needs no pattern change at all comes "
                               "first — it is free and it is often the answer. Then the "
                               "rest, ordered by what the test costs you: a reading, "
                               "then pins, then a scrap of calico, then unpicking and "
                               "setting a seam again, then cutting the "
                               "fitting garment. Last come the causes whose correction "
                               "cannot be undone — the armhole, the sleeve cap and the "
                               "neckline — however cheap their test looks, because "
                               "everything above them changes them."})
        blocks.append({"type": "para",
                       "text": "Where a test names an amount — five millimetres at a "
                               "shoulder tip, a centimetre at a slash — that number is a "
                               "starting step, not a threshold. It comes from ordinary "
                               "practice rather than from any published figure, and this "
                               "book has none to give you. Start there, look, and go "
                               "again if the sign moved in the right direction but not "
                               "far enough."})
        blocks.append({"type": "para",
                       "text": "Every cause ends with a line beginning \u201cRead "
                               "it\u201d, and it names TWO things that have to happen "
                               "together: the sign itself must reduce, and the "
                               "observation that told this cause apart must go with it. "
                               "Both matter. The three causes under one sign usually "
                               "make room in the same place, so any of the three tests "
                               "will ease the sign — if only the sign eases and the "
                               "second observation does not change, you have eased the "
                               "symptom without finding the cause. What the other two "
                               "outcomes mean — the sign unchanged, or a new sign "
                               "appearing somewhere else — is set out once in Chapter 6, "
                               "step six."})
        sids = [sid for sid, s in self.signs.items() if s["zone"] in z["zones"]]
        for sid in sids:
            blocks.extend(self.sign_entry(sid, with_chart=with_charts))

        blocks.append({"type": "h2", "text": "Where this leads"})
        blocks.append({"type": "para", "text": z["handoff"]})
        blocks.append({"type": "bullets",
                       "items": [self.families[f]["name"] for f in z["b2_families"]]})
        return blocks, sids
