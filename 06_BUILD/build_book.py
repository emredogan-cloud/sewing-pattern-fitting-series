#!/usr/bin/env python3
"""
build_book.py — Kitap 1'in TAM manüskriptini dizer ve ÖLÇER.

Faz 4. Pilot (`build_pilot.py`) tek bir kesiti dizerdi; bu script
kitabın tamamını dizer ve üç şeyi aynı anda üretir:

  ① 09_OUTPUT/BOOK_01.pdf            — dizilmiş kitap (.gitignore § ⑥)
  ② 02_CONTENT/public/manuscript_index.public.json
                                     — ÖLÇÜM: bölüm, sayfa, figür, iddia
  ③ stdout                           — sayfa bütçesi raporu

② PROZA TAŞIMAZ. Depo bir yayın-öncesi metin arşivi değildir
(`.gitignore § ①`, `DECISIONS.md K9`); ölçüm public, metin protected.

DİZGİ: `typeset.py` — pilotla AYNI motor. İkinci bir dizgi yolu yoktur.
FİGÜR: `figure_engine.render()` — ikinci bir çizim yolu yoktur.

SAYFA BÜTÇESİ bir uyarı değil, bir KAPIDIR: `series_config.json`
`pageTargetProvisional` bandının dışına çıkılırsa çıkış kodu 1'dir.
Çelişmeli inceleme `B-08` bunu Faz 4 kısıtı olarak yazdı; cilt payı
300 sayfada değişir ve bütün sayfa geometrisi yeniden hesaplanır.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from figure_engine import Engine  # noqa: E402
from typeset import Typesetter, run_blocks  # noqa: E402
from atlas import AtlasBuilder  # noqa: E402

from bookplan import (MANUSCRIPT_DIR, GENERATED, PARTS,  # noqa: E402
                      CHAPTER_TITLES, CHAPTER_BY_NUMBER, fill_index_slots,
                      INTERNAL_ID)  # TEK KOPYA — bookplan.py

READER_FIELDS = ("text", "caption", "title")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def check_reader_language(blocks: list, where: str) -> list:
    """İç kayıt kimliği okura dönük metinde GEÇEMEZ.

    Faz 2'de aynı kusur figürlerde bulundu (B-10 / K46) ve orada
    kapatıldı. Aynı kapı metin katmanında da olmalıdır; yoksa kusur
    yalnızca yer değiştirmiş olur."""
    bad = []
    for i, b in enumerate(blocks):
        vals = [b.get(f) for f in READER_FIELDS if isinstance(b.get(f), str)]
        vals += [str(x) for x in (b.get("items") or [])]
        for r in (b.get("rows") or []):
            vals += [str(c) for c in r]
        for v in vals:
            m = INTERNAL_ID.search(v)
            if m:
                bad.append(f"{where} blok {i} ({b['type']}): iç kimlik {m.group(0)!r} "
                           f"okur metninde — «{v[:70]}»")
    return bad


def resolve_cross_references(blocks: list, page_of: dict,
                             apx_of: dict | None = None) -> list:
    """'Chapter 8' → 'Chapter 8 (page 71)'.

    İkinci çelişmeli inceleme (A-05): kitaptaki ~45 iç atıfın HİÇBİRİ
    sayfa numarası taşımıyordu. Bir başvuru kitabında 'bkz. Bölüm 8'
    okuru 231 sayfanın içinde yalnız bırakır.

    Çözüm İKİ GEÇİŞLİDİR: birinci geçiş bölüm başlangıç sayfalarını
    ÖLÇER, ikinci geçiş onları metne yazar. Sayfa numarası tahmin
    edilmez."""
    if not page_of:
        return blocks
    pat = re.compile(r"\bChapter (\d{1,2})\b(?! \(page)")
    # ⚠ İÇERİK TURU: "Chapter N" atıfları sayfa alıyordu, "Appendix X"
    # ALMIYORDU. Okur metninde on bir yerde bir eke ADIYLA gönderiliyor
    # ve 265 sayfanın içinde onu kendisi arıyordu — Faz 5'in "bkz.
    # Bölüm 8" kusurunun ek katmanındaki aynısı. Ek sayfaları zaten
    # ÖLÇÜLÜYOR (apx_page); artık YAZILIYOR da.
    apat = re.compile(r"\bAppendix ([A-J])\b(?! \(page)(?! —)")
    # Bütün-giysi bölümü NUMARASIZDIR (iki bölüm 16 olamaz), bu yüzden
    # "Chapter N" deseniyle çözülemez. Adıyla anılır ve sayfası yine
    # ÖLÇÜLÜR — okur numarasız bir bölümü de bulabilmelidir.
    WG = "the whole-garment chapter"
    wg_page = page_of.get("ch16_atlas")

    def fix(v: str) -> str:
        def rep(m):
            n = int(m.group(1))
            key = CHAPTER_BY_NUMBER.get(n)
            pg = page_of.get(key)
            return f"Chapter {n} (page {pg})" if pg else m.group(0)
        v = pat.sub(rep, v)

        def arep(m):
            pg = (apx_of or {}).get(m.group(1))
            return f"Appendix {m.group(1)} (page {pg})" if pg else m.group(0)
        v = apat.sub(arep, v)
        if wg_page and WG in v and f"{WG} (page" not in v:
            v = v.replace(WG, f"{WG} (page {wg_page})")
        return v

    out = []
    for b in blocks:
        nb = dict(b)
        for f in READER_FIELDS:
            if isinstance(nb.get(f), str):
                nb[f] = fix(nb[f])
        if nb.get("items"):
            nb["items"] = [fix(str(x)) for x in nb["items"]]
        out.append(nb)
    return out


def build_indexes(atlas, sign_page: dict, page_of: dict, sources: list) -> list:
    """Ek C ve Ek H'nin GERÇEK dizinleri.

    İkinci çelişmeli inceleme:
      · Ek C "nerede bulacağınız" diye başlık atıp KONUM VERMİYORDU.
      · Ek H aile dizinini duyurup HİÇBİR ŞEY basmıyordu — kitabın son
        sayfasının üçte ikisi boştu.
      · 43 akış şemasının hepsi kitapta OLMAYAN bir 'zone chart'a
        çıkıyordu.

    Üçü de aynı eksiklikti: kitap çıkışlarını adlandırıyor ama nereye
    çıktığını söylemiyordu. Bu dizinler sayfa numaralarıyla üretilir ve
    ancak İKİNCİ geçişte doğrudur."""
    if not sign_page:
        return {}
    zones = atlas.labels["zones"]
    # ⚠ Faz 5'te ÖLÇÜLEN kusur: üretilen üç ek (C, H, I) yazılmış eklerin
    # SONUNA ekleniyordu, dolayısıyla kitapta basılan sıra
    # A, B, D, E, F, G, C, H, I idi. Ek C kitabın ASIL GİRİŞİDİR — 43
    # akış şemasının hepsi "go back to the sign index in Appendix C"
    # diyor — ve dokuz ekin yedincisinde basılıyordu; sırayla çeviren
    # okur C'yi B ile D arasında arar ve bulamaz. Üretilen bloklar artık
    # appendix.json'daki `index_slot` işaretlerine YERLEŞTİRİLİR.
    # Regresyon: 07_TESTS/selftest.py § test_appendices_print_in_letter_order
    blocks: list = [{"type": "h2", "text": "Appendix C — Where each sign is"},
                    {"type": "para",
                     "text": "Every sign in the book, by region, with the page its "
                             "entry begins on. This is the way in: find what you see, "
                             "then go to the page."}]
    by_zone: dict = {}
    for sid, sg in atlas.signs.items():
        by_zone.setdefault(sg["zone"], []).append(sid)
    for z in sorted(by_zone, key=lambda x: zones.get(x, x)):
        rows = [["What you see", "Page"]]
        for sid in by_zone[z]:
            pg = sign_page.get(sid)
            if pg:
                rows.append([atlas.content[sid]["title"], str(pg)])
        if len(rows) > 1:
            blocks.append({"type": "h3", "text": zones.get(z, z)})
            blocks.append({"type": "table", "rows": rows, "widths": [0.86, 0.14]})

    groups = {"C": blocks}
    blocks = [{"type": "h2", "text": "Appendix H — Where each region leads"}]
    blocks.append({"type": "para",
                   "text": "The twenty adjustment families this book can reach, and "
                           "the signs that lead to each. What a family does to a "
                           "pattern belongs to the second book."})
    fam_signs: dict = {}
    for sid, sg in atlas.signs.items():
        for c in sg["candidate_causes"]:
            fam = c.get("adjustment_family_ref")
            if fam:
                fam_signs.setdefault(fam, set()).add(sid)
    rows = [["Adjustment family", "Reached from pages"]]
    for fid, fam in sorted(atlas.families.items()):
        pgs = sorted({sign_page[s] for s in fam_signs.get(fid, ()) if s in sign_page})
        rows.append([fam["name"],
                     ", ".join(str(x) for x in pgs) if pgs else "—"])
    blocks.append({"type": "table", "rows": rows, "widths": [0.56, 0.44]})

    # ── Ek I: KAYNAKLAR ───────────────────────────────────────────────
    # İkinci çelişmeli inceleme (A-21): kitabın hiçbir kaynak listesi
    # YOKTU, ama metin defalarca adsız otoritelere başvuruyordu —
    # "yaygın olarak anılan eşik", "çoğu kaynak", "yerleşik uygulama".
    # Bir okur bunların hiçbirini kontrol edemezdi.
    #
    # Liste kaynak KAYITLARINDAN üretilir; elle yazılsaydı sicille ilk
    # değişiklikte ayrışırdı. Yalnızca TEKNİK OTORİTELER girer: platform
    # ve yazı tipi kayıtları kitabın teknik iddialarını desteklemez.
    blocks.append({"type": "h2", "text": "Appendix I — Where the technical claims "
                                         "come from"})
    blocks.append({"type": "para",
                   "text": "The measurement definitions, the ease and size-selection "
                           "rules, the order-of-work rules and the fold-and-pull "
                           "distinction are drawn from the publications below. Where "
                           "they disagree with each other, the book says so at the "
                           "point of disagreement rather than choosing silently."})
    srows = [["Publication", "Publisher", "Used for"]]
    for rec in sources:
        if not rec.get("technical_authority"):
            continue
        # ⚠ `used_for` PROJE dilindedir ve iç kimlik taşır; okura dönük
        # bir tabloya basılamaz (K46). Kaynak kaydının `reader_purpose`
        # alanı bunun için vardır ve yoksa kaynak listeye GİRMEZ —
        # eksik bir alan, sızdırılmış bir kimlikten iyidir.
        purpose = rec.get("reader_purpose")
        if not purpose:
            continue
        srows.append([rec.get("title", "?"),
                      str(rec.get("publisher") or "—"), purpose])
    blocks.append({"type": "table", "rows": srows, "widths": [0.34, 0.30, 0.36]})
    blocks.append({"type": "para",
                   "text": "Two standards that govern body-measurement definitions — "
                           "the international clothing size-designation standard and "
                           "the standard terminology for body dimensions — are cited "
                           "in this book's own records but were not obtained. Where a "
                           "definition rests on them, the book says that the sources "
                           "differ rather than asserting one."})
    groups["HI"] = blocks

    # ⚠ BAĞIMSIZ İNCELEME · M-8/M-9/M-10: Ek G iki sayı İLAN EDİYORDU
    # ("İKİ gerçek anlaşmazlık", "ALTI ayrılma") ve ikisi de metinle
    # uyuşmuyordu. Sayılar prozaya ELLE yazılmıştı; veri değişince
    # cümle değişmedi. Üç ayrı kusur doğurdu: bir AYRILMA kaynak
    # anlaşmazlığı diye sayıldı, bir "anlaşmazlık" tek kaynak ile bu
    # kitabı karşı karşıya koyuyordu, ve prozada duran YEDİNCİ ayrılma
    # hiç sayılmamıştı.
    # Kitabın kanıt duruşunu ilan eden cümle artık KAYITTAN üretilir:
    # sayılamayan bir şey ilan edilemez.
    mc = atlas.mcontent
    names = {mid: m["name"].lower() for mid, m in atlas.measures.items()}
    conf = sorted(mc.get("conflicts", {}))
    divg = sorted(mc.get("divergences", {}))

    def _join(ids):
        got = [names.get(i, i) for i in ids]
        return got[0] if len(got) == 1 else ", ".join(got[:-1]) + " and " + got[-1]

    _n = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX",
          7: "SEVEN", 8: "EIGHT", 9: "NINE", 10: "TEN"}
    txt = (f"It records {_n.get(len(conf), len(conf))} real "
           f"{'disagreement' if len(conf) == 1 else 'disagreements'} between "
           f"published sources — over the {_join(conf)} — and there it tells you to choose "
           f"one and record which. Separately, it records "
           f"{_n.get(len(divg), len(divg))} "
           f"{'place' if len(divg) == 1 else 'places'} where this book departs from "
           f"the one source it has: {_join(divg)}. Those are not disagreements "
           f"between authorities. They are decisions this book made, and the page "
           f"where each measurement is taught says so.")
    groups["G_counts"] = [{"type": "para", "text": txt}]
    return groups


def check_pages_render(pdf: Path):
    """Her sayfayı rasterleştirir; METNİ olup MÜREKKEBİ olmayan sayfayı arar.

    Dönüş: bozuk sayfa listesi, ya da araç yoksa None."""
    import shutil
    import subprocess
    import tempfile
    if not shutil.which("pdftoppm") or not shutil.which("pdftotext"):
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    pages = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                           capture_output=True, text=True).stdout.split("\f")[:-1]
    bad = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-png", "-r", "40", str(pdf), f"{td}/p"],
                       capture_output=True)
        for f in sorted(Path(td).glob("p-*.png")):
            n = int(re.search(r"p-(\d+)", f.name).group(1))
            if n > len(pages):
                continue
            has_text = bool(re.sub(r"\s+", "", pages[n - 1]))
            if has_text and Image.open(f).convert("L").getextrema()[0] == 255:
                bad.append(n)
    return bad


def build_front_matter(cfg: dict, book: dict) -> list:
    return [
        {"type": "h1", "text": book["title"], "kicker": book.get("series")},
        {"type": "lead", "text": book["subtitle"]},
        {"type": "para", "text": book["front_note"]},
        {"type": "pagebreak"},
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book-01")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-charts", action="store_true",
                    help="belirti akış şemalarını ATLA — sayfa bütçesi ölçümü için")
    ap.add_argument("--only", default=None, help="virgülle ayrılmış bölüm anahtarları")
    ap.add_argument("--index", default=None, help="ölçüm dosyası yolu")
    ap.add_argument("--no-ink-check", action="store_true",
                    help="görünmez sayfa denetimini atla (hızlı koşum)")
    args = ap.parse_args()

    bdir = paths.BOOK_DIRS[args.book]
    mdir = bdir / MANUSCRIPT_DIR
    if not mdir.exists():
        print(f"✗ manüskript dizini yok: {mdir.relative_to(paths.ROOT)}")
        return 2

    figs = load(paths.book_figures(args.book))
    # İÇ ARAÇ figürleri (tbl_af_index gibi) üretim/denetim içindir ve
    # KİTABA GİRMEZ. Sicilde `internal` bayrağıyla durur; burada meta
    # tablosuna hiç ALINMAZ, böylece bir bölüm onları çağırırsa
    # "figür sicilde yok" hatası verir ve sessizce basılmaz.
    meta_by_key = {m["source_file"].rsplit(".", 1)[0]: m
                   for m in figs["figure_meta"].values()
                   if m.get("source_file") and not m.get("internal")}
    internal_keys = {m["source_file"].rsplit(".", 1)[0]
                     for m in figs["figure_meta"].values()
                     if m.get("source_file") and m.get("internal")}
    geom = load(paths.PAGE_GEOMETRY)
    cfg = load(paths.SERIES_CONFIG)
    bookcfg = load(bdir / "book_config.json")

    out = Path(args.out) if args.out else bdir / "09_OUTPUT" / "BOOK_01.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    sources = [load(f) for f in sorted(paths.SOURCE_RECORDS.glob("S-*.json"))]
    eng = Engine(args.book)
    atlas = AtlasBuilder(args.book, mdir)
    only = set(args.only.split(",")) if args.only else None

    # ── Bölüm bloklarını BİR KEZ topla ────────────────────────────────
    collected: list = []          # (part, key, blocks)
    missing: list = []
    for pnum, ptitle, keys in PARTS:
        for key in keys:
            if only and key not in only:
                continue
            if key == "ch02":
                blocks, sids = atlas.measurement_chapter(), []
            elif key in GENERATED:
                blocks, sids = atlas.chapter(GENERATED[key],
                                             with_charts=not args.no_charts)
            else:
                f = mdir / f"{key}.json"
                if not f.exists():
                    missing.append(key)
                    continue
                doc = load(f)
                blocks, sids = doc["blocks"], doc.get("signs_covered", [])
            collected.append((pnum, ptitle, key, blocks, sids))

    # ── İKİ GEÇİŞ ─────────────────────────────────────────────────────
    # Birinci geçiş sayfa numaralarını ÖLÇER; ikincisi onları yazar.
    # Bir içindekiler tablosu tahminle yazılamaz ve kitap bir sayfa
    # kaydığında sessizce yalan söyleyemez.
    def run_pass(page_of: dict, toc: list, index_blocks: list | None = None,
                 apx_of: dict | None = None):
        ts = Typesetter(out, geom, eng)
        ts.set_running_head(bookcfg.get("titleWorking", ""), None)
        errs: list = []
        chapters: list = []
        claims_seen: dict = {}
        started_parts: set = set()
        sign_page: dict = {}
        apx_page: list = []
        part_page: dict = {}

        if toc:
            ts.h1("Contents")
            ts.para("Part Four is a reference. You will not read it end to end; "
                    "you go to the region where you see something.",
                    face="serif-italic", size=10.5)
            for title, level, pg in toc:
                ts.toc_line(title, pg, level=level)
            ts.start_recto()

        for pnum, ptitle, key, blocks, sids in collected:
            if key == "appendix":
                blocks = fill_index_slots(blocks, index_blocks)
            blocks = resolve_cross_references(blocks, page_of, apx_of)
            errs.extend(check_reader_language(blocks, key))
            for b in blocks:
                if b.get("type") == "figure" and b.get("key") in internal_keys:
                    errs.append(f"{key}: İÇ ARAÇ figürü kitaba konulamaz — "
                                f"{b['key']} (figures.json internal=true)")
            if pnum > 0 and pnum not in started_parts:
                ts.start_recto()
                ts.outline(f"Part {pnum} — {ptitle}", level=0)
                # ⚠ Faz 5'te ÖLÇÜLEN kusur: içindekilerdeki parça satırı
                # `c["page_start"]`i, yani parçanın İLK BÖLÜMÜNÜN sayfasını
                # gösteriyordu. Altı parçanın altısında da bu, parçanın
                # KENDİ ayraç sayfasını iki sayfa ATLIYORDU: "Part 4 —
                # The regional atlas … 89" diyen okur 89'a gidiyor ve
                # 87'deki Parça 4 ayracını görmeden Bölüm 9'a düşüyordu.
                # Ayracın sayfası da ÖLÇÜLÜR.
                part_page.setdefault(pnum, ts.page)
                ts.h1(f"Part {pnum}", kicker=None)
                ts.para(ptitle, face="serif-italic", size=13.0)
                ts.page_break()
                started_parts.add(pnum)
            # ⚠ Baştaki `recto` bloğu SAYFA AÇAR. p0 ondan ÖNCE alınırsa
            # bölümün başlangıcı olarak BİR ÖNCEKİ bölümün son sayfası
            # kaydedilir — içindekiler ve PDF ana hattı yanlış sayfayı
            # gösterir. İçindekiler yakınsadı ama YANLIŞ bir değere
            # yakınsadı; yakınsama doğruluk demek değildir.
            lead_in = []
            rest = list(blocks)
            while rest and rest[0].get("type") in ("recto", "pagebreak"):
                lead_in.append(rest.pop(0))
            if lead_in:
                errs.extend(run_blocks(ts, lead_in, meta_by_key))
            p0 = ts.page
            f0 = len(ts.figures_used)
            _ct = CHAPTER_TITLES.get(key, key)
            # recto üst bilgisi bölümün adını taşır: bir başvuru
            # kitabında okurun nerede olduğunu bilmesi gerekir.
            ts.set_running_head(bookcfg.get("titleWorking", ""),
                                _ct.split(" · ")[-1] if pnum > 0 else None)
            ts.outline(_ct, level=1 if pnum > 0 else 0)
            # Belirti başlıklarının SAYFASI kaydedilir: Ek C ve Ek H
            # bunlara işaret eder. Bloklar parça parça dizilir ki her
            # başlığın hangi sayfaya düştüğü ÖLÇÜLSÜN, tahmin edilmesin.
            seg: list = []
            for bi, b in enumerate(rest):
                is_sign = (b.get("type") == "h2" and b.get("claims")
                           and str(b["claims"][0]).startswith("SYM-"))
                # ⚠ Faz 5: içindekiler "Part 6 — Appendices" satırında
                # BİTİYORDU. Dokuz ekin hiçbiri listelenmiyordu, yani
                # okurun ekleri adıyla bulmasının hiçbir yolu yoktu.
                # Ek başlıklarının sayfası da ÖLÇÜLÜR, tahmin edilmez.
                is_apx = (key == "appendix" and b.get("type") == "h2"
                          and str(b.get("text", "")).startswith("Appendix "))
                if is_sign or is_apx:
                    if seg:
                        errs.extend(run_blocks(ts, seg, meta_by_key)); seg = []
                    # ⚠ Faz 5'te ÖLÇÜLEN KUSUR: sayfa, başlık DİZİLMEDEN
                    # ÖNCE kaydediliyordu. Başlık sayfanın dibine
                    # denk gelip sonraki sayfaya kaydığında kaydedilen
                    # numara BİR ÖNCEKİ sayfa oluyordu. Ek C — kitabın
                    # ilan ettiği "way in", 43 akış şemasının hepsinin
                    # işaret ettiği dizin — 43 belirtinin 18'inde okuru
                    # BİR SAYFA ERKENE gönderiyordu; o sayfaların çoğu
                    # BAŞKA bir belirtinin karar tablosudur ve
                    # "Not this sign — go back to the sign index in
                    # Appendix C" ile biter: kapalı döngü.
                    # Yer AÇMA işi önce yapılır, sayfa SONRA okunur.
                    ts.reserve_group(rest, bi, meta_by_key)
                    if is_sign:
                        sign_page[b["claims"][0]] = ts.page
                    else:
                        apx_page.append((b["text"], ts.page))
                seg.append(b)
            if seg:
                errs.extend(run_blocks(ts, seg, meta_by_key))
            # Ana hat girişi bölümün İLK sayfasına bağlanır
            chapters.append({
                "key": key, "part": pnum, "generated": key in GENERATED,
                "page_start": p0, "page_end": ts.page, "pages": ts.page - p0 + 1,
                "figures": len(ts.figures_used) - f0,
                "signs_covered": sids, "blocks": len(blocks),
                "words": sum(len(str(b.get("text", "")).split()) for b in blocks)
                         + sum(len(str(x).split()) for b in blocks
                               for x in (b.get("items") or [])),
            })
            for b in blocks:
                for cid in (b.get("claims") or []):
                    claims_seen.setdefault(cid, key)
        return ts, errs, chapters, claims_seen, sign_page, apx_page, part_page

    def make_toc(chs: list, apx: list, parts: dict) -> list:
        t: list = []
        seen: set = set()
        for c in chs:
            if c["part"] > 0 and c["part"] not in seen:
                pt = next(x for n, x, _ in PARTS if n == c["part"])
                t.append((f"Part {c['part']} — {pt}", 0,
                          parts.get(c["part"], c["page_start"])))
                seen.add(c["part"])
            title = CHAPTER_TITLES.get(c["key"], c["key"])
            # Parça adı ile tek bölümünün adı aynıysa satırı İKİ KEZ
            # yazmak okura hiçbir şey söylemez.
            if not (t and t[-1][0].endswith(f"— {title}")):
                t.append((title, 1, c["page_start"]))
        for name, pg in apx:
            t.append((name, 1, pg))
        return t

    # ── YAKINSAMA ─────────────────────────────────────────────────────
    # İçindekiler kitabı UZATIR ve uzattığı için içindeki sayfa
    # numaralarını KAYDIRIR. İki geçiş yetmez; sayfa numaraları
    # DEĞİŞMEYENE kadar tekrarlanır. Yakınsamazsa hata verilir —
    # yanlış numara taşıyan bir içindekiler, içindekisi olmamaktan
    # kötüdür: okur ona güvenir.
    page_of: dict = {}
    toc: list = []
    index_blocks: dict = {}
    ts = errors = chapters = claims_seen = None
    apx_of: dict = {}
    for attempt in range(1, 7):
        ts, errors, chapters, claims_seen, sign_page, apx_page, part_page = run_pass(
            page_of, toc, index_blocks, apx_of)
        # ⚠ Ek C'nin ÖLÇÜLEN sayfası figür motoruna YAKINSAMA
        # DENETİMİNDEN ÖNCE verilir: 43 akış şemasının çıkış kutusu
        # kitabın tek giriş yoluna işaret ediyor ve locator taşımıyordu
        # (İnceleme C). Denetimden sonra verilseydi döngü o değeri
        # kullanmadan kapanabilirdi.
        _apx_c = next((pg for nm, pg in apx_page
                       if nm.startswith("Appendix C")), None)
        if _apx_c and eng.ui.get("_apx_c_page") != _apx_c:
            eng.ui["_apx_c_page"] = _apx_c
            page_of = {}          # etiket değişti → bir tur daha ölç
        new_page_of = {c["key"]: c["page_start"] for c in chapters}
        new_apx_of = {nm.split("Appendix ", 1)[1][0]: pg
                      for nm, pg in apx_page if nm.startswith("Appendix ")}
        new_toc = make_toc(chapters, apx_page, part_page)
        if new_page_of == page_of and new_toc == toc and new_apx_of == apx_of:
            break
        page_of, toc, apx_of = new_page_of, new_toc, new_apx_of
        index_blocks = build_indexes(atlas, sign_page, page_of, sources)
        ts.c = None   # bu geçişin tuvali atılır
    else:
        print("✗ İÇİNDEKİLER YAKINSAMADI — sayfa numaraları her geçişte "
              "değişiyor. Yanlış numaralı bir içindekiler basılmaz.")
        return 1

    if errors:
        print(f"✗ {len(errors)} DİZGİ/OKUR DİLİ HATASI:")
        for e in errors[:30]:
            print(f"    - {e}")
        return 1

    # ⚠ FAZ 6'DA ÖLÇÜLEN KUSUR: `pdfinfo` şunu gösteriyordu —
    #   Title: untitled · Author: anonymous · Creator: anonymous
    # Görev talimatı § 43: nihai yayın varlığında YER TUTUCU METİN
    # KALAMAZ. Künye, KAYITTAN yazılır; elle girilmez.
    _series = cfg["series"]["workingName"]
    _title = f"{_series} — Book 1: {bookcfg['book']['workingTitle'].split('—')[-1].strip()}"
    ts.c.setTitle(_title)
    ts.c.setSubject(bookcfg["book"]["workingSubtitle"])
    ts.c.setAuthor(cfg["series"].get("imprintName", "Vâliçe Press"))
    ts.c.setCreator("06_BUILD/build_book.py — figure_engine + typeset (bu depo)")
    ts.c.setKeywords(["sewing", "pattern fitting", "pattern alteration",
                      "diagnosis", "toile", "muslin", "home sewing"])
    ts.save()
    total = ts.page

    band = next((b["pageTargetProvisional"] for b in cfg["books"]
                 if b["id"] == args.book), None)

    index = {
        "$comment": [
            "ÜRETİLMİŞ ÖLÇÜM DOSYASI — proza TAŞIMAZ (.gitignore § ①).",
            "Kaynak: 06_BUILD/build_book.py. Her sayı dizgi çıktısından okunur.",
        ],
        "generated_by": "06_BUILD/build_book.py",
        "book": args.book,
        "charts_included": not args.no_charts,
        "pages_total": total,
        "page_target": band,
        "figures_used": len(ts.figures_used),
        "figures_distinct": len(set(ts.figures_used)),
        "chapters_expected": sum(len(k) for _, _, k in PARTS),
        "chapters_built": len(chapters),
        "chapters_missing": missing,
        "signs_covered": sorted({s for c in chapters for s in c["signs_covered"]}),
        "claims_referenced": sorted(claims_seen),
        "chapters": chapters,
    }
    idx_path = Path(args.index) if args.index else \
        bdir / "02_CONTENT" / "public" / "manuscript_index.public.json"
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    # ── GÖRÜNMEZ SAYFA DENETİMİ ───────────────────────────────────────
    # İkinci çelişmeli inceleme, iki sayfanın metin taşıyıp hiç mürekkep
    # basmadığını bildirdi. Denetlendi ve o hâliyle DOĞRU DEĞİLDİ — boş
    # sayfaların hepsi bölüm açılışı versosu ve metinleri de yok.
    #
    # Ama denetimin KENDİSİ değerlidir: metni olup basılmayan bir sayfa,
    # okurun asla göremeyeceği bir kusurdur ve hiçbir veri kapısı onu
    # göremez. İddia yanlış çıktı, kapı kaldı.
    if not args.no_ink_check:
        bad = check_pages_render(out)
        if bad is None:
            print("  ⚠ mürekkep denetimi ATLANDI (pdftoppm veya Pillow yok)")
        elif bad:
            print(f"  ✗ GÖRÜNMEZ SAYFA: {bad} — metin taşıyor ama hiç mürekkep "
                  f"basmıyor.")
            return 1
        else:
            print("  ✓ metni olup basılmayan sayfa yok")

    print(f"▸ build_book.py — {out.relative_to(paths.ROOT)}")
    print(f"  {total} sayfa · {len(ts.figures_used)} figür yerleşimi "
          f"({len(set(ts.figures_used))} ayrı figür) · {len(chapters)} bölüm")
    atlas_pages = sum(c["pages"] for c in chapters if c["generated"])
    print(f"  bölge atlası: {atlas_pages} sayfa")
    if missing:
        print(f"  ⚠ YAZILMAMIŞ bölüm: {', '.join(missing)}")
    if band:
        lo, hi = band
        if missing:
            print(f"  · sayfa bütçesi {lo}–{hi} — eksik bölümler yüzünden DEĞERLENDİRİLMEDİ")
        elif not (lo <= total <= hi):
            print(f"  ✗ SAYFA BÜTÇESİ DIŞI: {total}, hedef {lo}–{hi} "
                  f"(çelişmeli inceleme B-08 · cilt payı 300 sayfada değişir)")
            return 1
        else:
            print(f"  ✓ sayfa bütçesi içinde ({lo}–{hi})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
