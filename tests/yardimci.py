"""Ekip ortak yardımcıları: test senaryosu tanımı + standartlara göre test verisi üretimi.

Bu modül validators'ın kaynak koduna bakılarak değil, yalnızca standartlara
(Base58Check, EIP-55) göre yazılmıştır (kara-kutu ilkesi).
"""

import hashlib

import pytest
from Crypto.Hash import keccak

V = True    # beklenen: geçerli  -> sonuc is True
I = False   # beklenen: geçersiz -> ValidationError (falsy)


def tc(test_id, girdi, beklenen, sinif, *, bug=None, **parametreler):
    """Tek test senaryosu = tek pytest.param. ID, T4 tablosundaki Test ID ile aynıdır.

    bug: Başarısız test bir bulguysa "BUG-xx: açıklama" verilir; test silinmez,
    strict xfail olarak işaretlenir ve raporda görünür.
    """
    marks = [pytest.mark.tc(sinif=sinif)]
    if bug:
        marks.append(pytest.mark.xfail(reason=bug, strict=True))
    return pytest.param(girdi, parametreler, beklenen, id=test_id, marks=marks)


def karakter_degistir(metin, indeks, yeni):
    return metin[:indeks] + yeni + metin[indeks + 1:]


# --- Base58Check (Bitcoin / TRON) -------------------------------------------
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


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


def trx_adresi(govde: bytes) -> str:
    """TRON adresi: 0x41 sürüm baytı + 20 bayt + checksum -> 'T' ile başlayan 34 karakter."""
    assert len(govde) == 20
    return base58check(b"\x41" + govde)


# --- EIP-55 (Ethereum checksum) ---------------------------------------------
def eip55(adres: str) -> str:
    """Adresin EIP-55 checksum'lı halini döndürür."""
    hex_kisim = adres.lower().removeprefix("0x")
    ozet = keccak.new(digest_bits=256, data=hex_kisim.encode()).hexdigest()
    return "0x" + "".join(
        c.upper() if c.isalpha() and int(ozet[i], 16) >= 8 else c
        for i, c in enumerate(hex_kisim)
    )
