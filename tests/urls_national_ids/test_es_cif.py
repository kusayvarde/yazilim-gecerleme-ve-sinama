"""es_cif için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-ES_CIF-EP-01', 'B25162520', V, 'Doküman örneği (geçerli)'),
    tc('TC-ES_CIF-EP-02', 'B25162529', I, 'Doküman örneği (geçersiz)'),
    tc('TC-ES_CIF-EP-03', '', I, 'I3 boş girdi'),
    tc('TC-ES_CIF-EP-04', 'B251 2520', I, 'I4 gövde içinde boşluk'),
    tc('TC-ES_CIF-EP-05', 'B251#2520', I, 'I5 gövde içinde özel karakter'),
    tc('TC-ES_CIF-EP-06', 'A25162520', V, 'V6 kuruluş türü A'),
    tc('TC-ES_CIF-EP-07', 'P2516252J', V, 'V7 kuruluş türü P'),
    tc('TC-ES_CIF-EP-08', 'N2516252J', V, 'V8 kuruluş türü N'),
    tc('TC-ES_CIF-EP-09', 'Z25162520', I, 'I9 kuruluş türü geçersiz'),
    tc('TC-ES_CIF-EP-10', 'B25162521', I, 'I10 yanlış kontrol rakamı'),
    tc('TC-ES_CIF-BVA-01', 'B2516252', I, 'Biçim uzunluğu SD-1 (8)'),
    tc('TC-ES_CIF-BVA-02', 'B25162520', V, 'Biçim uzunluğu SD (9)'),
    tc('TC-ES_CIF-BVA-03', 'B251625200', I, 'Biçim uzunluğu SD+1 (10)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_es_cif(dogrula, girdi, parametreler, beklenen):
    dogrula("es_cif", girdi, parametreler, beklenen)
