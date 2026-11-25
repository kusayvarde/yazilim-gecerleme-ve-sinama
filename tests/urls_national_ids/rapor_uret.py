"""MMHDJ bölümünün sonuçlarını XML'den yeniler ve kendi D1-D5 görsellerini üretir.

Kullanım: uv run python -m tests.urls_national_ids.rapor_uret
Önce tüm testler ve scripts/sonuc_tablosu.py çalıştırılmalıdır.
Paylaşılan betikleri, diğer alanların dosyalarını veya Git dallarını değiştirmez.
"""

import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parents[2]
ALAN = "urls_national_ids"
ADLAR = ["url", "es_nif", "es_nie", "es_cif", "es_doi", "fi_business_id",
         "fi_ssn", "fr_ssn", "ru_inn", "fr_department"]
GORSEL = KOK / "docs" / "diyagramlar"
RAPOR = KOK / "docs" / f"rapor_{ALAN}.md"


def tablo(baslik, satirlar):
    def hucre(v):
        return str(v).replace("|", "\\|").replace("\n", " ")
    return "\n".join("| " + " | ".join(map(hucre, s)) + " |"
                     for s in [baslik, ["---"] * len(baslik), *satirlar])


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
    # T1 kontrolü eksik/filtrelenmiş pytest çalıştırmalarının rapora girmesini önler.
    from scripts.sonuc_tablosu import izlenebilirlik
    t1 = csv_oku(f"T1_{ALAN}.csv")
    _, uyari = izlenebilirlik(t1, bizim)
    if uyari:
        raise ValueError("\n".join(uyari))
    return tumu, bizim


def kutular(ad, baslik, metinler):
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    xs = [0.15, 0.50, 0.85]
    for x, metin in zip(xs, metinler, strict=True):
        ax.text(x, 0.5, metin, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.8", facecolor="#e8eef8", edgecolor="#244775"))
    fleches = [(xs[0] + .13, xs[1] - .13), (xs[1] + .13, xs[2] - .13)]
    if ad == "D3":
        fleches[0] = (xs[1] - .13, xs[0] + .13)
    for depart, arrivee in fleches:
        ax.annotate("", xy=(arrivee, .5), xytext=(depart, .5),
                    arrowprops=dict(arrowstyle="->", color="#244775", lw=2))
    ax.set_title(baslik, fontsize=14, pad=18)
    fig.tight_layout()
    fig.savefig(GORSEL / f"{ad}_{ALAN}.png", dpi=160)
    plt.close(fig)


def diyagramlar(bizim):
    GORSEL.mkdir(exist_ok=True)
    kutular("D1", "D1 - URL ve ulusal kimlikler: kara-kutu modeli",
            ["Girdi\nURL / kimlik\n+ seçenekler", "validators 0.36.0\nİç yapı incelenmez", "Çıktı\nTrue / ValidationError"])
    test_sureci()
    kutular("D3", "D3 - INN eşdeğerlik sınıfları",
            ["Geçerli\n10 hane + kontrol\n12 hane + iki kontrol", "Girdi uzayı\nSentetik örnekler", "Geçersiz\nYanlış uzunluk\nHarf / bozuk kontrol"])
    fig, axes = plt.subplots(2, 1, figsize=(11, 4.8))
    for ax, values, labels, title in [
        (axes[0], [899, 900, 901], ["V", "I", "I"], "Geçici HETU alt sınırı (allow_temporal_ssn=False)"),
        (axes[1], [65534, 65535, 65536], ["V", "V", "I"], "URL hizmet portu üst sınırı"),
    ]:
        ax.axhline(0, color="#244775")
        ax.scatter(values, [0] * 3, c=["#2e7d32" if v == "V" else "#c62828" for v in labels], s=100, zorder=3)
        for value, label, pos in zip(values, labels, ["SD-1", "SD", "SD+1"], strict=True):
            ax.text(value, .15, f"{pos}: {value}\n{label}", ha="center")
        ax.set(xlim=(values[0] - .5, values[-1] + .5), ylim=(-.2, .6), yticks=[], xticks=[])
        ax.set_title(title, fontsize=11)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(GORSEL / f"D4_{ALAN}.png", dpi=160)
    plt.close(fig)
    counts = defaultdict(Counter)
    for p in bizim:
        counts[p["fonksiyon"]][p["durum"]] += 1
        counts[p["fonksiyon"]][p["teknik"]] += 1
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    for ax, columns, title in [
        (axes[0], [("PASS", "#2e7d32"), ("XFAIL", "#f9a825"), ("FAIL", "#c62828")], "Gerçek sonuçlar (JUnit XML)"),
        (axes[1], [("EP", "#1565c0"), ("BVA", "#6a1b9a")], "Test tasarım teknikleri"),
    ]:
        bottom = [0] * len(ADLAR)
        for col, color in columns:
            values = [counts[fn][col] for fn in ADLAR]
            ax.bar(ADLAR, values, bottom=bottom, label=col, color=color)
            bottom = [a + b for a, b in zip(bottom, values)]
        ax.set_title(title)
        ax.set_ylabel("Test sayısı")
        ax.tick_params(axis="x", labelrotation=55)
        for label in ax.get_xticklabels():
            label.set_ha("right")
        ax.legend()
    fig.tight_layout()
    fig.savefig(GORSEL / f"D5_{ALAN}.png", dpi=160)
    plt.close(fig)


def test_sureci():
    """Başarısız testin düzeltilmesi / bulgu olarak korunması döngüsünü çizer."""
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    nodes = {
        "req": (.14, .81, "Docstring + standart\nT1 gereksinimleri"),
        "design": (.49, .81, "EP + BVA\nTest senaryoları"),
        "run": (.85, .81, "pytest\nFonksiyonu çağır"),
        "analysis": (.49, .45, "FAIL analizi\nTest mi, kütüphane mi?"),
        "fix": (.14, .45, "Test / gereksinim\nverisini düzelt"),
        "finding": (.49, .13, "Kütüphane uyuşmazlığı\nT6 + strict xfail"),
        "report": (.85, .13, "XML / HTML\nTablolar + rapor"),
    }
    for x, y, label in nodes.values():
        ax.text(x, y, label, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=.7", facecolor="#e8eef8", edgecolor="#244775"))
    def arrow(start, end, label="", text_xy=None, rad=0):
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", lw=1.8, color="#244775",
                                    connectionstyle=f"arc3,rad={rad}"))
        if label:
            x, y = text_xy or ((start[0]+end[0])/2, (start[1]+end[1])/2)
            ax.text(x, y, label, ha="center", va="center", fontsize=10,
                    bbox=dict(facecolor="white", edgecolor="none", pad=1))
    arrow((.26,.81),(.37,.81))
    arrow((.62,.81),(.76,.81))
    arrow((.85,.74),(.85,.20),"PASS / beklenen XFAIL",(.85,.48))
    arrow((.81,.74),(.61,.50),"FAIL",(.73,.63))
    arrow((.36,.45),(.25,.45),"Test yanlış",(.30,.50))
    arrow((.14,.52),(.14,.74))
    arrow((.49,.38),(.49,.20),"Beklenti doğru",(.49,.29))
    arrow((.60,.13),(.91,.75),"Yeniden çalıştır",(.69,.36),rad=.43)
    ax.set_title("D2 - Test, analiz ve yeniden doğrulama döngüsü",fontsize=14,pad=12)
    fig.tight_layout()
    fig.savefig(GORSEL / f"D2_{ALAN}.png",dpi=160)
    plt.close(fig)


def yenile(tumu, bizim):
    t1 = csv_oku(f"T1_{ALAN}.csv")
    t6 = csv_oku(f"T6_{ALAN}.csv")
    # Gerçekleşen/Beklenen alanları pytest sonucundan yenilenir; elle doldurulmaz.
    by_id = {p["test_id"]: p for p in bizim}
    for row in t6[1:]:
        props = [by_id[i.strip()] for i in row[1].split(",")]
        row[2] = " | ".join(dict.fromkeys(p["girdi"] for p in props))
        row[3] = " | ".join(dict.fromkeys(p["beklenen"] for p in props))
        row[4] = " | ".join(dict.fromkeys(p["gerceklesen"] for p in props))
    with (KOK / "docs" / "tablolar" / f"T6_{ALAN}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, delimiter=";").writerows(t6)
    from scripts.sonuc_tablosu import t3_sinirlar
    t3, warnings = t3_sinirlar(bizim)
    if warnings:
        raise ValueError("\n".join(warnings))
    counters = defaultdict(Counter)
    for p in bizim:
        counters[p["fonksiyon"]]["Toplam"] += 1
        counters[p["fonksiyon"]][p["teknik"]] += 1
        counters[p["fonksiyon"]][p["durum"]] += 1
    result_rows = [[fn, *[counters[fn][c] for c in ("Toplam", "EP", "BVA", "PASS", "FAIL", "XFAIL")]] for fn in ADLAR]
    totals = [sum(row[i] for row in result_rows) for i in range(1, 7)]
    all_counts = Counter(p["durum"] for p in tumu)
    # Her işlev için geçerli/geçersiz bir EP temsilcisi ve bir BVA sonucu göster.
    t2_rows, t4_rows = [], []
    for fn in ADLAR:
        ep = [p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "EP"]
        for expected in ("True", "ValidationError"):
            p = next(p for p in ep if p["beklenen"] == expected)
            t2_rows.append([fn, p["sinif"], p["girdi"], p["beklenen"], p["test_id"]])
        p = next(p for p in bizim if p["fonksiyon"] == fn and p["teknik"] == "BVA")
        t4_rows.append([p[k] for k in ("test_id", "girdi", "parametreler", "beklenen", "gerceklesen", "durum")])
    blocks = {
        "T1": tablo(t1[0], t1[1:]),
        "T2": tablo(["Fonksiyon", "Sınıf", "Temsilci girdi", "Beklenen", "Test ID"], t2_rows),
        "T3": tablo(["Fonksiyon", "Sınır", "SD-1", "SD", "SD+1", "Beklenen", "Test ID"], t3),
        "T4": tablo(["Test ID", "Girdi", "Parametreler", "Beklenen", "Gerçekleşen", "Durum"], t4_rows),
        "T5": tablo(["Fonksiyon", "Toplam", "EP", "BVA", "PASS", "FAIL", "XFAIL"], result_rows + [["TOPLAM", *totals]])
              + f"\n\nAlan: {totals[0]} test, {totals[3]} PASS, {totals[4]} FAIL, {totals[5]} XFAIL. "
                f"Tüm depo: {len(tumu)} test, {all_counts['PASS']} PASS, {all_counts['FAIL']} FAIL, {all_counts['XFAIL']} XFAIL.\n\n"
                f"T1: {len(t1)-1} gereksinim; T3: {len(t3)} sınır grubu. Başarı oranı: %{100*totals[3]/totals[0]:.1f} "
                "(XFAIL başarıya eklenmemiştir).",
        "T6": tablo(t6[0], t6[1:]),
    }
    text = RAPOR.read_text(encoding="utf-8")
    for name, value in blocks.items():
        pattern = rf"(<!-- OTOMATIK:{name} -->).*?(<!-- /OTOMATIK:{name} -->)"
        text, n = re.subn(pattern, lambda m: m[1] + "\n" + value + "\n" + m[2], text, flags=re.S)
        if n != 1:
            raise ValueError(f"Raporda {name} işareti bulunamadı veya yinelenmiş")
    RAPOR.write_text(text, encoding="utf-8")


def main():
    tumu, bizim = sonuclari_oku()
    diyagramlar(bizim)
    yenile(tumu, bizim)
    print(f"{len(bizim)} test: rapor, T6 gerçekleşen sonuçları ve D1-D5 yenilendi.")


if __name__ == "__main__":
    main()
