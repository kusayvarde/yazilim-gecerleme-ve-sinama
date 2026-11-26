"""Alanlar arası ortak üreticiler: Base58 / Base58Check ve tek karakter bozma.

validators içe aktarılmaz (kara-kutu ilkesi).
"""

import hashlib

# Bitcoin Base58 alfabesi: 0, O, I ve l yoktur.
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def karakter_degistir(metin, indeks, yeni):
    """Geçerli bir veriden tek kuralı bozan geçersiz veri üretmek için tek karakteri değiştirir."""
    return metin[:indeks] + yeni + metin[indeks + 1:]


def base58check(payload: bytes) -> str:
    """payload + sha256(sha256(payload))[:4], Base58 ile kodlanır."""
    veri = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(veri, "big")
    sonuc = ""
    while n:
        n, kalan = divmod(n, 58)
        sonuc = B58[kalan] + sonuc
    bas_sifir = len(veri) - len(veri.lstrip(b"\0"))
    return "1" * bas_sifir + sonuc
