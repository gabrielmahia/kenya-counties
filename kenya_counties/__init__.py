"""
Kenya counties reference data — 47 counties, 2019 KNBS census.

Sources:
  Population: Kenya National Bureau of Statistics, 2019 Kenya Population and Housing Census
  Area: Kenya National Bureau of Statistics
  Codes: IEBC county codes (1-47)
  Capitals: County government offices
  Regions: Kenya National Census administrative regions
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator

@dataclass(frozen=True)
class County:
    """A Kenyan county."""
    code: int           # IEBC code 1–47
    name: str           # Official name
    capital: str        # County headquarters
    region: str         # Census administrative region
    population: int     # 2019 KNBS census
    area_km2: float     # Area in square kilometres

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-").replace("'", "")

    @property
    def population_density(self) -> float:
        return round(self.population / self.area_km2, 1) if self.area_km2 else 0.0

    def __str__(self) -> str:
        return f"{self.name} (County {self.code})"


# Population: 2019 KNBS Kenya Population and Housing Census, Volume I
# Area: KNBS Statistical Abstract 2021
_RAW: list[tuple] = [
    # code, name, capital, region, population, area_km2
    (1,  "Mombasa",         "Mombasa",        "Coast",         1208333,    212.5),
    (2,  "Kwale",           "Kwale",          "Coast",          866820,   8270.2),
    (3,  "Kilifi",          "Kilifi",         "Coast",         1453787,  12245.9),
    (4,  "Tana River",      "Hola",           "Coast",          315943,  35375.8),
    (5,  "Lamu",            "Lamu",           "Coast",          143920,   6497.7),
    (6,  "Taita-Taveta",    "Wundanyi",       "Coast",          340671,  17084.4),
    (7,  "Garissa",         "Garissa",        "North Eastern",  841353,  44175.1),
    (8,  "Wajir",           "Wajir",          "North Eastern",  781263,  56685.6),
    (9,  "Mandera",         "Mandera",        "North Eastern", 1025756,  25797.7),
    (10, "Marsabit",        "Marsabit",       "Eastern",        459785,  66923.1),
    (11, "Isiolo",          "Isiolo",         "Eastern",        268002,  25336.1),
    (12, "Meru",            "Meru",           "Eastern",       1545714,   6936.2),
    (13, "Tharaka-Nithi",   "Chuka",          "Eastern",        393177,   2609.5),
    (14, "Embu",            "Embu",           "Eastern",        608599,   2818.2),
    (15, "Kitui",           "Kitui",          "Eastern",       1136187,  30496.0),
    (16, "Machakos",        "Machakos",       "Eastern",       1421932,   6208.3),
    (17, "Makueni",         "Wote",           "Eastern",        987653,   8008.9),
    (18, "Nyandarua",       "Ol Kalou",       "Central",        638289,   3304.7),
    (19, "Nyeri",           "Nyeri",          "Central",        759164,   3337.3),
    (20, "Kirinyaga",       "Kerugoya",       "Central",        610411,   1478.1),
    (21, "Murang\'a",      "Murang\'a",     "Central",       1056640,   2558.8),
    (22, "Kiambu",          "Kiambu",         "Central",       2417735,   2543.5),
    (23, "Turkana",         "Lodwar",         "Rift Valley",   1155433,  68680.3),
    (24, "West Pokot",      "Kapenguria",     "Rift Valley",    621241,   9169.3),
    (25, "Samburu",         "Maralal",        "Rift Valley",    310327,  20182.5),
    (26, "Trans-Nzoia",     "Kitale",         "Rift Valley",    990341,   2496.0),
    (27, "Uasin Gishu",     "Eldoret",        "Rift Valley",   1163186,   3345.2),
    (28, "Elgeyo-Marakwet", "Iten",           "Rift Valley",    454480,   3024.8),
    (29, "Nandi",           "Kapsabet",       "Rift Valley",    885711,   2884.5),
    (30, "Baringo",         "Kabarnet",       "Rift Valley",    666763,  11015.3),
    (31, "Laikipia",        "Nanyuki",        "Rift Valley",    518560,   9462.5),
    (32, "Nakuru",          "Nakuru",         "Rift Valley",   2162202,   7509.5),
    (33, "Narok",           "Narok",          "Rift Valley",   1157873,  17921.2),
    (34, "Kajiado",         "Kajiado",        "Rift Valley",   1117840,  21292.7),
    (35, "Kericho",         "Kericho",        "Rift Valley",    901777,   2479.0),
    (36, "Bomet",           "Bomet",          "Rift Valley",    857850,   1997.9),
    (37, "Kakamega",        "Kakamega",       "Western",       1867579,   3033.8),
    (38, "Vihiga",          "Vihiga",         "Western",        590013,    563.3),
    (39, "Bungoma",         "Bungoma",        "Western",       1670570,   3032.4),
    (40, "Busia",           "Busia",          "Western",        893681,   1695.0),
    (41, "Siaya",           "Siaya",          "Nyanza",         993183,   2530.5),
    (42, "Kisumu",          "Kisumu",         "Nyanza",        1155574,   2085.9),
    (43, "Homa Bay",        "Homa Bay",       "Nyanza",        1131950,   3183.3),
    (44, "Migori",          "Migori",         "Nyanza",       1116436,   2596.5),
    (45, "Kisii",           "Kisii",          "Nyanza",       1266860,   1317.6),
    (46, "Nyamira",         "Nyamira",        "Nyanza",        605576,   900.3),
    (47, "Nairobi",         "Nairobi",        "Nairobi",      4397073,    696.1),
]

COUNTIES: tuple[County, ...] = tuple(
    County(code=r[0], name=r[1], capital=r[2], region=r[3], population=r[4], area_km2=r[5])
    for r in _RAW
)

_BY_CODE: dict[int, County] = {c.code: c for c in COUNTIES}
_BY_NAME: dict[str, County] = {c.name.lower(): c for c in COUNTIES}
_BY_SLUG: dict[str, County] = {c.slug: c for c in COUNTIES}


def get(name_or_code: str | int) -> County:
    """Look up a county by name (case-insensitive) or IEBC code.

    Examples:
        get("Nairobi")     → County(code=47, name='Nairobi', ...)
        get(47)            → County(code=47, name='Nairobi', ...)
        get("nairobi")     → County(code=47, name='Nairobi', ...)
        get("tana river")  → County(code=4,  name='Tana River', ...)

    Raises:
        KeyError: If county not found.
    """
    if isinstance(name_or_code, int):
        county = _BY_CODE.get(name_or_code)
        if county:
            return county
        raise KeyError(f"No county with code {name_or_code}. Valid codes: 1–47.")
    key = str(name_or_code).lower().strip()
    county = _BY_NAME.get(key) or _BY_SLUG.get(key)
    if county:
        return county
    # Fuzzy: check if key is a prefix of any county name
    matches = [c for c in COUNTIES if c.name.lower().startswith(key)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(c.name for c in matches)
        raise KeyError(f"Ambiguous: {name_or_code!r} matches {names}. Be more specific.")
    raise KeyError(
        f"County not found: {name_or_code!r}. "
        f"Try a full county name (e.g. \'Tana River\') or code (1–47)."
    )


def by_region(region: str) -> tuple[County, ...]:
    """Return all counties in a region (case-insensitive).

    Regions: Coast, North Eastern, Eastern, Central, Rift Valley, Western, Nyanza, Nairobi
    """
    key = region.lower().strip()
    result = tuple(c for c in COUNTIES if c.region.lower() == key)
    if not result:
        available = sorted({c.region for c in COUNTIES})
        raise KeyError(f"Region {region!r} not found. Available: {available}")
    return result


def all_regions() -> tuple[str, ...]:
    """Return all unique region names."""
    return tuple(sorted({c.region for c in COUNTIES}))


def total_population() -> int:
    """Sum of 2019 census population across all 47 counties."""
    return sum(c.population for c in COUNTIES)


def __iter__() -> Iterator[County]:
    return iter(COUNTIES)
