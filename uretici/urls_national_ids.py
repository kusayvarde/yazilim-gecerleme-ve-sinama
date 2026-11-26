"""Standartlardan türetilen sentetik veriler; validators kullanılmaz.

Kaynaklar ve kapsam sınırlamaları docs/rapor_urls_national_ids.md içindedir.
Üretilen numaralar biçim/kontrol anahtarı örnekleridir, gerçek kayıt değildir.
"""

NIF_HARFLERI = "TRWAGMYFPDXBNJZSQVHLCKE"
HETU_HARFLERI = "0123456789ABCDEFHJKLMNPRSTUVWXY"


def nif_uret(govde="12345678"):
    return govde + NIF_HARFLERI[int(govde) % 23]


def nie_uret(onek="X", govde="1234567"):
    sayi = str("XYZ".index(onek)) + govde
    return onek + govde + NIF_HARFLERI[int(sayi) % 23]


def cif_uret(onek="B", govde="2516252", *, harf=False):
    """MAPA teknik arşivi: çift konumlar + tek konumların iki katı, mod-10.

    https://www.mapa.gob.es/app/materialvegetal/docs/CIF.pdf
    Bu arşiv teknik hesap örneğidir; kuruluş türlerinin normatif kaynağı AEAT'dir.
    """
    toplam = sum(int(c) for c in govde[1::2])
    toplam += sum(sum(divmod(2 * int(c), 10)) for c in govde[::2])
    kontrol = (-toplam) % 10
    return onek + govde + ("JABCDEFGHI"[kontrol] if harf else str(kontrol))


def isletme_uret(govde="0112038"):
    kalan = sum(int(c) * w for c, w in zip(govde, (7, 9, 10, 5, 8, 4, 2), strict=True)) % 11
    if kalan == 1:
        raise ValueError("Kalan 1 olduğunda geçerli işletme kimliği üretilemez")
    return govde + "-" + str(0 if kalan == 0 else 11 - kalan)


def hetu_uret(tarih="010101", yuzyil="-", seri=10):
    """Vero mod-31 hesabı; seri alt sınırı için Statistics Finland 002-899.

    https://stat.fi/meta/kas/hetu.html
    """
    govde = tarih + f"{seri:03d}"
    return tarih + yuzyil + f"{seri:03d}" + HETU_HARFLERI[int(govde) % 31]


def nir_uret(govde="1841276451089", *, bosluk=False):
    # Korsika: 2A -> 19, 2B -> 18, yalnızca kontrol hesabında.
    sayisal = govde.replace("2A", "19").replace("2B", "18")
    anahtar = f"{97 - int(sayisal) % 97:02d}"
    if bosluk:
        return " ".join((govde[0], govde[1:3], govde[3:5], govde[5:7], govde[7:10], govde[10:13], anahtar))
    return govde + anahtar


def inn_uret(govde="783000229"):
    """MediaScout WebAPI 09.06.2023, §4.1 (s.10-11): INN katsayıları.

    https://www.mediascout.ru/for_docs/WebAPI_ORD_09062023.pdf
    Her kontrol, ağırlıklı toplamın önce mod-11 sonra mod-10 sonucudur.
    """
    def kontrol(metin, agirliklar):
        return str(sum(int(c) * w for c, w in zip(metin, agirliklar, strict=True)) % 11 % 10)
    if len(govde) == 9:
        return govde + kontrol(govde, (2, 4, 10, 3, 5, 9, 4, 6, 8))
    if len(govde) != 10:
        raise ValueError("INN gövdesi 9 veya 10 basamak olmalıdır")
    ilk = govde + kontrol(govde, (7, 2, 4, 10, 3, 5, 9, 4, 6, 8))
    return ilk + kontrol(ilk, (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8))


def son_basamak_boz(metin):
    return metin[:-1] + str((int(metin[-1]) + 1) % 10)


def ornekleri_dogrula():
    """Yayımlanmış sabit örneklerle üretici hesaplarını çapraz kontrol eder."""
    assert nif_uret("26643189") == "26643189N"
    assert nie_uret("X", "0095892") == "X0095892M"
    assert cif_uret() == "B25162520"
    assert isletme_uret() == "0112038-9"
    assert hetu_uret() == "010101-0101"
    assert nir_uret(bosluk=True) == "1 84 12 76 451 089 46"
    assert inn_uret() == "7830002293"
    assert inn_uret("5001007322") == "500100732259"


if __name__ == "__main__":
    ornekleri_dogrula()
    print("Üreticiler docstring ve bilinen örneklerle uyumlu.")
