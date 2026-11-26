"""payments_finance alanı için standartlardan türetilen test verisi üreticileri.

validators içe aktarılmaz ve kaynak kodu kullanılmaz (kara-kutu ilkesi).
Kaynaklar ve kapsam sınırlamaları docs/rapor_payments_finance.md içindedir.
Üretilen numaralar yalnızca biçim/kontrol basamağı örnekleridir; gerçek kart veya
menkul kıymet kaydı değildir.
"""

# --- Luhn (ISO/IEC 7812-1 Ek B) ----------------------------------------------


def luhn_toplam(rakamlar: str) -> int:
    """Sağdan başlayarak her ikinci basamak iki katına çıkarılır (9'dan büyükse 9 çıkarılır)."""
    toplam = 0
    for i, c in enumerate(reversed(rakamlar)):
        d = int(c)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        toplam += d
    return toplam


def luhn_gecerli(rakamlar: str) -> bool:
    return rakamlar.isdigit() and luhn_toplam(rakamlar) % 10 == 0


def luhn_tamamla(govde: str) -> str:
    """Gövdeye Luhn kontrol basamağını ekler."""
    for k in "0123456789":
        if luhn_gecerli(govde + k):
            return govde + k
    raise AssertionError("ulaşılamaz")


def kart_uret(onek: str, uzunluk: int) -> str:
    """Önekle başlayan, istenen uzunlukta, Luhn'u doğru numara (dolgu: 0)."""
    govde = onek + "0" * (uzunluk - len(onek) - 1)
    return luhn_tamamla(govde)


def luhn_boz(numara: str) -> str:
    """Yalnızca son (kontrol) basamağı değiştirir: önek ve uzunluk korunur."""
    son = str((int(numara[-1]) + 1) % 10)
    sonuc = numara[:-1] + son
    assert not luhn_gecerli(sonuc)
    return sonuc


# --- CUSIP (ANSI X9.6; CUSIP Global Services) ---------------------------------


def _cusip_deger(c: str) -> int:
    if c.isdigit():
        return int(c)
    if "A" <= c <= "Z":
        return ord(c) - ord("A") + 10
    return {"*": 36, "@": 37, "#": 38}[c]


def cusip_kontrol(govde8: str) -> str:
    """Çift konumlardaki (1 tabanlı) değer iki katına çıkar; basamak toplamlarının mod-10 tümleyeni."""
    assert len(govde8) == 8
    toplam = 0
    for i, c in enumerate(govde8):
        v = _cusip_deger(c)
        if i % 2 == 1:
            v *= 2
        toplam += v // 10 + v % 10
    return str((10 - toplam % 10) % 10)


def cusip_uret(govde8: str) -> str:
    return govde8 + cusip_kontrol(govde8)


# --- ISIN (ISO 6166) -----------------------------------------------------------


def isin_kontrol(govde11: str) -> str:
    """Harfler A=10…Z=35 ile sayıya çevrilir, ortaya çıkan rakam dizisine Luhn uygulanır."""
    assert len(govde11) == 11
    rakamlar = "".join(str(int(c, 36)) for c in govde11)
    return luhn_tamamla(rakamlar)[-1]


def isin_uret(govde11: str) -> str:
    return govde11 + isin_kontrol(govde11)


# --- SEDOL (London Stock Exchange) ----------------------------------------------

SEDOL_AGIRLIK = (1, 3, 1, 7, 3, 9)


def sedol_kontrol(govde6: str) -> str:
    """Ağırlıklar 1,3,1,7,3,9; harf değeri A=10…Z=35; kontrol = (10 - toplam mod 10) mod 10."""
    assert len(govde6) == 6
    toplam = sum(int(c, 36) * w for c, w in zip(govde6, SEDOL_AGIRLIK, strict=True))
    return str((10 - toplam % 10) % 10)


def sedol_uret(govde6: str) -> str:
    return govde6 + sedol_kontrol(govde6)


# --- Çapraz doğrulama ------------------------------------------------------------


def ornekleri_dogrula():
    """Üreticileri docstring ve kamuya açık bilinen örneklerle karşılaştırır."""
    # Docstring örnekleri
    assert cusip_uret("037833DP") == "037833DP2"
    assert sedol_uret("293692") == "2936921"
    for kart in ("4242424242424242", "5555555555554444", "378282246310005",
                 "6011111111111117", "3056930009020004", "3566002020360505",
                 "6200000000000005", "2200123456789019"):
        assert luhn_gecerli(kart), kart
    assert not luhn_gecerli("4242424242424241")
    # Kamuya açık bilinen örnekler (Apple, BAE Systems)
    assert cusip_uret("03783310") == "037833100"
    assert isin_uret("US037833100") == "US0378331005"
    assert sedol_uret("026349") == "0263494"
    assert sedol_uret("B0YBKJ") == "B0YBKJ7"
    print("Üreticiler docstring ve bilinen örneklerle uyumlu.")


if __name__ == "__main__":
    ornekleri_dogrula()
