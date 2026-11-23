"""Tüm ekip için ortak pytest ayarları.

`dogrula` fixture'ı her testte:
  1. fonksiyonu çağırır,
  2. girdi / beklenen / gerçekleşen bilgisini JUnit XML'e property olarak yazar
     (scripts/sonuc_tablosu.py bunlardan T4 ve T5 tablolarını üretir),
  3. kütüphanenin sözleşmesine göre doğrular:
       geçerli   -> sonuc is True
       geçersiz  -> not sonuc  ve  isinstance(sonuc, ValidationError)
"""

import pytest
import validators
from validators import ValidationError


def _teknik(test_id):
    for teknik in ("EP", "BVA", "DT"):
        if f"-{teknik}-" in test_id:
            return teknik
    return "?"


def _gorunum(sonuc):
    if sonuc is True:
        return "True"
    if isinstance(sonuc, ValidationError):
        return "ValidationError"
    return f"{type(sonuc).__name__}: {sonuc!r}"


@pytest.fixture
def dogrula(request):
    def _dogrula(fonksiyon_adi, girdi, parametreler, beklenen):
        test_id = request.node.callspec.id
        isaret = request.node.get_closest_marker("tc")
        kayit = request.node.user_properties
        kayit += [
            ("test_id", test_id),
            ("fonksiyon", fonksiyon_adi),
            ("girdi", repr(girdi)),
            ("parametreler", ", ".join(f"{k}={v}" for k, v in parametreler.items()) or "—"),
            ("teknik", _teknik(test_id)),
            ("sinif", isaret.kwargs.get("sinif", "") if isaret else ""),
            ("beklenen", "True" if beklenen else "ValidationError"),
        ]
        try:
            sonuc = getattr(validators, fonksiyon_adi)(girdi, **parametreler)
        except Exception as hata:
            kayit.append(("gerceklesen", f"EXCEPTION {type(hata).__name__}: {hata}"))
            raise
        kayit.append(("gerceklesen", _gorunum(sonuc)))

        if beklenen:
            assert sonuc is True, f"Geçerli girdi reddedildi: {sonuc!r}"
        else:
            assert not sonuc, f"Geçersiz girdi kabul edildi: {sonuc!r}"
            assert isinstance(sonuc, ValidationError), f"Dönüş tipi yanlış: {type(sonuc)}"

    return _dogrula
