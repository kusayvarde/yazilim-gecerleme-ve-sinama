"""payments_finance bölümünün sonuçlarını XML'den yeniler ve kendi D1-D5 görsellerini üretir.

Kullanım: uv run python -m tests.payments_finance.rapor_uret
Önce tüm testler (uv run pytest) ve scripts/sonuc_tablosu.py çalıştırılmalıdır.
Paylaşılan betikleri ve diğer alanların dosyalarını değiştirmez.
Yapı tests/urls_national_ids/rapor_uret.py ile aynıdır (ekip rapor biçimi).
"""

import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
ALAN = "payments_finance"
BASLIK = "Ödeme ve finans"
ADLAR = ["email", "cusip", "isin", "sedol", "card_number", "visa", "mastercard",
         "amex", "discover", "diners", "jcb", "unionpay", "mir"]
TEKNIKLER = ["EP", "BVA"]
GORSEL = KOK / "docs" / "diyagramlar"
RAPOR = KOK / "docs" / f"rapor_{ALAN}.md"

D3 = ("D3 - email eşdeğerlik sınıfları",
      ["Geçerli\ndot-atom / tırnaklı yerel kısım\nLDH alan adı, IDN\nseçenekle IP-literal",
       "Girdi uzayı\nRFC 5321 / 5322",
       "Geçersiz\n'@' yok / çift, nokta kuralı\netiket tire, sayısal TLD\nuzunluk aşımı"])
D4 = [([2719, 2720, 2721], ["V", "V", "I"], "Mastercard 2-serisi üst sınırı (önek)"),
      ([63, 64, 65], ["V", "V", "I"], "email yerel kısım uzunluğu (RFC 5321)")]


def tablo(baslik, satirlar):
    def hucre(v):
        return str(v).replace("|", "\\|").replace("\n", " ")
    return "\n".join("| " + " | ".join(map(hucre, s)) + " |"
                     for s in [baslik, ["---"] * len(baslik), *satirlar])


def kisalt(metin, sinir=60):
    if len(metin) <= sinir:
        return metin
    uzunluk = len(metin) - 2 if metin[:1] in "'\"" and metin[-1:] == metin[:1] else len(metin)
    return f"{metin[:sinir]}… ({uzunluk} karakter)"


def csv_oku(ad):
    with (KOK / "docs" / "tablolar" / ad).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f, delimiter=";"))


def sonuclari_oku():
    tumu, bizim = [], []
    for case in ET.parse(KOK / "reports" / "sonuc.xml").getroot().iter("testcase"):
        p = {v.get("name"): v.get("value") for v in case.iter("property")}
        if not p.get("test_id"):
            raise ValueError("XML içinde test kimliği olmayan kayıt var; önce tam pytest çalıştırın")
        skipped = case.find("skipped")
        p["durum"] = ("XFAIL" if skipped.get("type") == "pytest.xfail" else "SKIP") if skipped is not None else (
            "FAIL" if case.find("failure") is not None or case.find("error") is not None else "PASS")
        tumu.append(p)
        if f"tests.{ALAN}." in case.get("classname", ""):
            bizim.append(p)
    if {p["fonksiyon"] for p in bizim} != set(ADLAR):
        raise ValueError("XML bu alanın tüm fonksiyonlarını içermiyor")
    from scripts.sonuc_tablosu import izlenebilirlik
    _, uyari = izlenebilirlik(csv_oku(f"T1_{ALAN}.csv"), bizim)
    if uyari:
        raise ValueError("\n".join(uyari))
    return tumu, bizim


def kutular(ad, baslik, metinler):
    fig, ax = plt.subplots(figsize=(12, 3.4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    xs = [0.15, 0.50, 0.85]
    for x, metin in zip(xs, metinler, strict=True):
        ax.text(x, 0.5, metin, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.8", facecolor="#e8eef8", edgecolor="#244775"))
    oklar = [(xs[0] + .13, xs[1] - .13), (xs[1] + .13, xs[2] - .13)]
    if ad == "D3":
        oklar[0] = (xs[1] - .13, xs[0] + .13)
    for bas, son in oklar:
        ax.annotate("", xy=(son, .5), xytext=(bas, .5),
                    arrowprops=dict(arrowstyle="->", color="#244775", lw=2))
    ax.set_title(baslik, fontsize=14, pad=18)
    fig.tight_layout()
    fig.savefig(GORSEL / f"{ad}_{ALAN}.png", dpi=160)
    plt.close(fig)


def test_sureci():
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    dugumler = [
        (.14, .81, "Docstring + standart\nT1 gereksinimleri"),
        (.49, .81, "EP + BVA\nTest senaryoları"),
        (.85, .81, "pytest\nFonksiyonu çağır"),
        (.49, .45, "FAIL analizi\nTest mi, kütüphane mi?"),
        (.14, .45, "Test / gereksinim\nverisini düzelt"),
        (.49, .13, "Kütüphane uyuşmazlığı\nT6 + strict xfail"),
        (.85, .13, "XML / HTML\nTablolar + rapor"),
    ]
    for x, y, metin in dugumler:
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
    fig.savefig(GORSEL / f"D2_{ALAN}.png", dpi=160)
    plt.close(fig)


def diyagramlar(bizim):
    GORSEL.mkdir(exist_ok=True)
    kutular("D1", f"D1 - {BASLIK}: kara-kutu modeli",
            ["Girdi\nadres / kod / kart no\n+ seçenekler", "validators 0.36.0\nİç yapı incelenmez",
             "Çıktı\nTrue / ValidationError"])
    test_sureci()
    kutular("D3", *D3)
    fig, axes = plt.subplots(len(D4), 1, figsize=(11, 2.4 * len(D4)))
    for ax, (degerler, etiketler, baslik) in zip(axes, D4, strict=True):
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
    fig.savefig(GORSEL / f"D4_{ALAN}.png", dpi=160)
    plt.close(fig)
    sayac = defaultdict(Counter)
    for p in bizim:
        sayac[p["fonksiyon"]][p["durum"]] += 1
        sayac[p["fonksiyon"]][p["teknik"]] += 1
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    renk = {"EP": "#1565c0", "BVA": "#6a1b9a", "DT": "#00838f"}
    for ax, sutunlar, baslik in [
        (axes[0], [("PASS", "#2e7d32"), ("XFAIL", "#f9a825"), ("FAIL", "#c62828")], "Gerçek sonuçlar (JUnit XML)"),
        (axes[1], [(t, renk[t]) for t in TEKNIKLER], "Test tasarım teknikleri"),
    ]:
        alt = [0] * len(ADLAR)
        for sutun, r in sutunlar:
            degerler = [sayac[fn][sutun] for fn in ADLAR]
            ax.bar(ADLAR, degerler, bottom=alt, label=sutun, color=r)
            alt = [a + b for a, b in zip(alt, degerler)]
        ax.set_title(baslik)
        ax.set_ylabel("Test sayısı")
        ax.tick_params(axis="x", labelrotation=55)
        for etiket in ax.get_xticklabels():
            etiket.set_ha("right")
        ax.legend()
    fig.tight_layout()
    fig.savefig(GORSEL / f"D5_{ALAN}.png", dpi=160)
    plt.close(fig)


def yenile(tumu, bizim):
    t1 = csv_oku(f"T1_{ALAN}.csv")
    t6 = csv_oku(f"T6_{ALAN}.csv")
    # Girdi/Beklenen/Gerçekleşen pytest sonucundan yenilenir; elle doldurulmaz.
    kimlik = {p["test_id"]: p for p in bizim}
    for satir in t6[1:]:
        ids = [i.strip() for i in satir[1].split(",") if i.strip() in kimlik]
        if not ids:  # test bağlantısı olmayan gözlem satırı
            continue
        props = [kimlik[i] for i in ids]
        satir[2] = " | ".join(dict.fromkeys(kisalt(p["girdi"]) for p in props))
        satir[3] = " | ".join(dict.fromkeys(p["beklenen"] for p in props))
        satir[4] = " | ".join(dict.fromkeys(p["gerceklesen"] for p in props))
    with (KOK / "docs" / "tablolar" / f"T6_{ALAN}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, delimiter=";").writerows(t6)
    from scripts.sonuc_tablosu import t3_sinirlar
    t3, uyarilar = t3_sinirlar(bizim)
    if uyarilar:
        raise ValueError("\n".join(uyarilar))
    sutunlar = ["Toplam", *TEKNIKLER, "PASS", "FAIL", "XFAIL"]
    sayac = defaultdict(Counter)
    for p in bizim:
        sayac[p["fonksiyon"]]["Toplam"] += 1
        sayac[p["fonksiyon"]][p["teknik"]] += 1
        sayac[p["fonksiyon"]][p["durum"]] += 1
    sonuc = [[fn, *[sayac[fn][c] for c in sutunlar]] for fn in ADLAR]
    toplam = dict(zip(sutunlar, [sum(s[i] for s in sonuc) for i in range(1, len(sutunlar) + 1)]))
    tum = Counter(p["durum"] for p in tumu)
    t2, t4 = [], []
    for fn in ADLAR:
        ep = [p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "EP"]
        for beklenen in ("True", "ValidationError"):
            p = next(p for p in ep if p["beklenen"] == beklenen)
            t2.append([fn, p["sinif"], kisalt(p["girdi"]), p["beklenen"], p["test_id"]])
        p = next(p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "BVA")
        t4.append([kisalt(p[k]) if k == "girdi" else p[k]
                   for k in ("test_id", "girdi", "parametreler", "beklenen", "gerceklesen", "durum")])
    bloklar = {
        "T1": tablo(t1[0], t1[1:]),
        "T2": tablo(["Fonksiyon", "Sınıf", "Temsilci girdi", "Beklenen", "Test ID"], t2),
        "T3": tablo(["Fonksiyon", "Sınır", "SD-1", "SD", "SD+1", "Beklenen", "Test ID"], t3),
        "T4": tablo(["Test ID", "Girdi", "Parametreler", "Beklenen", "Gerçekleşen", "Durum"], t4),
        "T5": tablo(["Fonksiyon", *sutunlar], sonuc + [["TOPLAM", *toplam.values()]])
              + f"\n\nAlan: {toplam['Toplam']} test, {toplam['PASS']} PASS, {toplam['FAIL']} FAIL, "
                f"{toplam['XFAIL']} XFAIL. Tüm depo: {len(tumu)} test, {tum['PASS']} PASS, "
                f"{tum['FAIL']} FAIL, {tum['XFAIL']} XFAIL.\n\n"
                f"T1: {len(t1) - 1} gereksinim; T3: {len(t3)} sınır grubu. Başarı oranı: "
                f"%{100 * toplam['PASS'] / toplam['Toplam']:.1f} (XFAIL başarıya eklenmemiştir).",
        "T6": tablo(t6[0], t6[1:]),
    }
    metin = RAPOR.read_text(encoding="utf-8")
    for ad, deger in bloklar.items():
        desen = rf"(<!-- OTOMATIK:{ad} -->).*?(<!-- /OTOMATIK:{ad} -->)"
        metin, n = re.subn(desen, lambda m: m[1] + "\n" + deger + "\n" + m[2], metin, flags=re.S)
        if n != 1:
            raise ValueError(f"Raporda {ad} işareti bulunamadı veya yinelenmiş")
    RAPOR.write_text(metin, encoding="utf-8")


def main():
    tumu, bizim = sonuclari_oku()
    diyagramlar(bizim)
    yenile(tumu, bizim)
    print(f"{len(bizim)} test: rapor, T6 gerçekleşen sonuçları ve D1-D5 yenilendi.")


if __name__ == "__main__":
    main()
