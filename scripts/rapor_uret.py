"""Alan raporlarının otomatik bloklarını ve D1-D5 görsellerini pytest XML'den yeniler.

Kullanım:  uv run python scripts/rapor_uret.py <alan>      (ör. payments_finance)
           uv run python scripts/rapor_uret.py              (ALANLAR'daki tüm alanlar)
Önce:      uv run pytest  ve  uv run python scripts/sonuc_tablosu.py

docs/rapor_<alan>.md içindeki <!-- OTOMATIK:T1 --> ... <!-- /OTOMATIK:T1 --> (T1-T6, isteğe bağlı DT)
blokları yeniden yazılır; docs/tablolar/<alan>/T6_bulgular.csv'nin Girdi/Beklenen/Gerçekleşen
sütunları pytest sonucundan doldurulur (elle yazılmaz); docs/diyagramlar/<alan>/D1..D5 üretilir.
Yeni bir alan eklemek için ALANLAR sözlüğüne bir kayıt eklemek yeterlidir.
network_crypto raporu elle yazılmıştır; görselleri scripts/diyagramlar.py üretir.
"""

import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from sonuc_tablosu import izlenebilirlik, t3_sinirlar  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
TABLOLAR = KOK / "docs" / "tablolar"      # <alan>/T1_gereksinimler.csv, <alan>/T6_bulgular.csv
GORSEL = KOK / "docs" / "diyagramlar"     # <alan>/D1_...png … D5_...png
DIYAGRAM = {"D1": "D1_kara_kutu_modeli.png", "D2": "D2_test_sureci.png", "D3": "D3_esdegerlik_siniflari.png",
            "D4": "D4_sinir_degerleri.png", "D5": "D5_sonuc_grafigi.png"}

ALANLAR = {
    "domains_formats": dict(
        baslik="Alan adları ve biçimler",
        adlar=["domain", "hostname", "country_code", "currency", "iban", "between", "length",
               "calling_code", "slug", "base16", "base32", "base58", "base64", "ind_aadhar", "ind_pan"],
        teknikler=["EP", "BVA", "DT"],
        girdi="alan adı / kod / kodlama",
        d3=("D3 - IBAN eşdeğerlik sınıfları",
            ["Geçerli\nISO 13616 ülke kodu\nmod-97 = 1\nülkeye özgü uzunluk",
             "Girdi uzayı\nISO 13616",
             "Geçersiz\nyanlış kontrol basamağı\nkayıtsız ülke (XX)\nboşluk / küçük harf / uzunluk"]),
        d4=[([65534, 65535, 65536], ["V", "V", "I"], "hostname port üst sınırı"),
            ([62, 63, 64], ["V", "V", "I"], "domain etiket uzunluğu üst sınırı (RFC 1035)")],
    ),
    "payments_finance": dict(
        baslik="Ödeme ve finans",
        adlar=["email", "cusip", "isin", "sedol", "card_number", "visa", "mastercard",
               "amex", "discover", "diners", "jcb", "unionpay", "mir"],
        teknikler=["EP", "BVA"],
        girdi="adres / kod / kart no",
        d3=("D3 - email eşdeğerlik sınıfları",
            ["Geçerli\ndot-atom / tırnaklı yerel kısım\nLDH alan adı, IDN\nseçenekle IP-literal",
             "Girdi uzayı\nRFC 5321 / 5322",
             "Geçersiz\n'@' yok / çift, nokta kuralı\netiket tire, sayısal TLD\nuzunluk aşımı"]),
        d4=[([2719, 2720, 2721], ["V", "V", "I"], "Mastercard 2-serisi üst sınırı (önek)"),
            ([63, 64, 65], ["V", "V", "I"], "email yerel kısım uzunluğu (RFC 5321)")],
    ),
    "urls_national_ids": dict(
        baslik="URL ve ulusal kimlikler",
        adlar=["url", "es_nif", "es_nie", "es_cif", "es_doi", "fi_business_id",
               "fi_ssn", "fr_ssn", "ru_inn", "fr_department"],
        teknikler=["EP", "BVA"],
        girdi="URL / kimlik",
        d3=("D3 - INN eşdeğerlik sınıfları",
            ["Geçerli\n10 hane + kontrol\n12 hane + iki kontrol", "Girdi uzayı\nSentetik örnekler",
             "Geçersiz\nYanlış uzunluk\nHarf / bozuk kontrol"]),
        d4=[([899, 900, 901], ["V", "I", "I"], "Geçici HETU alt sınırı (allow_temporal_ssn=False)"),
            ([65534, 65535, 65536], ["V", "V", "I"], "URL hizmet portu üst sınırı")],
    ),
}


# ------------------------------------------------------------------ yardımcılar
def tablo(baslik, satirlar):
    def hucre(v):
        return str(v).replace("|", "\\|").replace("\n", " ")
    return "\n".join("| " + " | ".join(map(hucre, s)) + " |"
                     for s in [baslik, ["---"] * len(baslik), *satirlar])


def kisalt(metin, sinir=60):
    """Uzun girdi gösterimini kısaltır; parantezdeki uzunluk tırnaklar hariç asıl değerindir."""
    if len(metin) <= sinir:
        return metin
    uzunluk = len(metin) - 2 if metin[:1] in "'\"" and metin[-1:] == metin[:1] else len(metin)
    return f"{metin[:sinir]}… ({uzunluk} karakter)"


def csv_oku(alan, ad):
    with (TABLOLAR / alan / ad).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f, delimiter=";"))


def sonuclari_oku(alan, ayar):
    tumu, bizim = [], []
    for case in ET.parse(KOK / "reports" / "sonuc.xml").getroot().iter("testcase"):
        p = {v.get("name"): v.get("value") for v in case.iter("property")}
        if not p.get("test_id"):
            raise ValueError("XML içinde test kimliği olmayan kayıt var; önce tam pytest çalıştırın")
        atlandi = case.find("skipped")
        if atlandi is not None:
            p["durum"] = "XFAIL" if atlandi.get("type") == "pytest.xfail" else "SKIP"
        else:
            p["durum"] = "FAIL" if case.find("failure") is not None or case.find("error") is not None else "PASS"
        tumu.append(p)
        if f"tests.{alan}." in case.get("classname", ""):
            bizim.append(p)
    if {p["fonksiyon"] for p in bizim} != set(ayar["adlar"]):
        raise ValueError(f"{alan}: XML bu alanın tüm fonksiyonlarını içermiyor; tam pytest çalıştırın")
    # T1 kontrolü eksik/filtrelenmiş pytest çalıştırmalarının rapora girmesini önler.
    _, uyari = izlenebilirlik(csv_oku(alan, "T1_gereksinimler.csv"), bizim)
    if uyari:
        raise ValueError("\n".join(uyari))
    return tumu, bizim


# ------------------------------------------------------------------ diyagramlar
def kutular(dosya, baslik, metinler, ters_ilk_ok=False):
    fig, ax = plt.subplots(figsize=(12, 3.4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    xs = [0.15, 0.50, 0.85]
    for x, metin in zip(xs, metinler, strict=True):
        ax.text(x, 0.5, metin, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.8", facecolor="#e8eef8", edgecolor="#244775"))
    oklar = [(xs[0] + .13, xs[1] - .13), (xs[1] + .13, xs[2] - .13)]
    if ters_ilk_ok:  # D3: girdi uzayı ortada, oklar iki sınıfa doğru
        oklar[0] = (xs[1] - .13, xs[0] + .13)
    for bas, son in oklar:
        ax.annotate("", xy=(son, .5), xytext=(bas, .5),
                    arrowprops=dict(arrowstyle="->", color="#244775", lw=2))
    ax.set_title(baslik, fontsize=14, pad=18)
    fig.tight_layout()
    fig.savefig(dosya, dpi=160)
    plt.close(fig)


def test_sureci(dosya):
    """D2: başarısız testin düzeltilmesi / bulgu olarak korunması döngüsü."""
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    for x, y, metin in [
        (.14, .81, "Docstring + standart\nT1 gereksinimleri"),
        (.49, .81, "EP + BVA\nTest senaryoları"),
        (.85, .81, "pytest\nFonksiyonu çağır"),
        (.49, .45, "FAIL analizi\nTest mi, kütüphane mi?"),
        (.14, .45, "Test / gereksinim\nverisini düzelt"),
        (.49, .13, "Kütüphane uyuşmazlığı\nT6 + strict xfail"),
        (.85, .13, "XML / HTML\nTablolar + rapor"),
    ]:
        ax.text(x, y, metin, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=.7", facecolor="#e8eef8", edgecolor="#244775"))

    def ok(bas, son, metin="", xy=None, rad=0):
        ax.annotate("", xy=son, xytext=bas,
                    arrowprops=dict(arrowstyle="->", lw=1.8, color="#244775",
                                    connectionstyle=f"arc3,rad={rad}"))
        if metin:
            x, y = xy or ((bas[0] + son[0]) / 2, (bas[1] + son[1]) / 2)
            ax.text(x, y, metin, ha="center", va="center", fontsize=10,
                    bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ok((.26, .81), (.37, .81))
    ok((.62, .81), (.76, .81))
    ok((.85, .74), (.85, .20), "PASS / beklenen XFAIL", (.85, .48))
    ok((.81, .74), (.61, .50), "FAIL", (.73, .63))
    ok((.36, .45), (.25, .45), "Test yanlış", (.30, .50))
    ok((.14, .52), (.14, .74))
    ok((.49, .38), (.49, .20), "Beklenti doğru", (.49, .29))
    ok((.60, .13), (.91, .75), "Yeniden çalıştır", (.69, .36), rad=.43)
    ax.set_title("D2 - Test, analiz ve yeniden doğrulama döngüsü", fontsize=14, pad=12)
    fig.tight_layout()
    fig.savefig(dosya, dpi=160)
    plt.close(fig)


def sayi_dogrusu(dosya, satirlar):
    """D4: her sınır için SD-1 / SD / SD+1 noktaları (yeşil = geçerli, kırmızı = geçersiz)."""
    fig, axes = plt.subplots(len(satirlar), 1, figsize=(11, 2.4 * len(satirlar)))
    for ax, (degerler, etiketler, baslik) in zip(axes, satirlar, strict=True):
        ax.axhline(0, color="#244775")
        ax.scatter(degerler, [0] * 3, c=["#2e7d32" if e == "V" else "#c62828" for e in etiketler],
                   s=100, zorder=3)
        for d, e, konum in zip(degerler, etiketler, ["SD-1", "SD", "SD+1"], strict=True):
            ax.text(d, .15, f"{konum}: {d}\n{e}", ha="center")
        ax.set(xlim=(degerler[0] - .5, degerler[-1] + .5), ylim=(-.2, .6), yticks=[], xticks=[])
        ax.set_title(baslik, fontsize=11)
        for kenar in ax.spines.values():
            kenar.set_visible(False)
    fig.tight_layout()
    fig.savefig(dosya, dpi=160)
    plt.close(fig)


def sonuc_grafigi(dosya, bizim, adlar, teknikler):
    """D5: fonksiyon başına gerçek sonuçlar ve tasarım teknikleri."""
    sayac = defaultdict(Counter)
    for p in bizim:
        sayac[p["fonksiyon"]][p["durum"]] += 1
        sayac[p["fonksiyon"]][p["teknik"]] += 1
    renk = {"EP": "#1565c0", "BVA": "#6a1b9a", "DT": "#00838f"}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    for ax, sutunlar, baslik in [
        (axes[0], [("PASS", "#2e7d32"), ("XFAIL", "#f9a825"), ("FAIL", "#c62828")], "Gerçek sonuçlar (JUnit XML)"),
        (axes[1], [(t, renk[t]) for t in teknikler], "Test tasarım teknikleri"),
    ]:
        alt = [0] * len(adlar)
        for sutun, r in sutunlar:
            degerler = [sayac[fn][sutun] for fn in adlar]
            ax.bar(adlar, degerler, bottom=alt, label=sutun, color=r)
            alt = [a + b for a, b in zip(alt, degerler)]
        ax.set_title(baslik)
        ax.set_ylabel("Test sayısı")
        ax.tick_params(axis="x", labelrotation=55)
        for etiket in ax.get_xticklabels():
            etiket.set_ha("right")
        ax.legend()
    fig.tight_layout()
    fig.savefig(dosya, dpi=160)
    plt.close(fig)


def diyagramlar(alan, ayar, bizim):
    (GORSEL / alan).mkdir(parents=True, exist_ok=True)
    yol = lambda d: GORSEL / alan / DIYAGRAM[d]  # noqa: E731
    kutular(yol("D1"), f"D1 - {ayar['baslik']}: kara-kutu modeli",
            [f"Girdi\n{ayar['girdi']}\n+ seçenekler", "validators 0.36.0\nİç yapı incelenmez",
             "Çıktı\nTrue / ValidationError"])
    test_sureci(yol("D2"))
    kutular(yol("D3"), *ayar["d3"], ters_ilk_ok=True)
    sayi_dogrusu(yol("D4"), ayar["d4"])
    sonuc_grafigi(yol("D5"), bizim, ayar["adlar"], ayar["teknikler"])


# ------------------------------------------------------------------ rapor blokları
def t6_yenile(alan, bizim):
    """T6'nın Girdi/Beklenen/Gerçekleşen sütunlarını pytest sonucundan doldurur."""
    t6 = csv_oku(alan, "T6_bulgular.csv")
    kimlik = {p["test_id"]: p for p in bizim}
    for satir in t6[1:]:
        props = [kimlik[i.strip()] for i in satir[1].split(",") if i.strip() in kimlik]
        if not props:  # test bağlantısı olmayan gözlem satırı elle bırakılır
            continue
        satir[2] = " | ".join(dict.fromkeys(kisalt(p["girdi"]) for p in props))
        satir[3] = " | ".join(dict.fromkeys(p["beklenen"] for p in props))
        satir[4] = " | ".join(dict.fromkeys(p["gerceklesen"] for p in props))
    with (TABLOLAR / alan / "T6_bulgular.csv").open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, delimiter=";").writerows(t6)
    return t6


def bloklar(alan, ayar, tumu, bizim):
    adlar, teknikler = ayar["adlar"], ayar["teknikler"]
    t1 = csv_oku(alan, "T1_gereksinimler.csv")
    t6 = t6_yenile(alan, bizim)
    t3, uyarilar = t3_sinirlar(bizim)
    if uyarilar:
        raise ValueError("\n".join(uyarilar))

    sutunlar = ["Toplam", *teknikler, "PASS", "FAIL", "XFAIL"]
    sayac = defaultdict(Counter)
    for p in bizim:
        for anahtar in ("Toplam", p["teknik"], p["durum"]):
            sayac[p["fonksiyon"]][anahtar] += 1
    t5 = [[fn, *[sayac[fn][c] for c in sutunlar]] for fn in adlar]
    toplam = {c: sum(s[i] for s in t5) for i, c in enumerate(sutunlar, start=1)}
    tum = Counter(p["durum"] for p in tumu)

    # Her işlev için bir geçerli + bir geçersiz EP temsilcisi ve bir BVA sonucu.
    t2, t4 = [], []
    for fn in adlar:
        ep = [p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "EP"]
        for beklenen in ("True", "ValidationError"):
            p = next(p for p in ep if p["beklenen"] == beklenen)
            t2.append([fn, p["sinif"], kisalt(p["girdi"]), p["beklenen"], p["test_id"]])
        p = next(p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "BVA")
        t4.append([p["test_id"], kisalt(p["girdi"]), p["parametreler"], p["beklenen"],
                   p["gerceklesen"], p["durum"]])

    sonuc = {
        "T1": tablo(t1[0], t1[1:]),
        "T2": tablo(["Fonksiyon", "Sınıf", "Temsilci girdi", "Beklenen", "Test ID"], t2),
        "T3": tablo(["Fonksiyon", "Sınır", "SD-1", "SD", "SD+1", "Beklenen", "Test ID"], t3),
        "T4": tablo(["Test ID", "Girdi", "Parametreler", "Beklenen", "Gerçekleşen", "Durum"], t4),
        "T5": tablo(["Fonksiyon", *sutunlar], t5 + [["TOPLAM", *toplam.values()]])
              + f"\n\nAlan: {toplam['Toplam']} test, {toplam['PASS']} PASS, {toplam['FAIL']} FAIL, "
                f"{toplam['XFAIL']} XFAIL. Tüm depo: {len(tumu)} test, {tum['PASS']} PASS, "
                f"{tum['FAIL']} FAIL, {tum['XFAIL']} XFAIL.\n\n"
                f"T1: {len(t1) - 1} gereksinim; T3: {len(t3)} sınır grubu. Başarı oranı: "
                f"%{100 * toplam['PASS'] / toplam['Toplam']:.1f} (XFAIL başarıya eklenmemiştir).",
        "T6": tablo(t6[0], t6[1:]),
    }
    if "DT" in teknikler:
        sonuc["DT"] = tablo(
            ["Test ID", "Kural", "Parametreler", "Girdi", "Beklenen", "Gerçekleşen", "Durum"],
            [[p["test_id"], p["sinif"], p["parametreler"], p["girdi"], p["beklenen"],
              p["gerceklesen"], p["durum"]] for p in bizim if p["teknik"] == "DT"])
    return sonuc


def raporu_yaz(alan, blok):
    rapor = KOK / "docs" / f"rapor_{alan}.md"
    metin = rapor.read_text(encoding="utf-8")
    for ad, deger in blok.items():
        desen = rf"(<!-- OTOMATIK:{ad} -->).*?(<!-- /OTOMATIK:{ad} -->)"
        metin, n = re.subn(desen, lambda m: m[1] + "\n" + deger + "\n" + m[2], metin, flags=re.S)
        if n != 1:
            raise ValueError(f"{rapor.name}: {ad} işareti bulunamadı veya yinelenmiş")
    rapor.write_text(metin, encoding="utf-8")


def alani_yenile(alan):
    ayar = ALANLAR[alan]
    tumu, bizim = sonuclari_oku(alan, ayar)
    diyagramlar(alan, ayar, bizim)
    raporu_yaz(alan, bloklar(alan, ayar, tumu, bizim))
    print(f"{alan}: {len(bizim)} test -> rapor blokları, T6 sonuç sütunları ve D1-D5 yenilendi.")


def main():
    secilen = sys.argv[1:] or list(ALANLAR)
    bilinmeyen = [a for a in secilen if a not in ALANLAR]
    if bilinmeyen:
        sys.exit(f"Bilinmeyen alan: {', '.join(bilinmeyen)}. Seçenekler: {', '.join(ALANLAR)}")
    for alan in secilen:
        alani_yenile(alan)


if __name__ == "__main__":
    main()
