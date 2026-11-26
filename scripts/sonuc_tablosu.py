"""reports/sonuc.xml (JUnit) + docs/tablolar (T1, T6) -> rapor tabloları.

Kullanım:  uv run python scripts/sonuc_tablosu.py   (önce: uv run pytest)

reports/tablolar.xlsx sayfaları:
  T1  Gereksinimler           gereksinim başına bir satır (ID, gereksinim, örnek girdi, beklenen, kaynak, sınayan testler)
  T2  Eşdeğerlik Sınıfları    sınıf başına bir satır + temsilci değer           (test kodundan türetilir)
  T3  Sınır Değerler          sınır başına bir satır: SD−1 / SD / SD+1          (test kodundan türetilir)
  DT  Karar Tablosu           kural başına bir satır (ipv4, domain; fonksiyon sütunuyla)
  T4a Test Senaryoları        tasarım aşaması: Gerçekleşen ve Durum BOŞ
  T4b Test Sonuçları          pytest sonrası: Gerçekleşen ve Durum dolu
  T5  Sonuç Özeti             fonksiyon başına sayılar + TOPLAM
  T6  Bulgular                başarısız testlerin analizi

Ayrıca: T4_test_senaryolari.csv ve T5_sonuc_ozeti.csv (UTF-8 BOM + ';', Türkçe Excel uyumlu).
T1'deki "Sınayan testler" sütunu gerçek Test ID'lerle karşılaştırılır; olmayan ID'ler
ve hiçbir gereksinime bağlanmamış testler uyarı olarak yazdırılır.
"""

import ast
import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

KOK = Path(__file__).resolve().parent.parent
RAPOR = KOK / "reports"
TABLOLAR = KOK / "docs" / "tablolar"
XML = RAPOR / "sonuc.xml"

ANAHTAR = ["test_id", "fonksiyon", "girdi", "parametreler", "teknik", "sinif", "beklenen", "gerceklesen"]
HASHLER = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


# ============================================================ okuma / yazma
def csv_oku(yol):
    with yol.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f, delimiter=";"))


def alan_tablolari_oku(onek):
    """docs/tablolar/<onek>_<alan>.csv dosyalarını (her ekip üyesi bir dosya) tek tabloda birleştirir.

    Başlık ilk dosyadan alınır; tüm dosyaların başlığı aynı olmalıdır.
    """
    dosyalar = sorted(TABLOLAR.glob(f"{onek}_*.csv"))
    if not dosyalar:
        sys.exit(f"HATA: {TABLOLAR.relative_to(KOK)} içinde {onek}_<alan>.csv bulunamadı.")
    baslik, satirlar = None, []
    for yol in dosyalar:
        tablo = csv_oku(yol)
        if baslik is None:
            baslik = tablo[0]
        elif tablo[0] != baslik:
            sys.exit(f"HATA: {yol.name} başlığı {dosyalar[0].name} ile aynı değil.")
        satirlar += [s for s in tablo[1:] if any(h.strip() for h in s)]
    return [baslik] + satirlar


def csv_yaz(yol, satirlar):
    with yol.open("w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f, delimiter=";").writerows(satirlar)


def durum_bul(testcase):
    if (s := testcase.find("skipped")) is not None:
        return ("XFAIL" if s.get("type") == "pytest.xfail" else "SKIP"), s.get("message", "")
    for etiket in ("failure", "error"):
        if (h := testcase.find(etiket)) is not None:
            return "FAIL", (h.get("message") or "").splitlines()[0][:200]
    return "PASS", ""


def senaryolari_oku():
    sonuc = []
    for tcase in ET.parse(XML).getroot().iter("testcase"):
        oz = {p.get("name"): p.get("value") for p in tcase.iter("property")}
        kayit = {k: oz.get(k, "") for k in ANAHTAR}
        kayit["durum"], kayit["not"] = durum_bul(tcase)
        sonuc.append(kayit)
    return sonuc


# ============================================================ yardımcılar
def kisa(girdi_repr, sinir=30):
    """Uzun girdileri tabloda okunur kısaltır: 'aaaaaaaaaaaa…' (128 karakter)."""
    try:
        deger = ast.literal_eval(girdi_repr)
    except (ValueError, SyntaxError):
        return girdi_repr
    if isinstance(deger, str) and len(deger) > sinir:
        return f"'{deger[:12]}…' ({len(deger)} karakter)"
    return girdi_repr


def onek_listesi(req_id):
    """REQ-IPV4-03 -> ['IPV4'];  REQ-HASH-01 -> ['MD5', 'SHA1', ...]."""
    onek = req_id.split("-")[1]
    return [h.upper() for h in HASHLER] if onek == "HASH" else [onek]


def testleri_ac(req_id, metin):
    """'EP-01, BVA-01..03' -> tam Test ID kümesi."""
    sonuc = set()
    for parca in filter(None, (p.strip() for p in metin.split(","))):
        if m := re.fullmatch(r"(EP|BVA|DT)-(\d+)\.\.(\d+)", parca):
            kisalar = [f"{m[1]}-{n:02d}" for n in range(int(m[2]), int(m[3]) + 1)]
        else:
            kisalar = [parca]
        for onek in onek_listesi(req_id):
            sonuc.update(f"TC-{onek}-{k}" for k in kisalar)
    return sonuc


def izlenebilirlik(t1, senaryolar):
    """Test ID -> [REQ ID'leri]; tutarsızlıkları yazdırır."""
    var_olan = {s["test_id"] for s in senaryolar}
    test_req = defaultdict(list)
    uyari = []
    for satir in t1[1:]:
        req_id, testler = satir[0], satir[-1]
        for tid in sorted(testleri_ac(req_id, testler)):
            if tid in var_olan:
                test_req[tid].append(req_id)
            else:
                uyari.append(f"  {req_id}: {tid} diye bir test yok")
    bagsiz = sorted(var_olan - test_req.keys())
    uyari += [f"  {tid}: hiçbir gereksinime bağlı değil" for tid in bagsiz]
    return test_req, uyari


# ============================================================ tablolar
def t2_siniflar(senaryolar):
    """Her EP sınıfı bir satır. Hash'lerde aynı sınıf 6 fonksiyonda tek satıra indirgenir."""
    satirlar, hash_grubu = [], {}
    for s in senaryolar:
        if s["teknik"] != "EP":
            continue
        if m := re.match(r"^([VI]\d+[a-z]?)\s+(.*)$", s["sinif"]):
            kod, aciklama = m[1], m[2]
        else:
            kod, aciklama = "DOK", s["sinif"]
        if s["fonksiyon"] in HASHLER:
            grup = aciklama if kod == "DOK" else kod   # I2'nin açıklaması fonksiyona göre değişir
            if grup in hash_grubu:
                continue
            hash_grubu[grup] = True
            no = s["test_id"].rsplit("-", 1)[1]
            satirlar.append(["6 hash (N)", kod, aciklama, f"{kisa(s['girdi'])}  ← {s['fonksiyon']} için",
                             s["parametreler"], s["beklenen"], f"TC-<HASH>-EP-{no}"])
        else:
            satirlar.append([s["fonksiyon"], kod, aciklama, kisa(s["girdi"], 44), s["parametreler"],
                             s["beklenen"], s["test_id"]])
    return satirlar


SINIR_RE = re.compile(r"^(?P<ad>.+?)\s+(?P<k>SD-1|SD\+1|SD|N-1|N\+1|N)(?=[\s(]|$)(?P<ek>.*)$")
KONUM = {"SD-1": 0, "N-1": 0, "SD": 1, "N": 1, "SD+1": 2, "N+1": 2}


def t3_sinirlar(senaryolar):
    """Her sınır bir satır: SD−1 / SD / SD+1 değerleri ve beklenenler."""
    sinirlar, uyari = {}, []
    for s in senaryolar:
        if s["teknik"] != "BVA":
            continue
        m = SINIR_RE.match(s["sinif"])
        if not m:
            uyari.append(f"  {s['test_id']}: sınır adı ayrıştırılamadı ({s['sinif']!r})")
            continue
        anahtar = (s["fonksiyon"], m["ad"].strip())
        kayit = sinirlar.setdefault(anahtar, {"deger": ["—"] * 3, "bek": ["—"] * 3, "id": []})
        i = KONUM[m["k"]]
        deger = kisa(s["girdi"])
        if "karakter)" in deger and m["ek"].strip():   # kısaltılmışsa sınırın kendi değerini göster
            deger += f"  → sınır değeri {m['ek'].strip()}"
        if s["parametreler"] != "—":
            deger += f"  [{s['parametreler']}]"
        kayit["deger"][i] = deger
        kayit["bek"][i] = "V" if s["beklenen"] == "True" else "I"
        kayit["id"].append(s["test_id"])
    satirlar = [[fonk, ad, *k["deger"], " / ".join(k["bek"]), ", ".join(sorted(k["id"]))]
                for (fonk, ad), k in sinirlar.items()]
    return satirlar, uyari


def t5_ozet(senaryolar):
    ozet = defaultdict(lambda: defaultdict(int))
    for s in senaryolar:
        o = ozet[s["fonksiyon"]]
        o["Toplam"] += 1
        o[s["teknik"]] += 1
        o[s["durum"]] += 1
    return [[ad, o["Toplam"], o["EP"], o["BVA"], o["DT"], o["PASS"], o["FAIL"], o["XFAIL"],
             round(100 * o["PASS"] / o["Toplam"], 1)] for ad, o in ozet.items()]


# ============================================================ Excel biçimi
BASLIK_DOLGU = PatternFill("solid", fgColor="1F3864")
BASLIK_YAZI = Font(bold=True, color="FFFFFF")
INCE = Side(style="thin", color="BFBFBF")
KENAR = Border(left=INCE, right=INCE, top=INCE, bottom=INCE)
RENK = {"PASS": "C6EFCE", "XFAIL": "FFEB9C", "FAIL": "FFC7CE", "SKIP": "D9D9D9",
        "True": "E2EFDA", "ValidationError": "FCE4D6"}
RENKLI_SUTUN = {"Durum", "Beklenen", "Beklenen çıktı", "Gerçekleşen"}


def sayfa_ekle(wb, ad, baslik, satirlar, genislik, toplam=None, not_=None):
    ws = wb.create_sheet(ad)
    ilk = 1
    if not_:
        ws.append([not_])
        ws["A1"].font = Font(italic=True, color="595959")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(baslik))
        ilk = 2
    ws.append(baslik)
    for s in satirlar:
        ws.append(s)
    if toplam:
        ws.append(toplam)
        for h in ws[ws.max_row]:
            h.font = Font(bold=True)
            h.fill = PatternFill("solid", fgColor="D9E1F2")

    for h in ws[ilk]:
        h.fill, h.font = BASLIK_DOLGU, BASLIK_YAZI
        h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, g in enumerate(genislik, start=1):
        ws.column_dimensions[get_column_letter(i)].width = g

    renkli = [i for i, b in enumerate(baslik) if b in RENKLI_SUTUN]
    for satir in ws.iter_rows(min_row=ilk + 1):
        for h in satir:
            h.border = KENAR
            h.alignment = Alignment(vertical="top", wrap_text=True)
        for i in renkli:
            if r := RENK.get(satir[i].value):
                satir[i].fill = PatternFill("solid", fgColor=r)

    ws.freeze_panes = ws.cell(row=ilk + 1, column=2)
    ws.auto_filter.ref = f"A{ilk}:{get_column_letter(len(baslik))}{ilk + len(satirlar)}"


# ============================================================ ana akış
def main():
    t1 = alan_tablolari_oku("T1")
    t6 = alan_tablolari_oku("T6")

    # Fonksiyonları T1'deki sıraya diz (ipv4, ipv6, cron, ..., hash'ler)
    sira = []
    for satir in t1[1:]:
        for f in (HASHLER if satir[0].startswith("REQ-HASH") else [satir[1]]):
            if f not in sira:
                sira.append(f)
    senaryolar = senaryolari_oku()
    senaryolar.sort(key=lambda s: sira.index(s["fonksiyon"]) if s["fonksiyon"] in sira else 99)

    test_req, uyari = izlenebilirlik(t1, senaryolar)
    t3, uyari3 = t3_sinirlar(senaryolar)
    uyari += uyari3

    def t4_satiri(s, sonuc_dolu):
        return [s["test_id"], s["fonksiyon"], ", ".join(test_req.get(s["test_id"], [])), s["girdi"],
                s["parametreler"], s["teknik"], s["sinif"], s["beklenen"],
                s["gerceklesen"] if sonuc_dolu else "", s["durum"] if sonuc_dolu else ""]

    t4_baslik = ["Test ID", "Fonksiyon", "Gereksinim", "Girdi", "Parametreler", "Teknik",
                 "Sınıf / Sınır", "Beklenen", "Gerçekleşen", "Durum"]
    t4a = [t4_satiri(s, False) for s in senaryolar]
    t4b = [t4_satiri(s, True) + [s["not"]] for s in senaryolar]
    t5 = t5_ozet(senaryolar)
    t5_baslik = ["Fonksiyon", "Toplam", "EP", "BVA", "DT", "PASS", "FAIL", "XFAIL (bulgu)", "Başarı %"]

    # --- CSV
    csv_yaz(RAPOR / "T4_test_senaryolari.csv", [t4_baslik + ["Not"], *t4b])
    csv_yaz(RAPOR / "T5_sonuc_ozeti.csv", [t5_baslik, *t5])

    # --- Excel
    wb = Workbook()
    wb.remove(wb.active)
    sayfa_ekle(wb, "T1 Gereksinimler", t1[0], t1[1:], [13, 16, 50, 26, 15, 34, 40],
               not_="Her gereksinim bir satır. 'Sınayan testler' fonksiyon önekiyle kısaltılmıştır "
                    "(ör. REQ-IPV4 satırında EP-01 = TC-IPV4-EP-01; BVA-01..03 = 01'den 03'e).")
    sayfa_ekle(wb, "T2 Eşdeğerlik Sınıfları",
               ["Fonksiyon", "Sınıf", "Açıklama", "Temsilci değer", "Parametreler", "Beklenen", "Test ID"],
               t2_siniflar(senaryolar), [14, 7, 46, 44, 22, 16, 18],
               not_="V = geçerli sınıf, I = geçersiz sınıf, DOK = dokümandaki örnek. Her sınıftan bir temsilci. "
                    "6 hash fonksiyonu aynı sınıfları paylaşır; yalnızca uzunluk N değişir.")
    sayfa_ekle(wb, "T3 Sınır Değerler",
               ["Fonksiyon", "Sınır", "SD−1", "SD", "SD+1", "Beklenen (SD−1 / SD / SD+1)", "Test ID'ler"],
               t3, [14, 30, 30, 30, 30, 16, 44],
               not_="Her sınır bir satır. V = geçerli (True), I = geçersiz (ValidationError). "
                    "İki taraflı aralıklarda alt ve üst sınır ayrı satırdır. — : bu sınır için anlamlı değil.")
    # Genel biçim: her fonksiyonun DT'si farklı sayıda koşul (parametre) taşıyabilir.
    dt = [[s["test_id"], s["fonksiyon"], s["sinif"].split()[0], " ".join(s["sinif"].split()[1:]),
           s["parametreler"], s["girdi"], "V" if s["beklenen"] == "True" else "I"]
          for s in senaryolar if s["teknik"] == "DT"]
    sayfa_ekle(wb, "DT Karar Tablosu",
               ["Test ID", "Fonksiyon", "Kural", "Koşullar", "Parametreler", "Girdi", "Beklenen"], dt,
               [17, 11, 7, 40, 26, 18, 10],
               not_="Kural başına bir satır. ipv4: cidr × strict × (girdide CIDR var mı?); "
                    "domain: rfc_1034 × (sondaki nokta var mı?).")
    sayfa_ekle(wb, "T4a Test Senaryoları", t4_baslik, t4a, [18, 13, 14, 46, 22, 8, 40, 16, 14, 9],
               not_="Tasarım aşaması: Gerçekleşen ve Durum sütunları testler koşturulmadan önce boştur.")
    sayfa_ekle(wb, "T4b Test Sonuçları", t4_baslik + ["Not"], t4b, [18, 13, 14, 46, 22, 8, 40, 16, 16, 9, 60],
               not_="pytest sonrası: Gerçekleşen ve Durum sütunları JUnit XML'den otomatik dolduruldu.")
    top = [sum(r[i] for r in t5) for i in range(1, 8)]
    sayfa_ekle(wb, "T5 Sonuç Özeti", t5_baslik, t5, [14, 9, 7, 7, 7, 8, 8, 14, 10],
               toplam=["TOPLAM", *top, round(100 * top[4] / top[0], 1)])
    sayfa_ekle(wb, "T6 Bulgular", t6[0], t6[1:], [12, 26, 34, 16, 13, 70, 9])
    hedef = RAPOR / "tablolar.xlsx"
    try:
        wb.save(hedef)
    except PermissionError:   # dosya Excel'de açıksa Windows kilitler
        hedef = RAPOR / "tablolar_yeni.xlsx"
        wb.save(hedef)
        print("NOT: tablolar.xlsx Excel'de açık olduğu için kilitli; çıktı tablolar_yeni.xlsx'e yazıldı. "
              "Excel'i kapatıp betiği yeniden çalıştırın.")

    print(f"{len(senaryolar)} test | {len(t1) - 1} gereksinim | T2 {len(t2_siniflar(senaryolar))} sınıf | "
          f"T3 {len(t3)} sınır -> reports/{hedef.name}")
    if uyari:
        print("UYARI - izlenebilirlik / sınır tutarsızlıkları:\n" + "\n".join(uyari))
        sys.exit(1)
    print("İzlenebilirlik tam: her test en az bir gereksinime bağlı, tüm ID'ler mevcut.")


if __name__ == "__main__":
    main()
