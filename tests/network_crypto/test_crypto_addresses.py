"""btc_address, eth_address, trx_address (zor, 3'er puan) ve bsc_address (kolay, 1 puan).

Test verileri standartlara göre üretildi/doğrulandı: Base58Check (BTC/TRX),
BIP-173 bech32 örnekleri (SegWit), EIP-55 (ETH). Bkz. uretici/network_crypto.py.
"""

import pytest

from tests.yardimci import I, V, tc
from uretici.network_crypto import eip55, trx_adresi
from uretici.ortak import karakter_degistir

# --------------------------------------------------------------------------- BTC
BTC_P2SH = "3Cwgr2g7vsi1bXDUkpEnVoRLA9w4FZfC69"           # doküman örneği
BTC_P2PKH = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"          # bilinen geçerli legacy adres
BTC_SEGWIT = "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"
BTC_TESTNET = "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"  # BIP-173 test vektörü

BTC = [
    tc("TC-BTC-EP-01", BTC_P2SH, V, "V1 legacy P2SH (3...)"),
    tc("TC-BTC-EP-02", BTC_P2PKH, V, "V2 legacy P2PKH (1...)"),
    tc("TC-BTC-EP-03", BTC_SEGWIT, V, "V3 SegWit mainnet (bc1...)"),
    tc("TC-BTC-EP-04", BTC_TESTNET, V, "V4 SegWit testnet (tb1...)"),
    tc("TC-BTC-EP-05", BTC_P2SH[:-1] + "8", I, "I1 checksum bozuk (son harf)"),
    tc("TC-BTC-EP-06", karakter_degistir(BTC_P2SH, 10, "0"), I, "I2a Base58 dışı '0'"),
    tc("TC-BTC-EP-07", karakter_degistir(BTC_P2SH, 10, "O"), I, "I2b Base58 dışı 'O'"),
    tc("TC-BTC-EP-08", karakter_degistir(BTC_P2SH, 10, "I"), I, "I2c Base58 dışı 'I'"),
    tc("TC-BTC-EP-09", karakter_degistir(BTC_P2SH, 10, "l"), I, "I2d Base58 dışı 'l'"),
    tc("TC-BTC-EP-10", karakter_degistir(BTC_SEGWIT, 10, "b"), I, "I3 SegWit veri kısmında 'b'"),
    tc("TC-BTC-EP-11", "4" + BTC_P2SH[1:], I, "I4 yanlış önek (4...)"),
    tc("TC-BTC-EP-12", "bx" + BTC_SEGWIT[2:], I, "I5 yanlış SegWit HRP (bx1...)"),
    tc("TC-BTC-EP-13", "", I, "I6 boş string"),
    tc("TC-BTC-EP-14", "1BvBMsEYstWetqTFn5Au4m4GFg7xJaNVN2", I,
       "Doküman örneği (geçersiz; EP-02'deki adresin tek harfi küçük)"),
    # SegWit veri kısmı uzunluğu (14-74). Doküman: "SegWit için regexp ile makul
    # tahmin" -> checksum'sız dizeler biçim (regex) kuralını sınar.
    tc("TC-BTC-BVA-01", "bc1" + "q" * 13, I, "SegWit veri alt SD-1 (13)"),
    tc("TC-BTC-BVA-02", "bc1" + "q" * 14, V, "SegWit veri alt SD (14)"),
    tc("TC-BTC-BVA-05", "bc1" + "q" * 15, V, "SegWit veri alt SD+1 (15)"),
    tc("TC-BTC-BVA-06", "bc1" + "q" * 73, V, "SegWit veri üst SD-1 (73)"),
    tc("TC-BTC-BVA-03", "bc1" + "q" * 74, V, "SegWit veri üst SD (74)"),
    tc("TC-BTC-BVA-04", "bc1" + "q" * 75, I, "SegWit veri üst SD+1 (75)"),
]

# --------------------------------------------------------------------------- ETH
ETH_KUCUK = "0x9cc14ba4f9f68ca159ea4ebf2c292a808aaeb598"   # doküman örneği
ETH_EIP55 = "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"   # EIP-55 resmi test vektörü
ETH_DOKUMAN_KARISIK = "0x8Ba1f109551bD432803012645Ac136ddd64DBa72"

ETH = [
    tc("TC-ETH-EP-01", ETH_KUCUK, V, "V1 tümü küçük harf"),
    tc("TC-ETH-EP-02", "0x" + ETH_KUCUK[2:].upper(), V, "V2 tümü büyük harf"),
    tc("TC-ETH-EP-03", ETH_EIP55, V, "V3 doğru EIP-55 checksum"),
    tc("TC-ETH-EP-04", eip55(ETH_KUCUK), V, "V4 doğru EIP-55 (doküman adresinden üretildi)"),
    tc("TC-ETH-EP-05", "0x5aaeb6053F3E94C9b9A09f33669435E7Ef1BeAed", I, "I1 bozuk checksum (bir harf küçültüldü)"),
    tc("TC-ETH-EP-06", ETH_DOKUMAN_KARISIK, I, "I1b checksum'ı EIP-55'e uymayan karışık adres"),
    tc("TC-ETH-EP-07", ETH_KUCUK[2:], I, "I2 0x öneki yok"),
    tc("TC-ETH-EP-08", karakter_degistir(ETH_KUCUK, 3, "g"), I, "I3 hex olmayan karakter"),
    tc("TC-ETH-EP-09", "0X" + ETH_KUCUK[2:], I, "I4 büyük 0X öneki"),
    tc("TC-ETH-EP-10", "", I, "I5 boş string"),
    tc("TC-ETH-BVA-01", "0x" + "a" * 39, I, "Hex uzunluğu SD-1 (39)"),
    tc("TC-ETH-BVA-02", "0x" + "a" * 40, V, "Hex uzunluğu SD (40)"),
    tc("TC-ETH-BVA-03", "0x" + "a" * 41, I, "Hex uzunluğu SD+1 (41)"),
]

# --------------------------------------------------------------------------- TRX
TRX_DOKUMAN = "TLjfbTbpZYDQ4EoA4N5CLNgGjfbF8ZWz38"
TRX_USDT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
TRX_URETILEN = trx_adresi(bytes(range(20)))

TRX = [
    tc("TC-TRX-EP-01", TRX_DOKUMAN, V, "V1 geçerli (doküman)"),
    tc("TC-TRX-EP-02", TRX_USDT, V, "V2 geçerli (bilinen adres)"),
    tc("TC-TRX-EP-03", TRX_URETILEN, V, "V3 geçerli (Base58Check ile üretildi)"),
    tc("TC-TRX-EP-04", "A" + TRX_DOKUMAN[1:], I, "I1 T ile başlamıyor"),
    tc("TC-TRX-EP-05", "t" + TRX_DOKUMAN[1:], I, "I1b küçük t ile başlıyor"),
    tc("TC-TRX-EP-06", karakter_degistir(TRX_DOKUMAN, 10, "0"), I, "I2 Base58 dışı karakter"),
    tc("TC-TRX-EP-07", TRX_DOKUMAN[:-1] + "9", I, "I3 checksum bozuk (son karakter)"),
    tc("TC-TRX-EP-08", BTC_P2PKH, I, "I4 BTC adresi"),
    tc("TC-TRX-EP-09", "", I, "I5 boş string"),
    tc("TC-TRX-EP-10", "TR2G7Rm4vFqF8EpY4U5xdLdQ7XgJ2U8Vd", I, "Doküman örneği (geçersiz, 33 karakter)"),
    tc("TC-TRX-BVA-01", TRX_DOKUMAN[:-1], I, "Uzunluk SD-1 (33)"),
    tc("TC-TRX-BVA-02", TRX_DOKUMAN, V, "Uzunluk SD (34)"),
    tc("TC-TRX-BVA-03", TRX_DOKUMAN + "1", I, "Uzunluk SD+1 (35)"),
]

# --------------------------------------------------------------------------- BSC
BSC_DOKUMAN = "0x4e5acf9684652BEa56F2f01b7101a225Ee33d23f"

BSC = [
    tc("TC-BSC-EP-01", BSC_DOKUMAN, V, "V1 geçerli (karışık harf)"),
    tc("TC-BSC-EP-02", BSC_DOKUMAN.lower(), V, "V2 tümü küçük harf"),
    tc("TC-BSC-EP-03", karakter_degistir(BSC_DOKUMAN, 2, "E"), V,
       "V3 checksum'ı bozuk karışık harf (BSC'de checksum yok, tasarım gereği)"),
    tc("TC-BSC-EP-04", karakter_degistir(BSC_DOKUMAN, 3, "g"), I, "I1 hex olmayan"),
    tc("TC-BSC-EP-05", BSC_DOKUMAN[2:], I, "I2 0x öneki yok"),
    tc("TC-BSC-EP-06", "0X" + BSC_DOKUMAN[2:], I, "I3 büyük 0X öneki"),
    tc("TC-BSC-EP-07", "", I, "I4 boş string"),
    tc("TC-BSC-EP-08", "0x4g5acf9684652BEa56F2f01b7101a225Eh33d23z", I, "Doküman örneği (geçersiz)"),
    tc("TC-BSC-BVA-01", "0x" + "a" * 39, I, "Hex uzunluğu SD-1 (39)"),
    tc("TC-BSC-BVA-02", "0x" + "a" * 40, V, "Hex uzunluğu SD (40)"),
    tc("TC-BSC-BVA-03", "0x" + "a" * 41, I, "Hex uzunluğu SD+1 (41)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BTC)
def test_btc_address(dogrula, girdi, parametreler, beklenen):
    dogrula("btc_address", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", ETH)
def test_eth_address(dogrula, girdi, parametreler, beklenen):
    dogrula("eth_address", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", TRX)
def test_trx_address(dogrula, girdi, parametreler, beklenen):
    dogrula("trx_address", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", BSC)
def test_bsc_address(dogrula, girdi, parametreler, beklenen):
    dogrula("bsc_address", girdi, parametreler, beklenen)
