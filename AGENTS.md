# AGENTS.md

Instructions for any AI coding agent (Claude Code, Codex, Cursor, Copilot, Gemini, …) working in this
repository. Human teammates: read this too, it is the team's rulebook.

## What this is

A university assignment (Yazılım Geçerleme ve Sınama): **black-box** unit tests for the Python
`validators` (pyvalidators) library, using Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
and decision tables (DT). A 4-person team; **each person owns one area folder** under `tests/<area>/`
and writes one section of a shared report. The sections are merged into one report and one
presentation at the end.

The plan and the required tables (T1–T6) and diagrams (D1–D5) are in the PDF in the repo root
(`Kara-Kutu Birim Testi Rehberi – …pdf`); each teammate may have their own guide PDF for their area.
Code identifiers, table contents and the report are in **Turkish**; keep new work in Turkish too.

| # | Area folder (`<area>`) | Owner (GitHub) | Very hard (5) | Hard (3) | Medium (2) | Easy (1) | Points |
|---|---|---|---|---|---|---|---|
| 1 | `network_crypto` (15 functions) | kusayvarde | ipv4, ipv6 | cron, btc_address, eth_address, trx_address | – | bsc_address, mac_address, uuid, md5, sha1, sha224, sha256, sha384, sha512 | 31 |
| 2 | `domains_formats` (15 functions) | AFAHMAD1 | domain, hostname | country_code, currency, iban | between, length, calling_code | slug, base16, base32, base58, base64, ind_aadhar, ind_pan | 32 |
| 3 | `payments_finance` (13 functions) | KhaledZer | email | cusip, isin, sedol | card_number, visa, mastercard, amex, discover, diners, jcb, unionpay, mir | – | 32 |
| 4 | `urls_national_ids` (10 functions) | MMHDJ | url | es_nif, es_nie, es_cif, es_doi, fi_business_id, fi_ssn, fr_ssn, ru_inn | fr_department | – | 31 |

Area 1 is **done — use `tests/network_crypto/` and its tables/report as the reference example.**
Your branch is named after your GitHub username (e.g. `AFAHMAD1`); your files use your area name
(e.g. `tests/domains_formats/`, `docs/tablolar/T1_domains_formats.csv`, `docs/rapor_domains_formats.md`).

Note: `between` and `length` take keyword-only `min_val` / `max_val` arguments — pass them as keyword
parameters in `tc(...)` (e.g. `tc(..., min_val=1, max_val=5)`). Check each function's docstring and
`inspect.signature(validators.<fn>)` (public signature, allowed) for its exact parameters.

## Hard rules (graded or team-breaking)

1. **Black-box: never read the `validators` source code** — not in `.venv/`, not in site-packages,
   not on GitHub, not via `inspect.getsource`. To learn what a function should do, use only its
   published docs and docstring (`python -c "import validators; print(validators.<fn>.__doc__)"`)
   and the relevant standard (RFCs, ISO, Luhn, IBAN, …). To analyse a failing test, call the function
   and compare with the docstring/standard. The report must state that the source was not consulted.
2. **Stay in your own area.** Only create or edit files in your own `tests/<area>/`,
   `docs/tablolar/T1_<area>.csv`, `docs/tablolar/T6_<area>.csv`, `docs/rapor_<area>.md` and your own
   diagrams. The **shared files** below are changed only after telling the team (they affect
   everyone's results): `conftest.py`, `tests/yardimci.py`, `scripts/*`, `pyproject.toml`, `uv.lock`,
   `AGENTS.md`, `CLAUDE.md`, `README.md`.
3. **Never delete or weaken a failing test.** Decide: is the test wrong, or the library?
   - Test data/expectation wrong according to docs/standard → fix the test.
   - Test is correct but the library disagrees → it is a **finding**: add `bug="BUG-xx: …"` to the
     `tc(...)` (becomes a strict xfail) and add a row to your `T6_<area>.csv`.
4. **Never use `pytest.raises`.** The library does not raise on invalid input; it returns a falsy
   `ValidationError`. The shared `dogrula` fixture already asserts the contract.
5. **Never fill "Gerçekleşen" (actual) or "Durum" (status) by hand** — they are generated from pytest.
6. **Do not commit `reports/`** (generated, git-ignored), `.venv/`, or secrets.
7. **Do not push to `master` or `dev` directly** — see the Git workflow below.

## Commands

Uses `uv` and Python 3.14. `validators==0.36.0` is pinned (with the `crypto-eth-addresses` extra);
results depend on this version, so do not upgrade it.

```bash
uv sync                                         # install the exact locked environment
uv run pytest                                   # ALL areas → reports/sonuc.xml + reports/rapor.html
uv run pytest tests/<area>                      # only your area
uv run pytest -k "TC-IPV4-BVA-03"               # one test case, by Test ID
uv run python scripts/sonuc_tablosu.py          # → reports/tablolar.xlsx (T1–T6) + traceability check
uv run python scripts/sonuc_grafigi.py          # → reports/D5_sonuc_grafigi.png (after sonuc_tablosu.py)
uv run python scripts/diyagramlar.py            # network_crypto D1/D3/D4 diagrams
```

`-v`, JUnit XML and HTML report options are in `addopts` in `pyproject.toml`. On Windows consoles
with Turkish characters, prefix commands with `PYTHONIOENCODING=utf-8`.
Need a new dependency? Use `uv add …` (never hand-edit `uv.lock`) and tell the team.

## How a test is written

**One test case = one `pytest.param`, and its ID is the Test ID** `TC-<FONK>-<EP|BVA|DT>-<no>`
(e.g. `TC-EMAIL-BVA-03`). The same ID appears in the code, pytest output, HTML report and all tables.
`<FONK>` is the function name in upper case; function names never overlap between areas, so IDs are
unique across the team.

```python
"""validators.email - zor (3 puan). EP + BVA."""
import pytest
from tests.yardimci import I, V, tc

EP = [
    tc("TC-EMAIL-EP-01", "ali@ornek.com", V, "V1 standart adres"),
    tc("TC-EMAIL-EP-02", "aliornek.com", I, "I1 @ yok"),
]
BVA = [
    tc("TC-EMAIL-BVA-01", "a" * 63 + "@x.com", V, "Yerel kısım uzunluğu SD-1 (63)"),
    tc("TC-EMAIL-BVA-02", "a" * 64 + "@x.com", V, "Yerel kısım uzunluğu SD (64)"),
    tc("TC-EMAIL-BVA-03", "a" * 65 + "@x.com", I, "Yerel kısım uzunluğu SD+1 (65)"),
]

@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA)
def test_email(dogrula, girdi, parametreler, beklenen):
    dogrula("email", girdi, parametreler, beklenen)
```

(The values above only illustrate the pattern; derive real rules from the docstring and standard.)

- `tc(test_id, girdi, beklenen, sinif, *, bug=None, **parametreler)` in `tests/yardimci.py`.
  `V` = expected valid (`True`), `I` = expected invalid (`ValidationError`). Keyword arguments are
  passed to the validator (e.g. `strict=True`).
- `dogrula` (root `conftest.py`) calls `getattr(validators, name)`, records input/expected/actual into
  the JUnit XML (`junit_family = "xunit1"` is required for this) and asserts.
- See `tests/network_crypto/` for complete examples, including a decision table (`test_ipv4.py`) and
  one scenario list multiplied over several functions (`test_hashes.py`).

### Test-design conventions

- **Class labels** (`sinif`): `V1, V2, …` for valid classes, `I1, I2, …` for invalid ones, then a
  short description. Docstring examples use the label `"Doküman örneği (geçerli)"` /
  `"Doküman örneği (geçersiz)"`; **every docstring example gets its own test**.
- **Invalid classes are never merged** — one rule broken per test (avoids masking).
- **Every boundary gets SD−1 / SD / SD+1.** A two-sided range gets six tests
  (min−1, min, min+1, max−1, max, max+1).
- **BVA label format is parsed by the table script** — it must be
  `<boundary name> SD-1|SD|SD+1 [(value)]`, e.g. `"Dakika üst SD+1 (60)"`. Other formats break T3.
- Valid test data must be checked against the standard, independently of the library (write a small
  generator in your own test file, or propose one for `tests/yardimci.py`).
- Spread effort by difficulty/points: very hard ≈ 20–30 tests, hard ≈ 12–18, easy ≈ 6–10.

## Tables and traceability

Hand-written tables, **one file per area** (the script merges all of them, so teammates never edit
the same file):

- `docs/tablolar/T1_<area>.csv` — requirements, one row per rule. Header (must be identical):
  `ID;Fonksiyon;Gereksinim;Örnek girdi;Beklenen çıktı;Kaynak;Sınayan testler`.
  ID = `REQ-<FONK>-<no>`. The last column lists covering tests in short form
  (`EP-01, EP-03, BVA-01..03`), expanded with the function prefix.
- `docs/tablolar/T6_<area>.csv` — findings. Header:
  `Bulgu ID;Test ID;Girdi;Beklenen;Gerçekleşen;Kök neden yorumu;Önem`.
- **Bug ID ranges** (so IDs never collide): network_crypto `BUG-01…19`, teammate 2 `BUG-20…39`,
  teammate 3 `BUG-40…59`, teammate 4 `BUG-60…79`. Non-bug observations: `GÖZLEM-<no>` in the same ranges.
- Format: **UTF-8 with BOM (`utf-8-sig`), `;` delimiter** (Turkish Excel). Keep it when editing.
- `scripts/sonuc_tablosu.py` **exits with code 1** if a T1 row lists a non-existent test or any test
  is not linked to a requirement. **Whenever you add a test, add its ID to the matching T1 row.**
- T2, T3, T4a/T4b and T5 are generated from the tests — never written by hand.

## Report

Each person writes `docs/rapor_<area>.md` following the 10-section outline in the PDF (Kapsam,
Yöntem, Gereksinimler, Eşdeğerlik sınıfları, Sınır değer analizi, Test senaryoları, Otomasyon,
Sonuçlar, Bulgular, Değerlendirme). `docs/rapor_network_crypto.md` is the reference example.
Diagrams go in `docs/diyagramlar/`.

## Git workflow

```
master  ← final, submitted version (merged from dev only, by the repo owner)
  └─ dev  ← integration branch: everyone's work meets here
       ├─ <name>   (e.g. ahmet)  ← one branch per teammate, created FROM dev
       ├─ <name>
       └─ <name>
```

1. Start: `git fetch origin && git switch -c <name> origin/dev`.
2. Work and commit on your branch only. Small, clear commits; never commit `reports/`.
3. Before opening a PR, bring in teammates' work and check everything still passes:
   ```bash
   git fetch origin && git merge origin/dev
   uv run pytest && uv run python scripts/sonuc_tablosu.py   # both must succeed (exit 0)
   ```
4. Push your branch and open a **Pull Request `<name>` → `dev`**. Another teammate reviews it.
5. When all four areas are in `dev` and the full pipeline is green, the owner opens a PR
   **`dev` → `master`**. That is the final version for submission.

Merge conflicts should be rare because areas and table files are separate. If one happens in a
shared file, keep both sides' intent and re-run the full pipeline; for `uv.lock`, take `dev`'s
version and run `uv lock`.
