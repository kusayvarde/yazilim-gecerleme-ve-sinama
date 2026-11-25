"""fi_business_id için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-FI_BUSINESS_ID-EP-01', '0112038-9', V, 'Doküman örneği (geçerli)'),
    tc('TC-FI_BUSINESS_ID-EP-02', '1234567-8', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FI_BUSINESS_ID-EP-03', '1234567-1', V, 'V3 ağırlıklı mod-11 üretimi'),
    tc('TC-FI_BUSINESS_ID-EP-04', '7654321-2', V, 'V4 ağırlıklı mod-11 üretimi'),
    tc('TC-FI_BUSINESS_ID-EP-05', '', I, 'I5 boş girdi'),
    tc('TC-FI_BUSINESS_ID-EP-06', '01120389', I, 'I6 tire yok'),
    tc('TC-FI_BUSINESS_ID-EP-07', '0112038 9', I, 'I7 tire yerine boşluk'),
    tc('TC-FI_BUSINESS_ID-EP-08', 'A112038-9', I, 'I8 gövde harf içeriyor'),
    tc('TC-FI_BUSINESS_ID-EP-09', '0112038-A', I, 'I9 kontrol harfi'),
    tc('TC-FI_BUSINESS_ID-EP-10', '0112038-0', I, 'I10 yanlış kontrol basamağı'),
    tc('TC-FI_BUSINESS_ID-EP-11', '1000002-0', V, 'V11 mod-11 kalan 0'),
    tc('TC-FI_BUSINESS_ID-EP-12', '1000008-0', I, 'I12 mod-11 kalan 1'),
    tc('TC-FI_BUSINESS_ID-BVA-01', '0112038-', I, 'Biçim uzunluğu SD-1 (8)'),
    tc('TC-FI_BUSINESS_ID-BVA-02', '0112038-9', V, 'Biçim uzunluğu SD (9)'),
    tc('TC-FI_BUSINESS_ID-BVA-03', '0112038-90', I, 'Biçim uzunluğu SD+1 (10)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_fi_business_id(dogrula, girdi, parametreler, beklenen):
    dogrula("fi_business_id", girdi, parametreler, beklenen)
