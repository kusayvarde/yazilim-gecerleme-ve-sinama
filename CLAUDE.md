# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A university assignment: **black-box** unit tests (Equivalence Partitioning, Boundary Value Analysis, decision table) for the `validators` (pyvalidators) library. A 4-person team, where each person owns a folder under `tests/`. `tests/network_crypto/` covers 15 functions: ipv4, ipv6, cron, btc/eth/trx/bsc addresses, mac_address, uuid and 6 hashes. The plan and the required tables and diagrams are in the PDF in the repo root (`Kara-Kutu Birim Testi Rehberi – …pdf`). The code, identifiers and docs are in Turkish.

**Black-box rule (graded):** never read the `validators` source code, whether in `.venv` or on GitHub. To analyze a failing test, call the function and read its published docstring (`validators.<fn>.__doc__`). Check test data against the standards (Base58Check, EIP-55, BIP-173, RFCs, Unix cron).

## Commands

The project uses `uv` and Python 3.14. `validators==0.36.0` is pinned with the `crypto-eth-addresses` extra, which `eth_address` needs. Results depend on the library version.

```bash
uv sync
uv run pytest                                   # all tests → reports/sonuc.xml + reports/rapor.html
uv run pytest tests/network_crypto/test_ipv4.py # one file
uv run pytest -k "TC-IPV4-BVA-03"               # one test case, by Test ID
uv run python scripts/sonuc_tablosu.py          # sonuc.xml + docs/tablolar → reports/tablolar.xlsx (T1–T6 sheets) + T4/T5 CSV
uv run python scripts/sonuc_grafigi.py          # T5 → reports/D5_sonuc_grafigi.png (run after sonuc_tablosu.py)
```

The `-v`, JUnit XML and HTML report options are set in `addopts` in `pyproject.toml`. Console output with Turkish characters needs `PYTHONIOENCODING=utf-8` on this machine (cp1256 codepage).

## Architecture

The whole pipeline is built around one rule: **one test case = one `pytest.param`, and its ID is the Test ID** in the format `TC-<FONK>-<EP|BVA|DT>-<no>`. The same ID appears in the report tables.

- `tests/yardimci.py`: `tc(test_id, girdi, beklenen, sinif, *, bug=None, **parametreler)` builds the param `(girdi, parametreler, beklenen)` and attaches a `tc(sinif=...)` mark. `V`/`I` mean expected-valid/expected-invalid. Passing `bug="BUG-xx: …"` adds a strict `xfail`. The module also has standards-based test-data generators (`base58check`, `trx_adresi`, `eip55`, `karakter_degistir`) that do not depend on the library.
- `conftest.py` (root): the `dogrula(fonksiyon_adi, girdi, parametreler, beklenen)` fixture calls `getattr(validators, fonksiyon_adi)`. It writes test_id, input, params, technique (taken from the ID), class, expected and actual into `user_properties`. It then asserts according to the library's contract: valid → `sonuc is True`; invalid → `not sonuc` **and** `isinstance(sonuc, ValidationError)`. The library returns a falsy `ValidationError` and does not raise, so never use `pytest.raises`.
- Every test file follows the same pattern: lists of `tc(...)` (EP / BVA / DT), then `@pytest.mark.parametrize("girdi, parametreler, beklenen", ...)` and a one-line test that calls `dogrula`. `test_hashes.py` instead generates its cases for the 6 hash functions from a shared scenario list, with the function name as an extra leading param.
- `junit_family = "xunit1"` is required. It makes the per-test properties land in `reports/sonuc.xml`. The "Gerçekleşen" (actual) and "Durum" (status) columns are never filled by hand.
- `scripts/sonuc_tablosu.py` builds `reports/tablolar.xlsx`. T2 (one row per EP class), T3 (one row per boundary) and T4a/T4b are derived from the test properties. T3 groups BVA tests by parsing the class label with the pattern `<boundary name> SD-1|SD|SD+1 [(value)]` (`N-1|N|N+1` for hashes), so new BVA labels must follow it. T1 and T6 are read from `docs/tablolar/`.
- T1 has one row per requirement (`REQ-<FONK>-<no>`, or `REQ-HASH-…` for all 6 hashes). Its last column lists the covering tests in short form (`EP-01, BVA-01..03`, expanded with the function's prefix). The script exits with code 1 if a listed ID doesn't exist or a test isn't linked to any requirement. When adding a test, add its ID to the matching T1 row.

## Conventions

- A failing test is never deleted. If the test data is correct according to the docs or standards, mark it with `bug="BUG-xx: …"` (strict xfail) and add a row to `docs/tablolar/T6_bulgular.csv`. If the test itself is wrong, fix the expectation.
- Separate invalid classes are not merged; each gets its own test. Every boundary gets SD−1 / SD / SD+1 (boundary − 1, boundary, boundary + 1).
- All CSVs (hand-written and generated) use UTF-8 with BOM (`utf-8-sig`) and the `;` delimiter so Turkish Excel opens them correctly. Keep that format when editing T1/T6, because `sonuc_tablosu.py` reads them that way.
- Two-sided ranges get six BVA tests (min−1, min, min+1, max−1, max, max+1). Every docstring example has its own test (class "Doküman örneği").
- Hand-written tables (T1 requirements, T6 findings) live in `docs/tablolar/`, diagrams in `docs/diyagramlar/`. `reports/` is generated output and is git-ignored.
- A new team member's folder goes under `tests/<area>/` and uses the same `tc` + `dogrula` pattern.
