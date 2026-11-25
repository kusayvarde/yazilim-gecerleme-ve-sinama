"""fr_ssn için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-FR_SSN-EP-01', '1 84 12 76 451 089 46', V, 'Doküman örneği (geçerli)'),
    tc('TC-FR_SSN-EP-02', '1 84 12 76 451 089', V, 'Doküman örneği (geçerli)'),
    tc('TC-FR_SSN-EP-03', '3 84 12 76 451 089 46', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_SSN-EP-04', '1 84 12 76 451 089 47', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_SSN-EP-05', '2 84 12 76 451 089 93', V, 'V5 kadın'),
    tc('TC-FR_SSN-EP-06', '1 84 12 2A 451 089 33', V, 'V6 Korsika 2A'),
    tc('TC-FR_SSN-EP-07', '1 84 12 2B 451 089 60', V, 'V7 Korsika 2B'),
    tc('TC-FR_SSN-EP-08', '184127645108946', V, 'V8 boşluksuz sayısal NIR', bug='BUG-61: Boşluksuz 13/15 karakterli NIR reddediliyor; aynı veri docstring biçiminde boşluklarla kabul ediliyor. Resmi NIR sayısal gösterimi destekler; ancak docstring yalnızca boşluklu örnek verir. Bu nedenle biçim gereksinimi belirsizliği olarak sınıflandırılmıştır.'),
    tc('TC-FR_SSN-EP-09', '', I, 'I9 boş girdi'),
    tc('TC-FR_SSN-EP-10', '1 84 12 76 451 089 47', I, 'I10 kabul edilen boşluklu biçimde yalnızca mod-97 anahtarı yanlış'),
    tc('TC-FR_SSN-EP-11', '1 84 12 76 45A 089 46', I, 'I11 komün kodunda harf'),
    tc('TC-FR_SSN-BVA-01', '1 84 00 76 451 089 48', I, 'Ay 1 SD-1 (0)'),
    tc('TC-FR_SSN-BVA-02', '1 84 01 76 451 089 64', V, 'Ay 1 SD (1)'),
    tc('TC-FR_SSN-BVA-03', '1 84 02 76 451 089 80', V, 'Ay 1 SD+1 (2)'),
    tc('TC-FR_SSN-BVA-04', '1 84 11 76 451 089 30', V, 'Ay 12 SD-1 (11)'),
    tc('TC-FR_SSN-BVA-05', '1 84 12 76 451 089 46', V, 'Ay 12 SD (12)'),
    tc('TC-FR_SSN-BVA-06', '1 84 13 76 451 089 62', I, 'Ay 12 SD+1 (13)'),
    tc('TC-FR_SSN-BVA-07', '184127645108', I, 'Boşluksuz uzunluk 13 SD-1 (12)'),
    tc('TC-FR_SSN-BVA-08', '1841276451089', V, 'Boşluksuz uzunluk 13 SD (13)', bug='BUG-61: Boşluksuz 13/15 karakterli NIR reddediliyor; aynı veri docstring biçiminde boşluklarla kabul ediliyor. Resmi NIR sayısal gösterimi destekler; ancak docstring yalnızca boşluklu örnek verir. Bu nedenle biçim gereksinimi belirsizliği olarak sınıflandırılmıştır.'),
    tc('TC-FR_SSN-BVA-09', '18412764510894', I, 'Boşluksuz uzunluk 13 SD+1 (14)'),
    tc('TC-FR_SSN-BVA-10', '18412764510894', I, 'Boşluksuz uzunluk 15 SD-1 (14)'),
    tc('TC-FR_SSN-BVA-11', '184127645108946', V, 'Boşluksuz uzunluk 15 SD (15)', bug='BUG-61: Boşluksuz 13/15 karakterli NIR reddediliyor; aynı veri docstring biçiminde boşluklarla kabul ediliyor. Resmi NIR sayısal gösterimi destekler; ancak docstring yalnızca boşluklu örnek verir. Bu nedenle biçim gereksinimi belirsizliği olarak sınıflandırılmıştır.'),
    tc('TC-FR_SSN-BVA-12', '1841276451089460', I, 'Boşluksuz uzunluk 15 SD+1 (16)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_fr_ssn(dogrula, girdi, parametreler, beklenen):
    dogrula("fr_ssn", girdi, parametreler, beklenen)
