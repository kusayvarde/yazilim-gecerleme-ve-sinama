"""card_number, visa, mastercard, amex, discover, diners, jcb, unionpay, mir - orta (2'şer puan).
EP + BVA.

Beklentiler docstring'den, ISO/IEC 7812-1 (PAN en çok 19 basamak, Luhn kontrolü) ve
kart ağlarının kamuya açık IIN aralıklarından türetilmiştir (rapordaki kaynak listesi):
  Visa 4 (13/16/19) · Mastercard 51-55, 2221-2720 (16) · Amex 34, 37 (15)
  Discover 6011, 622126-622925, 644-649, 65 (16-19) · Diners 300-305, 36, 38-39 (14-19)
  JCB 3528-3589 (16-19) · UnionPay 62 (16-19) · Mir 2200-2204 (16-19)
Her geçersiz test tek kuralı bozar: önek dışı testlerde Luhn yeniden hesaplanır, Luhn
testinde önek ve uzunluk korunur. Veriler uretici/payments_finance.py ile bağımsız üretilir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from uretici.payments_finance import kart_uret as k
from uretici.payments_finance import luhn_boz
from tests.yardimci import I, V, tc

# ============================================================ card_number
CARD_NUMBER = [
    tc("TC-CARD_NUMBER-EP-01", "4242424242424242", V, "Doküman örneği (geçerli)"),
    tc("TC-CARD_NUMBER-EP-02", "4242424242424241", I, "Doküman örneği (geçersiz)"),
    tc("TC-CARD_NUMBER-EP-03", "378282246310005", V, "V1 15 haneli (marka bağımsız)"),
    tc("TC-CARD_NUMBER-EP-04", k("9", 16), V, "V2 ağ dışı önek, Luhn doğru (genel doğrulayıcı)"),
    tc("TC-CARD_NUMBER-EP-05", "4242a42424242424", I, "I1 rakam dışı karakter"),
    tc("TC-CARD_NUMBER-EP-06", "", I, "I2 boş girdi"),
    tc("TC-CARD_NUMBER-BVA-01", k("4", 18), V, "PAN üst uzunluk SD-1 (18)"),
    tc("TC-CARD_NUMBER-BVA-02", k("4", 19), V, "PAN üst uzunluk SD (19)"),
    tc("TC-CARD_NUMBER-BVA-03", k("4", 20), I, "PAN üst uzunluk SD+1 (20)",
       bug="BUG-43: uzunluk denetlenmiyor; ISO/IEC 7812 PAN en çok 19 basamak"),
]

# ================================================================== visa
VISA = [
    tc("TC-VISA-EP-01", "4242424242424242", V, "Doküman örneği (geçerli)"),
    tc("TC-VISA-EP-02", "2223003122003222", I, "Doküman örneği (geçersiz)"),
    tc("TC-VISA-EP-03", k("4", 13), V, "V1 13 haneli Visa",
       bug="BUG-44: yalnızca 16 haneli Visa kabul ediliyor; 13 ve 19 hane reddediliyor"),
    tc("TC-VISA-EP-04", k("4", 19), V, "V2 19 haneli Visa",
       bug="BUG-44: yalnızca 16 haneli Visa kabul ediliyor; 13 ve 19 hane reddediliyor"),
    tc("TC-VISA-EP-05", luhn_boz(k("4", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-VISA-BVA-01", k("3", 16), I, "Önek SD-1 (3)"),
    tc("TC-VISA-BVA-02", k("4", 16), V, "Önek SD (4)"),
    tc("TC-VISA-BVA-03", k("5", 16), I, "Önek SD+1 (5)"),
    tc("TC-VISA-BVA-04", k("4", 15), I, "Uzunluk 16 SD-1 (15)"),
    tc("TC-VISA-BVA-05", k("4", 16), V, "Uzunluk 16 SD (16)"),
    tc("TC-VISA-BVA-06", k("4", 17), I, "Uzunluk 16 SD+1 (17)"),
]

# ============================================================ mastercard
MASTERCARD = [
    tc("TC-MASTERCARD-EP-01", "5555555555554444", V, "Doküman örneği (geçerli)"),
    tc("TC-MASTERCARD-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-MASTERCARD-EP-03", k("51", 16), V, "V1 51 öneki"),
    tc("TC-MASTERCARD-EP-04", k("55", 16), V, "V2 55 öneki"),
    tc("TC-MASTERCARD-EP-05", luhn_boz(k("51", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-MASTERCARD-EP-06", k("56", 16), I, "I2 51-55 dışı önek (56)"),
    tc("TC-MASTERCARD-BVA-01", k("2220", 16), I, "2-serisi alt SD-1 (2220)"),
    tc("TC-MASTERCARD-BVA-02", k("2221", 16), V, "2-serisi alt SD (2221)"),
    tc("TC-MASTERCARD-BVA-03", k("2222", 16), V, "2-serisi alt SD+1 (2222)"),
    tc("TC-MASTERCARD-BVA-04", k("2719", 16), V, "2-serisi üst SD-1 (2719)"),
    tc("TC-MASTERCARD-BVA-05", k("2720", 16), V, "2-serisi üst SD (2720)"),
    tc("TC-MASTERCARD-BVA-06", k("2721", 16), I, "2-serisi üst SD+1 (2721)"),
    tc("TC-MASTERCARD-BVA-07", k("51", 15), I, "Uzunluk 16 SD-1 (15)"),
    tc("TC-MASTERCARD-BVA-08", k("51", 16), V, "Uzunluk 16 SD (16)"),
    tc("TC-MASTERCARD-BVA-09", k("51", 17), I, "Uzunluk 16 SD+1 (17)"),
]

# ================================================================== amex
AMEX = [
    tc("TC-AMEX-EP-01", "378282246310005", V, "Doküman örneği (geçerli)"),
    tc("TC-AMEX-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-AMEX-EP-03", k("34", 15), V, "V1 34 öneki"),
    tc("TC-AMEX-EP-04", k("37", 15), V, "V2 37 öneki"),
    tc("TC-AMEX-EP-05", luhn_boz(k("37", 15)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-AMEX-BVA-01", k("33", 15), I, "Önek 34 SD-1 (33)"),
    tc("TC-AMEX-BVA-02", k("34", 15), V, "Önek 34 SD (34)"),
    tc("TC-AMEX-BVA-03", k("35", 15), I, "Önek 34 SD+1 (35)"),
    tc("TC-AMEX-BVA-04", k("36", 15), I, "Önek 37 SD-1 (36)"),
    tc("TC-AMEX-BVA-05", k("37", 15), V, "Önek 37 SD (37)"),
    tc("TC-AMEX-BVA-06", k("38", 15), I, "Önek 37 SD+1 (38)"),
    tc("TC-AMEX-BVA-07", k("37", 14), I, "Uzunluk 15 SD-1 (14)"),
    tc("TC-AMEX-BVA-08", k("37", 15), V, "Uzunluk 15 SD (15)"),
    tc("TC-AMEX-BVA-09", k("37", 16), I, "Uzunluk 15 SD+1 (16)"),
]

# ============================================================== discover
DISCOVER = [
    tc("TC-DISCOVER-EP-01", "6011111111111117", V, "Doküman örneği (geçerli)"),
    tc("TC-DISCOVER-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-DISCOVER-EP-03", k("65", 16), V, "V1 65 öneki"),
    tc("TC-DISCOVER-EP-04", k("622126", 16), V, "V2 622126-622925 ortak markalı aralık",
       bug="BUG-47: Discover/UnionPay ortak aralığı 622126-622925 Discover olarak reddediliyor"),
    tc("TC-DISCOVER-EP-05", luhn_boz(k("6011", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-DISCOVER-EP-06", k("6012", 16), I, "I2 6011 dışı 601x öneki (6012)",
       bug="BUG-46: Discover önek denetimi geniş; 6012 ve 643 gibi Discover dışı önekler kabul ediliyor"),
    tc("TC-DISCOVER-BVA-01", k("643", 16), I, "644-649 alt SD-1 (643)",
       bug="BUG-46: Discover önek denetimi geniş; 6012 ve 643 gibi Discover dışı önekler kabul ediliyor"),
    tc("TC-DISCOVER-BVA-02", k("644", 16), V, "644-649 alt SD (644)"),
    tc("TC-DISCOVER-BVA-03", k("645", 16), V, "644-649 alt SD+1 (645)"),
    tc("TC-DISCOVER-BVA-04", k("6011", 15), I, "Uzunluk alt SD-1 (15)"),
    tc("TC-DISCOVER-BVA-05", k("6011", 16), V, "Uzunluk alt SD (16)"),
    tc("TC-DISCOVER-BVA-06", k("6011", 17), V, "Uzunluk alt SD+1 (17)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
    tc("TC-DISCOVER-BVA-07", k("6011", 18), V, "Uzunluk üst SD-1 (18)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
    tc("TC-DISCOVER-BVA-08", k("6011", 19), V, "Uzunluk üst SD (19)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
    tc("TC-DISCOVER-BVA-09", k("6011", 20), I, "Uzunluk üst SD+1 (20)"),
]

# ================================================================ diners
DINERS = [
    tc("TC-DINERS-EP-01", "3056930009020004", V, "Doküman örneği (geçerli)"),
    tc("TC-DINERS-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-DINERS-EP-03", k("36", 14), V, "V1 36 öneki, 14 hane (klasik)"),
    tc("TC-DINERS-EP-04", k("38", 16), V, "V2 38 öneki, 16 hane"),
    tc("TC-DINERS-EP-05", luhn_boz(k("36", 14)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-DINERS-EP-06", k("37", 14), I, "I2 Amex öneki 37"),
    tc("TC-DINERS-BVA-01", k("299", 14), I, "300-305 alt SD-1 (299)"),
    tc("TC-DINERS-BVA-02", k("300", 14), V, "300-305 alt SD (300)"),
    tc("TC-DINERS-BVA-03", k("301", 14), V, "300-305 alt SD+1 (301)"),
    tc("TC-DINERS-BVA-04", k("304", 14), V, "300-305 üst SD-1 (304)"),
    tc("TC-DINERS-BVA-05", k("305", 14), V, "300-305 üst SD (305)"),
    tc("TC-DINERS-BVA-06", k("306", 14), I, "300-305 üst SD+1 (306)",
       bug="BUG-48: Diners 300-305 aralığı dışındaki 306 kabul ediliyor"),
    tc("TC-DINERS-BVA-07", k("36", 13), I, "Uzunluk alt SD-1 (13)"),
    tc("TC-DINERS-BVA-08", k("36", 14), V, "Uzunluk alt SD (14)"),
    tc("TC-DINERS-BVA-09", k("36", 15), V, "Uzunluk alt SD+1 (15)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
]

# =================================================================== jcb
JCB = [
    tc("TC-JCB-EP-01", "3566002020360505", V, "Doküman örneği (geçerli)"),
    tc("TC-JCB-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-JCB-EP-03", k("3530", 19), V, "V1 19 haneli JCB",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
    tc("TC-JCB-EP-04", luhn_boz(k("3530", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-JCB-BVA-01", k("3527", 16), I, "3528-3589 alt SD-1 (3527)",
       bug="BUG-49: JCB 3528-3589 dışındaki 35xx önekleri (3527, 3590) kabul ediliyor"),
    tc("TC-JCB-BVA-02", k("3528", 16), V, "3528-3589 alt SD (3528)"),
    tc("TC-JCB-BVA-03", k("3529", 16), V, "3528-3589 alt SD+1 (3529)"),
    tc("TC-JCB-BVA-04", k("3588", 16), V, "3528-3589 üst SD-1 (3588)"),
    tc("TC-JCB-BVA-05", k("3589", 16), V, "3528-3589 üst SD (3589)"),
    tc("TC-JCB-BVA-06", k("3590", 16), I, "3528-3589 üst SD+1 (3590)",
       bug="BUG-49: JCB 3528-3589 dışındaki 35xx önekleri (3527, 3590) kabul ediliyor"),
    tc("TC-JCB-BVA-07", k("3530", 15), I, "Uzunluk alt SD-1 (15)"),
    tc("TC-JCB-BVA-08", k("3530", 16), V, "Uzunluk alt SD (16)"),
    tc("TC-JCB-BVA-09", k("3530", 17), V, "Uzunluk alt SD+1 (17)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
]

# ============================================================== unionpay
UNIONPAY = [
    tc("TC-UNIONPAY-EP-01", "6200000000000005", V, "Doküman örneği (geçerli)"),
    tc("TC-UNIONPAY-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-UNIONPAY-EP-03", k("62", 19), V, "V1 19 haneli UnionPay",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
    tc("TC-UNIONPAY-EP-04", luhn_boz(k("62", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-UNIONPAY-BVA-01", k("61", 16), I, "Önek SD-1 (61)"),
    tc("TC-UNIONPAY-BVA-02", k("62", 16), V, "Önek SD (62)"),
    tc("TC-UNIONPAY-BVA-03", k("63", 16), I, "Önek SD+1 (63)"),
    tc("TC-UNIONPAY-BVA-04", k("62", 15), I, "Uzunluk alt SD-1 (15)"),
    tc("TC-UNIONPAY-BVA-05", k("62", 16), V, "Uzunluk alt SD (16)"),
    tc("TC-UNIONPAY-BVA-06", k("62", 17), V, "Uzunluk alt SD+1 (17)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
]

# =================================================================== mir
MIR = [
    tc("TC-MIR-EP-01", "2200123456789019", V, "Doküman örneği (geçerli)"),
    tc("TC-MIR-EP-02", "4242424242424242", I, "Doküman örneği (geçersiz)"),
    tc("TC-MIR-EP-03", luhn_boz(k("2200", 16)), I, "I1 Luhn kontrolü yanlış"),
    tc("TC-MIR-BVA-01", k("2199", 16), I, "2200-2204 alt SD-1 (2199)"),
    tc("TC-MIR-BVA-02", k("2200", 16), V, "2200-2204 alt SD (2200)"),
    tc("TC-MIR-BVA-03", k("2201", 16), V, "2200-2204 alt SD+1 (2201)"),
    tc("TC-MIR-BVA-04", k("2203", 16), V, "2200-2204 üst SD-1 (2203)"),
    tc("TC-MIR-BVA-05", k("2204", 16), V, "2200-2204 üst SD (2204)"),
    tc("TC-MIR-BVA-06", k("2205", 16), I, "2200-2204 üst SD+1 (2205)"),
    tc("TC-MIR-BVA-07", k("2200", 15), I, "Uzunluk alt SD-1 (15)"),
    tc("TC-MIR-BVA-08", k("2200", 16), V, "Uzunluk alt SD (16)"),
    tc("TC-MIR-BVA-09", k("2200", 17), V, "Uzunluk alt SD+1 (17)",
       bug="BUG-45: 16-19 hane aralığındaki kartlarda yalnızca 16 (Diners 14/16) kabul ediliyor"),
]


def _test(fonksiyon):
    def _f(dogrula, girdi, parametreler, beklenen):
        dogrula(fonksiyon, girdi, parametreler, beklenen)
    return _f


_P = "girdi, parametreler, beklenen"
test_card_number = pytest.mark.parametrize(_P, CARD_NUMBER)(_test("card_number"))
test_visa = pytest.mark.parametrize(_P, VISA)(_test("visa"))
test_mastercard = pytest.mark.parametrize(_P, MASTERCARD)(_test("mastercard"))
test_amex = pytest.mark.parametrize(_P, AMEX)(_test("amex"))
test_discover = pytest.mark.parametrize(_P, DISCOVER)(_test("discover"))
test_diners = pytest.mark.parametrize(_P, DINERS)(_test("diners"))
test_jcb = pytest.mark.parametrize(_P, JCB)(_test("jcb"))
test_unionpay = pytest.mark.parametrize(_P, UNIONPAY)(_test("unionpay"))
test_mir = pytest.mark.parametrize(_P, MIR)(_test("mir"))
