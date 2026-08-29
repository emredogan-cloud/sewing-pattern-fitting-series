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


def _has_read_criterion(test: str) -> bool:
    """Yazılmış test sonucun nasıl okunacağını zaten söylüyor mu."""
    import re
    return bool(re.search(
        r"\b(if|when|unless)\b.{0,90}?\b(is|are|goes|clears?|disappears?|remains?|"
        r"stays?|settles?|closes?|drops?|persists?|returns?|improves?)\b",
        test, re.I))


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
        gates = [p for p in pairs if not p[0].get("adjustment_family_ref")]
        rest = [p for p in pairs if p[0].get("adjustment_family_ref")]
        ordered = gates + rest
        if gates:
            out.append({"type": "h3", "text": "Check these before the pattern"})
            out.append({"type": "para",
                        "text": "These need no pattern change and are the cheapest "
                                "things here to test. If one of them is the cause, "
                                "nothing is cut."})
        out.append({"type": "h3", "text": "Candidate causes"} if not gates
                   else {"type": "h3", "text": "Candidate causes, cheapest test first"})
        for i, (cause, authored, el) in enumerate(ordered, 1):
            fam = cause.get("adjustment_family_ref")
            out.append({"type": "h3", "text": f"{i}. {el['cause']}",
                        "claims": [f"{sid}.C{i}"]})
            items = [f"Tells it apart: {el['evidence']}",
                     f"Confirm by: {authored['measure']}",
                     f"Test: {authored['test']}"]
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
            if not _has_read_criterion(authored["test"]):
                items.append(
                    "Read it: this cause is confirmed if — " + _sign_clause(obs_text) +
                    " — is reduced and no new sign appears anywhere else. If the sign "
                    "is unchanged the hypothesis was wrong; if a new sign appears, "
                    "fabric was moved rather than added.")
            if fam == SIZE_FAMILY:
                # B-02 — bir düzeltme değil, bir çıkış kapısı
                items.append("This is not an adjustment. It is a size decision, and the "
                             "answer is in Chapter 3, not in a pattern change.")
            elif fam:
                line = f"Leads to: {self.families[fam]['name'].lower()}."
                if fam in shared:
                    line += (" Another cause on this sign leads to the same family in "
                             "the OPPOSITE direction — record which one you confirmed, "
                             "and in which direction, not just the family name.")
                items.append(line)
            else:
                items.append("Leads to: nothing on the pattern. This is not a pattern fault.")
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
            names = []
            for ref in col["causes"]:
                try:
                    k = int(ref.rsplit(".C", 1)[1]) - 1
                    names.append(lab["causes"][k]["cause"].lower())
                except (ValueError, IndexError):
                    continue
            if len(names) < 2:
                continue
            out.append({"type": "callout", "title": "These two can look the same",
                        "items": [
                            "On this sign, " + " and ".join(names) +
                            " can produce the same appearance, and the evidence above "
                            "does not reliably separate them.",
                            "Do not choose between them by eye. Test both, cheapest "
                            "first, and let the result decide.",
                            "This is a known limit of the published evidence rather "
                            "than something you have missed."]})

        # ── henüz değiştirme ──────────────────────────────────────────
        out.append({"type": "callout", "title": "Do not change yet", "items": c["hold"]})
        if c.get("order"):
            out.append({"type": "para", "text": "Order: " + c["order"]})

        # ── akış şeması ───────────────────────────────────────────────
        if with_chart:
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
        out.append({"type": "para",
                    "text": "If the sign is reduced but has not gone, there are two "
                            "possibilities and they call for different answers. The "
                            "commoner one is that the cause was right and the amount "
                            "was too small — increase it and test again before you "
                            "look for anything else. The other is that a second cause "
                            "is present as well: " + c["partial"]})
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
            {"type": "para", "text": "Measure in the underwear you will wear with the "
                                     "garment, and in shoes of the heel height you will "
                                     "wear with it. Stand as you normally stand, not at "
                                     "attention. Have someone else hold the tape wherever "
                                     "you can — nineteen of the measurements in this "
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
            {"type": "para", "text": "This matters more than it looks. Sources do not "
                                     "agree on where a natural waist is: the clothing "
                                     "size standard defines it as midway between the "
                                     "lowest rib and the top of the hip bone, other "
                                     "authorities use the narrowest point of the torso, "
                                     "the level of the navel, or simply where a belt "
                                     "sits. On one body those can be several centimetres "
                                     "apart."},
            {"type": "para", "text": "This book does not settle that argument, because it "
                                     "does not need to. What it needs is that your waist "
                                     "is in the same place every time you measure. A "
                                     "waist defined by a mark is repeatable; a waist "
                                     "defined by a word is not."},
            {"type": "side", "title": "The rule underneath",
             "text": "Where a measurement starts and ends IS the measurement. Its name "
                     "is not enough."},
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
                blocks.append({"type": "bullets", "items": items})
                if mid in mc["conflicts"]:
                    blocks.append({"type": "side", "title": "Sources differ",
                                   "text": mc["conflicts"][mid]})
                # ⚠ FAZ 4 ÖLÇÜMÜ: ilk tam dizgide 29 ölçüm figürünün
                # HİÇBİRİ kitapta yer almıyordu. Bir ölçü bölümünün işi
                # "şerit nereden nereye gider"i göstermektir; metin tek
                # başına onu yapamaz. Kapılar yeşildi ve ürün eksikti —
                # B-10 sınıfı bir kusur. qa_manuscript.py artık her
                # ölçünün figürünü ARIYOR.
                cap = (f"{m['name']}: how the number is arrived at."
                       if m["category"] == "derived" else
                       f"{m['name']}: the path the tape takes. Both landmarks are "
                       f"visible so the path can be repeated.")
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
                       "text": "Fill in the card opposite. Take five of the "
                               "decision-bearing measurements twice — high bust, full "
                               "bust, waist, full hip and centre back length — and record "
                               "both readings and the difference. Date it. You will "
                               "compare against this card every time you use this book, "
                               "and you will retake it when the numbers stop matching "
                               "your body."})
        blocks.append({"type": "figtable", "key": "tbl_form_measurement_card",
                       "caption": "The measurement card. Two readings, and the difference "
                                  "between them."})
        return blocks

    # ── bir bölge bölümü ──────────────────────────────────────────────
    def chapter(self, key: str, *, with_charts: bool = True) -> tuple:
        z = self.zones[key]
        blocks: list = [{"type": "recto"},
                        {"type": "h1", "text": z["title"],
                         "kicker": f"Chapter {z['number']}"},
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
        sids = [sid for sid, s in self.signs.items() if s["zone"] in z["zones"]]
        for sid in sids:
            blocks.extend(self.sign_entry(sid, with_chart=with_charts))

        blocks.append({"type": "h2", "text": "Where this leads"})
        blocks.append({"type": "para", "text": z["handoff"]})
        blocks.append({"type": "bullets",
                       "items": [self.families[f]["name"] for f in z["b2_families"]]})
        return blocks, sids
