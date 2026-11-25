"""fr_department için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-FR_DEPARTMENT-EP-01', 20, I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_DEPARTMENT-EP-02', '20', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_DEPARTMENT-EP-03', '971', V, 'Doküman örneği (geçerli)'),
    tc('TC-FR_DEPARTMENT-EP-04', '00', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_DEPARTMENT-EP-05', '2A', V, 'Doküman örneği (geçerli)'),
    tc('TC-FR_DEPARTMENT-EP-06', '2B', V, 'Doküman örneği (geçerli)'),
    tc('TC-FR_DEPARTMENT-EP-07', '2C', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FR_DEPARTMENT-EP-08', '75', V, 'V8 metropol'),
    tc('TC-FR_DEPARTMENT-EP-09', 75, V, 'V9 tamsayı metropol'),
    tc('TC-FR_DEPARTMENT-EP-10', '976', V, 'V10 Mayotte'),
    tc('TC-FR_DEPARTMENT-EP-11', '', I, 'I11 boş girdi'),
    tc('TC-FR_DEPARTMENT-EP-12', '2a', I, 'I12 küçük harf resmi kod değil'),
    tc('TC-FR_DEPARTMENT-BVA-01', '00', I, 'Metropol 1 SD-1 (0)'),
    tc('TC-FR_DEPARTMENT-BVA-02', '01', V, 'Metropol 1 SD (1)'),
    tc('TC-FR_DEPARTMENT-BVA-03', '02', V, 'Metropol 1 SD+1 (2)'),
    tc('TC-FR_DEPARTMENT-BVA-04', '94', V, 'Metropol 95 SD-1 (94)'),
    tc('TC-FR_DEPARTMENT-BVA-05', '95', V, 'Metropol 95 SD (95)'),
    tc('TC-FR_DEPARTMENT-BVA-06', '96', I, 'Metropol 95 SD+1 (96)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_fr_department(dogrula, girdi, parametreler, beklenen):
    dogrula("fr_department", girdi, parametreler, beklenen)
