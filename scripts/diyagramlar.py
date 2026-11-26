"""D1, D3, D4 tasarım diyagramlarını çizer (matplotlib).

Kullanım:  uv run python scripts/diyagramlar.py
Çıktı:     docs/diyagramlar/network_crypto/D1_kara_kutu_modeli.png
           docs/diyagramlar/network_crypto/D3_esdegerlik_siniflari.png
           docs/diyagramlar/network_crypto/D4_sinir_degerleri.png

Diyagramlar test tasarımını (T2 sınıfları, T3 sınırları) gösterir; test sonucuna
bağlı değildir. Sınıf kodları ve Test ID'leri test dosyalarındakiyle aynıdır.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "docs" / "diyagramlar" / "network_crypto"

YESIL, YESIL_ACIK = "#2e7d32", "#e8f5e9"
KIRMIZI, KIRMIZI_ACIK = "#c62828", "#ffebee"
KOYU, GRI = "#212121", "#616161"


def kutu(ax, x, y, w, h, metin, *, yuz="white", kenar=KOYU, renk=KOYU, boyut=10, kalin=False, lw=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=yuz, ec=kenar, lw=lw))
    ax.text(x + w / 2, y + h / 2, metin, ha="center", va="center", fontsize=boyut,
            color=renk, fontweight="bold" if kalin else "normal", linespacing=1.4)


def ok(ax, x1, y1, x2, y2, renk=KOYU):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=22,
                                 lw=2, color=renk))


# ---------------------------------------------------------------- D1
def d1():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    kutu(ax, 0.2, 1.3, 3.4, 1.9,
         "GİRDİ\n\nvalue: str\n(+ uuid.UUID nesnesi)\n\nparametreler:\ncidr, strict, private, host_bit",
         yuz="#e3f2fd", kenar="#1565c0", boyut=9.5)
    kutu(ax, 4.5, 1.3, 3.0, 1.9, "validators.<fonksiyon>\n\n(iç yapı görünmez)",
         yuz=KOYU, kenar=KOYU, renk="white", boyut=11, kalin=True)
    kutu(ax, 8.4, 2.35, 3.4, 0.85, "True  →  geçerli", yuz=YESIL_ACIK, kenar=YESIL, renk=YESIL,
         boyut=10.5, kalin=True)
    kutu(ax, 8.4, 1.3, 3.4, 0.85, "ValidationError  →  geçersiz\n(falsy nesne, istisna fırlatılmaz)",
         yuz=KIRMIZI_ACIK, kenar=KIRMIZI, renk=KIRMIZI, boyut=9.5)

    ok(ax, 3.65, 2.25, 4.45, 2.25)
    ok(ax, 7.55, 2.25, 8.35, 2.25)

    ax.text(6.0, 0.75, "Beklenen sonuç yalnızca dokümandan (docstring) ve standartlardan türetilir:\n"
            "RFC 791 / 4291, Unix cron, Base58Check, EIP-55, BIP-173, RFC 9562, FIPS 180-4",
            ha="center", va="center", fontsize=9.5, color=GRI, style="italic")
    ax.text(6.0, 3.85, "D1 – Kara-kutu modeli", ha="center", fontsize=14, fontweight="bold")
    kaydet(fig, "D1_kara_kutu_modeli.png")


# ---------------------------------------------------------------- D3
IPV4_V = [
    ("V1", "standart 4 oktet", "192.168.1.1"),
    ("V2", "CIDR (cidr=True)", "10.0.0.0/8"),
    ("V3", "strict=True + CIDR", "10.0.0.0/8"),
    ("V4", "private=True + private", "192.168.0.1"),
    ("V4b", "private=True + loopback", "127.0.0.1"),
    ("V4c", "private=True + broadcast", "255.255.255.255"),
    ("V5", "private=False + public", "8.8.8.8"),
    ("V6", "host_bit=False + host bit 0", "192.168.1.0/24"),
]
IPV4_I = [
    ("I1", "oktet > 255", "256.1.1.1"),
    ("I2", "eksik oktet (3)", "192.168.1"),
    ("I3", "fazla oktet (5)", "1.2.3.4.5"),
    ("I4", "harf içeriyor", "192.168.a.1"),
    ("I5", "boş string", "''"),
    ("I6", "negatif sayı", "-1.2.3.4"),
    ("I7", "baştaki sıfır", "01.2.3.4"),
    ("I8a", "sonda boşluk", "'1.2.3.4 '"),
    ("I8b", "özel karakter", "1.2.3.#"),
    ("I9", "CIDR öneki > 32", "1.2.3.4/64"),
    ("I10", "strict=True, CIDR yok", "1.2.3.4"),
    ("I11", "cidr=False, CIDR var", "10.0.0.0/8"),
    ("I12", "private=False + private", "192.168.1.1"),
    ("I13", "private=True + public", "8.8.8.8"),
    ("I14", "host_bit=False + host bit set", "192.168.1.1/24"),
    ("I15", "IPv6 adresi", "::1"),
]
IPV6_V = [
    ("V1", "tam 8 grup", "2001:0db8:…:8329"),
    ("V2", ":: kısaltması", "2001:db8::1"),
    ("V3", "loopback", "::1"),
    ("V4", "IPv4-mapped", "::ffff:192.0.2.128"),
    ("V5", "CIDR", "2001:db8::/32"),
    ("V6", "büyük harf hex", "2001:DB8::1"),
    ("V7", "belirtilmemiş (tümü 0)", "::"),
    ("V8", "strict=True + CIDR", "2001:db8::/32"),
    ("V9", "host_bit=False + host bit 0", "2001:db8::/32"),
]
IPV6_I = [
    ("I1", "9 grup", "1:2:3:4:5:6:7:8:9"),
    ("I2", "grupta 5 hex", "2001:db8::12345"),
    ("I3", "hex olmayan karakter", "2001:db8::g"),
    ("I4", "iki kez ::", "2001::db8::1"),
    ("I5", "önek > 128", "::1/200"),
    ("I6", "IPv4 adresi", "1.2.3.4"),
    ("I7", "boş string", "''"),
    ("I8", "strict=True, CIDR yok", "::1"),
    ("I9", "host_bit=False + host bit set", "2001:db8::1/32"),
    ("I10", "cidr=False, CIDR var", "2001:db8::/32"),
    ("I11", "üç iki nokta (:::)", ":::1"),
    ("I12", "sonda boşluk", "'2001:db8::1 '"),
]


def bolge(ax, x0, y0, w, h, baslik, siniflar, kolon, renk, acik):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=acik, ec=renk, lw=2))
    ax.text(x0 + 0.15, y0 + h - 0.3, baslik, fontsize=11, fontweight="bold", color=renk, va="center")
    satir = -(-len(siniflar) // kolon)
    hw, hh = (w - 0.3) / kolon, (h - 0.7) / satir
    for i, (kod, ad, ornek) in enumerate(siniflar):
        c, r = i // satir, i % satir
        x, y = x0 + 0.15 + c * hw, y0 + h - 0.65 - (r + 1) * hh
        ax.add_patch(FancyBboxPatch((x + 0.04, y + 0.04), hw - 0.08, hh - 0.08,
                                    boxstyle="round,pad=0,rounding_size=0.06", fc="white", ec=renk, lw=0.8))
        ax.text(x + 0.14, y + hh / 2, kod, fontsize=9, fontweight="bold", color=renk, va="center")
        ax.text(x + 0.75, y + hh / 2 + 0.11, ad, fontsize=7.6, color=KOYU, va="center")
        ax.text(x + 0.75, y + hh / 2 - 0.13, ornek, fontsize=7.2, color=GRI, va="center", family="monospace")


def d3():
    fig, axes = plt.subplots(2, 1, figsize=(15, 12.5),
                             gridspec_kw={"height_ratios": [len(IPV4_I) / 2 + 2.2, len(IPV6_I) / 2 + 2.2]})
    for ax, ad, v, i, vk, ik in [(axes[0], "ipv4", IPV4_V, IPV4_I, 1, 2),
                                 (axes[1], "ipv6", IPV6_V, IPV6_I, 1, 2)]:
        satir = max(-(-len(v) // vk), -(-len(i) // ik))
        h = satir * 0.62 + 0.8
        ax.set_xlim(0, 15)
        ax.set_ylim(0, h + 0.7)
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.05, 0.05), 14.9, h + 0.15, boxstyle="round,pad=0,rounding_size=0.2",
                                    fc="none", ec=KOYU, lw=1.5, ls="--"))
        ax.text(7.5, h + 0.45, f"validators.{ad} – girdi uzayı (değer × parametreler)",
                ha="center", fontsize=13, fontweight="bold")
        bolge(ax, 0.2, 0.15, 4.9, h - 0.1, f"Geçerli sınıflar (V)  →  True   [{len(v)}]", v, vk, YESIL, YESIL_ACIK)
        bolge(ax, 5.3, 0.15, 9.5, h - 0.1, f"Geçersiz sınıflar (I)  →  ValidationError   [{len(i)}]",
              i, ik, KIRMIZI, KIRMIZI_ACIK)
    fig.suptitle("D3 – Eşdeğerlik bölümleme (her sınıf = bir test, temsilci değerle)",
                 fontsize=15, fontweight="bold", y=0.995)
    fig.text(0.5, 0.005, "Geçersiz sınıflar birleştirilmez: her biri ayrı test (maskeleme önlenir). "
             "Dokümandaki örnekler ayrıca 'Doküman örneği' sınıfıyla test edilir.",
             ha="center", fontsize=9.5, color=GRI, style="italic")
    fig.tight_layout(rect=(0, 0.015, 1, 0.98))
    kaydet(fig, "D3_esdegerlik_siniflari.png")


# ---------------------------------------------------------------- D4
# (başlık, [(değer, beklenen, Test ID) × 6: min-1, min, min+1, maks-1, maks, maks+1])
SAYI_DOGRULARI = [
    ("ipv4 oktet  (geçerli aralık 0 – 255)",
     [(-1, "I", "IPV4-BVA-01"), (0, "V", "IPV4-BVA-02"), (1, "V", "IPV4-BVA-03"),
      (254, "V", "IPV4-BVA-04"), (255, "V", "IPV4-BVA-05"), (256, "I", "IPV4-BVA-06")]),
    ("ipv4 CIDR öneki  (geçerli aralık /0 – /32)",
     [(-1, "I", "IPV4-BVA-13"), (0, "V", "IPV4-BVA-14"), (1, "V", "IPV4-BVA-15"),
      (31, "V", "IPV4-BVA-16"), (32, "V", "IPV4-BVA-17"), (33, "I", "IPV4-BVA-18")]),
    ("cron dakika alanı  (geçerli aralık 0 – 59)",
     [(-1, "I", "CRON-BVA-01"), (0, "V", "CRON-BVA-02"), (1, "V", "CRON-BVA-22"),
      (58, "V", "CRON-BVA-23"), (59, "V", "CRON-BVA-03"), (60, "I", "CRON-BVA-04")]),
]
X = [1, 2, 3, 7, 8, 9]  # kesik eksen: alt sınır üçlüsü | … | üst sınır üçlüsü


def sayi_dogrusu(ax, baslik, noktalar):
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.6, 1.3)
    ax.axis("off")
    ax.text(0.05, 1.1, baslik, fontsize=12, fontweight="bold", va="center")
    # bölgeler
    ax.plot([0.2, 2], [0, 0], color=KIRMIZI, lw=5, solid_capstyle="butt")
    ax.plot([2, 8], [0, 0], color=YESIL, lw=5, solid_capstyle="butt")
    ax.plot([8, 9.8], [0, 0], color=KIRMIZI, lw=5, solid_capstyle="butt")
    ax.plot([4.6, 5.4], [0, 0], color="white", lw=7)  # eksen kesiği
    for dx in (4.6, 5.4):
        ax.plot([dx - 0.08, dx + 0.08], [-0.18, 0.18], color=KOYU, lw=1.5)
    ax.text(5.0, 0.32, "geçerli bölge (V)", ha="center", fontsize=10, color=YESIL, fontweight="bold")
    ax.text(0.9, 0.32, "geçersiz (I)", ha="center", fontsize=10, color=KIRMIZI, fontweight="bold")
    ax.text(9.1, 0.32, "geçersiz (I)", ha="center", fontsize=10, color=KIRMIZI, fontweight="bold")
    # sınır çizgileri
    for bx in (2, 8):
        ax.plot([bx, bx], [-0.35, 0.75], color=KOYU, lw=1, ls=":")
    ax.text(2, 0.85, "alt sınır", ha="center", fontsize=8.5, color=GRI)
    ax.text(8, 0.85, "üst sınır", ha="center", fontsize=8.5, color=GRI)
    etiketler = ["SD−1", "SD", "SD+1", "SD−1", "SD", "SD+1"]
    for x, (deger, beklenen, tid), et in zip(X, noktalar, etiketler):
        renk = YESIL if beklenen == "V" else KIRMIZI
        ax.plot(x, 0, "o", ms=13, mfc="white" if beklenen == "I" else renk, mec=renk, mew=2.5, zorder=5)
        ax.text(x, -0.42, str(deger), ha="center", fontsize=12, fontweight="bold")
        ax.text(x, -0.75, f"{et}  →  {beklenen}", ha="center", fontsize=9, color=renk)
        ax.text(x, -1.05, f"TC-{tid}", ha="center", fontsize=7.8, color=GRI, family="monospace")


def d4():
    fig, axes = plt.subplots(len(SAYI_DOGRULARI), 1, figsize=(13, 3.0 * len(SAYI_DOGRULARI) + 0.8))
    for ax, (baslik, noktalar) in zip(axes, SAYI_DOGRULARI):
        sayi_dogrusu(ax, baslik, noktalar)
    fig.suptitle("D4 – Sınır değer analizi: sayı doğruları (SD−1 / SD / SD+1)",
                 fontsize=15, fontweight="bold")
    fig.text(0.5, 0.01, "● dolu = geçerli (True beklenir)    ○ boş = geçersiz (ValidationError beklenir)    "
             "İki taraflı aralıkta 6 test: min−1, min, min+1, maks−1, maks, maks+1",
             ha="center", fontsize=9.5, color=GRI, style="italic")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    kaydet(fig, "D4_sinir_degerleri.png")


def kaydet(fig, ad):
    yol = HEDEF / ad
    fig.savefig(yol, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Diyagram -> {yol.relative_to(KOK)}")


if __name__ == "__main__":
    HEDEF.mkdir(parents=True, exist_ok=True)
    d1()
    d3()
    d4()
