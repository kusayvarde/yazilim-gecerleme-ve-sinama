"""Standartlardan türetilen test verisi üreticileri (kara-kutu ilkesi).

Bu paketteki hiçbir modül `validators` içe aktarmaz ve kaynak koduna bakılarak yazılmamıştır;
geçerli/geçersiz test verisi yalnızca ilgili standarda göre üretilir.

  ortak.py              alanlar arası: Base58 alfabesi, Base58Check, karakter_degistir
  network_crypto.py     TRON adresi (Base58Check), EIP-55
  domains_formats.py    IBAN (ISO 13616 mod-97), Aadhaar (Verhoeff)
  urls_national_ids.py  NIF/NIE/CIF, Fin işletme kimliği, HETU, NIR, INN
  payments_finance.py   Luhn / kart numarası, CUSIP, ISIN, SEDOL

Her alan modülü `ornekleri_dogrula()` ile docstring ve kamuya açık örneklerle çapraz denetlenebilir:
    uv run python -m uretici.<alan>
"""
