"""ru_inn için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-RU_INN-EP-01', '500100732259', V, 'Doküman örneği (geçerli)'),
    tc('TC-RU_INN-EP-02', '7830002293', V, 'Doküman örneği (geçerli)'),
    tc('TC-RU_INN-EP-03', '1234567890', I, 'Doküman örneği (geçersiz)'),
    tc('TC-RU_INN-EP-04', '7707083893', V, 'V4 bağımsız ağırlıklı mod-11/mod-10'),
    tc('TC-RU_INN-EP-05', '500100732259', V, 'V5 bağımsız ağırlıklı mod-11/mod-10'),
    tc('TC-RU_INN-EP-06', '', I, 'I6 boş girdi'),
    tc('TC-RU_INN-EP-07', '783000229A', I, 'I7 harf içeriyor'),
    tc('TC-RU_INN-EP-08', '78300 2293', I, 'I8 boşluk içeriyor'),
    tc('TC-RU_INN-EP-09', '7830002294', I, 'I9 10. kontrol basamağı yanlış'),
    tc('TC-RU_INN-EP-10', '500100732250', I, 'I10 12. kontrol basamağı yanlış'),
    tc('TC-RU_INN-EP-11', '500100732266', I, 'I11 11. basamak yanlış; 12. basamak yeniden hesaplandı', bug='BUG-62: 12 haneli INN için 11. kontrol basamağı bozulup 12. basamak yeniden hesaplandığında veri kabul ediliyor. Docstring iki kontrol basamağını da denetlemeyi taahhüt eder. Bu tek bir kontrol kuralını ihlal eden sentetik örnektir; iç neden kanıtlanmamıştır.'),
    tc('TC-RU_INN-BVA-01', '777777777', I, 'Uzunluk 10 SD-1 (9)'),
    tc('TC-RU_INN-BVA-02', '7830002293', V, 'Uzunluk 10 SD (10)'),
    tc('TC-RU_INN-BVA-03', '77777777777', I, 'Uzunluk 10 SD+1 (11)'),
    tc('TC-RU_INN-BVA-04', '77777777777', I, 'Uzunluk 12 SD-1 (11)'),
    tc('TC-RU_INN-BVA-05', '500100732259', V, 'Uzunluk 12 SD (12)'),
    tc('TC-RU_INN-BVA-06', '7777777777777', I, 'Uzunluk 12 SD+1 (13)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_ru_inn(dogrula, girdi, parametreler, beklenen):
    dogrula("ru_inn", girdi, parametreler, beklenen)
