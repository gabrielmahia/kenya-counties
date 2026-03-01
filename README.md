# kenya-counties

**Kenya's 47 counties — codes, capitals, regions, population, area. Zero dependencies.**

[![CI](https://github.com/gabrielmahia/kenya-counties/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielmahia/kenya-counties/actions)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![Tests](https://img.shields.io/badge/tests-36%20passing-brightgreen)](#)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-kenya--counties-orange)](#)

A single-file Python package containing authoritative reference data for all 47 Kenyan counties.
No external dependencies. No API calls. No CSV parsing. Just import and use.

**Data sources:** 2019 Kenya Population and Housing Census (KNBS) · IEBC county codes · KNBS Statistical Abstract 2021

---

## Install

```bash
pip install kenya-counties
```

Or from source:
```bash
pip install git+https://github.com/gabrielmahia/kenya-counties
```

---

## Usage

```python
from kenya_counties import get, by_region, COUNTIES

# Look up by name (case-insensitive)
nairobi = get("Nairobi")
print(nairobi.population)        # 4397073
print(nairobi.area_km2)          # 696.1
print(nairobi.population_density)  # 6317.5 people/km²
print(nairobi.capital)           # "Nairobi"
print(nairobi.region)            # "Nairobi"
print(nairobi.code)              # 47

# Look up by IEBC code
mombasa = get(1)
print(mombasa.name)   # "Mombasa"

# All counties in a region
rift_valley = by_region("Rift Valley")
print(len(rift_valley))   # 14

# Iterate all 47
for county in COUNTIES:
    print(f"{county.code:02d}  {county.name:<20} {county.population:>10,}")
```

---

## County fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | `int` | IEBC county code (1–47) |
| `name` | `str` | Official county name |
| `capital` | `str` | County headquarters |
| `region` | `str` | Census administrative region |
| `population` | `int` | 2019 KNBS census population |
| `area_km2` | `float` | Area in square kilometres |
| `slug` | `str` | URL-safe lowercase name (computed) |
| `population_density` | `float` | People per km² (computed) |

---

## API

```python
get(name_or_code)     # → County  (raises KeyError if not found)
by_region(region)     # → tuple[County, ...]
all_regions()         # → tuple[str, ...]  (8 regions)
total_population()    # → int  (47,564,296 — 2019 census)
COUNTIES              # → tuple[County, ...]  (all 47, ordered by code)
```

---

## Use with OpenResilience

```python
from kenya_counties import get, by_region
from openresilience import water_stress_index

# Drought risk for all Coast counties
for county in by_region("Coast"):
    wsi = water_stress_index(county.code)
    print(f"{county.name}: {wsi:.2f}")
```

---

## Data accuracy

Population and area figures are from the **2019 Kenya Population and Housing Census**, the most recent national census. County boundaries and IEBC codes are as of 2022. The next census is scheduled for 2029.

If you spot an error, open an Issue with your source document.

---

*Maintained by [Gabriel Mahia](https://github.com/gabrielmahia). Kenya × USA.*
