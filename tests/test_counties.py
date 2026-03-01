"""kenya-counties test suite — zero network calls."""
import pytest
from kenya_counties import (
    COUNTIES, get, by_region, all_regions, total_population, County
)


class TestCountiesConstant:
    def test_exactly_47_counties(self):
        assert len(COUNTIES) == 47

    def test_all_codes_unique(self):
        codes = [c.code for c in COUNTIES]
        assert len(set(codes)) == 47

    def test_codes_range_1_to_47(self):
        codes = sorted(c.code for c in COUNTIES)
        assert codes == list(range(1, 48))

    def test_all_names_unique(self):
        names = [c.name for c in COUNTIES]
        assert len(set(names)) == 47

    def test_nairobi_is_code_47(self):
        nairobi = next(c for c in COUNTIES if c.code == 47)
        assert nairobi.name == "Nairobi"

    def test_mombasa_is_code_1(self):
        assert COUNTIES[0].code == 1
        assert COUNTIES[0].name == "Mombasa"

    def test_all_populations_positive(self):
        for c in COUNTIES:
            assert c.population > 0, f"{c.name} has non-positive population"

    def test_all_areas_positive(self):
        for c in COUNTIES:
            assert c.area_km2 > 0, f"{c.name} has non-positive area"

    def test_total_population_matches_2019_census(self):
        # 2019 census total: ~47.6M
        total = total_population()
        assert 47_000_000 < total < 50_000_000, f"Total {total:,} outside expected range"

    def test_nairobi_highest_density(self):
        densities = {c.name: c.population_density for c in COUNTIES}
        assert densities["Nairobi"] == max(densities.values())

    def test_turkana_largest_area(self):
        areas = {c.name: c.area_km2 for c in COUNTIES}
        assert areas["Turkana"] == max(areas.values())

    def test_mombasa_smallest_area(self):
        areas = {c.name: c.area_km2 for c in COUNTIES}
        assert areas["Mombasa"] == min(areas.values())


class TestGet:
    def test_lookup_by_name(self):
        c = get("Nairobi")
        assert c.code == 47

    def test_lookup_case_insensitive(self):
        assert get("nairobi").code == get("NAIROBI").code == get("Nairobi").code

    def test_lookup_by_code(self):
        c = get(47)
        assert c.name == "Nairobi"

    def test_lookup_by_code_1(self):
        c = get(1)
        assert c.name == "Mombasa"

    def test_lookup_multiword_county(self):
        c = get("Tana River")
        assert c.code == 4

    def test_lookup_multiword_case_insensitive(self):
        c = get("tana river")
        assert c.code == 4

    def test_lookup_invalid_name_raises(self):
        with pytest.raises(KeyError):
            get("Atlantis")

    def test_lookup_invalid_code_raises(self):
        with pytest.raises(KeyError):
            get(0)

    def test_lookup_code_48_raises(self):
        with pytest.raises(KeyError):
            get(48)

    def test_lookup_slug(self):
        # slugs are lowercase-hyphenated
        c = get("tana-river")
        assert c.code == 4

    def test_all_counties_retrievable_by_name(self):
        for c in COUNTIES:
            found = get(c.name)
            assert found.code == c.code

    def test_all_counties_retrievable_by_code(self):
        for c in COUNTIES:
            found = get(c.code)
            assert found.name == c.name


class TestByRegion:
    def test_rift_valley_is_largest_region(self):
        rv = by_region("Rift Valley")
        assert len(rv) == 14

    def test_nairobi_region_has_one_county(self):
        nb = by_region("Nairobi")
        assert len(nb) == 1
        assert nb[0].name == "Nairobi"

    def test_coast_has_six_counties(self):
        coast = by_region("Coast")
        assert len(coast) == 6

    def test_case_insensitive(self):
        r1 = by_region("coast")
        r2 = by_region("Coast")
        assert set(c.code for c in r1) == set(c.code for c in r2)

    def test_invalid_region_raises(self):
        with pytest.raises(KeyError):
            by_region("Westeros")

    def test_all_regions_sum_to_47(self):
        total = sum(len(by_region(r)) for r in all_regions())
        assert total == 47


class TestCountyProperties:
    def test_slug_lowercase_hyphenated(self):
        c = get("Tana River")
        assert c.slug == "tana-river"

    def test_slug_nairobi(self):
        assert get("Nairobi").slug == "nairobi"

    def test_population_density_calculation(self):
        nairobi = get("Nairobi")
        expected = round(nairobi.population / nairobi.area_km2, 1)
        assert nairobi.population_density == expected

    def test_str_representation(self):
        c = get("Nairobi")
        assert "Nairobi" in str(c)
        assert "47" in str(c)
