"""domains_formats alanı için standartlara göre test verisi üreticileri.

Bu modül validators'ın kaynak koduna bakılarak değil, yalnızca standartlara
(ISO 13616 IBAN mod-97, Verhoeff algoritması / UIDAI Aadhaar) göre yazılmıştır.
Kütüphaneden bağımsızdır (kara-kutu ilkesi).
"""


# --- IBAN (ISO 13616, mod-97-10) ---------------------------------------------
def iban_uret(ulke: str, bban: str) -> str:
    """Ülke kodu + BBAN için doğru kontrol basamaklarını hesaplayıp IBAN'ı döndürür."""
    yeniden = bban + ulke + "00"
    sayi = int("".join(str(int(c, 36)) for c in yeniden))
    return f"{ulke}{98 - sayi % 97:02d}{bban}"


def iban_mod97_dogru_mu(iban: str) -> bool:
    yeniden = iban[4:] + iban[:4]
    return int("".join(str(int(c, 36)) for c in yeniden)) % 97 == 1


# --- Verhoeff (Aadhaar son basamağı) -----------------------------------------
_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]
_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def verhoeff_kontrol_basamagi(sayi: str) -> str:
    c = 0
    for i, ch in enumerate(reversed(sayi)):
        c = _D[c][_P[(i + 1) % 8][int(ch)]]
    return str(_INV[c])


def verhoeff_dogru_mu(sayi: str) -> bool:
    c = 0
    for i, ch in enumerate(reversed(sayi)):
        c = _D[c][_P[i % 8][int(ch)]]
    return c == 0


def aadhaar_uret(govde: str) -> str:
    """11 basamaklı gövdeye Verhoeff kontrol basamağını ekler -> 12 basamak."""
    assert len(govde) == 11 and govde.isdigit()
    return govde + verhoeff_kontrol_basamagi(govde)


def bosluklu(aadhaar: str) -> str:
    """'123456789012' -> '1234 5678 9012' (Aadhaar'ın basılı gösterimi)."""
    return " ".join(aadhaar[i:i + 4] for i in range(0, 12, 4))


# --- Kendi kendine doğrulama: üreticiler bilinen örneklerle uyuşmalı ----------
assert verhoeff_kontrol_basamagi("236") == "3"            # Verhoeff'in klasik örneği (2363)
assert verhoeff_dogru_mu("2363") and not verhoeff_dogru_mu("2364")
assert iban_uret("DE", "370400440532013000") == "DE89370400440532013000"
assert iban_uret("GB", "WEST12345698765432") == "GB82WEST12345698765432"
assert iban_mod97_dogru_mu("DE89370400440532013000")
