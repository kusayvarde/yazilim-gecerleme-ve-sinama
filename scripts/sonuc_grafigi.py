"""D5: T5 özetinden fonksiyon başına PASS / XFAIL / FAIL yığılmış bar grafiği.

Kullanım:  uv run python scripts/sonuc_grafigi.py   (önce sonuc_tablosu.py çalışmalı)
Çıktı:     reports/D5_sonuc_grafigi.png
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
T5 = KOK / "reports" / "T5_sonuc_ozeti.csv"
CIKTI = KOK / "reports" / "D5_sonuc_grafigi.png"


def main():
    with T5.open(encoding="utf-8-sig") as f:
        veri = list(csv.DictReader(f, delimiter=";"))
    adlar = [r["Fonksiyon"] for r in veri]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    alt = [0] * len(veri)
    for sutun, renk in [("PASS", "#2e7d32"), ("XFAIL (bulgu)", "#f9a825"), ("FAIL", "#c62828")]:
        degerler = [int(r[sutun]) for r in veri]
        ax1.bar(adlar, degerler, bottom=alt, label=sutun, color=renk)
        alt = [a + d for a, d in zip(alt, degerler)]
    ax1.set_title("Fonksiyon başına test sonuçları")
    ax1.set_ylabel("Test sayısı")
    ax1.legend()

    alt = [0] * len(veri)
    for sutun, renk in [("EP", "#1565c0"), ("BVA", "#6a1b9a"), ("DT", "#00838f")]:
        degerler = [int(r[sutun]) for r in veri]
        ax2.bar(adlar, degerler, bottom=alt, label=sutun, color=renk)
        alt = [a + d for a, d in zip(alt, degerler)]
    ax2.set_title("Teknik dağılımı (EP / BVA / Karar tablosu)")
    ax2.legend()

    for ax in (ax1, ax2):
        ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(CIKTI, dpi=150)
    print(f"Grafik -> {CIKTI.relative_to(KOK)}")


if __name__ == "__main__":
    main()
