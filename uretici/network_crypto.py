"""network_crypto alanı için standartlardan türetilen üreticiler: TRON adresi ve EIP-55.

validators içe aktarılmaz (kara-kutu ilkesi).
"""

from Crypto.Hash import keccak

from uretici.ortak import base58check


def trx_adresi(govde: bytes) -> str:
    """TRON adresi: 0x41 sürüm baytı + 20 bayt + checksum -> 'T' ile başlayan 34 karakter."""
    assert len(govde) == 20
    return base58check(b"\x41" + govde)


def eip55(adres: str) -> str:
    """Adresin EIP-55 checksum'lı halini döndürür."""
    hex_kisim = adres.lower().removeprefix("0x")
    ozet = keccak.new(digest_bits=256, data=hex_kisim.encode()).hexdigest()
    return "0x" + "".join(
        c.upper() if c.isalpha() and int(ozet[i], 16) >= 8 else c
        for i, c in enumerate(hex_kisim)
    )


def ornekleri_dogrula():
    """Üreticileri standarttaki örneklerle karşılaştırır."""
    # EIP-55 belgesindeki örnek adres
    assert eip55("0x5aaeb6053f3e94c9b9a09f33669435e7ef1beaed") == "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"
    assert trx_adresi(bytes(20)).startswith("T") and len(trx_adresi(bytes(20))) == 34
    print("Üreticiler standart örnekleriyle uyumlu.")


if __name__ == "__main__":
    ornekleri_dogrula()
